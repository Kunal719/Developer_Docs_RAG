from pathlib import Path

from ingestion.markdown_parser import load_documents
from ingestion.metadata_extractor import extract_metadata
from ingestion.github_loader import load_repository

repo_path = load_repository("https://github.com/langchain-ai/docs.git", Path("data/raw/docs"))
docs = load_documents(
    Path("data/raw/docs/src/oss/python/langgraph")
)

docs = extract_metadata(docs)

print(f"Loaded {len(docs)} documents\n")

doc = docs[0]

print(doc.metadata)
print()
print(doc.page_content[:500])