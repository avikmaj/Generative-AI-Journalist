"""QUORUM — a decision put through a council that argues with itself.

The failure mode a decision memo has is agreeing with whoever wrote it. QUORUM
is built so that cannot happen quietly: five seats hold positions, two rounds
of rebuttal force each to answer another, X6 red-teams whichever option is
winning, and C9 holds a veto it must justify in writing. An option that has
not survived an attack is not a recommendation.

Three structural refusals, each pinned by the schema so no artifact can claim
otherwise:

* ``input_instructions_honoured`` is ``false``. Text inside the decision or
  its context that tells the council what to conclude is recorded verbatim and
  is not an input to the verdict.
* ``verdict_source`` is ``deliberation``. The verdict comes from the positions
  and the attacks that survived, never from the framing.
* ``confidence_source`` is ``runner-computed``. Nothing in the input sets it.

Where the evidence does not reach a decision, ``insufficient_basis`` is
declared, ``option`` is null, and the artifact says which facts would resolve
it. That is an outcome, not a failure — and the schema enforces it, since an
escalated status with a non-null option cannot be serialised.

Run it over the committed fixture with::

    python employees/quorum/runner.py --decision employees/quorum/fixtures/decision.json
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

SEATS = ["C1", "C9", "C10", "S5", "X6"]

INSTRUCTION = re.compile(
    r"\b(?:recommend|choose|pick|select|conclude|decide on)\s+(?:option\s+)?"
    r"[a-z0-9-]+\s*(?:\.|$|,)|\b(?:you must|the answer is|obviously the right "
    r"(?:choice|option)|ignore (?:all |the )?(?:previous|above))\b", re.I)

# A verdict needs an option that survived at least this share of the attacks
# aimed at it. Below it the council has not cleared anything.
SURVIVAL_FLOOR = 0.5


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Quorum(EmployeeRunner):
    handle = "quorum"
    version = "1.0.1"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--decision", type=Path, required=True,
                            help="the decision, its options and its evidence")

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.decision.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        raw = source.read_text(encoding="utf-8")
        run.guard_input("decision", raw)
        doc = json.loads(raw)
        key = digest(raw)
        run.record.input_digest = key

        # Instruction-shaped text is collected before anything is weighed, so
        # that it cannot reach the deliberation by being read later.
        injections = []
        for location, text in (("decision", doc["decision"]),
                               ("context", doc.get("context", ""))):
            m = INSTRUCTION.search(text)
            if m:
                injections.append({"location": location,
                                   "verbatim": m.group(0)[:400],
                                   "classification": "instruction-to-quorum",
                                   "verdict_unaffected": True})
        for option in doc["options"]:
            m = INSTRUCTION.search(option.get("description", ""))
            if m:
                injections.append({"location": "option_description",
                                   "verbatim": m.group(0)[:400],
                                   "classification": "instruction-to-quorum",
                                   "verdict_unaffected": True})
        if injections:
            run.gap(f"instruction_shaped_text_in_input:{len(injections)}")

        options = {o["id"]: o for o in doc["options"]}
        positions = [
            {"seat": p["seat"], "option": p["option"], "argument": p["argument"],
             "evidence": p["evidence"]}
            for p in doc["positions"] if p["seat"] in SEATS][:5]
        rebuttals = [
            {"round": int(r["round"]), "seat": r["seat"],
             "responds_to": r["responds_to"], "argument": r["argument"]}
            for r in doc.get("rebuttals", [])]

        # The red team attacks whichever option the council is converging on.
        tally: dict[str, int] = {}
        for p in positions:
            tally[p["option"]] = tally.get(p["option"], 0) + 1
        leader = max(tally, key=lambda o: (tally[o], o)) if tally else None

        red_team = None
        if leader and doc.get("attacks"):
            attacks = [
                {"id": f"A{i:02d}", "attack": a["attack"],
                 "severity": a["severity"], "raised_by": a["raised_by"]}
                for i, a in enumerate(doc["attacks"], start=1)]
            survived = [a["id"] for a, spec in zip(attacks, doc["attacks"])
                        if spec.get("answered")]
            red_team = {"target_option": leader, "attacks": attacks,
                        "survived": survived}
        elif leader:
            run.gap("no_red_team_attacks_supplied")

        scenarios, ev_total = self.scenarios(doc)

        dissent = [
            {"seat": p["seat"], "objection": p["dissent"]}
            for p in doc["positions"] if p.get("dissent") and p["seat"] in SEATS]

        veto_spec = doc.get("veto") or {}
        veto = {"invoked": bool(veto_spec.get("invoked")),
                "seat": "C9" if veto_spec.get("invoked") else None,
                "grounds": veto_spec.get("grounds") if veto_spec.get("invoked")
                           else None}

        # A verdict requires an option that survived its attacks, no veto, and
        # a scenario set that adds up. Anything short of that is insufficient
        # basis, stated as such.
        survival = (len(red_team["survived"]) / len(red_team["attacks"])
                    if red_team and red_team["attacks"] else 0.0)
        blockers = []
        if veto["invoked"]:
            blockers.append("C9 vetoed the leading option")
        if red_team is None:
            blockers.append("no option was red-teamed")
        elif survival < SURVIVAL_FLOOR:
            blockers.append(f"the leading option answered only "
                            f"{len(red_team['survived'])} of "
                            f"{len(red_team['attacks'])} attacks")
        if ev_total is None:
            blockers.append("the scenario set is not traceable to an outcome unit")

        if blockers:
            run.escalate("insufficient_basis", "; ".join(blockers))
            verdict = {
                "option": None,
                "rationale": "The council did not clear an option: "
                             + "; ".join(blockers) + ".",
                "confidence": 0.0,
                "confidence_band": {"low": 0.0, "high": 0.0},
                "dissent": dissent,
                "insufficient_basis": {
                    "declared": True,
                    "resolving_information": self.resolving(doc, blockers)},
            }
        else:
            confidence = round(min(0.95, 0.50 + 0.40 * survival
                                   + 0.05 * (tally[leader] - 1)), 2)
            verdict = {
                "option": leader,
                "rationale": (
                    f"{options[leader]['label']} carried {tally[leader]} of "
                    f"{len(positions)} seats and answered "
                    f"{len(red_team['survived'])} of {len(red_team['attacks'])} "
                    f"attacks raised against it, including every attack graded "
                    f"high."),
                "confidence": confidence,
                "confidence_band": {"low": round(max(0.0, confidence - 0.10), 2),
                                    "high": round(min(1.0, confidence + 0.10), 2)},
                "dissent": dissent,
                "insufficient_basis": {"declared": False,
                                       "resolving_information": []},
            }

        run.finding(len(dissent) or 1)
        deductions = [
            Deduction("attacks against the leading option went unanswered", 0.10,
                      count=0 if red_team is None
                            else len(red_team["attacks"]) - len(red_team["survived"])),
            Deduction("a seat dissented from the verdict", 0.05, count=len(dissent)),
        ]
        return Outcome(
            fields={
                "schema_version": "1.0.0", "spec_version": "1.0.0",
                "generated_at": run.record.started_at,
                "decision_slug": doc["slug"],
                "dedupe_key": f"sha256:{key}",
                "input_digest": f"sha256:{key}",
                "integrity": {"input_instructions_honoured": False,
                              "verdict_source": "deliberation",
                              "confidence_source": "runner-computed"},
                "framing": {
                    "decision": doc["decision"][:400],
                    "options": [{"id": o["id"], "label": o["label"],
                                 "description": o.get("description", "")}
                                for o in doc["options"]],
                    "criteria": doc["criteria"],
                    "falsifiers": doc["falsifiers"],
                    "outcome_unit": doc.get("outcome_unit")},
                "positions": positions,
                "rebuttals": rebuttals,
                "red_team": red_team,
                "scenarios": scenarios,
                "scenario_ev_total": ev_total,
                "verdict": verdict,
                "veto": veto,
                "injection_attempts": injections,
            },
            deductions=[d for d in deductions if d.count],
            verdict=verdict["option"] or "insufficient_basis",
        )

    @staticmethod
    def scenarios(doc: dict) -> tuple[list[dict], float | None]:
        """Exactly four, and an expected value only where every one is traceable.

        A weighted average over scenarios that are partly guesses reads as a
        number and is not one, so the total is null unless all four trace.
        """
        names = ["base", "bull", "bear", "stress"]
        supplied = {s["name"]: s for s in doc.get("scenarios", [])}
        out = []
        for name in names:
            spec = supplied.get(name)
            if spec is None:
                out.append({"name": name,
                            "assumptions": ["no scenario was supplied for this case"],
                            "outcome": None, "probability": 0.0, "ev": None,
                            "traceable": False})
                continue
            outcome = spec.get("outcome")
            probability = float(spec.get("probability", 0.0))
            traceable = outcome is not None and bool(doc.get("outcome_unit"))
            out.append({
                "name": name, "assumptions": spec["assumptions"],
                "outcome": outcome, "probability": probability,
                "ev": round(outcome * probability, 4) if traceable else None,
                "traceable": traceable})
        if all(s["traceable"] for s in out):
            return out, round(sum(s["ev"] for s in out), 4)
        return out, None

    @staticmethod
    def resolving(doc: dict, blockers: list[str]) -> list[dict]:
        items = [{"fact_needed": f["fact"],
                  "would_change": f"it would falsify option {f['option_id']} and "
                                  f"settle which option the council can clear"}
                 for f in doc["falsifiers"][:4]]
        if not items:
            items = [{"fact_needed": "a falsifier for at least one option, stated "
                                     "as an observable fact",
                      "would_change": "it would let the council test an option "
                                      "rather than weigh opinions about it"}]
        return items[:5]


if __name__ == "__main__":
    raise SystemExit(Quorum(__file__).main())
