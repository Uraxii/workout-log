# Routines and as-you-go logging UX

Research slice C. Written 2026-08-31. Scope: preset routines, the "what do I
have today" answer, and the set-entry grammar. Data model, progression maths,
tool survey, and trainer-agent behaviour are other slices.

---

## TL;DR

**Routine representation.** One plain-text file per program. Days are an
ordered cycle, not a calendar. Each day is a list of lines shaped
`label: Exercise / sets x reps / weight-or-%/RPE / progress: rule`, borrowed
from Liftosaur's Liftoscript. Supersets are a group tag on the line, not a
nested structure. Optional accessories are marked `?` so a time-capped session
can drop them without asking.

**Rotation.** Sequence-based with a "next unfinished" cursor, wger's
`need_logs_to_advance` model. Missing Tuesday does not skip leg day; it moves
it. Calendar dates are recorded, never used to pick the day.

**Entry grammar.** Two grammars, not one. The *routine file* is sets-first
(`3x5`, the standard convention). The *chat log* is weight-first
(`225x5x3`, `135 5/5/4`, `same`, `+5`, `x8`, `@8`). Number-count and magnitude
disambiguate: two numbers = sets x reps, three numbers = weight x reps x sets,
a lone number in a set slot = reps.

**"What do I have today."** Three lines maximum, then stop. Day name, exercise
count, estimated minutes. Then the first exercise with its target, last
performance, and warm-up ladder. Never dump the whole day unless asked.

**As-you-go flow.** Agent states one exercise. User replies in any granularity
(one set, one exercise, one whole day). Agent confirms in <=1 line and states
the next target. Session stays open until closed or auto-closed; resuming
hours later replays the cursor, never re-asks what was already logged.

---

## 1. Routine and program representation

### 1.1 What the two open-source systems actually do

**wger** models the hierarchy `Routine -> Day -> Slot -> SlotEntry`, with the
actual numbers living in separate config objects rather than on the entry:
`WeightConfig`, `MaxWeightConfig`, `RepetitionsConfig`, `MaxRepetitionsConfig`,
`SetsConfig`, `RirConfig`, `RestConfig`. Each config applies from a given
iteration and either replaces a value (`operation=r`) or steps it by an
absolute or percentage amount.
([wger routine API docs](https://wger.readthedocs.io/en/latest/api/routines.html))

wger's `Day` model carries `routine`, `order`, `type`, `name`, `description`,
`is_rest`, `need_logs_to_advance`, and a `config` JSON field.
([wger/manager/models/day.py](https://github.com/wger-project/wger/blob/master/wger/manager/models/day.py))

Three wger ideas are directly reusable here:

- A **slot with more than one entry is automatically a superset**. No separate
  superset object; the system interleaves sets across the entries.
  ([wger routine API docs](https://wger.readthedocs.io/en/latest/api/routines.html))
- **`need_logs_to_advance`** on a day "stalls the sequence on a day until the
  user logs a session for it". This is exactly the "did day 2 twice" and
  "skipped Tuesday" answer. (same source)
- **Rest days are real days** with `is_rest=true` and no slots: they occupy a
  position in the sequence but produce no exercises. (same source)

wger also has `fit_in_week` on the routine, which pads iterations with empty
placeholder days so the cycle restarts on fixed weekdays. That is the opt-in
calendar behaviour, off by default.
([wger routine API docs](https://wger.readthedocs.io/en/latest/api/routines.html))

**Liftosaur** goes the other way: the whole program is one text blob.
Weeks are `#`, days are `##`, one exercise per line:

```liftoscript
# Week 1
## Day 1
Squat / 5x5 / progress: lp(5lb)

## Day 2
Squat / 3x8
```

([liftoscript.md, "Full mode, weeks and days"](https://github.com/astashov/liftosaur/blob/master/docs/content/liftoscript.md))

Liftosaur's line grammar is the model to copy for the routine file:

| Feature | Syntax | Source |
|---|---|---|
| Sets x reps | `Bench Press / 3x8` | liftoscript.md, "Basics" |
| Rep range | `Bench Press / 3x8-12` | same |
| Multiple set groups | `Bench Press / 1x5, 1x3, 1x1, 5x5` (8 sets total) | same |
| Percent of 1RM | `Bench Press / 3x12 80%` | same |
| Absolute weight | `Bench Press / 3x12 60kg` | same |
| RPE | `Bench Press / 3x12 @8` (weight derived from RPE table) | same |
| Mixed per set | `Bench Press / 1x5 @8, 1x3 @9, 1x1 @10, 5x5 50%` | same |
| Shared section | `Bench Press / 1x12, 5x5 / 20s 60%` | same |
| AMRAP | `+` after reps: `4x5, 1x5+` | same |
| Ask for weight | `+` after weight: `3x8 / 100lb+`, or `?+` | same |
| Rest timer | bare `90s` | same |
| Active set timer | `Plank / 3x1 60s|30s` (setTimer\|restTimer) | same |
| Auto-advance circuits | `Power Clean / 5x5 135lb 60s|0s auto` | same |
| Warm-ups | `Squat / 5x5 / warmup: 1x5 45lb, 1x5 135lb, 1x3 80%`, or `warmup: none` | same |
| Supersets | `superset: A` tag on each member line | same |
| Exercise labels | `main: Squat / 5x5` vs `accessory: Squat / 3x8` | same |
| Set labels | `Squat / 4x5 (Main), 1x5+ (AMRAP)` (8 chars max) | same |
| Progression | `progress: lp(5lb)`, `dp(5lb, 8, 12)`, `sum(30, 5lb)`, `custom()` | same |
| Reuse another line | `Squat / ...Bench Press` | same |
| Repeat across weeks | `Bench Press[1-4] / 3x8` | same |
| Explicit order | `Squat[1,1-4] / 3x8` (order, week range) | same |
| Template, not in program | `T1 / used: none / 1x10+, 3x10 / 70%` | same |
| Descriptions shown to user | `// Pause **2 seconds** at the bottom` | same |
| Notes hidden from user | `/// internal note` | same |

Liftosaur's stated reason for text over tapping: a 12-week, 4-day, 5-exercise
program has ~240 places where sets are specified, and editing that by tapping
is intolerable. ([liftoscript.md, "Ways to make written programs less
repetitive"](https://github.com/astashov/liftosaur/blob/master/docs/content/liftoscript.md))

### 1.2 Proposed representation

Take Liftosaur's line syntax, wger's rotation semantics, and drop the rest.

```
# Program: Upper/Lower 4-day
rotation: sequence            # not calendar
advance: on-log               # wger need_logs_to_advance

## A - Upper Push
main: Bench Press / 3x5 / progress: lp(5lb)
Overhead Press / 3x8-12 @8
Incline DB Press / 3x10 / superset: S1
Lateral Raise / 3x15 / superset: S1
? Triceps Pushdown / 3x12          # optional, first to cut
? Face Pull / 2x20

## B - Lower
Squat / 3x5 / progress: lp(10lb)
Romanian Deadlift / 3x8
? Leg Curl / 3x12

## R - Rest
rest: true
```

Deviations from Liftosaur, and why:

- **No weeks.** Weeks force a calendar. A day is a named node in a cycle. Week
  numbers are recoverable from the log if a program ever needs them, and
  block-periodised programs can express phases as separate cycles.
- **`?` prefix = optional slot.** Liftosaur has no optional-set concept in the
  syntax I found; the closest is per-day sets. This makes the trim rule
  mechanical rather than a judgement call (section 1.5). UNVERIFIED that no
  Liftosaur equivalent exists; I checked liftoscript.md only.
- **Superset tag, not nesting.** Liftosaur's `superset: A` and wger's
  multi-entry slot agree that a flat tag beats a tree. A tree costs nothing to
  read on screen but costs a lot to speak in chat.

### 1.3 Splits: what the shape has to survive

| Split | Cycle | Notes |
|---|---|---|
| Full body 3x/wk | `A, R, B, R, C, R, R` or just `A, B, C` | Same day repeated with progression, so days differ only by progression state |
| Upper/Lower | `U, L, U, L` | 4 nodes or 2 nodes depending on whether U1 and U2 differ |
| PPL | `P, Pl, L` (x1 or x2 per week) | 3 or 6 nodes |
| Bro split | `Ch, Bk, Lg, Sh, Ar` | 5 nodes, worst fit for calendar-based rotation |

All four collapse to "ordered list of day nodes, cursor walks it". Rest nodes
are optional: if rotation is sequence-based and the cursor only advances on a
logged session, explicit rest nodes are dead weight. Include them only if the
user wants the agent to say "today is a rest day" rather than "next up is
Lower, whenever you want it".

**Recommendation: omit rest days from the cycle by default.** They only earn
their place under `fit_in_week`-style calendar anchoring, which is off.

### 1.4 Rotation state, skipped days, repeated days

Three candidate rules:

1. **Calendar-based.** Monday = day A. Miss Monday, lose day A that week.
   This is how a paper plan works and how `fit_in_week` behaves in wger
   ([source](https://wger.readthedocs.io/en/latest/api/routines.html)). Bad
   for ADHD: a missed day is a permanent loss and a guilt event.
2. **Strict sequence.** Cursor advances one node per completed session. Never
   loses a day. This is wger's `need_logs_to_advance` behaviour
   ([source](https://wger.readthedocs.io/en/latest/api/routines.html)).
3. **Next unfinished, with override.** Sequence, but the user can name any
   day and the cursor jumps there.

**Proposed: rule 3.** Default is rule 2's answer, with a one-word override.

Consequences:

- **Skipped day.** Nothing happens. The cursor did not move because no session
  was logged. Next time the user asks, they get the same day. No apology text,
  no "you missed a workout" nag. The gap is visible in the log's dates for
  anyone who wants it.
- **Did day 2 twice.** Legal. `log to B` or "do B again" writes a second B
  session and leaves the cursor at whatever follows the second B. Progression
  rules see two B sessions in a row and apply twice, which is correct.
- **Out-of-order day.** `today: legs` jumps the cursor. The skipped node is not
  pushed to the back of a queue; it is simply next after the current node,
  because the cycle is circular.
- **Partial session.** A session with at least one logged set counts as
  attempted. Whether it advances the cursor is a policy choice; propose
  **advance on close, not on first set**, so abandoning after two sets and
  coming back tomorrow resumes the same day.

Boostcamp's model is the counterexample worth noting: users skip to the next
workout by hitting "complete workout" with nothing logged, and at least one
user report says this can freeze the app
([Boostcamp workout tracker page](https://www.boostcamp.app/workout-tracker),
skip behaviour from user reviews cited in
[a Boostcamp review roundup](https://healthynexercise.com/best-free-fitness-apps/boostcamp/) —
UNVERIFIED, secondary source, no first-party doc found for skip semantics).

### 1.5 Time-capped sessions

Fitbod is the clearest first-party precedent. Users set a preferred workout
duration in the Gym Profile (15 min to 1 h 30 in the picker, 1 min to 4 h
custom), and duration drives both exercise count per session and weekly set
targets. For a one-off short day, the Quick Edits menu regenerates the workout
at 15/30/45/60/90 minutes without touching the profile
([Fitbod help centre, Gym Profile / Quick
Edits](https://help.fitbod.me/hc/en-us/articles/360004429814-How-Fitbod-Creates-Your-Workout)).

Fitbod regenerates. A preset-routine system should **trim, not regenerate**,
because regeneration destroys the progression thread the user is following.

Proposed trim ladder, applied in order until the estimate fits:

1. Drop `?` slots, last first.
2. Drop the last set of each non-`main` exercise (Liftosaur set labels give a
   way to mark which sets are droppable:
   `4x5 (Main), 1x5+ (AMRAP)`,
   [source](https://github.com/astashov/liftosaur/blob/master/docs/content/liftoscript.md)).
3. Superset the remaining accessories in pairs.
4. Cut accessories entirely, keep `main:` lines only.

State the trim as one line, do not ask for confirmation: "30 min: bench 3x5,
squat 3x5, row 3x10. Cut pushdowns and face pulls." The user can say `keep
pushdowns` if they disagree. Never open a dialogue about it.

**Duration estimate.** `sum(sets * (set_seconds + rest_seconds)) + warmup +
transition`. Rest comes from the routine's rest spec, which Liftosaur already
carries per set (`90s`) or per exercise section
([source](https://github.com/astashov/liftosaur/blob/master/docs/content/liftoscript.md)).
Calibrate `set_seconds` and transition overhead against the user's own logged
session wall-clock after ~10 sessions. Until then use 40 s per working set and
60 s per exercise transition. UNVERIFIED: these constants are my estimate, not
sourced.

---

## 2. Set-entry grammar

### 2.1 What existing tools do

**Liftosaur** (prescription context) is unambiguously sets-first: `3x8` means
three sets of eight. `1x5, 1x3, 1x1, 5x5` is eight sets
([liftoscript.md](https://github.com/astashov/liftosaur/blob/master/docs/content/liftoscript.md)).
Suffixes: `+` after reps = AMRAP, `+` after RPE = log the RPE, `+` after
weight = ask what weight was used, `?+` = ask for weight with no explicit
prescription (same source).

**Hevy** does not use `AxB` text at all. Weight and reps go in separate
columns (`KG`/`LBS` and `REPS`); tapping the REPS header switches between a
single number and a rep range. RPE is a live-session-only column, off by
default
([Hevy: how to write sets and reps](https://www.hevyapp.com/features/how-to-write-sets-and-reps/)).

**Strong** pre-fills the previous session's values so a change is one edit
([Strong app store listing](https://apps.apple.com/us/app/strong-workout-tracker-gym-log/id464254577);
the pre-fill claim is also repeated in third-party comparisons
[e.g. setgraph](https://setgraph.app/articles/best-strong-app-alternatives-(2025)) —
first-party wording is thin, treat the exact mechanism as UNVERIFIED).

**Hevy** likewise auto-carries: "when you add an exercise you've done before,
the number of sets, the weight, and the reps you've done before are
automatically added, but you're free to adjust them"
([Hevy](https://www.hevyapp.com/features/how-to-write-sets-and-reps/)).

**Boostcamp** shows target sets/reps plus the last logged weight, starts the
rest timer on tap-to-log, and auto-adjusts the working weight up on success or
down on missed reps
([Boostcamp workout tracker](https://www.boostcamp.app/workout-tracker)).

**Notation convention in the wider sport.** Sets-first is the dominant
convention: 3x5 is three sets of five
([exercisemenu](https://exercisemenu.com/what-does-3x10-4x12-or-5x5-mean-workout/)).
The load-bearing rule for a parser is Testify's: **"reps are always second"**,
which holds in both `sets x reps` (`3 x 5`) and `weight x reps x sets`
(`165 x 5 x 3`)
([Testify Strength & Conditioning](https://testifysc.com/articles/lifting-notation-reps-are-always-second-20251230)).
The Starting Strength forum records the competing `5x3` reps-first habit and
the confusion it causes
([Starting Strength forum](https://startingstrength.com/resources/forum/general-q-and-a/76657-annotation-5x3-repsxsets-3x5.html)).
Programs occasionally flip to reps-first, so context matters
([exercisemenu](https://exercisemenu.com/what-does-3x10-4x12-or-5x5-mean-workout/)).

### 2.2 The core decision: two grammars

The ambiguity of `3x5` is not resolvable by cleverness, but it *is* resolvable
by context, because the two contexts have different shapes:

- **Routine file** is a *prescription*. Weight is often absent or relative
  (`80%`, `@8`). A bare `AxB` there is sets x reps.
- **Chat log** is a *report*. Weight is almost always present and is almost
  always the biggest number. A bare `135x5` there is 135 lb for 5 reps.

So: **routine file = sets-first (Liftosaur rules). Chat = weight-first
(Starting Strength rules).** The user never sees the seam because they only
type in one of the two at a time.

### 2.3 Grammar spec

```
log_line   := exercise? entry (";" entry)*
entry      := setspec | shorthand | command
setspec    := weight? reps_expr rpe?
weight     := NUM unit? | "bw" | "bw" ("+"|"-") NUM unit?
unit       := "kg" | "lb" | "#"
reps_expr  := NUM                       # one set
            | NUM "x" NUM               # see rule A
            | NUM "x" NUM "x" NUM       # weight x reps x sets
            | NUM ("/" NUM)+            # per-set reps, one number per set
            | NUM "+"                   # AMRAP result
rpe        := "@" NUM ("+"|"-")?        # RPE, optionally with a modifier
shorthand  := "same" | "done" | "as planned" | "+"NUM | "-"NUM | "x"NUM
command    := "skip" | "swap" TEXT | "undo" | "fix" TEXT | "note" TEXT
            | "done for today" | "next" | "what's next"
```

### 2.4 Ambiguity rules

**Rule A — two numbers joined by `x`, weight absent.**
Decide by magnitude of the first number, using the unit system in use:

- First number >= 25 (lb) or >= 12 (kg), OR carries a unit suffix
  -> **weight x reps**. `135x5` = 135 lb for 5 reps.
- First number <= 10 and second number <= 30 -> **sets x reps**.
  `3x5` = 3 sets of 5.
- Anything in between (11-24 lb) -> **ask, once, with a one-tap answer**:
  "20x8 — 20 lb for 8, or 20 sets of 8?" Then remember the choice for that
  exercise. Dumbbell lateral raises live in this band, so this will fire.

This is the "context clues" rule Testify states informally: nobody squats 4 lb
for 145 sets
([source](https://testifysc.com/articles/lifting-notation-reps-are-always-second-20251230)).

**Rule B — three numbers.** Always `weight x reps x sets`. Reps second, per
Testify. `225x5x3` = 225 lb, 5 reps, 3 sets.

**Rule C — slashes are per-set reps, in order.** `135 5/5/4` is three sets at
135 with 5, 5, then 4 reps. Slash count sets the set count and overrides the
prescribed count. No app I found uses this in text; it is the way lifters write
it in notebooks and forum posts. UNVERIFIED as an app convention; adopted
because it is the only compact way to express a failed last set.

**Rule D — a lone number in a set slot is reps.** If the agent just asked for
set 2 of bench at 135, `4` means 4 reps at 135. This is the single highest-value
rule for typing speed.

**Rule E — `@` always introduces RPE.** Liftosaur precedent
([source](https://github.com/astashov/liftosaur/blob/master/docs/content/liftoscript.md)).
`@8` on a 1-10 scale. Never parse `@` as a weight or a mention.

**Rule F — `bw` is bodyweight; `bw+25` is bodyweight plus 25.** `-25` for
assisted. The stored value is the added load plus a bodyweight snapshot, so
the number stays meaningful when bodyweight changes. Storage detail belongs to
the data-model slice.

**Rule G — `+5` / `-10` are deltas from the prescribed or last weight**, not
absolute. `x8` (leading `x`) is a reps override at the same weight. This
mirrors Strong's and Hevy's pre-fill-then-edit interaction in a text channel
([Hevy](https://www.hevyapp.com/features/how-to-write-sets-and-reps/)).

**Rule H — bare `+` after reps is AMRAP-completed**, per Liftosaur
([source](https://github.com/astashov/liftosaur/blob/master/docs/content/liftoscript.md)).
`12+` in a log means "the AMRAP set got 12".

**Rule I — units.** Default to the user's configured unit. A unit suffix wins.
`#` means lb (US gym convention). UNVERIFIED, no first-party citation; it is
common in powerlifting forums.

**Rule J — exercise names are fuzzy-matched against today's day first**, then
the whole exercise library. "ohp", "press", "overhead" all resolve to the one
overhead-press line in today's day without a disambiguation prompt. Only prompt
if two exercises in *today's day* match.

### 2.5 Worked examples

Context for each: today's day prescribes `Bench Press / 3x5 / 135lb`, and the
agent has just asked for set 2.

| # | User types | Parsed as | Rule |
|---|---|---|---|
| 1 | `5` | Bench, set 2, 135 lb x 5 | D |
| 2 | `135x5` | Bench, set 2, 135 lb x 5 | A (135 >= 25) |
| 3 | `4` | Bench, set 2, 135 lb x 4 (missed) | D |
| 4 | `same` | Copy set 1 exactly | G / carry-forward |
| 5 | `+5` | Bench, set 2, 140 lb x 5 (reps from prescription) | G |
| 6 | `x8` | Bench, set 2, 135 lb x 8 | G |
| 7 | `135 5/5/4` | Bench, all 3 sets: 135x5, 135x5, 135x4 — closes exercise | C |
| 8 | `225x5x3` | Bench replaced: 3 sets of 5 at 225 | B |
| 9 | `3x5` | 3 sets of 5 at prescribed weight (135) | A (3 <= 10) |
| 10 | `135x5 @8` | 135 lb x 5 at RPE 8 | A + E |
| 11 | `bw+25 x8` | Bodyweight plus 25 lb, 8 reps | F |
| 12 | `bw x12` | Bodyweight, 12 reps | F |
| 13 | `12+` | AMRAP set completed at 12 reps | H |
| 14 | `20x8` | **Ambiguous** — agent asks once, remembers | A (grey band) |
| 15 | `ohp 95 8/8/6` | Overhead Press: 95x8, 95x8, 95x6 | C + J |
| 16 | `done` | Current exercise completed exactly as prescribed | carry-forward |
| 17 | `as planned` | Whole remaining day completed as prescribed | carry-forward |
| 18 | `skip` | Current exercise marked skipped, move on | command |
| 19 | `swap incline db press` | Substitute exercise, keep set scheme | command |
| 20 | `undo` | Remove the last logged entry | command |
| 21 | `fix set 3 was 4 reps` | Amend an already-logged set | command |
| 22 | `60kg 3x8` | 60 kg, 3 sets of 8 — weight leads, then sets x reps | A + B-ish |
| 23 | `note left shoulder tweaky` | Free-text note on the current exercise | command |
| 24 | `done for today` | Close the session, advance the cursor | command |

Example 22 is the one genuine collision: `60kg 3x8` has an explicit weight, so
the `3x8` that follows falls back to prescription semantics (sets x reps). The
rule is: **once a weight has been consumed, a following `AxB` is sets x reps.**
Without that carve-out the parser would read `3x8` as 3 lb for 8 reps.

### 2.6 What the agent must never do

- Never ask "did you mean sets or reps" more than once per exercise. Store the
  resolution.
- Never reject a line. If parsing fails, log the raw text verbatim as a note
  on the current exercise and say so in five words. A lost set is worse than a
  messy one. This follows directly from the ADHD finding that decision friction
  and the demand for an "authentic" answer is what kills tracking
  ([Chasing Shadows, arXiv](https://arxiv.org/html/2603.22609)).

---

## 3. Carry-forward defaults

The whole point is that the common case is zero typing.

**What carries.** For each exercise, prefill from, in order:

1. The progression rule's output for this session (Liftosaur's `lp`/`dp`/`sum`
   compute the next prescription automatically —
   [source](https://github.com/astashov/liftosaur/blob/master/docs/content/liftoscript.md);
   Boostcamp does the same, bumping on success and dropping on missed reps —
   [source](https://www.boostcamp.app/workout-tracker)).
2. Last session's actual weight and reps for that exercise (Hevy and Strong
   both do this —
   [Hevy](https://www.hevyapp.com/features/how-to-write-sets-and-reps/)).
3. The routine's static prescription.

**One-word confirms.**

| Word | Means |
|---|---|
| `done` | This exercise, exactly as prescribed |
| `same` | This set, same as the previous set |
| `as planned` | Everything remaining today, as prescribed |
| `y` / `yes` / `✓` | Whatever the agent just proposed |

**Partial completion.** A session with some exercises logged and some not is a
first-class state, not an error. On close, unlogged exercises are recorded as
`not done`, no commentary. On resume, the agent picks up at the first unlogged
slot.

**Editing a mistake.** `fix <what>` in natural language, resolved against the
current session only. The agent restates the corrected row in one line. Edits
are appended as corrections, not in-place rewrites, so the history stays
auditable (this matters for the git-storage design, section 7).

**Undo.** `undo` removes the last entry. Repeatable. Always available, never
confirmed. Undo is the thing that makes fast entry psychologically safe: if a
wrong guess is one word to reverse, the agent can guess aggressively.

---

## 4. The "what do I have today" answer

### 4.1 Shape

Three lines, then stop:

```
Day B (Lower) - 5 exercises, ~40 min.
Squat 3x5 @ 185. Last time: 180x5,5,5.
Warm-up: bar x5, 95x5, 135x3, 165x2.
```

Then wait. Do not list exercises 2-5 unless asked. The whole day is available
on `list it` / `what's the whole day`.

**Rationale.** The ADHD self-tracking work reports users getting "stuck on a
question for one hour" and finding extremely simple tracking (a single X mark)
outperforming complex frameworks
([Chasing Shadows, arXiv](https://arxiv.org/html/2603.22609)). Ten lines of
plan is ten decisions.

### 4.2 Contents, ranked by value

1. **Which day.** One token.
2. **First exercise target.** Weight x reps from the progression rule.
3. **Last performance for that exercise.** The number the user actually wants,
   and the thing every app puts in the "previous" column
   ([Hevy](https://www.hevyapp.com/features/how-to-write-sets-and-reps/),
   [Boostcamp](https://www.boostcamp.app/workout-tracker)).
4. **Warm-up ladder with plate math.** Liftosaur auto-generates warm-ups and
   lets them be overridden per exercise; percentages in a `warmup:` section are
   of the *first working set's weight*, not 1RM
   ([source](https://github.com/astashov/liftosaur/blob/master/docs/content/liftoscript.md)).
   In chat, print the bar loading too: `165 = bar + 45,15` beats `165` because
   it removes an arithmetic step at the rack.
5. **Estimated duration.** One number, no range.
6. **PR hint — only when close.** "PR is 190x5, today is 185x5" is motivating.
   A PR table is noise. Gate it: mention only if today's top set is within one
   increment of a rep-max PR. Streaks: see section 6.

### 4.3 What to leave out

Volume totals, muscle-group balance, weekly set counts, "you're 3 sessions
into week 2". All of it is available on request and none of it belongs in the
opening message.

---

## 5. As-you-go flow

### 5.1 Turn shape

Agent turns are: **confirm what was logged (<=1 line) + state the next target
(<=1 line)**. Never more, unless the user asks.

**Batching is the user's choice, not the agent's.** The grammar in section 2
accepts a single set (`5`), a whole exercise (`135 5/5/4`), or a whole day
(`as planned`) in the same slot. The agent always *offers* per-set granularity
by asking for the next set, and always *accepts* larger chunks silently.

### 5.2 Rest timer

A chat agent cannot fire a timer reliably. Every tracker surveyed treats the
rest timer as core: Boostcamp starts it automatically on tap-to-log
([source](https://www.boostcamp.app/workout-tracker)); Liftosaur has per-set
rest specs, superset defaults, and an `auto` keyword that advances the workout
when rest ends
([source](https://github.com/astashov/liftosaur/blob/master/docs/content/liftoscript.md));
Fitbod has a dedicated rest-timer feature
([Fitbod help centre](https://fitbod.zendesk.com/hc/en-us/articles/360006340194-Rest-Timer)).

Options, in preference order:

1. **State the rest target in the confirm line** and let the user's phone
   timer or clock do the work: "Logged 135x5. Rest 3 min, then set 2 at 135."
   Zero infrastructure.
2. **Timestamp-derived feedback.** The agent knows when the last set was
   logged. When the next message arrives it can say "that was 2:10 rest" if
   asked, or flag unusually short rests. Passive, no push needed.
3. **Push notification** if the deployment ever has one. Out of scope here.

Do not fake it. An agent that says "starting your timer" and cannot ring is
worse than one that says nothing.

### 5.3 Interruptions and resume

A gym session is interrupted constantly. Design assumptions:

- **The session has no timeout that discards data.** Ever.
- **Resuming is stateless from the user's side.** "where was I" returns
  exactly: exercise, set index, target. One line.
- **Long gaps are noted, not punished.** If the last set was 3 hours ago,
  ask once: "Last set was 3 h ago. Same session, or new one?" Default to same
  session if the user just answers with a set.
- **Auto-close.** A session with no activity by end of day is closed
  automatically at the next interaction, with whatever was logged. The user is
  told in one clause, not asked.

### 5.4 Voice input

Phone voice dictation is likely for a gym setting (hands chalked, phone on the
floor). Consequences for the grammar:

- **Homophone hazard.** "one thirty five by five" dictates variously as
  `135 by 5`, `135 x 5`, `135 by five`. The parser must accept `by`, `x`, `X`,
  `*`, and the spelled words `one`..`twenty` as digits.
- **`@` will not survive dictation.** Accept "at eight RPE", "RPE eight",
  "at 8" as RPE.
- **No punctuation.** `bench one thirty five five five four` must parse.
  Heuristic: first number is weight if >= 25, remaining numbers are per-set
  reps.
- **Prefer short confirmations** because the user may be listening rather than
  reading, and a screen-reader pass over a table is intolerable mid-set.

UNVERIFIED: no first-party source found for how any tracker handles voice set
entry; these are design inferences.

### 5.5 Sample transcript, as-you-go

```
User:  what do i have today

Agent: Day B (Lower) - 5 exercises, ~40 min.
       Squat 3x5 @ 185 (up 5 from last). Last time: 180 x5,5,5.
       Warm-up: bar x5, 95x5, 135x3, 165x2.

User:  185x5

Agent: Squat set 1 logged, 185x5. Set 2 at 185.

User:  5

Agent: Set 2, 185x5. Last set.

User:  4 @9

Agent: Set 3, 185x4 @9. Squat done: 5/5/4.
       LP holds the weight next time. Next: Romanian Deadlift 3x8 @ 155.

User:  same as last week

Agent: RDL 3x8 @ 150, same as 2026-08-24. Next: Leg Press 3x12 @ 270.

       [2 hours later]

User:  where was i

Agent: Day B, 2 of 5 done. Next: Leg Press 3x12 @ 270.
       Last set was 2h ago - same session, or start fresh?

User:  same. 270 12/12/10

Agent: Leg Press logged 12/12/10. Next: Leg Curl 3x12 @ 90.

User:  only have 10 min

Agent: 10 min: Leg Curl 2x12 @ 90. Cutting calf raises.

User:  done

Agent: Leg Curl 2x12 @ 90 logged.

User:  done for today

Agent: Day B closed. 4 of 5, 52 min. Next up: Day A (Upper).
```

Turn count for a full session: 8 user messages, most of them 1-4 characters
of real content.

### 5.6 Sample transcript, after-the-fact whole routine

```
User:  did day A as planned except bench 3rd set was 4 reps

Agent: Logged Day A, today:
         Bench Press  135 x5, x5, x4
         OHP          95 x8, x8, x8
         Incline DB   50 x10 x3
         Lat Raise    20 x15 x3
         Pushdown     70 x12 x3
       Bench missed 5 on set 3, so LP holds 135 next time.
       Next up: Day B (Lower).

User:  actually i skipped the pushdowns

Agent: Pushdowns removed. Day A: 4 of 5.
```

Three things to note in that exchange:

1. The whole day is echoed back once, as a table, precisely because the user
   is *not* mid-set and can read it. The one-line rule is a mid-session rule.
2. The exception is applied to the named set without asking which set.
3. The correction is accepted with no friction and no confirmation prompt.

---

## 6. ADHD-specific friction reducers

Evidence, then what it implies here.

**Defaults and pre-filling.** The EAST framework's first principle is "make it
Easy", explicitly including harnessing defaults and reducing the "hassle
factor" of an action
([Behavioural Insights Team, EAST](https://www.bi.team/publications/east-four-simple-ways-to-apply-behavioural-insights/)).
Implication: every prompt has a correct default the user can accept with one
word (section 3).

**Minimal choices, and the cost of open questions.** The neurodivergent
self-tracking study reports participants "stuck on a question for one hour",
anxiety about giving an "authentic" answer to vague questions, and a finding
that extremely simple tracking (one participant used a single "X") outperformed
richer frameworks
([Chasing Shadows, arXiv](https://arxiv.org/html/2603.22609)).
Implication: never ask an open question mid-session. `skip` and `done` must
always be one word. RPE stays optional and unasked, matching Hevy, where RPE
is off by default and live-session only
([source](https://www.hevyapp.com/features/how-to-write-sets-and-reps/)).

**Flexible, low-commitment engagement.** The same study found short, optional
tracking periods reduced barriers versus demands for sustained commitment
([source](https://arxiv.org/html/2603.22609)).
Implication: sequence-based rotation (section 1.4). A missed week must cost
nothing and produce no repair work.

**Implementation intentions.** Gollwitzer and Sheeran's meta-analysis reports
d = 0.65 across 94 tests and 8,000+ participants for if-then plans on goal
attainment; a 642-test database finds .27 <= d <= .66, with larger effects for
contingent if-then format and for motivated participants
([Gollwitzer, goal intent PDF](https://cancercontrol.cancer.gov/sites/default/files/2020-06/goal_intent_attain.pdf);
[642-test meta-analysis](https://www.researchgate.net/publication/378870694_The_When_and_How_of_Planning_Meta-Analysis_of_the_Scope_and_Components_of_Implementation_Intentions_in_642_Tests)).
Implication: at session close, offer one optional if-then line — "next Lower
day, when you get to the gym, squat 190x5" — rather than a reminder at a fixed
time. Offer, do not impose.

**Immediate feedback.** Boostcamp's design gives the progression result at the
moment the set is logged
([source](https://www.boostcamp.app/workout-tracker)). Implication: the confirm
line carries the consequence ("LP holds 135 next time"), not just an
acknowledgement.

**Streaks — use with caution.** The CHI'16 work on habit-formation apps
frames dependency on the app as a risk in itself
([Don't Kick the Habit, CHI'16 LBW](https://discovery.ucl.ac.uk/1477627/1/Chi%202016%20LBW%202.1%20camera%20ready.pdf)),
and the mixed-outcome self-tracking experiment shows the visual presentation of
goal outcomes changes how users respond to partial success
([JMIR / PMC5917081](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5917081/)).
Implication: **no streak counter by default.** A streak converts a missed
session from a neutral event into a loss, which is the exact failure mode
sequence-based rotation was chosen to avoid. If any progress display is wanted,
prefer a cumulative, non-breakable count ("31 sessions this year") over a
consecutive one.

**Visible progress.** Show it on the lift, not on the habit: "185x5, up from
180 three weeks ago". That is intrinsic to the activity and cannot be broken
by a missed week.

---

## 7. State between messages

The agent is stateless between turns. Session state must live in the store and
be cheap to reconstruct.

### 7.1 Principle: derive the cursor, do not store it

Two sources of truth is one too many. **The rotation cursor should be derived
from the logs** — "the day after the most recently closed session's day" —
rather than stored in a counter that can drift out of sync with the log after
a manual edit, a merge, or a retry. Store only what cannot be derived:
which session is currently open, and any per-session overrides (trim decisions,
swapped exercises, the resolved answer to an ambiguous `20x8`).

### 7.2 Git-repo storage

Layout:

```
programs/upper-lower.md        # the routine file, section 1.2
logs/2026/2026-08-31-B.md      # one file per session, append-only
state/open-session.json        # exists only while a session is open
```

Session file, append-only, one row per event:

```markdown
# 2026-08-31 Day B (Lower)
started: 2026-08-31T18:04:12Z
program: upper-lower @ 9f2c1ab

| ts | exercise | set | weight | reps | rpe | msg |
|----|----------|-----|--------|------|-----|-----|
| 18:06:02 | Squat | 1 | 185 | 5 | | m_7f3a |
| 18:09:41 | Squat | 2 | 185 | 5 | | m_9c11 |
| 18:13:55 | Squat | 3 | 185 | 4 | 9 | m_2e08 |
```

- **`open-session.json`** holds the path of the open file, the cursor
  (exercise index, set index), and per-session overrides. It is deleted on
  close. Its existence *is* the "session open" flag, so there is no boolean to
  get wrong.
- **Commit granularity.** One commit per closed session, not per set. Per-set
  commits produce hundreds of commits and turn `git log` into noise. During an
  open session the file is dirty in the working tree; that is fine and is
  itself a recovery signal.
- **Corrections append.** A `fix` writes a new row with the same
  `(exercise, set)` key and a later timestamp. The reader takes last-write-wins
  per key. Nothing is ever edited in place, so the log stays a faithful record
  of what was said when — which is what makes `undo` safe.
- **Concurrency.** Single user, single device in practice. If two devices ever
  write, the append-only row format means git's merge produces a file with both
  rows and last-write-wins resolves it. UNVERIFIED that markdown table merges
  cleanly in all cases; a JSONL log file would merge more reliably at the cost
  of readability.

### 7.3 Notion storage

Notion has no append-only primitive and no commit, so idempotency has to be
explicit.

- **Sessions database.** One page per session. Properties: Date, Day, Program,
  Status (`open`/`closed`), Cursor (text, e.g. `Squat:3`), Overrides (text).
- **Sets database.** One row per set, related to the session page. Properties:
  Exercise (relation), Set index, Weight, Reps, RPE, Timestamp, and a
  **`client_key`** text property.
- **`client_key`** is `sha1(session_id + exercise + set_index + attempt)`, or
  for corrections, includes the message id. Before creating a row, query the
  Sets database filtered on `client_key`. If a row exists, update it instead of
  creating. This is the whole idempotency story.
- **Cursor** lives on the session page rather than being derived, because
  querying "most recent closed session" on every turn is a round trip Notion
  charges for in latency. Accept the duplication here; re-derive and repair on
  session open.

### 7.4 Idempotency when a message is re-sent

Same rule in both stores: **every incoming user message gets a stable id**
(hash of content + conversation position, or the platform's own message id),
and every write records the id that produced it.

- Before writing, check whether that message id already appears in the session.
  If it does, do not write; re-send the same confirmation reply.
- This makes a re-sent "5" a no-op rather than a duplicate set, which is the
  realistic failure mode when a phone loses signal mid-gym and retries.
- It also makes the agent's confirmations replayable, so a user who scrolls
  back and re-sends by accident sees the same answer, not a corrupted log.

---

## 8. Open questions for the user

These need a human answer; I could not settle them from sources.

1. **Units.** lb or kg? It changes the magnitude thresholds in Rule A
   (section 2.4) and the plate maths in the warm-up ladder.
2. **Does a partial session advance the rotation?** Proposed: advance on
   explicit close, not on first set. Confirm, because it decides whether
   abandoning after two sets means you get the same day tomorrow.
3. **Rest days in the cycle: yes or no?** Proposed no (section 1.3). Do you
   want the agent to be able to say "today is a rest day", or should it always
   answer "next up is X, whenever"?
4. **RPE: on, off, or on-request?** Proposed off by default, accepted if typed.
   Hevy keeps it off by default. Do you want it prompted for top sets?
5. **Streaks.** Proposed: none. Confirm this matches what you want, given the
   earlier note about them backfiring.
6. **Which store — git or Notion?** Section 7 covers both, but they imply
   different cursor strategies, and picking one removes a chunk of design.
7. **Voice input: real or hypothetical?** If real, the grammar needs the
   spelled-number and `by`/`at` handling in 5.4 to be first-class rather than a
   fallback. If not, that work can be dropped.
8. **Should the agent volunteer PR hints, or only on request?** Proposed:
   volunteer only when within one increment.
9. **The `20x8` grey band** (section 2.4, Rule A) will fire on dumbbell work.
   Is a one-time per-exercise question acceptable, or should the agent always
   guess (weight, given a weight-first log grammar) and rely on `undo`?

---

## Sources

- [Liftosaur, liftoscript.md (source of truth for Liftoscript syntax)](https://github.com/astashov/liftosaur/blob/master/docs/content/liftoscript.md)
- [Liftosaur documentation site](https://www.liftosaur.com/doc/liftoscript)
- [wger routine API documentation](https://wger.readthedocs.io/en/latest/api/routines.html)
- [wger Day model source](https://github.com/wger-project/wger/blob/master/wger/manager/models/day.py)
- [Hevy: How to Write Sets and Reps](https://www.hevyapp.com/features/how-to-write-sets-and-reps/)
- [Strong app, App Store listing](https://apps.apple.com/us/app/strong-workout-tracker-gym-log/id464254577)
- [Boostcamp workout tracker](https://www.boostcamp.app/workout-tracker)
- [Fitbod: How Fitbod Creates Your Workout](https://help.fitbod.me/hc/en-us/articles/360004429814-How-Fitbod-Creates-Your-Workout)
- [Fitbod: Rest Timer](https://fitbod.zendesk.com/hc/en-us/articles/360006340194-Rest-Timer)
- [Testify Strength & Conditioning: reps are always second](https://testifysc.com/articles/lifting-notation-reps-are-always-second-20251230)
- [Starting Strength forum: 5x3 vs 3x5 annotation](https://startingstrength.com/resources/forum/general-q-and-a/76657-annotation-5x3-repsxsets-3x5.html)
- [exercisemenu: What does 3x10, 4x12, or 5x5 mean](https://exercisemenu.com/what-does-3x10-4x12-or-5x5-mean-workout/)
- ["Chasing Shadows": self-tracking for neurodivergent individuals, arXiv](https://arxiv.org/html/2603.22609)
- [Behavioural Insights Team, EAST framework](https://www.bi.team/publications/east-four-simple-ways-to-apply-behavioural-insights/)
- [Gollwitzer, Implementation Intentions (NCI PDF)](https://cancercontrol.cancer.gov/sites/default/files/2020-06/goal_intent_attain.pdf)
- [The When and How of Planning: meta-analysis, 642 tests](https://www.researchgate.net/publication/378870694_The_When_and_How_of_Planning_Meta-Analysis_of_the_Scope_and_Components_of_Implementation_Intentions_in_642_Tests)
- [Don't Kick the Habit: dependency in habit formation apps, CHI'16 LBW](https://discovery.ucl.ac.uk/1477627/1/Chi%202016%20LBW%202.1%20camera%20ready.pdf)
- [How Mobile App Design Impacts User Responses to Mixed Self-Tracking Outcomes (PMC5917081)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5917081/)
- [Boostcamp third-party review (skip-day behaviour, secondary source)](https://healthynexercise.com/best-free-fitness-apps/boostcamp/)
- [setgraph: Strong alternatives (pre-fill claim, secondary source)](https://setgraph.app/articles/best-strong-app-alternatives-(2025))

Not reached inside the timebox, listed as gaps: FitNotes first-party docs,
Juggernaut AI, Alpha Progression, Hevy rest-timer specifics.
