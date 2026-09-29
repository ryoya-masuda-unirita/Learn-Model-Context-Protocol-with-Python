"""商品の一覧を表示するサンプル。"""
from products import products

for p in products:
    print(f"{p.id}, {p.name}, {p.price}")
