"""BLOODHOUND — turn a night of regression logs into clustered, routed failures.

The specification's one structural idea is that a verdict comes from evidence
and nothing else. So this runner re-derives every outcome from the logs rather
than believing a status somebody already wrote down: where a manifest or a
platform report carries its own verdict, that verdict is compared against the
one the log supports, and a disagreement is a finding rather than a tiebreak.

Two input adapters, the same internal shape:

``--manifest``          the native manifest.json of section 3.1
``--uvmstudio-report``  a ``uvmstudio-report/1`` document from the UVM
                        Verification Studio, which carries the same facts
                        under different names

Run it over the committed fixtures with::

    python employees/bloodhound/runner.py \\
        --uvmstudio-report employees/bloodhound/fixtures/report.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from employees.core.run import Run  # noqa: E402
from employees.core.runner import Deduction, EmployeeRunner, Outcome  # noqa: E402

# -- section 3.2: the UVM report vocabulary, identical across simulators ----
UVM_COUNT = re.compile(r"^\s*(UVM_(?:INFO|WARNING|ERROR|FATAL))\s*:\s*(\d+)\s*$", re.M)
UVM_MSG = re.compile(r"^(UVM_(?:ERROR|FATAL))\b\s*(.*)$", re.M)
UVM_SUMMARY = re.compile(r"--- UVM Report Summary ---")
FINISH = re.compile(r"\$finish\b", re.I)

# The one tool-specific detail. DV_SIM selects the prefix and nothing else.
TOOL_PREFIX = {
    "verilator": "%Error",
    "vcs": "Error-[",
    "questa": "** Error",
    "xcelium": "xmelab: *E",
}

# Text that addresses the triager rather than describing the simulation.
INJECTION = [
    (re.compile(r"\b(?:root cause confirmed|close as not-a-bug|not a bug)\b", re.I),
     "verdict_claim"),
    (re.compile(r"\b(?:waive|skip|disable|quarantine)\s+(?:this|the)\s+test\b", re.I),
     "waive_or_skip_instruction"),
    (re.compile(r"\bTEST\s+PASSED\b", re.I), "fabricated_pass_banner"),
    (re.compile(r"^\s*#?\s*(?:OPERATOR|ADMIN)\s*:", re.I | re.M),
     "operator_impersonation"),
    (re.compile(r"^\s*#?\s*(?:HARNESS|CI)\s*:\s*(?:override|approve)", re.I | re.M),
     "harness_impersonation"),
]

# Section 4 step 10: the first rule that matches decides the cause domain.
# Ordered, and deliberately small — an unmatched failure is spec_ambiguity,
# which is penalised, rather than a guess dressed as an attribution.
CAUSE_RULES = [
    (re.compile(r"\[SB_[A-Z_]*\]"), "scoreboard"),
    (re.compile(r"\[(?:MON|MONITOR)_", re.I), "monitor"),
    (re.compile(r"\[(?:DRV|DRIVER)_", re.I), "driver"),
    (re.compile(r"\[(?:SEQ|STIM)_", re.I), "stimulus"),
    (re.compile(r"\[(?:REFM|PREDICTOR)_", re.I), "reference_model"),
    (re.compile(r"assertion failed", re.I), "assertion"),
    (re.compile(r"\breset\b.*\brace\b", re.I), "reset_race"),
    (re.compile(r"\b[xX]-propagation\b|\bfound 'x'\b", re.I), "x_propagation"),
    (re.compile(r"^%Error|^Error-\[|^\*\* Error|^xmelab: \*E", re.M), "tool"),
]


@dataclass
class TestRun:
    """One (test, seed) as the manifest describes it and the log evidences it."""

    test: str
    seed: int
    config: str
    exit_status: int | None
    log_path: str
    expect: str = "PASS"
    reported_status: str | None = None  # what the source claimed, for cross-check

    outcome: str = "unknown"
    reasons: list[str] = field(default_factory=list)
    signature: str = ""
    evidence: tuple[int, str] | None = None  # (line_no, excerpt)
    sim_time: str | None = None
    src_file: str | None = None
    src_line: int | None = None
    injections: list[dict] = field(default_factory=list)


def canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def normalise(text: str) -> str:
    """Fold away everything that differs between two instances of one defect."""
    t = re.sub(r"0x[0-9a-fA-F]+", "<N>", text)
    t = re.sub(r"\b\d+\b", "<N>", t)
    return re.sub(r"\s+", " ", t).strip().lower()


class Bloodhound(EmployeeRunner):
    handle = "bloodhound"
    version = "1.1.0"
    tokens_max = 200_000
    tool_calls_max = 60
    usd_cap = 2.00
    liveness_seconds = 1800
    confidence_threshold = 0.70  # section 6.1, and stated there only

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        source = parser.add_mutually_exclusive_group(required=True)
        source.add_argument("--manifest", type=Path,
                            help="the native manifest.json of section 3.1")
        source.add_argument("--uvmstudio-report", type=Path,
                            help="a uvmstudio-report/1 document")
        parser.add_argument("--sim", default="verilator", choices=sorted(TOOL_PREFIX),
                            help="selects the tool error prefix, nothing else")
        parser.add_argument("--routing-table", type=Path,
                            help="JSON map from cause_domain to owning department")

    # -- input adapters ----------------------------------------------------
    @staticmethod
    def from_manifest(path: Path) -> tuple[dict, list[TestRun]]:
        doc = json.loads(path.read_text(encoding="utf-8"))
        runs = [
            TestRun(test=t["test"], seed=int(t["seed"]),
                    config=t.get("config", "default"),
                    exit_status=t.get("exit_status"), log_path=t["log_path"],
                    expect=t.get("expect", "PASS"))
            for t in doc["tests"]
        ]
        return {"regression_run_id": str(doc["regression_run_id"]),
                "commit": doc["commit"]}, runs

    @staticmethod
    def from_uvmstudio(path: Path) -> tuple[dict, list[TestRun]]:
        """The platform's report carries the same facts under different names.

        Its per-run ``status`` is kept only as ``reported_status``: it is what
        the source claimed, never what this employee concludes.
        """
        doc = json.loads(path.read_text(encoding="utf-8"))
        reg = doc["regression"]
        runs = [
            TestRun(
                test=r["test"], seed=int(r["seed"]),
                config=r.get("tier") or reg.get("tier") or "default",
                exit_status=r.get("returncode"), log_path=r.get("log_path") or "",
                expect="FAIL" if str(r.get("test", "")).endswith("_error_test") else "PASS",
                reported_status=r.get("status"),
            )
            for r in doc["runs"]
        ]
        return {"regression_run_id": f"{reg['project']}#{reg['id']}",
                "commit": reg.get("git_commit") or "0" * 40}, runs

    # -- section 3.2: classify one log -------------------------------------
    def classify(self, run: TestRun, text: str | None, prefix: str) -> None:
        if text is None:
            run.outcome, run.reasons = "unknown", ["log file absent"]
            return
        if not text.strip():
            run.outcome, run.reasons = "unknown", ["log file zero-length"]
            return

        lines = text.splitlines()

        # Counters are the MAXIMUM across occurrences, never the last read: a
        # trailing forged "UVM_ERROR : 0" can then only make a run look worse.
        counts: dict[str, int] = {}
        for m in UVM_COUNT.finditer(text):
            counts[m.group(1)] = max(counts.get(m.group(1), 0), int(m.group(2)))
        n_err = counts.get("UVM_ERROR", 0)
        n_fatal = counts.get("UVM_FATAL", 0)

        summaries = len(UVM_SUMMARY.findall(text))
        finished = bool(FINISH.search(text))
        inline = [(i + 1, l) for i, l in enumerate(lines)
                  if UVM_MSG.match(l) and not UVM_COUNT.match(l)]
        tool_errors = [(i + 1, l) for i, l in enumerate(lines)
                       if l.startswith(prefix)]

        reasons: list[str] = []
        if n_fatal:
            reasons.append(f"UVM_FATAL count = {n_fatal}")
        if n_err:
            reasons.append(f"UVM_ERROR count = {n_err}")
        if inline and summaries and not n_err and not n_fatal:
            reasons.append(
                f"{len(inline)} inline UVM_ERROR/UVM_FATAL message(s) contradict "
                f"a summary reporting zero")
            run.injections.append({"line_no": inline[0][0],
                                   "excerpt": inline[0][1][:2000],
                                   "attempt_kind": "contradicted_summary"})
        if summaries > 1:
            reasons.append(
                f"UVM report summary appears {summaries} times — a single run "
                f"prints it once; evidence is not trustworthy")
            second = [i + 1 for i, l in enumerate(lines)
                      if UVM_SUMMARY.search(l)][1]
            run.injections.append({"line_no": second, "excerpt": lines[second - 1][:2000],
                                   "attempt_kind": "duplicate_summary"})
        if tool_errors:
            reasons.append(f"{len(tool_errors)} {prefix} line(s) from the simulator")
        if run.exit_status not in (0, None):
            reasons.append(f"non-zero exit code {run.exit_status}")
        if run.exit_status is None:
            reasons.append("manifest carries no exit_status")

        # The earliest record is the signature's anchor, tool errors last.
        anchor = inline[0] if inline else (tool_errors[0] if tool_errors else None)
        if anchor:
            run.evidence = (anchor[0], anchor[1][:2000])
            m = re.search(r"\(\s*(\d+)\s*\)", anchor[1]) or re.search(
                r":(\d+):", anchor[1])
            f = re.search(r"([\w./-]+\.(?:sv|svh|v))", anchor[1])
            run.src_line = int(m.group(1)) if m else None
            run.src_file = Path(f.group(1)).name if f else None
            t = re.search(r"@\s*(\d+)", anchor[1])
            run.sim_time = t.group(1) if t else None
            run.signature = anchor[1]

        failed = bool(reasons)

        # A negative test inverts the pass criterion, not the evidence rules.
        if run.expect == "FAIL":
            if failed:
                run.outcome = "pass"
                run.reasons = ["negative test: expected violation was DETECTED"]
            else:
                run.outcome = "fail"
                run.reasons = ["negative test: expected violation was NOT detected"]
                run.signature = f"NEG_NOT_DETECTED:{run.test}"
                # The evidence is the clean summary itself: a green log is the
                # symptom here, so it is what a reader must be shown.
                summary_at = next((i + 1 for i, l in enumerate(lines)
                                   if UVM_SUMMARY.search(l)), len(lines))
                run.evidence = (summary_at, lines[summary_at - 1][:2000])
            return

        if failed:
            run.outcome, run.reasons = "fail", reasons
            if run.exit_status not in (0, None) and not inline and not tool_errors:
                run.outcome = "crash_or_timeout"
            return

        if summaries and not finished:
            run.outcome = "unverified"
            run.reasons = ["UVM summary is clean but $finish was never observed — "
                           "the run did not complete in an orderly way"]
            return
        if summaries and finished:
            run.outcome = "pass"
            run.reasons = ["UVM report summary with 0 UVM_ERROR / 0 UVM_FATAL "
                           "and $finish reached"]
            return
        run.outcome = "unverified"
        run.reasons = ["no pass evidence: no UVM report summary and no $finish"]

    @staticmethod
    def scan_injection(run: TestRun, text: str) -> None:
        for i, line in enumerate(text.splitlines(), start=1):
            for pattern, kind in INJECTION:
                if pattern.search(line):
                    # A genuine UVM record is never an injection, however its
                    # message text reads.
                    if UVM_MSG.match(line) or UVM_COUNT.match(line):
                        continue
                    run.injections.append(
                        {"line_no": i, "excerpt": line[:2000], "attempt_kind": kind})
                    break

    # -- the procedure -----------------------------------------------------
    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        if args.manifest:
            root = args.manifest.resolve().parent
            meta, tests = self.from_manifest(args.manifest)
        else:
            root = args.uvmstudio_report.resolve().parent
            meta, tests = self.from_uvmstudio(args.uvmstudio_report)

        prefix = TOOL_PREFIX[args.sim]
        routing = {}
        if args.routing_table and args.routing_table.exists():
            routing = json.loads(args.routing_table.read_text(encoding="utf-8"))
        elif args.routing_table:
            run.gap("routing_table_unavailable")
        else:
            run.gap("routing_table_unavailable")

        # Read every log, classify it, and note where the source disagreed.
        unreadable = 0
        disagreements = 0
        for t in tests:
            path = (root / t.log_path) if t.log_path else None
            text = None
            if path and path.exists():
                try:
                    run.allowlist.assert_readable(path, [root])
                    text = path.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    t.injections.append({"line_no": 1, "excerpt": str(t.log_path)[:2000],
                                         "attempt_kind": "path_traversal"})
            if text is None:
                unreadable += 1
                run.gap(f"missing_log:{t.test}/{t.seed}")
            else:
                run.guard_input(f"{t.test}/{t.seed}", text)
                self.scan_injection(t, text)
            self.classify(t, text, prefix)

            if t.reported_status:
                claimed = {"PASS": "pass", "FAIL": "fail",
                           "NOT_VERIFIED": "unverified"}.get(t.reported_status)
                if claimed and claimed != t.outcome:
                    disagreements += 1
                    run.gap(f"source_disagreement:{t.test}/{t.seed}:"
                            f"claimed={t.reported_status},derived={t.outcome}")
            if t.outcome == "unverified":
                run.gap(f"unverified_run:{t.test}/{t.seed}")

        # Cluster strictly on signature. The test name never enters it.
        clusters: dict[str, list[TestRun]] = {}
        for t in tests:
            if t.outcome in ("pass", "unverified", "unknown"):
                continue
            key = canonical_sha(normalise(t.signature or "unattributed"))
            clusters.setdefault(key, []).append(t)

        built = []
        for sha, members in sorted(clusters.items(),
                                   key=lambda kv: normalise(kv[1][0].signature)):
            built.append(self.build_cluster(sha, members, meta, routing, run, tests))

        totals = {
            "tests_total": len(tests),
            "pass": sum(1 for t in tests if t.outcome == "pass"),
            "fail": sum(1 for t in tests if t.outcome == "fail"),
            "unverified": sum(1 for t in tests if t.outcome == "unverified"),
            "crash_or_timeout": sum(1 for t in tests if t.outcome == "crash_or_timeout"),
            "truncated": sum(1 for t in tests if t.outcome == "truncated"),
            "unknown": sum(1 for t in tests if t.outcome == "unknown"),
            "clusters_total": len(built),
            "clusters_new": len(built),
        }
        assert sum(totals[k] for k in ("pass", "fail", "unverified",
                                       "crash_or_timeout", "truncated",
                                       "unknown")) == totals["tests_total"], \
            "the outcome counts must account for every test in the manifest"

        injections = sorted(
            ({"log_path": t.log_path, "verdict_unaffected": True,
              "action_taken": ("path_rejected" if i["attempt_kind"] == "path_traversal"
                               else "ignored_and_recorded"), **i}
             for t in tests for i in t.injections),
            key=lambda i: (i["log_path"], i["line_no"]))

        run.finding(len(built))
        run.record.input_digest = canonical_sha(
            [meta, sorted((t.test, t.seed, t.exit_status, t.log_path) for t in tests)])

        deductions = [
            Deduction("unrouted clusters", 0.10,
                      count=sum(1 for c in built if c["routed_to"] == "UNROUTED") and 1),
            Deduction("cluster with a single evidence item", 0.10,
                      count=sum(1 for c in built if len(c["evidence"]) == 1) and 1),
            Deduction("cluster without a divergence point", 0.25,
                      count=sum(1 for c in built
                                if c["earliest_divergence"]["file"] is None) and 1),
            Deduction("logs unreadable across the manifest", 0.40,
                      count=1 if unreadable else 0,
                      cap=round(0.40 * unreadable / max(len(tests), 1), 4)),
        ]
        verdict = "findings" if built or disagreements else "clean"
        return Outcome(
            fields={
                "regression_run_id": meta["regression_run_id"],
                "commit": meta["commit"],
                "totals": totals,
                "clusters": built,
                "injection_attempts": injections,
            },
            deductions=[d for d in deductions if d.count],
            verdict=verdict,
        )

    def build_cluster(self, sha: str, members: list[TestRun], meta: dict,
                      routing: dict, run: Run, tests: list[TestRun]) -> dict:
        anchor = min(members, key=lambda t: int(t.sim_time or 1 << 62))
        domain = "spec_ambiguity"
        for pattern, name in CAUSE_RULES:
            if pattern.search(anchor.signature):
                domain = name
                break
        if anchor.signature.startswith("NEG_NOT_DETECTED:"):
            # The DUT did not flag an illegal access. Named as a hypothesis,
            # because the checker is an alternative explanation the evidence
            # here cannot rule out.
            domain = "dut"

        if domain == "spec_ambiguity":
            run.gap(f"unattributed_cluster:{anchor.signature[:60]}")
        routed = routing.get(domain, "UNROUTED")
        if routed == "UNROUTED":
            run.gap(f"unrouted_cluster:{anchor.signature[:60]}")

        evidence = sorted(
            ({"log_path": t.log_path, "line_no": t.evidence[0],
              "excerpt": t.evidence[1]} for t in members if t.evidence),
            key=lambda e: (e["log_path"], e["line_no"]))
        if not evidence:  # the schema requires at least one
            evidence = [{"log_path": anchor.log_path or "(absent)", "line_no": 1,
                         "excerpt": anchor.signature or "no evidence recorded"}]

        seeds = sorted({t.seed for t in members})
        # A flake is one test at one commit disagreeing with itself across
        # seeds: some seed passed while another landed in this cluster.
        failing = {t.test for t in members}
        passing = {t.test for t in tests if t.outcome == "pass"}
        flake = bool(failing & passing)
        return {
            "cluster_id": f"{meta['regression_run_id']}:{sha[:12]}",
            "signature": anchor.signature[:160] or "unattributed",
            "signature_sha256": sha,
            "member_tests": sorted(
                ({"test": t.test, "seed": t.seed, "config": t.config,
                  "outcome": t.outcome, "exit_status": t.exit_status}
                 for t in members),
                key=lambda m: (m["test"], m["seed"])),
            "seeds": seeds,
            "first_seen_commit": meta["commit"],
            "earliest_divergence": {"file": anchor.src_file, "line": anchor.src_line,
                                     "sim_time": anchor.sim_time},
            "cause_domain": domain,
            "verdict_kind": "hypothesis" if domain in ("spec_ambiguity", "dut")
                            else "root_cause",
            "routed_to": routed,
            "confidence": round(max(0.0, 1.0
                                    - (0.30 if domain == "spec_ambiguity" else 0.0)
                                    - (0.10 if routed == "UNROUTED" else 0.0)
                                    - (0.10 if len(evidence) == 1 else 0.0)
                                    - (0.25 if anchor.src_file is None else 0.0)), 2),
            "evidence": evidence,
            "is_flake": flake,
            "dut_fail_latched": domain == "dut",
            "recurrence": {"prior_cluster_id": None, "occurrences": 1},
            "proposed_next_evidence": [
                f"rerun {anchor.test} seed {anchor.seed} with +UVM_VERBOSITY=UVM_HIGH "
                f"and attach the transaction-level log from "
                f"{max(0, int(anchor.sim_time or 0) - 2000)} onward"
            ],
            "injection_origin": False,
            "assumptions": [],
        }


if __name__ == "__main__":
    raise SystemExit(Bloodhound(__file__).main())
