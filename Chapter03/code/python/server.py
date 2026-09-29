# server.py
from mcp.server.fastmcp import FastMCP

# MCP サーバーを作る
mcp = FastMCP("Demo")


# 掛け算の tool を追加する
@mcp.tool()
def multiply(first: int, second: int) -> int:
    """2つの数を掛け算する"""
    return first * second


# 動的な挨拶の resource を追加する
@mcp.resource("echo://{message}")
def get_greeting(message: str) -> str:
    """メッセージをそのまま返す"""
    return f"リソースのエコー: {message}!"
