# AI SOC Analyst Assistant Architecture

## Overview

The AI SOC Analyst Assistant is a Retrieval-Augmented Generation (RAG) application that helps answer cybersecurity questions using a locally stored knowledge base and a locally hosted large language model.

Rather than relying only on an LLM's general knowledge, the application retrieves relevant cybersecurity documents before generating an answer. This reduces hallucinations and grounds responses in trusted reference material.

---

## System Components

### Streamlit Interface

The Streamlit frontend provides the user interface.

Responsibilities include:

- Accepting user questions
- Displaying AI-generated answers
- Displaying source documents
- Showing retrieved document chunks
- Displaying response timing
- Managing conversation history

---

### RAG Engine

The Retrieval-Augmented Generation engine coordinates the entire question-answering pipeline.

Responsibilities include:

- Receiving user questions
- Creating question embeddings
- Searching the FAISS vector database
- Retrieving relevant document chunks
- Building the LLM prompt
- Sending the prompt to Ollama
- Returning the generated answer

---

### Embedding Generator

Sentence Transformers generate numerical vector embeddings for every document chunk.

Embedding Model:

sentence-transformers/all-MiniLM-L6-v2

Embedding Dimension:

384

These embeddings allow semantic similarity searches instead of keyword matching.

---

### FAISS Vector Store

Facebook AI Similarity Search (FAISS) stores vector embeddings for every document chunk.

During a user query:

1. The user's question is converted into an embedding.
2. FAISS finds the closest matching document vectors.
3. The most relevant document chunks are returned.

---

### Ollama Client

Ollama runs a local Large Language Model.

Model:

llama3.2:3b

The retrieved document context is included with the user's question before sending the prompt to Ollama.

The generated response is returned to the Streamlit application.

---

### Knowledge Base

The knowledge base contains cybersecurity reference documents used for retrieval.

Examples include:

- Phishing
- Malware
- Incident Response
- Windows Security
- MITRE ATT&CK
- SOC Procedures
- NIST Guidance

The knowledge base can be expanded by adding additional documents and rebuilding the vector index.

---

## User Query Flow

1. User submits a cybersecurity question.
2. Streamlit sends the question to the RAG engine.
3. The question is converted into an embedding.
4. FAISS retrieves the most relevant document chunks.
5. The retrieved context is combined with the user's question.
6. The prompt is sent to Ollama.
7. Ollama generates a grounded response.
8. Streamlit displays the answer and supporting sources.

---

## Architecture Summary

User

↓

Streamlit Frontend

↓

RAG Engine

↓

Sentence Transformer Embedding

↓

FAISS Vector Search

↓

Relevant Documents

↓

Ollama LLM

↓

Grounded Response

↓

Streamlit Display

## Query Audit Logging

The Streamlit frontend includes a lightweight JSON Lines logging mechanism.
After each query, the application appends a structured record to
`logs/rag_queries.jsonl`.

Successful records include retrieval and performance information. Failed
records include the error message and elapsed execution time.

JSON Lines was selected because each query can be appended independently
without loading or rewriting the entire log file.