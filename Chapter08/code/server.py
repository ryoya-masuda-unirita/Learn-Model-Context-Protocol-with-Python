from mcp.server.fastmcp import FastMCP

# MCP サーバーを作る
mcp = FastMCP("Demo")


# 足し算の tool を追加する
@mcp.tool()
def add(a: int, b: int) -> int:
    """2つの数を足し算する"""
    return a + b

# 引き算の tool を追加する
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """2つの数を引き算する"""
    return a - b

if __name__ == "__main__":
    print("MCP サーバーを起動しています...")
    mcp.run(transport="stdio")