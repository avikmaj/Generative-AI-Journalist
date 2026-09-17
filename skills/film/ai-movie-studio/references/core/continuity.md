# Continuity — Consistency Across Shots & Scenes

## Continuity Is the Contract

Continuity is the implicit agreement with the audience: the world of the film is real and internally consistent. Every continuity break reminds the audience they are watching a constructed thing. Maintain it absolutely.

---

## Categories of Continuity

### Character Continuity

Everything about a character's appearance is locked from the moment they are introduced.

| Element | What to hold |
|---|---|
| Face | Identity token verbatim — face, hair colour, eye colour, age appearance |
| Hair | Length, style, any specific details (part, loose, tied) |
| Wardrobe | Every garment — colour, material, specific details (collar type, button count) |
| Accessories | Rings, watches, scars, tattoos |
| Injury progression | A wound acquired in scene 2 is still present in scene 3 |
| Emotional state | A character who is devastated in scene 4 does not arrive fresh in scene 5 |

**Lock format:**
```
CHARACTER CONTINUITY LOCK — [Name]:
Face: [exact description]
Hair: [state at start of sequence]
Wardrobe: [complete outfit with materials and colours]
Injuries: [any damage sustained — location, severity, appearance]
Emotional state carry: [what they're carrying from previous scene]
```

---

### Environmental Continuity

The world must be internally consistent.

| Element | Rule |
|---|---|
| Time of day | If scene starts at golden hour, it cannot end at midday without a time cut |
| Weather | Rain in shot 1, sunshine in shot 2 = continuity break |
| Prop placement | An object placed on a table in shot 1 is in the same position in shot 5 |
| Background elements | Extras, vehicles, structures in consistent positions |
| Lighting direction | If sun is from the left in master, it's from the left in CU |
| Shadow angles | Consistent with named time of day and lighting direction |

---

### Lighting Continuity

Lighting must be motivated by a consistent source across all shots in a scene.

**Rule:** Define the scene's dominant light source in the master. Hold it through every subsequent shot.

```
SCENE LIGHT LOCK:
Source: [the primary motivated light source]
Direction: [which side of frame]
Quality: [hard/soft, diffused/direct]
Colour temperature: [K value or description]
Secondary sources: [any practicals, their position and colour]
```

---

### Audio Continuity

Sound cannot jump between shots within a scene.

| Element | Rule |
|---|---|
| Room tone | The ambient sound of the space is consistent |
| Weather audio | Rain on glass in shot 1, rain on glass in shot 4 |
| Off-screen sounds | Sounds established as present (traffic, crowd) stay present |
| Music | Score cue should not begin and end randomly mid-scene |
| Reverb match | Interior reverb in CU matches the interior reverb in the master |

---

## The 180-Degree Rule

In any scene with two characters, establish an axis (the line between them). Keep the camera on one side of that axis through the entire scene.

Breaking the 180-degree rule causes spatial disorientation — the audience loses track of who is where.

**Exception:** Cross the line deliberately as a story device (the world changing, disorientation intentional) — but only with a motivated reason.

**Prompt phrase note:** Specify camera side consistently:
- "Camera on [A]'s side of the axis — [A] looks right, [B] looks left"
- Never: "[A] looks right" in shot 2, "[A] looks right" in shot 4 when camera crossed the line in shot 3

---

## The 30-Degree Rule

When cutting between two shots of the same subject, the camera must move at least 30 degrees between positions. Less than 30 degrees produces a jump cut — an uncomfortable, disorienting stutter.

**In AI generation:** Between generating similar coverage shots, specify enough angular change to avoid jump-cut reads.

---

## Match Cut

Cutting from one shot to another where a visual element — shape, movement, position — carries across the cut.

**Types:**
- **Action match:** Character begins movement in shot A, completes it in shot B
- **Eyeline match:** Character looks at X in shot A, shot B shows X
- **Shape match:** A circle in shot A becomes a different circle in shot B (planet → eye → coin)
- **Movement match:** Movement direction and speed holds across the cut

**Prompt phrase:** `shot ends on [specific action/position] — designed to match-cut to next shot's opening [specific action/position]`

---

## Jump Cut

Cutting between two shots of the same subject at an angle less than 30 degrees, creating a jolt.

**When to use intentionally:** Disorientation, time compression, psychological fracture, montage energy.

**Prompt phrase (intentional):** `deliberately discontinuous cut, jump-cut rhythm, [time compressed/psychological fracture]`

---

## Continuity Checklist (per shot in a sequence)

Before generating each shot in a sequence:

```
CONTINUITY HOLD:
[ ] Character identity token matches previous shots in sequence
[ ] Wardrobe unchanged (or changed with story justification)
[ ] Injuries consistent with what has happened
[ ] Lighting source and direction match master
[ ] Time of day holds (or a time-lapse/cut has been established)
[ ] Weather consistent with previous shots
[ ] Key props in same position
[ ] Camera side of 180-degree axis correct
[ ] Room tone and ambient audio consistent
[ ] Emotional state carries from previous scene
```

---

## Error Catalogue

Common continuity failures in AI generation and how to prevent them:

| Error | Prevention |
|---|---|
| Face drift | Paste identity token verbatim in every block — never summarize it |
| Hair length changes | Specify hair state in every block ("hair loose at shoulders, slight wind-movement") |
| Wardrobe swap | Name every garment with colour and material in every block |
| Lighting flip | Name the dominant source and its screen direction in every block |
| Weather inconsistency | Name weather condition in every block ("rain continuous, wet surfaces, overcast") |
| Prop disappears | Name props in every block where they should be present |
| Shadow direction flip | Name sun/key position relative to frame in every block |
| Injury vanishes | Name injuries explicitly in character state within every subsequent block |
| Scale mismatch | Establish reference size in master, note scale relationship in close shots |
| Perspective break | Maintain named camera position relative to spatial axis |

---

## Series-Level Continuity

For multi-episode or multi-clip productions:

Maintain a continuity log:

```
EPISODE / CLIP NUMBER:
Characters present:
  [Name]: [state at end of clip — wardrobe, injuries, emotional state]
Locations visited:
  [Location]: [conditions established — time, weather, lighting]
Story state:
  [What has happened that must carry forward]
Props introduced or consumed:
  [Object]: [its status at clip end]
Open story threads:
  [What remains unresolved]
```

Begin each new clip by consulting this log and loading the held state.

---

## Golden Rule

> An audience can forgive a plot hole they don't notice. They cannot forgive a blue shirt in shot 1 that becomes red in shot 3. Continuity breaks are the most visible failures in a production. Hold every detail.
