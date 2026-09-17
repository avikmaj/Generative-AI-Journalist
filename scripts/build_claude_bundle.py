#!/usr/bin/env python3
"""Render the Claude Project bundle into dist/claude/.

Claude supports native Agent Skills and nested file references, so skills are
copied whole — SKILL.md plus references/, assets/ and scripts/ — with no
flattening. Run scripts/validate_skills.py first.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from _bundle_lib import ROOT, discover_skills, report, reset_dist, write


def main() -> int:
    skills = discover_skills()
    if not skills:
        print("no skills found", file=sys.stderr)
        return 1

    target = reset_dist("claude")

    # 1. Project instructions — pasted into the Claude Project's instructions box.
    src = ROOT / "platforms" / "claude" / "project-instructions.md"
    if src.exists():
        write(target / "project-instructions.md", src.read_text(encoding="utf-8"))

    claude_md = ROOT / "platforms" / "claude" / "CLAUDE.md"
    if claude_md.exists():
        write(target / "CLAUDE.md", claude_md.read_text(encoding="utf-8"))

    # 2. Skills, copied whole — Claude reads references/ on demand.
    for s in skills:
        shutil.copytree(s.path, target / "skills" / s.name)

    # 3. Committed knowledge only. Licensed corpora are git-ignored and are
    #    resolved through .gitignore rather than re-listed here.
    ignored = _git_ignored()
    for src_file in sorted((ROOT / "knowledge").rglob("*")):
        if not src_file.is_file():
            continue
        rel = src_file.relative_to(ROOT)
        if rel.as_posix() in ignored:
            continue
        shutil.copy2(src_file, _ensure(target / rel))

    # 4. Manifest so the upload order is reproducible.
    lines = [
        "# Claude Project bundle",
        "",
        f"Rendered from `model/VERSION` {(ROOT / 'model' / 'VERSION').read_text().strip()}.",
        "",
        "## Upload steps",
        "",
        "1. Paste `project-instructions.md` into the Project's custom instructions.",
        "2. Upload each `skills/<name>/` directory as an Agent Skill.",
        "3. Add `knowledge/` files as Project knowledge.",
        "",
        "## Skills in this bundle",
        "",
        "| Family | Skill | References | Assets |",
        "|---|---|---|---|",
    ]
    for s in skills:
        lines.append(f"| `{s.family}` | `{s.name}` | {len(s.references)} | {len(s.assets)} |")
    write(target / "MANIFEST.md", "\n".join(lines) + "\n")

    report("claude", target)
    return 0


def _ensure(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _git_ignored() -> set[str]:
    """Paths under knowledge/ that git ignores — never ship licensed material."""
    import subprocess

    try:
        out = subprocess.run(
            ["git", "ls-files", "--others", "--ignored", "--exclude-standard", "knowledge"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return set(out.stdout.split())
    except Exception:
        return set()


if __name__ == "__main__":
    sys.exit(main())
