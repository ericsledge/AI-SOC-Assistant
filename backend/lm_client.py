"""Client for communicating with the local Ollama server."""

import os

from dotenv import load_dotenv
from openai import APIConnectionError, APIError, OpenAI

load_dotenv()


class LocalLLMClient:
    """Connect to Ollama through its OpenAI-compatible API."""

    def __init__(self) -> None:
        self.base_url = os.getenv(
            "LOCAL_LLM_BASE_URL",
            "http://localhost:11434/v1",
        )

        self.api_key = os.getenv(
            "LOCAL_LLM_API_KEY",
            "ollama",
        )

        self.model = os.getenv(
            "LOCAL_LLM_MODEL",
            "qwen2.5:1.5b",
        )

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=300.0,
        )

    def test_connection(self) -> bool:
        """Return True if Ollama is reachable and the model is installed."""

        try:
            models = self.client.models.list()
            installed_models = [model.id for model in models.data]

            if self.model not in installed_models:
                print(f"Model not installed: {self.model}")
                print(f"Run: ollama pull {self.model}")
                return False

            return True

        except APIConnectionError:
            print(
                "Could not connect to Ollama at "
                f"{self.base_url}"
            )
            return False

        except APIError as error:
            print(f"Ollama API error: {error}")
            return False

        except Exception as error:
            print(f"Unexpected error: {error}")
            return False

    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 700,
    ) -> str:
        """Send a request to Ollama and return the generated response."""

        if not user_prompt.strip():
            raise ValueError("The user prompt cannot be empty.")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content

            if not content:
                raise RuntimeError("Ollama returned an empty response.")

            return content.strip()

        except APIConnectionError as error:
            raise ConnectionError(
                "Python could not connect to Ollama."
            ) from error

        except APIError as error:
            raise RuntimeError(
                f"Ollama returned an API error: {error}"
            ) from error