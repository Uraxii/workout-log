"""Validate library/*.json against schema/program-schema.json (stdlib only).
Handles the keywords that schema uses: $ref, type, required, properties, items, enum, oneOf."""
import json, pathlib, sys

TYPES = {"object": dict, "array": list, "string": str, "integer": int,
         "number": (int, float), "boolean": bool}


def check(node: object, schema: dict, root: dict, at: str) -> list[str]:
    if "$ref" in schema:
        target = root
        for part in schema["$ref"].removeprefix("#/").split("/"):
            target = target[part]
        return check(node, target, root, at)
    if "type" in schema and not isinstance(node, TYPES[schema["type"]]):
        return [f"{at}: expected {schema['type']}, got {type(node).__name__}"]
    off_enum = "enum" in schema and node not in schema["enum"]
    bad = [f"{at}: {node!r} not in {schema['enum']}"] if off_enum else []
    if isinstance(node, dict):
        bad += [f"{at}: missing {k!r}" for k in schema.get("required", ()) if k not in node]
        for key, sub in schema.get("properties", {}).items():
            if key in node:
                bad += check(node[key], sub, root, f"{at}.{key}")
        alts = schema.get("oneOf", ())
        if alts and sum(all(k in node for k in a["required"]) for a in alts) != 1:
            bad.append(f"{at}: needs exactly one of {[a['required'] for a in alts]}")
    if isinstance(node, list) and "items" in schema:
        for i, item in enumerate(node):
            bad += check(item, schema["items"], root, f"{at}[{i}]")
    return bad


here = pathlib.Path(__file__).resolve().parent
top = json.loads((here.parent / "schema/program-schema.json").read_text())
files = sorted(here.glob("*.json"))
bad = {p.name: check(json.loads(p.read_text()), top, top, p.stem) for p in files}
for name, errors in bad.items():
    print(f"{name}: {'FAIL' if errors else 'ok'}", *[f"\n  {e}" for e in errors])
sys.exit(1 if any(bad.values()) else 0)
