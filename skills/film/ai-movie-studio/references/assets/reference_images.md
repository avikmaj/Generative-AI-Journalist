# Reference Images — Management, Naming & Application

## Reference Images Are the Identity Anchor

In AI video generation, especially with reference-image-driven workflows (Seedance Omni, Kling, Runway Gen-4), the reference image does more than describe — it locks. The text prompt tells the model what to do; the reference image tells it who to do it as and where to do it.

---

## Reference Image Types

### Character Sheet

The most critical reference type. Shows the character from multiple angles with consistent identity.

**Required views:**
- Front facing, neutral expression
- Side profile (left or right)
- Three-quarter angle
- Close-up of face, neutral
- Expression variants (3–4 key expressions)

**Naming:** `[character_name]_ref_sheet_v[version].png`

### Environment Reference

Establishes the visual character of a location.

**Required elements:**
- The space from an establishing angle
- Key lighting condition (the standard time of day for this location)
- Key surfaces and materials visible

**Naming:** `[location_name]_env_ref_v[version].png`

### Style Reference

Locks the visual grade and aesthetic look of the production.

**Required elements:**
- Sample frame(s) that show the intended grade
- Light quality
- Colour palette
- NOT a reference to another film's specific imagery — create original style references

**Naming:** `[film_title]_style_ref_v[version].png`

### Storyboard Reference

Sequential frame compositions for a scene, used to lock shot design.

**Naming:** `[scene_number]_[shot_number]_board.png`

---

## Reference Image Management

```
REFERENCE LIBRARY STRUCTURE:
references/
  characters/
    [character_name]/
      [character_name]_ref_sheet_v1.png
      [character_name]_expression_set_v1.png
  environments/
    [location_name]/
      [location_name]_env_standard_v1.png
      [location_name]_env_night_v1.png
  style/
    [film_title]_style_ref_v1.png
  storyboards/
    scene_[XX]/
      scene_[XX]_shot_[YY]_board.png
```

---

## Reference Image Application in Prompts

### Seedance / CapCut Omni Workflow

Before every clip block, declare the reference images:

```
REF IMAGES: @character_sheet + @environment_ref + @style_ref
```

All three default references for any clip with a recurring character in an established location.

Add as needed:
- `@storyboard` — when a specific composition must match a pre-designed frame
- `@prop_ref` — when a specific object must maintain design consistency

### Model-Specific Application

| Model | Reference image use |
|---|---|
| Seedance (Omni) | Required — primary identity anchor |
| Kling | Strong — attach character ref for face lock |
| Runway Gen-4 | Supported — character reference locking |
| Sora | Via image-to-video when available |
| Veo | Via API image conditioning |

---

## Reference Image Quality Standards

For character sheets to work effectively:

- **Resolution:** Minimum 1024x1024
- **Background:** Neutral (white / grey) — no environmental context that might compete
- **Lighting:** Even, flat, front-lit — character feature clarity is the priority
- **Style:** Consistent with the film's visual style, but optimized for identity clarity
- **Real faces:** NEVER use photographs of real people as character references — use original created or AI-generated characters

---

## Version Control

When a character changes significantly (wardrobe change, injury, time skip):

```
v1: [character_name] — starting state
v2: [character_name] — after [story event that changed them]
```

Always reference the correct version for the production stage.

---

## Golden Rule

> A great reference image does more work than 1,000 words of identity description. Invest in creating proper reference sheets before production begins. They are the most valuable asset in the library.
