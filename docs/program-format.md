# Program file format

One JSON object per template in `library/`, stored verbatim in the Notion
config page `program/current` and archived to `program/history/<date>`
(build-plan s6, s1.8). The file never changes at runtime: every moving number
lives in Notion, under the `progression` key on the agent's own bookkeeping
page, `agent/progression-state` (`stage_index`, `variation_index`,
`next_target`, s1.6), or in the cursor. `progression` is JSON, `{exercise
name: {field: value}}`. One shape covers all ten templates of
s7.1, with no second schema. Machine-checkable form:
`schema/program-schema.json` (draft 2020-12), checked by
`python3 library/check.py`, standard library only.

## Top level

| Field | Type | Meaning |
|---|---|---|
| `format_version` | integer `1` | Bumps only on a breaking shape change |
| `name` | string | Template name, the `program/current` header |
| `origin` | string | Credit line: author, and where the structure is published |
| `source` | object | `url`, optional `method_url`, `note` stating we wrote the structure ourselves |
| `progression_unit` | `session \| week \| block \| level` | *When* progression is evaluated. Notion enum, s1.8 |
| `dose` | `sets \| minutes` | How the work is prescribed. Notion enum, s1.8 |
| `days` | integer | Sessions per week the source prescribes |
| `notes` | string, optional | Anything no field carries |
| `rotation` | array of nodes | Ordered, at least one. The cursor indexes it |

## Node

`{"id": "A1", "label": "A1 (squat T1, bench T2)", "blocks": [...]}`
`blocks` empty means a **rest node**: show the label, take `done`, `rest`,
`skip` or any bare acknowledgement, write no set, advance the cursor (rule
L17). No `kind` field, so a node cannot claim to be a rest day while carrying
work. A day with a walk to log is a work node with one block.

## Block

One exercise's prescription. Exactly one of `exercise` or `sequence`.

| Field | Type | Meaning |
|---|---|---|
| `exercise` | string | Exercise name, e.g. `Barbell Squat`. Identity is the name; there is no slug |
| `sequence` | array of prescriptions | Ordered inner steps repeated `sets` times: C25K run/walk, kettlebell ladders, complexes |
| `label` | string | Tier or group shown in the opener, e.g. `T1` |
| `sets` | integer | Sets, or repeats of `sequence` |
| `reps` / `rep_range` | integer / `[lo, hi]` | Fixed reps, or the double-progression window |
| `amrap_last` | bool | Last set to failure (`is_amrap` on the row) |
| `duration_s`, `distance`, `interval_s`, `level` | int, `{value, unit}`, int, int | The nullable magnitude columns of `Sets`, s1.2. Which apply is decided by the catalog row's `measure`, never restated here |
| `rest_s` | integer | Rest target for the confirm line |
| `load_pct` | number, optional | Fraction of `progression[exercise].training_max` this set loads to, e.g. `0.85` for 85%. Carries a wave (nSuns): each `sequence` step sets its own. Absent means load comes from `start` or `next_target` instead |
| `side` | `each \| left \| right \| both`, optional, default `both` | `each` repeats the prescription once per side, alternating (a kettlebell get-up); `left`/`right` pin one side; `both` is bilateral or side-agnostic |
| `start` | start rule | Where the first load comes from |
| `progression` | progression rule | Absent means the block never advances by itself |
| `stages` | array of prescriptions | Ordered alternatives for this block; the current one is `progression[exercise].stage_index` |
| `note` | string | Free text for the opener |

A **prescription** carries the same magnitude fields plus `exercise`, and
overrides the block's when it is the active stage or a sequence step. That one
merge rule serves GZCLP set-and-rep stages and Otago level variants alike.

## Progression rule

```json
{"axis": "weight", "increment": 10, "increment_unit": "lb",
 "advance_when": {"kind": "all_prescribed_reps"},
 "on_miss": "next_stage",
 "reset": {"kind": "retest_pct", "test": "5rm", "pct": 0.85, "stage": 0}}
```

- `axis`: `weight | reps | level | duration | none`. *What* moves. The
  top-level `progression_unit` says *when* it is evaluated.
- `increment` plus `increment_unit` (`lb | kg | reps | levels | s`).
- `advance_when.kind`, a closed set, not an expression language:
  `all_prescribed_reps` (linear, GZCLP T1/T2), `top_of_rep_range` (double
  progression, RR, PHUL hypertrophy days), `amrap_at_least` + `reps` (GZCLP T3
  at 25), `sessions_at_stage` + `count` (Otago levels, time-based dose),
  `user_says_easy` (feel-based, Easy Strength: the coach asks whether the
  weight felt easy, and only for a block that carries this kind).
- `on_miss`: `hold | next_stage | deload`, with `deload_pct` for the last, fired
  after `after_misses` consecutive misses (integer, default `1`: fires on the
  first miss).
- `reset` fires when `on_miss` is `next_stage` and no stage is left. Same shape
  as `start`: `{"kind": "retest_pct", "test": "5rm", "pct": 0.85}` or
  `{"kind": "load_delta", "value": 15, "unit": "lb"}`, plus a `stage` index.

## Today, in one lookup

The cursor is `{"node": <index>, "cycle": <n>}`, stored in `Sessions.Cursor`
(advisory, rule L8) and in `program/current`. Today is `rotation[cursor.node]`,
one array index. Per block: the active prescription is
`stages[progression[exercise].stage_index]` merged over the block, the load is
`progression[exercise].next_target` written by `load-adjust` at last close, or
`start` on the first session. `progression[exercise]` itself reads from
`agent/progression-state`, the agent's own bookkeeping. Nothing is searched.
Advancing is
`(node + 1) % len(rotation)`, `cycle` incremented on wrap, the same operation
for a rest node.

## Mini example: double progression, a rest node, an interval day

```json
{"format_version": 1, "name": "Example", "origin": "us",
 "source": {"url": "-", "note": "illustration only"},
 "progression_unit": "session", "dose": "sets", "days": 2,
 "rotation": [
   {"id": "A", "label": "Day A", "blocks": [
     {"exercise": "Barbell_Squat", "sets": 3, "rep_range": [5, 8],
      "progression": {"axis": "weight", "increment": 5, "increment_unit": "lb",
       "advance_when": {"kind": "top_of_rep_range"}, "on_miss": "hold"}}]},
   {"id": "R", "label": "Rest", "blocks": []},
   {"id": "B", "label": "Day B (intervals)", "blocks": [
     {"sets": 8, "sequence": [{"exercise": "Running", "duration_s": 60},
                              {"exercise": "Walking", "duration_s": 90}]}]}]}
```

## HYPOTHESIS

- Not a hypothesis any more: `python3 tools/catalog/check.py` fails the build
  if any `library/` template prescribes a name `exercises/defaults.json` does
  not carry, so the whole library is checked on every run, not just
  `gzclp.json`. `Running` and `Walking` are both in the defaults.
- `sequence` is claimed to cover C25K, kettlebell EMOM and ladders, unproven
  until those two templates are authored. Same for the four `advance_when`
  kinds: a template needing a fifth means the shape is wrong, not the template.
- GZCLP T2 and T3 starting loads are left to intake. The cited sources give no
  single number worth asserting here.
- `rotation` is fully expanded, so Couch to 5k becomes 27 nodes rather than 9
  plus a repeat count. Untested against file size and reader load.
