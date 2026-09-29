# @mcp.tool()
# def get_product(product_id: int) -> Product:
#     """ID で商品を取得する"""
#     for product in products:
#         if product.name == product_id:
#             return {"type": "text", "name": f"ID: {product.name},price: {product.price},description: {product.description}"}
#     return None

from data import products
from .schema import ProductModel, GetProductInputModel

async def handler(args) -> ProductModel:
    # ID で商品を取得する
    input = GetProductInputModel(**args)
    
    # 指定された ID の商品を探す
    for product in products:
        if product.id == input.product_id:
            return product
    
    # 商品が見つからなければ、None を返すかエラーを発生させる
    return None

tool_get_product = {
    "name": "get_product",
    "description": "ID で商品を取得する",
    "input_schema": GetProductInputModel,
    "handler": handler
}