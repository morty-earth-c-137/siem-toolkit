"""
models.py
---------
Dataclasses representing structured Splunk API response objects.

References:
  https://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTsearch
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class SearchJob:
    """Represents a Splunk search job returned by POST /services/search/jobs."""
    sid: str


@dataclass
class JobStatus:
    """Represents the current status of a running Splunk search job."""
    sid: str
    dispatch_state: str
    done_progress: float
    is_done: bool
    is_failed: bool
    messages: List[str] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, sid: str, data: Dict[str, Any]) -> "JobStatus":
        entry = data.get("entry", [{}])[0]
        content = entry.get("content", {})
        dispatch_state = content.get("dispatchState", "UNKNOWN")
        done_progress = float(content.get("doneProgress", 0.0))
        is_done = content.get("isDone", False)
        is_failed = dispatch_state in ("FAILED", "PARSING_FAILED")
        raw_messages = content.get("messages", [])
        messages = [
            f"[{m.get('type', 'INFO')}] {m.get('text', '')}"
            for m in raw_messages if isinstance(m, dict)
        ]
        return cls(
            sid=sid,
            dispatch_state=dispatch_state,
            done_progress=done_progress,
            is_done=bool(is_done),
            is_failed=is_failed,
            messages=messages,
        )


@dataclass
class SearchResults:
    """Represents paginated results from a completed Splunk search job."""
    sid: str
    total_results: int
    results: List[Dict[str, Any]]
    fields: List[str]

    @classmethod
    def from_api_response(cls, sid: str, data: Dict[str, Any]) -> "SearchResults":
        raw_results = data.get("results", [])
        fields_meta = data.get("fields", [])
        if fields_meta and isinstance(fields_meta[0], dict):
            fields = [f.get("name", "") for f in fields_meta]
        else:
            fields = [str(f) for f in fields_meta]
        if not fields and raw_results:
            fields = list(raw_results[0].keys())
        return cls(
            sid=sid,
            total_results=len(raw_results),
            results=raw_results,
            fields=fields,
        )
