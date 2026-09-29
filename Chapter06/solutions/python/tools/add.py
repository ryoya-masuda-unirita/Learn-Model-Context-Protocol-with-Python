"""2つの数を足し算する add tool の定義。"""
from typing import Any

from .schema import AddInputModel

async def add_handler(args: dict[str, Any]) -> float:
    """2つの数を足し算する add tool のハンドラー。

    Parameters
    ----------
    args : dict[str, Any]
        tool に渡された引数。a と b を持つ。

    Returns
    -------
    float
        a と b の和。

    Raises
    ------
    ValueError
        引数が AddInputModel として不正な場合。
    """
    try:
        # Pydantic モデルで入力を検証する
        input_model = AddInputModel(**args)
    except Exception as e:
        raise ValueError(f"入力が不正です: {str(e)}")

    # TODO: Pydantic を追加して AddInputModel を作り、引数を検証できるようにする

    """add tool のハンドラー関数。"""
    return float(input_model.a) + float(input_model.b)

tool_add: dict[str, Any] = {
    "name": "add",
    "description": "2つの数を足し算する",
    "input_schema": AddInputModel,
    "handler": add_handler 
}

