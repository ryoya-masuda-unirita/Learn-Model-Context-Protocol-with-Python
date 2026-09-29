from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from mcp.types import SamplingMessage, TextContent

import json


from uuid import uuid4
from typing import List
from pydantic import BaseModel

import json

mcp = FastMCP(name="Sampling Example")

# characters.json を読み込む
with open("../characters.json") as f:
    characters = json.load(f)

@mcp.tool()
async def talk_to(name: str, topic: str, ctx: Context[ServerSession, None]) -> str:
    """キャラクターと話して、応答を得る。"""

    # characters からキャラクターを読み込む
    # characters をループして、"name" プロパティが name と一致するキャラクターを探す
    character = None
    for c in characters:
        if c["name"] == name:
            character = c
            break

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
    print("サーバーを起動しています...")
    mcp.run()