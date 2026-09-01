# Template choice table

One row per rule, checked top to bottom, first full match wins
(`scripts/library.py:pick_template`). A blank cell (`-`) means that column
never disqualifies the rule. `goal`, `equipment`, and `training_age` match if
any listed word appears in the athlete's own words; `min_days` requires
`days_per_week` to be at least that number.

| template | goal | equipment | min_days | training_age | reason |
|---|---|---|---|---|---|
| otago | falls, balance, older adult, frail | - | - | older adult, elderly, 65, 70, 80 | Otago is the falls-prevention standard for an older or frail adult. It progresses by level, not load, matching low-impact needs. |
| couch-to-5k | run, running, 5k, couch to 5k, cardio | - | - | - | Couch to 5k is the standard sedentary-to-5k on-ramp. No equipment needed, and it matches a running or cardio goal directly. |
| kettlebell-wiki | - | kettlebell only, only kettlebell | - | - | Kettlebell is the only equipment on hand, and the r/kettlebell wiki routine is the one template built for kettlebell alone. |
| bwf-rr | calisthenics, bodyweight, rings | bodyweight, none, rings | - | - | The bodyweight Recommended Routine covers a bodyweight or rings goal with no barbell required. |
| nsuns-lp | powerlifting | barbell | 4 | intermediate, experienced, advanced | nSuns is a 4+ day training-max wave built for an intermediate or more advanced lifter with a barbell, more volume than GZCLP asks for. |
| phul | hypertrophy, muscle, build muscle, bodybuilding | barbell, dumbbell | 4 | - | PHUL splits power and hypertrophy days across 4 days with barbell and dumbbell work, matching a muscle-building goal at that frequency. |
| ppl-metallicadpa | hypertrophy, muscle, push pull legs, ppl | barbell, dumbbell | - | - | Metallicadpa's PPL is the linear-progression push/pull/legs split for a muscle goal with barbell and dumbbell, any day count. |
| easy-strength | general health, longevity, wellness | - | 2 | - | Easy Strength holds submaximal daily work across five movement patterns, fitting a general-health goal at 2-3 days with whatever equipment is on hand. |
| bbr | strength, general strength, get stronger | barbell | 3 | novice, beginner, new, never trained | The Basic Beginner Routine is the standard first program for a true novice: 3 days, barbell, fixed increments, nothing to double-progress yet. |
| gzclp | strength, general strength, get stronger | barbell | 3 | - | GZCLP is the standing default for a 3-4 day barbell strength goal past the absolute-novice stage: double progression with a proven T1/T2/T3 shape. |
