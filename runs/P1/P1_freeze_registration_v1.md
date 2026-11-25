# P1 Solver Version Freeze and P1b Revision Registration (v1.4 §12.2 Sprint 0′ items 8-10)

**Date**: 2026-11-21
**Basis**: `Macro3D_to_2D_Smooth_Reduction_Roadmap_v1.4.md` §7.2, §7.3, §12.2
**Evidence level**: MODEL RESULT (P1a) / ESTABLISHED numerical consistency (P1b third review)

## 1. P1a static bubble wall: version freeze

- **Frozen version**: `DCC_P1_bubble_wall.py` (2026-11-19, leapfrog + Sommerfeld absorbing boundary,
  with `DCC_P1_metadata.md` as the single source of truth for parameters).
- **G1-A third-grid convergence** (added this round, `src/p1_wall/g1_closeout.py` →
  `runs/P1/g1_closeout_results.txt`):
  - Three resolutions N=401/801/1601 (same physical domain [−12,12], same BC);
  - Observed order of the field profile **p = 2.000** (v1.4 registered formula, consistent with second-order scheme expectation);
  - Wall thickness δ₀.₉ fine-grid relerr 6.7×10⁻⁶ (analytic 4.164066); tension p_obs = 2.000;
  - **G1-B σ_w analytic cross-check**: numerical integration vs analytic 2√2·λ^{1/2}v³/3 = 0.9428090416,
    fine-grid relerr 1.5×10⁻⁵, **Richardson extrapolation 1.0×10⁻¹⁰**;
  - Verdict: **G1-A/G1-B PASS** → the reservation "preliminary pass of the static baseline, convergence order unproven" is **lifted**.
- **New finding F-G1-3 (registered)**: the kink BVP contains a translational zero mode (modulus fixing); the truncation error along
  the zero mode is exponentially amplified, causing a wall-center drift of ~0.01 (does not converge with grid refinement). Fix: project the Newton correction
  orthogonally to φ′. This phenomenon applies to all kink-type static solvers (including future reuse of the P1a frozen version).

## 2. P1b collective-coordinate friction: revision registration (passed third review)

- **Correction**: ~~"η≈1.0 corresponds to 42.47 km/s"~~ → **"under the current nondimensionalization and scan table, η_eff ≈ 74.8"**
  (β_target = 42.47/299792.458 = 1.4166×10⁻⁴; η_target = 0.0106/1.4166×10⁻⁴ = 74.8).
- **Units and premises**: the units of F_drive, σ_w=0.9428 (G1-B extrapolated value), velocity and friction parameter follow
  `DCC_P1_metadata.md` §P1b; 42.47 km/s is archived as a **low-speed phenomenological assumption**, not a theoretical prediction.
- **Prohibition**: this formula is not full relativistic bubble-wall dynamics; **the true relativistic limit must not be extrapolated from the numerical upper bound at η=0**;
  a relativistic-velocity group must establish its own wall momentum equation and friction four-force definition (mandatory per v1.4 §7.3).

## 3. P1 stage-gate status

| Item | v1.4 requirement | Status |
|---|---|---|
| G1-A third-grid convergence order | Completed | **PASS** (p=2.000, field-profile criterion) |
| G1-B σ_w analytic cross-check | Completed | **PASS** (extrapolation 1e-10) |
| P1b η_eff revision | Third review completed | **Registered (74.8)** |
| P1 solver version freeze | Frozen | **Frozen** (this file) |
| Magnetic-source driven PDE | Handed off to R2 | Not started (not a mandatory G1 closure item per §7.3) |

**G1 closure conditions satisfied** (v1.4 §7.3: G1-A + G1-B completed + P1b parameter revision completed).
