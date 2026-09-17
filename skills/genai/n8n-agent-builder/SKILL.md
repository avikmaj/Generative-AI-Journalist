---
name: n8n-agent-builder
description: "Design node-based n8n automations and always-on AI agents: triggers, nodes, actions, the AI Agent node with model, tools and memory, error branches, retries and vector-store RAG. Load when the user asks about n8n, node-based automation, or a scheduled or webhook-driven agent. Not for Custom GPTs, Claude Projects, or hand-coded harnesses."
---

# n8n agent builder

Grounded in OUTSKILL Book Five. Nodes replace code; error paths make it production-grade.

## The three building blocks

**Trigger** — what starts the run. **Node** — a step that does one thing. **Action** — the effect a
node produces. A workflow reads left to right: triggers → nodes → actions.

## Procedure

1. **Pick the trigger from the real world, not the demo.**

   | Trigger | Use when |
   |---|---|
   | Webhook | Another system must push an event in |
   | Schedule | The job runs on a cadence — the heartbeat pattern |
   | Chat message | A human converses with the agent |
   | Form | A human submits structured input |

2. **Decide deterministic nodes versus an AI Agent node.** If the routing is known in advance, use
   IF/Switch nodes — cheaper, testable, and it cannot hallucinate a branch. Use the AI Agent node
   only where the next step genuinely depends on interpreting the input.
3. **Configure the AI Agent node in three parts:** *Model* (the brain), *Tools* (what it can call),
   *Memory* (conversation context). Keep the active tool set small; a long tool list causes wrong-tool
   selection and invented tool names.
4. **Write each tool's description as the routing instruction.** In n8n the description is how the
   agent decides. Vague descriptions cause more failures than a weak model.
5. **Add error branches before you ship.** A node failure must not kill the run:
   - Error branch on every external call, routed to a notification or a queue.
   - Retries with backoff on flaky APIs — never on a non-idempotent write.
   - A fallback reply when a tool returns nothing, so the user is never left silent.
6. **Add a vector store for RAG** when the agent must answer from a knowledge base rather than from
   live app data.
7. **Decide hosting.** n8n cloud for speed; self-host for data residency, cost at volume, or custom
   nodes. Either way, always-on means you own monitoring.

## Reference build — the support agent

| # | Node | Does |
|---|---|---|
| 1 | Trigger | A customer message arrives |
| 2 | AI Agent | Reads it, decides what to do |
| 3 | Tools | Look up an order, search the docs |
| 4 | Respond | Send the answer back |

Extend this shape rather than inventing a new topology: add classification before step 2, a
human-approval node before any refund or account change, and an error branch off every tool.

## Production checklist

- [ ] Every external call has an error branch
- [ ] Retries configured only on idempotent operations
- [ ] Fallback response when a tool returns empty
- [ ] Credentials scoped to least privilege, stored in n8n credentials, never in a node body
- [ ] Irreversible actions gated behind a human approval node
- [ ] Executions logged and failures alerted somewhere a human looks
- [ ] Tool count kept small enough to route reliably
- [ ] Tested with a malformed trigger payload

## Output format

Trigger → node table in execution order → AI Agent configuration (model, tools, memory) → error paths
→ production checklist status → `Open questions`.
