"""
main.py
-------
CLI entry point for the Splunk Cloud API client.

Three modes — pick exactly one:
  --query SPL    Validate and submit a single SPL query. Saves results to CSV.
  --rules FILE   Validate and submit all rules from an Excel .xlsx file.
  --optimize SPL Validate and analyse a query. Prints recommendations.
                 Does NOT submit to Splunk.

Supporting flags (combine with any mode):
  --validate-schema   Check query against config/schema.yaml (macros, indexes,
                      sourcetypes, datamodels, fields). Warnings only.
  --time RANGE        Time window sent to Splunk. Default: 30m (past 30 minutes).
                      Examples: 10m, 2h, 7d, @d, @w, @mon, 7d@d
  --dry-run           Validate and analyse but do NOT submit. Works with
                      --query and --rules.
  --debug             Enable verbose DEBUG logging.
  --results DIR       Override the CSV output directory.

Usage examples:
  python main.py --query "search index=main | head 10"
  python main.py --query "search index=main | head 10" --time 2h
  python main.py --query "search index=main | head 10" --dry-run
  python main.py --optimize "| tstats count from datamodel=Endpoint.Processes by Processes.dest"
  python main.py --optimize "search index=main | join user [search index=main]"
  python main.py --optimize "search index=main" --validate-schema
  python main.py --rules detections.xlsx
  python main.py --rules detections.xlsx --time 7d
  python main.py --rules detections.xlsx --dry-run
  python main.py --rules detections.xlsx --validate-schema
"""

import argparse
import logging
import os
import sys

# ---------------------------------------------------------------------------
# Path bootstrap — resolves splunk_client/ relative to main.py itself
# so imports work regardless of where the tool is installed or invoked from.
# ---------------------------------------------------------------------------
_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)
# ---------------------------------------------------------------------------

from splunk_client.config import load_config
from splunk_client.exceptions import SplunkClientError, SplunkConfigError
from splunk_client.logger import setup_logging
from splunk_client.rule_runner import run_rules_from_excel
from splunk_client.search import run_search
from splunk_client.query_optimizer import optimize_query
from splunk_client.schema_validator import validate_schema, write_validation_summary
from splunk_client.time_range import parse_time_range
from splunk_client.validator import validate_query
from splunk_client.exceptions import SplunkQueryValidationError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="splunk_client",
        description="Splunk Cloud API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
        epilog="""
Modes (pick one):
  --query SPL        Submit a query to Splunk and save results to CSV
  --rules FILE       Submit all rules from an Excel file
  --optimize SPL     Analyse a query and print recommendations (no submission)

Examples:
  python main.py --query "search index=main | head 10"
  python main.py --query "search index=main | head 10" --time 2h
  python main.py --query "search index=main | head 10" --dry-run --validate-schema
  python main.py --optimize "| tstats count from datamodel=Endpoint.Processes by Processes.dest"
  python main.py --optimize "search index=main | join user [search index=main]" --validate-schema
  python main.py --rules detections.xlsx --time 7d
  python main.py --rules detections.xlsx --dry-run --validate-schema
        """,
    )

    # --- Three modes — exactly one required ---
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--query",
        metavar="SPL",
        help="SPL query to validate and submit to Splunk. Results saved to CSV.",
    )
    mode.add_argument(
        "--rules",
        metavar="FILE",
        help="Path to a rules file (.csv or .xlsx). Columns must be 'title' and 'search' (Splunk export format).",
    )
    mode.add_argument(
        "--optimize",
        metavar="SPL",
        help=(
            "SPL query to validate and analyse. Prints optimisation recommendations "
            "based on the SPL 10.2 docs. Does NOT submit to Splunk. "
            "Combine with --validate-schema for full pre-flight analysis."
        ),
    )

    # --- Supporting flags ---
    parser.add_argument(
        "--validate-schema",
        action="store_true",
        default=False,
        dest="validate_schema",
        help=(
            "Check the query against config/schema.yaml — validates macros, "
            "indexes, sourcetypes, datamodels, and field combinations. "
            "Warnings only, does not block submission."
        ),
    )
    parser.add_argument(
        "--enforce-schema",
        action="store_true",
        default=False,
        dest="enforce_schema",
        help=(
            "Enforce schema checks — any schema warning blocks submission "
            "to Splunk and exits with an error. Implies --validate-schema."
        ),
    )
    parser.add_argument(
        "--validation-summary",
        action="store_true",
        default=False,
        dest="validation_summary",
        help=(
            "Write a validation summary CSV after running --rules. "
            "Columns: title, status (PASS/FAIL), failed_items. "
            "Saved to the results directory alongside search CSVs."
        ),
    )
    parser.add_argument(
        "--time",
        metavar="RANGE",
        default=None,
        dest="time_range",
        help=(
            "Time window for the search. Default: 30m (past 30 minutes). "
            "Examples: 10m, 2h, 7d, 2w, @d (start of today), "
            "@w (start of week), @mon (start of month), 7d@d (7 days snapped to day)."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        dest="dry_run",
        help=(
            "Validate and analyse but do NOT submit to Splunk. "
            "Applies to --query and --rules modes. "
            "(--optimize never submits, so --dry-run is implied.)"
        ),
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable verbose DEBUG logging.",
    )
    parser.add_argument(
        "--results",
        metavar="DIR",
        default=None,
        help="Override the results output directory (default: search_results).",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(level=logging.DEBUG if args.debug else logging.INFO)
    logger = logging.getLogger(__name__)

    # --- Load config ---
    # Skipped for --optimize (never contacts Splunk)
    # Skipped for --dry-run (validates only, never submits)
    # Required for --query and --rules without --dry-run
    config = None
    needs_config = (args.query or args.rules) and not getattr(args, 'dry_run', False)
    if needs_config:
        try:
            config = load_config()
        except SplunkConfigError as exc:
            logger.error("Configuration error: %s", exc)
            print(
                "\n[ERROR] Credentials not configured.\n"
                "  Open splunk_client/settings.py and set:\n"
                "    SPLUNK_HOST  = 'your-org.splunkcloud.com'\n"
                "    SPLUNK_TOKEN = 'your-bearer-token'\n"
            )
            sys.exit(1)

        if args.results:
            os.environ["RESULTS_DIR"] = args.results
            config = load_config()

    # --- Parse time range ---
    try:
        time_range = parse_time_range(getattr(args, "time_range", None))
    except SplunkQueryValidationError as exc:
        logger.error("Invalid --time value: %s", exc)
        sys.exit(1)

    # =========================================================================
    # MODE: --optimize SPL
    # Validate + analyse. Never submits.
    # =========================================================================
    if args.optimize:
        query = args.optimize
        print()
        try:
            clean = validate_query(query)
        except SplunkQueryValidationError as exc:
            print(f"  [VALIDATION FAILED]\n  {exc}\n")
            sys.exit(1)

        print("  [VALIDATION] Query passed.\n")

        opt = optimize_query(clean)
        opt.print_report()

        if args.validate_schema or args.enforce_schema:
            sr = validate_schema(clean, enforce=args.enforce_schema)
            sr.print_report()

        sys.exit(0)

    # =========================================================================
    # MODE: --query SPL
    # Validate, optionally analyse, then submit (unless --dry-run).
    # =========================================================================
    if args.query:
        query = args.query

        # Pre-flight analysis
        if args.validate_schema or args.dry_run:
            try:
                clean = validate_query(query)
            except SplunkQueryValidationError as exc:
                logger.error("Validation failed: %s", exc)
                sys.exit(1)

            if args.validate_schema or args.enforce_schema:
                sr = validate_schema(clean, enforce=args.enforce_schema)
                sr.print_report()

        if args.dry_run:
            print("  [DRY RUN] Query validated. Not submitted to Splunk.\n")
            sys.exit(0)

        try:
            csv_path = run_search(query=query, config=config, time_range=time_range)
            print(f"\n  Results saved to: {csv_path}\n")
        except SplunkClientError as exc:
            logger.error("Search failed: %s", exc)
            sys.exit(1)
        except Exception as exc:
            logger.error("Unexpected error: %s", exc, exc_info=args.debug)
            sys.exit(1)

    # =========================================================================
    # MODE: --rules FILE
    # Validate + optionally analyse all rules, then submit (unless --dry-run).
    # =========================================================================
    elif args.rules:
        # Per-rule analysis if --validate-schema / --enforce-schema / --dry-run requested
        preflight_summary_rows = []
        if args.validate_schema or args.enforce_schema or args.dry_run or args.validation_summary:
            import pandas as pd
            try:
                ext = os.path.splitext(args.rules)[1].lower()
                if ext == ".csv":
                    df = pd.read_csv(args.rules, dtype=str)
                elif ext in (".xlsx", ".xls"):
                    df = pd.read_excel(args.rules, engine="openpyxl", dtype=str)
                else:
                    logger.error("Unsupported file type '%s'. Use .csv or .xlsx.", ext)
                    sys.exit(1)
                df.columns = [str(c).strip().lower() for c in df.columns]
                if "search" not in df.columns:
                    logger.error(
                        "Rules file has no 'search' column. "
                        "Expected columns: 'title' and 'search' (Splunk export format)."
                    )
                    sys.exit(1)
                print()
                for idx, row in df.iterrows():
                    rule_name = str(row.get("title", f"rule_{idx+1}")).strip()
                    query_str = str(row.get("search", "")).strip()
                    if not query_str or query_str.lower() in ("nan", "none"):
                        continue
                    print(f"  {'='*56}")
                    print(f"  Rule: {rule_name}")
                    print(f"  {'='*56}")
                    row_status = "PASS"
                    row_failed = ""
                    try:
                        clean = validate_query(query_str)
                        if args.validate_schema or args.enforce_schema:
                            sr = validate_schema(clean, enforce=args.enforce_schema)
                            sr.print_report()
                            if sr.has_warnings:
                                row_status = "FAIL"
                                row_failed = sr.warning_summary()
                    except SplunkQueryValidationError as exc:
                        row_status = "FAIL"
                        row_failed = str(exc).splitlines()[0]
                        print(f"  [VALIDATION FAILED] {exc}\n")
                    preflight_summary_rows.append({
                        "title":        rule_name,
                        "status":       row_status,
                        "failed_items": row_failed,
                    })
            except Exception as exc:
                logger.error("Could not read rules file: %s", exc)
                sys.exit(1)

        if args.dry_run:
            print("  [DRY RUN] Rules validated. Not submitted to Splunk.\n")
            # Write validation summary CSV before exiting if requested
            if args.validation_summary and preflight_summary_rows:
                results_dir = (
                    config.results_dir if config
                    else os.path.join(os.path.dirname(os.path.abspath(args.rules)), "search_results")
                )
                os.makedirs(results_dir, exist_ok=True)
                summary_path = write_validation_summary(preflight_summary_rows, results_dir)
                print(f"  Validation summary: {summary_path}\n")
            sys.exit(0)

        try:
            run_rules_from_excel(
                excel_path=args.rules,
                config=config,
                time_range=time_range,
                enforce_schema=args.enforce_schema,
                write_summary=args.validation_summary,
            )
        except (FileNotFoundError, ValueError) as exc:
            logger.error("Rule runner failed: %s", exc)
            sys.exit(1)
        except Exception as exc:
            logger.error("Unexpected error: %s", exc, exc_info=args.debug)
            sys.exit(1)


if __name__ == "__main__":
    main()
