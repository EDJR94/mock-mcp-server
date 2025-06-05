"""

*** MCP Server ***

"""

from mcp.server.fastmcp import FastMCP
import os


mcp = FastMCP(name="MCP Server")


@mcp.tool()
def greeting(hint: str) -> str:
    """
    This tool just displays a message.

    Args:
        hint: The hint is always "MCP Server"
    """
    return "Hey, Lads! This is Felix Kewa and this is my own remote MCP Server!"


@mcp.tool()
def add(a: int, b: int) -> int:
    """
    This tool is used to add two numbers.

    Args:
        a: The first number
    """
    return a + b


if __name__ == "__main__":

    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.environ.get("PORT", 3000))
    mcp.run(transport="sse")