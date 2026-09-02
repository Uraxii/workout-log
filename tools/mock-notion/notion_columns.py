"""What one DDL column may say, per Notion's own rules.

`notion_ddl` owns the call envelope; this module owns a single column's type
and its configuration. Every constant is transcribed from
`research/19-notion-database-create-api.md`; rule numbers in the messages are
that file's numbering under "Rules a validator can enforce".
"""

from __future__ import annotations

import re

from ddl_grammar import DdlViolation, split_top, take_literal

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
# NUMBER and UNIQUE_ID take a trailing modifier word, never parentheses.
MODIFIER_TYPES = {"NUMBER": "FORMAT", "UNIQUE_ID": "PREFIX"}
KNOWN_TYPES = SIMPLE_TYPES | ARG_REQUIRED | ARG_OPTIONAL | frozenset(MODIFIER_TYPES)

MAX_OPTIONS = 100          # rule 14, `maxItems: 100`
MAX_COMMENT_CHARS = 280    # rule 18, `propertyDescriptionRequest`

_PROP_RE = re.compile(r'prop\("([^"]*)"\)')
_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
# Bare words a formula may legally contain that are not property references.
_FORMULA_LITERALS = frozenset(("true", "false"))


def validate_column(name: str, type_name: str, args: str | None, trailing: str,
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
            literal, trailing = take_literal(name, rest)
            if not 1 <= len(literal) <= MAX_COMMENT_CHARS:
                raise DdlViolation(
                    f'rule 18: column "{name}" COMMENT must be 1 to {MAX_COMMENT_CHARS} chars')
        elif word == MODIFIER_TYPES.get(type_name):
            _, trailing = take_literal(name, rest)
        else:
            raise DdlViolation(f'rule 17: column "{name}" carries unsupported clause {trailing!r}')
        trailing = trailing.strip()


def _validate_options(name: str, args: str) -> None:
    """Rules 13, 14, 15."""
    options = [opt for opt in split_top(args) if opt]
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
    parts = [p for p in split_top(args) if p]
    if not 1 <= len(parts) <= 2:
        raise DdlViolation(f'column "{name}": RELATION takes an id and an optional DUAL clause')
    target, _ = take_literal(name, parts[0])
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
    expression, _ = take_literal(name, args)
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


