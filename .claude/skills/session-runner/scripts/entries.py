"""What a resolved line becomes once the ladder has answered: the rows
written, the cursor and carry they advance, and the line said back.

Split out of `log_set.py` (house limit; docs/architecture.md "One script per
skill" applies the same way here, split by domain, never by execution step).
`log_set.py` owns the dispatch order and the seam contract; this module owns
the three shapes a dispatched line can end as, one function each: a normal
entry (rungs 1-4), a verbatim note (rung 5), and G2's grey-band reversal.
Same discipline as `lifecycle.py`: pure functions, `writes` appended in
place, the `Turn`-shaped dict returned.
"""

from __future__ import annotations

from typing import Any

import rows as row_shapes


def apply_greyband_fix(state, writes, last_greyband, session_id, session_key,
                       now, message_id) -> dict[str, Any]:
    """G2: a bare `fix` right after a grey-band read flips that reading."""
    confirm, new_rows = row_shapes.reverse_grey_band(last_greyband)
    exercise_id = last_greyband["exercise_id"]
    row_shapes.emit_rows(writes, new_rows, session_id, session_key, exercise_id,
                         last_greyband["set_index"], last_greyband["attempt"] + 1, now,
                         message_id, confirm)
    cursor = dict(state.get("cursor", {}))
    cursor[exercise_id] = last_greyband["set_index"] + len(new_rows)
    carry = {**state.get("carry", {}), exercise_id: row_shapes.carry_from(new_rows[-1])}
    last_greyband = {**last_greyband, "reading": row_shapes.other_reading(last_greyband["reading"]),
                     "attempt": last_greyband["attempt"] + 1}
    state.update(cursor=cursor, carry=carry, last_greyband=last_greyband)
    return {"writes": writes, "confirm_line": confirm, "state": state}


def notes_fallback(state, writes, line, session_id, session_key, message_id, now) -> dict[str, Any]:
    # Rung 5: no exercise or set index, so message_id stands in (rule L9);
    # a constant would collide write_key across every unparsed line (L8).
    confirm = "Noted."
    key = row_shapes.write_key(session_key, message_id, 0, 0)
    payload = {"Session": session_id, "Timestamp": now, "Notes": line, "attempt": 0,
              "write_key": key, "source_message_id": message_id,
              "Pain flag": "none", "confirm_line": confirm}
    writes.append({"verb": "row-create", "target": "Sets", "payload": payload})
    last_write = {"write_key": key, "exercise_id": None, "set_index": None}
    state.update(last_greyband=None, last_write=last_write)
    return {"writes": writes, "confirm_line": confirm, "state": state}


def log_entry(state, writes, result, is_new_name, known, cursor, carry, targets,
              session_id, session_key, now, message_id, units) -> dict[str, Any]:
    """`result["exercise_id"]` is the exercise NAME: identity is the name, so
    nothing is created anywhere and no id is predicted. Rung 4 is the case
    where no shipped table knew the name, so it is logged as typed and the
    confirm line says so; a quiet rung 4 is how a typo used to become a
    second lift with its own history (workout-log-9yj)."""
    exercise_id = result["exercise_id"]
    measure, entry = result["measure"], result["entry"]
    if is_new_name:
        known[exercise_id] = measure
    set_index = cursor.get(exercise_id, 1)
    last_index = set_index + len(entry["rows"]) - 1

    name = exercise_id
    prefix = f"First time logging {name}. " if is_new_name else ""
    confirm = row_shapes.confirm_line(name, set_index, entry, measure, last_index, units, prefix)
    row_shapes.emit_rows(writes, entry["rows"], session_id, session_key, exercise_id, set_index, 0, now,
                         message_id, confirm, entry.get("rpe"))
    cursor[exercise_id] = last_index + 1
    carry[exercise_id] = row_shapes.carry_from(entry["rows"][-1])
    scope = (exercise_id, measure)

    last_greyband = None  # only the turn right after a grey-band read is `fix`-able
    if entry["grey_band"]:
        row = entry["rows"][0]
        multi = len(entry["rows"]) > 1
        last_greyband = {"exercise_id": exercise_id, "set_index": set_index, "attempt": 0,
                         "reading": "sets_x_reps" if multi else "weight_x_reps",
                         "first": len(entry["rows"]) if multi else row["Load"],
                         "second": row["Reps"], "units": units}
    last_write = {"write_key": row_shapes.write_key(session_key, exercise_id, last_index, 0),
                 "exercise_id": exercise_id, "set_index": set_index}
    state.update(cursor=cursor, carry=carry, targets=targets,
                scope=list(scope), last_greyband=last_greyband, known=known,
                last_write=last_write)
    return {"writes": writes, "confirm_line": confirm, "state": state}
