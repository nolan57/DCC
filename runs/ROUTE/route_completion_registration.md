# Route completion — pre-registration of the four phase checks

**Registered**: 2026-11-22, **before any code in this round was run.**
**Authority**: governor instruction "To Complete ALL tasks of the route", following `gd_rulings_v1.md`.
**Products**: `runs/ROUTE/` — `p0_baseline_results.txt`, `p1_delta_ov_results.txt`, `p2_clock_results.txt`,
`p3_me3_jmu_results.txt`, plus the Phase 0 frame and its `.display.txt` block.

Each prediction below is falsifiable and stated in advance. If a prediction fails, the conclusion is weakened or
withdrawn rather than reinterpreted (the rule applied in `crosswalk_checks` X1 and in the stage-1 retraction).

---

## Phase 0 — S0/FL1 baseline, gate `ME4`

State set (as in the existing probes): `S_sheet` (one plate of thickness `t`), `S_stack` (two plates separated by
`5t`), `S_slab` (intact 70 mm body, zero conversion). Voxel complex on a lattice with pitch `h_v`.

| id | Prediction | Falsifier |
| --- | --- | --- |
| **P0a** | `β₁ = 0` for all three states — none contains a handle. ME4 clause 3 **PASS** | any state with `β₁ ≥ 1` |
| **P0b** | `N_comp = 1, 2, 1` for sheet, stack, slab respectively | any other count |
| **P0c** | **`χ` convention is mixed in the registered number.** `χ(solid ball) = 1`, `χ(its boundary) = 2`, `χ(disc) = 1`. The registered comparison `χ(2D)/χ(3D) = 1.18e10/2 = 5.9e9` therefore divides a *solid* count by a *surface* count. Under one convention the ratio is `1.18e10/1 = 1.18e10`; under the other, `2.36e10/2 = 1.18e10`. **Factor 2, and the conclusion is unchanged** | if the two same-convention ratios differ from each other |
| **P0d** | `CM5`: `μ_ov = 0` for `S_sheet` at `Δz_res > t`, `μ_ov = 1` for `S_slab` at any `Δz_res < 70 mm`, `μ_ov = 1` for `S_stack` below the gap | any of these three |
| **P0e** | ME4 clause 1 (monotonicity) is **not testable** at a single state; clause 2 (census match) is an **endpoint** condition and not applicable. Phase 0's gate is therefore clause 3 only | if clause 2 can be evaluated at the baseline |

**Prohibitions carried in.** No `δ` value may be chosen to make `CM5` pass; the frame may not claim to be a
faithful reflected-light frame (ME5 corollary); every `CM5` number carries `(t, derived-or-convention, Δz_res)`.

---

## Phase 1 — `δ_ov` derivation, falsifier = state-independence

`δ_ov` is defined as the **maximum `μ_ov` that a graph can produce under the `μ_ov` estimator** at a declared
`(Δx, Δz_res)` and slope class `s_max = ‖∇z‖_∞`.

| id | Prediction | Falsifier |
| --- | --- | --- |
| **P1a** | For the exact (continuum) estimator, `μ_ov = 0` for any graph with `s_max·Δx < Δz_res`. So `δ_ov = 0` is **achievable**, not merely "natural" | a graph with `s_max·Δx < Δz_res` and `μ_ov > 0` |
| **P1b** | For the **discrete** estimator (voxel centres, pitch `h_v = Δz_res`), overlap is reported iff the surface rises by `≥ Δz_res` across one lateral cell, i.e. `s_max·Δx ≥ Δz_res`. Below that, `μ_ov_est = 0` | a below-threshold case reporting overlap |
| **P1c** | `δ_ov` is a function of `(Δx, Δz_res, s_max)` **only**, so it is identical for `S_sheet`, `S_stack`, `S_slab` when each is a graph of the class. **The registered falsifier (state-independence) passes** | any variation across states at fixed `(Δx, Δz_res, s_max)` |
| **P1d** | At the declared resolutions, `δ_ov = 0` changes **no** verdict. Phase 1's relaxation is therefore **vacuous at the declared resolution** and becomes non-vacuous only for steep surfaces (`s_max·Δx ≥ Δz_res`) | any verdict that flips at `δ_ov = 0` |

---

## Phase 2 — clock and exposure (GD5 form)

`t_rip = √2 L / c = L / c_s`, `c_s = c/√2`.

| id | Prediction | Falsifier |
| --- | --- | --- |
| **P2a** | `t_rip = 9.43e-10, 4.71e-9, 3.30e-10 s` for `L = 0.20, 1.00, 0.070 m` | any value off by more than rounding |
| **P2b** | Reflected channel needs `2L/c = √2·t_rip`, so `2L/c > t_rip` by **exactly 1.414214** for every `L` — the corollary is an identity, not an estimate | any `L` where the ratio differs from `√2` |
| **P2c** | Transmission admits `τ_exp ≤ t_rip`, i.e. the reflected channel's required exposure is infeasible by exactly `√2` | — |
| **P2d** | Contrast-limited photon requirement per resolution element `N = SNR²/Δτ²`: at `Δτ = 1e-3` (284 eV) `N = 9e6`; at `Δτ = 1e-7` (visible) `N = 9e20`. The **visible** channel cannot acquire inside `t_rip`; the **284 eV** channel can, given a declared source | if the visible channel's requirement is achievable |

**GD5 falsifier**: the route terminates if no admissible exposure exists. Predicted verdict: **it does not
terminate** — an admissible exposure exists in the transmission channel at 284 eV, but not in the visible
reflected channel (which the frozen corollary already forbids).

---

## Phase 3 — `ME3` separation and the `J^μ` instrument

| id | Prediction | Falsifier |
| --- | --- | --- |
| **P3a** | `δ_E(S_sheet) ≲ 1e-12`, `δ_E(S_slab) ≈ 1` — separation `≥ 10` decades | separation `< 3` decades |
| **P3b** | Because the separation is `≥10` decades, **any** `δ_E,max ∈ (1e-10, 1e-2)` yields the same verdict for every state in the record. The threshold is therefore **verdict-insensitive** here — the opposite of `CM5`/`Δz_res`, which decided everything | any `δ_E,max` in that interval flipping a verdict |
| **P3c** | The particle current `J^μ = n u^μ` on the **prescribed** (D2) background satisfies `∇_μ J^μ = 0` identically for static `n`, and `J^0 = n c ≠ 0`. So the directive's "zeroed current = failure" test **does not fire** | non-conservation for static `n`, or `J^0 = 0` |

**Proposed** `δ_E,max = 1e-2`, on the stated ground that it is the 2D-reduction's perpendicular-kinetic-energy
accuracy (1 %), **not** because it makes anything pass — P3b is what licenses that claim. Flagged for
ratification as `GD6`.

---

## What this round will NOT claim

- Phase 4 (`FL1 → FL2 → FL3`) **cannot start**: Phase 3 closes only if `δ_E,max` is ratified and the instrument
  is accepted as an instrument (it works on prescribed backgrounds only, which is exactly `D2`).
- No physics result is produced by Phases 0–2 beyond bookkeeping, kinematics, and estimator bias.
- No archived product is edited; no threshold is moved; no state is certified as two-dimensional.

---

*Content generated by AI*
