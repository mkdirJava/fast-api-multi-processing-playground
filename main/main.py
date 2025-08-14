from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

import httpx
import requests
from fastapi import FastAPI

threadPool = ThreadPoolExecutor(max_workers=4)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    print("Shutting down thread pool...")
    threadPool.shutdown(wait=True)
    print("Thread pool shut down.")


app = FastAPI(
    title="FastAPI Example", description="A simple FastAPI application", version="1.0.0"
)


from enum import Enum

from fastapi import Query


class CallType(str, Enum):
    blocking = "blocking"
    non_blocking = "non_blocking"
    non_blocking_method = "non_blocking_method"


@app.get("/")
def entry(
    call_type: CallType = Query(
        CallType.blocking, description="Type of call: blocking or non_blocking"
    )
):
    match call_type:
        case CallType.blocking:
            return requests.get("http://localhost:9000/blocking-io", timeout=10).json()
        case CallType.non_blocking:
            threadPool.submit(
                lambda: (
                    requests.get(
                        "http://localhost:9000/non-blocking-io", timeout=10
                    ).json()
                )
            )
            return {
                "message": "I fired and do not need to return the result",
            }
        case CallType.non_blocking_method:
            none_blocking_io()
            return {
                "message": "I fired and do not need to return the result",
            }


async def none_blocking_io():
    async with httpx.AsyncClient() as client:
        await client.get("http://localhost:9000/non-blocking-io", timeout=10)
    return {"message": "This is a non-blocking IO endpoint!"}
