import asyncio

async def fetch_data(url: str):
   print("データを取得しています...")
   await asyncio.sleep(1)
   return {"data": f"{url} からの結果: なんらかのデータ"}

async def main():
   # 複数のコルーチンを別々の引数として渡し、正しくまとめて実行する
   results = await asyncio.gather(
       fetch_data("google.com"),
       fetch_data("bing.com"),
       fetch_data("yahoo.com"),
   )

   print(results)

asyncio.run(main())