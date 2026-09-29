# server.py
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from typing import Union

import uuid

# import 文を追加する
from typing import List, Dict, Any, Optional


# MCP サーバーを作る
mcp = FastMCP("Demo")

class Customer(BaseModel):
    id: int
    name: str
    email: str

    def __init__(self, **data):
        super().__init__(**data)

class Category(BaseModel):
    id: uuid.UUID
    name: str
    description: str

    def __init__(self, **data):
        if 'id' not in data:
            data['id'] = uuid.uuid4()
        super().__init__(**data)

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str

class CartItem(BaseModel):
    id: int
    cart_id: uuid.UUID
    product_id: int
    quantity: int

    def __init__(self, cart_id: uuid.UUID, product_id: int, quantity: int):
        if cart_id != uuid.UUID(int=0):
            self.cart_id = cart_id
        else:
            self.cart_id = uuid.uuid4()
        self.product_id = product_id
        self.quantity = quantity

class Cart(BaseModel):
    id: int
    customer_id: int

    def __init__(self, **data):
        if 'id' not in data:
            data['id'] = uuid.uuid4()
        super().__init__(**data)

class Order(BaseModel):
    id: uuid.UUID
    customer_id: int

    def __init__(self, **data):
        if 'id' not in data or not isinstance(data['id'], uuid.UUID):
            data['id'] = uuid.uuid4()
        super().__init__(**data)


products = [
    Product(id=1, name="商品 1", price=10.0, description="商品 1 の説明"),
    Product(id=2, name="商品 2", price=20.0, description="商品 2 の説明"),
    Product(id=3, name="商品 3", price=30.0, description="商品 3 の説明")
]

orders = [
    Order(id=1, customer_id=101),
    Order(id=uuid.uuid4(), customer_id=101),
    Order(id=uuid.uuid4(), customer_id=102)
]

carts = []
cart_items = []

customers = [
    Customer(id=1, name="顧客 1", email="email")
]


categories = [
    Category(id=uuid.uuid4(), name="カテゴリー 1", description="カテゴリー 1 の説明"),
    Category(id=uuid.uuid4(), name="カテゴリー 2", description="カテゴリー 2 の説明"),
    Category(id=uuid.uuid4(), name="カテゴリー 3", description="カテゴリー 3 の説明")
]

product_catalog = [
    {
        "name": "商品 1",
        "price": 10.0,
        "description": "商品 1 の説明",
        "category_id": 1
    },
    {
        "name": "商品 2",
        "price": 20.0,
        "description": "商品 2 の説明",
        "category_id": 2
    },
    {
        "name": "商品 3",
        "price": 30.0,
        "description": "商品 3 の説明",
        "category_id": 3
    }
]


# 注文を取得する
@mcp.tool()
def get_orders(customer_id:int = 0) -> List[Order]:
    """すべての注文を取得する"""

    if customer_id != 0 and not any(customer.id == customer_id for customer in customers):
        raise ValueError(f"customer_id が不正です: {customer_id}")

    filtered_orders = orders
    if customer_id != 0:
        filtered_orders = [order for order in orders if order.customer_id == customer_id]

    return filtered_orders

# ID で注文を取得する
@mcp.tool()
def get_order(order_id:int) -> Order | None:
    """ID で注文を取得する"""
    for order in orders:
        if order.order_id == order_id:
            return order
    return None

# 注文する
@mcp.tool()
def place_order(customer_id:int) -> Order:
    """注文する"""
    if customer_id != 0 and not any(customer.id == customer_id for customer in customers):
        raise ValueError(f"customer_id が不正です: {customer_id}")

    new_order = Order(0, customer_id)
    orders.append(new_order)
    return new_order

# カートを取得する
@mcp.tool()
def get_cart(customer_id:int) -> Cart | None:
    """カートを1つ取得する"""

    if customer_id != 0 and not any(customer.id == customer_id for customer in customers):
        raise ValueError(f"customer_id が不正です: {customer_id}")

    # 顧客 ID でカートを取得する
    cart = next((cart for cart in carts if cart.customer_id == customer_id), None)
    if cart:
        return cart
    return None


# カートの中身を取得する
@mcp.tool()
def get_cart_items(cart_id:int) -> List[CartItem]:
    """カートの中身を取得する"""

    # ID で特定のカートを探す
    items = [item for item in cart_items if item.cart_id == cart_id]

    # そのカートの中身を返す
    return items

# カートに追加する
@mcp.tool()
def add_to_cart(cart_id:int, product_id:int, quantity:int) -> CartItem:
    """カートに追加する"""
    new_cart_item = CartItem(cart_id, product_id, quantity)
    cart_items.append(new_cart_item)
    return new_cart_item

# tool：すべての商品
@mcp.tool()
def get_all_products() -> List[Product]:
    """すべての商品を取得する"""
    return products

# tool：ID で商品を取得
@mcp.tool()
def get_product(product_id: int) -> Product | None:
    """ID で商品を取得する"""
    for product in products:
        if product.id == product_id:
            return product
    return None

# tool：すべてのカテゴリー
@mcp.tool()
def get_all_categories() -> List[Category]:
    """すべてのカテゴリーを取得する"""
    return categories

# tool：すべての顧客
@mcp.tool()
def get_all_customers() -> List[Customer]:
    """すべての顧客を取得する"""
    return customers

# resource：商品カタログ
@mcp.resource("resource:product_catalog")
def get_product_catalog():
    """商品カタログを取得する"""
    return product_catalog