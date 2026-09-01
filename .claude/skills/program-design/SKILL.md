---
name: program-design
description: Fires on "make me a plan", a training block ending, or any newly opened config/limits entry. Picks a template from library/ against the athlete's profile, writes it to program/current with the reason stated, resolves a starting load from the intake baseline, and swaps one exercise in place when a new limits entry rules it out. Use whenever the athlete needs a program picked, started, or adjusted for a new restriction.
---

# program-design

Conversation belongs here; picking, retrieving, the baseline math, and every
write belong to `scripts/design.py`, pure and fixture-replayable
(`design_turn(line, state) -> {"writes", "say", "state"}`,
docs/architecture.md "The script seam"). `scripts/library.py` retrieves from
`library/`; `scripts/baselines.py` reads a `weight x reps` out of the
athlete's own words; `scripts/loads.py` turns that into a starting weight;
`scripts/substitutions.py` reads the swap table; `scripts/program_page.py`
owns what `program/current` holds. Never free-generates a program: every
template comes back verbatim from a `library/*.json` file (build-plan s7.1's
ten templates), adapted, not invented.

## Three kinds of turn, checked in that order

1. **A GAP category.** `library.refusal_for` matches the line against
   `references/wording.md`'s five categories (rings-specific calisthenics,
   dedicated loaded carries, named-restriction mobility, in-season
   maintenance, full-body hypertrophy, build-plan s7.2). No template exists
   for these; the reply is the scripted three-option refusal, no writes, no
   silence, no invented template.
2. **A new limits entry.** A line naming a newly opened restriction ("new
   limits entry: knee") swaps the one exercise it rules out for the
   substitute in `references/substitutions.md`, everywhere it appears in the
   active `rotation`, and writes the swapped program back to `program/current`
   (build-plan s6 trigger column, lim L-21). The swap is in the stored body,
   so the next chat reads the program the athlete actually has. Nothing else
   in the program changes: this is a swap, not a rebuild. An area with no substitute row
   says so and changes nothing, rather than guessing at a replacement.
3. **Everything else: a plan request.** `library.pick_template` runs
   `references/templates.md`'s rule table against the day count and the
   athlete's words, first match wins. Those words are this line PLUS the
   `goal`, `equipment` and `training_age` already on `config/athlete`, and
   the day count is this line's "3 days a week" or, failing that,
   `config/athlete.days_per_week`. An athlete who answered intake is never
   made to repeat the answers, and `min_days` filters on a real number
   instead of always on zero. GZCLP's own row has the widest match (any
   barbell strength goal, 3+ days), so it is the standing default for the
   common case once no more specific rule fires first, matching the
   3-day-barbell-commercial-gym profile most athletes walk in with.

## Starting loads

The baseline is the answer intake stored on
`config/athlete.strength_baseline` ("185x5 on squat"), or one typed into the
plan request itself. `baselines.parse` reads both the same way, pairing each
named lift with its nearest `NxR`, and for every block carrying a `start`
rule:

1. The typed weight converts to the arithmetic basis, kilograms
   (`loads.to_kg`, docs/unit-and-magnitude-model.md s1). It is in the
   athlete's unit, `config/preferences.units`, never assumed to be pounds.
2. Brzycki e1RM from that weight and the reps (`loads.brzycki_e1rm`,
   research/07-baselining-and-assessment.md s4.1), never above 10 reps.
3. A form allowance (`loads.FORM_ALLOWANCE_PCT`, 10%) haircuts that estimate,
   since it stands in for a real tested max the block's `start.test`
   (`1rm`/`3rm`/`5rm`) expects.
4. `loads.resolve_start_load` runs the same Brzycki relation in reverse to
   price that rep count off the adjusted estimate, applies `start.pct`,
   converts back to the athlete's unit and floors to something loadable
   there: 5 lb or 2.5 kg. Rounding happens in the unit the athlete loads,
   never in the basis, and always down.

The result writes to `Exercises.training_max` (the adjusted estimate itself)
and `Exercises.next_target` (the resolved starting weight, always carrying
its unit) via `row-create`, one write per exercise a baseline was given for.
A block with no `start` rule (GZCLP's T2 and T3, for example) gets no
computed load here; the source gives no single number worth asserting either
(`library/gzclp.json` notes).

## `load_pct`, `after_misses`, `side`, `user_says_easy`

Four format fields close gaps the first library round left open
(`schema/program-schema.json`, `docs/program-format.md`): a set's fraction of
`training_max` (nSuns' waves), a miss count before `on_miss` fires (BBR
deloads after 3, not 1), which side a prescription repeats for
(`kettlebell-wiki.json`'s get-up), and a feel-based advance kind
(`easy-strength.json`). Ask "did that feel easy?" only for a block whose
`progression.advance_when.kind` is `user_says_easy`; every other kind stays
silent between sessions.

## Turn 1, from cold

Three reads, in order. `config_read("program/current")` for the whole active
program: `body` is the picked template verbatim, JSON encoded, `template_id`
is its `library/` id, and `started_at` is when it was picked. Parse `body`
with `scripts/program_page.py::read_page`, never by hand. It answers `None`
for a page that is empty, unparsable, or from another `format_version`, and
all three mean the same thing: there is no active program, "what am I doing
today" has no answer, and this skill picks one. Nothing is repaired and no
half-built program is ever handed on.
`config_read("config/athlete")` for the profile that drives the pick,
`days_per_week`, `goal`, `equipment`, `training_age` and
`strength_baseline`; with an empty profile `references/templates.md`'s rule
table has nothing to match on, so ask rather than fall through to the GZCLP
default. `config_read("config/limits")` for open `entries`, since each one
can rule an exercise out and force the swap in "A new limits entry" above.

## Never

Never invent a template, a rep scheme, or a substitute exercise no reference
file names. Never rewrite the whole program for one restriction; swap the one
block. Never silently drop a plan request into a GAP category's refusal, or
the reverse.
