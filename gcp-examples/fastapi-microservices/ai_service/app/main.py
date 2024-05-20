from contextlib import asynccontextmanager
import io

from app.infra import bucket

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bucket.connect_async()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/{file_name}")
async def write_file(file_name: str, file_contents: str):
    bucket.upload_from_string(file_contents, file_name)
    return "OK"


@app.get("/{file_name}")
async def read_file(file_name: str) -> str:
    return bucket.download_file(file_name).decode("utf-8")
