""" imports """
import sys
sys.path.append('model_server')
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import asyncio
import uvicorn
from llm_model import model
from starlette.applications import Starlette

async def query(request):
    print(request.client.host)
    payload = await request.body()
    string = payload.decode("utf-8")
    responseQ = asyncio.Queue()
    # give user prompt to model queue
    await request.app.model_queue.put((string, responseQ))
    # wait for response from model 
    output = await responseQ.get()
    return JSONResponse({'modelOutput': output}, status_code=200)

async def serverLoop(q):
    while True:
        # when q is not empty 
        (string, responseQ) = await q.get()
        # get model output 
        out = model.inference(string)
        await responseQ.put(out)

app = Starlette(
    routes=[
        Route("/query", query, methods=["POST"]),
    ],
)

@app.on_event("startup")
async def startup_event():
    # initalise global queue 
    q = asyncio.Queue()
    app.model_queue = q
    asyncio.create_task(serverLoop(q))

if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, host="0.0.0.0", log_level="info")
    