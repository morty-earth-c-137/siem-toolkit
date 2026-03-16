"""
search.py
---------
Manages the full Splunk search job lifecycle:
  1. Validate query
  2. Submit  -> POST /services/search/jobs
  3. Poll    -> GET  /services/search/jobs/{sid}
  4. Fetch   -> GET  /services/search/jobs/{sid}/results
  5. Save    -> timestamped CSV in results directory

Time range is hard-enforced: earliest=-30m latest=now.

References:
  https://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTsearch
"""

import csv
import logging
import os
import time
from datetime import datetime
from typing import Optional

from splunk_client.client import SplunkClient
from splunk_client.config import SplunkConfig
from splunk_client.exceptions import SplunkJobError, SplunkResultsError, SplunkTimeoutError
from splunk_client.models import JobStatus, SearchJob, SearchResults
from splunk_client.time_range import TimeRange, parse_time_range
from splunk_client.validator import validate_query

logger = logging.getLogger(__name__)
_RESULTS_PAGE_SIZE = 10000


def run_search(
    query: str,
    config: SplunkConfig,
    rule_name: Optional[str] = None,
    time_range: Optional["TimeRange"] = None,
) -> Optional[str]:
    """
    Validates and runs a Splunk search end-to-end, saving results to CSV.

    Args:
        query (str): Raw SPL query string.
        config (SplunkConfig): Runtime configuration.
        rule_name (str, optional): Label for logging and file naming.
        time_range (TimeRange, optional): Time range to apply. Defaults to
            the last 30 minutes if not provided.

    Returns:
        str | None: Absolute path to the saved CSV file.
    """
    label = rule_name or f"query_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    logger.info("--- Starting search: '%s' ---", label)

    # Resolve time range — default to 30 minutes if not supplied
    tr = time_range or parse_time_range(None)
    tr.log_info()

    clean_query = validate_query(query)

    with SplunkClient(config) as client:
        job = _submit_job(client, clean_query, tr)
        logger.info("[%s] Job submitted — SID: %s", label, job.sid)
        _poll_job(client, job.sid, config, label)
        results = _fetch_results(client, job.sid, label)

    csv_path = _save_results_to_csv(results, config.results_dir, label)
    logger.info("[%s] Complete — %d result(s) saved to: %s", label, results.total_results, csv_path)
    return csv_path


def _submit_job(client: SplunkClient, query: str, time_range: TimeRange) -> SearchJob:
    if not query.lstrip().startswith("|") and not query.lower().lstrip().startswith("search"):
        spl = f"search {query}"
    else:
        spl = query

    payload = {
        "search": spl,
        "earliest_time": time_range.earliest,
        "latest_time": time_range.latest,
        "output_mode": "json",
        "exec_mode": "normal",
    }
    response = client.post("/services/search/jobs", data=payload)
    sid = response.get("sid")
    if not sid:
        raise SplunkJobError(f"No SID returned after job submission. Response: {response}")
    return SearchJob(sid=sid)


def _poll_job(client: SplunkClient, sid: str, config: SplunkConfig, label: str) -> None:
    elapsed = 0
    endpoint = f"/services/search/jobs/{sid}"

    while elapsed < config.job_max_wait:
        response = client.get(endpoint, params={"output_mode": "json"})
        status = JobStatus.from_api_response(sid, response)
        progress_pct = int(status.done_progress * 100)
        logger.info("[%s] %s (%d%%)", label, status.dispatch_state, progress_pct)

        for message in status.messages:
            logger.warning("[%s] Splunk: %s", label, message)

        if status.is_failed:
            raise SplunkJobError(
                f"[{label}] Job {sid} failed — state: '{status.dispatch_state}'. "
                f"Messages: {status.messages}"
            )
        if status.is_done:
            logger.info("[%s] Job completed.", label)
            return

        time.sleep(config.job_poll_interval)
        elapsed += config.job_poll_interval

    raise SplunkTimeoutError(
        f"[{label}] Job {sid} did not complete within {config.job_max_wait}s. "
        "Increase SPLUNK_JOB_MAX_WAIT in .env or simplify the query."
    )


def _fetch_results(client: SplunkClient, sid: str, label: str) -> SearchResults:
    endpoint = f"/services/search/jobs/{sid}/results"
    all_results = []
    fields = []
    offset = 0

    while True:
        try:
            response = client.get(endpoint, params={
                "output_mode": "json",
                "count": _RESULTS_PAGE_SIZE,
                "offset": offset,
            })
        except Exception as exc:
            raise SplunkResultsError(f"[{label}] Failed to fetch results: {exc}") from exc

        page = SearchResults.from_api_response(sid, response)
        if not page.results:
            break
        all_results.extend(page.results)
        if not fields:
            fields = page.fields
        if len(page.results) < _RESULTS_PAGE_SIZE:
            break
        offset += _RESULTS_PAGE_SIZE

    logger.info("[%s] Total fetched: %d", label, len(all_results))
    return SearchResults(sid=sid, total_results=len(all_results), results=all_results, fields=fields)


def _save_results_to_csv(results: SearchResults, results_dir: str, label: str) -> str:
    os.makedirs(results_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_label = "".join(c if (c.isalnum() or c in "-_") else "_" for c in label)
    filepath = os.path.abspath(os.path.join(results_dir, f"{safe_label}_{timestamp}.csv"))

    if not results.results:
        logger.warning("[%s] No results — writing empty CSV: %s", label, filepath)
        open(filepath, "w").close()
        return filepath

    fieldnames = results.fields or list(results.results[0].keys())
    with open(filepath, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results.results)

    return filepath
