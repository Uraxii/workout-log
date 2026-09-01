"""Text-out domain for `load-adjust`: every line this skill puts in front of
the athlete, and the number formatting those lines share. `parse.py` is
text-in, `rules.py` is the arithmetic, `load_adjust.py` is turn dispatch;
this is the fourth face of the same split (`docs/architecture.md`: "one
script per skill... split by domain, never by execution step").

Splitting it out is also what keeps `load_adjust.py` under the 200-line
limit. Every string the `make check` fixtures assert as a `say` row lives
here, so a wording change is one file, not a hunt through dispatch.
"""

from __future__ import annotations

from typing import Any

import parse

HRT_NOTE = {
    "feminizing": ("On feminizing HRT, endurance and hemoglobin drop before strength "
                    "does (research/11 s1.1): a slower pace or higher heart rate in the "
                    "first months is the hormone, not a stall, so this isn't a deload "
                    "trigger. Keeping resistance volume steady defends strength best."),
    "masculinizing": ("On masculinizing HRT, year one is the best strength window most "
                       "trans men get (research/11 s2.2): progress load, keep volume "
                       "conservative while tendons catch up to the faster muscle gain."),
}
MANUAL = "Progression is set to manual, not auto-adjusting. Logged for the record."
NO_BARE_CLEAR = ("Good to hear, but progression stays manual until 14 symptom-free "
                  "days pass or a clinician clearance / re-screen clears it. A "
                  "confirmation alone can't do that (rule S5).")

OUTCOME = {
    "bump": lambda name, cfg, r: f"{name}: top of the range, bumping "
        f"{'less assist' if r['kind'] == 'assist' else 'up'} to {fmt(cfg, r['value'])}.",
    "hold": lambda name, cfg, r: f"{name}: logged, holding at {fmt(cfg, r['value'])}.",
    "miss_hold": lambda name, cfg, r: f"{name}: missed the bottom of the range, holding.",
    "next_stage": lambda name, cfg, r: f"{name}: repeat miss, moving to the next stage, same load.",
    "deload_ask": lambda name, cfg, r: (f"{name}: {cfg['deload_pct']:g}% deload to "
        f"{fmt(cfg, r['proposed'])}? (yes/no)"),
    "deload_repeat": lambda name, cfg, r: f"{name}: repeat miss, holding (deload already declined).",
    "no_sets": lambda name, cfg, r: f"{name}: no sets on that line, nothing to adjust.",
}


def fmt(cfg: dict[str, Any], value: float) -> str:
    if cfg["axis"] != "weight":
        return f"{value:g}"
    return f"{value:g} {cfg.get('unit', '')}".strip()


def unreadable(bad: parse.Unreadable) -> str:
    """Refuse and ask, for the one token the grammar could not read.

    Three options exist for a malformed line and two of them are worse. A
    traceback mid-workout has failed the athlete outright. Writing a guessed
    number silently is worse still, the project's standing rule. Logging
    nothing and saying "Noted." is the third: it costs the athlete the set,
    because they walk away believing it landed. So: name the token, say what
    would have worked, confirm nothing was written, ask."""
    if not bad.token:
        return (f"Nothing was there where I needed {bad.expected}, so I logged "
                "nothing. What did you mean?")
    return (f"I couldn't read {bad.token!r}, so I logged nothing for it. "
            f"I need {bad.expected}. What did you mean?")
