"""low-level サーバー（server.py）に SSE で接続し、tool と prompt を試すクライアント。"""
from mcp import ClientSession, types
from mcp.client.sse import sse_client



async def run() -> None:
    """SSE でサーバーに接続し、tool と prompt を順に試す。"""
    async with sse_client(url="http://127.0.0.1:8000/sse") as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # 接続を初期化する
            await session.initialize()

            print("セッションを初期化しました")

            # # 使える prompt の一覧を取得する
            # prompts = await session.list_prompts()

            # # prompt を取得する
            # prompt = await session.get_prompt(
            #     "example-prompt", arguments={"arg1": "value"}
            # )

            # # 使える resource の一覧を取得する
            # resources = await session.list_resources()

            # 使える tool の一覧を取得する
            tools = await session.list_tools()
            print(tools)

            result = await session.call_tool("add", arguments={"a": 1, "b": 2})
            print("tool の結果:", result)

            prompts = await session.list_prompts()
            print("使える prompt:", prompts)

            prompt = await session.get_prompt(
                "example-prompt"
            )

            print("prompt:", prompt)

            # # resource を読み込む
            # content, mime_type = await session.read_resource("file://some/path")

            # # tool を呼び出す
            # result = await session.call_tool("tool-name", arguments={"arg1": "value"})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())