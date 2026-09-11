# Exercise defaults

In plain words: this folder is the list of exercises the agent picks from when
it writes a program, and the shorthand table that turns what somebody types
into a name on that list.

## The files

- `defaults.json`. One row per exercise: `name`, `measure`, and `source`.
- `aliases.json`. Typed shorthand to `name`, 142 entries. Every alias resolves
  to a row in `defaults.json`.
- `LICENSE-free-exercise-db.md`. The Unlicense text covering the rows whose
  `source` is `free-exercise-db`.

An exercise is identified by its `name`. There is no slug and no id.

## Measures

`measure` says what a set of that exercise is made of, which is what a log
row has to hold.

- `weight_reps`. Weight and repetitions. 59 rows.
- `reps_only`. Repetitions, bodyweight or band. 35 rows.
- `hold_time`. Seconds held. 8 rows.
- `distance_load`. Distance and a load carried or covered. 3 rows.
- `distance_time`. Distance and time. 2 rows.

## Why the list is short

107 rows, not the 913 in the database it draws from. It carries what the
skills and the research actually name and nothing speculative, because a lift
it lacks still gets logged under whatever the person typed. Adding rows for
lifts nobody prescribes buys a megabyte of instructions and image paths and no
coaching.

55 rows come from [yuhonas/free-exercise-db](https://github.com/yuhonas/free-exercise-db),
Unlicense. 52 are written for this project, closing the gaps in
the catalog coverage research. Every row says which it is in its
`source` field. Nothing is fetched at runtime.

## Adding one

Append `{"name": ..., "measure": ..., "source": "extra"}` to `defaults.json`,
and add any shorthand somebody might type to `aliases.json`.

Names are unique, and unique ignoring case. No alias may shadow a name.
