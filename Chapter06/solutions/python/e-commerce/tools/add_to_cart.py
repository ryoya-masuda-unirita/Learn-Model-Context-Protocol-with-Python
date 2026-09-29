from .schema import AddCartInputModel
from data import carts

async def add_handler(args) -> str:

    try:
        # Pydantic モデルで入力を検証する
        input_model = AddCartInputModel(**args)
        carts.append(input_model)

    except Exception as e:
        raise ValueError(f"入力が不正です: {str(e)}")

    # TODO: Pydantic を追加して AddInputModel を作り、引数を検証できるようにする

    """add tool のハンドラー関数。"""
    return f"カートに追加しました"

tool_add_to_cart = {
    "name": "add_to_cart",
    "description": "ショッピングカートに商品を追加する",
    "input_schema": AddCartInputModel,
    "handler": add_handler 
}