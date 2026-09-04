"""Progression arithmetic domain: pure functions over one exercise's
progression config plus one session's parsed sets. `load_adjust.py` owns the
turn/conversation domain and calls into these (`docs/architecture.md`
"one script per skill... split by domain, never by execution step", the
`log_set.py`/`grammar.py`/`tokens.py` split is the precedent). No I/O.

`load_kind = assist` inverts bump and deload direction (lim L-05): less
assistance is progress, so a bump *subtracts* magnitude and a deload *adds*
it back. `axis` picks which `agent/progression-state.progression` field a bump or deload targets
(lim L-20): `weight` writes `next_target`, `level` and `variation` write
`stage_index` / `variation_index` instead of ever touching load.
"""

from __future__ import annotations

from typing import Any

HIGH_RPE = 9.5
TARGET_FIELD = {"weight": "next_target", "level": "stage_index", "variation": "variation_index"}


def bumped_value(cfg: dict[str, Any], kind: str | None) -> float:
    if cfg["axis"] != "weight":
        return cfg["current"] + cfg["increment"]
    delta = cfg["increment"]
    return max(cfg["current"] - delta, 0) if kind == "assist" else cfg["current"] + delta


def deload_target(cfg: dict[str, Any], kind: str | None) -> float:
    delta = cfg["current"] * (cfg["deload_pct"] / 100)
    return cfg["current"] + delta if kind == "assist" else cfg["current"] - delta


def rpe_capped(cfg: dict[str, Any], rpe: float | None) -> bool:
    """Research/03 rule 4: RPE >= 9.5 *two sessions running* holds even at the
    top of the range. One hard session never blocks the bump.

    "Running" means consecutive, so the streak counts every session that
    reports one, whether or not it hit the top of the range. `evaluate` used
    to call this inside `top and not rpe_capped(...)`, and Python's
    short-circuit skipped the update on any missed session, letting two hard
    sessions with an easy one between them fire the hold (ayf.8). Callers
    must therefore call this exactly once per session, unconditionally.

    A session that reports no RPE is not a high-RPE session, so it breaks the
    run. That reading is not stated by rule 4 (see ayf.25): it is the
    conservative one, because RPE is accept-if-typed and this cap is a
    backstop, not the operating point (00-synthesis-trainer rule 4)."""
    cfg["high_rpe_streak"] = cfg["high_rpe_streak"] + 1 if (rpe is not None and rpe >= HIGH_RPE) else 0
    return cfg["high_rpe_streak"] >= 2


def evaluate(cfg: dict[str, Any], sets: list[dict[str, Any]], kind: str | None,
             rpe: float | None) -> dict[str, Any]:
    """One session's outcome against the stored rule. Returns an `outcome`
    tag (`bump`, `hold`, `miss_hold`, `next_stage`, `deload_ask`,
    `deload_repeat`) plus whatever value it produced; `load_adjust.py`
    turns that into writes and a `say` line."""
    if not sets:
        # `all([])` is True, so an empty session read as every set at the top
        # of the range *and* as every set below it, and bumped off nothing
        # lifted (ayf.12). Nothing happened is neither a success nor a miss:
        # SKILL.md "Turn 1, from cold" says no history holds and says there is
        # nothing to adjust, never bumps and never counts a failure.
        return {"outcome": "no_sets", "value": cfg["current"]}

    lo, hi = cfg.get("rep_range", (0, 10**9))
    reps = [s["reps"] for s in sets]
    capped = rpe_capped(cfg, rpe)  # once per session, before any short-circuit
    top = all(r >= hi for r in reps)
    bottom_miss = all(r < lo for r in reps)

    if top and not capped:
        cfg["fail_count"] = 0
        cfg["current"] = bumped_value(cfg, kind)
        return {"outcome": "bump", "field": TARGET_FIELD[cfg["axis"]], "value": cfg["current"]}

    if not bottom_miss:
        return {"outcome": "hold", "value": cfg["current"]}

    return _miss(cfg, kind)


def replay(cfg: dict[str, Any],
           sessions: list[tuple[list[dict[str, Any]], str | None, float | None]]
           ) -> dict[str, Any]:
    """Fold `evaluate` over already-parsed sessions, oldest first, against a
    scratch copy of `cfg`. Pure: never mutates the caller's `cfg`. `sessions`
    is exactly `evaluate`'s own trailing three arguments per entry, so
    hydrating a `SetRow` into one (a typed transcript line today, `Sets`
    rows after workout-log-rb0) is the caller's job (docs/architecture.md
    "Hydration belongs to the caller"), not this fold's."""
    acc = dict(cfg)
    outcomes = [evaluate(acc, sets, kind, rpe)["outcome"]
                for sets, kind, rpe in sessions]
    return {"current": acc["current"], "fail_count": acc["fail_count"],
            "high_rpe_streak": acc["high_rpe_streak"],
            "stage": acc.get("stage", 0), "outcomes": outcomes}


def _miss(cfg: dict[str, Any], kind: str | None) -> dict[str, Any]:
    cfg["fail_count"] += 1
    if cfg["fail_count"] < cfg["after_misses"]:
        return {"outcome": "miss_hold", "fail_count": cfg["fail_count"]}

    on_miss = cfg["on_miss"]
    if on_miss == "hold":
        return {"outcome": "miss_hold", "fail_count": cfg["fail_count"]}
    if on_miss == "next_stage":
        # GZCLP's cheap intermediate step (research/03 s6): the ladder
        # moves, the load does not. Always `stage_index`, independent of
        # the block's own progression axis.
        cfg["fail_count"] = 0
        cfg["stage"] = cfg.get("stage", 0) + 1
        return {"outcome": "next_stage", "field": "stage_index", "value": cfg["stage"], "fail_count": 0}

    declined = cfg["declined_streak"]
    if declined is not None and cfg["fail_count"] - declined < cfg["after_misses"]:
        # lim L-22: a decline is checked before re-offering. Re-ask only
        # once misses have piled up a fresh full streak past the decline,
        # not on every subsequent miss at the same streak.
        return {"outcome": "deload_repeat", "fail_count": cfg["fail_count"]}
    proposed = deload_target(cfg, kind)
    cfg["pending_deload"] = {"proposed": proposed, "kind": kind}
    return {"outcome": "deload_ask", "proposed": proposed, "fail_count": cfg["fail_count"]}
