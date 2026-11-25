# DCC P4 Report v1.0 — Observer and Scientific Rendering Pipeline (First 1+1 Slab Round)

**Project**: Dimensional Collapse Conjecture
**Document Type**: P4 first-round report (M6 pipeline part; 2+1 axisymmetric rendering pending completion of P2-C2)
**Date**: 2026-11-20
**Prerequisites**: P2 slab solution (`DCC_P2_1p1_frames.npz`, W1-slab-static);
P3 transmission coefficients (`DCC_P3_Effective_Theory_v1.md` §4, Fresnel normal incidence)
**Code/Results**: `DCC_P4_pipeline.py`, `DCC_P4_pipeline_results.txt`, `DCC_P4_observation.png`

---

## 0. Verdict Summary

| Item | Result |
|---|---|
| Acceptance criterion 1 (no hand-inserted Doppler/beaming factors) | **Passed**—all frequency shifts are given by two-ray shooting (geodesic arrival-time differences); intensity given by the P3 Fresnel coefficient T=0.940015 |
| Acceptance criterion 2 (frame-validity labels) | **Passed**—the results file labels each entry "T≤6 valid region / after that = assumption layer"; blocks with t_emit<0 are separately labeled as assumption layer |
| Acceptance criterion 3 (two wall-velocity groups listed separately) | **Passed**—Group A (relativistic β_w=0.5): ν_obs/ν_src=0.560 (labeled assumption layer for t_emit<0); Group B (phenomenological β_w=1.42e-4): 0.636; frequency-shift time-series scan (valid region): 0.859→0.865 |
| Rendering deliverables | **1+1 slab: pipeline + spectrum/light-curve plots completed**; 2-D images and video require a 2+1 axisymmetric background (after P2-C2 is completed)—**handover item** |

**Key numbers (within the valid region; geometric frequency shift = ratio of geodesic arrival-time differences)**:
- Frequency-shift time series: t_emit=1→5, ν_obs/ν_src decreases monotonically from 0.859324 to 0.865318
  (geometric expansion increases A → the received frequency is more redshifted; the rate of change matches the logarithmic growth rate of A);
- Single-wall transmission T=0.940015 (Fresnel normal incidence for the Z ratio 1/1.6487)—
  i.e., the interface is "nearly transparent" to electromagnetic waves (mild Z contrast), with no total reflection;
- Intensity ratio = T·(ν_obs/ν_src)³ (invariant I_ν/ν³ transport).

---

## 1. Pipeline Structure (Traceable Origin of Each Visual Parameter)

| Pipeline Stage | Implementation | Upstream Source |
|---|---|---|
| Background geometry | Bilinear interpolation of A(t,x), φ(t,x) from frames | P2 W1-slab-static (`DCC_P2_1p1_frames.npz`) |
| Null geodesic | dx/dt=1/A(t,x), RK45 (event-located arrival) | Roadmap §8-1 (N=1 synchronization gauge) |
| Frequency shift | Two-ray shooting: ν_obs/ν_src=Δτ_src/Δτ_obs | §8-1/§8-2 (dτ=√(1-A²v_c²)dt, v_c=β_w/A) |
| Transmission | Wall-crossing count × Fresnel T | P3 §4 (n=√(Z_out/Z)) |
| Intensity | I_obs/I_src = T·(ν_obs/ν_src)³ | Invariant I_ν/ν³ (§8-1, no hand-inserted factors) |
| Source motion | Group A β_w=0.5 (relativistic group); Group B β_w=1.42e-4 (42.47 km/s **phenomenological-assumption group**, not a theoretical prediction) | Following the P1b decision, archived separately |

## 2. Assumption-Layer Declarations (Item-by-Item Labeling for Acceptance Criterion 2)

1. Background geometry for t>6 (after the last frame): A(t,x) is frozen at its last-frame value—the geodesic propagation time is ~73,
   far exceeding the frame window, so **all arrival times t_arr≈58-80 lie in the assumption layer**;
   the **emission-time scan [1,5]** of the frequency-shift time series lies in the valid region, and its arrival-time-difference ratio depends only on
   the scale of geometric evolution along the path, so it is reported as a first-level result;
2. The single-point blocks of Groups A/B (t_emit≈-14) are in the assumption layer—labeled item by item;
3. 2-D images/video: require a 2+1 axisymmetric background (P2-C2 completion: York conformally flat initial data
   + axisymmetric evolution)—this round demonstrates the methodology with the 1+1 slab pipeline, with rendering handed over.

## 3. Handover Items

| Item | Content |
|---|---|
| P4-C1 | 2+1 axisymmetric rendering deliverable (prerequisite: P2-C2 York initial data + axisymmetric evolution) |
| P4-C2 | Finite-wall-thickness transfer matrix replacing steep-wall Fresnel (prerequisite: P3-C2) |
| P4-C3 | Full light curves for the relativistic group (family of frequency-shift/light-curve scans over β_w=0.1–0.9) |

---

## 4. Exposure Duration and Surface Brightness (Added in v2.6, Review Breakpoint 4)

**Exposure duration vs persistence of vision** (human-eye integration time 0.05-0.1 s):
- Relativistic group: the wall sweeps past the Earth at nearly the speed of light, t ≈ 12742 km/c ≈ 0.0425 s (Roadmap §5.2),
  **shorter than persistence of vision**—the human eye can perceive only a single flash and cannot integrate it into a "scene";
- Low-speed group (42.47 km/s, ≈300 s): the duration is sufficient, but this parameter has been judged FAIL in controllability and
  **permanently archived as a phenomenological assumption** (P1b decision)—neither group constitutes a ready-made verdict of "a scene visible to the human eye".

**Surface brightness**: Interface transmission T=94% / reflection R=6% (P3 §4)—the interface is nearly transparent;
image visibility depends on the contrast between the emission/scattering source term and the background brightness.
**This round does not provide a model for the emission source term**—"being visible" is a premise awaiting testing, not a completed acceptance item.

## 5. Statement Boundaries (Following the Review §3 "Can Say / Cannot Say" Checklist)

**May say** (with qualifiers, all three holding simultaneously):
> Under the specified contraction background (D2 level, not D3) and the infinite planar-front approximation, the apparent image of the phase-transition interface sweeping past the observer
> has been reconstructed from geodesics + radiative transfer; each frame is labeled as belonging either to the classical-geometry valid region or to the assumption layer after the degeneracy surface;
> the low-speed wall-velocity group is a phenomenological assumption, not a theoretical prediction.

**May not say**:
- "The model predicts/reproduces a two-dimensional scene as seen by the human eye"—breakpoint 1 (D3 not achieved) + breakpoint 2
  (optical criterion not closed for macroscopic L0, see P3 §2.1: a 7-order-of-magnitude shortfall at macroscopic scales);
- "The third dimension is compressed to optical invisibility"—breakpoint 2 (reachable only for micrometer-scale initial thickness, not for macroscopic values);
- Any rendering that gives the shape or color of a finite region—breakpoint 3 (1+1 infinite slab, no shape;
  P2-C2 axisymmetric initial data required) + breakpoint 4 (exposure/brightness not accepted).

**Lowest-cost path to "an optically indistinguishable third dimension"** (review suggestion, already executed):
the unit conversion + inequality verdict in P3 §2.1—conclusion: macroscopic L0 falls short by 7 orders of magnitude;
micrometer-scale L0 is reachable (t/t0~4); once D3 is achieved, any L0 is reachable.

---

## Epoch note (2026-11-22) — P2-C2 status changed: this report's stated prerequisite is now blocked

This report was written when P2-C2 (2+1 axisymmetric initial data + evolution) was simply *pending*. It is no
longer pending in that neutral sense. The production attempt of 2026-11-22 returned **NO-GO** on both halves of the
prerequisite:

- **Initial data:** no wall-dominated conformally flat constraint solution exists on **any constant-K CMC slice**
  (the high-|K| branch is K²-dominated, negative-mass; negative control A6 decisive).
- **Evolution:** the 2+1 ADM free evolution with zero shift + 1+log + 2nd-order FD is **grid-scale unstable**; the
  cure is a strongly hyperbolic formulation (BSSN/Z4c + Gamma-driver), not tuning.

**Therefore P4-C1 (2+1 axisymmetric rendering) is blocked further out than this report assumed**, and the
"breakpoint 3" line above ("P2-C2 axisymmetric initial data required") should be read as **"required and currently
unavailable"**. No number, verdict or figure in this report is changed by this note — it corrects only the implied
schedule. See roadmap §8.12 status, §F.7, and `docs/decisions/r4_finite_region_geometry_v1.md`.

---

*Content generated by AI*
