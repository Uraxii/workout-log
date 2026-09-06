"""Reading a strength baseline out of the athlete's own words.

`intake` stores the answer to "what's the most weight x reps you've done
recently" verbatim on `config/athlete.strength_baseline`; a plan request can
also carry one inline ("make me a plan ... squat 185x5"). Both are the same
free text from the same person, so one parser serves both and a user who
answered intake gets starting loads without retyping the numbers
(workout-log-k37).

Weights are in the athlete's own unit. Nothing here converts: the caller
knows the unit and owns the arithmetic (`loads.py`).
"""

from __future__ import annotations

import re

# Which exercise name a spoken lift name resolves to. Small and closed on
# purpose: it matches the four lifts every `start`-bearing block in
# `library/` uses today, and a fifth lift needing this is a library file
# waiting to be authored, not a reason to grow this table speculatively.
LIFT_ALIASES = {
    "squat": "Barbell Squat",
    "bench": "Barbell Bench Press - Medium Grip",
    "deadlift": "Barbell Deadlift",
    "overhead press": "Standing Military Press",
    "press": "Standing Military Press",
    "ohp": "Standing Military Press",
}
_NXR_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*x\s*(\d+)\b", re.IGNORECASE)


def parse(text: str) -> dict[str, tuple[float, int]]:
    """Pair each lift name in `text` with its own `NxR` (185x5), keyed by
    exercise name (identity is the name; there is no slug). Lift names are
    read left to right and each claims the nearest `NxR` not already claimed
    by an earlier lift name, so "squat 185x5, bench 135x5, deadlift 225x5"
    keeps each lift's own number instead of letting a closer neighbour's
    number leak across (workout-log-t5a)."""
    keyword_hits = sorted(
        (m.start(), exercise_name)
        for alias, exercise_name in LIFT_ALIASES.items()
        for m in re.finditer(rf"\b{re.escape(alias)}\b", text, re.IGNORECASE))
    nxr_hits = [(m.start(), float(m.group(1)), int(m.group(2))) for m in _NXR_RE.finditer(text)]
    found: dict[str, tuple[float, int]] = {}
    for keyword_pos, exercise_name in keyword_hits:
        if not nxr_hits:
            continue
        i, (_, weight, reps) = min(
            enumerate(nxr_hits), key=lambda hit: abs(hit[1][0] - keyword_pos))
        del nxr_hits[i]
        found[exercise_name] = (weight, reps)
    return found


def _self_check() -> None:
    """python3 baselines.py"""
    assert parse("squat 185x5") == {"Barbell Squat": (185.0, 5)}
    assert parse("185x5 on squat") == {"Barbell Squat": (185.0, 5)}
    assert parse("squat 185x5, bench 135x5") == {
        "Barbell Squat": (185.0, 5),
        "Barbell Bench Press - Medium Grip": (135.0, 5)}
    assert parse("squat 100.5x3") == {"Barbell Squat": (100.5, 3)}
    assert parse("no numbers here") == {}
    assert parse("185x5") == {}, "a number with no lift names nothing"
    print("baselines.py self-check: ok")


if __name__ == "__main__":
    _self_check()
