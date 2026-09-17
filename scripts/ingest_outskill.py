#!/usr/bin/env python3
"""Ingest the OUTSKILL course corpus into knowledge/outskill/index.jsonl.

Walks a source tree, extracts text from PDF / DOCX / MD / TXT, splits each
document on headings, and writes one JSON object per section:

    {"file": ..., "book": ..., "section": ..., "anchor": ..., "text": ...}

The `anchor` is what skills cite as `OUTSKILL/<file> §<anchor>`.

Both the output and any copied source are git-ignored: the corpus is licensed
course material and must never be committed. The script refuses to write
anywhere except knowledge/outskill/.

Usage:
    python3 scripts/ingest_outskill.py --src "/path/to/OUTSKILL"
    python3 scripts/ingest_outskill.py --src ... --copy-raw   # also stage raw/
    python3 scripts/ingest_outskill.py --src ... --stats      # report only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "knowledge" / "outskill"
INDEX = OUT_DIR / "index.jsonl"
RAW = OUT_DIR / "raw"

SUPPORTED = {".pdf", ".docx", ".md", ".markdown", ".txt"}
MIN_SECTION_CHARS = 40

# The corpus numbers each book 1-6 as a filename prefix, consistently across all
# four source tiers. Everything else is a standalone document.
BOOK_TITLES = {
    1: "Book 1 — The AI Generalist Mindset",
    2: "Book 2 — Vibe Coding",
    3: "Book 3 — AI Workflows and Connectors",
    4: "Book 4 — Custom AI Assistants and Agents",
    5: "Book 5 — Building AI Agents on n8n",
    6: "Book 6 — Visual Storytelling with AI",
}
BOOK_PREFIX_RE = re.compile(r"^\s*([1-6])\s*[.)]\s*\S")

# Source tiers cover the same book at increasing depth. When they conflict,
# prefer the highest precedence — the personal notes and compendium are the
# reconciled version. Skills use this to break ties.
TIERS = (
    ("personal-notes", 4, ("personal notes",)),
    ("session-notes", 3, ("session notes",)),
    ("workbook", 2, ("workbook", "hands on lab")),
    ("pre-read", 1, ("pre-read", "pre reads", "pre-reads")),
)


def extract_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        print("pypdf is required for PDF input: pip install -r requirements.txt", file=sys.stderr)
        raise SystemExit(1)
    reader = PdfReader(str(path))
    return "\n\n".join((page.extract_text() or "") for page in reader.pages)


def extract_docx(path: Path) -> str:
    try:
        import docx
    except ImportError:
        print("python-docx is required for DOCX input: pip install -r requirements.txt", file=sys.stderr)
        raise SystemExit(1)
    return "\n".join(p.text for p in docx.Document(str(path)).paragraphs)


def extract(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix == ".docx":
        return extract_docx(path)
    return path.read_text(encoding="utf-8", errors="replace")


def tier_of(path: Path) -> tuple[str, int]:
    """Which source tier a file belongs to, and its precedence (higher wins)."""
    posix = path.as_posix().lower()
    for name, precedence, needles in TIERS:
        if any(n in posix for n in needles):
            return name, precedence
    return "standalone", 5


def book_of(path: Path) -> str:
    """Classify by the 1-6 filename prefix, then by known standalone titles."""
    stem = path.name.lower()
    posix = path.as_posix().lower()

    if "compendium" in stem:
        return "Bootcamp Compendium (all six books, reconciled)"
    if "quick_reference" in stem or "quick reference" in stem:
        return "Quick Reference Cards"
    if "roadmap" in posix:
        return "AI Generalist Roadmap"
    if "money playbook" in stem:
        return "Bonus — GenAI Money Playbook"
    if "outskill_genai_session_notes" in stem:
        return "Session Notes (all six books, aggregate)"
    if "outskill_genai_workbook" in stem:
        return "Workbook (all six books, aggregate)"
    if "native_engineer" in stem or "native engineer" in stem:
        return "The AI-Native Engineer"
    if "redemption" in stem or "access your tools" in posix:
        return "Tool Access Guide"

    m = BOOK_PREFIX_RE.match(path.name)
    if m:
        return BOOK_TITLES[int(m.group(1))]

    # Fall back to a book number anywhere in the path (e.g. a parent folder).
    m = re.search(r"\bbook[\s_-]*([1-6])\b", posix)
    if m:
        return BOOK_TITLES[int(m.group(1))]
    return "Unclassified"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:80] or "section"


def split_sections(text: str) -> list[tuple[str, str]]:
    """Split on markdown headings, then on ALL-CAPS or numbered headings."""
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    lines = text.split("\n")
    sections: list[tuple[str, list[str]]] = [("Front matter", [])]
    for line in lines:
        stripped = line.strip()
        is_heading = bool(
            re.match(r"^#{1,4}\s+\S", stripped)
            or re.match(r"^(chapter|section|module|part|lesson)\b.{0,80}$", stripped, re.I)
            or (
                6 < len(stripped) < 90
                and stripped == stripped.upper()
                and re.search(r"[A-Z]{3}", stripped)
                and not stripped.endswith((".", ",", ";"))
            )
            or re.match(r"^\d{1,2}[.)]\s+[A-Z].{4,80}$", stripped)
        )
        if is_heading:
            title = re.sub(r"^#{1,4}\s+", "", stripped).strip()
            sections.append((title, []))
        else:
            sections[-1][1].append(line)

    out: list[tuple[str, str]] = []
    seen: dict[str, int] = {}
    for title, body in sections:
        content = "\n".join(body).strip()
        if len(content) < MIN_SECTION_CHARS:
            continue
        anchor = slugify(title)
        seen[anchor] = seen.get(anchor, 0) + 1
        if seen[anchor] > 1:
            anchor = f"{anchor}-{seen[anchor]}"
        out.append((title, anchor, content))  # type: ignore[arg-type]
    return out  # type: ignore[return-value]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True, help="path to the OUTSKILL source tree")
    ap.add_argument("--copy-raw", action="store_true", help="also stage sources into knowledge/outskill/raw/")
    ap.add_argument("--stats", action="store_true", help="report what would be ingested, write nothing")
    args = ap.parse_args()

    src = Path(args.src).expanduser()
    if not src.exists():
        print(f"source not found: {src}", file=sys.stderr)
        print(
            "If this is a local Windows path, run this script on that machine — "
            "a remote agent cannot reach your local filesystem.",
            file=sys.stderr,
        )
        return 1

    files = sorted(p for p in src.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED)
    if not files:
        print(f"no supported files ({', '.join(sorted(SUPPORTED))}) under {src}", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records = 0
    per_book: dict[str, int] = {}
    per_tier: dict[str, int] = {}
    failures: list[str] = []

    handle = None if args.stats else INDEX.open("w", encoding="utf-8")
    try:
        for path in files:
            rel = path.relative_to(src).as_posix()
            try:
                text = extract(path)
            except SystemExit:
                raise
            except Exception as exc:  # a single unreadable file must not kill the run
                failures.append(f"{rel}: {type(exc).__name__} {exc}")
                continue

            relpath = path.relative_to(src)
            book = book_of(relpath)
            tier, precedence = tier_of(relpath)
            sections = split_sections(text)
            if not sections:
                failures.append(f"{rel}: no extractable sections")
                continue

            for title, anchor, content in sections:
                if handle is not None:
                    handle.write(
                        json.dumps(
                            {
                                "file": rel,
                                "book": book,
                                "tier": tier,
                                "precedence": precedence,
                                "section": title,
                                "anchor": anchor,
                                "text": content,
                            },
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
                records += 1
                per_book[book] = per_book.get(book, 0) + 1
                per_tier[tier] = per_tier.get(tier, 0) + 1

            if args.copy_raw and not args.stats:
                dest = RAW / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(path.read_bytes())
    finally:
        if handle is not None:
            handle.close()

    verb = "would ingest" if args.stats else "ingested"
    print(f"{verb} {records} sections from {len(files)} files")
    for book, count in sorted(per_book.items()):
        print(f"  {book}: {count} sections")
    if per_tier:
        print("\nby source tier (higher precedence wins on conflict):")
        for tier, count in sorted(per_tier.items(), key=lambda kv: -kv[1]):
            print(f"  {tier}: {count} sections")
    if failures:
        print(f"\n{len(failures)} file(s) skipped:")
        for f in failures[:20]:
            print(f"  {f}")
    if not args.stats:
        print(f"\nwrote {INDEX.relative_to(ROOT)} ({INDEX.stat().st_size / 1024:.0f} KB)")
        print("This file is git-ignored on purpose. Never commit it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
