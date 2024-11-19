""" imports """
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import asyncio
from model_server.llm_model import model
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

# only allow api calls from localhost (flask app)
middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=['localhost', "testclient", 'testserver'])
]

async def query(request):
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
    middleware=middleware,
)

@app.on_event("startup")
async def startup_event():
    # initalise global queue 
    q = asyncio.Queue()
    app.model_queue = q
    asyncio.create_task(serverLoop(q))