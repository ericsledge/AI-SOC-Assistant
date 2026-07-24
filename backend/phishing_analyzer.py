"""Phishing email analysis logic."""

from __future__ import annotations

from backend.lm_client import LocalLLMClient


class PhishingAnalyzer:
    """Analyze email content for common phishing indicators."""

    SYSTEM_PROMPT = """
You are an AI assistant supporting an entry-level SOC analyst.

Your job is to examine email content for phishing indicators.

Analyze only the information provided. Do not invent sender details,
URLs, attachments, headers, or technical evidence.

Return the response using exactly these headings:

RISK LEVEL:
Choose one: LOW, MEDIUM, HIGH, or CRITICAL

SUMMARY:
Briefly explain the purpose of the email.

PHISHING INDICATORS:
List suspicious indicators. If none are found, write:
None identified.

LEGITIMATE INDICATORS:
List details that may indicate the email is legitimate. If none are
found, write:
None identified.

RECOMMENDED ACTIONS:
List clear actions the recipient or SOC analyst should take.

FINAL VERDICT:
Choose one: LIKELY SAFE, SUSPICIOUS, LIKELY PHISHING, or PHISHING
""".strip()

    def __init__(
        self,
        llm_client: LocalLLMClient | None = None,
    ) -> None:
        """Initialize the analyzer with an Ollama client."""

        self.llm_client = llm_client or LocalLLMClient()

    def analyze(self, email_text: str) -> str:
        """Analyze raw email text and return the assessment."""

        cleaned_email = email_text.strip()

        if not cleaned_email:
            raise ValueError("Email content cannot be empty.")

        user_prompt = f"""
Analyze the following email for phishing indicators.

EMAIL CONTENT
-------------
{cleaned_email}
-------------
""".strip()

        return self.llm_client.generate_response(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.0,
            max_tokens=700,
        )