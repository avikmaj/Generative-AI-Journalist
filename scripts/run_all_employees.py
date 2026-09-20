"""Run every employee against its committed fixture and check what came back.

This is the gate that makes the fixtures load-bearing. The other two checks
read the specifications; this one runs the code, so a schema change that the
extractor happily propagates but that no runner can satisfy fails here rather
than the first time somebody deploys.

What it asserts, per employee:

* the run completed without an unhandled error,
* it did not end ``failed`` — which is what a schema violation looks like from
  the outside, since ``Run.emit`` refuses to write an artifact that does not
  validate,
* with ``--apply`` it wrote exactly one artifact and one run record.

It deliberately does **not** assert that a run ends ``ok``. Every fixture was
built to give its employee something real to find, so ``partial`` and
``escalated`` are the expected results and a sudden ``ok`` would mean the
fixture stopped biting.

Usage:
    python scripts/run_all_employees.py            # read-only
    python scripts/run_all_employees.py --apply    # write into a temp root
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# KEYSTONE's input is the four repositories themselves rather than a fixture
# file, and it refuses a partial sweep on purpose — an unread repository cannot
# support any statement about cross-repository integrity. So it runs only where
# all four are checked out, which a CI job cloning one repository is not.
SIBLINGS = ("Generative-AI-Journalist", "DESIGN_VERIFICATION_SOLUTIONS",
            "BUSINESS_SOLUTIONS",
            "AVIK-STUDIO-MTEAM-Agentic-AI-Film-Production-Playbook")


def siblings_present(base: Path) -> bool:
    return all((base / name).is_dir() or (base / name.lower()).is_dir()
               for name in SIBLINGS)


# handle -> the arguments that point it at its fixture.
INVOCATIONS: dict[str, list[str]] = {
    "keystone": ["--repos", str(ROOT.parent)],
    "bloodhound": ["--uvmstudio-report", "employees/bloodhound/fixtures/report.json",
                   "--routing-table", "employees/bloodhound/fixtures/routing-table.json"],
    "cartographer": ["--coverage", "employees/cartographer/fixtures/coverage-summary.json",
                     "--vplan", "employees/cartographer/fixtures/verification_plan.json"],
    "argus": ["--signals", "employees/argus/fixtures/signals.json"],
    "herald": ["--video", "employees/herald/fixtures/video.json"],
    "augur": ["--analytics", "employees/augur/fixtures/week.json"],
    "tribunal": ["--submission", "employees/tribunal/fixtures/gate.json"],
    "aegis": ["--observations", "employees/aegis/fixtures/asset.json"],
    "ariadne": ["--spec", "employees/ariadne/fixtures/spec.json"],
    "mnemo": ["--batch", "employees/mnemo/fixtures/scene.json"],
    "quorum": ["--decision", "employees/quorum/fixtures/decision.json"],
    "genesis": ["--premise", "employees/genesis/fixtures/premise.json"],
    "aperture": ["--lock", "employees/genesis/fixtures/premise.json",
                 "--scene", "employees/aperture/fixtures/scene.json"],
    "splice": ["--cut", "employees/splice/fixtures/cut.json"],
    "meridian": ["--issuer", "employees/meridian/fixtures/issuer.json",
                 "--as-of", "2026-09-20"],
    "crucible": ["--deal", "employees/crucible/fixtures/deal.json"],
}

# Fixtures built to prove an employee refuses something. Each must end
# escalated with no artifact written: that refusal is the behaviour under test,
# so a run that quietly produced a report would be the failure.
REFUSALS: dict[str, list[list[str]]] = {
    "splice": [
        ["--cut", "employees/splice/fixtures/cut-unapproved.json"],
        ["--cut", "employees/splice/fixtures/cut-drawn-text.json"],
    ],
}


def status_of(stderr: str) -> str:
    for token in stderr.split():
        if token.startswith("status="):
            return token.split("=", 1)[1]
    return "(no status line)"


def invoke(handle: str, args: list[str], root: Path,
           apply: bool) -> tuple[int, str]:
    command = [sys.executable, f"employees/{handle}/runner.py", *args,
               "--reports-root", str(root)]
    if apply:
        command.append("--apply")
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return result.returncode, result.stderr.strip()


def main() -> int:
    apply = "--apply" in sys.argv[1:]
    # employees/core/runner.py is the shared base, not an employee.
    missing = sorted(set(p.parent.name for p in ROOT.glob("employees/*/runner.py"))
                     - set(INVOCATIONS) - {"core"})
    if missing:
        print(f"FAIL  {len(missing)} runner(s) have no fixture invocation: "
              f"{', '.join(missing)}")
        return 1

    problems = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        skipped = set()
        for handle, args in INVOCATIONS.items():
            if handle == "keystone" and not siblings_present(ROOT.parent):
                print(f"skip  {handle:14} needs all four repositories checked "
                      f"out beside this one; it refuses a partial sweep")
                skipped.add(handle)
                continue
            code, stderr = invoke(handle, args, root, apply)
            status = status_of(stderr)
            if code != 0:
                print(f"FAIL  {handle:14} exited {code}")
                print("        " + stderr.replace("\n", "\n        ")[:600])
                problems += 1
            elif status == "failed":
                print(f"FAIL  {handle:14} ended failed — the artifact did not "
                      f"validate, so nothing was written")
                print(f"        {stderr[:300]}")
                problems += 1
            else:
                print(f"ok    {handle:14} {stderr[:96]}")

        for handle, cases in REFUSALS.items():
            for args in cases:
                fixture = Path(args[-1]).name
                code, stderr = invoke(handle, args, root, apply)
                status = status_of(stderr)
                if code != 0 or status != "escalated":
                    print(f"FAIL  {handle:14} {fixture} should have escalated, "
                          f"got {status} (exit {code})")
                    problems += 1
                else:
                    print(f"ok    {handle:14} {fixture} refused as designed")

        if apply:
            artifacts = sorted(p.relative_to(root)
                               for p in root.glob("reports/*/*.json"))
            records = list(root.glob("runs/*/*/*.record.json"))
            expected = len(INVOCATIONS) - len(skipped)
            if len(artifacts) != expected:
                print(f"\nFAIL  {len(artifacts)} artifact(s) written, expected "
                      f"{expected}")
                problems += 1
            else:
                print(f"\nok    {expected} artifacts written, "
                      f"{len(records)} run records persisted")
            for path in artifacts:
                try:
                    json.loads((root / path).read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    print(f"FAIL  {path} is not valid JSON: {exc.msg}")
                    problems += 1

    total = (len(INVOCATIONS) - len(skipped)
             + sum(len(c) for c in REFUSALS.values()))
    note = f" ({len(skipped)} skipped)" if skipped else ""
    print(f"\n{total - problems}/{total} employees behaved as specified{note}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
