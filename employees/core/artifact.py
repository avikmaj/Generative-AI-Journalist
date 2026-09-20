"""Validate an artifact against its schema, then write it atomically.

An invalid artifact is never persisted to its final path. Validation happens
first, the bytes land in a temporary file beside the destination, and only a
rename publishes them — so a reader never observes a half-written report, and a
crash mid-write leaves the previous artifact intact.

``jsonschema`` performs the validation when it is installed. When it is not,
a structural fallback runs instead and says so: every result reports which
validator ran, because a run that silently degraded its own checking is exactly
the false-clean outcome these specifications exist to prevent.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:  # pragma: no cover - exercised by whichever environment is present
    import jsonschema  # type: ignore

    _HAVE_JSONSCHEMA = True
except ImportError:  # pragma: no cover
    jsonschema = None  # type: ignore
    _HAVE_JSONSCHEMA = False


@dataclass(frozen=True)
class ValidationResult:
    """Whether an artifact satisfied its schema, and how thoroughly it was asked."""

    valid: bool
    errors: tuple[str, ...]
    validator: str  # "jsonschema" or "structural-fallback"

    @property
    def complete(self) -> bool:
        """Whether full Draft 2020-12 validation ran."""
        return self.validator == "jsonschema"


def _structural_errors(instance: Any, schema: dict, path: str = "$") -> list[str]:
    """A deliberately partial check for environments without ``jsonschema``.

    Covers the constraints these schemas actually rely on — required keys,
    types, ``additionalProperties: false``, ``const``, ``enum`` and array item
    shape. It cannot replace a real validator, which is why the result says so.
    """
    errors: list[str] = []
    expected = schema.get("type")
    types = {
        "object": dict, "array": list, "string": str,
        "number": (int, float), "integer": int, "boolean": bool,
    }
    if expected in types and not isinstance(instance, types[expected]):
        if not (expected == "number" and isinstance(instance, bool) is False
                and isinstance(instance, (int, float))):
            return [f"{path}: expected {expected}, got {type(instance).__name__}"]
    if expected == "integer" and isinstance(instance, bool):
        return [f"{path}: expected integer, got boolean"]

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: {instance!r} is not one of {schema['enum']!r}")

    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing required property {key!r}")
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in properties:
                    errors.append(f"{path}: additional property {key!r} is not allowed")
        for key, sub in properties.items():
            if key in instance and isinstance(sub, dict):
                errors.extend(_structural_errors(instance[key], sub, f"{path}.{key}"))

    if isinstance(instance, list):
        items = schema.get("items")
        if isinstance(items, dict):
            for index, item in enumerate(instance):
                errors.extend(_structural_errors(item, items, f"{path}[{index}]"))

    return errors


def validate(instance: Any, schema: dict) -> ValidationResult:
    """Check ``instance`` against ``schema`` with the best validator available."""
    if _HAVE_JSONSCHEMA:
        validator = jsonschema.Draft202012Validator(schema)  # type: ignore[union-attr]
        errors = tuple(
            f"{'.'.join(str(p) for p in e.absolute_path) or '$'}: {e.message}"
            for e in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))
        )
        return ValidationResult(not errors, errors, "jsonschema")

    errors = tuple(_structural_errors(instance, schema))
    return ValidationResult(not errors, errors, "structural-fallback")


def canonical(instance: Any) -> str:
    """Canonical JSON: sorted keys, no insignificant whitespace, trailing newline.

    Two runs on identical input must produce identical bytes, so serialization
    cannot be left to dictionary ordering.
    """
    return json.dumps(instance, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n"


def digest(instance: Any) -> str:
    """``sha256:`` digest over the canonical form."""
    return "sha256:" + hashlib.sha256(canonical(instance).encode("utf-8")).hexdigest()


def write_atomic(path: str | Path, text: str) -> str:
    """Write ``text`` to ``path`` via a temporary file and a rename.

    Returns the sha256 of the bytes written, for the run record's
    ``artifacts[].sha256``.
    """
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    handle, tmp = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.", suffix=".tmp")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, target)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
