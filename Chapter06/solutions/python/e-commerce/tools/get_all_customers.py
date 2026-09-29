"""すべての顧客を取得する get_all_customers tool の定義。"""
from typing import Any

from data import customers
from .schema import CustomerModel

async def handler(args: dict[str, Any] | None) -> list[CustomerModel]:
    """すべての顧客を返す。

    Parameters
    ----------
    args : dict[str, Any] | None
        tool に渡された引数（この tool では使わない）。

    Returns
    -------
    list[CustomerModel]
        すべての顧客のリスト。
    """
    return customers

tool_get_all_customers: dict[str, Any] = {
    "name": "get_all_customers",
    "description": "すべての顧客を取得する",
    "input_schema": None,
    "handler": handler
}