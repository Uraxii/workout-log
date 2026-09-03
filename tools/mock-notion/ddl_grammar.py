"""The DDL grammar: how a `CREATE TABLE` statement is taken apart.

Syntax only. What the pieces are allowed to say is `notion_ddl`'s job. The
grammar is the one described in `research/19-notion-database-create-api.md`,
"Can the MCP tool express this?": column names double-quoted, type options
single-quoted, no escape form for either quote.

No function here returns text it did not read. See the comment above
`_LITERAL_RE` for why that is a rule and not a coincidence.
"""

from __future__ import annotations

import re

_COLUMN_RE = re.compile(r'^"([^"]+)"\s+(.*)$', re.DOTALL)
_TYPE_RE = re.compile(r"^([A-Z_]+)\s*(.*)$", re.DOTALL)


class DdlViolation(ValueError):
    """The `notion-create-database` call would be rejected by Notion.

    One type for one rejected call: a statement that will not parse and a
    statement Notion's rules forbid are the same outcome to the caller."""


def parse_column(text: str) -> tuple[str, str, str | None, str]:
    """`"Name" TYPE[(args)] [modifier]` -> (name, type, args, trailing)."""
    column = _COLUMN_RE.match(text)
    if column is None:
        raise DdlViolation(f"column name must be double-quoted: {text!r}")
    name, rest = column.group(1), column.group(2).strip()
    parsed = _TYPE_RE.match(rest)
    if parsed is None:
        raise DdlViolation(f'column "{name}": no type keyword in {rest!r}')
    args, trailing = _take_group(name, parsed.group(2))
    return name, parsed.group(1), args, trailing.strip()


def _take_group(name: str, text: str) -> tuple[str | None, str]:
    r"""The parenthesised argument list, if the type has one.

    Scanned, not matched with a regex: a greedy `\(.*\)` runs past the
    closing paren to a later one, so `FORMULA('if(a,b)') COMMENT 'x (y)'`
    parses as a single mangled argument list.
    """
    if not text.startswith("("):
        return None, text
    depth = 0
    quote = ""
    for i, char in enumerate(text):
        if quote:
            if char == quote:
                quote = ""
        elif char in "'\"":
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[1:i], text[i + 1:]
    raise DdlViolation(f'column "{name}": unclosed argument list')


# Every parser below is anchored to BOTH ends of the text it is given, so it
# has no remainder to hand back and no caller can drop one. That is the whole
# point of the shape: the old `take_literal` returned `(value, rest)`, three of
# its four callers bound `rest` to `_`, and `FORMULA('prop("N")', DROP TABLE)`
# and `RELATION('d' AND MORE JUNK)` rode in on the discard (workout-log-2as).
# A new argument-taking type inherits the check by having nothing else to call.
_LITERAL_RE = re.compile(r"'([^']*)'")
_OPTION_RE = re.compile(r"'([^']*)'(?:\s*:\s*([A-Za-z_]+))?")
_CLAUSE_RE = re.compile(r"([A-Za-z_]+)\s+'([^']*)'")


def _anchored(pattern: re.Pattern[str], text: str, message: str) -> re.Match[str]:
    match = pattern.fullmatch(text.strip())
    if match is None:
        raise DdlViolation(message)
    return match


def only_literal(rule: str, name: str, text: str) -> str:
    """The one single-quoted value `text` is, with nothing either side of it."""
    return _anchored(_LITERAL_RE, text, (
        f'{rule}: column "{name}" takes one single-quoted value, '
        f"got {text.strip()[:40]!r}")).group(1)


def take_option(rule: str, name: str, text: str) -> tuple[str, str]:
    """`'label'` or `'label':colour` -> (label, colour). Colour is "" if absent."""
    match = _anchored(_OPTION_RE, text, (
        f'{rule}: column "{name}" option must be \'name\' or \'name\':colour, '
        f"got {text.strip()[:40]!r}"))
    return match.group(1), match.group(2) or ""


def take_clauses(rule: str, name: str, text: str) -> list[tuple[str, str]]:
    """`WORD 'value'` repeated to the end of `text`, uppercased. [] if empty."""
    text = text.strip()
    found: list[tuple[str, str]] = []
    position = 0
    while position < len(text):
        match = _CLAUSE_RE.match(text, position)
        if match is None:
            raise DdlViolation(
                f'{rule}: column "{name}" carries unsupported clause {text[position:]!r}')
        found.append((match.group(1).upper(), match.group(2)))
        position = match.end()
        while position < len(text) and text[position].isspace():
            position += 1
    return found


def split_top(text: str) -> list[str]:
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
