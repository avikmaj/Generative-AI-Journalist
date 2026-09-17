# Compositing — CG Integration, Matte & Light Wrap

## Integration Is Invisibility

The goal of compositing is to make the join invisible. A CG element that reads as "added" breaks immersion immediately. Correct integration means the CG element responds to the same lighting, occupies the same depth, and casts and receives shadows as if it was always there.

---

## Light Wrap

The most critical integration technique. The background image bleeds its colour and light onto the edges of the foreground CG element, making it look like it was lit by the same environment.

**Prompt phrase:** `light wrap on [CG element], background environment colour bleeding onto element edges, integration of light from [key source direction], CG feels lit by scene`

---

## Shadow Casting and Receiving

CG elements must cast shadows onto the ground and other objects, and must receive shadows from the environment.

**Prompt phrase:** `[CG element] casts [shadow type — sharp/soft] onto [surface], shadow direction matches scene key light`

---

## Contact Shadow

The darkening that occurs where a surface meets the ground, even without a strong key light. Creates physical groundedness.

**Prompt phrase:** `contact shadow under [element], soft ambient occlusion at ground contact, element feels physically present in environment`

---

## Atmospheric Integration

CG elements in outdoor scenes must participate in the atmosphere: fog, haze, depth of field, heat shimmer.

**Prompt phrase:** `atmospheric integration, [CG element] shows atmospheric haze at [distance], depth of field matches camera setup, participates in scene atmosphere`

---

## Scale Reference

Without a human-scale reference, CG scale reads incorrectly. Always establish a scale anchor.

**Prompt phrase:** `scale reference — [human figure / known object] at [position] relative to [CG element], establishing true scale`

---

## Reflection Passes

CG elements should reflect in wet surfaces, mirrors, and polished materials in the scene.

**Prompt phrase:** `[CG element] reflected in [wet ground/mirror/water], reflection correctly distorted by [surface type], colour-matched`

---

## Golden Rule

> A composite is successful when no one looks for the seam. Every pass — light, shadow, atmosphere, reflection — is there to make the join disappear.
