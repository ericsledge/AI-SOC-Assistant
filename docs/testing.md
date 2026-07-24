# Testing Guide

## Automated Tests

Run:

python -m pytest -v

Expected Result:

All tests should pass successfully.

---

## Live RAG Test

Run:

python -m tests.run_week12_rag

Expected Result:

The application should retrieve relevant document chunks and generate a grounded response using Ollama.

---

## Manual Browser Testing

Launch:

streamlit run frontend\streamlit_app.py

Test Questions

1. What is phishing?

2. Explain the MITRE ATT&CK framework.

3. What are the phases of incident response?

4. What should a SOC analyst investigate after repeated failed Windows logins?

5. What immediate actions should be taken during a ransomware incident?

6. Who won the latest Super Bowl?

Expected Results

Cybersecurity questions should return accurate responses supported by relevant source documents.

The unrelated Super Bowl question should demonstrate that the assistant is limited by its knowledge base and should not confidently fabricate an answer.

---

## Success Criteria

- Streamlit launches successfully.
- RAG engine loads correctly.
- FAISS retrieves relevant documents.
- Ollama generates responses.
- Source documents are displayed.
- Response times are acceptable.

## Query Logging Validation

The Streamlit application records each completed query in the
`logs/rag_queries.jsonl` file.

Each record contains:

- UTC timestamp
- User question
- Ollama model
- Top-k retrieval setting
- Number of retrieved chunks
- Source documents
- Answer length
- Total response time
- Execution status
- Error information when applicable

The log was validated by submitting multiple questions through the
Streamlit interface and confirming that one valid JSON object was appended
per line.

The JSONL file was also parsed with Python to verify that every non-empty
line contained valid JSON.