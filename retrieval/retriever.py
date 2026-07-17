from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever


def build_retriever(vector_store: Chroma, k: int) -> VectorStoreRetriever:
    """
    Build the retriever for performing similarity search over the vector store

    Args:
        vector_store: The Chroma vector store containing indexed documents.
        k: Number of documents to retrieve for each query.

    Returns:
        A configured LangChain retriever.
    """
    return vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k": k}
    )