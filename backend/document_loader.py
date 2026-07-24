"""
PDF document loader for the AI SOC Analyst Assistant.

This module discovers PDF files inside the knowledge-base document
directory and extracts their text using pypdf.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader
from pypdf.errors import PdfReadError


LOGGER = logging.getLogger(__name__)


class DocumentLoader:
    """Load PDF documents from a local knowledge-base directory."""

    def __init__(self, documents_directory: str | Path) -> None:
        """
        Initialize the document loader.

        Args:
            documents_directory:
                Directory containing the PDF knowledge-base documents.
        """
        self.documents_directory = Path(documents_directory)

    def validate_directory(self) -> None:
        """
        Verify that the configured document directory exists.

        Raises:
            FileNotFoundError:
                If the configured directory does not exist.

            NotADirectoryError:
                If the configured path exists but is not a directory.
        """
        if not self.documents_directory.exists():
            raise FileNotFoundError(
                "Knowledge-base document directory does not exist: "
                f"{self.documents_directory.resolve()}"
            )

        if not self.documents_directory.is_dir():
            raise NotADirectoryError(
                "Knowledge-base document path is not a directory: "
                f"{self.documents_directory.resolve()}"
            )

    def get_pdf_files(self) -> list[Path]:
        """
        Return all PDF files found in the configured directory.

        The search includes PDFs inside nested subdirectories.

        Returns:
            A sorted list of PDF file paths.
        """
        self.validate_directory()

        pdf_files = [
            path
            for path in self.documents_directory.rglob("*")
            if path.is_file() and path.suffix.lower() == ".pdf"
        ]

        return sorted(
            pdf_files,
            key=lambda path: str(path).lower(),
        )

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Normalize extracted PDF text.

        This removes null characters, reduces unnecessary spaces, and
        prevents excessive blank lines.

        Args:
            text:
                Raw text extracted from a PDF.

        Returns:
            Cleaned text.
        """
        if not text:
            return ""

        cleaned = text.replace("\x00", " ")
        cleaned = cleaned.replace("\r\n", "\n")
        cleaned = cleaned.replace("\r", "\n")

        # Replace repeated spaces and tabs with one space.
        cleaned = re.sub(r"[ \t]+", " ", cleaned)

        # Remove spaces immediately before line endings.
        cleaned = re.sub(r" +\n", "\n", cleaned)

        # Limit repeated blank lines.
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

        return cleaned.strip()

    def read_pdf(self, pdf_path: str | Path) -> dict[str, Any]:
        """
        Extract text and metadata from one PDF.

        Args:
            pdf_path:
                Path to the PDF file.

        Returns:
            Dictionary containing document text, page information,
            metadata, and extraction warnings.
        """
        path = Path(pdf_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file does not exist: {path.resolve()}"
            )

        if not path.is_file():
            raise ValueError(
                f"PDF path is not a file: {path.resolve()}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                f"Unsupported file type: {path.suffix or 'no extension'}"
            )

        page_texts: list[str] = []
        warnings: list[str] = []

        try:
            reader = PdfReader(str(path), strict=False)

            if reader.is_encrypted:
                try:
                    decrypt_result = reader.decrypt("")
                except Exception as error:
                    raise PdfReadError(
                        f"Unable to decrypt encrypted PDF: {path.name}"
                    ) from error

                if decrypt_result == 0:
                    raise PdfReadError(
                        f"Encrypted PDF requires a password: {path.name}"
                    )

            for page_number, page in enumerate(reader.pages, start=1):
                try:
                    extracted_text = page.extract_text() or ""
                    cleaned_page_text = self.clean_text(extracted_text)

                    if not cleaned_page_text:
                        warnings.append(
                            f"Page {page_number} produced no extractable text."
                        )

                    page_texts.append(cleaned_page_text)

                except Exception as error:
                    warning = (
                        f"Page {page_number} could not be extracted: {error}"
                    )
                    warnings.append(warning)
                    page_texts.append("")
                    LOGGER.warning("%s - %s", path.name, warning)

            document_text = "\n\n".join(
                text for text in page_texts if text
            )

            raw_metadata = reader.metadata or {}

            metadata = {
                "title": raw_metadata.get("/Title"),
                "author": raw_metadata.get("/Author"),
                "subject": raw_metadata.get("/Subject"),
                "creator": raw_metadata.get("/Creator"),
                "producer": raw_metadata.get("/Producer"),
                "creation_date": str(
                    raw_metadata.get("/CreationDate") or ""
                ),
                "modification_date": str(
                    raw_metadata.get("/ModDate") or ""
                ),
            }

            return {
                "name": path.name,
                "stem": path.stem,
                "path": str(path.resolve()),
                "relative_path": self._get_relative_path(path),
                "file_type": "pdf",
                "page_count": len(reader.pages),
                "character_count": len(document_text),
                "word_count": len(document_text.split()),
                "text": document_text,
                "pages": page_texts,
                "metadata": metadata,
                "warnings": warnings,
                "loaded_successfully": True,
                "error": None,
            }

        except Exception as error:
            LOGGER.exception("Failed to load PDF: %s", path)

            return {
                "name": path.name,
                "stem": path.stem,
                "path": str(path.resolve()),
                "relative_path": self._get_relative_path(path),
                "file_type": "pdf",
                "page_count": 0,
                "character_count": 0,
                "word_count": 0,
                "text": "",
                "pages": [],
                "metadata": {},
                "warnings": [],
                "loaded_successfully": False,
                "error": str(error),
            }

    def _get_relative_path(self, path: Path) -> str:
        """
        Return a path relative to the document directory when possible.
        """
        try:
            return str(
                path.resolve().relative_to(
                    self.documents_directory.resolve()
                )
            )
        except ValueError:
            return path.name

    def load_documents(self) -> list[dict[str, Any]]:
        """
        Load every PDF in the configured knowledge-base directory.

        Returns:
            A list of document dictionaries.
        """
        pdf_files = self.get_pdf_files()

        if not pdf_files:
            LOGGER.warning(
                "No PDF files were found in %s",
                self.documents_directory.resolve(),
            )
            return []

        documents: list[dict[str, Any]] = []

        for pdf_path in pdf_files:
            print(f"Loading: {pdf_path.name}")
            document = self.read_pdf(pdf_path)
            documents.append(document)

        return documents


def main() -> None:
    """
    Run the loader directly for a simple manual verification.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    project_root = Path(__file__).resolve().parent.parent
    document_directory = project_root / "knowledge_base" / "documents"

    loader = DocumentLoader(document_directory)
    documents = loader.load_documents()

    successful = [
        document
        for document in documents
        if document["loaded_successfully"]
    ]

    failed = [
        document
        for document in documents
        if not document["loaded_successfully"]
    ]

    total_characters = sum(
        document["character_count"]
        for document in successful
    )

    total_pages = sum(
        document["page_count"]
        for document in successful
    )

    print("\nDocument loader summary")
    print("-" * 60)
    print(f"PDF files discovered: {len(documents)}")
    print(f"Successfully loaded:   {len(successful)}")
    print(f"Failed:                {len(failed)}")
    print(f"Total pages:           {total_pages}")
    print(f"Total characters:      {total_characters:,}")

    if failed:
        print("\nFailed documents:")

        for document in failed:
            print(
                f"- {document['name']}: "
                f"{document['error']}"
            )


if __name__ == "__main__":
    main()