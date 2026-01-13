import logging
from typing import List, Optional

import anyio

# Import KlAkOAPI modules
# Import KlAkOAPI modules
from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.ChunkAccessor import KlAkChunkAccessor
from KlAkOAPI.HostGroup import KlAkHostGroup
from KlAkOAPI.Tasks import KlAkTasks
from server.ksc.errors import KscApiError, KscAuthError
from server.models import HostDetail, HostInfo, TaskInfo, TaskRunResult, TaskState
from server.settings import settings

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
        try:
            host_group = KlAkHostGroup(self.server)
            host_group.GetDomains()
            return "pong"
        except Exception as e:
            logger.warning(f"Ping failed, retrying connection: {e}")
            self._connected = False
            self._connect_sync()
            return "pong"

    async def ping(self) -> str:
        return await anyio.to_thread.run_sync(self._ping_sync)

    def _safe_get(self, obj, key, default):
        """Helper to safely get values from KlAkParams objects or dicts."""
        try:
            return obj[key]
        except Exception:
            return default

    def _list_hosts_sync(
        self, group_name: Optional[str] = None, status: Optional[str] = None
    ) -> List[HostInfo]:
        self._ensure_connected()
        host_group = KlAkHostGroup(self.server)
        chunk_accessor = KlAkChunkAccessor(self.server)

        # Build filter string
        wstr_filter = ""
        # Improved filtering logic would go here
        if not wstr_filter:
            wstr_filter = '(KLHST_WKS_DN="*")'

        vec_fields = ["KLHST_WKS_DN", "KLHST_WKS_HOSTNAME", "KLHST_WKS_GRP", "id", "name"]

        try:
            res = host_group.FindHosts(
                wstrFilter=wstr_filter,
                vecFieldsToReturn=vec_fields,
                vecFieldsToOrder=[],
                pParams={"KLGRP_FIND_FROM_CUR_VS_ONLY": True},
                lMaxLifeTime=600,
            )

            str_accessor = res.OutPar("strAccessor")
            items_count = chunk_accessor.GetItemsCount(str_accessor).RetVal()

            hosts = []
            if items_count > 0:
                count_to_fetch = min(items_count, 50)
                res_chunk = chunk_accessor.GetItemsChunk(str_accessor, 0, count_to_fetch)
                chunk_data = res_chunk.OutPar("pChunk")

                if chunk_data and "KLCSP_ITERATOR_ARRAY" in chunk_data:
                    items_iter = chunk_data["KLCSP_ITERATOR_ARRAY"]
                    for item in items_iter:
                        # Use KLHST_WKS_HOSTNAME (Network Name) as the ID for MCP lookups
                        # This typically maps to what GetHostInfo(strHostName=...) expects
                        unique_name = self._safe_get(item, "KLHST_WKS_HOSTNAME", "")
                        if not unique_name:
                             # Fallback to Display Name
                             unique_name = self._safe_get(item, "KLHST_WKS_DN", "")
                        
                        hosts.append(
                            HostInfo(
                                id=str(unique_name),
                                name=str(unique_name),
                                display_name=self._safe_get(item, "KLHST_WKS_DN", "Unknown"),
                                group_id=self._safe_get(item, "KLHST_WKS_GRP", 0),
                                group_name="Unknown",
                                status=str(self._safe_get(item, "KLHST_WKS_STATUS", "0")),
                                ip_address=None,
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

        try:
            res = host_group.GetHostInfo(
                # host_id must be the unique string name (GUID-like) or Network Name
                strHostName=host_id,
                pFields2Return=["KLHST_WKS_DN", "KLHST_WKS_HOSTNAME"],
            )

            data = res.RetVal()
            return HostDetail(
                id=host_id,
                name=str(self._safe_get(data, "KLHST_WKS_DN", "Unknown")),
                products=[],
                os_info={},
            )
        except Exception as e:
            raise KscApiError(f"Failed to get host details: {e}")

    async def get_host_details(self, host_id: str) -> HostDetail:
        return await anyio.to_thread.run_sync(self._get_host_details_sync, host_id)

    def _move_host_sync(self, host_id: str, group_id: int) -> bool:
        self._ensure_connected()
        host_group = KlAkHostGroup(self.server)
        try:
            # MoveHostsToGroup(nGroup, pHostNames) where pHostNames is array of host IDs/names
            host_group.MoveHostsToGroup(nGroup=group_id, pHostNames=[host_id])
            return True
        except Exception as e:
            raise KscApiError(f"Failed to move host: {e}")

    async def move_host(self, host_id: str, group_id: int) -> bool:
        return await anyio.to_thread.run_sync(self._move_host_sync, host_id, group_id)

    def _list_tasks_sync(self) -> List[TaskInfo]:
        self._ensure_connected()
        tasks_api = KlAkTasks(self.server)

        try:
            res = tasks_api.ResetTasksIterator(
                nGroupId=-1,
                bGroupIdSignificant=False,
                strProductName="",
                strVersion="",
                strComponentName="",
                strInstanceId="",
                strTaskName="",
                bIncludeSupergroups=True,
            )

            iter_id = res.OutPar("strTaskIteratorId")
            tasks = []
            for _ in range(50):
                res_task = tasks_api.GetNextTask(iter_id)
                task_data = res_task.OutPar("pTaskData")
                if not task_data:
                    break
                
                # Check potential ID fields
                unique_name = self._safe_get(task_data, "TASK_UNIQUE_ID", "")
                if not unique_name:
                     # Fallback to strName if unique ID is missing (though unlikely given the keys)
                     unique_name = self._safe_get(task_data, "strName", "")

                tasks.append(
                    TaskInfo(
                        id=str(unique_name),
                        name=self._safe_get(task_data, "TASK_NAME", "Unknown"),
                        type=str(self._safe_get(task_data, "TASKSCH_TYPE", "Unknown")),
                        state="Unknown",
                    )
                )

            tasks_api.ReleaseTasksIterator(iter_id)
            return tasks

            tasks_api.ReleaseTasksIterator(iter_id)
            return tasks

        except Exception as e:
            raise KscApiError(f"Failed to list tasks: {e}")

    async def list_tasks(self) -> List[TaskInfo]:
        return await anyio.to_thread.run_sync(self._list_tasks_sync)

    def _run_task_sync(self, task_id: str) -> TaskRunResult:
        self._ensure_connected()
        tasks_api = KlAkTasks(self.server)
        try:
            tasks_api.RunTask(strTask=task_id)
            return TaskRunResult(task_id=task_id, status="Started")
        except Exception as e:
            raise KscApiError(f"Failed to run task: {e}")

    async def run_task(self, task_id: str) -> TaskRunResult:
        return await anyio.to_thread.run_sync(self._run_task_sync, task_id)

    def _get_task_state_sync(self, task_id: str) -> TaskState:
        self._ensure_connected()
        tasks_api = KlAkTasks(self.server)
        try:
            res = tasks_api.GetTaskStatistics(strTask=task_id)
            data = res.RetVal()
            # data typically has percentages, state code, etc.
            # mapping needs to be robust, here we use defaults
            return TaskState(
                task_id=task_id,
                percentage=self._safe_get(data, "nCompletion", 0),
                state_code=self._safe_get(data, "nState", 0),
                state_desc="Running"
                if self._safe_get(data, "nState", 0)
                else "Unknown",  # simplified
            )
        except Exception as e:
            raise KscApiError(f"Failed to get task state: {e}")

    async def get_task_state(self, task_id: str) -> TaskState:
        return await anyio.to_thread.run_sync(self._get_task_state_sync, task_id)


ksc_service = KscService()
