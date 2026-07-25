# Developer Docs RAG

A production-inspired Retrieval-Augmented Generation (RAG) project that answers developer questions using **official documentation** instead of relying solely on an LLM's internal knowledge.

Unlike many RAG tutorials that stop after indexing a set of documents into a vector database, this repository is intentionally built as an **iterative engineering project**. Each version introduces one architectural improvement while preserving and extending the previous implementation, allowing the system to evolve from a simple Dense RAG pipeline into a production-oriented developer documentation assistant.

---

# Why This Project?

Most RAG examples demonstrate the retrieval pipeline but assume the knowledge base is static.

Real-world systems are different.

Documentation changes continuously, repositories evolve, retrieval quality becomes increasingly important, and systems must be evaluated before introducing more advanced retrieval strategies.

The goal of this repository is to explore that evolution step by step by implementing production-inspired improvements rather than building multiple disconnected RAG projects.

Each version focuses on a single architectural enhancement while maintaining a clean, modular codebase.

This makes it possible to evaluate the impact of every change independently rather than combining multiple techniques into a single iteration. The project evolves through measured engineering decisions supported by benchmarking rather than feature accumulation.

---

# Current Implementation

The project currently consists of three completed milestones.

## ✅ Version 1 — Dense RAG

Version 1 established the complete Dense RAG pipeline from scratch.

Features include:

* GitHub repository ingestion
* Markdown / MDX parsing
* Metadata extraction
* Recursive document chunking
* OpenAI embeddings (`text-embedding-3-small`)
* Persistent Chroma vector database
* Dense semantic retrieval
* LCEL-based RAG pipeline
* Interactive CLI

---

## ✅ Version 2 — Incremental Indexing

Version 2 focuses on making the ingestion pipeline significantly more efficient.

Instead of rebuilding the vector database whenever documentation changes, the application updates only the affected documents.

Version 2 introduces:

* Sparse checkout repository synchronization
* SHA-256 document change detection
* Metadata index for tracked documents
* Detection of:

  * Newly added documents
  * Modified documents
  * Deleted documents
* Selective document loading
* Selective vector deletion
* Incremental embedding generation
* Persistent Chroma updates
* Automatic indexing skip when documentation has not changed

The retrieval pipeline remains unchanged while the indexing pipeline becomes significantly more efficient.

---

## ✅ Version 3 — Hybrid Retrieval

Version 3 focuses on improving retrieval quality by combining dense semantic search with sparse lexical search.

Instead of relying solely on vector similarity, the retrieval pipeline now fuses results from both retrieval strategies using Reciprocal Rank Fusion (RRF), improving recall for API names, function names, and exact developer terminology while preserving semantic search capabilities.

Version 3 introduces:

* Dense Retriever abstraction
* BM25 lexical retrieval
* Hybrid Retriever
* Reciprocal Rank Fusion (RRF)
* Unified retrieval interface
* Improved retrieval for API-centric queries
* Prompt refinement to encourage evidence-based synthesis across retrieved documentation

---

# Project Overview

The knowledge source for this project is the official **LangGraph documentation** from the LangChain GitHub repository.

The application performs two independent workflows.

## Indexing Pipeline

The indexing pipeline keeps the local vector database synchronized with the latest documentation.

```text
GitHub Repository
        │
        ▼
Sparse Checkout Synchronization
        │
        ▼
Repository Status
        │
 ┌──────┴─────────────┐
 │                    │
 │              Repository Updated
 │                    │
 │                    ▼
 │           SHA-256 Change Detection
 │                    │
 │                    ▼
 │        Delete Updated / Removed Vectors
 │                    │
 │                    ▼
 │          Load Changed Documents
 │                    │
 │                    ▼
 │          Metadata Extraction
 │                    │
 │                    ▼
 │               Document Chunking
 │                    │
 │                    ▼
 │          OpenAI Embedding Model
 │                    │
 │                    ▼
 │      Persistent Chroma Vector Store
 │
 ▼
Repository Unchanged
        │
        ▼
Skip Indexing
```

---

## Retrieval Pipeline

```text
User Question
      │
      ▼
Dense Retriever
      │
      ├─────────────┐
      ▼             │
BM25 Retriever      │
      │             │
      └──────┬──────┘
             ▼
   Reciprocal Rank Fusion
             │
             ▼
 Retrieved Documentation
             │
             ▼
 Prompt Template
             │
             ▼
 OpenAI Chat Model
             │
             ▼
 Generated Answer
```

---

# Project Structure

```text
developer-docs-rag/
│
├── app/
├── ingestion/
├── retrieval/
├── prompts/
├── utils/
├── tests/
├── data/
│   ├── chromadb/
│   ├── index_metadata.json
│   └── raw/
│
├── requirements.txt
├── README.md
├── main.py
└── .env
```

---

# Design Principles

The project follows several design principles that make future versions easier to build.

* Modular ingestion pipeline
* Separation of indexing and retrieval
* Persistent vector database
* Incremental document synchronization
* Version-by-version evolution
* Production-inspired architecture over notebook prototypes

---

# Tech Stack

* Python 3.12
* LangChain
* ChromaDB
* OpenAI
* GitPython
* python-frontmatter
* rank-bm25

---

# Example

<img width="1437" height="902" alt="image" src="https://github.com/user-attachments/assets/025413ac-60b9-41c6-8599-b143258fb7dd" />

<img width="1442" height="472" alt="image" src="https://github.com/user-attachments/assets/90dcacca-4004-40d7-9c91-3f8784cce71e" />

<img width="1452" height="772" alt="image" src="https://github.com/user-attachments/assets/56f2dc45-708e-44f9-bd5c-2befd6f0159f" />



---

# Improvements Introduced in Version 2

Compared to Version 1, the indexing pipeline now:

* Avoids reparsing unchanged documentation
* Avoids re-embedding unchanged documents
* Detects added, modified and deleted documentation
* Removes obsolete vectors before re-indexing
* Updates only affected documents
* Skips indexing completely when the documentation repository has not changed

These improvements significantly reduce startup work while preserving the same retrieval behaviour.

---

# Improvements Introduced in Version 3

Compared to Version 2, the retrieval pipeline now:

* Combines dense semantic retrieval with BM25 lexical retrieval
* Uses Reciprocal Rank Fusion (RRF) to merge retrieval results
* Improves retrieval of exact API names and developer terminology
* Introduces a modular retrieval architecture for future retrieval strategies
* Encourages synthesis across multiple retrieved documentation chunks while remaining grounded in the retrieved context

These improvements increase retrieval robustness while maintaining the existing indexing pipeline introduced in Version 2.

---

# Project Roadmap

## ✅ Version 1 — Dense RAG

* GitHub ingestion
* Markdown parsing
* Metadata extraction
* Recursive chunking
* Dense retrieval
* Persistent Chroma vector database
* LCEL RAG pipeline
* Interactive CLI

---

## ✅ Version 2 — Incremental Indexing

* Sparse repository synchronization
* SHA-256 document change detection
* Metadata index
* Selective document loading
* Selective vector deletion
* Incremental embedding updates
* Skip indexing when documentation is unchanged

---

## ✅ Version 3 — Hybrid Retrieval

* BM25
* Dense retrieval
* Reciprocal Rank Fusion (RRF)

---

## ⬜ Version 4 — Cross-Encoder Reranking

Improve retrieval quality by reranking retrieved documents before generation.

---

## ⬜ Version 5 — Documentation + API Knowledge Base

Expand the knowledge base by combining official documentation with the LangGraph API source code.

* Official documentation
* API source code
* Rich metadata
* Multi-corpus retrieval

---

## ⬜ Version 6 — Parent Document Retrieval

Retrieve larger parent documents while searching over smaller chunks to provide richer context.

---

## ⬜ Version 7 — Evaluation Framework

Evaluate retrieval and generation quality using:

* Recall@K
* MRR
* RAGAS
* Faithfulness
* Latency
* Cost analysis

---

## ⬜ Version 8 — Agentic RAG (LangGraph)

Introduce intelligent retrieval strategies including:

* Query rewriting
* Multi-hop retrieval
* Retrieval planning
* Tool calling
* Reflection

---

# Installation

```bash
git clone <repository-url>
cd developer-docs-rag
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

**Windows**

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file.

```env
OPENAI_API_KEY=your_api_key
```

Run the application.

```bash
python main.py
```

---

# Future Improvements

Possible extensions beyond the current roadmap include:

* Support multiple documentation repositories
* Background indexing
* Automatic documentation versioning
* Docker deployment
* CI/CD pipeline
* Web interface
* Streaming responses
* Conversation memory
