"""HTTP client for communicating with a local Ollama server."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from langchain_core import messages
import requests
from validators import url
from validators.url import url


class OllamaError(RuntimeError):
    """Base exception for Ollama client errors."""


class OllamaConnectionError(OllamaError):
    """Raised when the Ollama server cannot be reached."""


class OllamaModelError(OllamaError):
    """Raised when the requested model is unavailable."""


class OllamaResponseError(OllamaError):
    """Raised when Ollama returns an invalid or unsuccessful response."""


@dataclass(slots=True)
class OllamaClient:
    """Small HTTP client for the Ollama local API."""

    base_url: str = "http://localhost:11434"
    model: str = "llama3.2:3b"
    connect_timeout: float = 10.0
    read_timeout: float = 600.0

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")

        if not self.model.strip():
            raise ValueError("model cannot be empty")

        if self.connect_timeout <= 0:
            raise ValueError("connect_timeout must be greater than zero")

        if self.read_timeout <= 0:
            raise ValueError("read_timeout must be greater than zero")

    @property
    def timeout(self) -> tuple[float, float]:
        """Return the requests connect/read timeout tuple."""
        return self.connect_timeout, self.read_timeout

    def list_models(self) -> list[dict[str, Any]]:
        """Return models installed in the local Ollama instance."""
        url = f"{self.base_url}/api/tags"

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
        except requests.ConnectionError as exc:
            raise OllamaConnectionError(
                f"Could not connect to Ollama at {self.base_url}. "
                "Make sure Ollama is installed and running."
            ) from exc
        except requests.Timeout as exc:
            raise OllamaConnectionError(
                "Timed out while connecting to Ollama."
            ) from exc
        except requests.RequestException as exc:
            raise OllamaResponseError(
                f"Ollama model-list request failed: {exc}"
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise OllamaResponseError(
                "Ollama returned invalid JSON."
            ) from exc

        models = payload.get("models")

        if not isinstance(models, list):
            raise OllamaResponseError(
                "Ollama response did not contain a valid models list."
            )

        return models

    def is_available(self) -> bool:
        """Return True when the Ollama API can be reached."""
        try:
            self.list_models()
            return True
        except OllamaError:
            return False

    def model_is_installed(self, model: str | None = None) -> bool:
        """Return whether a model exists in Ollama."""
        requested_model = model or self.model

        installed_names = {
            item.get("name")
            for item in self.list_models()
            if isinstance(item, dict)
        }

        return requested_model in installed_names

    def chat(
        self,
        user_message: str,
        *,
        system_message: str | None = None,
        temperature: float = 0.2,
    ) -> str:
        """Send a non-streaming chat request to Ollama."""
        if not isinstance(user_message, str) or not user_message.strip():
            raise ValueError("user_message must be a non-empty string")

        if not 0.0 <= temperature <= 2.0:
            raise ValueError("temperature must be between 0.0 and 2.0")

        messages: list[dict[str, str]] = []

        if system_message:
            messages.append(
                {
                    "role": "system",
                    "content": system_message.strip(),
                }
            )

        messages.append(
            {
                "role": "user",
                "content": user_message.strip(),
            }
        )

        payload = {

            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": 300,
                "num_ctx": 4096,
            },
        }
        

        url = f"{self.base_url}/api/chat"

        

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout,
            )
        except requests.ConnectionError as exc:
            raise OllamaConnectionError(
                f"Could not connect to Ollama at {self.base_url}."
            ) from exc
        except requests.Timeout as exc:
            raise OllamaConnectionError(
                "Ollama did not respond before the timeout expired."
            ) from exc
        except requests.RequestException as exc:
            raise OllamaResponseError(
                f"Ollama chat request failed: {exc}"
            ) from exc

        if response.status_code == 404:
            raise OllamaModelError(
                f"Model '{self.model}' was not found. "
                f"Run: ollama pull {self.model}"
            )

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise OllamaResponseError(
                f"Ollama returned HTTP {response.status_code}: "
                f"{response.text[:500]}"
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise OllamaResponseError(
                "Ollama returned invalid JSON."
            ) from exc

        message = payload.get("message")

        if not isinstance(message, dict):
            raise OllamaResponseError(
                "Ollama response did not contain a message object."
            )

        content = message.get("content")

        if not isinstance(content, str) or not content.strip():
            raise OllamaResponseError(
                "Ollama returned an empty response."
            )

        return content.strip()