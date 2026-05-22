import app.ingestion.pg_connection as pg_connection

import os
from dotenv import load_dotenv

#from llama_index_core import 
from llama_index.readers.obsidian import ObsidianReader
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding



load_dotenv()

def ingest():

    vector_store = PGVectorStore.from_params(
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        password=os.getenv("POSTGRES_PW"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USR"),
        table_name="data_llamaindex"
        embed_dim=768
    )

    reader = ObsidianReader(
            input_dir=os.getenv("OBSIDIAN_PATH"),
            extract_tasks=False,
            remove_tasks_from_text=False,
    )

    embed_model = OllamaEmbedding(
            model_name=os.getenv("OLLAMA_EMBED_MODEL"),
            base_url=os.getenv("OLLAMA_HOST"),
    )

    return
