"""
time_range.py
-------------
Parses and validates Splunk time range specifications.

Supports all Splunk time modifier formats per the official docs:
  https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.2/specify-time-ranges

Supported formats for --time flag:
  Minutes : 10m          -> earliest=-10m  latest=now
  Hours   : 2h           -> earliest=-2h   latest=now
  Days    : 7d           -> earliest=-7d   latest=now
  Weeks   : 2w           -> earliest=-2w   latest=now
  Snap    : @d           -> earliest=@d    latest=now  (start of today)
  Snap    : @w           -> earliest=@w    latest=now  (start of this week)
  Snap    : @mon         -> earliest=@mon  latest=now  (start of this month)
  Snap+   : 7d@d         -> earliest=-7d@d latest=now  (7 days ago, snapped to day boundary)
  Custom  : 24h@h        -> earliest=-24h@h latest=now (24 hours ago, snapped to hour)

Snap units (per Splunk docs):
  @s   snap to second
  @m   snap to minute
  @h   snap to hour
  @d   snap to day
  @w   snap to week  (Monday)
  @w0  snap to Sunday
  @mon snap to month
  @q   snap to quarter
  @y   snap to year

Default if --time is not specified: -30m to now (preserves current behaviour).

References:
  https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.2/specify-time-ranges/select-time-ranges-to-apply-to-your-search
  https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.2/specify-time-ranges/time-modifiers-for-search
"""

import re
import logging
from dataclasses import dataclass
from typing import Optional

from splunk_client.exceptions import SplunkQueryValidationError

logger = logging.getLogger(__name__)

# Default time range — used when --time is not specified
DEFAULT_EARLIEST = "-30m"
DEFAULT_LATEST   = "now"

# Valid snap units per Splunk docs
_SNAP_UNITS = {"s", "m", "h", "d", "w", "w0", "w1", "w2", "w3", "w4", "w5", "w6", "mon", "q", "y"}

# Relative unit pattern: number followed by unit
_RELATIVE_PATTERN = re.compile(
    r"^(\d+)(m|h|d|w|mon|q|y)(@(s|m|h|d|w[0-6]?|mon|q|y))?$",
    re.IGNORECASE,
)

# Snap-only pattern: just @unit with no relative component
_SNAP_ONLY_PATTERN = re.compile(
    r"^@(s|m|h|d|w[0-6]?|mon|q|y)$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class TimeRange:
    """
    A validated Splunk time range ready to submit to the API.

    Attributes:
        earliest (str): Splunk earliest_time value, e.g. '-30m', '-7d@d', '@mon'
        latest   (str): Splunk latest_time value, always 'now' for CLI usage
        description (str): Human-readable description for console logging
    """
    earliest:    str
    latest:      str
    description: str

    def log_info(self) -> None:
        """Logs the resolved time range to the console."""
        logger.info(
            "Time range: %s  (earliest=%s  latest=%s)",
            self.description, self.earliest, self.latest,
        )


def parse_time_range(value: Optional[str]) -> TimeRange:
    """
    Parses a --time flag value into a validated TimeRange.

    If value is None or empty, returns the default 30-minute window.

    Args:
        value (str | None): The raw --time flag value from the CLI.

    Returns:
        TimeRange: Validated time range ready to send to the Splunk API.

    Raises:
        SplunkQueryValidationError: If the value is not a recognised format.

    Examples:
        parse_time_range("10m")    -> earliest=-10m  latest=now
        parse_time_range("2h")     -> earliest=-2h   latest=now
        parse_time_range("7d")     -> earliest=-7d   latest=now
        parse_time_range("7d@d")   -> earliest=-7d@d latest=now
        parse_time_range("@d")     -> earliest=@d    latest=now
        parse_time_range("@mon")   -> earliest=@mon  latest=now
        parse_time_range(None)     -> earliest=-30m  latest=now  (default)
    """
    if not value or not value.strip():
        return TimeRange(
            earliest=DEFAULT_EARLIEST,
            latest=DEFAULT_LATEST,
            description="past 30 minutes (default)",
        )

    raw = value.strip().lower()

    # --- Special keyword: "all" means search all indexed time ---
    # Splunk represents this as earliest=0 (Unix epoch start), latest=now
    if raw in ("all", "alltime", "all_time"):
        return TimeRange(
            earliest="0",
            latest=DEFAULT_LATEST,
            description="all indexed time (earliest=0)",
        )

    # --- Snap-only: @d, @w, @mon, @y etc ---
    if _SNAP_ONLY_PATTERN.match(raw):
        snap_unit = raw[1:]
        description = _snap_description(snap_unit)
        return TimeRange(
            earliest=raw,
            latest=DEFAULT_LATEST,
            description=description,
        )

    # --- Relative with optional snap: 10m, 2h, 7d, 7d@d, 24h@h ---
    match = _RELATIVE_PATTERN.match(raw)
    if match:
        number    = match.group(1)
        unit      = match.group(2).lower()
        snap_part = match.group(3) or ""          # e.g. "@d" or ""
        snap_unit = match.group(4).lower() if match.group(4) else None

        earliest    = f"-{number}{unit}{snap_part}"
        unit_label  = _unit_label(unit, int(number))
        description = f"past {number} {unit_label}"
        if snap_unit:
            description += f", snapped to {_snap_description(snap_unit)}"

        return TimeRange(
            earliest=earliest,
            latest=DEFAULT_LATEST,
            description=description,
        )

    # --- Not recognised ---
    raise SplunkQueryValidationError(
        f"Unrecognised --time value: '{value}'\n"
        "Valid formats:\n"
        "  Minutes  : 10m          (past 10 minutes)\n"
        "  Hours    : 2h           (past 2 hours)\n"
        "  Days     : 7d           (past 7 days)\n"
        "  Weeks    : 2w           (past 2 weeks)\n"
        "  Months   : 3mon         (past 3 months)\n"
        "  Years    : 1y           (past 1 year)\n"
        "  Snap     : @d           (start of today to now)\n"
        "  Snap     : @w           (start of this week to now)\n"
        "  Snap     : @mon         (start of this month to now)\n"
        "  Snap     : @y           (start of this year to now)\n"
        "  Combined : 7d@d         (7 days ago, snapped to day boundary)\n"
        "  All time : all          (search all indexed data, use with care)\n"
        "Examples:\n"
        "  python main.py --query '...' --time 10m\n"
        "  python main.py --query '...' --time 3mon\n"
        "  python main.py --query '...' --time 1y\n"
        "  python main.py --query '...' --time @y\n"
        "  python main.py --query '...' --time all\n"
    )


def _unit_label(unit: str, number: int) -> str:
    """Returns a human-readable label for a time unit."""
    labels = {
        "m":   "minute" if number == 1 else "minutes",
        "h":   "hour"   if number == 1 else "hours",
        "d":   "day"    if number == 1 else "days",
        "w":   "week"   if number == 1 else "weeks",
        "mon": "month"  if number == 1 else "months",
        "q":   "quarter" if number == 1 else "quarters",
        "y":   "year"   if number == 1 else "years",
    }
    return labels.get(unit, unit)


def _snap_description(snap_unit: str) -> str:
    """Returns a human-readable description for a snap unit."""
    descriptions = {
        "s":   "second boundary",
        "m":   "minute boundary",
        "h":   "hour boundary",
        "d":   "start of day",
        "w":   "start of week (Monday)",
        "w0":  "start of week (Sunday)",
        "mon": "start of month",
        "q":   "start of quarter",
        "y":   "start of year",
    }
    return descriptions.get(snap_unit, f"@{snap_unit} boundary")
