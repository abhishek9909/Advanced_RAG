# Local Retrieval augmented generation

How to build and host a retrieval augmented generation system locally

# Features:

- Serve a completion model
- Upload documents, create an embedding index.
- Client to handle chat completions asynchronously.

# TechStack:

- Python to load and serve the model. (CTransformers)
- Python to load documents and build index. (tesseract, pdfminer, langchain, chromaDB)
- Python for API (flask, websocket)
- Javascript to build the UI. (react)

# Functions:

`app.py` has 2 endpoints:

## 1. POST: Upload file to be prepare a vector index.

Creates the required vector index, provided a chunking size limit.

## 2. POST: Generate completion.

Generates a completion response over the vector index provided:

- num_query_expansion
- num_retrieval_docs
- num_top_reranked_docs

`embedding.py` exposes:

- index_embeddings
- search_embedding_db

`completion.py` exposes:

- completion_db

## 3. GET : List of previous chats.

## 4. GET : List of available contexts.
