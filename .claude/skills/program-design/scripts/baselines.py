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

# Which catalog id a spoken lift name resolves to. Small and closed on
# purpose: it matches the four lifts every `start`-bearing block in
# `library/` uses today, and a fifth lift needing this is a library file
# waiting to be authored, not a reason to grow this table speculatively.
LIFT_ALIASES = {
    "squat": "Barbell_Squat",
    "bench": "Barbell_Bench_Press_-_Medium_Grip",
    "deadlift": "Barbell_Deadlift",
    "overhead press": "Standing_Military_Press",
    "press": "Standing_Military_Press",
    "ohp": "Standing_Military_Press",
}
_NXR_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*x\s*(\d+)\b", re.IGNORECASE)


def display_name(exercise_id: str) -> str:
    """`Barbell_Squat` -> `Barbell Squat`: the catalog id is the display name
    with spaces swapped for underscores (`exercises/catalog.json`), so the
    reverse swap needs no catalog read."""
    return exercise_id.replace("_", " ")


def parse(text: str) -> dict[str, tuple[float, int]]:
    """Pair each lift name in `text` with its nearest `NxR` (185x5)."""
    keyword_hits = [(m.start(), exercise_id) for alias, exercise_id in LIFT_ALIASES.items()
                    for m in re.finditer(rf"\b{re.escape(alias)}\b", text, re.IGNORECASE)]
    nxr_hits = [(m.start(), float(m.group(1)), int(m.group(2))) for m in _NXR_RE.finditer(text)]
    found: dict[str, tuple[float, int]] = {}
    for keyword_pos, exercise_id in keyword_hits:
        if not nxr_hits:
            continue
        _, weight, reps = min(nxr_hits, key=lambda hit: abs(hit[0] - keyword_pos))
        found[exercise_id] = (weight, reps)
    return found


def _self_check() -> None:
    """python3 baselines.py"""
    assert display_name("Barbell_Squat") == "Barbell Squat"
    assert parse("squat 185x5") == {"Barbell_Squat": (185.0, 5)}
    assert parse("185x5 on squat") == {"Barbell_Squat": (185.0, 5)}
    assert parse("squat 185x5, bench 135x5") == {
        "Barbell_Squat": (185.0, 5),
        "Barbell_Bench_Press_-_Medium_Grip": (135.0, 5)}
    assert parse("squat 100.5x3") == {"Barbell_Squat": (100.5, 3)}
    assert parse("no numbers here") == {}
    assert parse("185x5") == {}, "a number with no lift names nothing"
    print("baselines.py self-check: ok")


if __name__ == "__main__":
    _self_check()
