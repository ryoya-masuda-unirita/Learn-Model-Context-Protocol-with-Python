"""low-level の Server クラスで作り、SSE で公開する MCP サーバー。

`python server.py` でポート 8000 で起動する。
"""
from typing import Any

import mcp.types as types
from pydantic import BaseModel
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, Route

# tools はこのファイルと同じディレクトリにあるパッケージ。python server.py で実行すると、
# スクリプトのディレクトリが import の検索パスに入るので、どこから実行しても見つかる
import tools

# サーバーのインスタンスを作る
# low-level の Server は、FastMCP のように関数から tool を自動で作らない。
# tools/list の応答も tools/call の振り分けも自分で書くので手間は増えるが、MCP のメッセージとの対応が見えやすい
server: Server = Server("low-level-server")

def pydantic_to_json(model_cls: type[BaseModel]) -> dict[str, Any]:
    """入力を表す pydantic モデルから、tool の inputSchema 用の JSON Schema を作る。

    各プロパティは型（type）だけを残した簡易的なスキーマにする。

    Parameters
    ----------
    model_cls : type[BaseModel]
        入力を表す pydantic モデルのクラス。

    Returns
    -------
    dict[str, Any]
        type、properties、required を持つ JSON Schema。
    """
    # pydantic のモデルから JSON Schema を作れるので、inputSchema を手で書かずに済む。
    # クライアント（LLM）は、このスキーマを見て tool に渡す引数を組み立てる
    schema = model_cls.model_json_schema()
    properties = {}
    required = schema.get("required", [])
    for prop, details in schema.get("properties", {}).items():
        properties[prop] = {"type": details.get("type", "string")}
    return {
        "type": "object",
        "properties": properties,
        "required": required
    }

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """登録されている tool（tools パッケージ）の一覧を返す。

    Returns
    -------
    list[types.Tool]
        公開する tool の定義のリスト。
    """
    tool_list = []
    print(tools)

    for tool in tools.tools.values():
        tool_list.append(
            types.Tool(
                name=tool["name"],
                description=tool["description"],
                inputSchema=pydantic_to_json(tool["input_schema"]),
            )
        )
    return tool_list

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, str] | None
) -> list[types.TextContent]:
    """指定された tool のハンドラーを呼び出し、結果をテキストで返す。

    Parameters
    ----------
    name : str
        呼び出す tool の名前。
    arguments : dict[str, str] | None
        tool に渡す引数。

    Returns
    -------
    list[types.TextContent]
        tool の結果を文字列にしたテキスト。

    Raises
    ------
    ValueError
        tool が存在しない場合、または tool の呼び出しでエラーが発生した場合。
    """
    # tools は tool 名をキーにした辞書
    # low-level の Server では、どの tool が呼ばれてもこの関数に来るので、name で振り分ける
    if name not in tools.tools:
        raise ValueError(f"不明な tool です: {name}")
    
    tool = tools.tools[name]

    result = "default"
    try:
        result = await tool["handler"](arguments)
    except Exception as e:
        raise ValueError(f"tool {name} の呼び出しでエラーが発生しました: {str(e)}")

    return [
        types.TextContent(type="text", text=str(result))
    ]   

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """公開する prompt の一覧を返す。

    Returns
    -------
    list[types.Prompt]
        example-prompt の定義。
    """
    return [
        types.Prompt(
            name="example-prompt",
            description="サンプルの prompt テンプレート",
            arguments=[
                types.PromptArgument(
                    name="arg1", description="サンプルの引数", required=True
                )
            ],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """指定された prompt の内容を返す。

    Parameters
    ----------
    name : str
        取得する prompt の名前。
    arguments : dict[str, str] | None
        prompt に渡す引数（このサンプルでは使わない）。

    Returns
    -------
    types.GetPromptResult
        prompt の説明とメッセージ。

    Raises
    ------
    ValueError
        prompt が存在しない場合。
    """
    if name != "example-prompt":
        raise ValueError(f"不明な prompt です: {name}")

    return types.GetPromptResult(
        description="サンプルの prompt",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text="サンプルの prompt のテキスト"),
            )
        ],
    )

# SSE トランスポートを自分で組み立てる（FastMCP の sse_app() がやっていることを手で書いている）。
#   GET  /sse        : 接続を開きっぱなしにし、サーバー → クライアントのメッセージを流す
#   POST /messages/  : クライアント → サーバーのメッセージを受け取る
# 引数の "/messages/" は、/sse に接続したクライアントへ「ここに POST して」と伝える URL
sse: SseServerTransport = SseServerTransport("/messages/")

async def handle_sse(request: Request) -> Response:
    """SSE の接続を受け付け、接続が続く間 MCP サーバーを動かす。

    Parameters
    ----------
    request : Request
        /sse への HTTP リクエスト。

    Returns
    -------
    Response
        接続が終わった後に返す空のレスポンス。
    """
    # 1つの SSE 接続が1つの MCP セッションになる。接続が続く間 server.run() が動き、切断されると抜ける
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await server.run(
            streams[0], streams[1], server.create_initialization_options()
        )
    return Response()

starlette_app: Starlette = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ],
)

import uvicorn

port: int = 8000

# if __name__ == "__main__" で囲んでいないので、このファイルを import しただけでサーバーが起動する点に注意
uvicorn.run(starlette_app, host="127.0.0.1", port=port)

# python server.py で起動する

# テスト方法: npx @modelcontextprotocol/inspector --cli http://localhost:8000/sse --method tools/list

# npx @modelcontextprotocol/inspector --cli http://localhost:8000/sse --method tools/call --tool-name add --tool-arg a=1 --tool-arg b=2
