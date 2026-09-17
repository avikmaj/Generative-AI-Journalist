# OUTSKILL corpus drop-zone

This folder holds the normalised OUTSKILL Generative AI Bootcamp material that grounds the `genai`
skill family.

## What is committed and what is not

| Path | Committed? | Why |
|---|---|---|
| `README.md` | Yes | This file |
| `CURRICULUM.md` | Yes | A structural map and concept index — original summary, not course text |
| `raw/` | **No** — git-ignored | The source PDFs are licensed course material |
| `index.jsonl` | **No** — git-ignored | Contains extracted verbatim course text |

Never commit `raw/` or `index.jsonl`. The `.gitignore` already excludes them; do not override it.

## Populating it

```bash
python scripts/ingest_outskill.py --src "C:/Users/Avik Majumdar/Downloads/AI BOOKS - STUDY ROOM/OUTSKILL"
```

The script walks the source tree, extracts text from PDF/DOCX/MD/TXT, splits on headings, and writes
one JSON object per section to `index.jsonl` with `{file, book, section, anchor, text}`. Section
anchors are what the skills cite as `OUTSKILL/<file> §<section>`.

## Source structure

The archive is organised as six books plus a toolkit:

```
BC11 - Generative AI Bootcamp - June 2026/
  1. Access Your Tools/          Tool access redemption guide
  2. Pre-Reads/                  Six pre-read PDFs, one per book
  3. Workbook - Hands on Lab/    Six hands-on workbooks
  4. Session Notes/              Six session notes + churn dataset
  5. Roadmap to become an AI Generalist/   Roadmap + Money Playbook
BC11 - Generative AI Bootcamp - Personal Notes/
  Six compiled books + Complete_Bootcamp_Compendium + Quick_Reference_Cards
The_AI_Native_Engineer.pdf       Engineers' track: harness, orchestration, RAG
```

Pre-read, workbook, session notes and personal notes cover the *same* book at increasing depth. When
they conflict, prefer the personal notes and compendium — they are the reconciled version.
