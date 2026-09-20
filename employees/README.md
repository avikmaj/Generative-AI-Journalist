# AI employees

One directory per employee. `EMPLOYEE.md` is the versioned specification; the
runner reads it and records its SHA as `prompt_sha` in every run record.

**Git is authoritative.** A copy held anywhere else — a project, a doc, a chat —
is a mirror, and a mirror that drifts is worse than none.

```
core/                  shared loop: budgets, retries, validation,
                       run records, escalation, redaction
<handle>/
  EMPLOYEE.md          the specification, fourteen sections
  schema/output.json   extracted from section 5
  runner.py            thin wiring of core to this employee's I/O
  evals/golden.jsonl   real past inputs with known-good outputs
  evals/rubric.md
  tests/
```

Validate before committing:

```bash
python scripts/validate_employees.py                      # all of them
python scripts/validate_employees.py employees/keystone   # just one
```

Authored from `docs/12-ai-employee-roster.md`. Sixteen employees, four waves;
`keystone` first.
