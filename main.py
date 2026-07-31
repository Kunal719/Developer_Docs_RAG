from dotenv import load_dotenv

from pipeline.initialization import initialize_resources
from pipeline.build_rag_pipeline import build_rag_pipeline
from pipeline.prepare_retrieval_resources import prepare_retrieval_resources


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

        vector_store, bm25_index = prepare_retrieval_resources(repository_status=repository_status, vector_store=vector_store)

        rag_chain, _, _ , _= build_rag_pipeline(vector_store=vector_store, bm25_index=bm25_index)

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
            # retrieved_docs = hybrid_retriever.retrieve(question)

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