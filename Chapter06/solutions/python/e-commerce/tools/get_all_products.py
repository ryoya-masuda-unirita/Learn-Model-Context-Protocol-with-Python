"""すべての商品を取得する get_all_products tool の定義。"""
from typing import Any

from data import products
from .schema import ProductModel

async def handler(args: dict[str, Any] | None) -> list[ProductModel]:
    """すべての商品を返す。

    Parameters
    ----------
    args : dict[str, Any] | None
        tool に渡された引数（この tool では使わない）。

    Returns
    -------
    list[ProductModel]
        すべての商品のリスト。
    """
    return products

tool_get_all_products: dict[str, Any] = {
    "name": "get_all_products",
    "description": "すべての商品を取得する",
    "input_schema": None,
    "handler": handler
}   
