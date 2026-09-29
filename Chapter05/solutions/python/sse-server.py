from starlette.applications import Starlette
from starlette.routing import Mount, Host

from mcp.server.fastmcp import FastMCP, Context
from typing import Optional, Dict, Any, List, AsyncGenerator
from mcp.types import (
    LoggingMessageNotificationParams,
    TextContent
)

# MCP サーバーを作る
mcp = FastMCP("Streamable DEMO")

@mcp.tool(description="ファイルの内容を返すシンプルな tool")
async def echo(message: str, ctx: Context) -> str:

    # ctx2 = mcp.get_context()
    # print(f"コンテキスト ID: {ctx2}")

    # await ctx.debug(f"ファイルを処理中 1/3: {message}")
    await ctx.info(f"ファイルを処理中 1/3:")
    await ctx.info(f"ファイルを処理中 2/3:")
    await ctx.info(f"ファイルを処理中 3/3:")

    # await ctx.log(
    #         level="info",
    #         message="こんにちは",
    #         logger_name="Obi Wan",
    #     )

    return TextContent(type="text", text=f"ファイルの内容です: {message}")

app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)