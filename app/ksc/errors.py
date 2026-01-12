class KscError(Exception):
    """Base exception for KSC MCP server."""

    pass


class KscAuthError(KscError):
    """Authentication failed."""

    pass


class KscApiError(KscError):
    """KSC API returned an error."""

    pass


class KscTaskError(KscError):
    """Error related to KSC tasks."""

    pass
