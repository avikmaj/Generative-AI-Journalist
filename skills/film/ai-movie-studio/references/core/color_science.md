# Color Science — Grading, Theory & Cinematic Color

## Color Is Storytelling

Colour is not post-production polish — it is a narrative tool. It sets the emotional register of the film before a single word of dialogue is spoken. A character bathed in cold blue is already in danger. A scene rendered in warm amber is already nostalgic. Design colour as deliberately as dialogue.

---

## Color Theory Fundamentals

### Color Temperature (Kelvin)

| Range | Look | Emotional Register |
|---|---|---|
| 1700–2500K | Deep orange-red | Primal, fire, survival, ancient |
| 2700–3500K | Warm gold-amber | Nostalgia, home, safety, romance |
| 4000K | Neutral warm | Commercial, accessible, real |
| 5500K | Daylight neutral | Natural, factual, clinical |
| 6500–7500K | Cool blue-white | Night, alienation, fear, technology |
| 8000K+ | Deep blue | Extreme cold, supernatural, void |

### Color Harmony Systems

**Complementary:** Colors directly opposite on the wheel (orange/blue, teal/red). Maximum contrast, visual tension. The dominant palette of Hollywood blockbusters — warm subjects against cool backgrounds.

**Analogous:** Colors adjacent on the wheel (blue/teal/green). Harmonious, unified, one emotional register. Used for mood-dominant films.

**Triadic:** Three colors equidistant on the wheel. Vibrant, complex, unstable. Used for visually aggressive or fantasy-heavy work.

**Split-complementary:** One dominant color, two colors flanking its complement. More nuanced than straight complementary.

---

## Cinematic Color Palettes

### Teal and Orange (Hollywood Blockbuster)

The dominant Hollywood palette. Human skin renders as warm orange; shadows and environments grade toward teal. Maximum separation of subject from background.

**Emotional register:** Modern, high-octane, accessible, cinematic.

**Prompt phrase:** `teal-orange grade, warm skin tones, teal-shifted shadows and environment, high saturation contrast`

---

### Desaturated / Washed Out

Muted colours, pulled toward grey. Reduced saturation across the board.

**Emotional register:** Realism, grit, war, trauma, poverty, the colour drained from a world.

**Best use:** War films, crime drama, social realism, aftermath scenes.

**Prompt phrase:** `desaturated grade, muted tones, grey-pulled colour, reduced saturation, gritty naturalism`

---

### High Contrast Monochrome

Black and white, pushed contrast, deep blacks, bright whites, minimal midtone.

**Emotional register:** Timelessness, moral clarity, the past, documentary truth, noir.

**Prompt phrase:** `high-contrast black and white, deep blacks, bright whites, minimal midtone, classic noir monochrome`

---

### Warm Golden Grade

Warm amber-yellow push across the frame. Shadows lifted toward amber. Skin glows.

**Emotional register:** Memory, nostalgia, summer, childhood, warmth and safety, love.

**Prompt phrase:** `warm golden grade, amber push, lifted warm shadows, skin glowing with warmth, nostalgic and beautiful`

---

### Cold Steel Blue

Cool blue-grey push. Shadows deep navy. Skin desaturated.

**Emotional register:** Danger, corporate threat, the clinical modern world, surveillance, controlled environments.

**Prompt phrase:** `cold steel-blue grade, blue-shifted shadows, desaturated skin, clinical and threatening`

---

### Cyberpunk / Neon

Magenta and cyan fight for dominance. Deep blacks. Electric saturation in accent colours only.

**Emotional register:** Hedonism, corruption, the hyperreal future city, pleasure and danger.

**Prompt phrase:** `cyberpunk neon grade, deep blacks, magenta and cyan accent saturation, electric colour in shadow, dark and vivid`

---

### Bleach Bypass / Silver Retention

Increased contrast, reduced saturation, silver grain retained. Colours partially washed out but shadows brutal.

**Emotional register:** War, crisis, adrenaline, the harshness of extreme situations.

**Best use:** Combat films, intense action, psychologically extreme drama.

**Prompt phrase:** `bleach bypass look, high contrast, partially desaturated, silvery shadow detail, harsh and intense`

---

### Pastel / Dream

Soft, high-key, lifted shadows, reduced contrast. Colors gentle and faded at the edges.

**Emotional register:** Fantasy, memory, the soft edges of a dream, innocence, longing.

**Prompt phrase:** `pastel dream grade, soft high-key, lifted shadows, gentle colours, mist at edges, dream-like quality`

---

### ACES (Academy Color Encoding System)

The professional standard for colour management across the full pipeline. HDR-capable, wide gamut.

**For generation:** Reference the look that ACES film emulation produces — rich midtones, controlled highlights, slight warmth in skin, detailed shadow.

**Prompt phrase:** `ACES film emulation, wide dynamic range, controlled highlight rolloff, rich midtone detail, cinematic colour science`

---

## Film Emulation LUTs

Emulating specific film stocks in AI generation:

### Kodak Vision3 500T (5219)

Warm, lush, smooth highlight rolloff. Slight cyan in shadows.

**Prompt phrase:** `Kodak Vision3 film stock, warm grain texture, cyan-shifted shadows, smooth highlight rolloff, organic colour`

### ARRI Look / Alexa Log

Clean, natural, high dynamic range. The signature of prestige TV and premium cinema.

**Prompt phrase:** `ARRI Alexa look, clean naturalistic grade, high dynamic range, smooth rolloff, prestige cinema palette`

### Fuji Velvia

High saturation, vivid greens and blues, strong contrast. Classic landscape/nature look.

**Prompt phrase:** `Fuji Velvia emulation, high saturation, vivid greens, strong contrast, punchy and beautiful`

### Fuji 8500 (Reala)

More muted than Velvia, natural skin tones, slight cool tendency.

**Prompt phrase:** `Fuji Reala film stock, natural muted tones, accurate skin, slight cool shift, organic and real`

---

## Color as Narrative Device

### Character Color Identity

Assign each major character a colour signature that subtly persists across the film. As the story changes their relationship, the colours interact differently.

**Example (crime drama):**
- Detective: desaturated blues → associated with system and reason
- Antagonist: deep red → violence, corruption
- Turning point scene: the detective's environment bleeds red for the first time → they've crossed a line

### Color Shift to Signal Change

The dominant grade shifts to signal a story change:
- Act I: warm, accessible colours → the world before
- Act II: cooling, increasing desaturation → things getting worse
- Act III: either warmth returns (triumph) or goes entirely cold (tragedy)

### Color as World-Building

Define each location by its colour temperature:
- The protagonist's home: warm, amber, lived-in
- The enemy's stronghold: cold, industrial, clinical
- The neutral meeting ground: flat, grey, neither world

**Prompt phrase for contrast between locations:**
`[Location A: warm 2800K interior, amber wood, lived-in warmth] / [Location B: cold 6500K fluorescent, grey concrete, no warmth]`

---

## Color Grading Prompt Templates

### Action Film Grade
```
GRADE: teal-orange complementary, warm skin, cool shadows, high contrast, Kodak print emulation, 
       slight grain, 2.39:1 anamorphic crop
```

### Crime / Noir Grade
```
GRADE: desaturated-to-monochrome range, deep blacks, minimal fill, high contrast, 
       bleach-bypass quality, silver retention in shadows
```

### Horror Grade
```
GRADE: green-shifted shadows, desaturated midtones, crushed blacks, cool moonlight key, 
       slight film degradation in extremes
```

### Fantasy / Epic Grade
```
GRADE: rich saturated colour, warm golden keys, deep complementary shadows, 
       high dynamic range, painterly colour science, ACES emulation
```

### War Film Grade
```
GRADE: desaturated, grey-green push, lifted shadows showing grime, bleach bypass quality, 
       organic grain, heat shimmer in distance
```

### Sci-Fi Grade
```
GRADE: cold blue-cyan base, neon accent saturation in practicals, deep shadows, 
       clean digital feel, high contrast, modern and cold
```

---

## Golden Rule

> Decide the film's emotional register in colour before generating a single frame. Consistent colour across a production is the mark of intention — inconsistent colour is the mark of accident.
