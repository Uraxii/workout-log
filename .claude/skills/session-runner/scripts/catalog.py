"""Exercise-name resolution, the fallback ladder's rungs 2-4 (build-plan s3.2).

Rung 1 (grammar parse against today's scope) and rung 5 (verbatim note) live
in `log_set.py`, which owns the dispatch order. This module only answers
"what exercise is this": a whole-word match inside the athlete's own
`Exercises` rows (rung 3's scope filter), the shipped alias table (rung 2),
and the shape of a create-on-demand row (rung 4).

Nothing here guesses. Similarity scoring against the 913-row shipped catalog
used to sit at rung 3 and is gone: measured over 23 typed names it returned 2
right answers and 5 silently wrong ones (`bnch press` -> Neck Press,
`deadlift` -> Car Deadlift), and no cutoff repairs it, because
`SequenceMatcher` scores `row` higher against `Wide-Grip Lat Pulldown` than
against `Bent Over Two-Dumbbell Row`. A wrong exercise poisons every trend
and progression decision that later reads the row, so an unrecognised name
falls to rung 4, which announces the catalog row it adds (workout-log-9yj).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable, Iterable

# <skill>/data is the copy tools/package/build_zip.py vendors into the ZIP;
# the repo root is the shared original a plugin checkout keeps (build-plan s8).
_SKILL_DIR = Path(__file__).resolve().parent.parent
_DATA_ROOT = (
    _SKILL_DIR / "data" if (_SKILL_DIR / "data").is_dir()
    else _SKILL_DIR.parents[2]
)
EXERCISES_DIR = _DATA_ROOT / "exercises"

_NON_WORD = re.compile(r"[^a-z0-9]+")

# Equipment abbreviations a lifter types as often as the full word. Expanded
# on both sides of a comparison, so `incline db press` and the catalog's
# `Incline Dumbbell Press` reduce to the same three words. A spelling rule,
# not a guess: `db` never means anything else in an exercise name.
_SAME_WORD = {"db": "dumbbell", "bb": "barbell", "kb": "kettlebell"}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def load_aliases() -> dict[str, str]:
    return _load_json(EXERCISES_DIR / "aliases.json")


def load_catalog_names() -> dict[str, str]:
    """`{lowercased catalog name: canonical id}`, for rung 1 and rung 3."""
    catalog = _load_json(EXERCISES_DIR / "catalog.json")
    return {row["name"].lower(): row["id"] for row in catalog}


def _words(name: str) -> set[str]:
    return {_SAME_WORD.get(w, w) for w in _NON_WORD.split(name.lower()) if w}


def sole_word_match(typed: str, names: Iterable[str]) -> str | None:
    """The one name made of exactly the words of `typed`, or failing that the
    one name carrying all of them. `incline db press` is the same word set as
    `Incline Dumbbell Press`, so it beats the longer `Hammer Grip Incline DB
    Bench Press` that merely contains those words; `row` is nobody's whole
    name, so it falls to containment and finds `Bent Over Two-Dumbbell Row`.

    `None` when a tier has no name or several, so `press` against a catalog
    holding a bench press and a military press refuses instead of picking.
    Rung 3's scope filter (build-plan s3.2). Whole words, never substrings:
    `row` must not answer `Narrow Grip Press`."""
    wanted = _words(typed)
    if not wanted:
        return None
    by_name = {name: _words(name) for name in names}
    for tier in (lambda words: words == wanted, lambda words: wanted <= words):
        hits = [name for name, words in by_name.items() if tier(words)]
        if len(hits) == 1:
            return hits[0]
    return None


def resolve_name(typed: str, catalog_names: dict[str, str], aliases: dict[str, str]) -> str | None:
    """The shipped tables: a catalog name (rung 1), an authored alias (rung
    2), then the one shipped name built from exactly these words, which is
    how `incline db press` reaches `Incline Dumbbell Press` without anyone
    authoring that alias. The authored table goes first because it is a
    deliberate answer to an ambiguous word: `dip` is Parallel Bar Dip, not
    one of the four shipped names carrying the word.

    `None` when no table knows the name, which sends the line to rung 4's
    announced create rather than to a guess."""
    key = typed.strip().lower()
    if key in catalog_names:
        return catalog_names[key]
    if key in aliases:
        return aliases[key]
    shipped = sole_word_match(key, catalog_names)
    return catalog_names[shipped] if shipped else None


def infer_measure(entry_shape: dict[str, Any] | None) -> str:
    """Rung 4: infer `measure` from the set shape the same line just typed,
    per s3.2 ("measure inferred from the set shape, confirm in the same
    line"). Falls back to `reps_only`, the shape needing the fewest fields."""
    if not entry_shape:
        return "reps_only"
    if "duration_s" in entry_shape:
        return "hold_time"
    if "distance" in entry_shape and "Load" in entry_shape:
        return "distance_load"
    if "distance" in entry_shape:
        return "distance_time"
    if "Load" in entry_shape:
        return "weight_reps"
    return "reps_only"


def new_row_payload(name: str, measure: str) -> dict[str, Any]:
    """Rung 4's `Exercises` row: the typed name, the inferred measure, no
    other seed fields (those belong to the shipped catalog, not a runtime add)."""
    return {"Name": name, "measure": measure, "source": "user"}


def load_measures() -> dict[str, str]:
    """`{canonical id: measure kind}`, for the ladder to know what it found."""
    catalog = _load_json(EXERCISES_DIR / "catalog.json")
    return {row["id"]: row["measure"] for row in catalog}


def make_lookup(catalog_map: dict[str, Any]) -> Callable[[str], tuple[str, str] | None]:
    """Rung 3 in scope order: the athlete's own `Exercises` rows first, by
    exact name and then by whole word, and only after they have no single
    answer do the shipped tables get asked.

    Scope first is what stops `row` meaning one of the shipped catalog's 55
    rows. It also makes the same word answer differently for two athletes:
    `row` is the dumbbell row for someone running GZCLP and the Pendlay row
    for someone whose catalog holds that instead."""
    catalog_names, aliases, measures = load_catalog_names(), load_aliases(), load_measures()
    # The athlete's own row wins over the shipped id for the same exercise.
    # `press` reaching `Standing_Military_Press` through the alias table while
    # every set they ever logged sits on their own `Exercises` page would
    # split one lift's history across two ids.
    owned = {catalog_names[nm.lower()]: info for nm, info in catalog_map.items()
             if nm.lower() in catalog_names}

    def lookup(name_text: str) -> tuple[str, str] | None:
        key = name_text.strip().lower()
        for nm, info in catalog_map.items():
            if nm.lower() == key:
                return info["id"], info["measure"]
        scoped = sole_word_match(key, catalog_map)
        if scoped is not None:
            return catalog_map[scoped]["id"], catalog_map[scoped]["measure"]
        resolved = resolve_name(name_text, catalog_names, aliases)
        if resolved is None:
            return None
        info = owned.get(resolved)
        return (info["id"], info["measure"]) if info else (resolved, measures[resolved])

    return lookup


def name_for(exercise_id: str, catalog_map: dict[str, Any],
            created_payload: dict[str, Any] | None) -> str:
    """The display name for a confirm line: the just-created payload, this
    fixture's own seeded scope, then the shipped catalog."""
    if created_payload:
        return created_payload["Name"]
    for nm, info in catalog_map.items():
        if info["id"] == exercise_id:
            return nm
    names = {row["id"]: row["name"] for row in _load_json(EXERCISES_DIR / "catalog.json")}
    return names.get(exercise_id, exercise_id)
