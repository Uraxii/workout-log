# Workout Log Data Model

Research slice A of 5. Date: 2026-08-31.
Scope: what the log must capture so an agent can prescribe today's work, log sets live, and later decide to raise or lower load.
Sibling slices (not covered here): progression heuristics, routines/UX, tool survey, trainer-agent skills.

---

## TL;DR

- **Five entities.** `Exercise` (catalog), `Program` (plan), `Session` (a day), `ExerciseInstance` (one exercise inside a day), `Set` (one row). Everything else is derived.
- **A fast set line needs two numbers: weight and reps.** Everything else defaults, carries forward from the last set, or is inherited from the program. This is the single most important design rule in the file.
- **Store weight as a `{value, unit}` pair, never a bare number.** Every serious open-source tracker does this (Liftosaur `IWeight`, wger `weight` + `weight_unit` FK). Converting on write loses the number the user actually saw on the bar.
- **Give exercises a stable opaque id plus an alias list.** Names change, ids must not. wger uses a UUID plus a separate `ExerciseAlias` table. Copy that.
- **RIR is the field that drives progression, not RPE.** Record whichever the user says, store both, and treat `RPE = 10 - RIR` as the conversion. Estimated 1RM from Epley or Brzycki is only trustworthy at ~10 reps or fewer.
- **Biggest modelling gap in every shipping app:** none of them cleanly model added/assisted load for bodyweight work, bar weight per equipment, or unilateral per-side reps. Liftosaur is the only one that gets close.

---

## 1. Entity overview

```
Program ──< ProgramDay ──< Slot ──< SlotEntry ─┐
                                                │ references
Exercise (catalog) ─────────────────────────────┤
                                                │
Session ──< ExerciseInstance ──< Set ───────────┘
```

Two trees. The **plan** tree (Program) says what should happen. The **log** tree (Session) says what did happen. A `Set` points back at the `SlotEntry` that prescribed it, when there was one. wger models exactly this link: `WorkoutLog` carries FKs to `session`, `exercise`, `routine`, and `slot_entry`, plus `iteration` ([wger/manager/models/log.py](https://github.com/wger-project/wger/blob/master/wger/manager/models/log.py)).

Keeping planned and actual in separate rows, rather than one row with a "did you hit it" flag, is what makes the progression decision computable later. wger goes further and stores both on the same row: `repetitions` next to `repetitions_target`, `weight` next to `weight_target`, `rir` next to `rir_target`, `rest` next to `rest_target` (same file). That is worth stealing — it means a set row is self-describing without a join.

---

## 2. Entity: `Set`

One row per set. The hot path. Everything here must be optional except the two numbers.

| Field | Type | Required | Default | Why it matters | Source |
|---|---|---|---|---|---|
| `id` | opaque string | yes | generated | Edit and delete without ambiguity | Liftosaur `ISet.id: string` ([types.ts](https://github.com/astashov/liftosaur/blob/master/src/types.ts)) |
| `weight` | `{value, unit}` | **yes** | carry-forward | The load. Unit travels with it | Liftosaur `IWeight {value, unit}` ([types.ts](https://github.com/astashov/liftosaur/blob/master/src/types.ts)) |
| `reps` | int | **yes** | carry-forward | The other half of the minimum entry | Strong CSV `Reps`; Hevy `reps` |
| `reps_left` / `reps_right` | int | no | null | Unilateral work where sides differ | Liftosaur `ISet.completedRepsLeft` + `isUnilateral` |
| `set_type` | enum | no | `working` | Warmups must be excluded from volume and PRs | Hevy enum `warmup \| normal \| failure \| dropset` ([openapi-spec.json](https://github.com/chrisdoc/hevy-mcp/blob/main/openapi-spec.json)) |
| `rir` | decimal | no | null | Primary progression signal | wger `rir = models.DecimalField` ([log.py](https://github.com/wger-project/wger/blob/master/wger/manager/models/log.py)) |
| `rpe` | decimal 6–10 | no | null | Same signal, other scale. Hevy restricts to a picklist | Hevy `rpe` enum `[6, 7, 7.5, 8, 8.5, 9, 9.5, 10]` ([openapi-spec.json](https://github.com/chrisdoc/hevy-mcp/blob/main/openapi-spec.json)) |
| `is_completed` | bool | no | true on log | Distinguishes planned rows from performed rows | Liftosaur `ISet.isCompleted` |
| `target_reps` | int | no | from plan | Lets the row answer "did I hit it" alone | wger `repetitions_target` |
| `target_weight` | `{value, unit}` | no | from plan | Same | wger `weight_target` |
| `target_rir` | decimal | no | from plan | Same | wger `rir_target` |
| `rest_seconds` | int | no | null (measure it) | Rest confounds progression reads | wger `rest` / `rest_target`; Hevy routine `rest_seconds` |
| `tempo` | string `E-P-C-P` | no | null | Rarely used; keep as free text, do not parse eagerly | UNVERIFIED — no surveyed export has a tempo column |
| `timestamp` | ISO 8601 | no | now | Recovers rest times and set order for free | Liftosaur `ISet.timestamp: number` |
| `notes` | string | no | null | Cheap escape hatch | Strong CSV `Notes`; FitNotes `Notes` |
| `pain_flag` | enum/bool | no | false | Safety gate: agent must not raise load into pain | UNVERIFIED — no surveyed tool has this field |
| `duration_seconds` | int | no | null | Timed holds, planks, carries | Hevy `duration_seconds`; Strong CSV `Seconds` |
| `distance` | `{value, unit}` | no | null | Carries, cardio | Hevy `distance_meters`; FitNotes `Distance` + `Distance Unit` |

**On `set_type`.** Hevy's four values (`warmup`, `normal`, `failure`, `dropset`) are the shipping minimum. AMRAP and backoff are missing there. Liftosaur models AMRAP as a boolean flag `isAmrap` on the set rather than a type, which is the better call — a set can be both a backoff and an AMRAP. Recommendation: keep `set_type` as an enum for the mutually exclusive roles (`warmup | working | backoff | dropset`) and add independent booleans `is_amrap` and `to_failure`.

**On `pain_flag`.** Nothing surveyed has it. It is the one field worth adding beyond the surveyed prior art, because it is the only input that can make an agent lower load against a rising trend. Suggest three values: `none | niggle | stop`.

---

## 3. Entity: `ExerciseInstance`

One exercise as it appeared in one session. The container for its sets.

| Field | Type | Required | Default | Why it matters | Source |
|---|---|---|---|---|---|
| `exercise_id` | catalog id | yes | — | Joins to the catalog | Hevy `exercise_template_id`; Liftosaur `IExerciseType.id` |
| `equipment` | string | no | catalog default | Same movement, different bar, different progression | Liftosaur `IExerciseType {id, equipment}` — equipment is part of the exercise identity |
| `order` | int | yes | append | Order affects fatigue, therefore affects the read | Hevy `index`; wger `SlotEntry.order` |
| `superset_group` | id/null | no | null | Sets inside a superset get shorter rest | Hevy `supersets_id`; Liftosaur `IHistoryEntry.superset` |
| `notes` | string | no | null | Per-exercise, not per-set | Hevy `Exercise.notes`; Strong CSV has separate `Notes` and `Workout Notes` |
| `machine_setting` | string | no | carry-forward | Seat height 4, pin 3. Reproducibility of the stimulus | UNVERIFIED — no surveyed export models this; closest is Liftosaur equipment `notes` |
| `band` | string | no | null | Band tension is not a weight | UNVERIFIED |
| `side` | enum | no | `both` | `left \| right \| both \| alternating` | Liftosaur `isUnilateral` only; no surveyed tool names the side |

### Load semantics — the part every app gets wrong

A logged number means different things per equipment. Liftosaur is the only surveyed tool that models this properly, in `IEquipmentData` ([types.ts](https://github.com/astashov/liftosaur/blob/master/src/types.ts)):

| Liftosaur field | Meaning | Why you need it |
|---|---|---|
| `bar: {lb, kg}` | Bar weight per unit | Total load = bar + plates. Store both units so no rounding on switch |
| `multiplier` | Number of implements | Dumbbells: log 20, lift 40 |
| `plates: [{weight, num}]` | Plate inventory | Plate math, and the achievable next jump |
| `fixed: IWeight[]`, `isFixed` | Fixed-weight rack / machine stack | Increment is not continuous |
| `useBodyweightForBar` | Bodyweight counts as the base load | Pull-ups, dips |
| `isAssisting` | The load *subtracts* | Assisted pull-up: more assistance is less work. Progression sign flips |

`isAssisting` is the one that matters for an agent. Without it, an assisted-pull-up machine trend reads backwards.

Recommendation: store a per-set `load` object rather than a scalar.

```json
{ "implement_weight": {"value": 20, "unit": "kg"},
  "bar_weight":      {"value": 20, "unit": "kg"},
  "added_weight":    {"value": 10, "unit": "kg"},
  "assist_weight":   null,
  "bodyweight_counts": false,
  "multiplier": 1 }
```

Total effective load is then a pure function, and the raw number the user typed survives.

---

## 4. Entity: `Session`

| Field | Type | Required | Default | Why it matters | Source |
|---|---|---|---|---|---|
| `id` | opaque | yes | generated | — | wger `id = UUIDField(default=uuid7)` ([session.py](https://github.com/wger-project/wger/blob/master/wger/manager/models/session.py)) |
| `date` | local date | yes | today | The unit users think in | wger `date = DateField` |
| `start_time` / `end_time` | ISO 8601 with offset | no | now / null | Duration, and rest reconstruction | Hevy `start_time` / `end_time`, ISO 8601 ([openapi-spec.json](https://github.com/chrisdoc/hevy-mcp/blob/main/openapi-spec.json)) |
| `timezone` | IANA name | no | device tz | See §8 | — |
| `program_id`, `day_id` | ids | no | null | Ties the session to what was planned | wger `routine` + `day` FKs |
| `iteration` | int | no | derived | Which pass through the program this is; progression rules key off it | wger `WorkoutLog.iteration` |
| `bodyweight` | `{value, unit}` | no | last known | Needed for bodyweight-exercise load, and for relative-strength trends | Hevy `BodyMeasurement.weight_kg` (separate endpoint) |
| `readiness`, `sleep_hours`, `energy` | int / decimal / int | no | null | Explains a bad session without lowering the plan | UNVERIFIED — surveyed apps only have a single impression field |
| `mood` / `impression` | enum | no | neutral | wger's version: `1 bad \| 2 neutral \| 3 good` | wger `impression` choices ([session.py](https://github.com/wger-project/wger/blob/master/wger/manager/models/session.py)) |
| `location` / `gym` | string/id | no | last used | Different gym, different plates, different bar. Changes what loads are reachable | Liftosaur `IGym` interface exists in types.ts |
| `notes` | string | no | null | — | wger `notes`; Strong CSV `Workout Notes` |
| `title` | string | no | day name | — | Hevy `Workout.title`; Strong CSV `Workout Name` |

**Recommendation on readiness fields:** one 1–5 integer, not four. Four fields that are usually blank teach the user to skip all of them. Sleep hours can come from elsewhere later. This is a UX call that overlaps slice C.

---

## 5. Entity: `Exercise` (catalog)

| Field | Type | Required | Default | Why it matters | Source |
|---|---|---|---|---|---|
| `id` | opaque, stable | yes | slug or uuid | **Must survive renames.** | wger `uuid = UUIDField`; free-exercise-db `id` pattern `^[0-9a-zA-Z_-]+$` ([schema.json](https://github.com/yuhonas/free-exercise-db/blob/main/schema.json)) |
| `name` | string | yes | — | Display | all |
| `aliases` | string[] | no | `[]` | Chat logging depends on this. "incline db press", "incline dumbbell bench" | wger has a dedicated `ExerciseAlias` model ([wger/exercises/models/exercise_alias.py](https://github.com/wger-project/wger/blob/master/wger/exercises/models/exercise_alias.py)) |
| `primary_muscles` | string[] | no | `[]` | Weekly sets-per-muscle | free-exercise-db `primaryMuscles` (17-value enum); Hevy `primary_muscle_group` |
| `secondary_muscles` | string[] | no | `[]` | Fractional volume counting | free-exercise-db `secondaryMuscles`; Hevy `secondary_muscle_groups` |
| `movement_pattern` | enum | no | null | squat/hinge/push-h/push-v/pull-h/pull-v/carry/isolation | UNVERIFIED — free-exercise-db offers `force` (`push \| pull \| static`) and `category` instead, which is coarser |
| `mechanic` | enum | no | null | `compound \| isolation` — drives increment size | free-exercise-db `mechanic` ([schema.json](https://github.com/yuhonas/free-exercise-db/blob/main/schema.json)) |
| `equipment` | string[] | no | `[]` | free-exercise-db has 13 values incl. `body only`, `barbell`, `dumbbell`, `machine` | free-exercise-db `equipment` |
| `is_unilateral` | bool | no | false | Halves the load bookkeeping | Liftosaur `ISet.isUnilateral` (per-set, not catalog) |
| `min_increment` | `{value, unit}` per equipment | no | derived from plates | **The field that makes progression executable.** No point telling the user +2.5 kg if the smallest pair is 5 lb | Liftosaur `IEquipmentData.plates` / `fixed` |
| `default_progression` | rule ref | no | program's rule | Per-exercise override (bench climbs slower than squat) | wger per-`SlotEntry` config models |
| `variation_group` | id | no | null | Groups low-bar/high-bar squat for trend comparison | wger `Exercise.variation_group = UUIDField` ([base.py](https://github.com/wger-project/wger/blob/master/wger/exercises/models/base.py)) |
| `level` | enum | no | null | `beginner \| intermediate \| expert` — of limited use to a personal log | free-exercise-db `level` |

**Seed source.** [free-exercise-db](https://github.com/yuhonas/free-exercise-db) is public-domain-ish JSON with ~800 exercises and a published `schema.json`; its 10 fields are all required in-schema. ExerciseDB (`bodyPart`, `target`, `equipment`, `gifUrl`, `secondaryMuscles`, `instructions`, `id`) is the alternative but its docs endpoint failed TLS verification on 2026-08-31 — **UNVERIFIED**, treat the field list as hearsay.

---

## 6. Entity: `Program` / `Routine`

wger's shape is the most expressive of the surveyed tools and worth mirroring:

`Routine` → `Day` → `Slot` → `SlotEntry` → per-field config rows.

| Level | Fields | Source |
|---|---|---|
| `Routine` | `name`, `description`, `created`, `start` (date), `end` (date), `is_template`, `is_public`, `fit_in_week` | [routine.py](https://github.com/wger-project/wger/blob/master/wger/manager/models/routine.py) |
| `Day` | `order`, `type`, `name`, `description`, `is_rest`, `need_logs_to_advance`, `config` (JSON) | [day.py](https://github.com/wger-project/wger/blob/master/wger/manager/models/day.py) |
| `Slot` | a position in the day; groups entries that form a superset | [slot.py](https://github.com/wger-project/wger/blob/master/wger/manager/models/slot.py) |
| `SlotEntry` | `exercise` FK, `repetition_unit`, `repetition_rounding`, `weight_unit`, `weight_rounding`, `order`, `comment`, `type`, `class_name`, `config` (JSON) | [slot_entry.py](https://github.com/wger-project/wger/blob/master/wger/manager/models/slot_entry.py) |
| progression | separate config models per field, each with an `iteration`: `WeightConfig`, `MaxWeightConfig`, `RepetitionsConfig`, `MaxRepetitionsConfig`, `SetsConfig` (0–50), `MaxSetsConfig`, `RiRConfig`, `MaxRiRConfig`, `RestConfig`, `MaxRestConfig` | files of the same names in [wger/manager/models/](https://github.com/wger-project/wger/tree/master/wger/manager/models) |

Two design choices there are load-bearing:

1. **Progression is expressed as per-field configs keyed by `iteration`**, not as one enum on the exercise. Weight can climb while reps stay fixed and RIR target drops. Min/max pairs bound each field.
2. **`repetition_rounding` and `weight_rounding` live on the plan, not the exercise.** That is where "round to the nearest 2.5 kg" belongs.

Liftosaur takes the opposite route: sets are *expressions* (`repsExpr`, `weightExpr`, `rpeExpr`, `minRepsExpr`, `timerExpr`, plus `isAmrap`, `askWeight`, `logRpe` — `IProgramSet` in [types.ts](https://github.com/astashov/liftosaur/blob/master/src/types.ts)), evaluated by its own scripting language. Maximum power, but it means the plan is code. For an agent-driven log the agent *is* the interpreter, so declarative configs beat a DSL.

**Recommended `ProgramSlot` fields:** `exercise_id`, `order`, `superset_group`, `target_sets`, `target_reps_min`, `target_reps_max`, `target_rir` (or `target_rpe`), `target_rest_seconds`, `progression_rule`, `deload_rule`, `equipment`, `weight_rounding`, `notes`.

Progression and deload rule *content* is slice B's problem. This model only needs a stable reference to a rule plus its per-exercise state (e.g. consecutive failures, current training max).

---

## 7. Minimum fields for a fast set entry

The user says "225 by 5" mid-workout. That must be a complete, valid record.

**Required (2):**

| Field | Why nothing else can be required |
|---|---|
| `weight` | Cannot be inferred without guessing intent |
| `reps` | Same |

Even these two collapse further when the plan is known: "done" against a prescribed set is a complete entry, because the plan supplies both.

**Resolved by context, never asked:** `set_id`, `timestamp`, `session_id`, `exercise_instance_id`, `set_index`, `unit`, `set_type`, `is_completed`.

**Offered, never demanded:** `rir`/`rpe`, `notes`, `pain_flag`.

### Carry-forward rules

Ordered by priority. First hit wins.

| Field | Carry-forward source |
|---|---|
| `unit` | Session unit → user default. **Never inferred from magnitude.** 100 is a plausible kg or lb bench |
| `weight` | Previous set, same exercise, same session → prescribed weight → last session's top set |
| `reps` | Prescribed reps → previous set this session |
| `set_type` | `working`, unless the user said "warmup" |
| `equipment` | Previous instance of this exercise → catalog default |
| `machine_setting` | Last recorded value for this exercise, any session |
| `rest_seconds` | Computed from timestamps. Never asked |
| `bodyweight` | Most recent measurement within 14 days, else null |
| `location`/`gym` | Last session |
| `rir`/`rpe` | **Never carried.** A stale RIR is worse than a missing one — it is the field the progression decision reads |

The last row is the important one. Carrying forward a subjective rating manufactures data that the agent will then act on.

---

## 8. Units, time, and identity

### Units

- **Store the unit with the number.** Liftosaur's `IWeight {value: number, unit: IUnit}` is the pattern; wger uses a FK `weight_unit` on every log row. Both refuse a bare number.
- **Do not normalise on write.** Round-tripping 45 lb → 20.41 kg → 45.0 lb accumulates drift and shows the user a number that was never on the bar.
- **Keep bar weight per unit.** Liftosaur's `IEquipmentData.bar: {lb: IWeight, kg: IWeight}` stores both, because a "45 lb bar" and a "20 kg bar" are different bars, not a conversion.
- **Increments come from inventory, not arithmetic.** The next achievable load is `bar + 2 × (some plate subset)`. `IEquipmentData.plates: [{weight, num}]` plus `fixed`/`isFixed` for stacks and fixed dumbbells.
- **Rounding lives on the plan.** wger's `weight_rounding` and `repetition_rounding` on `SlotEntry`.

### Time zones

- Store instants as ISO 8601 **with offset** — Hevy's `start_time`/`end_time`/`created_at`/`updated_at` are all ISO 8601 ([openapi-spec.json](https://github.com/chrisdoc/hevy-mcp/blob/main/openapi-spec.json)).
- Store the **session date separately as a local date**. wger models `date` as a `DateField` with `time_start`/`time_end` as `TimeField`s ([session.py](https://github.com/wger-project/wger/blob/master/wger/manager/models/session.py)) — deliberately not one timestamp. A 11 pm session belongs to that day for weekly-volume purposes regardless of UTC.
- Keep the IANA zone name on the session so a travel week does not scramble the week boundary. **UNVERIFIED** — no surveyed tool does this; it is a recommendation, not observed practice.
- Beware: wger has `unique_together = ('date', 'user', 'routine')` on sessions — one session per routine per day. Do not copy that constraint if two-a-days matter.

### Exercise identity

- **Opaque, stable id.** wger: `uuid`. free-exercise-db: slug matching `^[0-9a-zA-Z_-]+$`. Hevy: `exercise_template_id` string. Never key on the display name.
- **Aliases in their own table**, as wger does with `ExerciseAlias`. This is what lets chat entry resolve "OHP", "military press", "standing press" to one id.
- **Equipment is part of the identity, not an attribute.** Liftosaur's `IExerciseType {id, equipment?}` — "bench press (barbell)" and "bench press (dumbbell)" share a name but not a progression. Strong's export bakes this into the name string: `Snatch (Barbell)` ([sample export](https://github.com/AlexandrosKyriakakis/StrongAppAnalytics/blob/main/Data/strong.csv)).
- **`variation_group`** to relate variants for trend purposes without merging them (wger `Exercise.variation_group`).

---

## 9. Derived metrics

Nothing in this section is stored. All of it is computed, so the formula can change without a migration.

### Estimated 1RM

| Name | Formula | Valid range |
|---|---|---|
| Epley | `1RM = load × (1 + 0.0333 × reps)` | ≤10 reps |
| Brzycki | `1RM = load ÷ (1.0278 − 0.0278 × reps)` | ≤10 reps |

Accuracy figures come from [Thompson et al., PMC9465738](https://pmc.ncbi.nlm.nih.gov/articles/PMC9465738/), which reports Epley within 2.7 kg of a 5RM test and Brzycki within 3.1 kg of a 3RM test (both figures are Thompson quoting DiStasio 2014, not their own measurement).

**Brzycki sign: resolved 2026-09-01. The minus is correct.** Ship
`1RM = load ÷ (1.0278 − 0.0278 × reps)`. Three lines of evidence:

1. **Arithmetic.** At `reps = 1` the denominator must equal 1, so that a 1RM
   set estimates itself. `1.0278 − 0.0278 = 1.0000`. The plus version gives
   `1.0556`, which would predict a 1RM *lower* than a load the lifter just
   pressed once. The plus sign is impossible, not merely unsourced.
2. **A peer-reviewed table prints the minus.** Kemmler et al., a comparison of
   seven RTF prediction models in older adults, gives `1RM = rep weight /
   (1.0278 − (0.0278 × reps))` in its Table 1, citing Brzycki 1993 directly
   ([PMC11435939](https://pmc.ncbi.nlm.nih.gov/articles/PMC11435939/), captured
   in `.kb`; `llmwiki search "Brzycki one rep max equation"`).
3. **The error is confined to one paper.** PMC9465738 is the source that prints
   `1.0278 + 0.0278 × reps`. Its Epley is correct (`1 + 0.0333 × reps`).
   PMC11435939 is the reverse case: its Brzycki is correct but its Epley table
   entry reads `1 + 0.333 × reps`, an order of magnitude off the standard
   0.0333. **Take each formula from the paper that gets it right; neither
   paper is clean on both.**

Brzycki's 1993 original (*JOPERD* 64(1):88-90,
[doi:10.1080/07303084.1993.10606684](https://doi.org/10.1080/07303084.1993.10606684))
is paywalled at Taylor & Francis and was not read. The arithmetic check above
does not need it.

**Validity.** Brzycki's own claim is that the load/reps relation is near-linear at ≤10 reps and exponential above it; a bench-press validation found estimation improved markedly at ≤10 reps (R² = 0.85 vs 0.76) — [Validation of the Brzycki and Epley Equations, OpenSIUC](https://opensiuc.lib.siu.edu/cgi/viewcontent.cgi?article=1744&context=gs_rp) (**UNVERIFIED** — 403 on direct fetch 2026-08-31, figures taken from search-result snippets, not the paper body).

**Practical rules for the agent:**
- Do not compute e1RM above 10 reps. Return null.
- Do not compute e1RM from a set that was not near failure. Both formulas assume reps-to-fatigue. An 8-rep set at RIR 4 is not an 8RM.
- Prefer an **RPE-adjusted** estimate when RIR is recorded: convert to reps-to-failure (`reps + RIR`), then apply the formula. Liftosaur takes exactly this route — its `Weight_getOneRepMax(weight, reps, rpe)` divides by an `rpeMultiplier(reps, rpe)` lookup rather than using Epley at all, defaulting `rpe` to 10 when absent ([src/models/weight.ts](https://github.com/astashov/liftosaur/blob/master/src/models/weight.ts)).
- Liftosaur derives training max as `e1RM × 0.9` (`Weight_getTrainingMax`, same file).

### RPE ↔ RIR

`RPE = 10 − RIR`. RPE 10 is 0 reps in reserve, i.e. failure. From the RIR-based RPE scale in Zourdos et al. 2016 ([J Strength Cond Res](https://journals.lww.com/nsca-jscr/fulltext/2016/01000/novel_resistance_training_specific_rating_of.31.aspx), review application in [NSCA SCJ / PMC4961270](https://pmc.ncbi.nlm.nih.gov/articles/PMC4961270/)). The validation reported strong inverse correlation between bar velocity and RPE in experienced (r = −0.88) and novice (r = −0.77) lifters, and noted the RIR anchoring is more valid than traditional RPE at near-limit loads — which is the regime a progression decision cares about.

Hevy's discretisation is a good precedent for the input widget: `[6, 7, 7.5, 8, 8.5, 9, 9.5, 10]` ([openapi-spec.json](https://github.com/chrisdoc/hevy-mcp/blob/main/openapi-spec.json)). Half-points only above 7, because nobody can tell RPE 6 from 6.5.

### Volume

| Metric | Formula | Notes |
|---|---|---|
| Tonnage (volume load) | `Σ weight × reps` over working sets | Excludes warmups. Unit-sensitive: pick one unit before summing |
| Hard sets | count of working sets at RIR ≤ ~3 | The unit the literature uses |
| Sets per muscle per week | `Σ` over sets, `1.0` for each primary muscle, `0.5` for each secondary | **Sourced 2026-09-01**, was tagged UNVERIFIED. This is Pelland et al.'s 'fractional' quantification, which beat both 1.0 and 0.0 weighting of indirect sets on relative evidence and was used for their primary meta-regression models ([PMID 41343037](https://pubmed.ncbi.nlm.nih.gov/41343037/), see `03-progression-heuristics.md` "Volume evidence base"). Liftosaur has an `IMuscleMultiplier` interface in types.ts, implying it does something similar |
| Weekly volume benchmark | ~10+ sets per muscle per week | [Schoenfeld, Ogborn & Krieger 2017, J Sports Sci](https://pubmed.ncbi.nlm.nih.gov/27433992/): graded dose-response, each additional weekly set ≈ +0.37% gain; 10+ weekly sets was the best-performing category (categorical trend P = 0.074, continuous effect P = 0.002) |

### PRs and trend

Track at least four PR kinds, per exercise + equipment:
- heaviest weight at any reps
- heaviest weight at a given rep count (a rep-max table)
- best e1RM
- best single-set tonnage

Trend for the raise/lower decision: rolling e1RM (or top-set load at matched RIR) over the last N sessions of that exercise, plus a per-exercise stall counter (consecutive sessions failing the target). wger's `iteration` field is the natural counter for this.

### Cardio / conditioning (brief)

Fields: `distance {value, unit}`, `duration_seconds`, `avg_hr`, `max_hr`, `avg_pace` (derived: duration ÷ distance), `elevation`, `perceived_effort`. Hevy already reserves `distance_meters` and `duration_seconds` on every set, and a `custom_metric` "currently used for steps and floors" ([openapi-spec.json](https://github.com/chrisdoc/hevy-mcp/blob/main/openapi-spec.json)). FitNotes has a per-exercise `Kind` column of letters — `w` weight, `r` reps, `d` distance, `t` time, combinable as `wr` — which declares which fields a given exercise uses ([FitNotes iOS docs](https://www.getfitnotes.com/docs/migrate-from-other-apps.html)). That `Kind` idea is worth copying: one catalog field says which set fields are meaningful, so the logger knows what to ask for.

### Mobility (brief)

Model as sets with `duration_seconds` and no weight. Optional `rom_notes` free text. Do not count toward volume. Not worth its own entity.

---

## 10. Real-world schema comparison

Verified 2026-08-31.

| Concern | Strong (CSV) | Hevy (API v1) | FitNotes (CSV) | Liftosaur (TS) | wger (Django) | free-exercise-db | **Proposed** |
|---|---|---|---|---|---|---|---|
| Grain | one row per set | nested JSON | one row per set | nested objects | one row per set | catalog only | nested + flat CSV view |
| Weight | `Weight` (bare) | `weight_kg` only | `Weight (kg)` **and** `Weight (lbs)` | `IWeight {value, unit}` | `weight` + `weight_unit` FK | — | `{value, unit}` |
| Unit handling | implicit | kg canonical | both columns | per-value | per-row FK | — | per-value, no conversion on write |
| Reps | `Reps` | `reps` | `Reps` | `reps` / `completedReps` | `repetitions` + `repetitions_unit` | — | `reps` (+ per-side) |
| RPE / RIR | `RPE` col | `rpe` (enum 6–10) | none | `rpe`, `logRpe`, `completedRpe` | `rir` + `rir_target` | — | both, `RPE = 10 − RIR` |
| Set type | none | `warmup\|normal\|failure\|dropset` | none | `isAmrap`, `label`, warmups separate array | — | — | enum + `is_amrap` + `to_failure` |
| Planned vs actual | none | routines vs workouts | none | `reps` vs `completedReps` on same object | `*_target` beside actual | — | both on the row |
| Rest | none | routine `rest_seconds` | none | `timer`, `setTimer` | `rest` + `rest_target` | — | measured from timestamps |
| Superset | none | `supersets_id` | none | `IHistoryEntry.superset` | `Slot` groups entries | — | `superset_group` |
| Bar / plate math | none | none | none | **`IEquipmentData`: bar per unit, multiplier, plates, fixed, isFixed, useBodyweightForBar, isAssisting** | rounding fields only | — | copy Liftosaur |
| Bodyweight / added load | none | separate measurements endpoint | separate body-tracker export | `useBodyweightForBar` | — | — | `load` object on the set |
| Unilateral | none | none | none | `isUnilateral`, `completedRepsLeft` | — | — | per-side reps + `side` |
| Exercise id | name string incl. equipment | `exercise_template_id` | name + `Category` | `{id, equipment}` | `uuid` | slug `^[0-9a-zA-Z_-]+$` | opaque id + equipment |
| Aliases | no | no | no | no | **`ExerciseAlias` model** | no | yes, required for chat |
| Muscles | no | primary + secondary groups | `Category` only | `IMuscle`, `IBodyPart`, `IMuscleMultiplier` | `muscles` + `muscles_secondary` M2M | 17-value primary + secondary | primary + secondary, fractional |
| Session subjective | `Workout Notes` | `description` | `Notes` | — | `impression` (bad/neutral/good) + `notes` | — | readiness 1–5 + notes |
| Session timing | `Date` + `Duration` string | ISO `start_time`/`end_time` | `Date` (YYYY-mm-dd) | `startTime`/`endTime` epoch | `date` + `time_start`/`time_end` | — | local date + ISO instants + tz |
| Program model | none in export | Routine → exercises → sets, `rep_range` | none | expression DSL (`repsExpr`, `weightExpr`…) | Routine→Day→Slot→SlotEntry + per-field iteration configs | — | wger shape, declarative |
| Progression rules | none | none | none | Liftoscript | 10 config models | — | rule ref + per-exercise state |
| Pain flag | none | none | none | none | none | none | **`none\|niggle\|stop`** |

Column sources: Strong header row `Date,Workout Name,Duration,Exercise Name,Set Order,Weight,Reps,Distance,Seconds,Notes,Workout Notes,RPE` from a [real export in a public repo](https://github.com/AlexandrosKyriakakis/StrongAppAnalytics/blob/main/Data/strong.csv) (Strong's own [help page](https://help.strongapp.io/article/235-export-workout-data) confirms CSV export exists but does not list columns). FitNotes headers from [FitNotes iOS migration docs](https://www.getfitnotes.com/docs/migrate-from-other-apps.html). Hevy from the [OpenAPI spec](https://github.com/chrisdoc/hevy-mcp/blob/main/openapi-spec.json) — note Hevy's own [docs endpoint](https://api.hevyapp.com/docs/) served a default Swagger UI pointing at the petstore sample on 2026-08-31, so the spec was taken from a third-party mirror. **Partially UNVERIFIED against first-party Hevy source.**

**What no one has:** pain flags, machine settings, band tension, named unilateral sides, readiness. Those are the additions this model makes, and each should earn its place or be cut.

---

## 11. Proposed layout

Storage-agnostic model, three concrete renderings.

### Session file — `sessions/2026-08-31-push-a.md`

Markdown with YAML front matter. Human-editable, git-diffable, agent-parseable.

```markdown
---
id: 2026-08-31T17-42-lower-a
date: 2026-08-31
tz: America/Chicago
start: 2026-08-31T17:42:00-05:00
end:   2026-08-31T18:51:00-05:00
program: gzclp-v2
day: lower-a
iteration: 14
bodyweight: { value: 78.4, unit: kg }
gym: home
readiness: 4
notes: slept badly, still fine
---

## Squat (Barbell) [squat_barbell / barbell]

| set | type    | weight | unit | reps | rir | rest | flags     | note |
|-----|---------|--------|------|------|-----|------|-----------|------|
| 1   | warmup  | 60     | kg   | 5    |     |      |           |      |
| 2   | warmup  | 90     | kg   | 3    |     |      |           |      |
| 3   | working | 110    | kg   | 5    | 2   | 180  |           |      |
| 4   | working | 110    | kg   | 5    | 1   | 195  |           |      |
| 5   | working | 110    | kg   | 6    | 0   | 210  | amrap     | grinder |

## Romanian Deadlift (Barbell) [rdl_barbell / barbell] (superset: A)

| set | type    | weight | unit | reps | rir | rest | flags | note |
|-----|---------|--------|------|------|-----|------|-------|------|
| 1   | working | 80     | kg   | 10   | 3   | 90   |       |      |
| 2   | working | 80     | kg   | 10   | 2   | 90   | pain:niggle | left hamstring |
```

The header carries `[exercise_id / equipment]` so a rename in the display name never breaks the join. Blank cells mean "not recorded", not zero.

### Flat CSV view — `derived/sets.csv`

Generated from the session files, one row per set. This is what analysis reads.

```csv
session_id,date,tz,program,day,iteration,order,exercise_id,equipment,superset,set_index,set_type,is_amrap,weight,unit,bar_weight,added_weight,assist_weight,reps,reps_left,reps_right,side,rir,rpe,rest_s,duration_s,distance,distance_unit,pain,notes
2026-08-31T17-42-lower-a,2026-08-31,America/Chicago,gzclp-v2,lower-a,14,1,squat_barbell,barbell,,3,working,false,110,kg,20,,,5,,,both,2,8,180,,,,none,
2026-08-31T17-42-lower-a,2026-08-31,America/Chicago,gzclp-v2,lower-a,14,1,squat_barbell,barbell,,5,working,true,110,kg,20,,,6,,,both,0,10,210,,,,none,grinder
```

### Exercise catalog entry — `catalog/exercises.json`

```json
{
  "id": "squat_barbell",
  "name": "Squat (Barbell)",
  "aliases": ["squat", "back squat", "bb squat", "high bar squat"],
  "variation_group": "squat",
  "primary_muscles": ["quadriceps"],
  "secondary_muscles": ["glutes", "hamstrings", "lower back", "abdominals"],
  "movement_pattern": "squat",
  "mechanic": "compound",
  "equipment": ["barbell"],
  "is_unilateral": false,
  "tracks": ["weight", "reps"],
  "equipment_profiles": {
    "barbell": {
      "bar": { "kg": 20, "lb": 45 },
      "multiplier": 1,
      "plates": [
        { "weight": { "value": 20, "unit": "kg" }, "num": 4 },
        { "weight": { "value": 10, "unit": "kg" }, "num": 2 },
        { "weight": { "value": 5,  "unit": "kg" }, "num": 2 },
        { "weight": { "value": 2.5,"unit": "kg" }, "num": 2 },
        { "weight": { "value": 1.25,"unit":"kg" }, "num": 2 }
      ],
      "is_fixed": false,
      "is_assisting": false,
      "bodyweight_counts": false,
      "min_increment": { "value": 2.5, "unit": "kg" }
    }
  },
  "default_progression": "double-progression-5-8"
}
```

`tracks` is the FitNotes `Kind` idea: it tells the logger which fields to ask for.

### Routine — `programs/gzclp-v2.yaml`

```yaml
id: gzclp-v2
name: GZCLP v2
start: 2026-06-01
days:
  - id: lower-a
    order: 1
    name: Lower A
    slots:
      - order: 1
        entries:
          - exercise_id: squat_barbell
            equipment: barbell
            target_sets: 3
            target_reps_min: 5
            target_reps_max: 5
            last_set_amrap: true
            target_rir: 1
            target_rest_s: 180
            weight_rounding: { value: 2.5, unit: kg }
            progression_rule: linear-add-5kg-on-success
            deload_rule: drop-10pct-after-2-stalls
      - order: 2
        superset_group: A
        entries:
          - exercise_id: rdl_barbell
            target_sets: 3
            target_reps_min: 8
            target_reps_max: 12
            target_rir: 2
            target_rest_s: 90
            progression_rule: double-progression-8-12
```

**Notion mapping**, if that route is taken: one database per entity. `Sets` is the big one, with relations to `Sessions`, `Exercises`, and `ProgramSlots`. Notion's relation + rollup gives sets-per-muscle-per-week without code, but 3000+ set rows a year makes the API the bottleneck for anything analytical. Git + files keeps the derived layer cheap. **Cross-reference: slice D (existing tools) should settle this.**

---

## 12. Open questions for the user

Recorded, not asked — this is a delegated research file with no channel back.

1. **kg or lb, and is the gym ever mixed?** Determines whether dual-unit storage is real complexity or theatre.
2. **RIR or RPE — which do you actually say out loud?** Store both, but the prompt should ask for one. Asking for both trains you to skip both.
3. **Is a readiness/sleep/energy block something you'd fill in, or aspirational?** Recommendation is one 1–5 number. Say if even that is too much.
4. **Do you train unilaterally often enough to justify per-side reps on every row?** It widens the schema for a minority of exercises.
5. **Home gym, commercial gym, or both?** Plate inventory is per-location, and the min-increment logic falls apart without it.
6. **Two-a-days ever?** Changes whether `(date, program)` can be a session key.
7. **Do you want the agent to auto-log rest from timestamps**, or is a set logged 20 minutes late going to poison that?
8. **Notion or git?** Affects nothing in the model but everything in the derived layer.
9. **Migrating existing history in?** If it is a Strong or Hevy export, the import shape is settled; if it is paper, it is not.
10. ~~Verify the Brzycki sign (§9) before it ships in any calculator.~~
    **Closed 2026-09-01.** The minus is correct; see §9. Nothing left to decide.

---

## Verification notes

Fetched and read directly on 2026-08-31:
- [wger manager models](https://github.com/wger-project/wger/tree/master/wger/manager/models) — `log.py`, `session.py`, `slot_entry.py`, `routine.py`, `day.py`, and the ten config models. Field lists read from source.
- [wger exercises models](https://github.com/wger-project/wger/tree/master/wger/exercises/models) — `base.py` field list, `exercise_alias.py` existence.
- [Liftosaur `src/types.ts`](https://github.com/astashov/liftosaur/blob/master/src/types.ts) — 2015 lines; `ISet`, `IHistoryEntry`, `IHistoryRecord`, `IProgramSet`, `IExerciseType`, `IWeight`, `IPlate`, `IEquipmentData` read verbatim.
- [Liftosaur `src/models/weight.ts`](https://github.com/astashov/liftosaur/blob/master/src/models/weight.ts) — `getOneRepMax`, `getTrainingMax`, `platesWeight`.
- [free-exercise-db `schema.json`](https://github.com/yuhonas/free-exercise-db/blob/main/schema.json) — full property list and enums.
- [Hevy OpenAPI spec](https://github.com/chrisdoc/hevy-mcp/blob/main/openapi-spec.json) — all component schemas enumerated.
- [Strong sample export](https://github.com/AlexandrosKyriakakis/StrongAppAnalytics/blob/main/Data/strong.csv) — header row read directly.
- [FitNotes iOS migration docs](https://www.getfitnotes.com/docs/migrate-from-other-apps.html) — column list and formats.

Could not verify first-party on 2026-08-31:
- **Hevy** — [api.hevyapp.com/docs/](https://api.hevyapp.com/docs/) served a stock Swagger UI configured against the petstore sample spec. Schema taken from a third-party mirror.
- **ExerciseDB** — `exercisedb.dev` TLS certificate expired. No fields cited from it.
- **Strong** — [official help article](https://help.strongapp.io/article/235-export-workout-data) confirms CSV export but lists no columns. Columns taken from a real export file.
- **Brzycki/Epley validation ranges** — [OpenSIUC paper](https://opensiuc.lib.siu.edu/cgi/viewcontent.cgi?article=1744&context=gs_rp) returned 403 again on 2026-09-01. Still **UNVERIFIED**: the R² figures are from search snippets, not the paper body. The paper is real — it is DiStasio's 2014 SIU master's research paper, "Validation of the Brzycki and Epley Equations for the 1 Repetition Maximum Back Squat Test in Division I College Football Players", cited by name in PMC9465738's reference list. Only the numbers are unconfirmed, not the paper's existence.
- **Brzycki 1993 original** — *JOPERD* 64(1):88-90, paywalled at Taylor & Francis. The formula's sign is settled by arithmetic and by a second peer-reviewed table (§9), not by reading it.
- ~~**Fractional (0.5) secondary-muscle volume counting** — convention, no cited source.~~ **Closed 2026-09-01.** Pelland et al. 2026 tested exactly this weighting and it won on relative evidence ([PMID 41343037](https://pubmed.ncbi.nlm.nih.gov/41343037/)).
- **Tempo, pain flag, machine setting, band, per-session timezone, readiness fields** — no surveyed tool models these. Proposals, not observed practice.
