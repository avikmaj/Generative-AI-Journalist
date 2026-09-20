"""Extract each employee's output JSON Schema from its specification.

Section 5 OUTPUT CONTRACT carries the schema inline, because a person reading
the specification needs it there. A runner needs it as a file it can load and
validate against, which is ``employees/<handle>/schema/output.json``. This
script keeps the two in step: the specification stays authoritative, and the
file is derived from it rather than maintained beside it.

Usage:
    python scripts/extract_employee_schemas.py            # write the files
    python scripts/extract_employee_schemas.py --check    # verify, write nothing

``--check`` exits non-zero when any extracted file is missing or stale, which
makes it usable as a CI gate.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FENCE = re.compile(r"^```[A-Za-z0-9_+-]*[ \t]*\n(.*?)^```", re.S | re.M)


def output_contract(text: str) -> str:
    """The span of section 5, or the whole document when it cannot be located."""
    start = re.search(r"^#{0,6}\s*5[.):]?\s+OUTPUT\s+CONTRACT\s*$", text, re.M | re.I)
    if not start:
        return text
    after = re.search(r"^#{0,6}\s*6[.):]?\s+CONFIDENCE", text[start.end():], re.M | re.I)
    return text[start.end():start.end() + after.start()] if after else text[start.end():]


def find_schemas(text: str) -> tuple[list[dict], str]:
    """Return every schema in the output contract, and where they were found.

    A specification's section 5 also shows the run record, which is an example
    object rather than a schema. The schema is the block that declares
    ``$schema``; that is what separates the two.

    An employee may contract for more than one artifact — ARIADNE emits a
    verification plan and an RTM diff — so every schema is returned rather than
    the largest. Taking only one would silently drop a contract the
    specification makes.
    """
    for scope, label in ((output_contract(text), "section 5"), (text, "whole document")):
        found = []
        for block in FENCE.findall(scope):
            if '"$schema"' not in block:
                continue
            try:
                parsed = json.loads(block)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                found.append(parsed)
        if found:
            return found, label
    return [], "no block declaring $schema"


def filename_for(schema: dict, index: int) -> str:
    """Where a schema belongs, taken from its own $id when it declares one."""
    ident = str(schema.get("$id", ""))
    if ident:
        name = ident.rstrip("/").rsplit("/", 1)[-1]
        if name.endswith(".json"):
            return name
    return "output.json" if index == 0 else f"output-{index}.json"


def main() -> int:
    check = "--check" in sys.argv[1:]
    specs = sorted((ROOT / "employees").glob("*/EMPLOYEE.md"))
    if not specs:
        print("no EMPLOYEE.md found")
        return 0

    problems = 0
    for spec in specs:
        handle = spec.parent.name
        schemas, note = find_schemas(spec.read_text(encoding="utf-8"))
        if not schemas:
            print(f"FAIL  {handle:14} {note}")
            problems += 1
            continue

        for index, schema in enumerate(schemas):
            name = filename_for(schema, index)
            declared = str(schema.get("$schema", ""))
            if "2020-12" not in declared:
                print(f"FAIL  {handle:14} {name} declares "
                      f"{declared or '(nothing)'}, expected draft 2020-12")
                problems += 1
                continue

            rendered = json.dumps(schema, indent=2, ensure_ascii=False) + "\n"
            target = spec.parent / "schema" / name

            if check:
                current = target.read_text(encoding="utf-8") if target.exists() else None
                if current != rendered:
                    state = "missing" if current is None else "stale"
                    print(f"FAIL  {handle:14} {target.relative_to(ROOT)} is {state}")
                    problems += 1
                else:
                    print(f"ok    {handle:14} {name} current")
                continue

            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(rendered, encoding="utf-8")
            keys = len(schema.get("properties", {}))
            print(f"ok    {handle:14} {name:24} {keys:2} properties  ({note})")

    verb = "checked" if check else "extracted"
    print(f"\n{len(specs) - problems}/{len(specs)} schemas {verb}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
