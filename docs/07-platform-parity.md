# Platform parity

What each platform supports, what the builders do about it, and where behaviour legitimately differs.
Claude is the reference implementation: it is the only target that runs the canonical skill layout
unmodified.

## Capability matrix

| Capability | Claude Project | ChatGPT Custom GPT | Grok project |
|---|---|---|---|
| Native skills mechanism | Yes — Agent Skills | No | No |
| Nested `references/` honoured | Yes | No | No |
| Router location | In the skill descriptions | Inlined in the system prompt | Inlined in the instructions |
| Skill granularity shipped | One directory per skill | One file per skill, split when large | One file per family |
| Instruction length budget | Generous | Tighter | Tightest |
| Knowledge file count | Generous | Capped | Moderate |
| Executable assets (`.sv`, scripts) | Uploaded as files | Inlined in fenced blocks | Inlined in fenced blocks |
| Tool actions | Connectors / MCP | Actions via OpenAPI | Project tools |
| Live search bias | Low | Moderate | High |

## What the builders do about each gap

| Gap | Mitigation | Where |
|---|---|---|
| No native skills | Generate a router table from the skills actually rendered, and append it to the prompt | `build_chatgpt_bundle.py`, `build_grok_bundle.py` |
| No nested references | Flatten each `references/` file into a `## Reference: <path>` section, and tell the model to read those sections when a body points at `references/<path>` | `_bundle_lib.flatten` |
| Per-file size limits | Split a flattened skill into `_partNofM` at 280,000 characters; part 1 always carries the procedure | `_bundle_lib.MAX_FLAT_CHARS` |
| Knowledge file caps | Grok consolidates per family; the ChatGPT manifest states the count and what to drop first | `build_grok_bundle.py`, `build_chatgpt_bundle.py` |
| Non-markdown assets | Wrapped in language-tagged fences by extension | `_bundle_lib.flatten` |
| Licensed corpora | The Claude builder resolves `git ls-files --ignored` and skips anything git-ignored, rather than trusting a hardcoded deny-list | `build_claude_bundle.py` |

The generated router is generated on purpose. A hand-maintained router drifts from the filenames the
builder actually produced, and a router pointing at a file that was never uploaded fails silently —
the model simply improvises.

## Behaviour that is allowed to differ

- **Search citation strictness.** Grok's instructions add an explicit rule against browsing and then
  answering from recall, because its search bias makes that failure more likely.
- **Compression of examples.** The Grok and ChatGPT variants carry fewer worked examples. The rules
  are identical; only the illustration budget differs.

## Behaviour that must never differ

These are the invariants the golden set enforces on every platform. If a platform cannot hold one of
them, that is a defect in the bundle, not an acceptable variation.

1. The mode tag, including `[BOTH]`.
2. `UNVERIFIED` on any unsourceable version, price, model or metric claim.
3. `SYNTHETIC EXAMPLE` on any invented data.
4. `NOT_RUN`, `NOT_VERIFIED` and `BLOCKED` never reported as PASS.
5. No verbatim reproduction of licensed material.
6. No protocol, market or genre declared out of scope for lack of a dedicated module.
7. Cross-family routing on the shared vocabulary in the model card's disambiguation table.

## Verifying parity after a change

Run the same probes on all three platforms and compare:

```bash
python3 scripts/check_golden_set.py
```

Then hand the `route-*` and `guard-*` cases from `evals/golden-set.jsonl` to each platform. Any case
that passes on Claude and fails on another platform is a flattening or router bug — start by checking
whether the skill it should have loaded was actually uploaded, and whether it was split into parts.
