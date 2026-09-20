"""A line-delimited record of what a run did, written as it happens.

Appended rather than buffered, so a run killed by its liveness deadline still
leaves the trace that explains where it got to. Every value passes through the
redactor on the way out.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .redact import Redactor
from .runrecord import utcnow


class Trace:
    """Appends redacted events to a JSON Lines file."""

    def __init__(self, path: str | Path, redactor: Redactor | None = None) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._redact = redactor or Redactor()

    def event(self, kind: str, **fields: Any) -> None:
        record = {"at": utcnow(), "kind": kind, **fields}
        line = json.dumps(self._redact.scrub(record), sort_keys=True, ensure_ascii=False)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
            fh.flush()

    def __repr__(self) -> str:  # pragma: no cover - diagnostics only
        return f"Trace({self.path})"
