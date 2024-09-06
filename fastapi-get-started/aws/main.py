from typing_extensions import Optional
from fastapi import FastAPI
from infra import bucket

app = FastAPI()

@app.get("/")
def get_name(name: str = ""):
    if not name:
        return "Please provide a name"
    try:
        name_bytes = bucket.download_file(f"{name}.txt");
        return name_bytes.decode("utf-8")
    except:
        return f"{name} was not found"

@app.post("/")
def post_name(name: str):
    bucket.upload_from_string(name, f"{name}.txt")
    return "ok"
