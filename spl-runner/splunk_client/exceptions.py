"""
exceptions.py
-------------
Custom exception hierarchy for the Splunk Cloud API client.

All exceptions inherit from SplunkClientError to allow broad or targeted
exception handling by callers.
"""


class SplunkClientError(Exception):
    """Base exception for all Splunk client errors."""


class SplunkAuthError(SplunkClientError):
    """Raised when authentication fails (invalid token, expired session)."""


class SplunkConnectionError(SplunkClientError):
    """Raised when the HTTP connection to Splunk Cloud fails."""


class SplunkTimeoutError(SplunkClientError):
    """Raised when a search job exceeds the configured polling timeout."""


class SplunkQueryValidationError(SplunkClientError):
    """Raised when a query fails pre-flight validation."""


class SplunkJobError(SplunkClientError):
    """Raised when Splunk reports an error status on a search job."""


class SplunkResultsError(SplunkClientError):
    """Raised when results cannot be retrieved or parsed."""


class SplunkConfigError(SplunkClientError):
    """Raised when required configuration values are missing or invalid."""
