"""
Automated tests for the Week 12 text chunker.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from backend.document_loader import DocumentLoader  # noqa: E402
from backend.rag_models import DocumentChunk  # noqa: E402
from backend.text_chunker import TextChunker  # noqa: E402


DOCUMENT_DIRECTORY = PROJECT_ROOT / "knowledge_base" / "documents"


@pytest.fixture
def loader() -> DocumentLoader:
    """Create the project document loader."""
    return DocumentLoader(DOCUMENT_DIRECTORY)


@pytest.fixture
def chunker() -> TextChunker:
    """Create the standard Week 12 text chunker."""
    return TextChunker(
        chunk_size=500,
        overlap=100,
    )


def test_chunker_configuration() -> None:
    """Confirm valid chunker settings are stored."""
    chunker = TextChunker(
        chunk_size=500,
        overlap=100,
    )

    assert chunker.chunk_size == 500
    assert chunker.overlap == 100


def test_invalid_chunk_size() -> None:
    """Reject zero or negative chunk sizes."""
    with pytest.raises(ValueError):
        TextChunker(chunk_size=0, overlap=0)

    with pytest.raises(ValueError):
        TextChunker(chunk_size=-1, overlap=0)


def test_invalid_overlap() -> None:
    """Reject invalid overlap values."""
    with pytest.raises(ValueError):
        TextChunker(chunk_size=500, overlap=-1)

    with pytest.raises(ValueError):
        TextChunker(chunk_size=500, overlap=500)

    with pytest.raises(ValueError):
        TextChunker(chunk_size=500, overlap=600)


def test_empty_document_returns_no_chunks(
    chunker: TextChunker,
) -> None:
    """An empty document should not produce chunks."""
    document = {
        "name": "empty.pdf",
        "path": "empty.pdf",
        "relative_path": "empty.pdf",
        "file_type": "pdf",
        "text": "",
        "loaded_successfully": True,
    }

    chunks = chunker.chunk_document(document)

    assert chunks == []


def test_short_document_creates_one_chunk(
    chunker: TextChunker,
) -> None:
    """Text smaller than chunk_size should create one chunk."""
    document = {
        "name": "short.pdf",
        "path": "short.pdf",
        "relative_path": "short.pdf",
        "file_type": "pdf",
        "text": "Cybersecurity incident response.",
        "loaded_successfully": True,
    }

    chunks = chunker.chunk_document(document)

    assert len(chunks) == 1
    assert isinstance(chunks[0], DocumentChunk)
    assert chunks[0].chunk_number == 1
    assert chunks[0].source_name == "short.pdf"
    assert chunks[0].text == "Cybersecurity incident response."


def test_long_document_creates_multiple_chunks() -> None:
    """Long text should be divided into overlapping chunks."""
    chunker = TextChunker(
        chunk_size=100,
        overlap=20,
    )

    document = {
        "name": "long.pdf",
        "path": "long.pdf",
        "relative_path": "long.pdf",
        "file_type": "pdf",
        "text": "A" * 250,
        "loaded_successfully": True,
    }

    chunks = chunker.chunk_document(document)

    assert len(chunks) > 1

    for chunk in chunks:
        assert len(chunk.text) <= 100


def test_chunk_metadata_is_preserved(
    chunker: TextChunker,
) -> None:
    """Document metadata should be copied into every chunk."""
    document = {
        "name": "nist.pdf",
        "path": r"C:\documents\nist.pdf",
        "relative_path": r"NIST\nist.pdf",
        "file_type": "pdf",
        "text": "Incident response " * 100,
        "loaded_successfully": True,
    }

    chunks = chunker.chunk_document(document)

    assert chunks

    for index, chunk in enumerate(chunks, start=1):
        assert chunk.source_name == "nist.pdf"
        assert chunk.source_path == r"C:\documents\nist.pdf"
        assert chunk.category == "NIST"
        assert chunk.file_type == "pdf"
        assert chunk.chunk_number == index
        assert chunk.chunk_id


def test_load_and_chunk_real_documents(
    loader: DocumentLoader,
    chunker: TextChunker,
) -> None:
    """Load the real knowledge base and produce chunks."""
    documents = loader.load_documents()

    assert documents, (
        "No knowledge-base documents were loaded."
    )

    successful_documents = [
        document
        for document in documents
        if document["loaded_successfully"]
        and document["text"].strip()
    ]

    assert successful_documents, (
        "No successfully loaded documents contained extractable text."
    )

    chunks = chunker.chunk_documents(
        successful_documents
    )

    assert chunks, (
        "The real knowledge-base documents produced no chunks."
    )

    for chunk in chunks:
        assert isinstance(chunk, DocumentChunk)
        assert chunk.text.strip()
        assert len(chunk.text) <= chunker.chunk_size
        assert chunk.chunk_id
        assert chunk.source_name
        assert chunk.chunk_number > 0


def test_chunk_ids_are_unique(
    loader: DocumentLoader,
    chunker: TextChunker,
) -> None:
    """Every generated chunk should have a unique identifier."""
    documents = loader.load_documents()
    chunks = chunker.chunk_documents(documents)

    chunk_ids = [
        chunk.chunk_id
        for chunk in chunks
    ]

    assert len(chunk_ids) == len(set(chunk_ids))