"""asyncio.wait で複数のコルーチンの完了を待つサンプル。"""
import asyncio

async def fetch_data(url: str) -> dict[str, str]:
   """URL からデータを取得する処理をシミュレートする。

   Parameters
   ----------
   url : str
       取得先の URL。

   Returns
   -------
   dict[str, str]
       取得したデータ。
   """
   print("データを取得しています...")
   await asyncio.sleep(1)
   return {"data": f"{url} からの結果: なんらかのデータ"}

async def main() -> None:
   """3つの取得処理を asyncio.wait で並行に実行し、結果を表示する。"""
   # Python 3.11 以降、asyncio.wait にはコルーチンではなくタスクを渡す必要がある
   done, _ = await asyncio.wait([
       asyncio.create_task(fetch_data("google.com")),
       asyncio.create_task(fetch_data("bing.com")),
       asyncio.create_task(fetch_data("yahoo.com"))
   ])

   # done は set なので、順番は決まっていない（実行するたびに表示の順番が変わることがある）。
   # 渡した順に結果がほしいなら gather を使う
   for task in done:
       print(task.result())

asyncio.run(main())