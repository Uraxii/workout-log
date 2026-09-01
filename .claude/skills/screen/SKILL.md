---
name: screen
description: Pre-participation health screening. Asks the PAR-Q+ seven general health questions verbatim, with follow-ups only when the answer is YES, and writes the clearance state. Runs inside intake on first setup, and re-fires standalone on any health change or after 12 months.
---

# screen

Conversation belongs here; the question text and the turn loop belong to
`scripts/screen.py`, pure and fixture-replayable
(`screen_turn(line, state) -> {"writes", "say", "state"}`,
docs/architecture.md "The script seam"). What a pass is worth (the clearance
value, rule S5's `progression: manual` exit) belongs to
`scripts/clearance.py`. `intake` calls the same `is_yes` / `clearance_write`
helpers in-process for its own safety block, so the questions and the
clearance rule live in exactly one place (`references/parq-plus.md`).

## The seven questions, verbatim, in order

`references/parq-plus.md` carries the PAR-Q+ general health questions
quoted from the current form, with citation and the licence term that
forbids paraphrasing or dropping one (build-plan s5.2, dec "T3 PAR-Q+ asked
verbatim"). `screen` presents each exactly as written, one per turn.

## Follow-up, only on YES

All seven NO: `config/limits.clearance = "cleared"`, `parq_date` = today, no
follow-up turn. Any YES: one follow-up turn asks, as a **yes/no question**,
whether a clinician has already cleared exercise, and for the condition and
the date alongside it. Only that explicit answer decides `clearance`:
`"cleared"` on yes, `"referred"` on no, `"pending"` on anything else, and
`screen` asks again until it gets a yes or a no. Never read clearance out of
free text: "my clinician has not cleared me" contains every word a
substring match wants and means the opposite (ticket R4). **Only `screen`
writes `clearance`** (rule S8): `intake` never sets it directly, even though
the PAR-Q+ pass runs inside `intake`'s turn loop.

## Rule S5: the re-screen that clears `progression: manual`

`pain-triage` switches progression to manual on a stop-level report; nothing
but rule S5 turns it back on, and S5 needs two things at once. A completed
re-screen ending `cleared` is one. The other is `SYMPTOM_FREE_DAYS` (14)
symptom-free **logged** days. Both hold: `screen` writes `progression: auto`
in the same turn and says so. Only one holds: progression stays manual,
`screen` names the missing half and tells the athlete her current count, so
the brake she cannot otherwise inspect says what it is waiting for. A
re-screen on its own never releases the brake.

A day counts toward the window when a `Sessions` row carries that local date
(training was logged), the date is strictly after the last symptom, and the
session was not left `halted`. Calendar days are not a substitute and never
were: counting them let an athlete who crashed, trained nothing for two weeks
and re-screened take the brake off with no recovery shown at all, which is
build-plan s11 risk 19 built rather than prevented (ticket workout-log-3fc).

The window starts at the newest `opened_at` across every `config/limits`
entry, resolved or not, because that is the date of the last stop-level
report: `pain-triage` rewrites `opened_at` whenever it re-opens an entry for
that area (rule S8). That is what "consecutive" means in S5. A fresh report
moves the date forward and the count restarts at zero, however many days were
logged before it. No dated entry at all means no anchor, which counts zero
and holds the brake: `progression: manual` is only ever written alongside an
entry, so the pairing missing is corruption, not consent.

`fixtures/06-logged-days` proves the release and the reset;
`fixtures/06-rescreen` proves 20 calendar days with nothing logged do not
release it.

## Re-fire triggers

Beyond the one pass inside `intake`: any reported health change, and the
form's own 12-month expiry on the clearance date (`references/parq-plus.md`
"Expiry"). A re-fire is a fresh pass through all seven questions: the form's
own licence forbids skipping any of them, even on a re-screen.

## Turn 1, from cold

One read for clearance: `config_read("config/limits")`, for `clearance` and
`parq_date`. A re-screen against `progression: manual` needs a second,
`row_query("Sessions")`, for the logged-day count above; `state` carries it as
`sessions_by_date` (`tools/mock-notion/hydrate.py`). Absent, the count is zero
and the brake holds, so a caller that skips the read errs toward manual.
`{}`, or a page carrying no `clearance` key, means never screened: ask all
seven PAR-Q+ questions verbatim from `references/parq-plus.md`, in order, one
per turn. A `parq_date` more than 12 months old re-fires the same full pass
("Re-fire triggers" above), and the licence forbids skipping a question on a
re-screen, so a partial re-ask is not an option either. Never infer clearance
from the absence of a `config/limits` entry. Absent is `pending`, never
`cleared` and never `not_required`.

## Never

Never paraphrase, reorder, or drop a PAR-Q+ question. Never ask a follow-up
when every question was NO. Never infer a clinician's clearance from a
sentence the athlete wrote about it; ask the yes/no question again instead,
and leave `clearance` at `pending` while you wait. Rule S8 also reserves the *per-injury* entry
status `cleared by clinician` for `screen` alone, against a named clinician
and a date; that is a different, later field on a `config/limits` entry
(owned by `session-runner` / `pain-triage`, phase 6), not this skill's
top-level `clearance` value, and this phase does not write it.
