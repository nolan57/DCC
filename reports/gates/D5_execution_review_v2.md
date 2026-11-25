# D5 Execution Review Report v2 (§9.4 ⑥: single status column version)

- **Review scope**: all executable content of `Macro3D_to_2D_Smooth_Reduction_Roadmap_v1.4.md`
- **Review date**: 2026-11-21 (third round, following D5 v1 and G0P-002)
- **Supersedes**: `reports/gates/D5_execution_review_v1.md`
- **Decision record**: `docs/decisions/G0p_seven_row_verdict_v3.md`
- **Reason for rewrite**: §2 "Passed items" and §6 "Review round-trip record" of v1 contradict each other — §2 still lists v1's PASS and v1's numbers row by row, while §6 revokes 5 of those rows. A report cannot say both "passed" and "revoked" at once. v2 removes the sectional opposition and switches to **a single status column per item**, with revoked items written directly as revoked.

## 0. Status definitions

| Status | Meaning |
|---|---|
| **PASS** | Code checks pass **and** the physical conclusion has not been revoked; the evidence category must be stated |
| **PASS(code) / conclusion downgraded** | Numerical computation is correct, but the physical conclusion is downgraded to OPEN / interval / UNDECIDED |
| **REVOKED** | Conclusion erroneous and revoked; does not enter downstream work |
| **OPEN** | Not completed or not closed |
| **BLOCKED** | Depends on unresolved upstream items |

## 1. Overall verdict

**The second-round freeze (G0P-002) has been revoked.** The freeze was overturned not by "finding one wrong number" but by **failure of the evidence chain**: of the 10 tests in v2, 4 were identities (back-solving after construction, self-comparison of the same expression, differentiation of a power law), and the one genuinely wrong quantity (`n_e` off by 10 times) happened to fall in a test blind spot. At the same time, the same slab used four mutually incompatible sets of dimensions across four modules, making `X_p` vary by 28 times and the final-state constraint-stress requirement by 3.5 times — precisely the quantities G2′/G5′ were to use.

**Status after v3**: frozen-state geometry and thermodynamic baselines may be cited (MODEL RESULT); β-equilibrium quantities must be cited as three-convention envelopes; the ion phase state and effective-2D domain coverage are UNDECIDED / OPEN.

## 2. Item-by-item status (single status column)

### 2.1 G0′ series

| Item | Status | Evidence | Product |
|---|---|---|---|
| G0′ v1 (G0P-001) numerical chain | **REVOKED** | Wrong `n_2D=(Z/A)N_s` convention; whole chain low by 10 times | `runs/G0/g0_prime_*` (archive) |
| G0′ v2 (G0P-002) numerical chain | **PASS** | 2D UR Fermi-gas algebra correct; `E_F=73.37`, `u=1.72e17`, `P=8.62e16` | `runs/G0/g0p2_results.txt` |
| G0′ v2 test conclusions | **REVOKED** | 4 of 10 were identities and 1 had a labeling error; "10/10 PASS" cannot serve as correctness evidence | Same as above |
| G0′ v2 handoff line `n_e` | **REVOKED** | Wrote `Z_eff·n_B=0.2200 fm^-3`; should be `Z_A·n_B=0.02200 fm^-3` | `scale_budget_v2.py:345-346` |
| G0′ v3 (G0P-003) | **PASS** | CHECK 7/7, IDENT 3/3 (not counted as evidence), NEGCTRL 1/1 | `runs/G0/g0p3_results.txt` |
| G0′ v3 handoff fix | **PASS** | `r1=r2=r3=2.200490e-02 fm^-3`; the wrong expression is off by exactly 10.000000 times | Same as above [2] |
| G0′ seven-row verdict | **PASS (3 rows settled / 4 rows OPEN)** | Rows 1 and 6 NO-GO, row 7 NO, rows 2–5 OPEN | `G0p_seven_row_verdict_v3.md` |

### 2.2 R1-B series

| Item | Status | Evidence | Product |
|---|---|---|---|
| R1-B1 v1 EOS | **REVOKED** | Missing `(ħc)²` factor, wrong density baseline | `r1b1_eos_results_v1_REVOKED.txt` |
| R1-B1 v2 unit fix | **PASS** | `p=ħc k_F`, `(ħc)^-3`; Chandrasekhar `P/u→1/3` | `r1b1_eos_results.txt` |
| R1-B1 v2 single-convention conclusion (`X_p=1.6e-3`) | **Conclusion downgraded** | Holds only under ALL3D; contradicts the 204 MeV subband spacing of R1-B4 | Same as above |
| R1-B1 v3 three-convention envelope | **PASS (conclusion is an interval)** | `X_p∈[1.62e-3,4.50e-2]`, `μ_e∈[6.73,24.96]`, `P_tot∈[1.84e16,6.48e16] N/m` | `r1b1_eos_v3_results.txt` |
| R1-B1 v3 dual values of `c_s²` | **PASS** | Unified as `dP/dε=0.1055` | Same as above, K3 |
| R1-B1 v3 new finding: 2D electrons have a lower density bound for β equilibrium | **PASS** | HYB `n_thr=6.15e-6`, ALL2D `6.82e-6`, ALL3D no bound | Same as above [2] |
| R1-B2 v1 `Γ_i=0.179` | **REVOKED** | This ratio is not the classical coupling parameter (`Γ→∞` at `T=0`) | `r1b234_screening_results_v1_REVOKED.txt` |
| R1-B2 v2 "crystal reversal" | **REVOKED** | Three O(1) problems: WS radius used as Madelung distance, 3D-OCP frequency, no screening | `r1b234_v2_results.txt` |
| R1-B2 v3 phase-state verdict | **PASS(code) / conclusion UNDECIDED** | Lindemann `δ=0.180`, `E_zp/|E_M|=0.107`, band 0.05–0.26 spanning 0.1–0.2 | `r1b234_v3_results.txt` |
| R1-B3 v2 `σ_ν=1e-43 m²` | **REVOKED** | Too large by about 1e5 (weak-interaction cross section at 10–30 MeV ~1e-48 m²) | Same as above |
| R1-B3 v3 transport timescale | **PASS(code) / conclusion downgraded** | `τ_T=1.464`, diffusion 1.03 ns, `τ_ν=4.2e-20`; full transport OPEN | Same as above |
| R1-B4 v1 energy gap (passing off `E_1`) | **REVOKED** | `E_1` is the ground-state energy, not the energy gap | v1 archive |
| R1-B4 v2 energy-gap values | **PASS** | `ΔE₁₂^NR=613.5`, `ΔE₁₂^rel=430.0` MeV | `r1b234_v2_results.txt` |
| R1-B4 v3 domain coverage | **PASS(code) / conclusion OPEN (conditional)** | At G0 density `E_F,nuc=24.0<42.6` inside the domain; at `n_0`, `58.4>42.6` outside | `r1b234_v3_results.txt` |
| R1-B4 v3 electron `E_1` label | **REVOKED** | Using the NR formula for the electron printed 3.8e5 MeV — a labeling error | Same as above |

### 2.3 R2 series

| Item | Status | Evidence | Product |
|---|---|---|---|
| Check ③ v1 | **REVOKED** | Field component written as `F_tx` (should be `F_ty`), and symbolic computation not executed | `check123_results_v1_REVOKED.txt` |
| Check ③ v2 conclusion | **PASS** | "No solution" direction correct; `d_t f = d_x E` correct | `check123_v2_results.txt` |
| Check ③ v2 "machine execution" claim | **REVOKED** | `dF_A/dF_B` is a hand-written dictionary entry, followed by `simplify(∂_t f − ∂_t f)==0`, which is tautologically true | `inverse_problem_check_v2.py:65-76` |
| Check ③ v3 exterior derivative | **PASS** | Real implementation of `ext_d()`; `d(dω)=0` self-check passed | `check123_v3_results.txt` [T1]–[T4] |
| Check ③ v3 "no solution" strength | **PASS (strengthened)** | `κp_x,req=−[(γ−h/2)²+3h²/4]<0` vs `κp_x,B=+f²e^{−4ht}/2>0`, parameter-independent | Same as above [T7] |
| R2-D L1 / L2 | **PASS** | 5/5, 4/4 | `r2d_l1/l2_results.txt` |
| R2-A ten mappings | **PASS (1 item OPEN)** | P2-C6 still OPEN | `R2A_registration_v1.md` |
| G3′ gate | **OPEN** | Depends on P2-C6 and the N11 boundary condition | — |

### 2.4 Stage gates

| Gate | Status | Gap |
|---|---|---|
| G0′ | **PASS (v3, numbers citable)** | 4 of 7 rows still OPEN, which is not a gate problem |
| G1 | **PASS** | P1 freeze registered in `runs/P1/P1_freeze_registration_v1.md` |
| G2′ | **BLOCKED** | The three-convention envelope must first be implemented in the D3 budget |
| G3′ | **OPEN** | P2-C6, N11 boundary condition |
| G4 / G5′ / G6 | **OPEN** | Depends on upstream |

## 3. Process findings added this round (not carried to the next round)

1. **"Pass counts" are not evidence.** From now on all reports must count by CHECK / IDENT / NEGCTRL categories and explicitly print the IDENT count. v2's "10/10 PASS" and v3's "7/7 CHECK + 3 IDENT" are semantically completely different.
2. **Negative controls should be retained permanently.** The wrong expression `Z_eff·n_B` was not deleted but registered as `NEGCTRL`, required to deviate by exactly 10.000 times. If this ratio ever becomes 1.0, it means the guard has failed rather than the error having been fixed.
3. **Cross-module quantities must be defined at a single point.** `src/common/conv.py` is the sole source for constants, column/bulk density conversions, dimension assignment, and the β solver; all four v3 modules `import` it.
4. **Dimensional conventions must be reported together with the numbers.** Reporting `X_p` without reporting `D_e/D_nuc` is equivalent to not reporting it.

## 4. Still not closed (must not be treated as concluded)

| Item | Status | Required action |
|---|---|---|
| β-equilibrium final-state composition and pressure | OPEN | Three-convention envelope given; must be narrowed after R1-B4 determines nucleon dimensions |
| Ion phase state CRYSTAL/LIQUID | UNDECIDED | Screened 2D-OCP criterion (MC or Lindemann calibration) |
| Effective 2D domain | OPEN | The domain does not cover `n_0`; the `E_probe` upper bound must be recalibrated |
| Neutrino transport and entropy ledger | OPEN | R1-B3 full weak-interaction rates |
| P2-C6 | EXECUTED at screening level | See addendum §6 row A3; production perturbation theory remains the boundary |
| N11 boundary condition | EXECUTED / approach falsified | See addendum §6 row A4; dynamical apparatus model + G0↔P2 unit bridge OPEN |
| York initial data | EXECUTED at screening level; **production attempt NO-GO** | See addendum §6 row A5 and §7; time-dependent 2+1 evolution attempted 2026-11-22 and **refused by the physics** (no wall-dominated conformally flat CMC slice; free evolution grid-scale unstable) |
| KZ estimation, `ε_mn` time-integration scan | EXECUTED | See addendum §6 rows A1/A2; KZ quantitative conclusion downgraded |
| R5-L2 self-consistent $\sigma_s(\omega)$ | **Baseline defect fixed — re-run DONE at v3 baseline (2026-11-22)** | Original run hard-coded `N_2D=2.20e27`, `E_F=23.20 MeV` (pre-G0P-003-v3); its "G0 consistency 5.5e-7 PASS" validated the revoked chain. Re-run at `2.20e28` / `73.37 MeV`, with `m*/m_e` now **derived** from `E_F` (the literal `45.4` had silently desynchronised) and the probe row moved 50→200 MeV so the interband switch still demonstrates. Thresholds unchanged. `OVERALL: PASS`, `C0 7.09e-05`, all registered expectations met. Superseded run archived as `r5l2_sigma_s_results_v1_REVOKED_BASELINE.txt`. **Still not a compliant §6.7 input**: τ is scanned not solved, interband line shape unknown, G4/G5′ open ⇒ label stays, no visibility conclusion. Registration `runs/R5/r5l2_rerun_registration.md` |

## 5. In one sentence

The credibility gain of v3 does not come from "measuring a few more items," but from **dividing tests into those that can fail and those that cannot, and acknowledging that the second category makes up one third**.

---

## 6. Addendum (2026-11-21, fourth execution round: single status column, same discipline)

> Executor: AI (ZCode session). Five previously OPEN actionable items were executed; products are registered in
> roadmap Appendix F.6. This addendum extends the §4 table; it does not supersede anything in §2.

| Item | Status | Evidence | Product |
|---|---|---|---|
| A1 Sprint-1 Kibble–Zurek estimate | **PASS(code) / conclusion downgraded** | Freeze-out anchors 2/2; monotone direction captured; p_KZ = 1/6 vs p_num = 2.29 (deep-adiabatic window) and normalization drift ~83x — pure-gap KZ registered as qualitative only | `runs/R1A/r1a1_kz_results.txt` |
| A2 Sprint-1 B(t)/ε_mn/P_m→n scan | **PASS(code)** | 5/5: cross-implementation anchor 1e-10, static anchor, monotonicity across 3 exponent families, convergence 5.9e-7; KG raw drift 1.1e-6 registered + invariant projection (post 4.4e-16) | `runs/R1A/r1a1_ptilde_scan_results.txt` |
| A3 P2-C6 linear perturbative stability | **PASS (screening level)** | 5/5: lambda_max <= 0.03 << sqrt(2) bound on 5 backgrounds; tachyonic anchor 1e-6; constraint control 2.1e-7 < 1e-4; two-tolerance convergence 0.0000 | `runs/R2/r2c6_linear_stability_results.txt` |
| A4 N11 into 1+1 slab | **Machinery PASS / approach FALSIFIED (registered)** | Injection validated at 1.1e-16; three falsification modes registered (zero in-plane response of in-plane tension + D2 window destroyed; ansatz degeneracy H_B+H_C→0 with singular solve; drift up to 18x); crashes archived | `runs/R2/r2d_l3_n11_slab_results.txt` |
| A5 R4-⑤ / P2-C2 York initial data | **PASS (screening level) + major finding** | 5/5: vacuum 3e-13, puncture order 2.01, kink order 2.3 resid <=2e-10; **existence threshold bracketed (0.05, 0.07) × P1a wall density — full-strength wall admits NO time-symmetric slice**; run-1 divergence documented in the module header (**process slip registered: run-1 stdout overwritten before archiving, no raw log**) | `runs/R4/r4_york_initial_data_results.txt` |
| A6 Blocked items (unchanged) | **OPEN — require humans or upstream gates** | M4 external review; literal two-person recomputation; R5-L3/L4 numerical solution (gated G4/G5′); HNC EOS / Level-B atomic model (refinement level) | — |

### 6.1 Gate-level consequences of this round

1. **G3′**: the last acceptance item (P2-C6) is closed at the screening level with the honest scope boundary
   registered; the gate recommendation becomes "conditionally met — production perturbation theory outstanding".
2. **G4 prerequisite (R4-⑤)**: the initial-data layer is delivered; the existence-threshold finding must be carried
   into any D3/G3′-level verdict discussion of strong-wall configurations.
3. **N11**: the single-point 8.62e16 requirement is unattainable via prescribed stress within the registered ansatz;
   any N11 closure claim now requires a dynamical apparatus model (registered OPEN).

---

## 7. Addendum (2026-11-22, fifth execution round: R4-⑤⑥ production attempt)

> Executor: AI (WorkBuddy session). Two modules executed under the same discipline; products registered in roadmap
> Appendix F.7. Decision record: `docs/decisions/r4_finite_region_geometry_v1.md`. This addendum extends §6; it
> supersedes no verdict but **narrows** the R4-⑤ finding from a slicing-specific obstruction to a family-wide one.

| Item | Status | Evidence | Product |
|---|---|---|---|
| R4-⑤′ CMC initial data (is the K=0 obstruction a slicing artefact?) | **Executed — answer is NO (decisive negative control)** | Machinery 2/2 PASS (MMS; nonlinear 3-grid order 2.314, resid ≤1e-12). A5 finds the constraint solvable at high \|K\| (scale_crit 0.9394 at K=0.5, 2.2202 at K=1.0) but **A6 withdraws it**: at \|K\| = 0.75/1.0/2.0 the background deviation is 0.6871/0.7244/0.7987 with the wall OFF and M(R) ≈ −64.7/−69.2/−78.8 ⇒ K²-dominated, negative-mass, not asymptotically flat. A1 FAIL-at-floor (1.6e-12, IDENT, threshold **not** edited) | `runs/R4/r4_cmc_initial_data_results.txt` |
| R4-⑤″ / ⑥ 2+1 axisymmetric evolution | **Executed — geometry operator PASS, free evolution FAIL** | B2 (independent elliptic solver as source) 3-grid Richardson **2.01 PASS**. B1/B3/B4/B6 FAIL; B0 shows the unstable mode is **grid-scale** (`rate × h` ≈ 0.26–0.39 constant, growth worsens under refinement), and KO dissipation (ε ≤ 0.4) + Dirichlet outer BC both fail. B5 no valid data (scale=1.0 RuntimeError). B7 FALSIFIED AS PREDICTED (axis artefact O(h⁻²), ×4.00 per halving) | `runs/R4/r4_axisym_2p1_results.txt` |

### 7.1 Gate-level consequences of this round

1. **R4-⑤ is NO-GO at production level, and the obstruction is now family-wide.** It is no longer "no K=0 slice";
   it is "no wall-dominated conformally flat slice on any constant-K CMC slice". Any future strong-wall verdict that
   leaned on "pick a different slicing" is closed. The only surviving route is a **localized K(ρ,z)**, which forces a
   **joint Hamilton+Mom solve** for (ψ, β) because `K ≠ const` breaks the identity that makes the momentum constraint
   trivial.
2. **R4-⑥ (exterior asymptotics) is NOT testable yet** and its 10.55%-vs-5% failure must **not** be cited as a
   boundary-reflectivity result: with the grid-scale instability present, that number is an upper bound on
   artefact **plus** instability. ⑥ is blocked behind ⑤, not independently adjudicated.
3. **A gate-level prerequisite is now explicit and new:** an initial-data slice that cannot be evolved is not a
   finite-region geometry result, so **a strongly hyperbolic formulation (BSSN/Z4c + Gamma-driver shift) is a
   prerequisite**, not an optimisation. This dependency did not exist in v3's gate structure.
4. **No verdict in §2 or §3 changes.** The round adds a refusal and removes a route; it credits nothing.

---

## 8. Errata found by the 2026-11-22 documentation audit (record-level, no verdicts change)

> A line-by-line verification of the 2026-11-21 round's claims against `runs/`, `src/` and the roadmap found every
> **number** correct and every **verdict** correctly stated. What it did find is a class of *record* defects: stale
> status lines and one broken citation. Archived run logs are **not** edited (§9.1 keeps them as produced); the
> corrections are recorded here and in the affected documents.

### 8.1 Broken citation (serious for §9.1 purposes)

`runs/R4/r4_screening_registration.md` stated that the York run-1 Picard divergence was "archived as
`r4_york_initial_data_run1_FAIL.txt`". **That file does not exist anywhere in the repository**, and this report's
own §6 correctly records that run-1's stdout was *overwritten before archiving, no raw log*. Two documents
disagreed and the specific one was wrong: the record asserted an archive that was never created.
**Corrected** in the registration; the honest statement is "documented in the module header, no raw log exists".

### 8.2 Mislabelled threshold in the P2-C6 run log (not edited)

`runs/R2/r2c6_linear_stability_results.txt` prints `catastrophic := lambda_max > 1.48492 = sqrt(max V'')`. That
label is false: `sqrt(max V'') = sqrt(2λv²) = 1.41421`, while the constant actually applied is
`1.05 × 1.41421 = 1.48492` — a **5% tolerance band above** the exact bound. So the log describes a relaxed
threshold as an exact physical bound. The *summary tables elsewhere were right* ("√2 catastrophic bound"); it is
the solver's own print that mislabels it. **Verdict unaffected**: λ_max ≤ 0.02901 is >50× below either number.
Fixed in the source so a future run prints it correctly; the archived log is preserved as-is.

### 8.3 Stale bracket in the York run log (not edited)

`runs/R4/r4_york_initial_data_results.txt` carries an intermediate diagnostic line saying the existence threshold
is "bracketed in (0.05, 0.1)", while the verdict line and the registered finding both say **(0.05, 0.07)**. The
(0.05, 0.07) value is the correct one (the 0.07 row was scanned and has no solution). The inline note is a stale
intermediate and should be read as superseded by the verdict line.

### 8.4 Wording: "monotone over two decades"

The quoted "two decades" refers to the **range of the observable** `n_exc` (2.6e-3 → 2.2e-5, ≈1.95 decades), not
to the range of the scan parameter. The scan is `β_C = |β_e|/τ` over `τ ∈ (0.5,1,2,4)` × `|β_e| ∈ {1/3,1/2,2/3}`,
i.e. **β_C spans a factor 16 (1.2 decades)**. Monotonicity holds across that scan for all three exponent families.
The claim is correct; the phrasing invites a 2-decade reading of the control parameter that the run does not support.

### 8.5 Sections that had gone stale and are now corrected

| Location | Was | Now |
|---|---|---|
| roadmap §12.3 execution banner | "The KZ estimate and B(t) scan **have not been started**" | both EXECUTED, with the KZ downgrade and the diagonal-P_mn result stated |
| roadmap §12.6 execution banner | "⑤ EXECUTED at screening level … ⑥ OPEN" | carries the 2026-11-22 correction: ⑤ NO-GO at production, ⑥ NO-GO blocked behind it |
| `runs/R2/R2A_registration_v1.md` §2 table | acceptance row "linear perturbative stability = **OPEN**" | EXECUTED at screening level (5/5 PASS), production perturbation theory still OPEN — the row had not been updated after the run its own prose describes |

### 8.6 What the audit confirmed as correct

Every figure in the 2026-11-21 status table verified exactly against the run files: KZ 4/4 PASS with
p_KZ = 0.1667 vs p_num = 2.2919 and ~83× normalisation drift; the P_m→n scan 5/5 PASS with diagonal P (an exact
consequence of translation invariance, stated as such); P2-C6 5/5 PASS; N11 machinery at 1.125e-16 with the
prescribed-stress approach falsified; York 5/5 PASS with the (0.05, 0.07) bracket. The disclosure that the raw
KG residual (1.107e-6) **exceeded** its registered 1e-8 threshold and was remedied by an invariant projection at
extraction was present and accurate — it is registered as measured, not silently corrected.

## 9. Addendum (2026-11-22, eighth round: S3→S4 branch specification, M_eff boundary draft v0.1)

**Gate effect: none.** No criterion in §2 or §3 changes, and no numerical verdict moves. This round registered a
*specification* and audited it; it added no physics and no run that could pass or fail a gate.

| Item | Status | Evidence |
|---|---|---|
| S3→S4 branch specification (M_eff boundary) | **Registered verbatim, audit CLOSED** | `docs/specs/meff_boundary_v0_1.md` (verbatim, LaTeX artefacts preserved); `reports/reviews/meff_boundary_v0_1_audit.md` (F1–F11); probe `runs/S45/meff_boundary_probe_results.txt` 6/6 registered criteria met at IDENTITY/ARITHMETIC level |
| `C_info` (information-loss constraint) | **REJECT as formulated** | ΔH/A = 1.248e22 bit·m⁻² at a₀; ΔH = 4.99e20 bit for the registered object; extensive (ratio 10.000000); a 1 Tbit budget admits ≤ 8e-11 m², the object needs 5e8× more |
| `C_top` (topological invariance) | **REJECT — falsified by the registered census** | χ(2D) = 1.18e10 vs χ(3D) = 2, ratio 5.9e9; condition holds on converted fraction ≤ 8.5e-11, and is directionally inverted |
| `C_geo` (curvature) | **REJECT as formulated** | identical to `λ_obs/R_⊥` (rel. diff 0.0); vacuous where defined (3.4e-18 plate, 1.1e-3 ridge) |
| `C_phys` (action ratio) | **REJECT as formulated** (analytic, not measured) | ratio of an indefinite quantity; needs a positive-definite perpendicular energy fraction |
| **Lifetime constraint** | **MISSING — the decisive omission** | `t_rip/(2L/c) = 1/√2` exactly for L = 0.20/1.00/0.070 m (12 digits); no constraint in the draft contains a time scale |
| **Injectivity / graph-ness** | **MISSING — the core of relaxing C1** | `C_geo` and `C_info` both presuppose `z = z(x_i)`, i.e. assume the very property the 3D object violates |

### 9.1 Governance change (the one thing that does move)

Ledger §9 previously said branch products "may not be cited as evidence for the chain", without distinguishing
**boundary data** from **validation evidence**. The draft's §3/§4 supplies that distinction and it is correct: S2's
solve will require outer/asymptotic data, and refusing it would make S2 unsolvable. **Adopted**: the branch may
supply boundary data to the S0→S2 solve; it may never contribute to the S0–S2 validation ledger, nor to any
statement about whether 2D-ification works. `staged_relaxation_visual_route_v1.md` §9 amended accordingly; the
original sentence is superseded in letter and preserved in intent.

### 9.2 Carried into the OPEN list

- **v0.2 of the specification** — **WRITTEN AND ADOPTED 2026-11-22** (`docs/specs/meff_boundary_v0_2.md`):
  `ME1` injectivity, `ME2` parallax at the declared sampling scale, `ME3` positive-definite perpendicular energy
  fraction, `ME4` fragment census, `ME5` lifetime; `C_info` dissolved into `ME1` plus a non-gate bit budget. See §11.
- **`ε` scalarisation convention** — **RESOLVED 2026-11-22**: `ε := 1 − φ_conv`, with `φ_conv` the converted
  proper-volume fraction; direction `dε/dB < 0` and non-uniqueness of the field→scalar map declared in v0.2 §1.
- **Naming debt — RESOLVED 2026-11-22.** roadmap §6.1's `C1–C4` (contrast criteria) collided with the ledger's
  `C1–C3`. Renamed **`CM1–CM4`**, *not* `K1–K4` as provisionally proposed: the four items offered under `K1–K4`
  were the enhancement techniques rather than the §6.1 criteria, and `K1–K4` was already in use as the sci-fi
  boundary's four consistency checks (`scifi_boundary_v1.md`, `internal_consistency_v1.py`, archived output).
  Rule registered in the ledger §12; registry `docs/conventions/symbol_registry.md`; enforcement
  `src/common/symbol_lint.py` (`MUST-FIX = 0`). See roadmap §F.10.

*Content generated by AI*

## 10. Addendum (2026-11-22, ninth round: symbol namespace isolation)

**Gate effect: none.** Names only; no threshold, verdict or numerical result changes. Recorded because the gate
documents themselves cite these labels.

| Item | Status | Evidence |
|---|---|---|
| `C` conflict (constraints C1–C3 vs §6.1 criteria C1–C4) | **RESOLVED** | §6.1 renamed **CM1–CM4**; ownership rule R2 awards `C` to the load-bearing set |
| `K1–K4` as the replacement | **REJECTED** | (i) content mismatch: the four items were the enhancement techniques, now `EN1–EN4`; (ii) `K1–K4` already owned by the sci-fi boundary's four consistency checks, and `K` is the extrinsic-curvature trace |
| `L` conflict (optics layers / R2-D redshift layers / fidelity levels) | **STAGED — OPEN** | three-way; R2-D labels are embedded in file paths, so renaming would break §9.1 reproducibility |
| `B`, `P`, `M` label conflicts | **RESOLVED in prose / ERRATA in archives** | `LOC-B*`; probe checks `Q1–Q6`; proposed v0.2 set `ME1–ME5` |
| Enforcement | **OPERATIONAL** | `src/common/symbol_lint.py` → `runs/CONVENTIONS/symbol_lint_results.txt`; `MUST-FIX (A,C,D) = 0` |

### 10.1 Process note

This round is the first in which the *record* was machine-audited for label consistency rather than read. The
linter found the `K1–K4` collision and the pre-existing `[P1]…[P6]` in `persistent_visualization_v1.py` — neither was
visible on inspection. It also distinguishes mentions from uses (code spans) and archived stdout from active prose,
so it does not demand edits that §9.1 forbids.

**One instruction error is registered** (roadmap §F.10.2): the proposed `K1–K4` mapping assigned the enhancement
techniques to the §6.1 criteria slots. Had it been applied literally, the "single source of truth" would have
recorded four wrong definitions — the precise failure the registry exists to prevent. The same class of check
applies to this round's own output: the v0.1 draft's `C_geo/C_phys/C_info/C_top` are non-compliant under rule R4
regardless of whether their content is adopted.

*Content generated by AI*

## 11. Addendum (2026-11-22, tenth round: disposition of the M_eff boundary draft — rulings D-A, D-B)

**Gate effect: none.** No threshold, verdict or numerical result changes. What changes is what the branch may be
cited for, and which constraints define the branch.

| Item | Status | Evidence |
|---|---|---|
| Boundary-data / validation-evidence split (D-A) | **RATIFIED**, condition `PROV-3` added | `docs/decisions/meff_boundary_disposition_v1.md` §2; `docs/conventions/provenance_tags_v1.md` |
| `C_info` (D-B) | **DISSOLVED** — not repaired | injectivity → `ME1`; magnitude → non-gate budget (`BUDGET-1`); `δ_info` withdrawn |
| Dissolution content-preserving? | **YES**, by exhaustive check | D5: `ΔH = N_ov·log2 V` and `ΔH = 0 ⟺ injective`, 256/256 configs, error `0.00e+00` |
| `C_info`'s actual content | **restated** | `A_crit ∝ δ_info` exactly (D3) ⇒ it is an upper bound on base **area**, not an information threshold |
| v0.2 spec `ME1`–`ME5` | **ADOPTED** | `docs/specs/meff_boundary_v0_2.md`; v0.1 superseded, body preserved unedited |
| `C_geo`/`C_phys`/`C_info`/`C_top` | **RETIRED** (R4) | may not be reintroduced; any future citation is historical |
| `ε` scalarisation | **RESOLVED** as a convention | `ε := 1 − φ_conv`, converted proper-volume fraction, with direction (`dε/dB < 0`) and non-uniqueness declared (v0.2 §1) |
| Branch tolerances `δ_ov`, `ℓ_samp`/`Δz_tol`, `δ_E,max` | **OPEN** | v0.2 certifies **no** membership; a definition registered before its thresholds — the correct state |
| `L` conflict | **STAGED — OPEN**, unchanged | §10 row stands |
| Provenance enforcement | **OPERATIONAL, negative-tested** | `src/common/provenance_lint.py` → `runs/CONVENTIONS/provenance_lint_results.txt`; `VIOLATION = 0`; a planted branch file claiming `CHAIN-EVIDENCE` was flagged, and a planted incomplete `BOUNDARY-INPUT` was flagged |

### 11.1 The one substantive objection, and how it is handled

D-A as stated prevents the branch from *citing* itself as evidence, but not from *determining* the answer: for an
elliptic problem, Dirichlet data over the whole outer boundary fix the interior uniquely, so a branch-fed S2 run
would reproduce the branch, and no agreement between them would test anything. Condition `PROV-3` closes this with
three declared fields (type / over-determination count / derivation independence) and a reporting rule ("solution
given data D", never "confirmation of D"). Recorded because a future round will be tempted to treat the split as
sufficient on its own.

Also recorded at closure: supplying boundary data does **not** confer well-posedness. That is a property of
*(operator, boundary type, function space)*, independent of the values — the R4 CMC round demonstrated the point
when a Neumann row at the inner cut produced a singular Jacobian and the fix was a change of *type* (Robin), not of
data.

*Content generated by AI*
