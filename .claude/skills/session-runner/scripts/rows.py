"""`Sets` row shaping: write identity, magnitude rendering, the confirm line
and G2's grey-band reversal math. `log_set.py` owns state; this module is a
pure function of the fields already decided.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

# <skill>/data is the copy tools/package/build_zip.py vendors into the ZIP;
# the repo root is the shared original a plugin checkout keeps (build-plan s8).
_SKILL_DIR = Path(__file__).resolve().parent.parent
_DATA_ROOT = (
    _SKILL_DIR / "data" if (_SKILL_DIR / "data").is_dir()
    else _SKILL_DIR.parents[2]
)
SCHEMA_PATH = _DATA_ROOT / "schema" / "notion-schema.json"
MEASURE_KINDS = json.loads(SCHEMA_PATH.read_text())["measure_kinds"]
_UNIT_OF = {"Load": "Unit", "distance": "distance_unit"}
_SECONDS = {"duration_s", "interval_s"}
_CARRY_KEYS = ("Load", "Unit", "Reps", "load_kind")


def session_key(start: str, tz: str) -> str:
    """Client-side session identity (defect 2): the frozen open time plus the
    frozen timezone (rules L3, L4), never a predicted Notion page id. Real
    Notion page ids are opaque UUIDs assigned at write time, so this is
    computable before any write and stays stable across a real install."""
    return f"{start}|{tz}"


def week_index(local_date: str) -> int:
    """Rule L18: the ISO calendar week of `Date` (`YYYY-MM-DD`) in the
    session's stored zone, written once at open alongside `Date` itself
    (00 sS delta 2)."""
    return date.fromisoformat(local_date).isocalendar().week


def write_key(session_key: str, exercise_id: str, set_index: int, attempt: int) -> str:
    """Rule L8 identity: the natural key, written out. `session_key` is the
    client-side session identity above, not the Notion page id;
    `exercise_id` is the exercise NAME, which is what identifies an exercise
    now that there is no catalog database and no slug."""
    return f"{session_key}|{exercise_id}|{set_index}|{attempt}"


def carry_from(row: dict[str, Any]) -> dict[str, Any]:
    """What rule D/G/"same" need remembered: the last row's weight shape."""
    return {k: v for k, v in row.items() if k in _CARRY_KEYS}


def magnitudes_text(measure: str, fields: dict[str, Any]) -> str:
    """The measure kind's non-null magnitudes, schema order, `x`-joined."""
    order = MEASURE_KINDS[measure]["magnitudes"]
    unit_keys = set(_UNIT_OF.values())
    parts = []
    for key in order:
        if key in unit_keys or fields.get(key) is None:
            continue
        value = fields[key]
        unit_key = _UNIT_OF.get(key)
        if unit_key and fields.get(unit_key):
            parts.append(f"{value} {fields[unit_key]}")
        elif key in _SECONDS:
            parts.append(f"{value}s")
        else:
            parts.append(str(value))
    return " x ".join(parts)


def confirm_line(name: str, set_index: int, entry: Any, measure: str, last_index: int,
                 units: str, prefix: str) -> str:
    """`<exercise> set <n>, <magnitudes>[ @rpe]. <next target>.` (build-plan s4),
    with a create-on-demand prefix (rung 4) and G2's reading note folded in."""
    text = magnitudes_text(measure, entry["rows"][-1])
    rpe = entry.get("rpe")
    suffix = f" @{rpe}" if rpe is not None else ""
    grey = ", read as" if entry["grey_band"] else ","
    index_text = f"{set_index}-{last_index}" if last_index != set_index else str(set_index)
    target_row = carry_from(entry["rows"][-1])
    if measure == "weight_reps" and target_row.get("Load") is not None:
        next_target = f"Set {last_index + 1} at {target_row['Load']} {target_row.get('Unit', units)}"
    elif measure == "hold_time":
        next_target = f"Set {last_index + 1}, same target"
    else:
        next_target = f"Set {last_index + 1}"
    fix_note = " fix if reversed." if entry["grey_band"] else "."
    return f"{prefix}{name} set {index_text}{grey} {text}{suffix}{fix_note} {next_target}."


def emit_rows(writes: list[dict[str, Any]], rows: list[dict[str, Any]], session_id: str,
             session_key: str, exercise_id: str, start_index: int, first_attempt: int, now: str,
             message_id: str, confirm: str, rpe: float | None = None) -> None:
    """Append one `row-create` write per row. Only the last row in a multi-row
    entry (a ladder, an EMOM) carries the confirm line.

    `session_id` fills the `Session` text column; `session_key` (defect 2) feeds
    `write_key` instead. Every row, including row 2..N of a multi-row turn
    (a ladder, an EMOM), keeps the bare `message_id`: that is its true
    provenance (rule L9 defect 3). `write_key` already varies by `Set index`
    within the turn, so it alone is each row's real identity; the mock
    writer dedupes on identity, not on `source_message_id`, so same-message
    rows no longer collide (see `tools/mock-notion/writer.py`).
    """
    for offset, fields in enumerate(rows):
        attempt = first_attempt if offset == 0 else 0
        payload = {"Session": session_id, "Exercise": exercise_id, "Set index": start_index + offset,
                  "Set type": "working", "Timestamp": now, "Side": "both", **fields, "attempt": attempt,
                  "write_key": write_key(session_key, exercise_id, start_index + offset, attempt),
                  "source_message_id": message_id, "Pain flag": "none",
                  "confirm_line": confirm if offset == len(rows) - 1 else ""}
        if rpe is not None:
            payload["RPE"] = rpe
        writes.append({"verb": "row-create", "target": "Sets", "payload": payload})


def other_reading(reading: str) -> str:
    return "sets_x_reps" if reading == "weight_x_reps" else "weight_x_reps"


def reverse_grey_band(gb: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    """G2's undo: flip weight-x-reps (one row) against sets-x-reps (N rows of
    bare reps; no weight source exists yet on a first-ever set)."""
    reading = other_reading(gb["reading"])
    if reading == "weight_x_reps":
        rows = [{"Load": gb["first"], "Unit": gb["units"], "load_kind": "absolute", "Reps": gb["second"]}]
    else:
        rows = [{"Reps": gb["second"]} for _ in range(int(gb["first"]))]
    measure = "weight_reps" if reading == "weight_x_reps" else "reps_only"
    text = magnitudes_text(measure, rows[0])
    confirm = f"Fixed: now read as {text} x {len(rows)}." if len(rows) > 1 else f"Fixed: now read as {text}."
    return confirm, rows
