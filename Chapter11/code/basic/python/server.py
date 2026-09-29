from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp.server import FastMCP
from typing import Any, Literal
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import asyncio
import datetime

settings = {
    "host": "localhost",
    "port": 8000,
    "auth_server_url": AnyHttpUrl("http://localhost:8001"),
    "mcp_scope": "mcp:read",
    "server_url": AnyHttpUrl("http://localhost:8000"),
}

def valid_token(token: str) -> bool:
    # "Bearer " という接頭辞を取り除く
    if token.startswith("Bearer "):
        token = token[7:]
        return token == "secret-token"
    return False

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        has_header = request.headers.get("Authorization")
        if not has_header:
            print("-> Authorization ヘッダーがありません！")
            return Response(status_code=401, content="認証されていません")

        if not valid_token(has_header):
            print("-> トークンが無効です！")
            return Response(status_code=403, content="アクセスが拒否されました")

        print("有効なトークンです。処理を続けます...")
        print(f"-> 受信: {request.method} {request.url}")
        response = await call_next(request)
        response.headers['Custom'] = 'Example'
        return response


app = FastMCP(
    name="MCP Resource Server",
    instructions="認可サーバーの introspection でトークンを検証するリソースサーバー",
    host=settings["host"],
    port=settings["port"],
    debug=True,
)

@app.tool()
async def get_time() -> dict[str, Any]:
    """
    サーバーの現在時刻を取得する。

    この tool は、システム情報を OAuth 認証で保護できることを示す。
    アクセスするには、ユーザーが認証されている必要がある。
    """

    now = datetime.datetime.now()

    return {
        "current_time": now.isoformat(),
        "timezone": "UTC",  # デモ用に簡略化している
        "timestamp": now.timestamp(),
        "formatted": now.strftime("%Y-%m-%d %H:%M:%S"),
    }

async def setup(app) -> None:
    """StreamableHTTP transport でサーバーを実行する。"""
    

    starlette_app = app.streamable_http_app()
    return starlette_app

async def run(starlette_app):
    import uvicorn
    config = uvicorn.Config(
            starlette_app,
            host=app.settings.host,
            port=app.settings.port,
            log_level=app.settings.log_level.lower(),
        )
    server = uvicorn.Server(config)
    await server.serve()


middleware = [
    Middleware(CustomHeaderMiddleware, header_value='Customized')
]

async def main():
    print("MCP リソースサーバーを実行しています...")
    starlette_app = await setup(app)
    print("カスタム middleware を追加しています...")
    starlette_app.add_middleware(CustomHeaderMiddleware)

    await run(starlette_app)

if __name__ == "__main__":
    asyncio.run(main())