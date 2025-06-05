"""
*** MCP Server ***
"""

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request
from fastapi import Request
from starlette.requests import Request
import requests
import os
import logging
import traceback

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MCPServer")

mcp = FastMCP(name="MCP Server")


def get_bearer_token():
    try:
        request: Request = get_http_request()
        headers = request.headers
        authorization_header = headers.get('Authorization')

        if authorization_header:
            parts = authorization_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                return parts[1]
            else:
                raise ValueError("Invalid Authorization header format")
        else:
            raise ValueError("Authorization header missing")
    except Exception as e:
        logger.error("Error extracting bearer token: %s", str(e))
        traceback.print_exc()
        raise


@mcp.tool()
def greeting(hint: str) -> str:
    logger.info(f"Greeting tool invoked with hint: {hint}")
    return "Hey, Lads! This is Felix Kewa and this is my own remote MCP Server!"


@mcp.tool()
def add(a: int, b: int) -> int:
    logger.info(f"Add tool invoked with a={a}, b={b}")
    try:
        token = get_bearer_token()
        expected = os.environ.get("BEARER_TOKEN")

        logger.info(f"Expected token: {expected}")
        logger.info(f"Received token: {token}")

        if token != expected:
            logger.warning("Unauthorized token received.")
            raise PermissionError("Unauthorized")

        result = a + b
        logger.info(f"Returning result: {result}")
        return result

    except Exception as e:
        logger.error("Error in 'add' tool: %s", str(e))
        traceback.print_exc()
        raise


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    logger.info(f"Starting MCP Server on 0.0.0.0:{port}")
    try:
        mcp.run(transport="sse", port=port, host="0.0.0.0")
    except Exception as e:
        logger.critical("Failed to start server: %s", str(e))
        traceback.print_exc()