"""EC サイトを題材に、注文・カート・商品などを扱う tool を公開する MCP サーバー。"""
# server.py
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from typing import Union

import uuid

# import 文を追加する
from typing import List, Dict, Any, Optional


# MCP サーバーを作る
mcp: FastMCP = FastMCP("Demo")

class Customer(BaseModel):
    """顧客。"""

    id: int
    name: str
    email: str

    def __init__(self, **data: Any) -> None:
        """顧客を作る。

        Parameters
        ----------
        **data : Any
            各フィールドの値。
        """
        super().__init__(**data)

class Category(BaseModel):
    """商品カテゴリー。"""

    id: uuid.UUID
    name: str
    description: str

    def __init__(self, **data: Any) -> None:
        """カテゴリーを作る。id が指定されていなければ生成する。

        Parameters
        ----------
        **data : Any
            各フィールドの値。
        """
        if 'id' not in data:
            data['id'] = uuid.uuid4()
        super().__init__(**data)

class Product(BaseModel):
    """商品。"""

    id: int
    name: str
    price: float
    description: str

class CartItem(BaseModel):
    """カートに入っている商品。"""

    id: int
    cart_id: int
    product_id: int
    quantity: int

    def __init__(self, cart_id: int, product_id: int, quantity: int) -> None:
        """カートの商品を作る。id は採番する。

        Parameters
        ----------
        cart_id : int
            カートの ID。0 を渡すと新しいカートの ID を採番する。
        product_id : int
            商品の ID。
        quantity : int
            数量。
        """
        # pydantic のモデルは super().__init__() でフィールドを設定する必要がある
        # （先に self.xxx へ代入すると、初期化前のモデルとしてエラーになる）
        if cart_id == 0:
            cart_id = max((item.cart_id for item in cart_items), default=0) + 1
        super().__init__(id=len(cart_items) + 1, cart_id=cart_id, product_id=product_id, quantity=quantity)

class Cart(BaseModel):
    """顧客のカート。"""

    id: int
    customer_id: int

    def __init__(self, **data: Any) -> None:
        """カートを作る。id が指定されていなければ採番する。

        Parameters
        ----------
        **data : Any
            各フィールドの値。
        """
        if 'id' not in data:
            data['id'] = len(carts) + 1
        super().__init__(**data)

class Order(BaseModel):
    """注文。"""

    id: int
    customer_id: int

    def __init__(self, **data: Any) -> None:
        """注文を作る。id が指定されていなければ採番する。

        Parameters
        ----------
        **data : Any
            各フィールドの値。
        """
        if 'id' not in data:
            data['id'] = max((order.id for order in orders), default=0) + 1
        super().__init__(**data)


products: list[Product] = [
    Product(id=1, name="商品 1", price=10.0, description="商品 1 の説明"),
    Product(id=2, name="商品 2", price=20.0, description="商品 2 の説明"),
    Product(id=3, name="商品 3", price=30.0, description="商品 3 の説明")
]

orders: list[Order] = [
    Order(id=1, customer_id=101),
    Order(id=2, customer_id=101),
    Order(id=3, customer_id=102)
]

carts: list[Cart] = []
cart_items: list[CartItem] = []

customers: list[Customer] = [
    Customer(id=1, name="顧客 1", email="email"),
    Customer(id=101, name="顧客 101", email="email"),
    Customer(id=102, name="顧客 102", email="email")
]


categories: list[Category] = [
    Category(id=uuid.uuid4(), name="カテゴリー 1", description="カテゴリー 1 の説明"),
    Category(id=uuid.uuid4(), name="カテゴリー 2", description="カテゴリー 2 の説明"),
    Category(id=uuid.uuid4(), name="カテゴリー 3", description="カテゴリー 3 の説明")
]

product_catalog: list[dict[str, Any]] = [
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
    """すべての注文を取得する。

    Parameters
    ----------
    customer_id : int, optional
        絞り込む顧客の ID。0 ならすべての注文を返す。デフォルトは 0。

    Returns
    -------
    List[Order]
        条件に合う注文のリスト。

    Raises
    ------
    ValueError
        存在しない顧客の ID が指定された場合。
    """
    if customer_id != 0 and not any(customer.id == customer_id for customer in customers):
        raise ValueError(f"customer_id が不正です: {customer_id}")

    filtered_orders = orders
    if customer_id != 0:
        filtered_orders = [order for order in orders if order.customer_id == customer_id]

    return filtered_orders

# ID で注文を取得する
@mcp.tool()
def get_order(order_id:int) -> Order | None:
    """ID で注文を取得する。

    Parameters
    ----------
    order_id : int
        取得する注文の ID。

    Returns
    -------
    Order | None
        見つかった注文。見つからなければ None。
    """
    for order in orders:
        if order.id == order_id:
            return order
    return None

# 注文する
@mcp.tool()
def place_order(customer_id:int) -> Order:
    """注文する。

    Parameters
    ----------
    customer_id : int
        注文する顧客の ID。

    Returns
    -------
    Order
        作成した注文。

    Raises
    ------
    ValueError
        存在しない顧客の ID が指定された場合。
    """
    if customer_id != 0 and not any(customer.id == customer_id for customer in customers):
        raise ValueError(f"customer_id が不正です: {customer_id}")

    new_order = Order(customer_id=customer_id)
    orders.append(new_order)
    return new_order

# カートを取得する
@mcp.tool()
def get_cart(customer_id:int) -> Cart | None:
    """カートを1つ取得する。

    Parameters
    ----------
    customer_id : int
        カートを持つ顧客の ID。

    Returns
    -------
    Cart | None
        見つかったカート。見つからなければ None。

    Raises
    ------
    ValueError
        存在しない顧客の ID が指定された場合。
    """
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
    """カートの中身を取得する。

    Parameters
    ----------
    cart_id : int
        中身を取得するカートの ID。

    Returns
    -------
    List[CartItem]
        カートに入っている商品のリスト。
    """
    # ID で特定のカートを探す
    items = [item for item in cart_items if item.cart_id == cart_id]

    # そのカートの中身を返す
    return items

# カートに追加する
@mcp.tool()
def add_to_cart(cart_id:int, product_id:int, quantity:int) -> CartItem:
    """カートに追加する。

    Parameters
    ----------
    cart_id : int
        追加先のカートの ID。
    product_id : int
        追加する商品の ID。
    quantity : int
        数量。

    Returns
    -------
    CartItem
        追加したカートの商品。
    """
    new_cart_item = CartItem(cart_id, product_id, quantity)
    cart_items.append(new_cart_item)
    return new_cart_item

# tool：すべての商品
@mcp.tool()
def get_all_products() -> List[Product]:
    """すべての商品を取得する。

    Returns
    -------
    List[Product]
        すべての商品のリスト。
    """
    return products

# tool：ID で商品を取得
@mcp.tool()
def get_product(product_id: int) -> Product | None:
    """ID で商品を取得する。

    Parameters
    ----------
    product_id : int
        取得する商品の ID。

    Returns
    -------
    Product | None
        見つかった商品。見つからなければ None。
    """
    for product in products:
        if product.id == product_id:
            return product
    return None

# tool：すべてのカテゴリー
@mcp.tool()
def get_all_categories() -> List[Category]:
    """すべてのカテゴリーを取得する。

    Returns
    -------
    List[Category]
        すべてのカテゴリーのリスト。
    """
    return categories

# tool：すべての顧客
@mcp.tool()
def get_all_customers() -> List[Customer]:
    """すべての顧客を取得する。

    Returns
    -------
    List[Customer]
        すべての顧客のリスト。
    """
    return customers

# resource：商品カタログ
@mcp.resource("resource:product_catalog")
def get_product_catalog() -> list[dict[str, Any]]:
    """商品カタログを取得する。

    Returns
    -------
    list[dict[str, Any]]
        商品カタログ（name、price、description、category_id を持つ辞書）のリスト。
    """
    return product_catalog