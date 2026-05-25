from app.backends.ollama import OllamaBackend
from app.backends.anthropic import AnthropicBackend
from app.rag.postgres_utils import get_vector_store, get_embed_model

from llama_index.core import VectorStoreIndex

class SolHarness():
    def __init__(self):
        self.history = []
        self.backend = None
        self.pg_vector_store = get_vector_store()
        self.index = VectorStoreIndex.from_vector_store(
                self.pg_vector_store,
                embed_model=get_embed_model()
        )
        self.retriever = self.index.as_retriever(
                vector_store_query_mode="default",
                similarity_top_k=15,
        )



    def get_backend(self, backend_id):
        if backend_id == "a":
            return AnthropicBackend()
        elif backend_id == "o":
            return OllamaBackend()
        else:
            raise ValueError(f"Unknown backend: {backend_id}")


    def call_generate(self, backend_id, prompt):
        call_context = ""
        self.backend = self.get_backend(backend_id)
        
        self.history.append(prompt)
        for entry in self.retriever.retrieve(prompt):
            call_context += entry.node.text
        for node in self.history:
            call_context += node
        
        response = self.backend.generate(call_context)
        self.history.append(response)

        print(response)


    def call_stream(self, backend_id, prompt):
        call_context = ""
        stream_dump = ""
        self.backend = self.get_backend(backend_id)
        
        self.history.append(prompt)
        for entry in self.retriever.retrieve(prompt):
            call_context += entry.node.text
        for node in self.history:
            call_context += node
        
        response = self.backend.stream(call_context)
        for chunk in response:
            print(chunk, end="", flush=True)
            stream_dump += chunk
        print()

        self.history.append(stream_dump)
        
