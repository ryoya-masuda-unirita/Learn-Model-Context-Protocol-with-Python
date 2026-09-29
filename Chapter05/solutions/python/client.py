from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio
import json
from typing import Optional, Dict, Any, List
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream

from typing import AsyncGenerator

import mcp.types as types

from mcp.types import (
    LoggingMessageNotificationParams,
    TextContent,
)

from mcp.shared.session import RequestResponder

class LoggingCollector:
    def __init__(self):
        self.log_messages: list[LoggingMessageNotificationParams] = []

    async def __call__(self, params: LoggingMessageNotificationParams) -> None:
        self.log_messages.append(params)

logging_collector = LoggingCollector()

port = 8000

# 通常のメッセージ、通知、例外を受け取る
async def message_handler(
        message: RequestResponder[types.ServerRequest, types.ClientResult]
        | types.ServerNotification
        | Exception,
    ) -> None:
        print("メッセージを受信:", message)
        if isinstance(message, Exception):
            raise message
        else:
            if isinstance(message, types.ServerNotification):
                print("通知:", message)
            elif isinstance(message, RequestResponder):
                print("リクエストへの応答:", message)
            else:
                print("サーバーからのリクエスト:", message)

async def main():
    print("クライアントを起動しています...")
    # Streamable HTTP サーバーに接続する
    async with streamablehttp_client(f"http://localhost:{port}/mcp") as (
        read_stream,
        write_stream,
        session_callback,
    ): 
        # クライアントのストリームを使ってセッションを作る
        async with ClientSession(
            read_stream, 
            write_stream,
            logging_callback=logging_collector,
            message_handler=message_handler,
        ) as session:

            # まだ初期化していないので None のはず
            id = session_callback()
            print("ID: ", id)

            # 接続を初期化する
            await session.initialize()

            id = session_callback()
            print("ID: ", id)

            print("セッションを初期化しました。tool を呼び出せます。")
          
            # tool を呼び出す
            results = []
            tool_result = await session.call_tool("echo", {"message": "こんにちは"})

            gen = None
            # tool_result が非同期ジェネレーターなら、その要素を表示する

            # tool_result.text が awaitable か非同期イテラブルなら、AsyncGenerator に変換する
           
            print("tool の結果:", tool_result)
            # log = logging_collector.log_messages[0]
            # print("ログメッセージ:", log)

            


asyncio.run(main())