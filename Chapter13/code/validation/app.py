from pydantic import BaseModel, ValidationError

class Product(BaseModel):
    id: str
    name: str
    price: float

class Book(BaseModel):
    id: str
    title: str
    author: str
    pages: int
    abstract: str | None = None

product = { "id": "1", "name": "商品 1", "price": 10.0 }
book = { "id": "1", "title": "本 1", "author": "著者 1", "pages": 100 }

# 2. より安全な検証方法
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
   product_that_will_crash = Product(**product_crashable)
except ValidationError as e:
    print(f"検証エラー: {e}")

class ComplexUser(BaseModel):
    id: str
    name: str
    age: int
    email: str
    is_active: bool
    attendance: dict[str, bool]

complex_user_data = { 
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