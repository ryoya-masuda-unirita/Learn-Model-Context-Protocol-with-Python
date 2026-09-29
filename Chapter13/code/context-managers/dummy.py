class DummyStream:
    async def read(self): pass
    async def write(self, data): pass

class DummyClientSession:
    def __init__(self, read_stream, write_stream):
        self.read_stream = read_stream
        self.write_stream = write_stream

    async def __aenter__(self):
        print("セッションを開始しました")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("セッションを閉じました")

    async def initialize(self):
        print("セッションを初期化しています...")

    async def list_tools(self):
        class Tool:
            def __init__(self, name): self.name = name
        return type("ToolList", (), {"tools": [Tool("ToolA"), Tool("ToolB")]})()

async def streamablehttp_client(url):
    print(f"{url} に接続しています")
    return DummyStream(), DummyStream(), None

# メインの非同期関数
async def main():
    read_stream, write_stream, _ = await streamablehttp_client("http://localhost:8000/mcp")
    async with DummyClientSession(read_stream, write_stream) as session:
        await session.initialize()
        tools = await session.list_tools()
        print(f"使える tool: {[tool.name for tool in tools.tools]}")

# 非同期関数を実行する
import asyncio
asyncio.run(main())
