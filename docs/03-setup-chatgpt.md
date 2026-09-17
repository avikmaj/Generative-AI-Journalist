# ChatGPT setup

The canonical, limit-safe instructions are in
[`11-setup-cards.md`](11-setup-cards.md#chatgpt-custom-gpt).

Build with:

```bash
python3 scripts/build_chatgpt_bundle.py
```

Paste `dist/chatgpt/system-prompt.md` after its first `---` separator. Upload exactly five knowledge
files: `FAMILY_DV.md`, `FAMILY_GENAI.md`, `FAMILY_BUSINESS.md`, `FAMILY_FILM.md`, and `CONTROL.md`.
The builder fails above 4,000 instruction characters or if the upload count differs from five.

Use the connected private GitHub repository for the larger corpora; do not upload duplicate
`KNOWLEDGE_*.md` files.
