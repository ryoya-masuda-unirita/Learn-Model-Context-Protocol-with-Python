import asyncio

async def task(name, delay):
    print(f"タスク {name} を開始しました")
    await asyncio.sleep(delay)
    print(f"タスク {name} が {delay} 秒後に終了しました")

async def main():
    await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3)
    )
    

asyncio.run(main())