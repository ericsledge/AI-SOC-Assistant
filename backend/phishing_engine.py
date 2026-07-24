"""Deterministic phishing indicator and risk scoring engine."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlparse

from backend.email_parser import parse_message
from backend.ioc_extractor import extract_iocs


@dataclass(frozen=True)
class Indicator:
    """One suspicious email indicator."""

    name: str
    description: str
    points: int
    evidence: str


@dataclass(frozen=True)
class AnalysisResult:
    """Complete deterministic phishing assessment."""

    score: int
    risk_level: str
    verdict: str
    indicators: list[Indicator]
    iocs: dict[str, list[str]]
    parsed_email: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert the result into a serializable dictionary."""

        result = asdict(self)
        return result


URGENCY_TERMS = {
    "urgent",
    "immediately",
    "within 24 hours",
    "within one hour",
    "act now",
    "final warning",
    "time sensitive",
    "expires today",
    "limited time",
    "failure to respond",
}

THREAT_TERMS = {
    "account suspended",
    "account disabled",
    "account locked",
    "account closed",
    "permanently deleted",
    "legal action",
    "unauthorized activity",
    "security alert",
    "unusual activity",
    "payment failed",
}

CREDENTIAL_TERMS = {
    "verify your password",
    "confirm your password",
    "enter your password",
    "username and password",
    "login credentials",
    "verify your account",
    "confirm your identity",
    "sign in to verify",
}

FINANCIAL_TERMS = {
    "wire transfer",
    "gift card",
    "bank account",
    "direct deposit",
    "payment details",
    "credit card",
    "invoice attached",
    "cryptocurrency",
    "bitcoin",
    "refund",
}

SUSPICIOUS_TLDS = {
    "zip",
    "click",
    "top",
    "xyz",
    "work",
    "support",
    "info",
    "live",
    "shop",
    "buzz",
    "tk",
    "ml",
    "ga",
    "cf",
    "gq",
}

URL_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "rebrand.ly",
    "cutt.ly",
    "shorturl.at",
}

SUSPICIOUS_ATTACHMENT_EXTENSIONS = {
    ".exe",
    ".scr",
    ".bat",
    ".cmd",
    ".com",
    ".js",
    ".jse",
    ".vbs",
    ".vbe",
    ".ps1",
    ".msi",
    ".hta",
    ".iso",
    ".img",
    ".lnk",
    ".jar",
}


class PhishingAnalysisEngine:
    """Analyze email content using transparent scoring rules."""

    def analyze(
        self,
        raw_email: str | bytes,
        filename: str = "",
    ) -> AnalysisResult:
        """Parse an email, detect indicators, and calculate risk."""

        parsed_email = parse_message(
            raw_email=raw_email,
            filename=filename,
        )

        raw_text = parsed_email.get(
            "raw_text",
            "",
        )

        iocs = extract_iocs(raw_text)

        indicators: list[Indicator] = []

        indicators.extend(
            self._check_urgency(raw_text)
        )

        indicators.extend(
            self._check_threat_language(raw_text)
        )

        indicators.extend(
            self._check_credentials(raw_text)
        )

        indicators.extend(
            self._check_financial_language(raw_text)
        )

        indicators.extend(
            self._check_urls(iocs["urls"])
        )

        indicators.extend(
            self._check_sender_domains(
                parsed_email,
                iocs["domains"],
            )
        )

        indicators.extend(
            self._check_reply_to_mismatch(
                parsed_email
            )
        )

        indicators.extend(
            self._check_suspicious_attachments(
                parsed_email.get(
                    "attachments",
                    [],
                )
            )
        )

        indicators.extend(
            self._check_missing_identity(
                parsed_email
            )
        )

        total_score = min(
            100,
            sum(
                indicator.points
                for indicator in indicators
            ),
        )

        risk_level, verdict = (
            self._classify_score(total_score)
        )

        return AnalysisResult(
            score=total_score,
            risk_level=risk_level,
            verdict=verdict,
            indicators=indicators,
            iocs=iocs,
            parsed_email=parsed_email,
        )

    def _check_urgency(
        self,
        text: str,
    ) -> list[Indicator]:
        """Detect urgent or pressure-based language."""

        matched_terms = self._find_terms(
            text,
            URGENCY_TERMS,
        )

        if not matched_terms:
            return []

        return [
            Indicator(
                name="Urgency or pressure language",
                description=(
                    "The message pressures the recipient "
                    "to act quickly."
                ),
                points=12,
                evidence=", ".join(matched_terms),
            )
        ]

    def _check_threat_language(
        self,
        text: str,
    ) -> list[Indicator]:
        """Detect account threats and fear-based language."""

        matched_terms = self._find_terms(
            text,
            THREAT_TERMS,
        )

        if not matched_terms:
            return []

        return [
            Indicator(
                name="Threat or fear language",
                description=(
                    "The message uses consequences or fear "
                    "to influence the recipient."
                ),
                points=15,
                evidence=", ".join(matched_terms),
            )
        ]

    def _check_credentials(
        self,
        text: str,
    ) -> list[Indicator]:
        """Detect requests for credentials or identity verification."""

        matched_terms = self._find_terms(
            text,
            CREDENTIAL_TERMS,
        )

        if not matched_terms:
            return []

        return [
            Indicator(
                name="Credential request",
                description=(
                    "The message requests passwords, login "
                    "details, or account verification."
                ),
                points=25,
                evidence=", ".join(matched_terms),
            )
        ]

    def _check_financial_language(
        self,
        text: str,
    ) -> list[Indicator]:
        """Detect payment and financial manipulation language."""

        matched_terms = self._find_terms(
            text,
            FINANCIAL_TERMS,
        )

        if not matched_terms:
            return []

        return [
            Indicator(
                name="Financial request",
                description=(
                    "The message contains financial, payment, "
                    "or fund-transfer language."
                ),
                points=18,
                evidence=", ".join(matched_terms),
            )
        ]

    def _check_urls(
        self,
        urls: list[str],
    ) -> list[Indicator]:
        """Inspect URLs for suspicious characteristics."""

        indicators: list[Indicator] = []

        if not urls:
            return indicators

        if len(urls) >= 3:
            indicators.append(
                Indicator(
                    name="Multiple URLs",
                    description=(
                        "The message contains several external links."
                    ),
                    points=5,
                    evidence=f"{len(urls)} URLs found",
                )
            )

        for url in urls:
            try:
                parsed = urlparse(url)
            except ValueError:
                continue

            hostname = (
                parsed.hostname
                or ""
            ).lower()

            if not hostname:
                continue

            if parsed.scheme.lower() == "http":
                indicators.append(
                    Indicator(
                        name="Unencrypted HTTP link",
                        description=(
                            "The message contains a link that "
                            "does not use HTTPS."
                        ),
                        points=10,
                        evidence=url,
                    )
                )

            if hostname in URL_SHORTENERS:
                indicators.append(
                    Indicator(
                        name="Shortened URL",
                        description=(
                            "The destination is hidden behind "
                            "a URL-shortening service."
                        ),
                        points=12,
                        evidence=url,
                    )
                )

            if self._looks_like_ip_address(
                hostname
            ):
                indicators.append(
                    Indicator(
                        name="IP-address URL",
                        description=(
                            "The link uses a numeric IP address "
                            "instead of a normal domain."
                        ),
                        points=20,
                        evidence=url,
                    )
                )

            tld = hostname.rsplit(
                ".",
                maxsplit=1,
            )[-1]

            if tld in SUSPICIOUS_TLDS:
                indicators.append(
                    Indicator(
                        name="Higher-risk top-level domain",
                        description=(
                            "The link uses a domain ending that "
                            "is frequently abused in malicious campaigns."
                        ),
                        points=8,
                        evidence=hostname,
                    )
                )

            if "@" in url:
                indicators.append(
                    Indicator(
                        name="URL contains an at-sign",
                        description=(
                            "An at-sign inside a URL can obscure "
                            "the actual destination."
                        ),
                        points=15,
                        evidence=url,
                    )
                )

            if hostname.count("-") >= 3:
                indicators.append(
                    Indicator(
                        name="Heavily hyphenated domain",
                        description=(
                            "The domain contains multiple hyphens, "
                            "which may indicate impersonation."
                        ),
                        points=6,
                        evidence=hostname,
                    )
                )

            if len(hostname) >= 40:
                indicators.append(
                    Indicator(
                        name="Unusually long domain",
                        description=(
                            "The hostname is unusually long."
                        ),
                        points=6,
                        evidence=hostname,
                    )
                )

        return self._remove_duplicate_indicators(
            indicators
        )

    def _check_sender_domains(
        self,
        parsed_email: dict[str, Any],
        domains: list[str],
    ) -> list[Indicator]:
        """Inspect sender information and detected domains."""

        sender = str(
            parsed_email.get(
                "sender",
                "",
            )
        ).lower()

        if not sender:
            return []

        sender_match = re.search(
            r"@([A-Za-z0-9.-]+\.[A-Za-z]{2,})",
            sender,
        )

        if not sender_match:
            return []

        sender_domain = sender_match.group(1).lower()

        linked_domains = {
            domain
            for domain in domains
            if domain != sender_domain
        }

        if not linked_domains:
            return []

        return [
            Indicator(
                name="Sender and link domain mismatch",
                description=(
                    "The sender domain differs from one or more "
                    "domains used in the message."
                ),
                points=12,
                evidence=(
                    f"Sender: {sender_domain}; "
                    f"Links: {', '.join(sorted(linked_domains))}"
                ),
            )
        ]

    def _check_reply_to_mismatch(
        self,
        parsed_email: dict[str, Any],
    ) -> list[Indicator]:
        """Check whether From and Reply-To use different domains."""

        sender = str(
            parsed_email.get("sender", "")
        )

        reply_to = str(
            parsed_email.get("reply_to", "")
        )

        sender_domain = self._extract_email_domain(
            sender
        )

        reply_domain = self._extract_email_domain(
            reply_to
        )

        if (
            not sender_domain
            or not reply_domain
            or sender_domain == reply_domain
        ):
            return []

        return [
            Indicator(
                name="Reply-To domain mismatch",
                description=(
                    "Replies would be sent to a domain that "
                    "differs from the visible sender domain."
                ),
                points=18,
                evidence=(
                    f"From: {sender_domain}; "
                    f"Reply-To: {reply_domain}"
                ),
            )
        ]

    def _check_suspicious_attachments(
        self,
        attachments: list[str],
    ) -> list[Indicator]:
        """Detect dangerous attachment extensions."""

        suspicious_files: list[str] = []

        for attachment in attachments:
            extension = Path(
                attachment.lower()
            ).suffix

            if extension in SUSPICIOUS_ATTACHMENT_EXTENSIONS:
                suspicious_files.append(attachment)

        if not suspicious_files:
            return []

        return [
            Indicator(
                name="Potentially dangerous attachment",
                description=(
                    "The email contains an attachment type "
                    "that can execute code or deliver malware."
                ),
                points=30,
                evidence=", ".join(suspicious_files),
            )
        ]

    def _check_missing_identity(
        self,
        parsed_email: dict[str, Any],
    ) -> list[Indicator]:
        """Detect absent sender or subject fields."""

        missing_fields: list[str] = []

        if not parsed_email.get("sender"):
            missing_fields.append("From")

        if not parsed_email.get("subject"):
            missing_fields.append("Subject")

        if not missing_fields:
            return []

        return [
            Indicator(
                name="Missing email identity fields",
                description=(
                    "The message is missing expected sender "
                    "or subject information."
                ),
                points=5,
                evidence=", ".join(missing_fields),
            )
        ]

    @staticmethod
    def _find_terms(
        text: str,
        terms: set[str],
    ) -> list[str]:
        """Return matched case-insensitive phrases."""

        lowered_text = text.lower()

        return sorted(
            term
            for term in terms
            if term in lowered_text
        )

    @staticmethod
    def _extract_email_domain(
        value: str,
    ) -> str:
        """Extract the domain from an email-containing string."""

        match = re.search(
            r"@([A-Za-z0-9.-]+\.[A-Za-z]{2,})",
            value,
        )

        if not match:
            return ""

        return match.group(1).lower()

    @staticmethod
    def _looks_like_ip_address(
        hostname: str,
    ) -> bool:
        """Return True when a hostname resembles an IPv4 address."""

        octets = hostname.split(".")

        if len(octets) != 4:
            return False

        try:
            return all(
                0 <= int(octet) <= 255
                for octet in octets
            )
        except ValueError:
            return False

    @staticmethod
    def _remove_duplicate_indicators(
        indicators: list[Indicator],
    ) -> list[Indicator]:
        """Remove exact duplicate indicators."""

        unique: dict[
            tuple[str, str],
            Indicator,
        ] = {}

        for indicator in indicators:
            key = (
                indicator.name,
                indicator.evidence,
            )
            unique[key] = indicator

        return list(unique.values())

    @staticmethod
    def _classify_score(
        score: int,
    ) -> tuple[str, str]:
        """Convert a numeric score into risk and verdict labels."""

        if score >= 75:
            return "CRITICAL", "PHISHING"

        if score >= 50:
            return "HIGH", "LIKELY PHISHING"

        if score >= 25:
            return "MEDIUM", "SUSPICIOUS"

        return "LOW", "LIKELY SAFE"