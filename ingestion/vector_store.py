from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from pathlib import Path

def build_vector_store(documents: list[Document], embedding_model: OpenAIEmbeddings, persistent_dir: Path, collection_name: str, rebuild: bool = False) -> Chroma:
    """
    Create or load a persistent Chroma vector store.

    If the collection already contains documents, it is reused.
    Otherwise, the provided documents are embedded and indexed.

    Args:
        documents: Chunked documents to index.
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

        chroma_store = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_model,
            persist_directory=str(persistent_dir),
            collection_metadata={"hnsw:space": "cosine"},
        )

        chroma_store.add_documents(documents)

    elif chroma_store._collection.count() == 0:
        chroma_store.add_documents(documents)

    return chroma_store