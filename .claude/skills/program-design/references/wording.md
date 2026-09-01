# Refusal with options (build-plan s7.2)

Five categories ship no template in release 1 (research/16-program-library.md
"Gaps"). `program-design` never invents one; it uses this one scripted reply,
three options, no silence:

> "I don't have a template for X. Three things I can do: run the nearest one
> I do have, [named template], which shares [what it shares]; build X's
> movements into your current program as accessory work; or point you at
> [source] to bring numbers back. Which?"

`scripts/library.py:refusal_for` matches the athlete's line against
`keywords`, then fills the script from the row's `nearest`, `shares`, and
`source`. A category with no partial template still gets all three slots:
`nearest` names the closest reference material instead of a template, and
`shares` says so plainly.

| category | keywords | nearest | shares | source |
|---|---|---|---|---|
| rings | rings, ring work, gymnastic rings | the bodyweight Recommended Routine (RR) | its ring rows and ring dips, just not the advanced strength holds | GymnasticBodies or Overcoming Gravity |
| carries | loaded carry, loaded carries, carry program, farmer carry program | Easy Strength | its carry work, just not as the whole program | Simple and Sinister by Pavel Tsatsouline |
| mobility | mobility for, restriction mobility, ankle mobility program, shoulder mobility program | the Squat University mobility articles | a named-restriction drill list, not a dated multi-week plan | squatuniversity.com's mobility series |
| in_season | in season, in-season, maintenance during season | Easy Strength | its low-volume, submaximal shape, close to a maintenance dose | the NSCA in-season strength infographic |
| hypertrophy | full body hypertrophy, full-body hypertrophy | Metallicadpa's PPL | the same rep-range hypertrophy work, just split by body part, not full-body in one session | the ACSM sets-per-muscle guidelines |
