#!/usr/bin/env python3
"""Zip each skill for upload to Claude's Agent Skills UI.

Claude accepts one zip per skill, with SKILL.md at the archive root. Run
build_claude_bundle.py first; this packages what that produced.

Writes dist/claude/skill-zips/<skill-name>.zip
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "dist" / "claude" / "skills"
OUT = ROOT / "dist" / "claude" / "skill-zips"


def main() -> int:
    if not SRC.is_dir():
        print("run scripts/build_claude_bundle.py first", file=sys.stderr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.zip"):
        old.unlink()

    total = 0
    for skill_dir in sorted(p for p in SRC.iterdir() if p.is_dir()):
        if not (skill_dir / "SKILL.md").exists():
            print(f"skipping {skill_dir.name}: no SKILL.md", file=sys.stderr)
            continue
        target = OUT / f"{skill_dir.name}.zip"
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
                # SKILL.md must sit at the archive root, not under a folder.
                z.write(f, f.relative_to(skill_dir).as_posix())
        total += 1
        print(f"  {target.name:38s} {target.stat().st_size / 1024:6.0f} KB")

    print(f"\npackaged {total} skills -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
