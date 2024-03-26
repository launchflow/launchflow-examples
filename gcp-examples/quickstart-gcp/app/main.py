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
    to_write = io.BytesIO()
    to_write.write(file_contents.encode("utf-8"))
    to_write.seek(0)
    bucket.upload_file(to_write, file_name)
    return "OK"


@app.get("/{file_name}")
async def read_file(file_name: str) -> str:
    return bucket.download_file(file_name).decode("utf-8")
