"""asyncio.gather で複数のコルーチンを並行に実行するサンプル。"""
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
   """3つの取得処理を asyncio.gather で並行に実行し、結果を表示する。"""
   # 複数のコルーチンを別々の引数として渡し、正しくまとめて実行する
   # gather の結果は、終わった順ではなく渡した順に並ぶ。それぞれ1秒かかるが、並行に動くので全体も約1秒で終わる
   results = await asyncio.gather(
       fetch_data("google.com"),
       fetch_data("bing.com"),
       fetch_data("yahoo.com"),
   )

   print(results)

asyncio.run(main())