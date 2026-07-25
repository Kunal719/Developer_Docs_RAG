from dotenv import load_dotenv

from app.llm import get_llm
from pipeline.initialization import initialize_resources
from pipeline.prepare_chunks import prepare_chunks
from ingestion.chunker import chunk_documents, assign_chunk_id
from ingestion.github_loader import RepositoryStatus
from ingestion.markdown_parser import load_selected_documents
from ingestion.metadata_extractor import extract_metadata
from ingestion.vector_store import delete_documents
from ingestion.document_index import update_index_metadata, detect_changes, ChangeSet
from ingestion.bm25_index import build_bm25_index, save_bm25_index, load_bm25_index
from retrieval.rag_chain import build_rag_chain
from retrieval.dense_retriever import DenseRetriever
from retrieval.bm25 import BM25Retriever
from retrieval.hybrid_retriever import HybridRetriever


# Configuration
from config import (
    DOCUMENTATION_PATH,
    INDEX_PATH,
    BM25_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    DENSE_TOP_K,
    BM25_TOP_K,
    HYBRID_TOP_K,
    RRF_K,
    MODEL_NAME,
    MODEL_PROVIDER
)

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
        repository_status, vector_store = initialize_resources()

        if repository_status is RepositoryStatus.CLONED:
            chunks = prepare_chunks()

            # Create bm25 index
            print("\nCreating bm25 index...")
            bm25_index = build_bm25_index(chunks, top_k=BM25_TOP_K)
            save_bm25_index(bm25_index, BM25_PATH)
            print("bm25 index created")

            # Add documents to vector store
            print("\nAdding documents to vector store...")
            vector_store.add_documents(chunks)
            print("Documents added to vector store")

            # Creating the metadata index
            change_set = ChangeSet(
                         new={chunk.metadata["source"] for chunk in chunks},
                         updated=set(),
                         deleted=set(),
                         has_changes=False)
            print("\nUpdating metadata index...")
            update_index_metadata(
                index_path=INDEX_PATH,
                change_set=change_set,
                docs_path=DOCUMENTATION_PATH,
            )
            print("Metadata index updated")
        
        elif repository_status is RepositoryStatus.UPDATED:

            print("\nDetecting documentation changes...")
            change_set = detect_changes(DOCUMENTATION_PATH, INDEX_PATH)

            if change_set.has_changes:
                print("Detected documentation changes: "f"{len(change_set.new)} new, "f"{len(change_set.updated)} updated, "f"{len(change_set.deleted)} deleted.")
                # Check for deleted documents first, then new and updated documents
                if change_set.deleted or change_set.updated:
                    print("\nDeleting old documents from vector store")
                    sources_to_delete = change_set.deleted | change_set.updated
                    delete_documents(vector_store, sources_to_delete)
                    print("Old documents deleted from vector store")
            
                if change_set.new or change_set.updated:
                    print("\nLoading and extracting metadata of new or updated documents...")
                    new_and_updated_docs = change_set.new | change_set.updated
                    documents = load_selected_documents(new_and_updated_docs, DOCUMENTATION_PATH)
                    documents = extract_metadata(documents, DOCUMENTATION_PATH)
                    print(f"Loaded and extracted metadata of {len(documents)} new or updated documents")

                    print("\nChunking documents and adding them to vector store...")
                    chunks = chunk_documents(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
                    assign_chunk_id(chunks)
                    print(f"Created {len(chunks)} chunks")
                    vector_store.add_documents(chunks)
                    print("New or updated documents added to vector store")

                # Update the metadata index
                print("\nUpdating metadata index...")
                update_index_metadata(
                    index_path=INDEX_PATH,
                    change_set=change_set,
                    docs_path=DOCUMENTATION_PATH,
                )
                print("Metadata index updated")

                # Create BM25 index again
                chunks = prepare_chunks()

                print("\nCreating bm25 index...")
                bm25_index = build_bm25_index(chunks, top_k=BM25_TOP_K)
                save_bm25_index(bm25_index, BM25_PATH)
                print("bm25 index created")
            
            else:
                print("No changes in documentation detected")
                print("\nLoading bm25 index...")
                bm25_index = load_bm25_index(BM25_PATH)
                print("bm25 index loaded")

        else:
            print("Repository already up to date. Skipping indexing")
            print("\nLoading bm25 index...")
            bm25_index = load_bm25_index(BM25_PATH)
            print("bm25 index loaded")


        print("\nBuilding retriever...")
        dense_retriever = DenseRetriever(vector_store=vector_store, top_k=DENSE_TOP_K)
        bm25_retriever = BM25Retriever(bm25_index=bm25_index)
        hybrid_retriever = HybridRetriever(bm25_retriever=bm25_retriever, dense_retriever=dense_retriever, top_k=HYBRID_TOP_K, rrf_k=RRF_K)
        print("Retriever ready")

        print("\nInitializing LLM...")
        llm = get_llm(
            model_name=MODEL_NAME,
            model_provider=MODEL_PROVIDER,
        )
        print("LLM ready")

        print("\nBuilding RAG pipeline...")
        rag_chain = build_rag_chain(
            retriever=hybrid_retriever,
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
            retrieved_docs = hybrid_retriever.retrieve(question)

            # print("\n" + "=" * 80)
            # print("Retrieved Documents")
            # print("=" * 80)
            # for i, doc in enumerate(retrieved_docs, start=1):
            #     print(f"{i}. {doc.metadata['source']}")
            #     # print(doc.page_content[:300])

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