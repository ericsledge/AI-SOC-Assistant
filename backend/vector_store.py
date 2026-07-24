"""
FAISS vector storage for the AI SOC Analyst Assistant.

This module stores normalized document-chunk embeddings in a FAISS
inner-product index. It also saves and restores the index and its chunk
metadata.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Sequence

import faiss
import numpy as np

from backend.rag_models import DocumentChunk


class FAISSVectorStore:
    """Store and search document embeddings using FAISS."""

    SCHEMA_VERSION = 1

    def __init__(self, embedding_dimension: int) -> None:
        """
        Initialize an empty vector store.

        Args:
            embedding_dimension:
                Number of float values in every embedding vector.
        """
        if embedding_dimension <= 0:
            raise ValueError(
                "embedding_dimension must be greater than zero."
            )

        self.embedding_dimension = embedding_dimension

        # IndexFlatIP performs exact inner-product similarity search.
        # Because the project embeddings are normalized, the score acts
        # as cosine similarity.
        self.index = faiss.IndexFlatIP(embedding_dimension)

        self.chunks: list[DocumentChunk] = []

    @property
    def vector_count(self) -> int:
        """Return the number of embeddings currently in the index."""
        return int(self.index.ntotal)

    def __len__(self) -> int:
        """Return the number of indexed vectors."""
        return self.vector_count

    def _validate_embeddings(
        self,
        embeddings: np.ndarray,
        expected_count: int | None = None,
    ) -> np.ndarray:
        """
        Validate and normalize the structure of an embedding matrix.

        Returns:
            A contiguous float32 NumPy array suitable for FAISS.
        """
        if not isinstance(embeddings, np.ndarray):
            raise TypeError(
                "embeddings must be a NumPy array."
            )

        if embeddings.ndim != 2:
            raise ValueError(
                "embeddings must be a two-dimensional array."
            )

        if embeddings.shape[1] != self.embedding_dimension:
            raise ValueError(
                "Embedding dimension mismatch. "
                f"Expected {self.embedding_dimension}, "
                f"received {embeddings.shape[1]}."
            )

        if expected_count is not None:
            if embeddings.shape[0] != expected_count:
                raise ValueError(
                    "Embedding count does not match the chunk count. "
                    f"Embeddings: {embeddings.shape[0]}, "
                    f"chunks: {expected_count}."
                )

        if not np.all(np.isfinite(embeddings)):
            raise ValueError(
                "Embeddings contain NaN or infinite values."
            )

        converted = np.asarray(
            embeddings,
            dtype=np.float32,
        )

        return np.ascontiguousarray(converted)

    @staticmethod
    def _validate_chunks(
        chunks: Sequence[DocumentChunk],
    ) -> list[DocumentChunk]:
        """Validate a collection of DocumentChunk objects."""
        validated_chunks: list[DocumentChunk] = []

        for index, chunk in enumerate(chunks):
            if not isinstance(chunk, DocumentChunk):
                raise TypeError(
                    f"Item at index {index} is not a DocumentChunk."
                )

            if not chunk.chunk_id.strip():
                raise ValueError(
                    f"Chunk at index {index} has no chunk ID."
                )

            if not chunk.text.strip():
                raise ValueError(
                    f"Chunk at index {index} contains no text."
                )

            validated_chunks.append(chunk)

        return validated_chunks

    def reset(self) -> None:
        """Remove all vectors and metadata from the store."""
        self.index = faiss.IndexFlatIP(
            self.embedding_dimension
        )

        self.chunks = []

    def add(
        self,
        chunks: Sequence[DocumentChunk],
        embeddings: np.ndarray,
    ) -> None:
        """
        Add chunks and their embeddings to the vector store.

        The ordering of chunks must exactly match the row ordering of the
        embedding matrix.
        """
        if not chunks:
            if embeddings.shape[0] == 0:
                return

            raise ValueError(
                "Embeddings were provided without chunks."
            )

        validated_chunks = self._validate_chunks(chunks)

        validated_embeddings = self._validate_embeddings(
            embeddings,
            expected_count=len(validated_chunks),
        )

        existing_chunk_ids = {
            chunk.chunk_id
            for chunk in self.chunks
        }

        incoming_chunk_ids = [
            chunk.chunk_id
            for chunk in validated_chunks
        ]

        if len(incoming_chunk_ids) != len(
            set(incoming_chunk_ids)
        ):
            raise ValueError(
                "The incoming chunks contain duplicate chunk IDs."
            )

        duplicates = existing_chunk_ids.intersection(
            incoming_chunk_ids
        )

        if duplicates:
            duplicate_preview = ", ".join(
                sorted(duplicates)[:5]
            )

            raise ValueError(
                "One or more chunk IDs already exist in the store: "
                f"{duplicate_preview}"
            )

        self.index.add(validated_embeddings)
        self.chunks.extend(validated_chunks)

        self._validate_store_consistency()

    def build(
        self,
        chunks: Sequence[DocumentChunk],
        embeddings: np.ndarray,
    ) -> None:
        """
        Replace the current store with a new index.

        This resets the existing index before adding the supplied vectors.
        """
        self.reset()
        self.add(chunks, embeddings)

    def _validate_store_consistency(self) -> None:
        """
        Confirm that FAISS vectors and chunk metadata remain aligned.
        """
        if self.vector_count != len(self.chunks):
            raise RuntimeError(
                "Vector-store consistency error. "
                f"FAISS vectors: {self.vector_count}, "
                f"metadata records: {len(self.chunks)}."
            )

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        minimum_score: float | None = None,
    ) -> list[dict[str, Any]]:
        """
        Search for chunks similar to one query embedding.

        Args:
            query_embedding:
                Query vector shaped either `(dimension,)` or
                `(1, dimension)`.

            top_k:
                Maximum number of results to return.

            minimum_score:
                Optional similarity-score threshold.

        Returns:
            Ranked dictionaries containing the matching chunk and score.
        """
        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        if self.vector_count == 0:
            return []

        if not isinstance(query_embedding, np.ndarray):
            raise TypeError(
                "query_embedding must be a NumPy array."
            )

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        if query_embedding.ndim != 2:
            raise ValueError(
                "query_embedding must be one- or two-dimensional."
            )

        if query_embedding.shape[0] != 1:
            raise ValueError(
                "search accepts exactly one query embedding."
            )

        validated_query = self._validate_embeddings(
            query_embedding
        )

        result_count = min(
            top_k,
            self.vector_count,
        )

        scores, indices = self.index.search(
            validated_query,
            result_count,
        )

        results: list[dict[str, Any]] = []

        for rank, (score, vector_index) in enumerate(
            zip(scores[0], indices[0]),
            start=1,
        ):
            vector_index = int(vector_index)
            numeric_score = float(score)

            # FAISS can return -1 when no valid neighbor exists.
            if vector_index < 0:
                continue

            if minimum_score is not None:
                if numeric_score < minimum_score:
                    continue

            chunk = self.chunks[vector_index]

            results.append(
                {
                    "rank": rank,
                    "score": numeric_score,
                    "vector_index": vector_index,
                    "chunk": chunk,
                    "chunk_id": chunk.chunk_id,
                    "text": chunk.text,
                    "source_name": chunk.source_name,
                    "source_path": chunk.source_path,
                    "category": chunk.category,
                    "file_type": chunk.file_type,
                    "page_number": chunk.page_number,
                    "chunk_number": chunk.chunk_number,
                }
            )

        return results

    def save(
        self,
        index_path: str | Path,
        metadata_path: str | Path,
    ) -> None:
        """
        Save the FAISS index and chunk metadata to disk.

        FAISS vectors are stored in the index file. Chunk text and source
        information are stored in a separate JSON metadata file.
        """
        self._validate_store_consistency()

        if self.vector_count == 0:
            raise ValueError(
                "Cannot save an empty vector store."
            )

        resolved_index_path = Path(index_path)
        resolved_metadata_path = Path(metadata_path)

        resolved_index_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        resolved_metadata_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            str(resolved_index_path),
        )

        metadata = {
            "schema_version": self.SCHEMA_VERSION,
            "embedding_dimension": self.embedding_dimension,
            "index_type": type(self.index).__name__,
            "vector_count": self.vector_count,
            "chunks": [
                asdict(chunk)
                for chunk in self.chunks
            ],
        }

        with resolved_metadata_path.open(
            "w",
            encoding="utf-8",
        ) as metadata_file:
            json.dump(
                metadata,
                metadata_file,
                ensure_ascii=False,
                indent=2,
            )

    @classmethod
    def load(
        cls,
        index_path: str | Path,
        metadata_path: str | Path,
    ) -> "FAISSVectorStore":
        """
        Load a saved FAISS index and its chunk metadata.

        Returns:
            A fully restored FAISSVectorStore.
        """
        resolved_index_path = Path(index_path)
        resolved_metadata_path = Path(metadata_path)

        if not resolved_index_path.exists():
            raise FileNotFoundError(
                f"FAISS index file does not exist: "
                f"{resolved_index_path.resolve()}"
            )

        if not resolved_metadata_path.exists():
            raise FileNotFoundError(
                f"Metadata file does not exist: "
                f"{resolved_metadata_path.resolve()}"
            )

        loaded_index = faiss.read_index(
            str(resolved_index_path)
        )

        with resolved_metadata_path.open(
            "r",
            encoding="utf-8",
        ) as metadata_file:
            metadata = json.load(metadata_file)

        schema_version = metadata.get("schema_version")

        if schema_version != cls.SCHEMA_VERSION:
            raise ValueError(
                "Unsupported vector-store metadata schema. "
                f"Expected {cls.SCHEMA_VERSION}, "
                f"received {schema_version}."
            )

        embedding_dimension = int(
            metadata["embedding_dimension"]
        )

        if int(loaded_index.d) != embedding_dimension:
            raise ValueError(
                "The saved FAISS index dimension does not match "
                "the metadata dimension."
            )

        store = cls(
            embedding_dimension=embedding_dimension
        )

        store.index = loaded_index

        raw_chunks = metadata.get("chunks", [])

        store.chunks = [
            DocumentChunk(**chunk_data)
            for chunk_data in raw_chunks
        ]

        expected_vector_count = int(
            metadata.get("vector_count", -1)
        )

        if store.vector_count != expected_vector_count:
            raise ValueError(
                "The saved FAISS vector count does not match "
                "the metadata vector count."
            )

        store._validate_store_consistency()

        return store