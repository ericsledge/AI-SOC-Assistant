"""Display Week 10 phishing-engine results in the terminal."""

from pathlib import Path

from backend.phishing_engine import PhishingAnalysisEngine


PROJECT_ROOT = Path(__file__).resolve().parent.parent
EMAIL_PATH = (
    PROJECT_ROOT
    / "data"
    / "week10_phishing_email.txt"
)


def main() -> None:
    """Analyze the Week 10 phishing sample."""

    email_text = EMAIL_PATH.read_text(
        encoding="utf-8"
    )

    engine = PhishingAnalysisEngine()

    result = engine.analyze(
        raw_email=email_text,
        filename=EMAIL_PATH.name,
    )

    print("=" * 60)
    print("WEEK 10 PHISHING ANALYSIS ENGINE")
    print("=" * 60)
    print(f"Risk Score: {result.score}/100")
    print(f"Risk Level: {result.risk_level}")
    print(f"Verdict: {result.verdict}")
    print()

    print("URLs:")
    for url in result.iocs["urls"]:
        print(f"  - {url}")

    print()

    print("Domains:")
    for domain in result.iocs["domains"]:
        print(f"  - {domain}")

    print()

    print("Suspicious Indicators:")
    for indicator in result.indicators:
        print(
            f"  - {indicator.name} "
            f"(+{indicator.points})"
        )
        print(
            f"    Evidence: {indicator.evidence}"
        )

    print("=" * 60)


if __name__ == "__main__":
    main()