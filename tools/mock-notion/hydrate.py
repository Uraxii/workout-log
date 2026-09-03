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

import json
import sys
from pathlib import Path
from typing import Any

from from_sets import known_exercises, set_cursor
from reader import MockNotionReader

_SKILLS_DIR = Path(__file__).resolve().parents[2] / ".claude" / "skills"
sys.path.insert(0, str(_SKILLS_DIR / "program-design" / "scripts"))
sys.path.insert(0, str(_SKILLS_DIR / "session-runner" / "scripts"))
sys.path.insert(0, str(_SKILLS_DIR / "intake" / "scripts"))

import program as program_lib  # noqa: E402  (owns the cursor contract)
import program_page  # noqa: E402  (owns the `program/current` round trip)
import rows as row_shapes  # noqa: E402  (owns the client-side session key)
import storage  # noqa: E402  (owns is_proven/refusal, the cold-start gate)

DEFAULT_UNITS = "lb"


def hydrate(reader: MockNotionReader) -> dict[str, Any]:
    """Every state key a cold chat's first turn needs, read back from the
    store. A page or database that was never written yields the same empty
    value the seams already default to, so turn 1 of a genuinely empty
    workspace hydrates without a single special case."""
    preferences = reader.config_read("config/preferences")
    units = preferences.get("units", DEFAULT_UNITS)
    # `trainer_core` reads `limits.clearance`, `load_adjust` reads
    # `limits.progression`, `pain_triage` reads `limits.entries`.
    limits = reader.config_read("config/limits")
    athlete = reader.config_read("config/athlete")
    storage_platform = athlete.get("storage_platform")
    if storage_platform is not None and not storage.is_proven(storage_platform):
        # Gate 2 of two (docs/storage-section-design.md "Refusing a
        # store"). `None` means the question has not been asked yet, which
        # is not a refusal; a named, unproven store stops every skill's
        # cold start here, not just intake's, because hydrate.py is the
        # one chokepoint every cold turn already routes through.
        raise RuntimeError(storage.refusal(storage_platform))
    state: dict[str, Any] = {
        "units": units,
        # The gym's plates, read by `loads.increment_for`. Was `Locations`.
        "preferences": preferences,
        "limits": limits,
        "athlete": athlete,
        # What `intake` asked for and wrote (ticket workout-log-mqs). The
        # creates need the page id, and each one's returned data source id
        # is named by the next database's relation columns; no read verb
        # answers "which databases exist", so `intake` persists the ids the
        # caller handed it and they come back from the page.
        "notion_parent_page_id": athlete.get("notion_parent_page_id"),
        "databases": json.loads(athlete.get("notion_data_sources") or "{}"),
    }
    program_body = reader.config_read("program/current")
    page = program_page.read_page(program_body)
    state["has_program"] = page is not None
    state["progression"] = json.loads(program_body.get("progression") or "{}")

    # ponytail: every `Sets` row, unfiltered, so it grows with the log.
    # `row_query` has no ranges; add one and filter on `Timestamp` when this
    # gets slow.
    logged = reader.row_query("Sets")
    state["known"] = known_exercises(logged)

    state.update(_session_state(reader, athlete, logged))
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


def _session_state(reader: MockNotionReader, athlete: dict[str, Any],
                   logged: list[dict[str, Any]]) -> dict[str, Any]:
    """Session identity and the open session's set cursor, from two reads of
    `Sessions` plus the `Sets` rows already in hand."""
    sessions = reader.row_query("Sessions")
    open_rows = reader.row_query("Sessions", {"Status": "open"})
    open_row = open_rows[-1] if open_rows else None
    last_zone = (sessions[-1].get("Timezone") or "") if sessions else ""
    return {
        "session_seq": len(sessions),
        # `intake` asks for the zone and writes it to `config/athlete`
        # (ticket workout-log-ayf.16). Before that key existed, the frozen
        # `Sessions.Timezone` (rule L3) was its only record anywhere, so an
        # install whose first session had not opened yet had nothing to
        # carry and froze an empty zone onto session 1. A workspace set up
        # before the question existed still has only the last session's
        # zone, which is what that fallback is for.
        "tz": athlete.get("timezone") or last_zone,
        "sessions_by_date": _sessions_by_date(sessions),
        "session_id": open_row["page_id"] if open_row else None,
        "session_status": open_row["Status"] if open_row else None,
        "cursor": set_cursor(logged, open_row),
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
