from .base import LLMBackend
from dotenv import load_dotenv
import os
import ollama

load_dotenv()
ollama_host = os.getenv("OLLAMA_HOST")

class OllamaBackend(LLMBackend):
    def __init__(self):
        self.host = ollama_host
        self.client = ollama.Client(host=self.host)
        self.model = os.getenv("OLLAMA_GENERATION_MODEL")

    def complete(self, messages: list[dict], tools: list[dict] = []):
        return self.client.chat(
            model=self.model,
            messages=messages,
            tools=tools if tools else None,
        ).message

    def chat(self, messages: list[dict], tools: list[dict] = []) -> Iterator[str]:
        stream = self.client.chat(
            model=self.model,
            messages=messages,
            tools=tools if tools else None,
            stream=True,
        )
        for chunk in stream:
            if chunk.message.content:
                yield chunk.message.content
