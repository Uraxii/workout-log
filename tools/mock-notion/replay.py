"""Phase proof runner: replay a fixture transcript, diff against expected.tsv.

    python3 tools/mock-notion/replay.py fixtures/01-three-sets

Exit 0 when the emitted TSV equals expected.tsv byte for byte, 1 otherwise
with a unified diff on stdout. No Notion, no LLM: the skill-side script under
test is a pure function of (chat line, state).
"""

from __future__ import annotations

import difflib
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import writer  # noqa: E402  (same-dir module; the dir name is not importable)
from hydrate import hydrate  # noqa: E402
from reader import MockNotionReader  # noqa: E402
from seams import SEAMS  # noqa: E402
from transcript import Fixture, parse_transcript  # noqa: E402

# build-plan s3.2's round-trip ceiling covers exercise RESOLUTION cost, not a
# multi-row entry's legitimate set count: rungs 1-3 add 0 round trips, rung 4
# adds "1 create" (s3.2:193). A multi-row entry (EMOM, a ladder, rule B/C)
# writes one `Sets` row per set on purpose (s1.3 row 5: 10 rows, one EMOM
# turn) and is not part of this ceiling.
MAX_RESOLUTION_WRITES_PER_TURN = 1  # at most one `Exercises` create per turn

# No round-trip ceiling covers a single entry's row count, but an unbounded
# one (e.g. a mistyped EMOM round count) still shouldn't silently write
# hundreds of rows. Sanity ceiling, not from the spec: double the largest
# documented legitimate case (s1.3 row 5, 10 rows).
MAX_SET_ROWS_PER_TURN = 20


def replay(fixture: Fixture, notion: writer.MockNotion) -> list[str]:
    """Feed each turn through the skill script, apply the writes it returns.

    Returns one `say` TSV row per turn: the exact text the user reads, JSON
    encoded so a multi-line script (PAR-Q+, a refusal) stays one TSV line.
    State threads turn to turn; the script never touches Notion itself.

    A `@cold` turn threads nothing: the chat ended, so its state is rebuilt
    from the store's read verbs (`hydrate.py`). No per-turn read ceiling
    guards that, because no seam issues reads at all (they are pure
    functions of `(line, state)`); hydration is a turn-1 caller cost, off
    the s3.2 budget the same way `intake`'s database-create turn is.
    """
    reader = MockNotionReader(notion)
    catalog = {}
    for entry in fixture.catalog:
        page_id = notion.seed_row("Exercises", {"Name": entry["name"], "measure": entry["measure"]})
        catalog[entry["name"]] = {"id": page_id, "measure": entry["measure"]}

    state = {
        "tz": fixture.timezone,
        "units": fixture.units,
        "catalog": catalog,
        "session_id": None,
        "session_seq": 0,
        "exercise_seq": len(catalog),
        "cursor": {},
        # No parent page id: a fixture that needs one gets it the way the
        # athlete does, by answering `intake`'s first question in its own
        # transcript (ticket workout-log-mqs). Seeding one here made it
        # impossible for a fixture to prove intake ever asks.
        "databases": {},
    }
    if fixture.intake_cursor is not None:
        state["intake"] = {"cursor": int(fixture.intake_cursor), "answers": {}, "any_yes": False}

    say_rows = []
    last_pre_state = None
    for turn in fixture.turns:
        if turn.cold:
            state = hydrate(reader)
        call_state = last_pre_state if turn.resend else state
        call_state["now"] = turn.now
        call_state["message_id"] = turn.message_id
        if turn.rest_node_label is not None:
            call_state["program"]["rotation"].append(
                {"id": "REST", "label": turn.rest_node_label, "blocks": []})
        turn_fn, say_key = SEAMS[turn.skill]
        result = turn_fn(turn.line, call_state)
        if not turn.resend:
            last_pre_state = call_state
        # The s3.2 ceiling bounds exercise-resolution cost (build-plan s3.2);
        # it does not apply to `intake`'s one-time, multi-write
        # database-creation turn (build-plan s5.1), which runs once at
        # install, off the budget.
        if turn.skill == "session-runner":
            resolution_writes = sum(1 for w in result["writes"] if w["target"] == "Exercises")
            set_rows = sum(1 for w in result["writes"] if w["target"] == "Sets")
            if resolution_writes > MAX_RESOLUTION_WRITES_PER_TURN:
                raise AssertionError(
                    f"{turn.message_id} {turn.line!r}: {resolution_writes} Exercises "
                    f"creates exceeds the s3.2 round-trip ceiling of {MAX_RESOLUTION_WRITES_PER_TURN}")
            if set_rows > MAX_SET_ROWS_PER_TURN:
                raise AssertionError(
                    f"{turn.message_id} {turn.line!r}: {set_rows} Sets rows "
                    f"exceeds the sanity ceiling of {MAX_SET_ROWS_PER_TURN}")
        created: dict[str, str] = {}
        for write in result["writes"]:
            if write["verb"] == "row-create":
                notion.row_create(write["target"], write["payload"])
            elif write["verb"] == "config-write":
                for key, value in write["payload"].items():
                    notion.config_write(write["target"], key, value)
            elif write["verb"] == "database-create":
                created[write["target"]] = notion.database_create(
                    write["target"], write["payload"])
            else:
                raise ValueError(f"unknown write verb {write['verb']!r}")
        state = result["state"]
        # `notion-create-database` answers with the new data source id, and
        # the next database's relation columns need it. Threading it back is
        # the caller's job: a seam is a pure function of (line, state) and
        # never sees a response.
        state.setdefault("databases", {}).update(created)
        say_rows.append(
            f"say\t{turn.skill}\t{turn.message_id}\t{json.dumps(result[say_key])}\n")

    return say_rows


def run_fixture(fixture_dir: Path, update: bool = False) -> int:
    """Replay one fixture directory. 0 = actual.tsv matches expected.tsv.

    `update` rewrites expected.tsv from the run instead of comparing, so no
    expectation is ever hand computed.
    """
    fixture = parse_transcript((fixture_dir / "transcript.txt").read_text())
    expected_path = fixture_dir / "expected.tsv"
    expected = expected_path.read_text()

    with tempfile.TemporaryDirectory() as tmp:
        out_path = Path(tmp) / "actual.tsv"
        notion = writer.MockNotion(out_path)
        say_rows = replay(fixture, notion)
        actual = out_path.read_text() or "\t".join(writer.TSV_HEADER) + "\n"
    actual += "".join(say_rows)

    if update:
        expected_path.write_text(actual)
        return 0

    if actual == expected:
        return 0

    diff = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile="expected.tsv",
        tofile="actual.tsv",
    )
    sys.stdout.writelines(diff)
    return 1


def main(argv: list[str]) -> int:
    """CLI entry: one fixture directory per invocation, `--update` to rewrite."""
    dirs = [a for a in argv if a != "--update"]
    if len(dirs) != 1:
        print("usage: replay.py [--update] <fixture-dir>", file=sys.stderr)
        return 2
    return run_fixture(Path(dirs[0]), update="--update" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
