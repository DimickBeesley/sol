from .base import LLMBackend
from dotenv import load_dotenv
import os
import anthropic

load_dotenv()

class AnthropicBackend(LLMBackend):
    def __init__(self):
        self.anthropic_model = os.getenv("ANTHROPIC_MODEL")
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def generate(self, prompt):
        output = self.client.messages.create(
            max_tokens=1024,
            messages=[{
                "content": prompt,
                "role": "user"
            }],
            model=self.anthropic_model,
        )
        return output.content[0].text

    def embed(self, text):
        raise NotImplementedError("Anthropic backend does not support embeddings")

    def stream(self, prompt):
        with self.client.messages.stream(
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
            model=self.anthropic_model,
        ) as stream:
            for text in stream.text_stream:
                yield text
