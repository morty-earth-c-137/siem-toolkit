"""
rule_runner.py
--------------
Batch search execution from an Excel rules file.

Excel file format (two required columns):
  - "title"  : rule name / label  (Splunk export header)
  - "search" : SPL search query   (Splunk export header)

Each rule is validated and executed independently. Failed rules are
skipped and execution continues. A summary is printed and saved as CSV.

Callable standalone:
  python -m splunk_client.rule_runner --file rules.xlsx
  python -m splunk_client.rule_runner --file rules.csv

Or imported:
  from splunk_client.rule_runner import run_rules_from_excel
"""

import argparse
import csv
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import pandas as pd

from splunk_client.config import SplunkConfig, load_config
from splunk_client.exceptions import SplunkClientError, SplunkQueryValidationError
from splunk_client.logger import setup_logging
from splunk_client.search import run_search
from splunk_client.schema_validator import validate_schema, write_validation_summary
from splunk_client.validator import validate_query as _validate_query_for_schema
from splunk_client.time_range import TimeRange, parse_time_range

logger = logging.getLogger(__name__)

# Column headers matching Splunk export format
COLUMN_RULE_NAME = "title"
COLUMN_QUERY     = "search"


@dataclass
class RuleResult:
    rule_name: str
    query: str
    status: str = "PENDING"
    csv_path: str = ""
    error: str = ""


def run_rules_from_excel(
    excel_path: str,
    config: SplunkConfig,
    time_range: Optional[TimeRange] = None,
    enforce_schema: bool = False,
    write_summary: bool = False,
) -> List[RuleResult]:
    """
    Reads an Excel rules file and executes each rule as a Splunk search.

    Args:
        excel_path (str): Path to the rules file (.csv or .xlsx).
        config (SplunkConfig): Validated runtime configuration.
        time_range (TimeRange, optional): Time range for all rules.
            Defaults to past 30 minutes if not provided.

    Returns:
        List[RuleResult]: One result record per rule.
    """
    excel_path = os.path.abspath(excel_path)
    if not os.path.isfile(excel_path):
        raise FileNotFoundError(
            f"Rules file not found: {excel_path}\n"
            "Provide a valid path to a .csv or .xlsx file."
        )

    logger.info("Loading rules from: %s", excel_path)

    ext = os.path.splitext(excel_path)[1].lower()
    try:
        if ext == ".csv":
            df = pd.read_csv(excel_path, dtype=str)
        elif ext in (".xlsx", ".xls"):
            df = pd.read_excel(excel_path, engine="openpyxl", dtype=str)
        else:
            raise ValueError(
                f"Unsupported file type: '{ext}'. "
                "Provide a .csv or .xlsx file."
            )
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"Could not read '{excel_path}': {exc}") from exc

    df.columns = [str(c).strip().lower() for c in df.columns]

    missing = [c for c in (COLUMN_RULE_NAME, COLUMN_QUERY) if c not in df.columns]
    if missing:
        raise ValueError(
            f"Rules file is missing column(s): {missing}\n"
            f"Found: {list(df.columns)}\n"
            "Ensure the file has a 'title' column and a 'search' column "
            "(these are the default Splunk saved-search export headers)."
        )

    df = df.dropna(subset=[COLUMN_RULE_NAME, COLUMN_QUERY], how="all")
    total = len(df)

    if total == 0:
        logger.warning("No rules found in the Excel file.")
        return []

    tr = time_range or parse_time_range(None)
    logger.info("Found %d rule(s) to execute.", total)
    logger.info("Time range for all rules: %s  (earliest=%s  latest=%s)",
                tr.description, tr.earliest, tr.latest)
    results: List[RuleResult] = []
    summary_rows: List[dict] = []

    for idx, row in df.iterrows():
        rule_name = str(row.get(COLUMN_RULE_NAME, "")).strip()
        query     = str(row.get(COLUMN_QUERY, "")).strip()

        if not rule_name or rule_name.lower() in ("nan", "none"):
            rule_name = f"rule_{idx + 1}"
        if not query or query.lower() in ("nan", "none"):
            logger.warning("[%s] Empty query — skipping.", rule_name)
            results.append(RuleResult(rule_name=rule_name, query="", status="SKIPPED", error="Empty query."))
            continue

        logger.info("--- Rule %d/%d: '%s' ---", len(results) + 1, total, rule_name)
        result = RuleResult(rule_name=rule_name, query=query)
        schema_warning_summary = ""

        # Schema validation — runs before submission when enforce or summary requested
        if enforce_schema or write_summary:
            try:
                _clean = _validate_query_for_schema(query)
                _sr    = validate_schema(_clean, enforce=enforce_schema)
                schema_warning_summary = _sr.warning_summary()
                if _sr.has_warnings:
                    _sr.print_report()
            except SplunkQueryValidationError as _schema_exc:
                result.status = "FAILED_SCHEMA"
                result.error  = str(_schema_exc).splitlines()[0]
                logger.error("[%s] SCHEMA ENFORCEMENT FAILED: %s", rule_name, result.error)
                summary_rows.append({
                    "title": rule_name,
                    "status": "FAIL",
                    "failed_items": result.error,
                })
                results.append(result)
                continue

        try:
            csv_path = run_search(query=query, config=config, rule_name=rule_name, time_range=tr)
            result.status   = "PASSED"
            result.csv_path = csv_path or ""
            logger.info("[%s] PASSED -> %s", rule_name, csv_path)
        except SplunkQueryValidationError as exc:
            result.status = "FAILED_VALIDATION"
            result.error  = str(exc)
            logger.error("[%s] VALIDATION FAILED: %s", rule_name, exc)
        except SplunkClientError as exc:
            result.status = "FAILED_SEARCH"
            result.error  = str(exc)
            logger.error("[%s] SEARCH FAILED: %s", rule_name, exc)
        except Exception as exc:
            result.status = "FAILED_SEARCH"
            result.error  = f"Unexpected error: {exc}"
            logger.error("[%s] UNEXPECTED ERROR: %s", rule_name, exc, exc_info=True)

        # Add row to validation summary
        is_pass = result.status == "PASSED"
        summary_rows.append({
            "title": rule_name,
            "status": "PASS" if is_pass else "FAIL",
            "failed_items": "" if is_pass else " | ".join(
                filter(None, [schema_warning_summary, result.error])
            ),
        })
        results.append(result)

    _print_summary(results)
    _save_summary_csv(results, config.results_dir)
    if write_summary and summary_rows:
        summary_path = write_validation_summary(summary_rows, config.results_dir)
        print(f"\n  Validation summary: {summary_path}\n")
    return results


def _print_summary(results: List[RuleResult]) -> None:
    passed  = sum(1 for r in results if r.status == "PASSED")
    failed  = sum(1 for r in results if r.status.startswith("FAILED"))
    skipped = sum(1 for r in results if r.status == "SKIPPED")

    print("\n" + "=" * 60)
    print("  RULE RUNNER SUMMARY")
    print("=" * 60)
    print(f"  Total   : {len(results)}")
    print(f"  Passed  : {passed}")
    print(f"  Failed  : {failed}")
    print(f"  Skipped : {skipped}")
    print("=" * 60)
    for r in results:
        icon = {"PASSED": "✓", "SKIPPED": "–"}.get(r.status, "✗")
        print(f"  {icon} [{r.status:<20}] {r.rule_name}")
        if r.error:
            print(f"      └─ {r.error[:120]}")
        if r.csv_path:
            print(f"      └─ {r.csv_path}")
    print("=" * 60 + "\n")


def _save_summary_csv(results: List[RuleResult], results_dir: str) -> None:
    os.makedirs(results_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(results_dir, f"_summary_{timestamp}.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["rule_name", "status", "csv_path", "error", "query"])
        writer.writeheader()
        for r in results:
            writer.writerow({"rule_name": r.rule_name, "status": r.status,
                             "csv_path": r.csv_path, "error": r.error, "query": r.query})
    logger.info("Summary saved: %s", path)
    print(f"  Summary: {path}\n")


if __name__ == "__main__":
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Run Splunk searches from an Excel rules file.",
        allow_abbrev=False,
    )
    parser.add_argument("--file", required=True, metavar="PATH",
                        help=(
                            "Path to a rules file (.csv or .xlsx). "
                            "Required columns: 'title' (rule name) and 'search' (SPL query). "
                            "These match Splunk saved-search export headers."
                        ))
    parser.add_argument("--time", metavar="RANGE", default=None, dest="time_range",
                        help="Time range for all rules (e.g. 10m, 2h, 7d, @d, @mon). Default: 30m.")
    args = parser.parse_args()
    try:
        from splunk_client.time_range import parse_time_range
        cfg = load_config()
        tr  = parse_time_range(args.time_range)
        run_rules_from_excel(excel_path=args.file, config=cfg, time_range=tr)
    except Exception as e:
        logger.error("%s", e)
        sys.exit(1)
