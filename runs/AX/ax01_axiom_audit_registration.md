# AX-01 registration — axiom audit of the DCC programme's fixed premises

**Date**: 2026-11-24
**Status**: PRE-REGISTERED BEFORE INSTRUMENT — no `runs/AX/ax01_axiom_audit_results.txt` exists at the
time of writing.
**Authority**: Governor directive G-68-01 (round 68). This file fixes the target list, the label
schema, the predicted counts and the numeric assertions **before** the instrument is run. Nothing
here may be edited after emission; a later correction must take the form of an appended erratum with
its own product.
**Evidence class**: STRUCTURAL / EPISTEMIC AUDIT. `PROVENANCE: NEITHER`. This review establishes no
physics, passes no gate, and is not evidence for or against any route.

---

## 1. One question

For every quantity, relation and criterion the programme currently treats as fixed, what is its
epistemic status, is its stated form coordinate- or convention-dependent, and which downstream
conclusions move if it is replaced?

## 2. Label schema (exactly one per item)

| label | meaning |
|---|---|
| `MEASURED` | from experiment, independent of model choice |
| `DERIVED-COVARIANT` | derived; result is a scalar/invariant |
| `DERIVED-COORD` | derived, but the stated value/form depends on coordinates or gauge |
| `CONVENTION` | defined by fiat inside the programme |
| `ASSUMPTION` | used as a premise, never justified or derived in the record |
| `UNVERIFIED` | claimed true; no derivation, measurement or citation on file |

`MEASURED` is assigned only where the record's number is an experimental constant in the ordinary
sense (`a₀`, the solar irradiance in a declared band). A number that is "measured" **for a declared
scene under a declared instrument** (e.g. `C = 3.3166`) is not itself an audited item; the derived
`Φ` that consumes it is, and is labelled `DERIVED-COORD`.

## 3. Target list — 35 items, fixed before the run

`G` geometry/metric · `D` dynamics/constraints · `T` thresholds/pricing · `L` definitions/logic ·
`S` programme structure · `X` items discovered during this audit.

| id | subject | predicted label |
|---|---|---|
| `AX-G01` | `a₀` = 5.2917721e−11 m | MEASURED |
| `AX-G02` | `N_s` = `M/(m̄A_⊥)` = 4.2155e27 m⁻² | DERIVED-COVARIANT |
| `AX-G03` | `d∥` = 15.40 fm = `N_s^{-1/2}` | DERIVED-COORD |
| `AX-G04` | metric ansatz `ds²=−dt²+dx²+dy²+f²dz²` (`N=1`, `β=0`, `g_xx=g_yy=1`) | CONVENTION |
| `AX-G05` | `L_z` = 1.0 fm, density-inferred | CONVENTION |
| `AX-G06` | "atomic spacing" 0.3 nm | CONVENTION |
| `AX-G07` | `d∥` **used as** the plate thickness (RL-6 denominator, `ME1`/`C1b`) | ASSUMPTION |
| `AX-G08` | reference object `(M=70 kg, A_⊥=1 m², m̄=10 amu)` | CONVENTION |
| `AX-G09` | `Z/A` = 0.522 | CONVENTION |
| `AX-G10` | `T = 0` for the frozen state | ASSUMPTION |
| `AX-D01` | `κρ_req = −f_xx/f` | DERIVED-COORD |
| `AX-D02` | `κj_x,req = ∂_x(f_t/f)` | DERIVED-COORD |
| `AX-D03` | `j_y = j_z = 0` | DERIVED-COVARIANT |
| `AX-D04` | `K² − K_ijK^ij = 0` | DERIVED-COVARIANT |
| `AX-D05` | `Λ = 0` | ASSUMPTION |
| `AX-D06` | `c = 1`, `G`, `ħ` unit fixing | CONVENTION |
| `AX-T01` | `Φ = −4.5` orders | DERIVED-COORD |
| `AX-T02` | `V = ε` | CONVENTION |
| `AX-T03` | the value of `ε` (`relief/pitch`) | UNVERIFIED |
| `AX-T04` | `RL-6` = `2×10⁴×` | DERIVED-COORD |
| `AX-T05` | purchasable / not-purchasable binary | CONVENTION |
| `AX-T06` | full sun `2.7740e21 m⁻²s⁻¹` at 2.25 eV | MEASURED |
| `AX-T07` | declared band 2.25 eV (visible 1.65–3.26 eV) | CONVENTION |
| `AX-L01` | effective-2D four-slot conditional | CONVENTION |
| `AX-L02` | "observation scale" (`θ` tuple) | CONVENTION |
| `AX-L03` | "frozen degrees of freedom" | ASSUMPTION |
| `AX-L04` | Kasner `f = t` as the negative control | CONVENTION |
| `AX-L05` | row 1's "none stated (geometric, convention-independent)" | UNVERIFIED |
| `AX-S01` | existence of a continuous controlled 3D→2D route | ASSUMPTION |
| `AX-S02` | adiabaticity of the smooth 2D-ization branch | ASSUMPTION |
| `AX-S03` | `L_z` as an external control parameter (no back-reaction) | ASSUMPTION |
| `AX-X01` | `C_eye = 0.01` (Weber) | CONVENTION |
| `AX-X02` | `Q3 = log₂(1 + C/C_eye)` | CONVENTION |
| `AX-X03` | `λ = 500 nm` in the `C1` optical-vacuity argument | CONVENTION |
| `AX-X04` | neglected pair-plasma back-reaction in `RL-5` | ASSUMPTION |

Predicted distribution: `MEASURED 2`, `DERIVED-COVARIANT 3`, `DERIVED-COORD 5`, `CONVENTION 15`,
`ASSUMPTION 8`, `UNVERIFIED 2` → **35**.

## 4. Predictions (numbers, not directions)

| id | prediction | kill condition |
|---|---|---|
| `AX-P1` | `total = 35`; distribution exactly as §3 | any count differs |
| `AX-P2` | `closure_errors = 0`: every parent and every blast target resolves to an audited id or a registered downstream token; every item has ≥1 chain row and ≥1 blast row | any error |
| `AX-P3` | `test_coverage = 30/30` non-covariant items carry a `C`-row; plus `3` positive controls on the covariant ones | any missing |
| `AX-P4` | `d∥ = 15.40194 fm`, `d∥/a₀ = 2.911e−4`; `RL-6` ratio at `15.402 fm = 1.948e4`, at `6.742 fm = 4.450e4`, at `L_z = 1 fm = 3.000e5` | any value differs by `> 0.5%` |
| `AX-P5` | `Φ = −4.50499`; `Q3(3.3166) = 8.37790`; `Q3` at doubled `C_eye` = `7.38223` | any differs by `> 1e−3` |
| `AX-P6` | `ΔE_z(250 nm) = 2.4797 eV`; `γ_flip = 1.1021` | either differs by `> 1e−3` |
| `AX-P7` | `V3`-identity holds: `K² − K_ijK^ij` simplifies to `0` for arbitrary `f(t,x)` | non-zero residual |
| `AX-P8` | the flat sector of the `f→0` classification is `f` affine in `(t,x)`; `f = t + εx²` gives `K = 16ε²/f² → ∞` | either statement fails |
| `AX-P9` | findings: at least the five subjects (i) `d∥`-as-thickness, (ii) "convention-independent" reverse-on, (iii) `K²−K_ijK^ij` identity, (iv) adiabaticity, (v) undeclared `Λ=0` | fewer than five |
| `AX-P10` | `OVERALL: PASS-WITH-FINDINGS` | any other verdict |

## 5. Negative controls (must fail)

| id | injection | required behaviour |
|---|---|---|
| `AX-N1` | one item with an empty label | closure reports exactly `1` unlabelled error |
| `AX-N2` | one blast target that is neither an audited id nor a registered token | closure reports exactly `1` dangling error |
| `AX-N3` | one `DERIVED-COVARIANT` item with no `C`-row | coverage reports exactly `1` missing test |
| `AX-N4` | one item whose parent list is empty | chain reports exactly `1` rootless error |

Each control is run on a deep copy of the item table; the real table is never mutated.

## 6. Result-class ceiling and prohibited actions

The maximum admissible claim is descriptive: *this is the label, the root, the tested dependence and
the blast radius of each listed premise.* Explicitly **not** claimed: physical viability, matter
survival, visibility, route adoption, gate movement, or that any label is a defect.

Prohibited, and enforced by `AX-9` in the instrument: repairing or re-sealing any existing product,
lock or ledger entry; advancing any gate, threshold, terminal class or D-state; treating a prior
`MET`/`PASS` as evidence of `DERIVED-COVARIANT`; stopping at the first derivation layer.

## 7. Provenance of the review itself

`PROVENANCE: NEITHER`. Inputs are the contract documents only: `docs/conventions/` (effective-2D
definition, dimensional conventions, constraint crosswalk), `docs/specs/relaxation_ladder_v1.md`,
`docs/decisions/G0p_seven_row_verdict_v3.md`, `reports/DCC_terminal_answer_v1.md`,
`runs/P1/phase1*_results.txt`, `docs/decisions/kinematic_vs_dynamic_unfolding_v1.md`,
`docs/specs/intrinsic_structure_tiers_v1.md`, `docs/decisions/scifi_boundary_v1.md`. No numerical
simulation is run; all arithmetic is closed-form and reproducible from the printed constants.

---

## 8. Pre-emission clarification (disclosed before the instrument was run)

**No product existed when this was appended.** `AX-P3`'s `30/30` is correct and is now stated with
its derivation, because an intermediate version of this section asserted `32/32` and was withdrawn
before any run.

Directive §7 requires a documented test for `DERIVED-COORD`, `CONVENTION`, `ASSUMPTION` and
`UNVERIFIED` items. From §3 that is `5 + 15 + 8 + 2 = 30` items. The two `MEASURED` items (`a₀`, the
solar flux) and the three `DERIVED-COVARIANT` items are **not** in that set: the former need a
citation, not a transformation; the latter carry a positive control instead. Hence:

| quantity | count |
|---|---|
| items requiring a `C`-row | 30 |
| `C`-rows for them | 30 |
| positive controls on `DERIVED-COVARIANT` items | 3 |
| total `C`-rows | 33 |

`AX-P1`, `AX-P2`, `AX-P4`–`AX-P10` stand as written. §3's label table was never changed.
