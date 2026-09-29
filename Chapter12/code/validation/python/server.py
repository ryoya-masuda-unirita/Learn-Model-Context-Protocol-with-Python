"""pydantic モデルで tool の入力を検証する MCP サーバー。"""
import sys
from mcp.server.fastmcp import FastMCP
from uuid import uuid4

mcp: FastMCP = FastMCP(name="Tool Example")

from pydantic import BaseModel

class User(BaseModel):
    """ユーザー。"""

    id: int
    name: str
    email: str

users: list[User] = []

@mcp.tool()
def create_user(user: User) -> User:
    """ユーザーを作成する。

    入力は User モデルで検証されるので、必須のフィールドがなければエラーになる。

    Parameters
    ----------
    user : User
        作成するユーザー。id は採番し直す。

    Returns
    -------
    User
        作成したユーザー。
    """
    # ユーザーを作成する処理をここに書く
    user.id = len(users) + 1
    users.append(user)
    return user

@mcp.tool()
def sum(a: int, b: int) -> int:
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

if __name__ == "__main__":
    # stdio では stdout が MCP の通信に使われるので、メッセージは stderr に出す
    print("MCP サーバーを起動しています...", file=sys.stderr)
    mcp.run()