"""The read-time layer, s1.7 (closes R9): e1RM, display conversion, ranking.
Storage is untouched, every function here is read-only over `Sets`-row-shaped
dicts (`Load`, `Unit`, `Reps`, `Set type`, `load_kind`). Pure, stdlib only.

`e1rm` reuses `program-design/scripts/loads.py`'s Brzycki implementation
(`docs/architecture.md` "script seam": one script per concern, shared by
import, never copy-pasted) rather than re-deriving it: the schema's `Sets.e1RM`
formula `Load / (1.0278 - 0.0278 * Reps)` is the same relation rearranged
(1.0278 = 37/36, 0.0278 = 1/36), so `loads.brzycki_e1rm` already computes it.

`load_kind = assist` inverts the difficulty direction (lim L-05): more
assistance is easier, so a *falling* `Load` on an assisted set is the lifter
getting stronger, never a decline, and a *rising* `Load` is regression, never
progress. `effective_difficulty` encodes that inversion once so ranking and
trend both read it correctly instead of each re-deriving the sign.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "program-design" / "scripts"))
import loads  # noqa: E402  (shared Brzycki e1RM, see module docstring)

KG_PER_LB = 0.45359237


def to_unit(value: float, from_unit: str, to_unit_: str) -> float:
    """Read-only display conversion (lim L-35). Never touches a stored row."""
    if from_unit == to_unit_:
        return value
    if from_unit == "lb" and to_unit_ == "kg":
        return value * KG_PER_LB
    if from_unit == "kg" and to_unit_ == "lb":
        return value / KG_PER_LB
    raise ValueError(f"unsupported unit pair {from_unit!r} -> {to_unit_!r}")


def e1rm(load: float, reps: int, set_type: str = "working") -> float | None:
    """`Sets.e1RM`'s formula. Null above 10 reps or off a non-`working` set,
    exactly the schema's `null_when` (schema/notion-schema.json Sets.e1RM)."""
    if set_type != "working":
        return None
    return loads.brzycki_e1rm(load, reps)


def effective_difficulty(row: dict[str, Any]) -> float | None:
    """Signed difficulty on one common scale: `absolute`/`added` loads count
    up, `assist` counts down, since more assistance is less difficult
    (lim L-05). `None` when the row carries no load (a hold, a level set)."""
    load = row.get("Load")
    if load is None:
        return None
    return -load if row.get("load_kind") == "assist" else load


def rank_best(rows: list[dict[str, Any]], target_unit: str) -> dict[str, Any] | None:
    """Best e1RM across rows stored in mixed units (lim L-35), converting
    each row's `Load` to `target_unit` before ranking so a lb row and a kg
    row compare correctly. Never mutates a row; returns the winning row plus
    its converted e1RM, or `None` if nothing qualifies."""
    best = None
    best_value = None
    for row in rows:
        if row.get("Load") is None or row.get("load_kind") == "assist":
            continue  # an assisted best is not a "how much can I lift" answer
        converted = to_unit(row["Load"], row.get("Unit", target_unit), target_unit)
        value = e1rm(converted, row.get("Reps", 0), row.get("Set type", "working"))
        if value is None:
            continue
        if best_value is None or value > best_value:
            best, best_value = row, value
    if best is None:
        return None
    return {**best, "e1RM": best_value, "e1RM_unit": target_unit}


def trend_label(rows_in_order: list[dict[str, Any]]) -> str:
    """`improving` / `declining` / `flat`, comparing the first and last
    row's `effective_difficulty` (lim L-05: assist inverted first, so this
    never reads a falling assist `Load` as a decline, or a rising one as
    progress). Never phrased as a raw-`Load` "rising trend": callers should
    use this label's own words, not "load is up", when the row carries
    `load_kind = assist`."""
    values = [v for v in (effective_difficulty(r) for r in rows_in_order) if v is not None]
    if len(values) < 2 or values[-1] == values[0]:
        return "flat"
    return "improving" if values[-1] > values[0] else "declining"
