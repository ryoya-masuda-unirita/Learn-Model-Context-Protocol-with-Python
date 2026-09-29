"""
`examples/snippets/clients` ディレクトリに移動して、次を実行する：
    uv run client
"""

import asyncio
import os

from pydantic import AnyUrl

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.shared.context import RequestContext

import os
from openai import OpenAI

# stdio 接続用のサーバーパラメーターを作る
server_params = StdioServerParameters(
    command="python",  # python でサーバーを実行する
    args=["server.py"]
)

async def call_llm(prompt: str, system_prompt: str) -> str:
    client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.environ["GITHUB_TOKEN"],
)

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="openai/gpt-4o-mini",
        temperature=1,
        max_tokens=200,
        top_p=1
    )

    return response.choices[0].message.content


# 任意：サンプリングのコールバックを作る
async def handle_sampling_message(
    context: RequestContext[ClientSession, None], params: types.CreateMessageRequestParams
) -> types.CreateMessageResult:
    print(f"サンプリングのリクエスト: {params.messages}")

    message = params.messages[0].content.text
    system_prompt = params.systemPrompt or "あなたは親切なアシスタントです。話題から外れず、話を作りすぎないようにしつつ、必ず魅力的な商品説明を作成してください"

    # TODO: 実際の LLM を呼び出すように、以下を変更する
    response = await call_llm(message, system_prompt)

    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text=response,
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, sampling_callback=handle_sampling_message) as session:
            # 接続を初期化する
            await session.initialize()


            # tool を呼び出す（fastmcp_quickstart の create_product tool）
            result = await session.call_tool("talk_to", arguments={"name": "Monsieur Lestrange", "topic": "あなた自身について教えて"})
            print("結果:", result.content[0].text)


def main():
    """クライアントスクリプトのエントリーポイント。"""
    asyncio.run(run())


if __name__ == "__main__":
    main()