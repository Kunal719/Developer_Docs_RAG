from retrieval.rag_chain import build_rag_chain
from retrieval.rag_chain_v3 import build_hybrid_rag_chain
from retrieval.base import BaseRetriever
from prompt.rag_prompt import rag_prompt
from reranking.base_reranker import BaseReranker
from evaluation.observer import PipelineObserver
from langchain_core.language_models.chat_models import BaseChatModel

from evaluation.benchmark_loader import load_questions
from evaluation.models import EvaluationResult, ExperimentMetadata, OverallMetrics

from time import perf_counter

from config import (
    EMBEDDING_MODEL, 
    MODEL_NAME, 
    CHUNK_OVERLAP, 
    CHUNK_SIZE, 
    DENSE_TOP_K, 
    BM25_TOP_K, 
    HYBRID_TOP_K, 
    RRF_K, 
    RERANK_TOP_K,
    RERANKER_MODEL,
    PROJECT_VERSION)

from pathlib import Path
from datetime import datetime

class BenchmarkRunner():
    def __init__(self, retriever: BaseRetriever, llm: BaseChatModel, questions_path: Path, reranker: BaseReranker | None = None):
        self._retriever = retriever
        self._reranker = reranker
        self._llm = llm
        self._questions_path = questions_path

    def run(self) -> list[EvaluationResult]:
        experiment_metadata = ExperimentMetadata(
            version=PROJECT_VERSION,
            timestamp=datetime.now(),
            embedding_model=EMBEDDING_MODEL,
            llm=MODEL_NAME,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            dense_top_k=DENSE_TOP_K,
            bm25_top_k=BM25_TOP_K,
            hybrid_top_k=HYBRID_TOP_K,
            rrf_k=RRF_K,
            reranker_top_k=RERANK_TOP_K if self._reranker is not None else None,
            reranker_name=RERANKER_MODEL if self._reranker is not None else None
        )

        questions = load_questions(self._questions_path)

        observer = PipelineObserver()
        if self._reranker is None:
            chain = build_hybrid_rag_chain(self._retriever, self._llm, rag_prompt, observer=observer)
        else:
            chain = build_rag_chain(self._retriever, self._reranker, self._llm, rag_prompt, observer=observer)

        results : list[EvaluationResult] = []

        for question in questions:
            observer.reset()

            start = perf_counter()
            answer = chain.invoke(question.question)
            end = perf_counter()

            generation_metrics = observer.get_generation_metrics()

            overall_metrics = OverallMetrics(
                total_latency = (end - start),
                total_cost = generation_metrics.estimated_cost
            )

            results.append(EvaluationResult(
                question=question,
                pipeline_stages=observer.get_pipeline_stages(),
                generation_metrics=generation_metrics,
                overall_metrics=overall_metrics,
                experiment_metadata=experiment_metadata
            ))

        return results

        