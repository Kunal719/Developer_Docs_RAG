from dotenv import load_dotenv
from pathlib import Path

from pipeline.initialization import initialize_resources
from pipeline.build_rag_pipeline import build_rag_pipeline
from pipeline.prepare_retrieval_resources import prepare_retrieval_resources

from evaluation.benchmark_runner import BenchmarkRunner
from evaluation.result_writer import ResultWriter


def main() -> None:
    """
    Run the evaluation benchmark against the developer documentation assistant.
    """

    load_dotenv()

    print("=" * 60)
    print("Developer Documentation Assistant Evaluation")
    print("=" * 60)
    print()

    try:
        repository_status, vector_store = initialize_resources()

        vector_store, bm25_index = prepare_retrieval_resources(repository_status=repository_status, vector_store=vector_store)

        _, hybrid_retriever, cross_encoder_reranker, llm = build_rag_pipeline(vector_store=vector_store, bm25_index=bm25_index)

        print("\nRunning benchmark...")
        benchmark_runner = BenchmarkRunner(
            retriever=hybrid_retriever,
            llm=llm,
            questions_path=Path("evaluation/benchmark_advanced_questions.json"),
            reranker=None
        )

        results = benchmark_runner.run()

        output_path = ResultWriter.save(results)

        print("\nBenchmark completed successfully.")
        print(f"\nResults saved to: {output_path}")

    except Exception as e:
        print(f"\nBenchmark execution failed:\n{e}")
        return


if __name__ == "__main__":
    main()