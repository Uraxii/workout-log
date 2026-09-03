"""Turning a stored value into the athlete's shape, and back.

SKELETON ONLY. Every body below is a TODO stub. The design is
docs/storage-section-design.md; nothing here is implemented.

Phase 2 and phase 3 of that design. One body of domain knowledge: how the
athlete counts weeks and reads dates. The store holds ISO 8601 and only
ISO 8601, because `hydrate.py` compares `Start time` lexically and keys
`sessions_by_date` on `Date`, so the stored format is a correctness
constraint and never a preference. These functions govern what she may
type and what she reads back.

Consumers, once implemented:

- `.claude/skills/session-runner/scripts/rows.py` `week_index` (rule L18,
  `Sessions.week_index`), which today hardcodes `isocalendar().week` and so
  puts every Sunday session of a Sunday-start athlete in the wrong week.
- `.claude/skills/session-runner/scripts/lifecycle.py` `_FIX_DATE_RE`
  (rule L15's 7-day backfill), which today accepts `YYYY-MM-DD` and
  nothing else.
"""

from __future__ import annotations


def week_index(local_date: str, week_start: str) -> int:
    """The week number of `YYYY-MM-DD` for an athlete whose week starts on
    `week_start` (`monday` or `sunday`).

    Monday is ISO 8601 and stays the shipped default. The number is stored,
    written once at session open, and no later read repairs a wrong one,
    which is why `week_start` is asked in the storage section before
    session 1 can open.
    """
    ...  # TODO


def read_date(text: str, date_order: str) -> str | None:
    """One date the athlete typed, as `YYYY-MM-DD`, or `None`.

    `date_order` is `iso`, `day_first` or `month_first`. ISO input is
    accepted under all three, because it is never ambiguous. `None` means
    the text holds no date this athlete's convention can resolve, and the
    caller re-asks rather than guessing a day.
    """
    ...  # TODO


def say_date(local_date: str, date_order: str) -> str:
    """`YYYY-MM-DD` rendered the way the athlete reads dates.

    Every string a seam returns is asserted byte for byte, so a fixture
    that speaks a date pins this rendering.
    """
    ...  # TODO
