# Setup — Claude

Two independent surfaces. Do both if you use both.

## A · Claude Project (chat)

1. **Create the project.** Claude → Projects → New project, named `Generative AI Journalist`.
2. **Set custom instructions.** Copy the whole body of
   [`platforms/claude/project-instructions.md`](../platforms/claude/project-instructions.md) below its
   `---` separator into Project settings → custom instructions.
3. **Add project knowledge.** Upload:
   - `knowledge/dv/DV_Bible_Index.md` and `knowledge/dv/DV_Engineering_Bible_Vol1.md`
   - `knowledge/dv/agentic_ai_dv_architecture.md`
   - `knowledge/outskill/CURRICULUM.md`
   - your generated `knowledge/outskill/index.jsonl` content, if you want verbatim course recall
4. **Install the skills.** Run `python scripts/build_claude_bundle.py`, then add each folder under
   `dist/claude/skills/` as an Agent Skill. Keep the folder structure — `references/` and `assets/`
   must travel with each `SKILL.md`.
5. **Verify routing.** Ask the four checks in `docs/05-evaluation.md`. Each should name the skill or
   module it used.

## B · Claude Code (terminal)

1. Clone the repo and copy the repo guide into place:

   ```bash
   cp platforms/claude/CLAUDE.md ./CLAUDE.md
   ```

2. Optionally symlink the skills so Claude Code discovers them:

   ```bash
   mkdir -p .claude/skills
   ln -s ../../skills/dv/dv-engineering-suite .claude/skills/dv-engineering-suite
   for d in skills/genai/*/; do ln -s "../../$d" ".claude/skills/$(basename "$d")"; done
   ```

   On Windows without developer mode, copy instead of symlinking, and re-copy after edits.

3. Confirm with `/skills` that all eleven skills are listed.

## Expected result

| Ask | Should load |
|---|---|
| "Write a vplan for this AXI bridge spec" | `dv-engineering-suite` → module 02, then 11 |
| "My scoreboard mismatches at 4200ns" | `dv-engineering-suite` → module 17 |
| "Build me a shotlist for a 60-second film" | `visual-storytelling-director` |
| "Design the agent loop for a research tool" | `agent-harness-engineer` |

If a DV question loads a `genai` skill, the DV description's trigger keywords need widening — not the
other way round.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Skill never triggers | Description lacks the user's actual phrasing | Add trigger keywords to `description` |
| Both families trigger | Overlapping keywords, e.g. "agent" | Both suites carry explicit DO-NOT-use lines; keep them |
| Broken reference link | Folder uploaded without `references/` | Re-upload the complete folder |
| Answers ignore the rules | Instructions pasted with the header | Paste only the body below the `---` |
