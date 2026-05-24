import os
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.readers.obsidian import ObsidianReader
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding



load_dotenv()

def ingest():

    reader = ObsidianReader(
            input_dir=os.getenv("OBSIDIAN_PATH"),
            extract_tasks=False,
            remove_tasks_from_text=False,
    )

    documents = reader.load_data()

    vector_store = PGVectorStore.from_params(
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        password=os.getenv("POSTGRES_PW"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USR"),
        table_name="data_llamaindex",
        embed_dim=768,
    )

    embed_model = OllamaEmbedding(
        model_name=os.getenv("OLLAMA_EMBED_MODEL"),
        base_url=os.getenv("OLLAMA_HOST"),
    )

    storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
    )
    
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
    )

    print("Ingestion complete.")
