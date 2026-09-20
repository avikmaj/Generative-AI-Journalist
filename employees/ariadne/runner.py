"""ARIADNE — the thread from a specification sentence to the test that closes it.

A requirements traceability matrix is only worth having if it distinguishes
what the specification *says* from what a reader *supplied*. So every
requirement carries a label, and the label is the point:

``CONFIRMED``   the specification states it
``INFERRED``    it follows from what the specification states
``ASSUMED``     a working default was used, and the assumption is written down
``AMBIGUOUS``   the specification can be read two ways, including when the
                text is instruction-shaped rather than requirement-shaped
``UNKNOWN``     the source could not be read

A requirement is ``closed`` only when a test claims it fully, that test has
actually run and passed, and every required evidence type is satisfied. A test
that exists but has never run closes nothing — a matrix that counted it would
be worse than no matrix, because it would look like coverage.

Specification text that addresses the tool, or that waives itself ("this
requirement needs no verification"), is recorded and labelled ``AMBIGUOUS``.
The schema pins ``action_taken`` to exactly that, so the recording cannot be
described as having been obeyed.

Run it over the committed fixture with::

    python employees/ariadne/runner.py --spec employees/ariadne/fixtures/spec.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from employees.core.run import Run  # noqa: E402
from employees.core.runner import Deduction, EmployeeRunner, Outcome  # noqa: E402
from employees.core.runrecord import today  # noqa: E402

SUSPECT = [
    (re.compile(r"\b(?:ignore (?:all |the )?(?:previous|above)|you are now|"
                r"do not trace|skip this requirement)\b", re.I),
     "instruction_to_tool"),
    (re.compile(r"\b(?:no verification (?:is )?(?:required|needed)|"
                r"requires no test|self[- ]evident|waived by design)\b", re.I),
     "self_waiving_requirement"),
    (re.compile(r"\.\./|\.\.\\"), "path_traversal"),
    (re.compile(r"\b(?:approved by the (?:owner|architect)|the lead has signed)\b",
                re.I), "operator_impersonation"),
]


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_id(prefix: str, text: str, width: int) -> str:
    return f"{prefix}-{digest(text)[:width]}"


class Ariadne(EmployeeRunner):
    handle = "ariadne"
    version = "1.0.0"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--spec", type=Path, required=True,
                            help="specification sections and the test tree")

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.spec.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        raw = source.read_text(encoding="utf-8")
        run.guard_input("spec", raw)
        doc = json.loads(raw)
        run.record.input_digest = digest(raw)

        tests_by_scenario: dict[str, list[dict]] = {}
        all_tests = doc.get("tests", [])
        for test in all_tests:
            for scenario in test.get("scenarios", []):
                tests_by_scenario.setdefault(scenario, []).append(test)

        injections = []
        requirements = []
        traced_tests: set[str] = set()

        for entry in doc["requirements"]:
            text = entry["text"]
            label = entry.get("label", "CONFIRMED")
            assumption = entry.get("assumption")
            consequence = entry.get("consequence")

            # Instruction-shaped or self-waiving text is not a requirement that
            # can be read at face value. It is recorded and demoted.
            for pattern, kind in SUSPECT:
                m = pattern.search(text)
                if m:
                    injections.append({
                        "source_doc": entry["source"]["doc"],
                        "source_section": entry["source"]["section"],
                        "quoted_text": text[max(0, m.start() - 30):
                                            m.start() + 200] or text,
                        "classification": kind,
                        "action_taken":
                            "recorded_as_spec_content_and_labelled_AMBIGUOUS",
                        "verdict_unaffected": True})
                    label = "AMBIGUOUS"
                    consequence = consequence or (
                        "the section carries text that is not a verifiable "
                        "requirement; a human must restate it before it can be "
                        "traced")
                    break

            scenarios = []
            tests = []
            for scenario in entry.get("scenarios", []):
                scenario_id = stable_id("SCN", scenario["description"], 8)
                scenarios.append({
                    "scenario_id": scenario_id,
                    "description": scenario["description"],
                    "category": scenario["category"]})
                for test in tests_by_scenario.get(scenario["key"], []):
                    traced_tests.add(test["test_path"])
                    tests.append({
                        "test_name": test["test_name"],
                        "test_path": test["test_path"],
                        "scenario_id": scenario_id,
                        "coverage_claim": test.get("coverage_claim", "partial"),
                        "execution_status": test.get("execution_status",
                                                     "unknown")})

            evidence = []
            for requirement_evidence in entry["evidence_types_required"]:
                kind = requirement_evidence["evidence_type"]
                satisfied = self.evidence_satisfied(kind, tests, entry)
                evidence.append({
                    "evidence_type": kind,
                    "exit_criterion": requirement_evidence["exit_criterion"],
                    "satisfied": satisfied})

            status = self.status_of(label, tests, evidence)
            if status != "closed":
                run.finding(1)
            if label == "ASSUMED" and assumption:
                run.gap(f"assumed_requirement:{entry['source']['section']}")
            if label in ("AMBIGUOUS", "UNKNOWN"):
                run.gap(f"{label.lower()}_requirement:"
                        f"{entry['source']['section']}")

            requirements.append({
                "req_id": stable_id("REQ", text, 8),
                "text": text, "source": entry["source"], "label": label,
                "assumption": assumption, "consequence": consequence,
                "scenarios": scenarios, "tests": tests,
                "coverage_bins": entry.get("coverage_bins", []),
                "evidence_types_required": evidence,
                "status": status, "owner": entry.get("owner"),
            })
        requirements.sort(key=lambda r: r["req_id"])

        orphans = sorted(
            ({"test_name": t["test_name"], "test_path": t["test_path"],
              "reason": "no_requirement_traced"}
             for t in all_tests if t["test_path"] not in traced_tests),
            key=lambda t: t["test_path"])
        for orphan in orphans:
            run.gap(f"orphan_test:{orphan['test_path']}")

        open_count = sum(1 for r in requirements if r["status"] != "closed")
        deductions = [
            Deduction("requirements not closed by evidence", 0.02,
                      count=open_count, cap=0.20),
            Deduction("tests trace to no requirement", 0.10,
                      count=1 if orphans else 0),
            Deduction("specification text could not be read as a requirement",
                      0.15, count=1 if injections else 0),
        ]
        return Outcome(
            fields={
                "schema_version": "1.0.0",
                "generated_at_utc": today(),
                "employee_version": self.version,
                "spec_digest": f"sha256:{digest(json.dumps(doc['requirements'], sort_keys=True))}",
                "test_tree_sha": f"sha256:{digest(json.dumps(all_tests, sort_keys=True))}",
                "requirements": requirements,
                "orphan_tests": orphans,
                "injection_attempts": injections,
            },
            deductions=[d for d in deductions if d.count],
            verdict="findings" if open_count or orphans else "clean",
        )

    @staticmethod
    def evidence_satisfied(kind: str, tests: list[dict], entry: dict) -> bool:
        """Evidence is satisfied by something that happened, not by a plan."""
        if kind == "simulation_pass":
            return any(t["execution_status"] == "run_passed" for t in tests)
        if kind == "assertion_pass":
            return any(t["execution_status"] == "run_passed"
                       and t["coverage_claim"] == "full" for t in tests)
        if kind == "functional_coverage":
            return bool(entry.get("coverage_bins")) and any(
                t["execution_status"] == "run_passed" for t in tests)
        # formal_proof and review_signoff are attested externally; absent an
        # attestation they are simply not satisfied.
        return bool(entry.get("attestations", {}).get(kind))

    @staticmethod
    def status_of(label: str, tests: list[dict], evidence: list[dict]) -> str:
        if label == "UNKNOWN":
            return "source_unavailable"
        if label == "AMBIGUOUS":
            return "escalated"
        if not tests:
            return "open"
        if all(e["satisfied"] for e in evidence) and any(
                t["coverage_claim"] == "full"
                and t["execution_status"] == "run_passed" for t in tests):
            return "closed"
        if any(t["execution_status"] == "run_passed" for t in tests):
            return "partial_coverage"
        return "open"


if __name__ == "__main__":
    raise SystemExit(Ariadne(__file__).main())
