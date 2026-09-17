#!/usr/bin/env python3
"""Validate evals/golden-set.jsonl: schema, uniqueness, and cross-references.

Structural checks only — this does not call a model. Grading is described in
evals/rubric.md. Exit code is non-zero if the set is malformed, so CI can gate on it.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GOLDEN = ROOT / "evals" / "golden-set.jsonl"
RUBRIC = ROOT / "evals" / "rubric.md"

REQUIRED = {"id", "family", "mode_expected", "skill_expected", "prompt", "assertions", "rubric_dims", "notes"}
ASSERT_KEYS = {"must_include", "must_not_include", "must_label"}
MODES = {"[DV]", "[GENAI]", "[BIZ]", "[FILM]", "[BOTH]"}


def main() -> int:
    if not GOLDEN.exists():
        print(f"missing {GOLDEN.relative_to(ROOT)}", file=sys.stderr)
        return 1

    skills = {p.parent.name: p.parent.parent.name for p in (ROOT / "skills").glob("*/*/SKILL.md")}
    rubric_dims = set(re.findall(r"^\| `([a-z_]+)` \|", RUBRIC.read_text(encoding="utf-8"), re.M))

    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()
    cases = 0

    for lineno, line in enumerate(GOLDEN.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        cases += 1
        try:
            c = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {lineno}: invalid JSON — {exc}")
            continue

        cid = c.get("id", f"<line {lineno}>")
        missing = REQUIRED - c.keys()
        if missing:
            errors.append(f"{cid}: missing field(s) {sorted(missing)}")
        if cid in seen_ids:
            errors.append(f"{cid}: duplicate id")
        seen_ids.add(cid)

        if c.get("mode_expected") not in MODES:
            errors.append(f"{cid}: mode_expected {c.get('mode_expected')!r} not in {sorted(MODES)}")

        skill = c.get("skill_expected")
        if skill not in skills:
            errors.append(f"{cid}: skill_expected '{skill}' does not exist under skills/")
        elif skills[skill] != c.get("family"):
            errors.append(
                f"{cid}: family '{c.get('family')}' but skill '{skill}' lives in '{skills[skill]}'"
            )

        a = c.get("assertions", {})
        if not isinstance(a, dict) or set(a) - ASSERT_KEYS:
            errors.append(f"{cid}: assertions must be an object with keys {sorted(ASSERT_KEYS)}")
        elif not any(a.get(k) for k in ASSERT_KEYS):
            warnings.append(f"{cid}: no assertions — case is rubric-only and cannot fail automatically")

        for dim in c.get("rubric_dims", []):
            if dim not in rubric_dims:
                errors.append(f"{cid}: rubric dimension '{dim}' is not defined in evals/rubric.md")
        if not c.get("rubric_dims"):
            warnings.append(f"{cid}: no rubric dimensions")
        if not str(c.get("notes", "")).strip():
            warnings.append(f"{cid}: no notes — record why this case exists")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)

    if errors:
        print(f"\nFAILED — {len(errors)} error(s) across {cases} case(s)", file=sys.stderr)
        return 1
    print(f"\nvalidated {cases} golden-set cases against {len(rubric_dims)} rubric dimensions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
