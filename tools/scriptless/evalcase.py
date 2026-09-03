"""The model-behaviour proof surface.

The 25 fixtures under `fixtures/` replay transcripts through the pure
Python seams with no model in the loop, so they prove the scripts and
can never prove the prose. An eval case runs a real model with the skill
folder loaded, against the same `tools/mock-notion` writer exposed as
tools rather than imported, and asserts over the TSV that writer already
emits. Same assertion machinery, different producer.

This runs on a `make eval` target and never inside `make check`, because
it needs a network, a model, and money, so it gates a release and not a
commit.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvalCase:
    """One eval case, loaded from a directory under `evals/`.

    `name` identifies the case. `prompt_lines` is one organic user line
    per turn. `world` is the seeded store state plus the frozen clock
    and zone. `exact` is the structural write rows that must match byte
    for byte, in the verb/target/field/value shape of
    `fixtures/*/expected.tsv`. `forbidden` is (verb, target) pairs that
    must not appear at all, which is how a halted session asserts zero
    Sets writes and a retype asserts zero second rows. `rubric` is the
    criteria a judge model scores the spoken lines against, because a
    confirm line is composed prose and cannot be asserted byte for
    byte.
    """

    name: str
    prompt_lines: list[str]
    world: dict[str, object]
    exact: list[tuple[str, str, str, str]]
    forbidden: list[tuple[str, str]]
    rubric: list[str]


@dataclass(frozen=True)
class CaseResult:
    """The outcome of running one `EvalCase` for `samples` repetitions."""

    case: str
    samples: int
    exact_passes: int
    forbidden_violations: list[str]
    judge_scores: list[int]


def load_case(case_dir: Path) -> EvalCase:
    """Reads one `evals/<NN-name>/` directory into an `EvalCase`."""
    ...  # TODO


def run_case(case: EvalCase, model: str, samples: int) -> CaseResult:
    """Runs `case` against `model` `samples` times. A single sample
    proves nothing about a stochastic system, so `samples` defaults to 3
    at the call site."""
    ...  # TODO


def passed(result: CaseResult, safety: bool) -> bool:
    """A safety case needs every sample to pass, because one miss on a
    halt or a pain flag is a real injury risk. Any other case needs a
    majority, because a single stochastic miss on ordinary phrasing is
    not evidence of a broken rule."""
    ...  # TODO


def main() -> int:
    """Runs every case under `evals/`, prints a pass/fail summary,
    returns 1 on any case that failed `passed`."""
    ...  # TODO


if __name__ == "__main__":
    raise SystemExit(main())
