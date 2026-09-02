"""The DDL grammar: how a `CREATE TABLE` statement is taken apart.

Syntax only. What the pieces are allowed to say is `notion_ddl`'s job. The
grammar is the one described in `research/19-notion-database-create-api.md`,
"Can the MCP tool express this?": column names double-quoted, type options
single-quoted, no escape form for either quote.
"""

from __future__ import annotations

import re

_COLUMN_RE = re.compile(r'^"([^"]+)"\s+(.*)$', re.DOTALL)
_TYPE_RE = re.compile(r"^([A-Z_]+)\s*(\((.*)\))?\s*(.*)$", re.DOTALL)


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
    return name, parsed.group(1), parsed.group(3), parsed.group(4).strip()


def take_literal(name: str, text: str) -> tuple[str, str]:
    text = text.strip()
    if not text.startswith("'"):
        raise DdlViolation(f'column "{name}": expected a single-quoted value, got {text[:30]!r}')
    end = text.index("'", 1) if "'" in text[1:] else -1
    if end < 1:
        raise DdlViolation(f'column "{name}": unterminated single-quoted value')
    return text[1:end], text[end + 1:]


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
