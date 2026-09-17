#!/usr/bin/env python3
"""Render the ChatGPT Custom GPT bundle into dist/chatgpt/.

A Custom GPT has no native skills mechanism and no nested file references, so:
  - the skill router is inlined into the system prompt
  - each skill is flattened into one knowledge file (split when very large)
  - prompts and evals are consolidated into single files
Run scripts/validate_skills.py first.
"""
from __future__ import annotations

import sys

from _bundle_lib import (
    ROOT,
    collect_markdown,
    discover_skills,
    flatten,
    report,
    reset_dist,
    skill_index_table,
    write,
)


def main() -> int:
    skills = discover_skills()
    if not skills:
        print("no skills found", file=sys.stderr)
        return 1

    target = reset_dist("chatgpt")
    rendered: dict[str, list[str]] = {}

    # 1. Flattened skills as knowledge files.
    for s in skills:
        names = []
        for filename, content in flatten(s):
            write(target / filename, content)
            names.append(filename)
        rendered[s.slug] = names

    # 2. System prompt with the generated router appended, so the router can
    #    never drift from what was actually uploaded.
    src = ROOT / "platforms" / "chatgpt" / "system-prompt.md"
    prompt = src.read_text(encoding="utf-8") if src.exists() else ""
    table = skill_index_table(skills, lambda s: rendered[s.slug][0])
    prompt += (
        "\n\n---\n\n## Generated skill router — do not edit by hand\n\n"
        "Silently pick the matching skill and open its knowledge file before answering. "
        "If a skill was split into parts, part 1 carries the procedure; open later parts only "
        "when you need a specific reference module.\n\n" + table + "\n"
    )
    write(target / "system-prompt.md", prompt)

    # 3. Supporting canonical documents.
    write(target / "MODEL_CARD.md", (ROOT / "model" / "MODEL_CARD.md").read_text(encoding="utf-8"))

    prompts = collect_markdown(ROOT / "prompts", "Reusable task prompts")
    if prompts:
        write(target / "PROMPTS.md", prompts)

    evals = collect_markdown(ROOT / "evals", "Evaluation rubric")
    if evals:
        write(target / "EVALS.md", evals)

    for family in ("dv", "business", "film"):
        doc = collect_markdown(ROOT / "knowledge" / family, f"{family.upper()} knowledge index")
        if doc:
            write(target / f"KNOWLEDGE_{family.upper()}.md", doc)

    # 4. Manifest — Custom GPTs cap the number of knowledge files, so the count matters.
    files = sorted(p.name for p in target.iterdir() if p.is_file() and p.name != "system-prompt.md")
    lines = [
        "# ChatGPT Custom GPT bundle",
        "",
        "## Upload steps",
        "",
        "1. Paste `system-prompt.md` into Configure → Instructions.",
        "2. Upload every other file in this directory as Knowledge.",
        "3. Add `platforms/chatgpt/actions/openapi.example.yaml` under Actions if you need tools.",
        "",
        f"**Knowledge files: {len(files)}.** Custom GPTs cap knowledge file count — if you exceed it,",
        "drop the `KNOWLEDGE_*.md` indexes first, then the largest split skill parts.",
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
