import importlib
import logging
import pkgutil

from mcp.server.fastmcp import FastMCP

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ksc-mcp")

# Initialize FastMCP
mcp = FastMCP("ksc-mcp")


def load_tools():
    """
    Auto-discovers and registers tools from the src.server.tools package.
    """
    import src.server.tools as tools_pkg

    package_path = tools_pkg.__path__
    prefix = tools_pkg.__name__ + "."

    for _, name, _ in pkgutil.iter_modules(package_path, prefix):
        try:
            logger.info(f"Loading tools from module: {name}")
            module = importlib.import_module(name)
            if hasattr(module, "register"):
                module.register(mcp)
            else:
                logger.warning(f"Module {name} has no 'register' function.")
        except Exception as e:
            logger.error(f"Failed to load tools from {name}: {e}")


def main():
    """Server entry point."""
    logger.info("Starting KSC MCP Server...")
    load_tools()
    mcp.run()


if __name__ == "__main__":
    main()
