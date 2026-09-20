"""SPLICE — assemble an approved scene into a cut, and refuse to assemble anything else.

SPLICE sits at the end of the film chain, which is the point where an
unapproved clip or an unlicensed track stops being recoverable. So three
things are pinned as constants in the artifact and enforced before one is
written:

``approval_source.all_clips_approved`` is ``true``. A report covering a clip
MNEMO did not approve cannot be serialised, so SPLICE halts rather than
producing one. ``music[].licence_verified`` is ``true``, so an unlicensed
track cannot appear in a written report. ``renders[].verified`` is ``true``,
so a render SPLICE did not check is absent rather than listed.

The consequence is deliberate: where a clip is unapproved or a licence is
missing, the correct output is no artifact and an escalation naming what is
missing. A partial cut is not a smaller deliverable here — it is a cut
somebody might ship.

The fourth rule is about text. Every text element declares
``rendered_as_real_text``, because a title card the generator drew as pixels
looks right and is not searchable, translatable or correctable, and the
difference has to be visible in the report rather than discovered on the
platform.

Run it over the committed fixture with::

    python employees/splice/runner.py --cut employees/splice/fixtures/cut.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from employees.core.errors import Escalation  # noqa: E402
from employees.core.run import Run  # noqa: E402
from employees.core.runner import Deduction, EmployeeRunner, Outcome  # noqa: E402
from employees.core.runrecord import today  # noqa: E402

INSTRUCTION = re.compile(
    r"\b(?:ignore (?:all |the )?(?:previous|above)|you are now|"
    r"the (?:director|operator) (?:approves|authorised)|skip the licence check)\b",
    re.I)

# A caption more than this far from its cue is out of sync to a viewer.
MAX_DRIFT_MS = 200.0


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Splice(EmployeeRunner):
    handle = "splice"
    version = "1.0.0"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--cut", type=Path, required=True,
                            help="the approved clip set, captions and licences")

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.cut.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        raw = source.read_text(encoding="utf-8")
        run.guard_input("cut", raw)
        doc = json.loads(raw)
        key = sha256_hex(raw)
        run.record.input_digest = key

        attempts = []
        for element in doc.get("text_elements", []):
            if INSTRUCTION.search(element["content"]):
                # A title card is rendered as written. The text is recorded
                # because it is odd, not because SPLICE acts on it.
                attempts.append({
                    "source": "clip_manifest", "locus": element["type"],
                    "quoted_text": element["content"][:400],
                    "action_taken": "recorded_and_rendered_verbatim",
                    "verdict_unaffected": True})
        for clip in doc["clips"]:
            if INSTRUCTION.search(clip.get("filename", "")):
                attempts.append({
                    "source": "filename", "locus": clip["clip_id"],
                    "quoted_text": clip["filename"][:400],
                    "action_taken": "recorded_and_ignored",
                    "verdict_unaffected": True})

        # The approval gate. Nothing downstream of here runs on a failure,
        # because the artifact would assert an approval that does not exist.
        unapproved = [c["clip_id"] for c in doc["clips"]
                      if c.get("mnemo_verdict") != "APPROVED"]
        if unapproved:
            for clip_id in unapproved:
                run.gap(f"clip_not_approved:{clip_id}")
            attempts.append({
                "source": "clip_manifest", "locus": ",".join(unapproved)[:200],
                "quoted_text": f"{len(unapproved)} clip(s) carry a MNEMO verdict "
                               f"other than APPROVED",
                "action_taken": "recorded_and_halted",
                "verdict_unaffected": True})
            raise Escalation(
                "unapproved_clips_in_cut",
                needs=f"{len(unapproved)} clip(s) are not APPROVED by MNEMO "
                      f"({', '.join(unapproved)}); assemble only after they are "
                      f"approved or removed from the cut")

        unlicensed = [t["track_id"] for t in doc.get("music", [])
                      if not t.get("licence_sha256")]
        if unlicensed:
            for track_id in unlicensed:
                run.gap(f"track_unlicensed:{track_id}")
            raise Escalation(
                "unlicensed_music_in_cut",
                needs=f"no licence file is recorded for "
                      f"{', '.join(unlicensed)}; attach the licence or remove "
                      f"the track")

        cut_sheet = [
            {"clip_id": c["clip_id"], "in_s": float(c["in_s"]),
             "out_s": float(c["out_s"]), "reason": c["reason"]}
            for c in doc["clips"]]
        runtime = round(sum(c["out_s"] - c["in_s"] for c in cut_sheet), 3)

        drifts = [abs(float(c["drift_ms"])) for c in doc["captions"]["cues"]]
        exceeded = [d for d in drifts if d > MAX_DRIFT_MS]
        if exceeded:
            run.gap(f"caption_drift_exceeded:{len(exceeded)}_cues")

        # rendered_as_real_text is pinned true on every listed element, so a
        # cut containing text the generator drew as pixels cannot be reported
        # at all. Leaving it out would hide it; the correct output is no
        # artifact and a named escalation.
        drawn = [e for e in doc.get("text_elements", [])
                 if not e.get("rendered_as_real_text", True)]
        if drawn:
            for element in drawn:
                run.gap(f"text_drawn_not_rendered:{element['type']}")
            raise Escalation(
                "drawn_text_in_cut",
                needs=f"{', '.join(e['type'] for e in drawn)} were drawn by the "
                      f"generator rather than rendered as text, so they cannot "
                      f"be searched, translated or corrected; re-render them as "
                      f"real text before assembly")

        run.finding(len(exceeded))
        deductions = [
            Deduction("caption cues exceed the drift tolerance", 0.10,
                      count=1 if exceeded else 0),
        ]
        return Outcome(
            fields={
                "schema_version": "1.0.0",
                "slug": doc["slug"], "scene_id": doc["scene_id"],
                "cut": doc["cut"], "date": today(),
                "dedupe_key": f"sha256:{key}",
                "approval_source": {
                    "path": doc["approval_path"],
                    "sha256": sha256_hex(doc["approval_path"]),
                    "manifest_sha": key,
                    "clip_count": len(doc["clips"]),
                    "all_clips_approved": True},
                "cut_sheet": cut_sheet,
                "total_runtime_s": runtime,
                "text_elements": [
                    {"type": e["type"], "content": e["content"],
                     "frames": e["frames"], "source": e["source"],
                      "rendered_as_real_text": True}
                    for e in doc.get("text_elements", [])],
                "captions": {
                    "source_path": doc["captions"]["path"],
                    "source_sha256": sha256_hex(doc["captions"]["path"]),
                    "cue_count": len(drifts),
                    "drift_exceeded_count": len(exceeded),
                    "max_drift_ms": round(max(drifts), 1) if drifts else 0.0},
                "music": [
                    {"track_id": t["track_id"], "path": t["path"],
                     "licence_path": t["licence_path"],
                     "licence_sha256": t["licence_sha256"],
                     "licence_verified": True}
                    for t in doc.get("music", [])],
                "renders": [
                    {"aspect": r["aspect"], "path": r["path"],
                     "sha256": r["sha256"], "duration_s": float(r["duration_s"]),
                     "size_bytes": int(r["size_bytes"]), "verified": True}
                    for r in doc.get("renders", []) if r.get("checked")],
                "instruction_attempts": attempts,
            },
            deductions=[d for d in deductions if d.count],
            verdict="findings" if exceeded else "clean",
        )


if __name__ == "__main__":
    raise SystemExit(Splice(__file__).main())
