"""elicitation で、空いていない日付の代わりをユーザーに尋ねる旅行予約の MCP サーバー。

`uvicorn server:app` でポート 8000 の SSE サーバーとして起動する。
"""
from pydantic import BaseModel, Field

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

from starlette.applications import Starlette
from starlette.routing import Mount, Host

mcp: FastMCP = FastMCP(name="Elicitation Example")

# TODO: elicitation のサンプル。SSE に対応させる

class BookingPreferences(BaseModel):
    """ユーザーの希望を集めるためのスキーマ。"""

    checkAlternative: bool = Field(description="別の日付を確認しますか？")
    alternativeDate: str = Field(
        default="2024-12-26",
        description="代わりの日付（YYYY-MM-DD）",
    )

def not_available_date(date: str) -> bool:
    """指定した日付が予約できないかを判定する。

    Parameters
    ----------
    date : str
        判定する日付（YYYY-MM-DD）。

    Returns
    -------
    bool
        予約できなければ True。このサンプルでは 2024-12-25 以外はすべて予約できない。
    """
    # 日付が空いているかのチェックをシミュレートする
    return date != "2024-12-25"


@mcp.tool()
async def book_trip(date: str, ctx: Context[ServerSession, None]) -> str:
    """日付の空きを確認して旅行を予約する。

    日付が空いていなければ、elicitation でユーザーに別の日付を尋ねる。

    Parameters
    ----------
    date : str
        予約したい日付（YYYY-MM-DD）。
    ctx : Context[ServerSession, None]
        MCP のリクエストコンテキスト。elicitation に使う。

    Returns
    -------
    str
        予約の結果を表すメッセージ。
    """
    # 日付が空いているか確認する
    if not_available_date(date):
        # 日付が空いていない - ユーザーに代わりの日付を尋ねる
        result = await ctx.elicit(
            message=(f"{date} に予約できる旅行はありません。別の日付を試しますか？"),
            schema=BookingPreferences,
        )

        if result.action == "accept" and result.data:
            if result.data.checkAlternative:
                return f"[SUCCESS] {result.data.alternativeDate} で予約しました"
            return "[CANCELLED] 予約は行われませんでした"
        return "[CANCELLED] 予約はキャンセルされました"

    # 日付が空いている
    return f"[SUCCESS] {date} で予約しました"

app: Starlette = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)

if __name__ == "__main__":
    print("Elicitation サンプルの MCP サーバーを起動しています...")
    mcp.run()