"""Regression tests for the RAG engine."""

from __future__ import annotations

from unittest.mock import Mock

from backend.rag_models import DocumentChunk
from backend.rag_engine import RAGEngine


def build_test_engine() -> RAGEngine:
    """Create a RAG engine with mocked external dependencies."""
    embedding_generator = Mock()
    vector_store = Mock()
    ollama_client = Mock()

    ollama_client.chat.return_value = (
        "The supplied context describes phishing protections."
    )

    return RAGEngine(
        embedding_generator=embedding_generator,
        vector_store=vector_store,
        ollama_client=ollama_client,
        top_k=3,
        minimum_score=0.30,
        max_context_characters=6000,
    )


def test_build_context_accepts_document_chunk() -> None:
    """DocumentChunk results should be included in context."""
    engine = build_test_engine()

    chunk = DocumentChunk(
        chunk_id="test-document_0",
        text="Phishing emails may contain malicious links.",
        source_name="test-document.pdf",
        source_path="knowledge_base/test-document.pdf",
        category="Phishing",
        file_type="pdf",
        page_number=1,
        chunk_number=0,
    )

    results = [
        {
            "rank": 1,
            "score": 0.85,
            "vector_index": 0,
            "chunk": chunk,
        }
    ]

    context = engine.build_context(results)

    assert "test-document.pdf" in context
    assert "test-document_0" in context
    assert "Phishing emails may contain malicious links." in context
    assert "0.8500" in context


def test_build_context_handles_no_results() -> None:
    """Empty retrieval results should return a clear message."""
    engine = build_test_engine()

    context = engine.build_context([])

    assert context == (
        "No relevant knowledge-base context was retrieved."
    )


def test_answer_builds_sources_from_document_chunks() -> None:
    """Answer results should expose source metadata."""
    engine = build_test_engine()

    chunk = DocumentChunk(
        chunk_id="incident-response_2",
        text="Contain the affected endpoint.",
        source_name="incident-response.pdf",
        source_path="knowledge_base/incident-response.pdf",
        category="Incident_Response",
        file_type="pdf",
        page_number=2,
        chunk_number=2,
    )

    retrieval_results = [
        {
            "rank": 1,
            "score": 0.91,
            "vector_index": 2,
            "chunk": chunk,
        }
    ]

    engine.embedding_generator.encode_query.return_value = [0.1, 0.2, 0.3]

    engine.vector_store.search.return_value = retrieval_results

    result = engine.answer(
        "How should an affected endpoint be contained?"
    )

    assert len(result["sources"]) == 1
    assert result["sources"][0]["source"] == (
        "incident-response.pdf"
    )
    assert result["sources"][0]["chunk_id"] == (
        "incident-response_2"
    )
    assert result["sources"][0]["score"] == 0.91
    assert "incident-response.pdf" in result["context"]