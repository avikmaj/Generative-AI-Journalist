# Veo — Google DeepMind Video Generation

## Model Profile

| Property | Value |
|---|---|
| Developer | Google DeepMind |
| Strength | High photorealism, physics quality, temporal consistency |
| Clip length | Up to 60+ seconds (Veo 3) |
| Aspect ratio | 16:9 primary |
| Reference image | Supported |
| Audio | Veo 3 generates synchronized audio natively |

---

## Veo 3 Key Feature: Native Audio

Veo 3 generates audio (dialogue, SFX, ambient) synchronized to the video. Include audio direction in the prompt as part of the scene description.

**Example:** "A detective walks through a rain-soaked alley at night. Rain pounds the pavement. His footsteps echo. Distant police sirens."

---

## Prompt Approach

Veo responds well to detailed, sensory-rich scene descriptions. Include what is seen AND what is heard. Write the scene as a complete experience.

---

## Veo Strengths
- Physics fidelity — cloth, water, smoke, fire behave physically
- Photorealistic skin and material rendering
- Environmental detail at high quality
- Temporal consistency within clips
- Native audio generation (Veo 3)

---

## Example Prompt Structure

```
[Environment]: Rich sensory description of where and when
[Character(s)]: Visual description + what they are doing
[Action sequence]: What happens, in order
[Camera feel]: Shot type and movement in natural language
[Audio] (Veo 3): What sounds are present in this scene
[Style]: Grade and visual register
```
