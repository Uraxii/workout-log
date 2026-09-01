"""Set-entry grammar (build-plan s3, research/04 s2.3-s2.4): text in, per-row
magnitude fields out. Rules A-J plus G2's grey-band resolution. Pure,
stdlib-only. `parse_entry` tries one production family at a time, first
match wins, `None` falls through to the next ladder rung. Token families
live in `tokens.py`, the per-measure-kind shapes in `measures.py`, and
exercise-name resolution (rule J) in `catalog.py`.
"""

from __future__ import annotations

import re
from typing import Any, TypedDict

import measures
import tokens

# Rule A cutoffs: below is sets x reps, above weight x reps, between is G2's grey band.
SETS_MAX = {"lb": 10, "kg": 10}
WEIGHT_MIN = {"lb": 25, "kg": 12}
ROUNDS_REPS_MIN = 31  # branch 4: first <= 10, second > 30 -> rounds x reps

class EntryContext(TypedDict, total=False):
    """What `parse_entry` needs about the exercise besides the typed text."""
    units: str
    carry: dict[str, Any] | None      # last logged row's fields, or None
    target: dict[str, Any] | None     # program-prescribed Load/Reps, or None

class Entry(TypedDict):
    rows: list[dict[str, Any]]   # one dict of magnitude fields per row
    rpe: float | None
    grey_band: bool              # True if G2 resolved this one

normalize = tokens.normalize
_num = tokens.num

_RPE_RE = re.compile(r"\s*@(\d+(?:\.\d+)?)([+-])?\s*$")

def _split_rpe(text: str) -> tuple[str, float | None]:
    """Rule E: `@N` always introduces RPE, never a weight or a mention."""
    m = _RPE_RE.search(text)
    return (text, None) if not m else (text[:m.start()].strip(), _num(m.group(1)))

def _weight_row(load: float, unit: str, reps: int) -> dict[str, Any]:
    return {"Load": load, "Unit": unit, "load_kind": "absolute", "Reps": reps}

_TWO_NUM_RE = re.compile(rf"^(\d+(?:\.\d+)?){tokens.UNIT_RE}\s*x\s*(\d+)$", re.IGNORECASE)
_THREE_NUM_RE = re.compile(rf"^(\d+(?:\.\d+)?){tokens.UNIT_RE}\s*x\s*(\d+)\s*x\s*(\d+)$", re.IGNORECASE)
# Once a weight is consumed, a following AxB is sets x reps (research/04:423-426).
_WEIGHT_THEN_SETS_RE = re.compile(rf"^(\d+(?:\.\d+)?)(kg|lb|#)\s+(\d+)\s*x\s*(\d+)$", re.IGNORECASE)
_SLASH_RE = re.compile(rf"^(?:(\d+(?:\.\d+)?){tokens.UNIT_RE}\s+)?(\d+(?:/\d+)+)$", re.IGNORECASE)
_LONE_NUM_RE = re.compile(r"^(\d+)$")
_DELTA_RE = re.compile(r"^([+-])(\d+(?:\.\d+)?)$")
_REPS_OVERRIDE_RE = re.compile(r"^x(\d+)$", re.IGNORECASE)
_AMRAP_RE = re.compile(r"^(\d+)\+$")
_BW_RE = re.compile(
    r"^bw\s*(?:([+-])\s*(\d+(?:\.\d+)?))?\s*(kg|lb|#)?(?:\s*x\s*(\d+))?$", re.IGNORECASE)

def _grey_band_reading(first: float, ctx: EntryContext) -> str:
    """G2, no dialogue: program target's `Reps` matching `first` means it was
    a set count; else default to weight x reps. `fix` reverses the reading."""
    target = ctx.get("target") or {}
    return "sets_x_reps" if target.get("Reps") == first else "weight_x_reps"

def _rows_from_reps(carry: dict, target: dict, units: str, reps: int, count: int) -> list[dict]:
    load = carry.get("Load", target.get("Load"))
    if load is None:
        return [{"Reps": reps} for _ in range(count)]
    unit = carry.get("Unit", target.get("Unit", units))
    return [_weight_row(load, unit, reps) for _ in range(count)]

def parse_entry(text: str, measure: str, ctx: EntryContext) -> Entry | None:
    """Rung 1 of the ladder. An entry with no rows is not a parse: `0x0` and
    `a x 5` reach a branch that shapes zero rows, and a zero-row entry has no
    last row for the confirm line to render, so it falls to the next rung
    (build-plan s3.2 rung 5, the verbatim note) instead of half-writing.
    Checked here, at the one exit every branch below returns through, so a
    new branch cannot reintroduce it."""
    entry = _parse_entry(text, measure, ctx)
    return entry if entry is not None and entry["rows"] else None

def _parse_entry(text: str, measure: str, ctx: EntryContext) -> Entry | None:
    """One production family per branch, first match wins."""
    text, rpe = _split_rpe(normalize(text))
    units = ctx.get("units", "lb")
    carry = ctx.get("carry") or {}
    target = ctx.get("target") or {}

    rows = measures.entry_for(text, measure, units)
    if rows:
        return {"rows": rows, "rpe": rpe, "grey_band": False}

    m = _SLASH_RE.match(text)
    if m and "/" in m.group(3):
        load = _num(m.group(1)) if m.group(1) else carry.get("Load") or target.get("Load")
        unit = tokens.unit_of(m.group(2), units)
        rows = [_weight_row(load, unit, int(r)) if load is not None else {"Reps": int(r)}
                for r in m.group(3).split("/")]
        return {"rows": rows, "rpe": rpe, "grey_band": False}

    m = _THREE_NUM_RE.match(text)
    if m:
        load, unit, reps, sets = _num(m.group(1)), tokens.unit_of(m.group(2), units), int(m.group(3)), int(m.group(4))
        return {"rows": [_weight_row(load, unit, reps) for _ in range(sets)], "rpe": rpe, "grey_band": False}

    m = _WEIGHT_THEN_SETS_RE.match(text)
    if m:
        load, unit, sets, reps = _num(m.group(1)), tokens.unit_of(m.group(2), units), int(m.group(3)), int(m.group(4))
        return {"rows": [_weight_row(load, unit, reps) for _ in range(sets)], "rpe": rpe, "grey_band": False}

    if text == "same" and carry:
        return {"rows": [dict(carry)], "rpe": rpe, "grey_band": False}

    m = _DELTA_RE.match(text)
    if m and (carry.get("Load") is not None or target.get("Load") is not None):
        base = carry.get("Load", target.get("Load"))
        reps = carry.get("Reps", target.get("Reps"))
        unit = carry.get("Unit", target.get("Unit", units))
        signed = float(m.group(2)) * (1 if m.group(1) == "+" else -1)
        return {"rows": [_weight_row(_num(str(base + signed)), unit, reps)], "rpe": rpe, "grey_band": False}

    m = _REPS_OVERRIDE_RE.match(text)
    if m and (carry.get("Load") is not None or target.get("Load") is not None):
        load = carry.get("Load", target.get("Load"))
        unit = carry.get("Unit", target.get("Unit", units))
        return {"rows": [_weight_row(load, unit, int(m.group(1)))], "rpe": rpe, "grey_band": False}

    m = _AMRAP_RE.match(text)
    if m:
        load = carry.get("Load", target.get("Load"))
        unit = carry.get("Unit", target.get("Unit", units))
        row = _weight_row(load, unit, int(m.group(1))) if load is not None else {"Reps": int(m.group(1))}
        row["is_amrap"] = True
        return {"rows": [row], "rpe": rpe, "grey_band": False}

    m = _LONE_NUM_RE.match(text)
    if m and (carry.get("Load") is not None or measure == "reps_only"):
        reps = int(m.group(1))
        if carry.get("Load") is not None:
            return {"rows": [_weight_row(carry["Load"], carry.get("Unit", units), reps)], "rpe": rpe, "grey_band": False}
        return {"rows": [{"Reps": reps}], "rpe": rpe, "grey_band": False}

    m = _BW_RE.match(text)
    if m and measure == "weight_reps":
        sign, magnitude, unit_token, reps_token = m.groups()
        reps = int(reps_token) if reps_token else carry.get("Reps", target.get("Reps"))
        row: dict[str, Any] = {"Reps": reps} if reps is not None else {}
        if magnitude is None:
            row["load_kind"] = "absolute"
        else:
            row.update(Load=_num(magnitude), Unit=tokens.unit_of(unit_token, units),
                       load_kind="added" if sign == "+" else "assist")
        return {"rows": [row], "rpe": rpe, "grey_band": False}

    m = _TWO_NUM_RE.match(text)
    if m and measure == "weight_reps":
        first, unit_token, second = _num(m.group(1)), m.group(2), int(m.group(3))
        if unit_token or first >= WEIGHT_MIN[units]:
            return {"rows": [_weight_row(first, tokens.unit_of(unit_token, units), second)], "rpe": rpe, "grey_band": False}
        if first <= SETS_MAX[units] and second <= 30:
            return {"rows": _rows_from_reps(carry, target, units, second, int(first)), "rpe": rpe, "grey_band": False}
        if first <= SETS_MAX[units] and second >= ROUNDS_REPS_MIN:
            return {"rows": [{"Reps": second} for _ in range(int(first))], "rpe": rpe, "grey_band": False}
        reading = _grey_band_reading(first, ctx)
        if reading == "weight_x_reps":
            rows = [_weight_row(first, units, second)]
        else:
            rows = _rows_from_reps(carry, target, units, second, int(first))
        return {"rows": rows, "rpe": rpe, "grey_band": True}

    return None
