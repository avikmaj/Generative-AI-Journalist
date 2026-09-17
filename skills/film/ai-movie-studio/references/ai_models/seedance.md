# Seedance — ByteDance Video Generation

## Model Profile

| Property | Value |
|---|---|
| Developer | ByteDance |
| Strength | Reference image workflow, Omni reference, high quality |
| Clip length | Up to 15 seconds |
| Reference image | Required in Omni workflow |
| Platform access | Via CapCut / Dreamina |

---

## Omni Reference Workflow

Seedance's primary strength is the Omni Reference system. Multiple reference images provided simultaneously to lock character, environment, and style.

```
Reference image inputs:
  @character_sheet  -- face/body/wardrobe reference
  @environment_ref  -- world/location reference
  @style_ref        -- grade/tone/look reference
  @storyboard       -- composition reference (optional)
```

**Critical note:** Seedance scans reference images for real photoreal faces before reading the prompt. Keep references stylized/original. Never use photographs of real people as reference.

---

## Prompt Approach

Six-dimension block structure from skill.md maps directly to Seedance processing:

```
[Tone] [Style/Grade] [Character identity + action] [Composition] [Lighting] [Camera]
Then: VFX . SFX . Dialogue . Text
```

---

## Fallback

If Seedance/CapCut is unavailable: Dreamina (dreamina.capcut.com) runs the same Seedance 2.0 model with identical Omni Reference workflow.
