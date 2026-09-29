"""固定のトークンで認証する middleware を付けた、Streamable HTTP の MCP サーバー。"""
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp.server import FastMCP
from typing import Any, Literal
from starlette.middleware import Middleware
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
import asyncio
import datetime

settings: dict[str, Any] = {
    "host": "localhost",
    "port": 8000,
    "auth_server_url": AnyHttpUrl("http://localhost:8001"),
    "mcp_scope": "mcp:read",
    "server_url": AnyHttpUrl("http://localhost:8000"),
}

def valid_token(token: str) -> bool:
    """有効なトークンかどうかを、Authorization ヘッダーの値で判定する。

    Parameters
    ----------
    token : str
        Authorization ヘッダーの値（"Bearer <トークン>"）。

    Returns
    -------
    bool
        トークンが "secret-token" なら True。
    """
    # "Bearer " という接頭辞を取り除く
    if token.startswith("Bearer "):
        token = token[7:]
        return token == "secret-token"
    return False

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    """Authorization ヘッダーのトークンを検証する middleware。"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """トークン（Authorization ヘッダー）を検証してから、次の処理に渡す。

        Parameters
        ----------
        request : Request
            受け取った HTTP リクエスト。
        call_next : RequestResponseEndpoint
            次の middleware またはアプリケーションを呼び出す関数。

        Returns
        -------
        Response
            検証に失敗した場合は 401 / 403 のレスポンス。成功した場合は後続の処理のレスポンス。
        """
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


app: FastMCP = FastMCP(
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

    Returns
    -------
    dict[str, Any]
        現在時刻（ISO 形式）、タイムゾーン、UNIX タイムスタンプ、整形した日時。
    """
    now = datetime.datetime.now()

    return {
        "current_time": now.isoformat(),
        "timezone": "UTC",  # デモ用に簡略化している
        "timestamp": now.timestamp(),
        "formatted": now.strftime("%Y-%m-%d %H:%M:%S"),
    }

async def setup(app: FastMCP) -> Starlette:
    """StreamableHTTP transport 用の Starlette アプリケーションを作る。

    Parameters
    ----------
    app : FastMCP
        公開する MCP サーバー。

    Returns
    -------
    Starlette
        Streamable HTTP で MCP サーバーを公開する ASGI アプリケーション。
    """
    starlette_app = app.streamable_http_app()
    return starlette_app

async def run(starlette_app: Starlette) -> None:
    """指定した ASGI アプリケーションを uvicorn で起動する。

    Parameters
    ----------
    starlette_app : Starlette
        起動する ASGI アプリケーション。
    """
    import uvicorn
    config = uvicorn.Config(
            starlette_app,
            host=app.settings.host,
            port=app.settings.port,
            log_level=app.settings.log_level.lower(),
        )
    server = uvicorn.Server(config)
    await server.serve()


middleware: list[Middleware] = [
    Middleware(CustomHeaderMiddleware, header_value='Customized')
]

async def main() -> None:
    """アプリケーションを作り、トークンを検証する middleware を追加してから起動する。"""
    print("MCP リソースサーバーを実行しています...")
    starlette_app = await setup(app)
    print("カスタム middleware を追加しています...")
    starlette_app.add_middleware(CustomHeaderMiddleware)

    await run(starlette_app)

if __name__ == "__main__":
    asyncio.run(main())