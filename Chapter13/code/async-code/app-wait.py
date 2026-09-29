import asyncio

async def fetch_data(url: str):
   print("データを取得しています...")
   await asyncio.sleep(1)
   return {"data": f"{url} からの結果: なんらかのデータ"}

async def main():
   done, _ = await asyncio.wait([
       fetch_data("google.com"),
       fetch_data("bing.com"),
       fetch_data("yahoo.com")
   ])

   for task in done:
       print(task.result())

asyncio.run(main())