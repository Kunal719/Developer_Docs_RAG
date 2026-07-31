from app.llm import get_llm
from langchain_core.language_models.chat_models import BaseChatModel
from retrieval.rag_chain import build_rag_chain
from retrieval.dense_retriever import DenseRetriever
from retrieval.bm25 import BM25Retriever
from retrieval.hybrid_retriever import HybridRetriever
from reranking.cross_encoder import CrossEncoderReranker
from langchain_chroma import Chroma
from langchain_core.runnables import Runnable



# Configuration
from config import (
    DENSE_TOP_K,
    HYBRID_TOP_K,
    RRF_K,
    MODEL_NAME,
    MODEL_PROVIDER,
    RERANKER_MODEL,
    RERANK_TOP_K
)

def build_rag_pipeline(vector_store: Chroma, bm25_index: BM25Retriever) -> tuple[Runnable, HybridRetriever, CrossEncoderReranker, BaseChatModel]:
    """
    Build the runtime RAG pipeline.

    Initializes the retrievers, reranker, language model,
    and constructs the RAG chain.

    Returns:
        The RAG chain, hybrid retriever, and reranker.
    """
    
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

    print("\nInitializing reranker...")
    cross_encoder_reranker = CrossEncoderReranker(
        rerank_model=RERANKER_MODEL,
        top_k=RERANK_TOP_K
    )
    print("Reranker ready")

    print("\nBuilding RAG pipeline...")
    rag_chain = build_rag_chain(
        retriever=hybrid_retriever,
        reranker=cross_encoder_reranker,
        llm=llm,
    )
    print("RAG pipeline ready")

    return rag_chain, hybrid_retriever, cross_encoder_reranker, llm