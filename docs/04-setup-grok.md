# Grok setup

The canonical, limit-safe instructions are in
[`11-setup-cards.md`](11-setup-cards.md#grok-project).

Build with:

```bash
python3 scripts/build_grok_bundle.py
```

Paste `dist/grok/project-instructions.md` after its first `---` separator. Upload exactly five files:
`FAMILY_DV.md`, `FAMILY_GENAI.md`, `FAMILY_BUSINESS.md`, `FAMILY_FILM.md`, and `CONTROL.md`. The
governing VIP rules are inside `CONTROL.md`.

The builder fails above 4,000 instruction characters or if the upload count differs from five. Use
the connected private GitHub repository for larger corpora.
