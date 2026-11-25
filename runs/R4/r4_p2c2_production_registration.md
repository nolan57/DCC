# R4 ⑤ production / P2-C2 — registration (v1.4 §8.12 ⑤⑥, §12.6)

**Date**: 2026-11-22
**Executor**: AI (WorkBuddy session), registered discipline of §9.1/§9.3: zero file I/O in solvers,
thresholds registered before the run, unit tests + analytic anchors, stdout redirected into `runs/R4/`.
**Dependency versions**: python 3.13.12, numpy 2.4.6, scipy 1.18.0, sympy 1.14.0 (`requirements.txt`).
**Git**: repository not initialised in this workspace (registered as a known §9.1 gap, unchanged from
previous rounds).

## Prior state being continued

- `runs/R4/r4_york_initial_data_results.txt` (2026-11-21): time-symmetric (K_ij = 0) conformally flat slice,
  spherical subclass, 5/5 PASS, **registered finding: the York existence threshold is bracketed in
  (0.05, 0.07) × P1a wall density — the full-strength wall has NO time-symmetric conformally flat slice.**
- OPEN then: (a) whether that obstruction is a *slicing artefact* (K=0) or a *physical/geometric* one;
  (b) the time-dependent 2+1 axisymmetric evolution (P2-C2 production); (c) R4 ⑥ exterior asymptotics.

## This round: two modules

### Module A — `src/r4_frontier/cmc_initial_data.py` → `runs/R4/r4_cmc_initial_data_results.txt`

Question A: is the K=0 obstruction removable by choosing a slice with non-zero mean curvature?

Lichnerowicz–York system, γ_ij = ψ⁴δ_ij, K_ij = (K/3)γ_ij (K = const ⇒ **momentum constraint identically
satisfied**, zero shift), source = registered P1a kink wall:

    ∇²ψ = -(κ/4) ρ ψ⁵ - (Â²/8) ψ^{-7} + (K²/12) ψ⁵ ,   ρ = scale·(½ φ'² ψ^{-4} + V(φ))

Note the three terms have **different conformal weights** (ψ⁵ / ψ^{-7} / ψ⁵): the matter term and the
K² term are both ψ⁵ but with **opposite signs**, so the answer to question A is decided by sign, not by
numerics. The scan converts that sign into a number: K_min(scale).

Registered tests (thresholds fixed before the run):

| ID | Test | Threshold |
|---|---|---|
| A1 | K→0 regression vs the 2026-11-21 York module (same r-grid, same source) | max abs diff < 1e-12 (IDENT, not counted as evidence) |
| A2 | MMS for the discrete Laplacian + Robin row (analytic ψ_M, manufactured source) | observed order ∈ [1.6, 2.4] |
| A3 | 3-grid self-convergence of the nonlinear CMC solve (K≠0, scale=0.3) | observed order ∈ [1.6, 2.4], discrete residual < 1e-8 |
| A4 | Sign/monotonicity: existence threshold vs K | threshold must move **monotonically** in \|K\|; direction reported, not assumed |
| A5 | Existence of the full-strength wall (scale=1.0) at some \|K\| | PASS = a positive regular solution found for scale=1.0, 0.3, 0.1 |

Continuation is used in K (previous solution as the next initial guess) so that branch loss is not
misreported as non-existence. Failure branches are logged, never deleted (§9.1).

### Module B — `src/r4_frontier/axisym_2p1_evolution.py` → `runs/R4/r4_axisym_2p1_results.txt`

Question B: does the configuration actually evolve, and does the finite-region geometry behave?

Formulation (registered, all in code units κ=1, c=1, signature −+++, G=κT):

- 3+1 ADM, **axisymmetry exactly imposed**: coordinates (ρ, φ, z), ∂_φ = 0, metric components
  γ_ρρ, γ_ρz, γ_zz, γ_φφ and K_ρρ, K_ρz, K_zz, K_φφ as functions of (ρ, z, t).
  Odd-under-reflection components (γ_ρφ, γ_φz) are identically zero (no rotation) — this is an
  **ansatz identity**, not an approximation.
- Gauge: **1+log lapse** ∂_tα = −2αK, **zero shift**. Registered limitation: no Gamma-driver, so the
  gauge freezes once |K| accumulates (reported quantitatively as the lapse-collapse time).
- Grid: uniformly staggered in **both** directions (ρ_i = (i+½)h, z_j = (j+½)h) so that ρ = 0 and z = 0
  are never grid points; the axis and the equatorial plane are handled by **parity ghost cells**
  (even: γ_ρρ, γ_zz, γ_φφ, K_ρρ, K_zz, K_φφ, α, φ, Π; odd: γ_ρz, K_ρz). No 1/ρ singularity is ever
  evaluated — the staggered axis removes it by construction. 3 ghost layers, 2nd-order centred FD, RK4.
- Outer boundary: zero-gradient (Neumann) — deliberately the *worst* absorbing choice, so that the
  R4 ⑥ test measures a genuine spurious-signal level instead of hiding it behind a sponge.
- Geometry (Christoffel, Ricci, D_iD_jα, D²φ) is computed **generically from the FD metric** in the
  (ρ, φ, z) coordinate basis — no hand-transcribed component formulas, so no transcription sign risk.

Registered tests (thresholds fixed before the run):

| ID | Test | Threshold |
|---|---|---|
| B1 | Flat-space stationarity (γ=δ, K=0, α=1, φ=±v ⇒ V=0): constraint norms | ≤ 1e-10 relative, drift over t=20 < 10× |
| B2 | **Independent-geometry cross-check**: the code's own R + K² − K_ijK^ij − 2κρ on the 2026-11-21 York slice (produced by a *different* solver) | residual → 0 at observed order ∈ [1.6, 2.4] |
| B3 | Spherical isotropy (spherical data must stay isotropic): defect between the ρ-axis and z-axis profiles at equal areal radius | observed order ∈ [1.6, 2.4] |
| B4 | Constraint propagation: ||Ham||, ||Mom|| bounded over the run (no exponential growth) | growth factor over the run < 10 |
| B5 | Full-strength wall on the Module-A CMC slice: evolution for Δt = 1/\|K_min\| | constraints bounded, no NaN; outcome reported as-is |
| B6 | R4 ⑥ exterior asymptotics: α→1, γ→flat, ψ_eff−1 falloff outside the front; spurious signal = difference against a 1.5× larger domain | spurious signal < 5% of the front amplitude |

Evidence level of the whole round: **MODEL RESULT (screened)**, with the honest boundary that 2nd-order
FD + zero shift + non-absorbing outer boundary is a machinery validation, not a production GR evolution.

## Addendum — everything added AFTER the first run of each module (full disclosure)

§9.1/§9.3 require thresholds to be fixed before the run. The following items were **not** in the
table above when the modules were first executed. Each is listed with what it changed, so that a
reader can discount the round accordingly. **No threshold registered in the tables above was edited,
relaxed or deleted at any point.** All are recorded here rather than being folded silently into v1.

### A. Module A

| Item | When | Why it was added | Effect on verdicts |
|---|---|---|---|
| A3 case amended from (scale=0.30, K=4.0) to (scale=0.03, K=1.0) | **before** the A3 run that is archived | the registered (0.30, 4.0) case has **no solution** (branch does not exist, not a numerical failure); a convergence test on a non-existent branch measures nothing | none — order window [1.6, 2.4] and residual tolerance 1e-8 unchanged |
| `FAIL-AT-FLOOR` tag for A1 | after A1 returned 1.6e-12 vs tol 1e-12 | the K→0 regression sits at the round-off floor of the sparse solve; I refused to edit the threshold | A1 stays **FAIL**, stays labelled IDENT, stays excluded from the evidence count |
| **A6** negative control | after A5 first returned PASS | A5 PASS was suspected bogus; probing showed ψ already 0.31 with the wall switched off (`scale=1e-6`) and `M(R) ≈ −65`. A6 asks the question A5 does not: *does the solution still describe the wall?* Registered criterion (fixed before A6 ran): `bg_dev = max|ψ(scale→0) − 1| < 0.1` **AND** `M(R) > 0` | **decisive**: A6 FAIL **withdraws the A5 headline**. A5's PASS is retained as a statement about solvability only |

Reading rule for Module A: A5 and A6 answer different questions and are **not** in conflict.
A5 = "can Ham be solved with the wall present" (yes at high |K|). A6 = "is the solution still the
wall" (no). The published conclusion uses A6.

### B. Module B

| Item | When | Why it was added | Effect on verdicts |
|---|---|---|---|
| inner excise radius `RHO_IN = 4.0` (chart becomes an annulus) | after flat space gave `Ham = 30.7` instead of 0 | near the staggered axis `Γ^φ_{ρφ} = 1/ρ` cannot be differenced consistently; the artifact grows as 1/h² (7.68 → 30.7 → 122.9). A reference-subtraction fix was tried and **rejected** (floor 6e-2, never converged) | shrinks the domain of validity of *every* B-test to ρ ≥ 4; this is a **retreat**, recorded as B7 rather than hidden |
| matter weight `WEIGHT = 0.05` on ρ, S_ij, j_i | after B2 was O(h⁰) (0.68, order ≈ 0.02) | the York module sources the constraint with `scale = 0.05` × wall density; my evolution was using full strength, so B2 was comparing two different physical configurations. The weight is the **same 0.05** that Module A/B5 hands off | none on the thresholds; this is what makes B2 a legitimate cross-check (order 2.01) |
| **B0** instability diagnosis (3 resolutions, no source) | after B1/B3/B4/B6 all raised `FloatingPointError: non-finite lapse` | needed to distinguish a hyperbolic instability from a coding error before touching anything. Diagnostic block, **no threshold** | explanatory only; it is what converts "it blew up" into "the unstable mode is grid-scale (`rate × h ≈ 0.26–0.39`, constant)" |
| **B7** axis-inclusion falsification | after the RHO_IN decision | a retreat that is not tested is indistinguishable from a bug hidden by a domain cut. Registered criterion (fixed before B7 ran): flat-space artifact must scale as **O(h⁻²)** and the axis-inclusive evolution must fail. Prediction stated in advance: "falsified as predicted" ⇒ the axis must be excised | **confirms** the excise was necessary and not cosmetic; separates "axis not representable by this discretisation" from "this code is broken" |
| closing-summary string in `axisym_2p1_evolution.py` | after the results were read | the block was a **static string written before the run** asserting the scheme was "validated against … exact spherical symmetry (B3)". B3 = **FAIL**, so that sentence was false. Replaced by a block derived from the verdict flags | **documentation only, verified.** Re-run into `r4_axisym_2p1_results_rerun_check.txt`; `diff` against the archive shows **only the closing block differs — all 115 numeric lines are byte-identical**. Archived stdout untouched; no test logic, threshold or numerical path changed. Side benefit: the round is **bit-reproducible** |

### C. What this round must NOT be read as

- Not a stability result: the free evolution is unstable in a grid-scale way that **worsens** under
  refinement. B2 passing does not rescue B1/B3/B4/B6 — a correct *spatial operator* on an unstable
  *evolution system* is exactly what those four tests were designed to separate.
- Not a strong-wall result: B5 has **no valid initial data** at scale 1.0, and Module A explains why
  (A6). The strongest slice evolved is scale 0.05, which is 5% of the P1a wall density.
- Not an R4 ⑥ closure: B6 FAILs at 10.6% spurious signal against a 5% threshold, and the noise floor
  there is inseparable from the instability.

## Prohibitions carried forward

- No physical-scale statement: everything is in κ=1 code units; **a local wall solution may not be
  extrapolated into a front enveloping the Earth** (§8.12 prohibition unchanged).
- No visibility statement (G6 gate unchanged).
