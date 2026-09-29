from data import carts
from .schema import AddCartInputModel

async def handler(args) -> list[AddCartInputModel]:
    return carts

tool_get_all_carts = {
    "name": "get_all_carts",
    "description": "すべてのカートを取得する",
    "input_schema": None,
    "handler": handler
}
