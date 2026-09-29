# TODO: Python のクライアントを追加する

import asyncio

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.types import ElicitRequestParams, ElicitResult, TextContent
from mcp.shared.context import RequestContext

async def elicitation_callback_handler(context: RequestContext[ClientSession, None], params: ElicitRequestParams):
    print(f"[CLIENT] elicitation のデータを受信しました: {params.message}")
 
    # 1. 別の日付を選ぶのを断る
    # return ElicitResult(action="accept", content={
    #     "checkAlternative": False
    # }) # 予約は行われなかったと返るはず（動作確認済み）

    # 2. 予約をキャンセルする
    # return ElicitResult(action="decline"), 動作確認済み

    print("[CLIENT]: 代わりの日付を選択します: 2025-01-01")

    # 3. 別の日付 2025-01-01 を選び、予約が成立する
    return ElicitResult(action="accept", content={
         "checkAlternative": True,
         "alternativeDate": "2025-01-01"
    }) # 最初の 1月2日ではなく 1月1日で予約されるはず


    

async def main():
    # Server-Sent Events (SSE) サーバーに接続する
    async with sse_client(url="http://localhost:8000/sse") as (
        read_stream,
        write_stream
    ):
        # クライアントのストリームを使ってセッションを作る
        async with ClientSession(
            read_stream, 
            write_stream,
            elicitation_callback=elicitation_callback_handler) as session:
            # 接続を初期化する
            await session.initialize()
            # 使える tool の一覧を取得する
            tools = await session.list_tools()
            print(f"使える tool: {[tool.name for tool in tools.tools]}")

            # tool を呼び出す
            result = await session.call_tool("book_trip", {
                "date": "2025-01-02"
            })
            print("結果: ", result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())