"""LLM を使って呼び出す tool を決める、MCP サーバー（server.py）のクライアント。

自然言語のプロンプトを LLM に渡し、LLM が選んだ tool を MCP サーバーで実行する。
"""
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from openai import OpenAI
from openai.types.chat import ChatCompletionFunctionToolParam, ChatCompletionMessageFunctionToolCall

# LLM
import os
import json
from typing import Any

# stdio 接続用のサーバーパラメーターを作る
server_params: StdioServerParameters = StdioServerParameters(
    command="mcp",  # 実行ファイル
    args=["run", "server.py"],  # コマンドライン引数（任意）
    env=None,  # 環境変数（任意）
)

def call_llm(prompt: str, functions: list[ChatCompletionFunctionToolParam]) -> list[dict[str, Any]]:
    """LLM にプロンプトと tool の定義を渡し、呼び出すべき tool を決めてもらう。

    Parameters
    ----------
    prompt : str
        ユーザーが入力したプロンプト。
    functions : list[ChatCompletionFunctionToolParam]
        LLM に渡す tool の定義（OpenAI の function calling 形式）のリスト。

    Returns
    -------
    list[dict[str, Any]]
        呼び出すべき tool の名前（name）と引数（args）の辞書のリスト。
    """
    token = os.environ["GITHUB_TOKEN"]
    endpoint = "https://models.github.ai/inference"

    model_name = "gpt-4o"

    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )

    print("LLM を呼び出しています")
    response = client.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": "あなたは親切なアシスタントです。",
            },
            {
            "role": "user",
            "content": prompt,
            },
        ],
        model=model_name,
        tools = functions,
        # 任意のパラメーター
        temperature=1.,
        max_tokens=1000,
        top_p=1.    
    )

    # テキストの応答だけを見たいなら .content を使う
    response_message = response.choices[0].message
    
    functions_to_call = []

    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            # function 形式以外（custom tool）の呼び出しは、このサンプルでは扱わない
            if not isinstance(tool_call, ChatCompletionMessageFunctionToolCall):
                continue
            # print("tool: ", tool_call)
            name = tool_call.function.name
            print("tool 名: ", name)
            args = json.loads(tool_call.function.arguments)
            functions_to_call.append({ "name": name, "args": args })

    return functions_to_call

def convert_to_llm_tool(tool: types.Tool) -> ChatCompletionFunctionToolParam:
    """MCP の tool の定義を、OpenAI の function calling 形式に変換する。

    Parameters
    ----------
    tool : types.Tool
        MCP サーバーから取得した tool の定義。

    Returns
    -------
    ChatCompletionFunctionToolParam
        OpenAI の Chat Completions API の tools に渡せる形式の定義。
    """
    tool_schema: ChatCompletionFunctionToolParam = {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": {
                "type": "object",
                "properties": tool.inputSchema["properties"]
            }
        }
    }

    return tool_schema

async def run() -> None:
    """サーバーに接続し、入力されたプロンプトを LLM に渡して tool を呼び出す。

    'quit' と入力すると終了する。
    """
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # 接続を初期化する
            await session.initialize()

        
          

            # 使える tool の一覧を取得する
            tools = await session.list_tools()
            print("tool の一覧")

            functions: list[ChatCompletionFunctionToolParam] = []

            for tool in tools.tools:
                print("tool: ", tool.name)
                # print("Tool", tool.inputSchema["properties"])
                functions.append(convert_to_llm_tool(tool))
            
            while True:
                print("入力を待っています...（'quit' で終了）")
                prompt = input("プロンプトを入力してください: ")
                if prompt == "quit":
                    break
            
                # どの tool を呼ぶべきか（あれば）LLM に聞く
                functions_to_call = call_llm(prompt, functions)

                # 提案された関数を呼び出す
                for f in functions_to_call:
                    result = await session.call_tool(f["name"], arguments=f["args"])
                    print("tool の結果: ", result.content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())