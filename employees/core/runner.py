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

            artifact = {
                "employee": self.handle,
                "version": self.version,
                "run_id": run.record.run_id,
                "generated_at": run.record.started_at,
                "artifact_path": self.artifact_path(args),
                "verdict": outcome.verdict,
                "confidence": confidence,
                **outcome.fields,
                "gaps": list(run.record.gaps),
                "escalations": list(run.record.escalations),
            }

            # The comparison is inclusive: a run landing exactly on the
            # threshold escalates, since a capped deduction can sum to exactly
            # the distance between 1.00 and it.
            if confidence <= self.confidence_threshold:
                run.escalate("confidence_below_threshold",
                             "; ".join(d.reason for d in outcome.deductions if d.count)
                             or "confidence below threshold")
                artifact["escalations"] = list(run.record.escalations)

            if run.emit(reports_root / self.artifact_path(args), artifact, schema) is None:
                print(canonical(artifact), end="")

        import sys
        print(f"status={run.record.status} confidence={run.record.confidence} "
              f"verdict={artifact.get('verdict')} gaps={len(run.record.gaps)}",
              file=sys.stderr)
        return 0
