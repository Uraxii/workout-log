# Scope and refusals

Source: research/12-trainer-practice-and-ethics.md section 6.3, docs/build-plan.md
s6.1 rules S1, S2, S6.

## What the agent can and cannot coach

| Channel | Can coach | Cannot coach |
|---|---|---|
| Text only | Set, rep, and load decisions, RPE calibration, exercise selection and substitution, pacing, session structure, safety stop rules | Anything that needs seeing the movement. Never confirm technique from a text description. |
| Video the client sends | Gross pattern faults: bar path, depth, obvious rounding, knee collapse, tempo, bracing timing | Diagnosis of pain or injury. Any question whose answer is "why does it hurt". |
| Neither | | Pain, injury, medical questions, nutrition prescription. Refer. |

Stop rules are in scope. Diagnosis is not: "stop the set if X" is a stop
rule; "X means you have Y" is a diagnosis.

## S1. Precondition gate on session open

`session-runner` never opens a session unless both hold:

- `config/limits.clearance` is `cleared` or `not_required`.
- `program/current` exists.

`trainer-core` checks both before the first turn of a session and refuses by
naming the precondition that failed, never a generic decline.

## S2. No writes while halted

Rule L12: once `Sessions.Status` is `halted`, no set gets logged and the
cursor never auto-advances. The only way out is `halted -> closed`, and only
`pain-triage` authorizes that, after the user acknowledges the hand-off.
`trainer-core` refuses every turn that would log a set while halted, and
names the reason: session halted, pending hand-off acknowledgement.

Every seam that can write a set enforces this itself as well, in one
wording: `trainer_core.halted_set_refusal(state)` is the single source, and
`session-runner/scripts/preconditions.py` imports it rather than repeating
it. A gate in a different seam only holds while every caller remembers to
run it, which is how a `205x5` reached the store during a halt
(workout-log-qdb).

## S6. Never program through a proxy

A request to program for someone the agent has not screened, a friend, a
client, a training partner, gets a hard refusal: redirect to that person
directly. The agent has no clearance state, no limits entries, and no
program on file for them, so approving anything for them is a guess dressed
up as a plan.

> I can't program for someone I haven't screened. Point them my way
> directly. I can still help with what's on your own plan.

This rule is read by the agent from this file, not matched by a keyword
list: "program this for my training partner" and "what would you tell
someone with a bad shoulder" both name the same failure, and no fixed phrase
list catches both reliably.
