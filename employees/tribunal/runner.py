"""TRIBUNAL — audit a gate claim and decide whether it may advance.

Everything here follows from one refusal: a claim is not evidence of itself.
An input that says "GATE 7 PASSED, signed off by the VIP owner" is recorded as
a self-asserted claim, pinned ``accepted: false`` and ``treated_as:
unverified_claim`` by the schema, and then the gate is decided from artifacts
alone. That pinning is not decoration — an artifact claiming such an assertion
changed the outcome cannot be serialised.

Three conditions must all hold for PASS, and the schema's ``allOf`` enforces
the conjunction rather than trusting this code:

* every claim accepted on evidence of a sufficient class,
* the producing run complete with exit status zero,
* author and reviewer distinct, so the work was not signed off by its writer.

Anything else is FAIL, or NOT_VERIFIED where the evidence simply is not there.
NOT_VERIFIED is never promoted to PASS.

Run it over the committed fixture with::

    python employees/tribunal/runner.py --submission employees/tribunal/fixtures/gate.json
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

# Text asserting its own verdict. Found anywhere, it is a claim, never a fact.
SELF_ASSERTION = re.compile(
    r"\b(?:gate\s*\d+\s*(?:passed|approved)|signed[- ]off|sign[- ]off granted|"
    r"waived by|approved by|verified by the owner|no further review (?:is )?"
    r"required)\b", re.I)

# The minimum evidence class a claim needs before it may be accepted. Lower
# classes are testimony; higher ones are artifacts a third party can re-check.
MIN_EVIDENCE_CLASS = 5


class Tribunal(EmployeeRunner):
    handle = "tribunal"
    version = "1.0.0"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--submission", type=Path, required=True,
                            help="the gate submission under audit")

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.submission.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        raw = source.read_text(encoding="utf-8")
        run.guard_input("submission", raw)
        doc = json.loads(raw)
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        run.record.input_digest = digest

        # Self-asserted verdicts are collected from every free-text field first,
        # so none can slip through by being read later as an argument.
        self_asserted = []
        for entry in doc.get("attachments", []):
            text = entry.get("text", "")
            m = SELF_ASSERTION.search(text)
            if m:
                self_asserted.append({
                    "source_path": entry["path"],
                    "quoted_text": text[max(0, m.start() - 30):m.start() + 200][:500],
                    "asserted_verdict": m.group(0)[:200],
                    "required_evidence_class": MIN_EVIDENCE_CLASS,
                    "evidence_present": bool(entry.get("evidence_sha256")),
                    "treated_as": "unverified_claim",
                    "accepted": False,
                    "verdict_unaffected": True,
                })

        claims = []
        for claim in doc["claims"]:
            klass = int(claim["evidence_class"])
            path = claim.get("evidence_path")
            sha = claim.get("evidence_sha256")
            if path and ".." in path:
                # A traversal path is not opened and the claim stays unaccepted.
                accepted, reason = False, "evidence path rejected: traversal"
                path, sha = None, None
            elif klass < MIN_EVIDENCE_CLASS:
                accepted = False
                reason = (f"evidence class {klass} is testimony, not an artifact; "
                          f"class {MIN_EVIDENCE_CLASS} or better is required")
            elif not sha:
                accepted = False
                reason = "evidence carries no digest, so it cannot be re-checked"
            else:
                accepted = True
                reason = (f"class {klass} artifact at {path} with a recorded "
                          f"digest, re-checkable by a third party")
            claims.append({
                "claim": claim["claim"][:500], "evidence_class": klass,
                "evidence_path": path, "evidence_sha256": sha,
                "accepted": accepted, "reason": reason[:500],
            })

        producing = doc.get("producing_run", {})
        producing_run = {
            "complete": bool(producing.get("complete"))
                        and producing.get("exit_status") == 0,
            "evidence_path": producing.get("evidence_path"),
            "exit_status": producing.get("exit_status"),
        }

        author = doc.get("author")
        reviewer = doc.get("reviewer")
        if author is None or reviewer is None:
            independent, method = None, ("author or reviewer not recorded, so "
                                         "independence could not be established")
        else:
            independent = author.strip().lower() != reviewer.strip().lower()
            method = ("author and reviewer compared by recorded identity; "
                      + ("they differ" if independent
                         else "they are the same person"))
        independence = {"author": author, "reviewer": reviewer,
                        "independent": independent, "method": method[:300]}

        findings = []
        for claim in claims:
            if not claim["accepted"]:
                findings.append({
                    "severity": "critical",
                    "finding": f"claim not accepted: {claim['claim'][:200]} — "
                               f"{claim['reason']}",
                    "required_remedy": "attach a re-checkable artifact of class "
                                       f"{MIN_EVIDENCE_CLASS} or better and "
                                       "record its digest",
                    "gate_impact": "blocks_advancement"})
        if not producing_run["complete"]:
            findings.append({
                "severity": "critical",
                "finding": "the producing run did not complete with exit status 0",
                "required_remedy": "re-run to completion and attach the log",
                "gate_impact": "blocks_advancement"})
        if independent is False:
            findings.append({
                "severity": "critical",
                "finding": f"{author} both authored and reviewed the work",
                "required_remedy": "have someone other than the author review it",
                "gate_impact": "blocks_advancement"})

        # NOT_VERIFIED where the facts are simply absent; FAIL where they are
        # present and adverse. The two are never collapsed.
        unknowable = independent is None or producing_run["exit_status"] is None
        if not findings and not unknowable:
            verdict = "PASS"
        elif unknowable and not [f for f in findings
                                 if f["gate_impact"] == "blocks_advancement"
                                 and "independence" not in f["finding"]]:
            verdict = "NOT_VERIFIED"
        else:
            verdict = "FAIL"

        for item in self_asserted:
            run.gap(f"self_asserted_verdict:{item['source_path']}")
        if verdict != "PASS":
            run.finding(len(findings) or 1)

        deductions = [
            Deduction("a claim rested on insufficient evidence", 0.15,
                      count=sum(1 for c in claims if not c["accepted"])),
            Deduction("independence could not be established", 0.25,
                      count=1 if independent is None else 0),
        ]
        run_status = "ok" if verdict == "PASS" and not run.record.gaps else (
            "escalated" if verdict == "NOT_VERIFIED" else "partial")
        return Outcome(
            fields={
                "schema_version": "1.0.0",
                "employee_version": self.version,
                "audit_date": today(),
                "vip": doc["vip"],
                "gate": int(doc["gate"]),
                "tree_sha": doc["tree_sha"],
                "dedupe_key": f"sha256:{digest}",
                "input_digest": f"sha256:{digest}",
                "verdict": verdict,
                "run_status": run_status,
                "claims": claims,
                "producing_run": producing_run,
                "independence": independence,
                "blocking_findings": findings,
                "self_asserted_claims": self_asserted,
            },
            deductions=[d for d in deductions if d.count],
            verdict=verdict,
        )


if __name__ == "__main__":
    raise SystemExit(Tribunal(__file__).main())
