from langchain_core.documents import Document

def format_retrieved_context(documents: list[Document]) -> str:
    """
    Returns the retrieved context in a format that LLM can perceive better

    Args:
        documents: List of retrieved documents from RAG pipeline
    Returns:
        Formatted documents with content and source in string format
    """
    return "\n\n"+"-"*80+"\n\n".join([f"Source: {doc.metadata.get('source', 'Unknown Source')}:\n\n" f"{doc.page_content}" for doc in documents])