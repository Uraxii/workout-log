"""Text-in, structured-out for load-adjust's own turn grammar (see
`load_adjust.py`'s module docstring for the three line shapes). Pure, stdlib
only, split out from `load_adjust.py` to keep the dispatch module under the
200-line limit (`docs/architecture.md`: split by domain, not execution step).
"""

from __future__ import annotations

import re
from typing import Any

_SET_RE = re.compile(r"^(?:bw([+-])(\d+(?:\.\d+)?)|(\d+(?:\.\d+)?))x(\d+)$", re.IGNORECASE)
_DECIMAL_RE = re.compile(r"^\d+(?:\.\d+)?$")
_WHOLE_RE = re.compile(r"^\d+$")

SET_SHAPE = "a set like `185x8`, `bw+25x8`, `bw-25x8`, or a bare rep count like `8`"


class Unreadable(Exception):
    """A token this grammar cannot read. Carries the offending token and the
    shape that would have worked, so the seam refuses by name instead of
    raising `ValueError` from whichever `int()` sat nearest (ayf.12).

    Raised only by `number` and `count`, caught only at `load_adjust.
    adjust_turn`'s single exit: one gate in, one gate out, so a call site
    added later cannot forget to handle it and cannot half-write first."""

    def __init__(self, token: str, expected: str) -> None:
        super().__init__(f"{token!r} is not {expected}")
        self.token = token
        self.expected = expected


def number(token: str, expected: str) -> float:
    """Every decimal this grammar reads out of user text passes through here.
    Non-negative only: a negative load is a typo, not a measurement, so
    `-50x5` refuses rather than reaching `int()`."""
    text = token.strip()
    if not _DECIMAL_RE.match(text):
        raise Unreadable(text, expected)
    return float(text)


def count(token: str, expected: str) -> int:
    """Every whole number this grammar reads out of user text. Separate from
    `number` because truncating `8.5` reps to `8` would be a silently wrong
    number, which this project ranks below a loud refusal."""
    text = token.strip()
    if not _WHOLE_RE.match(text):
        raise Unreadable(text, expected)
    return int(text)


def rpe(fields: list[str]) -> float | None:
    """Trailing `rpe=<n>` fields, if any. RPE is accepted when typed and never
    prompted (dec S17), so its absence is fine; a trailing field that is
    neither absent nor an RPE refuses rather than being silently dropped."""
    value = None
    for field in fields:
        if not field.startswith("rpe="):
            raise Unreadable(field, "an `rpe=<n>` field")
        value = number(field[len("rpe="):], "an RPE like `9.5`")
    return value


def setup_config(fields: list[str]) -> dict[str, Any]:
    """`setup` line fields (`axis=weight`, `increment=10`, ...) into one
    progression-rule dict, `docs/program-format.md` "Progression rule" shape
    plus the runtime counters load-adjust tracks (`fail_count`, streaks)."""
    cfg: dict[str, Any] = {"fail_count": 0, "deload_declined_at": None, "declined_streak": None,
                            "high_rpe_streak": 0, "pending_deload": None}
    for field in fields:
        key, _, value = field.partition("=")
        if key == "rep_range":
            lo, _, hi = value.partition("-")
            cfg["rep_range"] = (count(lo, "a rep range like `5-8`"),
                                count(hi, "a rep range like `5-8`"))
        elif key in ("increment", "deload_pct", "current"):
            cfg[key] = number(value, f"a number for `{key}`")
        elif key == "after_misses":
            cfg[key] = count(value, "a whole number of sessions")
        else:
            cfg[key] = value  # axis, unit, on_miss, hrt
    return cfg


def sets(text: str) -> tuple[list[dict[str, Any]], str | None]:
    """One token per set. `185x8` absolute, `bw+25x8` added, `bw-25x8`
    assist; a bare `8` (no `x`) is a `level`/`variation`-axis rep count.
    Anything else raises `Unreadable`; the groups `_SET_RE` does match are
    digits by construction, so those conversions cannot fail."""
    rows, kind = [], None
    for token in text.split(","):
        m = _SET_RE.match(token.strip())
        if not m:
            rows.append({"reps": count(token, SET_SHAPE)})
            continue
        sign, magnitude, absolute, reps = m.groups()
        kind = "absolute" if absolute is not None else ("added" if sign == "+" else "assist")
        rows.append({"reps": int(reps), "load": float(absolute if absolute is not None else magnitude)})
    return rows, kind
