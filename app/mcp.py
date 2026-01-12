from typing import List

from mcp.server.fastmcp import FastMCP

from app.ksc.models import HostDetail, HostInfo, TaskInfo
from app.ksc.service import ksc_service

mcp = FastMCP("KSC MCP Server")


@mcp.tool()
async def ksc_ping() -> str:
    """Ping the KSC server to verify connectivity."""
    return await ksc_service.ping()


@mcp.tool()
async def ksc_list_hosts(group_name: str = None, status: str = None) -> List[HostInfo]:
    """List hosts managed by KSC, optionally filtered by group or status."""
    return await ksc_service.list_hosts(group_name, status)


@mcp.tool()
async def ksc_get_host_details(host_id: str) -> HostDetail:
    """Get detailed information about a specific host."""
    return await ksc_service.get_host_details(host_id)


@mcp.tool()
async def ksc_list_tasks() -> List[TaskInfo]:
    """List available tasks on the KSC server."""
    return await ksc_service.list_tasks()


@mcp.tool()
async def ksc_run_task(task_id: str) -> str:
    """Run a specific task by ID."""
    return await ksc_service.run_task(task_id)


@mcp.tool()
async def ksc_get_task_state(task_id: str) -> dict:
    """Get the current state/statistics of a task."""
    return await ksc_service.get_task_state(task_id)
