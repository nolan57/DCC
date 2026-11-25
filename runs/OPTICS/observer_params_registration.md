# Registration — `RQ-09`, the four unset observer parameters

**Written**: 2026-11-23, before `src/route/observer_params.py` existed.
**Question** (`round_queue_v1.json` `RQ-09`): *what are `Δz_res`, `δ_E,max`, `ℓ_samp`, `Δz_tol`, and what sets
each?*
**DoD**: each parameter bound **from the response**, with its derivation and a stated floor; no visibility
conclusion (`S9`).
**Source**: `reports/DCC_research_progress_v1.md` §8 open list; `docs/specs/meff_boundary_v0_2.md` §1–§2.
**Product**: `runs/OPTICS/observer_params_results.txt` (emitted by the program, not transcribed).

---

## 1. What "bound from the response" is allowed to mean

The record's standing prohibition (`meff_boundary_v0_2` §1, `phased_relaxation_route_v2` §2) is: **a tolerance
may not be back-solved from a desired verdict.** A round that reads `Δz_res`, `ℓ_samp`, `Δz_tol`, `δ_E,max` out
of the archived *verdicts* would be committing exactly the A5 error the prohibition names.

So this round binds nothing from a verdict. It asks a narrower question, which is decidable before any verdict
is computed:

> **Is each parameter a function of something already declared?**

Three outcomes, all of them results, and only the first two count as "bound":

| outcome | meaning | binding status |
| --- | --- | --- |
| **FUNCTION** | the parameter is determined by quantities already in `θ` or in the frame's own declaration; the experimenter makes no choice | **bound** — the value is computed, not selected |
| **INVARIANT** | a choice remains, but the criterion's verdict is constant over the whole admissible range of that choice | **bound** — the choice does not decide anything |
| **NOT BINDABLE** | the choice moves the verdict and nothing else fixes it | **open**, and the round must say so rather than pick |

A fourth case is anticipated and it is not a tolerance problem at all: a parameter whose *entire* admissible
range is vacuous (every object passes at every value) or redundant (it reproduces a predicate the record already
has). That is **VOID**, and a void parameter must be removed from the open list rather than bound, because no
measurement can ever settle it.

## 2. The four names and their arguments, declared before anything is computed

| parameter | lives in | its criterion | what could set it (a priori) |
| --- | --- | --- | --- |
| `Δz_res` | `CM5` (ex-`ME1`) | `μ_ov(Δz_res) ≤ δ_ov` | the observation channel: `θ`'s **band** (optical axial resolution) or `θ`'s **gate** (range resolution) |
| `ℓ_samp` | `ME2` | `ℓ_samp·‖∇z‖_∞ ≤ Δz_tol` | the frame's pixel pitch |
| `Δz_tol` | `ME2` | same | the viewer's depth acuity at the declared distance, *or* the display's depth quantiser |
| `δ_E,max` | `ME3` | `δ_E ≤ δ_E,max` | nothing — `ME3` is retired (`me3_phi_disposition_v1.md`) |

The a-priori claim is therefore: **none of the four is a free number.** Three are functions of declared
quantities; the fourth is void. If that claim is false the round will show it by exhibiting a parameter whose
verdict moves with a choice that nothing fixes.

## 3. Constants this round uses, and their provenance

| symbol | value | status |
| --- | --- | --- |
| band | `1–3 eV` | the record's reported optics band (`DCC_research_progress_v1.md` §7.2) |
| `hc` | `1.239841984e-6 eV·m` | exact |
| `NA` | `0.1 … 1.0` | instrument choice, **declared here** as the admissible range |
| `c` | `299792458 m/s` | exact |
| gate | `3 ns` | `Path A`'s declared instrumented observer (`relaxation_ladder_v1.md` §5, `PG-03`) |
| `d_∥` | `15.4 fm` | `meff_boundary_v0_2` §ME1 — **convention**, not derived (spec's own amendment) |
| slab thickness | `0.07 m` | the intact body used in the archived `ME1` checks |
| pitch | `0.4001 m`, `CELL = pitch/16`, `PX_M = CELL/8`, `λ = 4·CELL` | `demo_object_v1` §2; ladder rounds 49–50 |
| `a(ε)` | `ε·pitch` | the ladder's own definition of relief amplitude |
| `ε*` | `1.720e-4` (S form) | `r2_relief_contrast_results.txt` §3, the measured glint threshold |
| `ε_max` | `0.318229` | `r2` §Y6, the deposit's geometric limit |
| `D` | `0.25 m` | naked-eye near point, `fl_coordinate_results` F-5 |
| `b` | `65 mm` | interocular baseline, **declared here** as a convention |
| `δθ` | `30 arcsec` | stereoacuity, **declared here** as a convention |

Two of these (`b`, `δθ`) are new declarations in this round. They are declared as **conventions with a stated
source**: both are standard values, neither is measured by this project, and both enter only through the product
`D²δθ/b`, so a reader who prefers other values scales the result by their ratio.

## 4. Method, per parameter

**`Δz_res`.** Two channels, both computable:
- optical axial resolution `Δz = λ/(2·NA²)` with `λ = hc/E` over the band → an interval;
- range resolution of a gate `Δz = c·δt/2` (round trip) at the declared `3 ns` → a point.
Then `μ_ov` for a one-interval column is `1` if `t ≥ Δz_res` else `0` (the spec's own statement), so the census
gives the switch points, and the question becomes: **is the instrument band inside or outside the plateau?**

**`ℓ_samp`, `Δz_tol`.** The criterion contains neither alone; it contains the ratio. Test: rescale both by `k`
and show the criterion's value is unchanged. If so, "two parameters" is one, and the one is `s_max = Δz_tol/ℓ_samp`.

**ME2's verdict.** With `Δz_tol` at the viewer's reading (`D²δθ/b`), `ℓ_samp` at a declared pixel pitch, compute
`s_max` and compare with the deposit's measured slopes. Report the `ε` at which the criterion switches, because
that number is the criterion's only content.

**The slope measurement.** Max slope is computed analytically for both forms and **measured** on grids of
`1, 2, 4, 8, 16, 32` pixels per riser, with the analytic value as the limit. This is a deliberate re-test of
round 50's error (a 2-pixel central difference halves a one-pixel riser's slope), promoted from a post-hoc
explanation to a pre-registered convergence check.

**`δ_E,max`.** Two readings of `φ`, both already in the record:
- `φ` a **potential**, `u^μ = (c,0,0,0)` ⇒ `∂_z φ = 0` ⇒ `δ_E = 0` identically;
- `φ` the **signed distance** to the surface ⇒ `δ_E = R/t` exactly (`me3_phi_registration.md` P8).
Test whether the second reading is an independent criterion or a thickness criterion in disguise, by comparing
the rank order of `δ_E` with the rank order of `1/t` on the census. Then the dichotomy: is there **any** value of
`δ_E,max` that fails some object and passes another without being a thickness threshold?

## 5. Predictions, with numbers, before the program exists

| id | prediction | falsifier |
| --- | --- | --- |
| **Q1** | `Δz_res` is a function of `θ`'s band and gate only; the optical interval's endpoints are in the exact ratio `λ(1 eV)/λ(3 eV) = 3.000` | any dependence on a quantity outside `θ`, or a ratio off `3.0` by more than `1e-12` |
| **Q2** | optical band `= [206.6 nm, 62.0 µm]`, width `2.477` decades | width outside `2.477 ± 0.01` |
| **Q3** | over that whole band the census verdicts are constant, with `≥ 3` decades of margin on both sides: plate a graph by `7.13` dec, slab not a graph by `3.05` dec | any margin below 3 decades, or a verdict that flips inside the band |
| **Q4** | the slab becomes a graph only for a gate coarser than `467 ps`, i.e. `6.42×` the declared `3 ns` — so the declared gate already erases it, and the optical channel never does | a `Δz_res` inside the optical band that makes the slab a graph |
| **Q5** | ME2 is invariant under `(ℓ_samp, Δz_tol) → (k·ℓ_samp, k·Δz_tol)` to `1e-15` relative for `k ∈ {1e-6, 1, 1e3, 1e6}` | any `k`-dependence above `1e-15` |
| **Q6** | at the viewer's reading, `s_max = 0.7956` and ME2 passes the deposit at `ε*` by `368×` (sine) and `36×` (terrace) | a margin below `10×` |
| **Q7** | the terrace's max slope exceeds the sine's by exactly `32/π = 10.186` at equal peak-to-peak amplitude, measured to `1%` on a converged grid | ratio off by more than 1% |
| **Q8** | the measured slope is below the analytic value at every finite grid and the deficit **halves** as the grid doubles (the 2-pixel central difference), reaching `1.00 ± 0.02` by 32 px/riser | a deficit that does not shrink, or a measured value **above** analytic |
| **Q9** | `δ_E` under the signed-distance reading ranks objects exactly as `1/t` does, so the informative window of `δ_E,max` is a thickness threshold; under the potential reading `δ_E = 0` for all three objects, so no value fails anything | a pair whose `δ_E` order differs from its `1/t` order |
| **Q10** | the count: four names → two distinct computable quantities (`Δz_res`, `s_max`) → **zero** free parameters | a parameter that survives as free |

## 6. What this round will not do

1. **No membership verdict.** No object is certified in `ℳ_eff` or out of it (`meff_boundary_v0_2` §1).
2. **No visibility conclusion** (`S9`). The word does not appear in the product except in this sentence.
3. **No registered threshold.** The round computes what the tolerances *are functions of*; it registers none.
4. **No reclassification.** `GD1` Option B moved `ME1` out of `ℳ_eff` because "an observation predicate
   evaluated at an instrument resolution is not a gate on a physical state". If `ME2`'s tolerances are found to
   be presentation properties, the same argument applies to `ME2` — but moving a gate is a governor act, so the
   finding is recorded as a board note and the gate set is left byte-identical.
5. **No `δ_ov`.** It is a separate parameter with a separate owner (`GD3`, Phase 1) and is not in `RQ-09`'s
   question.

## 7. Reverse-on clauses

- **Q3** reverses if a channel exists whose `Δz_res` lands inside `(15.4 fm, 0.07 m)` — that would make the
  parameter a live dial and the binding would collapse to "choose a channel".
- **The `ME2` finding** reverses if `Δz_tol` can be shown to be a physical constant rather than a viewer's
  acceptance — the spec's own sentence says the opposite, so the reversal would have to be a ruling.
- **Q9** reverses if a reading of `φ` exists that is neither degenerate (identically zero) nor a thickness in
  disguise. `ME3`'s retirement already asserts none does; this round is the check.

---

## Errata

**E1** *(appended 2026-11-23 after the run; predictions unchanged and `Q8` stays `FALSIFIED`)*

`Q8` predicted that the measured max slope would sit below the analytic value at every finite grid and that the
deficit would halve as the grid doubles. The second half is wrong. Measured:

| px per riser | measured / analytic |
| --- | --- |
| 1 | `0.500000` |
| 2 | `1.000000` |
| 4, 8, 16, 32, 64 | `1.000000` |

So the deficit is not a convergence rate: it is **exactly `0.5` at one pixel per riser and zero at two**, because a
two-pixel central difference straddles the whole jump only when the riser is one pixel wide. There is no grid at
which the value is `0.7` or `0.9`. The clause it was meant to protect — round 50's factor of `2` — is confirmed
exactly, which is the part that mattered; the "halving" language described a gradual limit that the statistic does
not have.

**E2** *(same round; a numerical trap found while building §7, recorded because it inflates the answer)*

Two ways of building the terraced field both produced a max slope **above** the truth, and neither raised an error:

1. `ph = (x % period)/period` on a float grid loses precision at large `x` through the modulo, so the
   ramp's sample count silently changes with position. Replaced by an integer phase (`idx % per`).
2. Tiling a one-period sawtooth puts a **zero-width cliff** at the period boundary, where the down-riser should
   have width. `max|dz/dx|` latches onto that cliff and reports exactly `2×` the riser slope from `n = 2` upward.
   Replaced by an explicitly built period (up-riser, tread, down-riser, tread).

Lesson, worth carrying: **`‖∇z‖_∞` is a supremum and therefore the first statistic to be captured by an artefact.**
Any round that reports it must show the grid it used and the period it used.

---

*Content generated by AI*
