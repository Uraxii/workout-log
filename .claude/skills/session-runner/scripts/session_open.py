"""Session identity: opening (L1, L3, L4) and L11's `open -> abandoned`
half. Split out of `lifecycle.py` (house limit; docs/architecture.md "One
script per skill" applies the same way here, split by domain, never by
execution step): identity/opening is one body of knowledge, the Notes-row
commands `lifecycle.py` still owns are another.
"""

from __future__ import annotations

from typing import Any

import rows as row_shapes


def open_session(state: dict[str, Any], writes: list[dict[str, Any]],
                 now: str) -> tuple[str, str, int, bool, bool]:
    """L1: opens a session on the first logged line, or reopens one closed
    at this exact frozen instant (same `Start time`/`Timezone`: an immediate
    "done for today" then another line, or a resend). `session_seq` only
    advances on a genuinely new identity (writer.py `_resolve_session`,
    defect 1). Also returns whether this call opened it, rule L2's hook for
    the once-per-session readiness ask.

    L11's other half: stays open by default past its own date (dec "S21
    partial session"); this only arms `finish_or_advance` so `try_advance`
    below can abandon it on an explicit "advance" reply. Fifth return value
    is whether this call just armed it, `log_set.py`'s ask-once hook, same
    shape as `is_new`."""
    session_id, session_seq = state.get("session_id"), state.get("session_seq", 0)
    session_key = state.get("session_key")
    is_new = False
    just_armed = False
    if (session_id is not None and state.get("open_date") not in (None, now[:10])
            and state.get("finish_or_advance") is None):
        state["finish_or_advance"] = {"open_date": state["open_date"]}
        just_armed = True
    if session_id is None:
        candidate_key = row_shapes.session_key(now, state["tz"])
        by_date = dict(state.get("sessions_by_date", {}))
        prior = by_date.get(now[:10])
        if prior is not None and prior["session_key"] == candidate_key:
            session_id, session_key = prior["session_id"], candidate_key
        else:
            # A genuinely new session: `Set index` is scoped to
            # `(session, exercise)` (rule L7), so a carried-over cursor
            # from a prior, now-closed session would mislabel set 1 of a
            # new session as a continuation of the old one.
            session_seq += 1
            session_id, session_key = f"sessions-{session_seq}", candidate_key
            state["cursor"] = {}
            state["cursor_advanced"] = False  # program_cursor: one advance per session
            is_new = True
        writes.append({"verb": "row-create", "target": "Sessions", "payload": {
            "Date": now[:10], "Timezone": state["tz"], "Status": "open", "Start time": now,
            "week_index": row_shapes.week_index(now[:10]),
        }})
        by_date[now[:10]] = {"session_id": session_id, "session_key": session_key, "status": "open"}
        state["sessions_by_date"] = by_date
        state["open_date"] = now[:10]
    state.update(session_id=session_id, session_key=session_key, session_seq=session_seq)
    return session_id, session_key, session_seq, is_new, just_armed


def _readiness_ask(state: dict[str, Any], is_new: bool) -> str:
    """L2: appended once, on the turn that opens a session; never blocks."""
    if not is_new:
        return ""
    state["readiness_pending"] = True
    return "\nReadiness 1-5? (skip if you like)"


def finish_or_advance_prompt(open_date: str) -> str:
    """L11's ask, appended while `finish_or_advance` stays unanswered."""
    return (f"{open_date}'s session is still open. Keep logging to finish "
           "it, or say \"advance\" to start today fresh.")


def with_open_prompts(turn: dict[str, Any], state: dict[str, Any], is_new: bool, just_armed: bool) -> dict[str, Any]:
    """`log_set.py`'s hook: L2's readiness ask or L11's finish-or-advance
    ask, whichever this turn's `open_session` call just signalled. Never
    both; opening a session and staying in a stale one are exclusive."""
    if is_new:
        turn["confirm_line"] += _readiness_ask(state, True)
    elif just_armed:
        turn["confirm_line"] += "\n" + finish_or_advance_prompt(state["finish_or_advance"]["open_date"])
    return turn


def try_advance(state: dict[str, Any], pending: dict[str, Any], now: str) -> dict[str, Any]:
    """L11: `open -> abandoned` on answering *advance* to the ask
    `open_session` armed (dec "S21 partial session"). `pending` is that
    armed value, already popped by the caller. Abandons the stale session,
    then opens today's the same way any other first line of the day would,
    including L2's readiness ask if that call finds it new."""
    writes = [{"verb": "row-create", "target": "Sessions", "payload": {"Status": "abandoned"}}]
    by_date = dict(state.get("sessions_by_date", {}))
    entry = by_date.get(pending["open_date"])
    if entry is not None:
        by_date[pending["open_date"]] = {**entry, "status": "abandoned"}
    state.update(session_id=None, sessions_by_date=by_date)
    _, _, _, is_new, _ = open_session(state, writes, now)
    confirm = f"{pending['open_date']}'s session marked abandoned. Starting today fresh."
    confirm += _readiness_ask(state, is_new)
    return {"writes": writes, "confirm_line": confirm, "state": state}
