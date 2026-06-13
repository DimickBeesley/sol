from llama_index.core import VectorStoreIndex
from app.rag.postgres_utils import get_vector_store, get_embed_model

def retrieve_context(query: str):
    """Search the Obsidian vault for relevant context using the given query. Returns the most relevant chunks of documentation."""
    # TODO: extract vector store build out of this function and pass it as a parameter when the toool loop is all wired 
    pg_vector_store = get_vector_store()
    index = VectorStoreIndex.from_vector_store(
            pg_vector_store,
            embed_model=get_embed_model()
    )
    retriever = index.as_retriever(
            vector_store_query_mode="default",
            similarity_top_k=10,
    )
    results = retriever.retrieve(query)
    return "\n".join(entry.node.text for entry in results)
    

