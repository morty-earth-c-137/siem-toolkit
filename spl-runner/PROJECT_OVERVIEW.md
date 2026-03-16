# Splunk Client — Project Overview
### Quick reference for the team

---

## What This Project Does

A Python command-line tool that connects to a Splunk Cloud or Enterprise instance
via the REST API to run SPL search queries, validate them before submission,
analyse them for performance issues, and save results as CSV files.

It is designed to be run locally by a single analyst, run as an automated
pipeline in GitLab or GitHub CI/CD, or both at the same time.

---

## Current Version

**v4.3.0** — see `CHANGELOG.md` for full history.

---

## Project Structure

```
splunk_client/               ← project root (can be named anything)
│
├── main.py                  ← CLI entry point — run everything from here
│
├── splunk_client/           ← Python package (all logic lives here)
│   ├── settings.py          ← LOCAL credentials (gitignored, never on runner)
│   ├── config.py            ← Credential resolution + SIEM_TARGET routing
│   ├── auth.py              ← Bearer token header builder
│   ├── client.py            ← HTTPS session wrapper, retry logic
│   ├── search.py            ← Job lifecycle: submit → poll → fetch → CSV
│   ├── validator.py         ← Pre-flight SPL query validation
│   ├── query_optimizer.py   ← Performance analysis against SPL docs
│   ├── schema_validator.py  ← Macro/index/sourcetype/field checks
│   ├── time_range.py        ← --time flag parsing (30m, 2h, 7d, all, etc.)
│   ├── rule_runner.py       ← Batch execution from CSV or Excel rules file
│   ├── spl_knowledge.py     ← Loads SPL 10.2 reference docs at startup
│   ├── models.py            ← Dataclasses for API response objects
│   ├── exceptions.py        ← Custom exception hierarchy
│   └── logger.py            ← Structured console logging setup
│
├── spl_docs/                ← 194 Splunk 10.2 SPL reference docs (bundled)
│   └── *.md                 ← Used by spl_knowledge, validator, optimizer
│
├── config/
│   └── schema.yaml          ← Your environment schema: macros, indexes,
│                               sourcetypes, datamodels, field definitions
│
├── docs/
│   ├── HOW_TO_GUIDE.md      ← Plain-English setup guide (non-developer)
│   ├── OPSEC_LOCAL.md       ← Local terminal security practices
│   ├── OPSEC_CICD.md        ← GitLab/GitHub CI/CD variable setup + multi-SIEM
│   └── QUERY_EXAMPLES.md    ← SPL query examples from simple to advanced
│
├── .gitlab-ci.yml           ← GitLab pipeline (validate + search stages)
├── .github/workflows/
│   └── splunk_search.yml    ← GitHub Actions workflow
│
├── rules.csv                ← Example rules file (Splunk export format)
├── .env                     ← Runtime toggles — SSL, timeouts, auth mode
├── .env.example             ← Template with all options documented
├── .gitignore               ← Blocks settings.py, .env overrides, results
├── pyproject.toml           ← Build config (v4.3.0)
└── requirements.txt         ← Python dependencies
```

---

## How to Run It

```bash
cd wherever/the/project/is

# Run a single query
python main.py --query "search index=main | head 10"

# Run with a time range
python main.py --query "search index=main | head 10" --time 2h

# Analyse a query without submitting (no Splunk needed)
python main.py --optimize "| tstats count from datamodel=Endpoint.Processes by Processes.dest"

# Analyse + schema check
python main.py --optimize "| tstats ..." --validate-schema

# Run all rules in a CSV file
python main.py --rules rules.csv

# Run rules, validate but don't submit
python main.py --rules rules.csv --dry-run --validate-schema

# Run rules against a specific SIEM target
SIEM_TARGET=staging python main.py --rules rules.csv --time 7d
```

---

## CLI Reference

| Flag | Mode | Description |
|------|------|-------------|
| `--query SPL` | Submit | Validate and run a single SPL query |
| `--rules FILE` | Submit | Run all rules from a .csv or .xlsx file |
| `--optimize SPL` | Analyse | Validate and analyse — no submission |
| `--time RANGE` | All | Time window: `10m`, `2h`, `7d`, `3mon`, `1y`, `@d`, `@mon`, `@y`, `7d@d`, `all` |
| `--validate-schema` | All | Check macros, indexes, sourcetypes against schema.yaml |
| `--dry-run` | Submit | Validate only — do not submit to Splunk |
| `--debug` | All | Verbose logging |
| `--results DIR` | All | Override CSV output folder |

---

## Rules File Format

Columns must match the Splunk saved-search export format:

| title | search |
|-------|--------|
| Failed Logins | `search index=main EventCode=4625 \| stats count by user` |
| Advanced IP Scanner | `\| tstats \`security_content_summariesonly\` count ...` |

Export from Splunk Web: Settings → Searches, reports, and alerts → Export

Supported file types: `.csv` (preferred), `.xlsx`

---

## Credential and Config Hierarchy

```
Priority (highest wins):

1. OS environment variables / CI/CD injected variables
   SPLUNK_HOST, SPLUNK_TOKEN, SIEM_TARGET, etc.

2. .env file (local only, gitignored)
   Controls toggles: SPLUNK_VERIFY_SSL, timeouts, AUTH_MODE

3. settings.py (local only, gitignored)
   Default fallback values for local development
```

In CI/CD: `settings.py` and `.env` do not exist on the runner.
All values come from CI/CD variables with `AUTH_MODE=env`.

---

## Multi-SIEM Support

Set `SIEM_TARGET` to route to a named credential pair:

```bash
SIEM_TARGET=prod     →  uses SPLUNK_HOST_PROD  + SPLUNK_TOKEN_PROD
SIEM_TARGET=staging  →  uses SPLUNK_HOST_STAGING + SPLUNK_TOKEN_STAGING
SIEM_TARGET=lab      →  uses SPLUNK_HOST_LAB   + SPLUNK_TOKEN_LAB
(not set)            →  uses SPLUNK_HOST + SPLUNK_TOKEN
```

In GitLab: set `SIEM_TARGET` as a CI/CD variable per job or environment.
In GitHub: pass it as a workflow input or repository variable.

---

## Schema Configuration (config/schema.yaml)

Controls what `--validate-schema` checks. All sections can be toggled:

| Section | What it validates |
|---------|------------------|
| `macros` | Backtick macros exist in your environment |
| `indexes` | `index=` references are known |
| `sourcetypes` | `sourcetype=` references are known |
| `datamodels` | `datamodel=` references in tstats are valid |
| `sourcetype_fields` | Fields used match the sourcetype's known field list |

To add a new macro, index, or sourcetype — edit `config/schema.yaml`.
To add field definitions for a new sourcetype — add a block under `sourcetype_fields`.

---

## Pipeline Overview (GitLab)

```
Every push (any branch):
  validate_rules  →  --dry-run --validate-schema  (no Splunk needed)

On main/master:
  search_default  →  runs against default SIEM  (auto)
  search_prod     →  SIEM_TARGET=prod            (manual trigger or tag)
  search_staging  →  SIEM_TARGET=staging         (manual trigger)
  search_lab      →  SIEM_TARGET=lab             (manual trigger)
```

Results saved as pipeline artifacts, auto-expired after 7–30 days.

---

## Where to Extend This Project

### Add a new SIEM target
1. Add `SPLUNK_HOST_<TARGET>` and `SPLUNK_TOKEN_<TARGET>` to GitLab/GitHub variables
2. Add a job to `.gitlab-ci.yml` with `SIEM_TARGET: "<target>"`
3. No code changes required

### Add new macros / indexes / sourcetypes to validation
Edit `config/schema.yaml` — add entries under the relevant section.
No code changes required.

### Add field definitions for a new sourcetype
Add a block under `sourcetype_fields` in `config/schema.yaml`:
```yaml
my_sourcetype:
  notes: "Description"
  fields:
    - field_one
    - field_two
```

### Add a new validation check
Edit `splunk_client/validator.py` — add a check function following the
same pattern as `_check_bracket_balance`. Call it from `validate_query`.

### Add a new optimiser rule
Edit `splunk_client/query_optimizer.py` — add a `_check_*` function and
call it from `optimize_query`. Reference the relevant SPL doc in `spl_docs/`.

### Add a new CLI flag
Edit `parse_args` in `main.py` — add an `add_argument` call and wire the
value through to the appropriate function.

### Support a new file format in rule_runner
Edit `_load_rules_dataframe` equivalent in `splunk_client/rule_runner.py` —
add a new extension branch in the `if ext ==` block.

### Update SPL reference docs
Replace files in `spl_docs/` with newer Splunk documentation exports.
`spl_knowledge.py` picks them up automatically at startup.

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP client for Splunk REST API |
| `python-dotenv` | Reads `.env` file |
| `pandas` | Reads `.csv` and `.xlsx` rules files |
| `openpyxl` | Excel engine for pandas |
| `pyyaml` | Parses `config/schema.yaml` |

Install: `pip install -r requirements.txt`

---

## Key Files Not to Commit

| File | Why |
|------|-----|
| `splunk_client/settings.py` | Contains local credentials |
| `.env` | May contain credential overrides |
| `search_results/` | Contains query results (potentially sensitive data) |

All three are in `.gitignore`.

---

## Documents

| Document | Audience | Purpose |
|----------|----------|---------|
| `PROJECT_OVERVIEW.md` | Team | This file — capabilities, structure, where to extend |
| `README.md` | Developers | Technical setup and API reference |
| `docs/HOW_TO_GUIDE.md` | Non-developers | Step-by-step Mac setup guide |
| `docs/OPSEC_LOCAL.md` | All users | Local terminal security practices |
| `docs/OPSEC_CICD.md` | DevOps / CI | GitLab/GitHub variable setup and multi-SIEM |
| `docs/QUERY_EXAMPLES.md` | Analysts | SPL query examples from simple to advanced |
| `CHANGELOG.md` | All | Version history and change log |
