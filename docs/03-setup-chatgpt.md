# Setup — ChatGPT Custom GPT

## Steps

1. **Build the bundle.**

   ```bash
   python scripts/build_chatgpt_bundle.py
   ```

   This writes `dist/chatgpt/` with one flattened file per skill, because ChatGPT cannot resolve
   relative paths between knowledge files.

2. **Create the GPT.** ChatGPT → Explore GPTs → Create.

3. **Configure.**

   | Field | Value |
   |---|---|
   | Name | Generative AI Journalist |
   | Description | Two-mode technical collaborator: semiconductor design verification, and generative-AI engineering. |
   | Instructions | The body of [`platforms/chatgpt/system-prompt.md`](../platforms/chatgpt/system-prompt.md) below its `---` |
   | Conversation starters | The four in [`conversation-starters.md`](../platforms/chatgpt/conversation-starters.md) |

4. **Upload knowledge** from `dist/chatgpt/`. Names are load-bearing — the router in the system prompt
   references them literally. Do not rename. See
   [`knowledge-manifest.md`](../platforms/chatgpt/knowledge-manifest.md) for the full list.

5. **Set capabilities.** Web browsing **on** (rule 2 requires verifying versions and prices), code
   interpreter **on** (coverage math, log parsing), image generation **off**.

6. **Actions — optional.** Only if you expose a companion API. See
   [`actions/openapi.example.yaml`](../platforms/chatgpt/actions/openapi.example.yaml). Secure it
   first; a Custom GPT Action is callable on your behalf.

7. **Verify** with the checks in `docs/05-evaluation.md`.

## Knowledge-file budget

ChatGPT caps knowledge files, so the DV suite cannot ship as 23 separate files. The builder emits:

- `SKILL_dv_dv-engineering-suite.md` — hub plus the module router
- `DV_MODULES_CORE_UVM.md` — modules 01–10
- `DV_MODULES_PROTOCOLS_FORMAL.md` — modules 11–15
- `DV_MODULES_COVERAGE_DEBUG_OPS.md` — modules 16–22
- one `SKILL_genai_<name>.md` per genai skill

The system-prompt router points at these consolidated names. If you change the grouping, change the
router in the same commit.

## Known ChatGPT limitations

| Limitation | Workaround in this repo |
|---|---|
| No native skills | Router table inlined in the system prompt |
| No relative paths between files | `references/` flattened under `## Reference:` headings |
| Knowledge-file count cap | DV modules consolidated into three grouped files |
| Lossy PDF extraction | Everything shipped as Markdown |
| Shorter instruction budget | ChatGPT prompt is the compressed variant of the Claude one |
| No persistent per-project memory | Durable facts belong in the instructions, not in chat |
