#!/usr/bin/env python3
"""Zip every .claude/skills/<name> dir into dist/workout-skills.zip.

Each skill lands at the ZIP root as <name>/... so claude.ai's Customize >
Skills upload sees one top-level folder per skill with SKILL.md inside
(research/13-plugin-packaging.md s6). Rerunnable: always rewrites the same
entries for the same skill dirs.

The data a skill reads at runtime lives once at the repo root, shared. An
extracted ZIP has no repo around it, so every skill that reads one of those
files gets its own copy under <name>/data/<repo-root path> and resolves
that first (workout-log-d2y, build-plan s8).

    python3 tools/package/build_zip.py
"""
from __future__ import annotations

import os
import sys
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
DIST_ZIP = REPO_ROOT / "dist" / "workout-skills.zip"
SKIP_DIRS = {"__pycache__"}

# Repo-root globs per skill, matching what each skill's scripts actually read:
# library.py -> library/, rows.py -> schema/, catalog.py -> exercises/,
# intake's ddl.py -> schema/.
BUNDLED_DATA = {
    "intake": ("schema/notion-schema.json",),
    "program-design": ("library/*.json",),
    "session-runner": (
        "exercises/aliases.json",
        "exercises/catalog.json",
        "schema/notion-schema.json",
    ),
}


def skill_dirs() -> list[Path]:
    """Every .claude/skills/<name> dir that has a SKILL.md."""
    return sorted(
        p for p in SKILLS_DIR.iterdir()
        if p.is_dir() and (p / "SKILL.md").exists()
    )


def skill_files(skill_dir: Path) -> list[Path]:
    """Every file under skill_dir, excluding cache dirs."""
    return [
        p for p in skill_dir.rglob("*")
        if p.is_file()
        and not SKIP_DIRS & set(p.relative_to(skill_dir).parts)
    ]


def data_files(skill_name: str) -> list[tuple[Path, str]]:
    """(source, arcname) for every runtime data file skill_name needs."""
    bundled = []
    for pattern in BUNDLED_DATA.get(skill_name, ()):
        matches = sorted(REPO_ROOT.glob(pattern))
        if not matches:
            sys.exit(f"{skill_name}: {pattern} matches nothing under {REPO_ROOT}")
        bundled += [
            (m, f"{skill_name}/data/{m.relative_to(REPO_ROOT)}") for m in matches
        ]
    return bundled


def main() -> None:
    dirs = skill_dirs()
    DIST_ZIP.parent.mkdir(exist_ok=True)
    bundled = 0
    # ponytail: os.replace is atomic on POSIX only within one filesystem, so
    # the temp file must live in DIST_ZIP's own dir (never /tmp). Same fix
    # as tools/catalog/build.py, same reason: a concurrent make check reads
    # this zip while another run rewrites it.
    fd, tmp_path = tempfile.mkstemp(dir=DIST_ZIP.parent, suffix=".zip.tmp")
    try:
        os.close(fd)
        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for skill_dir in dirs:
                for f in skill_files(skill_dir):
                    arcname = f"{skill_dir.name}/{f.relative_to(skill_dir)}"
                    zf.write(f, arcname=arcname)
                for source, arcname in data_files(skill_dir.name):
                    zf.write(source, arcname=arcname)
                    bundled += 1
        os.replace(tmp_path, DIST_ZIP)
    except BaseException:
        os.unlink(tmp_path)
        raise
    names = ", ".join(d.name for d in dirs)
    print(f"wrote {DIST_ZIP} with {len(dirs)} skill(s): {names}")
    print(f"bundled {bundled} data file(s) under <skill>/data/")


if __name__ == "__main__":
    main()
