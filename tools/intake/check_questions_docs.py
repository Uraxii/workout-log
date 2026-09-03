#!/usr/bin/env python3
"""Check intake's question docs agree with `questions.FIELD_STEPS`.

`references/questions.md` and `SKILL.md`'s "The question flow" section both
restate the question order in prose, by hand. Three separate agents found
one of these docs stale in the same afternoon (workout-log, 2026-09-02): a
question got added to `FIELD_STEPS` and a doc kept describing the old flow.
This is the mechanism that replaces re-reading them by eye
(`principle-encode-lessons-in-structure`).

`questions.md`'s table is the full listing, so every id in `FIELD_STEPS`
must appear in it, in order (checked against table rows only, so prose
above or below the table can't produce a false match: an intro sentence
that names "goal" as a category is not a claim about row order).

`SKILL.md`'s "The question flow" section makes one precise claim and the
rest loose prose: "Three questions about the tool come first". Only that
claim is checked, against the three ids `FIELD_STEPS` itself marks
`section: "storage"`, restricted to that section so an unrelated mention
elsewhere in the file (`notion_parent_page_id` inside a code span in the
database-creation section) can't look like an ordering claim. Presence is
not required (the section spells `notion_parent_page_id` out in English,
"the Notion parent page id", never as the bare token, and that is a fine
sentence, not a stale doc): whichever of the three it does name just can't
come out of order. The rest of the section names categories ("goal,
history, constraints, ...") and one illustrative example ("say, units
plus..."), neither committing to per-id order, so checking every
`FIELD_STEPS` id there would fail on ordinary prose that never claimed to
be exhaustive.

`docs/install.md` is deliberately excluded: it is user-facing prose and, by
`technical-writing`, should never carry an internal identifier like
`storage_platform`. There is nothing literal in it to check without either a
hand-maintained phrase-to-id map (the drift this script exists to avoid) or
a check broad enough to fire on ordinary wording.

PAR-Q+'s seven questions (`screen.QUESTIONS`, `SAFETY_IDS` in
`questions.py`) are excluded too: they are a fixed block owned by the
`screen` skill and pinned byte for byte by its own fixture, not part of
`FIELD_STEPS`, so they carry none of the drift this check guards against.

    python3 tools/intake/check_questions_docs.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
INTAKE_DIR = REPO_ROOT / ".claude" / "skills" / "intake"
sys.path.insert(0, str(INTAKE_DIR / "scripts"))
import questions  # noqa: E402  (source of truth: FIELD_STEPS)

QUESTIONS_MD = INTAKE_DIR / "references" / "questions.md"
SKILL_MD = INTAKE_DIR / "SKILL.md"
QUESTION_FLOW_HEADING = "## The question flow"

FIELD_IDS = tuple(step["id"] for step in questions.FIELD_STEPS)
STORAGE_IDS = tuple(step["id"] for step in questions.FIELD_STEPS
                     if step.get("section") == "storage")


def _table_rows(text: str) -> str:
    """Markdown table row lines only, so surrounding prose is out of view."""
    return "\n".join(line for line in text.splitlines() if line.startswith("|"))


def _section(text: str, heading: str) -> str:
    """Text of the named '## heading' section, up to the next '## ' heading."""
    start = text.index(heading)
    rest = text[start + len(heading):]
    end = re.search(r"\n## ", rest)
    return rest[: end.start() if end else None]


def _positions(text: str, ids: tuple[str, ...]) -> dict[str, int]:
    """Earliest offset of each id that appears in `text` as a whole word."""
    found = {}
    for id_ in ids:
        match = re.search(rf"\b{re.escape(id_)}\b", text)
        if match:
            found[id_] = match.start()
    return found


def check(path: Path, text: str, ids: tuple[str, ...], require_all: bool) -> list[str]:
    """Errors for one doc: ids missing (table only) or out of order."""
    positions = _positions(text, ids)
    errors = []
    if require_all:
        missing = [id_ for id_ in ids if id_ not in positions]
        if missing:
            errors.append(f"{path}: missing question id(s): {', '.join(missing)}")
    present = [id_ for id_ in ids if id_ in positions]
    by_text_order = sorted(present, key=positions.get)
    if by_text_order != present:
        bad = next(a for a, b in zip(present, by_text_order) if a != b)
        errors.append(
            f"{path}: {bad!r} out of order, expected question order {present!r}"
        )
    return errors


def main() -> int:
    errors = [
        *check(QUESTIONS_MD, _table_rows(QUESTIONS_MD.read_text()), FIELD_IDS,
               require_all=True),
        *check(SKILL_MD, _section(SKILL_MD.read_text(), QUESTION_FLOW_HEADING),
               STORAGE_IDS, require_all=False),
    ]
    for e in errors:
        print(e, file=sys.stderr)
    print(f"checked questions.md's table against {len(FIELD_IDS)} FIELD_STEPS "
          f"ids, SKILL.md's question-flow section against {len(STORAGE_IDS)} "
          f"storage ids")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
