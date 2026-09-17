#!/usr/bin/env python3
"""Render the Grok project bundle into dist/grok/.

Grok projects take a single instructions block plus uploaded files, and are the
tightest of the three on instruction length. The builder therefore emits one
compressed instruction file with a router, and one consolidated knowledge file
per family rather than per skill. Run scripts/validate_skills.py first.
"""
from __future__ import annotations

import sys
from _bundle_lib import (
    ROOT,
    collect_markdown,
    compact_skill_router,
    discover_skills,
    family_bundle,
    report,
    reset_dist,
    write,
)

MAX_INSTRUCTION_CHARS = 4_000
MAX_UPLOAD_FILES = 5


def main() -> int:
    skills = discover_skills()
    if not skills:
        print("no skills found", file=sys.stderr)
        return 1

    target = reset_dist("grok")
    # 1. Four family uploads.
    families = sorted({s.family for s in skills})
    for family in families:
        write(target / f"FAMILY_{family.upper()}.md", family_bundle(family, skills))

    # 2. Instructions: the canonical Grok instructions plus a generated router.
    src = ROOT / "platforms" / "grok" / "project-instructions.md"
    text = src.read_text(encoding="utf-8") if src.exists() else ""
    text += "\n\n---\n\n" + compact_skill_router(
        skills, lambda s: f"FAMILY_{s.family.upper()}.md"
    ) + "\n"
    if len(text) > MAX_INSTRUCTION_CHARS:
        print(f"Grok instructions exceed {MAX_INSTRUCTION_CHARS}: {len(text)}", file=sys.stderr)
        return 2
    write(target / "project-instructions.md", text)

    # 3. One control upload: global policy, prompts, and governing VIP rules.
    rules = ROOT / "platforms" / "grok" / "dv-vip-factory-team-rules.md"
    control = (ROOT / "model" / "MODEL_CARD.md").read_text(encoding="utf-8")
    prompts = collect_markdown(ROOT / "prompts", "Reusable task prompts")
    control += "\n\n---\n\n" + prompts
    if rules.exists():
        control += "\n\n---\n\n# Governing VIP team rules\n\n" + rules.read_text(encoding="utf-8")
    write(target / "CONTROL.md", control)

    files = sorted(
        p.name for p in target.iterdir()
        if p.is_file() and p.name != "project-instructions.md"
    )
    if len(files) != MAX_UPLOAD_FILES:
        print(f"Grok upload count must be {MAX_UPLOAD_FILES}, got {len(files)}", file=sys.stderr)
        return 3
    lines = [
        "# Grok project bundle",
        "",
        "## Upload steps",
        "",
        "1. Paste `project-instructions.md` into the project instructions.",
        "2. Upload the four `FAMILY_*.md` files and `CONTROL.md`.",
        "",
        f"**Uploads: {len(files)}. Instruction characters: {len(text)}.**",
        "",
        "| File | KB |",
        "|---|---|",
    ]
    for name in files:
        lines.append(f"| `{name}` | {(target / name).stat().st_size / 1024:.0f} |")
    write(target / "MANIFEST.md", "\n".join(lines) + "\n")

    report("grok", target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
