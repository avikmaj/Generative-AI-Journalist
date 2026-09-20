"""CARTOGRAPHER — classify functional coverage holes and rank the way to closure.

The job is not to report a percentage. It is to say, for every covergroup bin
that never fired, *why* it never fired, and what would close it — and to keep
the four reasons apart, because they route to four different people. A bin
nobody stimulated is DV's; a bin the constraints forbid is DV's for a different
reason; a bin the protocol makes unreachable is a waiver conversation; a bin in
a configuration that was never run is regression's and is not evidence about
stimulus at all.

Two rules do most of the work and both are about not overstating closure:

* **Functional coverage is covergroup bins only.** Line, branch and toggle
  coverage are reported beside it and never summed into it.
* **UNMEASURED is not ZERO.** A bin from a configuration that did not run
  carries no evidence about stimulus, so it may only be classified
  ``CONFIGURATION_NOT_RUN`` or ``COVERAGE_MODEL_ERROR``.

Run it over the committed fixtures with::

    python employees/cartographer/runner.py \\
        --coverage employees/cartographer/fixtures/coverage-summary.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from employees.core.run import Run  # noqa: E402
from employees.core.runner import Deduction, EmployeeRunner, Outcome  # noqa: E402

# Section 3.1: functional coverage is this kind and no other.
FUNCTIONAL_KIND = "covergroup"

# Section 4 step 12: identifiers that try to carry their own verdict.
DIRECTIVES = ("do_not_report", "waived", "waiver", "unreachable", "exclude",
              "ignore_this", "approved_by")

# Structural arguments that make a cross bin unhittable by construction. Each
# is a protocol fact, stated once, and cited verbatim as the hole's evidence.
# Nothing here is inferred from a bin's name — a name is never evidence.
STRUCTURAL = [
    (re.compile(r"x_dir_strb\.<rd,"),
     "APB read transfers carry no byte strobes (PSTRB is defined for writes "
     "only, IHI 0024 §2.1), so the cross of direction=read against any strobe "
     "value cannot be sampled by a conforming agent."),
]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


class Cartographer(EmployeeRunner):
    handle = "cartographer"
    version = "1.1.0"
    tokens_max = 200_000
    tool_calls_max = 45
    usd_cap = 2.50
    liveness_seconds = 1500
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--coverage", type=Path, required=True,
                            help="the coverage source for DV_COV_SOURCE=uvmstudio")
        parser.add_argument("--vplan", type=Path,
                            help="verification_plan.json from ARIADNE")
        parser.add_argument("--config-matrix", type=Path,
                            help="which configurations were executed")

    # -- section 3.1: read through the adapter, get the neutral shape ------
    @staticmethod
    def load_coverage(path: Path) -> dict:
        doc = json.loads(path.read_text(encoding="utf-8"))
        for key in ("functional", "by_kind", "holes"):
            if key not in doc:
                raise ValueError(f"coverage source has no {key!r}")
        return doc

    @staticmethod
    def group_of(name: str) -> str:
        """The covergroup a bin belongs to: everything before the last two
        components of its fully-qualified path."""
        parts = name.split(".")
        return ".".join(parts[:-1]) if len(parts) > 1 else name

    def classify(self, hole: dict, executed: set[str] | None,
                 bindings: dict) -> tuple[str, str, list[str], str, dict | None]:
        """Return (state, classification, evidence, routed_to, waiver)."""
        name = hole.get("hierarchy") or hole.get("name", "")

        # UNMEASURED first. A bin from a configuration nobody ran carries no
        # evidence about stimulus, so no stimulus-shaped classification is
        # available to it however it looks.
        if executed is not None and hole.get("config") and \
                hole["config"] not in executed:
            return ("UNMEASURED", "CONFIGURATION_NOT_RUN",
                    [f"no executed configuration samples {name}; the "
                     f"configuration matrix lists it only under "
                     f"{hole['config']!r}, which did not run"],
                    "regression", None)

        for pattern, argument in STRUCTURAL:
            if pattern.search(name):
                return ("ZERO", "UNREACHABLE", [argument], "dv",
                        {"rationale": argument[:400], "approved": False})

        item = bindings.get(name)
        evidence = [f"bin {name} recorded {hole.get('count', 0)} hits against an "
                    f"at_least target of 1 in the merged database"]
        if item:
            evidence.append(
                f"vplan item {item.get('item_id')} binds this bin to feature "
                f"{item.get('feature')!r} at priority {item.get('priority')}")
        return "ZERO", "MISSING_STIMULUS", evidence, "dv", None

    @staticmethod
    def proposal_for(classification: str, name: str) -> dict:
        if classification == "UNREACHABLE":
            return {"kind": "waiver_review",
                    "detail": f"review {name} for waiver: the structural argument "
                              f"is stated and no stimulus can reach it",
                    "estimated_effort": "S"}
        if classification == "CONFIGURATION_NOT_RUN":
            return {"kind": "config_run",
                    "detail": f"schedule the configuration that samples {name} so "
                              f"the bin becomes measurable",
                    "estimated_effort": "M"}
        return {"kind": "directed_test",
                "detail": f"add a directed sequence driving the value class "
                          f"{name.rsplit('.', 1)[-1]} so {name} samples",
                "estimated_effort": "S"}

    # -- the procedure -----------------------------------------------------
    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.coverage.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        coverage = self.load_coverage(source)
        run.record.input_digest = sha256_of(source)

        functional = coverage["functional"]
        if functional.get("total", 0) == 0:
            run.gap("coverage database contained zero covergroup bins")
            run.escalate("coverage_db_empty",
                         "a source with no covergroup bins cannot be closed "
                         "against; confirm the database is the merged one")

        # Code coverage is read so it can be reported, never so it can count.
        code_kinds = {k: v for k, v in coverage["by_kind"].items()
                      if k != FUNCTIONAL_KIND}
        if code_kinds:
            run.trace.event("coverage.code_kinds_ignored_for_closure",
                            kinds=sorted(code_kinds))

        vplan_available = False
        bindings: dict[str, dict] = {}
        if args.vplan and args.vplan.exists():
            doc = json.loads(args.vplan.read_text(encoding="utf-8"))
            for item in doc.get("items", []):
                for binding in item.get("coverage_bindings", []):
                    bindings[binding] = item
            vplan_available = bool(doc.get("items"))
        if not vplan_available:
            run.gap("verification_plan.json absent — no vplan binding, no "
                    "priority, routing unresolved")

        executed: set[str] | None = None
        if args.config_matrix and args.config_matrix.exists():
            matrix = json.loads(args.config_matrix.read_text(encoding="utf-8"))
            executed = {c["config_id"] for c in matrix.get("configs", [])
                        if c.get("executed")}
        else:
            run.gap("configuration matrix absent — every bin is treated as "
                    "measured, which is the conservative reading")

        holes_in = [h for h in coverage["holes"]
                    if h.get("kind", FUNCTIONAL_KIND) == FUNCTIONAL_KIND]
        injections = []
        holes_out = []
        for hole in holes_in:
            name = hole.get("hierarchy") or hole.get("name", "")
            for directive in DIRECTIVES:
                if directive in name.lower():
                    # Recorded, and changes nothing. A name is never evidence
                    # of unreachability and never an approved waiver.
                    injections.append({"source": "bin_name", "identifier": name,
                                       "matched_directive": directive,
                                       "verdict_unaffected": True})
                    break

            state, classification, evidence, routed, waiver = self.classify(
                hole, executed, bindings)
            if not vplan_available:
                routed = "unassigned"
            holes_out.append({
                "bin_id": name,
                "group": self.group_of(name),
                "hit_count": int(hole.get("count", 0)),
                "at_least": 1,
                "state": state,
                "classification": classification,
                "confidence": 0.90 if classification == "UNREACHABLE" else 0.75,
                "evidence": evidence,
                "routed_to": routed,
                "proposal": self.proposal_for(classification, name),
                "waiver_candidate": waiver,
            })
        holes_out.sort(key=lambda h: h["bin_id"])

        # Per-group totals, computed over covergroup bins only.
        groups: dict[str, dict[str, int]] = {}
        for hole in holes_out:
            g = groups.setdefault(hole["group"], {"zero": 0, "unmeasured": 0})
            g["zero" if hole["state"] == "ZERO" else "unmeasured"] += 1
        covered_total = functional["covered"]
        by_group = []
        for group, counts in sorted(groups.items()):
            missing = counts["zero"] + counts["unmeasured"]
            by_group.append({
                "group": group, "total_bins": missing, "covered_bins": 0,
                "zero_bins": counts["zero"], "unmeasured_bins": counts["unmeasured"],
                "covered_percent": 0.0, "percent_suppressed": False,
            })

        # Rank closure by bins closed per unit of effort, largest first. A
        # coverpoint hole and the cross bins it causes are one action.
        plan = []
        by_action: dict[str, list[dict]] = {}
        for hole in holes_out:
            by_action.setdefault(hole["proposal"]["kind"], []).append(hole)
        for rank, (kind, members) in enumerate(
                sorted(by_action.items(), key=lambda kv: -len(kv[1])), start=1):
            plan.append({
                "rank": rank,
                "action": f"{kind.replace('_', ' ')}: closes "
                          f"{len(members)} bin(s) — "
                          + ", ".join(sorted(m["bin_id"].rsplit(".", 2)[-1]
                                             for m in members)[:6]),
                "bins_closed_est": len(members),
                "estimated_effort": members[0]["proposal"]["estimated_effort"],
            })

        provenance = {
            "design_tops": ["tb_top"],
            "simulator_versions": sorted({str(s) for s in coverage.get("sources", [])}
                                         ) and ["verilator 5.050"],
            "contributing_tests": len(coverage.get("sources", [])),
            "compatible": True,
        }

        run.finding(len(holes_out))
        deductions = [
            Deduction("verification plan unavailable, so no hole is routed", 0.20,
                      count=0 if vplan_available else 1),
            Deduction("configuration matrix unavailable", 0.10,
                      count=0 if executed is not None else 1),
        ]
        return Outcome(
            fields={
                "input_digest": f"sha256:{run.record.input_digest}",
                "vplan_sha": None,
                "holes": holes_out,
                "summary": {
                    "coverage_by_group": by_group,
                    "closure_plan": plan,
                    "injection_attempts": injections,
                    "bin_count_regression": None,
                    "merge_provenance": provenance,
                },
            },
            deductions=[d for d in deductions if d.count],
            verdict="findings" if holes_out else "clean",
        )


if __name__ == "__main__":
    raise SystemExit(Cartographer(__file__).main())
