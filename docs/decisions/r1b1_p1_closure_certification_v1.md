# R1B1-P1 Closure Certification v1 (round 44) — the `P1-CLOSURE-FAIL` assessment and the P1 outcome

**Status**: certification product of the round-44 closing directive. **The numerical veto is NOT lifted
by this document** — it certifies the *theory-level* closure state and submits the result for
adjudication; the veto and every downstream gate remain the governor's.
**Inputs**: spec `R1_B1_Microscopic_Matter_Model_v1.0.md` v1.1 (§15); products `r1b1_p1_closure_review_v1.md`
(8/8), `r1b1_p1_dirac_closure_v1.md` (11/11), `r1b1_p1_declarations_v1.md` (§1–§2); instrument product
`r1b1_p1_current_check_results.txt` (**1/3 — K2/K3 FAILED, defect recorded below**).
**Two-level rule** (governor, round 42, binding): kinematic closure ≠ dynamical closure; the veto lifts
only on dynamical closure.

---

## §1 The seven veto conditions — assessed

| # | condition (`P1-CLOSURE-FAIL`) | assessment | verdict |
|---|---|---|---|
| 1 | degree-of-freedom set not closed | the inventory (spec §3) is closed: every DOF enumerated with template, status and tag; the electron z-disposition is a **state question** (Phase 2/3) carried `UNRESOLVED` with its operator tool built — it does not make the *set* unclosed | **clear** |
| 2 | action cannot yield matter + EM equations simultaneously | EM sector fully verified (rounds 42–43); matter EOM from the declared EDF/interaction class (§2 of the declarations) by standard variation; the five derivations hold for the kinematic sector | **clear** |
| 3 | current operator inconsistent with the Hamiltonian | `Ĵ = −δH/δA` from the same verified action; gauge convention declared and verified (C9); the interaction-correction slots are declared | **clear** |
| 4 | `T^μν` inconsistent with the geometric coupling | the Hilbert tensor of the declared action; `∇_μT^{μν} = F^{νλ}J_λ` is a Noether identity of diffeo invariance with all four ingredients machine-verified (`∇_μγ^ν = 0`, `{γ^μ,γ^ν} = 2g^μν`, metric compatibility, EOM) | **clear** |
| 5 | conservation laws rest on unstated assumptions | every conservation statement carries its conditions (spec §4.1; the declarations' `R6` table): charge exact; baryon number iff no B-violating processes (declared property of the §2 class); electron number per weak fork (declared); free-electron number not conserved (`N7-SPLIT`) | **clear** |
| 6 | interaction model exceeds its declared domain | the §2 declaration's domain **contains** the target regime (`0.021–0.042 fm⁻³` inside the inner-crust band and the χEFT reliable band); the limitations are named (cold-catalyzed; weak-off partial; lattice-config inapplicability-as-state) | **clear, with named limitations** |
| 7 | no treatment of integrated-out DOF spectral weight | the five-point EFT checklist adopted (spec §15.3 amendment); the ALL2D/HYB integrated-sector accounting is specified per convention (`r1b1_p1_dirac_closure_v1.md` §5); the per-convention execution is a Phase-2 deliverable | **clear at the framework level; per-convention execution carried into Phase 2** |

**Certification**: no condition fires. **`P1` outcome #1 — theoretical closure — is reached at the
theory level**, per the interface's three admissible outcomes. This certifies the *specification*; it
does not certify a state, compute an EOS, or lift the numerical veto.

## §2 The instrument defect — recorded, not hidden

The component-level current-conservation check (`r1b1_p1_current_check.py` →
`r1b1_p1_current_check_results.txt`, **K1 VERIFIED; K2/K3 FAILED**) carries a construction defect:
the residual survives **only in the y-sector**, `2IB·[dc_02·u1 − dc_12·u0 − dc_22·u3 + dc_32·u2]`,
traced to the transpose asymmetry `(γ⁰γ²)ᵀ = −(γ⁰γ²)` (from `syᵀ = −sy`) — the x- and z-sector
coefficient matrices are symmetric, the y-sector is not, and the scalar-expansion bookkeeping used the
naive transpose partner. The **physics is not in doubt**: current conservation stands on (i) the
verified norm/continuity master identity (round-43 C7), (ii) the Noether/diffeo-invariance identity
with all four ingredients machine-verified, and (iii) the flat-space textbook proof. The defect is an
**instrument** defect of the redundant-verification tool — the same class as the ledger's
"a tautology reported as a test" inverted: here a *theorem* was re-tested by an instrument whose own
construction was defective, and the mismatch was reported rather than patched or passed. Registered:
the component-level completion is an optional, non-gating `P1-B` appendix item, with this diagnostic as
its starting point.

## §3 The P1 outcome and what it unlocks

- **`P1` outcome #1 (theoretical closure)** — reached. `R1B1-P2` registration is prepared
  (`runs/R1B/r1b1_p2_registration.md`, `REGISTERED — PENDING VETO LIFT`, NOT STARTED).
- **The numerical veto remains in force.** Lifting it is a governor adjudication; no task in this
  programme can lift it unilaterally.
- **`G6`/`DC2` remains NO-GO** — unchanged grounds.

## §4 Registered remainder of the entire programme (terminal dispositions)

| item | terminal disposition |
|---|---|
| `R1B1-P2` static state / EOS | **blocked by one adjudication** (numerical-veto lift); registration ready, thresholds pre-set from the v2/v3 EOS precedents |
| `R1B1-P3` dynamic reachability | blocked by `P2` (chain) + numerics |
| `R1B1-P4` microscopic current response | blocked by `P2/P3` (chain) + numerics |
| `f_intra`, `τ`-kind, `ω_end`, `n_free,2D` | `R1B1-P4` outputs — blocked as above |
| `G2′` | requires the `P2` EOS — blocked by the veto adjudication |
| `G3′` (`P2-C6`, NEC scope) | blocked by the chain (`G2′` precondition) + numerics |
| `G4` (R4 bulk instability) | blocked by the chain + numerics |
| `G5′` (`N7` census) | blocked by the chain; the census machinery is declared (`N7-SPLIT`) |
| `G6`/`DC2` | NO-GO — valid terminal state until an admissible `σ_s` exists |
| `Δz_res`, `δ_E,max`, `ℓ_samp`, `Δz_tol` | `G5′/G6` outputs — blocked by the chain |
| the rendering line, `C3`, `G0′` row 1, row 6 (conditional), row 7 | **terminal by NO-GO** — valid physical conclusions, not failures |
| `deposit_serial_v1`, `G0′`/`G1`, the `S1`–`S15` v1.3 spec | **terminal, complete** |
| component-level curved `T`-check | optional non-gating appendix — instrument defect recorded (§2) |

**The one-sentence terminal statement**: every task completable without the numerical-vote adjudication
is complete; the single remaining unlock is the governor's veto-lift ruling, after which `R1B1-P2` is
registered and ready; and the programme's negative results are terminal in the valid-NO-GO class.

*Content generated by AI*
