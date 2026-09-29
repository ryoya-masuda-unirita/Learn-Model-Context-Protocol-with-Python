"""すべてのカートを取得する get_all_carts tool の定義。"""
from typing import Any

from data import carts
from .schema import AddCartInputModel

async def handler(args: dict[str, Any] | None) -> list[AddCartInputModel]:
    """すべてのカートを返す。

    Parameters
    ----------
    args : dict[str, Any] | None
        tool に渡された引数（この tool では使わない）。

    Returns
    -------
    list[AddCartInputModel]
        すべてのカートのリスト。
    """
    return carts

tool_get_all_carts: dict[str, Any] = {
    "name": "get_all_carts",
    "description": "すべてのカートを取得する",
    "input_schema": None,
    "handler": handler
}
