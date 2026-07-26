from __future__ import annotations

import inspect
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

ENV_PATH = PROJECT_ROOT / ".env"

LOG_DIRECTORY = PROJECT_ROOT / "logs"
QUERY_LOG_PATH = LOG_DIRECTORY / "rag_queries.jsonl"

DEFAULT_INDEX_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "indexes"
    / "soc_knowledge.faiss"
)

DEFAULT_METADATA_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "indexes"
    / "soc_knowledge_metadata.json"
)


# Load environment variables before importing backend services.
load_dotenv(ENV_PATH)


from backend.rag_engine import load_rag_engine  # noqa: E402


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI SOC Analyst Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def format_duration(seconds: float) -> str:
    """Convert seconds into a readable display value."""
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"

    return f"{seconds:.2f} seconds"


def get_setting(name: str, default: str) -> str:
    """Read a string setting from the environment."""
    value = os.getenv(name)

    if value is None or not value.strip():
        return default

    return value.strip()


def get_integer_setting(name: str, default: int) -> int:
    """Read and validate an integer setting."""
    value = os.getenv(name)

    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        return default


def get_float_setting(name: str, default: float) -> float:
    """Read and validate a floating-point setting."""
    value = os.getenv(name)

    if value is None:
        return default

    try:
        return float(value)
    except ValueError:
        return default


@st.cache_resource(show_spinner="Loading the SOC knowledge base...")
def initialize_rag_engine() -> Any:
    """
    Load the RAG engine once and reuse it across Streamlit reruns.

    This compatibility loader supports several common load_rag_engine()
    signatures.
    """
    if not DEFAULT_INDEX_PATH.exists():
        raise FileNotFoundError(
            "The FAISS index was not found at: "
            f"{DEFAULT_INDEX_PATH}"
        )

    if not DEFAULT_METADATA_PATH.exists():
        raise FileNotFoundError(
            "The FAISS metadata file was not found at: "
            f"{DEFAULT_METADATA_PATH}"
        )

    signature = inspect.signature(load_rag_engine)
    parameter_names = list(signature.parameters)

    # Factory takes no explicit arguments.
    if not parameter_names:
        return load_rag_engine()

    keyword_arguments: dict[str, Any] = {}

    supported_values: dict[str, Any] = {
        "index_path": DEFAULT_INDEX_PATH,
        "faiss_index_path": DEFAULT_INDEX_PATH,
        "vector_index_path": DEFAULT_INDEX_PATH,
        "metadata_path": DEFAULT_METADATA_PATH,
        "index_metadata_path": DEFAULT_METADATA_PATH,
        "model_name": get_setting(
            "EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2",
        ),
        "embedding_model_name": get_setting(
            "EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2",
        ),
        "ollama_model": get_setting(
            "OLLAMA_MODEL",
            "llama3.2:3b",
        ),
        "base_url": get_setting(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        ),
        "ollama_base_url": get_setting(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        ),
        "top_k": get_integer_setting("RAG_TOP_K", 5),
        "minimum_score": get_float_setting(
            "RAG_MINIMUM_SCORE",
            0.30,
        ),
        "max_context_characters": get_integer_setting(
            "RAG_MAX_CONTEXT_CHARACTERS",
            6000,
        ),
    }

    for parameter_name in parameter_names:
        if parameter_name in supported_values:
            keyword_arguments[parameter_name] = supported_values[
                parameter_name
            ]

    # Use recognized keyword arguments whenever possible.
    if keyword_arguments:
        return load_rag_engine(**keyword_arguments)

    # Final fallback for a two-positional-argument factory.
    if len(parameter_names) == 2:
        return load_rag_engine(
            DEFAULT_INDEX_PATH,
            DEFAULT_METADATA_PATH,
        )

    raise TypeError(
        "The dashboard could not automatically determine how to call "
        "load_rag_engine(). Detected signature: "
        f"{signature}"
    )


def normalize_answer_result(result: Any) -> dict[str, Any]:
    """
    Convert different RAG result formats into one dashboard format.

    Supported result types:
    - dictionary
    - dataclass or object with attributes
    - plain string
    """
    normalized: dict[str, Any] = {
        "answer": "",
        "sources": [],
        "retrieved_chunks": [],
        "timings": {},
    }

    if isinstance(result, str):
        normalized["answer"] = result
        return normalized

    if isinstance(result, dict):
        normalized["answer"] = (
            result.get("answer")
            or result.get("response")
            or result.get("content")
            or ""
        )

        normalized["sources"] = (
            result.get("sources")
            or result.get("source_documents")
            or []
        )

        normalized["retrieved_chunks"] = (
            result.get("retrieved_chunks")
            or result.get("results")
            or result.get("context_chunks")
            or []
        )

        normalized["timings"] = (
            result.get("timings")
            or result.get("metrics")
            or {}
        )

        return normalized

    normalized["answer"] = (
        getattr(result, "answer", None)
        or getattr(result, "response", None)
        or getattr(result, "content", None)
        or str(result)
    )

    normalized["sources"] = (
        getattr(result, "sources", None)
        or getattr(result, "source_documents", None)
        or []
    )

    normalized["retrieved_chunks"] = (
        getattr(result, "retrieved_chunks", None)
        or getattr(result, "results", None)
        or []
    )

    normalized["timings"] = (
        getattr(result, "timings", None)
        or getattr(result, "metrics", None)
        or {}
    )

    return normalized


def extract_source_name(source: Any) -> str:
    """Extract a readable source name from a source object."""
    if isinstance(source, str):
        return source

    if isinstance(source, dict):
        return str(
            source.get("source")
            or source.get("source_file")
            or source.get("filename")
            or source.get("file_name")
            or source.get("document_name")
            or source.get("title")
            or "Unknown source"
        )

    return str(
        getattr(source, "source", None)
        or getattr(source, "source_file", None)
        or getattr(source, "filename", None)
        or getattr(source, "file_name", None)
        or getattr(source, "document_name", None)
        or "Unknown source"
    )


def extract_chunk_text(chunk: Any) -> str:
    """Extract readable text from a retrieved chunk."""
    if isinstance(chunk, str):
        return chunk

    if isinstance(chunk, dict):
        return str(
            chunk.get("text")
            or chunk.get("content")
            or chunk.get("chunk_text")
            or ""
        )

    return str(
        getattr(chunk, "text", None)
        or getattr(chunk, "content", None)
        or getattr(chunk, "chunk_text", None)
        or ""
    )


def extract_chunk_score(chunk: Any) -> float | None:
    """Extract a similarity score from a retrieved chunk."""
    if isinstance(chunk, dict):
        score = chunk.get("score")

        if score is None:
            score = chunk.get("similarity_score")

        if score is None:
            score = chunk.get("similarity")

    else:
        score = (
            getattr(chunk, "score", None)
            or getattr(chunk, "similarity_score", None)
            or getattr(chunk, "similarity", None)
        )

    if score is None:
        return None

    try:
        return float(score)
    except (TypeError, ValueError):
        return None


def run_rag_query(
    engine: Any,
    question: str,
    top_k: int,
    minimum_score: float,
) -> dict[str, Any]:
    """
    Call the RAG engine while supporting common answer() signatures.
    """
    answer_signature = inspect.signature(engine.answer)
    parameter_names = list(answer_signature.parameters)

    arguments: dict[str, Any] = {}

    if "question" in parameter_names:
        arguments["question"] = question
    elif "query" in parameter_names:
        arguments["query"] = question
    elif "user_question" in parameter_names:
        arguments["user_question"] = question

    if "top_k" in parameter_names:
        arguments["top_k"] = top_k

    if "minimum_score" in parameter_names:
        arguments["minimum_score"] = minimum_score
    elif "min_score" in parameter_names:
        arguments["min_score"] = minimum_score

    if arguments:
        result = engine.answer(**arguments)
    else:
        result = engine.answer(question)

    return normalize_answer_result(result)

def build_source_log_list(sources: list[Any]) -> list[str]:
    """Return a unique list of readable source names."""
    source_names: list[str] = []
    seen_sources: set[str] = set()

    for source in sources:
        source_name = extract_source_name(source)

        if source_name and source_name not in seen_sources:
            source_names.append(source_name)
            seen_sources.add(source_name)

    return source_names


def write_query_log(
    *,
    question: str,
    model: str,
    top_k: int,
    retrieved_chunks: int,
    sources: list[Any],
    answer_length: int,
    total_seconds: float,
    status: str,
    error: str | None = None,
) -> None:
    """Append one query record to the JSONL audit log."""
    try:
        LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

        log_record: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "question": question,
            "model": model,
            "top_k": top_k,
            "retrieved_chunks": retrieved_chunks,
            "sources": build_source_log_list(sources),
            "answer_length": answer_length,
            "total_seconds": round(total_seconds, 3),
            "status": status,
        }

        if error:
            log_record["error"] = error

        with QUERY_LOG_PATH.open(
            mode="a",
            encoding="utf-8",
        ) as log_file:
            log_file.write(
                json.dumps(
                    log_record,
                    ensure_ascii=False,
                )
                + "\n"
            )

    except (OSError, TypeError, ValueError) as logging_error:
        st.warning(
            "The query completed, but its log could not be written: "
            f"{logging_error}"
        )

def initialize_session_state() -> None:
    """Create session variables used by the interface."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "last_error" not in st.session_state:
        st.session_state.last_error = None


def clear_conversation() -> None:
    """Clear browser-session conversation history."""
    st.session_state.messages = []
    st.session_state.last_error = None


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

initialize_session_state()

st.title("🛡️ AI SOC Analyst Assistant")

st.markdown(
    """
Ask questions about cybersecurity operations, threats, detections,
incident response, phishing, malware, MITRE ATT&CK, and related SOC topics.

The assistant retrieves relevant information from the local knowledge base
before generating its response with Ollama.
"""
)

with st.sidebar:
    st.header("Configuration")

    ollama_model = get_setting(
        "OLLAMA_MODEL",
        "llama3.2:3b",
    )

    ollama_url = get_setting(
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    )

    default_top_k = get_integer_setting("RAG_TOP_K", 5)
    default_minimum_score = get_float_setting(
        "RAG_MINIMUM_SCORE",
        0.30,
    )

    st.text_input(
        "Ollama model",
        value=ollama_model,
        disabled=True,
    )

    st.text_input(
        "Ollama server",
        value=ollama_url,
        disabled=True,
    )

    top_k = st.slider(
        "Retrieved chunks",
        min_value=1,
        max_value=10,
        value=max(1, min(default_top_k, 10)),
        help="Number of knowledge-base chunks retrieved for each question.",
    )

    minimum_score = st.slider(
        "Minimum similarity score",
        min_value=0.0,
        max_value=1.0,
        value=max(0.0, min(default_minimum_score, 1.0)),
        step=0.05,
        help=(
            "Retrieved chunks below this similarity score are excluded."
        ),
    )

    show_retrieved_context = st.checkbox(
        "Show retrieved context",
        value=False,
    )

    st.divider()

    if st.button(
        "Clear conversation",
        use_container_width=True,
    ):
        clear_conversation()
        st.rerun()

    st.caption(
        "All model processing is performed through your local Ollama server."
    )


try:
    rag_engine = initialize_rag_engine()

except Exception as initialization_error:
    st.error("The RAG engine could not be initialized.")

    st.exception(initialization_error)

    st.markdown(
        """
Confirm that:

1. The FAISS index exists.
2. The metadata JSON file exists.
3. Your `.env` values are correct.
4. The embedding model can load.
5. Your backend modules import successfully.
"""
    )

    st.stop()


# Display previous messages.
for message in st.session_state.messages:
    role = message.get("role", "assistant")

    with st.chat_message(role):
        st.markdown(message.get("content", ""))

        metadata = message.get("metadata")

        if role == "assistant" and metadata:
            sources = metadata.get("sources", [])
            retrieved_chunks = metadata.get("retrieved_chunks", [])
            total_time = metadata.get("total_time")

            if total_time is not None:
                st.caption(
                    f"Total response time: "
                    f"{format_duration(total_time)}"
                )

            if sources:
                with st.expander(
                    f"Sources ({len(sources)})",
                    expanded=False,
                ):
                    displayed_sources: set[str] = set()

                    for source in sources:
                        source_name = extract_source_name(source)

                        if source_name not in displayed_sources:
                            st.markdown(f"- `{source_name}`")
                            displayed_sources.add(source_name)

            if show_retrieved_context and retrieved_chunks:
                with st.expander(
                    "Retrieved knowledge-base context",
                    expanded=False,
                ):
                    for chunk_number, chunk in enumerate(
                        retrieved_chunks,
                        start=1,
                    ):
                        chunk_text = extract_chunk_text(chunk)
                        chunk_score = extract_chunk_score(chunk)
                        source_name = extract_source_name(chunk)

                        st.markdown(
                            f"**Chunk {chunk_number} — "
                            f"{source_name}**"
                        )

                        if chunk_score is not None:
                            st.caption(
                                f"Similarity score: "
                                f"{chunk_score:.4f}"
                            )

                        st.write(chunk_text)

                        if chunk_number < len(retrieved_chunks):
                            st.divider()


question = st.chat_input(
    "Ask a cybersecurity question..."
)

if question:
    cleaned_question = question.strip()

    if not cleaned_question:
        st.warning("Enter a question before submitting.")

    else:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": cleaned_question,
            }
        )

        with st.chat_message("user"):
            st.markdown(cleaned_question)

        with st.chat_message("assistant"):
            with st.spinner(
                "Searching the knowledge base and generating an answer..."
            ):
                start_time = time.perf_counter()

                try:
                    normalized_result = run_rag_query(
                        engine=rag_engine,
                        question=cleaned_question,
                        top_k=top_k,
                        minimum_score=minimum_score,
                    )

                    total_time = time.perf_counter() - start_time

                    answer_text = normalized_result["answer"].strip()

                    if not answer_text:
                        answer_text = (
                            "The RAG engine completed, but it returned "
                            "an empty response."
                        )

                    sources = normalized_result["sources"]
                    retrieved_chunks = normalized_result[
                        "retrieved_chunks"
                    ]

                    write_query_log(
                         question=cleaned_question,
                         model=get_setting(
                            "OLLAMA_MODEL",
                            "llama3.2:3b",
                        ),
                        top_k=top_k,
                        retrieved_chunks=len(retrieved_chunks),
                        sources=sources,
                        answer_length=len(answer_text),
                        total_seconds=total_time,
                        status="success",
                    )

                    st.markdown(answer_text)

                    st.caption(
                        f"Total response time: "
                        f"{format_duration(total_time)}"
                    )

                    if sources:
                        with st.expander(
                            f"Sources ({len(sources)})",
                            expanded=True,
                        ):
                            displayed_sources: set[str] = set()

                            for source in sources:
                                source_name = extract_source_name(source)

                                if source_name not in displayed_sources:
                                    st.markdown(f"- `{source_name}`")
                                    displayed_sources.add(source_name)

                    if show_retrieved_context and retrieved_chunks:
                        with st.expander(
                            "Retrieved knowledge-base context",
                            expanded=False,
                        ):
                            for chunk_number, chunk in enumerate(
                                retrieved_chunks,
                                start=1,
                            ):
                                chunk_text = extract_chunk_text(chunk)
                                chunk_score = extract_chunk_score(chunk)
                                source_name = extract_source_name(chunk)

                                st.markdown(
                                    f"**Chunk {chunk_number} — "
                                    f"{source_name}**"
                                )

                                if chunk_score is not None:
                                    st.caption(
                                        f"Similarity score: "
                                        f"{chunk_score:.4f}"
                                    )

                                st.write(chunk_text)

                                if chunk_number < len(
                                    retrieved_chunks
                                ):
                                    st.divider()

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer_text,
                            "metadata": {
                                "sources": sources,
                                "retrieved_chunks": retrieved_chunks,
                                "total_time": total_time,
                            },
                        }
                    )

                    st.session_state.last_error = None

                except Exception as query_error:
                    total_time = time.perf_counter() - start_time

                    write_query_log(
                        question=cleaned_question,
                        model=get_setting(
                            "OLLAMA_MODEL",
                            "llama3.2:3b",
                        ),
                        top_k=top_k,
                        retrieved_chunks=0,
                        sources=[],
                        answer_length=0,
                        total_seconds=total_time,
                        status="error",
                        error=str(query_error),
                    )

                    error_message = (
                        "The assistant could not complete the request. "
                        "Check that Ollama is running and that the configured "
                        "model is installed."
                    )

                    st.error(error_message)
                    st.exception(query_error)

                    st.caption(
                        f"Failed after "
                        f"{format_duration(total_time)}"
                    )

                    st.session_state.last_error = str(query_error)