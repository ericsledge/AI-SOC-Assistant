"""
Manual verification script for Week 12 embedding generation.
"""

from __future__ import annotations

from pathlib import Path
from time import perf_counter

import numpy as np

from backend.document_loader import DocumentLoader
from backend.embedding_generator import EmbeddingGenerator
from backend.text_chunker import TextChunker


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCUMENT_DIRECTORY = PROJECT_ROOT / "knowledge_base" / "documents"
MODEL_CACHE_DIRECTORY = PROJECT_ROOT / "knowledge_base" / "models"


def main() -> None:
    """Load, chunk, and embed the knowledge-base documents."""
    print()
    print("WEEK 12 EMBEDDING GENERATOR")
    print("=" * 72)

    loader = DocumentLoader(DOCUMENT_DIRECTORY)
    documents = loader.load_documents()

    successful_documents = [
        document
        for document in documents
        if document.get("loaded_successfully", False)
        and document.get("text", "").strip()
    ]

    if not successful_documents:
        raise RuntimeError(
            "No successfully loaded documents contain extractable text."
        )

    chunker = TextChunker(
        chunk_size=500,
        overlap=100,
    )

    chunks = chunker.chunk_documents(
        successful_documents
    )

    if not chunks:
        raise RuntimeError(
            "No chunks were generated from the loaded documents."
        )

    print(f"Documents loaded: {len(successful_documents)}")
    print(f"Chunks generated: {len(chunks)}")

    generator = EmbeddingGenerator(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        device="cpu",
        batch_size=16,
        cache_folder=MODEL_CACHE_DIRECTORY,
    )

    start_time = perf_counter()

    embeddings = generator.encode_chunks(
        chunks,
        show_progress_bar=True,
    )

    elapsed_seconds = perf_counter() - start_time

    print()
    print("EMBEDDING SUMMARY")
    print("-" * 72)
    print(f"Model:               {generator.model_name}")
    print(f"Device:              {generator.device}")
    print(f"Embedding dimension: {generator.embedding_dimension}")
    print(f"Embedding count:     {embeddings.shape[0]}")
    print(f"Embedding shape:     {embeddings.shape}")
    print(f"NumPy data type:     {embeddings.dtype}")
    print(f"Contiguous array:    {embeddings.flags['C_CONTIGUOUS']}")
    print(f"Elapsed seconds:     {elapsed_seconds:.2f}")

    first_vector = embeddings[0]
    first_norm = float(np.linalg.norm(first_vector))

    print(f"First vector length: {len(first_vector)}")
    print(f"First vector norm:   {first_norm:.6f}")
    print(
        "First five values:  "
        f"{first_vector[:5].tolist()}"
    )

    if embeddings.shape[0] != len(chunks):
        raise RuntimeError(
            "The number of embeddings does not match the number of chunks."
        )

    if embeddings.shape[1] != generator.embedding_dimension:
        raise RuntimeError(
            "The embedding matrix has the wrong dimension."
        )

    if embeddings.dtype != np.float32:
        raise RuntimeError(
            "Embeddings must use the float32 data type."
        )

    print()
    print("Manual embedding verification passed.")


if __name__ == "__main__":
    main()