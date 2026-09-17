# Troubleshooting — Failure Diagnosis & Retry Strategies

## Debugging One Variable at a Time

When a generation fails, the instinct is to rewrite the entire prompt. This is wrong. A complete rewrite changes everything simultaneously, making it impossible to identify which element caused the failure.

**Debug methodology:**
```
OBSERVE → IDENTIFY THE FAILURE CATEGORY → MODIFY ONE VARIABLE → GENERATE → COMPARE → DOCUMENT
```

---

## Failure Categories and Fixes

### F1 — Instant Rejection (Model Refuses Immediately)

**Symptom:** Generation fails in the first 10 seconds or model returns an error.

**Cause:** Content moderation triggered by wording in the prompt.

**Fix:**
1. Identify the phrase that triggered the filter
2. Reword to describe the same intent with different language
3. Focus on outcomes and emotional impact rather than method
4. Use cinematic/professional language ("depicted violence" vs raw descriptions)

---

### F2 — Mid-Generation Stall

**Symptom:** Generation starts, then freezes or returns an error partway through.

**Cause:** Server/connection issue (most common) or generation complexity exceeding model limits.

**Fix:**
1. Retry the identical prompt — server issues are often transient
2. If persistent, try a backup platform or fallback model
3. If complexity-related, simplify the prompt (reduce simultaneous demands)

---

### F3 — Character Identity Drift

**Symptom:** Character looks different from the reference or from previous clips.

**Cause:** Identity token not specific enough, reference image not attached, or model variance on visual details.

**Fix (in order):**
1. Attach the character reference image explicitly
2. Strengthen the identity token — add more unique physical descriptors
3. Add negative prompts: "identity consistent with reference, no face drift"
4. Try the prompt with reference image only (no text) to test base model identity adherence

---

### F4 — Wrong Shot Type / Composition

**Symptom:** The model generated a different shot than specified.

**Cause:** Shot type description was ambiguous or conflicted with subject matter.

**Fix:**
1. Move shot type to the first sentence of the prompt
2. Add composition details: "subject at left third, negative space right, rule of thirds"
3. Add camera position explicitly: "camera at chest height, facing character"

---

### F5 — Physics Failure

**Symptom:** Cloth, hair, fire, water, smoke, or debris behave incorrectly.

**Cause:** Physics behavior was not explicitly stated; model inferred incorrectly.

**Fix:**
1. Add explicit physics direction: "cloth follows body with gravity and inertia"
2. Specify the force: "strong wind from screen-left — hair and fabric driven right"
3. Add negative prompts for the observed failure: "no floating cloth, no reversed wind"

---

### F6 — Lighting Mismatch

**Symptom:** Lighting does not match the direction, quality, or colour temperature specified.

**Cause:** Lighting description too general, or conflicts with the model's inference from scene content.

**Fix:**
1. Name the light source explicitly: "single practical — a bare bulb at ceiling center"
2. State shadow direction: "shadows fall toward camera, to screen-left"
3. State colour temperature: "2700K warm tungsten"
4. Add negative prompt: "no fill light, no bounce from walls"

---

### F7 — Temporal Instability / Flickering

**Symptom:** The clip flickers between frames, elements change between frames.

**Cause:** Model uncertainty about details leading to frame-by-frame variance.

**Fix:**
1. Reduce the number of simultaneously constrained variables
2. Simplify background elements
3. Anchor identity more strongly: add "held stable, temporally consistent" to the prompt
4. Try generating at shorter duration first to test stability

---

### F8 — Audio-Visual Sync Failure

**Symptom:** Dialogue is out of sync with lip movement, or audio doesn't match action.

**Cause:** Lip sync attempted on an invalid shot type, or audio generation mis-timed.

**Fix:**
1. Check if the shot is valid for lip sync (must be held CU with face visible and no camera movement)
2. Remove dialogue from the visual prompt and apply audio separately in editing
3. Use silent generation + added voiceover workflow

---

### F9 — Scale Inconsistency

**Symptom:** Character is the wrong size relative to the environment.

**Cause:** No scale reference established, or environment and character generated with independent scale assumptions.

**Fix:**
1. Add explicit scale reference: "[Character] stands at the base of [environmental feature], [character] reaching only to [point on feature]"
2. Establish a scale anchor in the master shot before generating close shots

---

## The Retry Ladder

When a prompt fails:

```
RETRY 1: Identical prompt — many failures are transient
RETRY 2: Identify failure category (above) — modify ONE element
RETRY 3: Strip to the minimum viable prompt — just identity + action + environment
          Add elements back one by one until failure reappears
RETRY 4: Try on a different model / platform
RETRY 5: Redesign the shot — the failure may indicate a fundamental limit of current models
```

---

## Documentation of Fixes

When a retry succeeds, document what changed:

```
GENERATION LOG:
Clip: [ID]
Initial prompt: [summary of first attempt]
Failure: [what went wrong — category and symptom]
Fix applied: [what was changed]
Result: [approved / needed further iteration]
Lesson: [what this teaches about this model's behavior]
```

---

## Golden Rule

> Never rewrite the whole prompt in response to a specific failure. Change the minimum necessary. The prompt that almost worked is 90% right — find the 10% that was wrong.
