"""The shared loop: one context manager that owns a run from start to record.

An employee's own runner stays thin because everything an employee must do
identically lives here — the budgets, the allowlist, the redaction, the
validation before the write, the run record afterwards, and the status the run
ends in.

The status rules are the ones every specification's degradation table states,
in the same precedence:

    failed      a ceiling breached, a write refused, an artifact that would not
                validate, or an input that could not be established
    escalated   the work is sound and a human decision is owed
    partial     a gap, or any finding
    ok          none of the above

``ok`` therefore requires an empty gap list. An unknown is never a pass.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from . import artifact as artifact_mod
from .blast import Allowlist
from .budget import Budget
from .errors import ArtifactInvalid, CoreError, SensitiveDataInInput
from .redact import Redactor, find_credentials
from .runrecord import RunRecord, Status, utcnow
from .trace import Trace


class Run:
    """One execution of one employee."""

    def __init__(
        self,
        *,
        employee: str,
        version: str,
        model: str,
        spec_path: str | Path,
        trigger_kind: str,
        budget: Budget,
        allowlist: Allowlist,
        secret_env_names: Iterable[str] = (),
        runs_root: str | Path = "runs",
    ) -> None:
        from .runrecord import prompt_sha, today

        self.budget = budget
        self.allowlist = allowlist
        self.redactor = Redactor(secret_env_names)
        self.record = RunRecord(
            employee=employee,
            version=version,
            model=model,
            prompt_sha=prompt_sha(spec_path),
            trigger_kind=trigger_kind,
        )
        trace_path = Path(runs_root) / today() / employee / f"{self.record.run_id}.jsonl"
        self.record.trace_path = str(trace_path)
        self.trace = Trace(trace_path, self.redactor)
        self._findings = 0

    # -- lifecycle --------------------------------------------------------
    def __enter__(self) -> "Run":
        self.trace.event(
            "run.start",
            employee=self.record.employee,
            version=self.record.version,
            prompt_sha=self.record.prompt_sha,
            apply=self.allowlist.apply,
        )
        if not self.budget.priced:
            self.record.gap("usd-ceiling-unenforceable:no-price-table")
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if isinstance(exc, CoreError):
            self.record.status = exc.status
            self.record.escalate(exc.reason, getattr(exc, "needs", "") or str(exc))
            self.record.gap(f"{exc.reason}")
            self.trace.event("run.error", reason=exc.reason, detail=str(exc))
        elif exc is not None:
            self.record.status = "failed"
            self.record.escalate("unhandled_exception", f"{type(exc).__name__}: {exc}")
            self.record.gap("unhandled_exception")
            self.trace.event("run.error", reason="unhandled_exception", detail=str(exc))
        else:
            self.record.status = self.resolve_status()

        self.record.ended_at = utcnow()
        self.record.budget = self.budget.as_record()
        self.trace.event(
            "run.end",
            status=self.record.status,
            gaps=len(self.record.gaps),
            **self.budget.as_record(),
        )
        self.persist_record()
        return isinstance(exc, CoreError)  # handled; a caller sees the record

    def resolve_status(self) -> Status:
        """The status implied by what the run accumulated."""
        if self.record.escalations:
            return "escalated"
        if self.record.gaps or self._findings:
            return "partial"
        return "ok"

    # -- the things every employee does the same way ----------------------
    def finding(self, count: int = 1) -> None:
        """Note that the run found something. Findings keep a run off ``ok``."""
        self._findings += count

    def escalate(self, reason: str, needs: str) -> None:
        self.record.escalate(reason, needs)
        self.trace.event("escalation", reason=reason, needs=needs)

    def gap(self, text: str) -> None:
        self.record.gap(text)
        self.trace.event("gap", detail=text)

    def guard_input(self, identity: str, text: str) -> None:
        """Halt if an input carries a credential.

        The finding names where it was found and what kind it was. It never
        carries the value, which is why :func:`~employees.core.redact.find_credentials`
        returns labels rather than matches.
        """
        kinds = find_credentials(text)
        if kinds:
            self.trace.event("sensitive_data", source=identity, kinds=kinds)
            raise SensitiveDataInInput(
                f"credential-shaped value in input {identity}: {', '.join(kinds)}",
                needs="remove the credential from the input, then re-run",
            )

    def emit(self, path: str | Path, instance: Any, schema: dict) -> str | None:
        """Validate, then write atomically. Returns the sha256, or ``None`` on a dry run.

        Validation precedes the write, so an invalid artifact never reaches its
        final path. On a read-only run the artifact is still validated — the
        check is the point of a dry run — and the write is skipped.
        """
        result = artifact_mod.validate(instance, schema)
        self.trace.event(
            "artifact.validate",
            valid=result.valid,
            validator=result.validator,
            errors=list(result.errors[:5]),
        )
        if not result.complete:
            self.gap(f"schema-validation-degraded:{result.validator}")
        if not result.valid:
            detail = "; ".join(result.errors[:5]) or "no detail"
            raise ArtifactInvalid(
                f"artifact failed {result.validator} validation: {detail}"
            )

        if not self.allowlist.apply:
            self.trace.event("artifact.dry_run", path=str(path))
            return None

        target = self.allowlist.assert_writable(path)
        sha = artifact_mod.write_atomic(target, artifact_mod.canonical(instance))
        self.record.artifact(target, sha)
        self.trace.event("artifact.write", path=str(target), sha256=sha)
        return sha

    def persist_record(self) -> None:
        """Write the run record beside its trace.

        Written outside the write allowlist on purpose: a record is how a failed
        run reports itself, including a run that failed *because* a write was
        refused, and a record that a blast-radius violation could suppress would
        hide the very violation it must report.
        """
        path = Path(self.record.trace_path).with_suffix(".record.json")
        payload = self.redactor.scrub(self.record.as_dict())
        artifact_mod.write_atomic(path, artifact_mod.canonical(payload))
