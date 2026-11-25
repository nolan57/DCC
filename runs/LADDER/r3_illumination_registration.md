# `RL-3` pre-registration — oblique against normal illumination, one relief

**Registered**: 2026-11-23, before `src/route/ladder_r3.py` exists.
**Queue item**: `RQ-14`, `docs/program/round_queue_v1.json`.
**Authority for the question**: `docs/specs/relaxation_ladder_v1.md` §5 order 3 and erratum `E1` item 2;
`runs/LADDER/r2_relief_contrast_results.txt` §7. `RL-2` passes `L3` only in environment `E2`, and its price
`V = ε` was shown to price nothing measured — so the next question is whether `RL-3`, the other `V = 0`
rung, is a rung at all.
**Environment term**: `docs/specs/theta_environment_v1.md` (`RQ-18`, this round's companion declaration).
**Product**: `runs/LADDER/r3_illumination_results.txt`.

---

## §1 What is being decided

`RL-3` relaxes *illumination*: "normal ambient → oblique / structured", `V = 0`, and its fingerprint is
written as **"contrast collapses to the `RL-0` value under normal incidence"**. Two things are wrong with
that sentence before any measurement, and this round decides both:

1. **It conflates two independent axes of `E`.** *Direction* (`θ_i`) and *angular width* (`β`) are different
   parameters. `RL-0`'s collapse is caused by a **wide** environment (`E1`: radiance constant over the whole
   sphere), not by a **normal** one. Round 49 measured `C = 3.317` at normal incidence in a narrow
   environment — six times above the `Q3 ≥ 2` threshold — which is the collapse's exact opposite.
2. **For a specular surface the deflection is `2α` at every incidence.** Reflection about the local normal
   is an isometry, so the angle between the reflected ray and the source is `2 arctan α` and carries **no**
   `θ_i`. If that is what the channel sees, `RL-2` and `RL-3` are one rung by theorem, and the rung table is
   wrong to list them separately.

What can still separate them is not the glint. It is (i) the **Fresnel gain** `R(θ_i)` — a flux factor, and
(ii) **self-shadowing** of the corrugation at grazing — a geometric occlusion, `V(x)` in
`theta_environment_v1.md` §6. This round measures all three and reports which one, if any, moves `C`.

## §2 The model, declared before the numbers

Scene: the `PA-16` plate of `runs/LADDER/r2_relief_contrast_results.txt` (one isolated plate, `s = 12` cells
on a `p = 16` lattice, grid `128`, `pitch = 0.400100 m`, `PX_M = 3.126e-3 m`), one corrugation of period
`λ = 4 cells = 0.100025 m`, two forms — `S` sinusoidal, `T` terraced with a one-pixel riser — and amplitudes
`a ∈ {10, 68.8, 100, 316, 1000} µm`, which brackets `a*(E2) = 68.8 µm` from round 49.

Reflection is computed in **three dimensions**, per pixel, from the surface normal — the `|2α| < β` shortcut
is *not* used as the model; it is printed beside the result as the identity it is claimed to be:

```
n(x) = (−α(x), 0, 1)/√(1+α²)        v = declared camera direction (surface → camera)
r(x) = 2(n·v)n − v                  s = (sin θ_i, 0, cos θ_i)   (surface → source)
bright(x)  ⇔  arccos(r·s) < β       β = 4.65e-3 rad
```

Two camera geometries, because the answer is a function of the camera and `θ` does not carry one:

| id | geometry | consequence, derived before the run |
|---|---|---|
| `G_A` | camera on the mirror image of the source, `v = (−sin θ_i, 0, cos θ_i)` — the specular configuration | the angle between `r` and `s` is exactly `2 arctan α`, so the bright set is **`θ_i`-independent** |
| `G_B` | camera at normal incidence, `v = ẑ`, source oblique — the "fixed tripod" configuration | the bright set is `\|2 arctan α − θ_i\| < β`, a window centred on facets tilted by `θ_i/2`; it **leaves the surface** when `θ_i > 2 arctan α_max` |

Fresnel, from the record's own sheet reflectance `r = −Z₀σ_s/(2 + Z₀σ_s)`
(`scifi_boundary_v1.md` §7.5.4), generalised to incidence by the shunt-sheet boundary condition:

```
r_s(θ) = −Z₀σ_s / (2 cos θ + Z₀σ_s)      r_p(θ) = −Z₀σ_s cos θ / (2 + Z₀σ_s cos θ)
R(θ)   = (|r_s|² + |r_p|²)/2             (unpolarised; s-pol alone also reported)
```

`Z₀σ_s` is treated as a **declared grid** `{10, 30, 80, 300, 1e4}`, because no product in `runs/` records it
at `284 eV`: the value `1e4` is the record's own eV-band figure and `80` is that figure scaled by
`2.25/284`. **No single value is claimed**, and the invariance result does not depend on which one is used.

Occlusion is the horizon test of `theta_environment_v1.md` §6, evaluated on the periodic field:

```
V(x) = 1  ⇔  z(x+h) − z(x) < h·cot θ_i   for all 0 < h ≤ λ/2
I(x) = R · L_e(r(x)) · V(x)
```

## §3 Predictions

| id | prediction | falsified if |
|---|---|---|
| `Z1` | **`G_A` is exactly `θ_i`-invariant.** `C_w` in the glint channel is identical at `θ_i = 0/45/75°` to `< 1e-12` relative, for both forms, at `a = 100 µm` and `1 mm`. This is the queue's own theorem, and confirming it means the glint channel **cannot** separate `RL-2` from `RL-3` | any relative deviation `> 1e-12` |
| `Z2` | **`G_B` is a blackout, not a lever.** With the camera fixed at normal incidence, the bright set leaves the surface: `f(45°) = f(75°) = 0` exactly for the sinusoidal form at `a = 1 mm`, with onset at `θ = 2 arctan α_max − β = 3.33°`. The terraced form survives to `2 arctan(a/PX_M) = 35.5°` because its risers are ten times steeper — so the **relief form**, not the illumination, sets the angular tolerance | any bright pixel at `45°` or `75°` on the sine, or `C_w(0°)` not reproducing `3.3166` |
| `Z3` | **Fresnel gain does not move `C`.** Multiplying the image by `R(θ_i)` leaves `C_w` unchanged to `< 1e-12` relative, at every `θ_i` and every grid member. `C_w = std/mean` is scale-invariant — a theorem, verified rather than assumed | any change above `1e-12` |
| `Z4` | **The gain is bounded by `1/R(0) − 1 ≈ 4/\|Z₀σ_s\|`.** s-pol gain at `75°` `≤ 1 + 4/\|Z₀σ_s\|` on every grid member; at `\|Z₀σ_s\| = 80` the gain is `≤ 5%` (`0.021` orders of `Φ`). For a **2-D sheet** the unpolarised gain is `< 1` — a *loss* — because `R_p → 0` at grazing while `R_s → 1`, so the sheet eats with one polarisation what it gains with the other | s-pol gain above the bound, or unpolarised gain `> 1` |
| `Z5` | **Occlusion is the only `θ_i`-dependent contrast mechanism, and it needs a riser.** `f_s(75°, a = 1 mm) ∈ [2%, 6%]` on the terraced form (`a·tan75°/λ ≈ 3.7%`); `f_s = 0` **exactly** on the sine at every `θ_i` (its steepest slope `0.0314` never exceeds `cot 75° = 0.268`); `f_s(45°) = 0` on both, because shadowing needs `tan θ_i > PX_M/a = 3.13`, i.e. `θ_i > 72.3°` | `f_s` outside the window, or any shadow on the sine |
| `Z6` | **Occlusion's price in `ε`.** The riser amplitude at which half the tread is shadowed at `75°` is `a₅₀ = tread/tan 75° = 13.4 ± 1 mm`, i.e. `ε = 3.35e-2` — **195×** the glint threshold `ε*(S) = 1.72e-4` and **503×** `ε*(T) = 6.66e-5` | `a₅₀` outside `[10, 20] mm` |
| `Z7` | **`RL-2` and `RL-3` are one rung.** Separation `S_θ = max C/min C` over `θ_i` is `1.000` in `G_A` (no occlusion) and `≤ 1.10` in `G_A` with occlusion at `a = 10 mm`; the declared bar for "two rungs" is `2.0`. In `G_B` the separation is infinite and *negative in value* (the image ceases to exist), which is a hazard, not a purchase | `S_θ > 2.0` in `G_A`, or a `G_A` value that is not the maximum of the curve |

**Declared bar.** `S_θ = 2.0` is the same factor as the `L3` threshold's contrast ratio (`Q3 = 2` at
`C/C_eye = 3`, i.e. a factor 3 in contrast); it is fixed here, before the run, and cannot be moved after.
It is a *reporting* bar, not a threshold: it decides whether one rung or two appear in the ladder's table,
and it writes nothing into any product's verdict.

## §4 What this round does not do

- It does not measure the deposit. `DEPOSIT-BLIND`, `MR1.6` untouched: one declared plate, declared forms.
- It does not re-price `RL-3`'s `V = 0`. That `V` is the ladder's own claim that illumination is not the
  object; this round tests whether the rung buys anything at that price.
- It does not decide `RL-5` (`PG-03` still unmarked) and does not touch the flux gate, which erratum `E1`
  already showed to be a restatement of `L3`.
- It writes no threshold, revises no tier, and adds no environment to `E1`/`E2`/`E4` of
  `theta_environment_v1.md` — `G_A`/`G_B` are *camera* geometries within those instances, and that
  distinction is one of the round's results, not one of its assumptions.

## §5 The label hazard, disclosed

`E1`…`E4` (environments, `r2`), `G_A`/`G_B` (camera geometries, this round) and `Z1`…`Z7` (predictions)
are three namespaces on purpose: the round's finding is precisely that the first two are independent, and
using one label set for both would hide the finding inside its own notation. `RL-0`…`RL-6` remain the rungs.

---

## Errata

**E1** *(appended 2026-11-23 after the run; `Z1`–`Z7` above are untouched, and the product is
`runs/LADDER/r3_illumination_results.txt`)*

Two of the predictions carry a number derived from the terraced riser's slope, and **both used the wrong
slope**: `Z2`'s "terrace to `2 arctan(a/PX_M) = 35.5°`" and `Z5`'s "`f_s(75°, T, 1 mm) ∈ [2%, 6%]`". The
continuum riser slope is `a/PX_M = 0.320`; the **discretized** field's is `a/(4·PX_M) = 0.080`, for two
arithmetic reasons that compound:

1. the terraced profile spans `±a/2` (peak-to-peak `a`, the same convention as the sine), so the riser
   rises `a/2` per sample;
2. `np.gradient` is a 2-px central difference, so a one-sample riser is divided by `2·PX_M`.

Consequences, all arithmetic:

| registered | corrected | by |
|---|---|---|
| terrace glints to `2 arctan(a/PX_M)` = `35.5°` at `a = 1 mm` | **`9.15°`** | `2 arctan(a/(4 PX_M))` |
| `Z5` window `f_s(75°, T, 1 mm) ∈ [2%, 6%]` | **`0` exactly** — no shadow, so `Z5` is **FALSIFIED** | the facet must satisfy `tan θ_i > slope`; `0.080 < cot 75° = 0.268` |
| shadow threshold `a > PX_M cot 75° = 0.84 mm` | `a > 4 PX_M cot 75° = 3.35 mm` | same factor |

**What is unaffected.** `Z2`'s *falsifier* — "any bright pixel at 45° or 75° on the sine, or `C_w(0°)` not
reproducing `3.3166`" — is met, so `Z2` is graded CONFIRMED with its terrace figure corrected here. `Z6`'s
`a₅₀ = tread/tan 75°` is untouched: it follows from the shadow **length** `(a/2)·tan θ_i` against the tread,
which contains no slope. `Z1`, `Z3`, `Z4`, `Z7` do not reach the riser at all.

**What this does not change.** No threshold, no rung price, no tier, no verdict. `Z5`'s failure *weakens*
the occlusion lever rather than the round's conclusion: the mechanism now costs four times the relief
predicted, which is the direction the conclusion already pointed.

**One disclosure about `f_s`.** The shadowed fraction is printed twice, per **surface** and per **plate**.
They differ by up to 4× because the shadow band is phase-locked to the corrugation while the plate boundary
is not, so the plate clips the band. The surface value is the physical one; both are printed so the choice
is visible rather than silent.

---

**E2** *(`RETRO-DECLARED`, appended 2026-11-23 after the run; `Z1`–`Z7` above and `E1` are untouched)*

Checked against `docs/specs/theta_camera_v1.md` (round 51), which makes `G` a mandatory slot of `θ`. This round
**passes** the check, and it is the only one of the three ladder rounds that does: `G_A` and `G_B` are declared
in §2, both are evaluated in §3, and the comparison between them is the round's finding rather than its
premise. The retro-application therefore adds one thing only — the **status** of the two labels:

| label | what §2 declared | now |
|---|---|---|
| `G_A` specular-coupled | camera on the mirror ray, `n̂_v = r(θ_i)` | confirmed as the round's reading; noted as *not a single instrument* for an extended surface, since it requires co-rotating camera and source |
| `G_B` fixed | camera fixed on the normal, source moves | confirmed; its blackout angles (3.31° / 8.88°) are the numbers `theta_camera_v1.md` §3 and §5 now cite |

**One temptation refused.** `Z5` is `FALSIFIED` — no shadow at `75°`, `a = 1 mm`. With the camera slot declared
it is now easy to write "but at `75°` under `G_B` the plate is dark anyway", which sounds like a rescue. It is
not one, and the reason is worth recording: `Z5` predicted a non-zero **dark fraction on a lit surface** — a
shadow cast by a riser inside an otherwise bright field. Whole-field darkness under `G_B` is the absence of an
image, not a shadow, and it would be present at every `θ_i` beyond `8.88°` regardless of relief height. Using
it to explain `Z5`'s failure would attribute to geometry what `E1` already attributed to discretization — and
`E1` is the correct explanation, because the same 4× slope error also moved `Z2`'s terrace figure by the same
factor. `Z5` stays `FALSIFIED`.

---

*Content generated by AI*
