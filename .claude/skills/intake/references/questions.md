# Intake question order

Build-plan s5.2: v1's groups stand, safety / goal / history / constraints /
body / recovery / preferences, every question asked, nothing silently
defaulted. One item per turn (`principle-experience-first`: fast to answer
from a phone). Age has no gate (dec "T18 final"): it is an ordinary profile
fact, asked in its normal turn.

Three questions about the tool come first, because nothing works without
them: the storage platform, the Notion parent page id (ticket
workout-log-mqs), and the timezone, frozen onto session 1 (rule L3). Naming
a store this build has no DDL for does not fail to parse; it is recorded,
then refused in place of the next prompt (`storage.refusal`, pinned byte for
byte by `fixtures/13-storage-refusal`). Then safety runs, via `screen`'s
seven PAR-Q+ questions, verbatim, one per turn:
`.claude/skills/screen/references/parq-plus.md`. `intake` calls
`screen_turn` in-process for that block; `intake_cursor` still advances one
step per PAR-Q+ question, so an interruption mid-PAR-Q+ resumes there, not at
the top (lim L-48).

| # | id | Prompt | Writes to |
|---|---|---|---|
| 1 | `storage_platform` | "Where do you want your training log kept? Notion is what I can write to today. Name anything else and I'll tell you straight away rather than half build it." | `config/athlete.storage_platform` |
| 2 | `storage_root` | "First, where should I put your logs?" and then the words of the store she named in question 1 (`ddl.ROOT_PROMPT`, `vault.ROOT_PROMPT`) | `config/athlete.storage_root` |
| 3 | `timezone` | "What timezone are you in? I need it as an IANA name, like America/Los_Angeles or Europe/London, so a late session lands on the right day." | `config/athlete.timezone` |
| 4-10 | `parq_1`..`parq_7` | PAR-Q+ Q1-Q7 verbatim | `config/limits.clearance`, `.parq_date` (via `screen`) |
| 11 | `parq_followup` | Only asked if any Q1-Q7 was YES | `config/limits.clearance`, `.parq_date` (via `screen`) |
| 12 | `units` | "Pounds or kilos?" | `config/preferences.units` |
| 13 | `jurisdiction` | "What country or state are you in? Scope-of-practice rules vary." | `config/athlete.jurisdiction` |
| 14 | `goal` | "What's the goal? Strength, muscle, fat loss, endurance, sport, general health, or rehab-adjacent?" | `config/athlete.goal` |
| 15 | `training_age` | "Have you trained before? How long, how consistently?" | `config/athlete.training_age` |
| 16 | `days_per_week` | "How many days a week can you train?" | `config/athlete.days_per_week` |
| 17 | `equipment` | "What equipment do you have? Barbell, dumbbells, machines, bands, bodyweight only?" | `config/athlete.equipment` |
| 18 | `baseline` | "Know your 1RM on your main lifts? If not, what's the most weight x reps you've done recently?" | see baseline branch below |
| 19 | `measure_kinds` | "Do any of these apply: timed holds, loaded carries, running, level-graded work like Otago?" | `config/athlete.measure_kinds` |
| 20 | `age` | "How old are you?" | `config/athlete.age` |
| 21 | `nutrition_strictness` | "How strict do you want nutrition guidance? None, general, or specific numbers?" | `config/preferences.nutrition_strictness` |
| 22 | `referral_name` | "If something needs a referral, who's the name on file? A GP is the default." | `config/athlete.referral_name` |
| 23 | `location` | "What gym or space are you training in? Name it, so I can track its equipment." | `config/preferences.location` |

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
