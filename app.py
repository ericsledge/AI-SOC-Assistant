"""Command-line application for the AI SOC Analyst Assistant."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from backend.phishing_analyzer import PhishingAnalyzer


PROJECT_ROOT = Path(__file__).resolve().parent
REPORTS_DIRECTORY = PROJECT_ROOT / "reports"
LOGS_DIRECTORY = PROJECT_ROOT / "logs"


def collect_email_input() -> str:
    """Collect multiline email content from the terminal."""

    print()
    print("Paste the complete email below.")
    print("Type END on a new line when finished.")
    print()

    lines: list[str] = []

    while True:
        line = input()

        if line.strip().upper() == "END":
            break

        lines.append(line)

    return "\n".join(lines).strip()


def save_report(email_text: str, analysis: str) -> Path:
    """Save the email and analysis in a timestamped report."""

    REPORTS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = (
        REPORTS_DIRECTORY
        / f"phishing_analysis_{timestamp}.txt"
    )

    report_content = f"""
AI SOC ANALYST ASSISTANT
Phishing Email Analysis Report

Generated: {datetime.now().isoformat(timespec="seconds")}

ORIGINAL EMAIL
==============
{email_text}

ANALYSIS
========
{analysis}
""".strip()

    report_path.write_text(
        report_content,
        encoding="utf-8",
    )

    return report_path


def write_log(message: str) -> None:
    """Write an event to the application log."""

    LOGS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    log_path = LOGS_DIRECTORY / "application.log"

    timestamp = datetime.now().isoformat(timespec="seconds")

    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp} | {message}\n")


def main() -> None:
    """Run the AI SOC Analyst Assistant."""

    print("=" * 60)
    print("AI SOC ANALYST ASSISTANT")
    print("Phishing Email Analysis")
    print("=" * 60)

    analyzer = PhishingAnalyzer()

    print("Checking the Ollama connection...")

    if not analyzer.llm_client.test_connection():
        print("The application could not connect to Ollama.")
        write_log("Application stopped: Ollama connection failed.")
        return

    print(f"Connected to model: {analyzer.llm_client.model}")

    email_text = collect_email_input()

    if not email_text:
        print("No email was entered. Analysis cancelled.")
        write_log("Analysis cancelled: empty input.")
        return

    try:
        print()
        print("Analyzing email...")
        print("This may take several minutes on this CPU-only server.")

        analysis = analyzer.analyze(email_text)

        print()
        print("=" * 60)
        print("ANALYSIS RESULT")
        print("=" * 60)
        print(analysis)
        print("=" * 60)

        report_path = save_report(
            email_text=email_text,
            analysis=analysis,
        )

        print()
        print(f"Report saved to: {report_path}")

        write_log(
            f"Analysis completed successfully. "
            f"Report: {report_path.name}"
        )

    except ValueError as error:
        print(f"Input error: {error}")
        write_log(f"Input error: {error}")

    except ConnectionError as error:
        print(f"Connection error: {error}")
        write_log(f"Connection error: {error}")

    except RuntimeError as error:
        print(f"Model error: {error}")
        write_log(f"Model error: {error}")

    except KeyboardInterrupt:
        print()
        print("Analysis cancelled by the user.")
        write_log("Analysis cancelled by the user.")

    except Exception as error:
        print(f"Unexpected error: {error}")
        write_log(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()