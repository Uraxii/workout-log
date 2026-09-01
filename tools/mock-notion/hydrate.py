"""Turn-1 state reconstruction: rebuild a chat's `state` from reads alone.

The seam is a pure function of `(line, state)` by contract
(docs/architecture.md "The script seam"), so producing `state` is the
CALLER's job, never a seam's: the LLM in production, `replay.py` in a
fixture. That is why no skill script changes to support a cold start, and
why this module lives in the harness rather than under `.claude/skills/`.

Read order is fixed and each read is issued once, so `expected.tsv` asserts
the hydration sequence itself, not just its result.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from reader import MockNotionReader

_SKILLS_DIR = Path(__file__).resolve().parents[2] / ".claude" / "skills"
sys.path.insert(0, str(_SKILLS_DIR / "program-design" / "scripts"))
sys.path.insert(0, str(_SKILLS_DIR / "session-runner" / "scripts"))

import program as program_lib  # noqa: E402  (owns the cursor contract)
import program_page  # noqa: E402  (owns the `program/current` round trip)
import rows as row_shapes  # noqa: E402  (owns the client-side session key)

DEFAULT_UNITS = "lb"


def hydrate(reader: MockNotionReader) -> dict[str, Any]:
    """Every state key a cold chat's first turn needs, read back from the
    store. A page or database that was never written yields the same empty
    value the seams already default to, so turn 1 of a genuinely empty
    workspace hydrates without a single special case."""
    state: dict[str, Any] = {
        "units": reader.config_read("config/preferences").get("units", DEFAULT_UNITS),
        # `trainer_core` reads `limits.clearance`, `load_adjust` reads
        # `limits.progression`, `pain_triage` reads `limits.entries`.
        "limits": reader.config_read("config/limits"),
        "athlete": reader.config_read("config/athlete"),
    }
    page = program_page.read_page(reader.config_read("program/current"))
    state["has_program"] = page is not None

    catalog = {
        row["Name"]: {"id": row["page_id"], "measure": row.get("measure")}
        for row in reader.row_query("Exercises")
    }
    state["catalog"] = catalog
    state["exercise_seq"] = len(catalog)

    state.update(_session_state(reader))
    state.update(_program_state(reader, page))
    state.update(_EMPTY_AFTER_COLD)
    return state


# What a cold chat genuinely has none of, at the values `log_set.py` reads
# them back with (`state.get(key, default)` at log_set.py:59-63).
#
# ponytail: `last_write` (rule L16's `undo` target) and `attempts`
# (`lifecycle.try_fix_set`'s per-slot counter) stay absent on purpose.
# `undo` means "the row I just wrote", and across a chat boundary there is
# no such row: the previous chat's last write is not this chat's undo
# target. Reconstructing either would invent an intent the athlete never
# expressed in this chat.
_EMPTY_AFTER_COLD = {
    "carry": {},
    "scope": None,
    "targets": {},
    "last_greyband": None,
}


def _session_state(reader: MockNotionReader) -> dict[str, Any]:
    """Session identity and the open session's set cursor, from two reads of
    `Sessions` plus (only when one is open) one of `Sets`."""
    sessions = reader.row_query("Sessions")
    open_rows = reader.row_query("Sessions", {"Status": "open"})
    open_row = open_rows[-1] if open_rows else None
    return {
        "session_seq": len(sessions),
        # ponytail: no key in `config_pages` records the athlete's timezone;
        # the stored `Sessions.Timezone` (rule L3, frozen at open) is its
        # only record anywhere, so the last session's zone is the only thing
        # a cold chat can carry forward. A real gap in the schema, named
        # here rather than papered over with an invented config key.
        "tz": (sessions[-1].get("Timezone") or "") if sessions else "",
        "sessions_by_date": _sessions_by_date(sessions),
        "session_id": open_row["page_id"] if open_row else None,
        "session_status": open_row["Status"] if open_row else None,
        "cursor": _cursor(reader, open_row),
    }


def _sessions_by_date(sessions: list[dict[str, Any]]) -> dict[str, Any]:
    """The shape `session_open.open_session` and `lifecycle.try_fix_backfill`
    read (rule L15's 7-day window resolves a date to a session through it):
    `{date: {"session_id", "session_key", "status"}}`. `session_key` is
    derived, not stored: it is `sha256(Start time|Timezone)` by construction
    (defect 2), so the two frozen open fields regenerate it exactly."""
    by_date = {}
    for row in sessions:
        local_date, start = row.get("Date"), row.get("Start time")
        if local_date is None or start is None:
            continue
        by_date[local_date] = {
            "session_id": row["page_id"],
            "session_key": row_shapes.session_key(start, row.get("Timezone") or ""),
            "status": row.get("Status"),
        }
    return by_date


def _cursor(reader: MockNotionReader, open_row: dict[str, Any] | None) -> dict[str, int]:
    """The NEXT `Set index` per exercise, which is the value `log_set.py`
    stores (`cursor[exercise_id] = last_index + 1`) and reads back
    (`cursor.get(exercise_id, 1)`), so the max stored index plus one.

    No open session means no cursor and no query: `Set index` is scoped to
    `(session, exercise)` (rule L7), so a closed session's indices would
    mislabel set 1 of the next session as a continuation."""
    if open_row is None:
        return {}
    cursor: dict[str, int] = {}
    for row in reader.row_query("Sets", {"Session": open_row["page_id"]}):
        exercise_id, set_index = row.get("Exercise"), row.get("Set index")
        if exercise_id is None or set_index is None:
            continue
        cursor[exercise_id] = max(cursor.get(exercise_id, 0), set_index + 1)
    return cursor


def _closed_since(reader: MockNotionReader, started_at: str) -> int:
    """How many sessions THIS program has consumed: the closed ones that
    also STARTED at or after it was picked. `Start time` is frozen at open
    (rule L3), so it is the field that says which program a session ran
    under; a session opened under the old program and closed after the new
    one was picked belongs to the old one and is not counted.

    Counting every closed session in the workspace instead is what made a
    second program start its rotation wherever the first left off
    (workout-log-ayf.15). `row_query` matches exactly and has no ranges, so
    the comparison is the caller's, on ISO timestamps that sort lexically.
    An empty `started_at` (a program picked with no clock) counts
    everything, which is the old behaviour and the only sane reading of
    "since always"."""
    closed = reader.row_query("Sessions", {"Status": "closed"})
    return sum(1 for row in closed if (row.get("Start time") or "") >= started_at)


def _program_state(reader: MockNotionReader,
                   page: program_page.ProgramPage | None) -> dict[str, Any]:
    """The active template, its id, when it started, and where the rotation
    stands. `read_page` already refused a body that is missing, malformed or
    from another format version, so there is nothing to repair here: no
    usable page means no active program, and the next turn picks one."""
    if page is None:
        return {"program": None, "program_id": None, "program_cursor": None,
                "program_started_at": ""}
    return {
        "program": page.program,
        "program_id": page.template_id,
        "program_started_at": page.started_at,
        "program_cursor": program_lib.cursor_after(
            page.program, _closed_since(reader, page.started_at)),
    }
