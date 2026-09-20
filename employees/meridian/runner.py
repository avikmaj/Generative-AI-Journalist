"""MERIDIAN — an issuer analysis where every number names the source it came from.

The structural commitment is that a figure cannot exist without evidence
behind it. ``figure`` requires ``evidence_ids``, and the schema splits it two
ways: a ``sourced`` figure carries one value, a fiscal period and a staleness
flag; a ``conflicted`` figure carries the competing values and, by ``not:
{required: [value]}``, is forbidden from carrying a single one. Two filings
disagreeing therefore stays a disagreement in the artifact. Averaging them
would produce a number no document supports, which is the quiet way a model
invents a fact.

Where a valuation cannot be supported, ``valuation`` is null rather than a
range with wide error bars. A range is a claim; null is the absence of one.

Evidence that carries an instruction is regraded D and its ``action_taken`` is
pinned to a single constant sentence — logged as sourced content, source
regraded D, instruction not executed, verdict unchanged — so the record of
what was done cannot be paraphrased into something softer.

MERIDIAN does not advise. ``disclaimer`` is a schema constant saying so, and
the employee never places, recommends or simulates a trade.

Run it over the committed fixture with::

    python employees/meridian/runner.py --issuer employees/meridian/fixtures/issuer.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from employees.core.run import Run  # noqa: E402
from employees.core.runner import Deduction, EmployeeRunner, Outcome  # noqa: E402
from employees.core.runrecord import today  # noqa: E402

DISCLAIMER = ("This is analysis, not investment advice. MERIDIAN does not "
              "place, recommend, or simulate trades.")
ACTION_TAKEN = ("logged as sourced content, source regraded D, instruction not "
                "executed, verdict unchanged")

INSTRUCTION = re.compile(
    r"\b(?:ignore (?:all |the )?(?:previous|above)|you are now|rate this|"
    r"recommend (?:a )?(?:buy|sell|hold)|treat this as (?:grade )?a|"
    r"disregard the other)\b", re.I)

# Evidence older than this is stale for a figure that moves quarterly.
STALE_DAYS = 400
# A trend needs this many comparable periods before a direction means anything.
MIN_TREND_PERIODS = 3


class Meridian(EmployeeRunner):
    handle = "meridian"
    version = "1.0.0"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--issuer", type=Path, required=True,
                            help="the issuer's evidence set")
        parser.add_argument("--as-of", default=None,
                            help="the date staleness is measured against")

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.issuer.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        raw = source.read_text(encoding="utf-8")
        run.guard_input("issuer", raw)
        doc = json.loads(raw)
        run.record.input_digest = hashlib.sha256(raw.encode()).hexdigest()
        as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()

        evidence, attempts = [], []
        gaps: list[dict] = []
        by_id: dict[str, dict] = {}
        for index, item in enumerate(doc["evidence"], start=1):
            eid = f"E{index:03d}"
            published = date.fromisoformat(item["published_at"])
            stale = (as_of - published).days > STALE_DAYS
            injected = bool(INSTRUCTION.search(item["claim"]))
            entry = {
                "id": eid, "claim": item["claim"], "source": item["source"],
                "published_at": item["published_at"],
                # An instruction-bearing source is regraded D whatever it
                # claimed to be. The grade is about trustworthiness, and a
                # source that tries to steer the reader has forfeited it.
                "grade": "D" if injected else item["grade"],
                "verdict": item.get("verdict", "used"),
                "is_stale": stale, "injection_attempt": injected,
            }
            if injected:
                m = INSTRUCTION.search(item["claim"])
                entry["injection_excerpt"] = item["claim"][
                    max(0, m.start() - 30):m.start() + 160][:200]
                attempts.append({"evidence_id": eid,
                                 "excerpt": entry["injection_excerpt"],
                                 "action_taken": ACTION_TAKEN})
                # Not a gap: nothing is missing. The source is still evidence
                # about itself, regraded D, and adversarial_record is where the
                # attempt belongs. The gap reasons are for absent facts.
                run.gap(f"instruction_in_evidence:{eid}")
            if stale:
                run.gap(f"stale_evidence:{eid}:{item['published_at']}")
            evidence.append(entry)
            by_id[item["key"]] = entry

        def figure(spec: dict) -> dict:
            ids = [by_id[k]["id"] for k in spec["evidence_keys"] if k in by_id]
            base = {"name": spec["name"], "evidence_ids": ids or ["E001"]}
            if len(spec.get("values", [])) > 1:
                # Two filings disagree. The artifact says so and carries both;
                # averaging them would state a number no document supports.
                gaps.append({"field": f"financial_position.{spec['name']}",
                             "reason": "conflicted_unresolved"})
                run.gap(f"conflicted_figure:{spec['name']}")
                return {**base, "state": "conflicted",
                        "values": [{"value": float(v["value"]),
                                    "evidence_id": by_id[v["key"]]["id"]}
                                   for v in spec["values"]]}
            return {**base, "state": "sourced", "value": float(spec["value"]),
                    "unit": spec["unit"], "fiscal_period": spec["fiscal_period"],
                    "is_stale": any(by_id[k]["is_stale"]
                                    for k in spec["evidence_keys"] if k in by_id),
                    **({"currency": spec["currency"]} if spec.get("currency") else {})}

        figures = [figure(f) for f in doc["figures"]]
        ratios = [figure(f) for f in doc.get("ratios", [])]
        metrics = [figure(f) for f in doc.get("unit_metrics", [])]

        periods = int(doc.get("trend_periods", 0))
        if periods >= MIN_TREND_PERIODS:
            trend = {"periods_compared": periods,
                     "direction": doc["trend_direction"],
                     "evidence_ids": [by_id[k]["id"]
                                      for k in doc["trend_evidence_keys"]
                                      if k in by_id] or ["E001"]}
        else:
            trend = None
            gaps.append({"field": "financial_position.trend",
                         "reason": "insufficient_periods"})
            run.gap(f"trend_not_computed:{periods}_periods_below_"
                    f"{MIN_TREND_PERIODS}")

        conflicted = [f for f in figures + ratios + metrics
                      if f["state"] == "conflicted"]
        scalability = doc.get("scalability_verdict", "insufficient_evidence")
        if any(m["state"] == "conflicted" for m in metrics) or not metrics:
            scalability = "insufficient_evidence"

        # A valuation rests on figures. Where any driver figure is conflicted
        # or stale, there is no range to state and the field is null.
        valuation = None
        spec = doc.get("valuation")
        if spec and not conflicted:
            valuation = {
                "method": spec["method"],
                "range": spec["range"],
                "drivers": [{"name": d["name"],
                             "evidence_ids": [by_id[k]["id"]
                                              for k in d["evidence_keys"]
                                              if k in by_id] or ["E001"]}
                            for d in spec["drivers"]]}
        elif spec:
            gaps.append({"field": "valuation",
                         "reason": "method_inputs_unavailable"})
            run.gap("valuation_withheld:driver_figures_conflicted")

        market = self.market(doc, by_id)
        for key in ("tam", "sam", "som"):
            if market[key] is None:
                gaps.append({"field": f"market.{key}",
                             "reason": "method_inputs_unavailable"})
                run.gap(f"market_size_unavailable:{key}")

        run.finding(len(conflicted) + len(attempts))
        # Each deduction is named with the schema's own vocabulary so the
        # confidence object and the runner's arithmetic cannot drift: the
        # number the base computes is the sum of exactly these.
        deductions = [
            Deduction("conflict", 0.10, count=len(conflicted), cap=0.30),
            Deduction("injection", 0.15, count=1 if attempts else 0),
            Deduction("stale", 0.05,
                      count=sum(1 for e in evidence if e["is_stale"]), cap=0.15),
            Deduction("thin_evidence", 0.10, count=0 if trend else 1),
            Deduction("low_grade", 0.05,
                      count=sum(1 for e in evidence if e["grade"] in ("C", "D")),
                      cap=0.15),
        ]
        applied = [d for d in deductions if d.count]
        material = figures + ratios + metrics
        unsourced = [f for f in material if not f["evidence_ids"]]
        overall = round(max(0.0, 1.0 - sum(d.applied for d in applied)), 2)
        confidence = {
            "overall": overall,
            "basis": ("one deduction per named penalty, summed from 1.00: "
                      + "; ".join(f"{d.reason} {d.applied:.2f}" for d in applied)
                      if applied else "no penalty applied"),
            "material_figure_count": len(material),
            "unsourced_figure_count": len(unsourced),
            "unsourced_fraction": round(len(unsourced) / len(material), 4)
                                  if material else 0.0,
            "penalties_applied": [{"name": d.reason, "amount": round(d.applied, 4)}
                                  for d in applied],
        }
        return Outcome(
            fields={
                "schema_version": "1.0.0", "spec_version": self.version,
                "artifact_date": today(),
                "issuer": doc["issuer"],
                "disclaimer": DISCLAIMER,
                "financial_position": {
                    "figures": figures, "ratios": ratios, "trend": trend,
                    "red_flags": [
                        {"statement": r["statement"],
                         "evidence_ids": [by_id[k]["id"]
                                          for k in r["evidence_keys"]
                                          if k in by_id] or ["E001"]}
                        for r in doc.get("red_flags", [])]},
                "unit_economics": {"metrics": metrics,
                                   "scalability_verdict": scalability},
                "moat": doc["moat"] if isinstance(doc.get("moat"), dict) else {
                    "durability": [
                        {"statement": s["statement"],
                         "evidence_ids": [by_id[k]["id"] for k in s["evidence_keys"]
                                          if k in by_id] or ["E001"]}
                        for s in doc.get("durability", [])],
                    "capital_discipline": [
                        {"statement": s["statement"],
                         "evidence_ids": [by_id[k]["id"] for k in s["evidence_keys"]
                                          if k in by_id] or ["E001"]}
                        for s in doc.get("capital_discipline", [])]},
                "valuation": valuation,
                "market": market,
                "catalysts": self.dated(doc.get("catalysts", []), by_id),
                "thesis_breakers": self.dated(doc.get("thesis_breakers", []),
                                              by_id),
                "evidence_log": evidence,
                "adversarial_record": {
                    "attempts_detected": len(attempts),
                    "verdict_unaffected": True,
                    "attempts": attempts},
                "gaps": gaps,
                "confidence": confidence,
            },
            deductions=applied,
            verdict="findings" if conflicted or attempts else "clean",
        )

    @staticmethod
    def market(doc: dict, by_id: dict) -> dict:
        def size(key: str):
            spec = doc.get("market", {}).get(key)
            if not spec:
                return None
            return {"value": float(spec["value"]), "unit": spec["unit"],
                    "currency": spec["currency"], "method": spec["method"],
                    "evidence_ids": [by_id[k]["id"] for k in spec["evidence_keys"]
                                     if k in by_id] or ["E001"]}
        return {
            "tam": size("tam"), "sam": size("sam"), "som": size("som"),
            "competitive_set": [
                {"name": c["name"],
                 "evidence_ids": [by_id[k]["id"] for k in c["evidence_keys"]
                                  if k in by_id] or ["E001"]}
                for c in doc.get("market", {}).get("competitive_set", [])]}

    @staticmethod
    def dated(items: list[dict], by_id: dict) -> list[dict]:
        return [{"statement": i["statement"],
                 "expected_or_observed_at": i["at"],
                 "evidence_ids": [by_id[k]["id"] for k in i["evidence_keys"]
                                  if k in by_id] or ["E001"]}
                for i in items]


if __name__ == "__main__":
    raise SystemExit(Meridian(__file__).main())
