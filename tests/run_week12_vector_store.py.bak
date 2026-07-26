"""
Manual end-to-end verification for the Week 12 FAISS vector store.
"""

from __future__ import annotations

from pathlib import Path
from time import perf_counter

from backend.document_loader import DocumentLoader
from backend.embedding_generator import EmbeddingGenerator
from backend.text_chunker import TextChunker
from backend.vector_store import FAISSVectorStore


PROJECT_ROOT = Path(__file__).resolve().parent.parent

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

INDEX_DIRECTORY = (
    PROJECT_ROOT
    / "knowledge_base"
    / "indexes"
)

INDEX_PATH = (
    INDEX_DIRECTORY
    / "soc_knowledge.faiss"
)

METADATA_PATH = (
    INDEX_DIRECTORY
    / "soc_knowledge_metadata.json"
)


def print_results(
    query: str,
    results: list[dict],
) -> None:
    """Display vector-search results."""
    print()
    print(f"QUERY: {query}")
    print("-" * 78)

    if not results:
        print("No matching chunks were returned.")
        return

    for result in results:
        preview = result["text"].replace(
            "\n",
            " ",
        )[:250]

        print(
            f"Rank: {result['rank']} | "
            f"Score: {result['score']:.4f}"
        )

        print(
            f"Source: {result['source_name']} | "
            f"Chunk: {result['chunk_number']} | "
            f"Page: {result['page_number']}"
        )

        print(f"Preview: {preview}")
        print()


def main() -> None:
    """Build, save, load, and search the FAISS knowledge base."""
    print()
    print("WEEK 12 FAISS VECTOR STORE")
    print("=" * 78)

    total_start = perf_counter()

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

    if not successful_documents:
        raise RuntimeError(
            "No successfully loaded documents contain text."
        )

    print(
        f"Documents loaded: "
        f"{len(successful_documents)}"
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
            "No chunks were generated."
        )

    print(f"Chunks generated: {len(chunks)}")

    embedding_generator = EmbeddingGenerator(
        model_name=(
            "sentence-transformers/"
            "all-MiniLM-L6-v2"
        ),
        device="cpu",
        batch_size=16,
        cache_folder=MODEL_CACHE_DIRECTORY,
    )

    embedding_start = perf_counter()

    embeddings = embedding_generator.encode_chunks(
        chunks,
        show_progress_bar=True,
    )

    embedding_seconds = (
        perf_counter()
        - embedding_start
    )

    print(
        f"Embeddings generated: "
        f"{embeddings.shape}"
    )

    print(
        f"Embedding time: "
        f"{embedding_seconds:.2f} seconds"
    )

    store = FAISSVectorStore(
        embedding_dimension=(
            embedding_generator.embedding_dimension
        )
    )

    store.build(
        chunks=chunks,
        embeddings=embeddings,
    )

    print(
        f"Vectors indexed: "
        f"{store.vector_count}"
    )

    store.save(
        index_path=INDEX_PATH,
        metadata_path=METADATA_PATH,
    )

    print(f"Index saved: {INDEX_PATH}")
    print(f"Metadata saved: {METADATA_PATH}")

    loaded_store = FAISSVectorStore.load(
        index_path=INDEX_PATH,
        metadata_path=METADATA_PATH,
    )

    print(
        f"Reloaded vectors: "
        f"{loaded_store.vector_count}"
    )

    queries = [
        (
            "How should a security analyst investigate "
            "a phishing email?"
        ),
        (
            "What steps should be taken during malware "
            "incident response?"
        ),
        (
            "How can an organization reduce unauthorized "
            "access to accounts?"
        ),
    ]

    for query in queries:
        query_embedding = (
            embedding_generator.encode_query(
                query
            )
        )

        results = loaded_store.search(
            query_embedding=query_embedding,
            top_k=5,
        )

        print_results(
            query=query,
            results=results,
        )

    total_seconds = (
        perf_counter()
        - total_start
    )

    print("=" * 78)
    print("VECTOR STORE SUMMARY")
    print("-" * 78)
    print(
        f"Documents:           "
        f"{len(successful_documents)}"
    )
    print(
        f"Chunks:              "
        f"{len(chunks)}"
    )
    print(
        f"Vectors:             "
        f"{loaded_store.vector_count}"
    )
    print(
        f"Embedding dimension: "
        f"{loaded_store.embedding_dimension}"
    )
    print(
        f"Index file exists:   "
        f"{INDEX_PATH.exists()}"
    )
    print(
        f"Metadata exists:     "
        f"{METADATA_PATH.exists()}"
    )
    print(
        f"Total seconds:       "
        f"{total_seconds:.2f}"
    )
    print()
    print(
        "Manual FAISS vector-store verification passed."
    )


if __name__ == "__main__":
    main()