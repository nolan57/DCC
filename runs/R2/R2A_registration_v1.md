# R2-A homogeneous Bianchi-I forward solution — execution registration (v1.4 §8.5 / Sprint 2)

**Date**: 2026-11-21
**Execution method**: building on the frozen P2 assets of the DCC main chain + this round's machine re-derivation of the three §4.4 checks (G3′ prerequisite)
**Evidence level**: MODEL RESULT

## §8.5 item-by-item mapping

| §8.5 requirement | Status | Inherited asset / evidence |
|---|---|---|
| Action S=∫√-g[R/2κ−½(∇φ)²−V(φ)−¼Z(φ)F²], Z>0 | **Implemented** | `DCC_P2_homogeneous.py` (v=1, λ=1, α=0.5, Z=e^{αφ/v}) |
| Independent symbolic derivation of all Einstein components + scalar equation + Maxwell equations + dF=0 | **Implemented** | `DCC_sympy_derivation.py` (sympy_stdout.txt; P2 validation: homogeneous limit / flat slicing / Kretschmann all assertions passed); this round `src/r2_homogeneous/inverse_problem_check.py` independently re-derived Bianchi-I G_μν (three anchors: V1 isotropic 3H² / V2 vacuum Kasner / V3 Maxwell stress, ALL PASS) |
| Full conservation law ρ̇+2H_A(ρ+p_A)+H_B(ρ+p_B)=0 | **Implemented** | P2 solver evolves according to the conservation law; this round's check ① gives the required stress budget (machine output κρ=h²−2γh, κp_x=p_y=γh−γ²−h², κp_z=−3h²) |
| Test: isotropic limit reproduces FRW | **PASS** | inverse_problem_check V1 (G_00=3H² machine identity) |
| Test: vacuum limit reproduces Misner/Kasner | **PASS** | inverse_problem_check V2 (Kasner (2/3,2/3,−1/3) G_μν=0) + P2 vacuum-only case (H_C≡−0.125 persists, Kasner-type shear) |
| Test: h=0 stress-budget coefficient check (4.4 check ①, 3/2 factor) | **PASS (conclusion upgraded)** | runs/R2/check123_results.txt: v1.1 relation = overall sign flip of the machine budget; h=0 target requires (ρ,px,py,pz)=(0,−γ²/κ,−γ²/κ,0) -- contradicts the Maxwell source in all components and violates NEC; "ρ_B=γ²/κ automatically satisfies the budget" is falsified |
| Acceptance: Ham constraint residual < registered threshold and no drift | **PASS** | P2 homogeneous 132 cases: C_H_max≤6.8e-6 (threshold 1e-4) |
| Acceptance: scan of Z(φ), V(φ) and initial data | **PASS** | P2 132-case table (baseline/shear/magnetic-only/vacuum-only/true-vac, etc.) |
| Acceptance: curvature invariants, energy density | **PASS** | P2: K_max≤0.266, ρ_min≥0, ρB_max bounded |
| Acceptance: linear perturbative stability | **EXECUTED at screening level (2026-11-21)** *(row corrected 2026-11-22: it still read OPEN after the run)* | = P2-C6, 5/5 PASS — `runs/R2/r2c6_linear_stability_results.txt`: λ_max ≤ 0.029 vs the registered bound 1.05·√2 = 1.48492 on 5 backgrounds; "no identified catastrophic linear instability" at the homogeneous-sector + test-field scope. **Production gauge-fixed cosmological perturbation theory (coupled metric perturbations at k≠0) remains OPEN** — this row is not a production closure |
| D2 achieved | **PASS** | P2: magnetically driven H_C crosses to negative (D2=True), W3 no-flux control H_C≡0 (causal closure) |

## New G3′-level conclusions this round (from §4.4 check ②)

1. **Two-level NEC determination** (runs/R2/check123_results.txt): the required stress for the constant-rate target (h,−γ)
   is κ(ρ+p_z)=−2h(h+γ)<0, κ(ρ+p_x)=−γ(γ+h)<0 -- NEC violated for any h,γ>0;
   power-law feasible region: z direction 2α(1−α−β_C)≥0, x direction (α−β_C−β_C²−αβ_C)≥0, Ham requires α≥2β_C.
2. **Quantitative determination for the D2 specified background (1/2,1/2,−1/2)**: t²κρ=−1/4<0 (Ham requires negative energy),
   t²κ(ρ+p_x)=−(1+t²)/4<0 -- this background is NO-GO within the specified action and can only serve as a phenomenologically specified background
   (the P3/P4 "specified contraction background" annotation must be permanently retained); z-direction NEC=0 (saturated), consistent with its "power-law specified"
   nature.
3. The P2 homogeneous forward solution (magnetic sector) is an NEC-saturated trajectory (NEC_min=0, same determination as runs/G0), consistent with
   this round's analytic feasible region -- the forward-solution and inverse-problem layers corroborate each other.

## Remaining items

- P2-C6 linear perturbative stability (the last G3′ acceptance item) -- **EXECUTED at screening level (2026-11-21,
  `src/r2_homogeneous/linear_stability_c6.py` → `runs/R2/r2c6_linear_stability_results.txt`, 5/5 PASS)**:
  tangent-flow Lyapunov analysis of the frozen 8-variable homogeneous state on 5 registered backgrounds
  (lambda_max <= 0.03 vs the registered catastrophic bound sqrt(2 lam v^2) = 1.414) + k!=0 test-field scalar sector
  (tachyonic anchor validated to 1e-6) + constraint control under initial-data perturbation (2.1e-7 < 1e-4).
  Verdict at screened scope: **no identified catastrophic linear instability**; the barrier-top tachyonic mode is the
  registered bubble-nucleation mechanism. Production gauge-fixed cosmological perturbation theory (coupled metric
  perturbations at k!=0) remains the registered boundary of this assessment;
- Incorporation of the N11 constraint stress P_2D as an R2-D L3 boundary condition -- **EXECUTED at the 1+1 slab layer
  (2026-11-21, `src/r2_redshift/slab_n11_boundary.py` → `runs/R2/r2d_l3_n11_slab_results.txt`)**: the prescribed-stress
  injection is validated at machine precision (1.1e-16 against the frozen homogeneous implementation), but the
  PRESCRIBED-STRESS APPROACH IS FALSIFIED there (three registered failure modes: in-plane tension gives exactly zero
  in-plane Einstein response while destroying the D2 window; decelerating sectors drive the zstatic ansatz into its
  degenerate configuration H_B+H_C→0; constraint drift up to 18x). OPEN: dynamical apparatus model + G0↔P2 unit bridge;
- R2-C inhomogeneous φ+F stepwise sequence (§8.7) -- **four levels inherited**: fixed background φ (P1a kink) →
  fixed background φ+F (P1a magnetic_source diagnostic) → dynamic geometry without flux (P2 1+1 W3 no-flux
  control slab, H_C≡0 causal-closure verification) → dynamic geometry with flux (P2 1+1 W1/W2, D2 achieved + second-order
  self-convergence); the fifth level, "finite-region matching boundary", is assigned to R4 (step ⑤ executed at
  screening level 2026-11-21, see runs/R4).
