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

# Evaluation Philosophy

Each architectural improvement in this project is evaluated before moving to the next iteration.

Rather than assuming a new retrieval strategy improves the system, every version is benchmarked independently using the project's evaluation framework. This approach makes it possible to understand not only whether a change helps, but also where it helps and where it introduces new trade-offs.

Detailed benchmark reports and experiment outputs are available in the `evaluation/` directory.

---

# Current Implementation

The project currently consists of five completed milestones.

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

## ✅ Version 4 — Cross-Encoder Reranking & Evaluation

Version 4 introduces a Cross-Encoder reranking stage to improve retrieval quality after Hybrid Retrieval.

Rather than assuming this architectural change improves the system, the project now includes a dedicated evaluation framework for benchmarking retrieval strategies across different versions.

Version 4 introduces:

* Cross-Encoder document reranking
* Modular evaluation framework
* Experiment metadata tracking
* Pipeline stage logging
* Structured JSON experiment outputs
* Benchmark question framework
* Manual evaluation workflow
* Benchmark reports and observations

---

## ✅ Version 5 — Multi-Corpus Retrieval

Version 5 expands the knowledge base beyond the official documentation by introducing multi-corpus retrieval.

Instead of searching only the LangGraph documentation, the retrieval pipeline now combines evidence from multiple sources before reranking and generation.

Version 5 introduces:

* Official LangGraph documentation corpus
* LangGraph API reference corpus
* LangGraph implementation source code corpus
* Unified multi-corpus retrieval
* Cross-corpus reranking
* Implementation-aware question answering
* Support for deep runtime and source-level reasoning

This enables the system to answer implementation-focused developer questions that cannot be answered reliably using documentation alone.

---

# Project Overview

The knowledge base for this project consists of two corpuses:

* Official LangGraph documentation
* Carefully selected LangGraph API Reference/implementation source code

The retrieval pipeline searches across all corpora, combines the retrieved candidates, reranks them using a Cross-Encoder, and generates answers grounded in both documentation and implementation details.

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
Multi-Corpus Retrieval
      │
 ┌────┼─────────────┐
 │    │             │
 ▼    ▼             ▼
Documentation   API Reference   Implementation
 │    │             │
 └────┴─────────────┘
        │
        ▼
Cross-Encoder Reranker
        │
        ▼
Top Retrieved Context
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

## Evaluation Pipeline

```text
Benchmark Question
        │
        ▼
Retrieval Pipeline
        │
        ▼
Generation
        │
        ▼
Capture Pipeline Stages
        │
        ▼
Capture Generation Metrics
        │
        ▼
Capture Overall Metrics
        │
        ▼
Experiment JSON
        │
        ▼
Evaluation using LLM with Human judgment
```

# Project Structure

```text
developer-docs-rag/
│
├── app/
├── ingestion/
├── retrieval/
├── reranking/
├── pipeline/
├── prompts/
├── evaluation/
│   └── results/
├── data/
│   ├── chromadb/
│   ├── bm25/
│   └── raw/
├── tests/
├── utils/
│
├── main.py
├── requirements.txt
├── README.md
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
* sentence-transformers
* FlagEmbedding / BAAI BGE Reranker

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

# Improvements Introduced in Version 4

Compared to Version 3, the retrieval pipeline now:

* Adds Cross-Encoder reranking after Hybrid Retrieval.
* Improves ranking of semantically relevant documentation chunks.
* Introduces a modular evaluation framework for benchmarking retrieval strategies.
* Captures experiment metadata and pipeline stage metrics.
* Produces structured experiment JSON for reproducible analysis.
* Enables systematic comparison between retrieval pipeline versions.

These improvements make retrieval evaluation a first-class component of the project rather than relying solely on qualitative inspection.

---

# Improvements Introduced in Version 5

Compared to Version 4, the retrieval pipeline now:

* Introduces multi-corpus retrieval.
* Indexes the LangGraph API reference.
* Indexes the LangGraph implementation source code.
* Retrieves evidence across documentation, API reference, and implementation.
* Improves implementation-level question answering.
* Enables source-code grounded explanations for internal runtime behaviour.

These improvements significantly expand the knowledge available to the retrieval pipeline while preserving the retrieval architecture introduced in Version 4.

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

## ✅ V4 Cross Encoder + Evaluation

Improve retrieval quality by reranking retrieved documents before generation.

---

## ✅ Version 5 — Multi-Corpus Retrieval

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

# Version 5 Evaluation

Version 5 was evaluated using approximately 60 challenging implementation-focused benchmark questions covering:

* Pregel runtime
* Scheduling
* StateGraph
* ToolNode
* Interrupts
* Checkpointing
* Store
* Subgraphs
* Command
* Send
* Runtime debugging

The evaluation showed that multi-corpus retrieval substantially improved implementation-level question answering. Remaining errors were primarily caused by LLM reasoning and code generation rather than retrieval quality.

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
