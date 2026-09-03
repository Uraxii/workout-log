"""Plausibility bounds for a `Sets` row's magnitudes
(`docs/unit-and-magnitude-model.md` s4, `workout-log-ayf.3`).

One table, one function, one call site. `log_set.py` wires
`reject_implausible_writes` around every turn's assembled writes, the same
shape `preconditions.no_sets_while_halted` already uses for rule S2: read
what the turn actually produced, not the line the user typed, so a `Sets`
row-create write is caught no matter which handler built it, including one
not written yet.

Refuse, never clamp. A clamp turns a typo into a data point nothing
downstream can tell from a real one; every defect in this family had that
shape (`-200` silently became `Load = -15`, a bare `185` silently became
`Reps = 185`).

The model's own file puts these ranges in `schema/notion-schema.json` so
`writer.py` enforces them too. That file is out of scope for this change, so
this table is the only declaration; the seam-side refusal alone already
satisfies "no row is written" for every write path in this skill.
"""

from __future__ import annotations

import copy
from typing import Any

SET_TARGET = "Sets"

# Load's bound depends on the row's own `Unit`; every other magnitude below
# is unit-independent in the row it is stored in (s4 table).
_LOAD_RANGE_BY_UNIT = {"lb": (0.0, 1000.0), "kg": (0.0, 500.0)}

# distance is stored in the row's own `distance_unit` (m, km, mi), but s4
# states the bound only in km ("above 0, up to 100 km"), so this converts to
# meters first. 1 km = 1000 m and 1 mi = 1609.344 m are both exact by
# definition; the mi figure is not itself in the doc, flagged in the report.
_METERS_PER_UNIT = {"m": 1.0, "km": 1000.0, "mi": 1609.344}
_DISTANCE_RANGE_M = (0.0, 100_000.0)

# field -> (min, max, human label for the refusal text), inclusive both ends.
_SCALAR_RANGES = {
    "Reps": (1, 100, "reps"),
    "duration_s": (1, 14400, "hold time"),
    "interval_s": (1, 3600, "interval"),
}


def _load_refusal(fields: dict[str, Any]) -> str | None:
    load = fields.get("Load")
    if load is None:
        return None
    unit = fields.get("Unit", "lb")
    lo, hi = _LOAD_RANGE_BY_UNIT.get(unit, _LOAD_RANGE_BY_UNIT["lb"])
    if lo <= load <= hi:
        return None
    return (f"{load} {unit} is outside the plausible load range "
           f"({lo:g} to {hi:g} {unit}). Nothing written. Retype the set.")


def _distance_refusal(fields: dict[str, Any]) -> str | None:
    distance = fields.get("distance")
    if distance is None:
        return None
    unit = fields.get("distance_unit", "m")
    meters = distance * _METERS_PER_UNIT.get(unit, 1.0)
    lo, hi = _DISTANCE_RANGE_M
    if lo < meters <= hi:
        return None
    return (f"{distance} {unit} is outside the plausible distance range "
           "(above 0, up to 100 km). Nothing written. Retype the set.")


def _scalar_refusal(fields: dict[str, Any]) -> str | None:
    for field, (lo, hi, label) in _SCALAR_RANGES.items():
        value = fields.get(field)
        if value is None or lo <= value <= hi:
            continue
        return (f"{value} is outside the plausible {label} range "
               f"({lo:g} to {hi:g}). Nothing written. Retype the set.")
    return None


def reject_implausible(fields: dict[str, Any]) -> str | None:
    """The one choke point every magnitude passes through before a row is
    written. `fields` is a `Sets` row payload, or the subset of one a caller
    already has; only the keys present are checked, so a caller need not
    know which magnitude kind it is holding. `None` means the row may
    proceed as typed."""
    return _load_refusal(fields) or _distance_refusal(fields) or _scalar_refusal(fields)


def reject_implausible_writes(turn: dict[str, Any], before: dict[str, Any]) -> dict[str, Any]:
    """Wired around every turn in `log_set.py`. Scans the turn's own `Sets`
    row-create writes; a violation drops the whole turn atomically (no
    partial entry, no exercise auto-create surviving a refused set) and
    reverts state to `before`, so cursor and carry never advance on a
    refused line, the same shape `preconditions.no_sets_while_halted` uses
    for rule S2."""
    for write in turn["writes"]:
        if write["target"] != SET_TARGET:
            continue
        refusal = reject_implausible(write["payload"])
        if refusal is not None:
            return {"writes": [], "confirm_line": refusal, "state": copy.deepcopy(before)}
    return turn


def _self_check() -> None:
    """python3 bounds.py"""
    assert reject_implausible({"Load": 185, "Unit": "lb", "Reps": 5}) is None
    assert reject_implausible({"Load": 0, "Unit": "lb"}) is None  # zero assist, s4
    assert "load" in reject_implausible({"Load": -15, "Unit": "lb", "Reps": 5})
    assert "load" in reject_implausible({"Load": 1500, "Unit": "lb"})
    assert "load" in reject_implausible({"Load": 600, "Unit": "kg"})
    assert reject_implausible({"Reps": 100}) is None
    assert "reps" in reject_implausible({"Reps": 185})
    assert "reps" in reject_implausible({"Reps": 0})
    assert reject_implausible({"duration_s": 14400}) is None
    assert "hold time" in reject_implausible({"duration_s": 20000})
    assert reject_implausible({"interval_s": 60}) is None
    assert "interval" in reject_implausible({"interval_s": 9999})
    assert reject_implausible({"distance": 100, "distance_unit": "km"}) is None
    assert "distance" in reject_implausible({"distance": 150, "distance_unit": "km"})
    assert "distance" in reject_implausible({"distance": 0, "distance_unit": "m"})
    assert reject_implausible({"level": 3, "Reps": 5}) is None  # level: s4 silent, unbounded

    turn = {"writes": [{"verb": "row-create", "target": "Sets",
                        "payload": {"Load": -15, "Unit": "lb", "Reps": 5}}],
           "confirm_line": "x", "state": {"cursor": {"e": 9}}}
    before = {"cursor": {"e": 1}}
    refused = reject_implausible_writes(turn, before)
    assert refused["writes"] == []
    assert refused["state"] == before
    assert refused["state"] is not before  # deep-copied, not aliased

    ok_turn = {"writes": [{"verb": "row-create", "target": "Sets",
                           "payload": {"Load": 185, "Unit": "lb", "Reps": 5}}],
              "confirm_line": "ok", "state": {"cursor": {"e": 2}}}
    assert reject_implausible_writes(ok_turn, before) is ok_turn

    # A non-magnitude Sets write (a note, a stale tombstone) never trips it.
    note_turn = {"writes": [{"verb": "row-create", "target": "Sets",
                             "payload": {"Notes": "185 felt heavy"}}],
                "confirm_line": "Noted.", "state": {}}
    assert reject_implausible_writes(note_turn, before) is note_turn
    print("bounds.py self-check: ok")


if __name__ == "__main__":
    _self_check()
