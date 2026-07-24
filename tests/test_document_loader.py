"""
Tests for the Week 12 PDF document loader.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from backend.document_loader import DocumentLoader  # noqa: E402


DOCUMENT_DIRECTORY = PROJECT_ROOT / "knowledge_base" / "documents"


@pytest.fixture
def loader() -> DocumentLoader:
    """Create a document loader for the project knowledge base."""
    return DocumentLoader(DOCUMENT_DIRECTORY)


def test_document_directory_exists() -> None:
    """Confirm the knowledge-base document directory exists."""
    assert DOCUMENT_DIRECTORY.exists(), (
        "The knowledge-base document directory does not exist: "
        f"{DOCUMENT_DIRECTORY}"
    )

    assert DOCUMENT_DIRECTORY.is_dir(), (
        "The knowledge-base document path is not a directory: "
        f"{DOCUMENT_DIRECTORY}"
    )


def test_pdf_files_are_available(
    loader: DocumentLoader,
) -> None:
    """Confirm at least one PDF is available for loading."""
    pdf_files = loader.get_pdf_files()

    assert pdf_files, (
        "No PDF files were found in "
        f"{DOCUMENT_DIRECTORY}. Add the Week 12 cybersecurity PDFs."
    )

    for pdf_file in pdf_files:
        assert pdf_file.exists()
        assert pdf_file.is_file()
        assert pdf_file.suffix.lower() == ".pdf"


def test_clean_text() -> None:
    """Confirm PDF text normalization works."""
    raw_text = (
        "Cybersecurity   framework\r\n"
        "\r\n"
        "\r\n"
        "Threat\tintelligence\x00"
    )

    cleaned = DocumentLoader.clean_text(raw_text)

    assert "\x00" not in cleaned
    assert "\r" not in cleaned
    assert "\t" not in cleaned
    assert "\n\n\n" not in cleaned
    assert "Cybersecurity framework" in cleaned
    assert "Threat intelligence" in cleaned


def test_load_documents(
    loader: DocumentLoader,
) -> None:
    """Load the complete knowledge base and validate its structure."""
    documents = loader.load_documents()

    assert documents, (
        "The loader returned no documents. Confirm that PDF files are "
        f"inside {DOCUMENT_DIRECTORY}."
    )

    successful_documents = [
        document
        for document in documents
        if document["loaded_successfully"]
    ]

    assert successful_documents, (
        "None of the PDF documents were loaded successfully."
    )

    text_documents = [
        document
        for document in successful_documents
        if document["text"].strip()
    ]

    assert text_documents, (
        "The PDFs loaded, but none produced extractable text. "
        "The files may contain scanned images instead of selectable text."
    )

    required_keys = {
        "name",
        "stem",
        "path",
        "relative_path",
        "file_type",
        "page_count",
        "character_count",
        "word_count",
        "text",
        "pages",
        "metadata",
        "warnings",
        "loaded_successfully",
        "error",
    }

    for document in documents:
        assert required_keys.issubset(document.keys())

        assert isinstance(document["name"], str)
        assert isinstance(document["path"], str)
        assert isinstance(document["page_count"], int)
        assert isinstance(document["character_count"], int)
        assert isinstance(document["word_count"], int)
        assert isinstance(document["text"], str)
        assert isinstance(document["pages"], list)
        assert isinstance(document["metadata"], dict)
        assert isinstance(document["warnings"], list)
        assert isinstance(document["loaded_successfully"], bool)

        if document["loaded_successfully"]:
            assert document["page_count"] > 0
            assert document["character_count"] == len(
                document["text"]
            )


def test_single_pdf(
    loader: DocumentLoader,
) -> None:
    """Validate loading one PDF directly."""
    pdf_files = loader.get_pdf_files()

    assert pdf_files, "No PDF files are available for this test."

    document = loader.read_pdf(pdf_files[0])

    assert document["name"] == pdf_files[0].name
    assert document["file_type"] == "pdf"
    assert isinstance(document["loaded_successfully"], bool)

    if document["loaded_successfully"]:
        assert document["page_count"] > 0
        assert isinstance(document["pages"], list)
        assert len(document["pages"]) == document["page_count"]
        assert document["error"] is None
    else:
        pytest.fail(
            f"Failed to load {document['name']}: "
            f"{document['error']}"
        )