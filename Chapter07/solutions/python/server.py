"""商品とカートを扱う tool を持つ MCP サーバー。

クライアント（client.py、client_llm.py）から `mcp run server.py` で stdio 経由で起動される。
"""
# server.py
from mcp.server.fastmcp import FastMCP
import uuid
from pydantic import BaseModel
from typing import Any, Union, List

# MCP サーバーを作る
mcp: FastMCP = FastMCP("Demo")

class Product(BaseModel):
    """商品。"""

    id: int
    name: str
    price: float
    description: str
    category: str


class CartItem(BaseModel):
    """カートに入っている商品。"""

    cart_id: int
    product_id: int
    quantity: int

    def __init__(self, **data: Any) -> None:
        """カートの商品を作る。cart_id が指定されていなければ 1 にする。

        Parameters
        ----------
        **data : Any
            各フィールドの値。
        """
        if 'cart_id' not in data:
            data['cart_id'] = 1
        super().__init__(**data)

products: list[dict[str, Any]] = [
    {
        "id": 1,
        "name": "商品 1",
        "price": 10.0,
        "description": "商品 1 の説明",
        "category": "カテゴリー 1"
    },
    {
        "id": 2,
        "name": "商品 2",
        "price": 20.0,
        "description": "商品 2 の説明",
        "category": "カテゴリー 2"
    },
    {
        "id": 3,
        "name": "商品 3",
        "price": 30.0,
        "description": "商品 3 の説明",
        "category": "カテゴリー 3"
    }
]

cart: list[CartItem] = []

# カートに商品を追加する
@mcp.tool()
def add_product_to_cart(product_name: str) -> CartItem:
    """カートに商品を追加する。

    Parameters
    ----------
    product_name : str
        追加する商品の名前（例: "商品 1"）。

    Returns
    -------
    CartItem
        追加したカートの商品。
    """
    product = next((p for p in products if p["name"] == product_name), None)
    if not product:
        return {"type": "text", "name": f"商品 [{product_name}] が見つかりません"}
    cart_item = CartItem(cart_id=0, product_id=product["id"], quantity=1)
    cart.append(cart_item)
    return cart_item

# カートの中身を一覧表示する
@mcp.tool()
def list_cart() -> List[CartItem]:
    """カートの中身をすべて一覧表示する。

    Returns
    -------
    List[CartItem]
        カートに入っている商品のリスト。
    """
    return cart

# tool：すべての商品
@mcp.tool()
def get_products() -> List[Product]:
    """すべての商品を取得する。

    Returns
    -------
    List[Product]
        すべての商品のリスト。
    """
    # 商品データを Product オブジェクトに変換する
    products_vm = [Product(**product) for product in products]
    return products_vm

