# Cinematic FX — Lens Effects, Bloom, Grain & DOF

## Camera-Native Effects

These effects simulate the physical behavior of camera optics and film stock. They add filmic authenticity and should be calibrated to the visual style of the production.

---

## Depth of Field (DOF)

The range of the frame that is in sharp focus. Everything outside this range is progressively blurred (bokeh).

**Shallow DOF:** Only the subject is sharp. Background melts away.
- Creates: Intimacy, isolation of subject, the subject is all that matters.
- Achieved with: Long lenses (85mm+), wide aperture (f/1.4–f/2.8), close subject distance.

**Deep DOF:** Subject AND background are sharp.
- Creates: Documentary realism, environment as important as subject, nowhere to hide.
- Achieved with: Wide lenses (24mm or less), small aperture (f/8+).

**Prompt phrases:**
- `shallow depth of field, subject sharp, background melts to soft bokeh, 85mm aperture wide`
- `deep focus, subject and full background in equal sharpness, 24mm, f/8`
- `rack focus — starts on background detail, pulls to subject in foreground`

---

## Bokeh

The quality of the out-of-focus blur behind (or in front of) the subject.

| Bokeh type | Visual character |
|---|---|
| Spherical bokeh | Circular blur circles, standard lens |
| Anamorphic bokeh | Oval/elongated circles, cinematic and wide |
| Highlight bokeh | Background lights become soft circles or ovals |
| Specular bokeh | Sparkle quality in bright highlights |

**Prompt phrase:** `anamorphic bokeh, oval out-of-focus highlights in background, cinematic widescreen`

---

## Motion Blur

Objects in motion are blurred along their direction of movement. Faster movement = more blur.

**Natural motion blur:** Corresponds to the camera's shutter angle (typically 180° = half the frame duration).

**Overcranked (slow motion):** Reduced motion blur — each frame captured faster, movement smoother.

**Undercranked (fast action):** Increased blur — more movement per frame, energetic chaos.

**Prompt phrase:**
- `natural motion blur on moving subjects, shutter angle 180 degrees`
- `slow-motion capture, reduced motion blur, high-fps feel, ultra-clear movement`
- `fast-action undercranked, increased motion blur, energetic and visceral`

---

## Lens Flares

Light hitting the lens directly, creating artefacts — streaks, circles, hexagons depending on lens construction.

**Natural (ARRI/cinema):** Subtle, warm, well-behaved, cinematic.

**Anamorphic flare:** Horizontal light streak across the frame. One of the most recognizable cinematic visual signatures.

**Artificial/stylized:** Dramatic multi-element flares, heavy use in sci-fi and action.

**Prompt phrase:**
- `natural lens flare from [light source], warm subtle, cinematic`
- `anamorphic horizontal lens flare, light streak across frame when looking toward source`
- `strong stylized lens flare at [position], sci-fi aesthetic, blue-white`

---

## Bloom

Light sources bleed softly into surrounding areas. Makes bright objects appear to glow.

**Heavy bloom:** Fantasy, dream, sacred imagery, otherworldly beauty.

**Subtle bloom:** Natural daylight realism, diffusion filter look.

**Prompt phrase:**
- `subtle bloom on bright sources, natural diffusion, filmic`
- `heavy bloom on [light source], light bleeds into surrounding frame, dream-like glow`

---

## Chromatic Aberration

Lens imperfection causing colour channels to separate at the edges of the frame, producing coloured fringing.

**When to use:** Distress, hallucination, damaged footage aesthetic, horror, extreme force/impact.

**Prompt phrase:** `chromatic aberration, colour fringing at frame edges, lens distortion effect, [mild/strong]`

---

## Film Grain

The texture of analogue film — random noise pattern that gives film its organic, alive quality.

**Fine grain (ISO 100–400 film):** Barely visible, adds texture without drawing attention.

**Heavy grain (ISO 1600+ or pushed film):** Visible, organic, matches high-contrast dark scenes, crime drama, war.

**Prompt phrase:**
- `fine film grain, organic texture, adds life to image, [period/filmic aesthetic]`
- `heavy film grain, visible organic noise, pushed film stock character, gritty`

---

## Heat Distortion / Heat Shimmer

Thermal convection from hot surfaces causes light to distort visibly — the air above a fire, a desert road in summer, the barrel of a weapon just fired.

**Prompt phrase:** `heat shimmer above [hot surface], thermal convection distortion, air wavering in the heat`

---

## Vignette

Darkening at the corners and edges of the frame, directing the eye to the center.

**Natural vignette:** Optical effect of wide-aperture lenses — gentle, adds filmic depth.

**Stylized vignette:** Heavy darkening, noir or horror, oppressive framing.

**Prompt phrase:**
- `natural lens vignette, gentle darkening at edges, filmic`
- `heavy vignette, dark corners pressing in, oppressive, noir or horror`

---

## Cinematic FX Stack Template

For a standard cinematic grade:

```
CINEMATIC FX:
  DOF:                 [shallow / deep / rack focus description]
  Motion blur:         [natural / slow-mo / undercranked]
  Lens flare:          [none / subtle / anamorphic / stylized]
  Bloom:               [none / subtle / heavy]
  Film grain:          [none / fine / medium / heavy]
  Chromatic aberration:[none / mild / strong — justified by story]
  Vignette:            [natural / stylized]
  Heat shimmer:        [none / present — source location]
```

---

## Golden Rule

> Lens effects are properties of the camera, not decorations on the image. Apply them to simulate optical behavior, not to add production value. An unmotivated lens flare is visual noise.
