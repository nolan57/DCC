# Intrinsic structure tiers `L0`–`L3` (v2) — definitions, quantities, locked thresholds

**Date**: 2026-11-22
**Status**: **definitions adopted for evaluation** (governor's instruction of 2026-11-22); **no tier is admitted yet** —
admission is a machine verdict produced by `src/route/structure_tiers.py`, not a statement in this file.
**Supersedes**: the extrinsic `L0`–`L3` of `docs/decisions/exhaustive_matrix_route_v1.md` §III, **withdrawn** (audit
`exhaustive_matrix_route_v1_audit.md` M2–M6: all four referred to the original object, and 0 of 4 increased with
2D-ification).
**Lock**: `runs/MATRIX/threshold_lock.json` + `.sha256`, written before any evaluation.
**Pre-registration**: `runs/MATRIX/tier_redefinition_registration.md`.

---

## 0. The rule this file obeys

A tier enters the matrix **iff** all three parts are present and machine-verifiable:

| part | requirement | verified by |
| --- | --- | --- |
| **(a)** | a formal definition that refers **only to the scene** — no reference to the original object, its invariants, or its appearance | token scan of the definition text (`INTRINSIC_FORBIDDEN`) |
| **(b)** | a quantity that takes **different values** on an unstructured null and on at least one structured control, with a declared separation | numeric: null must fail, ≥1 control must pass |
| **(c)** | a threshold **declared before evaluation and hash-locked** | recomputed SHA-256 of the lock file must equal the recorded digest |

Missing any one ⇒ the tier is **REFUSED**, and the matrix may not carry that column. The three parts are checked
independently, so a tier with a beautiful definition and no lock is refused, and a tier with a locked threshold and
an extrinsic definition is refused. The verdict names which part failed.

## 1. Declared scene model

A scene is a discrete field `u: Λ → ℝ` on a `128 × 128` grid of square cells of side `h` (declare `h = 1` cell; all
lengths below are in cells). Values are quantized to `B = 64` bins spanning `[min u, max u]`; `Δu = max u − min u`.

**Declared null ensemble** `𝒩`: `M = 16` realizations of i.i.d. `U(0,1)`, seeds `4000…4015`. Every quantity below
is referenced to the mean of that ensemble over the *same* grid and binning, so no tier compares across instruments.

Declared calibration scenes (seeds fixed, generators in `src/route/structure_tiers.py`):

| id | what it is | role |
| --- | --- | --- |
| `NOISE` | i.i.d. `U(0,1)` | the **unstructured null** (must fail every tier) |
| `NOISE-S` | same, different seed | null repeat (guards against a lucky draw) |
| `BLUR` | i.i.d. noise through a Gaussian of `σ = 6` cells | one scale, no segments |
| `DITHER` | constant field with `5%` of cells flipped by `±3` bins | predictable, no scale, no hierarchy |
| `RAMP` | linear gradient, full range | trivially organized, no scale |
| `STEP` | one vertical step edge | organized, broadband (no characteristic scale) |
| `GRATING` | sinusoid, period `32` cells | organized, one scale, no hierarchy |
| `TILED` | `16 × 16` constant tiles; tile content is a quadrant of a disc so that the global disc appears **only if the tiles are in the canonical order** | organized, one scale, multi-level; the layout-convention case |
| `BLANK` | constant field | **degenerate** — must return *no verdict*, never a maximum |

---

## 2. `L0` — topological organization

**(a) Definition (scene only).**
Let `Dgm₀(u)` be the 0-dimensional persistence diagram of the **superlevel** filtration of `u`, computed on the
4-neighbour grid (join tree). Each pair `(b, d) ∈ Dgm₀` is the birth and death level of one connected component.
Define the **topological fragmentation**

```
P0(u) = (1/|Λ|) · Σ_{(b,d) ∈ Dgm₀}  (b − d) / Δu
```

i.e. the total intensity lifetime of all components, measured in units of the scene's own dynamic range, per cell.
`P0` is an *intensive* quantity: for an i.i.d. field it tends to a positive constant, while a field organized into
few persistent segments has `P0 = O(1/|Λ|) → 0`.

*Precondition (declared):* `σ_u / Δu ≥ 0.01`. A constant field carries no structure of either kind, so `L0` returns
**no verdict** on it — not a pass. (Without this clause a blank frame would score maximal organization, which is the
obvious first way to cheat this tier.)

**(b) Quantity.**
```
Q0 = 1 − P0(u) / P0(𝒩)
```
`Q0 = 0` at the null by construction; `Q0 → 1` as fragmentation is removed. Range `(−∞, 1]`.

**(c) Threshold (locked).** `Q0 ≥ 0.50` — at least half of the null's topological fragmentation absent.

---

## 3. `L1` — characteristic scale in the scene's own metric

**(a) Definition (scene only).**
Let `R(ℓ)` be the normalized autocorrelation of `u` at lag `ℓ ∈ {0,1,…}`, averaged over the 4 axis directions, with
`R(0) = 1`. Define the **characteristic scale**

```
ξ = min { ℓ : R(ℓ) < e^{−1} }
```

in cells. `ξ` is measured entirely in the scene's own embedding metric; no external length enters.

**(b) Quantity.** `Q1 = ξ / h ∈ [0, 64]`. Unstructured: `ξ ≈ 0–1` (a scale does not exist below the sampling
scale). Structured: `ξ` is a finite multiple of the cell — for `BLUR` `ξ ≈ 6–10`, for `GRATING` `ξ ≈ 12–20`.

**(c) Threshold (locked).** `Q1 ≥ 4.0` — a scale at least four cells wide, i.e. resolvable independently of the
sampling lattice.

---

## 4. `L2` — predictability (information, self-referenced)

**(a) Definition (scene only).**
Quantize the two neighbours `W = u(i−1,j)` and `N = u(i,j−1)` into `16` levels each, giving 256 contexts `c`.
Let `H(u)` be the marginal entropy in bits and `H(u | c)` the conditional entropy given the context, both as
**plug-in estimators** on the same grid. Define the **predictability**

```
q₂(u) = 1 − H(u | c) / H(u)                                  (plug-in, biased low)
Q2    = ( q₂(u) − q₂(𝒩) ) / ( 1 − q₂(𝒩) )                    q₂(𝒩) = mean over the null ensemble
```

> **Why the renormalisation is in the definition and not a patch.** Plug-in conditional entropy is biased
> *downward*: with 256 contexts and `|Λ| = 16384`, each context holds ~64 samples over 64 bins, so `H(u|c)` is
> underestimated even when the context carries no information. Raw `q₂` on pure i.i.d. noise comes out visibly
> above zero, and a tier that reported that as structure would be measuring its own estimator. `Q2` therefore maps
> the null ensemble to `0` **by construction, using the identical estimator**, and perfect predictability to `1`.
> This is declared here, before any evaluation, because it is a property of the estimator and not of the scenes.

**(b) Quantity.** `Q2 = 0` at the null by construction; `Q2 → 1` as the field becomes determined by its
neighbourhood. Unstructured: neighbours carry no information. Structured: `Q2` rises toward 1.

This is the *intrinsic* replacement for `I(Scene; Structure)`. The audit's M4 killed the mutual-information form
two ways — undefined without an ensemble, and maximised by noise. `Q2` is defined for one scene, and noise sits at
its **minimum**, not its maximum, because the reference is the scene's own marginal rather than an external joint.

*Declared caveat:* `Q2` is large for any locally smooth or locally constant field, including one with no
large-scale organization. It is a tier-0-style test and is not, by itself, evidence of a readable picture.

**(c) Threshold (locked).** `Q2 ≥ 0.50` — at least half of the marginal entropy removed by local context.

---

## 5. `L3` — legibility through a declared observer

**(a) Definition (scene only, plus a declared observer).**
Declare an observer: a Gaussian point-spread function of `σ_eye = 2.0` cells (one acuity element spans two scene
cells at the declared viewing geometry — a **declared convention**, `DC4`), a contrast threshold
`C_eye = 0.01` (Weber), and a channel factor `q` from the declared photon budget. Define the **band-limited contrast
at the characteristic scale**

```
u_ξ  = DoG( u ; σ₁ = ξ/2, σ₂ = 2ξ )
C_ξ  = std(u_ξ) / mean(u)
```

and
```
Q3 = log₂( 1 + C_ξ · q / C_eye )
```

*Precondition (declared):* `ξ/h ≥ 2`. Legibility **of structure** is not defined when no structure exists, so a
scene without a characteristic scale returns **no verdict** — it is not certified legible merely for being noisy.

*Channel factor.* `q = 1` for a declared instrumented channel; `q` for the naked-eye reflected channel is computed
from the registered exposure budget (`p2_clock_results` P2-2/P2-3) and is **exactly 0**, because reflection has
zero exposure budget. `L3` is therefore a function of the channel, and the channel must be named on every `L3` cell.

**(b) Quantity.** `Q3 ∈ [0, ∞)` in units of *distinguishable levels* (bits). Unstructured with no scale: no verdict.
Structured at low contrast: `Q3 → 0`. Structured above threshold: `Q3 > 2` means at least three distinguishable
levels survive the observer.

**(c) Threshold (locked).** `Q3 ≥ 2.0` — at least `2² = 4` distinguishable levels.

---

## 6. What these definitions deliberately do not contain

| removed | because |
| --- | --- |
| any word about the original object | that was the single cause of M2–M6: all four columns measured what 2D-ification destroys |
| `χ`, `β₀`, `d_H`, `W₁` computed *against the pre-conversion state* | same |
| `I(scene; structure)` | undefined without an ensemble, and maximised by noise (M4) |
| a per-cell choice of metric or threshold | makes the tier identically satisfied via the pullback metric (M3) and is post-hoc fitting (M8) |
| any `π`-dependent quantity | the layout convention is not physics (`unfold_is_real_v1` §4); it must be a declared `DC` item, not a tier |

## 7. Consequences the governor should expect

1. **`L3` will still be empty under `C1` in reflection** — not because the tier is extrinsic, but because `q = 0`
   there. The redefinition does not rescue `L3`; it explains the emptiness as photon physics rather than as a bad
   metric. `L3` becomes evaluable only on a channel with `q > 0`.
2. **`L0`, `L1`, `L2` are no longer ordered by construction.** They measure organization, scale, and predictability —
   three different things. A scene can pass one and fail another (a step edge passes `L0`, fails `L1`; a dithered
   plateau passes `L2`, fails `L0`/`L1`). So "max tier reached" is a *profile*, not a linear rank, and the matrix
   must report the profile rather than a maximum. This is the structural change the audit asked for (M6): the old
   matrix needed a total order that did not exist; this one does not need one.
3. **A tier can be REFUSED on its own evidence.** `(b)` is a numerical test: if the null passes the threshold, or no
   control does, the tier does not enter the matrix no matter how good its definition reads.

## 8. Admission is not a claim

Admission says a tier is *well-formed and discriminating*. It says nothing about whether any constraint row reaches
it. Those are different questions, and the matrix is allowed to be empty in every column.
