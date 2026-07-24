"""Test the phishing analyzer using a sample phishing email."""

from pathlib import Path

from backend.phishing_analyzer import PhishingAnalyzer


def main() -> None:
    """Read and analyze the phishing sample."""

    project_root = Path(__file__).resolve().parent.parent
    email_path = project_root / "data" / "phishing_email.txt"

    if not email_path.exists():
        print(f"Test file not found: {email_path}")
        return

    email_text = email_path.read_text(encoding="utf-8")

    analyzer = PhishingAnalyzer()

    print("Analyzing phishing test email...")
    print("This may take several minutes on a CPU-only system.")
    print()

    try:
        result = analyzer.analyze(email_text)

        print("=" * 60)
        print("PHISHING ANALYSIS RESULT")
        print("=" * 60)
        print(result)
        print("=" * 60)

    except Exception as error:
        print(f"Test failed: {error}")


if __name__ == "__main__":
    main()