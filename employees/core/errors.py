"""Failures that the shared loop raises, and the run status each implies.

Every one carries the status the run must end in, so a runner never has to
decide that for itself. A specification's degradation rule distinguishes
``failed`` from ``escalated``: a failed run could not establish its result, an
escalated run established it and owes a human a decision.
"""

from __future__ import annotations


class CoreError(Exception):
    """Base for every failure the shared loop raises."""

    status = "failed"
    reason = "core_error"

    def __init__(self, message: str, *, reason: str | None = None) -> None:
        super().__init__(message)
        if reason:
            self.reason = reason


class BudgetExceeded(CoreError):
    """A ceiling would be crossed. Raised before the call, never after."""

    status = "failed"
    reason = "budget_breach"


class LivenessExceeded(BudgetExceeded):
    """The run outlived its deadline."""

    reason = "liveness_deadline"


class RetriesExhausted(CoreError):
    """A call kept failing after its bounded attempts."""

    status = "failed"
    reason = "api_retries_exhausted"


class BlastRadiusViolation(CoreError):
    """A write was attempted outside the allowlist."""

    status = "failed"
    reason = "blast_radius_violation"


class ArtifactInvalid(CoreError):
    """The artifact did not satisfy its schema, and was not written."""

    status = "failed"
    reason = "artifact_schema_invalid"


class Escalation(CoreError):
    """The work is sound and a human decision is owed.

    This is a successful controlled outcome, not an implementation failure,
    which is why it carries ``escalated`` rather than ``failed``.
    """

    status = "escalated"
    reason = "escalated"

    def __init__(self, message: str, *, needs: str = "", reason: str | None = None) -> None:
        super().__init__(message, reason=reason)
        self.needs = needs


class SensitiveDataInInput(Escalation):
    """A credential-shaped value appeared in an input.

    The run halts and records where it was found. It never records what it was.
    """

    reason = "sensitive_data_in_input"
