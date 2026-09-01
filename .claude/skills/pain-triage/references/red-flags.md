# Red flags: phrase table and the Ottawa age branch

Source for the phrase table: docs/build-plan.md s6.1 rule S3 (lim L-38).
Source for the age branch: research/17-ottawa-paediatric.md DECISION,
answering rule S4 (lim L-40).

## S3. Phrase to enum

`pain_triage.classify()` scans the user's line for these words and returns
the enum on the right. A line that names any `stop` word is `stop`, even if
a `niggle` word appears in the same line: `stop` always wins.

| The user says | Maps to |
|---|---|
| twinge | niggle |
| tight | niggle |
| sore | niggle |
| sharp | stop |
| pop | stop |
| gave way | stop |
| gave out | stop |
| shooting | stop |

`stop` also opens a dated entry on `config/limits` and moves the session to
`halted` (rule L12). `niggle` writes nothing and does not halt.

## Crash and fatigue language (lim L-43)

Add these words to the `stop` set. A post-exertional crash is not a joint
injury, but it switches off automatic progression the same way a `stop`
pain report does (research/00-synthesis-trainer.md "PEM hard stop"):

| The user says | Maps to |
|---|---|
| crash | stop |
| wiped out | stop |
| payback | stop |
| flare | stop |

## S4. Ottawa ankle and knee rule, under 18

For a client under 18, age 5 and up: the Ottawa ankle and knee rule text
applies unchanged, the same two-timepoint weight-bearing test and the same
tenderness landmarks used for an adult. This is sourced to Dowling 2009 for
the ankle (12 pooled studies, n = 3,130, pooled sensitivity 98.5%) and to
Vijayasankar 2009 for the knee (3 pooled studies, n = 1,130, pooled
sensitivity 99%).

Under age 5, including exactly age 5, there is no rule arithmetic. Any
suspected ankle or knee fracture after an acute injury refers for imaging,
regardless of what the exam finds. The paediatric meta-analyses found not
enough data below age 5 to say the rule holds there, and the rule's known
miss, a Salter-Harris growth-plate fracture, concentrates in exactly that
age band.

This branch is read out loud by the agent, never checked by code: age and
the presence of an acute ankle or knee injury both come from free text, and
a hard-stop safety rule should refer rather than guess when either is
unclear.

## Area extraction

`pain_triage._area()` looks for one of these words in the line to name the
`config/limits` entry: knee, ankle, shoulder, hip, back, elbow, wrist, neck,
foot, calf, hamstring, groin. No match writes the entry as `unspecified`,
never blocks the halt.
