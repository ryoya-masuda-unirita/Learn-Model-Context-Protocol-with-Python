from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from mcp.types import SamplingMessage, TextContent

import json


from uuid import uuid4
from typing import List
from pydantic import BaseModel

mcp = FastMCP(name="Sampling Example")

class Product(BaseModel):
    id: int
    name: str
    description: str

    def __init__(self, name: str, description: str):
        super().__init__(
            id=len(products) + 1,
            name=name,
            description=description
        )

products: List[Product] = []

@mcp.tool()
def get_products() -> list[Product]:
    """すべての商品を一覧表示する。"""
    return products

# @mcp.tool()
# def get_products() -> [Product]:
#     """すべての商品を一覧表示する。"""
#     return [{"type": "text", "name": f"ID: {item.id}, product: {item.name}, description: {item.description}"} for item in products]

@mcp.tool()
async def create_product(product_name: str, keywords: str, ctx: Context[ServerSession, None]) -> str:
    """商品を作成し、LLM のサンプリングで商品説明を生成する。"""

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
    return json.dumps({
        "id": product.id,
        "name": product.name,
        "description": product.description
    })

if __name__ == "__main__":
    print("サーバーを起動しています...")
    mcp.run()