"""商品の一覧を表示するサンプル。"""
# products.py は同じディレクトリにある。python app.py で実行すると、スクリプトのディレクトリが
# import の検索パスに入るので、どこから実行しても見つかる
from products import products

for p in products:
    print(f"{p.id}, {p.name}, {p.price}")
