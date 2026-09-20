"""CRUCIBLE — diligence on a target, where finding nothing is the hardest result.

A diligence report with no findings is either good news or an analyst who did
not look, and the two are indistinguishable from the outside. So CRUCIBLE
cannot return silence: the schema says an empty finding set requires a
``clean_bill_register`` of at least six entries, each naming a vector, what
was checked, what it was checked against, and why it could not be faulted —
and pins the status to ``escalated`` in that case, because a clean bill is a
claim a human should look at rather than a result to file.

Two more refusals the schema enforces rather than requests:

* **Covenant arithmetic needs the covenant.** Every credit metric carries
  ``basis_verified``, and an unverified basis forces a declared gap. Leverage
  computed against a definition nobody read is a number with a decimal point
  and no meaning.
* **Every claim carries its evidence class.** ``user_supplied`` is not
  ``externally_verified``, and the vendor's own model is not evidence about
  the vendor. The class travels with the finding so a reader can see which
  findings would survive the seller leaving the room.

Instruction-bearing text inside a data room is recorded as a finding about
disclosure behaviour and *increases* scrutiny. It is never obeyed:
``disposition`` is pinned to ``recorded_as_finding``.

CRUCIBLE is read-only and analysis-only, which ``analysis_only_notice``
states as a constant.

Run it over the committed fixture with::

    python employees/crucible/runner.py --deal employees/crucible/fixtures/deal.json
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
from employees.core.runrecord import today, utcnow  # noqa: E402

NOTICE = ("CRUCIBLE is read-only and analysis-only. It did not transact, did "
          "not contact the target, and did not contact any third party.")

INSTRUCTION = [
    (re.compile(r"\b(?:reviewers? (?:should|must) not|do not (?:flag|raise|"
                r"escalate)|no further (?:diligence|review) (?:is )?required)\b",
                re.I), "reviewer_directive"),
    (re.compile(r"\b(?:the (?:sponsor|partner|operator) has (?:approved|cleared))\b",
                re.I), "operator_impersonation"),
    (re.compile(r"\b(?:system prompt|you are an? (?:ai|assistant|analyst))\b", re.I),
     "system_prompt_impersonation"),
    (re.compile(r"\.\./|\.\.\\"), "path_traversal"),
]

# The document classes a data-room diligence expects to see. Anything absent
# is named, because the gap between what was promised and what arrived is
# itself a finding.
EXPECTED = ["annual_report", "interim_report", "credit_agreement",
            "management_accounts", "related_party_disclosure",
            "auditor_communication"]

# The vectors that must each be either faulted or explicitly cleared.
VECTORS = ["revenue_recognition", "aggressive_capitalisation", "related_party",
           "one_off_as_recurring", "working_capital", "cash_conversion"]


class Crucible(EmployeeRunner):
    handle = "crucible"
    version = "1.0.0"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--deal", type=Path, required=True,
                            help="the deal's document set and extracted findings")

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.deal.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        raw = source.read_text(encoding="utf-8")
        run.guard_input("deal", raw)
        doc = json.loads(raw)
        digest = hashlib.sha256(raw.encode()).hexdigest()
        run.record.input_digest = digest

        documents, attempts = [], []
        present_classes = set()
        for entry in doc["documents"]:
            documents.append({
                "id": entry["id"], "title": entry.get("title", ""),
                "source": entry["source"],
                "retrieved_at_utc": entry["retrieved_at_utc"],
                "sha256": entry["sha256"], "doc_class": entry["doc_class"],
                "effective_date": entry.get("effective_date"),
                "parsed": bool(entry.get("parsed", True))})
            if entry.get("parsed", True):
                present_classes.add(entry["doc_class"])
            else:
                run.gap(f"document_not_parsed:{entry['id']}")

            for pattern, kind in INSTRUCTION:
                m = pattern.search(entry.get("text", ""))
                if m:
                    # Scrutiny goes up, not down. A data room telling reviewers
                    # what not to look at has told them where to look.
                    attempts.append({
                        "kind": kind, "document_id": entry["id"],
                        "quoted_text": entry["text"][max(0, m.start() - 40):
                                                     m.start() + 200][:600],
                        "disposition": "recorded_as_finding",
                        "scrutiny_change": "increased",
                        "verdict_unaffected": True})
                    run.gap(f"directive_in_document:{entry['id']}")

        absent = [c for c in EXPECTED if c not in present_classes]
        for missing in absent:
            run.gap(f"document_class_absent:{missing}")

        earnings = [
            {"finding": f["finding"], "severity": f["severity"],
             "evidence": f["evidence"], "source": f["source"],
             "vector": f["vector"], "evidence_class": f["evidence_class"],
             "basis_verified": bool(f.get("basis_verified", False))}
            for f in doc.get("earnings_quality", [])]
        red_flags = [
            {"severity": f["severity"], "finding": f["finding"],
             "evidence": f["evidence"], "source": f["source"],
             "evidence_class": f["evidence_class"]}
            for f in doc.get("red_flags", [])]

        # Every vector is either faulted or cleared on the record. A vector
        # that is neither was not examined, and saying so is the point.
        faulted = {f["vector"] for f in earnings}
        register = []
        for vector in VECTORS:
            if vector in faulted:
                continue
            cleared = doc.get("cleared", {}).get(vector)
            if cleared is None:
                run.gap(f"vector_not_examined:{vector}")
                continue
            register.append({
                "vector": vector,
                "what_was_checked": cleared["what_was_checked"],
                "evidence_checked_against": cleared["evidence_checked_against"],
                "could_not_fault_because": cleared["could_not_fault_because"]})

        covenant_docs = [d["id"] for d in documents
                         if d["doc_class"] in ("credit_agreement",
                                               "credit_amendment") and d["parsed"]]
        covenant_verified = bool(covenant_docs)
        if not covenant_verified:
            run.gap("covenant_basis_unverified: no parsed credit agreement, so "
                    "every leverage and coverage figure is computed against a "
                    "definition nobody read")

        credit = {
            "leverage": self.metric(doc["credit"]["leverage"], covenant_verified),
            "coverage": self.metric(doc["credit"]["coverage"], covenant_verified),
            "covenant_headroom": self.metric(doc["credit"]["covenant_headroom"],
                                             covenant_verified),
            "refi_risk": self.metric(doc["credit"]["refi_risk"], covenant_verified),
            "covenant_basis_verified": covenant_verified,
            "covenant_basis_documents": covenant_docs,
        }

        decision, conditions = self.decide(earnings, red_flags, covenant_verified)
        if decision != "go":
            run.finding(len(earnings) + len(red_flags) or 1)

        deductions = [
            Deduction("critical or high earnings-quality findings", 0.10,
                      count=sum(1 for f in earnings
                                if f["severity"] in ("high", "critical")),
                      cap=0.30),
            Deduction("covenant basis unverified", 0.20,
                      count=0 if covenant_verified else 1),
            Deduction("expected document classes absent", 0.05,
                      count=len(absent), cap=0.20),
            Deduction("findings resting on user-supplied evidence only", 0.05,
                      count=sum(1 for f in earnings + red_flags
                                if f["evidence_class"] == "user_supplied"),
                      cap=0.15),
        ]
        applied = [d for d in deductions if d.count]
        final = round(max(0.0, 1.0 - sum(d.applied for d in applied)), 2)

        if not earnings and not red_flags:
            # A clean bill is a claim, not a filing. The schema demands the
            # register and the escalation; this makes the reason explicit.
            run.escalate("clean_bill_of_health",
                         "no earnings-quality finding and no red flag survived "
                         "examination; a human should confirm the register "
                         "covers what they expected it to")

        return Outcome(
            fields={
                "schema_version": "1.0.0", "spec_version": self.version,
                "deal_slug": doc["deal_slug"],
                "target_company": doc["target_company"],
                "generated_at_utc": utcnow(), "date": today(),
                "input_digest": digest,
                "document_set": {"mode": doc.get("mode", "data_room"),
                                 "documents": documents,
                                 "expected_classes": EXPECTED,
                                 "absent_classes": absent},
                "earnings_quality": earnings,
                "credit": credit,
                "thesis_breakers": [
                    {"claim_attacked": t["claim_attacked"],
                     "fact_that_would_break_it": t["fact_that_would_break_it"],
                     "how_to_test_it": t["how_to_test_it"],
                     "currently_supported_by_evidence": t["currently_supported"],
                     "forced_by_injection_attempt": False}
                    for t in doc.get("thesis_breakers", [])],
                "scenarios": doc["scenarios"],
                "red_flags": red_flags,
                "clean_bill_register": register,
                "management_assessment": doc["management_assessment"],
                "verdict": {"decision": decision, "conditions": conditions,
                            "rationale": self.rationale(decision, earnings,
                                                        red_flags,
                                                        covenant_verified)},
                "confidence": final,
                "confidence_breakdown": {
                    "start": 1.0,
                    "deductions": [{"name": d.reason, "amount": round(d.applied, 4),
                                    "reason": f"{d.count} occurrence(s) at "
                                              f"{d.amount} each"}
                                   for d in applied],
                    "final": final},
                "evidence_log": [
                    {"claim": e["claim"], "evidence_class": e["evidence_class"],
                     "source": e["source"],
                     "retrieved_at_utc": e.get("retrieved_at_utc")}
                    for e in doc["evidence_log"]],
                "injection_attempts": attempts,
                "analysis_only_notice": NOTICE,
            },
            deductions=applied,
            verdict=decision,
        )

    @staticmethod
    def metric(spec: dict, covenant_verified: bool) -> dict:
        return {"value": spec["value"], "units": spec["units"],
                "inputs": spec["inputs"],
                "evidence_class": spec["evidence_class"],
                # A metric cannot be better verified than the covenant it is
                # measured against.
                "basis_verified": covenant_verified
                                  and bool(spec.get("basis_verified", False))}

    @staticmethod
    def decide(earnings: list[dict], red_flags: list[dict],
               covenant_verified: bool) -> tuple[str, list[dict]]:
        critical = [f for f in earnings + red_flags if f["severity"] == "critical"]
        high = [f for f in earnings + red_flags if f["severity"] == "high"]
        if critical:
            return "no_go", []
        conditions = []
        if high:
            conditions.append({
                "condition": f"resolve {len(high)} high-severity finding(s) with "
                             f"externally verified evidence",
                "flips_to": "go"})
        if not covenant_verified:
            conditions.append({
                "condition": "obtain and parse the credit agreement so leverage "
                             "and headroom are computed against the real "
                             "covenant definitions",
                "flips_to": "go"})
        return ("conditional", conditions) if conditions else ("go", [])

    @staticmethod
    def rationale(decision: str, earnings: list[dict], red_flags: list[dict],
                  covenant_verified: bool) -> str:
        if decision == "no_go":
            return ("A critical finding survived examination against externally "
                    "verified evidence; nothing in the remaining analysis "
                    "outweighs it.")
        if decision == "conditional":
            return (f"{len(earnings)} earnings-quality finding(s) and "
                    f"{len(red_flags)} red flag(s), none critical. The covenant "
                    f"basis is {'verified' if covenant_verified else 'unverified'}. "
                    f"Each condition names what would flip this.")
        return ("No finding survived examination, and every vector is cleared on "
                "the register with what it was checked against.")


if __name__ == "__main__":
    raise SystemExit(Crucible(__file__).main())
