from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class BenchmarkQuestion:
    id: int
    category: str
    intent: str
    difficulty: str
    question: str

@dataclass
class RetrievedDocument:
    chunk_id: str
    source: str
    score: Optional[float] = None

@dataclass
class PipelineStage:
    name: str
    latency: float
    top_k: int
    documents: list[RetrievedDocument]

@dataclass
class ExperimentMetadata:
    version: str
    timestamp: datetime
    embedding_model: str
    llm: str
    chunk_size: int
    chunk_overlap: int
    dense_top_k: int
    bm25_top_k: int
    hybrid_top_k: int
    rrf_k: int
    reranker_top_k: Optional[int] = None
    reranker_name: Optional[str] = None

@dataclass
class GenerationMetrics:
    answer: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float
    generation_latency: float

@dataclass
class OverallMetrics:
    total_latency: float
    total_cost: float

@dataclass
class EvaluationResult:
    question: BenchmarkQuestion
    experiment_metadata: ExperimentMetadata
    pipeline_stages: list[PipelineStage]
    generation_metrics: GenerationMetrics
    overall_metrics: OverallMetrics