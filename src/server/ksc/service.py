import logging
from typing import List, Optional

import anyio

# Import KlAkOAPI modules
from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.ChunkAccessor import KlAkChunkAccessor
from KlAkOAPI.HostGroup import KlAkHostGroup
from KlAkOAPI.Tasks import KlAkTasks

from server.ksc.errors import KscApiError, KscAuthError
from server.models import GroupInfo, HostDetail, HostInfo, TaskInfo, TaskRunResult, TaskState
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
                verify=(
                    settings.KSC_CERT_PATH
                    if settings.KSC_CERT_PATH
                    else settings.KSC_VERIFY_SSL
                ),
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
        # Build filter string
        # wstr_filter = ""
        # wstr_filter = "" # Original line, replaced by new logic below
        # Improved filtering logic would go here # Original line, replaced by new logic below
        # if not wstr_filter: # Original line, replaced by new logic below
        #     wstr_filter = '(KLHST_WKS_DN="*")' # Original line, replaced by new logic below

        vec_fields = [
            "KLHST_WKS_DN",
            "KLHST_WKS_HOSTNAME",
            "KLHST_WKS_GRP",
            "KLHST_WKS_STATUS",
            "id",
            "name",
            "KLHST_WKS_IP",
            "KLHST_WKS_RTP_STATE",
            "KLHST_WKS_STATUS_ID",
        ]

        # Build filter
        filters = []
        if group_name:
            # Attempting group name filter if possible, or usually we filter by browsing group.
            filters.append(f'(KLHST_WKS_GRP_NAME="{group_name}")')

        final_filter = ""
        if group_name:
             # Reverting to original logic for group_name to avoid breaking changes in this task
             # But it effectively filters by Host Name currently.
             final_filter = f"(name=\"{group_name}\")"

        if status:
            status_map = {
                "OK": 0,
                "CRITICAL": 1,
                "WARNING": 2
            }
            # Case insensitive check
            s_upper = status.upper()
            if s_upper in status_map:
                sid = status_map[s_upper]
                status_filter = f"(KLHST_WKS_STATUS_ID={sid})"
                if final_filter:
                    final_filter = f"(&{final_filter}{status_filter})"
                else:
                    final_filter = status_filter

        # If no specific filters, default to all hosts
        if not final_filter:
            final_filter = '(KLHST_WKS_DN="*")'

        try:
            res = host_group.FindHosts(
                wstrFilter=final_filter,
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

                        grp_id = self._safe_get(item, "KLHST_WKS_GRP", 0)
                        grp_name = "Unknown"
                        if grp_id == 0:
                            grp_name = "Managed Devices"

                        # Extract other fields safely
                        dn = self._safe_get(item, "KLHST_WKS_DN", "Unknown")
                        hostname = self._safe_get(item, "KLHST_WKS_HOSTNAME", "Unknown")
                        status = self._safe_get(item, "KLHST_WKS_STATUS", "0")
                        ip_val = self._safe_get(item, "KLHST_WKS_IP", None)

                        # Decode IP
                        ip_str = None
                        if ip_val is not None:
                            try:
                                ip_int = int(ip_val)
                                if ip_int < 0:
                                    ip_int += 2**32
                                import socket
                                import struct
                                packed_ip = struct.pack('<I', ip_int)
                                ip_str = socket.inet_ntoa(packed_ip)
                            except Exception:
                                ip_str = str(ip_val)

                        # Fetch RTP State
                        rtp_state_val = self._safe_get(item, "KLHST_WKS_RTP_STATE", 0)
                        rtp_desc = "Unknown"
                        try:
                            rtp_int = int(rtp_state_val)
                            rtp_map = {
                                0: "Unknown",
                                1: "Stopped",
                                2: "Suspended",
                                3: "Starting",
                                4: "Running",
                                5: "Running (Max Protection)",
                                6: "Running (Max Speed)",
                                7: "Running (Recommended)",
                                8: "Running (Custom)",
                                9: "Failure"
                            }
                            rtp_desc = rtp_map.get(rtp_int, str(rtp_int))
                        except Exception:
                            rtp_desc = str(rtp_state_val)

                        # Fetch Status ID (OK/Critical/Warning)
                        status_id_val = self._safe_get(item, "KLHST_WKS_STATUS_ID", 0)
                        status_id_desc = "Unknown"
                        try:
                             sid_int = int(status_id_val)
                             if sid_int == 0:
                                 status_id_desc = "OK"
                             elif sid_int == 1:
                                 status_id_desc = "Critical"
                             elif sid_int == 2:
                                 status_id_desc = "Warning"
                             else:
                                 status_id_desc = str(sid_int)
                        except Exception:
                            status_id_desc = str(status_id_val)

                        # Decode Status Bitmask
                        status_str = str(status)
                        try:
                            s_int = int(status)
                            status_desc_parts = []
                            # Bit 0 (1): Visible
                            if s_int & 0b1:
                                status_desc_parts.append("Visible")
                            # Bit 2 (4): Agent Installed
                            if s_int & 0b100:
                                status_desc_parts.append("Agent Installed")
                            # Bit 3 (8): Agent Active
                            if s_int & 0b1000:
                                status_desc_parts.append("Agent Active")
                            # Bit 4 (16): RTP Installed
                            if s_int & 0b10000:
                                status_desc_parts.append("RTP Installed")

                            # Combine
                            status_details = (
                                ", ".join(status_desc_parts) if status_desc_parts else "None"
                            )
                            status_str = (
                                f"[{status_id_desc}] Status: {status} "
                                f"({status_details}) | RTP: {rtp_desc}"
                            )
                        except Exception:
                            pass

                        hosts.append(
                            HostInfo(
                                id=str(unique_name),
                                name=str(hostname),
                                display_name=str(dn),
                                group_id=grp_id,
                                group_name=grp_name,
                                status=status_str,
                                ip_address=ip_str,
                            )
                        )

            return hosts

        except Exception as e:
            raise KscApiError(f"Failed to list hosts: {e}")

    def _list_groups_sync(
        self, group_name: Optional[str] = None, parent_id: Optional[int] = None
    ) -> List[GroupInfo]:
        self._ensure_connected()
        host_group = KlAkHostGroup(self.server)
        chunk_accessor = KlAkChunkAccessor(self.server)

        # Build filter
        wstr_filter = ""
        if group_name:
            # Simple wildcard support
            wstr_filter = f'(name="{group_name}")'

        # Note: parent_id filtering is usually implicit by calling FindGroups on a specific group
        # But FindGroups searches strictly in subtree or globally depending on flags.
        # "pParams" can control search depth or scope.
        p_params = {}
        if parent_id is not None:
            # If we want to search ONLY in a specific parent,
            # we might need different API call or params
            pass
            # We usually use 'one level' search or 'subtree' search.

        vec_fields = ["id", "name", "grp_full_name", "KLGRP_CHLDHST_CNT"]

        try:
            res = host_group.FindGroups(
                wstrFilter=wstr_filter,
                vecFieldsToReturn=vec_fields,
                vecFieldsToOrder=[],
                pParams=p_params,
                lMaxLifeTime=600,
            )

            str_accessor = res.OutPar("strAccessor")
            items_count = chunk_accessor.GetItemsCount(str_accessor).RetVal()

            groups = []
            if items_count > 0:
                count_to_fetch = min(items_count, 100)
                res_chunk = chunk_accessor.GetItemsChunk(str_accessor, 0, count_to_fetch)
                chunk_data = res_chunk.OutPar("pChunk")

                if chunk_data and "KLCSP_ITERATOR_ARRAY" in chunk_data:
                    items_iter = chunk_data["KLCSP_ITERATOR_ARRAY"]
                    for item in items_iter:
                        groups.append(
                            GroupInfo(
                                id=self._safe_get(item, "id", 0),
                                name=str(self._safe_get(item, "name", "Unknown")),
                                full_name=str(self._safe_get(item, "grp_full_name", "")),
                                host_count=self._safe_get(item, "KLGRP_CHLDHST_CNT", 0),
                                # TODO: Get parent ID if possible,
                        # usually requires extra query or fields
                                parent_id=0
                            )
                        )

            return groups

        except Exception as e:
            raise KscApiError(f"Failed to list groups: {e}")

    async def list_groups(
        self, group_name: Optional[str] = None, parent_id: Optional[int] = None
    ) -> List[GroupInfo]:
        return await anyio.to_thread.run_sync(self._list_groups_sync, group_name, parent_id)

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

    def _list_tasks_sync(self, group_id: int = -1, scan_all_groups: bool = False) -> List[TaskInfo]:
        self._ensure_connected()
        tasks_api = KlAkTasks(self.server)

        # Strategy:
        # 1. If scan_all_groups is True, get all groups first, then iterate.
        # 2. If scan_all_groups is False, just query the specific group_id (or Global if -1).

        target_groups = []
        if scan_all_groups:
            # Fetch all groups. We could filter by parent_id if needed,
            # but for "all" we want the flat list presumably.
            # _list_groups_sync with no args usually returns all top-level or searchable groups.
            # However, FindGroups usually searches deep if configured.
            # _list_groups_sync uses wstrFilter='(name="{group_name}")' if named, else all?
            # Let's check _list_groups_sync implementation. It uses empty filter -> all groups.
            kv_groups = self._list_groups_sync()
            target_groups = [g.id for g in kv_groups]

            # Also include global tasks (group -1)
            target_groups.append(-1)
        else:
            target_groups = [group_id]

        all_tasks = []

        for gid in target_groups:
            # If group_id is not -1, we assume it's significant
            group_id_significant = gid != -1

            try:
                res = tasks_api.ResetTasksIterator(
                    nGroupId=gid,
                    bGroupIdSignificant=group_id_significant,
                    strProductName="",
                    strVersion="",
                    strComponentName="",
                    strInstanceId="",
                    strTaskName="",
                    # Maybe False if scanning all to avoid dups? But True is safer for visibility.
                    bIncludeSupergroups=True,
                )

                iter_id = res.OutPar("strTaskIteratorId")

                # Fetch tasks for this group
                for _ in range(50): # Limit per group to avoid timeout loops
                    res_task = tasks_api.GetNextTask(iter_id)
                    task_data = res_task.OutPar("pChunk")
                    if not task_data:
                        break

                    # Check potential ID fields
                    unique_name = self._safe_get(task_data, "TASK_UNIQUE_ID", "")
                    if not unique_name:
                         unique_name = self._safe_get(task_data, "strName", "")


                    # Check if already added (simple dedup by ID)
                    t_id = str(unique_name)
                    if any(t.id == t_id for t in all_tasks):
                        continue

                    # Resolve friendly name
                    # unique_name is the ID needed for GetTask
                    friendly_name = self._safe_get(task_data, "TASK_NAME", "Unknown")

                    try:
                        # Fetch full details to get DisplayName
                        details = tasks_api.GetTask(str(unique_name))

                        # details might be KlAkResponse or KlAkParams or dict-like
                        # Try item access first as it seems most reliable for these wrappers
                        dn = None
                        try:
                            dn = details["DisplayName"]
                        except Exception:
                            # Try .get if available
                            if hasattr(details, "get"):
                                try:
                                    dn = details.get("DisplayName")
                                except Exception:
                                    pass

                            # check if it's a list or tuple (sometimes KlAkParams)
                            if not dn:
                                try:
                                    # Try extracting from raw if it's wrapped
                                    # But for now assume dict-like access works or fails
                                    pass
                                except Exception:
                                    pass

                        if not dn:
                            try:
                                # Sometimes details is a wrapper that needs OutPar or similar?
                                # But GetTask generally returns KlAkParams.
                                # If ParseResponse returns dict (from json), we are good.
                                rv = details
                                if hasattr(details, "RetVal"):
                                    rv = details.RetVal()

                                try:
                                    dn = rv["DisplayName"]
                                except Exception:
                                    pass
                            except Exception:
                                pass

                        if dn:
                             friendly_name = dn

                    except Exception:
                        pass

                    all_tasks.append(
                        TaskInfo(
                            id=t_id,
                            name=str(friendly_name),
                            type=str(self._safe_get(task_data, "TASKSCH_TYPE", "Unknown")),
                            state="Unknown",
                        )
                    )

                tasks_api.ReleaseTasksIterator(iter_id)

            except Exception:
                # If one group fails (e.g. permissions), log/ignore and continue to next
                continue

        return all_tasks



    async def list_tasks(self, group_id: int = -1, scan_all_groups: bool = False) -> List[TaskInfo]:
        return await anyio.to_thread.run_sync(self._list_tasks_sync, group_id, scan_all_groups)

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
