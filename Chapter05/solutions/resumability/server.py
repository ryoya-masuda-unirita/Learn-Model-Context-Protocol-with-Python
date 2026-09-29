# server.py
from itertools import count
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send

import contextlib
import anyio

from collections.abc import AsyncIterator
from typing import Any
import mcp.types as types

from mcp.server.fastmcp import FastMCP, Context
from typing import Optional, Dict, Any, List, AsyncGenerator
from mcp.types import (
    LoggingMessageNotificationParams,
    TextContent
)
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
import logging
import uvicorn

from mcp.server.lowlevel import Server

from event_store import InMemoryEventStore

# ログの準備
logger = logging.getLogger(__name__)
# ログを設定する
logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# メッセージ用のストアを作る
event_store = InMemoryEventStore()

# MCP サーバーを作る
app = Server("mcp-streamable-http-demo")

# アプリとイベントストアを使ってセッションマネージャーを作る
session_manager = StreamableHTTPSessionManager(
    app=app,
    event_store=event_store,  # resumability を有効にする
    json_response=True,
)

# Streamable HTTP 接続用の ASGI ハンドラー
async def handle_streamable_http(scope: Scope, receive: Receive, send: Send) -> None:
    await session_manager.handle_request(scope, receive, send)

@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[None]:
    """セッションマネージャーのライフサイクルを管理するコンテキストマネージャー。"""
    async with session_manager.run():
        logger.info("StreamableHTTP セッションマネージャー付きでアプリケーションを起動しました！")
        try:
            yield
        finally:
            logger.info("アプリケーションを終了しています...")

files = [
    "file1.txt",
    "file2.txt",
    "file3.txt"
]

# tool の呼び出し
@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.ContentBlock]:
    ctx = app.request_context
    print("コンテキスト:", ctx)

    no_of_files = len(files)

    # 指定した間隔で、指定した数の通知を送る
    for i in range(no_of_files):
        # resumability のデモ用に、詳しいメッセージを含める
        notification_msg = f"[{i + 1}/{no_of_files}] '{files[i]}' からのイベント - 切断された場合は Last-Event-ID を使って再開できます"
        print("コンテキストのログ送信メソッド", ctx.session.send_log_message)
        
        await ctx.session.send_log_message(
            level="info",
            data=notification_msg,
            logger="notification_stream",
            # この通知を元のリクエストに関連付ける
            # 通知が正しいレスポンスストリームに送られるようにする
            # これがないと、通知の送り先は次のどちらかになる：
            # - 独立した SSE ストリーム（GET リクエストに対応している場合）
            # - どこにも送られない（GET リクエストに対応していない場合）
            related_request_id=ctx.request_id,
        )
        logger.debug(f"通知を送信しました {i + 1}/{no_of_files}")
        # if i < no_of_files - 1:  # 最後の通知の後は待たない
        await anyio.sleep(0.1)

    return [
        types.TextContent(
            type="text",
            text=(f"{no_of_files} 件を処理しました"),
        )
    ]

# tool の一覧（どんな tool があるか）を定義する
@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="process-files",
            description=("複数のファイルを処理する"),
            inputSchema={
                "type": "object",
                "required": [],
                "properties": {},
            },
        )
    ]


starlette_app = Starlette(
    debug=True,
    routes=[
        Mount("/mcp", app=handle_streamable_http),
    ],
    lifespan=lifespan,
)

uvicorn.run(starlette_app, host="127.0.0.1", port=3000)