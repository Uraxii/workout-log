"""Notion's own `notion-create-database` rules, encoded once.

Production never calls `POST /v1/databases`. It calls the hosted MCP tool
`notion-create-database`, whose `schema` argument is a SQL DDL `CREATE TABLE`
statement and whose `parent` is a separate argument. This module validates
that call.

**This module must never read `schema/notion-schema.json`.** A validator that
checks the repo's schema against the repo's schema is circular and proves
nothing (ticket workout-log-yir). Every constant and every rule below is
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

# Nothing in research/19 caps the property count, the property-name length,
# whether a zero-property data source is legal, or whether the initial data
# source accepts a name. All four are listed under "UNSOURCED — do not
# enforce". They stay unchecked on purpose; adding one here would invent an
# API rule the sources do not support.
UNENFORCED = ("max property count", "max property-name length",
              "zero-property data source", "initial data source name")

# `selectColor`, research/19 rule 15.
SELECT_COLORS = frozenset((
    "default", "gray", "brown", "orange", "yellow", "green", "blue",
    "purple", "pink", "red"))

# Type keywords the tool accepts, research/19 "Type syntax". Split by whether
# the keyword takes a parenthesised argument list, because research/19 rule 9
# turns on exactly that: the configuration object of a simple type is empty,
# and `emptyObject` sets `additionalProperties: false`.
SIMPLE_TYPES = frozenset((
    "TITLE", "RICH_TEXT", "DATE", "PEOPLE", "CHECKBOX", "URL", "EMAIL",
    "PHONE_NUMBER", "STATUS", "FILES", "CREATED_TIME", "LAST_EDITED_TIME"))
# A relation with no target and a formula with no expression cannot be
# rendered at all; a select with no options is legal, Notion adds them as
# rows use them (research/19 `multi_select` row).
ARG_REQUIRED = frozenset(("FORMULA", "RELATION", "ROLLUP"))
ARG_OPTIONAL = frozenset(("SELECT", "MULTI_SELECT"))
ARG_TYPES = ARG_REQUIRED | ARG_OPTIONAL
# NUMBER and UNIQUE_ID take a trailing modifier word, never parentheses.
MODIFIER_TYPES = {"NUMBER": "FORMAT", "UNIQUE_ID": "PREFIX"}
KNOWN_TYPES = SIMPLE_TYPES | ARG_TYPES | frozenset(MODIFIER_TYPES)

MAX_OPTIONS = 100          # rule 14, `maxItems: 100`
MAX_COMMENT_CHARS = 280    # rule 18, `propertyDescriptionRequest`
MAX_BODY_BYTES = 500 * 1024  # rule 19, request-limits

_CREATE_RE = re.compile(r"^CREATE TABLE\s*\((.*)\)$", re.DOTALL)
_COLUMN_RE = re.compile(r'^"([^"]+)"\s+(.*)$', re.DOTALL)
_TYPE_RE = re.compile(r"^([A-Z_]+)\s*(\((.*)\))?\s*(.*)$", re.DOTALL)
_PROP_RE = re.compile(r'prop\("([^"]*)"\)')
_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
# Bare words a formula may legally contain that are not property references.
_FORMULA_LITERALS = frozenset(("true", "false"))


class DdlViolation(ValueError):
    """The `notion-create-database` call would be rejected by Notion."""


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
    _validate_ddl(ddl.strip(), known_data_source_ids)


def _validate_parent(parent: object) -> None:
    """Rules 2 and 3. The MCP tool drops the REST `workspace` branch, so
    `page_id` is the only accepted form (research/19, "Can the MCP tool
    express this?")."""
    if parent is None:
        raise DdlViolation("rule 2: `parent` is required")
    if not isinstance(parent, dict):
        raise DdlViolation(
            f"rule 3: `parent` must be an object, got {parent!r}")
    if parent.get("type") != "page_id":
        raise DdlViolation(f'rule 3: `parent.type` must be "page_id", got {parent.get("type")!r}')
    page_id = parent.get("page_id")
    if not isinstance(page_id, str) or not page_id:
        raise DdlViolation(f"rule 3: `parent.page_id` must be a non-empty string, got {page_id!r}")
    if set(parent) - {"type", "page_id"}:
        raise DdlViolation(f"rule 3: unexpected keys in `parent`: {sorted(set(parent) - {'type', 'page_id'})}")


def _validate_ddl(ddl: str, known_data_source_ids: set[str]) -> None:
    body = _CREATE_RE.match(ddl)
    if body is None:
        raise DdlViolation(f"`schema` must be `CREATE TABLE (...)`, got {ddl[:60]!r}")
    columns = [_parse_column(part) for part in _split_top(body.group(1)) if part]
    names = [name for name, _, _, _ in columns]
    if len(set(names)) != len(names):
        raise DdlViolation(f"duplicate column name in {names}")
    titles = [name for name, type_name, _, _ in columns if type_name == "TITLE"]
    if len(titles) != 1:
        # Rule 8, and the tool silently auto-adds a "Name" column when the
        # DDL has no title, so a missing title never surfaces as an error.
        raise DdlViolation(
            f"rule 8: exactly one TITLE column required, found {len(titles)}: {titles}")
    for name, type_name, args, trailing in columns:
        _validate_column(name, type_name, args, trailing, names, known_data_source_ids)


def _parse_column(text: str) -> tuple[str, str, str | None, str]:
    """`"Name" TYPE[(args)] [modifier]` -> (name, type, args, trailing)."""
    column = _COLUMN_RE.match(text)
    if column is None:
        raise DdlViolation(f"column name must be double-quoted: {text!r}")
    name, rest = column.group(1), column.group(2).strip()
    parsed = _TYPE_RE.match(rest)
    if parsed is None:
        raise DdlViolation(f'column "{name}": no type keyword in {rest!r}')
    return name, parsed.group(1), parsed.group(3), parsed.group(4).strip()


def _validate_column(name: str, type_name: str, args: str | None, trailing: str,
                     all_names: list[str], known_data_source_ids: set[str]) -> None:
    if type_name not in KNOWN_TYPES:
        raise DdlViolation(f'rule 7: column "{name}" has unknown type {type_name}')
    if type_name in SIMPLE_TYPES and args is not None:
        raise DdlViolation(f'rule 9: column "{name}" is {type_name} and takes no options, got ({args})')
    if type_name in ARG_REQUIRED and args is None:
        raise DdlViolation(f'column "{name}": {type_name} requires an argument list')
    if type_name in ("SELECT", "MULTI_SELECT"):
        _validate_options(name, args or "")
    elif type_name == "RELATION":
        _validate_relation(name, args or "", known_data_source_ids)
    elif type_name == "FORMULA":
        _validate_formula(name, args or "", all_names)
    _validate_trailing(name, type_name, trailing)


def _validate_trailing(name: str, type_name: str, trailing: str) -> None:
    """Only the type's own modifier and `COMMENT 'text'` may follow a type.

    This is where the repo's non-API metadata gets caught: rule 17 (no
    `default` anywhere in `propertyConfigurationRequest`) and rule 7 (an
    unknown key matches no branch) both land here, because a DDL has no
    place to put one.
    """
    while trailing:
        word, _, rest = trailing.partition(" ")
        word = word.upper()
        if word == "COMMENT":
            literal, trailing = _take_literal(name, rest)
            if not 1 <= len(literal) <= MAX_COMMENT_CHARS:
                raise DdlViolation(
                    f'rule 18: column "{name}" COMMENT must be 1 to {MAX_COMMENT_CHARS} chars')
        elif word == MODIFIER_TYPES.get(type_name):
            _, trailing = _take_literal(name, rest)
        else:
            raise DdlViolation(f'rule 17: column "{name}" carries unsupported clause {trailing!r}')
        trailing = trailing.strip()


def _take_literal(name: str, text: str) -> tuple[str, str]:
    text = text.strip()
    if not text.startswith("'"):
        raise DdlViolation(f'column "{name}": expected a single-quoted value, got {text[:30]!r}')
    end = text.index("'", 1) if "'" in text[1:] else -1
    if end < 1:
        raise DdlViolation(f'column "{name}": unterminated single-quoted value')
    return text[1:end], text[end + 1:]


def _validate_options(name: str, args: str) -> None:
    """Rules 13, 14, 15."""
    options = [opt for opt in _split_top(args) if opt]
    if len(options) > MAX_OPTIONS:
        raise DdlViolation(f'rule 14: column "{name}" has {len(options)} options, max {MAX_OPTIONS}')
    for option in options:
        label, _, color = option.partition(":")
        label = label.strip()
        if not (len(label) > 2 and label.startswith("'") and label.endswith("'")):
            raise DdlViolation(f'rule 13: column "{name}" option {option!r} has no quoted name')
        color = color.strip()
        if color and color not in SELECT_COLORS:
            raise DdlViolation(f'rule 15: column "{name}" option colour {color!r} not in selectColor')


def _validate_relation(name: str, args: str, known_data_source_ids: set[str]) -> None:
    """Rules 10, 11, 12."""
    parts = [p for p in _split_top(args) if p]
    if not 1 <= len(parts) <= 2:
        raise DdlViolation(f'column "{name}": RELATION takes an id and an optional DUAL clause')
    target, _ = _take_literal(name, parts[0])
    if target not in known_data_source_ids:
        raise DdlViolation(
            f'rules 10-11: column "{name}" relates to {target!r}, which is not a data source '
            f"id this run has created; create its target first")
    if len(parts) == 2:
        dual = parts[1]
        if dual != "DUAL" and not (dual.startswith("DUAL '") and dual.endswith("'")):
            raise DdlViolation(f'rule 12: column "{name}" second argument must be DUAL, got {dual!r}')


def _validate_formula(name: str, args: str, all_names: list[str]) -> None:
    """Rule 16: `prop("Name")` is the only property-reference form, and the
    name inside it must exist in this same data source."""
    expression, _ = _take_literal(name, args)
    for referenced in _PROP_RE.findall(expression):
        if referenced not in all_names:
            raise DdlViolation(
                f'rule 16: column "{name}" formula references prop("{referenced}"), '
                f"which is not a column of this data source")
    remainder = re.sub(r'"[^"]*"', " ", _PROP_RE.sub(" ", expression))
    for token in _IDENT_RE.finditer(remainder):
        if token.group(0) in _FORMULA_LITERALS:
            continue
        if remainder[token.end():].lstrip().startswith("("):
            continue  # a function call, e.g. `if(...)`
        raise DdlViolation(
            f'rule 16: column "{name}" formula uses bare identifier '
            f'{token.group(0)!r}; property references must be prop("{token.group(0)}")')


def _split_top(text: str) -> list[str]:
    """Split on commas outside quotes and parentheses."""
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    quote = ""
    for char in text:
        if quote:
            buf.append(char)
            if char == quote:
                quote = ""
            continue
        if char in "'\"":
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append("".join(buf).strip())
            buf = []
            continue
        buf.append(char)
    parts.append("".join(buf).strip())
    return parts
