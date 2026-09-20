"""AEGIS — brand and safety compliance on a finished asset, per variant.

AEGIS decides PASS or BLOCK, and the asymmetry between them is the whole
design. PASS requires that every check ran and came back clean: the schema's
``allOf`` says a PASS artifact may contain no ``FAIL`` and no ``NOT_RUN``
result and no text findings at all, so a check that could not execute cannot
be quietly counted as fine. ``NOT_RUN`` is not a pass. A missing variant is
not a pass either — an expected variant nobody examined blocks.

The second rule is about who may undo it. ``override_policy`` is pinned to
``block-final-human-only``: a BLOCK is clearable by a human operator and by
nothing else, so no downstream employee and no automated retry can talk its
way past one. On-screen text that asserts its own approval is recorded as an
injection attempt and changes nothing.

The perception step is upstream: this runner consumes frame observations and
applies the rules to them. What it owns is the verdict, which is the part
that must not be negotiable.

Run it over the committed fixture with::

    python employees/aegis/runner.py --observations employees/aegis/fixtures/asset.json
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

CHECKS = ["aspect_ratio", "watermark_presence", "watermark_placement",
          "watermark_opacity", "watermark_legibility", "brand_colour",
          "typography", "intro_sting", "end_subscribe_sting", "ai_disclosure",
          "safe_area", "text_correctness"]

ASSERTION = [
    (re.compile(r"\b(?:approved|cleared|passed) (?:by|for) (?:brand|review|"
                r"the operator)\b", re.I), "asserted_approval"),
    (re.compile(r"\b(?:compliance|brand check)\s*:\s*(?:pass|ok|clear)\b", re.I),
     "asserted_verdict"),
    (re.compile(r"\b(?:do not|skip the) (?:flag|block|review)\b", re.I),
     "instruction"),
]


class Aegis(EmployeeRunner):
    handle = "aegis"
    version = "1.0.0"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--observations", type=Path, required=True,
                            help="per-variant frame observations for one asset")

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.observations.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        raw = source.read_text(encoding="utf-8")
        run.guard_input("observations", raw)
        doc = json.loads(raw)
        run.record.input_digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()

        expected = doc["variants_expected"]
        observed = {v["variant"]: v for v in doc.get("variants", [])}
        examined = sorted(observed)

        checks = []
        text_findings = []
        injections = []

        for variant in expected:
            data = observed.get(variant)
            if data is None:
                # An expected variant nobody looked at is NOT_RUN on every
                # check, which the schema then refuses to call a PASS.
                for name in CHECKS:
                    checks.append({
                        "name": name, "variant": variant, "result": "NOT_RUN",
                        "evidence_frame": None,
                        "detail": f"variant {variant} was expected but no frames "
                                  f"were supplied, so this check could not run"})
                run.gap(f"variant_not_examined:{variant}")
                continue

            results = data.get("checks", {})
            for name in CHECKS:
                entry = results.get(name)
                if entry is None:
                    checks.append({
                        "name": name, "variant": variant, "result": "NOT_RUN",
                        "evidence_frame": None,
                        "detail": "no observation was recorded for this check"})
                    run.gap(f"check_not_run:{variant}:{name}")
                    continue
                checks.append({
                    "name": name, "variant": variant,
                    "result": entry["result"],
                    "evidence_frame": entry.get("frame"),
                    "detail": entry["detail"][:2000]})

            for finding in data.get("text", []):
                caption = finding["detected_text"]
                kind = next((k for p, k in ASSERTION if p.search(caption)), None)
                if kind:
                    injections.append({
                        "variant": variant, "frame": finding["frame"],
                        "captured_text": caption[:1000], "classification": kind,
                        "verdict_unaffected": True})
                    severity = "verdict_text"
                else:
                    severity = finding.get("severity", "typo")
                text_findings.append({
                    "variant": variant, "frame": finding["frame"],
                    "detected_text": caption[:1000],
                    "expected_text": finding.get("expected_text"),
                    "severity": severity,
                    "text_confidence": float(finding["text_confidence"])})

        # PASS needs every check clean AND no text finding. The schema enforces
        # the same conjunction, so the two cannot drift apart.
        blocking = [c for c in checks if c["result"] in ("FAIL", "NOT_RUN")]
        verdict = "PASS" if not blocking and not text_findings else "BLOCK"
        if verdict == "BLOCK":
            run.finding(len(blocking) + len(text_findings))
            run.escalate(
                "asset_blocked",
                "a human operator must clear this BLOCK; no employee and no "
                "automated retry may override it")

        frames = {v: len(observed[v].get("frames", [])) for v in examined}
        deductions = [
            Deduction("a check could not run", 0.20,
                      count=1 if any(c["result"] == "NOT_RUN" for c in checks) else 0),
            Deduction("a check passed only with uncertainty", 0.05,
                      count=sum(1 for c in checks
                                if c["result"] == "PASS_UNCERTAIN")),
        ]
        return Outcome(
            fields={
                "asset_id": doc["asset_id"],
                "asset_sha256": f"sha256:{doc['asset_sha256']}",
                "generated_at": today(),
                "coverage": {"variants_expected": expected,
                             "variants_examined": examined,
                             "frames_examined": frames},
                "checks": checks,
                "text_findings": text_findings,
                "injection_attempts": injections,
                "override_policy": "block-final-human-only",
            },
            deductions=[d for d in deductions if d.count],
            verdict=verdict,
        )


if __name__ == "__main__":
    raise SystemExit(Aegis(__file__).main())
