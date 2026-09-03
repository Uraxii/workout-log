---
name: load-adjust
description: Fires at the end of a set, an exercise, a session, and on any performance question ("how's my squat going", "why did my run get slower"). Applies the active program's progression rule (docs/program-format.md) to decide bump, hold, or deload for one exercise, steps a level or variation axis instead of weight when the rule says so, and carries the HRT-aware read for a performance question. Never invents a rule the program didn't state. Use whenever a set, an exercise, or a session closes, or the user asks how a lift is trending.
---

# load-adjust

Conversation belongs here; the progression arithmetic, the deload ask, and
the progression write-back belong to `scripts/rules.py` (pure arithmetic)
and `scripts/load_adjust.py` (turn dispatch, `docs/architecture.md` "The
script seam"). `scripts/read_layer.py` is the s1.7 read-time layer: e1RM,
unit display conversion, and ranking, read-only over `Sets` rows, never
called from a write path. `scripts/parse.py` is text-in and `scripts/say.py`
is text-out: every line the athlete reads lives in the latter.

## A number it can't read is refused out loud, never guessed, never dropped

`parse.number` and `parse.count` are the only places user text becomes a
number. Anything they reject raises `parse.Unreadable`, caught once at
`adjust_turn`'s exit, which discards the whole turn: zero writes, state
untouched, and one line naming the bad token and the shape that would have
worked. Three outcomes were possible for a malformed line and two are worse.
A traceback mid-workout has failed the athlete. A guessed number is worse,
by this project's standing rule. Logging nothing and saying "Noted." is
worst of all, because the athlete walks away believing the set landed. The
refusal holds under `progression: manual` too: on the PEM hard-stop path a
bad line still answers, still writes nothing (ayf.12).

Accepted: `185x8`, `185.5x8`, `bw+25x8`, `bw-25x8`, bare whole rep counts,
comma-separated lists of those, an optional trailing `rpe=<n>`. Refused:
words including spoken numbers (`five`), empty tokens and empty set fields,
negatives (`-50x5`), fractional rep counts (`8.5`), a malformed or empty
`rpe=`, any other trailing field, and a `setup` field whose `increment`,
`deload_pct`, `current`, `after_misses` or `rep_range` will not parse.
Spoken numbers are refused here on purpose: `session-runner`'s
`tokens.normalize` accepts them, this seam does not yet, and closing that
gap is its own ticket (ayf.24).

## The off switch comes first (rule S5's hard stop)

Before evaluating anything, check `config/limits.progression`. If it is
`manual`, no bump, hold, or deload evaluation runs, full stop: log the
line and say so. This skill has no code path that ever writes `progression`
back to `auto`; only `screen` (a re-run) or `session-runner` (a 14-day
symptom-free window) can clear it (rule S8). A bare reassurance
("I'm fine") gets a plain answer explaining that, never a cleared switch,
whether it lands here or at `pain-triage` (rule S5, `docs/limitations.md`
L-42).

## Small bumps are automatic, deloads and -10% drops ask first (rule S7)

All prescribed sets at the top of the rep range, RPE not pinned at 9.5+ for
two sessions running: bump the load one increment, write `next_target`, say
the bump in one line. That is the whole automatic path.

"Two sessions running" means consecutive (research/03 rule 4), so the streak
counts every session that reports an RPE, hit or missed, and any session
below 9.5 resets it. A session reporting no RPE also resets it: RPE is
accept-if-typed and never prompted, and this cap is a backstop rather than
the operating point. A session with no sets at all is not a successful
session; it holds and says there is nothing to adjust (ayf.8, ayf.12).

A miss (every set below the bottom of the range) increments `fail_count`.
Below `after_misses`, hold and say so. At the threshold, the program's
`on_miss` decides: `hold` stays put, `next_stage` moves the ladder with no
load change (GZCLP's cheap intermediate step, research/03 s6), and `deload`
is the only path that asks before writing anything to the load. The
question states the exact drop and the resulting number; the reply is
`yes`/`no` on the very next turn.

## Declined once, not re-offered (`deload_declined_at`, lim L-22)

`no` writes `deload_declined_at` and records the fail-count streak it was
declined at. The same streak never asks again; only a fresh streak past
that point re-offers.

## Weight, level, or variation: one engine, three targets (lim L-20)

The program's `axis` field says what moves: `weight` writes
`next_target`, `level` writes `stage_index` (Otago-style dosage
levels), `variation` writes `variation_index` (a bodyweight-fitness chain,
research/03 s11: "if the data model treats variation index and load as the
same abstract difficulty axis, one engine covers both"). Same top-of-range
trigger, same miss counter, different field. HYPOTHESIS: `level`'s real
rule is a session count (`sessions_at_stage`), not top-of-range; this pass
reuses the weight-axis trigger for both, a documented simplification, not a
second rule to maintain.

## Assistance reads the right direction (lim L-05)

`load_kind = assist` means the number is help subtracted from bodyweight,
not a weight added to it. A bump there *lowers* the stored `Load` (less
assistance, harder set) and a deload *raises* it (more assistance, easier).
`read_layer.effective_difficulty` inverts the sign once so a trend or a
ranking query never reads a falling assist number as regression, or a
rising one as progress. Never describe an assist trend as "rising" in the
same sense a barbell number rising means: say "less assist" instead.

## The read-time layer (s1.7, lim L-35, L-36)

Storage never normalizes: a row keeps the unit it was logged in.
`read_layer.rank_best` converts every row to one display unit before
comparing e1RM, so a mixed lb/kg history still finds the right best lift.
`read_layer.e1rm` is the same relation as the `Sets.e1RM` Notion formula,
reused from `program-design/scripts/loads.py` rather than re-derived.

## HRT branch, stated plainly (research/11, lim L-44)

On feminizing HRT, hemoglobin and endurance fall in the first few months
while strength holds; a slower pace or a higher heart rate in that window
is the hormone, not a stall, and is never read as a deload trigger. On
masculinizing HRT, year one is the best strength window most trans men
get; load can progress aggressively while volume stays conservative,
because tendon adaptation lags the faster muscle gain. Both notes are
descriptive, sourced to research/11, and read out on a performance
question when the athlete's HRT direction is on file. Never a diagnosis,
never a cause, never a recommendation to change dose or timing; that is
always the client's own clinician.

## Turn 1, from cold

`config_read("config/limits")` first, always, for `progression`. `manual` is
the hard stop above: nothing else in this skill runs, whatever the remaining
reads would have said. Then, for the exercise in question,
`row_query("Sets", {"Exercise": <name>})` for its history and
`config_read("program/current")` for the `progression` key, whose JSON body
is `{exercise name: {field: value}}` and holds `training_max`, `next_target`,
`fail_count`, `deload_declined_at` and `stage_index`. That state used to be
an `Exercises` row and is not a log, so it lives on the program page now.
Rows come back raw, in
the unit they were logged in; `scripts/read_layer.py` converts and ranks
them, and this skill never does that itself. An empty `Sets` result means no
history: hold, say there is nothing to adjust yet, never bump and never read
a trend off one point.

## Never

Never guess at a number the grammar could not read, and never swallow one
silently; refuse it by name. Never bump off a session with no sets in it.
Never write a deload without an explicit `yes` on the very next turn.
Never write `progression: manual` back to `auto`. Never read an assist
row's falling `Load` as a decline, or a rising one as progress. Never
invent a progression rule the program didn't state; a bare `weight_reps`
exercise with no rule on file just holds and says there is nothing to
adjust yet.
