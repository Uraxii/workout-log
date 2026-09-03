"""Prove `Sets.e1RM`'s Notion formula and `read_layer.e1rm` are one truth.

`docs/unit-and-magnitude-model.md` s2 settles that there is exactly one e1RM
relation, exact Brzycki `Load * 36 / (37 - Reps)`, null off the validated
range. The Notion formula and the Python read layer are two renderings of it,
written by hand in two languages, so a document saying "these must agree" is
the thing that already failed twice (workout-log-8ms, -8jb). This is the
mechanism that replaces the document (`principle-encode-lessons-in-structure`).

Comparison, not generation: Python cannot be generated from a Notion formula
string, so a swept comparison is the only direction that survives either side
being edited (s2, "How the agreement is enforced").

The evaluator below reads the schema's `expression` string, so a formula edit
is checked without touching this file. Notion's expression grammar overlaps
Python's for everything the expression uses (`prop("Name")` calls, `* / + -`,
`== != < <= > >=`, `and`/`or`/`not`, string and number literals), with one
collision: Notion's `if(cond, a, b)` is a call and `if` is a Python keyword,
so `if(` is rewritten to `if_(` before parsing. `if_` is evaluated lazily,
which is what makes a guard a guard; see NOTION SYNTAX in the module's
sibling notes:

    if(cond, a, b)   <https://developers.notion.com/reference/property-object#formula>
                     <https://www.notion.com/help/formula-syntax>
    empty()          <https://www.notion.com/help/common-formula-errors>

Run it:

    python3 tools/schema/check_e1rm.py
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT / ".claude" / "skills" / "load-adjust" / "scripts"))
import read_layer  # noqa: E402  (the Python rendering under comparison)

SCHEMA_PATH = _ROOT / "schema" / "notion-schema.json"

# `loads._FLOOR_TOLERANCE`'s reasoning, reused: one part in a billion is far
# below any loadable increment and far above float error on this arithmetic.
TOLERANCE = 1e-9

# Every rep count the check must cover. 1 and 10 bound Brzycki's validated
# range, 11 and 36 are the window where an unguarded formula shows a number
# the Python nulls, 37 is the divide by zero, 38 goes negative, and 100 is
# the ceiling `session-runner/scripts/bounds.py` permits.
REPS = (0, 1, 2, 5, 10, 11, 36, 37, 38, 100)
# 0 and 1000 are `bounds.py`'s ends. 100 leads so the example load in a
# reported failure carries a visible magnitude: at Load 0 every wrong answer
# prints as 0.0 and the reader learns nothing from it.
LOADS = (100.0, 0.0, 1.0, 315.0, 1000.0)

_BINOP = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b,
          ast.Mult: lambda a, b: a * b, ast.Div: lambda a, b: a / b}
_COMPARE = {ast.Eq: lambda a, b: a == b, ast.NotEq: lambda a, b: a != b,
            ast.Lt: lambda a, b: a < b, ast.LtE: lambda a, b: a <= b,
            ast.Gt: lambda a, b: a > b, ast.GtE: lambda a, b: a >= b}


class FormulaError(ValueError):
    """The expression uses something this evaluator will not guess at."""


def evaluate(expression: str, row: dict[str, Any]) -> Any:
    """One Notion formula expression against one `Sets`-row-shaped dict.

    `None` is Notion's empty value. Raises `ZeroDivisionError` when the
    expression actually divides by zero, which is a finding, not a crash.
    """
    tree = ast.parse(re.sub(r"\bif\(", "if_(", expression), mode="eval")
    return _eval(tree.body, row)


def _eval(node: ast.AST, row: dict[str, Any]) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINOP:
        return _BINOP[type(node.op)](_eval(node.left, row), _eval(node.right, row))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval(node.operand, row)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return not _eval(node.operand, row)
    if isinstance(node, ast.BoolOp):
        values = [_eval(value, row) for value in node.values]
        return all(values) if isinstance(node.op, ast.And) else any(values)
    if isinstance(node, ast.Compare) and len(node.ops) == 1:
        operator = _COMPARE.get(type(node.ops[0]))
        if operator is not None:
            return operator(_eval(node.left, row), _eval(node.comparators[0], row))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return _call(node, row)
    raise FormulaError(f"unsupported expression node {ast.dump(node)}")


def _call(node: ast.Call, row: dict[str, Any]) -> Any:
    name = node.func.id
    if name == "prop" and len(node.args) == 1:
        return row.get(_eval(node.args[0], row))
    if name == "empty" and not node.args:
        return None  # `empty()` is Notion's empty value (common-formula-errors)
    if name == "if_" and len(node.args) == 3:
        # Lazily, so the untaken branch's arithmetic is never performed. This
        # is what a guard means, and it is the shape Notion's own docs
        # prescribe: `if(Date, Date.dateAdd(1, "day"), empty())`.
        chosen = node.args[1] if _eval(node.args[0], row) else node.args[2]
        return _eval(chosen, row)
    raise FormulaError(f"unsupported function {name}({len(node.args)} args)")


def _schema_value(expression: str, row: dict[str, Any]) -> tuple[Any, str | None]:
    """The formula's answer, or the reason it has none."""
    try:
        return evaluate(expression, row), None
    except ZeroDivisionError:
        return None, "divide by zero"


def disagreements(expression: str, set_types: tuple[str, ...]) -> list[str]:
    """One line per (Set type, Reps) the two renderings answer differently,
    naming the first `Load` that showed it. Divide by zero sorts first: it is
    the failure that says the formula has no guard at all."""
    failures: list[tuple[int, str]] = []
    for set_type in set_types:
        for reps in REPS:
            for load in LOADS:
                row = {"Load": load, "Reps": reps, "Set type": set_type}
                schema, fault = _schema_value(expression, row)
                python = read_layer.e1rm(load, reps, set_type)
                if fault is None and _agrees(schema, python):
                    continue
                failures.append((0 if fault else 1, (
                    f'Set type={set_type} Reps={reps} Load={load:g}: '
                    f'schema {fault or schema!r}, python {python!r}')))
                break
    return [line for _, line in sorted(failures, key=lambda pair: pair[0])]


def _agrees(schema: Any, python: float | None) -> bool:
    if schema is None or python is None:
        return schema is None and python is None
    return abs(schema - python) <= TOLERANCE


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text())
    sets = schema["databases"]["Sets"]["properties"]
    expression = sets["e1RM"]["expression"]
    set_types = tuple(sets["Set type"]["enum"])
    print(f"e1RM expression: {expression}")
    failures = disagreements(expression, set_types)
    if failures:
        print(f"FAIL: {len(failures)} (Set type, Reps) pair(s) disagree "
              f"with read_layer.e1rm (tolerance {TOLERANCE:g}):")
        print("\n".join(f"  {line}" for line in failures))
        return 1
    print(f"check_e1rm: ok. {len(set_types) * len(REPS) * len(LOADS)} rows agree "
          f"within {TOLERANCE:g}, reps {REPS[0]}-{REPS[-1]}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
