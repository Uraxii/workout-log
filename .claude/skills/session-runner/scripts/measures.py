"""Per-measure-kind entry shapes: what a line means once the exercise's
`measure` is known (build-plan s1.3, s3.1).

Split out of `grammar.py` (house limit; docs/architecture.md "One script per
skill" applies the same way here, split by domain, never by execution step):
rules A-J read a weight-and-reps line with no idea what exercise it is, while
this module answers the different question of what a `hold_time` or
`distance_load` exercise accepts. Token parsing itself stays in `tokens.py`.
"""

from __future__ import annotations

import re
from typing import Any

import tokens

_LEVEL_RE = re.compile(r"^(?:step|level|progression)\s+(\d+)\s*x\s*(\d+)$", re.IGNORECASE)
_EMOM_RE = re.compile(
    rf"^emom\s+(\d+)\s*x\s*(\d+)(?:\s*@(\d+(?:\.\d+)?){tokens.UNIT_RE})?$", re.IGNORECASE)


def _distance_rows(text: str, measure: str, units: str) -> list[dict[str, Any]] | None:
    """`400m`, `1.5km 20kg` -> one row. A `distance_load` line may carry a
    trailing load; `distance_time` may not."""
    parts = text.split()
    dist = tokens.parse_distance(parts[0]) if parts else None
    if not dist:
        return None
    distance, dunit = dist
    fields = {"distance": distance, "distance_unit": dunit}
    rest = " ".join(parts[1:]).lstrip("@").strip()
    if measure == "distance_load" and rest:
        m = re.match(rf"^(\d+(?:\.\d+)?){tokens.UNIT_RE}$", rest, re.IGNORECASE)
        if m:
            fields.update(Load=tokens.num(m.group(1)),
                          Unit=tokens.unit_of(m.group(2), units), load_kind="absolute")
    return [fields]


def _emom_rows(text: str, units: str) -> list[dict[str, Any]] | None:
    """`emom 10x10 @24kg` -> one row per round (build-plan s1.3 row 5)."""
    m = _EMOM_RE.match(text)
    if not m:
        return None
    rounds, reps, load, unit = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)
    row = {"Reps": reps, "interval_s": 60}
    if load:
        row.update(Load=tokens.num(load), Unit=tokens.unit_of(unit, units),
                   load_kind="absolute")
    return [dict(row) for _ in range(rounds)]


def entry_for(text: str, measure: str, units: str) -> list[dict[str, Any]] | None:
    """Time/distance/side token families by measure kind, plus the two s1.3
    shapes (`step N xR`, `emom NxR @load`) that need no general grammar rule.
    `None` means this measure's own shapes do not match, so rules A-J run."""
    if measure == "hold_time":
        fields = tokens.parse_time(text)
        return [fields] if fields else None
    if measure in ("distance_load", "distance_time"):
        return _distance_rows(text, measure, units)
    if measure == "level_reps":
        m = _LEVEL_RE.match(text)
        return [{"level": int(m.group(1)), "Reps": int(m.group(2))}] if m else None
    if measure == "interval_reps":
        return _emom_rows(text, units)
    side = tokens.parse_side(text)
    return [side] if side else None
