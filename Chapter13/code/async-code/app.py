"""asyncio で複数のタスクを並行に実行する基本的なサンプル。"""
import asyncio

async def task(name: str, delay: float) -> None:
    """開始と終了を表示するだけのタスク。

    Parameters
    ----------
    name : str
        タスクの名前。
    delay : float
        終了までに待つ秒数。
    """
    print(f"タスク {name} を開始しました")
    # time.sleep() だとプログラム全体が止まるが、await asyncio.sleep() は待っている間にほかのタスクへ順番を譲る。
    # だから A・B・C は同時に始まり、短い順（B → A → C）に終わる
    await asyncio.sleep(delay)
    print(f"タスク {name} が {delay} 秒後に終了しました")

async def main() -> None:
    """3つのタスクを asyncio.gather で並行に実行する。"""
    await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3)
    )
    

# MCP の SDK は async で書かれているので、サンプルのクライアントも async def main() を asyncio.run() で動かしている
asyncio.run(main())