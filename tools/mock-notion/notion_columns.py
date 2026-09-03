"""What one DDL column may say, per Notion's own rules.

`notion_ddl` owns the call envelope; this module owns a single column's type
and its configuration. Two sources feed it, and they are not interchangeable:

- `research/19-notion-database-create-api.md`, which carries a primary
  `developers.notion.com` URL per rule. Every `rule N` in a message below is
  that file's numbering under "Rules a validator can enforce".
- The live `notion-create-database` MCP tool schema, read off this session's
  tool registry on 2026-09-02 (research/19, "Can the MCP tool express this?",
  quotes the part this repo needs). The 19 type keywords and their argument
  shapes come from there and only from there: research/19 lists the subset
  the repo uses, so it is not the provenance for the whole list. The tool
  schema is a grammar, not an API rule. It says how a column is written; the
  numbered rules say what the written column may then contain.
"""

from __future__ import annotations

import re
from typing import Callable

from ddl_grammar import (DdlViolation, only_literal, split_top, take_clauses,
                         take_option)

# `selectColor`, research/19 rule 15.
SELECT_COLORS = frozenset((
    "default", "gray", "brown", "orange", "yellow", "green", "blue",
    "purple", "pink", "red"))

# The 19 type keywords, transcribed from the MCP tool schema:
#
#   TITLE  RICH_TEXT  DATE  PEOPLE  CHECKBOX  URL  EMAIL  PHONE_NUMBER
#   STATUS  FILES  CREATED_TIME  LAST_EDITED_TIME
#   NUMBER [FORMAT 'x']              UNIQUE_ID [PREFIX 'X']
#   SELECT('opt':color, ...)         MULTI_SELECT('opt':color, ...)
#   FORMULA('expression')
#   RELATION('data_source_id'[, DUAL ['synced_name' ['synced_id']]])
#   ROLLUP('rel_prop','target_prop','function')
#
# Split by argument shape, because research/19 rule 9 turns on exactly that:
# the configuration object of a simple type is empty, and `emptyObject` sets
# `additionalProperties: false`.
SIMPLE_TYPES = frozenset((
    "TITLE", "RICH_TEXT", "DATE", "PEOPLE", "CHECKBOX", "URL", "EMAIL",
    "PHONE_NUMBER", "STATUS", "FILES", "CREATED_TIME", "LAST_EDITED_TIME"))
# NUMBER and UNIQUE_ID take a trailing modifier word, never parentheses.
MODIFIER_TYPES = {"NUMBER": "FORMAT", "UNIQUE_ID": "PREFIX"}

MAX_OPTIONS = 100          # rule 14, `maxItems: 100`
MAX_COMMENT_CHARS = 280    # rule 18, `propertyDescriptionRequest`

_PROP_RE = re.compile(r'prop\("([^"]*)"\)')
_IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
# Bare words a formula may legally contain that are not property references:
# the two boolean literals, and the three logical operators, which Notion
# writes as words as well as symbols ("true and false", "not true") per
# <https://www.notion.com/help/formula-syntax>, the page
# <https://developers.notion.com/reference/property-object#formula> names as
# the formula syntax reference. Without these, rule 16 reads `and` as a
# property named "and" and rejects every guarded expression.
_FORMULA_LITERALS = frozenset(("true", "false", "and", "or", "not"))
# Functions a formula may call. `prop` is substituted out before the scan;
# `if` and `empty` are the two the repo's own expressions use and the two the
# pages above show. Anything else is reported as a bare identifier, which is
# the safe direction: a real Notion function missing from this set fails
# loudly and gets added with its source, where the old test (any identifier
# with a `(` after it) waved `Reps (1)` through as a call and lost rule 16.
_FORMULA_FUNCTIONS = frozenset(("if", "empty"))
# `fullmatch`, so a third literal cannot ride along behind DUAL unread.
_DUAL_RE = re.compile(r"DUAL(?:\s+'[^']*'){0,2}")


def _validate_trailing(name: str, type_name: str, trailing: str) -> None:
    """Only the type's own modifier and `COMMENT 'text'` may follow a type.

    This is where the repo's non-API metadata gets caught: rule 17 (no
    `default` anywhere in `propertyConfigurationRequest`) and rule 7 (an
    unknown key matches no branch) both land here, because a DDL has no
    place to put one.
    """
    for word, literal in take_clauses("rule 17", name, trailing):
        if word == "COMMENT":
            if not 1 <= len(literal) <= MAX_COMMENT_CHARS:
                raise DdlViolation(
                    f'rule 18: column "{name}" COMMENT must be 1 to {MAX_COMMENT_CHARS} chars')
        elif word != MODIFIER_TYPES.get(type_name):
            raise DdlViolation(
                f'rule 17: column "{name}" carries unsupported clause {word} {literal!r}')


def _validate_options(name: str, args: str) -> None:
    """Rules 13, 14, 15."""
    options = [opt for opt in split_top(args) if opt]
    if len(options) > MAX_OPTIONS:
        raise DdlViolation(f'rule 14: column "{name}" has {len(options)} options, max {MAX_OPTIONS}')
    for entry in options:
        _, colour = take_option("rule 13", name, entry)
        if colour and colour not in SELECT_COLORS:
            raise DdlViolation(f'rule 15: column "{name}" option colour {colour!r} not in selectColor')


def _validate_relation(name: str, args: str, known_data_source_ids: set[str]) -> None:
    """Rules 10, 11, 12."""
    parts = [p for p in split_top(args) if p]
    if not 1 <= len(parts) <= 2:
        raise DdlViolation(f'column "{name}": RELATION takes an id and an optional DUAL clause')
    target = only_literal("rules 10-11", name, parts[0])
    if target not in known_data_source_ids:
        raise DdlViolation(
            f'rules 10-11: column "{name}" relates to {target!r}, which is not a data source '
            f"id this run has created; create its target first")
    if len(parts) == 2 and not _DUAL_RE.fullmatch(parts[1].strip()):
        raise DdlViolation(f'rule 12: column "{name}" second argument must be DUAL, got {parts[1]!r}')


def _validate_formula(name: str, args: str, all_names: list[str]) -> None:
    """Rule 16: `prop("Name")` is the only property-reference form, and the
    name inside it must exist in this same data source."""
    expression = only_literal("rule 16", name, args)
    for referenced in _PROP_RE.findall(expression):
        if referenced not in all_names:
            raise DdlViolation(
                f'rule 16: column "{name}" formula references prop("{referenced}"), '
                f"which is not a column of this data source")
    remainder = re.sub(r'"[^"]*"', " ", _PROP_RE.sub(" ", expression))
    for token in _IDENT_RE.finditer(remainder):
        word = token.group(0)
        if word in _FORMULA_LITERALS:
            continue
        if word in _FORMULA_FUNCTIONS and remainder[token.end():].lstrip().startswith("("):
            continue
        raise DdlViolation(
            f'rule 16: column "{name}" formula uses bare identifier '
            f'{word!r}; property references must be prop("{word}")')


def _validate_rollup(name: str, args: str) -> None:
    """`ROLLUP('rel_prop','target_prop','function')`, the tool schema's only
    form. No source says what the three values may hold, so the arity and the
    quoting are all this checks, and `notion_ddl.UNENFORCED` says so."""
    parts = [p for p in split_top(args) if p]
    if len(parts) != 3:
        raise DdlViolation(
            f'column "{name}": ROLLUP takes three quoted values '
            f"('rel_prop','target_prop','function'), got {len(parts)}")
    for part in parts:
        only_literal("ROLLUP", name, part)


# One row per type keyword that takes a parenthesised argument list: whether
# the list is required, and the validator that reads it. A table, not a branch
# chain, so a keyword cannot be declared and left unread the way ROLLUP was
# (workout-log-2as). `ARG_REQUIRED` is derived from the same rows, so the two
# cannot drift apart.
ArgValidator = Callable[[str, str, list[str], set[str]], None]
ARG_TYPES: dict[str, tuple[bool, ArgValidator]] = {
    # A relation with no target and a formula with no expression cannot be
    # rendered at all; a select with no options is legal, Notion adds them as
    # rows use them (research/19 `multi_select` row).
    "FORMULA": (True, lambda name, args, names, ids: _validate_formula(name, args, names)),
    "RELATION": (True, lambda name, args, names, ids: _validate_relation(name, args, ids)),
    "ROLLUP": (True, lambda name, args, names, ids: _validate_rollup(name, args)),
    "SELECT": (False, lambda name, args, names, ids: _validate_options(name, args)),
    "MULTI_SELECT": (False, lambda name, args, names, ids: _validate_options(name, args)),
}
ARG_REQUIRED = frozenset(name for name, (required, _) in ARG_TYPES.items() if required)
KNOWN_TYPES = SIMPLE_TYPES | frozenset(ARG_TYPES) | frozenset(MODIFIER_TYPES)


def validate_column(name: str, type_name: str, args: str | None, trailing: str,
                    all_names: list[str], known_data_source_ids: set[str]) -> None:
    if type_name not in KNOWN_TYPES:
        raise DdlViolation(f'rule 7: column "{name}" has unknown type {type_name}')
    if type_name not in ARG_TYPES and args is not None:
        raise DdlViolation(f'rule 9: column "{name}" is {type_name} and takes no options, got ({args})')
    if type_name in ARG_REQUIRED and args is None:
        raise DdlViolation(f'column "{name}": {type_name} requires an argument list')
    if type_name in ARG_TYPES:
        ARG_TYPES[type_name][1](name, args or "", all_names, known_data_source_ids)
    _validate_trailing(name, type_name, trailing)
