"""
client.py
---------
Core HTTPS session wrapper for the Splunk REST API.

Features:
  - Bearer token authentication on every request
  - TLS/HTTPS only — no HTTP fallback
  - Retry with exponential backoff on transient 5xx/429 errors
  - Structured error messages for all failure modes

References:
  https://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTprolog
"""

import logging
from typing import Any, Dict, Optional

import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from splunk_client.auth import build_auth_headers
from splunk_client.config import SplunkConfig
from splunk_client.exceptions import SplunkAuthError, SplunkConnectionError

logger = logging.getLogger(__name__)

_RETRY_STRATEGY = Retry(
    total=3,
    backoff_factor=1.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"],
    raise_on_status=False,
)


class SplunkClient:
    """
    HTTPS client for the Splunk Cloud REST API.

    Use as a context manager:
        with SplunkClient(config) as client:
            response = client.post("/services/search/jobs", data={...})
    """

    def __init__(self, config: SplunkConfig) -> None:
        self._config = config
        self._session: Optional[requests.Session] = None
        if not config.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(build_auth_headers(self._config))
        session.verify = self._config.verify_ssl
        adapter = HTTPAdapter(max_retries=_RETRY_STRATEGY)
        session.mount("https://", adapter)
        return session

    def __enter__(self) -> "SplunkClient":
        self._session = self._build_session()
        return self

    def __exit__(self, *_: Any) -> None:
        if self._session:
            self._session.close()

    def _url(self, endpoint: str) -> str:
        return f"{self._config.base_url}{endpoint}"

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = self._url(endpoint)
        try:
            response = self._session.post(url, data=data, timeout=self._config.timeout)
        except requests.exceptions.SSLError as exc:
            raise SplunkConnectionError(
                f"SSL certificate verification failed connecting to {url}.\n"
                "  If using localhost or a self-signed certificate, add this to your .env file:\n"
                "  SPLUNK_VERIFY_SSL=false\n"
                "  Or run: export SPLUNK_VERIFY_SSL=false in your terminal.\n"
                "  Only disable on trusted internal networks — never on production."
            ) from exc
        except requests.exceptions.ConnectionError as exc:
            raise SplunkConnectionError(
                f"Cannot reach Splunk at {url}. "
                "Check SPLUNK_HOST and your network connection."
            ) from exc
        except requests.exceptions.Timeout:
            raise SplunkConnectionError(
                f"Request to {url} timed out after {self._config.timeout}s."
            )
        return self._handle_response(response, url)

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = self._url(endpoint)
        try:
            response = self._session.get(url, params=params, timeout=self._config.timeout)
        except requests.exceptions.SSLError as exc:
            raise SplunkConnectionError(
                f"SSL certificate verification failed connecting to {url}.\n"
                "  If using localhost or a self-signed certificate, add this to your .env file:\n"
                "  SPLUNK_VERIFY_SSL=false\n"
                "  Or run: export SPLUNK_VERIFY_SSL=false in your terminal.\n"
                "  Only disable on trusted internal networks — never on production."
            ) from exc
        except requests.exceptions.ConnectionError as exc:
            raise SplunkConnectionError(f"Connection error on GET {url}: {exc}") from exc
        except requests.exceptions.Timeout:
            raise SplunkConnectionError(f"GET {url} timed out after {self._config.timeout}s.")
        return self._handle_response(response, url)

    @staticmethod
    def _handle_response(response: requests.Response, url: str) -> Dict[str, Any]:
        if response.status_code in (401, 403):
            raise SplunkAuthError(
                f"Authentication failed (HTTP {response.status_code}). "
                "Check your SPLUNK_TOKEN in settings.py — it may be expired or invalid."
            )
        if not response.ok:
            raise SplunkConnectionError(
                f"Splunk returned HTTP {response.status_code} for {url}. "
                f"Body: {response.text[:500]}"
            )
        try:
            return response.json()
        except ValueError as exc:
            raise SplunkConnectionError(
                f"Non-JSON response from {url}: {response.text[:300]}"
            ) from exc
