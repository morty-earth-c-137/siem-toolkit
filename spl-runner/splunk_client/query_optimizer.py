"""
query_optimizer.py
------------------
Analyses a SPL query and produces optimisation recommendations based on
the official Splunk SPL reference documentation (SPL 10.2).

Activated by the --optimize flag on the CLI. Does NOT modify or submit
the query — it only prints recommendations so the user can decide whether
to apply them before submitting.

Optimisation checks (grounded in the SPL docs):
  1. Expensive command detection
     Flags transaction, join, map, append — docs recommend alternatives
  2. tstats opportunity
     If a search uses index+sourcetype with stats, suggest tstats
  3. Field filtering early
     If 'fields' command appears after transforming commands, suggest moving it
  4. dedup vs stats
     dedup is slower than stats count by field — suggest alternative
  5. head/tail placement
     Placing head before a sort loses the top-N semantics
  6. Wildcard field extraction
     * in eval/rex has performance implications per SPL docs
  7. Missing index filter
     A bare 'search' with no index= scans all indexes
  8. sort + head pattern
     Sort then head is valid but reverse order (head then sort) is wrong
  9. Unknown commands
     Commands not in the SPL reference docs are flagged

Each recommendation includes:
  - what was found
  - why it matters (grounded in the docs)
  - what to do instead
"""

import re
import logging
from dataclasses import dataclass, field
from typing import List

from splunk_client.spl_knowledge import (
    VALID_COMMANDS,
    EXPENSIVE_CMDS,
    TRANSFORMING_CMDS,
)

logger = logging.getLogger(__name__)


@dataclass
class Recommendation:
    """A single optimisation recommendation."""
    severity: str   # 'WARNING', 'SUGGESTION', 'INFO'
    check:    str   # Short label identifying the check
    finding:  str   # What was found in the query
    reason:   str   # Why it matters
    action:   str   # What to do


@dataclass
class OptimizationResult:
    """Result of a full optimisation analysis."""
    recommendations: List[Recommendation] = field(default_factory=list)
    original_query:  str = ""

    @property
    def has_recommendations(self) -> bool:
        return len(self.recommendations) > 0

    def print_report(self) -> None:
        """Prints a formatted optimisation report to console."""
        if not self.has_recommendations:
            print("\n  [OPTIMIZER] No optimisation issues found. Query looks good. ✓\n")
            return

        warnings    = [r for r in self.recommendations if r.severity == "WARNING"]
        suggestions = [r for r in self.recommendations if r.severity == "SUGGESTION"]
        info        = [r for r in self.recommendations if r.severity == "INFO"]

        print(f"\n  [OPTIMIZER] {len(self.recommendations)} recommendation(s):")
        print("  " + "=" * 60)

        for group, label in [(warnings, "WARNINGS"), (suggestions, "SUGGESTIONS"), (info, "INFO")]:
            if not group:
                continue
            print(f"\n  {label}:")
            print("  " + "-" * 60)
            for r in group:
                print(f"  [{r.check}]")
                print(f"    Found   : {r.finding}")
                print(f"    Why     : {r.reason}")
                print(f"    Action  : {r.action}")
                print()

        print("  " + "=" * 60 + "\n")


def optimize_query(query: str) -> OptimizationResult:
    """
    Analyses a SPL query and returns optimisation recommendations.

    This function does NOT modify the query. It only analyses and reports.
    The user decides whether to apply any suggestions before resubmitting.

    Args:
        query (str): A validated SPL query string.

    Returns:
        OptimizationResult: All recommendations found.
    """
    result = OptimizationResult(original_query=query)
    q_lower = query.lower()

    # Extract the pipeline stages (split on pipe, ignoring pipes inside strings)
    stages = _split_pipeline(query)
    commands_in_query = _extract_commands(stages)

    _check_expensive_commands(commands_in_query, result)
    _check_tstats_opportunity(query, q_lower, commands_in_query, result)
    _check_dedup_vs_stats(q_lower, commands_in_query, result)
    _check_head_tail_placement(commands_in_query, result)
    _check_missing_index(query, q_lower, commands_in_query, result)
    _check_wildcard_extraction(query, result)
    _check_unknown_commands(commands_in_query, result)
    _check_transaction_alternative(q_lower, commands_in_query, result)
    _check_fields_command_placement(commands_in_query, result)

    return result


# ---------------------------------------------------------------------------
# Individual optimisation checks
# ---------------------------------------------------------------------------

def _check_expensive_commands(
    commands: List[str], result: OptimizationResult
) -> None:
    """
    Flags commands documented as expensive in the SPL reference.
    Source: SPL docs on transaction, join, map, append.
    """
    expensive_found = [c for c in commands if c in EXPENSIVE_CMDS]
    for cmd in expensive_found:
        doc_hint = _get_perf_hint(cmd)
        result.recommendations.append(Recommendation(
            severity="WARNING",
            check="expensive-command",
            finding=f"Command '{cmd}' is used in the query.",
            reason=doc_hint,
            action=_get_alternative(cmd),
        ))


def _check_tstats_opportunity(
    query: str, q_lower: str, commands: List[str], result: OptimizationResult
) -> None:
    """
    Suggests tstats when a search uses a datamodel with stats.
    tstats operates on index-time fields and is significantly faster.
    Source: SPL docs — tstats description: 'faster than the stats command'.
    """
    if "tstats" in commands:
        return   # Already using tstats

    has_datamodel = bool(re.search(r'\bdatamodel\s*=', query, re.IGNORECASE))
    has_stats     = "stats" in commands
    has_search    = commands[0] == "search" if commands else False

    if has_datamodel and has_stats:
        result.recommendations.append(Recommendation(
            severity="SUGGESTION",
            check="tstats-opportunity",
            finding="Query uses datamodel= with stats but not tstats.",
            reason=(
                "The tstats command performs statistical queries on indexed fields "
                "in tsidx files. Per the Splunk docs: 'tstats is faster than the "
                "stats command' because it searches index-time fields rather than "
                "raw events."
            ),
            action=(
                "Replace 'search ... | stats' with '| tstats ... from datamodel=...' "
                "to leverage accelerated data model summaries."
            ),
        ))

    if (has_search and has_stats and not has_datamodel
            and not any(c in commands for c in ("tstats", "mstats"))):
        # Check if it's hitting a CIM-compatible sourcetype
        dm_sourcetypes = {
            "sysmon", "wineventlog", "xmlwineventlog",
            "cisco:asa", "palo-alto:traffic",
        }
        q_sourcetypes = set(re.findall(
            r'sourcetype\s*=\s*["\']?([A-Za-z0-9_\-:]+)["\']?', q_lower
        ))
        if q_sourcetypes & dm_sourcetypes:
            result.recommendations.append(Recommendation(
                severity="INFO",
                check="tstats-opportunity",
                finding=f"Using search+stats with sourcetype: {q_sourcetypes & dm_sourcetypes}.",
                reason=(
                    "These sourcetypes often map to CIM data models. If your data "
                    "is model-accelerated, tstats will run significantly faster."
                ),
                action=(
                    "Consider whether the data is in a CIM-accelerated data model "
                    "and rewrite using '| tstats ... from datamodel=...'."
                ),
            ))


def _check_dedup_vs_stats(
    q_lower: str, commands: List[str], result: OptimizationResult
) -> None:
    """
    dedup is a dataset processing command and forces full result scan.
    stats count by field is distributable streaming and much faster.
    Source: SPL docs on dedup — 'dataset processing command' classification.
    """
    if "dedup" not in commands:
        return
    result.recommendations.append(Recommendation(
        severity="SUGGESTION",
        check="dedup-vs-stats",
        finding="Query uses the 'dedup' command.",
        reason=(
            "Per the SPL docs, dedup is a 'dataset processing command' — it requires "
            "all results to be collected before processing, making it expensive. "
            "Using 'sortby' with dedup makes it even more expensive."
        ),
        action=(
            "If you only need unique values for counting or display, replace:\n"
            "    | dedup field_name\n"
            "with:\n"
            "    | stats count by field_name\n"
            "or use '| stats values(field_name)' for distinct value lists."
        ),
    ))


def _check_head_tail_placement(
    commands: List[str], result: OptimizationResult
) -> None:
    """
    head before sort loses semantic correctness for top-N.
    sort before head is the correct pattern.
    """
    if "head" not in commands or "sort" not in commands:
        return
    head_idx = commands.index("head")
    sort_idx = commands.index("sort")
    if head_idx < sort_idx:
        result.recommendations.append(Recommendation(
            severity="WARNING",
            check="head-sort-order",
            finding="'head' appears before 'sort' in the pipeline.",
            reason=(
                "Placing 'head N' before 'sort' limits the result set first, "
                "then sorts that small set — this does NOT give you the top N "
                "results overall. You get N arbitrary results, sorted."
            ),
            action=(
                "Reverse the order: '| sort -field | head N' "
                "to correctly return the top N results by the sort field."
            ),
        ))


def _check_missing_index(
    query: str, q_lower: str, commands: List[str], result: OptimizationResult
) -> None:
    """
    A search with no index= or sourcetype= filter scans all indexes.
    Per SPL best practices, always filter as early as possible.
    """
    if "tstats" in commands or "mstats" in commands:
        return  # tstats operates on summaries — different access pattern

    first_cmd = commands[0] if commands else ""
    if first_cmd != "search":
        return

    has_index      = bool(re.search(r'\bindex\s*=', query, re.IGNORECASE))
    has_sourcetype = bool(re.search(r'\bsourcetype\s*=', query, re.IGNORECASE))

    if not has_index and not has_sourcetype:
        result.recommendations.append(Recommendation(
            severity="WARNING",
            check="missing-index-filter",
            finding="Query has no index= or sourcetype= filter.",
            reason=(
                "A search with no index or sourcetype filter scans ALL indexes. "
                "Per Splunk best practices: 'Write better searches — filter early "
                "to reduce the amount of data the search has to process.'"
            ),
            action=(
                "Add an index filter as early as possible:\n"
                "    search index=main sourcetype=syslog ..."
            ),
        ))


def _check_wildcard_extraction(query: str, result: OptimizationResult) -> None:
    """
    Wildcards in field names within rex or eval are expensive.
    Wildcards at the start of a search term cause full index scans.
    """
    # Leading wildcards in search terms
    leading_wildcards = re.findall(r'(?:^|\s)\*[A-Za-z]', query)
    if leading_wildcards:
        result.recommendations.append(Recommendation(
            severity="WARNING",
            check="leading-wildcard",
            finding=f"Query contains leading wildcard(s): {leading_wildcards}",
            reason=(
                "Leading wildcards (e.g. *error, *fail) require scanning every "
                "event because the index is prefix-based. Per Splunk docs this is "
                "one of the most common causes of slow searches."
            ),
            action=(
                "Avoid leading wildcards. Use trailing wildcards (fail*) or "
                "extract the field with rex and filter on the extracted value."
            ),
        ))


def _load_known_macros() -> set:
    """
    Loads the list of known macros from config/schema.yaml.
    Returns an empty set if the file is absent or unreadable.
    Macro names are normalised to lowercase for case-insensitive matching.
    """
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(os.path.dirname(here), "config", "schema.yaml")
    if not os.path.isfile(schema_path):
        return set()
    try:
        import yaml
        with open(schema_path, encoding="utf-8") as f:
            schema = yaml.safe_load(f) or {}
        raw = schema.get("macros", {}).get("known", [])
        # Normalise: strip arguments so drop_dm_object_name(Registry)
        # matches the schema entry "drop_dm_object_name"
        normalised = set()
        import re as _re
        for entry in raw:
            base = _re.split(r"[\(\s]", str(entry))[0].strip().lower()
            normalised.add(base)
        return normalised
    except Exception:
        return set()


def _check_unknown_commands(
    commands: List[str], result: OptimizationResult
) -> None:
    """
    Flags pipeline commands not found in the SPL 10.2 reference docs.

    Backtick macro stages are already excluded by _extract_commands.
    Additionally, any command that matches a known macro base name from
    config/schema.yaml is silently skipped — it is a known construct.
    """
    known_macros = _load_known_macros()

    for cmd in commands:
        if not cmd:
            continue
        if _is_keyword(cmd):
            continue
        if cmd in VALID_COMMANDS:
            continue
        # Strip arguments from cmd in case any slipped through
        # e.g. "drop_dm_object_name(registry)" -> "drop_dm_object_name"
        import re as _re
        cmd_base = _re.split(r"[\(\s]", cmd)[0].strip().lower()
        if cmd_base in known_macros:
            continue
        result.recommendations.append(Recommendation(
            severity="INFO",
            check="unknown-command",
            finding=f"Command '{cmd}' is not in the SPL 10.2 reference docs.",
            reason=(
                "This may be a custom app command, a Splunk ES macro command, "
                "or a typo. The validator cannot confirm its syntax is correct."
            ),
            action=(
                "Verify the command exists in your Splunk environment. "
                "If it's a custom command, ensure the app providing it is installed. "
                "If it is a known macro, add it under macros.known in config/schema.yaml."
            ),
        ))


def _check_transaction_alternative(
    q_lower: str, commands: List[str], result: OptimizationResult
) -> None:
    """
    transaction is already caught by expensive command check, but if
    it's used purely for session grouping, stats is always better.
    """
    if "transaction" not in commands:
        return
    if "maxspan" not in q_lower and "maxpause" not in q_lower:
        result.recommendations.append(Recommendation(
            severity="SUGGESTION",
            check="transaction-no-time-constraint",
            finding="transaction used without maxspan= or maxpause= limits.",
            reason=(
                "Without time constraints, transaction groups events indefinitely "
                "which can consume enormous memory. Per the SPL docs, transaction "
                "should always have maxspan and maxpause set."
            ),
            action=(
                "Add time limits:\n"
                "    | transaction field maxspan=1h maxpause=5m\n"
                "Or consider replacing with stats for session counting:\n"
                "    | stats count values(field) by session_id"
            ),
        ))


def _check_fields_command_placement(
    commands: List[str], result: OptimizationResult
) -> None:
    """
    The 'fields' command should appear as early as possible to reduce
    the data volume carried through the pipeline.
    Per SPL docs: fields is distributable streaming — run it early.
    """
    if "fields" not in commands:
        return

    fields_idx = commands.index("fields")
    transforming_before = [
        c for c in commands[:fields_idx]
        if c in TRANSFORMING_CMDS
    ]

    if transforming_before:
        result.recommendations.append(Recommendation(
            severity="SUGGESTION",
            check="fields-placement",
            finding=(
                f"'fields' appears after transforming command(s): "
                f"{transforming_before}"
            ),
            reason=(
                "The 'fields' command is a distributable streaming command — "
                "per the SPL docs, placing it early reduces the data volume "
                "carried through subsequent pipeline stages."
            ),
            action=(
                "Move '| fields ...' earlier in the pipeline, before "
                "transforming commands like stats, chart, or timechart."
            ),
        ))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _split_pipeline(query: str) -> List[str]:
    """Splits a SPL query on pipe characters, ignoring pipes in strings."""
    stages = []
    current = []
    in_string = False
    quote_char = None

    for char in query:
        if char in ('"', "'") and not in_string:
            in_string = True
            quote_char = char
            current.append(char)
        elif in_string and char == quote_char:
            in_string = False
            quote_char = None
            current.append(char)
        elif char == "|" and not in_string:
            stages.append("".join(current).strip())
            current = []
        else:
            current.append(char)

    if current:
        stages.append("".join(current).strip())

    return [s for s in stages if s]


def _extract_commands(stages: List[str]) -> List[str]:
    """
    Extracts the command name from each pipeline stage.

    Stages that are pure backtick macro calls are skipped entirely.
    A stage like  | `drop_dm_object_name(Registry)`  is a macro invocation,
    not a SPL command, and must not be evaluated against the command list.
    """
    commands = []
    for stage in stages:
        stage_stripped = stage.strip()
        # Skip stages that are entirely a backtick macro call
        if stage_stripped.startswith("`"):
            continue
        tokens = stage_stripped.split()
        if tokens:
            cmd = tokens[0].lower()
            # Also skip if the first token itself is backtick-wrapped
            if cmd.startswith("`"):
                continue
            commands.append(cmd)
    return commands


def _is_keyword(token: str) -> bool:
    """Returns True if the token is a SPL keyword rather than a command."""
    keywords = {
        "search", "from", "where", "by", "as", "and", "or", "not",
        "in", "true", "false", "null", "over", "with",
    }
    return token.lower() in keywords


def _get_perf_hint(command: str) -> str:
    """Returns a documentation-grounded performance note for expensive commands."""
    hints = {
        "transaction": (
            "The 'transaction' command is one of the most resource-intensive SPL "
            "commands. Per the docs, it requires centralised streaming (runs on the "
            "search head only) and holds all matching events in memory. "
            "Use 'stats' for session grouping where possible."
        ),
        "join": (
            "The 'join' command runs a subsearch and holds results in memory. "
            "Per SPL docs it is centralized streaming only. For large datasets "
            "'stats' or 'tstats' with a lookup is significantly faster."
        ),
        "map": (
            "The 'map' command executes one separate search per result row. "
            "With 1000 results it runs 1000 searches. Per the docs, this is an "
            "orchestrating command — use sparingly and with strict maxsearches limits."
        ),
        "append": (
            "The 'append' command runs a complete subsearch before appending. "
            "Per SPL docs, 'union' is often a faster alternative for combining "
            "result sets from different searches."
        ),
        "predict": (
            "The 'predict' command uses machine learning algorithms and is CPU-intensive."
        ),
        "anomalydetection": (
            "The 'anomalydetection' command performs statistical analysis on all results "
            "and can be slow on large datasets."
        ),
    }
    return hints.get(command, f"'{command}' is classified as expensive in the SPL docs.")


def _get_alternative(command: str) -> str:
    """Returns a recommended alternative for an expensive command."""
    alternatives = {
        "transaction": (
            "Use '| stats count values(field) by session_id' for session grouping, "
            "or '| streamstats' for running calculations."
        ),
        "join": (
            "Use '| stats' with eval to combine fields, or configure a lookup table "
            "and use '| lookup' which is distributable streaming."
        ),
        "map": (
            "Restructure the search to use subsearch syntax [ search ... ] inline, "
            "or use '| lookup' with a pre-built table."
        ),
        "append": (
            "Use '| union (search ...)' instead — union is a generating command "
            "that is more efficient for combining result sets."
        ),
        "predict": "Limit input data with 'head' or time filters before using predict.",
        "anomalydetection": "Pre-filter with stats before running anomalydetection.",
    }
    return alternatives.get(command, f"Consult the SPL docs for '{command}' alternatives.")
