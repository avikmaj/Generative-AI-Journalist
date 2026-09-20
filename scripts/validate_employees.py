"""Validate generated employee specifications against the fourteen-section contract.

Checks every ``employees/*/EMPLOYEE.md`` against the contract in
``docs/12-ai-employee-roster.md``. Runs locally and in CI, and covers the same
ground KEYSTONE will cover once deployed. Nothing else checks these files: the
prompt library's own validator globs only ``prompts/*/*/sector-expert.md``.

Usage:
    python scripts/validate_employees.py [path ...]

With no argument it validates every ``employees/*/EMPLOYEE.md``. A path may be
a specification file or a directory to search. Exit status is non-zero when any
specification fails.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SECTIONS = [
    "IDENTITY",
    "TRIGGER",
    "INPUTS",
    "PROCEDURE",
    "OUTPUT CONTRACT",
    "CONFIDENCE & ESCALATION",
    "BLAST RADIUS",
    "BUDGETS",
    "IDEMPOTENCY",
    "FAILURE MODES",
    "DEGRADATION RULE",
    "SUCCESS METRIC",
    "TESTS",
    "VERSION HISTORY",
]

XML_TAGS = [
    "role",
    "context",
    "input_handling",
    "task",
    "output_specification",
    "quality_criteria",
    "constraints",
]

SECRET_PATTERNS = [
    (r"sk-ant-[A-Za-z0-9]", "Anthropic API key"),
    (r"ghp_[A-Za-z0-9]{20}", "GitHub personal access token"),
    (r"github_pat_[A-Za-z0-9]", "GitHub fine-grained token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key id"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
]


def heading_index(text: str, number: int, name: str) -> int:
    """Offset of the heading for one numbered section, or -1.

    Tolerates ``## 3. INPUTS``, ``### 3 INPUTS`` and a bare ``3. INPUTS`` line,
    since the standard fixes the wording of a heading but not its depth.
    """
    escaped = re.escape(name).replace(r"\ ", r"\s+")
    pattern = rf"^#{{0,6}}\s*{number}[.):]?\s+{escaped}\s*$"
    match = re.search(pattern, text, re.M | re.I)
    return match.start() if match else -1


def section_body(text: str, start: int, next_start: int) -> str:
    end = next_start if next_start > start else len(text)
    return text[start:end]


def validate(path: Path) -> list[str]:
    """Return the specification's violations, empty when it conforms."""
    text = path.read_text(encoding="utf-8")
    bad: list[str] = []

    # --- structure ------------------------------------------------------
    offsets = []
    for number, name in enumerate(SECTIONS, start=1):
        at = heading_index(text, number, name)
        if at < 0:
            bad.append(f"missing section {number} {name}")
        offsets.append(at)

    present = [(n, o) for n, o in zip(SECTIONS, offsets) if o >= 0]
    for (name_a, off_a), (name_b, off_b) in zip(present, present[1:]):
        if off_b < off_a:
            bad.append(f"section {name_b} appears before {name_a}")

    meta = re.search(r"^#{1,6}\s*Metadata\s*$", text, re.M | re.I)
    if not meta:
        bad.append("missing '## Metadata' block")
    elif offsets[0] >= 0 and meta.start() > offsets[0]:
        bad.append("'## Metadata' must appear before section 1 IDENTITY")

    for heading in ("OPEN QUESTIONS", "STATED ASSUMPTIONS"):
        if not re.search(rf"^#{{1,6}}\s*{heading}\s*$", text, re.M | re.I):
            bad.append(f"missing '## {heading}' heading")

    # --- prompt body ----------------------------------------------------
    for tag in XML_TAGS:
        if f"<{tag}>" not in text or f"</{tag}>" not in text:
            bad.append(f"prompt body missing <{tag}> ... </{tag}>")

    # --- tests ----------------------------------------------------------
    if offsets[12] >= 0:
        tests = section_body(text, offsets[12], offsets[13])
        if "adversarial" not in tests.lower():
            bad.append("TESTS has no adversarial row")
        if tests.count("|") < 8:
            bad.append("TESTS does not contain a table")

    # --- version history ------------------------------------------------
    if offsets[13] >= 0:
        history = section_body(text, offsets[13], len(text))
        if not re.search(r"\b\d+\.\d+\.\d+\b", history):
            bad.append("VERSION HISTORY carries no semantic version")

    # --- markers --------------------------------------------------------
    open_q = re.search(r"^#{1,6}\s*OPEN QUESTIONS\s*$", text, re.M | re.I)
    boundary = open_q.start() if open_q else len(text)
    if "<<FILL:" in text[:boundary]:
        bad.append("unresolved <<FILL:> marker in the body, outside OPEN QUESTIONS")
    if "<<ASSUMED:" in text:
        bad.append("<<ASSUMED:> marker left in place; the value must be written in")

    # --- output schema --------------------------------------------------
    blocks = re.findall(r"```(?:json|jsonc)?\s*\n(.*?)```", text, re.S)
    schemas = [b for b in blocks if '"$schema"' in b or '"properties"' in b]
    if not schemas:
        bad.append("OUTPUT CONTRACT carries no JSON Schema block")
    else:
        for block in schemas:
            try:
                parsed = json.loads(block)
            except json.JSONDecodeError as exc:
                bad.append(f"JSON Schema does not parse: {exc.msg} at line {exc.lineno}")
                continue
            declared = str(parsed.get("$schema", ""))
            if declared and "2020-12" not in declared:
                bad.append(f"JSON Schema declares {declared}, expected draft 2020-12")

    # --- model and determinism ------------------------------------------
    if re.search(r"claude-haiku-4-5-\d", text):
        bad.append("Haiku model id carries a date suffix; use claude-haiku-4-5")
    for match in re.finditer(r"temperature", text, re.I):
        window = text[max(0, match.start() - 300) : match.start() + 300]
        if "claude-opus-5" in window and "reject" not in window.lower():
            bad.append("temperature applied near claude-opus-5, which rejects it with HTTP 400")
            break

    # --- secrets ---------------------------------------------------------
    for pattern, label in SECRET_PATTERNS:
        if re.search(pattern, text):
            bad.append(f"possible {label} committed in the specification")

    return bad


def collect(args: list[str]) -> list[Path]:
    if not args:
        return sorted((ROOT / "employees").glob("*/EMPLOYEE.md"))
    found: list[Path] = []
    for arg in args:
        path = Path(arg)
        if path.is_dir():
            found.extend(sorted(path.rglob("EMPLOYEE.md")))
        elif path.is_file():
            found.append(path)
        else:
            print(f"error: no such path: {arg}", file=sys.stderr)
    return found


def main() -> int:
    specs = collect(sys.argv[1:])
    if not specs:
        print("no EMPLOYEE.md found — nothing to validate")
        return 0

    failed = 0
    for spec in specs:
        handle = spec.parent.name
        violations = validate(spec)
        if violations:
            failed += 1
            print(f"FAIL  {handle}  ({len(violations)})")
            for v in violations:
                print(f"        - {v}")
        else:
            print(f"PASS  {handle}")

    print(f"\n{len(specs) - failed}/{len(specs)} specifications conform")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
