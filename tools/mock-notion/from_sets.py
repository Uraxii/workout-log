"""What one unfiltered read of `Sets` tells a cold chat.

Split out of `hydrate.py` (house limit; docs/architecture.md "One script per
skill" applies the same way to the harness, split by domain never by
execution step). `hydrate.py` owns which reads happen and in what order and
assembles the whole `state`; this owns the two things derived from the log
itself.

Both were reads before. `known` was a `row_query("Exercises")`, until the
athlete's Notion became logs-only and there was no such database; `cursor`
was a second, filtered `row_query("Sets")`. One read answers both, so
`hydrate.py` issues it once and hands the rows here.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude" / "skills"
                       / "session-runner" / "scripts"))

import catalog  # noqa: E402  (owns the defaults and measure inference)


def known_exercises(logged: list[dict[str, Any]]) -> dict[str, str]:
    """`{exercise name: measure kind}` for every exercise this athlete has
    logged a set of, which is the fallback ladder's scope filter.

    The measure comes from the shipped `exercises/defaults.json` when it
    carries the name, and otherwise from the row's own magnitudes, which is
    the same inference rung 4 made when that set was first logged.
    """
    known: dict[str, str] = {}
    for row in logged:
        name = row.get("Exercise")
        if not name or name in known:
            continue
        known[name] = catalog.measure_of(name) or catalog.infer_measure(row)
    return known


def set_cursor(logged: list[dict[str, Any]],
               open_row: dict[str, Any] | None) -> dict[str, int]:
    """The NEXT `Set index` per exercise, which is the value `log_set.py`
    stores (`cursor[exercise_id] = last_index + 1`) and reads back
    (`cursor.get(exercise_id, 1)`), so the max stored index plus one.

    No open session means no cursor: `Set index` is scoped to
    `(session, exercise)` (rule L7), so a closed session's indices would
    mislabel set 1 of the next session as a continuation.
    """
    if open_row is None:
        return {}
    cursor: dict[str, int] = {}
    for row in logged:
        if row.get("Session") != open_row["page_id"]:
            continue
        exercise_id, set_index = row.get("Exercise"), row.get("Set index")
        if exercise_id is None or set_index is None:
            continue
        cursor[exercise_id] = max(cursor.get(exercise_id, 0), set_index + 1)
    return cursor
