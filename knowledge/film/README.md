# Film knowledge base

Deep source material behind the `ai-movie-studio` skill.

## Contents

| File | Covers |
|---|---|
| `AI_Film_Production_Bible_v2_Vol1.md` | Core craft — story, script, directing, cinematography, lighting, composition, colour |
| `AI_Film_Production_Bible_v2_Vol2.md` | Audio — score, sound design, dialogue, voice, mix, master |
| `AI_Film_Production_Bible_v2_Vol3.md` | VFX and effects prompt engineering |
| `AI_Film_Production_Bible_v2_Vol4.md` | Model adapters, quality control, worked productions |

The matching PDFs ship in the source archive but are git-ignored — they duplicate the Markdown.

## Reading order

1. The skill's own modules under `skills/film/ai-movie-studio/references/` — the distilled layer.
   Start here for any actual production task.
2. The relevant volume above — chapter-level depth when a module is insufficient.

Vol1 is ~290 KB. Never load a whole volume into a model context; locate the chapter and read that.

## Platform note

For a Custom GPT or Claude Project, upload the skill's `references/` modules rather than these
volumes. The modules are written to be routed; the volumes are the archive behind them.
