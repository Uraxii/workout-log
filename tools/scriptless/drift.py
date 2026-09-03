"""Build-time check that the normative rules in the SKILL.md prose and
the Python scripts still say the same thing.

Same job and same exit convention as `tools/intake/check_questions_docs.py`,
which is the precedent. The reason: script execution is certain only in
the Claude Code terminal, so the prose is the authority on every other
host, and a rule that exists in only one of the two places is a rule
that silently disappears.

    python3 tools/scriptless/drift.py
"""

from __future__ import annotations

from pathlib import Path


def prose_rule_ids(skill_root: Path) -> set[str]:
    """Every rule id (L1 to L18, S1 to S8, G2) cited anywhere under
    `skill_root`."""
    ...  # TODO


def plan_rule_ids(plan_path: Path) -> set[str]:
    """Every rule id `docs/build-plan.md` defines."""
    ...  # TODO


def markdown_table(path: Path, heading: str) -> list[tuple[str, str]]:
    """The row pairs of the markdown table under `heading` in `path`."""
    ...  # TODO


def check_rule_coverage(skill_root: Path, plan_path: Path) -> list[str]:
    """Returns one failure line per rule the plan defines that no prose
    file cites. A rule living only in `build-plan.md` and a `.py`
    docstring is the exact failure the host matrix names."""
    ...  # TODO


def check_red_flags(reference_path: Path, script_path: Path) -> list[str]:
    """Parses the phrase-to-enum table out of the markdown reference and
    asserts the script's word sets honour every row it lists.
    The table is a floor: the prose lets a model map more phrases to
    `stop` than the table lists, so the direction that must hold is that
    every table row is honoured by the script, not that the script maps
    nothing else."""
    ...  # TODO


def check_cards(schema_path: Path, out_dir: Path) -> list[str]:
    """Failure lines for any field card `cards.is_current` reports
    stale."""
    ...  # TODO


def main() -> int:
    """Prints every failure line and returns 1, or prints a one-line
    pass and returns 0."""
    ...  # TODO


if __name__ == "__main__":
    raise SystemExit(main())
