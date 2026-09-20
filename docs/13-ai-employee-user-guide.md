# AI Employee User Guide

How to actually use the sixteen. Specifications live in `employees/<handle>/EMPLOYEE.md`;
this is the operator's page.

---

## 1. The thirty-second version

Every employee is one command with the same shape:

```bash
python employees/<handle>/runner.py <its inputs>            # look, write nothing
python employees/<handle>/runner.py <its inputs> --apply    # write the report
```

Try one right now — every employee except KEYSTONE ships a fixture:

```bash
python employees/bloodhound/runner.py \
  --uvmstudio-report employees/bloodhound/fixtures/report.json

python scripts/run_all_employees.py     # all sixteen, read-only
```

No API key. No network. No install beyond Python 3.12. `jsonschema` is optional
— without it a structural fallback validates instead and says so in the output.

---

## 2. The two flags every employee has

| Flag | Effect |
|---|---|
| *(omitted)* | **Read-only.** Prints the report to stdout. Writes no report. |
| `--apply` | Writes the report to `reports/<handle>/<date>.json`. |
| `--reports-root DIR` | Where `reports/` and `runs/` are rooted. Defaults to the current directory. |

**The safety model in one line:** without `--apply` an employee can read but not
write, and a write is refused unless its destination is on that employee's
allowlist in section 7 of its specification.

**One thing is always written, with or without `--apply`:** the run record, at
`runs/<date>/<handle>/<run_id>.record.json`. That is deliberate — a record is how
a failed run reports itself, including one that failed *because* a write was
refused, so it lives outside the allowlist that could otherwise suppress it.

---

## 3. Reading what comes back

Every run ends with one line on stderr:

```
status=escalated confidence=0.65 verdict=findings gaps=3
```

### status — read this first

| Status | Meaning | What you do |
|---|---|---|
| `ok` | Clean, no gaps, nothing unknown. | Nothing. |
| `partial` | It found something, or something was missing. | Read the findings. |
| `escalated` | **A human decision is owed.** | Read `escalations[]` — it says what is needed. |
| `failed` | A ceiling was breached, a write refused, or the report would not validate. | **No report was written.** Read the run record. |

`ok` requires an empty gap list. An unknown is never a pass — that rule is the
whole point of the set, so expect `partial` and `escalated` to be normal.

### confidence

Fifteen of the sixteen escalate at **`confidence <= 0.70`**. KEYSTONE escalates
at `<= 0.90` because it guards everything else. The comparison is inclusive on
purpose: a capped deduction can land exactly on the line, and an exclusive
comparison would let that through.

### gaps

`gaps` is the list of what it could not establish. It is not noise — it is the
reason the status is what it is. `usd-ceiling-unenforceable:no-price-table`
appears on every run until you configure token prices, which correctly keeps
runs off `ok` rather than pretending a cost ceiling is enforced.

---

## 4. The sixteen: what each is for

### Platform

| | Reach for it when | Feed it |
|---|---|---|
| **KEYSTONE** | You changed a skill, a catalog or a prompt anywhere across the four repos and want to know what drifted. | `--repos <dir containing all four repos>` |

### DV — your day job

| | Reach for it when | Feed it |
|---|---|---|
| **BLOODHOUND** | A nightly regression failed and you want clusters, not a list of failing test names. | `--uvmstudio-report <report.json>` or `--manifest <manifest.json>` |
| **CARTOGRAPHER** | Coverage is short of closure and you need to know *why* each hole is open — missing stimulus, over-constrained, unreachable, or a config nobody ran. | `--coverage <coverage-summary.json>` |
| **ARIADNE** | You need a traceability matrix that distinguishes a requirement closed by a passing test from one "closed" by a test that never ran. | `--spec <spec.json>` |
| **TRIBUNAL** | Somebody says a gate passed and you want that claim audited against artifacts. | `--submission <gate.json>` |

### Channel — the YouTube side

| | Reach for it when | Feed it |
|---|---|---|
| **ARGUS** | Deciding what to make next and you want topics that clear a bar, not a daily list of ten. | `--signals <signals.json>` |
| **HERALD** | A video is finished and needs titles, description, tags and thumbnail copy — with every title checked against the transcript. | `--video <video.json>` |
| **AUGUR** | The weekly numbers are in and you want real movers, not back-fill noise. | `--analytics <week.json>` |
| **AEGIS** | A master is about to go out and you want brand and safety compliance per aspect ratio. | `--observations <asset.json>` |

### Film — the production chain

| | Reach for it when | Feed it |
|---|---|---|
| **GENESIS** | A premise needs locking into structure, characters, identity tokens, world rules and style before a single shot is written. | `--premise <premise.json>` |
| **APERTURE** | A locked scene needs shot prompts, one per target model, with identity tokens copied byte-exactly. | `--lock <lock> --scene <scene>` |
| **MNEMO** | Clips came back and you need continuity checked against the locks, per clip and across the scene. | `--batch <scene.json>` |
| **SPLICE** | Approved clips need assembling into a cut — and anything unapproved or unlicensed must stop it. | `--cut <cut.json>` |

### Business

| | Reach for it when | Feed it |
|---|---|---|
| **MERIDIAN** | An issuer needs analysing and you want every number to name its source — with disagreements kept as disagreements. | `--issuer <issuer.json>` |
| **QUORUM** | A real decision needs five seats arguing it, a red team on the leading option, and the dissent recorded. | `--decision <decision.json>` |
| **CRUCIBLE** | Diligence on a target, where "we found nothing" must be distinguishable from "we did not look". | `--deal <deal.json>` |

---

## 5. Copy-paste: every employee against its fixture

Swap the fixture path for your own file when you have one. Add `--apply` to write.

```bash
# Platform
python employees/keystone/runner.py --repos ..

# DV
python employees/bloodhound/runner.py \
  --uvmstudio-report employees/bloodhound/fixtures/report.json \
  --routing-table   employees/bloodhound/fixtures/routing-table.json
python employees/cartographer/runner.py \
  --coverage employees/cartographer/fixtures/coverage-summary.json \
  --vplan    employees/cartographer/fixtures/verification_plan.json
python employees/ariadne/runner.py  --spec       employees/ariadne/fixtures/spec.json
python employees/tribunal/runner.py --submission employees/tribunal/fixtures/gate.json

# Channel
python employees/argus/runner.py  --signals   employees/argus/fixtures/signals.json
python employees/herald/runner.py --video     employees/herald/fixtures/video.json
python employees/augur/runner.py  --analytics employees/augur/fixtures/week.json
python employees/aegis/runner.py  --observations employees/aegis/fixtures/asset.json

# Film
python employees/genesis/runner.py  --premise employees/genesis/fixtures/premise.json
python employees/aperture/runner.py \
  --lock  employees/genesis/fixtures/premise.json \
  --scene employees/aperture/fixtures/scene.json
python employees/mnemo/runner.py  --batch employees/mnemo/fixtures/scene.json
python employees/splice/runner.py --cut   employees/splice/fixtures/cut.json

# Business
python employees/meridian/runner.py --issuer   employees/meridian/fixtures/issuer.json
python employees/quorum/runner.py   --decision employees/quorum/fixtures/decision.json
python employees/crucible/runner.py --deal     employees/crucible/fixtures/deal.json
```

### Optional flags worth knowing

| Employee | Flag | Use |
|---|---|---|
| BLOODHOUND | `--sim verilator\|vcs\|questa\|xcelium` | Selects the tool error prefix and nothing else. The UVM verdict is identical across all four. |
| BLOODHOUND | `--routing-table <json>` | Maps `cause_domain` to an owning department. Without it every cluster is `UNROUTED` and confidence drops. |
| CARTOGRAPHER | `--vplan`, `--config-matrix` | Without the vplan, holes are classified but routed `unassigned`. |
| APERTURE | `--models veo-3,sora-2,...` | A model with no known price leaves `cost_complete: false` rather than guessing zero. |
| MERIDIAN | `--as-of YYYY-MM-DD` | The date staleness is measured against. |
| GENESIS | `--format "<format>"` | Overrides the series default. |

---

## 6. The two chains

**Film** — each feeds the next:

```
GENESIS  →  APERTURE  →  (you generate clips)  →  MNEMO  →  SPLICE
 lock       prompts                               continuity  cut
```

APERTURE reads GENESIS's lock; SPLICE refuses any clip MNEMO did not approve.

**DV** — each answers a different question about the same night:

```
              ┌→ BLOODHOUND    why did it fail
regression ───┼→ CARTOGRAPHER  what is not covered
              └→ TRIBUNAL      may this gate advance
ARIADNE ─────────────────────→ what is not even traced
```

---

## 7. Two kinds of employee — and which need an API key

None of them calls a model today. Every runner is deterministic Python. But that
splits the sixteen in two, and it matters for what you can expect:

**Derives everything from raw inputs** — genuinely end-to-end today:
KEYSTONE, BLOODHOUND, CARTOGRAPHER, ARIADNE, TRIBUNAL, AUGUR, HERALD, GENESIS,
APERTURE, SPLICE.

BLOODHOUND reads raw simulation logs and reaches its own verdict. CARTOGRAPHER
parses a coverage database and classifies every hole. Nothing is supplied to them
but the artifacts themselves.

**Enforces the rules over judgment you supply** — the contract works, the
judgment has to come from somewhere:
AEGIS and MNEMO (need vision over frames), MERIDIAN, CRUCIBLE and QUORUM (need
analysis), ARGUS (needs scoring).

QUORUM red-teams, scores and vetoes the five seats' arguments — it does not yet
write them. Those six are where an API key buys you something.

---

## 8. Checking the set still holds together

```bash
python scripts/validate_employees.py                       # 14-section contract
python scripts/extract_employee_schemas.py --check         # schemas match specs
python -m unittest discover -s employees/core/tests -t .   # the shared loop
python scripts/run_all_employees.py --apply                # all sixteen run
```

All four run in CI on every change under `employees/` or `scripts/`.

After editing any `EMPLOYEE.md` section 5, re-extract the schema:

```bash
python scripts/extract_employee_schemas.py
```

The specification is authoritative; the schema file is derived from it, never
edited beside it.

---

## 9. When something goes wrong

| Symptom | Cause | Fix |
|---|---|---|
| `status=failed`, no output | The report did not validate, so it was refused. | Read `runs/<date>/<handle>/*.jsonl` — the `run.error` line names the exact field. |
| KEYSTONE exits 1 immediately | It refuses a partial sweep; one of the four repos is missing. | Check out all four side by side, or skip it. |
| Every run says `usd-ceiling-unenforceable` | No token price table configured. | Expected. Configure prices, or accept that runs stay off `ok`. |
| `schema-validation-degraded` gap | `jsonschema` is not installed. | `pip install jsonschema` — or accept the structural fallback, which says so. |
| A gap you disagree with | Usually a stated assumption that does not match your setup. | Check `## STATED ASSUMPTIONS` at the bottom of that `EMPLOYEE.md`. That is the correction sheet. |

---

## 10. Regenerating the DV fixtures

BLOODHOUND's and CARTOGRAPHER's fixtures are produced by driving the real code of
`avikmaj/Verification_Studio_platform_repo`, not written by hand:

```bash
python scripts/make_dv_fixtures.py --studio-src <platform-checkout>/src
```

A change to that platform's verdict logic changes the fixtures, rather than
letting them silently diverge.
