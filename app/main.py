import logging
import sys

from app.mcp import mcp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)


def main():
    """Entry point for the MCP server."""
    # Initialize connection on startup (optional, but good for fail-fast)
    # We can't await here easily in sync main, but FastMCP handles lifecycle.
    # ideally we'd use a startup hook but FastMCP is simple.
    # The service constructs lazy, so connection happens on first call.
    mcp.run()


if __name__ == "__main__":
    main()
