---
name: intake
description: First run, "set me up", or a life change. Creates the four Notion databases from schema/notion-schema.json, seeds the exercise catalog, then asks every profile question in order with no silent defaults. Use on "set me up", a fresh workspace, or when the athlete's situation has changed enough to redo the profile.
---

# intake

Conversation belongs here; parsing, question order, and every write belongs to
`scripts/intake.py`, which is pure and fixture-replayable
(`intake_turn(line, state) -> {"writes", "say", "state"}`, docs/architecture.md
"The script seam"). This skill calls it once per user turn, says exactly
`say`, and applies `writes` through `row-create` / `config-write` /
`database-create`.

## Database creation, first "set me up" (build-plan s5.1)

There is no template page. `intake.py` returns **one** `database-create` write
per turn until all four `schema/notion-schema.json` databases exist, because
`notion-create-database` answers with the new data source id and the next
database's relation columns need it. Apply the write, then put the returned id
in `state["databases"][<name>]` before the next turn; the seam is a pure
function of `(line, state)` and never sees a response.

The order comes from the schema's relation graph, not a list: `Locations` and
`Exercises` carry no relations out, `Sessions` relates to `Locations`, and
`Sets` relates to `Sessions` and `Exercises`. Each call is query-before-create
(rule L8): a database of that name under the user's page is adopted, not
duplicated, so a second "set me up" is harmless and appends nothing.

**The payload is rendered from the schema by `scripts/ddl.py`, never
hand-built.** The tool takes a SQL DDL `CREATE TABLE` statement, and a payload
an LLM assembles from prose drifts from the schema. See
`references/db-create.md`.

The parent page id is the user's, read from `state["notion_parent_page_id"]`.
With no id there is nothing to create under, and the questions still run.

## Catalog seeding

After the four databases exist, seed `Exercises` from
`exercises/catalog.json` (913 rows) with one `row_create` per row. Notion
Free is rate-limited to roughly 3 requests/second, so this is a one-time step
of **roughly 5 minutes**. Tell the user this before starting, and do not
block the question flow on it finishing: the questions can run while it
seeds, or right after; either order is fine as long as the user is told.

## The question flow

`references/questions.md` has the ordered list: safety (PAR-Q+, seven
questions plus a conditional follow-up, delegated in-process to `screen`),
then goal, history, constraints, body, recovery, preferences (build-plan
s5.2). **One question per turn**, since this is a phone conversation
(`principle-experience-first`), and **no silent defaults**: every item on
the list gets asked, including age, with no gate (dec "T18 final").

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
but `units` and `nutrition_strictness` lands. `{}` means this install was
never set up, so the `database-create` writes start and the questions
start at item 1 of `references/questions.md`. A populated page means a
resumed intake, and `intake_cursor` names the next unanswered item (lim
L-48): pick up there, never restart the list. This read is what the
`@intake_cursor` fixture directive was standing in for, so a resumed
conversation no longer needs a seeded cursor to work.

## Never

No silent default for any of: units, training age, goal, days per week,
equipment, jurisdiction, nutrition strictness, referral name, age. No age
gate, no guardian consent flow, no DPIA (dec "T18 final"). PAR-Q+ wording is
never paraphrased; see `.claude/skills/screen/references/parq-plus.md`.
