from ingestion.github_loader import load_repository, RepositoryStatus
from ingestion.vector_store import build_vector_store
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from config import REBUILD_INDEX

def initialize_resources(
        github_repo_url: str,
        local_repo_path: str,
        sparse_paths: list[str],
        persistent_directory: str,
        collection_name: str,
        embedding_model: OpenAIEmbeddings) -> tuple[RepositoryStatus, Chroma]:
    """
    Initialize the application by preparing the repository,
    embedding model, and vector store.

    Returns:
        Repository status, embedding model, and vector store.
    """
    print("\nSyncing repository...")
    _, repository_status = load_repository(github_repo_url, sparse_paths, local_repo_path)
    print("Repository ready")

    print("\nBuilding vector store...")
    vector_store = build_vector_store(
        embedding_model=embedding_model,
        persistent_dir=persistent_directory,
        collection_name=collection_name,
        rebuild=REBUILD_INDEX
    )
    print("Vector store ready")

    return repository_status, vector_store