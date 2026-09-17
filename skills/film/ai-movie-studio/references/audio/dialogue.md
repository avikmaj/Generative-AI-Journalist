# Dialogue — ADR, Voice Direction & Delivery

## Dialogue Is Action

Characters in dialogue are not exchanging information — they are pursuing objectives, defending themselves, trying to get what they want. Every line is an attempt to do something to the other person.

---

## ADR (Automated Dialogue Replacement)

ADR is the process of re-recording dialogue in post when the original recording is unusable (poor location audio, noise, performance improvement). For AI generation, ADR principles guide how to specify clean, controllable dialogue delivery.

### ADR direction rules:
- Match the emotional state of the original performance
- Match the mouth rhythm and breath pattern
- Specify the acoustic environment the voice should occupy: intimate close-up acoustics (no room), medium room interior, or exterior (open acoustic, no reverb buildup)

**Prompt phrase for ADR-style clean dialogue:**
`voice recording, close and intimate, no room reverb, clean and direct, matches on-screen mouth movement, [emotional state]`

---

## Voice Direction Vocabulary

Direction for vocal performance. State the internal condition, not the sonic result.

| Delivery Direction | What it produces |
|---|---|
| "Holding back — just barely" | Voice controlled, audibly effortful, slight roughness at edges |
| "The decision has already been made" | Calm, even, low, no wavering — the most dangerous delivery |
| "Trying to keep it together" | Starts controlled, slight breaks in rhythm, breath not quite right |
| "She's done — completely" | Flat, quiet, drained of colour — not angry, past angry |
| "He knows it's a lie but says it anyway" | Too smooth, too measured, fractionally over-controlled |
| "The last thing he will ever say" | Weight on every word, deliberate, not melodramatic |
| "Terror she cannot show" | Surface calm, voice slightly too high, pace slightly too fast |

---

## Dialogue Scene Types

### The Information Scene

Characters exchanging plot-critical information. Risk: becomes dry exposition.

**Direction:** Bury the information inside conflict. The information is delivered between people who want different things. The scene is not about the information — it is about what the information means for each character.

### The Confession Scene

A character reveals something they have been keeping. Highest emotional stakes.

**Direction:** The build before the confession is as important as the confession itself. The character attempts deflection, then partial admission, then the full truth. The pause before the truth is the scene's most important moment.

**Prompt phrase:** `dialogue, confessional register — building from resistance to admission, breath irregular, eye contact breaks and returns, truth arriving`

### The Threat Scene

Danger communicated without direct statement. Subtext is the entire scene.

**Direction:** The threat is never stated directly. The power of the scene is in what isn't said. The threatened character understands perfectly.

**Prompt phrase:** `dialogue, threat subtext — surface words are ordinary, underlying meaning is clear danger, delivery controlled and quiet`

### The Argument Scene

Two characters in direct conflict. Energy, escalation, potential violence.

**Direction:** Arguments have structure: opening position → challenge → escalation → peak → aftermath. Design each stage. Arguments that immediately start at maximum volume have nowhere to go.

### The Farewell Scene

A character is leaving — permanently or temporarily. Possibly the last conversation.

**Direction:** What isn't said is the scene. Both characters know things they won't say. The subtext is the grief or relief or love that has no language.

---

## Pause Architecture

Pauses are not empty space — they are the scene breathing.

| Pause type | Duration | Meaning |
|---|---|---|
| Beat pause | Half a second | Processing, transition, deciding |
| Emotional pause | 1–3 seconds | Something has landed and must be absorbed |
| Deliberate pause (power) | 3–5 seconds | The person who waits controls the room |
| Agonized silence | 5+ seconds | Something that has no words |

**Prompt phrase:** `[character] pauses — [duration] — before responding, [what the pause contains]`

---

## Lip Sync Rules

Lip sync is technically demanding and fails on shots where:
- The face is not visible or partially obscured
- The shot contains cuts during the line
- The character is not in a close or medium-close framing
- The line is longer than the held shot

**Safe lip sync:** Held CU or MCU, single subject, single continuous shot, line under 10 seconds.

**Prompt phrase for lip sync:** `held close-up, no camera movement, face fully visible, lip sync to dialogue — [exact line]`

---

## Dialogue Prompt Template

```
DIALOGUE:
  Speaker:       [Character name, descriptor]
  Emotional state: [What they're experiencing internally — not the expression, the cause]
  Objective:     [What they want from this conversation]
  Delivery:      [specific vocal description — see above]
  Exact line:    ["Quote here."]
  Pause note:    [if a pause is built into the delivery]
  Reaction:      [character listening — what does their face do while they hear this?]
```

---

## Golden Rule

> Every line of dialogue is an action. Before writing it, name what the character is doing: threatening, seducing, confessing, deflecting, accusing, comforting. The action determines the delivery.
