from langchain_core.documents import Document
import frontmatter
from pathlib import Path

def extract_metadata(documents: list[Document], docs_path: Path) -> list[Document]:
    """
    Enrich Langchain Documents with metadata like title, category, code presence, etc

    Args:
        documents: List of documents to enrich

    Returns:
        List of enriched documents
    """
    for doc in documents:
        parsed_doc = frontmatter.loads(doc.page_content)
        doc.metadata.update(parsed_doc.metadata)
        doc.page_content = parsed_doc.content

        # Check if code is present
        doc.metadata["has_code"] = "```" in doc.page_content

        # Store the source as a path relative to the documentation root
        relative_source_path = Path(doc.metadata["source"]).relative_to(docs_path)
        doc.metadata["source"] = relative_source_path.as_posix()

        # Assign category to document based on path
        doc_source = Path(doc.metadata["source"])
        if "errors" in doc_source.parts:
            doc.metadata["category"] = "errors"
        elif "frontend" in doc_source.parts:
            doc.metadata["category"] = "frontend"
        else:
            doc.metadata["category"] = "general"
   
    return documents

