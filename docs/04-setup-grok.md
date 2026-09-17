# Setting up the Grok project

Grok is the third target. It has no native skills mechanism and the tightest instruction budget of
the three, so its bundle is the most compressed: one consolidated knowledge file per family rather
than one per skill.

## 1. Build the bundle

```bash
python3 scripts/validate_skills.py
python3 scripts/build_grok_bundle.py
```

This writes `dist/grok/`:

| File | Purpose |
|---|---|
| `project-instructions.md` | Paste into the project instructions. Ends with a generated router. |
| `GROK_KNOWLEDGE_DV.md` | Both DV skills, flattened, with reference modules inlined |
| `GROK_KNOWLEDGE_GENAI.md` | All 10 genai skills |
| `GROK_KNOWLEDGE_BUSINESS.md` | The business-management skill and its references |
| `GROK_KNOWLEDGE_FILM.md` | The ai-movie-studio skill and its 60 modules |
| `dv-vip-factory-team-rules.md` | The governing VIP rules, kept standalone on purpose |
| `MODEL_CARD.md` | The canonical behavioural definition |
| `PROMPTS.md` | The consolidated prompt library |
| `MANIFEST.md` | What to upload, with file sizes |

## 2. Create the project

1. Create a new Grok project named `Generative AI Journalist`.
2. Paste the whole of `dist/grok/project-instructions.md` into the project instructions.
3. Upload every other file from `dist/grok/` except `MANIFEST.md`.

Upload `dv-vip-factory-team-rules.md` as its own file. It is the governing document for VIP work and
must be citable on its own; buried inside a family file it stops being quotable as authority.

## 3. Verify the routing

Run these three probes. They are the cheapest way to catch a broken upload.

| Probe | Expected |
|---|---|
| "My agent isn't seeing transactions on the analysis port." | `[DV]`, opens the DV knowledge file, talks about the monitor and `connect_phase` |
| "My agent loops forever calling the same tool." | `[GENAI]`, talks about termination conditions — **not** UVM |
| "Kick off a new I3C target VIP at L2." | `[DV]`, runs Gate 0, derives `FR-###` from spec, does **not** say the protocol is unsupported |

If the first two both answer in the same family, the router did not load — re-check that the
instructions were pasted in full, including the generated router at the end.

## Known differences from Claude

| Behaviour | Consequence for Grok |
|---|---|
| No native skills | The router is inlined in the instructions, so it must be pasted whole |
| No nested file references | Reference modules appear as `## Reference: <path>` sections inside the family files |
| Tighter instruction budget | The instruction block is the compressed variant; do not paste the Claude version |
| Aggressive live search | Rule 3 matters more here: if it browses, it must cite what it read, not fall back to recall |

The full comparison is in [07-platform-parity.md](07-platform-parity.md).

## Re-uploading after a change

Grok does not diff uploads. After any change to `model/` or `skills/`, re-run the builder and replace
the affected family file wholesale. Bump `model/VERSION` and note it in [CHANGELOG.md](CHANGELOG.md)
so you can tell which project has which build.
