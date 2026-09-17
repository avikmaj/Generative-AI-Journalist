# Movie Prompts — Feature Film Templates & Scene Formulas

## The Feature Film Prompt Package

A feature-length AI film is a series of scenes, each a discrete prompt package. Design the film architecture first, then generate scene by scene.

---

## Feature Film Prompt Package Structure

```
FILM TITLE:
GENRE:
LOGLINE:
VISUAL STYLE (held across film):
COLOUR GRADE (held across film):
SCORE CHARACTER (held across film):

CHARACTER ROSTER:
  [Name]: [identity token string]
  [Name]: [identity token string]

SCENE PACKAGE:
  Scene 1: [heading, location, time, story beat]
  Scene 2: ...
  [Continue through full film]
```

---

## Opening Scene Formula

The opening scene establishes: world, tone, and protagonist's status quo. Design it to also contain the thematic statement of the film.

```
OPENING SCENE PROMPT:
TONE: [the emotional world of this film stated immediately]
ENVIRONMENT: [world of the film — the specific, not the generic]
PROTAGONIST: [identity token], [their status at film start — where they are in life]
ACTION: [what they are doing when we first see them — this choice matters.
         The first image of a character is their defining image.]
CAMERA: [the camera approach that will characterize this film's visual style]
SOUND: [the sound world of this film at rest]
NO DIALOGUE FIRST: [let the audience read the world before anyone speaks]
THEMATIC NOTE: [what does this opening image say about the film's core theme?]
```

---

## Genre Scene Templates

### Crime Drama — The Discovery Scene

```
DETECTIVE: [identity token]
CRIME SCENE: [location, condition, what happened here is visible in the space]
TIME: [night / early morning — the in-between time]
LIGHTING: [scene investigation — bright forensic lights against dark ambient]
CAMERA: [begins wide on scene, slowly finds detective, then follows their eye to [detail]]
DISCOVERY: [what they find / realize — the thing that changes everything]
REACTION: [a small reaction — not dramatic. The character is professional. 
            But something crosses the face.]
AUDIO: [forensic environment — quiet, focused, the sound of controlled investigation]
```

### Thriller — The Confrontation

```
CHARACTER A: [the one with information / the one with power]
CHARACTER B: [the one who needs something / the one being confronted]
SPACE: [tight, no easy exit — this conversation cannot be escaped]
POWER DYNAMIC: [who has it, who wants it, how it shifts]
DIALOGUE STRATEGY: [surface conversation / underlying negotiation — they are not 
                     saying what they mean]
CAMERA: [two-shot establishing power balance / OTS alternating / CU on the moment 
         the power shifts]
TENSION INSTRUMENT: [what in the scene creates physical tension — object / proximity / 
                      implied threat]
RESOLUTION: [the scene ends with the power dynamic changed — someone won or lost something]
```

### War Drama — The Quiet Before

```
SOLDIERS: [two to four, identity tokens if recurring]
SITUATION: [hours before an assault / waiting in position / down time in a war zone]
TONE: [the strange peace of waiting for danger — gallows humor / genuine connection / 
        the weight of what is coming]
ENVIRONMENT: [field position / temporary shelter / destroyed building used as camp]
DIALOGUE: [not about the mission — about home / family / what they will do after /
            anything except what they are about to do]
CAMERA: [intimate — these are human beings, not soldiers]
LIGHTING: [campfire / minimal artificial / available light]
NOTE: [this scene earns the cost of what follows. If the audience doesn't know them, 
       their deaths mean nothing.]
```

---

## The Climax Scene Formula

```
CLIMAX REQUIREMENTS:
  [ ] Stakes at maximum — highest consequence of the story is present
  [ ] Character's arc reaches its crisis — the internal flaw meets the external conflict
  [ ] All major threads converge in this space and time
  [ ] The outcome is genuinely in doubt until the moment of resolution
  [ ] The resolution comes from character, not from coincidence

CLIMAX PROMPT:
ENVIRONMENT: [the space appropriate to this story's climax — chosen for meaning, 
               not spectacle]
CHARACTERS: [all who matter are here]
STATUS: [where everyone stands at the start of the climax sequence]
TURNING POINT: [the specific action or decision that decides the outcome]
RESOLUTION: [what the final state is — and how it differs from the story's opening state]
FINAL IMAGE: [the last thing the audience sees before the credit sequence begins — 
               designed to echo the opening image and show what has changed]
```

---

## Golden Rule

> Every scene in a feature is a short film. It has a beginning, a middle, and an end. It changes something. It earns its place. Design each one as if it could stand alone, then make sure it cannot.
