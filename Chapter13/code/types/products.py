"""型ヒントを使った商品クラスと、そのサンプルデータ。"""
from typing import List, Dict, Literal, Optional, Union, Any

class Product:
    """商品。

    Attributes
    ----------
    id : str
        商品の ID。
    name : str
        商品名。
    price : float
        価格。
    """

    def __init__(self, id: str, name: str, price: float) -> None:
        """商品を作る。

        Parameters
        ----------
        id : str
            商品の ID。
        name : str
            商品名。
        price : float
            価格。
        """
        self.id = id
        self.name = name
        self.price = price

products: List[Product] = []

products.append(Product(id="1", name="商品 1", price=10.0))

if __name__ == "__main__":
   for p in products:
      print(f"{p.id}, {p.name}, {p.price}")
