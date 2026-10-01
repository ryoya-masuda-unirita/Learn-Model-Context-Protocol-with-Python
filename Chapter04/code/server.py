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
# mcp.sse_app() は、SSE トランスポートの MCP サーバーを ASGI アプリとして返す。中には2つのエンドポイントがある
#   GET  /sse        : サーバー → クライアントの通り道。接続を開きっぱなしにして、応答や通知をイベントとして流す
#   POST /messages/  : クライアント → サーバーの通り道。リクエストを1件ずつ POST する
# HTTP は1回のリクエストに1回の応答しか返せないため、stdio の stdin / stdout の代わりに、向きごとに道を分けている
# '/' にマウントしているので、クライアントは http://localhost:<ポート>/sse に接続する
app: Starlette = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)
