#!/usr/bin/env python3
"""Validate every skill under skills/<family>/<skill-name>/.

Checks, per skill:
  1. SKILL.md exists
  2. YAML frontmatter parses and is delimited correctly
  3. `name` matches the directory name exactly, and is lowercase
     alphanumeric plus single internal hyphens, 1-64 chars
  4. `description` present, 1-1024 chars, single logical line
  5. `description` ends with an explicit DO NOT clause (cross-family guard)
  6. Every relative markdown/backtick path referenced from SKILL.md resolves
  7. SKILL.md body stays within the size budget

Exit code 0 = all pass, 1 = at least one error.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BODY_BUDGET = 20000  # characters; ~5k tokens
DESC_MAX = 1024

# `references/foo.md`, `assets/bar.sv`, scripts/baz.py in backticks
PATH_RE = re.compile(r"`((?:references|assets|scripts)/[A-Za-z0-9_./-]+)`")

errors: list[str] = []
warnings: list[str] = []


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        raise ValueError("SKILL.md does not begin with '---' frontmatter delimiter")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("frontmatter is not closed with '---'")
    raw = text[3:end].strip("\n")
    body = text[end + 4 :]

    fields: dict[str, str] = {}
    key = None
    for line in raw.split("\n"):
        m = re.match(r"^([a-z][a-z0-9_-]*):\s*(.*)$", line)
        if m and not line.startswith(" "):
            key = m.group(1)
            fields[key] = m.group(2).strip()
        elif key is not None:
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields, body


def check(skill_dir: Path) -> None:
    rel = skill_dir.relative_to(ROOT)
    md = skill_dir / "SKILL.md"
    if not md.exists():
        errors.append(f"{rel}: no SKILL.md")
        return

    text = md.read_text(encoding="utf-8")
    try:
        fields, body = split_frontmatter(text)
    except ValueError as exc:
        errors.append(f"{rel}: {exc}")
        return

    name = fields.get("name", "").strip().strip("\"'")
    if not name:
        errors.append(f"{rel}: frontmatter is missing `name`")
    else:
        if name != skill_dir.name:
            errors.append(f"{rel}: name '{name}' != directory '{skill_dir.name}'")
        if not NAME_RE.match(name):
            errors.append(f"{rel}: name '{name}' must be lowercase alphanumeric with single hyphens")
        if len(name) > 64:
            errors.append(f"{rel}: name is {len(name)} chars, limit 64")

    desc = fields.get("description", "").strip()
    desc = re.sub(r"^[>|][-+]?\s*", "", desc).strip()
    if not desc:
        errors.append(f"{rel}: frontmatter is missing `description`")
    else:
        if len(desc) > DESC_MAX:
            errors.append(f"{rel}: description is {len(desc)} chars, limit {DESC_MAX}")
        if "\n" in desc:
            errors.append(f"{rel}: description must fold to a single logical line")
        upper = desc.upper()
        if not any(g in upper for g in ("DO NOT", "NOT FOR", "NEVER FOR")):
            errors.append(
                f"{rel}: description has no explicit negative guard clause "
                "('DO NOT use for ...' / 'Not for ...') "
                "— required to stop cross-family collisions"
            )

    if len(body) > BODY_BUDGET:
        warnings.append(f"{rel}: body is {len(body)} chars, over the {BODY_BUDGET} budget")

    for ref in sorted(set(PATH_RE.findall(text))):
        if "<" in ref or ref.endswith("/"):
            continue  # placeholder such as references/ai_models/<model>.md
        if not (skill_dir / ref).exists():
            errors.append(f"{rel}: SKILL.md references missing path '{ref}'")


def main() -> int:
    if not SKILLS.is_dir():
        print("no skills/ directory found", file=sys.stderr)
        return 1

    skill_dirs = sorted(p.parent for p in SKILLS.glob("*/*/SKILL.md"))
    stray = sorted(p for p in SKILLS.glob("*/*") if p.is_dir() and not (p / "SKILL.md").exists())
    for p in stray:
        errors.append(f"{p.relative_to(ROOT)}: directory under skills/ has no SKILL.md")

    for d in skill_dirs:
        check(d)

    families = sorted({d.parent.name for d in skill_dirs})
    print(f"validated {len(skill_dirs)} skills across {len(families)} families: {', '.join(families)}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if errors:
        print(f"\n{len(errors)} error(s)")
        return 1
    print("all skills valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
