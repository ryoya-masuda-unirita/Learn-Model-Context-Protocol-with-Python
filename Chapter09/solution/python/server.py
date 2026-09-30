"""キャラクターになりきって話す tool を持つ MCP サーバー。

characters.json のキャラクター設定を使い、応答の生成をクライアントの LLM に依頼する。
"""
import sys
from pathlib import Path
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from mcp.types import SamplingMessage, TextContent

import json


from uuid import uuid4
from typing import List
from pydantic import BaseModel

import json

mcp: FastMCP = FastMCP(name="Sampling Example")

# characters.json を読み込む
# '../characters.json' とだけ書くとカレントディレクトリから探されるため、このファイルの場所を基準にする
CHARACTERS_PATH: Path = Path(__file__).resolve().parent.parent / "characters.json"
with open(CHARACTERS_PATH) as f:
    characters = json.load(f)

@mcp.tool()
async def talk_to(name: str, topic: str, ctx: Context[ServerSession, None]) -> str:
    """キャラクターと話して、応答を得る。

    キャラクターの設定をシステムプロンプトにして、クライアントにサンプリングを依頼する。

    Parameters
    ----------
    name : str
        話す相手のキャラクター名（characters.json の name）。
    topic : str
        話題。
    ctx : Context[ServerSession, None]
        MCP のリクエストコンテキスト。サンプリングの依頼に使う。

    Returns
    -------
    str
        キャラクターとして LLM が生成した応答。

    Raises
    ------
    ValueError
        指定した名前のキャラクターが見つからない場合。
    """
    # characters からキャラクターを読み込む
    # characters をループして、"name" プロパティが name と一致するキャラクターを探す
    character = None
    for c in characters:
        if c["name"] == name:
            character = c
            break
    if character is None:
        raise ValueError(f"キャラクター {name} が見つかりません")

    system_prompt = f"あなたは {character['name']} です。{character['description']}。{character['personality']}"

    prompt = f"{name} と話してください。"
    prompt += f"話題は「{topic}」です。"
    
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(type="text", text=prompt),
            )
        ],
        system_prompt=system_prompt,
        temperature=0.9,
        max_tokens=4000,
    )

    return result.content.text

if __name__ == "__main__":
    # stdio では stdout が MCP の通信に使われるので、メッセージは stderr に出す
    print("サーバーを起動しています...", file=sys.stderr)
    mcp.run()