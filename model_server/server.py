from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.responses import Response
from starlette.routing import Route
import asyncio

from model_server.llm_model import model

async def query(request):
    if request.client.host == '127.0.0.1':
        payload = await request.body()
        string = payload.decode("utf-8")
        responseQ = asyncio.Queue()
        await request.app.model_queue.put((string, responseQ))
        output = await responseQ.get()
        return JSONResponse({'modelOutput': output}, status_code=200)
    else:
        return Response(status_code=401)

async def serverLoop(q):
    while True:
        (string, responseQ) = await q.get()
        out = model.inference(string)
        await responseQ.put(out)


app = Starlette(
    routes=[
        Route("/query", query, methods=["POST"]),
    ],
)


@app.on_event("startup")
async def startup_event():
    q = asyncio.Queue()
    app.model_queue = q
    asyncio.create_task(serverLoop(q))