# Existing tools, exercise databases, and formats

Research slice D. Dated **2026-08-31**. Star counts and last-commit dates in the main tables were checked on that date via the GitHub REST API. Anything not checked is tagged **UNVERIFIED**.

Scope: what an agent-driven personal workout log can **reuse instead of build**. Other slices cover the data model, progression rules, routines/UX, and trainer-agent behaviour.

---

## TL;DR — the three things to steal

1. **free-exercise-db for the exercise list.** 876 exercises, JSON, images, released under the Unlicense (public domain). No attribution, no share-alike, no API key, no server. A friend clones one repo and is done. <https://github.com/yuhonas/free-exercise-db>
2. **Liftosaur's Liftoscript DSL as the shape of a program file.** One readable line per exercise carries sets, reps, weight/percentage/RPE, and the progression rule. It is compact enough for an LLM to write and read reliably. Imitate the grammar; do not depend on the app. <https://www.liftosaur.com/doc/liftoscript>
3. **wger's Routine → Day → Slot → SlotEntry model as the schema.** The extra "slot" layer is what makes supersets representable without hacks. Crib the schema even if you never run their Django stack. <https://wger.readthedocs.io/en/latest/api/routines.html>

Two things worth knowing before you write any MCP code:

- **`chrisdoc/hevy-mcp` already exists** — MIT, 448 stars, pushed 2026-08-31. The best available reference for what a workout-logging MCP tool surface looks like. <https://github.com/chrisdoc/hevy-mcp>
- **wger ships an official MCP server** — <https://github.com/wger-project/mcp-server>, maintained by the wger org. It is the only official MCP server for a self-hostable FLOSS workout backend, which makes "just run wger" a real contender rather than a fallback.

**Replicability scores below are my judgment, not a cited fact.** 5 = a friend runs one command or clones one repo. 1 = paid account plus manual export.

---

## Master table

### Commercial apps

| Name | URL | License / OSS | Price | Export | Import | API | Self-host | Friend score | What to steal | Red flags |
|---|---|---|---|---|---|---|---|---|---|---|
| Hevy | [hevy.com](https://hevy.com) | Closed | Free tier (4 routines, 7 custom exercises, 3mo graph history cap) + Hevy Pro ($2.99/mo, $23.99/yr, $74.99 lifetime) | **CSV, columns verified** (see below) | Yes — has a documented Strong-CSV importer ([help](https://help.hevyapp.com/hc/en-us/articles/38001424401943-How-to-Import-Strong-App-CSV-Files-and-Export-Your-Data-in-Hevy)) | **Yes, but Pro-gated.** Key at `hevy.com/settings?developer`, `api-key` header, docs at <https://api.hevyapp.com/docs/> | No | 2 | The CSV column set is the closest thing to a community lingua franca; the MCP server already exists; `exercise_title` + `superset_id` + `set_type` pattern (Appendix A) | API requires a paid subscription; Swagger page is JS-rendered so I could not read endpoint details directly (**UNVERIFIED**: rate limits) |
| Strong | [strongapp.io](https://www.strongapp.io) | Closed | Free tier + Strong Pro (~$4.99/mo, ~$29.99/yr, region-dependent) | CSV. Official help: "You can export your workout data to a spreadsheet friendly CSV format" ([help](https://help.strongapp.io/article/235-export-workout-data)) | **No** — same page: "Exported files cannot be imported back into Strong" | None found — no official public API. Reverse-engineered clients exist ([tolik518/strong-api-workout-sync](https://github.com/tolik518/strong-api-workout-sync)); community warns of "legal implications" of using it (Appendix A) | No | 2 | Its CSV is the de facto migration source everyone else writes importers for; one row per set with `RPE` and `Workout Notes` columns | One-way export; vendor appears hostile to a public API. **UNVERIFIED**: whether export needs Pro — the help page does not say |
| FitNotes | [fitnotesapp.com](https://www.fitnotesapp.com/) | **Closed — confirmed NOT open source.** Package name `com.github.jamesgay.fitnotes` looks like an OSS repo path but no license or source repo was found (Appendix A) | Free — "Free to use and no ads - ever!" (site). "FitNotes Supporter" IAP unlocks extra exercise types | **CSV export, free** (Appendix A) | **Yes** — imports CSV from Strong, Fitbod, IronGAINS, HeavySet, Hevy, Liftin, and WeightFit via a fixed header schema ([migration docs](https://www.getfitnotes.com/docs/migrate-from-other-apps.html)) | None found | No | 3 | Long-standing free Android logger; its fixed CSV header is a de facto import target other converters already emit (Appendix A) | Documentation is thin; Android only; misleading package name implies OSS but is not |
| Liftosaur | [liftosaur.com](https://www.liftosaur.com) | Client is **AGPL-3.0** ([repo](https://github.com/astashov/liftosaur), 690★, pushed 2026-08-31). Server open-source status **UNVERIFIED** — not proven the backend runs the same license | Free tier functional (built-in programs, logging, offline, Liftoscript editor); Premium adds cloud sync, advanced analytics | Export mechanism implied by reviews, **UNVERIFIED** (gating signals conflict, Appendix A) | **UNVERIFIED** | **REST API exists, Pro-gated.** Docs at <https://www.liftosaur.com/doc/api>, Bearer `lftsk_...` key, 403 without premium. Endpoints: programs, workout history, live workout, gyms/equipment, exercise-data, measurements. Rate limits not documented (corrects the prior "no public API" claim in this table) | **No** — Docker support is an [open unresolved request](https://github.com/astashov/liftosaur/issues/158) | 3 | **The DSL and the 60+ program library**; Liftoscript `/playground` simulate-before-save; idempotent set-logging pattern | Not self-hostable; API paywalled despite AGPL client and server OSS status unproven |
| Boostcamp | [boostcamp.app](https://www.boostcamp.app) | Closed (presumed — no evidence of OSS) | Free: full 11,000+ program library, tracking, no ads. Pro: Strength Score, muscle heatmap, coach programs. **UNVERIFIED** exact price — secondary sources say ~$59.99/yr or $14.99/mo, not corroborated on a primary page | No native export. A third-party Chrome extension scrapes `/history` JSON to CSV; full column list **UNVERIFIED** (Appendix A) | None found | No official API. Reverse-engineered via `boostcamp-api` (email/password login), which powers [Alex-Keyes/boostcamp-mcp](https://github.com/Alex-Keyes/boostcamp-mcp), 7★, pushed 2026-04-06. No docs, rate limits **UNVERIFIED** | No | 2 | The MCP server is the closest precedent for this project's own tool surface; free tier gives the full program library, paywall is on analytics only | Zero official export/API; reverse-engineered API's ToS status not checked (Appendix A) |
| Fitbod | [fitbod.me](https://fitbod.me) | Closed | Free: 3 workouts + tracking. Premium ~$15.99/mo or $95.99/yr (secondary source, price may be stale) | **CSV export confirmed** — Settings → "Export Workout Data". Columns verified (Appendix A). Free-vs-paid gating of export **UNVERIFIED** | No CSV import; Apple Health workout sync only | No official public API found; a third-party "Akousa" OAuth2 listing is **UNVERIFIED** and looks like an unofficial aggregator, not primary | No | 2 | `isWarmup` + `multiplier` fields encode warm-up/superset/drop-set state; separates Distance/Incline/Resistance from Weight/Reps; adaptive per-workout generation overlaps with what a trainer agent should do | Export paywall status unclear; closed source |
| JEFIT | [jefit.com](https://www.jefit.com) | Closed | Free: 1,400+ exercise library, unlimited logging. Elite $12.99/mo or $69.99/yr | Official export page unreachable (SSL error). Secondary sources: export is an encrypted `.bak` SQLite file needing manual decrypt/convert — no clean native CSV (Appendix A) | **UNVERIFIED** | Unofficial only: [denolfe/jefit](https://github.com/denolfe/jefit), reverse-engineered, needs public userId + profile visibility "Everyone". No official docs | No | 1 | Per-set weight/reps/duration with calculated 1RM per set; native smartwatch logging | Worst export story in the survey (encrypted SQLite `.bak`); closed source |
| Alpha Progression | [alphaprogression.com](https://alphaprogression.com) | Closed (presumed — no evidence found either way) | Free: full logging, 795 exercises w/ video, body measurements. Pro $12.99/mo or $79.99/yr (14-day trial): plan generator, progression recs, periodization/RIR/deload | Official FAQ confirms CSV export exists ("raw numbers" from analytics). Column names and free-vs-paid gating **UNVERIFIED** | **UNVERIFIED** | None found | No | 1 | Periodization/deload/RIR as first-class fields in the plan generator; multiple gym profiles (equipment per gym) | Least-documented app in the survey for programmatic reuse |
| Juggernaut AI | [juggernautai.app](https://www.juggernautai.app) | Closed | Subscription | None found | — | None found | No | 1 | RPE/velocity-driven autoregulation as a concept | Closed, expensive, no export path found |
| RP Hypertrophy | [rpstrength.com](https://rpstrength.com) | Closed | Subscription | None found | — | None found | No | 1 | Its set-progression and soreness-feedback loop is the reference implementation of that idea | Closed; content is the product |
| Gravitus | [gravitus.com](https://gravitus.com) | Closed | Freemium | None found | — | None found | No | 1 | — | Social-first; no export found |
| Setgraph | [setgraph.app](https://setgraph.app) | Closed | Freemium | **CSV export exists** | UNVERIFIED | None found | No | 2 | Charting approach | Column names not recovered |
| GymBook | [gymbookapp.com](https://www.gymbookapp.com/) | Closed — only a defunct translation-strings repo found ([sallvi/localize-gymbook](https://github.com/sallvi/localize-gymbook)), no evidence of OSS code | Free core (unlimited, no ads); Pro $1.99/mo, $8.99/yr, $22.99 lifetime (fetched 2026-08-31) | **CSV + XML + DB backup, Pro-only** | Yes — DB backup restore on another device ([App Store listing](https://apps.apple.com/us/app/gymbook-strength-training/id650113307)) | None found | No | 2 | DB-file backup+restore as a full-state round-trip primitive — worth copying even without a text format | Export is Pro-gated; no API |
| Simple Workout Log | [simpleworkoutlog.com](https://www.simpleworkoutlog.com) | Proprietary; a community helper script is MIT-style ([treischl/sl5x5-to-workoutlog](https://github.com/treischl/sl5x5-to-workoutlog)) | Free tier + low-cost Premium; exact price **UNVERIFIED** | CSV/Excel export via a "Tools" tab; gating **UNVERIFIED**, column names NOT FOUND | Local SQLite backup file `workoutlog.bak`; a community script writes into that DB directly | None found | No | 2 | The name is the design brief: what a minimal log looks like. The real interchange format is the raw `workoutlog.bak` SQLite file, not the CSV | No documented CSV columns; pricing unconfirmed |
| Progression | [progressionapp.com](https://progressionapp.com) | NOT FOUND — presumed closed | Free unlimited logging; Pro IAP price NOT FOUND | CSV export claimed by listicles; official confirmation NOT FOUND | NOT FOUND | NOT FOUND | No | 1 | Coach/client split model | Developer identity **UNVERIFIED** — the Play Store package `workout.progression.lite` is attributed to Zoltan Demant, not the "Rade Stanojevic" this survey originally assumed; least-documented app surveyed |
| Stacked | [stackedapp.co](https://stackedapp.co) | NOT FOUND | "100% FREE" per App Store listing | NOT FOUND | NOT FOUND | NOT FOUND | No | 1 | — | iOS app last updated 2022-06-07, likely dead. A Legion Athletics product page links the same App Store ID under a different developer name (**UNVERIFIED**); a separate Android listing is unresolved |

### Open-source projects

| Name | URL | License | Stars (2026-08-31) | Last commit | Self-host | Friend score | What to steal | Red flags |
|---|---|---|---|---|---|---|---|---|
| **wger** | [github.com/wger-project/wger](https://github.com/wger-project/wger) | AGPL-3.0 | 6,809 | 2026-08-28 | Yes, docker-compose ([image](https://hub.docker.com/r/wger/server)) | 4 | **Routine → Day → Slot → SlotEntry schema** ([docs](https://wger.readthedocs.io/en/latest/api/routines.html)); read API needs no auth key | Django/DRF is heavy for a personal tool; AGPL if you fork; exercise data is separately CC-licensed per entry |
| **workout-cool** | [github.com/Snouzy/workout-cool](https://github.com/Snouzy/workout-cool) | **MIT** | 8,433 | 2026-07-31 | Yes, Docker ([self-hosting doc](https://github.com/Snouzy/workout-cool/blob/main/docs/SELF-HOSTING.md)) | 4 | Most-starred, and MIT means no copyleft friction if you lift code. Next.js + Prisma, close to MCP-server tooling | Exercise DB's own license not stated inline (**UNVERIFIED**) |
| **Liftosaur** | [github.com/astashov/liftosaur](https://github.com/astashov/liftosaur) | AGPL-3.0 | 690 | 2026-08-31 | No | 2 | Liftoscript grammar; [60+ program library](https://www.liftosaur.com/programs) incl. [GZCLP](https://www.liftosaur.com/programs/gzclp), 5/3/1 variants, PPL, Strong Curves | Not self-hostable; no bulk export API; check per-program licensing before copying programs verbatim |
| **LiftLog** | [github.com/LiamMorrow/LiftLog](https://github.com/LiamMorrow/LiftLog) | AGPL-3.0 | 553 | 2026-08-30 | Client-only, optional backup server | 3 | End-to-end-encrypted optional sync — the right pattern if multi-device sync ever matters | Sync mechanics are **UNVERIFIED** (search-summarised, not read from the in-repo docs) |
| jovandeginste/workout-tracker | [repo](https://github.com/jovandeginste/workout-tracker) | NOASSERTION | 1,249 | 2026-08-18 | Yes | 4 | — | GPX/running-focused, not strength |
| granite | [github.com/MorrisMorrison/granite](https://github.com/MorrisMorrison/granite) | AGPL-3.0 | 4 | 2026-08-31 | Yes — self-describes as "open-source, self-hostable, offline-first workout tracker" | 3 | Closest stated match to the brief, but tiny | 4 stars; effectively one person's project |
| wingfit | [repo](https://github.com/itskovacs/wingfit) | NOASSERTION | 521 | **2025-08-11 (stale >1yr)** | Yes | 2 | — | Unmaintained; no SPDX license detected |
| Flexify | [repo](https://github.com/brandonp2412/Flexify) | MIT | 422 | 2026-09-01 | Mobile app | 3 | — | No server component |
| MyFit | [repo](https://github.com/WhyAsh5114/MyFit) | AGPL-3.0 | 139 | 2026-08-29 | Yes | 3 | Hypertrophy-oriented progression logic | Small project |
| LibreFit | [repo](https://github.com/LibreFitOrg/LibreFit) | GPL-3.0 | 208 | 2026-07-27 | Yes | 3 | — | Small |
| Iron | [repo](https://github.com/karimknaebel/Iron) | GPL-3.0 | 229 | **2024-11-17 (stale)** | — | 1 | — | Abandoned |
| OpenLifter | [gitlab.com/openpowerlifting/openlifter](https://gitlab.com/openpowerlifting/openlifter) | UNVERIFIED | 22 (GitLab) | 2026-07-18 | Yes | — | **Nothing — skip.** It is meet-day competition scoring, not a training log | Irrelevant to this project |

**Note on searching:** a GitHub search for "gym tracker" is useless — it returns reinforcement-learning `Gym` environment repos. The `workout-tracker` **topic** is the clean query.

### Plain-text ecosystems

| Name | What people actually do | Steal | Cite |
|---|---|---|---|
| Obsidian | No dominant plugin. The common pattern is Dataview inline fields in daily notes (`Workout:: 30m`). One purpose-built plugin exists: Gym Workout Tracker | The inline-field convention, e.g. `Exercise:: Bench / 3x8 / 135lb` — a lightweight text format an agent can read and write | [plugin](https://community.obsidian.md/plugins/gym-workout-tracker), [pattern writeup](https://www.i-josh.com/posts/obsidian-workout-log/) |
| Logseq | Weaker. No purpose-built tracker; people repurpose habit trackers or use a property-block per exercise (Type/Name/Sets/Reps/Weight/Difficulty) | Block-property-per-set as a plain-text convention — same idea as Obsidian's | [community template](https://discuss.logseq.com/t/example-creating-an-exercise-plan/9232), [writeup](https://perrotta.dev/2025/06/logseq-template-for-working-out/) |

Neither beats wger's schema or Liftoscript as reuse material. Their contribution is a convention, not code.

---

## Verified CSV shapes

These are the two formats worth being compatible with, because every third-party tool parses one of them.

**Hevy** — exact header, copied from a committed sample file:

```
"title","start_time","end_time","description","exercise_title","superset_id","exercise_notes","set_index","set_type","weight_kg","reps","distance_km","duration_seconds","rpe"
```

Sample row: `"Morning workout","22 Dec 2025, 08:00","22 Dec 2025, 08:37","","Pull Up (Assisted)",,"",0,"normal",21,10,,0,8.5`

Source: <https://github.com/matanabudy/workout-data-sync/blob/main/examples/hevy_export_sample.csv>

Worth noting what this shape implies: **one row per set**, fully denormalised, workout metadata repeated on every row. `superset_id` is how supersets survive the flattening. `set_type` distinguishes warmup from working sets.

**Strong** — columns reported as: `Date, Workout Name, Duration, Exercise Name, Set Order, Weight, Reps, Distance, Seconds, Notes, Workout Notes, RPE`. Same one-row-per-set shape. **UNVERIFIED** — this came from search results summarising parser repos, not from a header line I read myself. Verify against a real export before writing an importer. Parsers to check: [StrongAppAnalytics](https://github.com/AlexandrosKyriakakis/StrongAppAnalytics), [strong-statistics](https://github.com/DaKheera47/strong-statistics).

---

## Liftoscript — the syntax worth copying

Liftosaur's program DSL puts sets, reps, intensity, and the progression rule on **one line per exercise**. That is the property that matters here: it is dense enough for a human to read at a glance and regular enough for an agent to generate without drifting.

```
"Bench Press / 3x8"
"Bench Press / 3x8-12"
"Bench Press / 1x5, 1x3, 1x1, 5x5"
"Bench Press / 3x12 @8"          // RPE
"Bench Press / 3x12 80%"         // percentage of training max
"Bench Press / 3x12 60kg"        // absolute load

// built-in progression rules
"Bench Press / 3x8 / progress: lp(5lb)"            // linear progression
"Bench Press / 3x8 / progress: dp(5lb, 8, 12)"     // double progression
"Bench Press / 3x10+ / progress: sum(30, 5lb)"     // total-reps target

// custom progression — arbitrary logic
"Bench Press / 3x8 / progress: custom() {~
  if (completedReps[1] >= reps[1]) {
    weights += 5lb
  }
~}"
```

Source: <https://www.liftosaur.com/doc/liftoscript> and <https://github.com/astashov/liftosaur/blob/master/docs/content/liftoscript.md>

**Caveat:** these snippets were transcribed from the docs by a delegated researcher, not read by me directly. Re-check the exact grammar against the docs page before implementing a parser.

The design lessons, independent of the exact syntax:

- **Intensity is polymorphic in one slot** — `@8` (RPE), `80%` (percentage), `60kg` (absolute) all occupy the same position. Your data model needs one intensity field with a tagged type, not three columns.
- **The progression rule lives with the exercise**, not in a separate table. That is why an agent can read one line and know what to do next week.
- **Named rules with an escape hatch.** `lp()`, `dp()`, `sum()` cover the common cases; `custom() {~ ~}` covers everything else. Copy that shape — a small vocabulary of named progressions plus an escape hatch beats either a rigid enum or a general-purpose scripting language.
- Note the state it assumes: `completedReps[]` and `reps[]` indexed per set, and a mutable `weights`. That tells you what the log must hand the progression engine.

Licensing: Liftosaur is AGPL-3.0. The **grammar as an idea** is not copyrightable, so writing your own parser is clean. Copying their program library verbatim is a different question — check per-program attribution on <https://www.liftosaur.com/programs> first.

---

## Exercise database recommendation

**Use `free-exercise-db`.** <https://github.com/yuhonas/free-exercise-db>

**License check:** The Unlicense — a public domain dedication. Confirmed two ways: the [LICENSE.md](https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/LICENSE.md) file, and the `license.spdx_id` field of <https://api.github.com/repos/yuhonas/free-exercise-db> returning `unlicense`. That means **no attribution requirement, no share-alike, no redistribution restriction**. You can vendor the whole file into a public repo and a friend can clone it without inheriting any obligation.

876 exercises. 1,821 stars, pushed 2026-08-30. Field names, read from the real `dist/exercises.json`:

```json
{
  "name": "3/4 Sit-Up",
  "force": "pull",
  "level": "beginner",
  "mechanic": "compound",
  "equipment": "body only",
  "primaryMuscles": ["abdominals"],
  "secondaryMuscles": [],
  "instructions": ["Lie down on the floor and secure your feet. ..."],
  "category": "strength",
  "images": ["3_4_Sit-Up/0.jpg", "3_4_Sit-Up/1.jpg"],
  "id": "3_4_Sit-Up"
}
```

Source: <https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json>

The `id` is a stable slug. That matters — it is your join key between the exercise catalogue and the log, and it survives renames better than a display name.

**The alternatives, and why they lose:**

| DB | License | Verdict |
|---|---|---|
| wger exercise DB | App is AGPL-3.0; **the data is licensed per-exercise**, chosen from CC-BY-SA 3.0, CC-BY 4.0, CC-BY-SA 4.0, CC0, or ODbL ([README](https://raw.githubusercontent.com/wger-project/wger/master/README.md), [license endpoint](https://wger.de/api/v2/license/?format=json)) | **Fallback, not the pick.** 862 exercises, read API needs no auth key. But redistributing means tracking attribution and share-alike per entry. Real bookkeeping for no gain over public domain |
| ExerciseDB (RapidAPI) | Proprietary API terms, not a data license. Free tier ~10 req/day | **Reject.** Paywalled, quota-capped, and the caching/redistribution terms could not be read from a primary source (**UNVERIFIED** — WebFetch returned an empty page twice) |
| MuscleWiki | Proprietary ToS. `robots.txt` disallows `/api/` (confirmed by direct fetch of <https://musclewiki.com/robots.txt>) | **Reject.** ToS reportedly bars redistribution and building a competing dataset. **UNVERIFIED** — the ToS pages returned HTTP 403 to automated fetches, so this rests on search snippets. A human should open <https://musclewiki.com/terms> before treating it as settled — but the `robots.txt` alone is enough to walk away |
| everkinetic/data | CC-BY-SA-4.0 ([LICENSE.md](https://raw.githubusercontent.com/everkinetic/data/main/LICENSE.md)) | **Reject.** Share-alike is viral, only 293 exercises, and the image host `img.everkinetic.com` is dead (confirmed by direct request failure). 121★, pushed 2026-01-21 |
| wrkout/exercises.json | Unlicense | Superseded — free-exercise-db is the maintained successor. 633★, pushed 2025-02-16 |
| exercemus/exercises | MIT | Permissive but small (49★, pushed 2025-07-31) and not vetted further |

One residual risk: free-exercise-db's images inherit the repo-wide Unlicense, but the **original photograph provenance was not traced further back** (UNVERIFIED). If the images end up on a public site, that is worth ten minutes of checking. The JSON itself is not in doubt.

---

## Is there a standard format for strength-training logs?

**No. There is no de facto or de jure interchange format for strength-training logs.** Every app ships its own CSV shape and migration is written per vendor pair.

Evidence:

- The two dominant exports do not share a single column name. Hevy uses `exercise_title`, `set_index`, `weight_kg`, `set_type`, `superset_id`; Strong uses `Exercise Name`, `Set Order`, `Weight`, `Reps`. Different names, different casing, different unit handling. (Sources above.)
- Migration is a **bespoke per-vendor feature**, not a format conversion. Hevy ships a dedicated help article for importing *Strong's* CSV specifically — <https://help.hevyapp.com/hc/en-us/articles/38001424401943-How-to-Import-Strong-App-CSV-Files-and-Export-Your-Data-in-Hevy>. A standard would make that article unnecessary.
- Third parties maintain per-app importers and migration guides rather than one parser — e.g. <https://openweight.dev/migrate/hevy.html>, and the separate Strong parser repos listed above.
- Strong's export is explicitly one-way: "Exported files cannot be imported back into Strong" (<https://help.strongapp.io/article/235-export-workout-data>).
- The MCP ecosystem duplicates itself per vendor: 9+ independent Hevy servers, 10+ Strava, 10 Whoop, several Garmin — each wrapping one app's bespoke REST API (see the MCP section). That duplication is what a missing interchange format looks like from the outside.

The health-platform standards do not fill the gap either, because **they model workouts as sessions, not as sets**:

| Format | Strength support | Status |
|---|---|---|
| Apple HealthKit | `traditionalStrengthTraining` and `functionalStrengthTraining` exist as [`HKWorkoutActivityType`](https://developer.apple.com/documentation/healthkit/hkworkoutactivitytype) cases. No set/rep/weight record type surfaced in the docs — `HKWorkout` carries workout-level stats plus optional route/events. **UNVERIFIED as exhaustive** (the full HKQuantityType list was not enumerated) | Session-level |
| Google Health Connect | `ExerciseSessionRecord` = type + start/end + optional `ExerciseSegment`/`ExerciseLap`. No sets/reps/weight field surfaced ([docs](https://developer.android.com/health-and-fitness/health-connect)) | Session-level |
| Google Fit | **Not dead yet** — new sign-ups closed 2024-05-01, existing APIs stated as supported "until end of 2026", no exact shutdown date announced ([migration FAQ](https://developer.android.com/health-and-fitness/health-connect/migration/fit/faq)) | Being retired into Health Connect |
| Garmin FIT | **The one format that genuinely models sets.** `Profile.xlsx` defines a `set` message carrying exercise name, reps, weight, duration ([SDK](https://developer.garmin.com/fit/), [forum thread](https://forums.garmin.com/developer/fit-sdk/f/discussion/270009/examples-for-encoding-strength-training-activity-files)). But: Garmin-specific, binary, and the SDK cookbook ships no worked example for it — light real use even inside Garmin | Vendor-controlled |
| TCX / GPX | Trackpoint/lap oriented — lat/long/time/HR/cadence. No set concept. **UNVERIFIED this session** (schema not re-read) | Not applicable |
| Open mHealth | Closest schema is "Physical activity" — session-level name/duration/distance/intensity/calories. **Deprecated December 2022** in favour of IEEE 1752.1, and never had strength granularity ([schema library](https://www.openmhealth.org/documentation/schema-docs/schema-library/)) | Dead end |
| schema.org | [`ExerciseAction`](https://schema.org/ExerciseAction) and [`ExercisePlan`](https://schema.org/ExercisePlan) exist, but `exerciseType` is a free-text string. Generic activity vocabulary, no set/rep/weight structure | Too generic |
| Strava API | Strava's app added structured strength logging (exercises/sets/reps/weight), but that detail is reportedly write/sync-only from partner apps and **not exposed on API read endpoints** (**UNVERIFIED** — community post not fetched directly). Rate limits confirmed: 200 req/15min and 2,000/day overall ([docs](https://developers.strava.com/docs/rate-limits/)) | Cardio-first |

The single exception is Garmin's FIT `set` message, which really does model reps and weight per set — but it is binary, vendor-controlled, and barely used even inside Garmin's own tooling. It is not a format anyone else reads.

**Practical consequence for this project:** stop looking for a standard to adopt. Define your own plain-file schema, and treat *Hevy's CSV column set as the import/export target* — it is the closest thing to a shared vocabulary, it is verified, and a tool that reads it inherits the largest existing ecosystem.

---

## MCP and agent integrations

**Fitness MCP servers exist and the space is active.** Results from the GitHub search API (`q=mcp+workout+fitness&sort=stars`), checked 2026-08-31:

| Repo | Stars | Last push | License | What it does |
|---|---|---|---|---|
| [chrisdoc/hevy-mcp](https://github.com/chrisdoc/hevy-mcp) | **448** | 2026-08-31 | MIT | **The one that matters.** Manages Hevy workouts, routines, folders, exercise templates. TypeScript. Actively developed |
| [JamsusMaximus/trainingpeaks-mcp](https://github.com/JamsusMaximus/trainingpeaks-mcp) | 149 | 2026-08-02 | MIT | TrainingPeaks workouts and fitness metrics |
| [cygnusb/coros-mcp](https://github.com/cygnusb/coros-mcp) | 114 | 2026-08-28 | MIT | Coros watch data — sleep, HRV, activities |
| [hhopke/intervals-icu-mcp](https://github.com/hhopke/intervals-icu-mcp) | 61 | 2026-08-31 | MIT | Read/write Intervals.icu, generates workouts |
| [pablo-albaladejo/kaiord](https://github.com/pablo-albaladejo/kaiord) | 9 | 2026-08-31 | MIT | Local-first training platform, Garmin + WHOOP sync, MCP support |
| [Alex-Keyes/boostcamp-mcp](https://github.com/Alex-Keyes/boostcamp-mcp) | 7 | 2026-04-06 | — | Boostcamp for Claude Desktop/Code |
| [gmen1057/fitness-coach](https://github.com/gmen1057/fitness-coach) | 7 | 2026-06-16 | MIT | AI fitness coach, 27 MCP tools |
| [Juxsta/wger-mcp](https://github.com/Juxsta/wger-mcp) | 4 | 2026-02-07 | MIT | **wger API via MCP** — relevant if wger becomes the backend |
| [csjoblom/musclesworked-mcp](https://github.com/csjoblom/musclesworked-mcp) | 4 | 2026-02-17 | MIT | Exercise-to-muscle mapping, 856 exercises across 65 muscles |
| [nchemb/whoop-mcp](https://github.com/nchemb/whoop-mcp) | 3 | 2026-04-27 | MIT | Whoop recovery/sleep/strain |
| [Milofax/xert-mcp](https://github.com/Milofax/xert-mcp) | 5 | 2026-03-04 | — | Xert training load |
| [natejswenson/local-fitness](https://github.com/natejswenson/local-fitness) | 3 | 2026-08-31 | MIT | Garmin data into training briefings |
| [Mnemoclaw/smartrabbit-mcp](https://github.com/Mnemoclaw/smartrabbit-mcp) | 2 | 2026-03-14 | MIT | Smart Rabbit workout programs |

A second Hevy MCP also exists, `ndeast/hevy-history-mcp` (analytics over Hevy history) — listed on Glama and LobeHub. **UNVERIFIED** stars/license.

### The one official server

**wger publishes its own MCP server**: [wger-project/mcp-server](https://github.com/wger-project/mcp-server), maintained by the wger organisation itself. That is the only case here of an official, org-maintained MCP server for a self-hostable FLOSS workout backend. If wger becomes the store, the agent integration is already blessed upstream rather than reverse-engineered. A community alternative also exists ([Juxsta/wger-mcp](https://github.com/Juxsta/wger-mcp), MIT, 4★).

### What the pattern tells you

Nobody has built the MCP server for a **plain-file, self-hosted, agent-owned** log. Every other server above is a client for somebody else's SaaS.

The density is itself evidence. There are 9+ independently written Hevy MCP servers ([chrisdoc](https://github.com/chrisdoc/hevy-mcp), [VReippainen](https://github.com/VReippainen/hevy-mcp-server), [zachsai](https://github.com/zachsai/hevy-mcp), [zelosleone](https://github.com/zelosleone/Hevy-MCP) in Rust, [Vellarasan](https://github.com/Vellarasan/hevy-mcp), others), 10+ for Strava, 10 for Whoop, and several for Garmin — all wrapping each vendor's bespoke REST API. That is exactly the duplication you get when no shared interchange format exists. It is a symptom of the "no standard" finding above, not of a healthy ecosystem.

### Other integration paths checked

- **Strong**: no MCP server found. Only [tolik518/strong-api-workout-sync](https://github.com/tolik518/strong-api-workout-sync), a sync script. Query run: `"strong app" mcp server github workout`.
- **Apple Health**: several MCP servers exist ([PhilipAD/health-export-mcp](https://github.com/PhilipAD/health-export-mcp), [the-momentum/apple-health-mcp-server](https://github.com/the-momentum/apple-health-mcp-server) using DuckDB, others). All parse the `export.xml` you manually export from the Health app — **none talk to a live HealthKit API**, because Apple exposes none server-side. Any Apple Health path is therefore a manual-export path.
- **Garmin**: [Nicolasvegam/garmin-connect-mcp](https://github.com/Nicolasvegam/garmin-connect-mcp), [st3v/garmin-workouts-mcp](https://github.com/st3v/garmin-workouts-mcp), [matin/garth-mcp-server](https://github.com/matin/garth-mcp-server), others — all built on **reverse-engineered** libraries (`python-garminconnect`, `garth`), not Garmin's official Health API. Fragile by construction.
- **Home Assistant**: [hudsonbrendon/HA-hevy](https://github.com/hudsonbrendon/HA-hevy) and [DisplacedForest/ha-hevy-tracker](https://github.com/DisplacedForest/ha-hevy-tracker), both requiring Hevy Pro. Google Fit integrations exist but are undermined by the Fit retirement. No strength-set-level HA integration found.
- **First-party connectors**: no official Anthropic or OpenAI fitness connector. Only third-party commercial bridges (athletedata.health, wellnessproject.ai, a Tredict ChatGPT plugin).
- **Registries**: [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) has an *open, unmerged* issue ([#4680](https://github.com/punkpeye/awesome-mcp-servers/issues/4680)) proposing an exercise-API server, suggesting fitness is not yet a settled category there. Glama, mcp.so, and mcpservers.org do list Health/Wellness buckets.

Star counts and last-commit dates in this "other paths" list are **UNVERIFIED** — the search budget ran out before the GitHub API pass. The table above them was verified.

---

## Gaps

Ranked by how much they'd change a decision.

1. **Nine of sixteen commercial apps previously had no verified export/API data**: FitNotes, Boostcamp, Fitbod, JEFIT, Alpha Progression, GymBook, Simple Workout Log, Progression, Stacked. Detail merged from three sub-survey reports, see Appendix A. Residual gaps remain per app — exact pricing, CSV column lists, and export/import gating — see the GAPS notes inside Appendix A.
2. **The most direct test of the "no standard" question never ran.** The queries `open workout format` and `workout log json schema` were queued when the budget ran out. The NO answer rests on strong indirect evidence (below), not on that search. One follow-up search when the budget resets would settle it.
3. **Strong's CSV header is unverified** — reported by parser repos, not read from a header line. Verify against a real export before writing an importer.
4. **Star counts and commit dates in the "other integration paths" list are unverified.** The main MCP table was checked via the GitHub API; the narrative list below it was not. So "which of those are maintained vs abandoned" is open.
5. **HealthKit and Health Connect set/rep modelling is asserted, not swept.** Neither the full HKQuantityType list nor the complete Health Connect record reference was enumerated. The conclusion matches every downstream behaviour observed (all Apple Health MCP servers parse export.xml; every app stores set detail in its own DB), but it is not a completed proof.
6. **TCX/GPX schemas were not re-read this session.**
7. **Hevy API rate limits unknown** — the Swagger page is JS-rendered and did not fetch.
8. **FIT SDK licence terms not captured** — the protocol page returned navigation chrome only.
9. **workout-cool's exercise DB licence** is not stated inline. Matters only if you lift their data rather than free-exercise-db.
10. **wger's per-exercise licence id** — `/api/v2/exercise/` exposes `license_author` but not the licence id; the endpoint that does was not identified.
11. **MuscleWiki and RapidAPI ToS** rest on search snippets, not primary reads (403 / empty page). Both are rejected on other grounds anyway.

---

## Open questions for you

I could not ask mid-run, so these are recorded rather than resolved. The first two are the ones that change what gets built.

1. **Is wger the backend, or just the schema?** It is self-hostable FLOSS, docker-compose, 6.8k stars, actively developed, its read API needs no auth key, and it is the only project here with an **official** MCP server. That is a lot of the system already built. The counterargument is weight: it is a full Django nutrition-and-fitness suite, and you want a log an agent owns. Cribbing the schema is the cheap option; running the thing is the fast one. This is the decision I would settle first.
2. **Emit an interchange format, or only consume your own store?** If the log is agent-native and private, the "no standard exists" finding is irrelevant. If you want to import a friend's Strong history or push to a phone app, Hevy's CSV column set is the target to write against. Different amount of work.
3. **Liftoscript: reimplement or import?** The DSL is the standout find, but Liftosaur is AGPL and not self-hostable. A REST API exists (Appendix A) but it is Pro-gated and not a bulk-export endpoint. Either write a Liftoscript-*like* grammar from scratch, or vendor their public program library as seed content. Different licence exposure.
4. **Is Hevy acceptable as the store?** If yes, `hevy-mcp` plus Hevy Pro is most of the system today. But the API is Pro-gated, so **every friend needs a paid subscription** — which directly contradicts the "friends replicate it easily" requirement. My read: no. Your call.
5. **AGPL vs MIT for a base.** If you ever fork rather than crib, workout-cool (MIT, 8.4k★) is far lower friction than wger or Liftosaur (both AGPL). Worth deciding before anyone writes code.
6. **Phone-native health integration — worth it?** Apple Health and Health Connect model sessions, not sets. Integration buys a calorie estimate and a closed ring, not your log. Cheap to skip.

---

## Appendix A: commercial app survey detail

Three sub-agents each surveyed a slice of the nine previously-uncovered apps. This appendix carries their raw findings, sources, and gaps. The master table above reflects a summary; read this section for column-level detail, exact prices, and the caveats each sub-report flagged.

Each sub-report used its own confidence markers. Where a sub-report wrote "NOT FOUND" or left a claim unsourced, that is preserved as-is below rather than upgraded to UNVERIFIED — the two mean slightly different things (NOT FOUND: looked and found nothing; UNVERIFIED: found a claim but could not confirm it against a primary source).

### A.1 Boostcamp, Fitbod, JEFIT, Alpha Progression

| App | Price / free tier | Export | Import | Public API | Open source |
|---|---|---|---|---|---|
| Boostcamp | Free: full 11,000+ program library, tracking, no ads. Pro: adds Strength Score, muscle heatmap, 20+ coach programs, advanced analytics. Exact price **UNVERIFIED** — the official site withholds it; third-party sources say ~$59.99/yr or $14.99/mo but that is not corroborated from a primary page | No native export. A third-party Chrome extension scrapes `/history` JSON to CSV; columns not fully enumerated | None found | No official API. Reverse-engineered via `boostcamp-api` (email/password login → session token), used by an MCP server. No rate-limit or doc info | No |
| Fitbod | Free: 3 workouts + tracking. Premium ~$15.99/mo or $95.99/yr (secondary source, dated ~2025, price likely stale) | Settings → "Export Workout Data" → CSV. Real column list confirmed (below). Free-vs-paid gating of export **UNVERIFIED** | No CSV import; only Apple Health workout sync | No official public API found. An "Akousa" listing claiming OAuth2 looks like an unverified third-party aggregator, not a primary source | No (the org's public repos are sample/interview projects and forks, not the app) |
| JEFIT | Free: 1,400+ exercise library, unlimited logging, community routines. Elite $12.99/mo or $69.99/yr: pro plans, advanced analytics, watch app, AI progression | Official support page unreachable (SSL error on fetch). Secondary sources: export is a `.bak` SQLite file, needs manual decrypt/convert to CSV; no clean native CSV | **UNVERIFIED** | Unofficial only: `denolfe/jefit` reverse-engineered, no auth beyond a public userId with profile visibility set to "Everyone". No official docs | No |
| Alpha Progression | Free: full logging, 795 exercises w/ video, body measurements. Pro $12.99/mo or $79.99/yr (14-day trial): plan generator, progression recommendations, charts, multi-gym profiles, periodization/RIR/deload | Official FAQ confirms CSV export exists ("raw numbers" from analytics). Column names **UNVERIFIED**, free-vs-paid gating **UNVERIFIED** | **UNVERIFIED** | None found | No evidence found either way; presumed closed |

Fitbod CSV columns (from `rhnfzl/fitbod-report` parser): `Date, Exercise, Reps, Weight(kg), Duration(s), Distance(m), Incline, Resistance, isWarmup, Note, multiplier`. Source: <https://github.com/rhnfzl/fitbod-report>

What to steal:
- **Boostcamp**: `boostcamp-mcp` (<https://github.com/alex-keyes/boostcamp-mcp>) exposes programs, custom exercises, and analytics as MCP tools — the closest precedent to this project found in the whole survey. The free tier gives the full program library; the paywall sits on analytics, not content. Weekly Sunday auto-reports plus a per-muscle volume heatmap. Red flag: zero official export/API.
- **Fitbod**: `isWarmup` boolean plus `multiplier` field encode warm-up/superset/drop-set state in one row. Separates Distance/Incline/Resistance from Weight/Reps. Adaptive per-workout generation. Red flag: export paywall status unclear.
- **JEFIT**: session timestamp plus per-set weight/reps/duration plus a calculated 1RM per set. Native smartwatch logging. Red flag: worst export story surveyed (encrypted SQLite `.bak`).
- **Alpha Progression**: periodization/deload/RIR as first-class fields in the plan generator; multiple gym profiles (equipment per gym). Red flag: least documented app for programmatic reuse.

Sources: <https://www.boostcamp.app/> · <https://github.com/Dugsteer/Boostcamp_history_download_chrome_extension> · <https://github.com/blaekhossa/boostc_2_dataframe> · <https://github.com/alex-keyes/boostcamp-mcp> · <https://fitbod.me/> · <https://github.com/Fitbod> · <https://github.com/rrebase/fitdata> · <https://github.com/rhnfzl/fitbod-report> · <https://www.jefit.com/> · <https://www.jefit.com/elite> · <https://github.com/denolfe/jefit> · <https://github.com/aensidhe/JefitExporter> · <https://alphaprogression.com/en> · <https://push-pull.app/blog/push-pull-vs-alpha-progression> (secondary) · <https://www.sensai.fit/blog/hevy-vs-strong-vs-fitbod-vs-jefit> (secondary)

**GAPS (A.1):** Boostcamp's exact Pro price, full CSV columns, and closed-source status are assumed, not confirmed. Fitbod's export paywall gating, 2026 price, and the "Akousa" API claim are all **UNVERIFIED**. JEFIT's official export article was unreachable (SSL), and import is unconfirmed. Alpha Progression's CSV columns, gating, import, API, and OSS status are all unconfirmed. None of the four apps in this slice have a confirmed CSV import path. The licensing/ToS status of the reverse-engineered APIs (Boostcamp, JEFIT) was not checked.

### A.2 Strong, Hevy, FitNotes, Liftosaur

| App | Price / free tier | Export | Import | API | Open source |
|---|---|---|---|---|---|
| Strong | Free w/ limited routines; Pro ~$4.99/mo, ~$29.99/yr (App Store shows EUR 4.99–5.99/mo, EUR 24–34/yr, EUR 89–100 lifetime, varies by region) | CSV export exists (paid-gating **UNVERIFIED**) | No CSV import | No official public API. Reverse-engineered only; community warns of "legal implications" | Closed |
| Hevy | Free: unlimited logging, capped at 4 routines / 7 custom exercises / 3 months of graph history. Pro: $2.99/mo, $23.99/yr, $74.99 lifetime | CSV export exists (free-tier accessible per help article title) | Yes: imports Strong CSV | REST API, Pro-gated ("API access requires Hevy Pro" per Serval docs). API key header. Rate limits **UNVERIFIED** | Closed |
| FitNotes | Free, no ads. "FitNotes Supporter" IAP unlocks extra exercise types | CSV export, free | Yes: FitNotes iOS imports CSV from Strong, Fitbod, IronGAINS, HeavySet, Hevy, Liftin, WeightFit via a fixed header schema | No API found | **NOT open source** — the package name `com.github.jamesgay.fitnotes` misleads; no license or source repo found |
| Liftosaur | Free tier functional (built-in programs, logging, offline, Liftoscript editor). Premium: cloud sync, advanced analytics; export gating signals conflict | Export implied by reviews; mechanism **UNVERIFIED** | **UNVERIFIED** | REST API at liftosaur.com/doc/api, Bearer `lftsk_...` key, requires premium (403 otherwise). Endpoints: programs, workout history, live workout, gyms/equipment, exercise-data, measurements. Rate limits not documented | Client is AGPL-3.0 (<https://github.com/astashov/liftosaur>); server OSS status **UNVERIFIED** |

What to steal:
- **Strong**: one CSV row per set: `Date, Workout Name, Duration, Exercise Name, Set Order, Weight, Reps, Distance, Seconds, Notes, Workout Notes, RPE`.
- **Hevy**: `exercise_title` + `superset_id` + `set_type` (normal/warmup/failure/dropset); the `/exercise_templates` endpoint pattern.
- **FitNotes**: its fixed CSV header is the de facto lingua franca — FitNotes2Hevy, GymRun→Hevy, and JEFIT→Hevy converters all emit it. Worth matching as an import target.
- **Liftosaur**: Liftoscript DSL for progression logic embedded in program text; `/playground` simulate-before-save; idempotent set-logging writes with device/client headers.

Red flags: Strong's export is one-way and the vendor is hostile to a public API. Hevy's API is paywalled and its rate limits are opaque. FitNotes is closed and CSV-only. Liftosaur's API is paid despite an AGPL client, and the backend has not been proven open.

Sources: <https://help.strongapp.io/article/235-export-workout-data> · <https://apps.apple.com/DE/app/id464254577> · <https://github.com/AlexandrosKyriakakis/StrongAppAnalytics/blob/main/Data/strong.csv> · <https://github.com/tolik518/strong-api-workout-sync> · <https://api.hevyapp.com/docs/> · <https://docs.serval.com/sections/integrations/hevy> · <https://github.com/matanabudy/workout-data-sync/blob/main/examples/hevy_export_sample.csv> · <https://help.hevyapp.com/hc/en-us/articles/38001424401943-How-to-Import-Strong-App-CSV-Files-and-Export-Your-Data-in-Hevy> (title only, Cloudflare-blocked) · <https://www.getfitnotes.com/docs/migrate-from-other-apps.html> · <http://www.fitnotesapp.com/faq/> · <https://github.com/astashov/liftosaur> · <https://www.liftosaur.com/doc/api> · <https://www.liftosaur.com/>

**GAPS (A.2):** Strong's export gating is unconfirmed. Hevy's rate limits and CSV gating are unconfirmed (page body Cloudflare-blocked). Liftosaur's export gating (conflicting signals) and import path are unconfirmed. FitNotes' non-OSS status is ruled out by absence of evidence, not a definitive license statement. No app in this slice documents its rate limits.

### A.3 GymBook, Simple Workout Log, Progression, Stacked

| App | Price / free tier | Export | Import | Public API | Open source |
|---|---|---|---|---|---|
| GymBook | Free core (unlimited, no ads); Pro $1.99/mo, $8.99/yr, $22.99 lifetime (gymbookapp.com, fetched 2026-08-31) | CSV + XML + DB backup, Pro-only | Yes: DB backup restore on another device (App Store listing) | NOT FOUND | No; only a defunct translation-strings repo (sallvi/localize-gymbook) |
| Simple Workout Log | Free tier + low-cost Premium (price **UNVERIFIED**) | CSV/Excel export via "Tools" tab; gating **UNVERIFIED**, columns NOT FOUND | Local SQLite backup `workoutlog.bak`; a community script writes into that DB (treischl/sl5x5-to-workoutlog) | NOT FOUND | Proprietary; the helper script is MIT-style |
| Progression (Zoltan Demant, `workout.progression.lite`; this survey originally named "Rade Stanojevic" as the developer — that could not be verified and is likely wrong) | Free unlimited logging; Pro IAP price NOT FOUND | CSV export per listicles; official confirmation NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND |
| Stacked (M4L, Inc., iOS id1116989938) | "100% FREE" per App Store | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND |

Notes: GymBook is active (v7.1.3, 2026-08-29). Its DB-file backup+restore is a full-state round-trip primitive worth copying; the Pro-gated export is a red flag. Simple Workout Log's real interchange point is the raw SQLite file, not its CSV. Stacked's iOS build was last updated 2022-06-07 and is likely dead; Legion Athletics markets a "Stacked" at legionathletics.com/stacked linking the same App Store ID under a different developer name (**UNVERIFIED**); a separate Play Store listing is also unverified.

Sources: <https://www.gymbookapp.com/> · <https://apps.apple.com/us/app/gymbook-strength-training/id650113307> · <https://github.com/sallvi/localize-gymbook> · <https://www.simpleworkoutlog.com/> · <https://www.simpleworkoutlog.com/faq.php> · <https://github.com/treischl/sl5x5-to-workoutlog> · <https://play.google.com/store/apps/details?id=workout.progression.lite> · <https://appgrooves.com/android/workout.progression.lite/progression-workout-tracker/zoltan-demant> · <https://apps.apple.com/us/app/stacked-workout-tracker-for/id1116989938> · <https://legionathletics.com/stacked/>

**GAPS (A.3):** Progression's developer identity is unresolved. CSV columns for all four apps in this slice are NOT FOUND. APIs are NOT FOUND for all four. Licenses are closed or NOT FOUND for all four. Simple Workout Log's and Progression's pricing are unconfirmed. The Stacked Android-listing and developer-name discrepancy is unresolved. This sub-report also hit a WebSearch session cap (200 calls) mid-task, which capped how far it could dig.
