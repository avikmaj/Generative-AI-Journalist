# AI employees

Sixteen unattended workers. Each starts from an exact trigger, reads defined
inputs, runs a bounded procedure, validates its own output against a schema
before writing it, writes only to allowlisted destinations, persists a run
record, and escalates uncertainty rather than guessing.

`EMPLOYEE.md` is the versioned specification; the runner reads it and records its
SHA as `prompt_sha` in every run record.

**Git is authoritative.** A copy held anywhere else — a project, a doc, a chat —
is a mirror, and a mirror that drifts is worse than none.

---

## Run one

Every employee is the same command shape:

```bash
python employees/<handle>/runner.py <inputs>            # read-only, prints the report
python employees/<handle>/runner.py <inputs> --apply    # writes the report
```

No API key, no network, Python 3.12. Every employee but KEYSTONE ships a fixture,
so all of these run as-is from the repository root:

```bash
python employees/bloodhound/runner.py --uvmstudio-report employees/bloodhound/fixtures/report.json
python scripts/run_all_employees.py     # all sixteen at once, read-only
```

---

## Who does what

### Platform

| Employee | What it does | Run it |
|---|---|---|
| **KEYSTONE** | Sweeps all four repositories for drift between skills, catalogs and specifications. Refuses a partial sweep — an unread repository cannot support a claim about cross-repository integrity. | `--repos <dir holding all four repos>` |

### DV — regression, coverage, traceability, gates

| Employee | What it does | Run it |
|---|---|---|
| **BLOODHOUND** | Turns a night of regression logs into a few clustered, owner-routed failures. Clusters on failure **signature**, never on test name, so one root cause is one cluster. Reads the UVM report vocabulary, so the verdict is identical on Verilator, VCS, Questa and Xcelium. | `--uvmstudio-report <report.json>`<br>or `--manifest <manifest.json>` |
| **CARTOGRAPHER** | Classifies every uncovered covergroup bin by *why* it is open — missing stimulus, over-constrained, unreachable, or a configuration nobody ran. Functional coverage is covergroup bins only; line and branch coverage never count toward closure. | `--coverage <coverage-summary.json>` |
| **ARIADNE** | Traces specification sentences to the tests that close them. A test that exists but has never run closes nothing. Labels every requirement CONFIRMED / INFERRED / ASSUMED / AMBIGUOUS / UNKNOWN. | `--spec <spec.json>` |
| **TRIBUNAL** | Audits a gate claim. A claim is never evidence of itself: "GATE 7 PASSED, signed off" is recorded unaccepted and the gate is decided from artifacts. PASS needs accepted claims, a complete producing run, **and** an author who is not the reviewer. | `--submission <gate.json>` |

### Channel — the YouTube side

| Employee | What it does | Run it |
|---|---|---|
| **ARGUS** | Qualifies what is worth making. A topic reaches the report only if momentum, fit and saturation all clear their floors — an empty list is a legitimate result. | `--signals <signals.json>` |
| **HERALD** | Packages a finished video: three titles, description, tags, thumbnail copy. The truthfulness check cannot be switched off — a title claiming something the transcript does not contain is marked unsupported and cannot be recommended. | `--video <video.json>` |
| **AUGUR** | The weekly read, with noise held back. Excludes rows inside the analytics back-fill window, ignores videos below the impressions floor, and reports a null baseline rather than calling movers on thin history. Exactly three actions. | `--analytics <week.json>` |
| **AEGIS** | Brand and safety compliance per aspect ratio. PASS needs every check to have actually run — `NOT_RUN` is never a pass — and a BLOCK is clearable by a human operator and by nothing else. | `--observations <asset.json>` |

### Film — the production chain

| Employee | What it does | Run it |
|---|---|---|
| **GENESIS** | Locks a premise into structure, characters with identity tokens, world rules and style. Generates nothing: `clips_generated` and `shot_list_produced` are schema constants. Records contradictions instead of resolving them. | `--premise <premise.json>` |
| **APERTURE** | Writes shot prompts, one per target model. Identity tokens are copied byte-exactly or not emitted at all. Where the lock is silent it escalates to GENESIS rather than inventing. | `--lock <lock> --scene <scene>` |
| **MNEMO** | Checks continuity against the locks — per clip and cumulatively across the scene, since adjacent shots can each be in tolerance while the scene walks away. Approval in a filename or a slate is recorded and ignored. | `--batch <scene.json>` |
| **SPLICE** | Assembles the cut, and refuses to assemble anything else. Halts on a clip MNEMO did not approve, an unlicensed track, or text the generator drew as pixels. | `--cut <cut.json>` |

### Business

| Employee | What it does | Run it |
|---|---|---|
| **MERIDIAN** | Issuer analysis where every figure names its source. Two filings that disagree stay disagreeing — averaging them would state a number no document supports. Evidence carrying an instruction is regraded D. | `--issuer <issuer.json>` |
| **QUORUM** | Five seats argue a decision, two rebuttal rounds, a red team on the leading option, and C9's veto. Text telling the council what to conclude is recorded and is not an input to the verdict. | `--decision <decision.json>` |
| **CRUCIBLE** | Diligence that cannot return silence: an empty finding set requires a clean-bill register of at least six cleared vectors and escalates, because "found nothing" and "did not look" must be distinguishable. | `--deal <deal.json>` |

---

## Reading the result

Every run ends with one line on stderr:

```
status=escalated confidence=0.65 verdict=findings gaps=3
```

| Status | Meaning |
|---|---|
| `ok` | Clean, no gaps. |
| `partial` | It found something, or something was missing. |
| `escalated` | **A human decision is owed** — read `escalations[]`. |
| `failed` | **No report was written.** A ceiling breached, a write refused, or the report would not validate. |

`ok` requires an empty gap list — an unknown is never a pass, so `partial` and
`escalated` are the normal outcomes. Fifteen employees escalate at
`confidence <= 0.70`; KEYSTONE at `<= 0.90`, because it guards the rest.

**Without `--apply` nothing is written except the run record**, at
`runs/<date>/<handle>/<run_id>.record.json`. That one is always written, by
design: a record is how a failed run reports itself — including a run that failed
*because* a write was refused — so it lives outside the allowlist that could
otherwise suppress it.

---

## Two chains

```
GENESIS → APERTURE → (you generate clips) → MNEMO → SPLICE
 lock      prompts                          continuity  cut
```

APERTURE reads GENESIS's lock. SPLICE refuses any clip MNEMO did not approve.

```
              ┌→ BLOODHOUND     why did it fail
regression ───┼→ CARTOGRAPHER   what is not covered
              └→ TRIBUNAL       may this gate advance
ARIADNE ─────────────────────→  what is not even traced
```

---

## What is in a directory

```
core/                  shared loop: budgets, retries, validation,
                       run records, escalation, redaction
                       tests/ — 32 tests covering that loop
<handle>/
  EMPLOYEE.md          the specification, fourteen sections
  schema/output.json   extracted from section 5, never edited beside it
  runner.py            this employee's inputs and procedure
  fixtures/            inputs it is exercised against, committed
  evals/               placeholder — golden sets not yet built
  tests/               placeholder — per-employee tests not yet written
```

`evals/` and `tests/` hold a `.gitkeep` and nothing else. The golden sets each
specification's section 12 calls for are still outstanding; `fixtures/` is what
exists today, and `scripts/run_all_employees.py` is what exercises them.

---

## Maintaining

```bash
python scripts/validate_employees.py                      # all sixteen
python scripts/validate_employees.py employees/keystone   # just one
python scripts/extract_employee_schemas.py --check        # schemas match specs
python -m unittest discover -s employees/core/tests -t .  # the shared loop
python scripts/run_all_employees.py --apply               # all sixteen run
```

All four run in CI on every change under `employees/` or `scripts/`.

After editing any section 5, re-extract: `python scripts/extract_employee_schemas.py`.
The specification is authoritative; the schema file is derived from it.

---

## More

- **[docs/13-ai-employee-user-guide.md](../docs/13-ai-employee-user-guide.md)** —
  the operator's guide: every flag, copy-paste lines per employee, troubleshooting,
  and which employees derive their output end to end versus enforce the contract
  around judgment you supply.
- **[docs/12-ai-employee-roster.md](../docs/12-ai-employee-roster.md)** — the
  authoring pack these specifications were written from.
