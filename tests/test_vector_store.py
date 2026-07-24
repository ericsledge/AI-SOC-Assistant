"""
Automated tests for the Week 12 FAISS vector store.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from backend.document_loader import DocumentLoader  # noqa: E402
from backend.embedding_generator import (  # noqa: E402
    EmbeddingGenerator,
)
from backend.rag_models import DocumentChunk  # noqa: E402
from backend.text_chunker import TextChunker  # noqa: E402
from backend.vector_store import FAISSVectorStore  # noqa: E402


DOCUMENT_DIRECTORY = (
    PROJECT_ROOT
    / "knowledge_base"
    / "documents"
)

MODEL_CACHE_DIRECTORY = (
    PROJECT_ROOT
    / "knowledge_base"
    / "models"
)


def make_chunk(
    chunk_number: int,
    text: str,
) -> DocumentChunk:
    """Create a test DocumentChunk."""
    return DocumentChunk(
        chunk_id=f"chunk_{chunk_number}",
        text=text,
        source_name="test.pdf",
        source_path="test.pdf",
        category="test",
        file_type="pdf",
        page_number=1,
        chunk_number=chunk_number,
    )


def normalized_vectors() -> np.ndarray:
    """Create three simple normalized test vectors."""
    vectors = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=np.float32,
    )

    return vectors


def test_vector_store_configuration() -> None:
    """Confirm the vector-store dimension and initial state."""
    store = FAISSVectorStore(
        embedding_dimension=384
    )

    assert store.embedding_dimension == 384
    assert store.vector_count == 0
    assert len(store) == 0
    assert store.chunks == []


def test_invalid_embedding_dimension() -> None:
    """Reject invalid vector dimensions."""
    with pytest.raises(ValueError):
        FAISSVectorStore(
            embedding_dimension=0
        )

    with pytest.raises(ValueError):
        FAISSVectorStore(
            embedding_dimension=-1
        )


def test_add_vectors() -> None:
    """Add matching chunks and embeddings."""
    store = FAISSVectorStore(
        embedding_dimension=3
    )

    chunks = [
        make_chunk(1, "Phishing investigation"),
        make_chunk(2, "Malware analysis"),
        make_chunk(3, "Account security"),
    ]

    vectors = normalized_vectors()

    store.add(
        chunks=chunks,
        embeddings=vectors,
    )

    assert store.vector_count == 3
    assert len(store.chunks) == 3


def test_reject_embedding_dimension_mismatch() -> None:
    """Reject vectors with an incorrect dimension."""
    store = FAISSVectorStore(
        embedding_dimension=3
    )

    chunks = [
        make_chunk(1, "Phishing")
    ]

    incorrect_vectors = np.array(
        [[1.0, 0.0]],
        dtype=np.float32,
    )

    with pytest.raises(ValueError):
        store.add(
            chunks=chunks,
            embeddings=incorrect_vectors,
        )


def test_reject_count_mismatch() -> None:
    """Reject unequal chunk and embedding counts."""
    store = FAISSVectorStore(
        embedding_dimension=3
    )

    chunks = [
        make_chunk(1, "One chunk")
    ]

    vectors = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=np.float32,
    )

    with pytest.raises(ValueError):
        store.add(
            chunks=chunks,
            embeddings=vectors,
        )


def test_reject_invalid_chunk_type() -> None:
    """Reject objects that are not DocumentChunk instances."""
    store = FAISSVectorStore(
        embedding_dimension=3
    )

    vectors = np.array(
        [[1.0, 0.0, 0.0]],
        dtype=np.float32,
    )

    with pytest.raises(TypeError):
        store.add(
            chunks=["invalid"],  # type: ignore[list-item]
            embeddings=vectors,
        )


def test_reject_duplicate_chunk_ids() -> None:
    """Reject duplicate chunk identifiers."""
    store = FAISSVectorStore(
        embedding_dimension=3
    )

    chunks = [
        make_chunk(1, "First"),
        make_chunk(1, "Duplicate"),
    ]

    vectors = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=np.float32,
    )

    with pytest.raises(ValueError):
        store.add(
            chunks=chunks,
            embeddings=vectors,
        )


def test_exact_similarity_search() -> None:
    """The closest vector should rank first."""
    store = FAISSVectorStore(
        embedding_dimension=3
    )

    chunks = [
        make_chunk(1, "Phishing investigation"),
        make_chunk(2, "Malware response"),
        make_chunk(3, "Account protection"),
    ]

    store.build(
        chunks=chunks,
        embeddings=normalized_vectors(),
    )

    query = np.array(
        [[1.0, 0.0, 0.0]],
        dtype=np.float32,
    )

    results = store.search(
        query_embedding=query,
        top_k=3,
    )

    assert len(results) == 3
    assert results[0]["chunk_id"] == "chunk_1"
    assert results[0]["score"] == pytest.approx(1.0)
    assert results[0]["rank"] == 1


def test_search_accepts_one_dimensional_query() -> None:
    """A one-dimensional query should be reshaped."""
    store = FAISSVectorStore(
        embedding_dimension=3
    )

    chunks = [
        make_chunk(1, "Phishing"),
        make_chunk(2, "Malware"),
        make_chunk(3, "Identity"),
    ]

    store.build(
        chunks=chunks,
        embeddings=normalized_vectors(),
    )

    query = np.array(
        [0.0, 1.0, 0.0],
        dtype=np.float32,
    )

    results = store.search(
        query_embedding=query,
        top_k=1,
    )

    assert len(results) == 1
    assert results[0]["chunk_id"] == "chunk_2"


def test_search_empty_store() -> None:
    """Searching an empty store should return no results."""
    store = FAISSVectorStore(
        embedding_dimension=3
    )

    query = np.array(
        [[1.0, 0.0, 0.0]],
        dtype=np.float32,
    )

    results = store.search(
        query_embedding=query,
        top_k=5,
    )

    assert results == []


def test_invalid_top_k() -> None:
    """Reject non-positive result counts."""
    store = FAISSVectorStore(
        embedding_dimension=3
    )

    query = np.array(
        [[1.0, 0.0, 0.0]],
        dtype=np.float32,
    )

    with pytest.raises(ValueError):
        store.search(
            query_embedding=query,
            top_k=0,
        )


def test_minimum_score_filter() -> None:
    """Exclude results below a specified threshold."""
    store = FAISSVectorStore(
        embedding_dimension=3
    )

    chunks = [
        make_chunk(1, "First"),
        make_chunk(2, "Second"),
        make_chunk(3, "Third"),
    ]

    store.build(
        chunks=chunks,
        embeddings=normalized_vectors(),
    )

    query = np.array(
        [[1.0, 0.0, 0.0]],
        dtype=np.float32,
    )

    results = store.search(
        query_embedding=query,
        top_k=3,
        minimum_score=0.5,
    )

    assert len(results) == 1
    assert results[0]["chunk_id"] == "chunk_1"


def test_save_and_load(
    tmp_path: Path,
) -> None:
    """Save and restore an index and its metadata."""
    store = FAISSVectorStore(
        embedding_dimension=3
    )

    chunks = [
        make_chunk(1, "Phishing"),
        make_chunk(2, "Malware"),
        make_chunk(3, "Identity"),
    ]

    store.build(
        chunks=chunks,
        embeddings=normalized_vectors(),
    )

    index_path = tmp_path / "test.faiss"
    metadata_path = tmp_path / "test.json"

    store.save(
        index_path=index_path,
        metadata_path=metadata_path,
    )

    assert index_path.exists()
    assert metadata_path.exists()

    loaded_store = FAISSVectorStore.load(
        index_path=index_path,
        metadata_path=metadata_path,
    )

    assert loaded_store.embedding_dimension == 3
    assert loaded_store.vector_count == 3
    assert len(loaded_store.chunks) == 3
    assert loaded_store.chunks[0].text == "Phishing"

    query = np.array(
        [[0.0, 0.0, 1.0]],
        dtype=np.float32,
    )

    results = loaded_store.search(
        query_embedding=query,
        top_k=1,
    )

    assert results[0]["chunk_id"] == "chunk_3"


def test_reset_store() -> None:
    """Reset should remove all vectors and metadata."""
    store = FAISSVectorStore(
        embedding_dimension=3
    )

    chunks = [
        make_chunk(1, "One"),
        make_chunk(2, "Two"),
        make_chunk(3, "Three"),
    ]

    store.build(
        chunks=chunks,
        embeddings=normalized_vectors(),
    )

    assert store.vector_count == 3

    store.reset()

    assert store.vector_count == 0
    assert store.chunks == []


@pytest.fixture(scope="module")
def embedding_generator() -> EmbeddingGenerator:
    """Load one embedding model for integration testing."""
    return EmbeddingGenerator(
        model_name=(
            "sentence-transformers/"
            "all-MiniLM-L6-v2"
        ),
        device="cpu",
        batch_size=8,
        cache_folder=MODEL_CACHE_DIRECTORY,
    )


def test_real_semantic_search(
    embedding_generator: EmbeddingGenerator,
) -> None:
    """
    Test the vector store with a small real knowledge-base sample.
    """
    loader = DocumentLoader(
        DOCUMENT_DIRECTORY
    )

    documents = loader.load_documents()

    successful_documents = [
        document
        for document in documents
        if document.get(
            "loaded_successfully",
            False,
        )
        and document.get(
            "text",
            "",
        ).strip()
    ]

    assert successful_documents

    chunker = TextChunker(
        chunk_size=500,
        overlap=100,
    )

    all_chunks = chunker.chunk_documents(
        successful_documents
    )

    assert all_chunks

    sample_chunks = all_chunks[:20]

    embeddings = (
        embedding_generator.encode_chunks(
            sample_chunks,
            show_progress_bar=False,
        )
    )

    store = FAISSVectorStore(
        embedding_dimension=(
            embedding_generator.embedding_dimension
        )
    )

    store.build(
        chunks=sample_chunks,
        embeddings=embeddings,
    )

    query_embedding = (
        embedding_generator.encode_query(
            "cybersecurity risk and incident response"
        )
    )

    results = store.search(
        query_embedding=query_embedding,
        top_k=5,
    )

    assert results
    assert len(results) <= 5

    for result in results:
        assert result["chunk"].text
        assert result["source_name"]
        assert isinstance(
            result["score"],
            float,
        )