from dotenv import load_dotenv
from pathlib import Path

from app.llm import get_llm
from ingestion.chunker import chunk_documents
from ingestion.embedding_model import get_embedding_model
from ingestion.github_loader import load_repository
from ingestion.markdown_parser import load_documents
from ingestion.metadata_extractor import extract_metadata
from ingestion.vector_store import build_vector_store
from retrieval.rag_chain import build_rag_chain
from retrieval.retriever import build_retriever

# Configuration
GITHUB_REPO_URL = "https://github.com/langchain-ai/docs.git"
LOCAL_REPO_PATH =  Path("data/raw/docs")
DOCUMENTATION_PATH = Path("data/raw/docs/src/oss/langgraph")

PERSISTENT_DIRECTORY = Path("data/chromadb")
COLLECTION_NAME = "langgraph_docs"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
TOP_K = 4

MODEL_NAME = "gpt-4.1-nano"
MODEL_PROVIDER = "openai"

REBUILD_INDEX = False

def main() -> None:
    """
    Run the developer docs assistant
    """

    load_dotenv()

    print("=" * 60)
    print("Developer Documentation Assistant")
    print("=" * 60)
    print()

    try:
        print("[1/9] Loading repository...")
        repository_path = load_repository(GITHUB_REPO_URL, LOCAL_REPO_PATH)
        print("Repository ready")

        print("\n[2/9] Loading documentation...")
        documents = load_documents(DOCUMENTATION_PATH)
        print(f"Loaded {len(documents)} documents")

        print("\n[3/9] Extracting metadata...")
        documents = extract_metadata(documents)
        print("Metadata extracted")

        print("\n[4/9] Chunking documents...")
        chunks = chunk_documents(
            documents,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
        print(f"Created {len(chunks)} chunks")

        print("\n[5/9] Initializing embedding model...")
        embedding_model = get_embedding_model()
        print("Embedding model ready")

        print("\n[6/9] Building vector store...")
        vector_store = build_vector_store(
            documents=chunks,
            embedding_model=embedding_model,
            persistent_dir=PERSISTENT_DIRECTORY,
            collection_name=COLLECTION_NAME,
            rebuild=REBUILD_INDEX,
        )
        print("Vector store ready")

        print("\n[7/9] Building retriever...")
        retriever = build_retriever(
            vector_store=vector_store,
            k=TOP_K,
        )
        print("Retriever ready")

        print("\n[8/9] Initializing LLM...")
        llm = get_llm(
            model_name=MODEL_NAME,
            model_provider=MODEL_PROVIDER,
        )
        print("LLM ready")

        print("\n[9/9] Building RAG pipeline...")
        rag_chain = build_rag_chain(
            retriever=retriever,
            llm=llm,
        )
        print("RAG pipeline ready")

    except Exception as e:
        print(f"\nFailed to initialize the application:\n{e}")
        return

    print("\n" + "=" * 60)
    print("Ask questions about the documentation.")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:
        question = input("\nYou > ").strip()

        if not question:
            continue

        if question.lower() in {"exit", "quit"}:
            print("\nAssistant > Goodbye!")
            break

        try:
            # retrieved_docs = retriever.invoke(question)

            # print("\n" + "=" * 80)
            # print("Retrieved Documents")
            # print("=" * 80)

            # for i, doc in enumerate(retrieved_docs, start=1):
            #     print(f"\nDocument {i}")
            #     print(f"Source     : {doc.metadata.get('source')}")
            #     print(f"Title      : {doc.metadata.get('title')}")
            #     print(f"Description: {doc.metadata.get('description')}")
            #     print(f"Category   : {doc.metadata.get('category')}")
            #     print(f"Has Code   : {doc.metadata.get('has_code')}")
            #     print(f"Chunk Length: {len(doc.page_content)}")
            #     print("\nContent Preview:")
            #     print(doc.page_content[:300])   # First 300 characters
            #     print("\n" + "-" * 80)
            
            response = rag_chain.invoke(question)
            print(f"\nAssistant > {response}")

        except Exception as e:
            print(f"\nAssistant > Failed to process your request.\nError: {e}")


if __name__ == "__main__":
    main()