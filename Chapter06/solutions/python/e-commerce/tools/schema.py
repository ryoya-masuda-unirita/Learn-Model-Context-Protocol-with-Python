"""EC サイトの tool の入出力を表す pydantic モデル。"""
from pydantic import BaseModel

class AddCartInputModel(BaseModel):
    """add_to_cart tool の入力（カートに追加する商品）。"""

    cart_id: int
    product_id: int
    quantity: int

class AddInputModel(BaseModel):
    """add tool の入力。"""

    a: float
    b: float

class CategoryModel(BaseModel):
    """商品カテゴリー。"""

    name: str
    description: str

class CustomerModel(BaseModel):
    """顧客。"""

    id: int
    name: str
    email: str

class ProductModel(BaseModel):
    """商品。"""

    id: int
    name: str
    price: float
    description: str

class CartItemModel(BaseModel):
    """カートに入っている商品。"""

    cart_id: int
    product_id: int
    quantity: int

class OrderModel(BaseModel):
    """注文。"""

    order_id: int
    customer_id: int
    quantity: int
    total_price: float

class GetOrderInputModel(BaseModel):
    """get_orders tool の入力。"""

    customer_id: int

class GetProductInputModel(BaseModel):
    """get_product tool の入力。"""

    product_id: int