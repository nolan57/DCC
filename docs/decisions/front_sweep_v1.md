# What the Unfolding Process Looks Like When the Two-Dimensionalization Front Sweeps Through a Human Body (front_sweep v1)

**Date**: 2026-11-21  **Status**: OPEN
**Upstream**: `unfold_is_real_v1.md` (four-question verdict), `unfold_appearance_v1.md` (rendering)
**Recomputation**: `src/analysis/front_sweep_v1.py` → `runs/ANALYSIS/front_sweep_v1.txt` (9/9 PASS)

---

## 0. In One Sentence

> The front is a **layer-peeling machine**: each time it peels off one atomic layer (0.215 nm), the entire layer is translated as a rigid body to its lattice site and joined edge-to-edge.
> There are 8.1×10⁹ peelings in all, with a minimum of 2.2 s, punctuated by a 10–30 μs thermal flash.
> **Not a single deformation** — the intralayer strain is always 0, and all displacement is taken up by the interlayer interfaces.

---

## 1. How Many Pieces Are There After the Cut (Answering Last Round's Open Item)

The number of 4-connected components is counted in each layer's cross-section (using the same synthetic phantom, 200² pixels):

| Region | z range (m) | Connected components | Single-piece area (m²) |
|---|---|---|---|
| calf → thigh | 0.012–0.800 | **2.00** | 0.0063–0.0221 |
| pelvis | 0.800–0.960 | 1.00 | 0.0457 |
| abdomen | 0.960–1.170 | 1.00 | 0.0464–0.0516 |
| thorax | 1.170–1.380 | 1.00 | 0.0540 |
| shoulder | 1.380–1.470 | 1.00 | 0.0490 |
| neck | 1.470–1.560 | 1.00 | 0.0098 |
| head | 1.560–1.738 | 1.00 | 0.0202–0.0303 |

Average **1.457 components/layer** → **1.18×10¹⁰ fragments** in total (not 8.1×10⁹ sheets).

**Conclusion: not "8.1 billion whole sheets", but "about 12 billion thin plates"** — the extra pieces all come from the two-leg segment (splitting into two per layer) and cross-section splits in the neck/head segments. Each piece is 0.215 nm thick with area 6×10⁻³–5×10⁻² m²; the total side area is only 0.72 m² (2×10⁻⁹ of the front area) — **they are plates, not crumbs**.

Phantom self-check: ∫A_c dz = 0.0601 m³, 14% below the nominal 0.070 (the phantom is rather thin); the area is slightly smaller in proportion, which does not affect the order of magnitude.

---

## 2. The Three Steps per Layer (Microscopic Sequence)

| Step | What happens | Key point |
|---|---|---|
| ① Break | the cross-layer bonds between this layer and adjacent layers **lose their domain of definition** | not "pulled apart". Stretching requires time and force; dimensional reduction means the z direction disappears and the bonds' domain of definition no longer exists. The fracture surface = the whole layer cross-section, occurring simultaneously. |
| ② Spread | the whole layer is translated to its lattice site as a 2D rigid body | **intralayer (x,y) identity map → intralayer strain always 0**. |
| ③ Land | it enters the lattice site and joins neighboring sites edge-to-edge | no in-plane bonding is performed. The space between pieces is vacuum. |

The entire unfolding is therefore **8.12×10⁹ SE(2) rigid translations**, none of which is a deformation.

This corrects last round's phrasing "stretched 9.28×10⁸ times": 9.28×10⁸ is the **displacement gradient of the mapping**, not the strain of the material. What the material actually experiences is "zero strain within pieces + bonds vanishing between pieces". Therefore:

> **"Smoothness" holds in the advance of the front (zero intralayer strain at each conversion) and fails everywhere between layers (all 8.12×10⁹ interfaces are broken).**

### 2.1 Scope clause — what step ② does not do (added 2026-11-22)

A submission proposed separating "kinematic unfolding" (what D2 does) from "dynamic unfolding" (what a body driven by its own constitutive law would do), and asked for that distinction in the route's body. **The distinction is correct and is registered here**, where its object lives. Ruling: `docs/decisions/kinematic_vs_dynamic_unfolding_v1.md`.

> **D2 performs no deformation.** Each layer is translated as a rigid body and joined edge-to-edge, with vacuum between pieces. Intralayer strain is zero *by construction*, not by an idealisation of the material. No claim is made that a body driven by its own constitutive law would arrange itself the way D2 arranges it. That question is not merely unanswered — it is **unaddressed**; and it is not a defect of the deposition, because the deposition does not build a strained body.
>
> **Declared, not measured.** No frame may depict elastic unfolding, differential strain, wave propagation, or fracture as a consequence of D2.

**Why the zero is structural, and what it costs.** Steps ①–③ contain no elasticity, so there is no stored energy to release — hence no rebound, no delamination, no recovery. The price is that the arrangement is *chosen*: `Π` is ours, and nothing in the mechanism selects it over any other relabelling with the same piece census. That is the honest reading of "kinematic", and it is weaker than "we idealised and the idealisation is harmless".

**Why no frame can settle it either way.** For the counterfactual body such a submission posits (bonded, compressed to `2δ`, released), the two response times bracket the conversion: the thickness returns in `2δ/c_s = 4.3e-13 s`, i.e. `1.9e4 ×` **before** `t_rip = 8.2553e-9 s` ends, and the in-plane arrangement settles in `R/c_s = 1.8e-4 s`, i.e. `2.2e4 ×` **after** it. Their ratio is `R/(2δ) = 4.19e8`, independent of `μ` and `ρ`. **There is no instant at which that body looks like the kinematic map** — so the choice is not falsifiable by any image at `t ≤ t_rip`, and must not be presented as though an image could confirm it.

---

### 2.2 Scope clause — the site is not defined by this document (added 2026-11-22)

Step ② says each layer is carried "to **its** lattice site". The possessive asserts a map

```
sigma : n_z -> (u, v)      layer index -> site coordinates
```

that **this document does not supply, and no other document supplies either**. §5 constrains the *order*
only by transport speed and accepts two families. So:

> **The mechanism specifies every layer's destination region and never specifies its destination.**
> A frame that draws a site's **content** (as opposed to a symbol for occupancy) has already answered
> this question silently, and must not be drawn until `sigma` is declared and locked.

Registered as `GD11`, open. Choosing `sigma` is a **convention**, not a derivation — §2.1 says in this
document's own words that nothing in the mechanism selects `Π`. It is also downstream of `GD10`: if the
array side is `108628`, the site set changes and so does every `sigma`.

Measured, not chosen (ruling `space_filling_vs_identity_v1.md`, `P11`–`P14`): on `256²`, raster order is
maximally anisotropic (`rho = 256`, a vertical neighbour `256` layers away, a horizontal one `1`) and
`0.9961` contiguous; a Hilbert curve is isotropic (`rho = 1.0`), `1.0000` contiguous, median adjacent
`|Δn| = 1`, at the cost of one `21845`-layer jump where the curve passes near itself. Both are locally
faithful; the curve is the more isotropic of the two. No preference is recorded here.

**Addendum 2026-11-22 — `σ` is declared, for a different object.** A governor directive replaced the
demonstration subject: the 2D renderings no longer use body slices, and `σ` is declared for the replacement.
`DEMO-1` (`docs/specs/demo_object_v1.md`, hash-locked) is four coaxial shells with `H = 0.230 m`, array
`65536²`, one plate per cell, and `σ : p = k·N + n → Hilbert index` — component-major, because layer-major is
annihilated by the `1:16384` decimation any renderable frame imposes. **None of that applies to this document's
object.** The body still has no `σ`; the prohibition above stands, and `GD11` remains open for it.

---

## 3. Time Budget

Placement distances (origin at the body center, square array 90126²): **average 13.8 km, maximum 25.5 km (diagonal)**.

| Total duration | Speed of farthest atom | Kinetic energy/atom | Interpretation |
|---|---|---|---|
| 2.2 s | 11.6 km/s | 4.2 eV | already at bond-energy scale |
| 10 s | 2.6 km/s | 0.20 eV | moderate |
| 100 s | 0.25 km/s | 2 meV | very moderate |
| 1750 s | 14 m/s | 6 μeV | completely lossless |

Criterion: transport kinetic energy < bond energy (~4 eV) → **v ≤ 11.3 km/s → total duration ≥ 2.25 s**.

> **Three-to-two-dimensional reduction cannot be completed in under a second.** Any faster and the atoms would be "flung" into place rather than "placed" into it, and the landing points would scatter.

Corresponding front speed: if T=2.25 s, v_front = 1.75/2.25 = **0.78 m/s**; if relaxed to the minute scale, the front is on the order of **1 mm/s** — a very slow sweep.

---

## 4. Thermal Budget (Will the Image Burn Itself Away?)

Cut energy per unit area = 2γ_eff; total cut area 3.25×10⁸ m².

| γ_eff (J/m²) | Total heat released (J) | Temperature rise ΔT (K) | Diffusion before cooling |
|---|---|---|---|
| 0.07 (soft tissue) | 4.6×10⁷ | 155 | 1×10⁻⁷ m |
| 0.30 | 2.0×10⁸ | 663 | 9×10⁻⁸ m |
| 1.00 (covalent solid) | 6.5×10⁸ | 2210 | 4×10⁻⁸ m |

Radiative cooling time is 10–30 μs; before that, atoms travel 10–100 nm according to the liquid diffusion coefficient.

**Conclusion: atomic-scale detail is lost over 10–100 nm, while the readable scale of the image is 1 mm — a difference of 4–5 orders of magnitude.** This picture is "atomically blurred, anatomically clear". The thermal flash will not destroy it, but will downgrade it from an "atomic-scale archive" to a "nanometer-scale archive".

---

## 5. Sequencing Budget (Placement Order Is Not Entirely Free)

- If "the picture is finished when the front finishes sweeping" is required → the farthest lattice site must be filled first, i.e. **farthest first, nearest last**.
- If one insists on "placing in head-to-toe order" → the sites for the last batch of pieces are 25.5 km away, requiring a **~2 s transport tail**.
- Both are acceptable; it is just that "front finished sweeping" and "picture formed" are two different moments.

**Speed-of-light negative control (proving the arrangement cannot be a long thin strip)**:

| Strip width | Strip length | Required speed within 2.25 s | Interpretation |
|---|---|---|---|
| 0.20 m | 1.62×10⁶ km | 2.41 c | **rejected** |
| 0.49 m | 6.63×10⁵ km | 0.98 c | marginal |
| 1.00 m | 3.25×10⁵ km | 0.48 c | feasible |

> Namely: the imagined "160 million km long film" cannot pass the speed-of-light test; the width must be > 0.48 m. A square arrangement (18 km on a side) is one of the transport-optimal options.

---

## 6. Relationship to Existing Conclusions

- **K5 (timescale)**: this round gives its quantitative version — a minimum of 2.2 s, from transport kinetic energy. Stronger than "no timescale separation": it now has a lower bound.
- **K5b (geometry, previous round)**: this round gives its process form — not "tearing", but "layer-by-layer peeling", with zero strain in each layer.
- **The definition of "smooth" needs tightening**: smooth should mean "no shock in the front's advance + zero intralayer strain at each conversion", **not including "material continuity"**. If "material continuity" is insisted upon, it conflicts with the bijection (K5b) and the feasible region is empty.
- **Visualization**: the thermal flash is the only self-luminous source on this route. If the front sweeps at 1 mm/s, the heat-release power is 4.6×10⁷/1750 = 26 kW, spread over a 0.04 m² front face (650 kW/m²), giving a film temperature of about 450 K — **visible only in the infrared, invisible to the human eye**. Only when γ_eff→1 (the cut passes through many covalent bonds) does it rise above 2000 K and show a dark red. The direction agrees with the earlier "abandoning smoothness is most spectacular" conclusion, but the magnitude is much smaller: not 99× the solar surface, but a hotplate element.

---

## 7. Open Items

- [ ] What value γ_eff should take: does tissue cutting run between molecules (0.07) or through covalent bonds (1.0)? Real tissue fracture-toughness data are needed.
- [ ] Melting point of the 2D film: this document uses Lindemann + k=20 N/m to obtain ~700 K; if k is taken as 500 N/m for covalent bonds it becomes 1.7×10⁴ K, a factor of 25 difference, requiring independent verification.
- [ ] **Shape** of the fragments: after cutting, each piece is bounded by a tomographic contour (including internal cavities such as lungs and bowel gas); in 2D are these cavities holes or "filled in"? This affects whether pieces can truly be joined edge-to-edge.
