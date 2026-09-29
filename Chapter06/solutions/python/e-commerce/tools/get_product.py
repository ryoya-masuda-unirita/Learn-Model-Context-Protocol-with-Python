"""ID で商品を取得する get_product tool の定義。"""
# @mcp.tool()
# def get_product(product_id: int) -> Product:
#     """ID で商品を取得する"""
#     for product in products:
#         if product.name == product_id:
#             return {"type": "text", "name": f"ID: {product.name},price: {product.price},description: {product.description}"}
#     return None

from typing import Any

from data import products
from .schema import ProductModel, GetProductInputModel

async def handler(args: dict[str, Any]) -> ProductModel | None:
    """ID で商品を返す。

    Parameters
    ----------
    args : dict[str, Any]
        tool に渡された引数。product_id を持つ。

    Returns
    -------
    ProductModel | None
        見つかった商品。見つからなければ None。
    """
    # ID で商品を取得する
    input = GetProductInputModel(**args)
    
    # 指定された ID の商品を探す
    for product in products:
        if product.id == input.product_id:
            return product
    
    # 商品が見つからなければ、None を返すかエラーを発生させる
    return None

tool_get_product: dict[str, Any] = {
    "name": "get_product",
    "description": "ID で商品を取得する",
    "input_schema": GetProductInputModel,
    "handler": handler
}