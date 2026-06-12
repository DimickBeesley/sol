from typing import Protocol, Iterator

class LLMBackend(Protocol):
    def chat(self, messages: list[dict], tools: list[dict] = []) -> Iterator[str]: ...
