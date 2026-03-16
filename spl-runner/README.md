# Splunk Cloud API Client

A Python client for executing SPL search queries against Splunk Cloud via the REST API.
Supports single queries, Excel-driven batch execution, enforced time windows, pre-flight validation, and CSV output.

---

## Project Structure

```
splunk_client/
├── splunk_client/
│   ├── __init__.py        # Package exports
│   ├── auth.py            # Bearer token authentication
│   ├── client.py          # HTTP session wrapper with retry logic
│   ├── config.py          # Environment variable loading and validation
│   ├── exceptions.py      # Custom exception hierarchy
│   ├── logger.py          # Structured console logging setup
│   ├── models.py          # Response dataclasses
│   ├── rule_runner.py     # Excel batch rule execution module
│   ├── search.py          # Search job lifecycle (submit → poll → fetch → CSV)
│   └── validator.py       # Pre-flight SPL query validation
├── docs/
│   ├── HOW_TO_GUIDE.md    # Step-by-step guide for non-developers (Mac)
│   ├── OPSEC_LOCAL.md     # Security guide for local terminal testing
│   └── OPSEC_CICD.md      # Security guide for GitLab and GitHub CI/CD
├── tests/                 # Test directory
├── main.py                # CLI entry point
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Quick Start

```bash
# 1. Create and activate virtual environment
python3 -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure credentials
cp .env.example .env
# Edit .env with your SPLUNK_HOST and SPLUNK_TOKEN

# 4. Run a search
python main.py --query "search index=main | head 10"

# 5. Run from Excel rules file
python main.py --rules rules.xlsx
```

---

## Configuration

All configuration is via environment variables. Copy `.env.example` to `.env` for local use.

| Variable | Required | Default | Description |
|---|---|---|---|
| `SPLUNK_HOST` | ✓ | — | Splunk Cloud hostname |
| `SPLUNK_TOKEN` | ✓ | — | Splunk Bearer token |
| `SPLUNK_PORT` | | `8089` | REST API management port |
| `SPLUNK_VERIFY_SSL` | | `true` | SSL certificate verification |
| `SPLUNK_TIMEOUT` | | `30` | HTTP timeout in seconds |
| `SPLUNK_JOB_POLL_INTERVAL` | | `3` | Seconds between job polls |
| `SPLUNK_JOB_MAX_WAIT` | | `120` | Max job wait time in seconds |
| `RESULTS_DIR` | | `search_results` | CSV output directory |

---

## Time Range Policy

All queries are hard-locked to `earliest=-30m latest=now`. Inline time modifiers in
query strings are stripped and logged as warnings. This cannot be overridden at runtime.

---

## Excel Rules File Format

The rules file must be a `.xlsx` file with these exact column headers in row 1:

| rule name | query |
|---|---|
| Failed Logins | search index=main sourcetype=auth failed |
| Error Rate | search index=main log_level=ERROR \| stats count by host |

---

## Documentation

| Document | Audience |
|---|---|
| `docs/HOW_TO_GUIDE.md` | Non-developers — full setup walkthrough for Mac |
| `docs/OPSEC_LOCAL.md` | Anyone running the tool locally — security practices |
| `docs/OPSEC_CICD.md` | Developers — GitLab and GitHub CI/CD credential management |

---

## Dependencies

- `requests` — HTTP client
- `python-dotenv` — `.env` file loading
- `pandas` + `openpyxl` — Excel file reading

---

## References

- [Splunk REST API Reference](https://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTprolog)
- [Splunk Search Jobs](https://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTsearch#search.2Fjobs)
- [Splunk Token Authentication](https://docs.splunk.com/Documentation/Splunk/latest/Security/UseAuthTokens)
