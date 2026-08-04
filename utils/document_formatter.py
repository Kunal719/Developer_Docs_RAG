from langchain_core.documents import Document

def format_retrieved_context(documents: list[Document]) -> str:
    """
    Returns the retrieved context in a format that LLM can perceive better

    Args:
        documents: List of retrieved documents from RAG pipeline
    Returns:
        Formatted documents with content and source in string format
    """
    formatted_documents = []

    for doc in documents:
        corpus = doc.metadata.get('corpus', 'unknown').capitalize()
        source = doc.metadata.get('source', 'unknown')
        title = doc.metadata.get('title', 'unknown')
        
        if corpus == "Documentation":
            formatted_doc = (
                "=== Documentation ===\n"
                f"Source: {source}\n"
                f"Title: {title}\n\n"
            )
        else:
            formatted_doc = (
                "=== Implementation (Python Source Code) ===\n"
                f"Source: {source}\n\n"
            )

        formatted_doc += ('\n' f"{doc.page_content}\n")

        formatted_documents.append(formatted_doc)

    return ("\n" + "=" * 80 + "\n\n").join(formatted_documents)