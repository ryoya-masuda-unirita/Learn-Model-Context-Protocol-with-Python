"""Starlette の最小限の Web アプリケーション。

`uvicorn main:app` で起動し、ルートにアクセスすると JSON を返す。
"""
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request: Request) -> JSONResponse:
    """ルートへのリクエストに JSON で応答する。

    Parameters
    ----------
    request : Request
        受け取った HTTP リクエスト。

    Returns
    -------
    JSONResponse
        挨拶を含む JSON のレスポンス。
    """
    return JSONResponse({'hello': '世界'})


app: Starlette = Starlette(debug=True, routes=[
    Route('/', homepage),
])

# uvicorn main:app
