"""カートの中身をすべて取得する get_all_cart_items tool の定義。"""
# @mcp.tool()
# def get_cart_items(cart_id:int) -> [CartItem]:
#     """カートの中身を取得する"""
#     cart_items = [item for item in carts if item.cart_id == cart_id]
#     return [{"type": "text", "name": f"ID: {item.cart_id},product: {item.product_id},quantity: {item.quantity}"} for item in cart_items]

from typing import Any

from data import cart_items
from .schema import CartItemModel

async def handler(args: dict[str, Any] | None) -> list[CartItemModel]:
    """カートの中身をすべて返す。

    Parameters
    ----------
    args : dict[str, Any] | None
        tool に渡された引数（この tool では使わない）。

    Returns
    -------
    list[CartItemModel]
        すべてのカートの中身のリスト。
    """
    return cart_items

tool_get_all_cart_items: dict[str, Any] = {
    "name": "get_all_cart_items",
    "description": "カートの中身をすべて取得する",
    "input_schema": None,
    "handler": handler
}   
