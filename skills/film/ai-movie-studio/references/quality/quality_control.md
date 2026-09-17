# Quality Control — The Pre-Generation & Post-Generation Checklist

## QC Is Not the Last Step

Quality control happens at three stages:
1. **Before generation** — catching problems in the prompt
2. **After generation** — reviewing what the model produced
3. **Before assembly** — ensuring clips work together as a sequence

---

## Pre-Generation QC Checklist

Run this before submitting any prompt to generation.

```
STORY / INTENT
[ ] Scene has a clear dramatic purpose — I can state it in one sentence
[ ] I know what the audience must feel by the end of this clip
[ ] The dominant emotion is consistent across all departments in this prompt

CHARACTER
[ ] Identity token string is present and verbatim from the character bible
[ ] Wardrobe is complete — no elements left to model inference
[ ] Any injuries from the story timeline are reflected in character state
[ ] Performance note included — internal state, not just expression label

ENVIRONMENT
[ ] Environment is fully established — time, weather, lighting direction
[ ] Environment matches the continuity of surrounding scenes
[ ] Key props in their established positions

CAMERA
[ ] Shot type is specified
[ ] Camera movement is specified and motivated by the scene
[ ] Lens focal length or feel is noted
[ ] Final hero frame is described

LIGHTING
[ ] Key light source named and motivated
[ ] Colour temperature noted
[ ] Shadow quality noted
[ ] Atmosphere / particles noted if applicable

AUDIO (for models with audio generation)
[ ] Ambient sound of location noted
[ ] Key SFX relevant to action noted
[ ] Dialogue / narration marked if applicable
[ ] Music direction noted

TECHNICAL
[ ] Six-dimension order correct: Tone > Style > Identity > Composition > Lighting > Camera
[ ] One-action rule obeyed — single main beat plus hero frame
[ ] Negative prompts added
[ ] Reference images declared

CONTINUITY
[ ] Lighting direction matches established scene master
[ ] Time of day matches surrounding clips
[ ] Character wardrobe matches preceding and following clips
```

---

## Post-Generation QC Checklist

Review every generated clip against these criteria before approving:

```
CHARACTER
[ ] Identity matches the character bible token
[ ] Wardrobe correct
[ ] Injuries present if they should be
[ ] Expression/performance matches the direction

TECHNICAL
[ ] No temporal flickering or instability
[ ] No identity drift within the clip
[ ] Physics behave correctly (cloth, hair, particles, fire, water)
[ ] No floating objects or broken geometry
[ ] Shadows consistent with lighting direction

CINEMATIC
[ ] Shot type matches what was specified
[ ] Camera movement matches what was specified
[ ] Lighting matches what was specified
[ ] Composition is as intended

AUDIO (if generated)
[ ] Ambient matches the environment
[ ] SFX timing matches visual action
[ ] Dialogue intelligible and in sync
[ ] Music level appropriate to other audio

CONTINUITY (in context of surrounding clips)
[ ] Lighting direction will cut with preceding and following clips
[ ] Character state matches continuity
[ ] Environment matches continuity
```

---

## Revision Decision Tree

When a generated clip fails QC:

```
Is the failure in character identity?
  -> Strengthen the identity token. Add more specific detail.
  -> Add negative prompts for the observed drift.
  -> Try again with the same prompt modified.

Is the failure in physics / environment?
  -> Add explicit physics descriptions.
  -> Add specific negative prompts for the observed failure.

Is the failure a camera / composition issue?
  -> Be more specific about shot type and camera movement.
  -> Add composition notes.

Is the failure in performance / emotion?
  -> Rewrite the performance note — state the internal cause of the expression, not the expression itself.

Is the failure in lighting?
  -> Add explicit light source motivation.
  -> Add exact colour temperature.
  -> Specify shadow direction.

Is it a random/transient model failure?
  -> Retry with identical prompt. AI video generation has variance.
  -> If multiple retries fail, modify the most constrained element.
```

---

## Sequence Assembly QC

When assembling clips into a sequence:

```
[ ] Cuts are motivated — each cut has a reason (match cut / action cut / reaction)
[ ] 180-degree rule maintained across cuts
[ ] Lighting direction is consistent across cuts within a scene
[ ] Audio transitions are clean — no jarring audio cuts without purpose
[ ] Pacing is intentional — slow scenes stay slow, fast scenes accelerate correctly
[ ] The final image of each scene is worthy of being the last thing seen in that space
```

---

## QC Score

Rate each clip on a 1–10 scale across categories:

```
Identity:       [1-10]
Environment:    [1-10]
Camera:         [1-10]
Performance:    [1-10]
Continuity:     [1-10]
Technical:      [1-10]

Total:          [6-60]
QC Pass:        [50+ = approve / 40-49 = approve with notes / below 40 = regenerate]
```

---

## Golden Rule

> A clip that fails QC costs less to regenerate now than to fix in assembly later. Hold the standard at the generation stage.
