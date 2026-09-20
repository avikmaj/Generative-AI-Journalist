# core

Shared mechanics for every employee. An employee's own runner supplies its
inputs, its procedure and its schema; everything it must do identically to the
other fifteen lives here.

| Module | Owns |
|---|---|
| `budget.py` | Token, tool-call, USD and regeneration ceilings, and the liveness deadline. Checked **before** a call, so one that would breach is never made. |
| `retry.py` | Four attempts at 1s/2s/4s/8s with ±20% jitter, a 60s request ceiling, counted against budget. A decision — a breach, a refused write — is never retried. |
| `redact.py` | Masks known secret values in everything emitted, and names credential *shapes* without ever carrying the value. |
| `blast.py` | Read-only by default; `--apply` permits a write; the allowlist decides where. Traversal is resolved away before anything opens. |
| `artifact.py` | Schema validation, canonical serialization, sha256 digests, atomic writes. |
| `runrecord.py` | The sixteen-field record, prompt SHA, deterministic fingerprints. |
| `trace.py` | Redacted JSON Lines, appended as the run happens. |
| `run.py` | The context manager that ties them together and resolves the final status. |

## Status precedence

```
failed      a ceiling breached, a write refused, an artifact that would not
            validate, or an input that could not be established
escalated   the work is sound and a human decision is owed
partial     a gap, or any finding
ok          none of the above
```

`ok` requires an empty gap list. **An unknown is never a pass.**

## On validation

`jsonschema` performs validation when installed. When it is not, a structural
fallback runs and **every result reports which validator ran** — a degraded
check adds a gap, so the run cannot report `ok`. A run that silently weakened
its own checking is the false-clean outcome these specifications exist to
prevent.

## Dependency-free

Standard library only. `jsonschema` is an optional upgrade, not a requirement.

## Tests

```bash
python -m unittest discover -s employees/core/tests -t .
```
