from fastmcp import FastMCP, Context
from typing import List, Optional
from enum import Enum

mcp = FastMCP("ERNI MCP")

@mcp.tool()
def suggest_solution(concerns: List[str]) -> str:
    """Suggest ERNI solution"""    
    return "Better ask ERNI!"

if __name__ == "__main__":
    mcp.run("sse")

