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
not enforced here. `UNENFORCED` below lists what else goes unchecked, and it
is meant to be read as a promise: a rule that fires is not allowed to sit in
it.
"""

from __future__ import annotations

import re

from ddl_grammar import DdlViolation, parse_column, split_top
from notion_columns import validate_column

__all__ = ["DdlViolation", "UNENFORCED", "validate_create"]

# What goes unchecked, and why each entry is honest.
#
# The first three are research/19's "UNSOURCED - do not enforce" list; adding
# one here would invent an API rule the sources do not support. Its fourth
# entry, "whether a zero-property data source is legal", used to sit in this
# tuple and was a falsehood printed to the user: rule 8 wants exactly one
# TITLE column, so `CREATE TABLE ()` is rejected either way (workout-log-2as).
# `_self_check` now pins that rejection so the entry cannot creep back.
#
# The last two are the parts of the MCP tool schema's grammar no source gives
# a vocabulary for. ROLLUP's arity and quoting are checked; what its three
# values may name is not. Same for the text after UNIQUE_ID PREFIX.
UNENFORCED = ("max property count", "max property-name length",
              "initial data source name",
              "ROLLUP rel_prop/target_prop/function values",
              "UNIQUE_ID prefix text")

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


def _self_check() -> None:
    """Every rule, shown rejecting something. A rule nobody has watched
    reject is not a rule (`principle-prove-it-works`); this is the guard
    against one going inert under a later edit.

        python3 tools/mock-notion/notion_ddl.py
    """
    parent = {"type": "page_id", "page_id": "b55c9c91"}

    def raises(payload: dict, ids: set[str] = frozenset()) -> str:
        """The violation message, asserting there is one."""
        try:
            validate_create(payload, set(ids))
        except DdlViolation as violation:
            return str(violation)
        raise AssertionError(f"accepted, should not have: {payload!r}")

    def rejects(schema: str, ids: set[str] = frozenset(), **extra) -> str:
        return raises({"parent": parent, "schema": schema, **extra}, ids)

    validate_create({"parent": parent, "schema": 'CREATE TABLE ("N" TITLE)'}, set())
    assert "rule 2" in raises({"schema": 'CREATE TABLE ("N" TITLE)'})
    assert "rule 3" in raises({"parent": "root-page", "schema": "x"})
    assert "rule 4" in rejects('CREATE TABLE ("N" TITLE)', properties={})
    assert "rule 7" in rejects('CREATE TABLE ("N" TITLE, "x" GEOPOINT)')
    assert "rule 8" in rejects('CREATE TABLE ("x" NUMBER)')
    assert "rule 8" in rejects('CREATE TABLE ("N" TITLE, "M" TITLE)')
    assert "rule 9" in rejects("CREATE TABLE (\"N\" TITLE, \"x\" CHECKBOX('a'))")
    assert "rules 10-11" in rejects("CREATE TABLE (\"N\" TITLE, \"r\" RELATION('Sessions'))")
    assert "rule 12" in rejects("CREATE TABLE (\"N\" TITLE, \"r\" RELATION('d', SINGLE))", {"d"})
    assert "rule 13" in rejects('CREATE TABLE ("N" TITLE, "s" SELECT(a))')
    assert "rule 14" in rejects('CREATE TABLE ("N" TITLE, "s" SELECT(%s))'
                                % ", ".join(f"'o{i}'" for i in range(101)))
    assert "rule 15" in rejects("CREATE TABLE (\"N\" TITLE, \"s\" SELECT('a':chartreuse))")
    assert "rule 16" in rejects("CREATE TABLE (\"N\" TITLE, \"f\" FORMULA('Load / 2'))")
    assert "rule 16" in rejects("CREATE TABLE (\"N\" TITLE, \"f\" FORMULA('prop(\"Nope\")'))")
    assert "rule 17" in rejects("CREATE TABLE (\"N\" TITLE, \"s\" SELECT('a') DEFAULT 'a')")
    assert "rule 17" in rejects("CREATE TABLE (\"N\" TITLE, \"f\" FORMULA('1') NULL_WHEN 'x')")
    assert "rule 18" in rejects("CREATE TABLE (\"N\" TITLE COMMENT '%s')" % ("x" * 281))
    assert "rule 19" in rejects('CREATE TABLE ("N" TITLE COMMENT \'%s\')' % ("x" * MAX_BODY_BYTES))
    # Nothing inside parentheses rides along unread (workout-log-2as). One
    # case per parser in `ddl_grammar`, because one discarded remainder is all
    # it takes to turn the whole module back into a rubber stamp.
    assert "rule 16" in rejects(
        'CREATE TABLE ("N" TITLE, "f" FORMULA(\'prop("N")\', Reps, DROP TABLE))')
    assert "rules 10-11" in rejects(
        'CREATE TABLE ("N" TITLE, "r" RELATION(\'d\' AND MORE JUNK))', {"d"})
    assert "rule 12" in rejects(
        "CREATE TABLE (\"N\" TITLE, \"r\" RELATION('d', DUAL 'a' 'b' 'c'))", {"d"})
    assert "rule 13" in rejects("CREATE TABLE (\"N\" TITLE, \"s\" SELECT('a' 'b'))")
    assert "rule 16" in rejects(
        'CREATE TABLE ("N" TITLE, "f" FORMULA(\'prop("N") + Reps (1)\'))')
    assert "ROLLUP" in rejects("CREATE TABLE (\"N\" TITLE, \"u\" ROLLUP('anything'))")
    assert "ROLLUP" in rejects("CREATE TABLE (\"N\" TITLE, \"u\" ROLLUP('a','b',c))")
    assert "rule 17" in rejects("CREATE TABLE (\"N\" TITLE, \"n\" NUMBER FORMAT 'x' JUNK)")
    # `zero-property data source` is not in UNENFORCED because rule 8 rejects
    # one. This is the line that keeps that tuple honest.
    assert "rule 8" in rejects("CREATE TABLE ()")
    # Accepted: every legal form the renderer can emit, plus the two argument
    # shapes it does not yet emit. The formula is the schema's real e1RM
    # guard, so `if(...)`, `and` and `empty()` are proven to survive the
    # bare-identifier check (ticket workout-log-8jb).
    validate_create({"parent": parent, "schema": (
        'CREATE TABLE ("N" TITLE COMMENT \'the name\', "L" NUMBER FORMAT \'dollar\', '
        "\"s\" SELECT('a':blue), \"m\" MULTI_SELECT, \"r\" RELATION('d', DUAL 'back'), "
        "\"u\" UNIQUE_ID PREFIX 'X', \"p\" ROLLUP('r','L','sum'), "
        "\"f\" FORMULA('if(prop(\"R\") >= 1 and prop(\"R\") <= 10, "
        "prop(\"L\") * 36 / (37 - prop(\"R\")), empty())'), \"R\" NUMBER)")}, {"d"})
    print(f"notion_ddl self-check: ok. not enforced: {', '.join(UNENFORCED)}")


if __name__ == "__main__":
    _self_check()
