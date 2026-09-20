"""Write destinations, checked before the write rather than after.

Read-only is the default; ``--apply`` is what permits a write at all. Every
specification also names the destinations it may touch, and anything else is
denied. Both checks happen before the filesystem or API call, because a write
refused after it happened is not a refusal.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from .errors import BlastRadiusViolation


class Allowlist:
    """The paths a run may write, and whether it may write at all."""

    def __init__(self, roots: Iterable[str | Path], *, apply: bool = False,
                 base: str | Path | None = None) -> None:
        self.apply = apply
        self._base = Path(base or os.getcwd()).resolve()
        self._roots = [self._resolve(r) for r in roots]

    def _resolve(self, path: str | Path) -> Path:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = self._base / candidate
        # resolve() collapses .. before the comparison, so a traversal cannot
        # climb out of an allowed root by spelling.
        return candidate.resolve()

    def permits(self, path: str | Path) -> bool:
        """Whether ``path`` lies inside an allowed root."""
        target = self._resolve(path)
        return any(target == root or root in target.parents for root in self._roots)

    def assert_writable(self, path: str | Path) -> Path:
        """Return the resolved path, or raise before anything is written."""
        target = self._resolve(path)
        if not self.apply:
            raise BlastRadiusViolation(
                f"read-only run: --apply is required to write {target}",
                reason="dry_run_write_attempt",
            )
        if not self.permits(target):
            raise BlastRadiusViolation(
                f"outside the allowlist: {target}",
                reason=f"blast_radius_violation:{target}",
            )
        return target

    def assert_readable(self, path: str | Path, roots: Iterable[str | Path]) -> Path:
        """Return ``path`` only if it resolves inside one of ``roots``.

        Separate from the write allowlist: an input arriving by path — a clip
        filename, a spec reference — may attempt traversal, and resolving it
        against its permitted roots is what stops the file being opened.
        """
        target = self._resolve(path)
        allowed = [self._resolve(r) for r in roots]
        if not any(target == root or root in target.parents for root in allowed):
            raise BlastRadiusViolation(
                f"input path resolves outside its permitted roots: {target}",
                reason="path_traversal_rejected",
            )
        return target

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        mode = "apply" if self.apply else "read-only"
        return f"Allowlist({mode}, {len(self._roots)} roots)"
