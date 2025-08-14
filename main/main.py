from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

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

from fastapi import Query


@app.get("/")
def entry(callBlocking: bool = Query(None, description=" should call blocking IO")):
    if callBlocking:
        #  This http request needs the results of the call
        return requests.get("http://localhost:9000/blocking-io", timeout=10).json()
    else:
        #  This http request does not need the results of the call
        threadPool.submit(
            lambda: (
                requests.get("http://localhost:9000/non-blocking-io", timeout=10).json()
            )
        )
        return {
            "message": "I fired and do not need to return the result",
        }
