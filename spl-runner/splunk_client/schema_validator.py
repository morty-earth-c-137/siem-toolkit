"""
schema_validator.py
-------------------
Validates a SPL query against the environment schema defined in
config/schema.yaml.

Schema validation is OPTIONAL and only runs when --validate-schema is
passed as a CLI flag.

By default it warns only and never blocks submission.
With --enforce-schema it raises SplunkQueryValidationError on any warning,
blocking submission to Splunk.

What it checks (each section can be toggled in schema.yaml):
  macros      : backtick macros in the query exist in schema.yaml
  indexes     : index= references exist in schema.yaml
  sourcetypes : sourcetype= references exist in schema.yaml
  datamodels  : datamodel= references in tstats exist in schema.yaml
  fields      : fields used with a known sourcetype match that
                sourcetype's defined fields

All issues are returned as a list of SchemaWarning objects so the
caller can decide how to display or enforce them.
"""

import csv
import os
import re
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

_HERE         = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_HERE)
_SCHEMA_PATH  = os.path.join(_PROJECT_ROOT, "config", "schema.yaml")


@dataclass
class SchemaWarning:
    category: str
    message: str
    suggestion: str = ""


@dataclass
class SchemaValidationResult:
    warnings: List[SchemaWarning] = field(default_factory=list)
    schema_loaded: bool = False
    schema_path: str = ""

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    def print_report(self) -> None:
        if not self.schema_loaded:
            print("\n  [SCHEMA] config/schema.yaml not found — schema checks skipped.\n")
            return
        if not self.warnings:
            print("\n  [SCHEMA] All schema checks passed. \u2713\n")
            return
        by_category: dict = {}
        for w in self.warnings:
            by_category.setdefault(w.category, []).append(w)
        print(f"\n  [SCHEMA] {len(self.warnings)} warning(s):")
        print("  " + "=" * 58)
        for category, warns in sorted(by_category.items()):
            print(f"\n  {category.upper()}:")
            print("  " + "-" * 58)
            for w in warns:
                print(f"  - {w.message}")
                if w.suggestion:
                    print(f"    -> {w.suggestion}")
        print("  " + "=" * 58 + "\n")

    def warning_summary(self) -> str:
        if not self.warnings:
            return ""
        return " | ".join(
            f"[{w.category}] {w.message}" for w in self.warnings
        )


def validate_schema(query: str, enforce: bool = False) -> SchemaValidationResult:
    """
    Validates a SPL query against config/schema.yaml.

    Args:
        query   (str):  SPL query (already stripped of comments).
        enforce (bool): When True, raises SplunkQueryValidationError if any
                        warning is produced — blocks submission to Splunk.
                        When False (default), warnings are collected and
                        returned but never block submission.

    Returns:
        SchemaValidationResult

    Raises:
        SplunkQueryValidationError: Only when enforce=True and warnings exist.
    """
    from splunk_client.exceptions import SplunkQueryValidationError

    result = SchemaValidationResult()
    schema = _load_schema()

    if schema is None:
        logger.debug("schema.yaml not found at %s — skipping.", _SCHEMA_PATH)
        return result

    result.schema_loaded = True
    result.schema_path   = _SCHEMA_PATH

    _check_macros(query, schema, result)
    _check_indexes(query, schema, result)
    _check_sourcetypes(query, schema, result)
    _check_datamodels(query, schema, result)
    _check_fields(query, schema, result)

    if enforce and result.has_warnings:
        lines = [f"  - [{w.category}] {w.message}" for w in result.warnings]
        raise SplunkQueryValidationError(
            "Schema enforcement failed — {} warning(s) block submission:\n".format(
                len(result.warnings)
            )
            + "\n".join(lines)
            + "\n\nFix the issues above or remove --enforce-schema to submit anyway."
        )

    return result


def write_validation_summary(rows: List[dict], results_dir: str) -> str:
    """
    Writes a validation summary CSV — one row per rule.

    Columns:
        title        — rule name from the rules file
        status       — PASS or FAIL
        failed_items — pipe-separated warnings (empty when PASS)

    Args:
        rows        (list): Each dict must have keys: title, status, failed_items
        results_dir (str):  Directory to write the file into.

    Returns:
        str: Absolute path to the written CSV.
    """
    os.makedirs(results_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(results_dir, "_validation_summary_{}.csv".format(timestamp))

    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["title", "status", "failed_items"],
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()
        writer.writerows(rows)

    logger.info("Validation summary written to: %s", path)
    return path


def _check_macros(query: str, schema: dict, result: SchemaValidationResult) -> None:
    cfg = schema.get("macros", {})
    if not cfg.get("enabled", True):
        return
    known_bases = {
        re.split(r"[\(\s]", str(k))[0].strip().lower()
        for k in cfg.get("known", [])
    }
    for raw in re.findall(r"`([^`]+)`", query):
        base = re.split(r"[\(\s]", raw)[0].strip().lower()
        if base and base not in known_bases:
            result.warnings.append(SchemaWarning(
                category="macro",
                message="`{}` is not listed in schema.yaml macros.".format(raw),
                suggestion=(
                    "If this macro exists in your Splunk environment, "
                    "add it under macros.known in config/schema.yaml"
                ),
            ))


def _check_indexes(query: str, schema: dict, result: SchemaValidationResult) -> None:
    cfg = schema.get("indexes", {})
    if not cfg.get("enabled", True):
        return
    known = set(cfg.get("known", []))
    for idx in re.findall(r'\bindex\s*=\s*["\']?([A-Za-z0-9_\-\*]+)["\']?', query, re.IGNORECASE):
        if idx not in known:
            result.warnings.append(SchemaWarning(
                category="index",
                message="index='{}' is not listed in schema.yaml indexes.".format(idx),
                suggestion="Add it under indexes.known in config/schema.yaml",
            ))


def _check_sourcetypes(query: str, schema: dict, result: SchemaValidationResult) -> None:
    cfg = schema.get("sourcetypes", {})
    if not cfg.get("enabled", True):
        return
    known = set(cfg.get("known", []))
    for st in re.findall(r'\bsourcetype\s*=\s*["\']?([A-Za-z0-9_\-:]+)["\']?', query, re.IGNORECASE):
        if st not in known:
            result.warnings.append(SchemaWarning(
                category="sourcetype",
                message="sourcetype='{}' is not listed in schema.yaml sourcetypes.".format(st),
                suggestion="Add it under sourcetypes.known in config/schema.yaml",
            ))


def _check_datamodels(query: str, schema: dict, result: SchemaValidationResult) -> None:
    cfg = schema.get("datamodels", {})
    if not cfg.get("enabled", True):
        return
    known = set(cfg.get("known", []))
    for dm in re.findall(r'\bdatamodel\s*=\s*["\']?([A-Za-z0-9_]+)', query, re.IGNORECASE):
        if dm not in known:
            result.warnings.append(SchemaWarning(
                category="datamodel",
                message="datamodel='{}' is not listed in schema.yaml datamodels.".format(dm),
                suggestion="Add it under datamodels.known in config/schema.yaml",
            ))


def _strip_quoted_values(query: str) -> str:
    """
    Removes quoted string values from a query before field extraction.
    Prevents false positives — e.g. "cmd.exe" contributing 'exe' as a field name.
    """
    query = re.sub(r'"[^"]*"', '""', query)
    query = re.sub(r"'[^']*'", "''", query)
    return query


def _check_fields(query: str, schema: dict, result: SchemaValidationResult) -> None:
    """
    Warns when fields used with a known sourcetype or datamodel dataset are not
    in the schema.yaml field definitions for that context.

    False positive prevention:
      - Quoted string values stripped before extraction (cmd.exe -> no 'exe' flag)
      - Datamodel reference parts excluded from the field check set
        (Endpoint.Processes -> 'Endpoint' and 'Processes' are not checked as fields)
      - Only leaf field names from dotted expressions are checked
      - SPL keywords and short tokens are excluded
    """
    cfg = schema.get("sourcetype_fields", {})
    if not cfg.get("enabled", True):
        return

    used_sourcetypes = re.findall(
        r'\bsourcetype\s*=\s*["\']?([A-Za-z0-9_\-:]+)["\']?',
        query, re.IGNORECASE
    )
    dm_datasets = re.findall(
        r'\bdatamodel\s*=\s*[A-Za-z0-9_]+\.([A-Za-z0-9_]+)',
        query, re.IGNORECASE
    )

    # All parts of datamodel references — exclude from field checking
    dm_ref_parts: set = set()
    for ref in re.findall(r'\bdatamodel\s*=\s*([A-Za-z0-9_.]+)', query, re.IGNORECASE):
        dm_ref_parts.update(ref.split("."))

    all_contexts = set(used_sourcetypes) | set(dm_datasets)
    query_clean  = _strip_quoted_values(query)

    skip_tokens = {
        "as", "by", "where", "from", "and", "or", "not", "in",
        "true", "false", "null", "count", "sum", "avg", "min", "max",
        "values", "earliest", "latest", "span", "bins", "eval",
    }

    for context in all_contexts:
        context_def = cfg.get(context) or cfg.get("Endpoint.{}".format(context))
        if not context_def:
            continue
        known_fields = set(context_def.get("fields", []))
        if not known_fields:
            continue

        fields_in_query: set = set()

        # Dotted prefix.leaf patterns — take only the leaf
        for m in re.finditer(
            r'([A-Za-z_][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)',
            query_clean
        ):
            leaf = m.group(2)
            fields_in_query.add(leaf)

        # BY clause fields — strip prefix, keep leaf
        by_match = re.search(r'\bby\b(.+?)(?:\||$)', query_clean, re.IGNORECASE | re.DOTALL)
        if by_match:
            for f in re.findall(r'[A-Za-z_][A-Za-z0-9_.]*', by_match.group(1)):
                fields_in_query.add(f.split(".")[-1])

        # Exclude datamodel reference parts and system fields
        fields_in_query -= dm_ref_parts
        fields_in_query -= {"_time", "host", "source", "sourcetype", "index"}

        unknown = fields_in_query - known_fields

        for uf in sorted(unknown):
            if len(uf) < 3 or uf.lower() in skip_tokens:
                continue
            result.warnings.append(SchemaWarning(
                category="field",
                message=(
                    "Field '{}' used with '{}' "
                    "is not in schema.yaml field definitions."
                ).format(uf, context),
                suggestion=(
                    "If this field exists, add it under "
                    "sourcetype_fields.{}.fields in config/schema.yaml".format(context)
                ),
            ))


def _load_schema() -> Optional[dict]:
    if not os.path.isfile(_SCHEMA_PATH):
        return None
    try:
        import yaml
        with open(_SCHEMA_PATH, encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except ImportError:
        return _load_schema_basic()
    except Exception as exc:
        logger.warning("Could not load schema.yaml: %s", exc)
        return None


def _load_schema_basic() -> Optional[dict]:
    try:
        schema: dict = {}
        current_section: Optional[str] = None
        current_list_key: Optional[str] = None
        current_subsection: Optional[str] = None

        with open(_SCHEMA_PATH, encoding="utf-8") as fh:
            for raw_line in fh:
                line    = raw_line.rstrip()
                stripped = line.lstrip()
                if not stripped or stripped.startswith("#"):
                    continue
                indent = len(line) - len(stripped)

                if indent == 0 and stripped.endswith(":"):
                    current_section = stripped[:-1]
                    schema[current_section] = {}
                    current_subsection = None
                    current_list_key   = None
                elif indent == 2 and current_section:
                    if stripped.startswith("- "):
                        if current_list_key and isinstance(
                            schema[current_section].get(current_list_key), list
                        ):
                            schema[current_section][current_list_key].append(
                                stripped[2:].strip().strip("'\"")
                            )
                    elif ":" in stripped:
                        key, _, val = stripped.partition(":")
                        val = val.strip().strip("'\"")
                        current_list_key = key.strip()
                        if val.lower() in ("true", "false"):
                            schema[current_section][current_list_key] = val.lower() == "true"
                        elif val:
                            schema[current_section][current_list_key] = val
                        else:
                            schema[current_section][current_list_key] = []
                        current_subsection = current_list_key
                elif indent == 4 and stripped.startswith("- "):
                    if current_subsection and current_section:
                        target = schema[current_section].get(current_subsection)
                        if isinstance(target, list):
                            target.append(stripped[2:].strip().strip("'\""))

        return schema
    except Exception as exc:
        logger.warning("Basic schema parser failed: %s", exc)
        return None
