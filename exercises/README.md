# Exercise catalog

`catalog.json` (913 rows) is generated. Never edit it by hand.

## Sources

- `free-exercise-db.json` — vendored [yuhonas/free-exercise-db](https://github.com/yuhonas/free-exercise-db),
  876 rows, Unlicense (public domain), text in `LICENSE-free-exercise-db.md`.
  No live API call at runtime.
- `extra.json` — 37 rows authored for this project, closing the probe gaps
  in `research/15-exercise-catalog-coverage.md`. Seed record shape plus a
  `measure` field.
- `aliases.json` — authored alias table, `alias -> canonical id`. Rung 2 of
  the fallback ladder in `docs/build-plan.md` s3.2.

## Rebuild

`python3 tools/catalog/build.py`

Idempotent: rerunning produces byte-identical output. Also validates:
unique ids, every `measure` is a real `schema/notion-schema.json` measure
kind, every alias resolves to a real id, no alias collides with an id.

## Adding a row

Append to `extra.json` in the seed's record shape (`id`, `name`, `force`,
`level`, `mechanic`, `equipment`, `primaryMuscles`, `secondaryMuscles`,
`instructions`, `category`) plus `measure`. Rebuild. Add any shorthand a
user might type for it to `aliases.json`.
