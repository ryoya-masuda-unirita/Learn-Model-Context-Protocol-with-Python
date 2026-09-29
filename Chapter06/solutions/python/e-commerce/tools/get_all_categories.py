"""すべての商品カテゴリーを取得する get_all_categories tool の定義。"""
from typing import Any

from data import categories
from .schema import CategoryModel

async def handler(args: dict[str, Any] | None) -> list[CategoryModel]:
    """すべての商品カテゴリーを返す。

    Parameters
    ----------
    args : dict[str, Any] | None
        tool に渡された引数（この tool では使わない）。

    Returns
    -------
    list[CategoryModel]
        すべての商品カテゴリーのリスト。
    """
    return categories

tool_get_all_categories: dict[str, Any] = {
    "name": "get_all_categories",
    "description": "すべての商品カテゴリーを取得する",
    "input_schema": None,
    "handler": handler 
}