"""FastAPI の最小限の Web アプリケーション。"""
from fastapi import FastAPI

# FastAPI のアプリも Starlette と同じ ASGI アプリなので、uvicorn で起動する（例: uvicorn app:app）
app: FastAPI = FastAPI()

@app.get("/")
async def read_root() -> dict[str, str]:
    """ルートへのリクエストに挨拶を返す。

    Returns
    -------
    dict[str, str]
        挨拶を含む辞書。JSON に変換して返される。
    """
    return {"Hello": "世界"}