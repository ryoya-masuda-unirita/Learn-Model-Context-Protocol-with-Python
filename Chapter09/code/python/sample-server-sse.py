"""サンプリングで商品説明を生成する tool を持つ MCP サーバー（SSE 版）。

`uvicorn sample-server-sse:app --port 3000` で起動する。
"""
import sys
from starlette.applications import Starlette
from starlette.routing import Mount, Host

from mcp.server.fastmcp import Context, FastMCP

from mcp.server.session import ServerSession
from mcp.types import SamplingMessage, TextContent

import json


from uuid import uuid4
from typing import List
from pydantic import BaseModel


mcp: FastMCP = FastMCP("My App")

class Product(BaseModel):
    """商品。"""

    id: int
    name: str
    description: str

    def __init__(self, name: str, description: str) -> None:
        """商品を作る。id は登録済みの商品数から採番する。

        Parameters
        ----------
        name : str
            商品名。
        description : str
            商品説明。
        """
        super().__init__(
            id=len(products) + 1,
            name=name,
            description=description
        )

# データはメモリ上のリストに持っているだけなので、サーバーが終了すると消える
products: List[Product] = []

@mcp.tool()
async def create_product(product_name: str, keywords: str, ctx: Context[ServerSession, None]) -> str:
    """商品を作成し、LLM のサンプリングで商品説明を生成する。

    商品説明の生成は、クライアントにサンプリング（sampling/createMessage）を依頼して行う。

    Parameters
    ----------
    product_name : str
        商品名。
    keywords : str
        商品説明に含めたい特徴（カンマ区切り）。
    ctx : Context[ServerSession, None]
        MCP のリクエストコンテキスト。サンプリングの依頼に使う。

    Returns
    -------
    str
        作成した商品（id、name、description）の JSON 文字列。
    """
    product = Product(name=product_name, description="")

    prompt = f"{product_name} の商品説明を作成してください。特徴: {keywords}"

    # サーバーは LLM を持っていないので、クライアントに「この内容で LLM に生成させて」と依頼する（sampling/createMessage）。
    # create_message() はクライアントの応答が返るまで待つので、tool の処理はここで一時停止する
    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(type="text", text=prompt),
            )
        ],
        # クライアントはこの上限まで生成する。日本語は1文字あたりのトークン数が多いので、短すぎると説明が途中で切れる
        max_tokens=300,
    )


    product.description = result.content.text

    products.append(product)

    # 完成した商品を返す
    # 日本語をエスケープせず、そのまま読める形で返す
    return json.dumps({
        "id": product.id,
        "name": product.name,
        "description": product.description
    }, ensure_ascii=False)

# 既存の ASGI サーバーに SSE サーバーをマウントする
# GET /sse（サーバー → クライアント）と POST /messages/（クライアント → サーバー）の2つの道ができる。
# サンプリングのリクエストは、サーバーからクライアントへ /sse の道を通って届く
app: Starlette = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)

if __name__ == "__main__":
    # python sample-server-sse.py でも SSE のサーバーとして起動できるようにする。
    # 以前は mcp.run()（stdio）を呼んでいたため、SSE ではなく stdio のサーバーとして起動してしまっていた
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=3000)
