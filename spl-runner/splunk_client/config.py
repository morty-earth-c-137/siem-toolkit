"""
config.py
---------
Loads runtime configuration by combining two sources in order of priority:

  1. settings.py  — core credentials (SPLUNK_HOST, SPLUNK_TOKEN, SPLUNK_PORT).
                    Set these directly in that file. No .env required for
                    basic usage.

  2. OS environment variables / .env file — optional overrides. A value here
                    always wins over settings.py. Useful for CI/CD pipelines,
                    or if you have SPLUNK_HOST already exported in your shell
                    (e.g. via .zshrc).

Priority (highest wins):
  OS environment variables  >  .env file  >  settings.py

IMPORTANT — shell exports take priority:
  If you have  export SPLUNK_HOST=...  in your .zshrc or .bashrc, that
  value will be used instead of whatever is in settings.py. The tool logs
  exactly which source each value came from at startup so there are no
  silent overrides.

AUTH_MODE (.env or OS env):
  dotenv  — load .env file for overrides (default, local use)
  env     — OS environment variables only (CI/CD pipelines)

SIEM_TARGET (optional, OS env or CI/CD variable):
  When set, selects a named credential pair instead of the defaults.
  The target name is appended (uppercased) to the variable names:

    SIEM_TARGET=prod     -> reads SPLUNK_HOST_PROD  / SPLUNK_TOKEN_PROD
    SIEM_TARGET=staging  -> reads SPLUNK_HOST_STAGING / SPLUNK_TOKEN_STAGING
    SIEM_TARGET=lab      -> reads SPLUNK_HOST_LAB   / SPLUNK_TOKEN_LAB

  Falls back to SPLUNK_HOST / SPLUNK_TOKEN if the target-specific
  variables are not set.

  In GitLab, set SIEM_TARGET as a CI/CD variable per environment or job.
  In GitHub Actions, set it as a repository variable or workflow input.
"""

import os
import logging
from dataclasses import dataclass

from dotenv import load_dotenv

from splunk_client.exceptions import SplunkConfigError

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Step 1: Import credential defaults from settings.py
# ---------------------------------------------------------------------------
try:
    from splunk_client.settings import SPLUNK_HOST  as _DEFAULT_HOST
    from splunk_client.settings import SPLUNK_TOKEN as _DEFAULT_TOKEN
    from splunk_client.settings import SPLUNK_PORT  as _DEFAULT_PORT
except ImportError as exc:
    raise SplunkConfigError(
        "settings.py not found inside the splunk_client folder.\n"
        f"Original error: {exc}"
    ) from exc

# ---------------------------------------------------------------------------
# Step 2: Resolve AUTH_MODE and optionally load .env overrides
# .env values are written into os.environ so the resolution logic below
# handles everything through a single os.getenv() path.
# ---------------------------------------------------------------------------
_AUTH_MODE = os.getenv("AUTH_MODE", "dotenv").strip().lower()

if _AUTH_MODE == "dotenv":
    _loaded = load_dotenv(override=False)   # env vars already in shell take priority
    if _loaded:
        logger.debug("AUTH_MODE=dotenv — .env file loaded (shell exports still take priority).")
    else:
        logger.debug("AUTH_MODE=dotenv — no .env file found. Using settings.py defaults.")
elif _AUTH_MODE == "env":
    logger.debug("AUTH_MODE=env — OS environment variables only.")
else:
    raise SplunkConfigError(
        f"Unknown AUTH_MODE value: '{_AUTH_MODE}'.\n"
        "Valid options:\n"
        "  AUTH_MODE=dotenv  — use .env file + shell exports (default)\n"
        "  AUTH_MODE=env     — OS environment variables only (CI/CD)"
    )


# ---------------------------------------------------------------------------
# Config dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SplunkConfig:
    """Immutable configuration object. Frozen to prevent accidental mutation."""
    host: str
    token: str
    port: int
    verify_ssl: bool
    timeout: int
    job_poll_interval: int
    job_max_wait: int
    results_dir: str

    @property
    def base_url(self) -> str:
        return f"https://{self.host}:{self.port}"


# ---------------------------------------------------------------------------
# Config loader
# ---------------------------------------------------------------------------

def load_config() -> SplunkConfig:
    """
    Builds and validates a SplunkConfig by merging settings.py values
    with any overrides from the shell environment or .env file.

    Credential values (host, token) are NEVER written to any log output
    at any level. Only non-sensitive info (port, timeouts, SSL state)
    is logged at DEBUG level for troubleshooting.

    Raises:
        SplunkConfigError: If SPLUNK_HOST or SPLUNK_TOKEN are still
                           placeholder values or empty.

    Returns:
        SplunkConfig: Fully resolved, validated configuration object.
    """
    logger.info("Splunk client starting (credentials loaded — not shown in logs)")

    # --- SIEM_TARGET: select named credential pair if set ---
    siem_target = os.getenv("SIEM_TARGET", "").strip().upper()
    if siem_target:
        host_key  = f"SPLUNK_HOST_{siem_target}"
        token_key = f"SPLUNK_TOKEN_{siem_target}"
        logger.debug("  SIEM_TARGET=%-20s -> %s / %s",
                     siem_target, host_key, token_key)
        host  = _resolve_str(host_key,  _DEFAULT_HOST,  host_key)
        token = _resolve_str(token_key, _DEFAULT_TOKEN, token_key)
    else:
        host  = _resolve_str("SPLUNK_HOST",  _DEFAULT_HOST,  "SPLUNK_HOST")
        token = _resolve_str("SPLUNK_TOKEN", _DEFAULT_TOKEN, "SPLUNK_TOKEN")
    port  = _resolve_int("SPLUNK_PORT",  _DEFAULT_PORT,  "SPLUNK_PORT")

    # Validate that placeholders have been replaced
    if host in {"your-organisation.splunkcloud.com", ""}:
        raise SplunkConfigError(
            "SPLUNK_HOST has not been set.\n"
            "Open splunk_client/settings.py and replace the placeholder, e.g.:\n"
            '  SPLUNK_HOST = "mycompany.splunkcloud.com"\n'
            "Or export it in your shell:  export SPLUNK_HOST=mycompany.splunkcloud.com"
        )
    if token in {"paste-your-token-here", ""}:
        raise SplunkConfigError(
            "SPLUNK_TOKEN has not been set.\n"
            "Open splunk_client/settings.py and replace the placeholder.\n"
            "Generate a token in Splunk Web: Settings > Tokens > New Token.\n"
            "Or export it in your shell:  export SPLUNK_TOKEN=your-token"
        )

    # Optional toggles — default values used if not set anywhere
    verify_ssl_raw = os.getenv("SPLUNK_VERIFY_SSL", "true").strip().lower()
    verify_ssl = verify_ssl_raw not in ("false", "0", "no")
    if not verify_ssl:
        logger.warning(
            "SSL verification DISABLED (SPLUNK_VERIFY_SSL=false). "
            "Only use this in a controlled dev environment, never in production."
        )

    timeout       = _resolve_int("SPLUNK_TIMEOUT",          30,  "SPLUNK_TIMEOUT")
    poll_interval = _resolve_int("SPLUNK_JOB_POLL_INTERVAL",  3, "SPLUNK_JOB_POLL_INTERVAL")
    max_wait      = _resolve_int("SPLUNK_JOB_MAX_WAIT",     120, "SPLUNK_JOB_MAX_WAIT")
    results_dir   = os.getenv("RESULTS_DIR", "search_results").strip()

    return SplunkConfig(
        host=host,
        token=token,
        port=port,
        verify_ssl=verify_ssl,
        timeout=timeout,
        job_poll_interval=poll_interval,
        job_max_wait=max_wait,
        results_dir=results_dir,
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _resolve_str(env_key: str, default: str, label: str) -> str:
    """
    Resolves a string config value and logs ONLY the source — never the value.

    Credential values (host, token) are never written to any log output
    regardless of log level. Only the source (env var / settings.py) is logged.
    """
    env_val = os.getenv(env_key, "").strip()
    if env_val:
        logger.debug("  %-28s <- OS environment ($%s)", label, env_key)
        return env_val
    logger.debug("  %-28s <- settings.py", label)
    return default.strip()


def _resolve_int(env_key: str, default: int, label: str) -> int:
    """
    Resolves an integer config value and logs the source.
    Integer values (ports, timeouts) are non-sensitive and safe to log.
    """
    env_val = os.getenv(env_key, "").strip()
    if env_val:
        try:
            val = int(env_val)
        except ValueError:
            raise SplunkConfigError(
                f"{env_key} must be a valid integer, got: '{env_val}'"
            )
        logger.debug("  %-28s = %s  <- OS environment ($%s)", label, val, env_key)
        return val
    logger.debug("  %-28s = %s  <- default", label, default)
    return default
