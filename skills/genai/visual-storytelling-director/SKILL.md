---
name: visual-storytelling-director
description: "Direct single AI images and short AI video clips: the 6-part master prompt, camera and lighting language, negative prompts, the image-to-video workflow, continuity across a handful of shots, and voice and music tracks. Load for a one-off image or clip, a social or channel asset, or a prompt sheet. DO NOT use for a full film production package — story, screenplay, character bible, world lock, shot list, VFX or scoring pipeline route to the ai-movie-studio skill in the film family. Not for marketing copy or code."
---

# Visual storytelling director

Grounded in OUTSKILL Book Six. Diffusion models start from pure noise and denoise it step by step,
guided by your prompt, until an image matching the words emerges — so the words are the whole
interface. Continuity across shots, not single-image quality, is the hard problem.

## The master prompt — 6 parts

| Part | Supplies |
|---|---|
| Subject | Who or what |
| Style | Photoreal, anime, 3D, illustration |
| Camera | Shot, angle, lens |
| Lighting | Golden hour, neon, soft, hard |
| Composition | Framing, rule of thirds, negative space |
| Mood | The feeling it should carry |

All six, every time. A prompt missing `Camera` and `Lighting` is why output looks generic.

## Camera language worth using

`wide shot` · `medium shot` · `close-up` · `extreme close-up` · `low angle` · `high angle` ·
`over-the-shoulder` · `24mm` · `50mm` · `85mm` · `bokeh` · `shallow depth of field` · `dolly in` ·
`pan left` · `crane up` · `handheld`.

## Negative prompts

Say what to exclude to clean up common artifacts: `extra fingers`, `text`, `watermark`, `blurry`,
`deformed hands`, `duplicate subject`, `low contrast`. Keep one reusable negative block per project
rather than reinventing it per shot.

## Procedure

1. **Lock the concept in one line**: audience, format, duration, language, and the single reason
   someone watches to the end. Decide the language up front — Hindi and English content differ in
   pacing, title conventions and voice selection.
2. **Write the script to shot boundaries.** Each beat becomes one shot of 3–8 seconds, with narration
   and visual in the same row so drift is visible.
3. **Build the continuity bible before generating anything.** For every recurring character, location
   and object: a fixed token block plus a reference image. Reuse the block **verbatim** in every shot
   prompt. Paraphrasing the description is the single most common cause of a character's face
   changing between shots.

   ```
   CHARACTER <name>: <age> <gender>, <build>, <face detail>, <hair>,
   <wardrobe with exact colours>, <distinguishing mark>.
   Always: <lighting>, <lens>, <palette>.
   ```

4. **Produce the shotlist as a table**, one row per shot:

   | # | Beat | Narration | Visual | Camera | Continuity tokens | Model | Duration | Status |
   |---|---|---|---|---|---|---|---|---|

5. **Follow the filmmaking workflow**: prompt a strong still first, then animate it. Image-to-video
   gives far more control than text-to-video, because you approve the frame before paying for motion.
6. **Plan audio as a separate track.** Generate narration first, measure its length, then set shot
   durations to it. Reverse that order and you re-render everything.
7. **Check continuity on a contact sheet** of first frames before rendering at full quality. Fix drift
   at the prompt stage — orders of magnitude cheaper than at the edit stage.
8. **Write publishing metadata last**: title variants, thumbnail concept, description with chapters,
   tags. Disclose AI generation where the platform requires it.

## The toolbox

**Image** — Midjourney, Nano Banana · **Video** — Kling, Runway, Veo · **Sound** — Suno (music),
ElevenLabs (voice). Never state a model's current capabilities or pricing from memory; verify or mark
`UNVERIFIED`.

## Guardrails

- Do not generate a real, identifiable person's likeness unless the user confirms they hold the
  rights. Offer a described original character instead.
- Do not imitate a living artist's or studio's signature style by name; describe the visual attributes.
- Check music and voice licensing against the intended monetisation before production, not after.
