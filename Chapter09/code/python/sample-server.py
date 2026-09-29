"""サンプリングで商品説明を生成する tool を持つ MCP サーバー。

クライアント（sample-client.py）から stdio 経由で起動される。
"""
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from mcp.types import SamplingMessage, TextContent

import json


from uuid import uuid4
from typing import List
from pydantic import BaseModel

mcp: FastMCP = FastMCP(name="Sampling Example")

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

products: List[Product] = []

@mcp.tool()
def get_products() -> list[Product]:
    """すべての商品を一覧表示する。

    Returns
    -------
    list[Product]
        登録されているすべての商品のリスト。
    """
    return products

# @mcp.tool()
# def get_products() -> [Product]:
#     """すべての商品を一覧表示する。"""
#     return [{"type": "text", "name": f"ID: {item.id}, product: {item.name}, description: {item.description}"} for item in products]

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

    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(type="text", text=prompt),
            )
        ],
        max_tokens=100,
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

if __name__ == "__main__":
    print("サーバーを起動しています...")
    mcp.run()