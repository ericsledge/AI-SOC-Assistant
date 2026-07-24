"""Extract indicators of compromise from email content."""

from __future__ import annotations

from ipaddress import ip_address
import re
from urllib.parse import urlparse


URL_PATTERN = re.compile(
    r"(?i)\b(?:https?://|www\.)"
    r"[^\s<>{}\[\]\"']+"
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+"
    r"\.[A-Za-z]{2,}\b"
)

IPV4_PATTERN = re.compile(
    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
)


def normalize_url(url: str) -> str:
    """Normalize a URL extracted from email text."""

    cleaned = url.strip().rstrip(
        ".,;:!?)]}>\"'"
    )

    if cleaned.lower().startswith("www."):
        return f"http://{cleaned}"

    return cleaned


def extract_urls(text: str) -> list[str]:
    """Extract unique HTTP and HTTPS URLs."""

    urls = {
        normalize_url(match.group(0))
        for match in URL_PATTERN.finditer(text)
    }

    return sorted(
        url for url in urls if url
    )


def extract_domain_from_url(url: str) -> str:
    """Extract a lowercase hostname from a URL."""

    normalized_url = normalize_url(url)

    try:
        parsed = urlparse(normalized_url)
        hostname = parsed.hostname or ""
    except ValueError:
        return ""

    return hostname.lower().strip(".")


def extract_domains(text: str) -> list[str]:
    """Extract domains from URLs and email addresses."""

    domains: set[str] = set()

    for url in extract_urls(text):
        domain = extract_domain_from_url(url)

        if domain:
            domains.add(domain)

    for email_address in extract_email_addresses(text):
        _, _, domain = email_address.rpartition("@")

        if domain:
            domains.add(domain.lower().strip("."))

    return sorted(domains)


def extract_email_addresses(text: str) -> list[str]:
    """Extract unique email addresses."""

    return sorted(
        {
            match.group(0).lower()
            for match in EMAIL_PATTERN.finditer(text)
        }
    )


def extract_ipv4_addresses(text: str) -> list[str]:
    """Extract valid IPv4 addresses."""

    valid_addresses: set[str] = set()

    for match in IPV4_PATTERN.finditer(text):
        candidate = match.group(0)

        try:
            parsed_address = ip_address(candidate)
        except ValueError:
            continue

        if parsed_address.version == 4:
            valid_addresses.add(str(parsed_address))

    return sorted(valid_addresses)


def extract_iocs(text: str) -> dict[str, list[str]]:
    """Extract all supported IOC types from text."""

    return {
        "urls": extract_urls(text),
        "domains": extract_domains(text),
        "email_addresses": extract_email_addresses(text),
        "ipv4_addresses": extract_ipv4_addresses(text),
    }