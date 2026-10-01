"""EC サイトのサンプルデータ（カテゴリー、顧客、商品、カート、注文）。"""
from pydantic import BaseModel

from tools.schema import AddCartInputModel, CategoryModel, CustomerModel, ProductModel, CartItemModel, OrderModel

# データはメモリ上のリストに持っているだけなので、サーバーを再起動すると追加した内容は消える
# carts は get_carts.py（tools/__init__.py に登録していない tool）だけが使う
carts: list[AddCartInputModel] = []

categories: list[CategoryModel] = [
    CategoryModel(name="家電", description="デバイスやガジェット"),
    CategoryModel(name="書籍", description="フィクションとノンフィクションの本"),
    CategoryModel(name="衣料品", description="衣類とアクセサリー"),
]

customers: list[CustomerModel] = [
    CustomerModel(id=1, name="Alice", email="alice@example.com"),
    CustomerModel(id=2, name="Bob", email="bob@example.com"),
    CustomerModel(id=3, name="Charlie", email="charlie@example.com"),
]

products: list[ProductModel] = [
    ProductModel(id=1, name="ノートパソコン", price=999.99, description="高性能なノートパソコン"),
    ProductModel(id=2, name="スマートフォン", price=499.99, description="最新モデルのスマートフォン"),
    ProductModel(id=3, name="ヘッドホン", price=199.99, description="ノイズキャンセリング機能付きのヘッドホン"),
]

cart_items : list[CartItemModel] = [
    CartItemModel(cart_id=1, product_id=1, quantity=1),
    CartItemModel(cart_id=1, product_id=2, quantity=2),
    CartItemModel(cart_id=2, product_id=3, quantity=1),
]

orders: list[OrderModel] = [
    OrderModel(order_id=1, customer_id=1, quantity=2, total_price=1499.98),
    OrderModel(order_id=2, customer_id=2, quantity=1, total_price=199.99),
    OrderModel(order_id=3, customer_id=3, quantity=3, total_price=299.97),
]