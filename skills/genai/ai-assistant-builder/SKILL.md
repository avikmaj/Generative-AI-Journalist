---
name: ai-assistant-builder
description: "Build saved AI assistants and agents in Custom GPTs, Claude Projects or Gemini Gems: system prompt in Markdown, reusable skills, tools, memory, no-code RAG over knowledge files, and loop or heartbeat scaling toward an AI employee. Load when the user wants to create a Custom GPT, Claude Project, Gem, or a briefed reusable assistant. Not for coded agent harnesses or n8n workflows."
---

# AI assistant builder

Grounded in OUTSKILL Book Four. Give it a role, skills, tools and memory — then let it loop.

## Place the request on the ladder first

**Chatbot** (answers) → **Assistant** (a saved, briefed helper) → **Agent** (takes actions with
tools) → **AI employee** (runs a whole job end to end).

Name the target rung before designing. Most requests for an "agent" only need an assistant, which is
cheaper, more reliable and shippable today. Climb a rung only when the rung below cannot do the job.

## Anatomy of an AI employee

| Component | Question it answers | Where it lives |
|---|---|---|
| System prompt | Who is it, and what are its rules? | Instructions field |
| Skills | How does it do each recurring job? | Skill files / knowledge files |
| Tools | What can it act on? | Actions, connectors, MCP |
| Memory | What does it carry forward? | Project memory, saved files |
| Loop | How does it know it is done? | Termination predicate + schedule |

Design all five. A missing termination predicate is why assistants stall halfway; missing skills are
why they answer inconsistently.

## Procedure

1. **Write the job description, not a personality.** One paragraph: the job it owns, the inputs it
   receives, the artifacts it produces, and the definition of done.
2. **Write the system prompt in Markdown.** Use `## Role`, `## Rules`, `## Steps`, `## Output`.
   Structure makes instructions easier for the model to follow than a wall of text. Numbered rules
   are followed more reliably than prose paragraphs.
3. **Extract skills.** Any procedure the assistant will repeat becomes its own playbook file rather
   than more system-prompt text. This keeps the system prompt short and the context window clean.
4. **Attach knowledge files for no-code RAG.** Attach documents to the Project so the assistant
   answers from them — no pipeline, no code. Require it to cite the file and section, and to say
   "not in the provided knowledge" rather than improvising.
5. **Add tools only for what it must change in the world.** Every tool is a new failure and permission
   surface. Put a confirmation step in front of anything irreversible.
6. **Choose the platform** by what the job needs:

   | Platform | Strength | Watch out |
   |---|---|---|
   | Custom GPT | Shareable, Actions via OpenAPI, browsing + code interpreter | Single instructions field; knowledge-file limits |
   | Claude Project | Long context, project knowledge, Skills, Artifacts | Sharing is workspace-scoped |
   | Gemini Gem | Tight Google Workspace reach | Thinner tool ecosystem |

   Projects are not just for teams — use one for personal work too.
7. **Test with the awkward cases first**: missing input, out-of-scope request, contradictory
   instruction, and a question the knowledge files do not answer. Passing these is what separates a
   working assistant from a demo.

## Scaling the work

- **Loop engineering** — keep it iterating until the definition of done is met, with a step cap.
- **Heartbeat** — it wakes on a schedule instead of waiting to be asked.
- **Agent swarm** — many agents split one job; only worth it when the sub-jobs are genuinely parallel.
- **Harness** — a runner (e.g. Codex-style) executes the agent loop outside the chat UI.

Add these in that order. Reaching for a swarm before loop discipline multiplies an unreliable unit.

## Output format

Ladder rung + rationale → job description → Markdown system prompt (complete, ready to paste) → skill
file list → knowledge file list → tool list with confirmation gates → test cases → `Open questions`.
