"""Manual end-to-end test for the Week 12 RAG pipeline."""

from __future__ import annotations

import time

from backend.rag_engine import load_rag_engine


def main() -> None:
    print("=" * 70)
    print("AI SOC ASSISTANT — WEEK 12 RAG TEST")
    print("=" * 70)

    print("\nLoading embedding model, FAISS index, and Ollama client...")
    engine = load_rag_engine()

    print(f"Loaded vectors: {engine.vector_store.vector_count}")
    print(f"Ollama model: {engine.ollama_client.model}")

    question = input(
        "\nEnter a cybersecurity question "
        "(or press Enter for the default question):\n> "
    ).strip()

    if not question:
        question = (
            "What indicators should a SOC analyst investigate "
            "during a suspected phishing incident?"
        )

    print("\nProcessing question...")
    start_time = time.perf_counter()

    result = engine.answer(question)

    print("\nRAW RESULT")
    print("=" * 70)
    print(result)

    elapsed = time.perf_counter() - start_time

    print("\n" + "=" * 70)
    print("ANSWER")
    print("=" * 70)
    print(result["answer"])

    print("\n" + "=" * 70)
    print("RETRIEVED SOURCES")
    print("=" * 70)

    if not result["sources"]:
        print("No sources met the retrieval threshold.")
    else:
        for source in result["sources"]:
            print(
                f"{source['rank']}. "
                f"{source['source']} | "
                f"chunk={source['chunk_id']} | "
                f"score={source['score']:.4f}"
            )

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Question: {result['question']}")
    print(f"Retrieved chunks: {len(result['sources'])}")
    print(f"Elapsed time: {elapsed:.2f} seconds")
    print("=" * 70)


if __name__ == "__main__":
    main()