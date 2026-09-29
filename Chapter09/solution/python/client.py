"""MCP サーバー（server.py）に stdio で接続し、サンプリングのリクエストに LLM で応えるクライアント。

LLM は Amazon Bedrock の OpenAI 互換 API 経由で呼び出す。
実行には、Bedrock を使える AWS の認証情報が必要（例: `AWS_PROFILE=oic uv run python client.py`）。
"""

import asyncio

from pydantic import AnyUrl

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.shared.context import RequestContext

from aws_bedrock_token_generator import provide_token
from openai import OpenAI
from openai.types.shared import ReasoningEffort

# Amazon Bedrock の OpenAI 互換エンドポイント（bedrock-mantle）と、使うモデル
BEDROCK_REGION: str = "us-east-1"
BEDROCK_BASE_URL: str = f"https://bedrock-mantle.{BEDROCK_REGION}.api.aws/openai/v1"
BEDROCK_MODEL_ID: str = "openai.gpt-5.5"
# GPT-5.5 は推論してから本文を書く。文章を書くだけのこの用途では推論は不要なので止め、
# max_tokens をすべて本文に使えるようにする（推論で上限を使い切ると本文が空になるため）
REASONING_EFFORT: ReasoningEffort = "none"

# stdio 接続用のサーバーパラメーターを作る
server_params: StdioServerParameters = StdioServerParameters(
    command="python",  # python でサーバーを実行する
    args=["server.py"]
)

async def call_llm(prompt: str, system_prompt: str) -> str:
    """LLM にプロンプトを送り、生成されたテキストを返す。

    Parameters
    ----------
    prompt : str
        ユーザーのプロンプト。
    system_prompt : str
        システムプロンプト。

    Returns
    -------
    str
        LLM が生成したテキスト。

    Raises
    ------
    RuntimeError
        LLM から本文が返ってこなかった場合。
    """
    # Bedrock の API キーとして、AWS の認証情報（AWS_PROFILE など）から短期トークンを作る
    client = OpenAI(
        base_url=BEDROCK_BASE_URL,
        api_key=provide_token(region=BEDROCK_REGION),
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
        model=BEDROCK_MODEL_ID,
        reasoning_effort=REASONING_EFFORT,
        temperature=1,
        max_tokens=200,
        top_p=1
    )

    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("LLM から本文が返ってきませんでした")
    return content


# 任意：サンプリングのコールバックを作る
async def handle_sampling_message(
    context: RequestContext[ClientSession, None], params: types.CreateMessageRequestParams
) -> types.CreateMessageResult:
    """サーバーからのサンプリングのリクエストを、LLM を呼び出して処理する。

    Parameters
    ----------
    context : RequestContext[ClientSession, None]
        リクエストのコンテキスト。
    params : types.CreateMessageRequestParams
        サーバーから届いたサンプリングのリクエスト。

    Returns
    -------
    types.CreateMessageResult
        LLM が生成したテキストを含む応答。

    Raises
    ------
    ValueError
        リクエストの内容がテキストでない場合。
    """
    print(f"サンプリングのリクエスト: {params.messages}")

    request_content = params.messages[0].content
    if not isinstance(request_content, types.TextContent):
        raise ValueError("テキスト以外のサンプリングのリクエストには対応していません")
    message = request_content.text
    system_prompt = params.systemPrompt or "あなたは親切なアシスタントです。話題から外れず、話を作りすぎないようにしつつ、必ず魅力的な商品説明を作成してください"

    # TODO: 実際の LLM を呼び出すように、以下を変更する
    response = await call_llm(message, system_prompt)

    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text=response,
        ),
        model=BEDROCK_MODEL_ID,
        stopReason="endTurn",
    )


def first_text(result: types.CallToolResult) -> str:
    """呼び出した tool の結果から、最初のコンテンツのテキストを取り出す。

    Parameters
    ----------
    result : types.CallToolResult
        tool の呼び出し結果。

    Returns
    -------
    str
        最初のコンテンツのテキスト。

    Raises
    ------
    ValueError
        最初のコンテンツがテキストでない場合（画像などが返ってきた場合）。
    """
    content = result.content[0]
    if not isinstance(content, types.TextContent):
        raise ValueError(f"テキスト以外のコンテンツには対応していません: {content.type}")
    return content.text


async def run() -> None:
    """サーバーに接続し、tool を呼び出して結果を表示する。"""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, sampling_callback=handle_sampling_message) as session:
            # 接続を初期化する
            await session.initialize()


            # tool を呼び出す（fastmcp_quickstart の create_product tool）
            result = await session.call_tool("talk_to", arguments={"name": "Monsieur Lestrange", "topic": "あなた自身について教えて"})
            print("結果:", first_text(result))


def main() -> None:
    """クライアントスクリプトのエントリーポイント。"""
    asyncio.run(run())


if __name__ == "__main__":
    main()