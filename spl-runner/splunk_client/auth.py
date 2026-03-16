"""
auth.py
-------
Builds authentication headers for all Splunk REST API requests.

Uses Splunk Bearer Token authentication — the recommended method for
Splunk Cloud. Tokens are provisioned in Splunk Web under:
  Settings > Tokens > New Token

References:
  https://docs.splunk.com/Documentation/Splunk/latest/Security/UseAuthTokens
"""

import logging
from typing import Dict

from splunk_client.config import SplunkConfig

logger = logging.getLogger(__name__)


def build_auth_headers(config: SplunkConfig) -> Dict[str, str]:
    """
    Constructs HTTP headers for authenticated Splunk API requests.

    The token is sourced from config (never logged or printed).

    Args:
        config (SplunkConfig): Validated configuration object.

    Returns:
        Dict[str, str]: Headers dict ready to pass to requests.Session.
    """
    logger.debug("Building auth headers.")
    return {
        "Authorization": f"Bearer {config.token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
