# R4 ⑤⑥ at production level: what the finite-region geometry actually permits (v1)

**Date**: 2026-11-22  **Status**: R4 ⑤ → **NO-GO at production level** (machinery only);
R4 ⑥ → **NO-GO** (blocked behind ⑤, not independently tested to threshold)
**Upstream**: `runs/R4/r4_screening_registration.md` (2026-11-21, ⑤ screening), `F.6` of the roadmap
**Recomputation**:
- `src/r4_frontier/cmc_initial_data.py` → `runs/R4/r4_cmc_initial_data_results.txt`
- `src/r4_frontier/axisym_2p1_evolution.py` → `runs/R4/r4_axisym_2p1_results.txt`
  (+ `r4_axisym_2p1_results_rerun_check.txt`, documentation-fix verification run)
**Registration**: `runs/R4/r4_p2c2_production_registration.md` (thresholds + full post-hoc addendum)

---

## 0. In One Sentence

> Upgrading R4 to axisymmetry produced **one working piece and two refusals**: the 3+1 geometry
> operator is correct (it reproduces an independent elliptic solver's Hamiltonian residual at 3-grid
> order 2.01), but **(a)** the strong wall has **no wall-dominated conformally flat initial-data slice
> at any constant mean curvature**, and **(b)** the 2+1 ADM free evolution is **unstable at the grid
> scale**, so the finite-region geometry problem is **not solvable by tuning this discretisation**.
> R4 ⑤ therefore advances from "obstructed at K=0" to "obstructed on the entire CMC family", and the
> remaining route is a **localized mean curvature K(ρ,z)** — i.e. the sweeping front itself — which
> must be solved as a joint Hamilton+Mom problem.

---

## 1. Finding A — the K=0 obstruction is not a slicing artefact, and no CMC slice rescues it

**Question carried in from 2026-11-21**: the full-strength wall had no time-symmetric conformally
flat slice (existence threshold bracketed in (0.05, 0.07) × P1a density). Was that an artefact of
choosing K = 0?

**Answer: no.** Two results, and the second is the decisive one.

### 1.1 The constraint does become solvable at high |K|

With `K_ij = (K/3)γ_ij` and K = const, the momentum constraint is satisfied **identically**, so only
the Lichnerowicz–York equation survives:

    ∇²ψ = −(κ/4) ρ ψ⁵ − (Â²/8) ψ⁻⁷ + (K²/12) ψ⁵ ,   ρ = scale·(½φ'² ψ⁻⁴ + V(φ))

The three source terms have **three different conformal weights** (ψ⁵ matter, ψ⁻⁷ shear, ψ⁵ mean
curvature) and the matter and K² terms carry **opposite signs**. The answer to "can K=0 be rescued"
is therefore a **sign question**, which the scan converts into numbers:

| K | scale_crit (bisection) | reading |
|---|---|---|
| 0 | 0.05–0.07 (2026-11-21) | wall-dominated branch exists only below ~6% density |
| 0.5 | 0.9394 | threshold moved up by ~15× |
| 1.0 | 2.2202 | threshold moved off the scale (scan ceiling ≥3.0 beyond this) |

So yes — **A5 PASS**: at high enough |K| the strong wall (scale = 1.0, 0.3, 0.1) *is* solvable. Read
alone, this would look like the obstruction was a slicing artefact.

### 1.2 …but that branch is not the wall (the decisive control)

A5 asks a solvability question. It does not ask whether the solution still *describes the wall*. A6
(non-local negative control, criterion fixed before it ran: `bg_dev = max|ψ(scale→0) − 1| < 0.1`
**AND** `M(R) > 0`) answers the second question:

| \|K\| | d_wall | bg_dev | M_bg(R) | M_wall(R) | verdict |
|---|---|---|---|---|---|
| 0.75 | 0.3607 | **0.6871** | **−64.69** | −64.32 | does NOT represent the wall |
| 1.00 | 0.2852 | **0.7244** | **−69.19** | −68.95 | does NOT represent the wall |
| 2.00 | 0.1851 | **0.7987** | **−78.79** | −78.70 | does NOT represent the wall |

With the wall **switched off** (`scale → 0`) the conformal factor is already O(1)-different from 1,
and the boundary mass proxy is large and **negative**. The apparent "existence restoration" is
carried by the K² term alone.

**A6 FAIL, and it withdraws the A5 headline.** The A5/A6 pair is not a contradiction; it is one fact
read at two levels:

> The only source term with the sign needed to cancel the matter term is the mean-curvature term —
> which is exactly why it can restore solvability while destroying the interpretation. At the |K|
> needed for solvability, K² **is** the dominant source and the wall is a subdominant correction to a
> K²-driven conformal factor.

This is consistent, not accidental: a slice with K = const ≠ 0 cannot be asymptotically flat, and the
Robin mass-falloff truncation is satisfied here by a **fake mass**.

### 1.3 Consequence

**The strong wall has no wall-dominated conformally flat constraint solution on any constant-K CMC
slice.** The K=0 obstructed branch is the *whole* conformally flat story, not its edge. Registered
constraint of this conclusion: it is a statement about **conformally flat** slices with **K = const**,
in κ=1 code units — see §4.

---

## 2. Finding B — the 2+1 ADM free evolution is unstable at the grid scale

### 2.1 The geometry operator is right

The one test that passes is the one that isolates the spatial operator from the evolution system:
**B2**, the code's own `R + K² − K_ijK^ij − 2κρ` evaluated on a slice produced by a *different*
solver (the 2026-11-21 York module):

| N | h | max\|Ham\| |
|---|---|---|
| 80 | 0.3 | 4.316e-04 |
| 160 | 0.15 | 1.068e-04 |
| 320 | 0.075 | 2.266e-05 |

pairwise orders 2.10, 2.44 → **3-grid Richardson order 2.01 → PASS**.

This required one substantive correction: the York module sources the constraint at
`scale = 0.05` × wall density, so the evolution had to use the **same** 5% weighting on ρ, S_ij, j_i.
Before that, B2 was O(h⁰) (0.68, order ≈ 0.02) — i.e. it was comparing two different physical
configurations. That is a legitimate physics fix, not a tolerance relaxation; it is disclosed in the
registration addendum.

### 2.2 The evolution is not

B1 (flat-space stationarity), B3 (spherical isotropy), B4 (constraint propagation) and B6 (exterior
asymptotics) **all fail**. Diagnosing *why* before changing anything was the point of B0:

| N | h | Ham(0) | Ham(t=2) | growth | rate × h |
|---|---|---|---|---|---|
| 48 | 0.4167 | 1.465e-04 | 9.348e-04 | 6.4× | 0.386 |
| 96 | 0.2083 | 7.316e-05 | 2.374e-03 | 32.5× | 0.362 |
| 192 | 0.1042 | 2.722e-05 | 4.077e-03 | 149.7× | 0.261 |

`rate × h` is **constant**: the unstable mode lives at the grid scale, and it **worsens** under
refinement. Both candidate cures were tried and **both fail**:

- Kreiss–Oliger dissipation at ε = 0.0 / 0.2 / 0.4 — still fails;
- Dirichlet background outer BC instead of extrapolation — still fails (×80, ×1524).

Recorded honestly: the cure is a **strongly hyperbolic formulation** (BSSN or Z4c with a Gamma-driver
shift), not parameter tuning. The registered gauge (zero shift, 1+log) is not strongly hyperbolic for
this system, and 1+log without a shift has no mechanism to stop the lapse from collapsing once |K|
accumulates.

### 2.3 What also fails, and why it matters

- **B3 FAIL is diagnostic, not incidental**: the isotropy defect *grows under refinement*
  (7.9e3 → 3.6e4 → 1.2e5, observed "order" −2.19, −1.74). Exact spherical symmetry violated at t=0
  by **0.000e+00** is driven to machine-irrelevant-then-catastrophic levels purely by the
  discretisation. This is the same instability seen from the symmetry side.
- **B6 FAIL**: spurious signal 10.55% against a 5% threshold. But note the honest limit — with the
  instability present, the "spurious signal" is dominated by the unstable mode, so this number is an
  **upper bound on the artefact plus instability**, not a clean measure of boundary reflectivity.
  R4 ⑥ was therefore **not independently tested to threshold**; it is blocked behind ⑤.
- **B5 has no valid data**: the full-strength wall cannot even be constructed (`RuntimeError` at
  scale=1.0), and Finding A now gives the geometric reason. The strongest *valid* slice (scale=0.05)
  evolves only to t ≈ 6, with `ham_rel` 6.6e-3 → 1.5e-1 and `alpha_min` 1.000 → 0.992.

---

## 3. Finding C — the axis itself is not representable by this discretisation

The staggered grid (ρ_i = (i+½)h) removes the `1/ρ` **division** but not the `1/ρ²` **cancellation**
between `∂_ρΓ^φ_{ρφ}` and `Γ^ρ_{φφ}Γ^φ_{ρφ}` in the Ricci trace. B7, with its prediction stated in
advance, confirms it:

| N | h | Ham(flat) | Ham(York) |
|---|---|---|---|
| 24 | 0.8333 | 7.680e+00 | 4.872e+00 |
| 48 | 0.4167 | 3.072e+01 | 1.959e+01 |
| 96 | 0.2083 | 1.229e+02 | 7.855e+01 |

Growth **×4.00 per resolution doubling** ⇒ the artefact is **O(h⁻²)**: the scheme is not convergent
at the axis. Verdict **FALSIFIED AS PREDICTED**, and the axis-inclusive evolution blows up before t=2.

A reference-subtraction fix (subtracting the flat-metric Ricci) was tried first and **rejected**: it
left a floor of ~6e-2 that never converged. The domain was therefore **retreated** to an annulus
ρ ≥ 4 — and B7 exists so that the retreat is a *tested, stated limitation* rather than a bug hidden
behind a domain cut.

---

## 4. What this does and does not close

**Answers, at the level stated:**

1. The 2026-11-21 K=0 obstruction is **geometric, not a slicing artefact**. Constant-K CMC slices do
   not rescue it, and Finding A explains the sign structure that forces that.
2. A 2+1 axisymmetric ADM **geometry** engine exists and is **independently validated** (B2, order
   2.01) on the regular part of the chart.
3. The 2+1 ADM **evolution** with zero shift + 1+log + 2nd-order FD + naive outer BC is **unfit for
   production**: grid-scale unstable, not curable by KO dissipation or boundary treatment.

**Does not follow, and must not be claimed:**

- **No stability result.** B2 passing does not rescue B1/B3/B4/B6. A correct spatial operator on an
  unstable evolution system is precisely what those four tests were designed to separate — and they
  separated it.
- **No physical-scale statement.** Everything is κ = 1 code units. **A local wall solution may not be
  extrapolated into a front enveloping the Earth** (§8.12 prohibition, unchanged).
- **No R4 ⑥ verdict.** Blocked behind ⑤.
- **No claim that "the wall resists".** The wall resists *being represented* by a conformally flat
  constant-K slice. That is a statement about the slice ansatz, not about the physics of the front.

---

## 5. The remaining route (registered OPEN)

Finding A localises the obstruction precisely: the term that restores solvability (K²) is the term
that destroys the interpretation, **because K is constant**. So the next attempt must use a
**localized mean curvature K(ρ,z)** — physically the sweeping front itself. That choice has one
immediate structural cost, and it is the reason this is a research step rather than a parameter:

> **K ≠ const breaks the identity that makes the momentum constraint trivially satisfied.** Hamilton
> and momentum must then be solved **jointly** (a 4-component elliptic system for ψ and the shift
> vector β), instead of a single scalar equation. That is a different, larger problem.

Two routes, in the order I would rank them:

| Route | Content | Cost / risk |
|---|---|---|
| **R4-⑤′** | Joint Hamilton+Mom solve for ψ and β with prescribed localized K(ρ,z); then evolve with **BSSN/Z4c + Gamma-driver** | correct physics, but no longer "conformally flat + CMC", so R4's original acceptance criteria must be re-registered |
| **R4-⑤″** | Stay in exact spherical symmetry (1+1), where the axis problem vanishes and B7 is irrelevant; accept that the axisymmetric-generic case stays untested | cheaper, but ⑤ was asked for *axial or spherical* — spherical alone under-delivers |

Either route requires the strongly hyperbolic reformulation **first**, since an initial-data slice that
cannot be evolved is not a finite-region geometry result. That dependency is the actual finding of
this round.

---

## 6. Honesty boundaries

- M4 external review — OPEN (needs humans).
- ~~The instability diagnosis is **structural** (grid-scale, `rate × h` constant) but the *specific*
  unstable mode was not identified by eigen-analysis; the claim is "not curable by KO/boundary
  treatment", which is weaker than "no formulation of this system can be stable".~~
  **SUPERSEDED later the same day — see §7.** The mode has now been identified by eigen-analysis and
  the boundary hypothesis has been falsified by a registered test.
- A1 is **FAIL-at-floor** (1.6e-12 vs 1e-12): the threshold was **not** edited. It is IDENT and
  excluded from the evidence count.
- The closing summary string in the evolution module was corrected **after** the run (it had
  pre-asserted a B3 validation that failed). Verified documentation-only by a re-run into
  `r4_axisym_2p1_results_rerun_check.txt`: `diff` against the archive shows **only the closing block
  differs, all 115 numeric lines byte-identical**. Archived stdout untouched. As a side benefit the
  round is thereby **bit-reproducible** — an independent execution of the same code reproduces every
  number in the record.
- All failed sub-runs are archived, none deleted (§9.1).

---

## 7. Amendment (2026-11-22, later the same day) — the instability localizes to the BULK, not a boundary

**Trigger.** §1-§2 left one route untested and the finding above admitted it: the *inner cut radius
was never varied*, and no eigen-analysis was done. A registered discrimination round
(`runs/R4/r4_instability_localization_registration.md`) was therefore run with the explicit
instruction that it could overturn §2.3. **It did not overturn it — it corroborated it, by killing the
competing hypothesis.**

### 7.1 Stage 1 — and its own two defects

| Test | Result |
|---|---|
| C3 Jacobian anchor (J·d vs directional derivative) | **PASS**, rel 1.0e-9 |
| C5 FD-step independence of the spectrum | **PASS**, 3.6e-10 |
| C1 geometry dependence (3 geometries, h = 0.4) | reported **INNER-EDGE** — **RETRACTED, see 7.2** |
| C4 spectrum vs measured growth | **FAIL**, ratio 5.02 (outside the registered [0.3, 3.0]) |
| C2 leading eigenvalue | Re λ = +0.51220 (N=16, h=1.25), +0.63602 (N=20, h=1.0); **ratio 1.242 vs h-ratio 1.25 ⇒ Re λ ∝ h^(−0.97)** |

Stage 1 contradicted itself (INNER-EDGE by growth ratio, but the eigenvector sat in the interior), and
reading it exposed **two defects in the metrics I had registered**, both disclosed in the registration
addendum *before* the corrected tests ran:

- **A1**: the 2D checkerboard index `|Σ(−1)^(i+j)|v|| / Σ|v|` **factorises and cancels** for a mode that
  alternates in one direction only, so it cannot certify "smooth". Replaced by per-direction indices.
- **A2**: C1's `growth = Ham(2)/Ham(0)` divides by an initial truncation level that **depends on the
  geometry** — `Ham(0)` was 1.421e-4 vs 1.738e-5 (8×) because moving the cut away from the steep `1/ρ`
  region lowers the truncation level. In absolute terms `Ham(2)` was 9.373e-4 vs 4.608e-4, a factor
  **2.0**, not the 4.02 the ratio reported. **The INNER-EDGE verdict was an artefact of a denominator.**

### 7.2 Stage 2 — the corrected, unconfounded test says BULK

**C7 (seeded amplification)** seeds the *same analytic perturbation* (Gaussian at ρ=12, z=0) in every
geometry and differences against an unseeded control on the same grid, so the truncation-amplitude
confound is removed and δ has zero ghost content:

| Geometry | A(t=2) | A(t=4) |
|---|---|---|
| baseline ρ_in=4, R=24 | 7.886 | 43.235 |
| inner cut ρ_in=8, R=24 | 7.878 | 43.002 |
| outer R=36 | 7.886 | 43.235 |

**Amplification ratios 1.000 / 0.999 / 1.000.** Moving the inner cut and the outer domain changes the
growth by **0.1%** — not "within 1.5×", but essentially exactly nothing. **C7 verdict: BULK.** The
registered INNER-EDGE and OUTER-EDGE branches are both **falsified**, and the boundary — the excise
surface and the frozen Dirichlet edge alike — is **exonerated as the driver**.

**C6 (mode structure)** then characterises what the mode actually is:

| Property | N=16 | N=20 |
|---|---|---|
| dominant field | gpp (0.57) | gpp (0.49) |
| alternation ρ / z | 0.13 / 0.12 | 0.10 / 0.10 |
| mass within 10% of inner / outer edge | 0.08 / 0.24 | 0.05 / 0.20 |
| radial mass peak (fraction of domain) | 0.969 | 0.975 |
| **‖Ham[v]‖/‖v‖** | **6.19e-2** | **1.30e-1** |

Two things follow. First, the mode is **constraint-carrying**, not constraint-neutral — so the
hypothesis I registered as A3 (that C4's factor-5 mismatch is because the leader is a gauge mode) is
**refuted**: the leader *is* the largest constrained mode. Second, the mode peaks near the outer edge
(peak 0.97), but C7's exact invariance proves that concentration is a **symptom, not a cause** — the
growth rate does not care where that edge is.

### 7.3 What survives, what is retracted

- **§2.3 finding 3 SURVIVES, and is now supported by a falsification rather than an assertion.** The
  registered sentence "the cure is a strongly hyperbolic formulation (BSSN/Z4c + Gamma-driver), not
  tuning" stands. The alternative explanation — that the instability is a boundary artefact of the
  ρ_in = 4 excise — was the most economical way to escape a formulation rewrite, and it is now **dead**
  at 0.1% precision.
- **Stage-1 C1's INNER-EDGE verdict is RETRACTED** as an artefact of the A2 confound. Quoted for the
  record: *"C1 verdict: INNER-EDGE … the F.7.2-3 sentence … is OVERTURNED for this mode and must be
  amended"* — that machine-generated conclusion is **wrong**, and no amendment to F.7.2-3 is made.
- **C4 remains FAIL as registered** (ratio 5.02). It is *not* reinterpreted into a pass. Observation
  only: the seeded version of the same comparison gives `ln(7.886)/2 = 1.033` against a 1/h-extrapolated
  `Re λ ≈ 1.59`, a ratio of **1.55**, which would fall inside the registered window. The unseeded C4
  measured the growth of a truncation pattern that projects weakly onto the growing modes; that is an
  explanation, not a revision.
- **Re λ ∝ h^(−0.97)** from two resolutions (N=16, 20). Two points fit a power law by construction, so
  this is stated as a scaling *consistency*, not a measured exponent.

### 7.4 What is newly OPEN (registered, not resolved)

- **"Smooth bulk mode" vs "under-resolved bulk mode" is not distinguished.** At N=16-20 there are only
  16-20 cells across the domain, and the per-direction alternation index detects *checkerboard* only;
  a mode varying over 3-4 cells would also read as ~0.1. Separating the two requires a spectrum at
  N ≥ 32, which was not run (dense eig cost). **This matters**: if the mode is genuinely smooth with
  Re λ ∝ 1/h, that is continuum ill-posedness; if it is merely unresolved, it is the ordinary
  weakly-hyperbolic short-wavelength sector. Either way BSSN/Z4c is the route, so the *decision* is
  unaffected — but the *diagnosis* is still coarse.
- C1's confounded metric is retained in the record as a negative example, not deleted.

**Nothing in §1-§6 changes except the struck sentence above. B1/B3/B4/B6 remain FAIL; locating the mode
is not curing it; no physical-scale statement is made.**

---

Content generated by AI

---

## 8. Erratum E1 (round 61) — the §7.4 N ≥ 32 item is discharged as a NO-GO on finite localisation

**Section 7 is not edited.** `RQ-07` emitted `runs/R4/r4_localisation_results.txt` from the
pre-registered instrument `src/r4_frontier/r4_localisation.py`.

- **E1** The §7.4 sentence *"Separating the two requires a spectrum at N ≥ 32, which was not run
  (dense eig cost)"* is superseded by the run now in evidence. A matrix-free Jacobian made N=32
  affordable; the archived N=16/20 values are reproduced to `5.39e−6 / 3.83e−6` relative
  (`runs/R4/r4_localisation_results.txt:46-49`). The three resolutions are N=16/20/32 with
  h=1.250/1.000/0.625 (`:26-38`).
- **E2** The result is **not** a smooth finite-width localized mode and **not** a 3-4-cell
  checkerboard. `Re lambda = 0.51220 / 0.63602 / 1.01514` fits `h^(−0.988)` (`:40-44`); the IPR
  widths are `xi = 15.668 / 16.027 / 17.291` code units, but `xi/L = 0.865` at N=32, i.e.
  domain-filling rather than interior-localised (`:29-38`, `:62-65`). Under the classifier fixed in
  `runs/R4/r4_localisation_registration.md` §6, `U1` and `U2` fire and `F1`/`F3` do not. The
  theorem-slot conclusion at `:72-81` is that no finite continuum localisation length exists for
  this sector of the ADM operator under test. This is a **conditional** result for zero-shift,
  1+log, 2nd-order FD ADM free evolution; it says nothing about BSSN/Z4c.
- **E3** Nothing in §1-§7 changes except the closure of this named open item. BULK remains BULK,
  the stage-1 `INNER-EDGE` verdict stays retracted, C4 stays FAIL at ratio 5.02, B1/B3/B4/B6 stay
  FAIL, no gate mark is written, and no physical-scale statement is made.

