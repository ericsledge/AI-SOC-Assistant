"""Perform limited live Week 11 threat-intelligence lookups."""

from backend.threat_intelligence import (
    ThreatIntelligenceClient,
)


def main() -> None:
    """Test configured providers using a small lookup set."""

    client = ThreatIntelligenceClient()

    print("=" * 60)
    print("WEEK 11 THREAT-INTELLIGENCE CONNECTION TEST")
    print("=" * 60)

    status = client.provider_status()

    print(
        "VirusTotal configured:",
        status["virustotal"],
    )

    print(
        "AbuseIPDB configured:",
        status["abuseipdb"],
    )

    print()

    print("VirusTotal domain lookup:")
    domain_result = client.lookup_virustotal_domain(
        "example.com"
    )

    print(domain_result)
    print()

    print("AbuseIPDB public-IP lookup:")
    ip_result = client.lookup_abuseipdb(
        "8.8.8.8"
    )

    print(ip_result)
    print("=" * 60)


if __name__ == "__main__":
    main()