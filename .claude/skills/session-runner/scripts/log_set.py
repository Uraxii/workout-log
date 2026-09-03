"""The seam: one chat line plus state in, row payloads plus confirm line out.

Deterministic and pure of Notion/LLM I/O, so a fixture replays it with no
LLM and no Notion. The agent does the conversation; this does the parse
(`grammar.py`, `tokens.py`, `measures.py`), the exercise lookup
(`ladder.py`, `catalog.py`), the lifecycle and program-cursor commands
(`lifecycle.py`, `program.py`), the row shaping (`rows.py`), what a resolved
line writes (`entries.py`) and rule S2's halted check (`preconditions.py`).

    python3 log_set.py            # {"line":..., "state":...} on stdin, Turn on stdout
    from log_set import log_set   # in-process, from the replay runner

`state` (JSON, threaded turn to turn): `tz`/`units`, `catalog`, `scope`,
`carry`, `targets`, `cursor`, `session_id`/`session_key`, `open_date`,
`sessions_by_date`, `attempts`, `last_write`, `program` (program-design's
template, unchanged), `program_cursor` (`program.py`, L17/L18),
`readiness_pending` (L2), `finish_or_advance` (L11, `session_open.py`). L9's
retype guard is a caller call content alone cannot answer; `replay.py`'s
`@resend` represents it, and `write_key` dedup then makes it a no-op.
"""

from __future__ import annotations

import copy
import json
import re
import sys
from typing import Any, Literal, TypedDict

import bounds
import catalog
import entries
import ladder
import lifecycle
import preconditions
import session_open
import titles
import program as program_lib
import rows as row_shapes


class Write(TypedDict):
    verb: Literal["row-create", "config-write"]
    target: str
    payload: dict[str, Any]


class Turn(TypedDict):
    writes: list[Write]
    confirm_line: str
    state: dict[str, Any]


def log_set(line: str, state: dict[str, Any]) -> Turn:
    """The seam. Every turn leaves through here, so three cross-cutting
    passes run here, on the turn's own writes rather than the line, so none
    depends on which handler produced them: rule S2, a halted session takes
    no set writes (`preconditions.py`, build-plan s6.1 S2, rule L12); an
    implausible magnitude is refused, never written (`bounds.py`,
    `docs/unit-and-magnitude-model.md` s4, `workout-log-ayf.3`); and every
    surviving `Sets` row gets its Notion title (`titles.py`,
    `workout-log-4sc`)."""
    turn = preconditions.no_sets_while_halted(_run_turn(line, state), state)
    return titles.name_every_set(bounds.reject_implausible_writes(turn, state), state)


def _run_turn(line: str, state: dict[str, Any]) -> Turn:
    """An unparseable line still returns a write (rung 5), never an empty turn."""
    state = copy.deepcopy(state)
    now, message_id, units = state["now"], state["message_id"], state.get("units", "lb")
    catalog_map = state.get("catalog", {})
    text = line.strip()
    # L11: "advance" answers a pending ask; anything else is an implicit "finish".
    pending_advance = state.pop("finish_or_advance", None)
    if pending_advance is not None and text.lower() == "advance":
        return session_open.try_advance(state, pending_advance, now)

    writes: list[Write] = []
    # Read after open_session: a genuinely new session resets `cursor` (L7).
    session_id, session_key, session_seq, is_new, just_armed = session_open.open_session(state, writes, now)
    cursor = state.get("cursor", {})
    carry = state.get("carry", {})
    targets = state.get("targets", {})
    scope = tuple(state["scope"]) if state.get("scope") else None
    last_greyband = state.get("last_greyband")
    ctx = {"session_id": session_id, "session_key": session_key, "now": now,
          "message_id": message_id, "units": units, "exercise_id": scope[0] if scope else None}

    def _finish(turn: Turn) -> Turn:
        return session_open.with_open_prompts(turn, state, is_new, just_armed)

    # Only before scope exists; after that a bare 1-5 is rule D's reps (lim L-49).
    if state.pop("readiness_pending", False) and scope is None and re.fullmatch(r"[1-5]", text):
        writes.append({"verb": "row-create", "target": "Sessions", "payload": {"Readiness": int(text)}})
        return _finish({"writes": writes, "confirm_line": "Noted.", "state": state})

    if text.lower() == "fix" and last_greyband is not None:
        return _finish(entries.apply_greyband_fix(state, writes, last_greyband, session_id,
                                                  session_key, now, message_id))

    lookup = catalog.make_lookup(catalog_map)
    implicit = [(info["id"], info["measure"]) for info in catalog_map.values()]

    def resolve(entry_text: str):
        return ladder.resolve(entry_text, scope, lookup, units, carry.get(scope[0]) if scope else None,
                              targets.get(scope[0]) if scope else None, implicit)

    for handler, needs_resolve in ((lifecycle.try_note, False), (program_lib.try_today, False),
                                   (lifecycle.try_rest_ack, "state_only"), (program_lib.try_swap, "lookup"),
                                   (lifecycle.try_done_for_today, False), (lifecycle.try_undo, "state_only"),
                                   (lifecycle.try_fix_set, True), (lifecycle.try_fix_backfill, True)):
        result = _dispatch(handler, needs_resolve, text, state, ctx, resolve, lookup)
        if result is not None:
            result["writes"] = writes + result["writes"]
            return _finish(result)

    result = resolve(text)
    created_payload = None
    if result is None:
        result = ladder.resolve_create(text, units)
        if result is not None:
            created_payload = catalog.new_row_payload(result["name"], result["measure"])

    if result is None:
        return _finish(entries.notes_fallback(state, writes, line, session_id, session_key, message_id, now))

    return _finish(entries.log_entry(state, writes, result, created_payload, catalog_map, cursor,
                                     carry, targets, session_id, session_key, now, message_id, units))


def _dispatch(handler, needs_resolve, text, state, ctx, resolve, lookup):
    if needs_resolve == "state_only":
        return handler(text, state)
    if needs_resolve == "lookup":
        return handler(text, state, ctx, lookup)
    if needs_resolve is True:
        return handler(text, state, ctx, resolve)
    return handler(text, state, ctx)


def main() -> int:
    request = json.load(sys.stdin)
    json.dump(log_set(request["line"], request.get("state", {})), sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
