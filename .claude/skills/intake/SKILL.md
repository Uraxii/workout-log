---
name: intake
description: First run, "set me up", or a life change. Creates the two Notion log databases from schema/notion-schema.json, then asks every profile question in order with no silent defaults. Use on "set me up", a fresh workspace, or when the athlete's situation has changed enough to redo the profile.
---

# intake

Conversation belongs here; the question table, its cursor and the parse of
each answer belong to `scripts/questions.py`, and every write belongs to
`scripts/intake.py`, which is pure and fixture-replayable
(`intake_turn(line, state) -> {"writes", "say", "state"}`, docs/architecture.md
"The script seam"). This skill calls it once per user turn, says exactly
`say`, and applies `writes` through `row-create` / `config-write` /
`database-create`.

## Database creation, first "set me up" (build-plan s5.1)

There is no template page. `intake.py` returns **one** `database-create` write
per turn until both `schema/notion-schema.json` databases exist. Apply the
write, then put the returned data source id in `state["databases"][<name>]`
before the next turn; the seam is a pure function of `(line, state)` and never
sees a response.

The two are `Sets` and `Sessions`, created in schema declaration order. That
is the whole list, because Notion holds logs only: the exercise catalog is
package data the agent reads, the gym's plates are `config/preferences`, and
per-exercise progression state is a key on `program/current`. No column is a
relation, so no create has to wait on another's id. Each call is
query-before-create (rule L8): a database of that name under the user's page
is adopted, not duplicated, so a second "set me up" is harmless and appends
nothing.

**The payload is rendered from the schema by `scripts/ddl.py`, never
hand-built.** The tool takes a SQL DDL `CREATE TABLE` statement, and a payload
an LLM assembles from prose drifts from the schema. See
`references/db-create.md`.

The parent page id is the user's, read from `state["notion_parent_page_id"]`.
It gets there by being asked for: it is the second question in the table,
right after `storage_platform` (ticket workout-log-mqs), because nothing
else can supply it and every create needs it. Until it is answered there is
nothing to create under, so the creates wait and the questions still run.

Each create answers with a data source id, and the caller threads it back
into `state["databases"]`. `intake.py` also writes that map to
`config/athlete.notion_data_sources`, JSON encoded: no read verb answers
"which databases exist", so that key is the only way a later chat learns it
(`tools/mock-notion/hydrate.py` reads it back).

## Nothing is seeded

There is no catalog to seed. `exercises/defaults.json` is 92 exercises the
agent reads out of the package when it builds a program, and it is never
copied into the athlete's workspace. Setup writes two `database-create` calls
and her answers, and nothing else.

## The question flow

`references/questions.md` has the ordered list. Three questions about the
tool come first, because nothing works without them: the storage platform
(`storage_platform`, docs/storage-section-design.md question 1), the Notion
parent page id (ticket workout-log-mqs), and the timezone, which is frozen
onto session 1 (rule L3) and read by every later day-boundary check (ticket
workout-log-ayf.16). A pasted page link and a bare id both answer the
parent page id; the id is stored dashed 8-4-4-4-12. Naming a store this
build has no DDL for does not fail to parse; it is recorded, then refused
in place of the next prompt, with the cursor held on `storage_platform` so
she can correct herself (`storage.refusal`, pinned byte for byte by
`fixtures/13-storage-refusal`). Then safety (PAR-Q+, seven questions plus a
conditional follow-up, delegated in-process to `screen`), then goal,
history, constraints, body, recovery, preferences (build-plan s5.2). Every
question after those first three is about her. **One question per turn**, since this is a phone conversation
(`principle-experience-first`), and **no silent defaults**: every item on
the list gets asked, including age, with no gate (dec "T18 final").

An answer that does not parse re-asks its own step instead of advancing the
cursor (ticket workout-log-481). That is one rule over the whole table, in
`questions.parse` returning `None`, not a retry branch on any one question:
"maybe" to a PAR-Q+ item is not silently a NO, and free text where the
follow-up needs a yes or no can no longer strand `config/limits.clearance`
at `pending`. Say the `reask` line back and ask again; never guess.

`intake_cursor` is written to `config/athlete` after every turn (lim L-48): a
dropped connection resumes at the next unanswered item, never restarts. If
the user volunteers a later answer mid-flow (say, units plus "I train 4 days"
in one line), `intake.py` writes it immediately and skips that item's turn
later with a short acknowledgement instead of asking again (lim L-47).

## Baseline (dec "Baseline flow", dec "Baseline session shape")

Ask once: known 1RM, or the heaviest recent `weight x reps`. The answer is
written verbatim to `config/athlete.strength_baseline`, so
`program-design` can price a starting load from it without asking the
athlete to type the numbers a second time; that skill owns the Brzycki
estimate (`references/questions.md` "Baseline branch", never above 10 reps,
research/07 s4.1). Storing the sentence rather than parsed numbers keeps one
answer on file and one parser (`program-design/scripts/baselines.py`). The
agent still decides per client whether a dedicated baseline session runs
before the first program, and any actual baseline sets are logged later
through `session-runner` like any other set.

## Turn 1, from cold

One read: `config_read("config/athlete")`, which is also where every answer
but `units` and `nutrition_strictness` lands, including the parent page id,
the timezone, and the `notion_data_sources` map that says which databases
already exist. `{}` means this install was
never set up, so the `database-create` writes start and the questions
start at item 1 of `references/questions.md`. A populated page means a
resumed intake, and `intake_cursor` names the next unanswered item (lim
L-48): pick up there, never restart the list. This read is what the
`@intake_cursor` fixture directive was standing in for, so a resumed
conversation no longer needs a seeded cursor to work.

## Never

No silent default for any of: the parent page id, the timezone, units,
training age, goal, days per week, equipment, jurisdiction, nutrition
strictness, referral name, age. Never guess a timezone from the clock and
never guess a page id: both are asked, and an answer that does not parse is
re-asked. No age
gate, no guardian consent flow, no DPIA (dec "T18 final"). PAR-Q+ wording is
never paraphrased; see `.claude/skills/screen/references/parq-plus.md`.
