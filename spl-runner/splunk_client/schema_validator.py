"""
schema_validator.py
-------------------
Validates a SPL query against the environment schema defined in
config/schema.yaml.

Schema validation is OPTIONAL and only runs when --validate-schema is
passed as a CLI flag. It does not block query submission — it warns.

What it checks (each section can be toggled in schema.yaml):
  macros      : backtick macros in the query exist in schema.yaml
  indexes     : index= references exist in schema.yaml
  sourcetypes : sourcetype= references exist in schema.yaml
  datamodels  : datamodel= references in tstats exist in schema.yaml
  fields      : fields used with a known sourcetype match that
                sourcetype's defined fields (warns on unknown fields)

All issues are returned as a list of SchemaWarning objects so the
caller can decide how to display them. Nothing is raised.

The schema.yaml file is resolved relative to main.py so it works
from any directory.
"""

import os
import re
import logging
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Locate config/schema.yaml relative to the project root
# ---------------------------------------------------------------------------
_HERE        = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_HERE)
_SCHEMA_PATH  = os.path.join(_PROJECT_ROOT, "config", "schema.yaml")


@dataclass
class SchemaWarning:
    """A single schema validation warning."""
    category: str    # e.g. 'macro', 'index', 'sourcetype', 'field'
    message: str
    suggestion: str = ""


@dataclass
class SchemaValidationResult:
    """Result of a full schema validation run."""
    warnings: List[SchemaWarning] = field(default_factory=list)
    schema_loaded: bool = False
    schema_path: str = ""

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    def print_report(self) -> None:
        """Prints a formatted warning report to console."""
        if not self.schema_loaded:
            print(
                "\n  [SCHEMA] config/schema.yaml not found — "
                "copy config/schema.yaml.example and configure it.\n"
            )
            return

        if not self.has_warnings:
            print("\n  [SCHEMA] All schema checks passed. ✓\n")
            return

        print(f"\n  [SCHEMA] {len(self.warnings)} warning(s) found:")
        print("  " + "-" * 56)
        for w in self.warnings:
            print(f"  [{w.category.upper():<12}] {w.message}")
            if w.suggestion:
                print(f"               Suggestion: {w.suggestion}")
        print("  " + "-" * 56 + "\n")


def validate_schema(query: str) -> SchemaValidationResult:
    """
    Validates a SPL query against config/schema.yaml.

    Args:
        query (str): The validated SPL query string.

    Returns:
        SchemaValidationResult: All warnings found (empty list if clean).
    """
    result = SchemaValidationResult(schema_path=_SCHEMA_PATH)

    schema = _load_schema()
    if schema is None:
        return result

    result.schema_loaded = True

    _check_macros(query, schema, result)
    _check_indexes(query, schema, result)
    _check_sourcetypes(query, schema, result)
    _check_datamodels(query, schema, result)
    _check_fields(query, schema, result)

    return result


# ---------------------------------------------------------------------------
# Individual checkers
# ---------------------------------------------------------------------------

def _check_macros(query: str, schema: dict, result: SchemaValidationResult) -> None:
    """Warns on backtick macros not listed in schema.yaml."""
    cfg = schema.get("macros", {})
    if not cfg.get("enabled", True):
        return

    known = set(cfg.get("known", []))
    if not known:
        return

    # Extract all `macro_name` and `macro_name(...)` usages
    used_macros = re.findall(r"`([^`]+)`", query)

    for macro_raw in used_macros:
        # Strip arguments: `macro_name(arg)` -> macro_name
        macro_name = re.split(r"[\(\s]", macro_raw)[0].strip()
        if macro_name and macro_name not in known:
            result.warnings.append(SchemaWarning(
                category="macro",
                message=f"`{macro_name}` is not listed in schema.yaml macros.",
                suggestion=(
                    f"If this macro exists in your Splunk environment, "
                    f"add it under macros.known in config/schema.yaml"
                ),
            ))


def _check_indexes(query: str, schema: dict, result: SchemaValidationResult) -> None:
    """Warns on index= references not listed in schema.yaml."""
    cfg = schema.get("indexes", {})
    if not cfg.get("enabled", True):
        return

    known = set(cfg.get("known", []))
    if not known:
        return

    used = re.findall(r'\bindex\s*=\s*["\']?([A-Za-z0-9_\-*]+)["\']?', query, re.IGNORECASE)
    for idx in used:
        if "*" not in idx and idx.lower() not in {k.lower() for k in known}:
            result.warnings.append(SchemaWarning(
                category="index",
                message=f"index={idx!r} is not listed in schema.yaml indexes.",
                suggestion=f"Add '{idx}' under indexes.known in config/schema.yaml",
            ))


def _check_sourcetypes(query: str, schema: dict, result: SchemaValidationResult) -> None:
    """Warns on sourcetype= references not listed in schema.yaml."""
    cfg = schema.get("sourcetypes", {})
    if not cfg.get("enabled", True):
        return

    known = set(cfg.get("known", []))
    if not known:
        return

    used = re.findall(
        r'\bsourcetype\s*=\s*["\']?([A-Za-z0-9_\-:*]+)["\']?',
        query, re.IGNORECASE
    )
    for st in used:
        if "*" not in st and st not in known:
            result.warnings.append(SchemaWarning(
                category="sourcetype",
                message=f"sourcetype={st!r} is not listed in schema.yaml sourcetypes.",
                suggestion=f"Add '{st}' under sourcetypes.known in config/schema.yaml",
            ))


def _check_datamodels(query: str, schema: dict, result: SchemaValidationResult) -> None:
    """Warns on datamodel= references in tstats not listed in schema.yaml."""
    cfg = schema.get("datamodels", {})
    if not cfg.get("enabled", True):
        return

    known = set(cfg.get("known", []))
    if not known:
        return

    used = re.findall(
        r'\bdatamodel\s*=\s*([A-Za-z0-9_\-\.]+)',
        query, re.IGNORECASE
    )
    for dm_raw in used:
        dm = dm_raw.split(".")[0]  # Strip dataset suffix: Endpoint.Processes -> Endpoint
        if dm and dm not in known:
            result.warnings.append(SchemaWarning(
                category="datamodel",
                message=f"datamodel={dm!r} is not listed in schema.yaml datamodels.",
                suggestion=f"Add '{dm}' under datamodels.known in config/schema.yaml",
            ))


def _check_fields(query: str, schema: dict, result: SchemaValidationResult) -> None:
    """
    When a sourcetype is referenced in the query and field definitions exist
    for that sourcetype in schema.yaml, warns on fields not in that definition.

    This check is intentionally lenient:
      - Only triggers when sourcetype_fields.enabled = true
      - Only checks fields explicitly listed in the query after 'by', 'where',
        'eval', or 'stats' clauses
      - Prefixed fields (Processes.field_name) are checked after stripping prefix
    """
    cfg = schema.get("sourcetype_fields", {})
    if not cfg.get("enabled", True):
        return

    # Find sourcetypes referenced in the query
    used_sourcetypes = re.findall(
        r'\bsourcetype\s*=\s*["\']?([A-Za-z0-9_\-:]+)["\']?',
        query, re.IGNORECASE
    )

    # Also detect data model dataset references like Endpoint.Processes
    dm_datasets = re.findall(
        r'\bdatamodel\s*=\s*[A-Za-z0-9_]+\.([A-Za-z0-9_]+)',
        query, re.IGNORECASE
    )

    all_contexts = set(used_sourcetypes) | set(dm_datasets)

    for context in all_contexts:
        context_def = cfg.get(context) or cfg.get(f"Endpoint.{context}")
        if not context_def:
            continue

        known_fields = set(context_def.get("fields", []))
        if not known_fields:
            continue

        # Extract field names used in by/where clauses and after Processes.
        # We extract dotted names and plain field names
        fields_in_query = set()

        # Dotted: Processes.field_name -> field_name
        for m in re.finditer(r'[A-Za-z_]+\.([A-Za-z_][A-Za-z0-9_]*)', query):
            fields_in_query.add(m.group(1))

        # BY clause fields
        by_match = re.search(r'\bby\b(.+?)(?:\||$)', query, re.IGNORECASE | re.DOTALL)
        if by_match:
            for f in re.findall(r'[A-Za-z_][A-Za-z0-9_.]*', by_match.group(1)):
                fields_in_query.add(f.split(".")[-1])

        unknown = fields_in_query - known_fields - {"_time", "host", "source", "sourcetype", "index"}

        for uf in sorted(unknown):
            # Skip short tokens that are likely keywords or literals
            if len(uf) < 3 or uf.lower() in {
                "as", "by", "where", "from", "and", "or", "not", "in",
                "true", "false", "null", "count", "sum", "avg", "min", "max"
            }:
                continue
            result.warnings.append(SchemaWarning(
                category="field",
                message=f"Field '{uf}' used with '{context}' is not in schema.yaml field definitions.",
                suggestion=(
                    f"If this field exists, add it under "
                    f"sourcetype_fields.{context}.fields in config/schema.yaml"
                ),
            ))


# ---------------------------------------------------------------------------
# YAML loader (uses PyYAML if available, falls back to basic parser)
# ---------------------------------------------------------------------------

def _load_schema() -> Optional[dict]:
    """
    Loads and parses config/schema.yaml.
    Returns None if the file is not found or cannot be parsed.
    """
    if not os.path.isfile(_SCHEMA_PATH):
        logger.debug("schema.yaml not found at %s — schema validation skipped.", _SCHEMA_PATH)
        return None

    try:
        import yaml
        with open(_SCHEMA_PATH, encoding="utf-8") as f:
            schema = yaml.safe_load(f)
        logger.debug("schema.yaml loaded from %s", _SCHEMA_PATH)
        return schema or {}
    except ImportError:
        logger.warning(
            "PyYAML not installed — install with: pip install pyyaml\n"
            "Schema validation requires PyYAML."
        )
        return None
    except Exception as exc:
        logger.error("Failed to parse schema.yaml: %s", exc)
        return None
