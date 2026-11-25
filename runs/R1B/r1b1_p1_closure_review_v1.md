# R1B1-P1 — Kinematic Closure Review v1 (round 42)

**Status**: first `R1B1-P1` theoretical product, under `runs/R1B/r1b1_p1_registration.md` (`IN PROGRESS —
THEORETICAL`). **Numerics remain vetoed** (`P1-CLOSURE-FAIL`); the only computational tool used is a CAS
algebra checker (`src/r1_dense/r1b1_p1_kinematic_check.py` → `runs/R1B/r1b1_p1_closure_check_results.txt`,
8/8 symbolic identities VERIFIED), authorized by the round-42 registration amendment — it verifies hand
derivations, it selects no solver and simulates nothing.
**Mandate** (governor, round 41): *"review whether the microscopic set of degrees of freedom and the
action in P1 can be simultaneously closed under the same B(t) geometric background, rather than writing
simulation code first."*
**Conventions fixed once**: `c = 1` (restoration mechanical); signature `(−,+,+,+)`;
`F_{0i} = E_i`, `F_{ij} = −ε_{ijk}B_k`; the `B ≡ 1` slice is the pre-compression geometry and the flat-recovery
check.

---

## §1 The answer in one line

**The DOF set and the action close simultaneously at the kinematic level under the same prescribed `B(t)`
background, for any declared weak convention.** What does not close is exactly what the interface
anticipated: the matter interaction sector (`P1-C`), the electron z-disposition (`UNRESOLVED` per spec
§3.2), and the internal-nuclear-DOF question. Partial closure is achieved; `P1-C` is the remaining gate.

## §2 The checked identities

| id | result | check |
|---|---|---|
| `R1` | only two independent Christoffel symbols: `Γ^t_zz = BḂ`, `Γ^z_tz = Ḃ/B` | results file §R1 |
| `R2` | `∇_μT^{μt} = ∂_tρ + (Ḃ/B)(ρ + p_z)` (homogeneous): **only `p_z` couples** — the x,y stresses do not enter, their scale factors are static | §R2a, §R2b |
| `R3` | **`B-WORK-TERM`: `dE/dt = −Ḃ·p_z` per unit lateral area = `−(Ḃ/B)∫√h T^zz d³x`** — the geometry compresses z like a piston; in-plane stresses do no work | §R3, §R3b |
| `R4` | Maxwell: homogeneous pair metric-independent (`dF = 0`); inhomogeneous pair carries the `B`-weights; `B ≡ 1` recovers canonical flat Maxwell, all four components | §R4 |
| `R5` | scalar probe: `□_Bφ = −φ̈ − (Ḃ/B)φ̇ + ∇_⊥²φ + φ_zz/B²` — every field feels (i) `1/B²` z-weights and (ii) the `Ḃ/B` friction | §R5 |
| `R6` | `(1/√−g)∂_μ(√−g J^μ) ≡ ∇_μJ^μ`: internal `U(1)` charges (electric, baryon) are conserved on the background exactly as in flat space — `B(t)` does not couple to phases | §R6 |

Two derived structural effects beyond the planned checks, both printed in the results file:

- **transverse EM damping** (`G^x`, `G^y`): the transverse Ampère equation acquires a `−(Ḃ/B)E_⊥` term —
  during compression, transverse electric fields decay at rate `Ḃ/B` with the measure. Derived, not
  assumed; relevant to Phase 3's non-adiabatic EM response and eventually to the state that feeds the
  optics line.
- **z-sector weights**: `∂_z(E_z/B)` in Gauss and `1/B²` on `∂_zB_⊥` — the z-flux dilution the record's
  fixed-area bookkeeping must eventually respect.

## §3 The governor's three check-items (round-41 ruling §IV), addressed

**1. Energy-momentum under an external `B(t)`.** Both forms are now *derived*, and their coexistence is
stated so they cannot be mixed:

- local covariant form: `∇_μT^{μν} = F^{νλ}J_λ` **exactly** — no local `S^ν` term; the background enters
  through the connection (`Γ^t_zz = BḂ`, `Γ^z_tz = Ḃ/B`);
- coordinate-split form (the governor's notation): `∂_μT^{μt} = F^{tλ}J_λ − (Ḃ/B)(ρ + p_z)`, i.e.
  **`S^t_bg = −(Ḃ/B)(ρ + p_z)`** — derived from the connection and the measure, never assumed zero, and
  integrating to the `B-WORK-TERM`.

Checks: `Ḃ = 0 ⇒ dE/dt = 0` (static anisotropy conserves energy); `B ≡ 1 ⇒` flat conservation. **The
declared branch for `R1-B1` is external-`B(t)`** — the DCC front is the programme's prescribed mechanism,
and the endogenous-realization question belongs to `G3′`/`R2-D L3` (roadmap v1.4: "only when L3 is
completed can one judge whether the target `B(t)` can be realized endogenously by the specified action").
The dynamical-`B` variant is recorded as a fork that changes the conservation statements (adds `B`'s own
DOF: total energy-momentum conserved, the matter subsystem's not) — not exercised in this line.

**2. Nuclear interactions ↔ DOF consistency.** The kinematic sector treats baryons as structureless —
**declared as an approximation, not an assumption**: its adequacy at `0.13–0.26 n₀` is itself a Phase-2
output, and `P1-C`'s applicability fields (density interval, energy range, many-body corrections, known
errors) gate any effective-nucleon description. If internal nuclear DOF must be explicit, nucleons stop
being structureless and the associated errors enter the declaration.

**3. Integrated-out DOF — the expanded checklist.** Veto item 7 is now a **five-point EFT review**
(spec §15.3 amendment, round 42): energy and stress contributions · effective corrections to current
operators · effective interactions · conservation laws and Ward identities · optical spectral weights
with high-energy compensation. **An `f`-sum compensating term alone does not close an incomplete
low-energy theory** — the record's own `THREE-OMEGA-G`, `V-F-IMPLIED`, and `G-SPLIT` are the three
recorded costs of skipping pieces of exactly this list.

## §4 `P1-A` status — the DOF set

| DOF | kinematic closure | gate |
|---|---|---|
| electrons (Dirac) | closed at structure: charge conserved (`R6`), `Ĵ = qψ̄γ^μψ` from gauge coupling, Ward transversality carries over | z-disposition `UNRESOLVED` (spec §3.2, re-scoped); interaction corrections → `P1-C` |
| baryons (heavy, structureless *declared approximation*) | closed at structure: baryon number conserved (`R6`) | internal-nuclear-DOF question → `P1-C`; adequacy → Phase 2 |
| EM field | **fully closed kinematically** (`R4`, including the damping and z-weights) | none at this level |
| neutrinos | fork: weak-off — absent, electron number conserved; weak-on — either dynamical (lepton number conserved) or free-escape (declared loss channel; the ν budget remains a non-citable placeholder, verdict v3 §5) | **the fork must be declared before the conservation derivation is finalized**; both branches close kinematically |

## §5 Verdict

| closure item | verdict | evidence |
|---|---|---|
| kinematic Maxwell on `B(t)` | **CLOSED** | `R4`, 8/8 checks |
| `Ĵ` (kinematic fields) | **CLOSED** at structure (interaction corrections → `P1-C`) | `R6` |
| `T^μν` + the exchange term | **CLOSED** | `R2`, `R3` |
| charge & baryon conservation | **CLOSED** | `R6` |
| energy ledger (external `B(t)`) | **CLOSED** | `B-WORK-TERM` (`R3`) |
| electron-number conservation | **CONDITIONAL** — weak fork to be declared | §4 |
| matter interaction sector | **NOT CLOSED** — `P1-C` gate, `UNRESOLVED` admissible | spec §15.2 |
| electron z-disposition | **NOT CLOSED** — `UNRESOLVED` declared, substitution mechanisms re-opened | spec §3.2 |
| internal nuclear DOF | **NOT CLOSED** — `P1-C` | spec §15.2 |
| `Ḃ` non-adiabatic couplings | **structure CLOSED** (friction + EM damping derived); transition rates → Phase 3 | `R5`, §2 |

This is the honest partial-closure state: **no veto condition fires at the kinematic level, and none of
the closed items was obtained by assumption** — the exchange term the interface required to be "derived,
not assumed zero" is now a checked identity.

## §6 Consequence for the optics line (`N7-SPLIT` carried through)

The record's `W_total = πe²n_2D/2m*` is a *baseline-model* quantity. Under `R1-B1`, the f-sum budget is
per-model (spec §10), and the Drude weight is a functional of the **participating** degrees of freedom —
`n_free,2D` — never of the total-charge bookkeeping `n_Q,2D` or of the baryon column `N_B`. The old
`n_2D` may not be inherited as a definitive optical input (governor round-41 §II; report §7.6 amended
this round).

## §7 What `P1` does next

1. `P1-A`: declare the weak-convention fork; state the electron z-disposition treatment (or its
   `UNRESOLVED` dependency, named).
2. `P1-B`: remaining derivation deliverable — the Dirac operator on this background with declared
   conventions (spin connection, the `Ḃ`-coupling in the z-sector, `Ĵ^μ` and `T^μν` for the declared
   fields, interaction-correction slots reserved for `P1-C`).
3. `P1-C`: the interaction-model declaration — the gate on which closure completes or `UNRESOLVED` is
   the recorded outcome.

Numerics remain vetoed throughout.

---

## §8 Round-43 amendments — the governor's round-42 qualifications, recorded

The governor accepts the round-42 derivations **under their specified conditions** and separates two
levels that must never be conflated: **kinematic closure ≠ dynamical closure**. The ruling table:

| item | ruling |
|---|---|
| background geometric kinematics | Passed |
| anisotropic fluid conservation structure | Passed |
| `B-WORK-TERM` | Passed |
| Maxwell geometric structure | symbolic check passed |
| microscopic Dirac operator | Incomplete → advanced in round 43 (`r1b1_p1_dirac_closure_v1.md`, 11/11) |
| nuclear interaction closure | Incomplete (`P1-C` gate) |
| full microscopic action closure | Incomplete |
| **overall** | **kinematic closure passed; dynamical closure not yet ruled** |

Qualifications recorded and implemented:

1. **`B-WORK-TERM` normalization (governor §I).** The energy per unit lateral area over a coordinate
   slice of thickness `Δz` is `E_area(Δz) = B·Δz·ρ`; round 42's `dE/dt = −Ḃ·p_z` is the `Δz = 1`
   coordinate-slice case. The general statement is `dE_area/dt = −Ḃ·p_z·Δz`; the integration
   normalization is now explicit, not hidden.
2. **The exchange-term status (governor §II).** `S^t_bg = −(Ḃ/B)(ρ + p_z)` is the connection/measure
   contribution *moved to the RHS of the coordinate energy equation* — **not an independent physical
   source added to the action**. And: with `∂_tg_μν ≠ 0` there is no time-translation Killing symmetry,
   hence no conserved Killing energy: **an externally prescribed `B(t)` provides or absorbs energy
   to/from matter and the EM field; local covariant conservation is not coordinate-energy conservation
   of the matter subsystem.** Elevated to spec §5 (this round).
3. **Transverse EM damping — not dissipation (governor §III).** The `−(Ḃ/B)E_⊥` term is geometrically
   induced redshift/dilution/mixing — **not** resistive dissipation, electron scattering, current
   relaxation, or absorption-weight transfer. Frame caveat: `E_⊥` in that equation is a
   *coordinate component*; Phase 3 must track local **orthonormal-frame** fields (spec §8 amendment).
   Round-43 refinement: the Dirac-sector analogue is the identity term `−(I/2)(Ḃ/B)𝟙` — likewise
   measure compensation, not dissipation; and `p_z` remains a good quantum number (`[H_D, p_z] = 0`),
   so round 42's "Ḃ drives transitions between z-modes" is superseded by: the non-adiabatic content is
   the explicitly time-dependent `1/B(t)` mode weights, not mode mixing.
4. **`R6` conditions (governor §IV).** Conservation statements carry their conditions:

   | quantity | status |
   |---|---|
   | total electric charge | conserved — gauge symmetry |
   | total baryon number | conserved **iff the adopted theory contains no baryon-number-violating processes** (a `P1-C` declaration) |
   | electron number | not necessarily — weak convention |
   | free electron number | not conserved — capture/release/transfer (`N7-SPLIT`) |

   `R6` is not conservation of all particle species and carrier numbers.

5. **Next step as ruled**: only the Dirac operator and the variational consistency of the same action —
   executed this round (`r1b1_p1_dirac_closure_v1.md`); no simulation code, no EOS, no conductivity;
   the numerical veto is not lifted.

*Content generated by AI*
