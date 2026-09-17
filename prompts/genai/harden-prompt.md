# Harden an existing prompt

Expected skill: `prompt-architect`. Expected mode: `[GENAI]`.

```text
Harden this prompt.

Current prompt: <PASTE>
Model and surface: <MODEL / API / PROJECT>
What goes wrong today: <OBSERVED FAILURE MODES>
Must never happen: <HARD CONSTRAINTS>

Return:
1. The rewritten prompt, complete and paste-ready.
2. A change table: what changed, which failure mode it addresses, and the risk it introduces.
3. Three adversarial inputs that would still break it, with the expected correct behaviour for each.

Do not add politeness padding or role-play framing that does not change behaviour. Prefer explicit
output contracts over stylistic instruction.
```

## Why it is shaped this way

Asking for the residual failure modes prevents a rewrite that merely looks more thorough. The change
table forces each edit to justify itself against an observed failure rather than a guess.
