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
        self.generation_model = os.getenv("OLLAMA_GENERATION_MODEL")
        self.embedding_model = os.getenv("OLLAMA_EMBED_MODEL")

    def generate(self, prompt):
        output = self.client.generate(model=self.generation_model, prompt=prompt).response
        return output

    def embed(self, text):
        embeddings = self.client.embed(model=self.embedding_model, input=text).embeddings
        return embeddings

    def stream(self, prompt):
        chunks = self.client.generate(model=self.generation_model, prompt=prompt, stream=true)
        for chunk in chunks:
            yield chunk.response
