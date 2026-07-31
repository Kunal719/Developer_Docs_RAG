from pathlib import Path

PROJECT_VERSION = "v3"

GITHUB_REPO_URL = "https://github.com/langchain-ai/docs.git"
LOCAL_REPO_PATH =  Path("data/raw/docs")
DOCUMENTATION_PATH = Path("data/raw/docs/src/oss/langgraph")

PERSISTENT_DIRECTORY = Path("data/chromadb")
EMBEDDING_MODEL = "text-embedding-3-small"
COLLECTION_NAME = "langgraph_docs"
INDEX_PATH = Path("data/index_metadata.json")
BM25_PATH = Path("data/bm25/bm25_index.pkl")

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200

DENSE_TOP_K = 10
BM25_TOP_K = 10
HYBRID_TOP_K = 5
RRF_K = 60

RERANKER_MODEL = "BAAI/bge-reranker-base"
RERANK_CANDIDATES = 15
RERANK_TOP_K = 5

MODEL_NAME = "gpt-4.1-nano"
MODEL_PROVIDER = "openai"

REBUILD_INDEX = False