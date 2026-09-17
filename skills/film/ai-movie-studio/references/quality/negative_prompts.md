# Negative Prompts — Comprehensive Failure Prevention

## Negative Prompts Are Guardrails

Negative prompts tell the model what to exclude. They are not a substitute for a well-constructed positive prompt — they are a backstop against predictable failure modes. Write the positive prompt first. Add negative prompts for known model failure patterns.

---

## Universal Negative Prompt (Apply to All Generations)

```
NEGATIVE: 
low quality, blurry, out of focus, artifacts, watermark, logo, text overlay, 
extra limbs, duplicate body parts, wrong anatomy, missing fingers, extra fingers, 
fused fingers, malformed hands, distorted face, face asymmetry, multiple faces, 
floating objects, broken physics, wrong shadows, inconsistent lighting direction, 
temporal flickering, frame inconsistency, visual noise, jpeg artifacts, 
compression artifacts, overexposed, underexposed, flat lighting, amateur composition
```

---

## Character-Specific Negative Prompts

### Human Characters (General)

```
NEGATIVE (character):
wrong number of fingers, extra fingers, fused fingers, claw-like hands, 
deformed hands, extra limbs, missing limbs, floating limbs, 
face distortion, asymmetrical face, multiple faces, melted features, 
body proportion errors, scale inconsistency between body parts,
wardrobe inconsistency [if a specific issue has been observed], 
hair growing from wrong location, disconnected hair
```

### Face / Identity Drift

```
NEGATIVE (face/identity):
face changing between frames, identity drift, different person, 
age inconsistency, feature morphing, unintended transformation,
wrong eye colour, wrong hair colour, wrong hair length
```

---

## Environment Negative Prompts

```
NEGATIVE (environment):
wrong time of day, lighting inconsistent with established [day/night], 
objects floating without support, physics violation, 
scale inconsistency of environmental elements, 
horizon at wrong angle, perspective errors, 
impossible architectural configurations, broken geometry
```

---

## Camera and Composition Negatives

```
NEGATIVE (camera):
dutch angle when not intended, fisheye distortion, 
extreme lens distortion not requested, vignette not requested,
over-sharpened, HDR tonemapping, Instagram filter look, 
wrong aspect ratio, letter-boxing when not intended
```

---

## Physics Negatives

```
NEGATIVE (physics):
cloth floating in wrong direction, hair defying gravity without wind, 
fire burning sideways or upward without wind source, 
water flowing uphill, objects without shadows, 
smoke going downward, debris floating without force, 
explosion without sequential expansion
```

---

## Audio Negative Notes

For models with audio generation:

```
NEGATIVE (audio):
audio clipping, distorted dialogue, robot voice quality, 
monotone speech with no expression, audio-visual sync errors, 
background music louder than dialogue, 
sound effects at wrong timing relative to visual action, 
echo inappropriate to the stated environment
```

---

## Genre-Specific Negative Prompts

### Action / Combat

```
NEGATIVE (action):
cartoonish violence aesthetics, comic-book impact effects (stars/spirals), 
bloodless impacts when realistic impacts are required, 
wrong physics for weapon impacts, superhero landing poses not requested, 
instant recovery from serious injuries
```

### Horror

```
NEGATIVE (horror):
jump scare cliche execution, cheap-looking monster, 
bright cheerful lighting in horror scenes, 
comedic tone when horror is required, 
threat fully visible in a shot designed for concealment
```

### Fantasy / Mythology

```
NEGATIVE (fantasy):
anachronistic modern elements in historical/fantasy settings, 
wrong cultural architecture mixing, 
magic effects inconsistent with the established magic system,
divine figures shown with modern proportions when mythic scale is required
```

---

## Model-Specific Common Failures

Add to the negative prompt for known issues with specific models:

### General AI Video Failure Modes

```
temporal instability, flickering between frames, identity drift mid-clip,
background element teleportation, disappearing props, 
character scale changing within clip
```

---

## Negative Prompt Application Rule

Negative prompts are cumulative from universal to specific:

```
FINAL NEGATIVE FOR ANY PROMPT:
[Universal negatives] + [Character negatives if character is present] + 
[Environment negatives if complex environment] + [Genre-specific negatives] + 
[Any model-specific known issues]
```

Keep negatives targeted — a negative prompt that is 500 words of "no bad things" adds no value beyond the first 20 targeted exclusions.

---

## Golden Rule

> A positive prompt describes what to create. A negative prompt corrects for what this model tends to create incorrectly when given this type of instruction. Target the actual failure modes.
