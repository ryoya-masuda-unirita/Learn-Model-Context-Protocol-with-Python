import asyncio
from typing import List

async def create_task(name:str, delay:int, workload: List[int], find_value:int) -> str:
   print(f"タスク {name} を開始しました")
   await asyncio.sleep(delay)
   # workload をループし、値が見つかれば返す。見つからなければ -1 を返す
   for no in workload:
      if no == find_value:
         return f"タスク {name} が {no} を見つけました"
   return f"{name} では見つかりませんでした"

async def main():
    tasks = [
        create_task("A", 3, [1, 2, 3], 2),
        create_task("B", 1, [4, 5, 6], 2),
        create_task("C", 5, [7, 8, 9], 2),
    ]

    finished, unfinished = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    for x in finished:
       print("タスクの結果:", x.result())

asyncio.run(main())