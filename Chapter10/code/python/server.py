from pydantic import BaseModel, Field

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

from starlette.applications import Starlette
from starlette.routing import Mount, Host

mcp = FastMCP(name="Elicitation Example")

# TODO: elicitation のサンプル。SSE に対応させる

class BookingPreferences(BaseModel):
    """ユーザーの希望を集めるためのスキーマ。"""

    checkAlternative: bool = Field(description="別の日付を確認しますか？")
    alternativeDate: str = Field(
        default="2024-12-26",
        description="代わりの日付（YYYY-MM-DD）",
    )

def not_available_date(date: str) -> bool:
    # 日付が空いているかのチェックをシミュレートする
    return date != "2024-12-25"


@mcp.tool()
async def book_trip(date: str, ctx: Context[ServerSession, None]) -> str:
    """日付の空きを確認して旅行を予約する。"""
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

app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)

if __name__ == "__main__":
    print("Elicitation サンプルの MCP サーバーを起動しています...")
    mcp.run()