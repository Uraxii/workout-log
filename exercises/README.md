# Exercise defaults

`defaults.json` is 103 exercises the agent reads when it builds a program. It
is package reference data and is **never written to the athlete's Notion
workspace**: Notion holds logs only. Authored by hand, not generated.

An exercise is identified by its `name`. There is no slug and no id. The name
is what a `Sets` row stores, what a `library/` template prescribes, and what
an alias resolves to.

## The files

- `defaults.json` - one row per exercise: `name`, `measure` (a
  `schema/notion-schema.json` measure kind), and `source`, which records
  where the row came from and is the per-row attribution.
- `aliases.json` - authored alias table, `typed shorthand -> name`. Rung 2 of
  the fallback ladder in `docs/build-plan.md` s3.2.
- `LICENSE-free-exercise-db.md` - the Unlicense text covering the 55 rows
  whose `source` is `free-exercise-db`.

## Why 92 and not 913

The list is the union of every exercise a shipped artifact names: the 48 the
ten `library/` templates prescribe, every target of the alias table, the
substitutes in `program-design/references/substitutions.md`, and the four
lifts `baselines.LIFT_ALIASES` reads out of a spoken strength baseline. It
carries nothing speculative, because it does not have to: a lift it lacks
still logs, under the name the athlete typed, through rung 4 of the ladder.

The 913-row build came from vendoring free-exercise-db whole so that every
row could be seeded into a Notion `Exercises` database. There is no such
database, so there is no reason to carry 1 MB of instructions and image
paths for lifts nothing prescribes.

## Sources

55 rows are taken from
[yuhonas/free-exercise-db](https://github.com/yuhonas/free-exercise-db),
Unlicense (public domain), text in `LICENSE-free-exercise-db.md`. 37 are
written for this project, closing the probe gaps in
`research/15-exercise-catalog-coverage.md`. Every row says which it is in its
`source` field. No live API call at runtime.

## Adding one

Append `{"name": ..., "measure": ..., "source": "extra"}` to `defaults.json`
and add any shorthand a user might type to `aliases.json`. Then:

	python3 tools/catalog/check.py

which holds the three files to one answer: names unique and unique
case-insensitively, every `measure` a real measure kind, every alias
resolving to a name, no alias shadowing a name, and every exercise a
`library/` template prescribes present.
