"""Integration checks for the live RAG retrieval pipeline."""

from __future__ import annotations

import pytest

from backend.rag_engine import load_rag_engine


@pytest.fixture(scope="module")
def rag_engine():
    """Load the RAG engine once for all integration tests."""
    return load_rag_engine()


@pytest.mark.parametrize(
    ("question", "expected_terms"),
    [
        (
            "What is phishing?",
            ["phishing"],
        ),
        (
            "How should an analyst investigate a suspicious email?",
            ["email", "phishing"],
        ),
        (
            "What is the NIST incident response lifecycle?",
            ["incident", "response"],
        ),
        (
            "What is MITRE ATT&CK used for?",
            ["mitre", "attack"],
        ),
    ],
)
def test_retrieval_returns_relevant_context(
    rag_engine,
    question: str,
    expected_terms: list[str],
) -> None:
    """Relevant questions should return usable knowledge-base context."""
    results = rag_engine.retrieve(question)

    assert results, f"No results returned for question: {question}"

    context = rag_engine.build_context(results).lower()

    assert "no relevant knowledge-base context" not in context
    assert "no usable knowledge-base context" not in context

    assert any(
        term.lower() in context
        for term in expected_terms
    ), (
        f"Expected one of {expected_terms} in retrieved context "
        f"for question: {question}"
    )