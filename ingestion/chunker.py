from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents: list[Document], chunk_size: int, chunk_overlap: int) -> list[Document]:
    """
    Return the chunked documents with RecursiveCharacterTextSplitter using the chunk_size and chunk_overlap parameters

    Args:
        documents: List of documents to chunk
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks

    Returns:
        List of chunked documents
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""])
    return text_splitter.split_documents(documents)