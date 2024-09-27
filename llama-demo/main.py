from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from llama_demo.chat_router import router
from mangum import Mangum

from llama_demo.settings import settings

app = FastAPI()

app.include_router(router)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "navigation": [
                {
                    "caption": "Llama Chat Demo",
                    "href": "/",
                    "active": True,
                }
            ],
            "streaming": settings.streaming,
        },
    )


handler = Mangum(app, lifespan="off")
