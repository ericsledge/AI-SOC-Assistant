"""
Text chunking utilities for the AI SOC Analyst Assistant.

This module converts documents loaded by DocumentLoader into overlapping
text chunks for embedding and semantic search.
"""

from __future__ import annotations

import hashlib
from typing import Any

from backend.rag_models import DocumentChunk


class TextChunker:
    """Split loaded knowledge-base documents into overlapping chunks."""

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 100,
    ) -> None:
        """
        Initialize the text chunker.

        Args:
            chunk_size:
                Maximum number of characters in a chunk.

            overlap:
                Number of characters repeated between neighboring chunks.
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")

        if overlap < 0:
            raise ValueError("overlap cannot be negative.")

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    @staticmethod
    def _get_value(
        document: Any,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Read a field from either a dictionary or a dataclass/object.

        Part 1's DocumentLoader returns dictionaries. This method also
        supports object-based document models for future compatibility.
        """
        if isinstance(document, dict):
            return document.get(key, default)

        return getattr(document, key, default)

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Remove unnecessary whitespace from chunk text."""
        if not text:
            return ""

        lines = [
            line.strip()
            for line in text.replace("\r\n", "\n").replace("\r", "\n").split(
                "\n"
            )
        ]

        return "\n".join(
            line for line in lines if line
        ).strip()

    @staticmethod
    def _create_chunk_id(
        source_name: str,
        page_number: int | None,
        chunk_number: int,
        text: str,
    ) -> str:
        """Create a stable, unique identifier for a document chunk."""
        identity = (
            f"{source_name}|{page_number}|{chunk_number}|{text}"
        )

        digest = hashlib.sha256(
            identity.encode("utf-8")
        ).hexdigest()[:16]

        return f"{source_name}_{chunk_number}_{digest}"

    def chunk_document(
        self,
        document: Any,
    ) -> list[DocumentChunk]:
        """
        Split one loaded document into overlapping chunks.

        Args:
            document:
                Document dictionary returned by DocumentLoader, or a
                compatible object containing document metadata.

        Returns:
            A list of DocumentChunk instances.
        """
        text = self._get_value(document, "text", "") or ""
        text = self._normalize_text(text)

        if not text:
            return []

        source_name = (
            self._get_value(document, "name")
            or self._get_value(document, "source_name")
            or "unknown_document"
        )

        source_path = (
            self._get_value(document, "path")
            or self._get_value(document, "source_path")
            or ""
        )

        relative_path = self._get_value(
            document,
            "relative_path",
            source_name,
        )

        category = self._get_value(document, "category")

        if not category:
            normalized_relative_path = str(relative_path).replace("\\", "/")
            path_parts = normalized_relative_path.split("/")

            if len(path_parts) > 1:
                category = path_parts[0]
            else:
                category = "general"

        file_type = self._get_value(document, "file_type", "pdf")
        page_number = self._get_value(document, "page_number")

        chunks: list[DocumentChunk] = []
        step_size = self.chunk_size - self.overlap
        start = 0
        chunk_number = 1

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk_id = self._create_chunk_id(
                    source_name=source_name,
                    page_number=page_number,
                    chunk_number=chunk_number,
                    text=chunk_text,
                )

                chunks.append(
                    DocumentChunk(
                        chunk_id=chunk_id,
                        text=chunk_text,
                        source_name=source_name,
                        source_path=str(source_path),
                        category=str(category),
                        file_type=str(file_type),
                        page_number=page_number,
                        chunk_number=chunk_number,
                    )
                )

                chunk_number += 1

            if end >= len(text):
                break

            start += step_size

        return chunks

    def chunk_documents(
        self,
        documents: list[Any],
    ) -> list[DocumentChunk]:
        """
        Split multiple documents into one combined list of chunks.
        """
        all_chunks: list[DocumentChunk] = []

        for document in documents:
            loaded_successfully = self._get_value(
                document,
                "loaded_successfully",
                True,
            )

            if not loaded_successfully:
                continue

            all_chunks.extend(
                self.chunk_document(document)
            )

        return all_chunks