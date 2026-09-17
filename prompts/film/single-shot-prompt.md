# Single shot or image prompt

Expected skill: `visual-storytelling-director`. Expected mode: `[FILM]`.

```text
Write the generation prompt for one visual.

What it must show: <SUBJECT AND ACTION>
Where it sits: <STANDALONE, OR THE SHOT BEFORE AND AFTER>
Target tool: <IMAGE OR VIDEO MODEL>
Aspect ratio and duration: <VALUES>
Continuity anchors to preserve: <CHARACTER, WARDROBE, LOCATION, LIGHTING, LENS>

Return:
1. The prompt, paste-ready for the named tool.
2. A negative prompt, if the tool supports one.
3. Two variants: one safer, one more ambitious, and what each trades.
4. What to check in the output before accepting it.

If this is part of a full production, say so and defer the surrounding structure to ai-movie-studio
rather than inventing a shotlist here.
```

## Why it is shaped this way

This is the narrow sibling of `ai-movie-studio`, so the prompt ends by naming the handoff. The
acceptance check matters because generation failures are usually visible only against the neighbouring
shots.
