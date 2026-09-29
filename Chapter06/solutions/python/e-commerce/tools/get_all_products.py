from data import products
from .schema import ProductModel

async def handler(args) -> list[ProductModel]:
    return products

tool_get_all_products = {
    "name": "get_all_products",
    "description": "すべての商品を取得する",
    "input_schema": None,
    "handler": handler
}   
