from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp.server import FastMCP
from typing import Any, Literal
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.applications import Starlette
from starlette.routing import Mount

import asyncio
import datetime

from dotenv import load_dotenv
import os
from util import validate_token
load_dotenv()

settings = {
    "host": "localhost",
    "port": 8000,
    "mcp_scope": "mcp:read",
    "server_url": AnyHttpUrl("http://localhost:8000"),
}

users = ["User Userson", "Admin Adminson"]

def is_user(token: str) -> bool:
    decodedToken = validate_token(token[7:])
    if not decodedToken:
        return False
    return decodedToken["name"] in users

def has_scope(token: str, scope: str) -> bool:
    token = token[7:]
    token = validate_token(token)

    if not token:
        return False
    # とても単純な scope のチェック。実際にはトークンをきちんと解析して scope を確認する
    return  scope in token["scopes"]

def validate_jwt(token: str) -> bool:
    token = token[7:]
    # print("トークンを検証しています:", token)
    return validate_token(token) != None
   

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        has_header = request.headers.get("Authorization")
        # print("Authorization ヘッダー:", has_header)
        if not has_header:
            print("-> Authorization ヘッダーがありません！")
            return Response(status_code=401, content="認証されていません")

        if not validate_jwt(has_header):
            print("-> トークンが無効です！")
            return Response(status_code=403, content="アクセスが拒否されました")

        print("有効なトークンです。処理を続けます...")

        if not is_user(has_header):
            print("-> ユーザーが存在しません！")
            return Response(status_code=403, content="アクセスが拒否されました - ユーザーが存在しません")
        print("ユーザーが存在します。処理を続けます...")

        if not has_scope(has_header, "Admin.Write"):
            print("-> 必要な scope がありません！")
            return Response(status_code=403, content="アクセスが拒否されました - scope が不足しています")

        print("ユーザーは必要な scope を持っています。処理を続けます...")

        print(f"-> 受信: {request.method} {request.url}")
        response = await call_next(request)
        response.headers['Custom'] = 'Example'
        return response

app = FastMCP(
    name="MCP Resource Server",
    instructions="認可サーバーの introspection でトークンを検証するリソースサーバー",
    host=settings["host"],
    port=settings["port"],
    debug=True
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

async def main():
    print("MCP リソースサーバーを実行しています...")
    starlette_app = await setup(app)
    print("カスタム middleware を追加しています...")
    starlette_app.add_middleware(CustomHeaderMiddleware)

    await run(starlette_app)

if __name__ == "__main__":
    asyncio.run(main())