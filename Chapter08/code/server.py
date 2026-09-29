"""足し算と引き算の tool を持つ MCP サーバー。

VS Code などの MCP ホストから stdio 経由で起動される。
"""
from mcp.server.fastmcp import FastMCP

# MCP サーバーを作る
mcp: FastMCP = FastMCP("Demo")


# 足し算の tool を追加する
@mcp.tool()
def add(a: int, b: int) -> int:
    """2つの数を足し算する。

    Parameters
    ----------
    a : int
        足される数。
    b : int
        足す数。

    Returns
    -------
    int
        a と b の和。
    """
    return a + b

# 引き算の tool を追加する
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """2つの数を引き算する。

    Parameters
    ----------
    a : int
        引かれる数。
    b : int
        引く数。

    Returns
    -------
    int
        a から b を引いた差。
    """
    return a - b

if __name__ == "__main__":
    print("MCP サーバーを起動しています...")
    mcp.run(transport="stdio")