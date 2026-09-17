# Directing — Shot Purpose, Scene Coverage & Performance Direction

## The Director's Job

The director makes one decision per shot: what should the audience feel, and what is the most efficient, emotionally honest way to make them feel it? Every creative decision downstream — camera, light, performance, sound — executes that single decision.

---

## Scene Coverage

Coverage is the set of shots that gives the editor enough to assemble the scene. For AI generation, design coverage before generating — then generate in order.

### Standard Coverage Pattern

| Shot | Purpose |
|---|---|
| Establishing / master shot | Orient the audience. Show where everyone is and what the space looks like. |
| Medium two-shot | Show the relationship between the two primary characters. |
| Over-the-shoulder (character A) | Character B's dialogue from character A's position. |
| Over-the-shoulder (character B) | Character A's dialogue from character B's position. |
| CU (character A) | The emotional reaction — the internal state revealed. |
| CU (character B) | The response reaction. |
| Insert shot (if needed) | Any object or detail that carries story significance. |
| Final hero shot | The image that closes the scene. Designed deliberately. |

**Generation rule:** Generate in coverage order. Master first. Never generate a CU before a master — the model has no spatial context for the CU without the master establishing the space.

---

## Coverage by Scene Type

### Combat / Action Scene

```
1. Establishing wide — geography of the space, forces visible
2. Medium — protagonist's immediate environment, threat established
3. POV — what they see, urgency of perspective
4. Handheld medium — chaos, the protagonist in action
5. CU reaction — decision made in heat
6. Wide aftermath — what remains
```

### Interrogation / Confrontation Scene

```
1. Master two-shot — both characters, equal or unequal power
2. OTS on interrogator — questioning from position of power
3. OTS on subject — response, resistance or surrender
4. CU interrogator — reading the subject, thinking
5. CU subject — fear, defiance, calculation
6. Insert — any object significant to the scene
7. Static hold — silence. Let the scene breathe.
```

### Action Chase Scene

```
1. Establishing — who is running, from what, through what environment
2. POV forward — urgency, we are the runner
3. Tracking medium — runner vs pursuer, relative position
4. Low angle wide — legs pounding, speed as physical fact
5. Over-the-shoulder backward — the threat gaining / falling behind
6. CU face — fear, determination, exhaustion
7. Resolution shot — escape or capture
```

---

## Blocking

Blocking is where characters stand, move, and relate to each other spatially. For AI generation, describe blocking in the prompt explicitly.

**Blocking communicates power:**
- **Character standing, other sitting:** power differential — standing character has control
- **Character at frame edge:** marginalized, pressed, threatened
- **Character center frame, facing camera:** authority, confrontation, declaration
- **Characters back to back:** disconnection, unresolved conflict
- **Characters moving toward each other:** convergence, resolution, confrontation
- **One character moving away:** abandonment, retreat, leaving

**Depth blocking:** Place characters at different depths to create visual interest and suggest relationship:
```
Foreground: the one we most identify with
Midground: the one they're dealing with
Background: the world watching
```

---

## Performance Direction

When directing AI-generated performance, describe the **internal state that causes the external behavior** — not the behavior itself.

### The Performance Formula

```
[Internal state] → [Physical manifestation] → [Specific behavior]
```

**Bad direction:** "He looks scared."
**Good direction:** "He's realizing there's no way out. His hands haven't moved in ten seconds. His eyes check the door. Check the window. Back to the threat. Calculating odds that keep getting worse."

### Key Performance Descriptors

| Internal State | Physical Expression |
|---|---|
| Fear | Shallow breathing, stillness, small movements, averted gaze, pale |
| Rage | Jaw set, stiff posture, controlled voice (or exploding), hands fisted or too still |
| Grief | Collapsed posture, empty eyes, breath uneven, weight of the world |
| Determination | Square posture, forward lean, steady eye contact, deliberate movement |
| Deception | Slightly elevated speech rate, over-explanation, hands still (controlled) |
| Love | Relaxed posture, face soft, small unconscious lean toward the other person |
| Exhaustion | Posture collapsed, movement economized, eyes heavy, voice flattened |
| Shame | Head down, shoulders curved inward, eyes on floor or ground |

---

## Facial Expressions — Reference Table

| Expression | Microexpression detail |
|---|---|
| Genuine joy | Eyes crinkle (Duchenne smile), cheeks raised |
| Fake smile | Mouth moves, eyes do not crinkle |
| Sadness | Inner brows raised and pulled together, mouth corners down |
| Anger | Brows lowered and drawn together, lips pressed or flared |
| Fear | Brows raised and drawn together, eyes wide, lips stretched horizontally |
| Disgust | Upper lip raised, nose wrinkled |
| Surprise | Brows raised, eyes wide, jaw drops slightly |
| Contempt | One-sided lip raise (unilateral smirk) |
| Calculation | Eyes narrow slightly, head tilts, mouth neutral |

**Prompt application:** Specify the microexpression, not just the label.

```
BAD: "She looks afraid."
GOOD: "Brows raised and pulled together, eyes wide, breath held, slight horizontal pull at the lip corners."
```

---

## Eye Direction in Performance

The eyes tell the story before the mouth does. Direct eye behavior precisely.

| Eye Behavior | Meaning |
|---|---|
| Direct, sustained eye contact | Confidence, challenge, intimacy, confrontation |
| Looking away — upward | Accessing memory, constructing an image |
| Looking away — downward | Shame, submission, accessing internal state |
| Rapid eye movement | Calculation, fear, threat assessment |
| Eyes narrow | Suspicion, concentration, anger building |
| Eyes widen | Surprise, fear, love revealed |
| Eyes still, mouth moving | Deception or suppression of emotion |
| Eyes moving, body still | High alert — taking stock before acting |

---

## Directing Crowd / Background Action

Background acting creates world texture. It is not random — it is directed with the same intention as the foreground.

**Rules:**
- Background characters never acknowledge the camera
- Their action should reinforce the scene's emotional register — a despondent crowd makes the scene feel heavier; an indifferent crowd makes the protagonist more isolated
- Scale and staging: background action small, foreground action full — no competing focal points
- Period accuracy: wardrobe, movement, technology consistent with the world

**Prompt phrase for crowd:** `background crowd [activity], paying no attention to camera, [density — sparse/medium/dense], [emotional register — indifferent/tense/celebratory]`

---

## The Hero Shot

The hero shot is the single most important composition in the film. It is designed first, not discovered.

**Properties of a great hero shot:**
- Subject compositionally dominant — low angle, center, or rule-of-thirds with clear space
- Lighting separates them from environment — rim or backlight
- Background suggests scale or context
- Expression or posture is definitive — this is who this character is
- The frame is complete — remove any element and something is lost

**Prompt phrase:** `hero shot, [character] [posture/expression], low angle, [lighting setup], [background context], definitive composition`

---

## Director's Scene Checklist

Before generating any scene:

```
[ ] I know the dramatic purpose of this scene — why it exists
[ ] I know what the audience must feel by the end of it
[ ] Coverage sequence designed — master through CU
[ ] Blocking described — character positions and spatial relationships
[ ] Performance notes written — internal state, not labels
[ ] Eyeline respected or deliberately broken
[ ] Final hero shot designed deliberately
[ ] Dominant emotion consistent across all departments
```

---

## Golden Rule

> Direct the cause, not the effect. Describe what the character is feeling and why, and let the behavior follow from it. Label-directing ("he looks sad") gives the model nothing to work with. State-directing gives it everything.
