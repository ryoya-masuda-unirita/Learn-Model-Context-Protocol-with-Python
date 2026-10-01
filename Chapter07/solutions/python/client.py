"""MCP サーバー（server.py）に stdio で接続し、コマンドで tool を呼び出す対話型クライアント。"""
from typing import Any

from pathlib import Path

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# 'server.py' とだけ書くとカレントディレクトリから探されるため、リポジトリのルートなど
# 別の場所から実行するとサーバーが起動できない。このファイルの場所を基準に絶対パスにする
SERVER_PATH: Path = Path(__file__).resolve().parent / "server.py"

# stdio 接続用のサーバーパラメーターを作る
# stdio_client はこのコマンドでサーバーを子プロセスとして起動し、stdin / stdout をつなぐ（Chapter02 で手で書いたことを SDK がやる）
server_params: StdioServerParameters = StdioServerParameters(
    command="mcp",  # 実行ファイル
    args=["run", str(SERVER_PATH)],  # コマンドライン引数（任意）
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

            tools: list[dict[str, Any]] = []

            for mcp_tool in mcp_tools.tools:
                print("tool: ", mcp_tool.name)
                tools.append({
                    "name": mcp_tool.name,
                    "description": mcp_tool.description,
                    "parameters": mcp_tool.inputSchema
                })

            while True:
                command = input("コマンドを入力してください（'quit' で終了）: ")
                if command == "quit":
                    break
                # 必要に応じて、ほかのコマンドも処理する

                # コマンドが tool 名なら、その tool を呼び出す
                if command in [tool["name"] for tool in tools]:
                    # tool を探す
                    selected = next((t for t in tools if t["name"] == command), None)
                    if selected:
                        print(f"使用する tool: {selected['name']}")

                        # tool に渡す引数を用意する
                        arguments: dict[str, Any] = {}
                        print("tool の引数:", selected["parameters"])
                        # inputSchema の properties を見れば、tool がどんな引数を受け取るかがわかる
                        # input() の値は文字列なので、数値の引数の tool では型が合わずにエラーになる点に注意
                        for param in selected["parameters"]["properties"]:
                            print(f"パラメーター: {param}")
                            arguments[param] = input(f"{param} を入力してください: ")

                        result = await session.call_tool(selected["name"], arguments=arguments)

                        print("結果: ", result.content)




if __name__ == "__main__":
    import asyncio

    asyncio.run(run())