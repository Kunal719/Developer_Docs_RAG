from langchain_core.documents import Document
from pathlib import Path

def extract_code_metadata(documents: list[Document], code_path: Path) -> list[Document]:
    """
    Normalize source paths and add implementation-specific metadata.

    Args:
        documents: List of documents to enrich

    Returns:
        List of enriched documents
    """
    for doc in documents:
        # Store the source as a path relative to the documentation root
        relative_source_path = Path(doc.metadata["source"]).relative_to(code_path)
        doc.metadata["source"] = relative_source_path.as_posix()

        # Add corpus
        doc.metadata["corpus"] = "implementation"

    # Keep documents which has page_content
    documents = [doc for doc in documents if doc.page_content.strip()]

    return documents