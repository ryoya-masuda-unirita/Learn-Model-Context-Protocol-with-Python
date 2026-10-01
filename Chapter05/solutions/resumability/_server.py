"""resumability に対応した Streamable HTTP の MCP サーバー（MCP SDK のサンプルを元にしたもの）。

click のコマンドとして、ポートやログレベルを指定して起動できる。
"""
import contextlib
import logging
from collections.abc import AsyncIterator
from typing import Any

import anyio
import click
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from pydantic import AnyUrl
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount
from starlette.types import ASGIApp, Receive, Scope, Send

from event_store import InMemoryEventStore

# ログを設定する
logger: logging.Logger = logging.getLogger(__name__)


@click.command()
@click.option("--port", default=3000, help="HTTP で待ち受けるポート")
@click.option(
    "--log-level",
    default="INFO",
    help="ログレベル（DEBUG、INFO、WARNING、ERROR、CRITICAL）",
)
@click.option(
    "--json-response",
    is_flag=True,
    default=False,
    help="SSE ストリームの代わりに JSON レスポンスを返す",
)
def main(
    port: int,
    log_level: str,
    json_response: bool,
) -> int:
    """ポートとログレベルを指定して、resumability に対応した Streamable HTTP の MCP サーバーを起動する。

    Parameters
    ----------
    port : int
        HTTP で待ち受けるポート。
    log_level : str
        ログレベル（DEBUG、INFO、WARNING、ERROR、CRITICAL）。
    json_response : bool
        True なら SSE ストリームの代わりに JSON レスポンスを返す。

    Returns
    -------
    int
        終了コード（常に 0）。
    """
    # ログを設定する
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    app = Server("mcp-streamable-http-demo")

    @app.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.ContentBlock]:
        """指定した件数の通知を、指定した間隔で送る。

        Parameters
        ----------
        name : str
            呼び出された tool の名前。
        arguments : dict[str, Any]
            tool に渡された引数。interval（秒）、count（件数）、caller（呼び出し元）を使う。

        Returns
        -------
        list[types.ContentBlock]
            送った通知の件数と間隔を伝えるテキスト。
        """
        ctx = app.request_context
        interval = arguments.get("interval", 1.0)
        count = arguments.get("count", 5)
        caller = arguments.get("caller", "不明")

        # 指定した間隔で、指定した数の通知を送る
        for i in range(count):
            # resumability のデモ用に、詳しいメッセージを含める
            notification_msg = f"[{i + 1}/{count}] '{caller}' からのイベント - 切断された場合は Last-Event-ID を使って再開できます"
            await ctx.session.send_log_message(
                level="info",
                data=notification_msg,
                logger="notification_stream",
                # この通知を元のリクエストに関連付ける
                # 通知が正しいレスポンスストリームに送られるようにする
                # これがないと、通知の送り先は次のどちらかになる：
                # - 独立した SSE ストリーム（GET リクエストに対応している場合）
                # - どこにも送られない（GET リクエストに対応していない場合）
                related_request_id=ctx.request_id,
            )
            logger.debug(f"通知を送信しました {i + 1}/{count}（呼び出し元: {caller}）")
            if i < count - 1:  # 最後の通知の後は待たない
                await anyio.sleep(interval)

        # GET リクエストで確立した独立した SSE を通じて、
        # resource の通知を送る
        await ctx.session.send_resource_updated(uri=AnyUrl("http:///test_resource"))
        return [
            types.TextContent(
                type="text",
                text=(f"{interval} 秒間隔で {count} 件の通知を送信しました（呼び出し元: {caller}）"),
            )
        ]

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        """公開する tool の一覧を返す。

        Returns
        -------
        list[types.Tool]
            start-notification-stream tool の定義。
        """
        return [
            types.Tool(
                name="start-notification-stream",
                description=("件数と間隔を指定して、通知をストリームで送る"),
                inputSchema={
                    "type": "object",
                    "required": ["interval", "count", "caller"],
                    "properties": {
                        "interval": {
                            "type": "number",
                            "description": "通知の間隔（秒）",
                        },
                        "count": {
                            "type": "number",
                            "description": "送る通知の数",
                        },
                        "caller": {
                            "type": "string",
                            "description": ("通知に含める呼び出し元の識別子"),
                        },
                    },
                },
            )
        ]

    # resumability 用のイベントストアを作る
    # InMemoryEventStore で、StreamableHTTP transport の resumability に対応できる。
    # SSE イベントを一意な ID 付きで保存するので、クライアントは次のことができる：
    #   1. SSE メッセージごとにイベント ID を受け取る
    #   2. GET リクエストで Last-Event-ID を送り、ストリームを再開する
    #   3. 再接続後に、受け取り損ねたイベントを再生する
    # 注意：このインメモリ実装はデモ専用。
    # 本番環境では永続化ストレージを使うこと。
    event_store = InMemoryEventStore()

    # アプリとイベントストアを使ってセッションマネージャーを作る
    session_manager = StreamableHTTPSessionManager(
        app=app,
        event_store=event_store,  # resumability を有効にする
        json_response=json_response,
    )

    # Streamable HTTP 接続用の ASGI ハンドラー
    async def handle_streamable_http(scope: Scope, receive: Receive, send: Send) -> None:
        """Streamable HTTP のリクエストをセッションマネージャーに渡す。

        Parameters
        ----------
        scope : Scope
            ASGI のスコープ。
        receive : Receive
            ASGI の受信関数。
        send : Send
            ASGI の送信関数。
        """
        await session_manager.handle_request(scope, receive, send)

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        """セッションマネージャーのライフサイクルを管理するコンテキストマネージャー。

        Parameters
        ----------
        app : Starlette
            対象の Starlette アプリケーション。

        Yields
        ------
        None
            セッションマネージャーが動いている間、制御をアプリケーションに渡す。
        """
        async with session_manager.run():
            logger.info("StreamableHTTP セッションマネージャー付きでアプリケーションを起動しました！")
            try:
                yield
            finally:
                logger.info("アプリケーションを終了しています...")

    # transport を使って ASGI アプリケーションを作る
    starlette_app: ASGIApp = Starlette(
        debug=True,
        routes=[
            Mount("/mcp", app=handle_streamable_http),
        ],
        lifespan=lifespan,
    )

    # ブラウザベースのクライアントに Mcp-Session-Id ヘッダーを公開するため、ASGI アプリケーションを
    # CORS middleware で包む（500 エラーにも正しい CORS ヘッダーが付くようにする）
    starlette_app = CORSMiddleware(
        starlette_app,
        allow_origins=["*"],  # すべてのオリジンを許可する（本番環境では必要に応じて調整する）
        allow_methods=["GET", "POST", "DELETE"],  # MCP の Streamable HTTP で使うメソッド
        expose_headers=["Mcp-Session-Id"],
    )

    import uvicorn

    uvicorn.run(starlette_app, host="127.0.0.1", port=port)

    return 0


# main() は click のコマンドなので、呼び出すとコマンドライン引数（--port など）を読んでから実行される。
# これがないと、python _server.py で実行しても何も起動せずに終わる
if __name__ == "__main__":
    main()