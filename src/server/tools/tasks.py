from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from src.server.ksc.service import ksc_service
from src.server.models import TaskInfo, TaskRunResult, TaskState


def register(mcp: FastMCP):
    @mcp.tool()
    async def list_tasks() -> list[TaskInfo]:
        """
        Enumerate all available tasks on the KSC server.

        Returns a list of task objects containing IDs and names.
        useful for finding a task ID before running it.
        """
        return await ksc_service.list_tasks()

    @mcp.tool()
    async def run_task(
        task_id: Annotated[str, Field(description="The unique identifier of the task to run.")]
    ) -> TaskRunResult:
        """
        Execute a specific task by its ID.

        Args:
            task_id: The unique identifier of the task to run.
        """
        return await ksc_service.run_task(task_id)

    @mcp.tool()
    async def get_task_state(
        task_id: Annotated[str, Field(description="The unique identifier of the task.")]
    ) -> TaskState:
        """
        Get the current execution state/statistics of a task.

        Use this to poll for completion or check progress.
        """
        return await ksc_service.get_task_state(task_id)
