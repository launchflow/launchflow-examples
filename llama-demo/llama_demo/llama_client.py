import httpx
from openai.types.chat import ChatCompletionMessageParam
from llama_demo.settings import settings
import openai
from typing import Dict, Any, Iterable


async def httpx_client():
    async with httpx.AsyncClient() as client:
        yield client


class LlamaClient:
    def __init__(self):
        self.client = openai.Client(
            base_url=settings.llama_server_address, api_key="no-api-key"
        )

    def chat(self, messages: Iterable[ChatCompletionMessageParam]):
        result = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",
            stream=True,
            max_tokens=int(settings.context_window / 2),
            timeout=600,
        )
        for r in result:
            content = r.choices[0].delta.content
            if content is not None:
                yield content
