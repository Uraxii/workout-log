"""Exercise-name resolution, the fallback ladder's rungs 2-4 (build-plan s3.2).

An exercise IS its name. There is no slug, no id, and no catalog database:
Notion holds logs only, so a `Sets` row stores the name as text and the
shipped `exercises/defaults.json` is package reference data the agent reads,
never something written to the athlete's workspace.

Rung 1 (grammar parse against today's scope) and rung 5 (verbatim note) live
in `log_set.py`, which owns the dispatch order. This module only answers
"what exercise is this": a whole-word match inside the names this athlete has
already logged (rung 3's scope filter), the shipped alias table (rung 2), and
the shipped defaults.

Nothing here guesses. Similarity scoring against the old 913-row catalog used
to sit at rung 3 and is gone: measured over 23 typed names it returned 2 right
answers and 5 silently wrong ones (`bnch press` -> Neck Press, `deadlift` ->
Car Deadlift), and no cutoff repairs it, because `SequenceMatcher` scores
`row` higher against `Wide-Grip Lat Pulldown` than against `Bent Over
Two-Dumbbell Row`. A wrong exercise poisons every trend and progression
decision that later reads the row, so an unrecognised name falls to rung 4,
which logs the name as typed and announces that it is new (workout-log-9yj).
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
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
# on both sides of a comparison, so `incline db press` and the defaults'
# `Incline Dumbbell Press` reduce to the same three words. A spelling rule,
# not a guess: `db` never means anything else in an exercise name.
_SAME_WORD = {"db": "dumbbell", "bb": "barbell", "kb": "kettlebell"}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


@lru_cache(maxsize=1)
def load_aliases() -> dict[str, str]:
    """`{typed shorthand: default name}`, rung 2's authored table."""
    return _load_json(EXERCISES_DIR / "aliases.json")


@lru_cache(maxsize=1)
def load_defaults() -> dict[str, str]:
    """`{default exercise name: measure kind}`, the shipped baseline the agent
    picks a program from. Read once per process, not once per typed name."""
    return {row["name"]: row["measure"]
            for row in _load_json(EXERCISES_DIR / "defaults.json")}


def measure_of(name: str, known: dict[str, str] | None = None) -> str | None:
    """This athlete's own measure kind for `name`, else the shipped default,
    else `None` so a caller renders no magnitudes rather than guessing."""
    if known and name in known:
        return known[name]
    return load_defaults().get(name)


def _words(name: str) -> set[str]:
    return {_SAME_WORD.get(w, w) for w in _NON_WORD.split(name.lower()) if w}


def sole_word_match(typed: str, names: Iterable[str]) -> str | None:
    """The one name made of exactly the words of `typed`, or failing that the
    one name carrying all of them. `incline db press` is the same word set as
    `Incline Dumbbell Press`, so it beats the longer `Hammer Grip Incline DB
    Bench Press` that merely contains those words; `row` is nobody's whole
    name, so it falls to containment and finds `Bent Over Two-Dumbbell Row`.

    `None` when a tier has no name or several, so `press` against defaults
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


def resolve_name(typed: str) -> str | None:
    """The shipped tables: a default name (rung 1), an authored alias (rung
    2), then the one default name built from exactly these words, which is
    how `incline db press` reaches `Incline Dumbbell Press` without anyone
    authoring that alias. The authored table goes first because it is a
    deliberate answer to an ambiguous word: `dip` is Parallel Bar Dip, not
    one of the four shipped names carrying the word.

    `None` when no table knows the name, which sends the line to rung 4,
    where it is logged under the name the athlete typed."""
    key = typed.strip().lower()
    defaults = load_defaults()
    by_lower = {name.lower(): name for name in defaults}
    if key in by_lower:
        return by_lower[key]
    aliases = load_aliases()
    if key in aliases:
        return aliases[key]
    return sole_word_match(key, defaults)


def infer_measure(entry_shape: dict[str, Any] | None) -> str:
    """Rung 4: infer `measure` from the set shape the same line just typed,
    per s3.2 ("measure inferred from the set shape"). Also reads it back off a
    stored `Sets` row, which carries the same magnitude keys. Falls back to
    `reps_only`, the shape needing the fewest fields."""
    if not entry_shape:
        return "reps_only"
    if entry_shape.get("duration_s") is not None:
        return "hold_time"
    if entry_shape.get("distance") is not None and entry_shape.get("Load") is not None:
        return "distance_load"
    if entry_shape.get("distance") is not None:
        return "distance_time"
    if entry_shape.get("Load") is not None:
        return "weight_reps"
    return "reps_only"


def make_lookup(known: dict[str, str]) -> Callable[[str], tuple[str, str] | None]:
    """Rung 3 in scope order: the names this athlete has already logged first,
    by exact name and then by whole word, and only after they have no single
    answer do the shipped tables get asked. Returns `(name, measure)`.

    Scope first is what stops `row` meaning one of the 92 shipped names. It
    also makes the same word answer differently for two athletes: `row` is the
    dumbbell row for someone whose log holds that, and the barbell row for
    someone who has logged neither and gets the authored alias."""
    def lookup(name_text: str) -> tuple[str, str] | None:
        key = name_text.strip().lower()
        for name, measure in known.items():
            if name.lower() == key:
                return name, measure
        scoped = sole_word_match(key, known)
        if scoped is not None:
            return scoped, known[scoped]
        resolved = resolve_name(name_text)
        if resolved is None:
            return None
        return resolved, measure_of(resolved, known)

    return lookup
