"""Utilities for parsing plain-text and EML email messages."""

from __future__ import annotations

from email import policy
from email.message import EmailMessage
from email.parser import BytesParser, Parser
from html import unescape
import re
from typing import Any


def strip_html(html_text: str) -> str:
    """Convert basic HTML email content into readable plain text."""

    without_scripts = re.sub(
        r"<(?:script|style).*?>.*?</(?:script|style)>",
        " ",
        html_text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    without_tags = re.sub(
        r"<[^>]+>",
        " ",
        without_scripts,
    )

    decoded = unescape(without_tags)

    normalized = re.sub(
        r"[ \t]+",
        " ",
        decoded,
    )

    normalized = re.sub(
        r"\n\s*\n+",
        "\n\n",
        normalized,
    )

    return normalized.strip()


def extract_message_body(message: EmailMessage) -> str:
    """Extract the preferred text body from a parsed email message."""

    plain_parts: list[str] = []
    html_parts: list[str] = []

    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            disposition = part.get_content_disposition()

            if disposition == "attachment":
                continue

            if content_type not in {
                "text/plain",
                "text/html",
            }:
                continue

            try:
                content = part.get_content()
            except Exception:
                payload = part.get_payload(decode=True)

                if not isinstance(payload, bytes):
                    continue

                charset = part.get_content_charset() or "utf-8"
                content = payload.decode(
                    charset,
                    errors="replace",
                )

            if not isinstance(content, str):
                continue

            if content_type == "text/plain":
                plain_parts.append(content.strip())
            else:
                html_parts.append(strip_html(content))

    else:
        try:
            content = message.get_content()
        except Exception:
            payload = message.get_payload(decode=True)

            if isinstance(payload, bytes):
                charset = (
                    message.get_content_charset()
                    or "utf-8"
                )

                content = payload.decode(
                    charset,
                    errors="replace",
                )
            else:
                content = str(
                    message.get_payload()
                    or ""
                )

        if message.get_content_type() == "text/html":
            html_parts.append(strip_html(str(content)))
        else:
            plain_parts.append(str(content).strip())

    if plain_parts:
        return "\n\n".join(
            part for part in plain_parts if part
        ).strip()

    if html_parts:
        return "\n\n".join(
            part for part in html_parts if part
        ).strip()

    return ""


def parse_message(
    raw_email: str | bytes,
    filename: str = "",
) -> dict[str, Any]:
    """Parse plain-text or EML email content into a normalized dictionary."""

    if isinstance(raw_email, bytes):
        raw_bytes = raw_email
        decoded_text = raw_bytes.decode(
            "utf-8",
            errors="replace",
        )
    else:
        decoded_text = raw_email
        raw_bytes = raw_email.encode(
            "utf-8",
            errors="replace",
        )

    normalized_filename = filename.lower().strip()

    looks_like_eml = (
        normalized_filename.endswith(".eml")
        or bool(
            re.search(
                r"^(from|to|subject|date|message-id):",
                decoded_text,
                flags=re.IGNORECASE | re.MULTILINE,
            )
        )
    )

    if looks_like_eml:
        try:
            message = BytesParser(
                policy=policy.default
            ).parsebytes(raw_bytes)
        except Exception:
            message = Parser(
                policy=policy.default
            ).parsestr(decoded_text)

        subject = str(message.get("subject", "")).strip()
        sender = str(message.get("from", "")).strip()
        recipient = str(message.get("to", "")).strip()
        reply_to = str(message.get("reply-to", "")).strip()
        return_path = str(
            message.get("return-path", "")
        ).strip()
        date = str(message.get("date", "")).strip()
        message_id = str(
            message.get("message-id", "")
        ).strip()

        body = extract_message_body(message)

        attachments: list[str] = []

        for part in message.iter_attachments():
            attachment_name = part.get_filename()

            if attachment_name:
                attachments.append(attachment_name)

        return {
            "subject": subject,
            "sender": sender,
            "recipient": recipient,
            "reply_to": reply_to,
            "return_path": return_path,
            "date": date,
            "message_id": message_id,
            "body": body,
            "attachments": attachments,
            "raw_text": decoded_text,
            "format": "eml",
        }

    return {
        "subject": extract_header_value(
            decoded_text,
            "Subject",
        ),
        "sender": extract_header_value(
            decoded_text,
            "From",
        ),
        "recipient": extract_header_value(
            decoded_text,
            "To",
        ),
        "reply_to": extract_header_value(
            decoded_text,
            "Reply-To",
        ),
        "return_path": extract_header_value(
            decoded_text,
            "Return-Path",
        ),
        "date": extract_header_value(
            decoded_text,
            "Date",
        ),
        "message_id": extract_header_value(
            decoded_text,
            "Message-ID",
        ),
        "body": decoded_text,
        "attachments": [],
        "raw_text": decoded_text,
        "format": "plain-text",
    }


def extract_header_value(
    text: str,
    header_name: str,
) -> str:
    """Extract a simple header value from plain-text email content."""

    match = re.search(
        rf"^{re.escape(header_name)}:\s*(.+)$",
        text,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    if not match:
        return ""

    return match.group(1).strip()