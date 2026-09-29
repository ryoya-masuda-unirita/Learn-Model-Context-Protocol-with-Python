from starlette.applications import Starlette
from starlette.routing import Mount, Host
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("My App")

@mcp.tool()
def add(a: int, b: int) -> int:
    """2つの数を足し算する"""
    return a + b
    

# 既存の ASGI サーバーに SSE サーバーをマウントする
app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)