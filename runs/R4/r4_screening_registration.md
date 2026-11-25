# R4 finite-region geometry and interface matching — screening-level registration (v1.4 §8.12)

**Date**: 2026-11-21
**Evidence level**: MODEL RESULT (inherited portion); OPEN (uninherited portion)

## §8.12 six-step execution status

| Step | Content | Status | Inherited asset |
|---|---|---|---|
| ① | 1+1 reduced-model finite-width front | **Inherited** | `DCC_P2_wall_1p1.py`: kink wall (finite thickness δ~4.17) + inhomogeneous φ(x) + E field + periodic-domain Z2 double-wall slab; second-order self-convergence (lnC 2.01) |
| ② | Interior/exterior region lapse/shift/metric/extrinsic curvature | **Inherited (1+1 level)** | Same as above: synchronous gauge N=1 solved over the whole domain, finite-thickness wall does not rely on junction conditions |
| ③ | Matching conditions and constraints | **Inherited (1+1 level)** | Dual-constraint projection (Ham+Mom) + Σw=0 pin; zstatic initial data at machine precision (~1e-16) |
| ④ | Thin-wall junction / direct finite-thickness solve | **Inherited** | §8.12 explicitly states the "direct finite-thickness solve of the field equations" path -- P2 1+1 is that path |
| ⑤ | Upgrade to axisymmetry/spherical symmetry | **EXECUTED at screening level (2026-11-21)**; **production attempt 2026-11-22 → NO-GO (see §7 below and `docs/decisions/r4_finite_region_geometry_v1.md`)** | `src/r4_frontier/york_initial_data.py` → `runs/R4/r4_york_initial_data_results.txt`: York conformally flat TIME-SYMMETRIC slice (K_ij=0, spherical subclass), 5/5 PASS (vacuum exact 3e-13; Brill–Lindquist anchor order 2.01; kink-shell solve order 2.3, residual ≤2e-10; momentum constraint trivial). **Registered finding: the York existence threshold sits in (0.05, 0.07) × P1a wall density — the full-strength wall shell admits NO time-symmetric conformally flat slice** (residual floor = source scale under two independent solvers; run-1 Picard divergence documented in the module header, and **its stdout was overwritten before archiving — no raw log exists** (registered §9.1 process slip, see D5 §6 and roadmap F.6.1; an earlier revision of this line wrongly cited an archived `r4_york_initial_data_run1_FAIL.txt` — **that file was never created**, corrected 2026-11-22)). OPEN within ⑤: the time-dependent 2+1 axisymmetric evolution (P2-C2 production) and the Maxwell flux sector on the slice |
| ⑥ | Restore the specified background in the asymptotic region outside the boundary | **OPEN — blocked behind ⑤** | P2 1+1 uses a periodic domain (no exterior asymptotic condition); an attempt was made 2026-11-22 (test B6) but is **not a valid test at threshold** because the free evolution is unstable |

## Inherited prohibitions

- **A local planar wall solution must not be extrapolated directly into a spherical front enveloping the Earth** (mandatory per §8.12) -- the ⑤ screening module computes a code-unit shell (R0=10 in κ=1 code units) and delivers no statement about any physical-scale front; all statements about a "whole macroscopic object front" remain prohibited until the production chain exists.
- The acceptance item "the boundary produces no spurious signal": under the periodic-domain + Z2 double-wall scheme, the large-scale drift of Mom is known
  (P2-C4, ill-conditioned projection operator) and is registered as a known limitation.

## Decision

R4 remains OPEN as a whole, but its critical initial-data gap (⑤) is closed at the screening level: the same elliptic
solver that serves P2-C2 has been delivered, and the **existence-threshold finding** (no time-symmetric slice for
wall energy above ~(0.05–0.07) × the registered P1a wall density) is registered as a G3′/D3-relevant constraint on
any strong-wall configuration. Advancement now requires the time-dependent 2+1 axisymmetric evolution (P2-C2
production) and the G3′ completion status of R2-C.

---

## 7. Production attempt (2026-11-22) — ⑤ NO-GO, ⑥ NO-GO

> Decision record: `docs/decisions/r4_finite_region_geometry_v1.md`.
> Registration + full post-hoc addendum: `runs/R4/r4_p2c2_production_registration.md`.
> Products: `runs/R4/r4_cmc_initial_data_results.txt`, `runs/R4/r4_axisym_2p1_results.txt`.

The advancement this section required was executed and **refused by the physics**, in two distinct ways. Neither
refusal is a tuning failure.

| Test | Result | Reading |
|---|---|---|
| Module A, A2/A3 (machinery) | **PASS** — MMS order, nonlinear 3-grid order 2.314, residual ≤1e-12 | the CMC solver is correct |
| Module A, A5 | **PASS but withdrawn** — the constraint *is* solvable at high \|K\| (scale_crit 0.05–0.07 → 0.9394 at K=0.5 → 2.2202 at K=1.0) | solvability alone is misleading |
| Module A, **A6** (negative control) | **FAIL — decisive** — with the wall switched off (scale→0) bg_dev = 0.6871/0.7244/0.7987 and M(R) ≈ −64.7/−69.2/−78.8 at \|K\| = 0.75/1.0/2.0 | the high-\|K\| branch is **K²-dominated, negative-mass, not asymptotically flat**: it does not represent the wall |
| Module B, **B2** (independent-geometry cross-check) | **PASS** — max\|Ham\| 4.316e-4 / 1.068e-4 / 2.266e-5, pairwise orders 2.10/2.44, 3-grid Richardson **2.01** | the 3+1 geometry operator is correct |
| Module B, B1/B3/B4/B6 | **FAIL** | free evolution is **grid-scale unstable** (`rate × h` ≈ const; growth worsens under refinement); KO dissipation (ε ≤ 0.4) and Dirichlet outer BC both fail |
| Module B, B5 | **no valid data** — `RuntimeError` at scale=1.0 | the strong wall is blocked at the initial-data layer, now with the geometric reason from A6 |
| Module B, B7 | **FALSIFIED AS PREDICTED** — flat-space Ricci artefact O(h⁻²), ×4.00 per halving | the axis is not representable by this discretisation; the chart is an annulus ρ ≥ 4 by necessity, not by choice |

**Narrowed statement of the 2026-11-21 finding:** the K=0 obstruction is **geometric, not a slicing artefact**.
The strong wall has **no wall-dominated conformally flat constraint solution on any constant-K CMC slice**. The only
source term with the sign needed to cancel the matter term is the mean-curvature term — which is exactly why it can
restore solvability while destroying the interpretation.

**Revised advancement requirement.** A single scalar CMC solve is exhausted. The remaining route is a
**localized mean curvature K(ρ,z)** (the sweeping front itself), which breaks the `K = const` identity that makes the
momentum constraint trivially satisfied, and therefore forces **Hamilton and momentum to be solved jointly** for
(ψ, β). That work additionally requires a **strongly hyperbolic evolution formulation (BSSN/Z4c + Gamma-driver)**,
because an initial-data slice that cannot be evolved is not a finite-region geometry result. R4 ⑥ stays blocked behind
⑤ for the same reason: its 10.55% spurious-signal number is dominated by the unstable mode and is an **upper bound**,
not a boundary-reflectivity measurement.

### 7.1 Follow-up the same day — the instability is BULK (boundary exonerated)

The production registration left one route untested: the inner cut radius was never varied, and no eigen-analysis was
run. A registered discrimination round (`r4_instability_localization_registration.md`, results in
`r4_instability_localization_results.txt` and `r4_instability_localization_stage2_results.txt`) closed it:

- **Seeded amplification is invariant to both boundaries at 0.1%** — A(t=2) = 7.886 / 7.878 / 7.886 for
  (ρ_in=4, R=24), (ρ_in=8, R=24), (ρ_in=4, R=36). The `RHO_IN` excise surface is **not** the cause.
- The leading mode is `gpp`-dominated, constraint-**carrying** (`‖Ham[v]‖/‖v‖` = 6.2e-2 … 1.3e-1) and scales as
  `Re λ ∝ h^(−0.97)`.
- A stage-1 `INNER-EDGE` verdict was produced and then **retracted** as an artefact of a confounded ratio (the
  denominator `Ham(0)` depended on the geometry). Both metric defects are disclosed in the registration addendum.

**Consequence for this section: the statement above that a strongly hyperbolic formulation is the remaining route
stands, and is now backed by a falsification of the cheapest alternative rather than by assertion.**
