"""Tests for the Week 11 threat-intelligence client."""

from pathlib import Path
from unittest.mock import Mock

from backend.threat_intelligence import (
    ThreatIntelligenceClient,
)


def create_mock_response(
    status_code: int,
    payload: dict,
) -> Mock:
    """Create a Requests-compatible mocked response."""

    response = Mock()
    response.status_code = status_code
    response.ok = 200 <= status_code < 300
    response.json.return_value = payload

    return response


def test_virustotal_domain_result(tmp_path: Path) -> None:
    """VirusTotal domain results should be normalized."""

    session = Mock()

    session.request.return_value = create_mock_response(
        200,
        {
            "data": {
                "attributes": {
                    "last_analysis_stats": {
                        "malicious": 4,
                        "suspicious": 1,
                        "harmless": 20,
                        "undetected": 10,
                    },
                    "reputation": -25,
                    "categories": {
                        "Vendor A": "phishing"
                    },
                }
            }
        },
    )

    client = ThreatIntelligenceClient(
        virustotal_api_key="test-key",
        abuseipdb_api_key="",
        cache_path=tmp_path / "cache.json",
        session=session,
    )

    result = client.lookup_virustotal_domain(
        "malicious.example"
    )

    assert result["status"] == "success"
    assert result["malicious_count"] == 4
    assert result["suspicious_count"] == 1
    assert result["malicious"] is True


def test_abuseipdb_result(tmp_path: Path) -> None:
    """AbuseIPDB data should be normalized correctly."""

    session = Mock()

    session.request.return_value = create_mock_response(
        200,
        {
            "data": {
                "ipAddress": "8.8.8.8",
                "abuseConfidenceScore": 80,
                "totalReports": 25,
                "countryCode": "US",
                "usageType": "Data Center/Web Hosting",
                "isp": "Example ISP",
                "domain": "example.net",
                "lastReportedAt": "2026-07-01T12:00:00+00:00",
                "isWhitelisted": False,
            }
        },
    )

    client = ThreatIntelligenceClient(
        virustotal_api_key="",
        abuseipdb_api_key="test-key",
        cache_path=tmp_path / "cache.json",
        session=session,
    )

    result = client.lookup_abuseipdb("8.8.8.8")

    assert result["status"] == "success"
    assert result["abuse_confidence_score"] == 80
    assert result["total_reports"] == 25
    assert result["malicious"] is True


def test_private_ip_is_skipped(tmp_path: Path) -> None:
    """Private IP addresses must not be sent externally."""

    session = Mock()

    client = ThreatIntelligenceClient(
        virustotal_api_key="test-key",
        abuseipdb_api_key="test-key",
        cache_path=tmp_path / "cache.json",
        session=session,
    )

    result = client.lookup_ip("192.168.1.10")

    assert result["status"] == "skipped"
    assert result["malicious"] is False
    session.request.assert_not_called()


def test_missing_api_key(tmp_path: Path) -> None:
    """Missing API keys should produce a controlled result."""

    client = ThreatIntelligenceClient(
        virustotal_api_key="",
        abuseipdb_api_key="",
        cache_path=tmp_path / "cache.json",
    )

    result = client.lookup_virustotal_domain(
        "example.com"
    )

    assert result["status"] == "not_configured"
    assert result["malicious"] is False


def test_rate_limit_handling(tmp_path: Path) -> None:
    """HTTP 429 should be reported without crashing."""

    session = Mock()

    session.request.return_value = create_mock_response(
        429,
        {},
    )

    client = ThreatIntelligenceClient(
        virustotal_api_key="test-key",
        abuseipdb_api_key="",
        cache_path=tmp_path / "cache.json",
        session=session,
    )

    result = client.lookup_virustotal_domain(
        "example.com"
    )

    assert result["status"] == "rate_limited"
    assert result["malicious"] is False


def test_cache_prevents_duplicate_request(
    tmp_path: Path,
) -> None:
    """A cached lookup should not call the API twice."""

    session = Mock()

    session.request.return_value = create_mock_response(
        200,
        {
            "data": {
                "attributes": {
                    "last_analysis_stats": {
                        "malicious": 0,
                        "suspicious": 0,
                        "harmless": 10,
                        "undetected": 5,
                    }
                }
            }
        },
    )

    client = ThreatIntelligenceClient(
        virustotal_api_key="test-key",
        abuseipdb_api_key="",
        cache_path=tmp_path / "cache.json",
        session=session,
    )

    first_result = client.lookup_virustotal_domain(
        "example.com"
    )

    second_result = client.lookup_virustotal_domain(
        "example.com"
    )

    assert first_result["cached"] is False
    assert second_result["cached"] is True
    assert session.request.call_count == 1