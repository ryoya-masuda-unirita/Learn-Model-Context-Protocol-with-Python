import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Mount, Route

import tools

# サーバーのインスタンスを作る
server = Server("low-level-server")

def pydantic_to_json(model_cls: type) -> dict:
    schema = model_cls.schema()
    properties = {}
    required = schema.get("required", [])
    for prop, details in schema.get("properties", {}).items():
        properties[prop] = {"type": details.get("type", "string")}
    return {
        "type": "object",
        "properties": properties,
        "required": required
    }

no_params_object = {
    "type": "object",
    "properties": {},
    "required": []  
}

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    tool_list = []
    print(tools)

    for tool in tools.tools.values():
        tool_list.append(
            types.Tool(
                name=tool["name"],
                description=tool["description"],
                inputSchema= pydantic_to_json(tool["input_schema"]) if tool["input_schema"] is not None else no_params_object,
            )
        )
    return tool_list

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, str] | None
) -> list[types.TextContent]:
    
    # tools は tool 名をキーにした辞書
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

sse = SseServerTransport("/messages/")

async def handle_sse(request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await server.run(
            streams[0], streams[1], server.create_initialization_options()
        )
    return Response()

starlette_app = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ],
)

if __name__ == "__main__":
    import uvicorn
    port = 8000
    uvicorn.run(starlette_app, host="127.0.0.1", port=port)

# python server.py で起動する

# テスト方法: npx @modelcontextprotocol/inspector --cli http://localhost:8000/sse --method tools/list

# npx @modelcontextprotocol/inspector --cli http://localhost:8000/sse --method tools/call --tool-name add_to_cart --tool-arg cart_id=1 --tool-arg product_id=2 --tool-arg quantity=3
# npx @modelcontextprotocol/inspector --cli http://localhost:8000/sse --method tools/call --tool-name get_all_categories
