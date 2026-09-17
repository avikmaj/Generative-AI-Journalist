#!/usr/bin/env python3
"""Render the Grok project bundle into dist/grok/.

Grok projects take a single instructions block plus uploaded files, and are the
tightest of the three on instruction length. The builder therefore emits one
compressed instruction file with a router, and one consolidated knowledge file
per family rather than per skill. Run scripts/validate_skills.py first.
"""
from __future__ import annotations

import sys
from collections import defaultdict

from _bundle_lib import ROOT, collect_markdown, discover_skills, flatten, report, reset_dist, write


def main() -> int:
    skills = discover_skills()
    if not skills:
        print("no skills found", file=sys.stderr)
        return 1

    target = reset_dist("grok")
    by_family: dict[str, list] = defaultdict(list)
    for s in skills:
        by_family[s.family].append(s)

    # 1. One knowledge file per family, so the upload count stays small.
    for family, members in sorted(by_family.items()):
        sections = [
            f"# {family.upper()} family — consolidated knowledge\n",
            f"Contains {len(members)} skill(s). Each skill begins at a `# Skill:` heading.\n",
        ]
        for s in members:
            for _, content in flatten(s):
                sections.append("\n\n" + content)
        write(target / f"GROK_KNOWLEDGE_{family.upper()}.md", "".join(sections))

    # 2. Instructions: the canonical Grok instructions plus a generated router.
    src = ROOT / "platforms" / "grok" / "project-instructions.md"
    text = src.read_text(encoding="utf-8") if src.exists() else ""
    rows = ["| Request looks like | Skill | Knowledge file |", "|---|---|---|"]
    for s in skills:
        trigger = s.description.split(".")[0]
        rows.append(
            f"| {trigger[:120]} | `{s.name}` | `GROK_KNOWLEDGE_{s.family.upper()}.md` |"
        )
    text += (
        "\n\n---\n\n## Generated skill router — do not edit by hand\n\n"
        "Open the family knowledge file and jump to the `# Skill: <name>` heading.\n\n"
        + "\n".join(rows)
        + "\n"
    )
    write(target / "project-instructions.md", text)

    # 3. The VIP factory team rules stay a standalone upload — they are the
    #    governing document and must not be buried inside a family file.
    rules = ROOT / "platforms" / "grok" / "dv-vip-factory-team-rules.md"
    if rules.exists():
        write(target / "dv-vip-factory-team-rules.md", rules.read_text(encoding="utf-8"))

    write(target / "MODEL_CARD.md", (ROOT / "model" / "MODEL_CARD.md").read_text(encoding="utf-8"))
    prompts = collect_markdown(ROOT / "prompts", "Reusable task prompts")
    if prompts:
        write(target / "PROMPTS.md", prompts)

    files = sorted(p.name for p in target.iterdir() if p.is_file())
    lines = [
        "# Grok project bundle",
        "",
        "## Upload steps",
        "",
        "1. Paste `project-instructions.md` into the project instructions.",
        "2. Upload the remaining files to the project.",
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
