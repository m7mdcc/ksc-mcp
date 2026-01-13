from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from server.ksc.service import ksc_service
from server.models import HostDetail, HostInfo, HostQuery, MoveHostParams

# Defines tools for manipulating hosts and groups


def register(mcp: FastMCP):
    @mcp.tool()
    async def get_hosts(query: HostQuery) -> list[HostInfo]:
        """
        Search for managed devices (hosts) in KSC.

        Use this tool to find hosts by group name or status.
        If no filters are provided, it returns all visible hosts (limited by default paging).
        """
        return await ksc_service.list_hosts(group_name=query.group_name, status=query.status)

    @mcp.tool()
    async def get_host_details(
        host_id: Annotated[
            str, Field(description="The unique identifier of the host (KSC ID preferred).")
        ],
    ) -> HostDetail:
        """
        Retrieve detailed information about a specific host.

        Args:
            host_id: The unique identifier of the host (KSC ID preferred).
        """
        return await ksc_service.get_host_details(host_id)

    @mcp.tool()
    async def move_host(params: MoveHostParams) -> bool:
        """
        Move a host to a different administration group.

        Args:
            params: Object containing host_id and target_group_id.
        """
        return await ksc_service.move_host(host_id=params.host_id, group_id=params.target_group_id)

    # Future: add list_groups here
