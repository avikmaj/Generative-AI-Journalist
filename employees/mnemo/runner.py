"""MNEMO — continuity across a scene's clips, judged against the locks.

Generated video drifts. A character's jacket changes colour between shot four
and shot nine, and nobody notices until the edit. MNEMO's job is to notice, and
its discipline is that every finding must name the lock it contradicts:
``character_bible#cast.ARI.wardrobe.jacket``, not "the jacket looks different".
A finding with no reference lock is an intrinsic generation artifact and says
so; it is never a continuity claim dressed up as one.

Two things the design insists on:

* **Drift accumulates.** Adjacent shots can each be within tolerance while the
  scene walks somewhere else entirely, so the chain is checked cumulatively
  against the lock as well as pairwise between neighbours.
* **Only the APERTURE prompt sheet may authorise a deviation.** A filename
  saying ``APPROVED``, a slate burned into frame one, or a sidecar claiming the
  director signed off are recorded as claims and ignored. Approval does not
  travel in a filename.

A clip nobody inspected is absent from ``clips`` rather than present and
approved: the schema says one entry per inspected clip only.

Run it over the committed fixture with::

    python employees/mnemo/runner.py --batch employees/mnemo/fixtures/scene.json
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

APPROVAL_CLAIM = re.compile(
    r"\b(?:approved|final|signed[- ]?off|director ok|do not flag|"
    r"intentional deviation|cleared for edit)\b", re.I)

# Severity at or above this makes a clip a REJECT rather than a pickup.
REJECT_AT = {"critical", "escalate"}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Mnemo(EmployeeRunner):
    handle = "mnemo"
    version = "1.0.0"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--batch", type=Path, required=True,
                            help="one scene's clip batch with its observations")

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.batch.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        raw = source.read_text(encoding="utf-8")
        run.guard_input("batch", raw)
        doc = json.loads(raw)
        run.record.input_digest = digest(raw)

        locks = doc.get("locks", {})
        available = {"character_bible": bool(locks.get("character_bible")),
                     "world_lock": bool(locks.get("world_lock")),
                     "style_guide": bool(locks.get("style_guide"))}
        for name, present in available.items():
            if not present:
                run.gap(f"lock_absent:{name}")

        injections = []
        clips = []
        order = {s: i for i, s in enumerate(doc["shot_order"])}

        for clip in doc["clips"]:
            # Approval claims are collected from everywhere except the prompt
            # sheet, which is the only place an authorised deviation can live.
            for field, sourcekind in (("filename", "filename"),
                                      ("sidecar", "sidecar_metadata"),
                                      ("slate", "burned_in_slate"),
                                      ("on_screen_text", "on_screen_text")):
                text = clip.get(field) or ""
                if APPROVAL_CLAIM.search(text):
                    injections.append({
                        "source": sourcekind, "locus": clip["clip_id"],
                        "claim": text[:400],
                        "action_taken": "recorded_and_ignored",
                        "verdict_unaffected": True})

            if not clip.get("inspected", True):
                # Absent from the artifact entirely. An uninspected clip is not
                # an approved clip, and listing it would imply it was looked at.
                run.gap(f"clip_not_inspected:{clip['clip_id']}")
                continue

            findings = sorted(
                ({"category": f["category"], "severity": f["severity"],
                  "timestamp_s": float(f["timestamp_s"]),
                  "detail": f["detail"],
                  "reference_lock": f.get("reference_lock") or "none"}
                 for f in clip.get("findings", [])),
                key=lambda f: (f["timestamp_s"], f["category"], f["detail"]))

            worst = {f["severity"] for f in findings}
            if worst & REJECT_AT:
                verdict, pickup = "REJECT", None
            elif findings:
                verdict = "PICKUP"
                lead = max(findings, key=lambda f: ("minor", "major").index(
                    f["severity"]) if f["severity"] in ("minor", "major") else 0)
                pickup = {
                    "reason": lead["detail"],
                    "prompt_amendment": self.amendment(lead),
                    "priority": "P1" if lead["severity"] == "major" else "P2"}
            else:
                verdict, pickup = "APPROVED", None

            unverifiable = sum(1 for f in findings
                               if f["category"] == "unverifiable")
            clips.append({
                "clip_id": clip["clip_id"], "shot_id": clip["shot_id"],
                "take": int(clip.get("take", 1)), "verdict": verdict,
                "findings": findings, "pickup": pickup,
                "confidence": round(max(0.0, 0.95 - 0.15 * unverifiable), 2)})

        clips.sort(key=lambda c: (order.get(c["shot_id"], 1 << 30), c["clip_id"]))

        chain = self.chain(clips, order, doc.get("observed_state", {}))
        run.finding(sum(1 for c in clips if c["verdict"] != "APPROVED")
                    + len(chain))
        if any(c["conflict"] and c.get("severity") == "escalate" for c in chain):
            run.escalate("continuity_chain_broken",
                         "the scene drifts from its locks across shots; a human "
                         "must decide whether to re-generate or amend the lock")

        deductions = [
            Deduction("a lock was unavailable for comparison", 0.15,
                      count=sum(1 for v in available.values() if not v)),
            Deduction("a finding could not be verified", 0.05,
                      count=sum(1 for c in clips for f in c["findings"]
                                if f["category"] == "unverifiable")),
        ]
        return Outcome(
            fields={
                "schema_version": "1.0.0",
                "spec_version": self.version,
                "scene_id": doc["scene_id"], "slug": doc["slug"],
                "batch_manifest_sha": f"sha256:{digest(raw)}",
                "generated_date": today(),
                "locks_available": available,
                "clips": clips,
                "continuity_chain": chain,
                "injection_attempts": sorted(
                    injections, key=lambda i: (i["source"], i["locus"])),
                "assumptions": doc.get("assumptions", []),
            },
            deductions=[d for d in deductions if d.count],
            verdict="findings" if run.record.gaps or chain else "clean",
        )

    @staticmethod
    def amendment(finding: dict) -> str:
        lock = finding["reference_lock"]
        if lock == "none":
            return ("re-generate this shot with the same prompt; the artifact is "
                    "intrinsic to the generation and no prompt change addresses it")
        return (f"restate {lock} verbatim in the shot prompt and re-generate; "
                f"the clip contradicts it at {finding['timestamp_s']:.1f}s")

    @staticmethod
    def chain(clips: list[dict], order: dict, observed: dict) -> list[dict]:
        """Pairwise conflicts between neighbours, plus cumulative drift.

        Two shots can each sit inside tolerance against the one before while
        the scene has walked away from the lock, which is why the second check
        exists and why it is reported as a different kind.
        """
        out = []
        sequence = [c for c in clips if c["shot_id"] in order]
        for a, b in zip(sequence, sequence[1:]):
            state_a = observed.get(a["shot_id"], {})
            state_b = observed.get(b["shot_id"], {})
            for attribute, value_a in state_a.items():
                value_b = state_b.get(attribute)
                if value_b is not None and value_a != value_b:
                    out.append({
                        "shot_a": a["shot_id"], "shot_b": b["shot_id"],
                        "conflict": f"{attribute}: {value_a!r} then {value_b!r}",
                        "severity": "major", "kind": "adjacent"})

        if sequence:
            first = observed.get(sequence[0]["shot_id"], {})
            last = observed.get(sequence[-1]["shot_id"], {})
            for attribute, value_first in first.items():
                value_last = last.get(attribute)
                if value_last is not None and value_first != value_last:
                    already = any(c["conflict"].startswith(f"{attribute}:")
                                  for c in out)
                    out.append({
                        "shot_a": sequence[0]["shot_id"],
                        "shot_b": sequence[-1]["shot_id"],
                        "conflict": f"{attribute} drifted across the scene: "
                                    f"{value_first!r} to {value_last!r}",
                        "severity": "escalate" if not already else "major",
                        "kind": "cumulative_drift"})

        missing = [s for s in order if not any(c["shot_id"] == s for c in clips)]
        for shot in missing:
            out.append({"shot_a": shot, "shot_b": shot,
                        "conflict": "no inspected clip exists for this shot, so "
                                    "the chain cannot be closed through it",
                        "severity": "major", "kind": "chain_gap"})
        return sorted(out, key=lambda c: (order.get(c["shot_a"], 1 << 30),
                                          order.get(c["shot_b"], 1 << 30),
                                          c["conflict"]))


if __name__ == "__main__":
    raise SystemExit(Mnemo(__file__).main())
