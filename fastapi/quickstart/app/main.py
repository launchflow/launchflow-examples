from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.infra import bucket


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bucket.connect_async()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/{file_name}")
async def write_file(file_name: str, file_contents: str):
    bucket.upload_file(file_contents, file_name)
    return {"message": "File written"}


@app.get("/{file_name}")
async def read_file(file_name: str) -> bytes:
    return bucket.download_file(file_name)
