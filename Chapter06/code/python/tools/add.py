from .schema import AddInputModel

async def add_handler(args) -> float:

    try:
        # Pydantic モデルで入力を検証する
        input_model = AddInputModel(**args)
    except Exception as e:
        raise ValueError(f"入力が不正です: {str(e)}")

    # TODO: Pydantic を追加して AddInputModel を作り、引数を検証できるようにする

    """add tool のハンドラー関数。"""
    return float(input_model.a) + float(input_model.b)

tool_add = {
    "name": "add",
    "description": "2つの数を足し算する",
    "input_schema": AddInputModel,
    "handler": add_handler 
}

