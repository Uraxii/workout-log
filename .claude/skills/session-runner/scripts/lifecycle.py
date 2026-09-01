"""Session lifecycle: the commands phase 2 left as Notes rows (build-plan
s2 rules L7, L9, L11, L14-L17): `note <text>`,
`undo`, `fix set <n> <correction>`, `fix <date> set <n> <correction>`
(L15's 7-day backfill), a rest-node acknowledgement (`done` / `as planned`
/ `skip` / `rest`, L17), and `done for today` (L11, closes the session).
Phase 4 adds `try_today` and `try_swap`, and teaches the rest ack to
advance `program_cursor` when today really is a rest day. Opening a
session (L1, L3, L4) and L11's `open -> abandoned` half live in
`session_open.py` (house limit split by domain).

Each `try_*` function returns a `Turn`-shaped dict or `None` if the line
does not match; `log_set.py` tries them in order before falling to grammar
parsing. Pure functions of `(text, state, ctx)`, no I/O, same discipline as
`log_set.py`. `ctx` carries the values `log_set.py` already resolved this
turn (`session_id`, `session_key`, `now`, `message_id`, `units`) so these
handlers never re-derive them.
"""

from __future__ import annotations

import re
from datetime import date
from typing import Any

import program as program_lib
import rows as row_shapes

FIX_BACKFILL_WINDOW_DAYS = 7  # rule L15
_ACK_WORDS = {"done", "as planned", "skip", "rest"}
_FIX_SET_RE = re.compile(r"^fix set (\d+)[,:]?\s+(.+)$", re.IGNORECASE)
_FIX_DATE_RE = re.compile(r"^fix (\d{4}-\d{2}-\d{2}) set (\d+)[,:]?\s+(.+)$", re.IGNORECASE)
_NOTE_RE = re.compile(r"^note[,:]?\s+(.+)$", re.IGNORECASE)


def try_note(text: str, state: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any] | None:
    """`note <text>`: a Notes row scoped to the session, short-circuited
    before grammar parsing so a number inside the note is never misread as
    a set (rung 5 already does this for unparsable text; this is the same
    shape for text an author flagged explicitly)."""
    match = _NOTE_RE.match(text)
    if match is None:
        return None
    confirm = f"Noted: {match.group(1)}"
    payload = {"Session": ctx["session_id"], "Timestamp": ctx["now"], "Notes": match.group(1),
              "attempt": 0, "write_key": row_shapes.write_key(ctx["session_key"], ctx["message_id"], 0, 0),
              "source_message_id": ctx["message_id"], "Pain flag": "none", "confirm_line": confirm}
    writes = [{"verb": "row-create", "target": "Sets", "payload": payload}]
    return {"writes": writes, "confirm_line": confirm, "state": state}


def try_rest_ack(text: str, state: dict[str, Any]) -> dict[str, Any] | None:
    """L17: rest ack, no set written. Phase 4: only advances
    `program_cursor` when the node it points at actually has no blocks, so
    the same words used generically elsewhere never skip a work day."""
    if text.lower() not in _ACK_WORDS:
        return None
    program = state.get("program")
    if program is not None:
        node = program_lib.current_node(program, program_lib.ensure_cursor(state))
        if not node["blocks"]:
            program_lib.advance_once(state)
            nxt = program_lib.current_node(program, state["program_cursor"])
            return {"writes": [], "confirm_line": f"Rest day logged. Next: {nxt['label']}.", "state": state}
    return {"writes": [], "confirm_line": "Rest day logged.", "state": state}


def try_done_for_today(text: str, state: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any] | None:
    """L11: `open -> closed`, merged into the open `Sessions` row. Phase 4:
    also this program's advance point; `advance_once` guards against a
    rest-day ack in the same session advancing twice."""
    if text.lower() != "done for today":
        return None
    writes = [{"verb": "row-create", "target": "Sessions",
              "payload": {"Status": "closed", "End time": ctx["now"]}}]
    by_date = dict(state.get("sessions_by_date", {}))
    entry = by_date.get(ctx["now"][:10])
    if entry is not None:
        by_date[ctx["now"][:10]] = {**entry, "status": "closed"}
    state.update(session_id=None, sessions_by_date=by_date)
    if state.get("program") is not None:
        program_lib.advance_once(state)
    return {"writes": writes, "confirm_line": "Session closed. Nice work today.", "state": state}


def try_undo(text: str, state: dict[str, Any]) -> dict[str, Any] | None:
    """L16: undoes the most recently written row, verbatim Notes included.
    No delete verb exists (build-plan s6), so undo merges `stale: true`
    into that row by its own `write_key` (writer.py's upsert, defect 1's
    mechanism reused) and, for a set, rewinds its exercise's cursor so the
    next real write at that slot supersedes it in place."""
    last = state.get("last_write")
    if text.lower() != "undo" or last is None:
        return None
    writes = [{"verb": "row-create", "target": "Sets",
              "payload": {"write_key": last["write_key"], "stale": True}}]
    cursor = dict(state.get("cursor", {}))
    if last.get("exercise_id") is not None:
        cursor[last["exercise_id"]] = last["set_index"]
    state.update(cursor=cursor, last_write=None)
    return {"writes": writes, "confirm_line": "Undid the last entry.", "state": state}


def try_fix_set(text: str, state: dict[str, Any], ctx: dict[str, Any],
                resolve) -> dict[str, Any] | None:
    """`fix set <n> <correction>` (L7, L14): a fix on an occupied slot
    writes `attempt + 1` and supersedes; the superseded row is flagged
    `stale`. `resolve(text) -> entry|None` re-parses the correction against
    the current scope's exercise, same grammar path as a normal set."""
    match = _FIX_SET_RE.match(text)
    if match is None or ctx.get("exercise_id") is None:
        return None
    set_index, correction = int(match.group(1)), match.group(2)
    result = resolve(correction)
    if result is None:
        return None
    attempts = dict(state.get("attempts", {}))
    slot = f"{ctx['exercise_id']}:{set_index}"
    old_attempt = attempts.get(slot, 0)
    new_attempt = old_attempt + 1
    row = result["entry"]["rows"][0]
    confirm = f"Fixed set {set_index}: now {row_shapes.magnitudes_text(result['measure'], row)}."
    old_key = row_shapes.write_key(ctx["session_key"], ctx["exercise_id"], set_index, old_attempt)
    new_key = row_shapes.write_key(ctx["session_key"], ctx["exercise_id"], set_index, new_attempt)
    stale_write = {"verb": "row-create", "target": "Sets", "payload": {"write_key": old_key, "stale": True}}
    new_payload = {"Session": ctx["session_id"], "Exercise": ctx["exercise_id"], "Set index": set_index,
                  "Set type": "working", "Timestamp": ctx["now"], "Side": "both", **row,
                  "attempt": new_attempt, "write_key": new_key, "source_message_id": ctx["message_id"],
                  "Pain flag": "none", "confirm_line": confirm}
    new_write = {"verb": "row-create", "target": "Sets", "payload": new_payload}
    attempts[slot] = new_attempt
    state.update(attempts=attempts)
    return {"writes": [stale_write, new_write], "confirm_line": confirm, "state": state}


def try_fix_backfill(text: str, state: dict[str, Any], ctx: dict[str, Any],
                     resolve) -> dict[str, Any] | None:
    """`fix <date> set <n> <correction>` (L15): release 1's only backfill,
    targeting a named prior session within 7 days. Writes into that
    session's identity, not the current one; `attempt` starts at 0 there,
    since a backfill fills a slot never logged, not one being corrected."""
    match = _FIX_DATE_RE.match(text)
    if match is None:
        return None
    target_date, set_index, correction = match.group(1), int(match.group(2)), match.group(3)
    age_days = (date.fromisoformat(ctx["now"][:10]) - date.fromisoformat(target_date)).days
    if age_days < 0 or age_days > FIX_BACKFILL_WINDOW_DAYS:
        return {"writes": [], "confirm_line": f"{target_date} is outside the 7-day fix window.",
                "state": state}
    session = state.get("sessions_by_date", {}).get(target_date)
    if session is None or ctx.get("exercise_id") is None:
        return {"writes": [], "confirm_line": f"No session on {target_date} to fix.", "state": state}
    result = resolve(correction)
    if result is None:
        return None
    row = result["entry"]["rows"][0]
    confirm = f"Backfilled {target_date} set {set_index}: {row_shapes.magnitudes_text(result['measure'], row)}."
    key = row_shapes.write_key(session["session_key"], ctx["exercise_id"], set_index, 0)
    payload = {"Session": session["session_id"], "Exercise": ctx["exercise_id"], "Set index": set_index,
              "Set type": "working", "Timestamp": ctx["now"], "Side": "both", **row, "attempt": 0,
              "write_key": key, "source_message_id": ctx["message_id"], "Pain flag": "none",
              "confirm_line": confirm}
    writes = [{"verb": "row-create", "target": "Sets", "payload": payload}]
    return {"writes": writes, "confirm_line": confirm, "state": state}
