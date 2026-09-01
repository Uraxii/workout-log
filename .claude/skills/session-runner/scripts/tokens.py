"""The token families normalization needs before the grammar runs
(build-plan s3.1): time, distance, side, composed spoken numbers, and the
unit suffix (`kg`, `lb`, `#`) every magnitude may carry.

Pure, stdlib-only, no exercise or session knowledge. `grammar.py` calls
`normalize()` first, then the three `parse_*` functions per measure kind.
"""

from __future__ import annotations

import re
from typing import Any

_ONES = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine".split())}
_TEENS = {w: 10 + i for i, w in enumerate(
    "ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
    "eighteen nineteen".split())}
_TENS = {w: 20 + 10 * i for i, w in enumerate(
    "twenty thirty forty fifty sixty seventy eighty ninety".split())}
_VALUE_WORDS = {**_ONES, **_TEENS, **_TENS}
# `a` and `and` join a spoken number without contributing a magnitude of
# their own, so they carry no value here and `_words_to_number` never sums
# one. A membership set, not a table: a table has to state a value for `a`,
# and any value it states is a claim the arithmetic below contradicts.
_COMPOSITION_WORDS = frozenset({"a", "and"})
_NUMBER_WORDS = _VALUE_WORDS.keys() | _COMPOSITION_WORDS | {"hundred"}
_WORD_RUN_RE = re.compile(
    r"\b(?:" + "|".join(sorted(_NUMBER_WORDS, key=len, reverse=True)) + r")"
    r"(?:\s+(?:" + "|".join(sorted(_NUMBER_WORDS, key=len, reverse=True)) + r"))*\b",
    re.IGNORECASE,
)


def _words_to_number(run: str) -> int | None:
    """`one thirty five` -> 135 (spoken shorthand), `a hundred and ten` -> 110,
    `twenty five` -> 25. `None` if the run is not a real composed number: a
    lone `a` is the English article, so `took a break` keeps its words."""
    words = [w for w in run.lower().split() if w != "and"]
    if not words or not all(w in _NUMBER_WORDS for w in words):
        return None
    if all(w in _COMPOSITION_WORDS for w in words):
        return None
    if "hundred" in words:
        i = words.index("hundred")
        prefix = _ONES.get(words[i - 1], 1) if i > 0 else 1
        rest = sum(_TEENS.get(w) or _TENS.get(w) or _ONES.get(w, 0) for w in words[i + 1:])
        return prefix * 100 + rest
    if len(words) >= 2 and words[0] in _ONES and words[0] != "zero":
        rest = _words_to_number(" ".join(words[1:]))
        if rest is not None and 10 <= rest <= 99:
            return _ONES[words[0]] * 100 + rest
    if len(words) == 1 or any(w in _TENS for w in words):
        return sum(_TEENS.get(w) or _TENS.get(w) or _ONES.get(w, 0) for w in words)
    return None


def _collapse_spoken_numbers(text: str) -> str:
    def repl(m: re.Match) -> str:
        value = _words_to_number(m.group(0))
        return str(value) if value is not None else m.group(0)
    return _WORD_RUN_RE.sub(repl, text)


# Both numbers must be whole standalone tokens (bounded by whitespace or the
# string ends), so `135 5/5/4` never eats the `5` off the slash group.
_JOIN_BARE_NUMBERS_RE = re.compile(r"(?:^|(?<=\s))(\d+)\s+(\d+)(?=\s|$)")


def normalize(text: str) -> str:
    """Spoken numbers collapse, `by`/`at`/`*` fold to `x`/`@`, adjacent bare
    numbers join into one magnitude (lim L-09: `1 85 x 5` -> `185x5`)."""
    text = _collapse_spoken_numbers(text.strip())
    text = re.sub(r"\bby\b", "x", text, flags=re.IGNORECASE)
    text = re.sub(r"\bat\b", "@", text, flags=re.IGNORECASE)
    text = text.replace("*", "x")
    while True:
        joined = _JOIN_BARE_NUMBERS_RE.sub(lambda m: m.group(1) + m.group(2), text)
        if joined == text:
            return text
        text = joined


def num(token: str) -> int | float:
    value = float(token)
    return int(value) if value.is_integer() else value


UNIT_RE = r"(kg|lb|#)?"


def unit_of(token: str | None, units: str) -> str:
    """`#` is pounds; no unit typed means the athlete's own units."""
    return "lb" if token == "#" else (token or units)


_TIME_RE = re.compile(
    r"^(\d+)m(\d+)$|^(\d+(?:\.\d+)?)\s*(?:min|mins|minute|minutes)$"
    r"|^(\d+(?:\.\d+)?)\s*(?:s|sec|secs|second|seconds)$", re.IGNORECASE)


def parse_time(text: str) -> dict[str, Any] | None:
    """`20s`, `45sec`, `1m30`, `2min`, `20 seconds` -> `duration_s`."""
    m = _TIME_RE.match(text)
    if not m:
        return None
    if m.group(1) is not None:
        return {"duration_s": int(m.group(1)) * 60 + int(m.group(2))}
    if m.group(3) is not None:
        return {"duration_s": num(m.group(3)) * 60}
    return {"duration_s": num(m.group(4))}


_DISTANCE_RE = re.compile(
    r"^(\d+(?:\.\d+)?)\s*(km|kilometres?|kilometers?|mi|miles?|m|metres?|meters?)$",
    re.IGNORECASE)


def parse_distance(text: str) -> tuple[float, str] | None:
    """`60m`, `400m`, `1.5km`, `0.5mi`, `60 metres` -> `(distance, distance_unit)`."""
    m = _DISTANCE_RE.match(text)
    if not m:
        return None
    value, unit = num(m.group(1)), m.group(2).lower()
    if unit.startswith("km") or unit.startswith("kilo"):
        return value, "km"
    if unit.startswith("mi"):
        return value, "mi"
    return value, "m"


_SIDE_SLASH_RE = re.compile(r"^(\d+)\s*l(?:eft)?\s*/\s*(\d+)\s*r(?:ight)?$", re.IGNORECASE)
_SIDE_WORDS_RE = re.compile(r"^(\d+)\s*left\s+(\d+)\s*right$", re.IGNORECASE)
_SIDE_EQUAL_RE = re.compile(r"^(\d+)\s*(?:per side|each side)$", re.IGNORECASE)


def parse_side(text: str) -> dict[str, Any] | None:
    """`5l/6r`, `8 left 7 right`, `10 per side` -> `reps_left`/`reps_right`."""
    m = _SIDE_SLASH_RE.match(text) or _SIDE_WORDS_RE.match(text)
    if m:
        return {"reps_left": int(m.group(1)), "reps_right": int(m.group(2))}
    m = _SIDE_EQUAL_RE.match(text)
    if m:
        n = int(m.group(1))
        return {"reps_left": n, "reps_right": n}
    return None
