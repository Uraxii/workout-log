"""Turn `schema/notion-schema.json` into `notion-create-database` calls.

The hosted MCP tool takes a SQL DDL `CREATE TABLE` statement, not a Notion
REST properties object, and returns the new data source id. One call creates
one database, and `create_payload` renders one call.

The schema declares no relation column, because Notion holds logs only: every
value is a string, number, date, select or checkbox, so no database points at
another. That is what removed the create-ordering problem this module used to
solve with a graph walk. Databases are created in schema declaration order.

This module is the reason `references/db-create.md` stopped carrying a
payload skeleton: an LLM hand-building a payload from prose drifts from the
schema (tickets workout-log-29l, -3lw, -6zr, -8ms are four symptoms of that
one cause), so the schema is read by code instead. The rules this output is
checked against live in `tools/mock-notion/notion_ddl.py` and come from
`research/19-notion-database-create-api.md`; nothing here is validated
against itself.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import storage

# <skill>/data is the copy tools/package/build_zip.py vendors into the ZIP;
# the repo root is the shared original a plugin checkout keeps (build-plan s8).
# Same resolution as session-runner/scripts/rows.py.
_SKILL_DIR = Path(__file__).resolve().parent.parent
_DATA_ROOT = (
    _SKILL_DIR / "data" if (_SKILL_DIR / "data").is_dir()
    else _SKILL_DIR.parents[2]
)
SCHEMA_PATH = _DATA_ROOT / "schema" / "notion-schema.json"


class RenderError(ValueError):
    """The schema declares something no DDL column can express."""


def _select(keyword: str, spec: dict[str, Any]) -> str:
    """`enum` becomes the option list. Notion assigns colours itself, so the
    schema declares none and none are emitted. A select with no declared
    enum takes no option list at all; Notion adds options as rows use them."""
    options = ", ".join(f"'{_literal(value)}'" for value in spec.get("enum", []))
    return f"{keyword}({options})" if options else keyword


# One row per schema `type`. A table, not a branch chain: adding a Notion
# type is a row here and nothing else (`principle-code-quality`). Repo-only
# metadata keys (`default`, `null_when`, `frozen_at`, `rule`, `range`,
# `written_by`, `derived_from`, `advisory_only`) are never read, so they
# cannot leak into the call.
COLUMN_DDL: dict[str, Callable[[dict[str, Any]], str]] = {
    "title": lambda spec: "TITLE",
    "rich_text": lambda spec: "RICH_TEXT",
    "number": lambda spec: "NUMBER",
    "checkbox": lambda spec: "CHECKBOX",
    "date": lambda spec: "DATE",
    "select": lambda spec: _select("SELECT", spec),
    "multi_select": lambda spec: _select("MULTI_SELECT", spec),
    "formula": lambda spec: f"FORMULA('{_literal(spec['expression'])}')",
}


def load_schema(path: Path = SCHEMA_PATH) -> dict[str, Any]:
    return json.loads(path.read_text())


def render(db: str, schema: dict[str, Any] | None = None) -> str:
    """One `CREATE TABLE` statement for one database, in schema property order."""
    properties = (schema or load_schema())["databases"][db]["properties"]
    columns = []
    for name, spec in properties.items():
        column = COLUMN_DDL.get(spec["type"])
        if column is None:
            raise RenderError(f"{db}.{name}: no DDL column for type {spec['type']!r}")
        columns.append(f'"{_literal(name, chr(34))}" {column(spec)}')
    return f"CREATE TABLE ({', '.join(columns)})"


def create_payload(db: str, parent_page_id: str,
                   schema: dict[str, Any] | None = None) -> dict[str, Any]:
    """The `notion-create-database` arguments for one database."""
    return {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": db,
        "schema": render(db, schema),
    }


def next_create_write(state: dict[str, Any]) -> list[dict[str, Any]]:
    """At most one `database-create` write: the next database still missing.

    One call per database, in schema declaration order, with the caller
    threading each returned data source id back into `state["databases"]`
    (ticket workout-log-29l) so a rerun adopts rather than duplicates.

    The parent page id is the user's, read from `state`. `intake` asking for
    it is ticket workout-log-mqs; with no id there is nothing to create under
    and the questions still run.
    """
    parent = state.get("notion_parent_page_id")
    created = state.get("databases", {})
    if parent is None:
        return []
    if not storage.is_proven(storage.named(state)):
        # Gate 1 of two (docs/storage-section-design.md "Refusing a
        # store"). Not one `database-create` for a store this build has no
        # DDL for, so nothing is created under the athlete's page.
        return []
    for db in load_schema()["databases"]:
        if db not in created:
            return [{"verb": "database-create", "target": db,
                     "payload": create_payload(db, parent)}]
    return []


def _literal(text: object, quote: str = "'") -> str:
    """DDL quotes have no escape form, so a value carrying its own delimiter
    is rejected here rather than silently producing a broken statement. A
    formula expression is single-quoted and its `prop("Name")` references are
    double-quoted, which nests without escaping."""
    if quote in str(text):
        raise RenderError(f"{text!r} contains a {quote} no DDL literal can carry")
    return str(text)


if __name__ == "__main__":
    for _db in load_schema()["databases"]:
        print(f"-- {_db}")
        print(render(_db))
