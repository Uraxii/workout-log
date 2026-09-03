# Swap-in-place table

A new `open` entry in `config/limits` re-triggers `program-design` (build-plan
s6 trigger column, lim L-21). Rather than rebuild the program, it swaps the
one exercise the entry rules out for a substitute, everywhere that exercise
appears in the active `rotation`. `scripts/design.py:_swap_for_area` looks up
the entry's `area` here.

| area | exercise | substitute | reason |
|---|---|---|---|
| knee | Barbell Squat | Leg Press | Leg Press holds the same quad-dominant pattern with the knee supported and no free-standing load. |
| knee | Front Barbell Squat | Leg Press | Same swap as the back squat: Leg Press keeps the pattern, drops the free-standing load on the knee. |
| back | Barbell Deadlift | Trap Bar Deadlift | The trap bar's neutral grip and higher start position cut spinal shear versus a straight bar pull. |
