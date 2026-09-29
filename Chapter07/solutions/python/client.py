"""MCP サーバー（server.py）に stdio で接続し、コマンドで tool を呼び出す対話型クライアント。"""
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# stdio 接続用のサーバーパラメーターを作る
server_params: StdioServerParameters = StdioServerParameters(
    command="mcp",  # 実行ファイル
    args=["run", "server.py"],  # コマンドライン引数（任意）
    env=None,  # 環境変数（任意）
)

async def run() -> None:
    """サーバーに接続し、入力されたコマンドに応じて tool を呼び出す。

    tool 名を入力すると、その tool の引数を1つずつ入力させてから呼び出す。
    'quit' と入力すると終了する。
    """
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # 接続を初期化する
            await session.initialize()

            # 使える tool の一覧を取得する
            mcp_tools = await session.list_tools()
            print("tool の一覧")

            tools = []

            for tool in mcp_tools.tools:
                print("tool: ", tool.name)
                tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                })

            while True:
                command = input("コマンドを入力してください（'quit' で終了）: ")
                if command == "quit":
                    break
                # 必要に応じて、ほかのコマンドも処理する

                # コマンドが tool 名なら、その tool を呼び出す
                if command in [tool["name"] for tool in tools]:
                    # tool を探す
                    tool = next((t for t in tools if t["name"] == command), None)
                    if tool:
                        print(f"使用する tool: {tool['name']}")

                        # tool に渡す引数を用意する
                        arguments = {}
                        print("tool の引数:", tool["parameters"])
                        for param in tool["parameters"]["properties"]:
                            print(f"パラメーター: {param}")
                            arguments[param] = input(f"{param} を入力してください: ")

                        result = await session.call_tool(tool["name"], arguments=arguments)

                        print("結果: ", result.content)




if __name__ == "__main__":
    import asyncio

    asyncio.run(run())