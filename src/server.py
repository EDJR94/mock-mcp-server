"""

*** MCP Server ***

"""

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
import os


mcp = FastMCP(name="MCP Server")

def get_bearer_token():
    request: Request = get_http_request()
    headers = request.headers
    # Check if 'Authorization' header is present
    authorization_header = headers.get('Authorization')

    
    if authorization_header:
        # Split the header into 'Bearer <token>'
        parts = authorization_header.split()
        
        if len(parts) == 2 and parts[0] == 'Bearer':
            return parts[1]
        else:
            raise ValueError("Invalid Authorization header format")
    else:
        raise ValueError("Authorization header missing")


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

    token = get_bearer_token()

    expected = os.environ.get("BEARER_TOKEN")

    print(f"Expected: {expected}")
    print(f"Token: {token}")

    if token != expected:
        print("Unauthorized")

    return a + b


if __name__ == "__main__":

    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.environ.get("PORT", 3000))
    mcp.run(transport="sse")