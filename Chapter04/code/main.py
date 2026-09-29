from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({'hello': '世界'})


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])

# uvicorn main:app