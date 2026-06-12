from .base import LLMBackend
from dotenv import load_dotenv
import os
import anthropic

load_dotenv()

class AnthropicBackend(LLMBackend):
    def __init__(self):
        self.anthropic_model = os.getenv("ANTHROPIC_MODEL")
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def chat(self, messages: list[dict], tools: list[dict] = []) -> Iterator[str]:
        with self.client.messages.stream(
            max_tokens=1024,
            messages=messages,
            model=self.anthropic_model,
        ) as stream:
            for text in stream.text_stream:
                yield text
