"""最初に結果を出したタスクを採用し、残りをキャンセルするサンプル。"""
# python
import asyncio
from typing import List, Optional

async def search_task(name: str, delay: int, workload: List[int], find_value: int, stop: asyncio.Event) -> Optional[str]:
    """待機した後、workload から値を探すタスク。見つけたら stop を立てる。

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
    stop : asyncio.Event
        ほかのタスクが見つけたことを知らせるイベント。

    Returns
    -------
    Optional[str]
        値を見つけたらタスクの名前。見つからなければ None。

    Raises
    ------
    asyncio.CancelledError
        タスクがキャンセルされた場合。
    """
    try:
        print(f"タスク {name} を開始しました")
        await asyncio.sleep(delay)             # I/O をシミュレートする
        if stop.is_set():
            return None
        for no in workload:
            await asyncio.sleep(0)            # キャンセルできるように制御を譲る
            if no == find_value:
                stop.set()
                return name
        return None
    except asyncio.CancelledError:
        print(f"タスク {name} がキャンセルされました")
        raise

async def main() -> None:
    """3つのタスクを実行し、最初に値を見つけたタスクを表示して残りをキャンセルする。"""
    stop = asyncio.Event()
    tasks = [
        asyncio.create_task(search_task("A", 3, [1,2,3], 2, stop)),
        asyncio.create_task(search_task("B", 1, [4,5,6], 2, stop)),
        asyncio.create_task(search_task("C", 5, [7,8,9], 2, stop)),
    ]

    try:
        for finished in asyncio.as_completed(tasks):
            res = await finished
            if res:
                print("見つかったタスク:", res)
                break
    finally:
        for t in tasks:
            if not t.done():
                t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())