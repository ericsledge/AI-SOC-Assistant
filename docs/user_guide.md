# User Guide

## Starting the Application

Activate the virtual environment.

Run:

streamlit run frontend\streamlit_app.py

The dashboard opens in your web browser.

---

## Asking Questions

Type a cybersecurity-related question into the chat input.

Examples:

What is phishing?

Explain MITRE ATT&CK.

What are the phases of incident response?

What indicators suggest ransomware?

---

## Viewing Sources

Each answer includes supporting source documents.

Expand the Sources section to view which documents were used.

Expand Retrieved Chunks to inspect the exact document passages used for answer generation.

---

## Supported Topics

The assistant answers questions related to documents contained in the knowledge base.

Examples:

- SOC Operations
- Incident Response
- Malware
- Phishing
- MITRE ATT&CK
- Windows Security
- Cybersecurity Concepts

---

## Questions Outside the Knowledge Base

Questions unrelated to cybersecurity may not produce accurate responses.

The assistant should only be relied upon for topics contained within the indexed documents.

---

## Ending the Session

Simply close the browser or stop Streamlit with:

Ctrl + C