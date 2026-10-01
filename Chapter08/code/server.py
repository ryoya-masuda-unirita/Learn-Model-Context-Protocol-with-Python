"""足し算と引き算の tool を持つ MCP サーバー。

VS Code などの MCP ホストから stdio 経由で起動される。
"""
import sys
from mcp.server.fastmcp import FastMCP

# MCP サーバーを作る
mcp: FastMCP = FastMCP("Demo")


# 足し算の tool を追加する
# VS Code の Copilot などのホストは、tools/list で受け取った名前と docstring（説明）を LLM に見せる。
# LLM は説明を読んで「足し算が必要だ」と判断したときに、この tool を呼び出す
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
    # stdio では stdout が MCP の通信に使われるので、メッセージは stderr に出す
    print("MCP サーバーを起動しています...", file=sys.stderr)
    # ホスト（VS Code など）がこのファイルを子プロセスとして起動し、stdin / stdout でやり取りする。
    # ホストの設定には、カレントディレクトリに左右されないよう server.py を絶対パスで書くのが確実
    mcp.run(transport="stdio")