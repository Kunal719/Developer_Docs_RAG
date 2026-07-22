from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from pathlib import Path

def build_vector_store(embedding_model: OpenAIEmbeddings, persistent_dir: Path, collection_name: str, rebuild: bool = False) -> Chroma:
    """
    Create or load a persistent Chroma vector store. 
    If rebuild is True, the existing collection will be deleted and recreated.

    Args:
        embedding_model: Embedding model used for indexing and retrieval.
        persist_directory: Directory where the Chroma database is stored.
        collection_name: Name of the Chroma collection.
        rebuild: Whether to rebuild the collection from scratch.

    Returns:
        A configured Chroma vector store.
    """
    
    chroma_store = Chroma(collection_name=collection_name, 
                          persist_directory=str(persistent_dir), 
                          embedding_function=embedding_model, 
                          collection_metadata={"hnsw:space": "cosine"})

    if rebuild:
        chroma_store.delete_collection()

        chroma_store = Chroma(collection_name=collection_name, 
                              persist_directory=str(persistent_dir), 
                              embedding_function=embedding_model, 
                              collection_metadata={"hnsw:space": "cosine"})

    return chroma_store


def delete_documents(vector_store: Chroma, sources: set[str]) -> None:
    """
    Delete documents from the vector store.

    Args:
        vector_store: The Chroma vector store containing indexed documents.
        sources: Relative document paths whose chunks should be removed.
    """
    if not sources:
        return
    
    # Find all IDs of vectors using metadata.source
    results = vector_store.get(where={"source": {"$in": list(sources)}}, limit=100000)
    vector_ids = results["ids"]

    if vector_ids:
        vector_store.delete(ids=vector_ids)
        print(f"Successfully deleted {len(vector_ids)} chunks belonging to those source paths.")
    else:
        print("No document chunks were found matching those source paths.")