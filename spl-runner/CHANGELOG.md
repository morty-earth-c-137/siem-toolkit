# Changelog

All notable changes to this project are documented here.
Versioning follows [Semantic Versioning](https://semver.org): MAJOR.MINOR.PATCH

---

## [1.0.0] — Initial Release

### Added
- `splunk_client/settings.py` — primary credential store (SPLUNK_HOST, SPLUNK_TOKEN, SPLUNK_PORT as Python variables)
- `splunk_client/config.py` — configuration loader merging settings.py with optional .env overrides
- `splunk_client/auth.py` — Bearer token authentication header builder
- `splunk_client/client.py` — HTTPS session wrapper with retry/backoff
- `splunk_client/validator.py` — pre-flight SPL query validation with forbidden command blocking and time range enforcement (earliest=-30m, latest=now)
- `splunk_client/search.py` — full search job lifecycle: submit, poll, paginated fetch, CSV export
- `splunk_client/rule_runner.py` — batch Excel rule execution with per-rule error isolation and summary report
- `splunk_client/models.py` — typed dataclasses for all API response objects
- `splunk_client/exceptions.py` — custom exception hierarchy
- `splunk_client/logger.py` — structured console logging
- `main.py` — CLI entry point with path-agnostic bootstrap (works in any directory, any folder name, any path depth)
- `pyproject.toml` — flat layout package config compatible with Python 3.10+ and pip install -e .
- `.env.example` — runtime toggles template (SSL, timeouts, results dir, auth mode)
- `.gitignore` — blocks settings.py, .env, search_results/, venvs, and build artifacts
- `docs/HOW_TO_GUIDE.md` — plain-English Mac setup and usage guide
- `docs/OPSEC_LOCAL.md` — local security practices for Mac terminal use
- `docs/OPSEC_CICD.md` — GitLab and GitHub CI/CD credential management guide

### Security
- Credentials stored as Python variables in settings.py, never hardcoded in logic modules
- settings.py blocked in .gitignore by default
- Bearer token never logged or printed
- All connections HTTPS only, SSL verification on by default
- Time range hard-locked to past 30 minutes on all queries
- Forbidden SPL command list blocks destructive operations

### Known Behaviour
- `pip install -e .` requires being run from inside the project folder
- `python main.py` works from the project folder regardless of its name or location

---

## [2.0.0] — Validator Expansion + SPL Knowledge Base

### Added
- `splunk_client/spl_knowledge.py` — loads all 159 SPL commands from the
  bundled Splunk 10.2 reference docs at startup. Provides VALID_COMMANDS,
  GENERATING_CMDS, TRANSFORMING_CMDS, EXPENSIVE_CMDS, and per-command doc text.
  Validator and optimizer both draw from this knowledge base.

- `splunk_client/query_optimizer.py` — 9 doc-grounded optimisation checks
  activated by `--optimize`. Covers: expensive commands (transaction, join, map,
  append), tstats opportunity, dedup vs stats, head/sort order, missing index
  filter, leading wildcards, unknown commands, transaction without time limits,
  and fields command placement. Recommendations include severity, finding, reason
  (with SPL doc citation), and concrete action.

- `splunk_client/schema_validator.py` — validates macros, indexes, sourcetypes,
  datamodels, and sourcetype-to-field combos against config/schema.yaml.
  Activated by `--validate-schema`. Warnings only — never blocks submission.

- `config/schema.yaml` — YAML environment schema. Pre-populated with common
  Splunk ES macros, CIM data models, common sourcetypes, indexes, and
  CIM Endpoint.Processes field definitions. Extend with your environment values.

- `spl_docs/` — all 194 Splunk SPL 10.2 reference documents bundled with the
  project. Used by spl_knowledge.py, validator, and optimizer.

### New CLI flags
- `--optimize`         : analyse query and print optimisation recommendations
- `--validate-schema`  : check query against config/schema.yaml
- `--dry-run`          : validate + analyse without submitting to Splunk
  All three flags can be combined. `--dry-run` always prevents submission.

### Changed
- `splunk_client/validator.py` — now draws the valid command list directly from
  the SPL docs via spl_knowledge.py. Unknown pipeline commands are warned, not
  hard-blocked (may be custom app commands). Source prefixes expanded to include
  all generating commands from the docs.
- `requirements.txt` — added pyyaml>=6.0.1 for schema.yaml parsing.

### Fixed
- Path bootstrap in main.py correctly resolves `splunk_client/` from `__file__`
  regardless of OS path, folder name, spaces, or nesting depth.
- Flat package layout (no src/) — pip install -e . works on Python 3.11+
  regardless of spaces in the parent directory path.
- settings.py as primary credential store — credentials are Python variables,
  not .env dependencies. .env scoped to runtime toggles only.
- config.py logs the source of every resolved value — no silent overrides from
  shell exports (e.g. .zshrc SPLUNK_HOST=...).

---

## [4.0.0] — Audit and Stabilisation

### Fixed
- `.env` file was truncated (43 bytes) by a failed test backup/restore.
  Restored to full content with all documented options.
- Stray directory `{splunk_client,docs,tests}` left by a bash expansion
  artefact — removed.
- `spl_knowledge.py` was missing the `_BUILTIN_COMMANDS` hardcoded fallback.
  Without it, the validator flagged all SPL commands (stats, eval, etc.) as
  unknown when `spl_docs/` was absent. Added full 159-command fallback list
  so the validator works correctly with or without the docs folder.
- `spl_docs/` confirmed present (194 docs) and is NOT removed from the project.
  It is actively used by `spl_knowledge.py`, `validator.py`, and
  `query_optimizer.py` at runtime.

### Clarified
- `.env` ships as a ready-to-use file with safe defaults. No copying required.
  Credentials live in `splunk_client/settings.py`, not `.env`.
  `.env` controls runtime toggles only: SSL, timeouts, auth mode, results dir.
- To fix the SSL self-signed certificate error on localhost, open `.env` and
  uncomment the line: `SPLUNK_VERIFY_SSL=false`
- Hidden files (`.env`, `.env.example`, `.gitignore`) are confirmed in the zip.
  They do not appear in `ls */*` because that command only shows subdirectory
  contents, not root-level or hidden files. Use `ls -la` to see them all.

---

## [4.1.0] — Full Audit Pass

### Fixed

#### query_optimizer.py
- Removed unused imports `GENERATING_CMDS` and `get_command_doc` from
  `spl_knowledge`. Both were imported but never referenced in the module body.

#### search.py
- Removed unused imports `DEFAULT_EARLIEST` and `DEFAULT_LATEST` from
  `time_range`. These were made redundant when the `TimeRange` object was
  introduced to carry time range values end-to-end. Direct constant usage
  was replaced by `tr.earliest` / `tr.latest`.

#### validator.py
- Removed unused direct import of `VALID_COMMANDS` from `spl_knowledge`.
  Command lookup is handled via `is_valid_command()` wrapper — the raw set
  was never accessed directly in this module.
- Removed leftover `import re as _re` alias inside `_find_unknown_commands`.
  The module already imports `re` at the top level; the alias was a residue
  from an earlier edit.

#### __init__.py
- Added missing public exports for modules introduced in v2/v4:
    `parse_time_range`, `TimeRange`  (from `time_range`)
    `optimize_query`                 (from `query_optimizer`)
    `validate_schema`                (from `schema_validator`)
  These are now importable directly from `splunk_client` and listed in `__all__`.

#### rule_runner.py (standalone mode)
- Added `--time` flag to the `__main__` block so standalone invocation
  (`python -m splunk_client.rule_runner --file rules.xlsx`) supports time
  range control, consistent with `main.py`.
- Added `allow_abbrev=False` to the standalone `ArgumentParser` to match
  the same safeguard applied to `main.py`.

### Verified (audit findings, not bugs)
- All mutable variables flagged by static analysis are function-local.
  They reset on every call and cannot bleed between modules. Confirmed safe.
- `allow_abbrev=False` in `main.py` correctly rejects `--rule` with exit
  code 2. It does not silently route to `--rules`. Confirmed working.
- No circular imports. No constant drift. No module-level shared state.
- End-to-end flow (validate → optimize → schema → time_range → config)
  passes cleanly from the public `__init__` API.

---

## [4.1.0] — CLI Redesign + Full Audit Pass

### Breaking change — CLI modes
`--optimize` is now a proper mode that accepts a query directly, not a boolean flag.

Before (broken):
  python main.py --query '...' --optimize   # --optimize had no standalone use
  python main.py --optimize '...'           # FAILED — argparse error

After (fixed):
  python main.py --optimize '...'           # works — validate + analyse, no submission
  python main.py --query '...'              # submit query
  python main.py --rules file.xlsx          # submit rules file

### Added
- `--optimize SPL` as a first-class mode alongside `--query` and `--rules`.
  Validates the query, runs the optimizer, prints recommendations, and exits.
  Does not load credentials or contact Splunk.
  Combine with `--validate-schema` for full pre-flight analysis.

### Fixed (code quality — found by full audit)
- `query_optimizer.py`: removed unused imports `GENERATING_CMDS`, `get_command_doc`
- `search.py`: removed unused imports `DEFAULT_EARLIEST`, `DEFAULT_LATEST`
- `validator.py`: removed unused `VALID_COMMANDS` import and leftover `_re` alias
- `__init__.py`: added missing public exports `parse_time_range`, `TimeRange`,
  `optimize_query`, `validate_schema`
- `rule_runner.py` standalone: added `--time` flag and `allow_abbrev=False`
  so standalone invocation is consistent with `main.py`

### Verified clean
- No circular imports
- No module-level shared mutable state
- No constant drift across modules
- All function signatures match every call site
- End-to-end flow passes from public `__init__` API

---

## [4.2.0] — Time Range Expansion

### Added
- `--time all` and `--time alltime` — searches all indexed data with no time
  boundary. Splunk receives `earliest=0` (Unix epoch). Use with care on large
  deployments — no time filter means every index bucket is scanned.
- `--time 3mon`, `--time 6mon` — months already worked but were not documented
  in the help text or error messages. Now explicitly called out.
- `--time 1y`, `--time 2y` — years already worked, now explicitly documented.
- `--time @y` — snap to start of this year, now documented.

### Complete --time reference
  10m        past 10 minutes
  2h         past 2 hours
  7d         past 7 days
  3mon       past 3 months
  1y         past 1 year
  @d         start of today to now
  @w         start of this week to now
  @mon       start of this month to now
  @y         start of this year to now
  7d@d       7 days ago snapped to day boundary
  all        all indexed data (earliest=0, no time boundary)

---

## [4.2.0] — CSV Support + Splunk Export Column Headers

### Changed
- `rule_runner.py` — column headers updated to match Splunk saved-search
  export format:
    - `rule name` → `title`
    - `query`     → `search`
  Files exported directly from Splunk Web (Settings > Searches, reports, and
  alerts > Export) will now load without any manual column renaming.

- `rule_runner.py` — CSV file support added alongside existing .xlsx support.
  The loader detects the file extension and reads accordingly:
    - `.csv`  → `pandas.read_csv`
    - `.xlsx` → `pandas.read_excel` (openpyxl)
  Any other extension is rejected with a clear error message.

- `main.py` — `--rules` analysis block updated to use the same format-aware
  loader and new column names.

### Error messages
- Wrong column names now explicitly state the expected headers:
  "Ensure the file has a 'title' column and a 'search' column
   (Splunk saved-search export headers)."
- Unsupported file type gives a clear message:
  "Unsupported file type: '.xyz'. Provide a .csv or .xlsx file."

### Time range expansion (also in this release)
- `--time all` / `--time alltime` — all indexed data (earliest=0)
- `--time 3mon`, `--time 1y`, `--time @y` — now documented in help text

---

## [4.3.0] — GitLab/GitHub CI/CD + Multi-SIEM + Project Overview

### Added

#### Pipeline files
- `.gitlab-ci.yml` — two-stage pipeline (validate + search).
  Stage 1 `validate` runs on every push with no credentials needed.
  Stage 2 `search` runs on protected branches with four named jobs:
  `search_default`, `search_prod`, `search_staging`, `search_lab`.
  Results saved as pipeline artifacts, auto-expired after 7–30 days.

- `.github/workflows/splunk_search.yml` — GitHub Actions workflow with
  the same two-job structure. Supports manual `workflow_dispatch` inputs
  for `siem_target`, `time_range`, `rules_file`, and `dry_run`.

#### Multi-SIEM support
- `SIEM_TARGET` environment variable added to `config.py`.
  When set, selects a named credential pair:
    `SIEM_TARGET=prod`     →  `SPLUNK_HOST_PROD` + `SPLUNK_TOKEN_PROD`
    `SIEM_TARGET=staging`  →  `SPLUNK_HOST_STAGING` + `SPLUNK_TOKEN_STAGING`
    `SIEM_TARGET=lab`      →  `SPLUNK_HOST_LAB` + `SPLUNK_TOKEN_LAB`
  Falls back to `SPLUNK_HOST` / `SPLUNK_TOKEN` if target-specific vars absent.
  No code changes needed to add a new SIEM target — just add CI/CD variables.

#### New files
- `rules.csv` — example rules file with correct Splunk export headers
  (`title`, `search`) ready to use with `--rules rules.csv`.
- `PROJECT_OVERVIEW.md` — team quick reference: capabilities, structure,
  CLI reference, credential hierarchy, schema config, pipeline overview,
  and a full "where to extend" guide for adding new modules or checks.

#### Updated
- `settings.py` — documented CI/CD usage and multi-SIEM local configuration.
- `docs/OPSEC_CICD.md` — fully rewritten with actual pipeline files,
  complete variable tables, multi-SIEM routing explanation, and
  per-platform setup instructions for GitLab and GitHub.

### CI/CD variable reference

Single SIEM:
  SPLUNK_HOST        Masked + Protected
  SPLUNK_TOKEN       Masked + Protected

Multi-SIEM:
  SPLUNK_HOST_PROD      SPLUNK_TOKEN_PROD       Masked + Protected
  SPLUNK_HOST_STAGING   SPLUNK_TOKEN_STAGING    Masked + Protected
  SPLUNK_HOST_LAB       SPLUNK_TOKEN_LAB        Masked + Protected

Optional:
  SIEM_TARGET        Which named target to use
  SPLUNK_VERIFY_SSL  true / false
  TIME_RANGE         Default time window for pipeline runs
  RULES_FILE         Path to rules file in the repo

---

## [4.3.1] — GitHub Actions Working Directory Fix

### Fixed
- `.github/workflows/splunk_search.yml` — added `defaults.run.working-directory: spl-runner`
  to every job. Without this, the runner executes from the repo root (`siem-toolkit/`)
  and cannot find `requirements.txt`, `main.py`, or `rules.csv` which all live inside
  the `spl-runner/` subfolder.
- `cache-dependency-path` updated to `spl-runner/requirements.txt` so pip caching
  resolves correctly from the repo root.
- `path:` in the upload-artifact step updated to `spl-runner/search_results/`
  (relative to repo root, which is where GitHub Actions resolves artifact paths).
- `paths:` trigger filters added — workflow only fires when files inside `spl-runner/`
  change, preventing unnecessary runs when other toolkit tools are updated.

---

## [4.3.2] — Security Fix: No Credential Logging + Settings Commit Fix

### Fixed

#### Issue 1 — settings.py missing after GitHub clone
`settings.py` was listed in `.gitignore` in earlier versions, meaning users
who cloned the repo from GitHub had no settings file and the tool crashed
immediately on `python main.py`. The file was already unblocked in v4.3.x
but this release explicitly documents and confirms the fix:
- `settings.py` is committed with placeholder values only — safe to push
- Real credentials are set locally after cloning, or via CI/CD variables
- The `.gitignore` comment explains this clearly

#### Issue 2 — Credentials printed to console (security)
Earlier versions of `config.py` logged `SPLUNK_HOST=hostname` and
`SPLUNK_TOKEN=eyJr... (masked)` at INFO level on every run. Even a
"masked" partial token is irresponsible to print on a shared terminal
or in a CI/CD log that might be stored or forwarded.

Fix:
- All credential resolution (host, token) is now at DEBUG level only
- DEBUG is off by default — only enabled with `--debug` flag
- The single INFO-level startup line now reads:
    "Splunk client starting (credentials loaded — not shown in logs)"
- No credential value, partial value, or variable name appears in
  INFO or WARNING output under any circumstances
- Verified: running the tool with a real host/token produces zero
  credential data in console output at default log level

---

## [4.3.3] — Validator: SPL Comment Block Support

### Added — splunk_client/validator.py

`strip_comments()` — a new pre-processing step that runs before all other
validation checks, implementing the full Splunk comment specification from:
Search Manual 9.2 — Add comments to searches.

Comment syntax per Splunk docs:
  - Three backticks open a comment:  ```
  - The next three backticks close it, regardless of content or newlines
  - Single/double backticks inside a comment are part of the comment
  - Backslash does NOT escape — triple-backtick always closes
  - Comments can span multiple lines

What strip_comments() does:
  1. Scans the query for opening triple-backtick sequences
  2. Finds the matching closing triple-backtick
  3. Raises SplunkQueryValidationError if a comment is opened but never closed
  4. Replaces each comment block with a single space to preserve token boundaries
  5. Returns the cleaned query for all subsequent validation checks

Effect on validation:
  - Brackets/parens inside comments no longer confuse the bracket balance check
  - Time modifiers inside comments are not stripped as false positives
  - Commands inside comments are not flagged as unknown
  - Unclosed comments (``` with no matching close) are caught and rejected
    with a clear error showing the position of the unclosed opener

Behaviour per Splunk docs for comment before a generating command:
  - Splunk itself rejects this at runtime (documented limitation)
  - The validator passes it through — it is syntactically valid SPL
  - Splunk will return an error when the job is submitted

Single/double backtick macros (e.g. `drop_dm_object_name(Processes)`)
are unaffected — they use one or two backticks, not three.

---

## [4.3.4] — GitHub Actions Version Updates

### Fixed
- `.github/workflows/splunk_search.yml` — updated all action versions to
  current latest to resolve Node.js 20 deprecation warnings:
    actions/checkout@v4      -> actions/checkout@v6
    actions/setup-python@v5  -> actions/setup-python@v6
    actions/upload-artifact@v4 -> actions/upload-artifact@v6

  v3 of upload-artifact was deprecated January 30 2025 and causes workflow
  failures. v4/v5 run on Node.js 20 which is now also deprecated. v6 runs
  on Node.js 24 and is the current stable version.

---

## [4.3.5] — Validator: Macro-as-First-Token Support

### Fixed — splunk_client/validator.py
A query starting with a bare backtick macro and nothing before it was
incorrectly rejected by the source command check:

  `windows_logging_event_streamer`                  ← was REJECTED
  `windows_logging_event_streamer` | stats count    ← was REJECTED

The validator only accepted macros preceded by a pipe:
  |`windows_logging_event_streamer`                 ← was accepted
  | `windows_logging_event_streamer`                ← was accepted

Fix: added `"\`"` to VALID_SOURCE_PREFIXES so a bare backtick macro
is recognised as a valid pipeline-opening token. This matches Splunk
behaviour — a macro can be a generating command and the sole entry
point of a query with no pipe prefix required.

All four forms now pass:
  `macro`
  `macro` | stats count by host
  |`macro`
  | `macro` | stats count by host

---

## [4.3.6] — Schema Enforcement + Validation Summary CSV + Field Check Fixes

### Fixed — schema_validator.py (_check_fields)
Two false positives in the sourcetype/datamodel field check:

1. Quoted string values (e.g. process_name="cmd.exe") were contributing
   'exe' as an extracted field name. Fixed by stripping all quoted string
   values before field extraction in _strip_quoted_values().

2. Datamodel reference parts (e.g. Endpoint.Processes in datamodel=...)
   were being extracted as field names. Fixed by collecting all parts of
   datamodel= references and excluding them from the field check set.

### Added — --enforce-schema flag
When passed, any schema warning blocks submission to Splunk and exits
with a clear error listing each failing item.

  python main.py --query '...' --enforce-schema
  python main.py --rules rules.csv --enforce-schema
  python main.py --optimize '...' --enforce-schema

Behaviour:
  --validate-schema alone  -> warns, never blocks
  --enforce-schema         -> warns AND blocks on any warning
  --enforce-schema implies --validate-schema (no need to pass both)

### Added -- --validation-summary flag
When passed with --rules, writes a clean CSV after the run with one
row per rule.

  python main.py --rules rules.csv --validation-summary
  python main.py --rules rules.csv --enforce-schema --validation-summary

Output file: search_results/_validation_summary_YYYYMMDD_HHMMSS.csv

Columns:
  title        — rule name from the rules file (title column)
  status       — PASS or FAIL
  failed_items — pipe-separated list of warnings/errors (empty on PASS)

Example rows:
  "Detect Brute Force","PASS",""
  "Registry Autostart","FAIL","[field] Field 'fake_field' not in schema.yaml"
  "Macro Detection","FAIL","[macro] `unknown_macro` not listed in schema.yaml"
