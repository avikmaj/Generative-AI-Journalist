"""Shared mechanics for every AI employee.

An employee's own runner supplies its inputs, its procedure and its schema.
Everything it must do identically to the other fifteen lives here: budgets that
stop a call before it breaches, bounded retries, redaction, an enforced write
allowlist, schema validation before any write, atomic writes, and a run record
persisted for every run whatever its outcome.

Nothing in this package calls a model or knows what an employee does. It is the
frame the work runs inside.
"""

from .artifact import ValidationResult, canonical, digest, validate, write_atomic
from .blast import Allowlist
from .budget import Budget
from .errors import (
    ArtifactInvalid,
    BlastRadiusViolation,
    BudgetExceeded,
    CoreError,
    Escalation,
    LivenessExceeded,
    RetriesExhausted,
    SensitiveDataInInput,
)
from .redact import Redactor, find_credentials
from .retry import call_with_retry
from .run import Run
from .runrecord import RunRecord, Status, fingerprint, prompt_sha, today, utcnow
from .trace import Trace

__all__ = [
    "Allowlist", "ArtifactInvalid", "BlastRadiusViolation", "Budget",
    "BudgetExceeded", "CoreError", "Escalation", "LivenessExceeded",
    "Redactor", "RetriesExhausted", "Run", "RunRecord", "SensitiveDataInInput",
    "Status", "Trace", "ValidationResult", "call_with_retry", "canonical",
    "digest", "find_credentials", "fingerprint", "prompt_sha", "today",
    "utcnow", "validate", "write_atomic",
]
