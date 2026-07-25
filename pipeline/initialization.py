from ingestion.embedding_model import get_embedding_model
from ingestion.github_loader import load_repository, RepositoryStatus
from ingestion.vector_store import build_vector_store
from langchain_chroma import Chroma

from config import GITHUB_REPO_URL, LOCAL_REPO_PATH, PERSISTENT_DIRECTORY, COLLECTION_NAME, REBUILD_INDEX

def initialize_resources() -> tuple[RepositoryStatus, Chroma]:
    """
    Initialize the application by preparing the repository,
    embedding model, and vector store.

    Returns:
        Repository status, embedding model, and vector store.
    """
    print("\nLoading repository...")
    _, repository_status = load_repository(GITHUB_REPO_URL, LOCAL_REPO_PATH)
    print("Repository ready")

    print("\nInitializing embedding model...")
    embedding_model = get_embedding_model()
    print("Embedding model ready")

    print("\nBuilding vector store...")
    vector_store = build_vector_store(
        embedding_model=embedding_model,
        persistent_dir=PERSISTENT_DIRECTORY,
        collection_name=COLLECTION_NAME,
        rebuild=REBUILD_INDEX,
    )
    print("Vector store ready")

    return repository_status, vector_store