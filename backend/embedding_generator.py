"""
Embedding generation for the AI SOC Analyst Assistant.

This module converts document chunks and search queries into normalized
dense vectors using a Sentence Transformer model.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from backend.rag_models import DocumentChunk


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingGenerator:
    """Generate dense text embeddings for document chunks and queries."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        device: str = "cpu",
        batch_size: int = 16,
        cache_folder: str | Path | None = None,
    ) -> None:
        """
        Initialize the embedding generator.

        Args:
            model_name:
                Sentence Transformer model name or local model path.

            device:
                Inference device. Use "cpu" for the current project.

            batch_size:
                Number of texts processed together during encoding.

            cache_folder:
                Optional folder used to cache the downloaded model.
        """
        if not model_name.strip():
            raise ValueError("model_name cannot be empty.")

        if batch_size <= 0:
            raise ValueError("batch_size must be greater than zero.")

        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size

        if cache_folder is None:
            self.cache_folder = None
        else:
            self.cache_folder = str(Path(cache_folder))

        self._model: SentenceTransformer | None = None
        self._embedding_dimension: int | None = None

    @property
    def model(self) -> SentenceTransformer:
        """
        Load the embedding model only when it is first needed.

        Returns:
            Loaded SentenceTransformer model.
        """
        if self._model is None:
            print(f"Loading embedding model: {self.model_name}")
            print(f"Embedding device: {self.device}")

            self._model = SentenceTransformer(
                self.model_name,
                device=self.device,
                cache_folder=self.cache_folder,
            )

            dimension = self._model.get_embedding_dimension()

            if dimension is None:
                test_embedding = self._model.encode(
                    ["dimension test"],
                    convert_to_numpy=True,
                    show_progress_bar=False,
                )

                dimension = int(test_embedding.shape[1])

            self._embedding_dimension = int(dimension)

            print(
                "Embedding model loaded. "
                f"Dimension: {self._embedding_dimension}"
            )

        return self._model

    @property
    def embedding_dimension(self) -> int:
        """Return the number of values in each embedding vector."""
        if self._embedding_dimension is None:
            _ = self.model

        if self._embedding_dimension is None:
            raise RuntimeError(
                "Unable to determine the embedding dimension."
            )

        return self._embedding_dimension

    @staticmethod
    def _validate_texts(texts: Sequence[str]) -> list[str]:
        """
        Validate and normalize a collection of text values.

        Raises:
            TypeError:
                If an item is not a string.

            ValueError:
                If an item contains only whitespace.
        """
        validated_texts: list[str] = []

        for index, text in enumerate(texts):
            if not isinstance(text, str):
                raise TypeError(
                    f"Text at index {index} must be a string."
                )

            cleaned_text = text.strip()

            if not cleaned_text:
                raise ValueError(
                    f"Text at index {index} cannot be empty."
                )

            validated_texts.append(cleaned_text)

        return validated_texts

    def encode_texts(
        self,
        texts: Sequence[str],
        show_progress_bar: bool = False,
    ) -> np.ndarray:
        """
        Convert text strings into normalized float32 embeddings.

        Args:
            texts:
                Text values to encode.

            show_progress_bar:
                Whether Sentence Transformers should show progress.

        Returns:
            A NumPy array shaped:
                number_of_texts × embedding_dimension
        """
        if not texts:
            return np.empty(
                (0, self.embedding_dimension),
                dtype=np.float32,
            )

        validated_texts = self._validate_texts(texts)

        embeddings = self.model.encode(
            validated_texts,
            batch_size=self.batch_size,
            show_progress_bar=show_progress_bar,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32,
        )

        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        if embeddings.shape[0] != len(validated_texts):
            raise RuntimeError(
                "Embedding count does not match the text count."
            )

        if embeddings.shape[1] != self.embedding_dimension:
            raise RuntimeError(
                "Generated embedding dimension does not match the "
                "model embedding dimension."
            )

        return np.ascontiguousarray(embeddings)

    def encode_chunks(
        self,
        chunks: Sequence[DocumentChunk],
        show_progress_bar: bool = True,
    ) -> np.ndarray:
        """
        Convert document chunks into normalized float32 embeddings.

        Args:
            chunks:
                DocumentChunk objects created by TextChunker.

            show_progress_bar:
                Whether to display embedding progress.

        Returns:
            A NumPy embedding matrix.
        """
        if not chunks:
            return np.empty(
                (0, self.embedding_dimension),
                dtype=np.float32,
            )

        texts: list[str] = []

        for index, chunk in enumerate(chunks):
            if not isinstance(chunk, DocumentChunk):
                raise TypeError(
                    f"Item at index {index} is not a DocumentChunk."
                )

            texts.append(chunk.text)

        return self.encode_texts(
            texts,
            show_progress_bar=show_progress_bar,
        )

    def encode_query(self, query: str) -> np.ndarray:
        """
        Convert one search query into a normalized embedding.

        Returns:
            A two-dimensional NumPy array shaped:
                1 × embedding_dimension
        """
        if not isinstance(query, str):
            raise TypeError("query must be a string.")

        cleaned_query = query.strip()

        if not cleaned_query:
            raise ValueError("query cannot be empty.")

        return self.encode_texts(
            [cleaned_query],
            show_progress_bar=False,
        )