# Route completion — Phases 0–3 executed, Phase 3 blocks Phase 4

**Registered**: 2026-11-22
**Authority**: governor instruction "To Complete ALL tasks of the route", under `docs/decisions/phased_relaxation_route_v2.md`
(as amended by `gd_rulings_v1.md`).
**Pre-registration**: `runs/ROUTE/route_completion_registration.md` — written before any code ran, and honoured,
including where its predictions failed.
**Products**: `runs/ROUTE/p0_baseline_results.txt`, `p1_delta_ov_results.txt`, `p2_clock_results.txt`,
`p3_me3_results.txt`, `s0_frame_fl1.png` + its `.display.txt`.

---

## 0. Verdict table

| Phase | Verdict | Deliverable |
| --- | --- | --- |
| **0** — baseline, gate `ME4` | **DELIVERED** | S0/FL1 frame + declaration block; `ME4` clause 3 PASS |
| **1** — `δ_ov` / O6 | **PASS-WITH-NARROWING** | `δ_ov` derived; the admissible set is `{0, 1}`, and neither value is usable |
| **2** — clock | **PASS** | `t_rip` exact; admissibility decided per channel; GD5 falsifier does not fire |
| **3** — `ME3` | **BLOCKED** | `ME3` has no verdict until `φ` is declared; `J^μ` instrument built and limited |
| **4** — `FL1→FL2→FL3` | **NOT STARTED** | depends on Phase 3 |

**The route is executed as far as it can be, and it stops in Phase 3 for a reason that is in the *spec*, not in the
route.** Two registered predictions failed and are reported as failed; one registered arithmetic error is corrected
and recorded; one proposal licensed by a failed prediction is withdrawn.

---

## 1. Phase 0 — delivered

**Gate.** `ME4` clause 3 (no handles; contractable) **PASS** on all three states: `β₁ = 0`, `χ = N_comp` exactly
(`1,2,1` for sheet, stack, slab). Clauses 1 and 2 are **not testable at a baseline** — monotonicity needs a sweep
sequence, and the census match is an endpoint condition (`N_comp = 1 ≪ 1.18e10`).

**So the gate certifies no tearing, and nothing about two-dimensionality.** The product's permitted wording was
fixed in `gd_rulings_v1.md` §1.3 and is used verbatim in the frame and in `p0_baseline_results.txt`.

**Self-correction inside the round.** The first run of the module reported `slab → μ_ov = 0` at coarse `Δz_res`,
because the 24-voxel lattice cannot hold a 70 mm body. That is a finite-box artefact, not physics. The CM5 table was
rebuilt with the **analytic span** as primary and the lattice as a cross-check that now reports `n/a` outside the
box. The correction is stated inside the archived output rather than silently applied.

**Finding `P0c` — a factor-2 error in a registered ratio, conclusion unchanged.** `χ(solid ball) = 1` while
`χ(boundary surface) = 2`. The registered comparison `χ(2D)/χ(3D) = 1.18e10/2 = 5.9e9` divides a *solid* count by a
*surface* count. Under one convention the ratio is `1.18e10/1`; under the other, `2.36e10/2 = 1.18e10`. **The two
agree exactly** (relative difference `0.00e+00`), so the correct ratio is `1.18e10`, the registered one is `2×` too
small, and the conclusion (`χ` must *increase*, so "`χ` must not change" was inverted) is unaffected.

**Finding `P0d` — the knife edge is at `t − h_v`, not `t`.** The measured switch converges `0.667 → 0.833 → 0.917 →
0.958` as `h_v = t/3, t/6, t/12, t/24`. The occupied set is sampled at voxel *centres*, so the largest separation
inside a plate of thickness `t` is `t − h_v`. This is the **fourth independent appearance** of the same edge
(crosswalk §3.1, X1, R1). It is a sampling property, so no amount of care in stating `t` removes it — only stating
`h_v` does.

---

## 2. Phase 1 — `δ_ov` derived, and it is not a tolerance

**The objective was met.** `δ_ov := sup over graphs of μ_ov_est`, with the estimator geometric rather than modelled:
a column's lateral footprint contributes the `(max − min)` of `z`, so the column reads double-valued iff that span
`≥ Δz_res`.

**Two registered predictions failed, both for the same reason — the registered span bound was wrong.**

| Prediction | Registered | Measured |
| --- | --- | --- |
| `P1b` | `span_max = s_max·Δx` | `span_max = (1 − 1/C)·d·s_max·Δx`, with `d ∈ [1, √2]` |
| `P1a` | `μ_ov = 0` for every graph at `Δz_res > s_max·Δx` | fails at 1.02× (one graph flags), holds only above `√2·s_max·Δx` |

The corrected form was **decomposed exactly**, not fitted: the sampling offset `(1 − 1/C)` was verified against
`C = 12, 24, 48, 96` to residuals of `1e-17`, and the direction factor `d = √2` was confirmed as `diag/plane =
1.4142`. Both are multiplicative constants of the estimator, not properties of any surface.

**The substantive result.** With `δ_ov` defined as a quantile bias it is **state-dependent** — at `Δz_res` half the
edge, four graphs with identical `s_max` give `μ_ov = 1.000, 0.625, 0.078, 0.125`, a spread of `0.92`. That fires
the registered falsifier, and it is reported rather than reinterpreted. The only state-independent definition is the
worst case, and it is **binary**:

```
δ_ov = 0   for  Δz_res > √2 · s_max · Δx        (inert: every state already passes the strict test)
δ_ov = 1   for  Δz_res ≤ √2 · s_max · Δx        (vacuous: μ_ov = 1 is admitted, so the intact slab passes)
```

**There is no third value**, because anything in `(0,1)` is either state-dependent or arbitrary. So Phase 1's
relaxation target exists, is unique, and **cannot be used**: raising it from 0 to its only other setting destroys the
discrimination the criterion lives on. Phase 1 relaxes nothing that was binding — consistent with `GD1` Option B,
which had already moved `CM5` out of the gate set.

**And the window is closed anyway.** For `CM5` to convict the converted state it must resolve the interlayer spacing
(`Δz_res ≤ 8.62e-12 m`); to acquit a real surface it must tolerate that surface's roughness
(`Δz_res > s_max·Δx`, hence `Δx < g_min/s_max`). At the S0 sampling scale of `100 μm` the window is closed by a
factor of **25** for atomic roughness over a `100 μm` correlation length, **116** for a surface flat to 1 nm over
`100 μm`, and **2.5e6** for atomic roughness over a 1 nm correlation length. A single `(Δx, Δz_res)` pair cannot
both see the layering and tolerate the roughness.

---

## 3. Phase 2 — the clock exists, and it is exact

`t_rip = √2 L/c` gives `9.434617e-10`, `4.717309e-9`, `3.302116e-10 s` for `L = 0.20, 1.00, 0.070 m`. The round trip
exceeds it by `1.414213562373` for every `L` — an identity, so the reflected channel has **zero** exposure budget.
`Λ_max` is retired and there is nothing to calibrate.

**Detection.** `N = (SNR/Δτ)²` per resolution element, so `9e6` at `Δτ = 1e-3` (284 eV) and `9e14` at `Δτ = 1e-7`
(visible). The requirement is **per unit area** and independent of the frame size, while the power it costs scales
with frame area. Consequence, at a declared `1e6 W` source:

| Channel | Flux required | Max frame side | Verdict |
| --- | --- | --- | --- |
| transmission, 284 eV | `9.54e23 m⁻² s⁻¹` | `0.152 m` | **admissible** (sub-field) |
| transmission, visible | `9.54e31 m⁻² s⁻¹` | `3.3e-3 m` | not admissible in practice |
| reflection, any band | — | `0` | **impossible** (frozen corollary) |

**GD5's falsifier does not fire**: an admissible exposure exists. The condition attached is that every such frame
declares its sub-field side — at `0.15 m` the canvas needs `~1.4e10` frames, and a sheet exists for one `t_rip`, so
that is `1.4e10` separate sheet events. The picture is not readable from one object.

> **Annotation 2026-11-22 (`GD8`) — the reflection row's "impossible" carries a premise.** The corollary is a
> statement at observer distance `D = L`, and `GD8` has now written that premise into the spec
> (`meff_boundary_v0_2.md`). The verdict above is unchanged *for naked-eye viewing*, because `D = L` is the most
> favourable case there: naked eye needs `D ≥ 0.25 m`, and `D ≥ L/√2` holds for every `L ≤ 0.3536 m`, so the
> conclusion applies a fortiori (`fl_coordinate_results` F-5). What changes is the row's scope, not its verdict:
> "impossible" is a statement about `D = L` **and beyond**, never a statement about every geometry.
> A per-patch window exists in principle for near-field instrumented frames; `GD8` did not adopt it, and it is
> recorded as an unregistered observation that licenses no frame (`route_goal_conformance_v1.md` F3).

**A registered arithmetic error, corrected and recorded.** The pre-registration stated `N = 9e20` at `Δτ = 1e-7`;
the correct value is `9e14` — a dropped factor of `1e6`. The verdict is unchanged (both are unattainable in-frame),
but the number is fixed in the product and the error is recorded rather than quietly absorbed.

---

## 4. Phase 3 — blocked, and the block is in the spec

### 4.1 `ME3` has no verdict, because `φ` is not declared

The adopted statement is `δ_E := ∫ρ(∂_zφ)² / ∫ρ[(∂_xφ)² + (∂_yφ)²] ≤ δ_E,max`, and **`φ` is defined nowhere in
v0.2**. Two natural declarations were evaluated:

| Declaration | `δ_E`, converted sheet | `δ_E`, intact body | Direction |
| --- | --- | --- | --- |
| `φ` = the material field (density-like) | `1.69e26` | `4.05e-1` | **inverted** — thinner scores worse |
| `φ` = a velocity potential, `u_⊥/u_∥ = t/λ` | `5.93e-27` | `~1` | intended |

They differ by `(λ/t)^4 = 2.8e52` and give **opposite verdicts on the same state**.

The scaling behind the first column is exact in the separable case, not fitted: with
`φ = sin(2πx/λ)·sin(πz/t)`, `δ_E = (λ/2t)²`, confirmed on `t = 8, 16, 32, 64` with residuals
`1.0082 … 1.0103` after correcting for the difference operator's attenuation of the lateral mode. So
`δ_E(material) → ∞` as `t → 0`: **the criterion is most violated by the most perfectly two-dimensional state.**
This is the same defect class as `C_top` (inverted), `Λ_max` (inverted) and `ME1`'s knife edge — the fourth instance
in this project, and the first one inside the adopted `ME` set.

### 4.2 The proposed threshold is withdrawn

`δ_E,max = 1e-2` was proposed in the pre-registration **on the explicit ground that `P3b` would show the threshold
to be verdict-insensitive**. `P3b` failed: the two declarations require `δ_E,max ≥ 1.7e26` and `≥ 5.9e-27`
respectively, `2.8e52` apart, so the value *decides* the verdict. The licence for the proposal is void, so **no
`δ_E,max` is registered in this round** — not a different value, none.

### 4.3 The `J^μ` instrument exists, and its limit is `D2`

`J^μ = n u^μ` with static `n` on a prescribed background is conserved **identically**
(`∇_μJ^μ = (1/√γ)∂_t(√γ n) = 0`), verified on a curved `γ_ij` with `max|∇_μJ^μ| = 0.0e+00`, and `J⁰ = ⟨n⟩c ≠ 0`
for every state. So the directive's "zeroing of the conserved current is a failure" clause **does not fire**.

**Declared limitation**: on a *solved* background `u^μ` must come from the evolution, which does not exist (the R4
grid-scale instability remains unlocalised in the bulk). The instrument therefore works on `D2` states only. It is an
instrument, as `GD4` specified — not a gate.

---

## 5. Phase 4 — not started, and correctly so

`FL2`/`FL3` are strictly postponed by the directive until Phases 0–3 close. Phase 3 is blocked, so **no FL2 or FL3
frame was produced**, and none should be. What `FL2`/`FL3` would require is unchanged and unaffected by this round:
a compliant `σ_s(ω)` with a *solved* `τ` (`G6`), `R5-L3/L4`, the `G0↔P2` unit bridge, and the `ME5` corollary on
every frame. None of those was touched.

---

## 6. What is now needed to unblock Phase 3 — `GD6`

The block is one undeclared symbol, and it cannot be resolved by the executor: choosing `φ` chooses the physics.

1. **Does `ME3` mean the material field or a velocity potential?** If material, the criterion is inverted and must be
   replaced (by `(t/λ)²`, or by `δ_E ≤ δ_E,max` with the ratio inverted) rather than re-toleranced. If velocity, `φ`
   must be declared in the spec and an instrument for `u_⊥/u_∥` must exist — none does, since the only velocity
   field in the record is `u^μ = (c,0,0,0)`, for which `u_⊥ = 0` identically and `δ_E = 0` trivially.
2. **Consequence of answering**: only after this can `δ_E,max` be registered, Phase 3 run, and Phase 4 start.

Registered as **`GD6`** in `docs/specs/meff_boundary_v0_2.md` open items and in the registry.

---

## 7. What this round changed, and what it did not

**Changed**: Phase 0's deliverable exists (a frame, a declaration block, a gate verdict with restricted wording);
Phase 1's tolerance is derived and shown to have no usable setting; Phase 2's clock is verified and its falsifier
tested; Phase 3's target is shown ill-posed; one `χ` ratio corrected by a factor 2; one knife edge located at
`t − h_v`; one arithmetic error in the pre-registration corrected; two predictions reported as failed; one proposal
withdrawn.

**Not changed**: no threshold was relaxed or registered; no archived product was edited; `δ_ov`, `Δz_res`, `ℓ_samp`,
`Δz_tol` remain OPEN and `δ_E,max` joins them; no state is certified as two-dimensional; no physics result was
produced beyond kinematics, estimator bias and one conservation identity.

---

*Content generated by AI*
