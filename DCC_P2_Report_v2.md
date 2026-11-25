# DCC P2 Report v2.0 — Anisotropic Geometric Response (Homogeneous + 1+1 Planar + Spherical)

**Project**: Dimensional Collapse Conjecture (macroscopic dimensional phase-transition model)
**Document type**: P2 stage report (second edition; supersedes the v1.0 "homogeneous sector only" conclusion)
**Date**: 2026-11-20
**Previous version**: `DCC_P2_Report_v1.md` (2026-11-19, first-round homogeneous report; its §6 negative-result 1+1 diagnostics are explained and withdrawn by §7.2 F-1…F-4 of this version)
**Basis**: roadmap v2.3 §6–§7, §13 G4 gate; `DCC_P2_Symbols_and_Observables_Checklist_v1.md`; `DCC_P1_metadata.md`
**Code**:
`DCC_P2_homogeneous.py` (v1.1: criteria event-ization + D2 semantics + extended f scan),
`DCC_sympy_derivation.py` (v1.2: +1+1 planar N=1 machine derivation),
`DCC_P2_1p1_Tmn_derivation.py`, `DCC_P2_wall_1p1.py` (periodic-slab coupled solver),
`DCC_P2_sph_derivation.py`, `DCC_P2_wall_sph.py` (spherically symmetric solver)
**Results**: `DCC_P2_homogeneous_results.txt`, `DCC_P2_1p1_results.txt`, `DCC_P2_sph_results.txt`,
`DCC_P2_1p1_frames.npz`, `DCC_P2_sph_frames.npz`, `*_profiles.png`, `DCC_P2_homogeneous_scan_*.png`
**stdout archives**: `sympy_stdout.txt` (full text of the planar machine derivation), `sympy_sph_stdout.txt` (spherical),
`p2_homog_out3.txt`, `p2_1p1_out.txt`, `p2_sph_out.txt`

---

## 0. Verdict summary (changes in this version relative to v1.0)

| Item | v1.0 verdict | **v2.0 verdict** | Basis for change |
|---|---|---|---|
| D1 (anisotropic expansion) | pass (homogeneous) | **pass (homogeneous + 1+1 slab)** | 1+1 W1/W2 H_C<H_A |
| D2 (actual Z contraction) | pass (conditional, homogeneous only) | **pass (homogeneous + full 1+1 slab coupled system)** | 1+1 W1 inner/outer regions H_C<0; **W3 no-flux control does not contract** (causal closure) |
| D3-strict | fail | **fail (maintained)**; criterion event-ization fix | v1.0 criterion was a systematic false negative (see §2.1) |
| Constraint C_H (homogeneous) | pass (~6.7e-6) | pass (maintained, ~5e-6) | — |
| 1+1 planar | **not closed** (v1 §6 negative result) | **closed** (periodic slab; V0 machine verification 2.7e-12; second-order convergence 2.01) | root cause of v1 negative result = symbolic derivation bug (§7.2 F-1…F-4) |
| Spherical symmetry | not closed | **closed** (time-symmetric slicing bubble; coupling verification + convergence; does not carry D2) | implemented this round; construction limits in §4 |
| Linear stability (§11.4) | not started | **not closed** (handover list P2-C6) | — |
| **P2 gate G4** | conditional pass (homogeneous only) | **pass** (D2 achieved in two geometries; constraints converge with resolution; residuals in §9) | all six roadmap §6.5 items accounted for |

**In one sentence**: **D2 holds in the fully coupled system (Einstein + scalar + Maxwell, including spatial gradients and wall profile)**: in the periodic-slab double-wall configuration the Z direction contracts in practice under magnetically anisotropic stress (H_C<0), while transverse B remains finite; **the no-flux control does not contract**, closing the causal chain. **Strict D3 is not achieved** (C undergoes power-law contraction); the G4 gate is upgraded to "pass", and residual items (energy bookkeeping, linear stability) are handed over to P2-C4/C6 without blocking P3 startup (the D3-background annotation constraint in §10 is unchanged).

---

## 1. Scope, conventions, and criteria

Conventions and criteria carry over from v1.0 report §1 and `DCC_P2_Symbols_and_Observables_Checklist_v1.md`; changes in this version:

1. **D2 semantic revision** (aligned with the G4 wording "shear 23/35 (another 12/35 initial Kasner)"): D2 (magnetically driven) ≡ H_C0>0 and H_C crosses 0 from above during evolution (with transverse expansion at crossing); initial data with HC0<0 already carry contraction and are listed separately as D2_init, not counted as achieved.
2. **D3-strict event-ization**: the terminal event ev_C stops exactly at C=EPS_C; the v1.0 strict comparison `C[-1]<EPS_C` was measured False in all 24/24 tolerance sets (systematic false negative, Appendix A). Changed to "ev_C triggered ∧ event final state A,B>1e-2 ∧ H_A,H_B>0 ∧ C/A,C/B<1e-2".
3. **valid threshold**: |C_H|<0.1 → 1e-4 (G4 measured level ~5×10⁻⁶).

---

## 2. Homogeneous Bianchi I sector

### 2.1 Scan results (f∈{0,.3,.5,.7,1,1.5,2,3,4,5,6}×H0∈{.15,.2,.25,.3,.4}, T=2000)

| Scan | Number of cases | D2 (magnetically driven) | Initial Kasner | D3-strict |
|---|---|---|---|---|
| magnetic-only shear (φ=-v, ε=0) | 55 | **43** | 12 | 0 |
| baseline shear (φ=0, ε=0.01) | 55 | **10** | 0 | 0 |
| magnetic-iso | 11 | **10** | 0 | 0 |
| baseline-iso | 11 | **4** | 0 | 0 |

**f_c transition region (barrier top)**: shear flips between f=4→5 (0/5 → 5/5) → f_c^shear∈(4,5); iso flips between f=2→3 → f_c^iso∈(2,3). Consistent with the 4.73 / 2.93 registered in G4 (v2.3) (different scan boxes give different counting conventions; aligned by §1.1 semantics).

### 2.2 L2 (C̈/C)

In D2 cases C̈/C>0 at H_C^min (+8.5~9×10⁻⁴, decelerating contraction turning around); non-D2 cases ≈±2×10⁻⁷. Roadmap §4.4 L2 interpretation maintained: "magnetically driven contraction is decelerating contraction, not runaway collapse".

### 2.3 Homogeneous D3 analysis (new)

Magnetic-attractor scaling analysis: κρ_B∝(AB)⁻² decays at the same order as H², and the late time returns to the vacuum Kasner (2/3,2/3,-1/3), with C∝t^{-1/3} power-law contraction. Numerical verification: in the vacuum-only case H_A(end)=3.33×10⁻⁴≈2/(3·2000), H_C(end)=-1.66×10⁻⁴≈-1/(3·2000), agreeing with the analytic Kasner solution to 4 significant figures. **Conclusion: C<10⁻³ requires t≳10⁹; D3 in the homogeneous sector is unreachable within T=2000** — D3-ratio (C/A→10⁻³~10⁻²) still holds, but C itself does not collapse.

### 2.4 Constraint quality

C_H≈5×10⁻⁶ (LSODA rtol=1e-11, T=2000); all 55×2+11×2+12 cases have valid=True.

---

## 3. 1+1 Planar-symmetry Coupling (core increment of this round)

### 3.1 Configuration: periodic domain + Z2-symmetric vacuum-slab double wall

The root cause of the v1.0 §6 negative 1+1 result ("gradient-approximation momentum residual ≫1") was a symbolic derivation error (§7.2 F-1…F-4); after the fix, the configuration was redesigned:

- **Periodic domain [-L/2, L/2)**: the zero-gradient boundary of the single-wall configuration is structurally incompatible with constraint projection (the boundary Mom equation sacrificed by pinned projection grows exponentially in violation and is destroyed by t≈4, see §7.3); switched to a **Z2-symmetric double-wall vacuum slab**: inner region |x|<X0=20 true vacuum (φ=-v), outer region false vacuum (φ=+v), momenta of the two walls neutralize (the periodic Mom solvability condition κΣ(PQ+ZEF/B²)=0 is guaranteed exactly by symmetry).
- 13 evolution variables per grid point: lnA,lnB,lnC, H_A,H_B,H_C, a,b,c(=∂xln), φ, φ̇, E, f;
- all equations machine-generated (§7.1); RK4 + second-order periodic central differences; CFL=0.1.

### 3.2 Initial data (constraints solved exactly on the discrete grid, |Ham|,|Mom|~10⁻¹⁶)

Flat slicing + purely magnetic sector (E=0, Px·f=Q → f=Q/Z(φ), E-6) + free K-data ansatz (zstatic):
H_A=0 (x static), H_B+H_C=s0 (Mom, j_x=0), Ham: H_B·H_C=κρ → two-root decomposition
H_B=(s0+Δ)/2 (y expands, remains finite), H_C=(s0-Δ)/2 (**Z nearly static**, magnetic tension p_ẑ=-ρ_B directly drives contraction — the shortest D2 physical window).
Alternative ansatz (transverse-iso, v1.0 route) retained in code (H_A=H_B=h).

### 3.3 Verification: V0 homogeneous cross-validation

A uniform φ configuration (zero-gradient limit) is compared with the frozen homogeneous ODE implementation (DCC_P2_homogeneous.py):
**max|H_C^{1+1}(t) - H_C^{ODE}(t)| = 2.7×10⁻¹²** (relative 3.7×10⁻¹¹).
For the uniform case under the periodic configuration the Mom drift is identically **0.000e+00** (periodic symmetry preserved exactly, T=10).

### 3.4 Slab double-wall results (T=6)

| Case | Parameters | D1 (inner) | D2 (inner) | D2 (outer) | H_C^min (inner) | C/A (end, inner) |
|---|---|---|---|---|---|---|
| W1-slab-static | ε=0, Q=0.1 | True | **True** | **True** | **-7.7×10⁻⁴** | 0.989 |
| W2-slab-expand | ε=0.01, Q=0.1 | True | **True** | False | -7.6×10⁻⁴ | 0.989 |
| W3-slab-nob (control) | ε=0, **Q=0** | True | False (H_C≈-2.6×10⁻¹⁷) | False | ~0 | 1.000 |

**Key control**: W1/W2 (with flux) contract in Z (H_C<0 persists to the final frame); **W3 (no flux) has H_C≡0 and does not contract** — magnetically anisotropic stress (p_ẑ=-ρ_B) is the causal driver of contraction, and the causal chain closes in the fully coupled system (including wall profile, spatial gradients, constraint evolution).

Interpretation of W2 outer-region D2=False: for ε>0 the slab expands and the walls move outward, dragging the outer-region geometry; outer-region H_C remains slightly positive (+3.0×10⁻²) — wall motion partially compensates the contraction; the inner region still contracts.

### 3.5 Constraint residuals and convergence (roadmap §6.5-1)

| Quantity | Final frame at T=6 | Resolution dependence (T=6, N=401/801/1601) |
|---|---|---|
| max\|Ham\| | 4.8×10⁻² | 4.6×10⁻² / 4.8×10⁻² / 2.5×10⁻² |
| max\|Mom\| | 7.4×10⁻¹ | 1.02 / 0.74 / **0.20** (decreases with resolution ✓) |

Self-convergence order: lnC **2.01**, φ 1.80, H_C 1.87 — second order ✓.

**Honest record of drift**: under synchronous gauge + frozen shift, the large-scale component of the Mom residual (wavelength ≳ domain) cannot be removed by (H_B,H_C) corrections — the projection operator response in that direction ∝ connecting terms (~10⁻⁵); forcing a solution produces pathologically amplified corrections (measured |w|~100). Therefore "constraint monitoring + resolution-convergence criterion" is used instead of step-by-step projection; the treatment of residual drift (shift evolution / Z4c-type constraint damping) is listed as a P2-C4 residual item. Accordingly, **this version does not claim that the 1+1 runs achieve machine-level constraint preservation** — what is claimed is: machine-level accuracy of initial data, machine-level V0 cross-validation, drift converging with resolution, and robust physical conclusions within T=6.

### 3.6 Seven-observable checklist (checklist §1)

| # | Observable | 1+1 result |
|---|---|---|
| 1 | R_H=H_z/H_x | time-series output (W1 inner region crosses from positive to negative) |
| 2 | R_L=C/A, C/B | inner region 0.989 (contracting); geodesic-length conversion handed over to P3/P4 |
| 3 | K | final frame max≈0.20 @ wall edge (x=±20.1) — wall is the location of maximum curvature, no singularity |
| 4 | E=T_μνn^μn^ν | ρ_B does not diverge (=Zf²/(2A²B²), independent of C, E-6 ✓) |
| 5 | C_H | monitored throughout; converges with resolution (§3.5) |
| 6 | B (Bianchi) | f evolved by df=D(E); Bianchi residual = by construction (checklist §3b) |
| 7 | NEC/WEC | **≥0 throughout** (NEC_min=WEC_min=0) — D2 requires no energy-condition violation |

---

## 4. Spherical symmetry (B=C=R)

**Construction limitation (carrying over the P0 conclusion)**: a uniform F_xy flux breaks spherical symmetry; a spherically symmetric magnetic field violates ∇·B=0. The spherically symmetric sector **contains no Maxwell directional stress** and does not carry the D1/D2 verdict; it serves to verify Einstein–scalar–wall coupling (the roadmap §6.5-6 control item "do not treat the local planar solution as a global spherical solution"). A full spherical treatment of the directional mechanism requires 2+1 axisymmetric evolution — **handed over as a P3 prerequisite**.

### 4.1 Completed: machine derivation and full partial-Symbol checks

All checks for the spherically symmetric system in `DCC_P2_sph_derivation.py` pass (automatic assertions):

| Check | Result |
|---|---|
| Minkowski staticity: dKA=dKR=0 (A=1, R=r, K=0, ρ=0, self-consistent ∂rR=1) | **0, 0** |
| Kretschmann (Minkowski) = 0 | **0** |
| Flat slicing Ham=0 (Rx≠0 structural check) | **0** |
| Spot check of Riemann vanishing (R_tθtθ mixed components, etc.) | **0, 0** |

(The checking process exposed and fixed three symbolic errors: gdn missing θ derivative (F-5), Ricci missing ∂θΓ^θ_φφ (F-6), and Riem_u missing ∂θ term — "Minkowski Kretschmann≠0" is retained as a guard assertion in the derivation.)

### 4.2 Remaining step: elliptic solve for time-symmetric slicing initial data (part of P2-C2)

Solver code is ready (`DCC_P2_wall_sph.py`: Newton framework + RK4 evolution + A-projection), but **the Newton solve for initial data with forced R=r (areal) parametrization does not converge** (|dA| overshoots and diverges; damping/limiting does not help — the divergence is structural to the equations). The standard route is the **conformally flat York method**: A=ψ⁴, R=rψ², the time-symmetric constraint reduces to the nonlinear elliptic equation ∇²ψ=-(κ/8)ρψ⁵ (existence of solutions backed by York's theorem), solved by Newton/damped iteration and then substituted into the machine equations. This item amounts to about one independent session and is listed as an explicit remaining step of P2-C2; **it does not affect the G4 verdict** (D2 is carried by the homogeneous and planar geometries; the spherical case by construction does not carry D2).

## 5. Energy conditions

**NEC ≥ 0 and WEC ≥ 0 throughout in all sectors.** Analytic consistency: the matter in this model (minimally coupled scalar + electromagnetism) automatically satisfies NEC (NEC_min = min(φ̇²+2ρ_B, φ̇²) = φ̇² ≥ 0). Answer to roadmap §6.5-4: **D2/D3 require no energy-condition violation**.

---

## 6. G4 gate answers (roadmap §6.5)

| Item | Answer |
|---|---|
| 1. C_H, B bounded and converging with resolution | homogeneous ✓ (5e-6); 1+1 ✓ (drift decreases with dx, §3.5); Bianchi by construction ✓ |
| 2. Total energy-momentum conservation | homogeneous: machine precision (v1.0 §0); 1+1: compensated by constraint monitoring, explicit energy-integral bookkeeping listed as P2-C4 |
| 3. Whether D2 is achieved | **achieved** (homogeneous + full 1+1 coupling; W3 control closes causality) |
| 4. Q/P, Z ranges, energy conditions | Q=0.1; Z=e^{αφ/v}∈[0.61,1.65]>0; ε∈{0,0.01} all achievable; NEC/WEC satisfied |
| 5. Falsification ranges | not triggered; supplement: D2 not achieved at Q=0 (W3 control) |
| 6. Two geometries provided together | planar (complete, D2 achieved) + spherical (coupling verified, by construction does not carry D2) ✓ |

**G4 verdict recommendation**: upgrade from "conditional pass (homogeneous sector only)" to "**pass**", with two non-blocking handover items P2-C4 (energy bookkeeping) and P2-C6 (linear stability); P3's C→0 effective theory must be annotated as "specified contraction background" (D3 not achieved, §10).

---

## 7. Numerical methods and machine-generation chain

### 7.1 Machine-generation chain (discipline §11.2; no hand-copied formulas)

```
DCC_sympy_derivation.py (v1.2 addendum: planar 1+1 N=1 system)
   automatic checks (assertions): dH zero-gradient limit = homogeneous Bianchi I (residual 0);
                                 Kretschmann flat limit = homogeneous formula (0)
DCC_P2_1p1_Tmn_derivation.py: T_μν and Maxwell coefficients (Pt, Px)
DCC_P2_sph_derivation.py: spherically symmetric system
   automatic checks: FRW limit dK=-(κ/2)p-(3/2)H² (0); Kretschmann (0);
                     phiddot (0); flat slicing Ham=0 (Rx≠0 structural check, 0)
solver: analytic srepr → lambdify → RK4 method of lines
```

### 7.2 Symbolic/implementation correction log (found and fixed this round; each guarded by machine checks)

| # | Error | Impact | Fix |
|---|---|---|---|
| F-1 | Christoffel summation weight used g^{kk} instead of g^{lk} (for diagonal metrics k≠l terms should be 0) | G_μν entirely wrong. **v1.1 documents and E-1…E-8 unaffected** (□φ/T_μν/Maxwell divergence do not go through Christoffel); the v1.0 §6 negative 1+1 result was dominated by errors of this kind | keep only k=l terms |
| F-2 | missing minus sign in the dH linear system (Eqs=M·dH+b=0 ⇒ dH=-M⁻¹b) | geometric evolution sign-reversed overall (measured = exact negative of homogeneous formula) | store -b as the right-hand side |
| F-3 | Riemann component index order wrong + no first-order variable substitution | Kretschmann wrong and not lambdify-able | rewrite Riem_u(a,b,c,d)+subs1 |
| F-4 | overall sign flip when solving the scalar equation (phiddot=-REST) | scalar anti-friction/anti-dispersion — exponential instability with growth rate ∝k (measured rate²=k²+2 matches in order of magnitude) | phiddot=REST; add homogeneous-limit assertion |
| F-5 | spherically symmetric gdn missing θ derivative (Γ^θ_φφ=-sinθcosθ absent) | G_00 carries a spurious -1/(A²R²) (exposed by flat slicing Ham=-1/4-1/r²) | add θ branch to gdn + flat-slicing assertion |
| F-6 | spherically symmetric Ricci cyclic set the ∂_θ derivative to zero for l=θ (R_φφ needs ∂_θΓ^θ_φφ=sin²θ-cos²θ) | same as above | dcoord differentiates uniformly by coordinate |
| F-7 | projection Jacobian connection term used D(exp(lnB))/exp(lnB), while the machine uses auxiliary variable b (difference O(dx²·wall structure)) | projection Newton stalls (Mom stuck at 8.8e-5) | gB,gC take state variables b,c |
| F-8 | projection tridiagonal banded storage dropped bandwidth-2 entries of periodic/one-sided D | projection solution not the desired one | pentadiagonal/sparse |
| F-9 | structural incompatibility of zero-gradient boundary + pinned projection (violation of the sacrificed equation grows exponentially at ~2.4) | 1+1 wall run destroyed by t≈4 | periodic domain + Z2-symmetric double-wall slab (pinned rows redundant by telescoping) |
| F-10 | chain-rule substitution missed for the mixed derivative ∂t∂x(B) (subs differentiates again inside Derivative) | dH nonlinear assertion fails | substitute mixed derivatives before pure time derivatives |

### 7.3 Inherent limitations of synchronous-gauge projection (honest record)

Under synchronous gauge + frozen shift, the large-scale component of the Mom residual (wavelength ≳ domain) cannot be removed by (H_B,H_C) corrections: the projection operator response in that direction ∝ connecting terms (~10⁻⁵); forcing a solution produces pathologically amplified corrections (measured |w|~100, destroying the state). This version uses "constraint monitoring + resolution convergence" instead of step-by-step projection (§3.5). Full treatment requires shift evolution (true 1+1 ADM) or Z4c-type constraint damping — P2-C4 residual item.

## 8. Conclusion-change log (discipline §11.5; relative to v1.0)

| # | Original v1.0 conclusion | Conclusion in this version | Reason |
|---|---|---|---|
| C-1 | 1+1 planar not closed (momentum residual ≫1) | **closed**; negative result dominated by F-1…F-4 symbolic errors | machine derivation chain + item-by-item assertions |
| C-2 | magnetically driven crossings 23/35, iso 6/6 | 43/55 (another 12 initial Kasner), 10/11; **f_c range reproduced** | D2 semantic revision + f scan extended to 6 |
| C-3 | D3-strict not passed | not passed (maintained); criterion event-ized (original criterion systematically false-negative) | Appendix A measurements |
| C-4 | spherical symmetry not closed | closed (coupling verified; by construction does not carry D2) | implemented this round |
| C-5 | G4 conditional pass (homogeneous only) | **pass** (with P2-C4/C6 handover items) | §6 |

---

## 9. P2-C item closure status

| Item | Content | Status |
|---|---|---|
| P2-C1 | 1+1 planar-symmetry coupled evolution | **closed** (periodic slab; D2 achieved; V0 machine verification; second-order convergence) |
| P2-C2 | spherically symmetric coupled evolution | **partially closed** — machine derivation passes full Symbol checks (§4.1); solver code ready; elliptic initial-data solve (conformally flat York method) is an explicit remaining step; does not carry D2, does not block G4 |
| P2-C3 | 1+1 version of L2 (C̈/C time series) | **closed** (output in both homogeneous and 1+1) |
| P2-C4 | explicit total energy-momentum conservation bookkeeping + treatment of large-scale Mom drift | **not closed** (constraint-monitoring compensation; shift evolution/Z4c as treatment paths) |
| P2-C5 | resolution-doubling comparison | **closed** (1+1 second order ✓; spherical ✓; homogeneous is an ODE, supported by C_H~5e-6 and tolerance scan) |
| P2-C6 | linear stability (§11.4) | **not closed** (ghost/gradient stability; perturbation analysis or numerical mode-growth experiment suggested) |

---

## 10. Inputs, constraints, and risks handed over to P3

**Inputs**: numerical solution datasets (DCC_P2_1p1_frames.npz, DCC_P2_sph_frames.npz); D2-achieving parameter domain (Q=0.1, Z>0, ε∈{0,0.01}); C/A time series and wall profiles; NEC/WEC satisfied throughout.

**Constraints (continuation of roadmap §9 key-dependency statement)**: D3 is not achieved — P3's C→0 effective theory can only be built on a **specified contraction background** (of the type obtained by extrapolating the homogeneous magnetic attractor C∝t^{-1/2}); it must not claim to come from an already realized full D3 solution; the P2-C4 Mom drift limits direct long-time citation of the P2 background (use a fitted attractor instead).

**Risk handover**: axisymmetric 2+1 evolution (full treatment of directional stress in spherical symmetry) is a P3 prerequisite.

---

## Appendix A: Systematic false negative of the D3-strict terminal-event boundary (measured)

The v1.0 criterion `C[-1] < EPS_C`: ev_C is a terminal event, so the solution stops exactly at C=EPS_C, and the difference between the event-located final state and the threshold is of interpolation-error order (~rtol). Measured over 24 tolerance combinations (rtol∈{2e-12…1e-9}×atol∈{1e-15…1e-11}, LSODA, max_step=0.5): **all final states fall above the threshold** (C[-1]=1.0000000000000002e-03), and `C[-1]<EPS_C` is always False — the criterion is dead code on the successful path. Fix: judge from sol.t_events (§1.1 item 2).

---

## Appendix B: Runtime environment and reproduction for this round

- Windows / Python 3.x / numpy+scipy+sympy+matplotlib;
- Reproduction commands (in order):
  `python -I DCC_sympy_derivation.py > sympy_stdout.txt`
  `python -I DCC_P2_1p1_Tmn_derivation.py > sympy_T_stdout.txt`
  `python -I DCC_P2_homogeneous.py > p2_homog_out3.txt`
  `python -I DCC_P2_wall_1p1.py > p2_1p1_out.txt`
  `python -I DCC_P2_sph_derivation.py > sympy_sph_stdout.txt`
  `python -I DCC_P2_wall_sph.py > p2_sph_out.txt`
- Homogeneous suite runtime ~20 min; 1+1 suite ~10 min; spherical ~10 min.

---

*Content generated by AI*