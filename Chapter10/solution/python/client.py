"""旅行予約の MCP サーバーに SSE で接続し、elicitation に応答するクライアント（会員登録版）。"""
import asyncio

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.types import CallToolResult, ElicitRequestParams, ElicitResult, TextContent
from mcp.shared.context import RequestContext

# サーバーが ctx.elicit() を呼ぶと、SDK がこの関数を呼ぶ。本来はここでユーザーに入力フォームを見せて答えてもらう。
# このサンプルでは動きを見るため、ユーザーの答えをハードコードしている
async def elicitation_callback_handler(context: RequestContext[ClientSession, None], params: ElicitRequestParams) -> ElicitResult:
    """サーバーからの elicitation のリクエストに、決まった内容で応答する。

    Parameters
    ----------
    context : RequestContext[ClientSession, None]
        リクエストのコンテキスト。
    params : ElicitRequestParams
        サーバーから届いた elicitation のリクエスト。

    Returns
    -------
    ElicitResult
        ユーザーの入力の代わりにハードコードした応答。
    """
    print(f"[CLIENT] elicitation のデータを受信しました: {params.message}")

    # 1. 会員になるのを断る
    # return ElicitResult(action="accept", content={
    #    "become_member": False
    # }) # 予約は行われなかったと返るはず（動作確認済み）

    # 2. 予約をキャンセルする（elicitation のやり取り自体を始めたくない）
    # return ElicitResult(action="decline") 動作確認済み

    print("[CLIENT]: 会員登録します: chris（chris@example.com）")

    # 3. 会員登録して予約する
    return ElicitResult(action="accept", content={
          "become_member": True,
          "name": "chris",
          "email": "chris@example.com"
    }) # 2025-01-02 で予約され、会員登録のお礼が返るはず


    

def first_text(result: CallToolResult) -> str:
    """呼び出した tool の結果から、最初のコンテンツのテキストを取り出す。

    Parameters
    ----------
    result : CallToolResult
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
    if not isinstance(content, TextContent):
        raise ValueError(f"テキスト以外のコンテンツには対応していません: {content.type}")
    return content.text


async def main() -> None:
    """サーバーに接続し、tool の一覧を表示してから book_trip を呼び出す。"""
    # Server-Sent Events (SSE) サーバーに接続する
    async with sse_client(url="http://localhost:3000/sse") as (
        read_stream,
        write_stream
    ):
        # クライアントのストリームを使ってセッションを作る
        async with ClientSession(
            read_stream, 
            write_stream,
            # elicitation_callback を渡すと、initialize でクライアントが elicitation に対応していると伝わる。
            # 渡さないと、サーバーが ctx.elicit() を呼んだときにエラーになる
            elicitation_callback=elicitation_callback_handler) as session:
            # 接続を初期化する
            await session.initialize()
            # 使える tool の一覧を取得する
            tools = await session.list_tools()
            print(f"使える tool: {[tool.name for tool in tools.tools]}")

            # tool を呼び出す
            result = await session.call_tool("book_trip", {
                "date": "2025-01-02",
                "member_id": "guest"
            })
            print("結果: ", first_text(result))


if __name__ == "__main__":
    asyncio.run(main())