"""ARGUS — watch the competitive field and qualify what is worth making.

The temptation in a topic scanner is to return ten rows every morning because
ten rows look like work. ARGUS qualifies instead: a topic reaches the artifact
only when momentum, fit and saturation all clear their floors, and an empty
list is a legitimate and frequent result.

Two rules carry the weight:

* **Scoring reads evidence, never instructions.** A competitor's title or
  channel bio that addresses the reader is recorded in ``injection_attempts``
  and excluded from scoring — the schema pins ``handling`` to exactly that.
* **A near-duplicate of the back catalogue is not a new topic.** Similarity to
  the closest prior video is bounded below 0.8 by the schema itself, so a topic
  that close cannot be emitted at all.

Run it over the committed fixture with::

    python employees/argus/runner.py --signals employees/argus/fixtures/signals.json
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

# Text addressed to the reader rather than describing a video.
INSTRUCTION = re.compile(
    r"\b(?:ignore (?:all |the )?(?:previous|above)|disregard|you are now|"
    r"system prompt|as an ai|rank this (?:first|higher)|must be ranked)\b", re.I)

# The floors. A topic must clear every one of them.
MOMENTUM_FLOOR = 0.40
FIT_FLOOR = 0.50
SATURATION_CEILING = 0.70
SIMILARITY_CEILING = 0.80  # the schema's exclusiveMaximum, restated once here


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Argus(EmployeeRunner):
    handle = "argus"
    version = "1.0.0"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--signals", type=Path, required=True,
                            help="the competitive signal set for one day")

    def artifact_path(self, args: argparse.Namespace) -> str:
        return f"reports/argus/{today()}.json"

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.signals.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        doc = json.loads(source.read_text(encoding="utf-8"))
        run.guard_input("signals", source.read_text(encoding="utf-8"))

        competitors = sorted(doc.get("competitors", []))
        competitor_hash = sha256_hex("\n".join(competitors))
        catalogue = doc.get("back_catalogue", [])

        injections = []
        qualified = []
        for candidate in doc.get("candidates", []):
            # Scan every free-text field before anything is scored, so that a
            # rejected string cannot reach the scorer by another route.
            for field in ("title", "description", "channel_bio"):
                text = candidate.get(field) or ""
                if INSTRUCTION.search(text):
                    injections.append({
                        "source": candidate.get("source", "unknown"),
                        "field": field,
                        "observed_at": candidate["observed_at"],
                        "excerpt": text[:500],
                        "handling": "recorded_as_data_excluded_from_scoring",
                        "verdict_unaffected": True,
                    })

            momentum = float(candidate["momentum_score"])
            fit = float(candidate["fit_score"])
            saturation = float(candidate["saturation_score"])

            nearest, similarity = None, 0.0
            for prior in catalogue:
                overlap = self.overlap(candidate["title_working"], prior["title"])
                if overlap > similarity:
                    nearest, similarity = prior, overlap

            if similarity >= SIMILARITY_CEILING:
                run.gap(f"near_duplicate_of_back_catalogue:"
                        f"{candidate['title_working'][:48]}")
                continue
            if momentum < MOMENTUM_FLOOR or fit < FIT_FLOOR \
                    or saturation > SATURATION_CEILING:
                continue

            qualified.append({
                "title_working": candidate["title_working"],
                "angle": candidate["angle"],
                "why_now": candidate["why_now"],
                "momentum_score": round(momentum, 3),
                "fit_score": fit,
                "saturation_score": round(saturation, 3),
                # Saturation subtracts: a crowded topic is worth less however
                # fast it is moving.
                "composite_rank": round(
                    max(0.0, min(1.0, 0.45 * momentum + 0.40 * fit
                                 - 0.15 * saturation)), 4),
                "evidence": candidate["evidence"],
                "closest_prior_video": (
                    None if nearest is None else {
                        "video_id": nearest["video_id"], "title": nearest["title"],
                        "published_at": nearest["published_at"],
                        "similarity": round(similarity, 3)}),
                "confidence": round(min(1.0, 0.55 + 0.45 * momentum), 2),
            })

        qualified.sort(key=lambda t: (-t["composite_rank"], t["title_working"]))
        topics = []
        for rank, topic in enumerate(qualified[:10], start=1):
            topics.append({"rank": rank, **topic})

        if not topics:
            run.gap("no candidate cleared the momentum, fit and saturation floors")
        run.finding(len(topics))
        run.record.input_digest = sha256_hex(json.dumps(doc, sort_keys=True))

        thin = [t for t in topics if len(t["evidence"]) == 1]
        deductions = [
            Deduction("topics resting on a single evidence item", 0.10,
                      count=1 if thin else 0),
            Deduction("instruction-shaped text in the signal set", 0.05,
                      count=1 if injections else 0),
        ]
        return Outcome(
            fields={
                "schema_version": "1.0.0",
                "date": today(),
                "competitor_set_hash": competitor_hash,
                "dedupe_key": f"{today()}:{competitor_hash[:16]}",
                "run_status": "ok" if topics and not run.record.gaps else "partial",
                "topics_qualified": len(topics),
                "topics": topics,
                "injection_attempts": injections,
            },
            deductions=[d for d in deductions if d.count],
            verdict="findings" if topics else "clean",
        )

    @staticmethod
    def overlap(a: str, b: str) -> float:
        """Jaccard overlap on content words. Crude on purpose: it decides only
        whether a human should look, and the schema refuses anything close."""
        stop = {"the", "a", "an", "of", "to", "in", "for", "and", "is", "how",
                "why", "what", "your", "you", "with", "on", "at", "it"}
        wa = {w for w in re.findall(r"[a-z0-9]+", a.lower()) if w not in stop}
        wb = {w for w in re.findall(r"[a-z0-9]+", b.lower()) if w not in stop}
        if not wa or not wb:
            return 0.0
        return len(wa & wb) / len(wa | wb)


if __name__ == "__main__":
    raise SystemExit(Argus(__file__).main())
