# Database creation payload

`intake` never hand-copies `schema/notion-schema.json`. It reads the schema at
call time and maps each declared property type to a Notion API property
type, so the create payload is generated, not authored twice (build-plan s5.1,
s2 rule L8).

## Type mapping

| Schema `type` | Notion property type sent to `notion-create-database` |
|---|---|
| `title` | `title` |
| `rich_text` | `rich_text` |
| `number` | `number` |
| `select` (has `enum`) | `select`, options = the enum values |
| `multi_select` | `multi_select`, options = the enum values if present |
| `checkbox` | `checkbox` |
| `date` | `date` |
| `relation` | `relation`, `database_id` = the already-created id of `properties.<name>.database` |
| `formula` | `formula`, `expression` = the schema's `expression` string |

Databases are created in dependency order so a `relation` property always
points at an id that already exists: `Sessions` and `Exercises` and
`Locations` first (no relations out), then `Sets` (relations to all three).

## Payload shape, one call per database

```json
{
  "parent": {"page_id": "<the user's blank page>"},
  "title": "Sets",
  "properties": {
    "Session": {"relation": {"database_id": "<Sessions db id>"}},
    "Exercise": {"relation": {"database_id": "<Exercises db id>"}},
    "Set index": {"number": {}},
    "Set type": {"select": {"options": [{"name": "warmup"}, {"name": "working"}, {"name": "backoff"}, {"name": "dropset"}]}},
    "...": "one entry per schema.databases.Sets.properties key, in schema order"
  }
}
```

Query-before-create (rule L8): before calling `notion-create-database`,
`intake` searches the parent page for a database already named `Sets` (or
`Sessions`, `Exercises`, `Locations`); if found, it adopts that id and issues
no create call. The offline mock (`tools/mock-notion/writer.py`
`database_create`) reproduces this by keying on `(db name, parent)` and
appending nothing to the TSV on the second call.

## Catalog seeding, after the four databases exist

`Exercises` is seeded from `exercises/catalog.json` (913 rows: free-exercise-db
plus `exercises/extra.json` plus the alias table). Each row is one
`row_create("Exercises", ...)` call. Notion Free is rate-limited to roughly 3
requests per second, so 913 rows is a one-time step of **roughly 5 minutes**;
`intake` tells the user this before starting and does not block the rest of
the conversation on it finishing. The offline proof does not replay all 913
rows (they are mechanical, one per catalog entry, and add nothing the fixture
format needs to assert); it asserts the four `database-create` calls only.
