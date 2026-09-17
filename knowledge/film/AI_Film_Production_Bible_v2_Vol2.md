# Chapter 1 — How to Use This Encyclopedia

*A library, not a manual*

> "Volume I taught you to direct. Volume II hands you the parts."

## What Volume II Is

Volume I of the AI Film Production Bible is a course: it explains how to think like a director and turn a story into a complete production brief. **Volume II is the parts bin.** It contains reusable, named components — camera moves, lighting setups, environments, performances, dialogue patterns, soundscapes, colour grades, effects, transitions — plus ready-to-shoot genre packs and the Avik Studio canon packs. You assemble a production from proven components instead of writing every prompt from a blank page.

Nothing here replaces Volume I. Every component obeys the same system: the ASPL prompt grammar (Ch2), the six-dimension Master Prompt block and reference-image rule (Ch3), and the module system that lets components stack cleanly (Ch4).

## The Five Parts

- **Part I — The Encyclopedia System (Ch1–4).** How the library is structured and how to assemble from it.
- **Part II — The Craft Preset Libraries (Ch5–13).** The core: camera, lighting, environment, performance, dialogue, audio, colour, VFX, and transition presets.
- **Part III — Genre Production Packs (Ch14–18).** Ready-to-shoot recipes for adventure/fantasy, mythology, sci-fi, children, and Shorts.
- **Part IV — The Avik Studio Canon Packs (Ch19–22).** Locked components for Maani Adventures, The Infinity Trap, Neo-Vega, and Skyhaven.
- **Part V — Production Systems (Ch23–26).** Template banks, the moderation-safe compiler, publishing systems, and the expansion blueprint.

## How to Read a Preset Entry

Every preset shares one anatomy so it drops straight into a prompt:

```
`PRESET_ID` — Name.  Purpose / emotion.  Key characteristics (the words to paste).
[optional] Best lens / camera · pairs-with · genre.
```

The **ID** (e.g. `CAM_ORBIT_002`, `GRADE_ADV_001`) is a stable handle you can reference in an instruction or reuse across a series. The **characteristics** are the actual phrasing to drop into the relevant ASPL section. Presets are model-agnostic; adapt the wording to the target model.

## The One-Minute Assembly Workflow

1. **Story Brief** — one line: character, goal, conflict, resolution, final image, emotion.
2. **Pick a pack** (Part III/IV) or build from scratch.
3. **Pull one preset per department** — camera + lighting + environment + performance + audio + colour, plus a transition into the next shot.
4. **Declare `REF IMAGES:`** — the @reference images the clip needs (Ch3).
5. **Drop the presets into the six-dimension block** in order, add the layer stack + in-prompt watermark, obey the One-Action Rule.
6. **Compile and QA** (Ch24) — moderation-safe language, identity, continuity, one memorable final image.

## Golden Rule

A preset is a starting point, not a straitjacket. Pick components that serve the emotion of the shot, then adapt their wording. The library exists to make good choices fast and repeatable — never to make every film look the same.

---

# Chapter 2 — The ASPL Prompt Grammar — Quick Reference

*The one page you keep open while writing prompts*

> "A prompt is a production specification. Fill the sections in order."

## The Section Order

Every generation prompt is assembled in this fixed order (the Avik Studio Prompt Language):

```
MISSION · PROJECT · MODEL · REFERENCE IMAGES · IDENTITY LOCK · STORY · CHARACTERS ·
ENVIRONMENT · VISUAL STYLE · PRODUCTION DESIGN · CAMERA · LIGHTING · PERFORMANCE ·
DIALOGUE · LIP SYNC · AUDIO · TIMELINE · CONTINUITY · TECHNICAL · QUALITY · OUTPUT
```

For a single 15-second clip you may collapse it into the six-dimension block (Ch3); the section order above is the full grammar behind that block.

## Priority Order

When the model can only honour so much, these carry the most weight, in order:

> Image References → Character Identity → Story → Environment → Camera → Lighting → Performance → Dialogue → Audio → Rendering → Effects

## The Five Rules

- **Identity before action.** Establish who the character is, then what they do.
- **One concept per sentence.** "The camera pushes in slowly." "Golden light rims her hair." Never braid unrelated instructions.
- **Positive over negative.** "Natural human anatomy, believable weight" beats "no bad hands." Keep negatives as a short backstop.
- **Intention before motion.** Describe the thought/emotion that causes the movement, then the movement.
- **One dominant emotion per shot.** Every department reinforces the same feeling.

## The Reusable Skeleton

```
MISSION               <one complete 15s cinematic sequence, publish-ready>
REFERENCE IMAGES      @character_sheet · @storyboard · @environment_ref · @style_ref
IDENTITY LOCK         <face/hair/eyes/body/wardrobe/voice/movement held>
STORY                 <beginning → conflict → resolution>
CHARACTERS            <profiles + emotion + goal>
ENVIRONMENT           <world/time/season/weather/atmosphere/ambient audio>
VISUAL STYLE          <one render style + grade>
CAMERA                <purpose · type · lens · height · movement · speed · focus>
LIGHTING              <time · key · fill · rim · atmosphere · colour temp>
PERFORMANCE           <thought → emotion → movement → reaction → recovery>
DIALOGUE / LIP SYNC   <speaker · emotion · breathing · pauses · sync>
AUDIO                 <dialogue · Foley · ambience · music · silence>
TIMELINE              <0–15s beats>
CONTINUITY            <identity · wardrobe · lighting · props · emotion held>
TECHNICAL / OUTPUT    <quality goals · one continuous clip, publish-ready>
```

## Model Adapter Note

The grammar is universal; the syntax is not. Keep the spec stable and adapt phrasing per model — CapCut Omni / Dreamina (primary), Veo, Kling, Seedance, Runway. Do not build a workflow on any one model's quirks.

---

# Chapter 3 — The Six-Dimension Master Prompt & Reference-Image System

*The single copy-paste block behind every clip*

> "One block. Six dimensions, in order. Then layer, then watermark."

## The Reference-Image Rule (do this first)

CapCut Omni is reference-image driven, so **before every clip's code block, declare the `REF IMAGES:` line** naming the @images to attach. Default every clip to `@character_sheet` (identity) + `@storyboard` (shot order / continuity); add `@environment_ref` (location), `@style_ref` (grade / mood), and `@prop_ref` (key objects) as the shot needs. Never output a clip prompt without its @images, and echo the same @images inside the block's REFERENCES / IDENTITY LOCK fields.

## The Six Dimensions

Every clip is ONE self-contained copy-paste block (fenced code), embedding all six dimensions in order:

```
[Emotional tone] + [Visual reference / render style + grade] + [Subject / locked character
anchors] + [Composition / framing + shot size] + [Lighting direction, quality, colour,
volumetrics] + [Camera settings / lens, movement, depth]
```

Then layer, in this order: **VFX · SFX · NARRATOR (deep male) · DIALOGUE (label voice gender) · ON-SCREEN TEXT · watermark.** Never split a clip across separate labelled lines outside the block.

## The One-Action Rule

Each 15-second clip = one main beat + one held final hero shot. Never chain "then X then Y then crane then logo." One action, cleanly executed, then the hero frame the audience remembers.

## Rendering & Watermark (everything in-prompt)

Put every element inside the generation prompt: watermark, end tagline, Subscribe. The watermark is `"CREATED BY AVIK STUDIO"` — small, subtle gold, lower-center, in **every** block. Render episode titles as a held closing title card on the outro clip; render the teaser title as "[Title] — Coming Soon." Never put "fade to logo / logo light-burst / logo chime" or the channel tagline inside a scene prompt — it garbles into a fake logo. Render words as a held title over the hero shot; send thumbnail prompts to a text-reliable image model.

## A Worked Clip Block

```
REF IMAGES: @character_sheet + @storyboard + @environment_ref

Warm, hopeful, wonder-struck. Photorealistic cinema, soft golden grade. A curious young
girl (locked identity: yellow raincoat, curly black hair, large brown eyes) kneels at the
edge of a mist-lit forest stream. Medium shot, rule of thirds, subject frame-left. Golden-hour
key from screen-right, soft sky fill, gentle rim, volumetric rays through pines, warm bounce
off wet stones. 50mm, slow push-in, shallow depth, natural acceleration then a held hero frame.
VFX: drifting pollen, faint water sparkle. SFX: stream, distant birds, soft breeze.
NARRATOR (deep male): "Some doors open only for the curious." DIALOGUE: none.
ON-SCREEN TEXT: none. Watermark: "CREATED BY AVIK STUDIO" — small subtle gold, lower-center.
```

## Golden Rule

The block is a container for intent, not a wall of adjectives. Six dimensions, one action, the @images that lock identity, the watermark that brands it — then stop.

---

# Chapter 4 — The Reusable Module System

*How components stack without fighting each other*

> "Build once, reuse forever. The studio gets faster with every shipped film."

## Modules, Not Paragraphs

Treat each department as a swappable module: `CAMERA_MODULE`, `LIGHT_MODULE`, `PERFORMANCE_MODULE`, `AUDIO_MODULE`, `ENVIRONMENT_MODULE`, `IDENTITY_MODULE`. A production is an assembly of modules, each drawn from Part II or written once and saved. Change the camera module without touching identity; swap the grade without rewriting the story.

## The Identity Cache (lock once, reference many)

Define each recurring character once as an identity block, then reference it rather than re-describing it every shot:

```
IDENTITY: MAANI
Female tricolour beagle · soft brown/black/white coat pattern (held) · long velvet ears ·
gentle brown eyes · light collar · natural pacing, nose leads · loyal, curious, playful.
Anatomy note (every block): Maani is FEMALE — smooth featureless underbelly, no genitalia
ever visible; frame side-on or upright (never belly-up); jumps low and modest.
```

Once cached, a clip only needs `identity: MAANI` plus the shot-specific action. Re-describing appearance every shot is the main cause of identity drift.

## Module Dependency Order

Changes propagate down this tree; resolve higher modules first:

```
Story → Character → { Dialogue · Performance · Wardrobe }
      → Environment → { Lighting · Audio · Weather }
      → Camera → { Timeline · Editing }
```

## Naming & Versioning

Name presets `DEPT_SUBTYPE_NNN` (e.g. `LIGHT_GOLDEN_003`, `CAM_TRACK_004`). Version productions `PROJECT / SCENE / SHOT / Vxx` and never overwrite a working generation. When a preset improves, bump its version and note what changed — the library is institutional memory, so history matters.

## Compression

Large productions exceed what a single prompt should carry. Compress by priority — keep story, identity, environment, camera, performance; trim decorative detail the model infers anyway. The point is to communicate intent clearly, not to maximise word count.

## Golden Rule

Never rewrite a prompt if a saved module already solves it. Every approved character, setup, grade, and template goes back into the library. Over time the studio becomes faster and more consistent because each production leaves it smarter than before.


# Chapter 5 — The Camera Preset Library

*Every move answers "why is the camera moving?"*

> "Pick the simplest move that serves the emotion. Then hold the hero frame."

## How to Use

Each preset is a `CAM_` handle plus the phrasing to drop into the CAMERA section. Pair a move with a lens and a purpose; obey the One-Action Rule (one move + one held frame per clip). Default storytelling lens is 35–50mm unless the emotion calls otherwise.

## Static

**`CAM_STATIC_001` — Locked Tripod.** Truth, calm, observation — absolutely stable frame; dialogue, documentary, product, wildlife.
**`CAM_STATIC_002` — Low Hero Static.** Power, arrival — low angle, subject towering, stable; heroes, monsters, architecture.
**`CAM_STATIC_003` — Overhead Static.** Pattern, scale, planning — top-down, symmetrical; maps, tables, choreography.
**`CAM_STATIC_004` — Macro Insert.** Detail, meaning — extreme close on a hand, object, or eye; reveals and emphasis.

## Push-In & Pull-Out

**`CAM_PUSH_001` — Slow Emotional Push.** Realisation, intimacy — 85/50mm, invisible acceleration, soft stop; dialogue rises under it.
**`CAM_PUSH_002` — Discovery Push.** Wonder — Steadicam, 35mm, slow approach to a mysterious object.
**`CAM_PUSH_003` — Menace Push.** Suspense — low key, controlled speed, no sudden change; villains, threats.
**`CAM_PULL_001` — Reflection Pull.** Loss, ending — very slow, reveals the surrounding world.
**`CAM_PULL_002` — Scale Reveal.** Epic — pull back and rise, revealing environment and true scale.

## Tracking

**`CAM_TRACK_001` — Side Track.** Journey, conversation — Steadicam, parallel, eye level, stable background separation.
**`CAM_TRACK_002` — Lead Track.** Hero advance — camera moves backward as the subject strides forward.
**`CAM_TRACK_003` — Follow Track.** Mystery — trails the subject from behind into the unknown.
**`CAM_TRACK_004` — Animal Track.** Wildlife, pets — species-appropriate pace, smooth, no shake; ideal for Maani walks.

## Orbit & Crane

**`CAM_ORBIT_001` — Hero Orbit.** Importance, victory — 180°, slow, steady radius, golden-hour finish.
**`CAM_ORBIT_002` — Wonder Orbit.** Magic — circular, floating, elegant around a glowing object.
**`CAM_CRANE_001` — Epic Rise.** Scale, hope — ground to sky, revealing the world.
**`CAM_CRANE_002` — Reveal Rise.** History, fantasy — rises behind a foreground object to unveil architecture.

## Aerial & Immersive

**`CAM_DRONE_001` — Sunrise Village Flyover.** 30–80m, forward glide, slow descent, warm morning light.
**`CAM_DRONE_002` — Summit Flyover.** 100–300m, forward with slight elevation gain; mountains, epic reveals.
**`CAM_DRONE_003` — Forest Descent.** Starts above the canopy, drops through trees to reveal a character.
**`CAM_FPV_001` — Chase FPV.** Adrenaline — high speed, obstacle avoidance, ground following; sports, action.
**`CAM_FPV_002` — Flowline FPV.** Momentum — one continuous swoop through a space; theme parks, cities.

## Specialty & Dialogue Coverage

**`CAM_SPEC_001` — Helmet/Bodycam.** Immersion, realism — head-driven motion, natural horizon shift.
**`CAM_SPEC_002` — Security/Found-Footage.** Tension — wide, fixed, slightly degraded; horror, investigation.
**`CAM_DLG_001` — Over-the-Shoulder.** Trust, connection — frames listener reaction.
**`CAM_DLG_002` — Shot / Reverse.** Balanced dialogue — alternating coverage with reaction beats.
**`CAM_DLG_003` — Two Shot.** Relationship — both characters framed; family, romance.

## Camera by Emotion

| Emotion / Need | Preset |
|---|---|
| Intimacy | `CAM_PUSH_001` |
| Wonder | `CAM_PUSH_002`, `CAM_ORBIT_002` |
| Power / arrival | `CAM_STATIC_002`, `CAM_ORBIT_001` |
| Scale | `CAM_CRANE_001`, `CAM_DRONE_002` |
| Adventure | `CAM_TRACK_001`, `CAM_DRONE_001` |
| Adrenaline | `CAM_FPV_001` |
| Truth / calm | `CAM_STATIC_001` |

## CAMERA Block Template

```
CAMERA: <purpose> · <CAM_ID> · <lens> · <height> · <movement> · <speed> · <focus> ·
        composition <rule> · transition <into next shot>
```

## Golden Rule

If removing the move would not weaken the emotion, keep the camera still. One motivated move, then the held hero frame.

---

# Chapter 6 — The Lighting Preset Library

*Shape the light, shape the feeling*

> "Name the source, the direction, the quality, and the reason — every time."

## How to Use

Each `LIGHT_` preset lists source, direction, quality, and mood. Define one lighting philosophy per scene and hold it across shots. Always motivate the key (sun, window, fire, screen) so shadows and reflections behave.

## Natural Light

**`LIGHT_GOLDEN_001` — Classic Golden Hour.** Hope, warmth — low warm sun, long shadows, soft haze, golden rim, natural skin tones.
**`LIGHT_GOLDEN_002` — Forest Sunrise.** Wonder — rays through trees, morning fog, warm moss bounce, floating dust.
**`LIGHT_BLUE_001` — Blue Hour.** Reflection, romance — deep blue sky, warm practical lights, soft contrast.
**`LIGHT_NIGHT_001` — Full Moon.** Fantasy, mystery — silver rim, cool blue fill, long shadows.
**`LIGHT_OVERCAST_001` — Soft Overcast.** Melancholy, calm — large soft source, low contrast, muted palette.
**`LIGHT_STORM_001` — Thunderstorm.** Conflict — lightning flashes, dark clouds, wet reflections, wind.

## Studio

**`LIGHT_STUDIO_001` — Three-Point.** Dialogue, commercial — key + fill + back; clean separation.
**`LIGHT_STUDIO_002` — Butterfly.** Beauty, luxury — high frontal key, soft symmetrical shadow.
**`LIGHT_STUDIO_003` — Rembrandt.** Drama, history — cheek triangle, one eye softly shadowed.
**`LIGHT_STUDIO_004` — Split.** Villains, tension — half face lit, half shadow, high contrast.

## Practical & Elemental

**`LIGHT_FIRE_001` — Campfire.** Friendship, survival — moving orange light, dynamic shadows, embers, smoke.
**`LIGHT_CANDLE_001` — Candlelit Room.** Intimacy, faith — soft flicker, low warm glow.
**`LIGHT_TORCH_001` — Ancient Interior.** Exploration — torch flicker, stone reflections, drifting smoke.
**`LIGHT_ELEM_001` — Rain-Wet Night.** Drama, noir — street reflections, neon, droplets on glass, headlights.
**`LIGHT_ELEM_002` — Snow Morning.** Peace, holiday — high ambient bounce, cool shadows, warm sun sparkle.

## Location & Genre

**`LIGHT_LOC_001` — Deep Forest Morning.** Canopy-filtered sun, moving leaf shadows, moss bounce, mist.
**`LIGHT_LOC_002` — Snow Peak Sunrise.** Warm sun, blue snow shadows, clean HDR air.
**`LIGHT_LOC_003` — Metropolitan Night.** Building LEDs, streetlights, traffic reflections, balanced exposure.
**`LIGHT_GENRE_001` — Cyberpunk Neon.** Blue/magenta neon, wet reflections, steam, LED signage.
**`LIGHT_GENRE_002` — Sacred Glow.** Mythic — god rays, warm bloom, floating motes, luminous fog.
**`LIGHT_GENRE_003` — Clean Sci-Fi.** LED panels, blue edge light, metallic reflections, minimal shadow.

## Emotional Lighting

**`LIGHT_EMO_HOPE`** — golden key, soft fill, gentle bloom, long shadows. **`LIGHT_EMO_FEAR`** — low key, hard shadows, cool tint, dark corners. **`LIGHT_EMO_WONDER`** — volumetric rays, warm bloom, floating particles. **`LIGHT_EMO_TRIUMPH`** — bright sky, backlit hero, golden rim, clear air.

## Colour Temperature

| Range | Reads As |
|---|---|
| Warm 2200–4500K | Comfort, family, adventure |
| Neutral 4500–5500K | Natural realism |
| Cool 6000–10000K | Mystery, technology, night, isolation |

## LIGHTING Block Template

```
LIGHTING: time <t> · key <source/direction> · fill <soft> · rim <colour> · bounce <surface> ·
          atmosphere <fog/rays> · colour temp <K> · shadow <quality> · continuity <hold across shots>
```

## Golden Rule

One motivated source per scene, consistent direction and colour across shots. Lighting succeeds when it enhances the story rather than announcing itself.

---

# Chapter 7 — The Environment Preset Library

*A world that existed before the story and will continue after it*

> "Describe a living world, not a list of objects."

## How to Use

Each `ENV_` preset defines terrain, vegetation, motion, wildlife, and a matching soundscape. Every environment supports weather variants (sunny → golden → blue → rain → storm → fog → snow → night). Always design foreground / midground / background for depth.

## Natural

**`ENV_FOREST_001` — Ancient Pine Forest.** Adventure, wonder — moss, roots, fallen logs, a stream; moving leaves, birds, floating pollen; birds + wind + water audio.
**`ENV_FOREST_002` — Enchanted Forest.** Fantasy — glowing mushrooms, fireflies, magic dust, warm bloom; whispers + crystal resonance.
**`ENV_RAINFOREST_001` — Rainforest.** Dense leaves, humidity, water droplets, fog; monkeys, parrots, frogs.
**`ENV_MOUNTAIN_001` — Himalayan Valley.** Epic — snow peaks, pine, river, waterfalls, meadows; wind, eagles, goats.

## Water

**`ENV_BEACH_001` — Tropical Beach.** Vacation, family — white sand, palms, turquoise waves, shells; waves + gulls + children.
**`ENV_BEACH_002` — Sunset Beach.** Romance — orange sky, pink horizon, long reflections.
**`ENV_OCEAN_001` — Open Sea.** Adventure, survival — deep blue, large waves, clouds; ocean + wind + gulls.
**`ENV_WATERFALL_001` — Waterfall Basin.** Wonder — mist, rainbow, wet rocks, backlit spray.

## Desert & Snow

**`ENV_DESERT_001` — Great Dunes.** Survival — sand dunes, heat shimmer, dry shrubs; wind + shifting sand + silence.
**`ENV_OASIS_001` — Hidden Oasis.** Hope — palms, fresh water, birds, shade.
**`ENV_SNOW_001` — Winter Forest.** Holiday, family — snow-laden trees, frozen lake, cabins, smoke; footsteps + wind.
**`ENV_ARCTIC_001` — Arctic Expanse.** Isolation, wonder — icebergs, aurora, frozen sea.

## Villages & Cities

**`ENV_VILLAGE_001` — Indian Village.** Warmth — mud houses, banyan tree, temple, market, pond; children + temple bell + animals.
**`ENV_VILLAGE_002` — Alpine Hamlet.** Peace — wooden cabins, stone paths, flower gardens, mountain lake.
**`ENV_CITY_001` — Modern Skyline.** Business, travel — glass towers, roads, metro, parks; traffic + crowds.
**`ENV_CITY_002` — Cyberpunk District.** Neon, rain, holographic signage, flying vehicles; hover traffic + announcements.

## Fantasy & Sci-Fi

**`ENV_FANTASY_001` — Floating Islands.** Floating peaks, waterfalls into cloud, ancient temples; golden magic glow.
**`ENV_FANTASY_002` — Crystal Kingdom.** Crystal towers, reflective lakes, glowing caves, magic bridges.
**`ENV_SCIFI_001` — Mars Colony.** Red desert, research domes, rovers, airlocks; thin-atmosphere wind + dust.
**`ENV_SCIFI_002` — Orbital Station.** Zero-g, observation windows, docking ports, robotic arms.

## Interior

**`ENV_HOME_001` — Family Living Room.** Warm, safe — sofa, books, plants, family photos, natural window light.
**`ENV_LAB_001` — Research Lab.** Discovery — glass, monitors, blue interface glow, clean surfaces.
**`ENV_TEMPLE_001` — Ancient Temple Hall.** Reverence — stone, statues, candles, dust, sacred glow.

## ENVIRONMENT Block Template

```
ENVIRONMENT: <ENV_ID> · time <t> · season <s> · weather <w> · foreground <x> · midground <y> ·
             background <z> · motion <leaves/water/dust> · ambient audio <layers> · continuity <hold>
```

## Golden Rule

If the characters left the frame, the environment should still tell a story. Give every location history, motion, and its own soundscape.


# Chapter 8 — The Performance & Motion Preset Library

*Characters move because they think, feel, and decide*

> "Movement alone is not acting. Describe intention first, motion second."

## How to Use

Each `PERF_` preset carries a movement plus its emotional cause. Drop it into PERFORMANCE and pair with a facial and hand preset. Every motion runs the loop: thought → emotion → preparation → movement → reaction → recovery.

## Human Locomotion

**`PERF_WALK_001` — Neutral Walk.** Natural heel strike, weight transfer, relaxed arm swing, forward gaze.
**`PERF_WALK_002` — Curious Child Walk.** Short stride, frequent stops, looks around, slight bounce, points at things.
**`PERF_WALK_003` — Hero Entrance.** Steady pace, upright posture, controlled arm swing, direct gaze; pairs with `CAM_PUSH_001`.
**`PERF_WALK_004` — Elderly Walk.** Measured pace, shorter stride, careful balance, steady breathing.
**`PERF_RUN_001` — Joyful Child Run.** High energy, variable stride, natural laughter, looking ahead.
**`PERF_RUN_002` — Athletic Sprint.** Forward lean, explosive push-off, strong arm drive, controlled breath.
**`PERF_RUN_003` — Panic Run.** Irregular stride, fast breathing, looking back, tense shoulders.

## Everyday Actions

**`PERF_SIT_001` — Relaxed Sit.** Natural lowering, comfortable posture, maintained eye contact.
**`PERF_SIT_002` — Nervous Sit.** Posture adjustments, clasped hands, foot tap, quick blinking.
**`PERF_LIFT_001` — Pick Up Object.** Look → reach → grip → lift → rebalance → carry naturally.
**`PERF_REACT_001` — Discovery Reaction.** Eyes widen → small inhale → lean in → slow smile.

## Child Behaviour

**`PERF_CHILD_001` — Age 4–6.** High energy, curiosity, quick head turns, looks to parents, open gestures, wide eyes.
**`PERF_CHILD_002` — Age 7–10.** More coordination, growing confidence, independent exploration, expressive hands.

## Animal Motion

**`PERF_DOG_001` — Beagle Neutral (Maani).** Medium pace, nose leads, tail natural, ears track sound, soft blinking, gentle panting.
**`PERF_DOG_002` — Happy Beagle.** Tail wag, quick steps, play bow, small modest hops, looks up at companion.
**`PERF_DOG_003` — Alert Beagle.** Sudden stop, head tilt, ears up, steady tail, focused gaze.
**`PERF_HORSE_001` — Gallop.** Powerful rear push, rhythmic stride, wind in mane, muscle movement.
**`PERF_BIRD_001` — Eagle Soar.** Wing extension, thermal glide, minimal flapping, occasional correction.
**`PERF_DRAGON_001` — Ancient Dragon.** Heavy body, powerful wing beats, tail balance, deep breathing, natural landing impact.

> **Maani anatomy — apply to every Maani block:** Maani is FEMALE — render correct female anatomy: a smooth, featureless underbelly with NO genitalia ever visible; always frame her side-on or standing upright (never belly-up); keep jumps low and modest with no belly-exposing mid-air poses.

## Micro-Expressions & Gestures

**`PERF_MICRO_CURIOUS`** — brows lift, eyes widen, head tilt, small inhale. **`PERF_MICRO_HAPPY`** — cheeks rise, eyes soften, genuine small smile. **`PERF_MICRO_FEAR`** — eyes widen, jaw loosens, fast blink, shoulders tense. **`PERF_MICRO_RESOLVE`** — focused eyes, relaxed jaw, controlled breath, steady posture.
**Hands** — open palm (invite/comfort), point (direction/discovery), hands on hips (confidence), clasped (nervous/hope). Keep fingers purposeful and relaxed; avoid rigid claw poses.

## PERFORMANCE Block Template

```
PERFORMANCE: emotion <x> · body language <y> · breathing <pattern> · eyes <behaviour> ·
             facial <PERF_MICRO_ID> · hands <gesture> · secondary motion <hair/cloth> ·
             recovery <returns to rest> · continuity <same movement style>
```

## Golden Rule

Never write "happy" or "runs." Write the thought and the muscles: eyes brighten → smile develops → weight shifts → she runs. Intention first, motion second.

---

# Chapter 9 — The Dialogue & Voice Preset Library

*Dialogue reveals character; it does not dump information*

> "People remember how a line made them feel, not the words."

## How to Use

Pair a `VOICE_` profile (who is speaking) with a `DLG_` pattern (what kind of exchange). Every line carries emotion, breathing, and a pause. Request lip sync where the model supports it. Keep Shorts dialogue to one exchange with room for reactions.

## Voice Profiles

**`VOICE_CHILD_001` — Young Child.** Medium-high pitch, warm, moderate speed, simple vocabulary, honest emotion, irregular excited breathing.
**`VOICE_ADULT_001` — Grounded Adult.** Balanced pitch, confident, varied pacing, pauses before decisions.
**`VOICE_ELDER_001` — Wise Elder.** Slower rhythm, measured breath, thoughtful pauses, gentle emphasis.
**`VOICE_HERO_001` — Hero.** Hope, conviction, clarity, natural leadership, steady warmth.
**`VOICE_VILLAIN_001` — Restrained Villain.** Slow, calm, controlled, quiet confidence (power through restraint, not volume).
**`VOICE_NARRATOR_001` — Deep Male Narrator.** Warm, resonant, unhurried, mythic gravity; the house narrator for LONG and SHORTS.

## Dialogue Patterns

**`DLG_GREET_001` — Greeting.** Warm open, eye contact, small smile after the line.
**`DLG_DISCOVER_001` — Discovery.** Hushed wonder, inhale before speaking, trailing awe.
**`DLG_WARN_001` — Warning.** Low urgency, clipped rhythm, glance toward the threat.
**`DLG_ENCOURAGE_001` — Encouragement.** Gentle rise, supportive tone, reassuring pause.
**`DLG_COMFORT_001` — Comfort.** Soft, slow, close, protective.
**`DLG_CELEBRATE_001` — Celebration.** Bright, fast, laughter breaks, shared joy.
**`DLG_FAREWELL_001` — Farewell.** Quiet, warm, a beat of silence before the last word.

## Narrator Styles

**`NARR_MYTH_001` — Mythic Opener.** "Long before the rivers had names…" — slow, reverent, sets scale.
**`NARR_HOOK_001` — Shorts Hook.** One line in the first second that poses a question the payoff answers.
**`NARR_CLOSE_001` — Warm Close.** A single reflective line over the final hero shot (the SHORTS end voiceover).

## Lip Sync

Request accurate phoneme sync: natural jaw motion, lip closure on consonants, tongue when visible, breathing on pauses, no robotic mouth. Leave reaction time between lines; do not overpack dialogue.

## DIALOGUE Block Template

```
DIALOGUE: speaker <VOICE_ID> · emotion <x> · line "<text>" · tone <y> · speed <z> ·
          breathing <inhale before> · pause <before final beat> · reaction <after line> ·
          lip sync <natural, accurate>
```

## Golden Rule

If a line can be cut without changing the story or the feeling, cut it — and let a look, a breath, or the narrator carry the moment instead.

---

# Chapter 10 — The Audio, Foley & Music Preset Library

*If the audience closes their eyes, they should still understand the scene*

> "The audience believes what they hear before they understand what they see."

## How to Use

Layer audio by hierarchy: dialogue → breathing → character Foley → object Foley → environmental Foley → ambience → weather → music → effects. Keep dialogue intelligible over music unless the story intentionally obscures it. Silence is a deliberate tool.

## Foley — Human & Animal

**`FOLEY_STEP_WOOD`** — indoor steps: heel contact, wood resonance, soft clothing. **`FOLEY_STEP_GRASS`** — outdoor: soft compression, leaves, breathing. **`FOLEY_STEP_WET`** — action: splashes, impact, heavy breath. **`FOLEY_HUG`** — clothing friction, gentle breath, emotional pause.
**`FOLEY_DOG_WALK` (Maani)** — soft paws, light breath, gentle collar, occasional sniff. **`FOLEY_DOG_PLAY`** — fast paws, tail wag, happy panting, soft bark. **`FOLEY_HORSE_GALLOP`** — rhythmic hooves, leather saddle, breath, ground vibration. **`FOLEY_BIRD_FLIGHT`** — wing beats, air displacement, occasional call.

## Foley — Objects

**`FOLEY_DOOR_WOOD`** — handle, hinge, closing resonance. **`FOLEY_SWORD_METAL`** — draw, swing, impact, sheath. **`FOLEY_BACKPACK`** — zip, fabric, buckle, weight shift. **`FOLEY_GLASS`** — tap, slide, break, reflectionless clarity.

## Ambience & Weather

**`AMB_FOREST`** — birds, wind, leaves, stream, insects, distant woodpecker. **`AMB_VILLAGE`** — temple bells, children, animals, market, cooking. **`AMB_CITY`** — traffic, metro, crowds, sirens, HVAC. **`AMB_OCEAN`** — waves, gulls, wind, harbour.
**`WX_RAIN_LIGHT`** — soft roof, leaves, puddles, gentle thunder. **`WX_STORM`** — strong wind, thunder, rain, debris, tree movement. **`WX_SNOW`** — quiet ambience, crunch, cold wind. **`WX_DESERT_WIND`** — sand movement, gusts, low-frequency wind, silence between.

## Music by Emotion

**`MUS_ADVENTURE`** — strings, French horn, percussion; discovery. **`MUS_FANTASY`** — choir, harp, flute; wonder. **`MUS_CHILDREN`** — ukulele, piano, bells; joy. **`MUS_DRAMA`** — solo piano, cello, strings; reflection. **`MUS_SPORTS`** — percussion, brass, electronic drive; energy. **`MUS_MYTH`** — choir, traditional instruments, deep percussion; destiny.

## Silence & Spatial

**`SIL_REVEAL`** — a beat of silence before a major reveal. **`SIL_LOSS`** — held silence around an emotional low. **`SPATIAL_FOREST`** — birds above, stream left, wind behind, footsteps centre. **`SPATIAL_STADIUM`** — crowd surrounds, commentary front, action follows.

## Audio Mixing Matrix

| Priority | Layer |
|---|---|
| 1 | Dialogue |
| 2 | Breathing |
| 3 | Critical Foley |
| 4 | Environmental Foley |
| 5 | Ambience |
| 6 | Weather |
| 7 | Music |
| 8 | Effects |

## AUDIO Block Template

```
AUDIO: dialogue <clear> · breathing <synced> · Foley <FOLEY_IDs> · ambience <AMB_ID> ·
       weather <WX_ID> · music <MUS_ID, evolves> · silence <where> · mix <dialogue over music>
```

## Golden Rule

Every sound answers four questions: what made it, where is it, why does it matter, how should it feel. If a sound has no narrative or environmental purpose, cut it.


# Chapter 11 — The Color Grade Preset Library

*Colour is silent dialogue*

> "Before the audience understands the story, they feel its colours."

## How to Use

Each `GRADE_` preset is a look you name in VISUAL STYLE and hold across the film. Colour follows story, not decoration: choose the palette that carries the emotion, preserve believable skin tones, and let the palette evolve as the story evolves.

## Grade Looks

**`GRADE_DOC_001` — Natural Documentary.** Accurate colour, moderate contrast, preserved highlights, realistic skin.
**`GRADE_ADV_001` — Hollywood Adventure.** Warm highlights, cool shadows, rich greens, wide dynamic range.
**`GRADE_FANTASY_001` — Fantasy Cinema.** Soft bloom, enhanced saturation, warm magical glow, gentle contrast.
**`GRADE_NOIR_001` — Neo-Noir.** High contrast, deep blacks, selective highlights, muted palette.
**`GRADE_LUX_001` — Luxury Commercial.** Clean whites, controlled highlights, premium skin, perfect product colour.
**`GRADE_KIDS_001` — Children's Bright.** High saturation, warm primaries, soft contrast, readable and cheerful.
**`GRADE_MYTH_001` — Mythic Gold.** Gold and amber highlights, deep jewel shadows, sacred warmth.
**`GRADE_SCIFI_001` — Clean Future.** Cool blues and cyans, clean whites, controlled contrast, subtle magenta accents.

## Colour by Emotion

**`GRADE_EMO_HOPE`** — golden yellow, warm orange, soft green, sky blue. **`GRADE_EMO_MYSTERY`** — deep blue, cool grey, silver, dark cyan. **`GRADE_EMO_DANGER`** — deep red, black, dark orange. **`GRADE_EMO_PEACE`** — light blue, white, soft green, warm beige. **`GRADE_EMO_MAGIC`** — purple, gold, turquoise, pink.

## Seasonal Palettes

**Spring** — fresh green, blossom pink, light blue, warm yellow (growth). **Summer** — bright blue, golden sand, deep green, white cloud (energy). **Autumn** — orange, brown, red, golden leaves (memory). **Winter** — blue, white, grey, silver (silence).

## Skin Tone & Continuity

Every grade preserves natural skin hue, healthy saturation, and consistent appearance between shots. Hold wardrobe colours, environment palette, and mood progression across connected shots; change the grade only when time or location changes.

## VISUAL STYLE Block Template

```
VISUAL STYLE: render <one style> · grade <GRADE_ID> · contrast <level> · saturation <intent> ·
              skin tones <preserved> · palette progression <act-by-act> · continuity <hold>
```

## Golden Rule

Do not ask "what colour looks best." Ask what the audience should feel, which palette says it, and how the colour shifts as the emotion shifts.

---

# Chapter 12 — The VFX & Atmosphere Preset Library

*Effects convince; they do not announce themselves*

> "The audience should remember the emotion — not the effect."

## How to Use

Each `FX_` preset has a narrative purpose and believable physics. Scale density to the scene: minimal for dialogue, layered for fantasy, high for epic beats, reduced for quiet endings. Effects should interact with light, characters, and environment.

## Atmospheric

**`FX_MIST_001` — Morning Mist.** Mystery, wonder — thin ground fog, slow drift, localised, low density.
**`FX_FOG_001` — Dense Fog.** Suspense, isolation — limited visibility, soft silhouettes, volumetric light.
**`FX_DUST_001` — Dust Motes.** Age, memory — slow float, visible in light beams, natural randomness.
**`FX_SMOKE_001` — Smoke.** Fire, battle — directional drift, turbulence, light interaction.
**`FX_STEAM_001` — Steam.** Urban, sci-fi — warm vapour, vertical rise, condensation.

## Weather & Nature

**`FX_RAIN_LIGHT`** — droplets, wet surfaces, ripples, hair/cloth response. **`FX_RAIN_HEAVY`** — reduced visibility, splashes, flowing water, wind. **`FX_SNOWFALL`** — multiple flake sizes, wind influence, soft accumulation. **`FX_SANDSTORM`** — dust, low visibility, flying debris.
**`FX_LEAVES`** — autumn drift, random rotation, depth variation. **`FX_PETALS`** — romance, celebration; soft rotation. **`FX_FIREFLIES`** — wonder, children; random flight, soft glow, clustering. **`FX_BUTTERFLIES`** — peace; irregular flight, flower interaction.

## Water, Fire, Electrical

**`FX_WAVES`** — wind-driven rhythm, foam, spray. **`FX_RIVER`** — current, ripples, rock interaction. **`FX_SPLASH`** — impact matches force, droplet variation. **`FX_FIRE_CAMP`** — variable flames, embers, smoke, heat distortion. **`FX_TORCH`** — small flame, wall illumination, wind response. **`FX_LIGHTNING`** — irregular timing, natural branching, sky flash, thunder delay. **`FX_SPARKS`** — short, random direction, brightness variation, smoke.

## Fantasy & Sci-Fi

**`FX_HEAL_AURA`** — soft golden glow, floating particles, gentle pulses. **`FX_PORTAL`** — energy ring, light distortion, floating debris, ground illumination. **`FX_SHIELD`** — semi-transparent energy, ripple, refraction, impact waves. **`FX_RUNES`** — glowing symbols, slow rotation, dust interaction. **`FX_HOLOGRAM`** — semi-transparent, scan lines, subtle flicker, correct perspective. **`FX_WARP`** — star streaks, energy distortion, blue-white glow.

## Density Guide

| Scene | Density |
|---|---|
| Dialogue | Minimal |
| Adventure | Moderate |
| Fantasy | Layered |
| Epic beat | High |
| Quiet ending | Reduced |

## VFX Block Template

```
VFX: <FX_IDs> · purpose <narrative reason> · physics <gravity/wind/light interaction> ·
     density <per scene> · characters respond <wet/hair/dust> · continuity <hold>
```

## Golden Rule

Every effect earns its place with a story reason and believable physics. Rain wets clothes, wind moves hair, fire casts moving light — the world reacts, and the effect disappears into the scene.

---

# Chapter 13 — The Transition & Editing Preset Library

*The best edit is the one the audience never notices*

> "Cut because the story moves — not because time has passed."

## How to Use

Each `TRANS_` preset joins two shots for a reason. Choose an editing rhythm by genre and hold it. Every cut answers: what new information, what emotional change, does the audience still know where to look.

## Transitions

**`TRANS_WHIP_001` — Whip Pan.** Action, comedy — fast motion blur hides the cut; the next shot begins mid-blur.
**`TRANS_WIPE_001` — Foreground Wipe.** Invisible edit — a passing object (tree, pillar, person, vehicle) fills frame, revealing a new location.
**`TRANS_LIGHT_001` — Light Transition.** Dream, hope — camera passes through sun, flare, window, or portal.
**`TRANS_SHADOW_001` — Shadow Transition.** Mystery, horror — into darkness, screen dark, out to a new place.
**`TRANS_WATER_001` — Water Transition.** Travel, nature — through waterfall, wave, or splash.
**`TRANS_MATCH_001` — Object Match.** Visual storytelling — a lantern becomes the sun; a shape carries across the cut.
**`TRANS_AUDIO_001` — Audio Bridge.** The next scene's sound starts before the visual cut, priming the location.
**`TRANS_ENV_001` — Environmental.** Natural progression — clouds → night; leaves → snow; rain → sun.

## Editing Rhythm by Genre

**`EDIT_DOC`** — long observations, minimal cutting, breathing room (5–15s shots). **`EDIT_FAMILY`** — discovery → reaction → movement → emotion → resolution. **`EDIT_ACTION`** — build → impact → reaction → recovery; readable geography, never constant intensity. **`EDIT_KIDS`** — simple, bright, positive: question → discovery → joy → ending. **`EDIT_COMMERCIAL`** — hook → product → benefit → emotion → brand.

## Time & Pacing

**`TIME_REAL`** — natural observation. **`TIME_COMPRESS`** — journey/montage: walk → mountain → camp → sunset. **`TIME_EXPAND`** — slow the emotional peak so details land. **`PACE_WONDER`** — quiet → discovery → pause → smile → music → hero shot. **`PACE_SUSPENSE`** — question → silence → movement → pause → reveal.

## Shorts, Trailer & Montage

**`STRUCT_SHORTS`** — 0–1s hook · 1–3s question · 3–8s discovery · 8–12s conflict · 12–15s payoff + strong final image. **`STRUCT_TRAILER`** — hook → mystery → character → conflict → epic beat → silence → title → final hook (never reveal the whole story). **`MONTAGE_JOURNEY`** — walk → landscape → camp → sunrise → destination. **`MONTAGE_GROWTH`** — child → learning → helping → confidence → hero.

## Genre Editing Matrix

| Genre | Style | Rhythm |
|---|---|---|
| Adventure | Balanced | Moderate |
| Documentary | Observational | Slow |
| Sports | Dynamic | Fast |
| Fantasy | Emotional | Moderate |
| Comedy | Timing-based | Fast |
| Romance | Gentle | Slow |
| Shorts | Hook-driven | Very fast |

## Golden Rule

Great editing follows the rhythm of story, emotion, performance, and attention — not flashy transitions. If a cut has no reason, it does not belong.


# Chapter 14 — The Adventure & Fantasy Pack

*Wonder, discovery, and worlds worth exploring*

> "Adventure is a feeling before it is a plot: the sense that something waits just ahead."

## Default Preset Stack

Assemble adventure/fantasy productions from these defaults, then adapt:

```
CAMERA    CAM_TRACK_001 / CAM_DRONE_003 / CAM_ORBIT_002
LIGHTING  LIGHT_GOLDEN_001 (adventure) · LIGHT_GENRE_002 Sacred Glow (fantasy)
ENV       ENV_FOREST_001 / ENV_MOUNTAIN_001 / ENV_FANTASY_001
PERF      PERF_WALK_002 / PERF_REACT_001 · creatures: PERF_DRAGON_001
AUDIO     AMB_FOREST · MUS_ADVENTURE / MUS_FANTASY
GRADE     GRADE_ADV_001 / GRADE_FANTASY_001
FX        FX_MIST_001 · FX_FIREFLIES · FX_HEAL_AURA (magic)
TRANS     TRANS_WIPE_001 · TRANS_LIGHT_001
```

## Story Engines

**Adventure:** ordinary life → invitation → decision → journey → obstacle → discovery → victory → return, changed. **Fantasy:** ancient world → a small wonder → a threshold crossed → a trial of courage → transformation → balance restored. Keep magic consistent to its own rules.

## Example Clip

```
REF IMAGES: @character_sheet + @storyboard + @environment_ref

Awe and courage. Fantasy cinema, GRADE_FANTASY_001. A young explorer (locked identity) steps
onto a stone bridge above a cloud sea toward a floating temple (ENV_FANTASY_001). Wide reveal,
subject small against scale. LIGHT_GENRE_002 sacred glow, god rays, warm bloom. CAM_CRANE_001
epic rise, 24mm, slow, held hero frame. VFX: FX_MIST_001, drifting motes. SFX: wind, distant
chimes. NARRATOR (VOICE_NARRATOR_001): "Some places wait a thousand years for the right footstep."
ON-SCREEN TEXT: none. Watermark: "CREATED BY AVIK STUDIO" — small subtle gold, lower-center.
```

## Do / Don't

Do: one wonder per shot, motivated magic light, epic scale balanced with a human face. Don't: overload the frame, chain multiple actions, let magic appear without affecting the environment.

---

# Chapter 15 — The Mythology Production Pack

*Authentic, lesser-known legends — cinematic, all-ages, non-graphic*

> "Keep the reverence. Move the danger into light."

## Moderation-Safe Deity Render Library

Do **not** put worshipped-deity proper names or sacred terms inside generation prompts; describe by visual attributes instead (keep the real names in the YouTube title / description / pinned comment, which are text metadata and not moderated):

- **Shiva** → "majestic blue-skinned celestial lord, matted hair with a glowing crescent-moon ornament, a flowing water-strand, glowing forehead mark, serpent at the neck, three-pronged trident, ash-pale skin."
- **Yama** → "towering dark blue-grey celestial underworld king, glowing amber eyes, tall golden crown, crimson robes, riding a giant black buffalo."
- **Indra** → "radiant crowned celestial king in golden armor holding a thunderbolt."
- **Vishnu** → "serene blue-skinned celestial protector, four arms bearing a conch, a spinning discus, a mace and a lotus, golden crown, yellow silks."
- **Brahma** → "serene elder celestial creator with four faces and a white beard, seated on a great lotus, holding sacred scrolls."
- **Ganesha** → "gentle elephant-headed celestial child-figure, rounded form, small axe and lotus, a bowl of sweets, a tiny mouse companion."
- **Hanuman** → "powerful noble monkey-faced celestial warrior, orange fur, golden mace, devoted expression."
- **Durga** → "radiant celestial warrior queen with many arms bearing weapons, riding a great lion, serene and powerful."
- **lingam** → "a sacred glowing rounded stone pillar on a round base."

## Safe-Word Swaps

noose → "glowing coil/loop of light" · death/die → "fade / his time ends / the end" · "God of Death" → "the Underworld King" · kill/slay → "defeat/banish in light" · bones → "life-force/light" · demon → "shadow-beast / shadow serpent" · violent → "powerful/great" · dying → "fading." Human character names (Markandeya, Nachiketa, Agastya, Dadhichi, Vritra) are fine in prompts.

## Child + Darkness Rule (strongest blocker)

Never place a child near death, afterlife, or dark-ominous imagery in the same shot. Children are always bright, confident, safe; the underworld/afterlife renders as "palaces of light," never dark. Avoid a child "in fierce meditation," explicit minor ages ("a young boy," not "boy about 15"), and distress words (weeping, tear, beg, alone).

## Default Preset Stack

```
CAMERA    CAM_CRANE_002 / CAM_ORBIT_001 / CAM_DRONE_002
LIGHTING  LIGHT_GENRE_002 Sacred Glow · LIGHT_FIRE_001
ENV       ENV_TEMPLE_001 · ENV_MOUNTAIN_001 · palaces of light
PERF      PERF_MICRO_RESOLVE · majestic, calm, powerful bearing
AUDIO     MUS_MYTH · choir + traditional instruments · SIL_REVEAL
GRADE     GRADE_MYTH_001 Mythic Gold
FX        FX_RUNES · FX_HEAL_AURA · FX_PORTAL (palaces of light)
NARRATOR  NARR_MYTH_001 (VOICE_NARRATOR_001)
```

## Example Clip

```
REF IMAGES: @character_sheet + @storyboard + @style_ref

Reverent and grand. Mythic cinema, GRADE_MYTH_001. A young sage-boy (bright, confident, safe)
stands in a hall of golden light before a towering dark blue-grey celestial underworld king with
glowing amber eyes, tall golden crown and crimson robes. Wide low hero framing. LIGHT_GENRE_002
sacred glow, god rays, warm bloom (palace of light, never dark). CAM_CRANE_002 reveal rise, 35mm,
slow, held hero frame. VFX: FX_RUNES drifting, warm motes. SFX: deep resonance, distant choir.
NARRATOR: "The boy did not fear the Underworld King — he asked him a question no one had dared."
ON-SCREEN TEXT: none. Watermark: "CREATED BY AVIK STUDIO" — small subtle gold, lower-center.
```

## Retry Ladder

If a prompt is blocked: (1) delete NARRATOR/DIALOGUE and generate visuals only; (2) strip to a bare scene-only prompt, then add detail back; (3) retry or switch model — moderation is partly probabilistic.

---

# Chapter 16 — The Robots & Science-Fiction Pack

*Technology with wonder, scale with clarity*

> "Sci-fi convinces when its technology has weight, purpose, and consistent rules."

## Default Preset Stack

```
CAMERA    CAM_STATIC_001 (clean) · CAM_TRACK_002 · CAM_FPV_002 · CAM_DRONE_002
LIGHTING  LIGHT_GENRE_003 Clean Sci-Fi · LIGHT_GENRE_001 Cyberpunk Neon (urban)
ENV       ENV_SCIFI_001 Mars · ENV_SCIFI_002 Orbital · ENV_CITY_002 Cyberpunk · ENV_LAB_001
PERF      robot: servo-precise, purposeful · human: PERF_MICRO_RESOLVE
AUDIO     engine hum, servos, interface tones · MUS_ADVENTURE (heroic) · MUS_DRAMA
GRADE     GRADE_SCIFI_001 Clean Future
FX        FX_HOLOGRAM · FX_WARP · FX_SPARKS · FX_STEAM_001
```

## Story Engines

Discovery of a new world; a machine that learns loyalty; a rescue against a countdown; first contact. Keep the technology internally consistent — a device that glows blue in one shot glows blue in all.

## Example Clip

```
REF IMAGES: @character_sheet + @storyboard + @environment_ref

Tense wonder. Clean future, GRADE_SCIFI_001. A small service robot (locked identity: panel lines,
blue edge lights) powers up a failing reactor core aboard an orbital station (ENV_SCIFI_002).
Medium shot, subject frame-right. LIGHT_GENRE_003 LED panels, blue edge light, metallic reflections.
CAM_PUSH_001 slow push, 50mm, held hero frame as the core stabilises. VFX: FX_HOLOGRAM readout,
FX_SPARKS settling. SFX: servos, rising hum, interface chime. NARRATOR: "It was built to follow
orders. Tonight it chose to save them." ON-SCREEN TEXT: none. Watermark: "CREATED BY AVIK STUDIO"
— small subtle gold, lower-center.
```

## Do / Don't

Do: motivate every light source, keep contrast controlled, give machines readable intention. Don't: scatter random coloured lights, chain actions, let holograms ignore perspective.

---

# Chapter 17 — The Children & Family Pack

*Safety, wonder, friendship, and hope*

> "Bright, clear, kind — and never a child near darkness."

## Default Preset Stack

```
CAMERA    CAM_STATIC_003 (readable) · CAM_TRACK_001 · CAM_DLG_003 Two Shot · gentle CAM_PUSH_002
LIGHTING  LIGHT_GOLDEN_001 · warm interiors · LIGHT_ELEM_002 Snow Morning
ENV       ENV_HOME_001 · ENV_VILLAGE_001 · ENV_BEACH_001 · ENV_FOREST_001
PERF      PERF_CHILD_001/002 · PERF_DOG_001/002 (Maani) · PERF_MICRO_HAPPY
AUDIO     AMB_VILLAGE · MUS_CHILDREN · warm laughter
GRADE     GRADE_KIDS_001 Bright
FX        FX_FIREFLIES · FX_BUTTERFLIES · FX_PETALS
```

## Safety Rules

Children are always bright, confident, and safe; keep them away from darkness, danger, and distress imagery. Frame the son only from behind / back to camera, face never visible. Apply the Maani anatomy note in every Maani block. Keep dialogue short, clear, positive, and age-appropriate.

## Example Clip

```
REF IMAGES: @character_sheet + @storyboard + @environment_ref

Joyful and warm. Bright family style, GRADE_KIDS_001. A young child (shown from behind, face not
visible) and a tricolour beagle (identity: MAANI; Maani anatomy note applied) chase fireflies in a
sunlit garden (ENV_HOME_001). CAM_TRACK_001 side track, 35mm, gentle, held hero frame as they laugh.
LIGHT_GOLDEN_001 warm key, soft fill, sparkle. VFX: FX_FIREFLIES. SFX: giggles, evening birds, soft
breeze. NARRATOR (VOICE_NARRATOR_001): "The best adventures start in your own backyard." DIALOGUE:
none. ON-SCREEN TEXT: none. Watermark: "CREATED BY AVIK STUDIO" — small subtle gold, lower-center.
```

## Golden Rule

If it would frighten a small child watching alone, it does not belong. Wonder, kindness, and a hopeful ending — every time.

---

# Chapter 18 — The Shorts Hook & Retention Pack

*Fifteen seconds that earn a rewatch*

> "Fit more meaning into fifteen seconds — not more story."

## The 15-Second Structure

```
0–1s   Visual hook (motion, mystery, or a striking image) + a one-line question
1–3s   Curiosity — establish who/where fast
3–8s   Discovery — the turn
8–12s  Conflict or escalation
12–15s Payoff + a memorable final hero image (warm end voiceover)
```

## Hook Library

**`HOOK_QUESTION`** — narrator poses a question the payoff answers. **`HOOK_MOTION`** — open on unexpected movement toward camera. **`HOOK_REVEAL_TEASE`** — show a fragment of the wonder, withhold the whole. **`HOOK_STAKES`** — one line that makes the next 14 seconds matter. **`HOOK_CUTE`** — Maani does one irresistible beat in the first second.

## Retention Tactics

One focal subject per shot; no dead frames; a curiosity question left open until the payoff; motion that leads the eye; a strong final image that rewards the watch. Keep on-screen text off the story clips; keep the tagline and Subscribe in the End Sting only.

## Example Shorts Block

```
REF IMAGES: @character_sheet + @storyboard

Playful mystery. Bright style, GRADE_KIDS_001. (0–3s) A tricolour beagle (identity: MAANI; anatomy
note applied) freezes, one ear up, staring at a glowing door in a hedge (HOOK_MOTION). (3–8s) The
door opens on a rainbow-lit tunnel; she peers in, tail high. (8–12s) A gentle gust of light-motes
swirls out. (12–15s) She steps through into a meadow of floating lanterns — held hero frame.
CAM_PUSH_002 discovery push, 35mm. LIGHT_GENRE_002 sacred glow. VFX: FX_FIREFLIES, FX_PORTAL (soft).
SFX: curious sniff, soft chimes. NARRATOR (VOICE_NARRATOR_001), warm close: "Some doors only open
for the brave." ON-SCREEN TEXT: none. Watermark: "CREATED BY AVIK STUDIO" — small subtle gold,
lower-center.
```

## Golden Rule

Win the first second, hold one question, land one image. A tight story with a strong character beats a busy sequence that tries to do everything.


# Chapter 19 — Maani Adventures — Series Pack

*The beagle, the boy, and worlds made of wonder (Series A)*

> "Family is the first universe. Everything else orbits it."

## Cast & Identity Anchors

Always lock identity to the series reference sheets (`@character_sheet`); the anchors below are the baseline.

- **Maani** — female tricolour beagle; soft brown/black/white coat pattern (held); long velvet ears; gentle brown eyes; light collar; natural pacing, nose leads; loyal, curious, playful. **Anatomy note (every Maani block):** Maani is FEMALE — smooth, featureless underbelly, no genitalia ever visible; frame side-on or upright (never belly-up); jumps low and modest, no belly-exposing mid-air poses.
- **Sarvik** — the boy companion; **shown only from behind / back to camera, face never visible**; bright, curious, safe.
- **Recurring wonders** — the **Rainbow Serpent Bus** (a friendly, luminous serpentine vehicle that carries them between worlds) and the **Nebula Leviathan** (a vast, gentle cosmic creature of starlight). Keep each visually consistent across appearances.

## Recommended Stacks

```
Everyday/warm   GRADE_KIDS_001 · LIGHT_GOLDEN_001 · ENV_HOME_001/ENV_VILLAGE_001 · MUS_CHILDREN
Adventure       GRADE_ADV_001 · CAM_TRACK_004 (Maani) · ENV_FOREST_001/ENV_MOUNTAIN_001 · MUS_ADVENTURE
Cosmic wonder   GRADE_FANTASY_001 · LIGHT_GENRE_002 · Nebula Leviathan · FX_HEAL_AURA · MUS_FANTASY
```

## Example Clip

```
REF IMAGES: @character_sheet + @storyboard + @environment_ref

Warm wonder. Bright style, GRADE_FANTASY_001. Maani (identity: MAANI; anatomy note applied) and the
boy (shown from behind, face not visible) ride the luminous Rainbow Serpent Bus over a sea of clouds
toward the gentle Nebula Leviathan drifting in starlight. Wide reveal, subjects small against scale.
LIGHT_GENRE_002 sacred glow, warm bloom. CAM_CRANE_001 epic rise, 24mm, held hero frame. VFX:
FX_HEAL_AURA motes, drifting stars. SFX: soft cosmic hum, Maani's happy panting. NARRATOR
(VOICE_NARRATOR_001): "Wherever Maani goes, the boy is never far behind." ON-SCREEN TEXT: none.
Watermark: "CREATED BY AVIK STUDIO" — small subtle gold, lower-center.
```

## Series Notes

Series A in the Shorts numbering. Recurring leads and wonders may return; only the specific premise/event must never repeat (see Ch26).

---

# Chapter 20 — The Infinity Trap — Dual-Continuity Pack

*Two continuities, kept separate on purpose (Series E)*

> "Same name, two worlds. Never let them bleed."

## The Two Continuities

- **Long-form continuity — Vihaan + Ananta.** A human pair navigate an endless shifting **labyrinth** (the Infinity Trap): corridors that rearrange, rooms that repeat, a structure that tests memory and resolve. Tone: cinematic, cerebral, suspenseful but non-graphic.
- **Shorts continuity — Maani's 7-Gate Saga.** A Maani-led arc through **seven gates**, each a self-contained trial with a bright, hopeful resolution. Tone: adventurous, all-ages, wonder-forward.

Keep the two strictly separate: different leads, different visual identity, no crossover of specific events.

## Identity Anchors

- **Vihaan / Ananta** — lock to `@character_sheet`; grounded adventurers, expressive under pressure. **Ananta the labyrinth** reads as vast, geometric, softly ominous but never dark-oppressive.
- **Maani (7-Gate)** — identity: MAANI (anatomy note applied); each gate glows a distinct colour so audiences track progress.

## Recommended Stacks

```
Labyrinth (long)  GRADE_NOIR_001 (softened) · LIGHT_STUDIO_004 Split · ENV geometric corridors ·
                  FX_FOG_001 · PACE_SUSPENSE · MUS_DRAMA
7-Gate (Shorts)   GRADE_FANTASY_001 · LIGHT_GENRE_002 · one signature colour per gate ·
                  FX_PORTAL/FX_RUNES · STRUCT_SHORTS · MUS_ADVENTURE
```

## Example — Shorts (7-Gate)

```
REF IMAGES: @character_sheet + @storyboard

Brave curiosity. Fantasy style, GRADE_FANTASY_001. (0–3s) Maani (identity: MAANI; anatomy note
applied) faces the Third Gate — a tall archway glowing emerald (HOOK_MOTION). (3–8s) Runes brighten
as she steps forward, ears alert. (8–12s) The gate resolves a simple trial of courage in light.
(12–15s) It opens to a meadow beyond — held hero frame, tail high. CAM_PUSH_002, 35mm. LIGHT_GENRE_002
sacred glow, emerald key. VFX: FX_RUNES, FX_PORTAL (soft). SFX: chimes, a determined little bark.
NARRATOR (VOICE_NARRATOR_001), warm close: "Six gates to go — and Maani fears none of them."
ON-SCREEN TEXT: none. Watermark: "CREATED BY AVIK STUDIO" — small subtle gold, lower-center.
```

## Series Notes

Series E. Track the two continuities separately in the do-not-repeat catalog so a long-form beat never collides with a Shorts gate.

---

# Chapter 21 — Neo-Vega — Robots & Transformers Pack

*Guardians of a neon city (Series C)*

> "Machines that choose loyalty are the ones audiences love."

## Cast & Identity Anchors

Lock to `@character_sheet`; baseline below.

- **Bolt** — an agile, good-hearted guardian robot; readable expressive optics; clean panel lines; a signature accent colour (held).
- **Aegis Prime** — the larger, steadfast protector; heavier build, calm authority, a warm core-light.
- **Neo-Vega** — the neon metropolis they protect: glass towers, holographic signage, rain-wet streets, hover traffic.

Canon note: **"Guardians of Neo-Vega"** is the **power-core RESCUE** short (Bolt & Aegis recover/stabilise a failing core) — **not** an awakening/origin pilot.

## Recommended Stack

```
CAMERA    CAM_TRACK_002 · CAM_FPV_002 · CAM_DRONE_002 (city) · CAM_PUSH_001 (core moment)
LIGHTING  LIGHT_GENRE_001 Cyberpunk Neon · LIGHT_GENRE_003 Clean Sci-Fi (interiors)
ENV       ENV_CITY_002 Cyberpunk · ENV_LAB_001 (core chamber)
AUDIO     servos, hum, interface tones · MUS_ADVENTURE (heroic) · SIL_REVEAL (core stabilises)
GRADE     GRADE_SCIFI_001 Clean Future
FX        FX_HOLOGRAM · FX_SPARKS · FX_STEAM_001 · FX_WARP (transit)
```

## Example Clip

```
REF IMAGES: @character_sheet + @storyboard + @environment_ref

Heroic urgency. Clean future, GRADE_SCIFI_001. Bolt (identity locked) sprints across a rain-wet
Neo-Vega rooftop toward the failing power core as Aegis Prime braces the collapsing gantry behind
him (ENV_CITY_002). Lead track, subject frame-centre. LIGHT_GENRE_001 neon key, wet reflections.
CAM_TRACK_002 then CAM_PUSH_001 on the core, 35mm, held hero frame as it steadies to warm gold.
VFX: FX_SPARKS settling, FX_HOLOGRAM readout. SFX: servos, rising hum, a deep stabilising chord.
NARRATOR (VOICE_NARRATOR_001): "Two guardians. One city. No margin for error." ON-SCREEN TEXT: none.
Watermark: "CREATED BY AVIK STUDIO" — small subtle gold, lower-center.
```

## Series Notes

Series C. Bolt, Aegis Prime, and Neo-Vega are shared canon and may recur; only the specific premise/event must never repeat.

---

# Chapter 22 — Skyhaven — Fantasy Worlds Pack

*A girl, a dragon, and a kingdom in the clouds (Series D)*

> "The bond is the story. The world is the stage."

## Cast & Identity Anchors

Lock to `@character_sheet`; baseline below.

- **Mira** — a brave, kind young heroine; expressive, agile; a signature garment colour (held). If shown as a child, keep her bright, confident, and safe.
- **Ember** — her dragon companion; warm-toned scales, gentle intelligent eyes, expressive wings; noble and protective (use `PERF_DRAGON_001` for motion).
- **Skyhaven** — a cloud-borne kingdom: floating islands, waterfalls into cloud, sky temples, lantern-lit terraces.

Canon note: the Fantasy Shorts premise is **"Mira & Ember and the Lost Cloud-Fawn"** (a rescue of a small lost sky-creature) — not "Heart of Skyhaven."

## Recommended Stack

```
CAMERA    CAM_ORBIT_002 · CAM_DRONE_003 · CAM_CRANE_001 · CAM_DLG_003 (Mira & Ember)
LIGHTING  LIGHT_GENRE_002 Sacred Glow · LIGHT_GOLDEN_001 · LIGHT_BLUE_001 (evening terraces)
ENV       ENV_FANTASY_001 Floating Islands · ENV_FANTASY_002 Crystal Kingdom
AUDIO     AMB_FOREST (sky-forest) · MUS_FANTASY · warm wingbeats
GRADE     GRADE_FANTASY_001 Fantasy Cinema
FX        FX_FIREFLIES · FX_HEAL_AURA · FX_PETALS · FX_MIST_001
```

## Example — Shorts (Lost Cloud-Fawn)

```
REF IMAGES: @character_sheet + @storyboard

Tender adventure. Fantasy cinema, GRADE_FANTASY_001. (0–3s) Mira (bright, confident) and Ember
(identity locked, PERF_DRAGON_001) spot a tiny glowing cloud-fawn stranded on a crumbling sky-ledge
(ENV_FANTASY_001) (HOOK_STAKES). (3–8s) Ember glides beneath as Mira reaches out. (8–12s) A gust
scatters light-petals; the fawn leaps to safety. (12–15s) The three rise together over Skyhaven —
held hero frame. CAM_ORBIT_002, 35mm. LIGHT_GENRE_002 sacred glow. VFX: FX_PETALS, FX_HEAL_AURA.
SFX: soft wingbeats, a relieved chirp, gentle chimes. NARRATOR (VOICE_NARRATOR_001), warm close:
"In Skyhaven, no one is ever truly lost." ON-SCREEN TEXT: none. Watermark: "CREATED BY AVIK STUDIO"
— small subtle gold, lower-center.
```

## Series Notes

Series D. Mira, Ember, and Skyhaven are shared canon and may recur; only the specific premise/event must never repeat.


# Chapter 23 — The Master Prompt Template Bank

*Fill-in blocks for every deliverable*

> "Never start from a blank page. Start from a proven block."

## Single Clip (six-dimension)

```
REF IMAGES: @character_sheet + @storyboard [+ @environment_ref / @style_ref / @prop_ref]

[Emotional tone]. [Render style + GRADE_ID]. [Subject + locked identity]. [Composition + shot size].
[Lighting: LIGHT_ID — key/fill/rim/atmosphere/colour temp]. [Camera: CAM_ID — lens/movement/speed,
held hero frame].
VFX: [FX_IDs]. SFX: [Foley/ambience]. NARRATOR (VOICE_NARRATOR_001): "[line]". DIALOGUE: [VOICE_ID / none].
ON-SCREEN TEXT: none. Watermark: "CREATED BY AVIK STUDIO" — small subtle gold, lower-center.
```

## LONG Package (16:9)

```
TITLE: [Episode Title]
CHARACTER & STYLE BIBLE: [identity locks · palette · GRADE_ID · world]
CLIP 1 (0–15s)  [setup]        — six-dimension block, ON-SCREEN TEXT: none
CLIP 2 (0–15s)  [development]  — six-dimension block, ON-SCREEN TEXT: none
CLIP 3 (0–15s)  [turn]         — six-dimension block, ON-SCREEN TEXT: none
CLIP 4 (0–15s)  [resolution]   — six-dimension block; render episode title as held closing card
                                 (sagas: "— To Be Continued")
TEASER (0–15s)  [strongest single image] — render "[Title] — Coming Soon"
INTRO STING (3s) · END STING (5s)   — the ONLY place the channel tagline + Subscribe appear
THUMBNAIL PROMPT + layout · YOUTUBE DESCRIPTION (chapters + hashtags) · PINNED COMMENT
```

## SHORTS Pack

```
SERIES [A–E] · Stories numbered continuously (track last-used number)
For each (~10 per pack):
  STORY N — [Title]
  Six-dimension SHORTS block with beats 0–3 / 3–8 / 8–12 / 12–15s, character-consistency line,
  baked-in sound design, warm end voiceover (NARR_CLOSE_001).
  YouTube title · description · hashtags.
```

## Intro / End Sting

```
INTRO STING (3s): neon "W" magenta→cyan logo reveal · tagline "Where AI Brings Legends To Life".
END STING (5s):   channel tagline + animated Subscribe cue + @avikstudioai.
```
(Keep both stings OUT of story clips; never render a Subscribe-button tap inside a scene — mangled hands.)

## Thumbnail Prompt (send to a text-reliable image model)

```
One clear subject · strong facial expression/emotion · high contrast · clean background ·
minimal text · title words legible on mobile · [episode hook] · brand accent (magenta→cyan).
```

## Golden Rule

Customise only what is unique to the story; let the template carry the rest. Consistent structure is what makes a channel feel like a studio.

---

# Chapter 24 — The Moderation-Safe & Continuity Compiler

*The pre-flight check every prompt passes before generation*

> "Catch the problem before the model does."

## Pre-Flight Order

Run these passes in order on every assembled prompt:

> Story clear → Identity locked → Moderation-safe → Generator-literalism → Continuity → QA score → Generate

## Pass 1 — Moderation-Safe

- No worshipped-deity proper names or sacred terms in the prompt — use the visual-attribute renders (Ch15). Real names live in metadata only.
- Apply the safe-word swaps (noose→coil of light; death→fade; kill→defeat in light; demon→shadow-beast; etc.).
- **Child + darkness:** never a child near death/afterlife/dark imagery in one shot; children bright and safe; afterlife = palaces of light; avoid explicit minor ages and distress words.

## Pass 2 — Generator-Literalism

- Animals "whole, healthy, alive, standing, full-body in frame." Render "giving" as "led away by rope" + "open empty hand" — never an animal/object "in hand."
- Infants "small bundle wrapped in cloth, shown only as gentle radiant light" — never a detailed newborn face.
- Liquids "into mouth" → "drawn upward into glowing form."
- Avoid characters handing objects to each other (limb fusion); safe prop: "glowing X floating beside him." Soften "clutching/embracing" → "carrying/holding." No AI Subscribe-tap.
- **Maani anatomy note** present in every Maani block.

## Pass 3 — Continuity

Hold across connected shots: character identity, wardrobe, hair, accessories, environment, weather, lighting direction, props, scale, emotional progression, audio bed. Change only when the story intends it.

## Pass 4 — QA Score

| Category | Weight | Category | Weight |
|---|---|---|---|
| Story | 20% | Environment | 10% |
| Character identity | 15% | Dialogue | 10% |
| Performance | 10% | Audio | 10% |
| Camera | 10% | Continuity | 10% |
| Lighting | 10% | Output/Rendering | 5% |

Target **90%+** before generation. Quality levels: Platinum 96–100 · Gold 90–95 (publish-ready) · Silver 80–89 · Bronze 70–79 · Prototype <70.

## Retry Ladder (on a block or a bad generation)

(1) Strip NARRATOR/DIALOGUE, generate visuals only. (2) Go scene-only, then add detail back. (3) Revise only the affected module. (4) Retry or switch model — moderation and quality are partly probabilistic.

## Golden Rule

The compiler protects the brand and the audience. A clip is not ready because it looks good — it is ready when it passes every pass.

---

# Chapter 25 — Publishing, Metadata & Thumbnail Systems

*The film is half the product; the package is the other half*

> "Metadata is where the real names, the reach, and the rewatch live."

## YouTube Metadata Templates

**LONG description**
```
[One-line hook]. In this episode, [character] [does what] — [emotional promise].

Chapters:
00:00 [Beat 1]
00:15 [Beat 2]
00:30 [Beat 3]
00:45 [Resolution]

#WonderCraftAI #AvikStudio #[Universe] #[Theme] #AIfilm #cinematic
```

**SHORTS description**
```
[Hook line] 🐾 [Series] · Story [N]
#Shorts #WonderCraftAI #[Universe] #[Theme] #AIshorts
```

**Pinned comment**
```
[Warm line inviting a reply] — which [world/character] should we visit next? 💫
[Real names, sources, or legend context go here — text metadata, not moderated.]
```

Real deity names and legend context belong in the **title / description / pinned comment**, never in the generation prompt.

## Thumbnail System

Generate thumbnails with a text-reliable image model (ChatGPT/DALL·E): one clear subject, strong emotion, high contrast, clean background, minimal legible title words, brand accent (magenta→cyan). Keep the composition readable at phone size; the thumbnail should pose the same curiosity question as the hook.

## Branding Placement

The channel tagline "Where AI Brings Legends To Life," the Subscribe cue, and the neon "W" logo live in the **Intro Sting (3s)** and **End Sting (5s)** only. Story clips carry only the small gold `"CREATED BY AVIK STUDIO"` watermark. Never repeat the generic tagline on story clips.

## Playlists & Series

Group uploads by universe (Maani Adventures, Infinity Trap, Neo-Vega, Skyhaven, Mythology) and tag the series letter (A–E). Consistent playlists and thumbnails compound a channel's identity over time.

## Golden Rule

Publish only after QA. The package — title, thumbnail, description, pinned comment, stings — should make the film easy to find, easy to click, and easy to rewatch.

---

# Chapter 26 — The Expansion Blueprint & Story-Numbering System

*How this seed library grows into the full encyclopedia*

> "Every shipped film should leave the library larger and smarter."

## The Growth Loop

```
Produce → QA → note what worked → add/upgrade presets → update packs → next production
```

Every approved camera move, lighting setup, grade, soundscape, performance, and template goes back in with a `DEPT_SUBTYPE_NNN` ID and a version. Never overwrite history — bump the version and record what changed.

## The Target Scale (roadmap)

This edition is a seed. Grow toward the full library by expanding each Part:

| Library | Seed (this volume) | Target |
|---|---|---|
| Camera | ~30 | 10,000+ |
| Lighting | ~25 | 5,000+ |
| Environment | ~25 | 3,000+ |
| Performance | ~25 | 5,000+ |
| Dialogue | ~20 | 5,000+ |
| Audio | ~30 | 2,000+ |
| Colour / VFX / Transitions | ~60 | thousands |
| Prompt modules / packs | ~40 | 20,000+ |

Expand by adding real, tested presets from shipped productions — not by padding. A smaller library of proven components beats a large one of untested guesses.

## Story-Numbering System

- **Series letters:** A = Maani · B = Hindu Mythology · C = Robots & Transformers · D = Fantasy Worlds · E = Infinity Trap.
- **Numbering:** stories are numbered **continuously across packs** — track the last-used number and continue from it (each Shorts pack is ~10 stories).
- **Two Infinity Trap continuities** (Vihaan+Ananta long-form; Maani 7-gate Shorts) are tracked separately so their beats never collide.

## The Do-Not-Repeat Catalog

Maintain a living catalog of every covered story so premises never repeat. Recurring leads and worlds (Maani & Sarvik, Bolt & Aegis / Neo-Vega, Mira & Ember / Skyhaven) are shared canon and may return — **only the specific premise/event must never repeat.** Record: story ID, series, title, one-line premise, characters, world, and date.

```
CATALOG ROW: [ID] · [Series A–E] · [Title] · [premise] · [characters] · [world] · [date] · [status]
```

## Closing

Volume I gave you the craft. Volume II gives you the parts and the system to reuse them. Keep the story first, lock identity, lead every clip with its reference images, respect the moderation-safe and canon rules, and let each production feed the library. Assemble, adapt, generate — the same way, to the same standard, every time.

---

*End of Volume II — The Avik Studio Prompt Encyclopedia. Expand each Part with your own tested presets and packs, and the Encyclopedia becomes the studio's permanent, compounding memory.*


