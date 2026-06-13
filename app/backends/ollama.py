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

    def chat(self, messages: list[dict], tools: list[dict] = [], tool_map: dict = {}) -> Iterator[str]:
        current_messages = messages.copy()

        # Tool loop — non-streaming so we can inspect tool calls before yielding text
        while True:
            response = self.client.chat(
                model=self.model,
                messages=current_messages,
                tools=tools if tools else None,
            )

            if not response.message.tool_calls:
                break

            # Only append to messages if tools were actually called
            current_messages.append(response.message)
            for tool_call in response.message.tool_calls:
                fn = tool_map.get(tool_call.function.name)
                if fn:
                    result = fn(**tool_call.function.arguments)
                    current_messages.append({
                        "role": "tool",
                        "content": str(result),
                    })

        # Stream the final response once tool calls are exhausted
        stream = self.client.chat(
            model=self.model,
            messages=current_messages,
            tools=tools if tools else None,
            stream=True,
        )
        for chunk in stream:
            if chunk.message.content:
                yield chunk.message.content
