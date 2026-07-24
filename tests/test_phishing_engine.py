"""Tests for the deterministic phishing analysis engine."""

from pathlib import Path

from backend.phishing_engine import PhishingAnalysisEngine


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = PROJECT_ROOT / "data"


def test_phishing_email_receives_high_score() -> None:
    """A clearly malicious sample should score as high risk."""

    email_path = (
        DATA_DIRECTORY
        / "week10_phishing_email.txt"
    )

    email_text = email_path.read_text(
        encoding="utf-8"
    )

    engine = PhishingAnalysisEngine()
    result = engine.analyze(
        raw_email=email_text,
        filename=email_path.name,
    )

    assert result.score >= 50
    assert result.risk_level in {
        "HIGH",
        "CRITICAL",
    }
    assert result.indicators
    assert result.iocs["urls"]


def test_safe_email_receives_low_score() -> None:
    """A normal class reminder should remain low risk."""

    email_path = (
        DATA_DIRECTORY
        / "week10_safe_email.txt"
    )

    email_text = email_path.read_text(
        encoding="utf-8"
    )

    engine = PhishingAnalysisEngine()
    result = engine.analyze(
        raw_email=email_text,
        filename=email_path.name,
    )

    assert result.score < 25
    assert result.risk_level == "LOW"


def test_domain_extraction() -> None:
    """Domains should be extracted from URLs and email addresses."""

    email_text = """
From: alert@example.com
Subject: Test

Visit https://security.example.net/login.
"""

    engine = PhishingAnalysisEngine()
    result = engine.analyze(email_text)

    assert "example.com" in result.iocs["domains"]
    assert "security.example.net" in result.iocs["domains"]