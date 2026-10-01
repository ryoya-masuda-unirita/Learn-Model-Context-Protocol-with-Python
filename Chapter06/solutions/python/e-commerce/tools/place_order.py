"""顧客の新しい注文を作成する place_order tool の定義。"""
# @mcp.tool()
# def place_order(customer_id:int) -> Order:
#     """注文する"""
#     if customer_id != 0 and not any(customer.id == customer_id for customer in customers):
#         raise ValueError(f"customer_id が不正です: {customer_id}")

#     new_order = Order(0, customer_id)
#     orders.append(new_order)
#     return {"type": "text", "name": f"ID: {new_order.order_id},customer: {new_order.customer_id}"}

from typing import Any

from data import orders, customers
from .schema import OrderModel, PlaceOrderInputModel

async def handler(args: dict[str, Any]) -> OrderModel:
    """顧客の新しい注文を作成する。

    Parameters
    ----------
    args : dict[str, Any]
        tool に渡された引数。customer_id、quantity、total_price を持つ。

    Returns
    -------
    OrderModel
        作成した注文。order_id は新しく採番する。

    Raises
    ------
    ValueError
        存在しない顧客の ID が指定された場合。
    """
    order = PlaceOrderInputModel(**args)

    # 0 は「すべての顧客」のような特別な意味を持たないので、存在しない顧客として弾く
    if not any(customer.id == order.customer_id for customer in customers):
        raise ValueError(f"customer_id が不正です: {order.customer_id}")

    # 新しい ID で新しい注文を作る
    new_order = OrderModel(order_id=len(orders) + 1, customer_id=order.customer_id, quantity=order.quantity, total_price=order.total_price)
    orders.append(new_order)

    return new_order

tool_place_order: dict[str, Any] = {
    "name": "place_order",
    "description": "顧客の新しい注文を作成する",
    "input_schema": PlaceOrderInputModel,
    "handler": handler
}