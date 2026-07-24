"""Threat-intelligence enrichment for phishing indicators."""

from __future__ import annotations

import base64
from datetime import datetime, timedelta, timezone
import ipaddress
import json
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CACHE_PATH = PROJECT_ROOT / "cache" / "threat_intelligence.json"

VIRUSTOTAL_BASE_URL = "https://www.virustotal.com/api/v3"
ABUSEIPDB_CHECK_URL = "https://api.abuseipdb.com/api/v2/check"


class ThreatIntelligenceClient:
    """Query threat-intelligence providers and cache their results."""

    def __init__(
        self,
        virustotal_api_key: str | None = None,
        abuseipdb_api_key: str | None = None,
        timeout: int | None = None,
        cache_hours: int | None = None,
        cache_path: Path | None = None,
        session: requests.Session | None = None,
    ) -> None:
        """Initialize API configuration and local cache settings."""

        self.virustotal_api_key = (
            virustotal_api_key
            if virustotal_api_key is not None
            else os.getenv("VIRUSTOTAL_API_KEY", "")
        ).strip()

        self.abuseipdb_api_key = (
            abuseipdb_api_key
            if abuseipdb_api_key is not None
            else os.getenv("ABUSEIPDB_API_KEY", "")
        ).strip()

        self.timeout = timeout or self._read_integer_setting(
            "THREAT_INTEL_TIMEOUT",
            default=15,
        )

        self.cache_hours = (
            cache_hours
            if cache_hours is not None
            else self._read_integer_setting(
                "THREAT_INTEL_CACHE_HOURS",
                default=24,
            )
        )

        self.cache_path = cache_path or DEFAULT_CACHE_PATH
        self.session = session or requests.Session()

    def provider_status(self) -> dict[str, bool]:
        """Return whether each provider has an API key configured."""

        return {
            "virustotal": bool(self.virustotal_api_key),
            "abuseipdb": bool(self.abuseipdb_api_key),
        }

    def enrich_iocs(
        self,
        iocs: dict[str, list[str]],
    ) -> dict[str, Any]:
        """Enrich extracted URLs, domains, and public IP addresses."""

        max_urls = self._read_integer_setting(
            "THREAT_INTEL_MAX_URLS",
            default=3,
        )

        max_domains = self._read_integer_setting(
            "THREAT_INTEL_MAX_DOMAINS",
            default=3,
        )

        max_ips = self._read_integer_setting(
            "THREAT_INTEL_MAX_IPS",
            default=3,
        )

        urls = self._unique_values(
            iocs.get("urls", [])
        )[:max_urls]

        domains = self._unique_values(
            iocs.get("domains", [])
        )[:max_domains]

        ipv4_addresses = self._unique_values(
            iocs.get("ipv4_addresses", [])
        )[:max_ips]

        results: dict[str, Any] = {
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "provider_status": self.provider_status(),
            "urls": [],
            "domains": [],
            "ip_addresses": [],
            "summary": {},
        }

        for url in urls:
            results["urls"].append(
                self.lookup_virustotal_url(url)
            )

        for domain in domains:
            results["domains"].append(
                self.lookup_virustotal_domain(domain)
            )

        for ip_value in ipv4_addresses:
            results["ip_addresses"].append(
                self.lookup_ip(ip_value)
            )

        results["summary"] = self._build_summary(results)

        return results

    def lookup_virustotal_url(
        self,
        url: str,
    ) -> dict[str, Any]:
        """Retrieve an existing VirusTotal URL reputation report."""

        if not self.virustotal_api_key:
            return self._unavailable_result(
                value=url,
                indicator_type="url",
                provider="VirusTotal",
                reason="VIRUSTOTAL_API_KEY is not configured.",
            )

        url_identifier = self._virustotal_url_identifier(url)
        endpoint = (
            f"{VIRUSTOTAL_BASE_URL}/urls/{url_identifier}"
        )

        response = self._request_json(
            provider="VirusTotal",
            method="GET",
            url=endpoint,
            headers={
                "x-apikey": self.virustotal_api_key,
                "Accept": "application/json",
            },
            cache_key=f"virustotal:url:{url}",
        )

        return self._normalize_virustotal_result(
            value=url,
            indicator_type="url",
            response=response,
        )

    def lookup_virustotal_domain(
        self,
        domain: str,
    ) -> dict[str, Any]:
        """Retrieve a VirusTotal domain reputation report."""

        normalized_domain = domain.lower().strip().strip(".")

        if not self.virustotal_api_key:
            return self._unavailable_result(
                value=normalized_domain,
                indicator_type="domain",
                provider="VirusTotal",
                reason="VIRUSTOTAL_API_KEY is not configured.",
            )

        endpoint = (
            f"{VIRUSTOTAL_BASE_URL}/domains/"
            f"{normalized_domain}"
        )

        response = self._request_json(
            provider="VirusTotal",
            method="GET",
            url=endpoint,
            headers={
                "x-apikey": self.virustotal_api_key,
                "Accept": "application/json",
            },
            cache_key=(
                f"virustotal:domain:{normalized_domain}"
            ),
        )

        return self._normalize_virustotal_result(
            value=normalized_domain,
            indicator_type="domain",
            response=response,
        )

    def lookup_virustotal_ip(
        self,
        ip_value: str,
    ) -> dict[str, Any]:
        """Retrieve a VirusTotal public-IP reputation report."""

        public_status = self._validate_public_ip(ip_value)

        if public_status is not None:
            return public_status

        if not self.virustotal_api_key:
            return self._unavailable_result(
                value=ip_value,
                indicator_type="ip_address",
                provider="VirusTotal",
                reason="VIRUSTOTAL_API_KEY is not configured.",
            )

        endpoint = (
            f"{VIRUSTOTAL_BASE_URL}/ip_addresses/{ip_value}"
        )

        response = self._request_json(
            provider="VirusTotal",
            method="GET",
            url=endpoint,
            headers={
                "x-apikey": self.virustotal_api_key,
                "Accept": "application/json",
            },
            cache_key=f"virustotal:ip:{ip_value}",
        )

        return self._normalize_virustotal_result(
            value=ip_value,
            indicator_type="ip_address",
            response=response,
        )

    def lookup_abuseipdb(
        self,
        ip_value: str,
    ) -> dict[str, Any]:
        """Retrieve public-IP reputation from AbuseIPDB."""

        public_status = self._validate_public_ip(ip_value)

        if public_status is not None:
            public_status["provider"] = "AbuseIPDB"
            return public_status

        if not self.abuseipdb_api_key:
            return self._unavailable_result(
                value=ip_value,
                indicator_type="ip_address",
                provider="AbuseIPDB",
                reason="ABUSEIPDB_API_KEY is not configured.",
            )

        response = self._request_json(
            provider="AbuseIPDB",
            method="GET",
            url=ABUSEIPDB_CHECK_URL,
            headers={
                "Key": self.abuseipdb_api_key,
                "Accept": "application/json",
            },
            params={
                "ipAddress": ip_value,
                "maxAgeInDays": 90,
                "verbose": "",
            },
            cache_key=f"abuseipdb:ip:{ip_value}",
        )

        if not response["success"]:
            return {
                "provider": "AbuseIPDB",
                "type": "ip_address",
                "value": ip_value,
                "status": response["status"],
                "error": response.get("error", ""),
                "cached": response.get("cached", False),
                "malicious": False,
            }

        data = response["data"].get("data", {})

        abuse_score = self._safe_integer(
            data.get("abuseConfidenceScore")
        )

        total_reports = self._safe_integer(
            data.get("totalReports")
        )

        return {
            "provider": "AbuseIPDB",
            "type": "ip_address",
            "value": ip_value,
            "status": "success",
            "cached": response.get("cached", False),
            "abuse_confidence_score": abuse_score,
            "total_reports": total_reports,
            "country_code": data.get("countryCode"),
            "usage_type": data.get("usageType"),
            "isp": data.get("isp"),
            "domain": data.get("domain"),
            "last_reported_at": data.get("lastReportedAt"),
            "is_whitelisted": data.get("isWhitelisted"),
            "malicious": (
                abuse_score >= 25
                or total_reports > 0
            ),
        }

    def lookup_ip(
        self,
        ip_value: str,
    ) -> dict[str, Any]:
        """Look up one IP address with both supported providers."""

        public_status = self._validate_public_ip(ip_value)

        if public_status is not None:
            return {
                "value": ip_value,
                "status": "skipped",
                "reason": public_status["error"],
                "virustotal": public_status,
                "abuseipdb": {
                    **public_status,
                    "provider": "AbuseIPDB",
                },
                "malicious": False,
            }

        virustotal_result = self.lookup_virustotal_ip(
            ip_value
        )

        abuseipdb_result = self.lookup_abuseipdb(
            ip_value
        )

        return {
            "value": ip_value,
            "status": "completed",
            "virustotal": virustotal_result,
            "abuseipdb": abuseipdb_result,
            "malicious": bool(
                virustotal_result.get("malicious")
                or abuseipdb_result.get("malicious")
            ),
        }

    def _request_json(
        self,
        provider: str,
        method: str,
        url: str,
        headers: dict[str, str],
        cache_key: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make a cached JSON request with safe error handling."""

        cached_value = self._read_cache(cache_key)

        if cached_value is not None:
            return {
                "success": True,
                "status": "success",
                "data": cached_value,
                "cached": True,
            }

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                timeout=self.timeout,
            )
        except requests.Timeout:
            return {
                "success": False,
                "status": "timeout",
                "error": (
                    f"{provider} did not respond within "
                    f"{self.timeout} seconds."
                ),
                "cached": False,
            }
        except requests.RequestException as exc:
            return {
                "success": False,
                "status": "connection_error",
                "error": str(exc),
                "cached": False,
            }

        if response.status_code == 404:
            return {
                "success": False,
                "status": "not_found",
                "error": (
                    f"{provider} does not have a report "
                    "for this indicator."
                ),
                "cached": False,
            }

        if response.status_code == 401:
            return {
                "success": False,
                "status": "authentication_error",
                "error": (
                    f"{provider} rejected the API key."
                ),
                "cached": False,
            }

        if response.status_code == 429:
            return {
                "success": False,
                "status": "rate_limited",
                "error": (
                    f"{provider} API rate limit reached."
                ),
                "cached": False,
            }

        if not response.ok:
            return {
                "success": False,
                "status": "http_error",
                "error": (
                    f"{provider} returned HTTP "
                    f"{response.status_code}."
                ),
                "cached": False,
            }

        try:
            response_data = response.json()
        except ValueError:
            return {
                "success": False,
                "status": "invalid_response",
                "error": (
                    f"{provider} returned invalid JSON."
                ),
                "cached": False,
            }

        self._write_cache(
            key=cache_key,
            value=response_data,
        )

        return {
            "success": True,
            "status": "success",
            "data": response_data,
            "cached": False,
        }

    def _normalize_virustotal_result(
        self,
        value: str,
        indicator_type: str,
        response: dict[str, Any],
    ) -> dict[str, Any]:
        """Convert a VirusTotal response to a compact result."""

        if not response["success"]:
            return {
                "provider": "VirusTotal",
                "type": indicator_type,
                "value": value,
                "status": response["status"],
                "error": response.get("error", ""),
                "cached": response.get("cached", False),
                "malicious": False,
            }

        attributes = (
            response["data"]
            .get("data", {})
            .get("attributes", {})
        )

        statistics = attributes.get(
            "last_analysis_stats",
            {},
        )

        malicious_count = self._safe_integer(
            statistics.get("malicious")
        )

        suspicious_count = self._safe_integer(
            statistics.get("suspicious")
        )

        harmless_count = self._safe_integer(
            statistics.get("harmless")
        )

        undetected_count = self._safe_integer(
            statistics.get("undetected")
        )

        return {
            "provider": "VirusTotal",
            "type": indicator_type,
            "value": value,
            "status": "success",
            "cached": response.get("cached", False),
            "malicious_count": malicious_count,
            "suspicious_count": suspicious_count,
            "harmless_count": harmless_count,
            "undetected_count": undetected_count,
            "reputation": attributes.get("reputation"),
            "categories": attributes.get("categories", {}),
            "last_analysis_date": attributes.get(
                "last_analysis_date"
            ),
            "malicious": (
                malicious_count > 0
                or suspicious_count > 0
            ),
        }

    def _read_cache(
        self,
        key: str,
    ) -> dict[str, Any] | None:
        """Return a non-expired cached response."""

        cache = self._load_cache()
        entry = cache.get(key)

        if not isinstance(entry, dict):
            return None

        timestamp_text = entry.get("stored_at")
        value = entry.get("value")

        if not timestamp_text or not isinstance(
            value,
            dict,
        ):
            return None

        try:
            stored_at = datetime.fromisoformat(
                timestamp_text
            )
        except ValueError:
            return None

        if stored_at.tzinfo is None:
            stored_at = stored_at.replace(
                tzinfo=timezone.utc
            )

        expires_at = stored_at + timedelta(
            hours=self.cache_hours
        )

        if datetime.now(timezone.utc) >= expires_at:
            return None

        return value

    def _write_cache(
        self,
        key: str,
        value: dict[str, Any],
    ) -> None:
        """Store a provider response in the local JSON cache."""

        self.cache_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cache = self._load_cache()

        cache[key] = {
            "stored_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "value": value,
        }

        temporary_path = self.cache_path.with_suffix(
            ".tmp"
        )

        temporary_path.write_text(
            json.dumps(
                cache,
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

        temporary_path.replace(self.cache_path)

    def _load_cache(self) -> dict[str, Any]:
        """Load the local cache or return an empty dictionary."""

        if not self.cache_path.exists():
            return {}

        try:
            data = json.loads(
                self.cache_path.read_text(
                    encoding="utf-8"
                )
            )
        except (
            OSError,
            ValueError,
            json.JSONDecodeError,
        ):
            return {}

        if not isinstance(data, dict):
            return {}

        return data

    @staticmethod
    def _build_summary(
        results: dict[str, Any],
    ) -> dict[str, int]:
        """Calculate totals for successful and malicious lookups."""

        all_items: list[dict[str, Any]] = []

        all_items.extend(results.get("urls", []))
        all_items.extend(results.get("domains", []))
        all_items.extend(
            results.get("ip_addresses", [])
        )

        malicious = sum(
            1
            for item in all_items
            if item.get("malicious")
        )

        successful = sum(
            1
            for item in all_items
            if item.get("status")
            in {"success", "completed"}
        )

        errors = sum(
            1
            for item in all_items
            if item.get("status")
            not in {
                "success",
                "completed",
                "skipped",
            }
        )

        return {
            "queried": len(all_items),
            "successful": successful,
            "malicious": malicious,
            "errors": errors,
        }

    @staticmethod
    def _virustotal_url_identifier(
        url: str,
    ) -> str:
        """Create the unpadded URL-safe Base64 identifier used by VT."""

        encoded = base64.urlsafe_b64encode(
            url.encode("utf-8")
        ).decode("ascii")

        return encoded.rstrip("=")

    @staticmethod
    def _validate_public_ip(
        ip_value: str,
    ) -> dict[str, Any] | None:
        """Return a skipped result for invalid or non-public IPs."""

        try:
            parsed_ip = ipaddress.ip_address(ip_value)
        except ValueError:
            return {
                "provider": "",
                "type": "ip_address",
                "value": ip_value,
                "status": "invalid",
                "error": "The value is not a valid IP address.",
                "malicious": False,
            }

        if not parsed_ip.is_global:
            return {
                "provider": "",
                "type": "ip_address",
                "value": ip_value,
                "status": "skipped",
                "error": (
                    "Private, loopback, reserved, or "
                    "otherwise non-public IP address."
                ),
                "malicious": False,
            }

        return None

    @staticmethod
    def _unavailable_result(
        value: str,
        indicator_type: str,
        provider: str,
        reason: str,
    ) -> dict[str, Any]:
        """Create a result for a provider with no configured key."""

        return {
            "provider": provider,
            "type": indicator_type,
            "value": value,
            "status": "not_configured",
            "error": reason,
            "cached": False,
            "malicious": False,
        }

    @staticmethod
    def _unique_values(
        values: list[str],
    ) -> list[str]:
        """Return unique nonempty values while preserving order."""

        return list(
            dict.fromkeys(
                value.strip()
                for value in values
                if value and value.strip()
            )
        )

    @staticmethod
    def _safe_integer(value: Any) -> int:
        """Convert an API value to an integer safely."""

        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _read_integer_setting(
        name: str,
        default: int,
    ) -> int:
        """Read a positive integer environment setting."""

        try:
            value = int(os.getenv(name, str(default)))
        except ValueError:
            return default

        return value if value > 0 else default