import uuid
from fastapi import FastAPI
from concurrent.futures import ThreadPoolExecutor

from datetime import datetime

from fastapi import FastAPI
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
import time

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
    title="FastAPI Example",
    description="A simple FastAPI application",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/non-blocking-io")
async def none_blocking_io():
    threadPool.submit(lambda: (time.sleep(2), print(f"Current date: {datetime.now()}")))
    return {"message": "This is a non-blocking IO endpoint!"}


@app.get("/blocking-io")
def blocking_io():
    time.sleep(2)
    print(f"Current date: {datetime.now()}")
    return {
        "message": "This is a blocking IO endpoint!",
    }
