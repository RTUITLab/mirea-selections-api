import asyncio
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse

import app.models.user


app = FastAPI()


@app.get('/__health')
def healthcheck():
    return {}


@app.get('/')
async def test_sse(req: Request) -> EventSourceResponse:
    async def event_generator():
        count = 0
        while True:
            if await req.is_disconnected():
                print('Client disconnected')
                break

            print(count)
            yield { 'data': count, 'retry': 1 }
            count += 1

            await asyncio.sleep(1)

    return EventSourceResponse(event_generator())
