# Consistency — Holding Character, World & Style Across a Production

## Consistency Is the Mark of Craft

A film that looks like it was made by ten different crews is a film whose audience cannot fully commit to its world. Consistency — of character, environment, style, lighting, and audio — is what makes a film feel like a single cohesive object.

---

## The Three Levels of Consistency

### Level 1 — Shot-to-Shot Consistency

Within a scene, consecutive shots must match:
- Lighting direction and quality
- Character position relative to the 180-degree axis
- Wardrobe detail
- Environmental conditions

This is the most critical level. See `../core/continuity.md` for the full rule set.

---

### Level 2 — Scene-to-Scene Consistency

Between scenes in the same act:
- Character injuries and physical state carry forward
- Time of day is consistent with story time
- Emotional state of characters at the end of one scene connects to their state at the start of the next
- The world's established rules remain constant

---

### Level 3 — Film-Wide Consistency

Across the entire film:
- Visual style and grade remain within the defined family
- Score character remains consistent
- Character arcs develop without contradiction
- World rules never change without a story reason

---

## Consistency Maintenance System

### The State Log

After generating each scene, record the current state:

```
AFTER SCENE [X] — STATE LOG:
  [Character A]: [wardrobe, physical state, emotional state, location]
  [Character B]: [same]
  [Location status]: [any changes to the environment — damage / time of day change]
  [Open story threads]: [what remains unresolved going into the next scene]
  [Objects of significance]: [where they are, who has them]
```

Consult this log before generating the next scene.

---

### The Continuity Board

A tracking document per character:

```
[CHARACTER NAME] — CONTINUITY BOARD

Scene | Wardrobe | Injuries | Emotional state | Location
------|----------|----------|----------------|----------
  1   |          |  none    |                |
  2   |          |  none    |                |
  3   |          | [acquired]|               |
  4   |          | [present] |               |
```

Update after each scene. Reference before generating.

---

## Common Consistency Failures and Prevention

### Character Identity Drift

**Symptom:** The character looks subtly different between scenes — same hairstyle, slightly different face; same wardrobe but a colour is off.

**Prevention:** 
- Paste the full identity token verbatim — never paraphrase or summarize
- Include a character reference image in every clip
- Add "identity matching [ref image], [character name] held across all shots" explicitly

### Lighting Continuity Break

**Symptom:** The key light appears to come from the left in the master shot and from the right in the close-up.

**Prevention:**
- State the key light direction in every prompt: "key light from screen-left"
- Specify the colour temperature in every prompt: "2800K warm"
- Specify shadow direction: "shadows falling to screen-right"

### Wardrobe Change

**Symptom:** A garment changes colour, or a piece disappears between shots.

**Prevention:**
- Name every garment with specific colour and material — not "blue jacket" but "navy wool peacoat, double-breasted, dark buttons"
- Use a character sheet reference image

### Physics Inconsistency

**Symptom:** The character's coat blows left in one shot and right in the next within the same exterior scene.

**Prevention:**
- Name the wind direction: "wind from screen-left, light and constant"
- Hold the weather description: "light overcast, still air" or "windy — wind from north (screen-left)"

---

## The Consistency Audit

Before assembling the final film, audit every clip for:

```
CONSISTENCY AUDIT:
[ ] All clips reviewed in sequence
[ ] Character identity consistent across all appearances
[ ] Lighting direction consistent within each scene
[ ] Continuity state carried across scene boundaries
[ ] World rules maintained throughout
[ ] Grade consistent with the film's style guide
[ ] Score character consistent with the film's sound identity
```

---

## Golden Rule

> The audience never notices perfect consistency. They only notice when it breaks. Build the systems that prevent the break.
