"""The scaffolding every employee runner shares.

KEYSTONE's runner showed which parts are the same for all sixteen and which are
the employee's own. The same parts are here: argument parsing, loading the
specification and its schema, constructing the budget and the allowlist,
assembling the artifact's common fields, computing confidence from declared
deductions, and deciding the status. What remains in an employee's runner is
its inputs and its procedure, which is the only part that differs.

Subclass :class:`EmployeeRunner`, declare the handle and ceilings, implement
``procedure``, and return the employee-specific fields. Everything else is
handled and, more importantly, handled the same way each time.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .artifact import canonical
from .blast import Allowlist
from .budget import Budget
from .run import Run
from .runrecord import today

# The fields the base offers on every artifact. Anything outside this set came
# from an employee's own procedure and is never filtered away.
COMMON_FIELDS = frozenset({
    "employee", "version", "run_id", "model", "prompt_sha", "input_digest",
    "generated_at", "artifact_date", "artifact_path", "verdict", "confidence",
    "status", "gaps", "escalations",
})


@dataclass
class Deduction:
    """One reason confidence is below 1.00, and by how much.

    Declared rather than computed inline so that a specification's confidence
    table and its implementation can be read side by side, and so the worst
    case can be checked: see :meth:`EmployeeRunner.worst_case_confidence`.
    """

    reason: str
    amount: float
    cap: float | None = None
    count: int = 0

    @property
    def applied(self) -> float:
        total = self.amount * self.count
        return min(total, self.cap) if self.cap is not None else total


@dataclass
class Outcome:
    """What an employee's procedure returns."""

    fields: dict[str, Any] = field(default_factory=dict)
    deductions: list[Deduction] = field(default_factory=list)
    verdict: str = "clean"


class EmployeeRunner:
    """Base for an employee's runner."""

    handle: str = ""
    version: str = "1.0.0"
    model: str = "claude-opus-5"
    tokens_max: int = 150_000
    tool_calls_max: int = 60
    usd_cap: float = 1.50
    liveness_seconds: int = 1200
    confidence_threshold: float = 0.90
    secret_env_names: tuple[str, ...] = ("ANTHROPIC_API_KEY", "GITHUB_TOKEN")

    def __init__(self, module_file: str | Path) -> None:
        self.directory = Path(module_file).resolve().parent
        self.spec = self.directory / "EMPLOYEE.md"
        self.schema_path = self.directory / "schema" / "output.json"

    # -- an employee implements this ---------------------------------------
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Declare the inputs this employee takes."""

    def procedure(self, run: Run, args: argparse.Namespace) -> Outcome:
        """Do the work. Return the artifact's employee-specific fields."""
        raise NotImplementedError

    def artifact_path(self, args: argparse.Namespace) -> str:
        """Where the artifact belongs, relative to the reports root."""
        return f"reports/{self.handle}/{today()}.json"

    # -- everything below is the same for all sixteen ----------------------
    @staticmethod
    def conform(artifact: dict[str, Any], schema: dict) -> dict[str, Any]:
        """Drop common fields this employee's schema does not declare.

        The sixteen specifications agree on what a run *means* but not on what
        its artifact *carries*: BLOODHOUND reports a regression and a commit
        where KEYSTONE reports neither, and every schema closes itself with
        ``additionalProperties: false``. Rather than teach the base which
        fields each employee wants, offer the full common set and let the
        schema — which section 5 of the specification is the source of — decide
        what survives. The specification stays authoritative, and a field
        renamed there stops appearing here instead of failing validation.

        Only the common fields are filtered. A field an employee's procedure
        returned is left alone: the employee asked for it, so a schema that
        rejects it is a real disagreement and should fail loudly.
        """
        if schema.get("additionalProperties") is not False:
            return artifact
        declared = set(schema.get("properties", {}))
        if not declared:
            return artifact
        return {k: v for k, v in artifact.items()
                if k in declared or k not in COMMON_FIELDS}

    def common_fields(self, run: Run, args: argparse.Namespace,
                      confidence: float, verdict: str) -> dict[str, Any]:
        """What every employee could report about a run, before conforming."""
        return {
            "employee": self.handle,
            "version": self.version,
            "run_id": run.record.run_id,
            "model": self.model,
            "prompt_sha": run.record.prompt_sha,
            "input_digest": run.record.input_digest,
            "generated_at": run.record.started_at,
            "artifact_date": today(),
            "artifact_path": self.artifact_path(args),
            "verdict": verdict,
            "confidence": confidence,
        }

    def worst_case_confidence(self, deductions: list[Deduction]) -> float:
        """Confidence when every declared deduction applies at its cap.

        The standard requires showing this: a deduction capped at exactly the
        distance between 1.00 and the threshold lands the saturated case on the
        boundary, which an exclusive comparison would let through.
        """
        worst = 1.0
        for d in deductions:
            worst -= d.cap if d.cap is not None else d.amount
        return round(max(0.0, worst), 2)

    def build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description=f"{self.handle} — see EMPLOYEE.md")
        parser.add_argument("--apply", action="store_true",
                            help="permit writes; without it the run is read-only")
        parser.add_argument("--reports-root", type=Path, default=Path.cwd(),
                            help="root the artifact path is relative to")
        self.add_arguments(parser)
        return parser

    def write_destinations(self, reports_root: Path) -> list[Path]:
        """The only paths this employee may write."""
        return [reports_root / "reports" / self.handle]

    def main(self, argv: list[str] | None = None) -> int:
        args = self.build_parser().parse_args(argv)
        reports_root = Path(args.reports_root).resolve()
        schema = json.loads(self.schema_path.read_text(encoding="utf-8"))

        budget = Budget(tokens_max=self.tokens_max, tool_calls_max=self.tool_calls_max,
                        usd_cap=self.usd_cap, liveness_seconds=self.liveness_seconds)
        allowlist = Allowlist(self.write_destinations(reports_root),
                              apply=args.apply, base=reports_root)

        artifact: dict[str, Any] = {}
        with Run(employee=self.handle, version=self.version, model=self.model,
                 spec_path=self.spec, trigger_kind="manual", budget=budget,
                 allowlist=allowlist, secret_env_names=self.secret_env_names,
                 runs_root=reports_root / "runs") as run:

            outcome = self.procedure(run, args)

            confidence = 1.0 - sum(d.applied for d in outcome.deductions)
            confidence = round(max(0.0, min(1.0, confidence)), 2)
            run.record.confidence = confidence
            for d in outcome.deductions:
                if d.count:
                    run.trace.event("confidence.deduction", reason=d.reason,
                                    applied=round(d.applied, 4), count=d.count)

            # The comparison is inclusive: a run landing exactly on the
            # threshold escalates, since a capped deduction can sum to exactly
            # the distance between 1.00 and it.
            if confidence <= self.confidence_threshold:
                run.escalate("confidence_below_threshold",
                             "; ".join(d.reason for d in outcome.deductions if d.count)
                             or "confidence below threshold")

            artifact = {
                **self.common_fields(run, args, confidence, outcome.verdict),
                **outcome.fields,
                "status": run.resolve_status(),
                "gaps": list(run.record.gaps),
                "escalations": list(run.record.escalations),
            }
            artifact = self.conform(artifact, schema)

            if run.emit(reports_root / self.artifact_path(args), artifact, schema) is None:
                print(canonical(artifact), end="")

        import sys
        print(f"status={run.record.status} confidence={run.record.confidence} "
              f"verdict={outcome.verdict} gaps={len(run.record.gaps)}",
              file=sys.stderr)
        return 0
