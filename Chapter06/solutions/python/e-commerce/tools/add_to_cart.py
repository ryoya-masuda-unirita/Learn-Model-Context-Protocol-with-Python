"""ショッピングカートに商品を追加する add_to_cart tool の定義。"""
from typing import Any

from .schema import AddCartInputModel, CartItemModel
from data import cart_items

async def add_handler(args: dict[str, Any]) -> str:
    """ショッピングカートに商品を追加する add_to_cart tool のハンドラー。

    Parameters
    ----------
    args : dict[str, Any]
        tool に渡された引数。cart_id、product_id、quantity を持つ。

    Returns
    -------
    str
        追加できたことを伝えるメッセージ。

    Raises
    ------
    ValueError
        引数が AddCartInputModel として不正な場合。
    """
    try:
        # Pydantic モデルで入力を検証する
        input_model = AddCartInputModel(**args)
        # get_all_cart_items が読む cart_items に追加する（別のリストに入れると、追加した商品が見えない）
        cart_items.append(CartItemModel(**input_model.model_dump()))

    except Exception as e:
        raise ValueError(f"入力が不正です: {str(e)}")

    return f"カートに追加しました"

tool_add_to_cart: dict[str, Any] = {
    "name": "add_to_cart",
    "description": "ショッピングカートに商品を追加する",
    "input_schema": AddCartInputModel,
    "handler": add_handler 
}