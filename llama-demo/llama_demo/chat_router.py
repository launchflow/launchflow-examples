from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends

from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from llama_demo.settings import settings
from llama_demo.schemas import Chat
from llama_demo.llama_client import LlamaClient

router = APIRouter(prefix="/v1", tags=["v1"])


class ChatResponse(BaseModel):
    content: str


@router.post("/chat", response_model=None)
async def chat(
    chat: Chat, model: Annotated[LlamaClient, Depends(LlamaClient)]
) -> StreamingResponse | JSONResponse:
    messages = []
    for message in chat.context:
        messages.append({"role": message.role, "content": message.content})

    context_string = "".join([msg["content"] for msg in messages])
    if len(context_string) > 512:
        trimmed_context = []
        current_length = 0
        for msg in reversed(messages):
            msg_length = len(msg["content"])
            if current_length + msg_length <= settings.context_window:
                trimmed_context.append(msg)
                current_length += msg_length
            else:
                num_to_append = msg_length - (settings.context_window - current_length)
                msg["content"] = msg["content"][-num_to_append:]
                trimmed_context.append(msg)
                break
        messages = list(reversed(trimmed_context))

    completion = model.chat(messages=messages)

    def iter_content():
        for item in completion:
            yield item

    if settings.streaming:
        return StreamingResponse(iter_content())

    full_content = ""
    for item in iter_content():
        full_content += item
    return JSONResponse(content={"content": full_content})
