"""掛け算の tool と、メッセージをそのまま返す resource を持つ最小限の MCP サーバー。"""
# server.py
from urllib.parse import unquote

from mcp.server.fastmcp import FastMCP

# MCP サーバーを作る
# `mcp run server.py` は、このファイルの中から FastMCP のオブジェクト（変数 mcp）を探して起動する。
# そのため、Chapter02 のように自分で stdin を読むループや if __name__ == "__main__" を書かなくてよい
mcp: FastMCP = FastMCP("Demo")


# 掛け算の tool を追加する
# @mcp.tool() を付けるだけで tools/list に載る。関数名が tool 名、docstring が説明、
# 引数の型ヒントが inputSchema になるので、Chapter02 のように JSON を手で組み立てなくてよい
@mcp.tool()
def multiply(first: int, second: int) -> int:
    """2つの数を掛け算する。

    Parameters
    ----------
    first : int
        掛けられる数。
    second : int
        掛ける数。

    Returns
    -------
    int
        first と second の積。
    """
    return first * second


# 動的な挨拶の resource を追加する
# URI に {message} のような変数を含めると「resource template」になる。
# クライアントが echo://hello を読むと、hello が引数 message に入ってこの関数が呼ばれる
@mcp.resource("echo://{message}")
def get_greeting(message: str) -> str:
    """メッセージをそのまま返す。

    Parameters
    ----------
    message : str
        返すメッセージ。URI の {message} 部分から渡される。

    Returns
    -------
    str
        メッセージを含むエコーの文字列。
    """
    # URI に使えるのは ASCII 文字だけなので、日本語などはクライアントが %E3%81%93... の形にエンコードして送ってくる。
    # そのまま返すと読めないので、元の文字に戻す
    return f"リソースのエコー: {unquote(message)}!"
