from typing import List, Optional

from pydantic import BaseModel, Field


class HostInfo(BaseModel):
    """
    Represents a managed device (host) in Kaspersky Security Center.
    """

    id: str = Field(..., description="Unique identifier of the host (KSC ID).")
    name: str = Field(..., description="NetBIOS or DNS name of the host.")
    display_name: str = Field(..., description="Display name of the host in KSC console.")
    group_id: int = Field(..., description="ID of the administration group the host belongs to.")
    group_name: str = Field(default="Unknown", description="Name of the administration group.")
    status: str = Field(
        default="0", description="Numeric status code of the host (Critical, Warning, OK)."
    )
    ip_address: Optional[str] = Field(default=None, description="IP address of the host, if known.")
    products: List[str] = Field(
        default_factory=list, description="List of Kaspersky products installed."
    )


class HostDetail(BaseModel):
    """
    Detailed information about a specific host.
    """

    id: str = Field(..., description="Unique identifier of the host.")
    name: str = Field(..., description="Host name.")
    products: List[str] = Field(
        default_factory=list, description="Installed security applications."
    )
    os_info: dict = Field(default_factory=dict, description="Operating system details.")


class HostQuery(BaseModel):
    """
    Parameters for querying hosts.
    """

    group_name: Optional[str] = Field(
        default=None,
        description="Filter hosts by administration group name. If None, searches all groups.",
    )
    status: Optional[str] = Field(
        default=None, description="Filter by status (e.g. 'Critical', 'Warning', 'OK')."
    )


class GroupInfo(BaseModel):
    """
    Represents an administration group in KSC.
    """

    id: int = Field(..., description="Unique numeric identifier of the group.")
    name: str = Field(..., description="Name of the group.")
    full_name: str = Field(..., description="Full path/name of the group.")
    parent_id: int = Field(default=0, description="ID of the parent group.")
    host_count: int = Field(default=0, description="Number of hosts in the group.")


class GroupQuery(BaseModel):
    """
    Parameters for querying groups.
    """

    group_name: Optional[str] = Field(
        default=None, description="Filter by group name (supports wildcards)."
    )
    parent_id: Optional[int] = Field(
        default=None, description="Filter by parent group ID."
    )


class MoveHostParams(BaseModel):
    """
    Parameters for moving a host to a different group.
    """

    host_id: str = Field(..., description="The ID of the host to move.")
    target_group_id: int = Field(..., description="The ID of the destination group.")


class TaskInfo(BaseModel):
    """
    Represents a KSC task.
    """

    id: str = Field(..., description="Unique task identifier.")
    name: str = Field(..., description="Human-readable name of the task.")
    type: str = Field(default="Unknown", description="Type of the task (e.g. 'Scan', 'Update').")
    state: str = Field(
        default="Unknown", description="Current execution state (e.g. 'Running', 'Completed')."
    )


class TaskRunResult(BaseModel):
    """
    Result of a task execution request.
    """

    task_id: str = Field(..., description="ID of the task that was run.")
    status: str = Field(..., description="Status of the run request (e.g. 'Started').")


class TaskState(BaseModel):
    """
    Current statistics/state of a task.
    """

    task_id: str = Field(..., description="ID of the task.")
    percentage: int = Field(default=0, description="Completion percentage (0-100).")
    state_code: int = Field(default=0, description="Numeric state code.")
    state_desc: str = Field(default="Unknown", description="Text description of the state.")
