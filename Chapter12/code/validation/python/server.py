from mcp.server.fastmcp import FastMCP
from uuid import uuid4

mcp = FastMCP(name="Tool Example")

from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

users = []

@mcp.tool()
def create_user(user: User):

    # ユーザーを作成する処理をここに書く
    user.id = len(users) + 1
    users.append(user)
    return user

@mcp.tool()
def sum(a: int, b: int) -> int:
    """2つの数を足し算する。"""
    return a + b

if __name__ == "__main__":
    print("MCP サーバーを起動しています...")
    mcp.run()