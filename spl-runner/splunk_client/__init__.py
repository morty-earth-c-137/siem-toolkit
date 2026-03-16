"""
splunk_client
-------------
Splunk Cloud REST API client package.

Quick imports:
  from splunk_client import run_search, run_rules_from_excel, load_config
"""

from splunk_client.config import load_config, SplunkConfig
from splunk_client.search import run_search
from splunk_client.rule_runner import run_rules_from_excel
from splunk_client.exceptions import (
    SplunkClientError,
    SplunkAuthError,
    SplunkConnectionError,
    SplunkTimeoutError,
    SplunkQueryValidationError,
    SplunkJobError,
    SplunkResultsError,
    SplunkConfigError,
)
from splunk_client.time_range import parse_time_range, TimeRange
from splunk_client.query_optimizer import optimize_query
from splunk_client.schema_validator import validate_schema

__all__ = [
    "load_config", "SplunkConfig", "run_search", "run_rules_from_excel",
    "parse_time_range", "TimeRange",
    "optimize_query", "validate_schema",
    "SplunkClientError", "SplunkAuthError", "SplunkConnectionError",
    "SplunkTimeoutError", "SplunkQueryValidationError",
    "SplunkJobError", "SplunkResultsError", "SplunkConfigError",
]
