"""Retrieval-augmented generation engine for the AI SOC Assistant."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv

from backend.embedding_generator import EmbeddingGenerator
from backend.ollama_client import OllamaClient
from backend.vector_store import FAISSVectorStore


DEFAULT_SYSTEM_PROMPT = """
You are an AI SOC Analyst Assistant.

Answer the user's cybersecurity question using only the supplied knowledge-base
context. Do not invent facts that are not supported by the context.

When appropriate:

1. Explain the issue clearly.
2. Describe indicators or evidence an analyst should inspect.
3. Recommend practical investigation or response actions.
4. State when the available context is insufficient.

Do not claim that an action was performed. You provide analysis and guidance
only.
""".strip()


@dataclass(slots=True)
class RAGEngine:
    """Retrieve relevant chunks and generate a grounded answer."""

    embedding_generator: EmbeddingGenerator
    vector_store: FAISSVectorStore
    ollama_client: OllamaClient
    top_k: int = 5
    minimum_score: float | None = 0.30
    max_context_characters: int = 6000
    system_prompt: str = DEFAULT_SYSTEM_PROMPT

    def __post_init__(self) -> None:
        if self.top_k <= 0:
            raise ValueError("top_k must be greater than zero")

        if self.max_context_characters <= 0:
            raise ValueError(
                "max_context_characters must be greater than zero"
            )

        if self.minimum_score is not None:
            if not -1.0 <= self.minimum_score <= 1.0:
                raise ValueError(
                    "minimum_score must be between -1.0 and 1.0"
                )

    def retrieve(self, question: str) -> list[dict[str, Any]]:
        """Embed a question and return the most relevant chunks."""
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question must be a non-empty string")

        query_embedding = self.embedding_generator.encode_query(
            question.strip()
        )

        results = self.vector_store.search(
            query_embedding,
            top_k=self.top_k,
            minimum_score=self.minimum_score,
        )

        return results

    def build_context(
        self,
        results: list[dict[str, Any]],
    ) -> str:
        """Format retrieved chunks into a bounded context block."""
        if not results:
            return "No relevant knowledge-base context was retrieved."

        sections: list[str] = []
        current_length = 0

        for rank, result in enumerate(results, start=1):
            chunk = result.get("chunk", {})
            score = result.get("score", 0.0)

            if chunk is None:
                continue

            text = str(getattr(chunk, "text", "")).strip()
            if not text:
                continue

            source = getattr(
                chunk,
                "source_name",
                "Unknown source",
            )

            chunk_id = getattr(
                chunk,
                "chunk_id",
                "Unknown chunk",
            )

            section = (
                f"[Source {rank}]\n"
                f"File: {source}\n"
                f"Chunk ID: {chunk_id}\n"
                f"Similarity score: {float(score):.4f}\n"
                f"Content:\n{text}\n"
            )

            if current_length + len(section) > self.max_context_characters:
                remaining = self.max_context_characters - current_length

                if remaining > 200:
                    sections.append(section[:remaining])

                break

            sections.append(section)
            current_length += len(section)

        if not sections:
            return "No usable knowledge-base context was retrieved."

        return "\n---\n".join(sections)

    def build_user_prompt(
        self,
        question: str,
        context: str,
    ) -> str:
        """Create the grounded prompt sent to Ollama."""
        return f"""
Use the following SOC knowledge-base context to answer the question.

KNOWLEDGE-BASE CONTEXT
======================
{context}

USER QUESTION
=============
{question.strip()}

RESPONSE REQUIREMENTS
=====================
- Base the answer on the provided context.
- Give a direct, technically accurate explanation.
- Include practical SOC investigation or response steps when relevant.
- Do not invent unsupported details.
- If the context is insufficient, say so clearly.
""".strip()

    def answer(self, question: str) -> dict[str, Any]:
        """Retrieve context, call Ollama, and return answer plus sources."""
        results = self.retrieve(question)
        context = self.build_context(results)
        user_prompt = self.build_user_prompt(question, context)

        

        answer_text = self.ollama_client.chat(
            user_prompt,
            system_message=self.system_prompt,
            temperature=0.2,
        )

        sources = []

        for rank, result in enumerate(results, start=1):
            chunk = result.get("chunk")

            if chunk is None:
                continue

            sources.append(
                {
                    "rank": rank,
                    "score": float(result.get("score", 0.0)),
                    "source": getattr(chunk, "source_name", "Unknown source"),
                    "chunk_id": getattr(chunk, "chunk_id", None),
                }
            )

        return {
            "question": question.strip(),
            "answer": answer_text,
            "sources": sources,
            "retrieved_results": results,
            "context": context,
        }


def load_rag_engine(
    *,
    index_path: str = "knowledge_base/indexes/soc_knowledge.faiss",
    metadata_path: str = (
        "knowledge_base/indexes/soc_knowledge_metadata.json"
    ),
) -> RAGEngine:
    """Load all components required by the RAG engine."""
    load_dotenv()

    embedding_generator = EmbeddingGenerator(
        model_name=os.getenv(
            "EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2",
        ),
        device="cpu",
    )

    vector_store = FAISSVectorStore.load(
        index_path=index_path,
        metadata_path=metadata_path,
    )

    ollama_client = OllamaClient(
        base_url=os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        ),
        model=os.getenv(
            "OLLAMA_MODEL",
            "llama3.2:3b",
        ),
        connect_timeout=10.0,
        read_timeout=600.0,
    )

    return RAGEngine(
        embedding_generator=embedding_generator,
        vector_store=vector_store,
        ollama_client=ollama_client,
        top_k=int(os.getenv("RAG_TOP_K", "3")),
        minimum_score=float(
            os.getenv("RAG_MINIMUM_SCORE", "0.30")
        ),
        max_context_characters=int(
            os.getenv("RAG_MAX_CONTEXT_CHARACTERS", "6000")
        ),
    )