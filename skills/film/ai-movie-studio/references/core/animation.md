# Animation — Motion Physics, Creature Behavior & Simulation

## Physics Is Believability

Nothing breaks immersion faster than physics that doesn't behave. Cloth that floats when it should fall. Hair that moves in the wrong direction. Water that lacks weight. Specify physics behavior explicitly in every prompt where simulated materials are present.

---

## Cloth Simulation

### Heavy Fabric (wool, leather, thick cotton)

Moves with inertia — slow to respond, keeps moving after the body stops.

**Prompt phrase:** `heavy fabric with realistic weight, cloth follows body movement with inertia, settles slowly after motion stops`

### Light Fabric (silk, linen, chiffon)

Responds to the slightest air movement. Continuous flutter even in still air.

**Prompt phrase:** `lightweight fabric, continuous subtle movement from ambient air, floats and settles with air currents, responsive to motion`

### Battle / War Armor and Capes

Cape catches air and lags behind directional movement. Metal pieces restrict range of motion.

**Prompt phrase:** `cape catches air in movement, billows and wraps with directional force, settles after movement, cape physics realistic`

---

## Hair Simulation

### Short Hair

Minimal simulation needed. Moves only in strong wind or intense physical action.

**Prompt phrase:** `short hair, minimal movement, responds only to strong force, closely follows head movement`

### Long Hair

Moves with body orientation and momentum. Leads or lags depending on direction change.

**Prompt phrase:** `long hair with realistic weight, trails behind directional movement, sweeps with head turns, full physics simulation`

### Hair in Wind

Wind direction consistent. Hair moves away from wind source, not randomly.

**Prompt phrase:** `hair blown by [direction] wind, consistent direction, strands separating and floating, wind source from [left/right/front/back]`

### Hair in Combat

Becomes increasingly dishevelled with each impact or intense move.

**Prompt phrase:** `hair loosening with combat intensity, strands falling across face progressively, disorder increasing`

---

## Water Physics

### Ocean / Large Body

Gravity-bound, constant motion, surface varies with wind and depth.

**Prompt phrase:** `realistic ocean physics, surface movement with wave propagation, depth visible through clarity gradient, foam at crests, weight and mass evident`

### Rain

Falls in direction consistent with wind. Splashes on impact. Collects on surfaces.

**Prompt phrase:** `rain falling at [angle], consistent wind direction, splash impact on surfaces, running water collecting on ground, wet surfaces reflecting`

### Running Water (River / Creek)

Moves around obstacles, creates turbulence, transparent over lighter substrate.

**Prompt phrase:** `flowing water with turbulence around obstacles, surface ripple from current, transparency showing bed, realistic hydraulics`

### Flood / Violent Water

Carries debris. Pushes against structures. White water at obstacles.

**Prompt phrase:** `violent flood water carrying debris, pushing against structures, white water at obstacles, massive force evident in movement`

### Blood (Combat Context)

Follows gravity and velocity. Splatter pattern consistent with impact force and direction.

**Prompt phrase:** `blood follows gravity, velocity-appropriate splatter, pooling on surfaces, no stylization — physical behavior`

---

## Fire Physics

### Torch / Small Flame

Wavers with air currents. Base bright, tip dimmer and smokier.

**Prompt phrase:** `torch flame, bright at base, dimmer and smokier at tip, wavers with air movement, consistent light source behavior`

### Campfire / Fire Pit

Multiple flame cores. Ember trail rising upward. Smoke column above.

**Prompt phrase:** `campfire, multiple flame cores, embers rising in thermal column, smoke drifting with wind, crackling physics`

### Structure Fire / Building Burn

Draws air inward at base, pushes heat and smoke upward. Orange-yellow core, dark smoke crown.

**Prompt phrase:** `structure fire, air drawn into base, heat convection column upward, rolling smoke above, orange core with dark smoke crown, intense heat shimmer`

### Explosion Fireball

Rapid expansion, white core, orange exterior, dark smoke trailing immediately after.

**Prompt phrase:** `explosion fireball, rapid expansion from center, white-hot core, orange exterior, immediate dark smoke trailing, shockwave visible in air`

---

## Smoke and Dust

### Gunsmoke / Muzzle Blast

Sharp initial burst at source, immediately dissipating and drifting.

**Prompt phrase:** `muzzle smoke, sharp burst at barrel, immediate dispersion, drifts with ambient air`

### Battlefield Smoke

Thick rolling columns, obscures vision at distance, multiple sources.

**Prompt phrase:** `battlefield smoke, multiple thick columns, obscuring mid-to-far distance, moving with wind, reduces visibility`

### Dust (Explosion, Impact, Cavalry)

Explosion: outward burst from ground up. Cavalry: churned upward and backward from hooves.

**Prompt phrase:** `impact dust, rapid outward expansion from point of impact, dissipates upward and outward, debris embedded in cloud`

---

## Particle Systems

### Falling Debris

Size varies. Heavier pieces fall faster and with more direct trajectory.

**Prompt phrase:** `debris falling with mass-appropriate physics, larger pieces fall faster and more directly, smaller pieces tumble and flutter`

### Sparks

Generated by metal-on-metal or explosive ignition. Travel in arcs from source, fade quickly.

**Prompt phrase:** `sparks generated at impact point, arc outward from source, fade and disappear within short distance, hot orange-white`

### Ash / Snow

Extremely light — minimal terminal velocity, responds to the smallest air current.

**Prompt phrase:** `[ash/snow] falling slowly, responds to air currents, irregular descent, accumulates on horizontal surfaces`

---

## Creature / Character Motion

### Quadruped Gaits

| Gait | Description |
|---|---|
| Walk | Diagonal pairs (LF-RR, RF-LR), four beats |
| Trot | Diagonal pairs simultaneously, two beats, bouncy |
| Canter | Three beats, leading leg extended, rolling gait |
| Gallop | Full suspension phase, all four feet off ground at peak, four beats |

**For AI generation:** Always specify the gait, not just "running" or "moving."

**Prompt phrase:** `horse at full gallop, all-four suspension phase, neck extended, hooves churning, full speed`

### Large Creature Motion

Massive creatures have inertia — they cannot change direction or stop quickly. Weight is visible in every movement.

**Prompt phrase:** `creature with massive inertia, movement has weight and momentum, takes time to change direction, ground impact reverberates`

### Bird Flight

Wing-beat cycle varies by size. Small birds: rapid continuous beats. Large birds: beat-glide cycle with long glide phases.

**Prompt phrase:** `[eagle/hawk] in soaring flight, minimal wingbeats, riding thermals, wings fully extended in glide, banking with body tilt`

---

## Crowd Simulation

Large crowds read as alive when they have variation — nobody is doing exactly the same thing.

**Prompt phrase principles:**
- Specify the dominant activity but allow variation
- Assign clusters of behaviour (group A moving, group B stationary, group C in conversation)
- Density affects movement: dense crowds shuffle and flow; sparse crowds move more individually

**Prompt phrase:** `crowd of [number], [dominant activity], variation in individual behavior, no two people identical, realistic density and spacing`

---

## Physics Consistency Check

For any scene with complex simulation:

```
[ ] Cloth: weight appropriate for fabric type? Inertia correct?
[ ] Hair: moving in consistent direction? Physics appropriate to intensity?
[ ] Water: gravity correct? Surface behavior physical?
[ ] Fire: drawing air at base? Smoke rising? Heat visible?
[ ] Explosion: expansion sequence correct? Smoke after fireball?
[ ] Debris: mass-appropriate trajectory? Not floating?
[ ] Smoke: drifting with consistent wind? Rising with heat?
[ ] Creatures: gait named and correct? Weight evident in movement?
```

---

## Golden Rule

> Physics is the first thing the eye checks unconsciously. Get it wrong and the audience knows something is false before they can name it. Specify it precisely and the impossible becomes believable.
