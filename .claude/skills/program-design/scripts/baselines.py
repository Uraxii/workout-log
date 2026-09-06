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
#
# "bench press" needs no entry of its own: the word "bench" inside it
# already matches the "bench" alias below. "press" alone still means
# overhead press (an athlete really does say just "press 135x5"), but
# _is_standalone_press keeps it from also firing inside ANY "<modifier>
# press" (leg press, incline press, chest press, floor press, dumbbell
# press), which would wrongly record an overhead press nobody named
# (workout-log-t5a).
LIFT_ALIASES = {
    "squat": "Barbell Squat",
    "bench": "Barbell Bench Press - Medium Grip",
    "deadlift": "Barbell Deadlift",
    "overhead press": "Standing Military Press",
    "press": "Standing Military Press",
    "ohp": "Standing Military Press",
}
_NXR_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*x\s*(\d+)\b", re.IGNORECASE)


def _is_standalone_press(text: str, start: int) -> bool:
    """True unless another word sits directly before "press" (only
    whitespace stripped): "press 135x5" is standalone, "leg press 300x10"
    is not, and neither is "overhead press" or "bench press" (each already
    has its own alias, so bare "press" firing there too would be a second,
    redundant hit for the same lift)."""
    before = text[:start].rstrip()
    return not before or not before[-1].isalpha()


def parse(text: str) -> dict[str, tuple[float, int]]:
    """Pair each lift name in `text` with the `NxR` (185x5) the athlete said
    for THAT lift, keyed by exercise name (identity is the name; there is no
    slug).

    Each lift name owns a segment of the text: from just after its own name
    to the start of the next lift name (end of text, for the last one). An
    `NxR` outside a lift's segment can never be paired with it, so one
    lift's number can never leak onto another (workout-log-t5a): no
    proximity contest across the whole line, no bookkeeping to stop a
    number being claimed twice. A lift with no `NxR` in its own segment
    comes back with no entry at all, rather than borrowing a neighbour's.
    The one lift named first also gets the text before it searched, so
    "185x5 on squat" still resolves with the number given before the name.
    """
    hits = sorted(
        (m.start(), m.end(), exercise_name)
        for alias, exercise_name in LIFT_ALIASES.items()
        for m in re.finditer(rf"\b{re.escape(alias)}\b", text, re.IGNORECASE)
        if alias != "press" or _is_standalone_press(text, m.start()))
    nxr_hits = [(m.start(), float(m.group(1)), int(m.group(2)))
                for m in _NXR_RE.finditer(text)]
    found: dict[str, tuple[float, int]] = {}
    for i, (pos, end, exercise_name) in enumerate(hits):
        segment_end = hits[i + 1][0] if i + 1 < len(hits) else len(text)
        candidates = [hit for hit in nxr_hits if end <= hit[0] < segment_end]
        if not candidates and i == 0:
            candidates = [hit for hit in nxr_hits if hit[0] < pos]
        if not candidates:
            continue
        _, weight, reps = min(candidates, key=lambda hit: abs(hit[0] - pos))
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
    assert parse("bench press 135x5, squat 185x5") == {
        "Barbell Bench Press - Medium Grip": (135.0, 5),
        "Barbell Squat": (185.0, 5)
    }, "bare 'press' inside 'bench press' must not spawn a phantom lift"
    assert parse("overhead press 95x5, squat 185x5") == {
        "Standing Military Press": (95.0, 5),
        "Barbell Squat": (185.0, 5)
    }, "a named overhead press must still resolve"
    assert parse("leg press 300x10, squat 185x5") == {
        "Barbell Squat": (185.0, 5)
    }, "leg press is not an overhead press"
    assert parse("incline press 95x5, squat 185x5") == {
        "Barbell Squat": (185.0, 5)
    }, "incline press is not an overhead press"
    assert parse("squat 185x5, bench, deadlift 225x5") == {
        "Barbell Squat": (185.0, 5),
        "Barbell Deadlift": (225.0, 5)
    }, "a lift named with no number must not steal a neighbour's"
    assert parse("ohp 95x5, bench press 135x5") == {
        "Standing Military Press": (95.0, 5),
        "Barbell Bench Press - Medium Grip": (135.0, 5)
    }
    assert parse("squat 315x5, bench 225x5, deadlift 405x3, press 135x5") == {
        "Barbell Squat": (315.0, 5),
        "Barbell Bench Press - Medium Grip": (225.0, 5),
        "Barbell Deadlift": (405.0, 3),
        "Standing Military Press": (135.0, 5)
    }, "a standalone 'press' after a comma still means overhead press"
    print("baselines.py self-check: ok")


if __name__ == "__main__":
    _self_check()
