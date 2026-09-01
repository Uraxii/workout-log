"""The seam for `pain-triage`: `triage_turn(line, state) -> Turn` (build-plan
s6, s6.1 rules S3, S5, S8). Same shape as `log_set`, `screen_turn`,
`gate_turn`:

    python3 pain_triage.py               # {"line":..., "state":...} on stdin, Turn on stdout
    from pain_triage import triage_turn  # in-process, from the replay runner

Pain-triage writes exactly two things on a `stop`-level report: the halted
status and a dated `config/limits` entry (build-plan s6 skill table). Both
ride in one turn as two `Write` objects; the second `Write`'s payload also
sets `progression: manual` in the same `config-write` call, since a `stop`
report is exactly the PEM-style hard stop that switches automatic
progression off (research/00-synthesis-trainer.md "PEM hard stop"). A
`niggle` report writes nothing. Neither report, nor a bare "I'm fine", ever
clears `progression: manual` or resolves an entry: rule S8 gives an open
entry exactly two exits, and a bare user say-so is neither (rule S5).

`state["limits"]["entries"]`: a list of `{"area", "status", "opened_at"}`
dicts, the in-memory mirror of `config/limits.entries`, which this module
serializes to JSON on write since the schema key has no sub-structure of its
own. A chat that starts cold reads the stored STRING back instead, so
`entries()` below is the one place either shape becomes a list. Re-opening an
entry for an already-tracked area updates it in place (rule S8's "neither
exit deletes it") and resets `opened_at`, which is the 14-day window
`session-runner` will read at close.
"""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Any, TypedDict

REFERENCES = Path(__file__).resolve().parent.parent / "references" / "red-flags.md"
_TABLE_ROW_RE = re.compile(r"^\|\s*([a-z ]+?)\s*\|\s*(niggle|stop)\s*\|$", re.MULTILINE)


def _phrase_table() -> tuple[tuple[str, ...], tuple[str, ...]]:
    """S3's phrase-to-enum table, plus L-43's crash/fatigue words, parsed
    once from `references/red-flags.md` so the word lists live in exactly
    one place (mirrors `screen.py`'s `_questions()`)."""
    rows = _TABLE_ROW_RE.findall(REFERENCES.read_text())
    niggle = tuple(word for word, level in rows if level == "niggle")
    stop = tuple(word for word, level in rows if level == "stop")
    if not niggle or not stop:
        raise ValueError(f"expected niggle and stop rows in {REFERENCES}, found {rows}")
    return niggle, stop


_NIGGLE_WORDS, _STOP_WORDS = _phrase_table()
_AREA_RE = re.compile(
    r"\b(knee|ankle|shoulder|hip|back|elbow|wrist|neck|foot|calf|hamstring|groin)\b",
    re.IGNORECASE)

HALT_SAY = ("Stopping here. That's a stop-level signal ({area}). See a physician "
            "or physiotherapist before that movement again. I can still help "
            "with everything else on the plan.")
NIGGLE_SAY = "Noted, keeping an eye on it. Say if it gets worse."
NO_BARE_CLEAR_SAY = ("Good to hear, but I can't clear that on your word alone: "
                      "it needs 14 symptom-free days or a clinician's clearance.")


class Write(TypedDict):
    verb: str
    target: str
    payload: dict[str, Any]


class Turn(TypedDict):
    writes: list[Write]
    say: str
    state: dict[str, Any]


def classify(line: str) -> str:
    """S3: `stop` wins over `niggle` when a line names both."""
    low = line.lower()
    if any(word in low for word in _STOP_WORDS):
        return "stop"
    if any(word in low for word in _NIGGLE_WORDS):
        return "niggle"
    return "none"


def _area(line: str) -> str:
    match = _AREA_RE.search(line)
    return match.group(1).lower() if match else "unspecified"


def entries(limits: dict[str, Any]) -> list[dict[str, Any]]:
    """`config/limits.entries` as a list, from either shape it arrives in.

    This module owns the key, and the schema gives it no sub-structure of its
    own, so it is stored as a JSON string and mirrored in state as a list. A
    warm turn hands back the list it last wrote; a cold turn hands back what
    the config read returned, which is the string. Parse here, once, and
    every caller downstream of this function sees a list.
    """
    stored = limits.get("entries") or []
    return json.loads(stored) if isinstance(stored, str) else stored


def _reopen_entry(tracked: list[dict[str, Any]], area: str,
                  today: str) -> list[dict[str, Any]]:
    """S8: re-open on any new mention, reset the 14-day window. An existing
    entry for the area is updated in place, never removed; a new area
    appends."""
    tracked = copy.deepcopy(tracked)
    for entry in tracked:
        if entry["area"] == area:
            entry["status"] = "open"
            entry["opened_at"] = today
            return tracked
    tracked.append({"area": area, "status": "open", "opened_at": today})
    return tracked


def _halt(line: str, state: dict[str, Any]) -> Turn:
    area = _area(line)
    today = state.get("now", "")[:10]
    limits = state.get("limits", {})
    reopened = _reopen_entry(entries(limits), area, today)

    writes: list[Write] = [
        {"verb": "row-create", "target": "Sessions", "payload": {"Status": "halted"}},
        {"verb": "config-write", "target": "config/limits",
         "payload": {"entries": json.dumps(reopened),
                     "progression": "manual"}},
    ]
    state["session_status"] = "halted"
    state["limits"] = {**limits, "entries": reopened, "progression": "manual"}
    return {"writes": writes, "say": HALT_SAY.format(area=area), "state": state}


def triage_turn(line: str, state: dict[str, Any]) -> Turn:
    """One pain report. Never clears anything (rules S5, S8): the only
    writes this function ever emits are the halt writes below."""
    state = copy.deepcopy(state)
    level = classify(line)

    if level == "stop":
        return _halt(line, state)
    if level == "niggle":
        return {"writes": [], "say": NIGGLE_SAY, "state": state}

    say = NO_BARE_CLEAR_SAY if state.get("session_status") == "halted" else "Noted."
    return {"writes": [], "say": say, "state": state}


def main() -> int:
    request = json.load(sys.stdin)
    json.dump(triage_turn(request["line"], request.get("state", {})), sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
