"""
spl_knowledge.py
----------------
Loads and indexes the SPL reference documentation into a searchable
knowledge base used by the validator and optimizer.

The knowledge base is built once at import time from the Markdown docs
in the spl_docs/ directory. It provides:

  - VALID_COMMANDS     : set of all known SPL commands (from doc filenames)
  - GENERATING_CMDS    : commands that generate results (start of pipeline)
  - TRANSFORMING_CMDS  : commands that transform the result set
  - STREAMING_CMDS     : distributable/centralized streaming commands
  - EXPENSIVE_CMDS     : commands known to be slow or resource-intensive
  - COMMAND_DOCS       : dict mapping command -> doc text (for optimizer)
  - get_command_doc()  : fetch full doc text for a command

The spl_docs/ directory is resolved relative to this file so it works
from any working directory.
"""

import os
import re
import logging
from typing import Dict, Set

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Locate spl_docs/ relative to this file — path-agnostic
# ---------------------------------------------------------------------------
_HERE     = os.path.dirname(os.path.abspath(__file__))
_DOCS_DIR = os.path.join(os.path.dirname(_HERE), "spl_docs")


# ---------------------------------------------------------------------------
# Internal loaders
# ---------------------------------------------------------------------------

# Hardcoded fallback — full SPL 10.2 command list from the reference docs.
# Used when spl_docs/ directory is not present so the validator still works.
_BUILTIN_COMMANDS: Set[str] = {
    "abstract","accum","addcoltotals","addinfo","addtotals","analyzefields",
    "anomalies","anomalousvalue","anomalydetection","append","appendcols",
    "appendpipe","arules","associate","autoregress","bin","bucket","bucketdir",
    "chart","cluster","cofilter","collect","concurrency","contingency","convert",
    "correlate","ctable","datamodel","datamodelsimple","dbinspect","dbxquery",
    "dedup","delete","delta","diff","entitymerge","erex","eval","eventcount",
    "eventstats","extract","fieldformat","fields","fieldsummary","filldown",
    "fillnull","findtypes","folderize","foreach","format","from","fromjson",
    "gauge","gentimes","geom","geomfilter","geostats","head","highlight",
    "history","iconify","ingestpreview","inputcsv","inputintelligence",
    "inputlookup","iplocation","join","kmeans","kvform","loadjob","localize",
    "localop","lookup","makecontinuous","makemv","makeresults","map","mcollect",
    "metadata","metasearch","meventcollect","mpreview","msearch","mstats",
    "multikv","multisearch","mvcombine","mvexpand","nomv","outlier","outputcsv",
    "outputlookup","outputtext","overlap","pivot","predict","rangemap","rare",
    "regex","reltime","rename","replace","require","rest","return","reverse",
    "rex","rtorder","run","savedsearch","script","scrub","search","searchtxn",
    "selfjoin","sendalert","sendemail","set","setfields","sichart","sirare",
    "sistats","sitimechart","sitop","snowevent","snoweventstream","snowincident",
    "snowincidentstream","sort","spath","stats","strcat","streamstats","table",
    "tags","tail","timechart","timewrap","tojson","top","transaction","transpose",
    "trendline","tscollect","tstats","typeahead","typelearner","typer","union",
    "uniq","untable","walklex","where","x11","xmlkv","xmlunescape","xpath","xyseries",
}


def _load_command_list() -> Set[str]:
    """
    Builds the complete set of valid SPL commands.

    When spl_docs/ is present: loads from doc filenames (159 commands).
    When spl_docs/ is absent:  falls back to _BUILTIN_COMMANDS so the
    validator works correctly regardless of whether the docs are bundled.
    """
    if not os.path.isdir(_DOCS_DIR):
        logger.debug(
            "spl_docs/ not found — using built-in command list (%d commands).",
            len(_BUILTIN_COMMANDS),
        )
        return set(_BUILTIN_COMMANDS)

    commands: Set[str] = set()
    for fname in os.listdir(_DOCS_DIR):
        if "_search-commands_" in fname and fname.endswith(".md"):
            cmd = fname.split("_search-commands_")[-1].replace(".md", "")
            if re.match(r"^[a-z]", cmd) and cmd != "3rd-party-custom-commands":
                commands.add(cmd)

    logger.debug("SPL knowledge base: %d commands loaded from spl_docs/.", len(commands))
    return commands

    for fname in os.listdir(_DOCS_DIR):
        if "_search-commands_" in fname and fname.endswith(".md"):
            cmd = fname.split("_search-commands_")[-1].replace(".md", "")
            if re.match(r"^[a-z]", cmd) and cmd != "3rd-party-custom-commands":
                commands.add(cmd)

    logger.debug("SPL knowledge base: %d commands loaded from docs.", len(commands))
    return commands


def _load_command_types(commands: Set[str]) -> tuple:
    """
    Reads the command-types reference doc and classifies commands into
    generating, transforming, and streaming sets.
    """
    generating:  Set[str] = set()
    transforming: Set[str] = set()
    streaming:   Set[str] = set()

    types_doc = _find_doc("command-types")
    if not types_doc:
        return generating, transforming, streaming

    text = open(types_doc, encoding="utf-8").read()

    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        cmd_raw = parts[1].split(",")[0].split(" ")[0].strip().lower()
        if cmd_raw not in commands:
            continue
        notes = parts[2].lower() if len(parts) > 2 else ""
        if "generating" in notes:
            generating.add(cmd_raw)
        if "transforming" in notes:
            transforming.add(cmd_raw)
        if "streaming" in notes:
            streaming.add(cmd_raw)

    # Hardcode well-known generating commands not always caught by regex
    generating.update({
        "tstats", "mstats", "search", "inputlookup", "inputcsv",
        "makeresults", "metadata", "datamodel", "from",
        "multisearch", "union", "gentimes", "loadjob",
    })

    return generating, transforming, streaming


def _load_all_docs(commands: Set[str]) -> Dict[str, str]:
    """Loads the full text of each command's reference doc."""
    docs: Dict[str, str] = {}
    if not os.path.isdir(_DOCS_DIR):
        return docs
    for fname in os.listdir(_DOCS_DIR):
        if "_search-commands_" in fname and fname.endswith(".md"):
            cmd = fname.split("_search-commands_")[-1].replace(".md", "")
            if cmd in commands:
                try:
                    docs[cmd] = open(
                        os.path.join(_DOCS_DIR, fname), encoding="utf-8"
                    ).read()
                except OSError:
                    pass
    return docs


def _find_doc(partial_name: str) -> str:
    """Returns full path to the first doc file matching partial_name."""
    if not os.path.isdir(_DOCS_DIR):
        return ""
    for fname in os.listdir(_DOCS_DIR):
        if partial_name in fname and fname.endswith(".md"):
            return os.path.join(_DOCS_DIR, fname)
    return ""


# ---------------------------------------------------------------------------
# Build the knowledge base at import time
# ---------------------------------------------------------------------------

VALID_COMMANDS: Set[str] = _load_command_list()

_gen, _trans, _stream = _load_command_types(VALID_COMMANDS)

GENERATING_CMDS:  Set[str] = _gen
TRANSFORMING_CMDS: Set[str] = _trans
STREAMING_CMDS:   Set[str] = _stream

# Commands that are known to be expensive / should be avoided or limited
EXPENSIVE_CMDS: Set[str] = {
    "transaction",   # Very expensive — use stats where possible
    "join",          # Expensive for large datasets — use stats/tstats
    "append",        # Runs entire subsearch — use union when possible
    "map",           # Runs one search per result — dangerous at scale
    "predict",       # ML-based — CPU intensive
    "anomalydetection",
    "x11",
}

COMMAND_DOCS: Dict[str, str] = _load_all_docs(VALID_COMMANDS)


def get_command_doc(command: str) -> str:
    """
    Returns the full reference documentation text for a SPL command.

    Args:
        command (str): Lowercase command name, e.g. 'tstats'.

    Returns:
        str: Doc text, or empty string if not found.
    """
    return COMMAND_DOCS.get(command.lower(), "")


def is_valid_command(command: str) -> bool:
    """Returns True if the command exists in the SPL reference docs."""
    return command.lower() in VALID_COMMANDS
