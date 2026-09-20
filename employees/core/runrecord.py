"""The record every run persists, including the runs that failed.

Its shape is fixed across all sixteen employees so one reader can follow any of
them. A record is written for an ``ok`` run, a ``partial`` one, a ``failed``
one and an ``escalated`` one alike: a run that ended without a record is
indistinguishable from a run that never started, and silence must never read as
success.
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

Status = Literal["ok", "partial", "failed", "escalated"]
STATUSES: tuple[Status, ...] = ("ok", "partial", "failed", "escalated")


def utcnow() -> str:
    """An RFC 3339 timestamp in UTC, to the second."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today() -> str:
    """The UTC date, as every artifact path spells it."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def prompt_sha(spec_path: str | Path) -> str:
    """The sha256 of the specification a run executed.

    Recorded per run so a quality regression can be bisected to the document
    that caused it rather than guessed at.
    """
    return hashlib.sha256(Path(spec_path).read_bytes()).hexdigest()


def fingerprint(*parts: Any) -> str:
    """A deterministic sha256 over ordered parts, for finding identity.

    Sorting of any collection is the caller's business and must happen before
    the call, so that enumeration order cannot change a fingerprint.
    """
    joined = "\n".join("" if p is None else str(p) for p in parts)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


@dataclass
class RunRecord:
    """One run, as it will be persisted."""

    employee: str
    version: str
    model: str
    prompt_sha: str
    trigger_kind: str
    input_digest: str = ""
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at: str = field(default_factory=utcnow)
    ended_at: str = ""
    status: Status = "failed"
    confidence: float = 0.0
    budget: dict = field(default_factory=dict)
    artifacts: list[dict] = field(default_factory=list)
    escalations: list[dict] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    trace_path: str = ""

    def escalate(self, reason: str, needs: str) -> None:
        self.escalations.append({"reason": reason, "needs": needs})

    def gap(self, text: str) -> None:
        """Record something the run could not establish.

        A gap is how an unknown stays an unknown. Nothing here ever converts one
        into a default, a zero or a pass.
        """
        if text not in self.gaps:
            self.gaps.append(text)

    def artifact(self, path: str | Path, sha256: str) -> None:
        self.artifacts.append({"path": str(path), "sha256": sha256})

    def as_dict(self) -> dict:
        """The record, in the field order every specification states."""
        return {
            "run_id": self.run_id,
            "employee": self.employee,
            "version": self.version,
            "model": self.model,
            "prompt_sha": self.prompt_sha,
            "trigger": {"kind": self.trigger_kind, "at": self.started_at},
            "input_digest": self.input_digest,
            "started_at": self.started_at,
            "ended_at": self.ended_at or utcnow(),
            "status": self.status,
            "confidence": round(self.confidence, 2),
            "budget": self.budget,
            "artifacts": self.artifacts,
            "escalations": self.escalations,
            "gaps": self.gaps,
            "trace_path": self.trace_path,
        }
