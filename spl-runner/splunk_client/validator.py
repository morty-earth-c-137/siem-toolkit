"""
validator.py
------------
Pre-flight SPL query validation, grounded in the Splunk SPL 10.2
reference documentation loaded by spl_knowledge.py.

Validation checks:
  1. Query is not empty or whitespace-only
  2. Query meets minimum length
  3. Query does not contain forbidden/dangerous SPL commands
     (grounded in SPL docs — delete, outputlookup, collect, etc.)
  4. Query does not contain inline time modifiers (stripped + warned)
  5. Query starts with a valid SPL source/generating command
     (validated against the live command list from the docs)
  6. Unknown commands in the pipeline are flagged as warnings
     (not hard failures — may be custom app commands)
  7. Brackets and parentheses are balanced

Time range policy:
  All queries are hard-locked to earliest=-30m latest=now.
  Inline modifiers are stripped and logged as warnings.

References:
  Splunk SPL 10.2 Search Reference — all commands documented in spl_docs/
"""

import re
import logging
from typing import List, Tuple

from splunk_client.exceptions import SplunkQueryValidationError
from splunk_client.spl_knowledge import (
    GENERATING_CMDS,
    is_valid_command,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Time range policy
# ---------------------------------------------------------------------------
# Time range constants imported from time_range.py
# Kept here for backward compatibility — search.py uses time_range directly
from splunk_client.time_range import DEFAULT_EARLIEST as ENFORCED_EARLIEST, DEFAULT_LATEST as ENFORCED_LATEST
MINIMUM_QUERY_LENGTH = 5

# ---------------------------------------------------------------------------
# Forbidden commands — blocked outright regardless of context
# These are commands that modify data, exfiltrate data, or execute shell code.
# Grounded in SPL docs: delete (manages indexes), outputlookup (writes files),
# collect (writes summary indexes), sendemail (exfiltration risk),
# runshellscript/script (code execution).
# ---------------------------------------------------------------------------
FORBIDDEN_COMMANDS: Tuple[str, ...] = (
    "delete",
    "outputlookup",
    "collect",
    "sendemail",
    "runshellscript",
    "script",
    "rest",
)

TIME_MODIFIER_PATTERN = re.compile(
    r"\b(earliest|latest)\s*=\s*[^\s|]+", re.IGNORECASE
)

# Valid pipeline-opening commands — must be generating or source commands
# per the SPL docs. Includes pipe-first syntax for tstats/inputlookup etc.
VALID_SOURCE_PREFIXES: Tuple[str, ...] = (
    "search",
    "index=",
    "sourcetype=",
    "source=",
    "host=",
    "|",
    "`",       # bare macro as first token e.g. `windows_logging_event_streamer`
    "tstats",
    "mstats",
    "inputlookup",
    "inputcsv",
    "metadata",
    "multisearch",
    "union",
    "from",
    "makeresults",
    "gentimes",
    "loadjob",
    "datamodel",
)


def strip_comments(query: str) -> str:
    """
    Strips SPL inline comment blocks from a query string.

    Per Splunk docs (Search Manual 9.2 — Add comments to searches):
      - Three backticks open a comment:  ```
      - The next three backticks close it regardless of content or newlines
      - Single/double backticks inside a comment are part of it
      - Backslash does NOT escape — triple-backtick always closes

    Raises SplunkQueryValidationError if a comment is opened but never closed.

    Args:
        query (str): Raw SPL query potentially containing comment blocks.

    Returns:
        str: Query with all comment blocks replaced by a single space.
    """
    TRIPLE = "```"
    result  = []
    pos     = 0
    length  = len(query)

    while pos < length:
        idx = query.find(TRIPLE, pos)
        if idx == -1:
            # No more triple-backticks — rest is SPL
            result.append(query[pos:])
            break

        # Everything before this triple-backtick is SPL
        result.append(query[pos:idx])

        # Find the closing triple-backtick
        close_idx = query.find(TRIPLE, idx + 3)
        if close_idx == -1:
            raise SplunkQueryValidationError(
                "Unclosed comment block detected.\n"
                "A comment opened with ``` was never closed.\n"
                "Every opening ``` must have a matching closing ```.\n"
                f"Opened at position {idx}: ...{query[idx:idx+40]!r}..."
            )

        # Replace the comment block with a single space to preserve token boundaries
        result.append(" ")
        pos = close_idx + 3

    cleaned = "".join(result).strip()
    # Collapse any runs of whitespace left by removed comments
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)
    return cleaned


def validate_query(query: str) -> str:
    """
    Validates and sanitises a raw SPL query string.

    Performs structural, policy, and doc-grounded checks before any
    API call is made. Strips inline time modifiers and warns.

    Args:
        query (str): The raw SPL query string.

    Raises:
        SplunkQueryValidationError: If any hard check fails.

    Returns:
        str: The cleaned, validated query string (time modifiers stripped).
    """
    if not query or not query.strip():
        raise SplunkQueryValidationError(
            "Query is empty. Please provide a valid SPL search string."
        )

    query = query.strip()

    # --- Strip comment blocks before any validation ---
    # This ensures brackets, commands, and time modifiers inside comments
    # do not interfere with validation checks.
    # Raises SplunkQueryValidationError if a comment is unclosed.
    query = strip_comments(query)

    # --- Check 1: Minimum length ---
    if len(query) < MINIMUM_QUERY_LENGTH:
        raise SplunkQueryValidationError(
            f"Query is too short ({len(query)} characters). "
            f"Minimum is {MINIMUM_QUERY_LENGTH} characters."
        )

    # --- Check 2: Forbidden commands (hard block) ---
    query_lower = query.lower()
    for command in FORBIDDEN_COMMANDS:
        if re.search(rf"\b{re.escape(command)}\b", query_lower):
            raise SplunkQueryValidationError(
                f"Query contains the forbidden SPL command '{command}'.\n"
                "This command is blocked for safety and data integrity reasons.\n"
                f"See spl_docs/ for the '{command}' reference."
            )

    # --- Check 3: Strip inline time modifiers ---
    inline_times = TIME_MODIFIER_PATTERN.findall(query)
    if inline_times:
        logger.warning(
            "Inline time modifier(s) found and removed: %s. "
            "Enforced range: earliest=%s latest=%s",
            inline_times, ENFORCED_EARLIEST, ENFORCED_LATEST,
        )
        query = TIME_MODIFIER_PATTERN.sub("", query).strip()
        query = re.sub(r" {2,}", " ", query)

    # --- Check 4: Valid pipeline opening command ---
    query_stripped = query.lstrip()
    starts_valid = any(
        query_stripped.lower().startswith(p.lower())
        for p in VALID_SOURCE_PREFIXES
    )
    if not starts_valid:
        # Check if it starts with any known SPL command (generating)
        first_token = query_stripped.split()[0].lower() if query_stripped.split() else ""
        if first_token in GENERATING_CMDS:
            starts_valid = True

    if not starts_valid:
        raise SplunkQueryValidationError(
            f"Query does not start with a recognised SPL source command.\n"
            f"Received: '{query[:80]}'\n"
            f"Expected one of: {', '.join(VALID_SOURCE_PREFIXES[:8])}...\n"
            "Example: search index=main sourcetype=syslog | stats count by host\n"
            "Or:      | tstats count from datamodel=Endpoint.Processes by Processes.dest"
        )

    # --- Check 5: Pipeline command validation ---
    # Warn (don't block) on unrecognised commands — may be custom app commands
    unknown = _find_unknown_commands(query)
    for cmd in unknown:
        logger.warning(
            "Command '%s' is not in the SPL 10.2 reference docs. "
            "This may be a custom/app command or a typo. "
            "Use --optimize to analyse the full pipeline.",
            cmd,
        )

    # --- Check 6: Bracket balance ---
    _check_bracket_balance(query)

    logger.info("Query validation passed.")
    return query


def _find_unknown_commands(query: str) -> List[str]:
    """
    Returns a list of pipeline commands not found in the SPL docs.

    Backtick macro calls are fully excluded — a stage whose first
    non-whitespace token is a backtick-wrapped expression is a macro
    invocation, not a command, and is never flagged here.

    Examples skipped:
      | `drop_dm_object_name(Registry)`        <- pure macro stage
      | `security_content_ctime(firstTime)`    <- pure macro stage
      | `active_setup_registry_autostart_filter` <- pure macro stage
    """
    unknown = []
    stages = [s.strip() for s in query.split("|") if s.strip()]

    for stage in stages[1:]:  # Skip first stage (validated above)
        stage_stripped = stage.strip()

        # Skip stages that are entirely a backtick macro call
        if stage_stripped.startswith("`"):
            continue

        first_token = stage_stripped.split()[0].lower() if stage_stripped.split() else ""

        # Skip empty, keyword-only, or backtick-prefixed tokens
        if not first_token or first_token.startswith("`"):
            continue

        if (not is_valid_command(first_token)
                and first_token not in {
                    "search", "from", "where", "by", "as", "and", "or",
                }):
            unknown.append(first_token)

    return unknown


def _check_bracket_balance(query: str) -> None:
    """Checks for unbalanced brackets in a query."""
    stack = []
    pairs = {")": "(", "]": "["}

    for i, char in enumerate(query):
        if char in "([":
            stack.append((char, i))
        elif char in ")]":
            if not stack or stack[-1][0] != pairs[char]:
                raise SplunkQueryValidationError(
                    f"Unmatched '{char}' at position {i}. "
                    "Check your brackets and subsearch syntax."
                )
            stack.pop()

    if stack:
        unclosed = ", ".join(f"'{c}' at pos {i}" for c, i in stack)
        raise SplunkQueryValidationError(
            f"Unclosed bracket(s): {unclosed}. "
            "Check your subsearch or eval expressions."
        )
