"""KEYSTONE — repo and catalog integrity officer.

Implements the deterministic passes of its specification. Most of the procedure
needs no model at all: reading frontmatter, comparing a name to its directory,
intersecting trigger-word sets, counting roles and measuring bytes are all
computation. Only semantic mandate comparison and rubric adjudication need one,
and where the run reaches a step it cannot perform it records a gap and carries
on, which keeps the run off ``ok`` without inventing an answer.

    python -m employees.keystone.runner --repos <dir-holding-the-four-checkouts>
    python -m employees.keystone.runner --repos <dir> --apply

Read-only without ``--apply``: the artifact is validated and printed, nothing
is written, and no issue is filed.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from employees.core import (  # noqa: E402
    Allowlist, Budget, Run, canonical, digest, fingerprint, today,
)

HANDLE = "keystone"
VERSION = "1.0.1"
MODEL = "claude-opus-5"
SPEC = Path(__file__).with_name("EMPLOYEE.md")
SCHEMA = Path(__file__).parent / "schema" / "output.json"

#: The four repositories, in the fixed order section 3.1 states. The tuple's
#: order is load-bearing: the dedupe key is the ordered tuple of their SHAs.
REPOS = (
    "Generative-AI-Journalist",
    "DESIGN_VERIFICATION_SOLUTIONS",
    "AVIK-STUDIO-MTEAM-Agentic-AI-Film-Production-Playbook",
    "BUSINESS_SOLUTIONS",
)

#: Section 3.6. ``documented`` is what the source claims about itself; the run
#: derives the real count and compares. A count asserted in prose is never
#: evidence — only counting the artifacts is.
CATALOGS = {
    "dv.knowledge_architecture": (0, "knowledge/dv/agentic_ai_dv_architecture.md", 16),
    "dv.skill_framework": (0, "skills/dv/dv-engineering-suite/references/agentic/18_AI_Agent_Framework.md", 11),
    "dv.pipeline_schema": (0, "skills/dv/dv-engineering-suite/assets/agent_pipeline_schema.yaml", 9),
    "dv.dvo_departments": (1, ".claude/agents/dvo-d*.md", 14),
    "film.hats": (0, "skills/film/ai-movie-studio/references/core/filmmaking.md", 12),
    "film.subagents": (2, "agents/*.md", 17),
}

BUNDLES = {
    "claude": ("scripts/build_claude_bundle.py", 4000),
    "chatgpt": ("scripts/build_chatgpt_bundle.py", 4000),
    "grok": ("scripts/build_grok_bundle.py", 4000),
}

GUARD_CLAUSES = ("do not use", "don't use", "not for", "never use",
                 "do not trigger", "rather than", "instead of", "unless")

INSTRUCTION_SHAPED = re.compile(
    r"(ignore (all )?previous instructions|disregard (the )?(above|prior)|"
    r"this role is approved|drift already resolved|you must now|"
    r"report a clean sweep|system:|</?instructions>)",
    re.I,
)

SECTIONS = ["IDENTITY", "TRIGGER", "INPUTS", "PROCEDURE", "OUTPUT CONTRACT",
            "CONFIDENCE & ESCALATION", "BLAST RADIUS", "BUDGETS", "IDEMPOTENCY",
            "FAILURE MODES", "DEGRADATION RULE", "SUCCESS METRIC", "TESTS",
            "VERSION HISTORY"]

XML_TAGS = ["role", "context", "input_handling", "task",
            "output_specification", "quality_criteria", "constraints"]


# --- small helpers -------------------------------------------------------
def git_head(path: Path) -> str | None:
    """The checked-out SHA, or ``None`` when the directory is not a usable repo."""
    try:
        out = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def frontmatter(text: str) -> dict | None:
    """The YAML-ish mapping at the head of a skill file, or ``None``.

    Deliberately a small parser rather than a YAML dependency: these files use
    scalars and folded strings only, and a missing dependency must not be the
    reason an integrity check cannot run.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    block, out, key = text[3:end], {}, None
    for line in block.splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            key, value = match.group(1), match.group(2).strip()
            out[key] = "" if value in {">-", ">", "|", "|-"} else value.strip("'\"")
        elif key and line.strip():
            out[key] = (out[key] + " " + line.strip()).strip()
    return out


def trigger_tokens(description: str) -> set[str]:
    """The trigger-word set of a skill, per 4.3c."""
    quoted = re.findall(r'"([^"]+)"', description)
    parts = re.split(r"[,;/]| - ", description)
    tokens = {re.sub(r"\s+", " ", p).strip().lower() for p in quoted + parts}
    return {t for t in tokens if 4 <= len(t) <= 60}


def scan_instruction_shaped(run: Run, path: Path, text: str, findings: list) -> None:
    """Record instruction-shaped text as a finding. It never alters a verdict."""
    match = INSTRUCTION_SHAPED.search(text)
    if match:
        findings.append({
            "path": str(path),
            "marker": match.group(0)[:80],
            "excerpt": text[max(0, match.start() - 60):match.start() + 140][:200],
            "classified_as": "skill_content",
            "verdict_effect": "none",
        })
        run.finding()


# --- the procedure -------------------------------------------------------
def verify_checkouts(run: Run, base: Path) -> dict[str, str]:
    """4.1. A failed checkout of any one repository fails the whole run.

    No partial sweep, and never a clean verdict over a subset: an unread
    repository cannot support any statement about cross-repository integrity.
    """
    shas: dict[str, str] = {}
    for name in REPOS:
        for candidate in (base / name, base / name.lower()):
            if candidate.is_dir():
                sha = git_head(candidate)
                if sha:
                    shas[name] = sha
                    run.trace.event("repo.verified", repo=name, sha=sha[:12])
                    break
        else:
            run.gap(f"stale-checkout:{name}:unreadable")
            raise SystemExit(_abort(run, f"repository not readable: {name}"))
    return shas


def _abort(run: Run, detail: str) -> int:
    run.escalate("stale_checkout", detail)
    return 1


def validate_skills(run: Run, roots: dict[str, Path], findings: list) -> tuple[int, list]:
    """4.3. Frontmatter, name agreement, guard clause, and pairwise collision."""
    failed, skills = [], []
    for repo, root in roots.items():
        for path in sorted(root.rglob("SKILL.md")):
            # dist/ holds generated copies of skills already counted at
            # their source. Enumerating both doubles every skill and makes
            # each one collide with itself.
            if "dist" in path.parts or ".git" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            rel = f"{repo}/{path.relative_to(root)}"
            run.guard_input(rel, text[:4000])
            scan_instruction_shaped(run, Path(rel), text, findings)

            meta = frontmatter(text)
            if meta is None:
                failed.append({"path": rel, "check": "FRONTMATTER_MISSING",
                               "detail": "no parseable frontmatter block"})
                continue

            name = str(meta.get("name", ""))
            expected = path.parent.name.lower().replace("_", "-")
            if name.lower().replace("_", "-") != expected:
                failed.append({"path": rel, "check": "NAME_MATCHES_DIRECTORY",
                               "detail": f"name {name!r} != directory {path.parent.name!r}"})

            description = str(meta.get("description", ""))
            if not any(clause in description.lower() for clause in GUARD_CLAUSES):
                failed.append({"path": rel, "check": "NEGATIVE_GUARD_MISSING",
                               "detail": "no negative guard clause in description"})

            skills.append((rel, name, trigger_tokens(description)))

    # 4.3c over the union of all repositories, so an edit to one skill still
    # surfaces the pair it now collides with.
    for i, (path_a, name_a, tokens_a) in enumerate(skills):
        for path_b, name_b, tokens_b in skills[i + 1:]:
            shared = tokens_a & tokens_b
            if shared:
                failed.append({
                    "path": path_a, "check": "TRIGGER_COLLISION",
                    "detail": f"shares {sorted(shared)[:3]} with {name_b or path_b}",
                })
    return len(skills), failed


def validate_employee_specs(run: Run, roots: dict[str, Path]) -> tuple[int, list]:
    """4.4. The fourteen-section contract, checked independently."""
    failed, validated = [], 0
    for repo, root in roots.items():
        for path in sorted(root.glob("employees/*/EMPLOYEE.md")):
            rel = f"{repo}/{path.relative_to(root)}"
            text = path.read_text(encoding="utf-8", errors="replace")
            validated += 1

            offsets = []
            for number, name in enumerate(SECTIONS, start=1):
                pattern = rf"^#{{0,6}}\s*{number}[.):]?\s+{re.escape(name)}\s*$"
                found = re.search(pattern, text, re.M | re.I)
                if not found:
                    failed.append({"path": rel, "check": "SECTION_CONTRACT",
                                   "detail": f"{number} {name}"})
                offsets.append(found.start() if found else -1)

            present = [o for o in offsets if o >= 0]
            if present != sorted(present):
                failed.append({"path": rel, "check": "SECTION_CONTRACT", "detail": "out of order"})

            meta = re.search(r"^#{1,6}\s*Metadata\s*$", text, re.M | re.I)
            if meta and offsets[0] >= 0 and meta.start() > offsets[0]:
                failed.append({"path": rel, "check": "METADATA_POSITION",
                               "detail": "Metadata follows section 1"})

            for tag in XML_TAGS:
                if f"<{tag}>" not in text or f"</{tag}>" not in text:
                    failed.append({"path": rel, "check": "XML_TAGS_INCOMPLETE", "detail": tag})

            tests = text[offsets[12]:offsets[13]] if offsets[12] >= 0 and offsets[13] > 0 else ""
            if "adversarial" not in tests.lower():
                failed.append({"path": rel, "check": "ADVERSARIAL_ROW_MISSING", "detail": ""})

            history = text[offsets[13]:] if offsets[13] >= 0 else ""
            if not re.search(r"^\s*[-*]+\s*[`*_]*\d+\.\d+\.\d+", history, re.M):
                failed.append({"path": rel, "check": "VERSION_HISTORY_EMPTY", "detail": ""})

            schema_file = path.parent / "schema" / "output.json"
            if not schema_file.exists():
                failed.append({"path": rel, "check": "SCHEMA_FILE_MISSING", "detail": "absent"})
            else:
                try:
                    parsed = json.loads(schema_file.read_text(encoding="utf-8"))
                    if "2020-12" not in str(parsed.get("$schema", "")):
                        failed.append({"path": rel, "check": "SCHEMA_INVALID",
                                       "detail": "not draft 2020-12"})
                except json.JSONDecodeError as exc:
                    failed.append({"path": rel, "check": "SCHEMA_UNPARSEABLE", "detail": exc.msg})
    return validated, failed


def extract_roles(path: Path, key: str) -> set[str]:
    """Role keys from one catalog, normalized for comparison.

    Deterministic extraction only. A role that needs a model to recognise is
    not counted here, and 4.6's semantic step is gapped rather than guessed.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    if key == "dv.knowledge_architecture":
        found = re.findall(r"^\|\s*\*{0,2}([A-Z][A-Z_]+_AGENT)\*{0,2}\s*\|", text, re.M)
        found += re.findall(r"\b(DV_ORCHESTRATOR)\b", text)
    elif key == "dv.skill_framework":
        found = re.findall(r"^###\s+Agent\s+\d+\s*[—-]\s*(.+?)\s*$", text, re.M)
        found += re.findall(r"^\|\s*(\d+)\s*—\s*([^|]+?)\s*\|", text, re.M) and []
        found += [m.strip() for m in re.findall(r"^\|\s*\d+\s*—\s*([^|]+?)\s*\|", text, re.M)]
    elif key == "dv.pipeline_schema":
        found = re.findall(r"^\s*-\s*id:\s*([A-Za-z0-9_]+)\s*$", text, re.M)
    elif key == "film.hats":
        found = re.findall(r"^\|\s*([A-Z][A-Za-z ]+?)\s*\|\s*[A-Z]", text, re.M)
        found = [f for f in found if f.lower() not in {"role", "responsibility"}]
    else:
        found = []
    return {re.sub(r"[^a-z0-9]+", "-", f.lower()).strip("-") for f in found if f}


def detect_drift(run: Run, roots: dict[str, Path], base: Path) -> list:
    """4.6. Count comparison and missing-role detection, both deterministic.

    Mandate comparison is semantic and needs a model; it is gapped explicitly
    rather than approximated, because a conflict missed is a false clean.
    """
    drift, populations = [], {}
    for key, (repo_index, pattern, documented) in CATALOGS.items():
        root = roots[REPOS[repo_index]]
        paths = sorted(root.glob(pattern)) if "*" in pattern else (
            [root / pattern] if (root / pattern).exists() else [])
        if not paths:
            run.gap(f"catalog-missing:{key}")
            drift.append({"catalog": key.split(".")[0], "role": f"__missing__:{key}",
                          "present_in": [], "absent_from": [key],
                          "mandate_conflict": False,
                          "derived": None, "documented": documented})
            run.finding()
            continue

        if "*" in pattern:
            roles = {p.stem.lower() for p in paths}
        else:
            roles = extract_roles(paths[0], key)
        populations[key] = roles

        if roles and len(roles) != documented:
            drift.append({"catalog": key.split(".")[0],
                          "role": f"__count__:{key}",
                          "present_in": [key], "absent_from": [],
                          "mandate_conflict": False,
                          "derived": len(roles), "documented": documented})
            run.finding()
            run.trace.event("drift.count", catalog=key, derived=len(roles),
                            documented=documented)
        elif not roles:
            run.gap(f"catalog-unparsed:{key}")
            run.finding()

    for family in ("dv", "film"):
        members = {k: v for k, v in populations.items() if k.startswith(family) and v}
        universe = set().union(*members.values()) if members else set()
        for role in sorted(universe):
            present = sorted(k for k, v in members.items() if role in v)
            absent = sorted(k for k in members if role not in members[k])
            if absent:
                drift.append({"catalog": family, "role": role, "present_in": present,
                              "absent_from": absent, "mandate_conflict": False,
                              "derived": None, "documented": None})
                run.finding()

    run.gap("mandate-comparison-not-run:requires-model")
    return drift


def measure_bundles(run: Run, hub: Path) -> list:
    """4.7. A builder exiting 0 is never evidence that its output complies."""
    rows = []
    for name, (script, limit) in BUNDLES.items():
        path = hub / script
        if not path.exists():
            rows.append({"name": name, "built": False, "size_bytes": None,
                         "limit_bytes": limit, "within_limit": False,
                         "error": "builder_absent"})
            run.gap(f"bundle-builder-absent:{name}")
            run.finding()
            continue
        try:
            proc = subprocess.run([sys.executable, str(path)], cwd=hub,
                                  capture_output=True, text=True, timeout=120)
        except subprocess.SubprocessError as exc:
            rows.append({"name": name, "built": False, "size_bytes": None,
                         "limit_bytes": limit, "within_limit": False,
                         "error": f"builder_error:{type(exc).__name__}"})
            run.gap(f"bundle-build-failed:{name}")
            run.finding()
            continue

        if proc.returncode != 0:
            rows.append({"name": name, "built": False, "size_bytes": None,
                         "limit_bytes": limit, "within_limit": False,
                         "error": f"builder_exit_{proc.returncode}"})
            run.gap(f"bundle-build-failed:{name}:exit_{proc.returncode}")
            run.finding()
            continue

        # The ceiling applies to the instruction file the platform loads,
        # not to the corpus shipped beside it.
        out = hub / "dist" / name
        instruction = next(
            (out / n for n in ("project-instructions.md", "CLAUDE.md",
                               "system-prompt.md", "instructions.md")
             if (out / n).exists()), None)
        size = instruction.stat().st_size if instruction else None
        rows.append({"name": name, "built": True, "size_bytes": size,
                     "limit_bytes": limit,
                     "within_limit": bool(size is not None and size <= limit),
                     "error": None})
        if size is None:
            run.gap(f"bundle-unmeasured:{name}")
            run.finding()
        elif size > limit:
            run.finding()
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repos", required=True, type=Path,
                        help="directory holding the four repository checkouts")
    parser.add_argument("--apply", action="store_true",
                        help="permit writes; without it the run is read-only")
    parser.add_argument("--reports-root", type=Path, default=None)
    args = parser.parse_args(argv)

    base = args.repos.resolve()
    hub = base / REPOS[0]
    reports_root = (args.reports_root or hub).resolve()
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    budget = Budget(tokens_max=150_000, tool_calls_max=60, usd_cap=1.50,
                    liveness_seconds=1200)
    allowlist = Allowlist([reports_root / "reports" / HANDLE], apply=args.apply,
                          base=reports_root)

    with Run(employee=HANDLE, version=VERSION, model=MODEL, spec_path=SPEC,
             trigger_kind="manual", budget=budget, allowlist=allowlist,
             secret_env_names=["ANTHROPIC_API_KEY", "GITHUB_TOKEN"],
             runs_root=reports_root / "runs") as run:

        shas = verify_checkouts(run, base)
        run.record.input_digest = digest([shas[name] for name in REPOS])
        roots = {name: base / name for name in REPOS}
        for name in REPOS:
            if not (base / name).is_dir():
                roots[name] = base / name.lower()

        findings: list = []
        skills_validated, skills_failed = validate_skills(run, roots, findings)
        run.finding(len(skills_failed))
        employees_validated, employees_failed = validate_employee_specs(run, roots)
        run.finding(len(employees_failed))
        drift = detect_drift(run, roots, base)
        bundles = measure_bundles(run, hub)

        run.gap("golden-set-not-run:requires-model")

        artifact = {
            "employee": HANDLE,
            "version": VERSION,
            "run_id": run.record.run_id,
            "generated_at": run.record.started_at,
            "artifact_path": f"reports/{HANDLE}/{today()}.json",
            "repo_shas": shas,
            "verdict": "findings" if (skills_failed or employees_failed or drift) else "clean",
            "skills_validated": skills_validated,
            "skills_failed": skills_failed,
            "employees_validated": employees_validated,
            "employees_failed": employees_failed,
            # Not run without a model. case_count 0 and no bars is how the
            # schema spells "nothing was measured"; the gap says why.
            # Not run without a model. Every bar reads false rather than
            # absent: a bar that was never measured must never be mistaken for
            # one that passed. The gap records why none of them ran.
            "golden_set": {
                "score": None, "delta": None, "case_count": 0, "regressions": [],
                "bars": {
                    "routing_guard_100pct": False,
                    "overall_assertion_pass_pct": 0.0,
                    "no_zero_on_critical_dims": False,
                    "rubric_mean": None,
                    "no_two_to_sub_two": False,
                },
            },
            "bundles": [
                {k: b[k] for k in ("name", "built", "size_bytes", "limit_bytes",
                                   "within_limit")}
                for b in bundles
            ],
            "drift": [
                {k: d[k] for k in ("catalog", "role", "present_in", "absent_from",
                                   "mandate_conflict")}
                for d in drift
            ],
            "instruction_shaped_text": findings,
            "gaps": run.record.gaps,
            "escalations": run.record.escalations,
            "confidence": 0.0,
        }

        # Deductions per section 6.2, for the dimensions this run could measure.
        confidence = 1.00
        confidence -= 0.15 * sum(1 for g in run.record.gaps if g.startswith("catalog-"))
        confidence -= 0.08 * sum(1 for b in bundles if not b["built"])
        confidence -= 0.20  # golden set could not run
        for d in drift:
            run.trace.event("drift.finding", fingerprint=fingerprint(
                d["catalog"], d["role"], ",".join(sorted(d["present_in"])),
                ",".join(sorted(d["absent_from"])),
                str(d["mandate_conflict"]).lower())[:12], **{
                    k: d[k] for k in ("catalog", "role")})
        artifact["confidence"] = round(max(0.0, min(1.0, confidence)), 2)
        run.record.confidence = artifact["confidence"]

        if artifact["confidence"] <= 0.90:
            run.escalate("confidence_below_threshold",
                         "model-backed steps could not run; supply an API key or "
                         "accept a deterministic-only sweep")

        artifact["gaps"] = list(run.record.gaps)
        artifact["escalations"] = list(run.record.escalations)

        written = run.emit(
            reports_root / "reports" / HANDLE / f"{today()}.json", artifact, schema
        )
        if written is None:
            print(canonical(artifact), end="")

    print(f"\nstatus={run.record.status} confidence={run.record.confidence} "
          f"verdict={artifact['verdict']} gaps={len(run.record.gaps)} "
          f"drift={len(drift)} skills={skills_validated} "
          f"skills_failed={len(skills_failed)} specs_failed={len(employees_failed)}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
