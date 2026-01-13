
from mcp.server.fastmcp import FastMCP

from server.ksc.service import ksc_service
from server.models import GroupQuery

# Defines tools for manipulating groups


def register(mcp: FastMCP):
    @mcp.tool()
    async def list_groups(query: GroupQuery) -> str:
        """
        List administration groups in KSC.

        Returns a JSON string of group objects.
        Use this to browse the group hierarchy or find specific groups by name.
        """
        import json
        groups = await ksc_service.list_groups(
            group_name=query.group_name, parent_id=query.parent_id
        )
        return json.dumps([g.model_dump() for g in groups], indent=2)
