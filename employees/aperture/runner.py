"""APERTURE — turn a locked scene into shot prompts, one per target model.

APERTURE is the only place an identity token is copied into a prompt, and the
copy is byte-exact or it does not happen. ``identity_tokens_used[].copied_verbatim``
is pinned ``true`` and ``token_integrity_violations[].emitted`` is pinned
``false``: a token that failed the comparison is recorded as a violation and
is *absent* from every prompt. The schema makes the alternative unwritable,
which matters because a token paraphrased by one character drifts a face
across twelve shots and nobody can see why.

The second discipline is about not inventing. Where the lock does not say what
a shot needs — a location's time of day, a character's wardrobe at this
sequence — APERTURE does not choose. It emits an escalation target naming the
missing field and its owner, which the schema pins to ``GENESIS``, because the
lock is where that decision belongs.

Cost is reported with its completeness attached. A model whose per-clip price
is unknown contributes nothing to the total and sets ``cost_complete: false``,
so a total is never quietly short.

Run it over the committed fixture with::

    python employees/aperture/runner.py \\
        --lock employees/genesis/fixtures/premise.json \\
        --scene employees/aperture/fixtures/scene.json
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

DIRECTIVE = [
    (re.compile(r"\b(?:ignore|override) the (?:lock|token|bible)\b", re.I),
     "directive-shaped-text"),
    (re.compile(r"\b(?:the director|the operator) (?:approves|says|authorised)\b",
                re.I), "operator-impersonation"),
    (re.compile(r"\.\./|\.\.\\"), "path-traversal-attempt"),
]

# Per-clip cost by model. A model absent here has an unknown price, which is
# reported as unknown rather than guessed at zero.
MODEL_COST_USD = {"veo-3": 0.48, "sora-2": 0.35}

NEGATIVE = ("text, watermark, subtitles, logo, extra fingers, deformed hands, "
            "duplicate face, warped glasses, modern signage, daylight")


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Aperture(EmployeeRunner):
    handle = "aperture"
    version = "1.0.0"
    confidence_threshold = 0.70

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--lock", type=Path, required=True,
                            help="the GENESIS lock this scene is written against")
        parser.add_argument("--scene", type=Path, required=True,
                            help="the scene's shot intents")
        parser.add_argument("--models", default="veo-3,sora-2",
                            help="comma-separated target models")

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        lock_path, scene_path = args.lock.resolve(), args.scene.resolve()
        for path in (lock_path, scene_path):
            run.allowlist.assert_readable(path, [path.parent])
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        scene_raw = scene_path.read_text(encoding="utf-8")
        run.guard_input("scene", scene_raw)
        scene = json.loads(scene_raw)
        run.record.input_digest = sha256_hex(scene_raw)

        models = [m.strip() for m in args.models.split(",") if m.strip()]
        lock_version = str(lock.get("lock_version", 1))

        # The tokens as the lock states them, by digest. Nothing else is ever
        # compared against.
        lock_tokens = {c["name"]: c["identity_token"] for c in lock["characters"]}
        locations = {loc["name"]: loc for loc in lock["world"]["locations"]}
        wardrobe = {c["name"]: sorted(c["wardrobe_by_sequence"],
                                      key=lambda w: w["sequence"])
                    for c in lock["characters"]}

        injections, violations, escalations, shots = [], [], [], []
        gaps: list[dict] = []
        cost_complete = True
        total_cost = 0.0

        for index, spec in enumerate(scene["shots"], start=1):
            shot_id = f"{scene['scene_id']}-S{index:02d}"

            for field in ("intent", "note"):
                text = spec.get(field) or ""
                for pattern, classification in DIRECTIVE:
                    m = pattern.search(text)
                    if m:
                        injections.append({
                            "source": f"{shot_id}.{field}",
                            "excerpt": text[max(0, m.start() - 30):
                                            m.start() + 200][:2000],
                            "classification": classification,
                            "action_taken": "recorded; the lock was used as "
                                            "written and the text was not obeyed",
                            "verdict_unaffected": True})

            tokens = []
            for entity in spec.get("entities", []):
                locked = lock_tokens.get(entity)
                supplied = spec.get("entity_tokens", {}).get(entity, locked)
                if locked is None:
                    escalations.append({
                        "shot_id": shot_id, "missing_field": f"identity_token[{entity}]",
                        "owner": "GENESIS",
                        "needs": f"{entity} appears in this shot but the lock "
                                 f"defines no identity token for it"})
                    continue
                if supplied != locked:
                    # Recorded, and not emitted. The prompt gets the locked
                    # token or the entity is absent from it.
                    violations.append({
                        "entity_id": entity,
                        "lock_token_sha256": sha256_hex(locked),
                        "observed_token_sha256": sha256_hex(supplied),
                        "emitted": False})
                    injections.append({
                        "source": f"{shot_id}.entity_tokens[{entity}]",
                        "excerpt": supplied[:2000],
                        "classification": "altered-identity-token",
                        "action_taken": "discarded; the shot uses the token as "
                                        "the lock states it",
                        "verdict_unaffected": True})
                tokens.append({"entity_id": entity, "token": locked,
                               "copied_verbatim": True})

            location = locations.get(spec["location"])
            if location is None:
                escalations.append({
                    "shot_id": shot_id, "missing_field": "location",
                    "owner": "GENESIS",
                    "needs": f"the lock defines no location named "
                             f"{spec['location']!r}"})
                gaps.append({
                    "code": "shot-omitted",
                    "detail": f"{shot_id} names location {spec['location']!r}, "
                              f"which the lock does not define",
                    "impact": "the shot is not written; writing it would invent "
                              "a location the lock does not contain"})
                run.gap(f"unlocked_location:{shot_id}")
                continue

            costume = self.costume(wardrobe, spec.get("entities", []),
                                   int(spec["sequence"]))
            if costume is None and spec.get("entities"):
                escalations.append({
                    "shot_id": shot_id, "missing_field": "wardrobe_by_sequence",
                    "owner": "GENESIS",
                    "needs": f"no wardrobe is locked at or before sequence "
                             f"{spec['sequence']} for this shot's characters"})

            parts = {
                "subject": ", ".join(t["token"] for t in tokens)
                           or spec.get("subject", location["name"]),
                "action": spec["action"],
                "environment": f"{location['name']}, {location['time_of_day']}; "
                               f"{location['description']}",
                "camera": spec["camera"],
                "lighting": spec.get("lighting", lock["style"]["grade"]),
                "style": lock["style"]["lens_language"],
            }
            if costume:
                parts["subject"] += f", wearing a {costume['colour']} "\
                                    f"{costume['garment']} ({costume['state']})"

            per_model, shot_cost, shot_known = [], 0.0, True
            for model in models:
                price = MODEL_COST_USD.get(model)
                if price is None:
                    shot_known = False
                    if not any(g["detail"].endswith(model) for g in gaps):
                        gaps.append({
                            "code": "cost-unknown",
                            "detail": f"no per-clip price is known for {model}",
                            "impact": "the scene total excludes every clip on "
                                      "this model, so it is a lower bound"})
                    run.gap(f"unpriced_model:{model}")
                else:
                    shot_cost += price * int(spec.get("clips", 1))
                per_model.append({
                    "model": model,
                    "rendered_prompt": self.render(parts, model),
                    "params": {"aspect_ratio": lock["style"]["aspect_ratios"][0],
                               "duration_s": int(spec.get("duration_s", 5))},
                    "est_cost_usd": None if price is None
                                    else round(price * int(spec.get("clips", 1)), 4),
                    "cost_known": price is not None,
                    "intent_preserved": True})

            if not shot_known:
                cost_complete = False
            total_cost += shot_cost
            shots.append({
                "shot_id": shot_id, "coverage": spec["coverage"],
                "intent": spec["intent"][:400], "prompt_parts": parts,
                "identity_tokens_used": tokens, "negative_prompt": NEGATIVE,
                "per_model": per_model,
                "continuity_note": spec.get("note")
                                   or "no continuity constraint beyond the lock",
                # The sum of what is priced. null only when nothing in this
                # shot is priced at all, because 0.0 would read as free.
                "est_cost_usd": round(shot_cost, 4)
                                if any(m["cost_known"] for m in per_model)
                                else None,
                "lock_version_used": lock_version})

        for target in escalations:
            gaps.append({
                "code": "missing-identity-token"
                        if "identity_token" in target["missing_field"]
                        else "reference-missing",
                "detail": f"{target['shot_id']}: {target['needs']}",
                "impact": "the field is left unstated in the prompt rather than "
                          "chosen here, and GENESIS owns supplying it"})
            run.gap(f"missing_from_lock:{target['shot_id']}:"
                    f"{target['missing_field']}")
        if escalations:
            run.escalate("lock_incomplete",
                         "GENESIS must supply the missing fields before these "
                         "shots can be written")
        run.finding(len(shots))

        deductions = [
            Deduction("an identity token was altered before it reached a prompt",
                      0.20, count=1 if violations else 0),
            Deduction("a shot needs a field the lock does not state", 0.10,
                      count=len(escalations), cap=0.30),
            Deduction("a model's per-clip cost is unknown", 0.05,
                      count=0 if cost_complete else 1),
        ]
        return Outcome(
            fields={
                "slug": lock["slug"], "scene_id": scene["scene_id"],
                "lock_version_used": lock_version,
                "generated_at_utc": today(),
                "target_models": models,
                "scene_totals": {
                    "shot_count": len(shots),
                    "clip_count": sum(int(s.get("clips", 1))
                                      for s in scene["shots"]),
                    "est_cost_usd": round(total_cost, 4),
                    "cost_complete": cost_complete},
                "shots": shots,
                "escalation_targets": escalations,
                "token_integrity_violations": violations,
                "injection_attempts": injections,
                "superseded": {"is_superseded": False},
                "gaps": gaps,
            },
            deductions=[d for d in deductions if d.count],
            verdict="findings" if escalations or violations else "clean",
        )

    @staticmethod
    def costume(wardrobe: dict, entities: list[str], sequence: int) -> dict | None:
        """The wardrobe in force at this sequence: the latest change at or
        before it. Nothing is invented for a sequence before the first entry."""
        for entity in entities:
            entries = [w for w in wardrobe.get(entity, [])
                       if w["sequence"] <= sequence]
            if entries:
                return entries[-1]
        return None

    @staticmethod
    def render(parts: dict, model: str) -> str:
        order = ["subject", "action", "environment", "camera", "lighting", "style"]
        return " | ".join(f"{k}: {parts[k]}" for k in order)


if __name__ == "__main__":
    raise SystemExit(Aperture(__file__).main())
