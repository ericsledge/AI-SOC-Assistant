"""
Automated tests for Week 12 embedding generation.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from backend.document_loader import DocumentLoader  # noqa: E402
from backend.embedding_generator import (  # noqa: E402
    EmbeddingGenerator,
)
from backend.rag_models import DocumentChunk  # noqa: E402
from backend.text_chunker import TextChunker  # noqa: E402


DOCUMENT_DIRECTORY = PROJECT_ROOT / "knowledge_base" / "documents"
MODEL_CACHE_DIRECTORY = PROJECT_ROOT / "knowledge_base" / "models"


@pytest.fixture(scope="module")
def generator() -> EmbeddingGenerator:
    """Create one embedding generator for all tests."""
    return EmbeddingGenerator(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        device="cpu",
        batch_size=8,
        cache_folder=MODEL_CACHE_DIRECTORY,
    )


def make_chunk(
    chunk_number: int,
    text: str,
) -> DocumentChunk:
    """Create a small DocumentChunk for isolated testing."""
    return DocumentChunk(
        chunk_id=f"test_{chunk_number}",
        text=text,
        source_name="test_document.pdf",
        source_path="test_document.pdf",
        category="test",
        file_type="pdf",
        page_number=1,
        chunk_number=chunk_number,
    )


def test_generator_configuration() -> None:
    """Confirm constructor values are stored."""
    generator = EmbeddingGenerator(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        device="cpu",
        batch_size=4,
    )

    assert generator.model_name == (
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    assert generator.device == "cpu"
    assert generator.batch_size == 4


def test_invalid_model_name() -> None:
    """Reject an empty model name."""
    with pytest.raises(ValueError):
        EmbeddingGenerator(model_name="")


def test_invalid_batch_size() -> None:
    """Reject zero or negative batch sizes."""
    with pytest.raises(ValueError):
        EmbeddingGenerator(batch_size=0)

    with pytest.raises(ValueError):
        EmbeddingGenerator(batch_size=-1)


def test_model_loads(
    generator: EmbeddingGenerator,
) -> None:
    """Confirm the model loads and exposes a valid dimension."""
    assert generator.model is not None
    assert generator.embedding_dimension > 0


def test_encode_one_text(
    generator: EmbeddingGenerator,
) -> None:
    """One text should produce one embedding."""
    embeddings = generator.encode_texts(
        ["credential theft investigation"]
    )

    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape == (
        1,
        generator.embedding_dimension,
    )
    assert embeddings.dtype == np.float32


def test_encode_multiple_texts(
    generator: EmbeddingGenerator,
) -> None:
    """Multiple texts should produce matching embedding rows."""
    texts = [
        "phishing email investigation",
        "malware containment procedure",
        "network intrusion detection",
    ]

    embeddings = generator.encode_texts(texts)

    assert embeddings.shape == (
        len(texts),
        generator.embedding_dimension,
    )

    assert embeddings.flags["C_CONTIGUOUS"]


def test_embeddings_are_normalized(
    generator: EmbeddingGenerator,
) -> None:
    """Normalized embeddings should have norms close to one."""
    embeddings = generator.encode_texts(
        [
            "incident response",
            "threat intelligence",
            "security operations center",
        ]
    )

    norms = np.linalg.norm(
        embeddings,
        axis=1,
    )

    assert np.allclose(
        norms,
        np.ones_like(norms),
        atol=1e-5,
    )


def test_encode_empty_collection(
    generator: EmbeddingGenerator,
) -> None:
    """An empty input should return an empty embedding matrix."""
    embeddings = generator.encode_texts([])

    assert embeddings.shape == (
        0,
        generator.embedding_dimension,
    )

    assert embeddings.dtype == np.float32


def test_reject_empty_text(
    generator: EmbeddingGenerator,
) -> None:
    """Whitespace-only text should be rejected."""
    with pytest.raises(ValueError):
        generator.encode_texts(["   "])


def test_reject_non_string_text(
    generator: EmbeddingGenerator,
) -> None:
    """Non-string text values should be rejected."""
    with pytest.raises(TypeError):
        generator.encode_texts(
            ["valid text", 123]  # type: ignore[list-item]
        )


def test_encode_chunks(
    generator: EmbeddingGenerator,
) -> None:
    """DocumentChunk objects should produce matching embeddings."""
    chunks = [
        make_chunk(
            1,
            "Analyze a suspicious PowerShell process.",
        ),
        make_chunk(
            2,
            "Investigate repeated failed login attempts.",
        ),
    ]

    embeddings = generator.encode_chunks(
        chunks,
        show_progress_bar=False,
    )

    assert embeddings.shape == (
        len(chunks),
        generator.embedding_dimension,
    )


def test_reject_invalid_chunk(
    generator: EmbeddingGenerator,
) -> None:
    """Objects that are not DocumentChunk instances are rejected."""
    with pytest.raises(TypeError):
        generator.encode_chunks(
            ["not a chunk"],  # type: ignore[list-item]
            show_progress_bar=False,
        )


def test_encode_query(
    generator: EmbeddingGenerator,
) -> None:
    """One query should produce one two-dimensional vector."""
    query_embedding = generator.encode_query(
        "How should an analyst investigate phishing?"
    )

    assert query_embedding.shape == (
        1,
        generator.embedding_dimension,
    )


def test_reject_empty_query(
    generator: EmbeddingGenerator,
) -> None:
    """An empty query should be rejected."""
    with pytest.raises(ValueError):
        generator.encode_query("")


def test_real_knowledge_base_embeddings(
    generator: EmbeddingGenerator,
) -> None:
    """
    Load a small real-document sample and generate embeddings.

    Only the first ten chunks are embedded so the automated test stays
    reasonably fast on CPU.
    """
    loader = DocumentLoader(DOCUMENT_DIRECTORY)
    documents = loader.load_documents()

    successful_documents = [
        document
        for document in documents
        if document.get("loaded_successfully", False)
        and document.get("text", "").strip()
    ]

    assert successful_documents

    chunker = TextChunker(
        chunk_size=500,
        overlap=100,
    )

    chunks = chunker.chunk_documents(
        successful_documents
    )

    assert chunks

    sample_chunks = chunks[:10]

    embeddings = generator.encode_chunks(
        sample_chunks,
        show_progress_bar=False,
    )

    assert embeddings.shape == (
        len(sample_chunks),
        generator.embedding_dimension,
    )

    assert embeddings.dtype == np.float32