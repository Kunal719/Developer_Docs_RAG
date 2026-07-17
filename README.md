# Developer Docs RAG

A Retrieval-Augmented Generation (RAG) project that answers developer questions using official documentation instead of relying solely on an LLM's internal knowledge.

This repository is designed as an **iterative learning project**, where each version introduces a new retrieval technique while preserving and improving the previous architecture. Rather than building multiple independent RAG projects, this repository evolves from a simple Dense RAG pipeline into a production-inspired developer documentation assistant.

---

# Project Overview

The knowledge source for this project is the official **LangGraph documentation** from the LangChain GitHub repository.

During indexing, the application:

- Clones (or updates) the documentation repository from GitHub.
- Parses Markdown/MDX documentation.
- Extracts useful metadata.
- Splits documents into semantic chunks.
- Generates embeddings using OpenAI.
- Stores embeddings in a persistent Chroma vector database.
- Retrieves relevant documentation to answer user questions.

The assistant only answers using the retrieved documentation and explicitly states when the documentation does not contain enough information.

---

# Version 1 - Dense RAG

The goal of Version 1 was **not** to build the most advanced RAG system.

Instead, the objective was to build every stage of a Dense RAG pipeline from scratch while keeping the architecture modular, maintainable, and easy to extend.

Version 1 implements:

- GitHub repository ingestion
- Markdown/MDX document parsing
- Metadata extraction
- Recursive document chunking
- OpenAI embeddings (`text-embedding-3-small`)
- Persistent Chroma vector database
- Dense semantic retrieval
- LCEL-based RAG pipeline
- Interactive command-line interface (CLI)

---

# Architecture

```text
                    GitHub Repository
                           │
                           ▼
                  Repository Loader
                           │
                           ▼
                 Markdown Parser (MDX)
                           │
                           ▼
                 Metadata Extraction
                           │
                           ▼
                     Document Chunking
                           │
                           ▼
                OpenAI Embedding Model
                           │
                           ▼
               Chroma Vector Database
                           │
                           ▼
                 Dense Retriever (Top-K)
                           │
                           ▼
              Prompt + OpenAI Chat Model
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
│
├── requirements.txt
├── README.md
└── .env
```

---

# Tech Stack

- Python 3.12
- LangChain
- ChromaDB
- OpenAI
- GitPython
- python-frontmatter

---

# Example

```text
You > How do I add a node?

Assistant > You can add a node to a graph using the `addNode` method. For better type safety, use the `GraphNode` type utility or `State.Node` to type your node functions. Here's an example in TypeScript:

```typescript
import { StateGraph, GraphNode } from "@langchain/langgraph";

const myNode: GraphNode<typeof State> = (state, config) => {
  // node implementation
  return { results: `Hello, ${state.input}!` };
};

const builder = new StateGraph(State)
  .addNode("myNode", myNode);
```

---

# Limitations Observed in Version 1

Building Version 1 helped establish a strong Dense RAG baseline while also exposing several retrieval limitations.

## 1. Full Reprocessing on Every Run

Every application startup currently:

- Loads the repository
- Parses every document
- Extracts metadata
- Recreates document chunks

Although embeddings are reused from the persistent Chroma database, the ingestion pipeline still performs unnecessary preprocessing for unchanged documentation.

---

## 2. Dense Retrieval Limitations

Semantic search performs well for procedural questions but occasionally struggles with:

- exact API names
- class definitions
- method lookups
- highly technical terminology

For example, queries about **StateGraph** may retrieve tutorial pages demonstrating its usage instead of the API documentation where it is introduced.

---

## 3. Chunk-Level Retrieval

Dense retrieval operates on individual chunks.

In some cases, retrieved chunks begin inside code examples while the explanatory paragraphs appear in neighbouring chunks, resulting in incomplete context being sent to the LLM.

---

# Why Version 2?

The next milestone focuses on **Incremental Indexing**.

Version 1 already avoids regenerating embeddings when a persistent Chroma collection exists.

However, it still reparses and rechunks every document during startup.

Version 2 will improve the indexing pipeline by:

- Detecting newly added documentation.
- Detecting modified documentation.
- Re-embedding only changed chunks.
- Reusing existing indexed documents.
- Maintaining stable document/chunk identifiers.
- Reducing startup time significantly.

This improves indexing efficiency without changing the retrieval architecture introduced in Version 1.

---

# Project Roadmap

## ✅ Version 1 — Dense RAG

- GitHub ingestion
- Metadata extraction
- Chunking
- Dense retrieval
- Persistent Chroma vector database
- LCEL RAG pipeline
- Interactive CLI

---

## 🚧 Version 2 — Incremental Indexing

- Detect new documents
- Detect modified documents
- Stable document IDs
- Update only changed embeddings
- Faster indexing

---

## ⬜ Version 3 — Hybrid Retrieval

- BM25
- Dense Retrieval
- Reciprocal Rank Fusion (RRF)

---

## ⬜ Version 4 — Cross-Encoder Reranking

Improve ranking quality by reranking retrieved documents before generation.

---

## ⬜ Version 5 — Parent Document Retrieval

Retrieve larger parent documents while searching over smaller chunks to provide richer context.

---

## ⬜ Version 6 — Agentic RAG (LangGraph)

Introduce intelligent retrieval strategies including:

- Query rewriting
- Multi-hop retrieval
- Tool calling
- Reflection
- Retrieval planning

---

## ⬜ Version 7 — Evaluation

Measure system quality using:

- Recall@K
- MRR
- RAGAS
- Latency
- Cost
- Faithfulness

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

Windows

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

Beyond the planned roadmap, possible future enhancements include:

- Multiple documentation repositories
- Web interface
- Streaming responses
- Conversation memory
- Configuration management
- Docker support
- CI/CD pipeline