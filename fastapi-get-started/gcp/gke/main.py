from fastapi import FastAPI
import launchflow as lf

app = FastAPI()

@app.get("/")
def index(name: str = ""):
    return f"Hello from {lf.project}/{lf.environment}"
