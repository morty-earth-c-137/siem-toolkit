"""
settings.py
-----------
Default credential and connection settings for LOCAL development only.

IN CI/CD (GitLab / GitHub):
  This file is listed in .gitignore and will NOT exist on the runner.
  All credentials are supplied via CI/CD variables (GitLab CI/CD Variables
  or GitHub Secrets) and read by config.py through os.getenv().
  Set AUTH_MODE=env in your pipeline to skip .env and settings.py entirely.

IN LOCAL DEVELOPMENT:
  Set SPLUNK_HOST and SPLUNK_TOKEN below before running the tool.
  This file stays on your machine only — never committed to Git.

MULTIPLE SIEM TARGETS:
  To switch between SIEM environments without editing this file, export
  the appropriate variables in your shell or CI/CD pipeline:

    export SIEM_TARGET=prod          # selects SPLUNK_HOST_PROD / SPLUNK_TOKEN_PROD
    export SIEM_TARGET=staging       # selects SPLUNK_HOST_STAGING / SPLUNK_TOKEN_STAGING
    export SIEM_TARGET=lab           # selects SPLUNK_HOST_LAB / SPLUNK_TOKEN_LAB

  If SIEM_TARGET is not set, the values below (SPLUNK_HOST / SPLUNK_TOKEN)
  are used as the default target.

  See config/schema.yaml for per-environment field and macro definitions.
  See docs/OPSEC_CICD.md for CI/CD variable setup instructions.
"""

# =============================================================================
# DEFAULT TARGET — set these for local use
# =============================================================================

# Your Splunk Cloud hostname (the part after https:// in your browser)
# Example: "mycompany.splunkcloud.com"
SPLUNK_HOST: str = "your-organisation.splunkcloud.com"  # <-- SET THIS

# Your Splunk Bearer token
# Generate: Splunk Web -> Settings -> Tokens -> New Token
SPLUNK_TOKEN: str = "paste-your-token-here"             # <-- SET THIS

# Splunk REST API port — always 8089 for Splunk Cloud
SPLUNK_PORT: int = 8089

# =============================================================================
# NAMED SIEM TARGETS — for multi-SIEM environments
# Uncomment and fill in the targets you use.
# In CI/CD these are set as pipeline variables, not here.
# =============================================================================

# Production SIEM
# SPLUNK_HOST_PROD:    str = "prod.splunkcloud.com"
# SPLUNK_TOKEN_PROD:   str = "paste-prod-token-here"

# Staging / QA SIEM
# SPLUNK_HOST_STAGING: str = "staging.splunkcloud.com"
# SPLUNK_TOKEN_STAGING: str = "paste-staging-token-here"

# Lab / Dev SIEM
# SPLUNK_HOST_LAB:     str = "lab.splunkcloud.com"
# SPLUNK_TOKEN_LAB:    str = "paste-lab-token-here"
