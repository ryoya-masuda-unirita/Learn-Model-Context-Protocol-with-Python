"""入れ子の pydantic モデルで、辞書との変換を行うサンプル。"""
from typing import Any

from pydantic import BaseModel
from typing import List, Dict 
import pydantic

class OfficeHour(BaseModel):
    """オフィスアワー（曜日と時間帯）。"""

    day: str
    from_: int
    to_: int

class Professor(BaseModel):
    """教授。"""

    id: int
    name: str
    office_hours: List[OfficeHour]

professor_dict: dict[str, Any] = {
    "id": 1,
    "name": "Dr. Smith",
    "office_hours": [
        {"day": "月曜日", "from_": 9, "to_": 12},
        {"day": "水曜日", "from_": 14, "to_": 17}
    ]
}

professor = Professor(**professor_dict)

professor_serialized = professor.model_dump() # {"id": 1, "name": "Dr. Smith", "office_hours": [{"day": "月曜日", "from_": 9, "to_": 12}, {"day": "水曜日", "from_": 14, "to_": 17}]}}

print("pydantic のバージョン: ", pydantic.__version__)

print(professor)
print(professor_serialized)