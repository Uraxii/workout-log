---
name: pain-triage
description: Fires on any mention of pain, numbness, tingling, a pop, swelling, or crash/fatigue language. Maps the free text to niggle or stop with references/red-flags.md's table, and on stop halts the session and opens a dated config/limits entry naming the area. Never clears an entry or progression:manual on a bare confirmation. Use whenever the user reports pain, an injury, or being wiped out.
---

# pain-triage

Conversation belongs here; the phrase-to-enum table, the halt, and the
`config/limits` write belong to `scripts/pain_triage.py`, pure and
fixture-replayable (`triage_turn(line, state) -> {"writes", "say",
"state"}`, docs/architecture.md "The script seam"). `references/red-flags.md`
is the source of record for the word lists; the script parses them from that
file instead of holding a second copy.

## Classify first (rule S3)

Every report maps to exactly one of `niggle` or `stop`. `stop` wins when a
line names both. `references/red-flags.md` carries the full table, plus the
crash and fatigue words a PEM-style report uses instead of pain words
(lim L-43), plus the under-18 Ottawa ankle and knee branch (rule S4). The
Ottawa branch is prose the agent reads and applies in conversation: age and
"is this an acute ankle or knee injury" both come from free text, and a
hard-stop safety rule should refer rather than guess when either is unclear.

## niggle: say something, write nothing

A `niggle` report gets acknowledged and nothing else happens: no status
change, no limits entry, no halt. The session keeps going.

## stop: exactly two writes (rule S2, L12)

A `stop` report is the only case that writes:

1. `Sessions.Status` becomes `halted`. The session takes no more set writes
   until a person explicitly acknowledges the hand-off; only `pain-triage`
   authorizes leaving `halted` (rule L12), and this skill does not do that
   itself in release 1, `session-runner` does at the acknowledged close.
2. `config/limits.entries` gains, or re-opens, a dated entry naming the
   area the user mentioned (elbow, knee, shoulder, and so on), and
   `config/limits.progression` becomes `manual` in the same write: a
   `stop` report is the PEM-style hard stop that turns automatic
   progression off (research/00-synthesis-trainer.md "PEM hard stop").

Say the hand-off out loud, using `references/wording.md`'s template: name
the reason, name the profession, offer to keep helping with what is still
in scope. This is a hard refusal (rule S7): no override, however the user
pushes back on continuing that movement today.

## Two exits, and this skill owns neither (rule S8)

An open `config/limits` entry never gets deleted. It resolves only when
`session-runner` sees the user say the problem is gone **and** 14
consecutive days pass with no `stop`-level mention of that area. It gets
`cleared by clinician` only from `screen`, against a named clinician and a
date. A bare "I'm fine" or similar reassurance to `pain-triage` writes
nothing: not a resolved entry, not a cleared `progression: manual`. Say so,
plainly, so the user knows why the state did not change.

## Re-open on any new mention

A later report naming an area already tracked in `config/limits.entries`
re-opens that entry in place, never a duplicate, and resets its date. That
is the 14-day window `session-runner` reads restarting from zero.

## Turn 1, from cold

Two reads. `config_read("config/limits")` for `entries`, so a new dated entry
appends beside the existing ones instead of overwriting them, and so a report
naming an area already tracked is recognised and re-opened in place rather
than duplicated ("Re-open on any new mention" above). Empty `entries` means
this is the first one. `row_query("Sessions", {"Status": "open"})` names the
session a `stop` halts; `[]` means there is nothing to halt, so the
`config/limits` write still happens and the `Sessions.Status` write does not.
An empty read clears nothing: a bare confirmation still writes neither a
resolved entry nor a cleared `progression: manual` (lim L-42), and that holds
just as hard when the state came from a read as when it came from memory.

## Never

Never diagnose. Never name a condition, a cause, or a treatment; only name
the stop rule and the profession to see. Never write a third field beyond
`Sessions.Status` and the `config/limits` write. Never clear an entry or
`progression: manual` from this skill; that authority lives in
`session-runner` and `screen` alone.
