"""Notion's own `notion-create-database` rules, encoded once.

Production never calls `POST /v1/databases`. It calls the hosted MCP tool
`notion-create-database`, whose `schema` argument is a SQL DDL `CREATE TABLE`
statement and whose `parent` is a separate argument. This module validates
that call: the envelope and the statement as a whole. What one column may
say is `notion_columns`; how DDL is taken apart is `ddl_grammar`.

**None of the three may read `schema/notion-schema.json`.** A validator that
checks the repo's schema against the repo's schema is circular and proves
nothing (ticket workout-log-yir). Every constant and every rule is
transcribed from `research/19-notion-database-create-api.md`, which carries a
primary `developers.notion.com` URL per rule; the DDL surface itself comes
from that file's "Can the MCP tool express this?" section, read off the live
tool registry. Rule numbers in the messages are that file's numbering, under
"Rules a validator can enforce".

Rules 1 (`Notion-Version` header) and 20 (three requests per second) describe
the REST transport and have no expression in an MCP tool call, so they are
not enforced here. Everything that file marks UNSOURCED is deliberately not
enforced; see `UNENFORCED` below.
"""

from __future__ import annotations

import re

from ddl_grammar import DdlViolation, parse_column, split_top
from notion_columns import validate_column

__all__ = ["DdlViolation", "UNENFORCED", "validate_create"]

# Nothing in research/19 caps the property count, the property-name length,
# whether a zero-property data source is legal, or whether the initial data
# source accepts a name. All four are listed under "UNSOURCED - do not
# enforce". They stay unchecked on purpose; adding one here would invent an
# API rule the sources do not support.
UNENFORCED = ("max property count", "max property-name length",
              "zero-property data source", "initial data source name")

MAX_BODY_BYTES = 500 * 1024  # rule 19, request-limits

_CREATE_RE = re.compile(r"^CREATE TABLE\s*\((.*)\)$", re.DOTALL)


def validate_create(payload: dict, known_data_source_ids: set[str]) -> None:
    """Check one `notion-create-database` call. Raises `DdlViolation`.

    `known_data_source_ids` is the set of ids the caller has already been
    handed by earlier create calls. Rules 10 and 11 make a relation carry the
    `data_source_id` of a data source that exists; an id nobody has issued
    yet cannot, which is what forces the create order.
    """
    if not isinstance(payload, dict):
        raise DdlViolation(f"payload must be an object, got {type(payload).__name__}")
    if "properties" in payload:
        raise DdlViolation(
            "rule 4: no top-level `properties`; the column list lives in `schema`")
    _validate_parent(payload.get("parent"))
    ddl = payload.get("schema")
    if not isinstance(ddl, str) or not ddl.strip():
        raise DdlViolation("`schema` must be a CREATE TABLE statement")
    if len(ddl.encode()) > MAX_BODY_BYTES:
        raise DdlViolation(f"rule 19: request body over {MAX_BODY_BYTES} bytes")
    _validate_statement(ddl.strip(), known_data_source_ids)


def _validate_parent(parent: object) -> None:
    """Rules 2 and 3. The MCP tool drops the REST `workspace` branch, so
    `page_id` is the only accepted form (research/19, "Can the MCP tool
    express this?")."""
    if parent is None:
        raise DdlViolation("rule 2: `parent` is required")
    if not isinstance(parent, dict):
        raise DdlViolation(f"rule 3: `parent` must be an object, got {parent!r}")
    if parent.get("type") != "page_id":
        raise DdlViolation(
            f'rule 3: `parent.type` must be "page_id", got {parent.get("type")!r}')
    page_id = parent.get("page_id")
    if not isinstance(page_id, str) or not page_id:
        raise DdlViolation(
            f"rule 3: `parent.page_id` must be a non-empty string, got {page_id!r}")
    extra = sorted(set(parent) - {"type", "page_id"})
    if extra:
        raise DdlViolation(f"rule 3: unexpected keys in `parent`: {extra}")


def _validate_statement(ddl: str, known_data_source_ids: set[str]) -> None:
    body = _CREATE_RE.match(ddl)
    if body is None:
        raise DdlViolation(f"`schema` must be `CREATE TABLE (...)`, got {ddl[:60]!r}")
    columns = [parse_column(part) for part in split_top(body.group(1)) if part]
    names = [name for name, _, _, _ in columns]
    if len(set(names)) != len(names):
        raise DdlViolation(f"duplicate column name in {names}")
    titles = [name for name, type_name, _, _ in columns if type_name == "TITLE"]
    if len(titles) != 1:
        # Rule 8, and the tool silently auto-adds a "Name" column when the DDL
        # has no title, so a missing title never surfaces as an error at all.
        raise DdlViolation(
            f"rule 8: exactly one TITLE column required, found {len(titles)}: {titles}")
    for name, type_name, args, trailing in columns:
        validate_column(name, type_name, args, trailing, names, known_data_source_ids)
