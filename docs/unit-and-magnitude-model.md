# Units and magnitudes

Five confirmed defects (`workout-log-ayf.1`, `.2`, `.3`, `.6`, `.7`) share one
cause: no module owns the question "what is a load, in what unit, and is it
plausible", so five files each answered it. This document settles the answer so
the five fixes implement one shape.

Read this before touching any of the five sites. Every claim below was
reproduced against head `2f0fc51`; the commands are in
"What was run".

## Contents

1. [The canonical basis](#1-the-canonical-basis)
2. [One e1RM](#2-one-e1rm)
3. [Loadable rounding](#3-loadable-rounding)
4. [Plausibility bounds](#4-plausibility-bounds)
5. [Where each rule lives](#5-where-each-rule-lives)
6. [Contradictions with the build plan](#6-contradictions-with-the-build-plan)
7. [What was run](#7-what-was-run)
8. [Left open](#8-left-open)

## 1. The canonical basis

**A magnitude that enters arithmetic is a float in kilograms.** Rows are
untouched: `Load` and `Unit` still store the number the user typed, in the unit
the user typed it. The basis exists only between the two conversion functions.

Two functions are the whole boundary, and they live in
`.claude/skills/program-design/scripts/loads.py`:

	to_kg(value: float, unit: str) -> float
	to_display(value_kg: float, unit: str) -> float

Between those two calls, no function takes a unit argument. The naming rule
that makes this checkable by eye: a variable holding a magnitude either carries
a `_kg` suffix, or it sits in a row dict beside its own `Unit` key. A bare
`load` float with an implicit unit is the bug, and it is what
`read_layer.trend_label` holds today.

### Why kilograms, not pounds

The international pound is defined as exactly 0.45359237 kg. So lb to kg is an
exact decimal scaling, and kg to lb is a non-terminating division. A kg basis
means every conversion *into* arithmetic is exact and only the conversion out
for display loses anything. The repo already carries the constant, once, as
`read_layer.KG_PER_LB`.

The reviewer's objection is fair: the current athlete logs in lb, so a kg basis
converts every number twice for no visible benefit. I still prefer kg, because
the alternative is picking a basis by whoever the first user was, and the whole
defect family is about a default that stopped being questioned.

### Where the conversion happens

The boundary is the point where a row dict becomes a number. In `load-adjust`
that point is one function, `read_layer.effective_difficulty`, which every
ranking and trend path already calls. So:

- `effective_difficulty(row)` returns kilograms.
- `rank_best` and `trend_label` stop converting for themselves.

Today `rank_best` converts and `trend_label` does not, which is
`workout-log-ayf.1` exactly. Observed on the history
`[225 lb, 230 lb, 110 kg]`:

	rank_best(lb) -> 110 kg row, e1RM 272.82 lb    (correct)
	trend_label   -> declining                     (wrong; 110 kg = 242.51 lb)

Fixing `trend_label` alone leaves the next reader free to add a sixth unit-blind
consumer. Moving the conversion into `effective_difficulty` means a new
consumer gets it by construction.

**Storage is not affected.** `docs/build-plan.md:45` says the typed number is
"never normalised at rest", and this model keeps that. The basis is
arithmetic-only.

## 2. One e1RM

**The source of truth is the relation `e1RM = Load * 36 / (37 - Reps)`**, the
exact Brzycki rational, already implemented as
`loads.brzycki_e1rm`. The schema's expression is rewritten to match it.

The schema currently says `Load / (1.0278 - 0.0278 * Reps)`, which is the same
relation with 37/36 and 1/36 truncated to four decimals. Observed drift:

	load  reps | python              | schema              | delta
	 315     5 | 354.375             | 354.4104410441044   | 0.035
	1000    10 | 1333.3333333333333  | 1333.6889837289943  | 0.356

A third of a pound is not a training problem. It is a correctness problem: two
numbers claim to be the same field, so a "best ever" answered from Notion and
one answered from Python can disagree about which set won.

Notion formulas do multiplication and division, so nothing is lost by writing
the exact form. Python does not change.

### Behaviour at the edges

| Reps | e1RM | Why |
|---|---|---|
| 0 | null | Brzycki is undefined below one rep, and a zero-rep set is a failed attempt, not a max. |
| 1 | `Load`, unchanged | 36/36. A single is its own 1RM. No special case needed. |
| 2 to 10 | the formula | Brzycki's validated range. |
| above 10 | null | Outside the validated range. Brzycki reads high and keeps climbing. |

Python already returns `None` for `Reps < 1`. The schema does not: its
`null_when` is `["Reps > 10", "Set type != working"]`, so `100 x 0` evaluates to
97.295 (observed). That number outranks nothing, but it sorts, and it is
non-null in a column whose whole purpose is "sort and take one". Add `Reps < 1`
to `null_when`.

### The column is canonical too

Rename the column `e1RM_kg` and make the expression convert:

	(if(Unit == "kg", Load, Load * 0.45359237)) * 36 / (37 - Reps)

`docs/build-plan.md:102` claims that sorting this column with `page_size=1`
answers "best ever" in one request. That claim is false today for a mixed-unit
history, because Notion sorts the raw number: 225 lb produces a larger e1RM
than 110 kg, and 110 kg is the heavier lift. Making the column canonical is
what makes the one-request claim true, and it is the same single-basis rule as
section 1 applied on the storage side.

The column name carries its unit for the same reason every other constant here
does. `e1RM` alone is a number whose meaning depends on which row you read it
from.

### How the agreement is enforced

A document saying "these must agree" is the thing that failed. The mechanism is
a check:

	tools/schema/check_e1rm.py

It reads the expression string out of `schema/notion-schema.json`, evaluates it
with a small `ast`-based evaluator restricted to the arithmetic and comparison
nodes a Notion formula uses, and compares the result against `loads.brzycki_e1rm`
composed with `loads.to_kg` over a fixed grid: reps 0, 1, 2, 5, 10, 11; both
units; and the `1000 x 10` case that exposed the drift. Any mismatch above 1e-9
exits non-zero. Wire it into `make check` beside the other offline proofs.

Before trusting it, flip one digit of the schema expression and watch the check
go red. A guard nobody has seen fail proves nothing.

Two directions were possible: generate one implementation from the other, or
compare them. Python cannot be generated from a Notion formula string, so
comparison is the cheaper direction and the only one that survives either side
being edited.

## 3. Loadable rounding

`loads.round_to` is deleted. It rounds to 5 in any unit and inherits Python's
banker's rounding, so it ties to even. Observed:

	round_to(182.5, 5) -> 180      round_to(187.5, 5) -> 190
	round_to(192.5, 5) -> 190      round_to(197.5, 5) -> 200
	round_to(2.5, 5)   -> 0

The same 2.5 offset rounds down at 182.5 and up at 187.5. Nobody chose that.

Its replacement:

	round_down_to_increment(value: float, unit: str) -> float

	LOADABLE_INCREMENT = {"lb": 5.0, "kg": 2.5}

### The increments

- **lb: 5.** Plates load in pairs and the smallest pair in a normal gym is
  2.5 lb a side.
- **kg: 2.5.** Same argument, 1.25 kg a side.
- **Machine stack: from the exercise, not from the unit.** A stack moves in
  whatever pin spacing it has. This needs a nullable `load_increment` on
  `Exercises`, which overrides the unit default when set. That field does not
  exist yet, so machines fall back to the unit default. Marked open in
  section 8.
- **Bodyweight-only: nothing to round.** `Load` is null, and
  `rules.TARGET_FIELD` already routes those exercises to the `level` or
  `variation` axis instead of a weight. `round_down_to_increment` is never
  called on them.

### Round in the athlete's unit, then stop

Convert to the athlete's unit first, then round in that unit. Rounding in the
canonical basis and converting afterwards produces unloadable numbers: 90 kg is
a clean plate load and 198.42 lb is not.

### Ties do not exist

Every caller wants the same direction:

- A bump rounds down, so a prescription never exceeds what the rule computed.
- A deload rounds down. Rounding a deload up defeats the deload, which is the
  whole reason the athlete is being given one.
- A start load rounds down. The form allowance in `loads.estimated_max` already
  assumes the first block should be conservative.

Since every direction is down, the direction parameter is unnecessary and the
function floors. No tie-breaking rule is needed, because floor has no ties.

Two consequences the caller owns, not the rounding function:

- A bump that floors back to the current weight has not moved. `rules.bumped_value`
  takes one increment when that happens. The floor rule lives in the progression
  domain, where "did the athlete progress" is a meaningful question.
- `round_down_to_increment(2.5, "lb")` is 0, an empty bar. That is a
  plausibility failure, not a rounding failure, and section 4 owns it.

Today `rules.deload_target` never rounds at all. Observed: 185 lb deloads to
166.5 and 47.5 kg deloads to 42.75. Neither number can be loaded.

## 4. Plausibility bounds

**Bounds are declared once, in `schema/notion-schema.json`, as a `range` on the
magnitude property.** They are enforced from that one declaration in two places,
neither of which is a copy of the numbers:

- `tools/mock-notion/writer.py::_validate` already rejects unknown properties
  and bad enum values against the schema. Four more lines make it reject an
  out-of-range number too. Every fixture, every skill, every `make check` run.
- The seam refuses before it emits a write. `rows.py` already loads
  `schema/notion-schema.json` for `measure_kinds`, so it reads the same ranges
  and gains `reject_implausible(measure, fields) -> str | None`.

Putting the bounds in the schema is what keeps `session-runner` from needing a
cross-skill import (see section 5).

### The bounds

Stated in the row's own unit, because that is what gets stored.

| Magnitude | Range | Catches |
|---|---|---|
| `Load` | 0 to 1000 lb, 0 to 500 kg | `-15 lb`; `1850` typed for `185` |
| `Reps` | 1 to 100 | a bare `185` read as 185 reps |
| `duration_s` | 1 to 14400 | a stopwatch left running |
| `distance` | above 0, up to 100 km | a unit misread |
| `interval_s` | 1 to 3600 | an EMOM parsed as a rep count |

`Load` has no negative case in any `load_kind`. Assistance already carries its
direction in `load_kind = assist`, so a negative `Load` is both redundant and
ambiguous: `-15 lb` with `load_kind = absolute` has no reading.

The upper bounds catch typos, not athletes. 1000 lb is above the heaviest lift
any human has recorded, so nothing real is refused.

### Refuse, do not clamp

On a violation the seam **refuses and asks**. It never clamps.

The argument, since asserting it would be the same mistake in a different
place. A clamp turns an input error into a plausible-looking data point that
nothing downstream can tell apart from a real one. Every defect in this family
has that shape. `-200` became `Load = -15 lb`, which looked like a load.
`185` became `Reps = 185`, which looked like reps. A kg athlete's start load
became `75 lb`, which looked like a target. Each one survived because some layer
produced a number rather than stopping. A clamp would be a sixth instance of the
same failure, shipped deliberately.

The costs are not symmetric. Refusing costs one round trip and the user retypes
the line. Clamping costs a wrong personal record in a history the user is
expected to trust, and this log is close enough to a medical record that a
number they did not lift is worse than a question they did not want. Observed
today: `rank_best` on a single `-100 lb` row reports e1RM `-112.5` as a best
ever.

`docs/build-plan.md:165-166` already settled this shape for a neighbouring
case, "an unknown unit suffix refuses to guess rather than falling through". The
rule here is the same rule, applied to a magnitude rather than a unit token.
`grammar._unit_of` does not implement it yet; it defaults instead.

### The refusal is not a note

Rung 5 of the fallback ladder writes the verbatim line as a `Notes` row, which
is right for text the grammar could not parse. An out-of-range number *was*
parsed. It is understood and not believed, which is a different answer and
needs a different path: a `confirm_line` that names the bound and echoes what it
read, so the user can see which reading went wrong.

One clamp survives, and it is not a guess: `rules.bumped_value` clamps assistance
at `max(current - delta, 0)`. Zero assistance is a real physical state. It has a
separate problem, noted in section 8.

## 5. Where each rule lives

### Module ownership

No new shared module. `program-design/scripts/loads.py` is 45 lines, already
holds `brzycki_e1rm` and `round_to`, and is already imported by
`load-adjust/scripts/read_layer.py`. It is the shared load-math module already;
it is just missing the conversion functions. Adding a second one would give the
codebase two places to look.

So `loads.py` gains `to_kg`, `to_display`, `round_down_to_increment`, and
`LOADABLE_INCREMENT`, and loses `round_to` and `WEIGHT_ROUND_LB`.
`read_layer.to_unit` is deleted; its callers use `loads.to_kg` and
`loads.to_display`.

### The cross-skill import constraint

Skills are packaged independently and an extracted ZIP has no repo root
(`workout-log-ayf.14`). The repo has exactly two cross-skill import edges today,
`load-adjust -> program-design` and `intake -> screen`, and both break a
single-skill upload.

**This model adds no third edge.** The consumers of unit conversion and rounding
are `load-adjust` and `program-design`, which is the edge that already exists.
The consumer that has no edge is `session-runner`, and its need is plausibility
bounds, which are data, not code. `rows.py` already resolves
`schema/notion-schema.json` through the `<skill>/data` copy that
`tools/package/build_zip.py` vendors, falling back to the repo root. Bounds ride
along in that file for free.

That is the reason bounds live in the schema rather than in `loads.py`. Domain
purity would put them next to the conversion functions. Packaging says
otherwise, and packaging is the constraint that actually breaks.

If a later change does need `session-runner` to call `loads.py`, the mechanism
already exists: add the file to `BUNDLED_DATA` in
`tools/package/build_zip.py` and resolve it through the same `<skill>/data`
pattern `rows.py`, `library.py`, and `catalog.py` all use. Do not add a
`sys.path` insert to a sibling skill directory.

### Defect to function

| Defect | Owning function | Module |
|---|---|---|
| `ayf.1` trend reads mixed units backwards | `effective_difficulty` returns kg; `trend_label` and `rank_best` stop converting | `.claude/skills/load-adjust/scripts/read_layer.py:49,59,80` |
| `ayf.2` start loads hardcoded to lb | `_plan_turn` reads the athlete's unit from state; `resolve_start_load` takes a `unit` and calls `round_down_to_increment`; `loads.format_load` renders the unit | `.claude/skills/program-design/scripts/design.py:144-148` and `.claude/skills/program-design/scripts/loads.py:45` |
| `ayf.3` negative loads and a bare `185` | `range` declared in the schema; `rows.reject_implausible` refuses; `writer._validate` enforces | `schema/notion-schema.json`, `.claude/skills/session-runner/scripts/rows.py`, `tools/mock-notion/writer.py:179` |
| `ayf.6` two disagreeing e1RMs | `loads.brzycki_e1rm` is the source; the schema expression is rewritten to match; `tools/schema/check_e1rm.py` enforces it in `make check` | `.claude/skills/program-design/scripts/loads.py:22` and `schema/notion-schema.json:51` |
| `ayf.7` deload never rounded, ties to even | `loads.round_down_to_increment` replaces `loads.round_to`; `rules.deload_target` and `rules.bumped_value` call it | `.claude/skills/program-design/scripts/loads.py:33` and `.claude/skills/load-adjust/scripts/rules.py:22,29` |

## 6. Contradictions with the build plan

The build plan is still content authority, so each of these needs reconciling
by whoever owns that document.

- **`docs/build-plan.md:102`**, the e1RM expression. The plan states
  `Load / (1.0278 - 0.0278 * Reps)`. Section 2 replaces it with
  `Load * 36 / (37 - Reps)`, converted to kilograms. The plan's line must change
  or the schema and the plan disagree by the 0.356 measured above.
- **`docs/build-plan.md:102`**, the one-request claim. "Sort plus `page_size=1`
  answers best ever in one request" is false today for a mixed-unit history and
  becomes true only once the column is canonical.
- **`docs/build-plan.md:102`**, `null_when`. The plan gives two null conditions.
  Section 2 adds `Reps < 1`.
- **`docs/build-plan.md:58`**, the column name `e1RM`. Section 2 renames it
  `e1RM_kg`.
- **`docs/build-plan.md:45`** is *not* contradicted, and this is stated so
  nobody reads section 1 as overturning it. "Raw number typed, never normalised
  at rest" stands. The canonical basis exists only inside arithmetic.
- **`docs/build-plan.md:165-166`** is not contradicted either. Its refuse rule
  for unknown unit suffixes is the same rule section 4 applies to magnitudes.
  It is simply not implemented; `grammar._unit_of` defaults instead of
  refusing.

## 7. What was run

The attack-pass probes at `/tmp/wl-attack/probes/`, copied to `/tmp/wl-live/`
with `_paths.py` repointed at this repo:

	mkdir -p /tmp/wl-live
	cp /tmp/wl-attack/probes/*.py /tmp/wl-live/
	# _paths.py rewritten to point at
	# /var/home/nicole/Projects/workout-log/.claude/skills
	cd /tmp/wl-live && python3 p2_units.py
	cd /tmp/wl-live && python3 p3_e1rm.py
	cd /tmp/wl-live && python3 p4_grammar.py
	cd /tmp/wl-live && python3 p7_progression.py
	cd /tmp/wl-live && python3 p7b_units_program.py

What they printed, at head `2f0fc51`:

`p2_units.py`

	trend_label   -> declining   <-- lifter went 225lb -> 242.5lb
	rank_best ->  {'Load': -100, ..., 'e1RM': -112.5, 'e1RM_unit': 'lb'}

`p3_e1rm.py`

	   100   0 | None                | 97.29519361743529   | None
	  1000  10 | 1333.3333333333333  | 1333.6889837289943  | 0.35565

`p4_grammar.py`

	'-200'  -> {'Load': -15, 'Unit': 'lb', 'load_kind': 'absolute', 'Reps': 5}
	'185'   -> {'Load': 185, 'Unit': 'lb', 'load_kind': 'absolute', 'Reps': 185}
	'2.5x5' -> [{'Reps': 5}, {'Reps': 5}]

`p7_progression.py`

	185.0lb -10% -> 166.5      47.5kg -10% -> 42.75
	round_to(182.5, 5) -> 180  round_to(187.5, 5) -> 190
	round_to(2.5, 5) -> 0
	assist bump 2 -> 0 (clamped at 0, then stuck)
	evaluate(cfg, [], None, None) -> {'outcome': 'bump', 'value': 190.0}

`p7b_units_program.py`

	units=lb: {'Name': 'Barbell Squat', 'next_target': '75 lb'}
	units=kg: {'Name': 'Barbell Squat', 'next_target': '75 lb'}

Two findings outside the five tickets, both from `p4_grammar.py` and
`p7_progression.py`: `2.5x5` loses the decimal weight and reads as two sets of
five, and `evaluate` on an empty set list bumps the target. Neither is in scope
here; see section 8.

## 8. Left open

- **`Exercises.load_increment`.** Machine stacks and micro-plates need a
  per-exercise increment. Section 3 falls back to the unit default until the
  field exists. One nullable number covers stacks, plate-loaded machines and
  micro-plates; do not build a stack model.
- **Bar weight.** Nothing stops a target landing below an empty bar, because no
  bar weight is stored anywhere. `round_down_to_increment(2.5, "lb")` is 0.
- **A failed set.** `Reps: 1` as the lower bound assumes zero reps is not
  written. `0x0` currently produces `rows: []` (observed). `workout-log-ayf.4`
  owns the representation.
- **Assistance reaching zero.** `bumped_value` clamps assist at 0 and then
  sticks there forever. The athlete has graduated to unassisted and the axis
  should change. Not a units defect.
- **`2.5x5` loses its decimal.** A kg athlete's 2.5 kg warm-up reads as two sets
  of five. The `_TWO_NUM_RE` branch compares against `WEIGHT_MIN[units]` and
  falls through. Related to `ayf.3` but a separate parse decision.
- **Empty-set-list bump.** `rules.evaluate` with no sets returns `bump`, so
  closing an exercise with nothing logged raises the target. Not a units defect.
