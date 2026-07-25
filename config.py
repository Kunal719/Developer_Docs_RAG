from pathlib import Path

GITHUB_REPO_URL = "https://github.com/langchain-ai/docs.git"
LOCAL_REPO_PATH =  Path("data/raw/docs")
DOCUMENTATION_PATH = Path("data/raw/docs/src/oss/langgraph")

PERSISTENT_DIRECTORY = Path("data/chromadb")
COLLECTION_NAME = "langgraph_docs"
INDEX_PATH = Path("data/index_metadata.json")
BM25_PATH = Path("data/bm25/bm25_index.pkl")

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200

DENSE_TOP_K = 5
BM25_TOP_K = 5
HYBRID_TOP_K = 5
RRF_K = 60

MODEL_NAME = "gpt-4.1-nano"
MODEL_PROVIDER = "openai"

REBUILD_INDEX = False