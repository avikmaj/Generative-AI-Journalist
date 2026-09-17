"""Shared discovery and rendering helpers for the platform bundle builders.

Every builder reads the same canonical sources — model/, skills/, knowledge/,
prompts/, evals/ — and writes only into dist/<platform>/. dist/ is generated and
git-ignored; nothing here ever writes back into the canonical tree.
"""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

# Flattened knowledge files larger than this are split into numbered parts, so a
# single upload never becomes unusable in a platform with per-file limits.
MAX_FLAT_CHARS = 280_000


@dataclass
class Skill:
    family: str
    name: str
    path: Path
    description: str = ""
    body: str = ""
    references: list[Path] = field(default_factory=list)
    assets: list[Path] = field(default_factory=list)
    scripts: list[Path] = field(default_factory=list)

    @property
    def slug(self) -> str:
        return f"{self.family}_{self.name}"


def _frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw, body = text[3:end], text[end + 4 :]
    fields: dict[str, str] = {}
    key = None
    for line in raw.strip("\n").split("\n"):
        m = re.match(r"^([a-z][a-z0-9_-]*):\s*(.*)$", line)
        if m and not line.startswith(" "):
            key = m.group(1)
            fields[key] = m.group(2).strip()
        elif key is not None:
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields, body.lstrip("\n")


def discover_skills() -> list[Skill]:
    """Every skill in skills/<family>/<name>/, sorted by family then name."""
    skills: list[Skill] = []
    for md in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        d = md.parent
        fields, body = _frontmatter(md.read_text(encoding="utf-8"))
        desc = re.sub(r"^[>|][-+]?\s*", "", fields.get("description", "")).strip()
        skills.append(
            Skill(
                family=d.parent.name,
                name=d.name,
                path=d,
                description=desc,
                body=body,
                references=sorted(p for p in (d / "references").rglob("*") if p.is_file()),
                assets=sorted(p for p in (d / "assets").rglob("*") if p.is_file()),
                scripts=sorted(p for p in (d / "scripts").rglob("*") if p.is_file()),
            )
        )
    return skills


def flatten(skill: Skill) -> list[tuple[str, str]]:
    """Render a skill as self-contained markdown for platforms without nested files.

    Returns [(filename, content), ...] — more than one entry when the skill is
    large enough to need splitting.
    """
    header = (
        f"# Skill: {skill.name}\n\n"
        f"**Family:** `{skill.family}`  \n"
        f"**When to use:** {skill.description}\n\n"
        "> Flattened for platforms without nested file references. Reference modules that were\n"
        "> separate files appear below as `## Reference: <path>` sections. Where the skill body\n"
        "> points at `references/<path>`, read that section here instead.\n\n---\n\n"
    )

    chunks: list[tuple[str, str]] = []
    for ref in skill.references:
        rel = ref.relative_to(skill.path).as_posix()
        if ref.suffix.lower() not in {".md", ".txt", ".yaml", ".yml", ".sv", ".svh", ".py"}:
            continue
        text = ref.read_text(encoding="utf-8", errors="replace")
        if ref.suffix.lower() not in {".md", ".txt"}:
            lang = {".sv": "systemverilog", ".svh": "systemverilog", ".py": "python"}.get(
                ref.suffix.lower(), "yaml"
            )
            text = f"```{lang}\n{text}\n```"
        chunks.append((rel, text))

    parts: list[list[str]] = [[]]
    size = len(header) + len(skill.body)
    for rel, text in chunks:
        block = f"\n\n---\n\n## Reference: {rel}\n\n{text}"
        if size + len(block) > MAX_FLAT_CHARS and parts[-1]:
            parts.append([])
            size = len(header)
        parts[-1].append(block)
        size += len(block)

    out: list[tuple[str, str]] = []
    total = len(parts)
    for i, blocks in enumerate(parts, start=1):
        suffix = "" if total == 1 else f"_part{i}of{total}"
        note = "" if total == 1 else (
            f"\n> **Part {i} of {total}.** The skill body appears in part 1 only; "
            "reference modules are split across parts.\n"
        )
        content = header + note + (skill.body if i == 1 else "") + "".join(blocks) + "\n"
        out.append((f"SKILL_{skill.slug}{suffix}.md", content))
    return out


def skill_index_table(skills: list[Skill], filename_for) -> str:
    """A markdown router table mapping each skill to its uploaded knowledge file."""
    rows = ["| Family | Skill | Load this file | When |", "|---|---|---|---|"]
    for s in skills:
        rows.append(f"| `{s.family}` | `{s.name}` | `{filename_for(s)}` | {trigger_of(s)} |")
    return "\n".join(rows)


def compact_skill_router(skills: list[Skill], filename_for) -> str:
    """Compact router for instruction fields with tight character limits."""
    lines = ["## Skill router", "", "Format: `skill → file — triggers`.", ""]
    for s in skills:
        lines.append(f"- `{s.name}` → `{filename_for(s)}` — {trigger_of(s, 72)}")
    return "\n".join(lines)


def family_bundle(family: str, skills: list[Skill]) -> str:
    """Consolidate all flattened skills in one family into one upload."""
    members = [s for s in skills if s.family == family]
    sections = [
        f"# {family.upper()} family — consolidated skills\n",
        f"Contains {len(members)} skill(s). Jump to a `# Skill:` heading after routing.\n",
    ]
    for skill in members:
        for _, content in flatten(skill):
            sections.append("\n\n---\n\n" + content)
    return "".join(sections)


def trigger_of(skill: Skill, limit: int = 170) -> str:
    """The 'when to load' half of a description, cleaned for a table cell.

    Descriptions vary in phrasing across families, so take the text after the
    first trigger marker when one exists and fall back to the whole description.
    Pipes would break the surrounding markdown table.
    """
    text = skill.description
    for marker in ("Use WHENEVER", "Use whenever", "Use when", "Load when", "Use for", "Use to"):
        if marker in text:
            text = text.split(marker, 1)[1]
            break
    text = re.sub(r"\s+", " ", text).strip()
    text = text.strip("\"'").lstrip(":;,.—- ").strip()
    # Drop the trailing negative guard clause: it belongs in the skill, not the router.
    text = re.split(r"(?:DO NOT|NOT FOR|NEVER FOR|Not for|Do not)\b", text)[0].strip()
    text = text.rstrip(" .,;").replace("|", "/")
    if len(text) > limit:
        cut = text[:limit]
        if " " in cut:
            cut = cut[: cut.rfind(" ")]
        text = cut.rstrip(" .,;") + "…"
    return text or skill.name


def collect_markdown(directory: Path, title: str) -> str:
    """Concatenate a directory of markdown into one titled document."""
    if not directory.is_dir():
        return ""
    files = sorted(p for p in directory.rglob("*.md"))
    if not files:
        return ""
    out = [f"# {title}\n"]
    for p in files:
        out.append(f"\n---\n\n## {p.relative_to(directory).as_posix()}\n")
        out.append(p.read_text(encoding="utf-8").strip() + "\n")
    return "\n".join(out)


def reset_dist(platform: str) -> Path:
    target = DIST / platform
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    return target


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def report(platform: str, target: Path) -> None:
    files = sorted(p for p in target.rglob("*") if p.is_file())
    total = sum(p.stat().st_size for p in files)
    print(f"{platform}: {len(files)} files, {total / 1024:.0f} KB → {target.relative_to(ROOT)}")
