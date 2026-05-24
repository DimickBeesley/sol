import os
from dotenv import load_dotenv

from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding

load_dotenv()

def get_embed_model() -> OllamaEmbedding:
    return OllamaEmbedding(
        model_name=os.getenv("OLLAMA_EMBED_MODEL"),
        base_url=os.getenv("OLLAMA_HOST"),
    )

def get_vector_store() -> PGVectorStore:
    return PGVectorStore.from_params(
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        password=os.getenv("POSTGRES_PW"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USR"),
        table_name="data_llamaindex",
        embed_dim=768,
    )
