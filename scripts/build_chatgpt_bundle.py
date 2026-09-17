#!/usr/bin/env python3
"""Render a five-upload ChatGPT Custom GPT bundle into dist/chatgpt/."""
from __future__ import annotations

import sys
from collections import defaultdict

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

    target = reset_dist("chatgpt")
    families = sorted({s.family for s in skills})
    for family in families:
        write(target / f"FAMILY_{family.upper()}.md", family_bundle(family, skills))

    # Keep policy and reusable prompts in one fifth upload.
    control = (ROOT / "model" / "MODEL_CARD.md").read_text(encoding="utf-8")
    prompts = collect_markdown(ROOT / "prompts", "Reusable task prompts")
    write(target / "CONTROL.md", control + "\n\n---\n\n" + prompts)

    # Compact instructions plus generated router. Hard-fail before the UI does.
    src = ROOT / "platforms" / "chatgpt" / "system-prompt.md"
    prompt = src.read_text(encoding="utf-8") if src.exists() else ""
    prompt += "\n\n---\n\n" + compact_skill_router(
        skills, lambda s: f"FAMILY_{s.family.upper()}.md"
    ) + "\n"
    if len(prompt) > MAX_INSTRUCTION_CHARS:
        print(f"ChatGPT instructions exceed {MAX_INSTRUCTION_CHARS}: {len(prompt)}", file=sys.stderr)
        return 2
    write(target / "system-prompt.md", prompt)

    # Manifest is documentation, not an upload.
    files = sorted(p.name for p in target.iterdir() if p.is_file() and p.name != "system-prompt.md")
    if len(files) != MAX_UPLOAD_FILES:
        print(f"ChatGPT upload count must be {MAX_UPLOAD_FILES}, got {len(files)}", file=sys.stderr)
        return 3
    lines = [
        "# ChatGPT Custom GPT bundle",
        "",
        "## Upload steps",
        "",
        "1. Paste `system-prompt.md` into Configure → Instructions.",
        "2. Upload the four `FAMILY_*.md` files and `CONTROL.md` as Knowledge.",
        "3. Add `platforms/chatgpt/actions/openapi.example.yaml` under Actions if you need tools.",
        "",
        f"**Knowledge uploads: {len(files)}. Instruction characters: {len(prompt)}.**",
        "",
        "| File | KB |",
        "|---|---|",
    ]
    for name in files:
        lines.append(f"| `{name}` | {(target / name).stat().st_size / 1024:.0f} |")
    write(target / "MANIFEST.md", "\n".join(lines) + "\n")

    report("chatgpt", target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
