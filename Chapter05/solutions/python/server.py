"""Streamable HTTP で公開する MCP サーバー。

`python server.py` で起動すると、ポート 8000 の /mcp で待ち受ける。
"""
# server.py
from mcp.server.fastmcp import FastMCP, Context
from typing import Optional, Dict, Any, List, AsyncGenerator
from mcp.types import (
    LoggingMessageNotificationParams,
    TextContent
)

# MCP サーバーを作る
mcp: FastMCP = FastMCP("Streamable DEMO")

@mcp.tool(description="ファイルの内容を返すシンプルな tool")
async def echo(message: str, ctx: Context) -> str:
    """ファイルを処理しているふりをして、進捗をログで通知しながらメッセージを返す。

    Parameters
    ----------
    message : str
        返すメッセージ。
    ctx : Context
        MCP のリクエストコンテキスト。ログの通知を送るのに使う。

    Returns
    -------
    str
        メッセージを含むファイルの内容。
    """
    # ctx2 = mcp.get_context()
    # print(f"コンテキスト ID: {ctx2}")

    # ctx.info() は notifications/message（ログの通知）をクライアントに送る。
    # tool の結果を返す前に送るので、クライアントは処理の途中経過を受け取れる
    # await ctx.debug(f"ファイルを処理中 1/3: {message}")
    await ctx.info(f"ファイルを処理中 1/3:")
    await ctx.info(f"ファイルを処理中 2/3:")
    await ctx.info(f"ファイルを処理中 3/3:")

    # await ctx.log(
    #         level="info",
    #         message="こんにちは",
    #         logger_name="Obi Wan",
    #     )

    return f"ファイルの内容です: {message}"

# Streamable HTTP では、クライアントは /mcp に JSON-RPC を POST するだけでよい（SSE のように道を2つに分けない）。
# サーバーは1件だけ返すなら JSON、途中で通知も送るなら SSE のストリームで応答を返す。
# デフォルトでは http://127.0.0.1:8000/mcp で待ち受ける
mcp.run(transport="streamable-http")