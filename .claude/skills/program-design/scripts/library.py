"""Retrieval from `library/`: which template a profile picks, the reason, and
the refusal-with-options script for a category with none (build-plan s7.1,
s7.2). Never free-generates a program; every template comes back verbatim
from `library/<id>.json` for the caller to adapt (swap-in-place lives in
`design.py`, which owns the athlete's live `state`).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, NamedTuple

# <skill>/data is the copy tools/package/build_zip.py vendors into the ZIP;
# the repo root is the shared original a plugin checkout keeps (build-plan s8).
_SKILL_DIR = Path(__file__).resolve().parent.parent
_DATA_ROOT = (
    _SKILL_DIR / "data" if (_SKILL_DIR / "data").is_dir()
    else _SKILL_DIR.parents[2]
)
LIBRARY_DIR = _DATA_ROOT / "library"
_REF_DIR = Path(__file__).resolve().parent.parent / "references"
_ROW_RE = re.compile(r"^\|\s*([\w.-]+)\s*\|(.+)\|$", re.MULTILINE)


class TemplateRule(NamedTuple):
    template: str
    goal: tuple[str, ...]
    equipment: tuple[str, ...]
    min_days: int
    training_age: tuple[str, ...]
    reason: str


class RefusalRow(NamedTuple):
    category: str
    keywords: tuple[str, ...]
    nearest: str
    shares: str
    source: str


def _cells(row: str) -> list[str]:
    return [c.strip() for c in row.split("|")]


def _words(cell: str) -> tuple[str, ...]:
    return () if cell == "-" else tuple(w.strip() for w in cell.split(","))


def _load_rules() -> list[TemplateRule]:
    text = (_REF_DIR / "templates.md").read_text()
    rules = []
    for match in _ROW_RE.finditer(text):
        first, rest = match.group(1), match.group(2)
        if first in ("template", "---"):
            continue
        template, goal, equipment, min_days, age, reason = [first] + _cells(rest)
        rules.append(TemplateRule(
            template, _words(goal), _words(equipment),
            0 if min_days == "-" else int(min_days), _words(age), reason))
    return rules


def _load_refusals() -> list[RefusalRow]:
    text = (_REF_DIR / "wording.md").read_text()
    rows = []
    for match in _ROW_RE.finditer(text):
        first, rest = match.group(1), match.group(2)
        if first in ("category", "---"):
            continue
        category, keywords, nearest, shares, source = [first] + _cells(rest)
        rows.append(RefusalRow(category, _words(keywords), nearest, shares, source))
    return rows


TEMPLATE_RULES = _load_rules()
REFUSAL_ROWS = _load_refusals()

REFUSAL_SCRIPT = (
    "I don't have a template for that. Three things I can do: run the "
    "nearest one I do have, {nearest}, which shares {shares}; build it into "
    "your current program as accessory work; or point you at {source} to "
    "bring numbers back. Which?"
)


def _any_word_in(words: tuple[str, ...], text: str) -> bool:
    low = text.lower()
    return any(word in low for word in words)


def refusal_for(line: str) -> str | None:
    """A GAP category's scripted reply (s7.2), or `None` if the line names
    none of the five."""
    low = line.lower()
    for row in REFUSAL_ROWS:
        if _any_word_in(row.keywords, low):
            return REFUSAL_SCRIPT.format(nearest=row.nearest, shares=row.shares, source=row.source)
    return None


def pick_template(text: str, days: int) -> tuple[str, str]:
    """First matching row of `references/templates.md` wins, checked against
    the athlete's own words in `text` (goal, equipment, and training age all
    live in one line, no separate slot per field). GZCLP's own row matches on
    goal alone, so it is the fallback for the common case (three days, double
    progression, commercial gym) once no more specific rule fires first."""
    for rule in TEMPLATE_RULES:
        if rule.goal and not _any_word_in(rule.goal, text):
            continue
        if rule.equipment and not _any_word_in(rule.equipment, text):
            continue
        if days and rule.min_days and days < rule.min_days:
            continue
        if rule.training_age and not _any_word_in(rule.training_age, text):
            continue
        return rule.template, rule.reason
    fallback = next(r for r in TEMPLATE_RULES if r.template == "gzclp")
    return fallback.template, fallback.reason


def load_template(template_id: str) -> dict[str, Any]:
    return json.loads((LIBRARY_DIR / f"{template_id}.json").read_text())
