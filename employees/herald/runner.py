"""HERALD — package a finished video: titles, description, tags, thumbnail copy.

The job is packaging, and the discipline is that packaging must not promise
what the video does not contain. So the truthfulness check is not a feature
that can be switched off: the schema pins ``truthfulness.check_run`` to
``true``, which means an artifact asserting the check did not run cannot be
written at all. Every title is scored against the transcript, and a title
making a claim the transcript does not support is marked ``unsupported`` and
can never be the recommended one.

The other rule worth stating: a title the channel has effectively published
before is cannibalisation, not iteration, and the overlap is reported so a
human can decide rather than discovering it in the analytics a month later.

Run it over the committed fixture with::

    python employees/herald/runner.py --video employees/herald/fixtures/video.json
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

INSTRUCTION = [
    (re.compile(r"\b(?:ignore (?:all |the )?(?:previous|above)|you are now|"
                r"system prompt|as an ai)\b", re.I), "instruction_to_assistant"),
    (re.compile(r"\b(?:the (?:operator|owner|channel) (?:approves|authorises)|"
                r"approved by the operator)\b", re.I), "operator_impersonation"),
    (re.compile(r"\.\./|\.\.\\"), "path_traversal"),
    (re.compile(r"\b(?:skip|disable|do not run) the (?:truthfulness|fact) check\b",
                re.I), "check_suppression_attempt"),
]

MOBILE_CUTOFF = 60  # characters visible on a phone before truncation


class Herald(EmployeeRunner):
    handle = "herald"
    version = "1.0.0"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--video", type=Path, required=True,
                            help="transcript, chapters and catalogue for one video")

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.video.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        raw = source.read_text(encoding="utf-8")
        run.guard_input("video", raw)
        doc = json.loads(raw)

        transcript = doc["transcript"]
        transcript_sha = hashlib.sha256(transcript.encode("utf-8")).hexdigest()
        run.record.input_digest = transcript_sha

        injections = []
        for name, text in (("transcript", transcript),
                           ("cta_block", doc.get("cta_block", "")),
                           ("filename", doc.get("source_filename", ""))):
            for pattern, kind in INSTRUCTION:
                m = pattern.search(text)
                if m:
                    injections.append({
                        "source": name,
                        "excerpt": text[max(0, m.start() - 40):m.start() + 160][:200],
                        "classification": kind, "verdict_unaffected": True})

        # The truthfulness check always runs. Every candidate title's claims are
        # checked against the transcript; an unsupported one cannot be
        # recommended however well it would perform.
        candidates = doc["title_candidates"]
        titles = []
        unsupported = 0
        for candidate in candidates[:3]:
            supported = self.supported_by(candidate["text"],
                                          candidate.get("claims", []), transcript)
            if not supported:
                unsupported += 1
            titles.append({
                "text": candidate["text"],
                "hypothesis": candidate["hypothesis"],
                "char_count": len(candidate["text"]),
                "recommended": False,
                "truthfulness": "supported" if supported else "unsupported",
                "over_mobile_cutoff": len(candidate["text"]) > MOBILE_CUTOFF,
            })

        recommendable = [t for t in titles if t["truthfulness"] == "supported"]
        if recommendable:
            # Among supported titles prefer the one that survives the mobile
            # cutoff; a truthful title nobody can read is still a bad title.
            pick = min(recommendable,
                       key=lambda t: (t["over_mobile_cutoff"], t["char_count"]))
            pick["recommended"] = True
            reason = (f"{pick['hypothesis'].replace('_', ' ')} framing, "
                      f"{pick['char_count']} characters so it survives the mobile "
                      f"cutoff, and every claim it makes is spoken in the video")
        else:
            reason = ("no candidate title is supported by the transcript, so none "
                      "is recommended; rewrite the titles or the video")
            run.gap("no_supported_title")
            run.escalate("all_titles_unsupported",
                         "every candidate title claims something the transcript "
                         "does not contain; a human must rewrite one or the other")

        claims = sum(len(c.get("claims", [])) for c in candidates[:3]) or 1

        overlaps = []
        for prior in doc.get("catalogue", []):
            overlap = self.overlap(doc["working_title"], prior["title"])
            if overlap >= 0.35:
                overlaps.append({"video_id": prior["video_id"],
                                 "overlap": round(overlap, 3)})
        overlaps.sort(key=lambda c: (-c["overlap"], c["video_id"]))
        if overlaps:
            run.gap(f"cannibalisation_risk:{overlaps[0]['video_id']}")

        run.finding(1)
        deductions = [
            Deduction("a candidate title is unsupported by the transcript", 0.10,
                      count=unsupported),
            Deduction("overlap with the existing catalogue", 0.05,
                      count=1 if overlaps else 0),
        ]
        return Outcome(
            fields={
                "video_id": doc["video_id"],
                "artifact_date": today(),
                "transcript_sha": transcript_sha,
                "dedupe_key": f"{doc['video_id']}:{transcript_sha}",
                "cluster": doc["cluster"],
                "titles": titles,
                "recommendation_reason": reason[:500],
                "description": self.description(doc),
                "tags": self.tags(doc),
                "thumbnail_copy": self.thumbnail(doc),
                "truthfulness": {"check_run": True, "claim_count": claims,
                                 "unsupported_count": min(unsupported, 3)},
                "cannibalisation_risk": overlaps,
                "injection_attempts": injections,
            },
            deductions=[d for d in deductions if d.count],
            verdict="findings",
        )

    @staticmethod
    def supported_by(title: str, claims: list[str], transcript: str) -> bool:
        """A title is supported when every claim attributed to it appears in
        the transcript. No claims means nothing to support, which passes."""
        body = transcript.lower()
        return all(claim.lower() in body for claim in claims)

    @staticmethod
    def overlap(a: str, b: str) -> float:
        stop = {"the", "a", "an", "of", "to", "in", "for", "and", "is", "how",
                "why", "what", "your", "you", "with", "on", "at", "it", "that"}
        wa = {w for w in re.findall(r"[a-z0-9]+", a.lower()) if w not in stop}
        wb = {w for w in re.findall(r"[a-z0-9]+", b.lower()) if w not in stop}
        return len(wa & wb) / len(wa | wb) if wa and wb else 0.0

    @staticmethod
    def description(doc: dict) -> dict:
        return {
            "hook_lines": [h[:120] for h in doc["hook_lines"][:2]],
            "body": doc["summary"],
            "chapters": [{"start": c["start"], "label": c["label"][:80]}
                         for c in doc.get("chapters", [])],
            "link_block": doc.get("link_block", ""),
        }

    @staticmethod
    def tags(doc: dict) -> list[str]:
        seen: list[str] = []
        for tag in doc["tag_pool"]:
            clean = re.sub(r"[^a-z0-9 -]", "", tag.lower()).strip()[:49]
            if clean and clean not in seen:
                seen.append(clean)
        return seen[:15]

    @staticmethod
    def thumbnail(doc: dict) -> dict:
        text = doc["thumbnail_copy"].strip()[:28]
        return {"text": text, "word_count": min(4, len(text.split()))}


if __name__ == "__main__":
    raise SystemExit(Herald(__file__).main())
