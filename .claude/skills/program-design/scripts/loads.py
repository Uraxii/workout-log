"""Starting-load math: intake baseline -> a block's first working weight.

Arithmetic basis is float kilograms (`docs/unit-and-magnitude-model.md` s1).
`to_kg` and `to_display` are the only functions here that take a unit, and
between them every magnitude carries a `_kg` suffix. Brzycki e1RM
(research/07-baselining-and-assessment.md s4.1): `1RM = w * 36 / (37 -
reps)`, never above 10 reps. A weight-x-reps baseline is an estimate, not a
tested max, so a form allowance (a conservative haircut) stands in for the
safety margin a real retest would have. `resolve_start_load` then runs the
same relation in reverse to find the weight for the block's `start.test` rep
count, applies `start.pct`, and floors the answer to something the gym can
actually load, in the athlete's own unit.
"""

from __future__ import annotations

import math

BRZYCKI_MAX_REPS = 10
FORM_ALLOWANCE_PCT = 0.10  # haircut on an estimated (untested) max
KG_PER_LB = 0.45359237     # the international pound, exact by definition
# Smallest pair a normal gym racks: 2.5 lb or 1.25 kg a side
# (`docs/unit-and-magnitude-model.md` s3).
LOADABLE_INCREMENT = {"lb": 5.0, "kg": 2.5}
_KG_PER_UNIT = {"lb": KG_PER_LB, "kg": 1.0}
_TEST_REPS = {"1rm": 1, "3rm": 3, "5rm": 5}
# A kg round trip lands 185 lb on 184.99999999999997, and a bare floor would
# hand that back a whole increment light. One part in a billion is far below
# any loadable increment and far above float error on a two-step conversion.
_FLOOR_TOLERANCE = 1e-9


def _for_unit(table: dict[str, float], unit: str) -> float:
    if unit not in table:
        raise ValueError(f"unsupported unit {unit!r}")
    return table[unit]


def to_kg(value: float, unit: str) -> float:
    """The athlete's typed number -> the arithmetic basis."""
    return value * _for_unit(_KG_PER_UNIT, unit)


def to_display(value_kg: float, unit: str) -> float:
    """The arithmetic basis -> the unit the athlete reads and loads."""
    return value_kg / _for_unit(_KG_PER_UNIT, unit)


def round_down_to_increment(value: float, unit: str) -> float:
    """Floor `value` to a loadable weight IN `unit`, never in the basis: 90 kg
    is a clean plate load and its 198.42 lb twin is not. Floors because every
    caller wants down (a bump must not exceed what the rule computed, a
    deload must not undo itself, a first block should be conservative), so
    there is no direction to pass and no tie to break."""
    increment = _for_unit(LOADABLE_INCREMENT, unit)
    return math.floor(value / increment + _FLOOR_TOLERANCE) * increment


def format_load(value: float, unit: str) -> str:
    """What the athlete reads. Never emitted without its unit."""
    return f"{value:g} {unit}"


def brzycki_e1rm(weight_kg: float, reps: int) -> float | None:
    """Estimated 1RM from one clean set. `None` above the validated range."""
    if reps < 1 or reps > BRZYCKI_MAX_REPS:
        return None
    return weight_kg * 36 / (37 - reps)


def estimated_max(weight_kg: float, reps: int) -> float | None:
    """Brzycki e1RM minus the form allowance, standing in for a tested max."""
    e1rm_kg = brzycki_e1rm(weight_kg, reps)
    return None if e1rm_kg is None else e1rm_kg * (1 - FORM_ALLOWANCE_PCT)


def resolve_start_load(effective_1rm_kg: float, start_rule: dict, unit: str) -> float | None:
    """A block's `start` rule (`docs/program-format.md` "Progression rule"),
    applied to an estimated max, answered in `unit` and already floored to a
    loadable weight. Only `retest_pct` carries baseline math; `load_delta`
    and `hold` have nothing to resolve from a baseline alone."""
    if start_rule.get("kind") != "retest_pct":
        return None
    test_reps = _TEST_REPS[start_rule["test"]]
    test_weight_kg = effective_1rm_kg * (37 - test_reps) / 36
    return round_down_to_increment(to_display(test_weight_kg * start_rule["pct"], unit), unit)


def _self_check() -> None:
    """python3 loads.py"""
    assert to_kg(100, "kg") == 100.0
    assert abs(to_kg(1, "lb") - KG_PER_LB) < 1e-12
    assert abs(to_display(to_kg(185, "lb"), "lb") - 185) < 1e-9
    for unit, value, want in (("lb", 141.525, 140.0), ("kg", 141.525, 140.0),
                              ("lb", 143.055, 140.0), ("kg", 143.055, 142.5),
                              ("lb", 2.5, 0.0), ("kg", 187.3125, 185.0)):
        got = round_down_to_increment(value, unit)
        assert got == want, f"{value} {unit} -> {got}, want {want}"
    # The round trip must not cost an increment (`_FLOOR_TOLERANCE`).
    assert round_down_to_increment(to_display(to_kg(185, "lb"), "lb"), "lb") == 185.0
    assert round_down_to_increment(to_display(to_kg(140, "kg"), "kg"), "kg") == 140.0
    for bad in ("stone", "", "LB"):
        for call in (lambda: to_kg(1, bad), lambda: to_display(1, bad),
                     lambda: round_down_to_increment(1, bad)):
            try:
                call()
            except ValueError:
                continue
            raise AssertionError(f"{bad!r} must raise")
    assert brzycki_e1rm(100, 0) is None and brzycki_e1rm(100, 11) is None
    assert brzycki_e1rm(100, 1) == 100.0
    rule = {"kind": "retest_pct", "test": "5rm", "pct": 0.85}
    assert resolve_start_load(estimated_max(to_kg(187, "lb"), 5), rule, "lb") == 140.0
    assert resolve_start_load(estimated_max(to_kg(187, "kg"), 5), rule, "kg") == 142.5
    assert resolve_start_load(1.0, {"kind": "hold"}, "lb") is None
    print("loads.py self-check: ok")


if __name__ == "__main__":
    _self_check()
