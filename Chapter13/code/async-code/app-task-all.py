"""asyncio.wait の ALL_COMPLETED で、すべてのタスクの完了を待つサンプル。"""
import asyncio
from typing import List

async def create_task(name:str, delay:int, workload: List[int], find_value:int) -> str:
   """待機した後、workload から値を探すタスク。

   Parameters
   ----------
   name : str
       タスクの名前。
   delay : int
       探し始める前に待つ秒数。
   workload : List[int]
       探索対象の値のリスト。
   find_value : int
       探す値。

   Returns
   -------
   str
       見つかったかどうかを伝えるメッセージ。
   """
   print(f"タスク {name} を開始しました")
   await asyncio.sleep(delay)
   # workload をループし、値が見つかれば返す。見つからなければ -1 を返す
   for no in workload:
      if no == find_value:
         return f"タスク {name} が {no} を見つけました"
   return f"{name} では見つかりませんでした"

async def main() -> None:
    """3つのタスクを実行し、すべて完了してから結果を表示する。"""
    tasks = [
        create_task("A", 3, [1, 2, 3], 2),
        create_task("B", 1, [4, 5, 6], 2),
        create_task("C", 5, [7, 8, 9], 2),
    ]

    finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    for x in finished:
       print("タスクの結果:", x.result())

asyncio.run(main())