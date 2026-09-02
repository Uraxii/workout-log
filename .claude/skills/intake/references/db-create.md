# Database creation payload

`intake` never hand-copies `schema/notion-schema.json`. It reads the schema at
call time and maps each declared property type to a SQL DDL column keyword,
because the hosted `notion-create-database` MCP tool takes DDL, not the REST
property object (`research/19-notion-database-create-api.md`). The call is
generated, not authored twice (build-plan s5.1, s2 rule L8).

## The renderer owns the payload

`scripts/ddl.py` reads `schema/notion-schema.json` and renders the call. There
is no type-mapping table here and no payload skeleton to copy, because a
payload hand-built from prose drifts from the schema: tickets
workout-log-29l, -3lw, -6zr and -8ms were four symptoms of that one cause.

	from ddl import create_order, create_payload
	create_payload(db, parent_page_id, data_source_ids)

- `create_order()` returns the database names in relation-graph order, so a
  relation column always names a data source that an earlier call returned.
  It is derived from the schema; adding a relation reorders the creates with
  no code change.
- `create_payload()` returns the `notion-create-database` arguments: `parent`
  (`{"type": "page_id", "page_id": ...}`), `title`, and `schema`, a SQL DDL
  `CREATE TABLE` statement. `COLUMN_DDL` in that module is the type table.
- `data_source_ids` maps an already-created database name to the id its call
  returned. **One create per turn**: the tool answers with the new data
  source id, and the next database needs it.

The rules the output must satisfy are in
`research/19-notion-database-create-api.md`, each with a primary
`developers.notion.com` URL, and are enforced offline by
`tools/mock-notion/notion_ddl.py`.

Query-before-create (rule L8): before calling `notion-create-database`,
`intake` searches the parent page for a database already named `Sets` (or
`Sessions`, `Exercises`, `Locations`); if found, it adopts that id and issues
no create call. The offline mock (`tools/mock-notion/writer.py`
`database_create`) reproduces this by keying on `(db name, parent)` and
appending nothing to the TSV on the second call.

## Catalog seeding

Seeding starts once the fourth create returns, since the creates run one per
turn. `Exercises` is seeded from `exercises/catalog.json`, which holds 913 rows:
876 vendored from free-exercise-db plus 37 in `exercises/extra.json`. The 131
aliases in `exercises/aliases.json` are a separate table and are not seeded.
Each catalog row is one `row_create("Exercises", ...)` call.

Notion paces each connection to an average of 3 requests per second, on every
plan, so 913 rows is a one-time step of **roughly 5 minutes**. The limit that
scales with the workspace plan is a separate per-workspace one with unpublished
numbers (`research/01-storage-options.md:61`,
`research/19-notion-database-create-api.md`). `intake` tells the user the
5-minute figure before starting and does not block the rest of the conversation
on it finishing.

The offline proof does not replay all 913 rows, because they are mechanical,
one per catalog entry, and add nothing the fixture format needs to assert. It
asserts the `database-create` calls only.
