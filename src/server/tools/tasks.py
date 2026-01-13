from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from server.ksc.service import ksc_service
from server.models import TaskInfo, TaskRunResult, TaskState


def register(mcp: FastMCP):
    @mcp.tool()
    async def list_tasks(
        group_id: int = Field(default=-1, description="Optional group ID to filter tasks. Defaults to -1 (Global)."),
        scan_all_groups: bool = Field(default=False, description="If true, scans ALL groups for tasks. Ignores group_id if set."),
    ) -> str:
        """
        Enumerate all available tasks on the KSC server.

        Returns a JSON string of task objects containing IDs and names.
        useful for finding a task ID before running it.
        Args:
            group_id: Optional. If set to -1 (default), lists global tasks. If set to a specific group ID, lists tasks for that group.
            scan_all_groups: Optional. If True, will iterate through ALL groups to find tasks. Use with caution on large servers.
        """
        import json
        tasks = await ksc_service.list_tasks(group_id=group_id, scan_all_groups=scan_all_groups)
        return json.dumps([t.model_dump() for t in tasks], indent=2)

    @mcp.tool()
    async def run_task(
        task_id: Annotated[str, Field(description="The unique identifier of the task to run.")],
    ) -> TaskRunResult:
        """
        Execute a specific task by its ID.

        Args:
            task_id: The unique identifier of the task to run.
        """
        return await ksc_service.run_task(task_id)

    @mcp.tool()
    async def get_task_state(
        task_id: Annotated[str, Field(description="The unique identifier of the task.")],
    ) -> TaskState:
        """
        Get the current execution state/statistics of a task.

        Use this to poll for completion or check progress.
        """
        return await ksc_service.get_task_state(task_id)
