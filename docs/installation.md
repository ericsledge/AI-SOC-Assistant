# Installation Guide

## Requirements

- Windows Server 2025
- Python 3.x
- Ollama
- Git (optional)
- Visual Studio Code

---

## Create a Virtual Environment

python -m venv venv

Activate:

venv\Scripts\activate

---

## Install Dependencies

pip install -r requirements.txt

---

## Install Ollama

Download and install Ollama.

Verify installation:

ollama --version

---

## Download the Model

ollama pull llama3.2:3b

Verify:

ollama list

---

## Build the Knowledge Base

Run the indexing script:

python backend\build_vector_store.py

This creates:

knowledge_base/indexes/

including the FAISS index and metadata.

---

## Launch the Application

streamlit run frontend\streamlit_app.py

Open:

http://localhost:8501

---

## Running Tests

python -m pytest -v

---

## Environment Variables

The application uses a .env file to configure:

- Ollama URL
- Embedding model
- Retrieval parameters
- Context length

## Logging Limitations

The current logging implementation stores query records in a local JSONL
file. It does not currently provide log rotation, encryption, centralized
collection, retention controls, or access-based permissions.

Because user questions are recorded, production deployments should define
appropriate privacy, retention, and sensitive-data handling policies.