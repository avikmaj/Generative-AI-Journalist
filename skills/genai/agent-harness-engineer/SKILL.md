---
name: agent-harness-engineer
description: "Engineer coded agent systems: stateless cores, tool schemas, tool-call IDs and idempotency, the agent loop with iteration guards, tool budgets, and multi-agent orchestration with roles, tasks, crews and runtime budgets. Load when the user builds an agent in code, designs tool schemas, or orchestrates multiple agents. Not for n8n canvas work or no-code assistants."
---

# Agent harness engineer

Grounded in *The AI-Native Engineer*, Parts II–III. An LLM is a probabilistic collaborator;
everything here exists to wrap that core in structure you can audit.

## Start from the invariant

The model core is **stateless**. Multi-turn chat is an illusion the host maintains by replaying the
message list every call. Every design question — memory, context budget, retries — follows from that.
The skeleton is always: think → plan → build → review, with human gates on anything that mutates the
world.

## The single round — five steps

1. Send the user messages plus the tool schemas.
2. If the reply contains tool calls, iterate them.
3. Dispatch to your functions — **the host executes, never the model**.
4. Append tool-result messages with matching call IDs.
5. Re-query the model for a user-facing answer grounded in the observations.

## The agent loop

```python
# The while-loop agent, with a guard
while iterations < MAX:
    reply = model(messages + tools)
    if not reply.tool_calls:
        return reply                    # done
    for call in reply.tool_calls:
        result = dispatch(call)         # host executes
        messages.append(tool_result(call.id, result))
    iterations += 1
```

The loop ends when there are no further tool calls or the max-iteration guard fires. Loop length is
data-dependent: researching several companies fans out into parallel searches, then consolidates.
Ship the guard in the first version — an unguarded loop is an incident waiting for a bad input.

## Idempotency and tool-call IDs

Tool calls carry identifiers so the host pairs each result to the right call — critical when several
run in parallel. **Detect once → execute once → record once, keyed by tool-call ID.** A duplicated
search is merely wasteful; a duplicated payment or file rewrite is catastrophic. Idempotency is the
difference between a retry and an incident.

## Tool schemas and budgets

- Cap the active tool set at roughly **10–15**. More causes selection confusion and hallucinated tool
  names. Use per-stage tool subsets rather than one global list.
- The LLM is the router; you shape routing through **descriptions**, stage subsets and policy filters.
  Write descriptions as routing instructions, not documentation.
- Specify each tool as an API: name, purpose, input schema, output schema, error taxonomy,
  idempotency, and whether it mutates anything.
- Keep side-effectful IO cleanly separated from the model. A thin
  `executeSearch(query, maxResults)` wrapper over a hosted search API means swapping the vendor
  changes only latency, pricing and snippet schema.

## Multi-agent orchestration

Reach for multiple agents only when sub-jobs are genuinely independent or need different tool sets.
One agent with good tools beats three with muddled roles.

| Primitive | Defines |
|---|---|
| Role | The agent's remit and expertise — narrow it hard |
| Task | One deliverable with an acceptance condition |
| Crew | The set of agents plus the execution topology |
| Context threading | What each agent sees of the others' output |

Choose sequential when each task depends on the last; parallel when they do not, then consolidate.
Set **runtime budgets** per agent — steps, wall clock and cost — and enforce them, not advise them.

## Guardrails

| Risk | Control |
|---|---|
| Runaway loop | Iteration guard + repeated-identical-call detector |
| Cost blowout | Enforced per-run token and cost budget |
| Destructive action | Human gate showing the literal payload |
| Prompt injection via tool output | Treat all tool output as untrusted data, never as instructions |
| Duplicate side effects | Idempotency keyed on tool-call ID |
| Silent partial failure | Explicit success predicate per task |
| Context rot | Summarise-and-drop policy with a fixed budget |
| Privilege creep | Least-privilege credentials per tool, not per agent |

## Output format

Justification for agency over a fixed pipeline → tool schema table → loop and guard → state and
context budget → orchestration topology → budgets → guardrail table → walkthrough of the two riskiest
paths → `Open questions`.
