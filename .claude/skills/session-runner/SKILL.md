---
name: session-runner
description: Runs a training session turn by turn - opens it, logs each set, answers "what am I doing today", advances the cursor, closes it. Use on any logged set, "next", "done", or a question about today's session.
---

# session-runner

Conversation belongs here; arithmetic and row shaping belong to
`scripts/log_set.py`, which is pure and fixture-replayable. This skill calls it,
then applies the returned writes through `row-create` / `config-write`.

## Grammar

Never parse a set line yourself. Call `log_set(line, state)` (in process or
`python3 scripts/log_set.py` with `{"line", "state"}` on stdin) and say back
its `confirm_line` verbatim. It never returns a question and never raises on
bad input; the fallback ladder (`ladder.py`, `catalog.py`) always finds an
exercise or creates one, and the grammar (`grammar.py`, `tokens.py`) always
returns a row or falls through to a note.

**What a user can type**, one example per shape:

- A bare number after you've asked for a set: `5` is reps at the last
  weight (rule D). `same` repeats the last set exactly.
- `weight x reps`: `135x5`. Once a weight has been typed, a following
  `AxB` is sets x reps: `60kg 3x8` is 3 sets of 8 at 60 kg.
- `weight x reps x sets`: `225x5x3` (225 lb, 5 reps, 3 sets).
- `weight reps/reps/reps`: `135 5/5/4`, one number per set, overrides the
  prescribed set count.
- `+5` / `-10`: a delta from the last weight. `x8`: a reps override at the
  last weight. `12+`: an AMRAP result of 12. `@8`: always RPE, never a
  weight or a mention.
- `bw`, `bw+25`, `bw-10`: bodyweight, plus an added load or minus an
  assisted one.
- Time: `20s`, `2min`. Distance: `60m`, `1.5km`. Side: `5l/6r`,
  `10 per side`. Level: `step 3 x8`. Interval: `emom 10x10 @24kg`. Spoken
  numbers collapse first: `one thirty five` becomes `135`.
- A leading name picks the exercise: `ohp 95 8/8/6`, `zercher squat 135x5`.
  Names are matched by whole word, never by similarity score. The athlete's
  own `Exercises` rows go first, so `row` is whichever row THEY train, and
  only then the shipped alias table and the shipped catalog. A word that
  several exercises could mean refuses rather than picking one: `press`
  against a catalog holding a bench press and a military press falls through
  to the alias table to be settled there.

**Grey band, no dialogue.** `20x8` with no prior weight for that exercise
and no program target reads as weight x reps, never a question (rule G2).
The confirm line states the reading and says `fix` reverses it; a bare
`fix` right after flips that one reading.

**When no table knows the name.** A line that still parses as a set adds one
`Exercises` row and says so in the confirm line ("Added bnch press to your
catalog."), so a typo is visible in the same breath rather than silently
attributed to a lift the athlete never did. A line that parses as nothing
becomes a verbatim `Notes` row on the open session, never rejected, never
re-asked.

**While the session is halted (rule S2, rule L12).** `log_set` checks this
itself, at its own exit, and does not rely on `trainer-core` having run
first: if a turn would write a `Sets` row while
`state["session_status"] == "halted"`, it drops every write that turn made
and returns `trainer-core`'s refusal instead, naming `Status: halted`. The
cursor does not move either. Say that line back verbatim and do not offer to
log the set anyway. Only `pain-triage` lifts a halt (rule L12), so route the
user's acknowledgement there, never back through this skill.

## Core loop (build-plan s4, s9 phase 4)

**The opener.** "what am i doing today" answers from the program cursor,
one turn, no writes: `state["program"]` is program-design's template,
threaded in unchanged (never invent one); `state["program_cursor"]`
(`{"node", "cycle"}`) indexes its `rotation`, lazily starting at `{0, 0}`
and resetting if the active template's name changes. `program.py`'s
`try_today` reads `rotation[cursor.node]`, names the day and its lead
block or two, and primes `scope` to the lead block's exercise so the very
next bare `185x5` needs no name (matching the spec's own worked example).
A rest node (`blocks: []`) states the label and how to move on instead.

**Readiness (rule L2).** The first turn of a new session gets `Readiness
1-5? (skip if you like)` appended once. Answering with a bare `1`-`5`
right after writes `Sessions.Readiness`; anything else, including the
first real set, just proceeds normally. Never asked twice in one session,
never blocks a log.

**Rest nodes (rule L17).** `done`, `rest`, `skip`, or `as planned` at a
rest node writes no set and advances `program_cursor`
((`node + 1) % len(rotation)`, `cycle` increments on wrap). The same words
at a work node stay the old generic ack and do not touch the cursor.

**Cursor advance.** A finished work day advances the same way at `done for
today` (`program_cursor` is one-advance-per-session-guarded, so a rest ack
and a same-session close never both fire).

**`swap <exercise>`.** Session-only: resolves the named exercise through
the normal catalog lookup and re-scopes, so the sets logged next name the
swap. Never rewrites `program` or `program/current` — that is
`program-design`'s swap-in-place (a different, permanent edit).

## Turn 1, from cold

The heaviest hydration of the seven, and what a day-2 "what am i doing today"
runs on. Four reads, in order:

1. `row_query("Exercises")` rebuilds `state["catalog"]`, `page_id` and
   `measure` per name. An empty result needs no special case: the fallback
   ladder creates a catalog row the first time it meets a name.
2. `row_query("Sessions")` gives `session_seq`, and the frozen `tz` from the
   last row's `Timezone` (rules L3, L4). Nothing else stores that zone.
3. `row_query("Sessions", {"Status": "open"})` gives `session_id` and
   `session_status`.
4. Only if a session is open, `row_query("Sets", {"Session": <id>})` rebuilds
   `state["cursor"]` as the highest `Set index` per exercise, so numbering
   continues instead of restarting at 1 (rule L7).

`state["program"]` and `state["program_cursor"]` come from
`config_read("program/current")`: `body` is the active template verbatim,
parsed by `program-design`'s `program_page.read_page`. The cursor is derived
from it, not stored: count the `Status: closed` sessions whose `Start time`
is at or after the page's `started_at` (`Start time` is frozen at open, so
it is what says which program a session ran under), then call
`program.cursor_after(program, that_count)`. Counting every closed session in
the workspace instead is what made a second program open on the first one's
day. Never hand-build the cursor dict: `cursor_after` is the only
constructor, the cursor names the program it belongs to, and anything else
raises rather than being silently discarded.

`carry`, `scope` and `targets` genuinely do not survive a chat boundary and
start empty, so the first bare `185x5` of a cold chat takes
its scope from the program cursor's lead block, not from carry-forward.
