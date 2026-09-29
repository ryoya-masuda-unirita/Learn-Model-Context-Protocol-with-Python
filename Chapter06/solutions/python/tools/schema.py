"""tool の入力を表す pydantic モデル。"""
from pydantic import BaseModel

class AddInputModel(BaseModel):
    """add tool の入力。"""

    a: float
    b: float