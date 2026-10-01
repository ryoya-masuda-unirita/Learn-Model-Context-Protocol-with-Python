"""pydantic で辞書のデータを検証するサンプル。"""
from typing import Any

from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    """商品。"""

    id: str
    name: str
    price: float

class Book(BaseModel):
    """本。"""

    id: str
    title: str
    author: str
    pages: int
    abstract: str | None = None

product: dict[str, Any] = { "id": "1", "name": "商品 1", "price": 10.0 }
book: dict[str, Any] = { "id": "1", "title": "本 1", "author": "著者 1", "pages": 100 }

# 2. より安全な検証方法
# 型ヒントと違い、pydantic のモデルは実行時に中身を検証する。型が合わない値は変換を試み、できなければ ValidationError になる。
# MCP の SDK も、tool の引数やメッセージの検証に pydantic を使っている
try:
   parsed_product = Product(**product)
   parsed_book = Book(**book)
   print(f"解析した商品: {parsed_product}")
   print(f"解析した本: {parsed_book}")
except ValidationError as e:
    print(f"検証エラー: {e}")

# 例外が発生する
try:
   product_crashable = { "id": "1", "name": "商品 1" }
   # price がないので検証エラーになることを示すための意図的な呼び出し
   product_that_will_crash = Product(**product_crashable)  # type: ignore[arg-type]
except ValidationError as e:
    print(f"検証エラー: {e}")

class ComplexUser(BaseModel):
    """入れ子のデータを持つユーザー。"""

    id: str
    name: str
    age: int
    email: str
    is_active: bool
    attendance: dict[str, bool]

complex_user_data: dict[str, Any] = { 
    "id": "1", 
    "name": "ユーザー 1", 
    "age": 30, 
    "email": "user1@example.com", 
    "is_active": True, 
    "attendance": { 
        "2023-01-01": True,
        "2023-01-02": False,
        "2023-01-03": True
    } 
}

complex = ComplexUser(**complex_user_data)
print(f"複雑なユーザー: {complex}")