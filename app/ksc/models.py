from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class HostFilter(BaseModel):
    group_name: Optional[str] = Field(None, description="Filter hosts by group name")
    status: Optional[str] = Field(
        None, description="Filter hosts by status (e.g., 'OK', 'WARNING', 'CRITICAL')"
    )


class HostInfo(BaseModel):
    id: str
    name: str
    display_name: str
    group_id: int
    group_name: str
    status: str
    last_seen: Optional[str] = None
    ip_address: Optional[str] = None


class TaskInfo(BaseModel):
    id: str
    name: str
    type: str  # e.g. "Update", "Scan"
    state: str
    result: Optional[str] = None
    created_at: Optional[str] = None


class TaskRunResult(BaseModel):
    task_id: str
    status: str
    message: str


class HostDetail(BaseModel):
    id: str
    name: str
    products: List[Dict[str, Any]] = []
    os_info: Optional[Dict[str, Any]] = None
    polices: List[Dict[str, Any]] = []
