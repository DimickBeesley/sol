import os
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, StorageContext
from app.rag.obsidian_reader import ObsidianReader
from app.rag.postgres_utils import get_vector_store, get_embed_model

load_dotenv()

def ingest():

    reader = ObsidianReader(
            input_dir=os.getenv("OBSIDIAN_PATH"),
            extract_tasks=False,
            remove_tasks_from_text=False,
    )

    documents = reader.load_data()

    vector_store = get_vector_store()

    embed_model = get_embed_model()

    storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
    )
    
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
    )

    print("Ingestion complete.")
