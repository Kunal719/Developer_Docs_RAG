from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from pathlib import Path
import pickle

def build_bm25_index(documents: list[Document], top_k: int) -> BM25Retriever:
    """
    Build a BM25 index from the documentation

    Args:
        docs_path: The path to the documentation.

    Returns:
        A configured BM25 LangChain retriever.
    """ 
    return BM25Retriever.from_documents(documents, k=top_k)

def save_bm25_index(bm25_index: BM25Retriever, path: Path) -> None:
    """
    Save the BM25 index to a persistent directory under data

    Args:
        bm25_index: The BM25 index to be saved
        directory: The directory to save the index
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(bm25_index, f, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"BM25 index saved to {path}")

def load_bm25_index(path: Path) -> BM25Retriever:
    """
    Load the BM25 index from a persistent directory under data

    Args:
        directory: The directory to load the index

    Returns:
        The loaded BM25 index
    """
    with open(path, "rb") as f:
        return pickle.load(f)