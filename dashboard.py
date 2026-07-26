"""Streamlit dashboard for the AI SOC Analyst Assistant."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from backend.phishing_analyzer import PhishingAnalyzer
from backend.phishing_engine import PhishingAnalysisEngine

from backend.threat_intelligence import (
    ThreatIntelligenceClient,
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIRECTORY = PROJECT_ROOT / "data"
REPORTS_DIRECTORY = PROJECT_ROOT / "reports"
LOGS_DIRECTORY = PROJECT_ROOT / "logs"

PHISHING_SAMPLE_PATH = DATA_DIRECTORY / "phishing_email.txt"
SAFE_SAMPLE_PATH = DATA_DIRECTORY / "safe_email.txt"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

def configure_page() -> None:
    """Configure the Streamlit browser page."""

    st.set_page_config(
        page_title="AI SOC Analyst Assistant",
        page_icon="ðŸ›¡ï¸",
        layout="wide",
        initial_sidebar_state="expanded",
    )


# ============================================================
# SESSION STATE
# ============================================================

def initialize_session_state() -> None:
    """Initialize values that must survive Streamlit reruns."""

    defaults: dict[str, Any] = {
        "threat_intel_result": None,
        "email_text": "",
        "analysis_result": "",
        "engine_result": None,
        "uploaded_filename": "",
        "current_report": "",
        "current_report_name": "phishing_analysis_report.txt",
        "analysis_history": [],
        "connection_checked": False,
        "connection_ok": False,
        "upload_message": "",
        "upload_error": "",
        "sample_error": "",
        "uploader_version": 0,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================
# OLLAMA / ANALYZER
# ============================================================

@st.cache_resource
def get_analyzer() -> PhishingAnalyzer:
    """Create and reuse one phishing analyzer instance."""

    return PhishingAnalyzer()


def test_ollama_connection() -> None:
    """Test the Ollama connection from a button callback."""

    analyzer = get_analyzer()

    try:
        connection_ok = analyzer.llm_client.test_connection()

        st.session_state.connection_checked = True
        st.session_state.connection_ok = connection_ok

    except Exception:
        st.session_state.connection_checked = True
        st.session_state.connection_ok = False


# ============================================================
# FILE READING
# ============================================================

def read_text_file(file_path: Path) -> str:
    """Read a UTF-8 text file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return file_path.read_text(encoding="utf-8")


def decode_uploaded_file(uploaded_file: Any) -> str:
    """Decode an uploaded text file."""

    raw_bytes = uploaded_file.getvalue()

    try:
        return raw_bytes.decode("utf-8")

    except UnicodeDecodeError:
        return raw_bytes.decode("latin-1")


# ============================================================
# CALLBACKS
# ============================================================

def clear_current_results() -> None:
    """Clear analysis results without clearing the email text."""

    st.session_state.analysis_result = ""
    st.session_state.current_report = ""
    st.session_state.current_report_name = (
        "phishing_analysis_report.txt"
    )


def clear_dashboard() -> None:
    """Clear the email, upload, and current analysis."""
    st.session_state.threat_intel_result = None
    st.session_state.engine_result = None
    st.session_state.uploaded_filename = ""
    st.session_state.email_text = ""
    st.session_state.analysis_result = ""
    st.session_state.current_report = ""
    st.session_state.current_report_name = (
        "phishing_analysis_report.txt"
    )
    st.session_state.upload_message = ""
    st.session_state.upload_error = ""
    st.session_state.sample_error = ""


def load_sample(sample_path: Path) -> None:
    """Load a sample email into the text area."""

    st.session_state.uploaded_filename = (
    sample_path.name
    )
    st.session_state.engine_result = None

    try:
        sample_text = read_text_file(sample_path)

        st.session_state.email_text = sample_text
        st.session_state.threat_intel_result = None
        st.session_state.analysis_result = ""
        st.session_state.current_report = ""
        st.session_state.current_report_name = (
            "phishing_analysis_report.txt"
        )
        st.session_state.upload_message = ""
        st.session_state.upload_error = ""
        st.session_state.sample_error = ""

        st.session_state.uploader_version += 1

    except FileNotFoundError as error:
        st.session_state.sample_error = str(error)


def process_uploaded_file() -> None:
    """Copy an uploaded text file into the email text area."""

    uploader_key = (
        f"uploaded_email_{st.session_state.uploader_version}"
    )

    uploaded_file = st.session_state.get(uploader_key)

    if uploaded_file is None:
        st.session_state.upload_message = ""
        st.session_state.upload_error = ""
        return

    try:
        uploaded_text = decode_uploaded_file(uploaded_file)

        st.session_state.email_text = uploaded_text
        st.session_state.threat_intel_result = None
        st.session_state.uploaded_filename = (
            uploaded_file.name
        )
        st.session_state.engine_result = None
        st.session_state.analysis_result = ""
        st.session_state.current_report = ""
        st.session_state.current_report_name = (
            "phishing_analysis_report.txt"
        )
        st.session_state.upload_message = (
            f"Loaded {uploaded_file.name}"
        )
        st.session_state.upload_error = ""

    except Exception as error:
        st.session_state.upload_message = ""
        st.session_state.upload_error = (
            f"Could not read the uploaded file: {error}"
        )


# ============================================================
# ANALYSIS PARSING
# ============================================================

def extract_section(
    analysis: str,
    heading: str,
) -> str:
    """Extract one section from the structured LLM response."""

    headings = [
        "RISK LEVEL",
        "SUMMARY",
        "PHISHING INDICATORS",
        "LEGITIMATE INDICATORS",
        "RECOMMENDED ACTIONS",
        "FINAL VERDICT",
    ]

    heading_pattern = "|".join(
        re.escape(item)
        for item in headings
    )

    pattern = (
        rf"{re.escape(heading)}\s*:\s*"
        rf"(.*?)"
        rf"(?=\n(?:{heading_pattern})\s*:|\Z)"
    )

    match = re.search(
        pattern,
        analysis,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return "Not available"

    return match.group(1).strip()


def first_line(value: str) -> str:
    """Return the first nonempty line from a value."""

    for line in value.splitlines():
        cleaned_line = line.strip()

        if cleaned_line:
            return cleaned_line

    return "Not available"


# ============================================================
# IOC EXTRACTION
# ============================================================

def extract_urls(email_text: str) -> list[str]:
    """Extract HTTP and HTTPS URLs."""

    pattern = r"https?://[^\s<>()\[\]\"']+"

    results = re.findall(
        pattern,
        email_text,
        flags=re.IGNORECASE,
    )

    cleaned_results = {
        item.rstrip(".,;:!?)")
        for item in results
    }

    return sorted(cleaned_results)


def extract_email_addresses(
    email_text: str,
) -> list[str]:
    """Extract email addresses."""

    pattern = (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}\b"
    )

    results = re.findall(
        pattern,
        email_text,
        flags=re.IGNORECASE,
    )

    return sorted(set(results))


def extract_ipv4_addresses(
    email_text: str,
) -> list[str]:
    """Extract valid IPv4 addresses."""

    candidates = re.findall(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        email_text,
    )

    valid_addresses: list[str] = []

    for candidate in candidates:
        octets = candidate.split(".")

        if all(
            0 <= int(octet) <= 255
            for octet in octets
        ):
            valid_addresses.append(candidate)

    return sorted(set(valid_addresses))


# ============================================================
# REPORTS AND LOGGING
# ============================================================

def create_report(
    email_text: str,
    analysis: str,
    engine_result: dict[str, Any] | None = None,
    threat_intel_result: dict[str, Any] | None = None,
) -> tuple[str, str]:
    """Create and save a timestamped phishing-analysis report."""

    REPORTS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"phishing_analysis_{timestamp}.txt"
    )

    report_path = (
        REPORTS_DIRECTORY / filename
    )

    engine_section = ""

    if engine_result:
        indicator_lines = "\n".join(
            (
                f"- {indicator['name']} "
                f"(+{indicator['points']}): "
                f"{indicator['evidence']}"
            )
            for indicator in engine_result[
                "indicators"
            ]
        )

        if not indicator_lines:
            indicator_lines = (
                "No suspicious indicators detected."
            )

        url_lines = "\n".join(
            engine_result["iocs"]["urls"]
        )

        if not url_lines:
            url_lines = "None"

        domain_lines = "\n".join(
            engine_result["iocs"]["domains"]
        )

        if not domain_lines:
            domain_lines = "None"

        engine_section = f"""
AUTOMATED PHISHING ENGINE
=========================
Risk Score: {engine_result['score']}/100
Risk Level: {engine_result['risk_level']}
Verdict: {engine_result['verdict']}

Indicators:
{indicator_lines}

URLs:
{url_lines}

Domains:
{domain_lines}
""".strip()

    threat_intel_section = ""

    if threat_intel_result:
        summary = threat_intel_result.get(
            "summary",
            {},
        )

        threat_lines: list[str] = []

        for url_result in threat_intel_result.get(
            "urls",
            [],
        ):
            threat_lines.append(
                (
                    f"URL: {url_result.get('value')}\n"
                    f"Provider: VirusTotal\n"
                    f"Status: {url_result.get('status')}\n"
                    f"Malicious detections: "
                    f"{url_result.get('malicious_count', 0)}\n"
                    f"Suspicious detections: "
                    f"{url_result.get('suspicious_count', 0)}"
                )
            )

        for domain_result in threat_intel_result.get(
            "domains",
            [],
        ):
            threat_lines.append(
                (
                    f"Domain: {domain_result.get('value')}\n"
                    f"Provider: VirusTotal\n"
                    f"Status: {domain_result.get('status')}\n"
                    f"Malicious detections: "
                    f"{domain_result.get('malicious_count', 0)}\n"
                    f"Suspicious detections: "
                    f"{domain_result.get('suspicious_count', 0)}"
                )
            )

        for ip_result in threat_intel_result.get(
            "ip_addresses",
            [],
        ):
            abuse_result = ip_result.get(
                "abuseipdb",
                {},
            )

            vt_result = ip_result.get(
                "virustotal",
                {},
            )

            threat_lines.append(
                (
                    f"IP Address: {ip_result.get('value')}\n"
                    f"VirusTotal status: "
                    f"{vt_result.get('status')}\n"
                    f"VirusTotal malicious detections: "
                    f"{vt_result.get('malicious_count', 0)}\n"
                    f"AbuseIPDB status: "
                    f"{abuse_result.get('status')}\n"
                    f"Abuse confidence score: "
                    f"{abuse_result.get('abuse_confidence_score', 0)}\n"
                    f"Total abuse reports: "
                    f"{abuse_result.get('total_reports', 0)}"
                )
            )

        threat_details = "\n\n".join(
            threat_lines
        )

        if not threat_details:
            threat_details = (
                "No indicators were available for enrichment."
            )

        threat_intel_section = f"""
THREAT INTELLIGENCE ENRICHMENT
==============================
Indicators Queried: {summary.get('queried', 0)}
Successful Lookups: {summary.get('successful', 0)}
Threat Matches: {summary.get('malicious', 0)}
Errors: {summary.get('errors', 0)}

{threat_details}
""".strip()

    report_text = f"""
AI SOC ANALYST ASSISTANT
Phishing Email Analysis Report

Generated: {generated_time}

ORIGINAL EMAIL
==============
{email_text}

{engine_section}

{threat_intel_section}

AI ANALYSIS
===========
{analysis}
""".strip()

    report_path.write_text(
        report_text,
        encoding="utf-8",
    )

    return filename, report_text


def write_log(message: str) -> None:
    """Append an event to the application log."""

    LOGS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    log_path = LOGS_DIRECTORY / "application.log"

    timestamp = datetime.now().isoformat(
        timespec="seconds"
    )

    with log_path.open(
        "a",
        encoding="utf-8",
    ) as log_file:
        log_file.write(
            f"{timestamp} | STREAMLIT | {message}\n"
        )


# ============================================================
# EMAIL ANALYSIS
# ============================================================

def analyze_email() -> None:
    """Analyze the email currently stored in session state."""

    email_text = st.session_state.email_text.strip()

    if not email_text:
        st.warning(
            "Paste an email or upload a text file "
            "before analyzing."
        )
        return

    engine = PhishingAnalysisEngine()

    engine_result = engine.analyze(
    raw_email=email_text,
    filename=st.session_state.get(
        "uploaded_filename",
        "",
    ),
)

    st.session_state.engine_result = (
    engine_result.to_dict()
)
    
    threat_intelligence_client = (
    ThreatIntelligenceClient()
)

    threat_intel_result = (
    threat_intelligence_client.enrich_iocs(
        engine_result.iocs
    )
)

    st.session_state.threat_intel_result = (
    threat_intel_result
)

    analyzer = get_analyzer()

    try:
        connection_ok = (
            analyzer.llm_client.test_connection()
        )

        st.session_state.connection_checked = True
        st.session_state.connection_ok = connection_ok

        if not connection_ok:
            st.error(
                "Ollama is unavailable. Start Ollama and "
                "verify that qwen2.5:1.5b is installed."
            )

            write_log(
                "Analysis blocked because Ollama "
                "was unavailable."
            )
            return

        with st.spinner(
            "Analyzing the email with the local "
            "Qwen model..."
        ):
            analysis = analyzer.analyze(email_text)

        filename, report_text = create_report(
            email_text=email_text,
            analysis=analysis,
            engine_result=engine_result.to_dict(),
            threat_intel_result=threat_intel_result,
        )

        risk_level = first_line(
            extract_section(
                analysis,
                "RISK LEVEL",
            )
        )

        verdict = first_line(
            extract_section(
                analysis,
                "FINAL VERDICT",
            )
        )

        history_item = {
            "Time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Engine Score": engine_result.score,
            "Risk": risk_level,
            "Verdict": verdict,
            "Report": filename,
        }

        st.session_state.analysis_result = analysis
        st.session_state.current_report = report_text
        st.session_state.current_report_name = filename

        st.session_state.analysis_history.insert(
            0,
            history_item,
        )

        write_log(
            f"Analysis completed successfully. "
            f"Report: {filename}"
        )

        st.success(
            "Analysis completed successfully."
        )

    except ValueError as error:
        st.error(f"Input error: {error}")
        write_log(f"Input error: {error}")

    except ConnectionError as error:
        st.error(f"Connection error: {error}")
        write_log(f"Connection error: {error}")

    except RuntimeError as error:
        st.error(f"Model error: {error}")
        write_log(f"Model error: {error}")

    except Exception as error:
        st.error(f"Unexpected error: {error}")
        write_log(f"Unexpected error: {error}")


# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar() -> None:
    """Render the Streamlit sidebar."""

    analyzer = get_analyzer()

    with st.sidebar:
        st.header("System Status")

        st.write("**Model**")
        st.code(analyzer.llm_client.model)

        st.write("**API endpoint**")
        st.code(analyzer.llm_client.base_url)

        st.button(
            "Test Ollama Connection",
            use_container_width=True,
            on_click=test_ollama_connection,
        )

        if st.session_state.connection_checked:
            if st.session_state.connection_ok:
                st.success("Status: Connected")
            else:
                st.error("Status: Disconnected")
        else:
            st.info("Status: Not tested")

        st.divider()

        st.header("Sample Emails")

        st.button(
            "Load Phishing Sample",
            use_container_width=True,
            on_click=load_sample,
            args=(PHISHING_SAMPLE_PATH,),
        )

        st.button(
            "Load Safe Sample",
            use_container_width=True,
            on_click=load_sample,
            args=(SAFE_SAMPLE_PATH,),
        )

        st.button(
            "Clear Dashboard",
            use_container_width=True,
            on_click=clear_dashboard,
        )

        if st.session_state.sample_error:
            st.error(
                st.session_state.sample_error
            )

        st.divider()

        st.caption(
            "The dashboard uses a local Ollama model. "
            "Email content remains on this machine."
        )


# ============================================================
# INPUT SECTION
# ============================================================

def render_input_section() -> None:
    """Render the email input section."""

    st.subheader("Email Input")

    paste_tab, upload_tab = st.tabs(
        [
            "Paste Email",
            "Upload Text File",
        ]
    )

    with paste_tab:
        st.text_area(
            "Paste the complete email",
            key="email_text",
            height=300,
            placeholder=(
                "Paste the sender, subject, message body, "
                "links, and available headers here."
            ),
        )

    with upload_tab:
        uploader_key = (
            f"uploaded_email_{st.session_state.uploader_version}"
        )

        st.file_uploader(
            "Upload a TXT or EML email",
            type=["txt", "eml"],
            accept_multiple_files=False,
            key=uploader_key,
            on_change=process_uploaded_file,
        )

        if st.session_state.upload_message:
            st.success(
                st.session_state.upload_message
            )

        if st.session_state.upload_error:
            st.error(
                st.session_state.upload_error
            )

        if st.session_state.email_text:
            with st.expander(
                "Preview current email text",
                expanded=True,
            ):
                st.text(
                    st.session_state.email_text
                )

    analyze_column, clear_column = st.columns(
        [3, 1]
    )

    with analyze_column:
        analyze_clicked = st.button(
            "Analyze Email",
            type="primary",
            use_container_width=True,
        )

    with clear_column:
        st.button(
            "Clear",
            use_container_width=True,
            on_click=clear_dashboard,
        )

    if analyze_clicked:
        analyze_email()


# ============================================================
# RESULTS
# ============================================================

def render_metrics(analysis: str) -> None:
    """Render the top analysis metrics."""

    risk_level = first_line(
        extract_section(
            analysis,
            "RISK LEVEL",
        )
    )

    verdict = first_line(
        extract_section(
            analysis,
            "FINAL VERDICT",
        )
    )

    urls = extract_urls(
        st.session_state.email_text
    )

    email_addresses = extract_email_addresses(
        st.session_state.email_text
    )

    metric_1, metric_2, metric_3, metric_4 = (
        st.columns(4)
    )

    metric_1.metric(
        "Risk Level",
        risk_level,
    )

    metric_2.metric(
        "Final Verdict",
        verdict,
    )

    metric_3.metric(
        "URLs Found",
        len(urls),
    )

    metric_4.metric(
        "Email Addresses",
        len(email_addresses),
    )

def render_engine_results() -> None:
    """Display deterministic Week 10 engine results."""

    engine_result = st.session_state.get(
        "engine_result"
    )

    if not engine_result:
        return

    st.divider()
    st.subheader("Automated Phishing Engine")

    score = engine_result["score"]
    risk_level = engine_result["risk_level"]
    verdict = engine_result["verdict"]

    score_column, risk_column, verdict_column = (
        st.columns(3)
    )

    score_column.metric(
        "Phishing Risk Score",
        f"{score}/100",
    )

    risk_column.metric(
        "Engine Risk Level",
        risk_level,
    )

    verdict_column.metric(
        "Engine Verdict",
        verdict,
    )

    st.progress(
        score / 100,
        text=f"Phishing risk score: {score}/100",
    )

    indicator_tab, domain_tab, header_tab = st.tabs(
        [
            "Suspicious Indicators",
            "URLs and Domains",
            "Parsed Email",
        ]
    )

    with indicator_tab:
        indicators = engine_result["indicators"]

        if not indicators:
            st.success(
                "No suspicious indicators were detected."
            )
        else:
            for indicator in indicators:
                with st.expander(
                    (
                        f"{indicator['name']} "
                        f"(+{indicator['points']} points)"
                    )
                ):
                    st.write(
                        indicator["description"]
                    )
                    st.write("**Evidence**")
                    st.code(
                        indicator["evidence"]
                    )

    with domain_tab:
        iocs = engine_result["iocs"]

        st.markdown("#### URLs")

        if iocs["urls"]:
            for url in iocs["urls"]:
                st.code(url)
        else:
            st.write("No URLs detected.")

        st.markdown("#### Domains")

        if iocs["domains"]:
            for domain in iocs["domains"]:
                st.code(domain)
        else:
            st.write("No domains detected.")

        st.markdown("#### Email Addresses")

        if iocs["email_addresses"]:
            for address in iocs["email_addresses"]:
                st.code(address)
        else:
            st.write(
                "No email addresses detected."
            )

        st.markdown("#### IPv4 Addresses")

        if iocs["ipv4_addresses"]:
            for address in iocs["ipv4_addresses"]:
                st.code(address)
        else:
            st.write(
                "No IPv4 addresses detected."
            )

    with header_tab:
        parsed_email = engine_result[
            "parsed_email"
        ]

        st.write(
            f"**Format:** "
            f"{parsed_email.get('format', '')}"
        )
        st.write(
            f"**From:** "
            f"{parsed_email.get('sender', '') or 'Not available'}"
        )
        st.write(
            f"**To:** "
            f"{parsed_email.get('recipient', '') or 'Not available'}"
        )
        st.write(
            f"**Subject:** "
            f"{parsed_email.get('subject', '') or 'Not available'}"
        )
        st.write(
            f"**Reply-To:** "
            f"{parsed_email.get('reply_to', '') or 'Not available'}"
        )

        attachments = parsed_email.get(
            "attachments",
            [],
        )

        st.write("**Attachments:**")

        if attachments:
            for attachment in attachments:
                st.code(attachment)
        else:
            st.write("None detected.")

def render_analysis_results() -> None:
    """Render the completed analysis."""

    analysis = st.session_state.analysis_result

    if not analysis:
        st.info(
            "Enter an email and select Analyze Email "
            "to begin."
        )
        return

    st.divider()
    st.subheader("Analysis Results")

    render_metrics(analysis)

    summary = extract_section(
        analysis,
        "SUMMARY",
    )

    phishing_indicators = extract_section(
        analysis,
        "PHISHING INDICATORS",
    )

    legitimate_indicators = extract_section(
        analysis,
        "LEGITIMATE INDICATORS",
    )

    recommended_actions = extract_section(
        analysis,
        "RECOMMENDED ACTIONS",
    )

    assessment_tab, indicators_tab, ioc_tab, raw_tab = (
        st.tabs(
            [
                "Assessment",
                "Indicators",
                "Extracted IOCs",
                "Raw Analysis",
            ]
        )
    )

    with assessment_tab:
        st.markdown("#### Summary")
        st.write(summary)

        st.markdown(
            "#### Recommended Actions"
        )
        st.write(recommended_actions)

    with indicators_tab:
        suspicious_column, legitimate_column = (
            st.columns(2)
        )

        with suspicious_column:
            st.markdown(
                "#### Phishing Indicators"
            )
            st.write(phishing_indicators)

        with legitimate_column:
            st.markdown(
                "#### Legitimate Indicators"
            )
            st.write(legitimate_indicators)

    with ioc_tab:
        urls = extract_urls(
            st.session_state.email_text
        )

        addresses = extract_email_addresses(
            st.session_state.email_text
        )

        ipv4_addresses = extract_ipv4_addresses(
            st.session_state.email_text
        )

        st.markdown("#### URLs")

        if urls:
            for url in urls:
                st.code(url)
        else:
            st.write("No URLs found.")

        st.markdown("#### Email Addresses")

        if addresses:
            for address in addresses:
                st.code(address)
        else:
            st.write(
                "No email addresses found."
            )

        st.markdown("#### IPv4 Addresses")

        if ipv4_addresses:
            for address in ipv4_addresses:
                st.code(address)
        else:
            st.write(
                "No IPv4 addresses found."
            )

    with raw_tab:
        st.text(analysis)

    if st.session_state.current_report:
        st.download_button(
            label="Download Analysis Report",
            data=st.session_state.current_report,
            file_name=(
                st.session_state.current_report_name
            ),
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# HISTORY
# ============================================================

def render_history() -> None:
    """Render current-session analysis history."""

    st.divider()
    st.subheader("Session Analysis History")

    history = st.session_state.analysis_history

    if not history:
        st.caption(
            "No emails have been analyzed "
            "during this session."
        )
        return

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# MAIN APPLICATION
# ============================================================

def render_virustotal_item(
    result: dict[str, Any],
) -> None:
    """Render one normalized VirusTotal lookup result."""

    value = result.get("value", "Unknown")
    status = result.get("status", "unknown")

    with st.expander(value):
        st.write(f"**Status:** {status}")

        if result.get("cached"):
            st.caption("Loaded from local cache.")

        if status != "success":
            st.warning(
                result.get(
                    "error",
                    "No provider result was available.",
                )
            )
            return

        malicious = result.get(
            "malicious_count",
            0,
        )

        suspicious = result.get(
            "suspicious_count",
            0,
        )

        harmless = result.get(
            "harmless_count",
            0,
        )

        undetected = result.get(
            "undetected_count",
            0,
        )

        column1, column2, column3, column4 = (
            st.columns(4)
        )

        column1.metric("Malicious", malicious)
        column2.metric("Suspicious", suspicious)
        column3.metric("Harmless", harmless)
        column4.metric("Undetected", undetected)

        if result.get("malicious"):
            st.error(
                "Threat-intelligence detections were found."
            )
        else:
            st.success(
                "No malicious or suspicious detections "
                "were returned."
            )

        reputation = result.get("reputation")

        if reputation is not None:
            st.write(
                f"**Reputation:** {reputation}"
            )

        categories = result.get(
            "categories",
            {},
        )

        if categories:
            st.write("**Provider categories:**")

            for provider, category in list(
                categories.items()
            )[:10]:
                st.write(
                    f"- {provider}: {category}"
                )

def render_threat_intelligence_results() -> None:
    """Display Week 11 threat-intelligence enrichment."""

    result = st.session_state.get(
        "threat_intel_result"
    )

    if not result:
        return

    st.divider()
    st.subheader("Threat Intelligence Enrichment")

    provider_status = result.get(
        "provider_status",
        {},
    )

    virus_total_configured = (
        provider_status.get(
            "virustotal",
            False,
        )
    )

    abuseipdb_configured = (
        provider_status.get(
            "abuseipdb",
            False,
        )
    )

    status_column1, status_column2 = st.columns(2)

    status_column1.metric(
        "VirusTotal",
        (
            "Configured"
            if virus_total_configured
            else "Not configured"
        ),
    )

    status_column2.metric(
        "AbuseIPDB",
        (
            "Configured"
            if abuseipdb_configured
            else "Not configured"
        ),
    )

    summary = result.get("summary", {})

    summary_column1, summary_column2, summary_column3 = (
        st.columns(3)
    )

    summary_column1.metric(
        "Indicators Queried",
        summary.get("queried", 0),
    )

    summary_column2.metric(
        "Successful Lookups",
        summary.get("successful", 0),
    )

    summary_column3.metric(
        "Threat Matches",
        summary.get("malicious", 0),
    )

    if summary.get("malicious", 0) > 0:
        st.error(
            "One or more indicators have threat-intelligence "
            "detections."
        )
    elif summary.get("successful", 0) > 0:
        st.success(
            "No queried indicators were marked malicious."
        )
    else:
        st.info(
            "No successful external reputation results "
            "were available."
        )

    url_tab, domain_tab, ip_tab = st.tabs(
        [
            "URL Reputation",
            "Domain Reputation",
            "IP Reputation",
        ]
    )

    with url_tab:
        url_results = result.get("urls", [])

        if not url_results:
            st.info("No URLs were available for lookup.")
        else:
            for url_result in url_results:
                render_virustotal_item(url_result)

    with domain_tab:
        domain_results = result.get(
            "domains",
            [],
        )

        if not domain_results:
            st.info(
                "No domains were available for lookup."
            )
        else:
            for domain_result in domain_results:
                render_virustotal_item(
                    domain_result
                )

    with ip_tab:
        ip_results = result.get(
            "ip_addresses",
            [],
        )

        if not ip_results:
            st.info(
                "No public IP addresses were "
                "available for lookup."
            )

        for ip_result in ip_results:
            ip_value = ip_result.get(
                "value",
                "Unknown",
            )

            with st.expander(ip_value):
                if ip_result.get("status") == "skipped":
                    st.info(
                        ip_result.get(
                            "reason",
                            "The IP was skipped.",
                        )
                    )
                    continue

                virustotal_result = (
                    ip_result.get(
                        "virustotal",
                        {},
                    )
                )

                abuseipdb_result = (
                    ip_result.get(
                        "abuseipdb",
                        {},
                    )
                )

                st.markdown("#### VirusTotal")

                vt_status = virustotal_result.get(
                    "status",
                    "unknown",
                )

                st.write(
                    f"**Status:** {vt_status}"
                )

                if vt_status == "success":
                    st.write(
                        "**Malicious detections:** "
                        f"{virustotal_result.get('malicious_count', 0)}"
                    )

                    st.write(
                        "**Suspicious detections:** "
                        f"{virustotal_result.get('suspicious_count', 0)}"
                    )
                else:
                    st.warning(
                        virustotal_result.get(
                            "error",
                            "No VirusTotal result.",
                        )
                    )

                st.markdown("#### AbuseIPDB")

                abuse_status = abuseipdb_result.get(
                    "status",
                    "unknown",
                )

                st.write(
                    f"**Status:** {abuse_status}"
                )

                if abuse_status == "success":
                    st.write(
                        "**Abuse confidence score:** "
                        f"{abuseipdb_result.get('abuse_confidence_score', 0)}%"
                    )

                    st.write(
                        "**Total reports:** "
                        f"{abuseipdb_result.get('total_reports', 0)}"
                    )

                    st.write(
                        "**Country:** "
                        f"{abuseipdb_result.get('country_code') or 'Unknown'}"
                    )

                    st.write(
                        "**ISP:** "
                        f"{abuseipdb_result.get('isp') or 'Unknown'}"
                    )
                else:
                    st.warning(
                        abuseipdb_result.get(
                            "error",
                            "No AbuseIPDB result.",
                        )
                    )


def main() -> None:
    """Run the Streamlit dashboard."""

    configure_page()
    initialize_session_state()
    render_sidebar()

    st.title("🛡️ AI SOC Analyst Assistant")

    st.caption(
        "Local AI-assisted phishing email "
        "triage dashboard"
    )

    st.warning(
        "This tool supports analyst review. "
        "Do not treat model output as a final "
        "security decision."
    )

    render_input_section()
    render_engine_results()
    render_threat_intelligence_results()
    render_analysis_results()
    render_history()


if __name__ == "__main__":
    main()
