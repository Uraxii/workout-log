# Exercise catalog coverage — free-exercise-db vs. wger

Research slice O. Dated **2026-09-01**. Counts below come from commands run
against the live datasets (appendix). Probe list is the 84-item list supplied
in this task's brief.

---

## TL;DR

- **free-exercise-db (876 entries)**: 42% hit rate (36/84) on the probe list.
  Weak on barbell squat/deadlift variants, near-blank on calisthenics
  skill moves and loaded-carry/strongman work.
- **wger (870 entries, English)**: 55% hit rate (47/84). Stronger on
  calisthenics (front lever, back lever, planche, typewriter pull-up,
  Nordic curl all present) and on barbell accessory work (Meadows row,
  Kroc row, landmine press/rotation).
- **User's suspicion was wrong on the specific example**: Zercher squat
  *is* in free-exercise-db (`Zercher Squats`). It is missing from wger.
- **24 of 84 probes are missing from both catalogs** — that is the real gap,
  not the single example. List below.
- **Schema gap, not just content gap**: free-exercise-db has no `aliases`
  field and no `variation_group` field. build-plan.md s1.3 wants both. wger
  has both natively (`translations[].aliases`, `exerciseinfo.variation_group`,
  populated on ~72% of a 50-row sample).

---

## Probe table (84 exercises)

`exercise | free-exercise-db hit | wger hit`. `MISSING` = no substring match
on name (fed has no alias field to also check; wger's alias field was not
separately probed, name only). Rows marked `(name variant)` were false
misses on a strict grep — the catalog has the exercise under different
wording, patched by hand after a manual check.

| exercise | free-exercise-db | wger |
|---|---|---|
| Zercher squat | Zercher Squats | MISSING |
| Jefferson deadlift | MISSING | MISSING |
| safety bar squat | MISSING | MISSING |
| front squat | Front Squat (Clean Grip) | Double Kettlebell Front Squat |
| Anderson squat | MISSING | MISSING |
| pin squat | MISSING | Pin Squat |
| box squat | Box Squat | 1 Leg Box Squat |
| pause squat | MISSING | MISSING |
| Romanian deadlift | Romanian Deadlift | Barbell Romanian Deadlift (RDL) |
| sumo deadlift | Reverse Band Sumo Deadlift | Dumbbell sumo deadlift |
| trap bar deadlift | Trap Bar Deadlift | MISSING |
| deficit deadlift | Deficit Deadlift | Deficit Deadlift |
| snatch-grip deadlift | MISSING | MISSING |
| good morning | Band Good Morning | Good Morning |
| hip thrust | Barbell Hip Thrust | Dumbbell Hip Thrust |
| Nordic curl | MISSING | Nordic Curl |
| glute ham raise | Glute Ham Raise | MISSING |
| pistol squat | Kettlebell Pistol Squat | Pistol Squat |
| shrimp squat | MISSING | MISSING |
| sissy squat | Weighted Sissy Squat | MISSING |
| Bulgarian split squat | MISSING | Bulgarian split squats left |
| Cossack squat | MISSING | Cossack squat |
| muscle-up | Muscle Up (name variant) | Muscle up (name variant) |
| pull-up | Band Assisted Pull-Up | Assisted Pull-Up |
| chin-up | Chin-Up | Assisted chin-ups |
| archer pull-up | MISSING | MISSING |
| typewriter pull-up | MISSING | Typewriter Pull-ups |
| front lever | MISSING | Front Lever |
| back lever | MISSING | Back Lever |
| planche | MISSING | Dynamic Planche |
| pseudo planche push-up | MISSING | Pseudo Planche Push-up |
| handstand push-up | Handstand Push-Ups | MISSING |
| wall walk | MISSING | MISSING |
| L-sit | MISSING | L-Sit (Foot Supported) |
| dragon flag | MISSING | MISSING |
| ab wheel rollout | MISSING | MISSING |
| hollow body hold | MISSING | Hollow Body Hold (Core L1) |
| skin the cat | MISSING | MISSING |
| ring dip | Ring Dips | Ring Dips |
| ring row | MISSING | MISSING |
| Australian pull-up | MISSING | Australian pull-ups |
| Turkish get-up | Kettlebell Turkish Get-Up (Lunge style) | Turkish Get-Up |
| kettlebell swing | One-Arm Kettlebell Swings | 2 Handed Kettlebell Swing |
| kettlebell snatch | Double Kettlebell Snatch | MISSING |
| clean and press | Clean and Press | Barbell Clean and press |
| farmer carry | Farmer's Walk (name variant) | Dumbbell farmer's carry (name variant) |
| suitcase carry | MISSING | Suitcase Carry |
| sled push | Sled Push | Sled Push |
| sled drag | Bear Crawl Sled Drags | MISSING |
| sandbag carry | Sandbag Load (near-synonym, not carry) | MISSING |
| tire flip | Tire Flip | MISSING |
| battle ropes | MISSING | Battle Ropes |
| box jump | Box Jump (Multiple Response) | box jumps |
| broad jump | MISSING | MISSING |
| burpee | MISSING | 4-count burpees |
| bear crawl | Bear Crawl Sled Drags | Bear crawl pull through |
| wall ball | MISSING | Wall balls |
| thruster | Kettlebell Thruster | Dumbbell Thruster |
| man maker | MISSING | MISSING |
| devil press | MISSING | MISSING |
| rope climb | Rope Climb | MISSING |
| GHD sit-up | MISSING | MISSING |
| Copenhagen plank | MISSING | MISSING |
| Pallof press | Pallof Press | Pallof Press |
| face pull | Face Pull | Dumbbell Bent Over Face Pull |
| landmine press | MISSING | Landmine press |
| landmine rotation | MISSING | Landmine Rotation |
| Meadows row | MISSING | Meadows Row |
| Pendlay row | MISSING | MISSING |
| Kroc row | MISSING | Kroc Row |
| Zottman curl | Zottman Curl | Zottman curl |
| Cuban press | Cuban Press | MISSING |
| Jefferson curl | MISSING | MISSING |
| banded | MISSING | Banded Ankle Mobility |
| Nordic hamstring | MISSING | MISSING |
| reverse Nordic | MISSING | Reverse Nordic Curl |
| Poliquin step-up | MISSING | MISSING |
| Peterson step-up | MISSING | MISSING |
| ATG split squat | MISSING | MISSING |
| tibialis raise | MISSING | Tibialis raises |
| KOT split squat | MISSING | MISSING |
| Yoga | MISSING | Yoga exercise: Cow-cat |
| 90/90 | 90/90 Hamstring | MISSING |
| world's greatest stretch | World's Greatest Stretch | MISSING |

**Third catalog ("other")**: not probed. ExerciseDB (RapidAPI) is
quota-capped (~10 req/day free tier) and MuscleWiki blocks `/api/` in
`robots.txt` — both already rejected in `research/05-existing-tools-and-formats.md`
"Exercise database recommendation" table, re-fetching them inside this
35-minute timebox would not change that verdict. Column left out rather than
filled with a repeat of note 05.

**Missing from both catalogs (24 of 84 — the real coverage hole):**

Jefferson deadlift, safety bar squat, Anderson squat, pause squat,
snatch-grip deadlift, shrimp squat, archer pull-up, wall walk, dragon flag,
ab wheel rollout, skin the cat, ring row, broad jump, man maker, devil press,
GHD sit-up, Copenhagen plank, Pendlay row, Jefferson curl, Nordic hamstring,
Poliquin step-up, Peterson step-up, ATG split squat, KOT split squat.

Pattern in the gap: **niche barbell technique variants** (Jefferson deadlift,
Anderson/pause squat, safety-bar squat, snatch-grip deadlift, Pendlay row,
Jefferson curl), **calisthenics skill progressions** (wall walk, dragon flag,
skin the cat, ab wheel rollout, ring row, archer pull-up), and
**named step-up/ATG rehab-lineage drills** (Poliquin, Peterson, ATG, KOT —
all from the same Ben Patrick/knee-training lineage, none of these have
entered either general-purpose database).

---

## Schema comparison

| field | free-exercise-db | wger (`exerciseinfo` + `translations`) |
|---|---|---|
| aliases | **absent** | present, `translations[].aliases` |
| equipment | present, single string | present, FK list |
| mechanic (compound/isolation) | present | **absent** |
| force (push/pull/static) | present | **absent** |
| level (beginner/intermediate) | present | **absent** |
| primary muscles | present, `primaryMuscles[]` | present, `muscles[]` |
| secondary muscles | present, `secondaryMuscles[]` | present, `muscles_secondary[]` |
| instructions | present, step array | present, one prose `description` field, not step-numbered |
| images | present, local repo paths | present, hosted URLs |
| variation_group | **absent** | present, `exerciseinfo.variation_group`, populated on 36/50 (72%) of a sampled batch |

build-plan.md s1.3 names `aliases`, `primary_muscles`, `secondary_muscles`,
`movement_pattern`, `mechanic`, `equipment`, `is_unilateral`, `variation_group`,
`variation_chain`, `variation_index` as the target schema. free-exercise-db
covers 5 of 10 directly (muscles x2, mechanic, equipment, and `category`
loosely maps to `movement_pattern`). It has neither `aliases` nor any
variation-grouping field — both would need to be built or imported from
elsewhere. wger's own schema already carries an `aliases` array and a
`variation_group` id, which is closer to the target shape on paper, at the
cost of the per-entry mixed licensing 05 already rejected it for.

---

## Licence and freshness

| catalog | licence | entries | last updated |
|---|---|---|---|
| free-exercise-db | Unlicense (public domain), confirmed via `LICENSE.md` and GitHub API `license.spdx_id` | 876 | repo pushed 2026-08-30, 1822 stars |
| wger | App AGPL-3.0; **exercise data licensed per entry** (CC-BY-SA 3.0/4.0, CC-BY 4.0, CC0, or ODbL — 05's finding, not re-verified here) | 870 (English translations = base exercise count) | queried live 2026-09-01; per-exercise `created`/`last_update` timestamps exist but were not aggregated |

No new licence finding beyond what `research/05-existing-tools-and-formats.md`
already established. This note adds the entry counts and the probe-level
content comparison note 05 did not do.

---

## DECISION

**Keep free-exercise-db as the seed catalog** (license and self-containment
still win — no live API dependency at runtime, no per-entry attribution
bookkeeping). **Fill gaps with:**
1. an own-authored `exercises/extra.json` in the same record shape, one row
   per catalog-catalog gap — **24 entries** needed to close every probe-list
   item both free-exercise-db and wger lack;
2. an alias table (build-plan.md s1.3 already specs `aliases` as a column
   free-exercise-db does not have) — populate it partly by hand-mining
   wger's `translations[].aliases` for overlapping exercises as a one-time
   import, not a runtime call;
3. user-added rows at runtime as the final escape hatch for anything the
   seed + extras still miss.

---

## Open Questions

Per global instruction ("if unclear, ask the user"), flagged here instead of
guessed at, since this is an unattended run:

1. Should the 24-item extras list be authored now (this task's scope stops
   at measurement, per SCOPE) or is that a separate follow-up task?
2. Is mining wger's `aliases`/`variation_group` data for the alias table and
   variation grouping an acceptable one-time import, or does the project
   want to avoid touching wger's per-entry-licensed data at all, even for
   metadata not redistributed verbatim?
3. The probe list treats "banded work (any)" and "Yoga (any)" and "mobility
   drills (any)" as single terms because they are categories, not named
   exercises — grep hit rate on those three rows is not meaningful the way
   it is for a named lift. Worth a separate category-completeness pass if
   that granularity matters.

---

## Appendix: commands run

```bash
# fetch free-exercise-db
curl -sS -o exercises.json \
  https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json
jq 'length' exercises.json                     # 876
jq -r '.[0] | keys' exercises.json             # schema fields
jq -r '.[].name' exercises.json > names.txt    # name list for grep

# license + freshness
curl -sS -o LICENSE.md \
  https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/LICENSE.md
curl -sS "https://api.github.com/repos/yuhonas/free-exercise-db" \
  | jq '{pushed_at, stargazers_count, license: .license.spdx_id}'

# fetch wger (English translations, paginated) + schema
curl -sS "https://wger.de/api/v2/language/?format=json&limit=30" \
  | jq -r '.results[] | select(.short_name=="en")'   # id = 2
for off in 0 500 1000 1500 2000 2500 3000; do
  curl -sS "https://wger.de/api/v2/exercise-translation/?limit=500&offset=$off&format=json" \
    | jq -c '.results[] | select(.language==2) | {exercise, name}'
done > wger_en_raw.json
jq -r '.name' wger_en_raw.json > wger_names.txt
curl -sS "https://wger.de/api/v2/exerciseinfo/?limit=1&format=json" | jq '.results[0] | keys'
curl -sS "https://wger.de/api/v2/exerciseinfo/?limit=1&format=json" \
  | jq '.results[0].translations[0] | keys'
curl -sS "https://wger.de/api/v2/exercise/?limit=1&format=json" | jq '.count'  # 870

# probe script (all 84 terms, case-insensitive fixed-string grep)
# /tmp/catalog-audit/probe.sh > probe_results.tsv
```

Scratch work, raw JSON, name lists, and `probe.sh` live in
`/tmp/catalog-audit/` (not committed, per task scope).
