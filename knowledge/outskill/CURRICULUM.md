# OUTSKILL Generative AI Bootcamp — curriculum map

Structural index of the corpus, used to route `genai` skills to the right source. Concept names below
are the canonical vocabulary the skills reuse verbatim, so answers match the course language.

Cohort: BC11, June 2026. Two tracks: the **Generalist** bootcamp (six books) and the
**AI-Native Engineer** bootcamp (four mentor sessions).

## Track 1 — The Generalist bootcamp

### Book One · The AI Generalist Mindset
Session 1. How models work, the craft of prompting, assembling a tool stack.

- How an LLM answers, five steps: tokenize → embed → attention → predict → decode & repeat
- The 6-part prompt formula: Role, Context, Task, Format, Constraints, Example
- Frameworks: CoStar (Context, Objective, Steps, Tools, Reflection); chain-of-thought; Socratic;
  ACR (Ask, Check, Recommend)
- Advanced techniques: zero-shot, few-shot, chain-of-thought, self-consistency, tree-of-thoughts, ReAct
- Context is the whole game — context rot, the "lost in the middle" degradation
- Tool stack by function: Reason / Image-video / Audio / Save / Act

→ Skill: `prompt-architect`

### Book Two · Vibe Coding
Session 2. Building real software by describing it.

- Every app has three layers: frontend, backend, database; an API carries requests between them
- The vibe-coding loop: describe → generate → preview → refine → deploy
- Tools: Lovable, Bolt, v0, Replit, Cursor
- Rules: start with a short PRD; one feature at a time; give context (paste errors, share
  screenshots); revert to the last working version when it breaks
- Prompt the invisible parts — architecture and UX, which the AI will not add unasked
- From build to business: payments (Stripe, Razorpay), Google auth, deploy on Vercel, add a domain

→ Skill: `vibe-coding-builder`

### Book Three · AI Workflows & Connectors
Session 3. From one-off prompts to repeatable systems that act across apps.

- Prompt → workflow: a repeatable chain where each step's output feeds the next
- Integration layers: Connector (no code) · MCP (the standard behind connectors) · API (full control)
  · RAG (ground in documents)
- Connectors turn chat into action: Gmail, Drive, Calendar, Notion
- The DRA deck workflow: Designer → Researcher → Analyst, run in sequence
- The ACR pattern: Ask, Check, Recommend
- Data analysis discipline: restate the columns first; ask ordered questions; force a "so what"

→ Skill: `ai-workflow-designer`

### Book Four · Building Custom AI Assistants & Agents
Day 2. From a chatbot to a self-improving AI employee.

- The ladder: Chatbot → Assistant → Agent → AI employee
- Anatomy of an AI employee: system prompt, skills, tools, memory, loop
- Where you build one: Custom GPTs, Claude Projects, Gemini Gems
- Write the system prompt in Markdown — `## Role`, `## Rules`, `## Steps`
- No-code RAG: attach knowledge files to a Project
- Scaling: loop engineering, heartbeat, agent swarm, harness

→ Skill: `ai-assistant-builder`

### Book Five · Building AI Agents on n8n
Day 2, session 2. Node-based automation and always-on agents.

- Three building blocks: trigger → node → action
- Triggers: webhook, schedule, chat message, form
- The AI Agent node: model, tools, memory
- Reference build — support agent: trigger → AI Agent → tools → respond
- Robustness: error branches, retries on flaky calls, fallback replies
- Going further: vector store for RAG; self-host or n8n cloud for always-on

→ Skill: `n8n-agent-builder`

### Book Six · Visual Storytelling with AI
Images and video via the diffusion pipeline.

- How diffusion works: start from noise, denoise step by step guided by the prompt
- The master prompt, six parts: Subject, Style, Camera, Lighting, Composition, Mood
- Camera language: wide shot, close-up, low angle, 85mm, bokeh, dolly in
- Negative prompts: exclude extra fingers, text, watermark, blurry
- The filmmaking workflow: still first, then animate
- Toolbox: Midjourney and Nano Banana (image); Kling, Runway, Veo (video); Suno and ElevenLabs (sound)

→ Skill: `visual-storytelling-director`

### Toolkit · The AI Generalist Roadmap + Gen AI Money Playbook
Five levels, definition of done per level, starter stack, three projects to ship per level, and a
model-selection framework. Level 1 Foundations (PRD method) → Level 2 Context & Connections (RAG, MCP)
→ Level 3 Multimodal Creation → Level 4 Agents & Automation → Level 5 Vibe Coding.

→ Skill: `ai-generalist-roadmap-coach`

## Track 2 — The AI-Native Engineer

Four mentor sessions plus breakouts, for people who build AI tools rather than only use them. The
through-line: an LLM is a probabilistic collaborator, and specs, phase gates, tool IDs, refusal logic
and evals exist to wrap that probabilistic core in auditable structure. The invariant skeleton is
think → plan → build → review, with human gates on anything that mutates the world.

| Part | Covers | Skill |
|---|---|---|
| I · Developer productivity with AI | Documentation-first habit, layered prompting in the IDE, plan vs auto mode, human-in-the-loop gates, context-window hygiene, spec-driven loops, MCP, sub-agents and skills, effort budgeting | `prompt-architect`, `vibe-coding-builder` |
| II · The single-agent harness | Stateless cores, multi-turn chat shape, agency and tool schemas, who executes, idempotency and tool-call IDs, the single round and the agent loop, tool budgets | `agent-harness-engineer` |
| III · Multi-agent orchestration | Framework trade-offs, agent primitives, tasks, crews, context threading, guardrails, runtime budgets, sequential vs parallel | `agent-harness-engineer` |
| IV · RAG fundamentals & retrieval quality | The canonical pipeline, parsing, chunking and overlap, embeddings and vector stores, retrieval symmetry, answer synthesis, splitters, parsers, evals | `rag-pipeline-designer`, `eval-harness-builder` |

## Citation convention

Skills cite the corpus as `OUTSKILL/<file> §<section>` — for example
`OUTSKILL/Quick_Reference_Cards.pdf §Book One`. Never quote more than a short phrase verbatim; the
material is licensed.
