# Explosions — Pyro, CG Blast Design & Combat FX

## The Anatomy of an Explosion

An explosion is not a single event — it is a sequence of events that must all be present for the effect to read as physically real.

### The Explosion Sequence

```
1. FLASH          — Instantaneous white-hot flash at the point of detonation (1–3 frames)
2. FIREBALL       — Rapid expansion of burning gases — orange-yellow exterior, white core
3. CONCUSSION     — Visible pressure wave in the air — distorts environment, ripples through dust/water
4. DEBRIS         — Material thrown outward from the source at velocity
5. SMOKE          — Dense black-brown smoke rising immediately after the fireball
6. FIRE           — Sustained burning at the source after initial blast
7. SETTLING       — Debris falls, dust drifts, smoke expands upward
```

Always specify which stages are visible in the shot.

---

## Explosion Types

### Grenade / IED (Small Scale)

Close-range, direct-force, personal-scale. The character is within the killing radius.

**Sequence:** Sharp crack → small orange fireball → debris scatter outward → gray-white smoke → silence

**Prompt phrase:** `grenade detonation, sharp crack, small orange fireball, debris scattered outward radially, gray smoke, [nearby character reaction — thrown / diving / stunned]`

---

### Car / Vehicle Bomb

Mid-scale. The vehicle is the container — metal fragments become projectiles.

**Sequence:** Initial crack → orange-black fireball → vehicle debris flung outward → thick black-brown smoke → sustained burn

**Prompt phrase:** `vehicle explosion, initial detonation crack, orange-black fireball, vehicle debris thrown outward, thick dark smoke, fire establishing at wreckage`

---

### Building Demolition / Artillery Strike

Large scale, sustained. Building collapses over several seconds. Dust clouds expand across the scene.

**Sequence:** Impact → structure damage → building collapse progressive → massive dust cloud expansion → debris rain → settling dust

**Prompt phrase:** `artillery strike on structure, impact flash, progressive building collapse, massive dust cloud expanding outward and upward, debris rain, settling`

---

### Military Ordnance / Massive Scale

Felt before it is heard. Sub-bass concussion wave. Environmental effects beyond the blast radius.

**Prompt phrase:** `massive detonation, sub-bass concussion wave visible in air distortion, environmental damage beyond blast radius, sustained column of fire and smoke, scale dwarfs all human elements`

---

### Fuel Explosion / Tanker

Liquid fuel explosion creates the most spectacular fireball — rolling, oily, very hot.

**Prompt phrase:** `fuel explosion, rolling oily fireball, orange-black columns, intense thermal heat visible, ground scorched, sustained heavy fire`

---

## Secondary FX

### Shockwave Visualization

**Prompt phrase:** `pressure wave visible passing through [dust/smoke/rain], ripple expanding outward from explosion center, distortion ring`

### Environmental Damage from Blast

**Windows:** `windows shattered outward, glass cascade`
**Foliage:** `trees stripped, leaves and branches thrown, surrounding area scorched`
**Ground:** `ground cratered, soil and rock ejected, scorch mark remaining`
**Fire spread:** `secondary fire established on [nearby material — wood/cloth/fuel]`

### Human Response to Explosion

**Near miss:**
`character thrown by blast wave, tumbling, disoriented, ears ringing — audio shifts to muffled ring, gets to hands and knees, looking for threat`

**Direct hit (survival):**
`character takes blast, clothing damaged, face and hands bleeding from fragments, hearing damaged, struggling to orient`

---

## Practical vs CG Explosion Aesthetics

### Practical Pyro Feel

- Organic, irregular edge behavior
- Yellow-orange warm core with brown-black smoke
- Debris has weight and mass — trajectory physics correct
- Light from explosion illuminates nearby surfaces realistically

**Prompt phrase:** `practical pyro explosion aesthetic, organic irregular fireball, warm yellow-orange core, weighted debris, explosion light illuminating surrounding surfaces`

### CG / Stylized Explosion

- More precise, larger scale
- Can be tinted (green for chemical, blue for electrical/sci-fi)
- Perfect geometry possible for stylized productions

**Prompt phrase:** `stylized CG explosion, [colour — orange/green/blue-white], precise geometry, [scale — massive], [style — sci-fi/fantasy/real]`

---

## Combat FX Beyond Explosions

### Muzzle Flash

**Prompt phrase:** `muzzle flash, sharp brief flash at barrel, [direction of firing], smoke trail, ejected casing if visible`

### Bullet Impact

**Surfaces:**
- Stone: `impact chip, dust, spark`
- Wood: `splinter burst, entry hole`
- Metal: `ricochet spark, metal fragment`
- Body: `entry wound, kinetic response, blood if required`
- Water: `splash column, impact ring`

### RPG / Rocket Trail

**Prompt phrase:** `RPG launch, backblast behind firer, rocket trail forward, smoke corkscrew, impact detonation`

---

## Golden Rule

> An explosion that happens in silence and doesn't illuminate nearby surfaces is a visual effect, not a physical event. Ground every explosion in physics: the concussion, the light, the debris, the aftermath.
