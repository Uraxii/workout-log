"""Renders one "field card" per Notion database from
`schema/notion-schema.json`.

A field card is the small markdown reference a model reads before a
`row-create`: property names, types, enum values, defaults, which
properties are formulas the store computes and must never be written,
and which magnitude columns each `measure` kind makes meaningful. It
exists because `schema/notion-schema.json` is 153 lines of JSON carrying
700-character explanatory notes, which is the wrong shape to read on
every turn. Generated, never hand-edited, so it cannot drift from the
schema.
"""

from __future__ import annotations

from pathlib import Path


def render_card(schema: dict[str, object], database: str) -> str:
    """The markdown field card for one database: property names, types,
    enum values, defaults, and which properties are formulas that must
    never be written."""
    ...  # TODO


def render_measure_table(schema: dict[str, object]) -> str:
    """The markdown table of which magnitude columns each `measure` kind
    makes meaningful."""
    ...  # TODO


def write_cards(schema_path: Path, out_dir: Path) -> list[Path]:
    """Renders every database's field card plus the measure table to
    `out_dir`, returns the paths written."""
    ...  # TODO


def is_current(schema_path: Path, out_dir: Path) -> list[str]:
    """Returns the list of card paths whose content differs from what
    `render_card` produces now. Empty list means current. Returning the
    stale paths rather than a bool is what lets `drift.py` name them in
    its failure message."""
    ...  # TODO
