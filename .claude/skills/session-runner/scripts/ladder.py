"""The fallback ladder's dispatch order (build-plan s3.2): given one chat
line, find the exercise and the entry together. Pure function of its inputs;
`log_set.py` owns all state mutation and writes.

Rung 1 (grammar parse) and rung 2/3 (alias, word match) share one search: try
the line with no exercise name first (the common case, continuing whatever is
in scope), then increasingly long leading-word prefixes as a candidate name.
Rung 4 repeats the search allowing an unresolved name and returns that name
verbatim, so a lift no shipped table knows still gets logged under what the
athlete called it. Rung 5 (verbatim note) is "nothing matched", left to the
caller.
"""

from __future__ import annotations

from typing import Any, Callable, TypedDict

import catalog
import grammar
import tokens

MAX_NAME_WORDS = 4
TRIAL_MEASURES = ["weight_reps", "hold_time", "distance_load", "distance_time", "reps_only"]

Lookup = Callable[[str], tuple[str, str] | None]  # typed name -> (id, measure)


class Resolution(TypedDict):
    kind: str            # "scoped" | "named" | "unknown"
    exercise_id: str     # the exercise NAME; identity is the name
    measure: str
    entry: grammar.Entry


def _entry_ctx(units: str, carry: dict[str, Any] | None, target: dict[str, Any] | None) -> grammar.EntryContext:
    return {"units": units, "carry": carry, "target": target}


def resolve(text: str, scope: tuple[str, str] | None, lookup: Lookup,
            units: str, carry: dict[str, Any] | None, target: dict[str, Any] | None,
            implicit_candidates: list[tuple[str, str]] = ()) -> Resolution | None:
    """Rungs 1-3: try the scoped exercise first, then (with no scope yet, one
    session's very first line) whichever seeded exercise is the sole one the
    text parses against, then a leading-word name."""
    text = tokens.normalize(text)
    words = text.split()

    if scope is not None:
        exercise_id, measure = scope
        entry = grammar.parse_entry(text, measure, _entry_ctx(units, carry, target))
        if entry:
            return {"kind": "scoped", "exercise_id": exercise_id,
                    "measure": measure, "entry": entry}
    else:
        hits = [(eid, measure, grammar.parse_entry(text, measure, _entry_ctx(units, None, None)))
                for eid, measure in implicit_candidates]
        hits = [(eid, measure, entry) for eid, measure, entry in hits if entry]
        if len(hits) == 1:
            eid, measure, entry = hits[0]
            return {"kind": "scoped", "exercise_id": eid, "measure": measure, "entry": entry}

    for i in range(1, min(len(words), MAX_NAME_WORDS) + 1):
        name_text, rest = " ".join(words[:i]), " ".join(words[i:])
        if not rest:
            continue
        found = lookup(name_text)
        if not found:
            continue
        exercise_id, measure = found
        entry = grammar.parse_entry(rest, measure, _entry_ctx(units, None, None))
        if entry:
            return {"kind": "named", "exercise_id": exercise_id,
                    "measure": measure, "entry": entry}

    return None


def resolve_unknown_name(text: str, units: str) -> Resolution | None:
    """Rung 4: the longest leading-word name whose remainder parses under any
    measure, tried longest-name-first so `zercher squat 135x5` keeps the full
    two-word name rather than stopping at `zercher`. The name is the exercise:
    there is no catalog row to create, so the typed words are what the `Sets`
    row stores."""
    text = tokens.normalize(text)
    words = text.split()
    empty_ctx = _entry_ctx(units, None, None)

    for i in range(min(len(words), MAX_NAME_WORDS), 0, -1):
        name_text, rest = " ".join(words[:i]), " ".join(words[i:])
        if not rest:
            continue
        for measure in TRIAL_MEASURES:
            entry = grammar.parse_entry(rest, measure, empty_ctx)
            if entry:
                inferred = catalog.infer_measure(entry["rows"][0] if entry["rows"] else None)
                return {"kind": "unknown", "exercise_id": name_text,
                        "measure": inferred, "entry": entry}
    return None
