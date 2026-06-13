from typing import Protocol, Iterator

class LLMBackend(Protocol):
    def chat(self, messages: list[dict], tools: list[dict] = [], tool_map: dict = {}) -> Iterator[str]: ...
