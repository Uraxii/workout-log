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
_ROW_RE = re.compile(r"^\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|", re.MULTILINE)


def for_area(area: str) -> dict[str, str]:
    """`{exercise_id: substitute_id}` for one area, empty when none is on
    file. An area with no substitute is answered, not guessed at."""
    found = {}
    for row_area, exercise_id, substitute in _ROW_RE.findall(REFERENCE.read_text()):
        if row_area == "area":
            continue
        if row_area == area:
            found[exercise_id] = substitute
    return found


def _self_check() -> None:
    """python3 substitutions.py"""
    knee = for_area("knee")
    assert knee, "the reference file must carry a knee row"
    assert all(k != v for k, v in knee.items()), "a substitute must differ"
    assert for_area("nostril") == {}, "an unknown area substitutes nothing"
    print("substitutions.py self-check: ok")


if __name__ == "__main__":
    _self_check()
