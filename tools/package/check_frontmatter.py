#!/usr/bin/env python3
"""Check every .claude/skills/*/SKILL.md has name and description frontmatter.

Stdlib stand-in for `skills-ref validate` (docs/build-plan.md s9 phase 7): the
skills-ref binary is not installed on this machine, so this checks the same
two required fields from the Agent Skills spec by hand.

    python3 tools/package/check_frontmatter.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
REQUIRED_FIELDS = ("name:", "description:")


def frontmatter_errors(skill_md: Path) -> list[str]:
    """Errors in skill_md's frontmatter block, empty when it is valid."""
    text = skill_md.read_text()
    if not text.startswith("---\n"):
        return [f"{skill_md}: does not start with '---'"]
    end = text.find("\n---", 4)
    if end == -1:
        return [f"{skill_md}: no closing '---' line"]
    block = text[4:end]
    return [
        f"{skill_md}: missing {field!r} in frontmatter"
        for field in REQUIRED_FIELDS
        if field not in block
    ]


def main() -> int:
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    errors = [e for f in skill_files for e in frontmatter_errors(f)]
    for e in errors:
        print(e, file=sys.stderr)
    print(f"checked {len(skill_files)} SKILL.md file(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
