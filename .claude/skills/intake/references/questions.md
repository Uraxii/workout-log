# Intake question order

Build-plan s5.2: v1's groups stand, safety / goal / history / constraints /
body / recovery / preferences, every question asked, nothing silently
defaulted. One item per turn (`principle-experience-first`: fast to answer
from a phone). Age has no gate (dec "T18 final"): it is an ordinary profile
fact, asked in its normal turn.

Safety runs first, via `screen`'s seven PAR-Q+ questions, verbatim, one per
turn: `.claude/skills/screen/references/parq-plus.md`. `intake` calls
`screen_turn` in-process for that block; `intake_cursor` still advances one
step per PAR-Q+ question, so an interruption mid-PAR-Q+ resumes there, not at
the top (lim L-48).

| # | id | Prompt | Writes to |
|---|---|---|---|
| 1-7 | `parq_1`..`parq_7` | PAR-Q+ Q1-Q7 verbatim | `config/limits.clearance`, `.parq_date` (via `screen`) |
| 8 | `parq_followup` | Only asked if any Q1-Q7 was YES | `config/limits.clearance`, `.parq_date` (via `screen`) |
| 9 | `units` | "Pounds or kilos?" | `config/preferences.units` |
| 10 | `jurisdiction` | "What country or state are you in? Scope-of-practice rules vary." | `config/athlete.jurisdiction` |
| 11 | `goal` | "What's the goal? Strength, muscle, fat loss, endurance, sport, general health, or rehab-adjacent?" | `config/athlete.goal` |
| 12 | `training_age` | "Have you trained before? How long, how consistently?" | `config/athlete.training_age` |
| 13 | `days_per_week` | "How many days a week can you train?" | `config/athlete.days_per_week` |
| 14 | `equipment` | "What equipment do you have? Barbell, dumbbells, machines, bands, bodyweight only?" | `config/athlete.equipment` |
| 15 | `baseline` | "Know your 1RM on your main lifts? If not, what's the most weight x reps you've done recently?" | see baseline branch below |
| 16 | `measure_kinds` | "Do any of these apply: timed holds, loaded carries, running, level-graded work like Otago?" | `config/athlete.measure_kinds` |
| 17 | `age` | "How old are you?" | `config/athlete.age` |
| 18 | `nutrition_strictness` | "How strict do you want nutrition guidance? None, general, or specific numbers?" | `config/preferences.nutrition_strictness` |
| 19 | `referral_name` | "If something needs a referral, who's the name on file? A GP is the default." | `config/athlete.referral_name` |
| 20 | `location` | "What gym or space are you training in? Name it, so I can track its equipment." | `Locations` row |

`parq_followup` is a conditional slot: `_advance` marks it pre-answered
(`"n/a"`) the moment all seven come back NO, so it is skipped with no spoken
line, the same skip machinery `references/questions.md` "Out-of-order
answers" uses for a volunteered field.

## Baseline branch (dec "Baseline flow", dec "Baseline session shape")

If a known 1RM is given, store it directly. Otherwise, from a reported
`weight x reps`, estimate with Brzycki: `1RM = weight * 36 / (37 - reps)`,
never above 10 reps (research/07 s4.1). The agent, not this script, decides
per client whether a dedicated baseline session runs before the first program
(dec "Baseline flow" overrides T4's default).

## Out-of-order answers (lim L-47)

Any line is scanned against every not-yet-answered item's pattern, not only
the current one. A match writes that item immediately and marks it answered;
when its turn comes, `intake` says one acknowledgement clause ("already got
that: 4 days a week.") instead of asking again.
