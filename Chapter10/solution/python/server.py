"""elicitation で、会員でないユーザーに会員登録を勧める旅行予約の MCP サーバー。

`uvicorn server:app --port 3000` で SSE サーバーとして起動する。
"""
import sys
from pydantic import BaseModel, Field, EmailStr

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

from starlette.applications import Starlette
from starlette.routing import Mount, Host

mcp: FastMCP = FastMCP(name="Elicitation Example")

# elicitation で使えるのは、文字列・数値・真偽値などの単純な型のフィールドだけ（ネストしたオブジェクトは不可）。
# クライアントが簡単な入力フォームとして表示できるようにするための制限
class MemberPreferences(BaseModel):
    """ユーザーの希望を集めるためのスキーマ。"""

    become_member: bool = Field(description="割引を受けられる会員になりますか？")
    name: str = Field(
        default="",
        description="あなたの名前"
    )
    email: str = Field(
        default="",
        description="あなたのメールアドレス"
    )

@mcp.tool()
async def book_trip(date: str, member_id: str, ctx: Context[ServerSession, None]) -> str:
    """旅行を予約する。会員かどうかを確認し、会員でなければ登録を勧める。

    会員でなければ、elicitation でユーザーに会員登録するかを尋ねる。

    Parameters
    ----------
    date : str
        予約したい日付（YYYY-MM-DD）。
    member_id : str
        会員 ID。会員でなければ "guest"。
    ctx : Context[ServerSession, None]
        MCP のリクエストコンテキスト。elicitation に使う。

    Returns
    -------
    str
        予約の結果を表すメッセージ。
    """
    # 会員かどうか確認する
    if not member_id or member_id == "guest":
        # 会員ではない - ユーザーに登録するか尋ねる
        # elicitation は「サーバー → クライアント」へのリクエスト。ユーザーに追加の入力を求める。
        # schema に渡したモデルが JSON Schema になってクライアントに届き、クライアントはそれを元に入力フォームなどを出す。
        # ユーザーが答えるまで、tool の処理はここで止まって待つ
        result = await ctx.elicit(
            message=(f"会員ではありませんか？ 会員登録しますか？"),
            schema=MemberPreferences,
        )

        # action は accept（入力して送信）/ decline（断った）/ cancel（閉じた）のどれか。
        # accept 以外では data は入ってこない
        if result.action == "accept" and result.data:
            if result.data.become_member and result.data.name and result.data.email:
                return f"[BOOKED] {date} で予約しました。{result.data.name} さん、会員登録ありがとうございます！"
            return f"[BOOKED] {date} で予約しました。会員登録したくなったら www.example.com から登録できます。"
        return f"[BOOKED] {date} で予約しました。会員登録は www.example.com からできます。"

    # 会員である
    return f"[SUCCESS] 会員 {member_id} として {date} で予約しました"

app: Starlette = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)

if __name__ == "__main__":
    # python server.py でも、クライアントが接続しにいく SSE のサーバーとして起動する。
    # 以前は mcp.run()（stdio）を呼んでいたため、python で起動するとクライアントが接続できなかった
    print("Elicitation サンプルの MCP サーバーを起動しています...", file=sys.stderr)
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=3000)