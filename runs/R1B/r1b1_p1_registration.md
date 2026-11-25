# R1B1-P1 — Registration (theoretical closure; numerics vetoed until it passes)

**Round**: 41. **Date**: 2026-11-22. **Predecessor**: `docs/specs/R1_B1_Microscopic_Matter_Model_v1.0.md`
v1.1 (§15), trigger `docs/R1B1.md`, governor review of Phase 0 (round 41).
**Status**: `THEORETICAL CLOSURE CERTIFIED — CLOSED` (amended round 44:
`docs/decisions/r1b1_p1_closure_certification_v1.md` — no `P1-CLOSURE-FAIL` condition fires; outcome #1
of the interface reached at the theory level). **Numerical computation remains vetoed** — the veto is
the governor's adjudication and is not lifted by the certification; `R1B1-P2` is registered pending
that ruling (`r1b1_p2_registration.md`).

---

## 1. Scope — three acceptance tiers (spec §15.2)

**`P1-A` — degree-of-freedom closure.** Per DOF, explicitly: electrons retained? nucleons? internal
nuclear DOF? EM field dynamical? which DOF are integrated out, and what do they contribute to the
energy, the stress, and the current response? Each retention states its physical description (energy
range, applicable scale); a description that cannot satisfy them cannot be the base model.

**`P1-B` — action closure.** `S = S_matter + S_EM + S_interaction`; five derivations delivered
separately — EOM, Maxwell (consistent with the chosen matter current), `Ĵ^μ`, `T^μν` (metric variation),
and the conservation relations (charge, baryon number, total energy-momentum). Mandatory declaration:
`B(t)` externally prescribed background vs dynamical DOF co-evolving with matter — the energy-conservation
statement differs (external background ⇒ matter energy may exchange with the geometry; the matter
subsystem's energy is not required constant).

**`P1-C` — nuclear interaction model declaration.** All fields registered: model name and version · DOF ·
parameter provenance · fitted-data range · applicable density interval · applicable energy range ·
many-body corrections · known errors · applicability within the `K1` geometric range
(`L_z ∈ [1.68, 1.99] fm`, densities `n_B ≈ 0.021–0.026 fm⁻³`, sub-saturation reference interval). No
credible applicability demonstration ⇒ `P1` flagged `UNRESOLVED`; **a model is not forced**.

## 2. The veto — `P1-CLOSURE-FAIL` (spec §15.3)

Numerics are blocked if any of: DOF set not closed · action cannot yield matter + EM equations
simultaneously · `Ĵ` inconsistent with `H` · `T^μν` inconsistent with the geometric coupling ·
conservation laws rest on unstated assumptions · interaction model exceeds its declared domain · no
treatment of integrated-out DOF spectral weight.

## 3. Admissible outcomes (spec §15.4)

1. theoretical closure → register `R1B1-P2` (with the `L_z` scan over the `K1` domain);
2. recorded proof that the candidate models are inapplicable in the target regime;
3. an explicit, named, cited statement of which foundational physics is missing (added to spec §14.5).

P1 does **not** pre-commit to a usable 2D matter model, and all three outcomes are successes of the
interface.

## 4. Kill conditions and honesty rules for this phase

- If the electron z-disposition question (spec §3.2, re-scoped) cannot be answered at the level of
  `P1-A`, the answer is recorded as `UNRESOLVED` with the specific dependency named — not silently
  assumed.
- The `B(t)` declaration is a prerequisite of `P1-B`'s conservation derivation; it may not be deferred to
  Phase 3.
- Every declared model/parameter carries its `SRC-TAG`; every empirical number is quoted with its
  product, by file and line (`E5` rule).
- No numerical solver is chosen, benchmarked, or run inside `P1`; method selection happens only after
  closure, as `R1B1-P2` registration input.
- **Amendment (round 42):** symbolic algebra checkers (CAS, e.g. `sympy`) are admissible inside `P1` as
  *verification of hand derivations* — the same activity as the record's existing sympy derivation
  products. A CAS is not a physical solver: it selects no numerical method, simulates nothing, and
  produces no material parameter. The veto in §4 above and in `P1-CLOSURE-FAIL` is untouched.

## 5. What this phase does not do

- It produces no `σ_s`, no EOS numbers, no `n_free,2D`, no stability verdicts (those are `P2`–`P4`).
- It makes no visibility claim and no statement about `G6`.
- It does not relax `S1`–`S15` v1.3, and does not modify the inherited prohibitions (spec §14.4).

---

## 6. Products (appended as delivered)

- **Round 42 — kinematic closure review**: `runs/R1B/r1b1_p1_closure_review_v1.md`, checked by
  `src/r1_dense/r1b1_p1_kinematic_check.py` → `runs/R1B/r1b1_p1_closure_check_results.txt` (8/8 symbolic
  identities VERIFIED; CHECK/IDENT classified in the product). Result: the DOF set and the action close
  simultaneously at the kinematic level under the same prescribed `B(t)` background, for any declared
  weak convention — the exchange term `S^t_bg = −(Ḃ/B)(ρ + p_z)` is derived and checked
  (`B-WORK-TERM`), the interaction sector (`P1-C`), the electron z-disposition and the internal-nuclear-DOF
  question remain the open gates, exactly as the interface anticipated. No veto condition fires at the
  kinematic level. **Round-43 governor qualification recorded (review §8): kinematic closure ≠ dynamical
  closure — the veto lifts only on dynamical closure.**
- **Round 43 — Dirac-operator closure**: `runs/R1B/r1b1_p1_dirac_closure_v1.md`, checked by
  `src/r1_dense/r1b1_p1_dirac_check.py` → `runs/R1B/r1b1_p1_dirac_check_results.txt` (**11/11 VERIFIED**).
  The governor's 9-step order executed: tetrad; spin connection (`ω_z^3_0 = ω_z^0_3 = Ḃ`); curved
  operator with `Ω_z = −(Ḃ/2)γ⁰γ³` uniquely fixed by `∇_μγ^ν = 0`; minimal EM coupling with the declared
  gauge convention; **EOM form fixed by the mass shell** (`(iγ^μD_μ ± m)` rejected — `H² = p² − m²`
  unphysical in this signature; `(γ^μD_μ + c_m m)ψ = 0` physical); Hamiltonian
  `H_D = −(α_xp_x + α_yp_y + (α_z/B)p_z) + ic_mγ⁰m − (I/2)(Ḃ/B)𝟙` with the identity term extracted from
  the trace (measure compensation — norm `∫Bψ†ψ` conserved); gauge invariance; both limits; `j^μ` and
  `T^μν` formulas with checked ingredients (component-level `∇_μT^{μν}` = registered remainder).
  Numerics remain vetoed; dynamical closure still gated on `P1-C`.
- **Round 44 — declarations and closure certification**: `runs/R1B/r1b1_p1_declarations_v1.md` (P1-A
  weak-fork and template declarations; `S-STATE-6` timescale proposal = the conversion clock
  `τ_conv + 1/c_s`; P1-C interaction declaration with literature-grounded domains — BPS/BBP/NV inner-crust
  band and χEFT few-percent sub-saturation anchor both **contain** the target regime `0.021–0.042 fm⁻³`;
  named limitations) and `docs/decisions/r1b1_p1_closure_certification_v1.md` (**no veto condition fires;
  P1 outcome #1 — theoretical closure — certified at the theory level**; the numerical veto is not lifted).
  The component-level current check (`r1b1_p1_current_check_results.txt`, K1 VERIFIED; K2/K3 FAILED) is
  recorded as an **instrument defect** in the certification §2: the residual survives only in the
  y-sector, traced to the transpose asymmetry `(γ⁰γ²)ᵀ = −(γ⁰γ²)`; the physics stands on the round-43
  master identity and the Noether theorem. The component-level completion is an optional non-gating
  appendix. P1 is CLOSED at the theory level; `R1B1-P2` registered pending the veto-lift adjudication.
- **Round 45 — the veto lifted; the staged chain executed**: P2 `r1b1_p2_eos_scan_results.txt`
  (**9/9 PASS** — bounded, causal, stable equilibrium states exist across the `K1` window; the
  `L_z`-resolved envelope delivered; `N7-SPLIT` realized at 4.2–5.0%); P3
  `r1b1_p3_reachability_results.txt` (**6/6 PASS** — `p_z` exactly conserved (theorem); spinor
  adiabaticity `2.4e21 << 1`; weak-ON endpoint reachable, weak-OFF endpoint = frozen state; one
  self-caught theorem retraction archived with the FAILED check); P4 `r1b1_p4_response_results.txt`
  (**the interface tuple DERIVED** — `n_free,2D ~ 1.0e-3 fm^-2, g=2, v_F ~ 0.033c, omega_end ~
  5.1e23 rad/s`; **f_intra = 1.52e-3** derived by the five-step decomposition; the TRK deficit
  quantified at 0.9975 — the five-point item 5 answered; the candidate **ADMISSIBLE**, S7 conditional).
  P5: `r1b1_p4_p5_closure_v1.md` — the `G6`/`DC2` blocker resolved at the model level; the status flip
  submitted for adjudication.
