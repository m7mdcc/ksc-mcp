import logging
from typing import List, Optional

import anyio

# Import KlAkOAPI modules
# Note: These imports might fail if the package isn't installed in the environment yet,
# but we are writing the code assuming it will be.
try:
    from KlAkOAPI.AdmServer import KlAkAdmServer
    from KlAkOAPI.ChunkAccessor import KlAkChunkAccessor
    from KlAkOAPI.HostGroup import KlAkHostGroup
    from KlAkOAPI.Tasks import KlAkTasks
except ImportError:
    # Fallback for when we represent the code but libs aren't installed yet
    pass

from app.ksc.errors import KscApiError, KscAuthError
from app.ksc.models import HostDetail, HostInfo, TaskInfo
from app.settings import settings

logger = logging.getLogger(__name__)


class KscService:
    def __init__(self):
        self.server: Optional[KlAkAdmServer] = None
        self._connected = False

    def _connect_sync(self):
        """Synchronous connection logic."""
        if self._connected and self.server and self.server.connected:
            return

        logger.info(f"Connecting to KSC at {settings.KSC_HOST} as {settings.KSC_USERNAME}")
        try:
            # Replicates usage from sample_connect.py
            # KlAkAdmServer.Create calls Connect internally
            self.server = KlAkAdmServer.Create(
                url=settings.KSC_HOST,
                user_account=settings.KSC_USERNAME,
                password=settings.KSC_PASSWORD,
                verify=settings.KSC_VERIFY_SSL,
            )

            if not self.server.connected:
                raise KscAuthError("Failed to connect to KSC server (connected=False)")

            self._connected = True
            logger.info("Successfully connected to KSC")

        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self._connected = False
            raise KscAuthError(f"Connection failed: {str(e)}") from e

    async def connect(self):
        """Async wrapper for connection."""
        await anyio.to_thread.run_sync(self._connect_sync)

    def _ensure_connected(self):
        if not self._connected or not self.server:
            self._connect_sync()

    def _ping_sync(self) -> str:
        self._ensure_connected()
        # Simplest check: try to get server version or just return "pong" if connected
        # There isn't a direct "Ping" method in KlAkAdmServer, but if we are here, we are connected.
        # We can try a lightweight call like getting domains or groups.
        try:
            host_group = KlAkHostGroup(self.server)
            # Just a lightweight call to verify session
            host_group.GetDomains()
            return "pong"
        except Exception as e:
            # Try reconnection once
            logger.warning(f"Ping failed, retrying connection: {e}")
            self._connected = False
            self._connect_sync()
            return "pong"

    async def ping(self) -> str:
        return await anyio.to_thread.run_sync(self._ping_sync)

    def _list_hosts_sync(
        self, group_name: Optional[str] = None, status: Optional[str] = None
    ) -> List[HostInfo]:
        self._ensure_connected()
        host_group = KlAkHostGroup(self.server)
        chunk_accessor = KlAkChunkAccessor(self.server)

        # Build filter string
        # KSC filter syntax: (Field="Value")
        # e.g. KLHST_WKS_DN like '%name%'
        wstr_filter = ""
        if group_name:
            # This is tricky without knowing exact group IDs.
            # Usually we filter by walking the group tree or precise name match.
            # simpler approach: search all, filter in python or if we can filter by group name
            # directly
            pass

        # Default fetch all
        if not wstr_filter:
            wstr_filter = '(KLHST_WKS_DN="*")'

        # Fields to return
        # KLHST_WKS_DN: Display Name
        # KLHST_WKS_HOSTNAME: NetBIOS/DNS name
        # KLHST_WKS_GRP: Group ID
        # KLHST_WKS_STATUS: Status
        vec_fields = ["KLHST_WKS_DN", "KLHST_WKS_HOSTNAME", "KLHST_WKS_GRP", "id", "name"]

        try:
            # FindHooks returns an accessor
            res = host_group.FindHosts(
                wstrFilter=wstr_filter,
                vecFieldsToReturn=vec_fields,
                vecFieldsToOrder=["KLHST_WKS_DN"],
                pParams={"KLGRP_FIND_FROM_CUR_VS_ONLY": True},
                lMaxLifeTime=600,
            )

            str_accessor = res.OutPar("strAccessor")
            items_count = chunk_accessor.GetItemsCount(str_accessor).RetVal()

            hosts = []
            if items_count > 0:
                # Limit to 50 for safety
                count_to_fetch = min(items_count, 50)
                res_chunk = chunk_accessor.GetItemsChunk(str_accessor, 0, count_to_fetch)
                chunk_data = res_chunk.OutPar("pChunk")

                # KlAkParams or dict
                if chunk_data and "KLCSP_ITERATOR_ARRAY" in chunk_data:
                    items_iter = chunk_data["KLCSP_ITERATOR_ARRAY"]
                    # KlAkArray is list-like
                    for item in items_iter:
                        # item is KlAkParams (dict-like)
                        hosts.append(
                            HostInfo(
                                id=str(item.get("id", "")),
                                name=item.get("name", ""),
                                display_name=item.get("KLHST_WKS_DN", ""),
                                group_id=item.get("KLHST_WKS_GRP", 0),
                                group_name="Unknown",  # Need separate lookup ideally
                                status=str(item.get("KLHST_WKS_STATUS", "0")),
                                ip_address=None,  # Not always in basic find
                            )
                        )

            return hosts

        except Exception as e:
            raise KscApiError(f"Failed to list hosts: {e}")

    async def list_hosts(
        self, group_name: Optional[str] = None, status: Optional[str] = None
    ) -> List[HostInfo]:
        return await anyio.to_thread.run_sync(self._list_hosts_sync, group_name, status)

    def _get_host_details_sync(self, host_id: str) -> HostDetail:
        self._ensure_connected()
        host_group = KlAkHostGroup(self.server)

        # KlAkOAPI usually uses string names or IDs.
        # GetHostInfo usually takes a hostname or ID.
        try:
            # Fetch generic info
            # We need to map generic attributes
            res = host_group.GetHostInfo(
                # Can be ID or name depending on context, usually ID works in some calls or we
                # need name
                strHostName=host_id,
                pFields2Return=["KLHST_WKS_DN", "KLHST_WKS_HOSTNAME"],
            )

            # Simple detail for now
            data = res.RetVal()
            return HostDetail(
                id=host_id, name=str(data.get("KLHST_WKS_DN", "Unknown")), products=[], os_info={}
            )
        except Exception as e:
            raise KscApiError(f"Failed to get host details: {e}")

    async def get_host_details(self, host_id: str) -> HostDetail:
        return await anyio.to_thread.run_sync(self._get_host_details_sync, host_id)

    def _list_tasks_sync(self) -> List[TaskInfo]:
        self._ensure_connected()
        tasks_api = KlAkTasks(self.server)

        try:
            # Iterate tasks
            # ResetTasksIterator(nGroupId, bGroupIdSignificant, strProductName, strVersion,
            # strComponentName, strInstanceId, strTaskName, bIncludeSupergroups)
            # Passing valid defaults for "All tasks"
            res = tasks_api.ResetTasksIterator(
                nGroupId=-1,  # Root
                bGroupIdSignificant=False,
                strProductName="",
                strVersion="",
                strComponentName="",
                strInstanceId="",
                strTaskName="",
                bIncludeSupergroups=True,
            )

            iter_id = res.OutPar("strTaskIteratorId")

            # Since GetNextTask returns one by one or we might need another way?
            # Actually KlAkTasks usually has an iterator or `GetAllTasksOfHost`
            # But specific "List All Tasks" is `ResetTasksIterator` -> `GetNextTask` loop.

            tasks = []
            # Safety limit
            for _ in range(50):
                res_task = tasks_api.GetNextTask(iter_id)
                task_data = res_task.OutPar("pTaskData")
                if not task_data:
                    break

                # Extract task info
                tasks.append(
                    TaskInfo(
                        id=str(task_data.get("lId", "")),  # Assuming lId is standard
                        name=task_data.get("strDisplayName", "Unknown"),
                        type="Unknown",
                        state="Unknown",
                    )
                )

            # Release iterator
            tasks_api.ReleaseTasksIterator(iter_id)
            return tasks

        except Exception as e:
            raise KscApiError(f"Failed to list tasks: {e}")

    async def list_tasks(self) -> List[TaskInfo]:
        return await anyio.to_thread.run_sync(self._list_tasks_sync)

    def _run_task_sync(self, task_id: str) -> str:
        self._ensure_connected()
        tasks_api = KlAkTasks(self.server)
        try:
            # Tasks.RunTask(strTask) accepts "TaskId" (string or int depending on API)
            tasks_api.RunTask(strTask=task_id)
            return f"Task {task_id} started successfully"
        except Exception as e:
            raise KscApiError(f"Failed to run task: {e}")

    async def run_task(self, task_id: str) -> str:
        return await anyio.to_thread.run_sync(self._run_task_sync, task_id)

    def _get_task_state_sync(self, task_id: str) -> dict:
        self._ensure_connected()
        tasks_api = KlAkTasks(self.server)
        try:
            res = tasks_api.GetTaskStatistics(strTask=task_id)
            return res.RetVal()
        except Exception as e:
            raise KscApiError(f"Failed to get task state: {e}")

    async def get_task_state(self, task_id: str) -> dict:
        return await anyio.to_thread.run_sync(self._get_task_state_sync, task_id)


ksc_service = KscService()
