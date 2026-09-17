# Production kickoff

Expected skill: `ai-movie-studio`. Expected mode: `[FILM]`.

```text
Start a production.

Logline: <ONE SENTENCE>
Format and length: <SHORT / SERIES EPISODE / FEATURE; RUNTIME>
Language and audience: <LANGUAGE, PLATFORM, AUDIENCE>
Tools available: <IMAGE, VIDEO, VOICE, MUSIC TOOLS>
Hard constraints: <BUDGET, DEADLINE, CONTENT LIMITS>

Return, in production order:
1. The treatment, then the beat sheet. Do not skip to shots.
2. The character and location bibles, with the continuity anchors that must stay fixed across shots.
3. The shotlist, each shot carrying its prompt, duration, and the continuity anchors it inherits.
4. The audio plan: dialogue, voice casting, music, sound design.
5. The QC gate: what would make a shot a reshoot rather than a fix in post.

Name the tool you assume for each generated asset, and label any model capability claim UNVERIFIED.
Do not describe a shot the named tool cannot produce.
```

## Why it is shaped this way

Continuity is the failure mode of AI film work, and it is decided in the bibles, before the shotlist.
Ordering the deliverable this way makes drift a process error rather than a surprise in the edit.
