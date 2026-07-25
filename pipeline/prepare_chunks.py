from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from ingestion.markdown_parser import load_documents
from ingestion.metadata_extractor import extract_metadata
from ingestion.chunker import chunk_documents, assign_chunk_id

from config import DOCUMENTATION_PATH, CHUNK_SIZE, CHUNK_OVERLAP

def prepare_chunks() -> list[Document]:
    """
    Prepare the chunks of the documentation
    """
    print("\nLoading documentation...")
    documents = load_documents(DOCUMENTATION_PATH)
    print(f"Loaded {len(documents)} documents")

    print("\nExtracting metadata...")
    documents = extract_metadata(documents, DOCUMENTATION_PATH)
    print("Metadata extracted")

    print("\nChunking documents...")
    chunks = chunk_documents(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    assign_chunk_id(chunks)
    print(f"Created {len(chunks)} chunks")

    return chunks