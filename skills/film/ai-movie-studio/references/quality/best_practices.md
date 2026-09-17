# Best Practices — Hollywood Production Wisdom for AI Filmmaking

## Why These Practices Exist

Every practice in this document exists because a production learned it the hard way. These are not guidelines — they are solutions to problems that will otherwise occur.

---

## Pre-Production Best Practices

### 1. Brief Before Prompting

Never write a prompt without a brief. A brief that can't answer "what does the audience feel at the end of this clip?" is not ready. The prompt will reflect the brief's incompleteness.

**Why:** Prompts written without a brief drift toward visual descriptions of actions rather than cinematic scenes with dramatic purpose. The result is technically competent but emotionally empty.

---

### 2. Lock Assets First

Character bibles and environment bibles before any generation. The asset documents are not prep — they are the source of truth.

**Why:** Every generation without locked assets requires the model to infer details it should be told. Inference produces drift. Drift compounds across clips.

---

### 3. Generate the Master Shot First

In any scene, generate the establishing/master shot before generating close-ups or coverage. The master establishes the geography, lighting direction, and tone. Coverage shots are generated in that context.

**Why:** Close-ups generated independently of the master have no spatial context. They're likely to have lighting that conflicts with the master, positioning that breaks the 180-degree rule, and environments that don't match.

---

### 4. Reference Images Are Worth Ten Times the Text

The most detailed text description of a character is less reliable than a clear reference image. For identity-critical characters, invest time in creating good reference sheets.

**Why:** Text description must be interpreted. A reference image is directly observed by the model. The result is consistently more stable when an image anchor is present.

---

## Production Best Practices

### 5. The One-Action Rule

Each 15–30 second clip has one main action, executed cleanly, followed by a held hero frame. Not two actions. Not a sequence of actions.

**Why:** Models that must track multiple simultaneous actions produce temporal instability — the actions compete for model attention across frames. One action produces consistent, holdable execution.

---

### 6. Match the Camera to the Emotion

The camera is not neutral. Every choice of shot size and movement is an emotional statement. Before specifying camera, state the emotion of the shot. Then choose the camera approach that serves it.

**Why:** Camera choices made without emotional intent produce technically correct shots that fail to communicate. The audience reads emotion first, not technique.

---

### 7. State the Light Source Before the Light Quality

"Warm golden key light" tells the model a quality. "The late afternoon sun from the window on the left side of the frame" tells the model a source and direction. Source-first lighting is more reliable.

**Why:** Light quality without a source produces light that changes between frames because the model has no anchor for where it comes from. Motivated light is stable because its direction is fixed.

---

### 8. Specify Physics Explicitly

Never assume the model will infer correct physics for cloth, hair, fire, water, or particles. State it.

**Why:** Physics inference produces high variance. Explicit physics direction reduces frame-to-frame inconsistency.

---

### 9. Debug One Variable at a Time

When a generation fails, change one element and retry. Never rewrite the complete prompt.

**Why:** Changing multiple variables simultaneously makes it impossible to identify the cause of failure. You'll generate something acceptable by accident without knowing what fixed it — making the next failure equally mysterious.

---

### 10. Document Every Generation

Log every clip with its prompt version, the result, and what (if anything) needed to change. The log becomes the production's institutional memory.

**Why:** Productions that don't log end up regenerating clips they already have, or lose track of what settings produced their best results. The log turns individual successes into repeatable processes.

---

## Post-Production Best Practices

### 11. Assemble in Story Order

When cutting clips together, assemble in story order even for the rough cut. Cutting non-linearly in a first assembly makes continuity errors invisible.

**Why:** Story-order assembly immediately reveals continuity breaks, pacing problems, and story clarity issues.

---

### 12. Color Grade After Assembly

Don't finalize grade on individual clips. Grade on the assembled sequence.

**Why:** Clips graded individually can match a reference but still not match each other. Grading on the assembled cut allows comparison of adjacent clips and ensures the grade serves the story across its full arc.

---

### 13. Audio Mix After Picture Lock

Don't finalize audio mix until the cut is locked. Audio is rebuilt from scratch when picture changes; every premature mix pass is wasted effort.

**Why:** Efficiency and sanity preservation.

---

### 14. The Director's Final Check

The last review before delivery is a director's review — watching the complete film from start to end, with the only question being: "Does this tell the story? Does the audience feel what we intended?"

Technical correctness is a prerequisite. Emotional correctness is the standard.

**Why:** Technical reviews catch errors. The director's review asks whether the film works as a film. These are different questions, and both need to be asked.

---

## The Production Golden Rules

> 1. Invest in pre-production. Every hour spent on briefs, bibles, and reference sheets saves three hours in generation.

> 2. One action per clip. Complexity compounds failure.

> 3. State the source of every light. Motivated light is stable light.

> 4. Paste identity tokens verbatim, always.

> 5. Debug one variable at a time.

> 6. Log everything. The log becomes the studio's institutional memory.

> 7. The test is always: does the audience feel what we intended?
