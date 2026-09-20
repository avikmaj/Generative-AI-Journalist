"""GENESIS — turn a premise into a lock that everything downstream must obey.

GENESIS writes the bible: structure, characters with their identity tokens,
world rules, style. Everything after it — APERTURE's prompts, MNEMO's
continuity findings, SPLICE's cut — is judged against this document, which is
why the one thing GENESIS must never do is generate.

``generation_scope`` pins all three of ``clips_generated: 0``,
``usd_generation_spent: 0`` and ``shot_list_produced: false`` as constants. A
GENESIS artifact claiming it produced a shot list or spent a cent on
generation cannot be serialised. The temptation is real — a premise often
arrives with "and go ahead and generate the first scene" attached — and the
schema is where that temptation is refused rather than in a paragraph asking
nicely.

The second rule is that a contradiction is recorded, not resolved. Where the
premise says one thing and the series bible another, GENESIS emits a
consistency finding naming both sides and does not pick. Picking would bake a
guess into a lock that twelve later shots inherit.

Run it over the committed fixture with::

    python employees/genesis/runner.py --premise employees/genesis/fixtures/premise.json
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

SUSPECT = [
    (re.compile(r"\b(?:skip|ignore|drop) the (?:lock|bible|continuity)\b", re.I),
     "instruction_to_skip_a_lock"),
    (re.compile(r"\b(?:let the (?:model|generator) decide|the generator will "
                r"(?:work|figure) (?:it|this) out)\b", re.I),
     "instruction_to_defer_lock_to_generator"),
    (re.compile(r"\byou are (?:now )?(?:the )?(?:director|editor|producer)\b", re.I),
     "role_reassignment"),
    (re.compile(r"\b(?:generate|render|produce) (?:the )?(?:first )?"
                r"(?:scene|shot|clip)s?\b", re.I),
     "out_of_scope_shot_request"),
    (re.compile(r"\.\./|\.\.\\"), "path_or_filename_directive"),
]

# An identity token below this many descriptors will not hold a face across
# shots; the count is reported so the weakness is visible rather than implied.
MIN_DESCRIPTORS = 6


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Genesis(EmployeeRunner):
    handle = "genesis"
    version = "1.0.0"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--premise", type=Path, required=True,
                            help="the premise and any series bible to lock from")
        parser.add_argument("--format", dest="fmt",
                            help="delivery format; defaults to the series default")

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        source = args.premise.resolve()
        run.allowlist.assert_readable(source, [source.parent])
        raw = source.read_text(encoding="utf-8")
        run.guard_input("premise", raw)
        doc = json.loads(raw)
        run.record.input_digest = sha256_hex(raw)

        injections = []
        for field, kind in (("premise", "premise"), ("series_bible", "series_bible")):
            text = doc.get(field) or ""
            for pattern, classification in SUSPECT:
                m = pattern.search(text)
                if m:
                    injections.append({
                        "source": kind,
                        "excerpt": text[max(0, m.start() - 30):m.start() + 180][:240],
                        "classification": classification,
                        "verdict_unaffected": True})
        if injections:
            run.gap(f"directive_text_in_premise:{len(injections)}")

        fmt = args.fmt or doc.get("default_format", "short-form 9:16")
        assumptions = []
        if not args.fmt:
            assumptions.append({
                "field": "format", "value": fmt,
                "basis": "no --format was supplied, so the series default was used"})

        characters = []
        for entry in doc["characters"]:
            token = entry["identity_token"]
            descriptors = len([p for p in re.split(r"[;,]", token) if p.strip()])
            if descriptors < MIN_DESCRIPTORS:
                run.gap(f"thin_identity_token:{entry['name']}:{descriptors}"
                        f"_descriptors")
            characters.append({
                "name": entry["name"],
                "identity_token": token,
                "identity_token_descriptor_count": descriptors,
                "wardrobe_by_sequence": entry["wardrobe_by_sequence"],
                "continuity_notes": entry.get("continuity_notes", []),
            })

        structure = [
            {"sequence": i, "beat": b["beat"], "purpose": b["purpose"],
             "est_clips": int(b["est_clips"]), "location": b["location"]}
            for i, b in enumerate(doc["structure"], start=1)]

        findings = self.consistency(doc, structure, characters)
        for finding in findings:
            run.gap(f"{finding['kind']}:{finding['finding_id']}")
        run.finding(len(findings))

        # Shooting order groups by location, because a location change is the
        # expensive move; the count of splits is reported so the saving is
        # checkable rather than asserted.
        order, splits = self.shooting_order(structure)

        deductions = [
            Deduction("the premise and the bible contradict each other", 0.15,
                      count=sum(1 for f in findings
                                if f["kind"] == "contradiction")),
            Deduction("an identity token is too thin to hold a face", 0.10,
                      count=sum(1 for c in characters
                                if c["identity_token_descriptor_count"]
                                < MIN_DESCRIPTORS)),
            Deduction("directive-shaped text in the premise", 0.05,
                      count=1 if injections else 0),
        ]
        return Outcome(
            fields={
                "slug": doc["slug"],
                "premise_sha256": f"sha256:{sha256_hex(doc['premise'])}",
                "dedupe_key": f"{sha256_hex(doc['premise'])}::{doc['slug']}",
                "format": fmt, "format_source": "run_parameter" if args.fmt
                                                else "default",
                "aspect_ratio_source": "format",
                "lock_version": int(doc.get("lock_version", 1)),
                "locked_at": today(),
                "generation_scope": {"clips_generated": 0,
                                     "usd_generation_spent": 0,
                                     "shot_list_produced": False},
                "logline": doc["logline"],
                "structure": structure,
                "characters": characters,
                "world": doc["world"],
                "consistency_findings": findings,
                "style": doc["style"],
                "shooting_order": order,
                "shooting_order_est_clips_total": sum(o["est_clips"] for o in order),
                "location_splits": splits,
                "lock_diff": [],
                "orphan_analysis": "not_applicable",
                "orphan_analysis_note": "this is the first lock for this slug, so "
                                        "no prior clips can have been orphaned",
                "orphaned_clips": [],
                "injection_attempts": injections,
                "assumptions": assumptions,
            },
            deductions=[d for d in deductions if d.count],
            verdict="findings" if findings else "clean",
        )

    @staticmethod
    def consistency(doc: dict, structure: list[dict],
                    characters: list[dict]) -> list[dict]:
        """Name contradictions. Never resolve one — a lock inherits the guess."""
        out = []
        locations = {loc["name"] for loc in doc["world"]["locations"]}
        for beat in structure:
            if beat["location"] not in locations:
                out.append({
                    "finding_id": f"CF-{len(out) + 1:03d}", "kind": "undetermined",
                    "side_a": f"structure sequence {beat['sequence']} is set in "
                              f"{beat['location']!r}",
                    "side_b": "the world lock defines no such location",
                    "detail": "the beat cannot be shot against a locked location, "
                              "so either the location or the beat must be added "
                              "before any shot is written"})
        for character in characters:
            # A wardrobe entry is a change point, not a per-sequence statement:
            # what is locked at sequence 4 is still worn at 5 and 6. Only the
            # sequences before the first entry are genuinely unstated, and
            # flagging the rest would bury the real gap in noise.
            worn = sorted(w["sequence"] for w in character["wardrobe_by_sequence"])
            if not worn:
                continue
            uncovered = sorted(b["sequence"] for b in structure
                               if b["sequence"] < worn[0])
            if uncovered:
                out.append({
                    "finding_id": f"CF-{len(out) + 1:03d}", "kind": "undetermined",
                    "side_a": f"{character['name']}'s wardrobe is first locked at "
                              f"sequence {worn[0]}",
                    "side_b": f"the structure begins at sequence {uncovered[0]}",
                    "detail": f"sequences {uncovered} precede any wardrobe lock, "
                              f"so a generator would choose the costume for them "
                              f"and continuity would drift from the first shot"})
        for claim in doc.get("bible_claims", []):
            if claim["premise_says"] != claim["bible_says"]:
                out.append({
                    "finding_id": f"CF-{len(out) + 1:03d}", "kind": "contradiction",
                    "side_a": f"premise: {claim['premise_says']}",
                    "side_b": f"series bible: {claim['bible_says']}",
                    "detail": f"{claim['about']} is stated two ways; a human must "
                              f"choose before this is locked"})
        return out

    @staticmethod
    def shooting_order(structure: list[dict]) -> tuple[list[dict], int]:
        by_location: dict[str, list[dict]] = {}
        for beat in structure:
            by_location.setdefault(beat["location"], []).append(beat)
        order = []
        for location, beats in sorted(by_location.items(),
                                      key=lambda kv: min(b["sequence"]
                                                         for b in kv[1])):
            for beat in beats:
                order.append({
                    "sequence": beat["sequence"],
                    "rationale": f"grouped with the other {location} beats so the "
                                 f"location is lit and struck once",
                    "location": location,
                    "est_clips": beat["est_clips"]})
        # A split is a return to a location already left behind.
        seen, splits, previous = set(), 0, None
        for entry in order:
            if previous is not None and entry["location"] != previous:
                if entry["location"] in seen:
                    splits += 1
            seen.add(entry["location"])
            previous = entry["location"]
        return order, splits


if __name__ == "__main__":
    raise SystemExit(Genesis(__file__).main())
