"""足し算の tool を持つ MCP サーバーを、SSE で公開する ASGI アプリケーション。

`uvicorn server:app` で起動する。
"""
from starlette.applications import Starlette
from starlette.routing import Mount, Host
from mcp.server.fastmcp import FastMCP


mcp: FastMCP = FastMCP("My App")

@mcp.tool()
def add(a: int, b: int) -> int:
    """2つの数を足し算する。

    Parameters
    ----------
    a : int
        足される数。
    b : int
        足す数。

    Returns
    -------
    int
        a と b の和。
    """
    return a + b


# 既存の ASGI サーバーに SSE サーバーをマウントする
app: Starlette = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)
