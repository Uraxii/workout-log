"""The seam for `intake`: `intake_turn(line, state) -> Turn` (build-plan s5,
s9), same shape as `log_set` and `screen_turn`:

    python3 intake.py                 # {"line":..., "state":...} on stdin, Turn on stdout
    from intake import intake_turn    # in-process, from the replay runner

This module shapes writes. The ordered question table, the cursor over it,
and whether a chat line answers the step in force live in `questions.py`
(docs/architecture.md "One script per skill": split by domain, never by
execution step). Safety runs first as seven PAR-Q+ items plus one
conditional follow-up, delegated in-process to `screen`
(`.claude/skills/screen/scripts/screen.py`) so the questions and the
clearance-write rule (S8) live in one place.

`intake_cursor` is the flat index into `questions.ALL_IDS`, written to
`config/athlete` after every turn (lim L-48). A line is scanned against
every not-yet-answered global field first (lim L-47): a match writes it and
marks it answered, so its own turn is skipped with a one-clause
acknowledgement instead of asked again.
"""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Any, TypedDict

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "screen" / "scripts"))
import screen  # noqa: E402  (skill-to-skill seam import, mirrors replay.py's own sys.path use)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ddl  # noqa: E402  (same-dir renderer; the dir name is not importable)
import questions  # noqa: E402  (same-dir table; the dir name is not importable)

TRIGGER_RE = re.compile(r"\bset\s*me\s*up\b", re.IGNORECASE)
DONE_SAY = 'All set. Say "what do I have today" to start.'


class Write(TypedDict):
    verb: str
    target: str
    payload: dict[str, Any]


class Turn(TypedDict):
    writes: list[Write]
    say: str
    state: dict[str, Any]


def _config_write(page: str, key: str, value: Any) -> Write:
    return {"verb": "config-write", "target": page, "payload": {key: value}}


def _answer_writes(step_id: str, line: str, value: Any,
                   state: dict[str, Any], now: str) -> list[Write]:
    """The writes one parsed answer earns, and the answer's mark in `ist`.

    PAR-Q+ earns nothing until the pass completes: all seven NO writes
    clearance straight away, any YES defers it to the follow-up turn. Rule
    S8 keeps that decision in `clearance.py`, reached through `screen`.

    A row carrying `state_key` also lands its answer on `state`, because
    the parent page id and the timezone are read by the rest of this same
    turn and the next one (`ddl.next_create_write`, `session_open`) rather
    than only by a later chat reading the page back.
    """
    ist = state["intake"]
    ist["answers"][step_id] = value
    if step_id == "parq_followup":
        return [screen.clearance_write(True, line, now)]
    if step_id in questions.SAFETY_IDS:
        ist["any_yes"] = ist["any_yes"] or bool(value)
        if step_id == "parq_7" and not ist["any_yes"]:
            ist["answers"]["parq_followup"] = "n/a"
            return [screen.clearance_write(False, "", now)]
        return []

    step = questions.FIELD_BY_ID[step_id]
    if step.get("state_key"):
        state[step["state_key"]] = value
    if step.get("location"):
        writes: list[Write] = [{"verb": "row-create", "target": "Locations",
                                "payload": {"Name": value}}]
    else:
        writes = [_config_write(step["page"], step["key"], value)]
    for other, found in questions.volunteered(line, ist["answers"], step_id):
        ist["answers"][other["id"]] = found
        writes.append(_config_write(other["page"], other["key"], found))
    return writes


def _data_source_writes(state: dict[str, Any], ist: dict[str, Any]) -> list[Write]:
    """Persist the data source ids the caller threaded back into
    `state["databases"]`, whenever they changed.

    No read verb answers "which databases exist", so a later cold chat has
    nowhere else to learn it (ticket workout-log-mqs); `hydrate.py` reads
    this key back. Written from what the creates actually returned, never
    from a guess at the id.
    """
    ids = state.get("databases") or {}
    encoded = json.dumps(ids, sort_keys=True)
    if not ids or ist.get("data_sources") == encoded:
        return []
    ist["data_sources"] = encoded
    return [_config_write("config/athlete", "notion_data_sources", encoded)]


def intake_turn(line: str, state: dict[str, Any]) -> Turn:
    state = copy.deepcopy(state)
    ist = state.get("intake", {"cursor": 0, "answers": {}, "any_yes": False})
    state["intake"] = ist
    now = state.get("now", "")

    # One database per turn until all four exist, on every turn and not only
    # the trigger turn, so the question flow is not stalled behind setup.
    writes: list[Write] = _data_source_writes(state, ist)
    writes += ddl.next_create_write(state)

    if TRIGGER_RE.search(line):
        # First "set me up" starts the creates and starts asking. A later one
        # (interruption, or a curious re-run) adopts what exists (idempotent
        # at the writer) and resumes at `intake_cursor` instead of restarting
        # (lim L-48).
        idx, acks = questions.advance(ist["answers"], ist["cursor"])
        ist["cursor"] = idx
        return {"writes": writes, "say": _say(acks, idx), "state": state}

    idx = ist["cursor"]
    if idx >= len(questions.ALL_IDS):
        return {"writes": writes, "say": DONE_SAY, "state": state}

    step_id = questions.ALL_IDS[idx]
    value = questions.parse(step_id, line)
    if value is None:
        # The one re-ask rule, for every row of the table (ticket
        # workout-log-481). An answer that did not parse re-enters its own
        # step: the cursor does not move, nothing is written for it, and no
        # step needs a retry branch of its own.
        return {"writes": writes, "say": questions.reask_for(step_id), "state": state}

    refuse = questions.FIELD_BY_ID.get(step_id, {}).get("refuse")
    refusal_text = refuse(value) if refuse else None
    writes += _answer_writes(step_id, line, value, state, now)
    if refusal_text is not None:
        # A row can opt into this generically (same shape as `state_key`
        # and `location`): the answer is still recorded above, so she is
        # never asked the question from scratch, but the cursor does not
        # move, so the same step catches her correction
        # (docs/storage-section-design.md "Refusing a store").
        return {"writes": writes, "say": refusal_text, "state": state}

    next_idx, acks = questions.advance(ist["answers"], idx + 1)
    ist["cursor"] = next_idx
    writes.append(_config_write("config/athlete", "intake_cursor", str(next_idx)))
    return {"writes": writes, "say": _say(acks, next_idx), "state": state}


def _say(acks: list[str], idx: int) -> str:
    """Skipped-question acknowledgements, then the next question, or the
    closing line once the table runs out."""
    tail = questions.prompt_for(questions.ALL_IDS[idx]) if idx < len(questions.ALL_IDS) else DONE_SAY
    return " ".join(acks + [tail])


def main() -> int:
    request = json.load(sys.stdin)
    json.dump(intake_turn(request["line"], request.get("state", {})), sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
