# `θ` and its environment term `E` — declaration

**Date**: 2026-11-23
**Queue item**: `RQ-18`, `docs/program/round_queue_v1.json`
**Authority for the obligation**: `docs/specs/relaxation_ladder_v1.md` erratum `E2` item 3 and
`runs/LADDER/r2_relief_contrast_results.txt` §7.1 — `θ` carries no environment term, so `RL-2`'s price is a
function of an undeclared variable.
**Status**: **DECLARATION.** It adds a term to `θ`, three declared instances, and a rule for each. It writes
no threshold, prices no rung, adds no tier, and changes no product. Nothing here is a measurement.

---

## §0 Why this file exists

`θ = (aperture, gate ≤ 3 ns, band, distance)` is the observer tuple the record requires every visibility
sentence to carry (`relaxation_frame_v1.md` §2 `S9`). It describes a *camera*. It does not describe what the
camera is pointed at, and for this object that is not a detail: the surface is a near-mirror, so the image is
a reflection, and a reflection carries the **environment's** angular radiance profile and almost nothing else.

Round 49 measured the size of that omission on one object, one band, one relief:

| environment | `C` at `a = 1 mm` (sinusoidal) | `C` at `a = 1 mm` (terraced) |
|---|---|---|
| uniform dome | `0.000e+00` **exactly** | `0.000e+00` **exactly** |
| collimated disc, `β = 4.65e-3` | `3.317` | `0.280` |

Same object, same relief amplitude, same band, same everything `θ` names. The contrast ranges from exactly
zero to `Q3 = 8.38`. `E` is therefore not a correction to the model; without it, a sentence of the form
"`RL-2` buys contrast" has no truth value.

**The epistemic point, stated once.** `E` is the one term in `θ` that the *experimenter chooses*. That makes
it a confounder: an operator who picks `E` after seeing `C` has designed a scene, not measured one — the
same error class as `BN-07` (mapping measured laws back onto geometry and calling the inverse solution a
result). Declaring `E` is what converts a free choice into an axis. That is the whole purpose of this file.

## §1 The term

`θ₅ = (aperture, gate ≤ 3 ns, band, distance; E)` where

> **`E`** is the angular radiance profile `L_e(ω̂)` of the environment as seen from the object, over the
> half-space the object's surface faces, **together with** the direction(s) at which that radiance is
> concentrated. It is a property of the *scene's illumination*, not of the object and not of the camera.

`E` is **mandatory** from this date: a visibility sentence that names `θ` must name `E`, in the form
"`θ = (…; E_k)`" with `k` from §3 or a declared instance that states its own rule. An unnamed environment
is read as `E1` — the *zero-contrast* member — so silence cannot be mistaken for a favourable case.

## §2 The rule that generates all the others

For a specular surface with local slope field `α(x) = ∇z(x)` and reflectance `R`, the image at the declared
band is the composition

> **`R0`**  `I(x) = R · L_e( r(x) )`, where `r(x)` is the mirror map — the direction that reaches the camera
> from `x`.

`R0` is exact for a specular surface and is the entire content of "the surface shows you its environment".
Three corollaries follow, and each is one of the declared instances below:

- **`L_e` constant on `r(Ω_object)`** ⇒ `I` constant ⇒ `C = 0` **identically**. Not small — zero, for every
  relief, every amplitude, every band. *(Corollary 1; measured as `E1`, difference `0.000e+00` over 73
  amplitudes and six decades, both relief forms.)*
- **`L_e` a step** (a disc edge) ⇒ `I` binary ⇒ `C` is a function of the bright **area fraction** `f` only,
  `C = √((1−f)/f)`, and `f` is a level-set measure of `α`. *(Corollary 2; measured as `E2`, §3.)*
- **`L_e` smooth** ⇒ `C ∝ |∇L_e/L_e| · std(α)` — a **gradient** law, linear in relief amplitude at small
  slope. *(Corollary 3; measured as `E4`, exponent `k = 1.000`.)*

Nothing else is needed to generate every number in round 49. That is the test this declaration has to pass:
a term whose rules reproduce the measurements is a term; a term that merely renames a knob is not.

## §3 The declared instances

| id | `E` | image under `R0` | `C` rule | status |
|---|---|---|---|---|
| **`E1`** | uniform dome, `L_e = L₀` on the sphere | `I = R·L₀` | `C = 0` identically; no function of relief enters | **MEASURED** (`0.000e+00`, 73 × 2 points) |
| **`E2`** | collimated disc, angular radius `β`, any direction | `I = R·L₀·1{\|2α(x)\| < β}` | `C = √((1−f)/f)`, `f = \|{x ∈ plate : \|2α(x)\| < β}\| / \|plate\|`; `f` and therefore `C` are **independent of the disc's direction** (reflection is an isometry in the incidence plane) | **MEASURED** (`f = 1/12 → C = 3.3166` S; `f = 0.9271 → C = 0.2804` T) |
| **`E4`** | smooth directional beam, incidence `θ_i`, `L_e ∝ cos` falloff | `I = R·L₀·max(0, cos(θ_i+arctan α))/cos θ_i` | `C ≈ tan θ_i · std(α)/mean(α)` at `\|α\| ≪ 1`, i.e. **linear in relief amplitude** | **MEASURED** (`k = 1.000`, `a* = 0.858 mm` at `θ_i = 60°`) |
| **`E3`** | collimated disc, out-of-plane tilt / finite 2-D source | — | not derived | **RESERVED — NOT USED.** `src/route/ladder_r2.py`'s `E3` branch is an alias of `E2` and was never selected; disclosed here so the label is not read as a measured instance |

`E1`/`E2`/`E4` keep the labels of `runs/LADDER/r2_relief_registration.md` §2 verbatim, so every number in
`r2_relief_contrast_results.txt` stays traceable to the instance it was measured under.

**On `β`.** `β = 4.65e-3 rad` is the solar angular radius, used as the "full sun" baseline. It is a
*declared* value, and at `284 eV` there is no sun: `E2` at this band is an **instrument**, not a natural
source. That is not a defect of the declaration — it is why `E` is a declaration and not a measurement.

## §4 What `E` may not be used for

1. **No maximum over `E`.** A contrast claim is a *profile* `{C(E_k)}`, reported per instance, exactly as a
   tier verdict is a profile and never a maximum (`matrix_reading_rules_v1.md` `MR1.2`). The best member of
   the set is not the set's value.
2. **No late declaration.** `E` is declared with the scene, before `C` is computed. Declaring it afterwards
   is an inverse solution (`BN-07`) and the resulting number is a design.
3. **No promotion.** `C(E2) = 3.317` does not make `RL-2` "worth 8.38 in `Q3`" in any sentence that does not
   carry `E2`. The rung's price stays `V = ε`; `E` decides what `ε` is worth, and that is a separate
   sentence with a separate subject.

## §5 What this declaration does not do

- It writes **no threshold**. `C_eye`, the `L3` threshold and `Q3 = log2(1 + C/C_eye)` are untouched.
- It prices **no rung**. `RL-2`'s `V = ε` is arithmetically unchanged; erratum `E2` already recorded that
  `V` prices nothing that was measured, and this file does not repair that — it makes the reason nameable.
- It adds **no tier** and no column to the matrix.
- It does not touch `S9`. `E` is a property of a declared scene; it licenses no sentence about a person.
- It does not make `E1`'s zero a failure. A mirror in an integrating sphere *is* invisible. The zero is the
  correct answer to the wrong question, and naming the question is the point.

## §6 The one blind spot, declared rather than left implicit

`R0` is a **pure specular composition**: it has no occlusion term. A corrugation with risers shadows itself
at grazing incidence, and that shadow is dark under `E2`/`E4` regardless of `R0` — so `R0` **under-predicts**
contrast for a terraced surface at high `θ_i`. The missing object is a visibility function `V(x) ∈ {0,1}`:

```
I(x) = R · L_e(r(x)) · V(x),      V(x) = 1 iff  z(x+h) − z(x) < h·cot θ_i  for all h > 0
```

This is stated here so that the next round cannot discover it and call it a surprise. `V` is
**geometry** (it depends on `α`, not on `L_e`'s profile), which is why the check that exercises it —
`RQ-14`, `runs/LADDER/r3_illumination_registration.md` — has to separate the two by construction: if
oblique illumination moves `C` only through `V`, then `RL-3` is `RL-2`'s geometry seen from a different
angle, not a rung of its own.

---

## Errata

**E1** *(appended 2026-11-23 by round 50, `runs/LADDER/r3_illumination_results.txt`; §1–§6 are **not**
edited)*

`R0` in §2 contains the camera — `r(x)` is defined as "the direction that reaches the camera" — but the
tuple `θ₅` in §1 does not name it. Round 50 measured how much that costs: the glint channel's entire
dependence on incidence is **camera geometry**, not environment geometry.

- With the camera on the mirror image of the source (the specular configuration), `C` is **identical** at
  `θ_i = 0/45/75°` — `0.0e+00` difference in float64, two forms, five amplitudes — because reflection about
  the local normal is an isometry, so the angle between the reflected ray and the source is `2 arctan α`
  and carries no `θ_i`.
- With the camera fixed at normal incidence, the bright set is `|2 arctan α − θ_i| < β` and it **leaves the
  surface** at `2 arctan α_max`, which is `3.31°` for the sine and `8.88°` for the terraced form at
  `a = 1 mm`. Beyond that the plate is uniformly dark: contrast is not reduced, the image ceases to exist.

**So the tuple is short by one slot**: `θ₆ = (aperture, gate, band, distance; E; camera)`, where `camera`
is the declared viewing direction in the object frame. The slot is recorded here and **not enacted** —
§1's definition stands as written, and making a sixth slot mandatory is a tightening of every visibility
sentence in the record, which is the governor's call, not this file's. Until it is taken, any sentence that
quotes a contrast must state the camera geometry in words (`G_A` / `G_B` in round 50), or the number is
under-determined by a factor that this round measured to be unbounded (from `3.32` to *no image*).

`R0` itself is unchanged and remains exact. `E1`/`E2`/`E4` are unchanged. Nothing in §4 is relaxed by this
erratum: it is one more parameter that must be declared before `C` is computed, not one more freedom.

---

*Content generated by AI*
