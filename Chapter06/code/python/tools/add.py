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
        # low-level の Server も inputSchema で型をチェックするが、ハンドラー側でも検証しておくと、
        # スキーマにない細かい条件（値の範囲など）もモデルに書いて弾ける
        input_model = AddInputModel(**args)
    except Exception as e:
        raise ValueError(f"入力が不正です: {str(e)}")

    return float(input_model.a) + float(input_model.b)

# server.py は、この辞書の name / description / input_schema から tools/list の応答を作り、
# tools/call が来たら handler を呼ぶ
tool_add: dict[str, Any] = {
    "name": "add",
    "description": "2つの数を足し算する",
    "input_schema": AddInputModel,
    "handler": add_handler 
}

