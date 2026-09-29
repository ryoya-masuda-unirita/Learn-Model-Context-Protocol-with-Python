"""掛け算の tool と、メッセージをそのまま返す resource を持つ最小限の MCP サーバー。"""
# server.py
from mcp.server.fastmcp import FastMCP

# MCP サーバーを作る
mcp: FastMCP = FastMCP("Demo")


# 掛け算の tool を追加する
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
    return f"リソースのエコー: {message}!"
