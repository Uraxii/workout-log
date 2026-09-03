"""`references/substitutions.md`: which exercise stands in for which, per
restricted area.

The reference file is the content authority (build-plan s6, lim L-21) and
this is the only reader of its table shape, so a row format change lands
here and nowhere else.
"""

from __future__ import annotations

import re
from pathlib import Path

REFERENCE = Path(__file__).resolve().parent.parent / "references" / "substitutions.md"
# Cells hold exercise NAMES, so they carry spaces, hyphens and apostrophes:
# anything but the `|` that ends the cell.
_ROW_RE = re.compile(r"^\|([^|]+)\|([^|]+)\|([^|]+)\|", re.MULTILINE)
_SEPARATOR = frozenset("-: ")


def for_area(area: str) -> dict[str, str]:
    """`{exercise name: substitute name}` for one area, empty when none is on
    file. An area with no substitute is answered, not guessed at."""
    found = {}
    for row_area, exercise, substitute in _ROW_RE.findall(REFERENCE.read_text()):
        row_area, exercise = row_area.strip(), exercise.strip()
        if row_area == "area" or set(row_area) <= _SEPARATOR:
            continue
        if row_area == area:
            found[exercise] = substitute.strip()
    return found


def _self_check() -> None:
    """python3 substitutions.py"""
    knee = for_area("knee")
    assert knee, "the reference file must carry a knee row"
    assert all(k != v for k, v in knee.items()), "a substitute must differ"
    assert for_area("nostril") == {}, "an unknown area substitutes nothing"
    assert knee.get("Barbell Squat") == "Leg Press", "names carry spaces"
    assert "---" not in knee and "" not in knee, "the header rule is not a row"
    print("substitutions.py self-check: ok")


if __name__ == "__main__":
    _self_check()
