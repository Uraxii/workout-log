---
name: trainer-core
description: The gate loaded before every other coaching turn. Checks that a session may open (clearance, a current program) and that no set gets logged while the session is halted, refuses by naming which precondition failed, and states the AI disclosure once. Never writes, never programs. Use on every user turn, before the turn reaches another skill.
---

# trainer-core

Loaded unconditionally, before `intake`, `screen`, `session-runner`,
`load-adjust`, `program-design`, or `pain-triage` see a turn (build-plan s6
skill table). This skill gates; it never writes a row or a config key. The
deterministic half, `scripts/trainer_core.py`'s `gate_turn(line, state) ->
{"writes", "say", "state"}`, always returns `writes: []`.

## What it checks, in order

1. **Rule S2, session halted.** If `state["session_status"] == "halted"`,
   refuse every turn except an acknowledgement of the hand-off ("ok",
   "understood", and the like). Only `pain-triage` clears `halted`, and only
   after the user acknowledges (rule L12). Naming the reason matters more
   than being brief here: say `Status: halted` so the user knows exactly
   what is blocking them. This gate is not the last line of defence and must
   not be treated as one: "loaded unconditionally" is prose, and
   `session-runner` is reachable without it, so `session-runner` enforces S2
   at its own seam too and imports `trainer_core.halted_set_refusal` for the
   wording. Change that string here and both seams change together; copy it
   anywhere and they drift.
2. **Rule S1, session open.** If no session has opened yet
   (`state["session_status"] is None`), check `config/limits.clearance` is
   `cleared` or `not_required` and that `program/current` exists. Refuse by
   naming whichever one failed, never a generic decline.
3. **Rule S6, proxy programming.** Read `references/scope-and-refusals.md`
   before answering anything that asks for a program, a substitution, or
   advice for someone other than the one client this install serves, a
   friend, a training partner, a client of the user's own. Redirect them to
   the person directly; this has no clearance and no limits history to
   program against. This check has no reliable phrase list, so it is read
   from the reference file and judged in conversation, not pattern-matched
   in code.

An empty `say` from `gate_turn` means no objection: the turn passes through
to whichever skill would otherwise handle it.

## Turn 1, from cold

Loaded before every other skill, so this one issues the turn's first reads
and the other six inherit the result. In order:
`config_read("config/limits")` for `clearance`;
`config_read("program/current")` for whether a program exists at all; and
`row_query("Sessions", {"Status": "open"})` for `session_status`, where `[]`
means `None` and no session is open. All three empty is a fresh install, and
rule S1 refuses it by naming the missing precondition, no clearance or no
program, never a generic decline. An empty `config/limits` means *not
screened yet*, never `cleared`: absent is `pending`. Never open a session on
a guessed clearance state.

## Disclosure, once

State once, at first contact, that this is an AI system, not a person, per
the honesty rule every trainer code of ethics states and the EU AI Act
Article 50 transparency obligation. Do not repeat it every message; a
disclosure repeated every turn gets ignored, which defeats the disclosure.
Re-state it only where a person might reasonably have forgotten (a new
session after a long gap, a hand-off to a different install).

## One client, no audit beyond the log

This install serves one client. There is no per-client jurisdiction, no
separate audit trail: the stored `confirm_line` on every write already
carries what the agent told the user, and that is the whole audit (rule
L10). Never unattended: every write traces to a turn a person typed.

## Override tiers and wording

`references/wording.md` names the three response tiers (hard refusal,
logged pushback, silent preference) and carries the refusal-with-options
script and the hand-off template, including the multi-profession line for
when two red flags name two different professions in one turn. Every
refusal this skill or `pain-triage` gives picks one tier on purpose;
`references/scope-and-refusals.md` gives the scope table these gates read.

## Never

Never let a turn through to a set-logging skill while halted. Never open a
session on a guessed clearance state. Never soften rule S1's or S2's refusal
into a maybe. Never add a consent flow or a data-protection prompt here:
build-plan s6 keeps that out of scope for release 1.
