"""Mask secret values in everything the loop emits.

Built from the environment by name: the runner names the variables that hold
credentials, the values are read once, and every string written afterwards has
them replaced. Detection of a credential *inside an input* is a separate matter
and halts the run, because an input carrying a token is a finding about the
input, not something to quietly mask.
"""

from __future__ import annotations

import os
import re
from typing import Any, Iterable

MASK = "***"

#: Shapes that identify a credential wherever it appears. Kept narrow on
#: purpose: a pattern loose enough to match ordinary prose would mask the
#: evidence an operator needs at 2am.
CREDENTIAL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("anthropic_api_key", re.compile(r"sk-ant-[A-Za-z0-9_\-]{16,}")),
    ("github_pat_classic", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
    ("github_pat_fine_grained", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("aws_access_key_id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
)

#: Shorter than this and a value is too common to mask without eating
#: legitimate text — "1", "true", a bare path segment.
MIN_SECRET_LENGTH = 8


class Redactor:
    """Replaces known secret values with :data:`MASK`."""

    def __init__(self, env_var_names: Iterable[str] = (), *, environ: dict | None = None) -> None:
        source = os.environ if environ is None else environ
        self._secrets: list[str] = []
        for name in env_var_names:
            value = source.get(name)
            if value and len(value) >= MIN_SECRET_LENGTH:
                self._secrets.append(value)
        # Longest first, so a secret containing another is masked whole.
        self._secrets.sort(key=len, reverse=True)

    def __call__(self, value: Any) -> Any:
        return self.scrub(value)

    def scrub(self, value: Any) -> Any:
        """Return ``value`` with every known secret replaced, recursing into containers."""
        if isinstance(value, str):
            for secret in self._secrets:
                value = value.replace(secret, MASK)
            for _, pattern in CREDENTIAL_PATTERNS:
                value = pattern.sub(MASK, value)
            return value
        if isinstance(value, dict):
            return {self.scrub(k): self.scrub(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return type(value)(self.scrub(v) for v in value)
        return value


def find_credentials(text: str) -> list[str]:
    """Names of the credential shapes present in ``text``.

    Returns what kind was found, never the match itself, so a caller reporting
    the finding cannot accidentally write the value into its artifact.
    """
    return sorted({label for label, pattern in CREDENTIAL_PATTERNS if pattern.search(text)})
