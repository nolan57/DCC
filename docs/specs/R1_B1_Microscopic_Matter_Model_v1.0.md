# R1-B1 — Microscopic Matter Model Specification v1.1 (Phase 0)

**Status**: `ACTIVE — PHASE 0 SPEC`. Theory specification only: **no numerical simulation is in scope**
until Phase 1 is separately registered. This document defines the object, the contracts, the acceptance
classes and the falsification conditions of R1-B1; it computes almost nothing, and everything it states
is either cited from the record or tagged.
**Trigger**: `docs/R1B1.md` (governor directive, round 40): R1-B1 is a **multi-layer physical model
derived from microscopic degrees of freedom** — not a 2D Drude model whose parameters are fitted until
they pass `S4`/`S5`. Two questions that cannot substitute for each other: (i) does a stable or
quasi-stable 2D-ified matter state exist under the DCC evolution; (ii) if so, what current response
follows from that state.
**Authority**: none beyond the record. Where this spec and the record disagree, the record wins.
**Predecessors**: roadmap v1.4 §8 (R1-A / R1-B dual track), `docs/decisions/G0p_seven_row_verdict_v3.md`
(rows 1–7, frozen baseline, ledger discipline, scope-of-validity), `runs/R1B/r1b1_eos_results.txt` (v2,
MODEL RESULT) and `runs/R1B/r1b1_eos_v3_results.txt` (three-convention envelope),
`docs/specs/surface_conductivity_v1.md` v1.3 (`S1`–`S15`), `docs/decisions/sc4_partition_citation_errata_v1.md`
(`E5`, the traceability rule).

> **Version note — v1.1 (round 41, governor review of Phase 0).** Phase 0's specification structure is
> accepted; four physical boundaries are fixed before `R1B1-P1` registration. **(1)** §2.3/§6: the
> **registration baseline** (`L_z = 1.0 fm`, reproduction of predecessor EOS only) is separated from the
> **`K1` valid computational domain** (`L_z ∈ [1.68, 1.99] fm`, where physical interpretation is
> permitted); the density figure is renamed a *reference interval*, not a phase assertion. **(2)** §3.2:
> the z-confinement conclusion is re-scoped — an energy-scale comparison refutes the *registered
> strictly-confined model under its boundary conditions*; it does not prove the nonexistence of
> electronic degrees of freedom. `πħc/L_z` is boundary-condition-specific; the `πa₀` and `L_z*`
> agreements are cross-checks of the formula's implementation, not proofs of its fm-scale applicability.
> **(3)** §4: `n_2D` is split into `n_Q,2D` (total charge) and `n_free,2D` (free carriers) with
> trapped/bound/ionized components registered separately; `N7` becomes a constraint *solved from the
> microscopic state*, never a pre-assigned fraction. **(4)** §0.3: the R1-B1 line adopts a closed symbol
> table; `d_par`/`d_∥` are deprecated inside R1-B1 documents. **§15 is new**: the `R1B1-P1` interface —
> three acceptance tiers, the `P1-CLOSURE-FAIL` veto, three admissible outcomes. No v1.0 threshold was
> moved; the criteria were sharpened.

---

## §0 Reading rules

### 0.1 What Phase 0 decides and what it refuses to decide

Phase 0 fixes: the physical object, the geometric input protocol, the degree-of-freedom inventory with
its evidence status, the conservation bookkeeping, the action-level contracts, the six stability
acceptance classes, the response-derivation chain, and the falsification conditions. Phase 0 does **not**
decide whether the state exists — that is Phase 2's outcome, and a NO-GO there is a valid physical
conclusion (§14), not a project failure.

**Phase 0 acceptance criterion** (`docs/R1B1.md` §7 Phase 0): *no unargued material parameters,
degeneracies, effective masses, or carrier-composition assumptions.* Every quantity in this document
therefore carries exactly one source tag:

| tag | meaning |
|---|---|
| `DERIVED` | obtained from microscopic equations of this programme, derivation shown or cited |
| `MEASURED` | independent empirical value (external physics) |
| `ASSUMED` | an input assumption not yet verified — must be either proven or discharged by a later phase |
| `FITTED` | a fitted parameter — admissible only inside its declared fit domain |
| `UNRESOLVED` | currently undeterminable; an honest `UNRESOLVED` is always preferred to a forced value |

The tags exist because of `E5` (`sc4_partition_citation_errata_v1.md` §7): the current module's
`f_intra = 1` was a construction input that masqueraded as a measured physical quantity. From day one,
R1-B1's outputs are tagged so that this failure class cannot recur silently. A tag may change only by a
recorded re-derivation, never by relabelling.

### 0.2 Label discipline (new namespaces)

This spec introduces three namespaces; the registry carries them. They must never be used bare:

- **`R1B1-P0` … `R1B1-P5`** — the six phases of §13. Qualified because bare `P0`–`P4` are Layer-A
  numerical stages (report §2).
- **`S-STATE-1` … `S-STATE-6`** — the stability acceptance classes of §7. Qualified because this is the
  **fourth** live `S` family (spec `S1`–`S15`, registry rules `S1`–`S10`, scene stages `S0`–`S4`).
- **`SRC-TAG`** — the five source tags of §0.1.

### 0.3 Symbol table for the R1-B1 line (binding from `R1B1-P1`)

Object confusion among `6.7420 fm`, `15.40 fm` and the `K1` window is fixed at the symbol level, not by
prose (governor review, round 41):

| symbol | quantity | unit | note |
|---|---|---|---|
| `d_carrier` | mean carrier areal spacing | fm | adopts (renames) the baseline's `d_par = 6.7420 fm` |
| `d_nuc` | nuclear cell characteristic length | fm | adopts (renames) the baseline's `d_∥ = 15.40 fm` |
| `L_z` | z-direction intrinsic thickness | fm | unchanged; the Phase-2 scan variable (§2.3 role B) |
| `B(t)` | z-direction coordinate scale factor | dimensionless | unchanged; geometric input (§2.1) |
| `n_B` | baryon number density of the 3D reconstruction | fm⁻³ | unchanged |
| `N_B` | baryon areal density | fm⁻² | unchanged |
| `n_Q,2D` | total charge areal density | one convention per product, declared | new (§4.2) |
| `n_free,2D` | free-carrier areal density | same convention | new (§4.2); never assumed equal to `n_Q,2D` |

`d_par` and `d_∥` remain the *record's* baseline labels — citable only with their
`G0p_seven_row_verdict_v3.md` §2 definitions — and are **deprecated inside R1-B1 documents**.

---

## §1 Objective and scope

### 1.1 The two questions

1. **Matter question** — under the DCC geometric evolution, what happens to the original particles,
   bound states and interactions? Can a new low-dimensional stable state form?
2. **Response question** — if such a state exists, what are its bands, carriers, scattering and current
   response? Can a spectrally finite, causally self-consistent `σ_s(ω)` be derived from it?

Question (i) unsolved ⇒ question (ii) has no legitimate material input. R1-B1 therefore **cannot start
from the four numbers** `(n_2D, g, v_F, ω_end)` and fit. The derivation order is fixed:
`H → Ĵ → Π^R → σ(ω) → W_total` (`docs/R1B1.md` §5.1; optics `FSUM-SINGLE-SOURCE`).

### 1.2 Branches — none may be presupposed

| branch | physical meaning | R1-B1 must answer | inherited status |
|---|---|---|---|
| A | original structure partially or fully retained | can atoms/nuclei/electronic structure be stable in the new geometry? | row 1 is **NO-GO** for the *original* network at fixed area (`G0p_seven_row_verdict_v3.md` row 1) — branch A survives only in weakened forms |
| B | original structure fails; a new state forms | do new bound states, collective states or low-dim condensates exist? | row 2 **OPEN** (three-convention envelope, not a state) |
| C | no stable end state | dissociation, particle escape, or continuous energy dissipation? | row 5 **OPEN** (`R1-B2` v3 UNDECIDED) |
| D | other non-equilibrium / quasi-stable states | finite lifetime, non-equilibrium, spatial inhomogeneity? | row 5 **OPEN**; `R1-B3` provides a reference timescale only |

Branch B is **not** the default target; C and D must be honestly retained (`docs/R1B1.md` §1.1; roadmap
v1.4 prohibition ③ — no sector's assignment in the four-category classification may be presupposed).
The `G0′` gate explicitly may not be used to reject the geometric branch, the dense-state branch, or the
effective-2D theory branch (report §5.2).

### 1.3 What this spec inherits, and how it may be cited

Per `G0p_seven_row_verdict_v3.md` §5: frozen-baseline values **may be cited, marked `MODEL RESULT`**;
β-equilibrium quantities (`X_p`, `μ_e`, `n_e`, `P`) **must be cited as the three-convention envelope**
(ALL3D / HYB / ALL2D — roadmap v1.4; single-convention single points are forbidden); the `ν` energy-loss
placeholder, `Γ_i`, and crystal-phase conclusions **must not be cited** (placeholder / revoked /
UNDECIDED). This spec adopts those rules verbatim for everything downstream of it.

---

## §2 DCC metric and evolution protocol (Layer 0)

### 2.1 The geometric input

Under the current DCC convention the intrinsic length along z is `dℓ_z = B(t) dz`, with the minimal
spatial metric

```
ds² = −c²dt² + dx² + dy² + B²(t) dz²
```

`B(t)` is **geometric input, not a fitted quantity** (`docs/R1B1.md` §1.2). The same final thickness does
not guarantee the same final state: fast and quasi-static compression traverse different non-equilibrium
paths — path dependence is a required Phase-3 output, not a nuisance parameter.

### 2.2 Layer-0 declaration checklist and its current status

| item | status | basis |
|---|---|---|
| `B(t)` evolution path | `UNRESOLVED` | only the total-duration bound is recorded: the conversion clock `t_rip = √2 L/c` is an **identity** (`Λ_max` retired; reflected channel has zero exposure budget — report §5.4) |
| compression rate / timescale | `UNRESOLVED`, with a recorded warning | `K5`: neutronisation `2.96 ns` ≈ expansion `4.72 ns` ≈ sound crossing `0.33 ns` — **no scale separation** (report §5.3); the quasi-static branch may not exist |
| lateral boundary conditions | `UNRESOLVED` — declared in Phase 1 | fixed projected area (`C1`/`H2`) is at best an initial condition unless a constraint stress of order `10¹⁷ N/m` exists (roadmap v1.4: the β-equilibrium final-state stress requirement is `1.8–6.5×10¹⁶ N/m`, envelope `P_tot`) |
| initial composition and total particle number | `ASSUMED` (baseline convention) | baryon column `N_B = n_2D/Z_A = 0.04216 fm⁻²` and charge fraction `Z_A = 0.522` (`G0p_seven_row_verdict_v3.md` §2); effective `A ≈ N_B/N_s ≈ 10` nucleons per nucleus — composition behind `Z_A`, `A` is an assumption Phase 2 must discharge |
| energy / momentum / external-constraint inputs | `UNRESOLVED` | row 6's NO-GO is conditioned on frozen ideal-gas pressure with `P_constraint = 0`; scenario W hardens `K2` — the electrostatic well available is `4–50 keV`, three orders below `E_F`, so **no known force can be the constraining agent** (report §5.3) |
| geometry-to-matter work and energy exchange | `UNRESOLVED`, with a recorded conflict | `K4`: constraint zero-point energy is `12.7×` the in-plane degeneracy energy (electrons) — the ledger must close, and this conflict must be resolved or reproduced by the model |

### 2.3 Scale referents — pinned, because they are three different quantities

`docs/R1B1.md` §2.3 calls `6.7420 fm` the "target thickness". In the record that number is the **carrier
spacing**, not a thickness (this is exactly the `E1` mixing class — report §10.2). The three referents:

| quantity | value | what it is | source |
|---|---|---|---|
| `L_z` | window `[1.68, 1.99] fm` | the layer **thickness** window in which eff-2D holds (only `1.19×` wide; the registered `1 fm` is thinner than a nucleon `1.68 fm` — conflict `K1`) | `K1` (report §5.3) |
| `d_par` | `6.7420 fm` | **carrier spacing** `1/√n_2D`, v3 baseline | verdict v3 §2 |
| `d_∥` | `15.40 fm` | **nuclear cell** `1/√N_s`, the `C1` cell | verdict v3 §2 |

All three are fm-scale, so every conclusion below that rests on "the endpoint is fm-scale, 4–5 orders
below the atomic scale `π a₀ = 1.66 Å`" is robust across all three referents.

**The two roles of `L_z` are separated (v1.1).** **(A) Registration baseline** — `L_z = 1.0 fm` with
`n_B = 0.04216 fm⁻³` is the fixed parameter set on which predecessor EOS calculations are reproduced
(`runs/R1B/r1b1_eos_results.txt:6,8`); it carries no physical-interpretation privilege outside its own
basis. **(B) Valid computational domain** — the `K1` window `[1.68, 1.99] fm` is where the eff-2D
criterion permits physical interpretation (`K1` flags the registered `1 fm` as thinner than a nucleon).
EOS results at the basis do not automatically describe the state in the window: the Phase-2 scan runs
over **(B)**, with **(A)** serving reproduction and cross-checks only. `1.0 fm` is never the sole
thickness.

---

## §3 Microscopic degrees of freedom — the central question

> The hardest part of R1-B1 (`docs/R1B1.md` §2.3): **determine which physical degrees of freedom still
> exist at the endpoint scale.** Ordinary atoms, molecules, orbitals, cross-sections and material
> parameters may not be carried past the point where their bound states cease.

### 3.1 The density regime

`DERIVED` (formula shown, from record values): baryon column `N_B = 0.04216 fm⁻²`, so the endpoint 3D
baryon density is `n_B(L_z) = N_B/L_z`:

| `L_z` | `n_B` [fm⁻³] | in units of `n₀ = 0.16 fm⁻³` (`MEASURED`, nuclear saturation) |
|---|---|---|
| `1.0 fm` (EOS basis) | `0.04216` | `0.26 n₀` |
| `1.68–1.99 fm` (`K1` window) | `0.0212 – 0.0251` | `0.13 – 0.16 n₀` |

The interval `n_B/n₀ = 0.13–0.26` is a **sub-saturation density reference interval** — `DERIVED`
arithmetic, `UNRESOLVED` physics. Density alone does not assert a phase: whether the matter forms any
neutron-star-crust-like phase — composition, proton fraction, electron chemical potential, nuclear
structure, interactions — is exactly what Phase 2 must solve. Crust physics is the **reference class for
candidate interactions and EOS forms** (the roadmap demands reproducing crust `μ_e`–`ρ` endpoints,
roadmap v1.4 §8), not a verdict about the state. It is **not** condensed matter, and **not**
above-nuclear density; the candidate theory classes are nuclear + leptonic + field physics.

### 3.2 The electron z-degree of freedom

`DERIVED` (order of magnitude, formulas shown). **Under the registered strictly-confined z-direction
assumption and its boundary conditions**, for relativistic carriers (`μ_e` up to `24.96 MeV ≫ m_e c²`),
the z-confinement scale is `E_z ≈ πħc/L_z` — a characteristic momentum scale under *particular* boundary
conditions, **not** a universal minimum-energy formula for all confinement problems:

| `L_z` | `E_z` | reference |
|---|---|---|
| `1.68 – 1.99 fm` | `311 – 369 MeV` | ≳ `12×` the envelope `μ_e` max (`24.96 MeV`) |
| `≈ 72 fm` | `≈ 73 MeV` | non-relativistic form `E_z = π²(ħc)²/(2 m_e c² L_z²)` crosses the baseline `E_F = 73.37 MeV` here |
| `π a₀ = 1.66 Å` | `≈ 13.6 eV` | cross-check of the formula's numerical implementation — matches row 1's `L_z^ion = 1.66 Å` ionization scale exactly |

**Re-scoped conclusion (v1.1).** Under the registered strictly-confined z-direction assumption and its
boundary conditions, the minimum electronic confinement energy (`311–369 MeV`) significantly exceeds the
current electron chemical-potential envelope (`≤ 24.96 MeV`). This confinement model is **incompatible
with the `K1` conditions** — but an energy-scale comparison does **not** prove that no electronic degree
of freedom exists: the true statement depends on the z boundary conditions, the allowed wavefunction
modes, whether a confining potential is present, whether electrons can escape along z, and whether other
particles or collective degrees of freedom substitute for the original carriers. **The z-direction
degrees of freedom of the electrons, together with their substitution mechanisms, are therefore
re-examined in Phases 1–2** (`UNRESOLVED`, the Phase-1/2 exit criterion). The candidate dispositions
remain: strictly confined 2D (whose zero-point cost must be paid — `K4`'s `12.7×` conflict), free or
escaping in z (charge separation ⇒ electrostatic fields — `K2`'s `4.7×10⁵` Schwinger scale if
unshielded), or trapped in a new configuration.

The agreements `L_z* ≈ 71.6 fm` with the baseline `E_F` and `E_z(πa₀) = 13.65 eV` with row 1's
ionization scale are **cross-checks of the formula's numerical implementation and internal consistency** —
they do not independently prove the physical applicability of that formula at the fm scale.

### 3.3 The inventory

| DOF | physics it must describe | status at the endpoint |
|---|---|---|
| electrons | spectrum, occupation, capture, escape, interactions | strict z-confinement refuted as a carrier model under its boundary conditions (§3.2, re-scoped v1.1); actual z-disposition and substitution mechanisms `UNRESOLVED`; carrier census is `N7`'s business (§4) |
| nuclei / nucleons | nuclear structure, inter-nucleon interaction, reactions | at `0.13–0.26 n₀`; under weak-on, β-equilibrium demands `>91%` neutronisation in all three conventions (`K6`); the *atomic* network is ruled out by row 1's NO-GO, but survival of bare nuclei/ions under the weak-off convention (where `K6` vanishes) is `UNRESOLVED` |
| electromagnetic field | charge interactions, screening, collective response | survives as a fundamental field; its effective form (static/dynamic screening, `q_TF`) is a Phase-4 output — `UNRESOLVED` |
| bound states | atomic/molecular/ionic or new low-dim bound states | atomic/molecular ruled out (row 1; §3.2); new ionic/collective bound states are branch-B candidates — `UNRESOLVED` (`R1-B2` v3 UNDECIDED) |
| collective DOF | density waves, condensates, polarization | `UNRESOLVED` |
| geometric DOF | coupling of DCC scale change to matter stress | `B(t)` prescribed (§2); the *back-reaction* (can the specified action realize `B(t)` endogenously) is `G3′`'s question, out of R1-B1 scope but its stress demand (`1.8–6.5×10¹⁶ N/m`) is R1-B1's EOS output |

Not every DOF will remain explicit in the final computation — but which are integrated out, and how their
spectral weight is carried, must be justified (§10's UV-completeness clause), never assumed.

---

## §4 Conserved quantities and N7

### 4.1 What is conserved, by convention

| quantity | conservation status | tag |
|---|---|---|
| baryon number `N_B` | conserved (strong processes conserve baryon number in both weak conventions) | `DERIVED`, convention-independent |
| electric charge `Q_total` | conserved exactly (gauge law) | `DERIVED`, convention-independent |
| electron number `N_e` | conserved **iff weak-off** (scenario W); under weak-on, β-processes `n ↔ p + e⁻ + ν̄_e` convert it | convention-dependent |
| lepton number | conserved iff neutrinos trapped; not conserved if they escape freely | `UNRESOLVED` (escape timescale vs compression clock is a Phase-2/3 computation; `K5` warns no scale separation) |
| ν energy budget | registered placeholder — **not citable** (verdict v3 §5) | `UNRESOLVED` |

### 4.2 N7 — charge is not a carrier census

`N7` is quantified in the record: the frozen 3D electron gas at the EOS basis has `μ_e,frozen = 171.07
MeV`, while β-equilibrium at the same density gives `μ_e = 24.96 MeV` with `n_e` reduced by `≈ 3.1×10²`
— **captured and reduced, not eliminated** (`runs/R1B/r1b1_eos_results.txt:32-34,44`; roadmap N7:
`μ_e = 73.4 MeV` exceeds every nuclide's capture threshold — p `0.782` … C `13.37 MeV` — so the final
state is not a cold degenerate electron gas). Conserving total electron number does not determine the
carrier state.

**The `n_2D` split (v1.1).** Two areal densities are defined **separately**: **`n_Q,2D`** — total charge
areal density, the bookkeeping quantity `Z_A·N_B` — and **`n_free,2D`** — free-carrier areal density, the
quantity that actually participates in the current response. Trapped, bound and ionized components are
registered in their own rows. In general `n_Q,2D ≠ n_free,2D`, and the optical Drude weight is a
functional of the degrees of freedom that actually participate, not of a total-charge proxy.
Conservation of total charge is **not** conservation of free electron number: free electrons can be
trapped, released, or transferred into other degrees of freedom at fixed total charge. **`N7` is
ultimately a constraint obtained by solving the microscopic state — never a pre-assigned free-carrier
fraction.**

The Phase-2 output must be the full census: free carriers · bound electrons · trapped electrons · other
charged particles · reaction-participating species (`docs/R1B1.md` §3.1) — the composition table, **not
a single `n_2D`**.

### 4.3 The frozen baseline, re-classified — what R1-B1 may and may not start from

This table is the operational meaning of "R1-B1 does not start by fitting `(n_2D, g, v_F, ω_end)`":

| baseline quantity | value | re-classified status for R1-B1 |
|---|---|---|
| `N_s` | `4.2155e27 m⁻²` | bookkeeping — nuclei column, `C1` cell; `DERIVED` (defining) |
| `N_B` | `0.04216 fm⁻²` | bookkeeping — baryon column; `DERIVED` (`n_2D/Z_A`); the `N_s`/`N_B` 10× distinction is the record's own NEGCTRL and a standing trap |
| `Z_A = 0.522`, `A ≈ 10` | — | `ASSUMED` composition of the baseline; Phase 2 must discharge or revise |
| `n_2D = 2.20049e28 m⁻²` | "carrier density" | **two quantities in one slot**, now split (§4.2): `n_Q,2D = Z_A·N_B` (bookkeeping, `DERIVED`) vs `n_free,2D` (`UNRESOLVED`, an output of Phases 2/4). The baseline assumed the two equal — that assumption is exactly `N7`'s target |
| `k_F = 0.371834 fm⁻¹`, `E_F = 73.37 MeV` | — | `DERIVED` *within the baseline model* (free 2D gas, `g = 2`, `v_F = c`); superseded by Phase-4 outputs; row 7: the frozen state is **not** the ground state at that density |
| `g = 2` | — | `ASSUMED` spin degeneracy; the participating `g` is a Phase-4 output, consistent in four places (`S15`; `G-SPLIT` is the recorded cost of getting this wrong) |
| `v_F = c` | implied by `E_F = ħk_F c` | `ASSUMED` (`V-F-IMPLIED`: the record *is* a `v_F = c` Dirac model and never said so); Phase 4 outputs the real dispersion derivative or reports that no single `v_F` exists |
| `u_2D`, `P_2D`, `c_s` | `1.7245e17 J/m²`, `8.6227e16 N/m`, `c/√2` | `DERIVED` within the baseline UR gas; superseded by the Phase-2 EOS (`F-R1B1-6`: the final-state EOS "remains model-level and is not frozen") |
| `ω_end` | does not exist in the record | `UNRESOLVED`; bare `ω_end` is forbidden (`S14`), and `440.18 MeV` as an input is forbidden (`THREE-OMEGA-G`) |
| `f_intra` | `1` (module construction) | **forbidden as input** — it is the module's own construction identity (`E5`; measured partition `W_intra/W_total = 1.000000000003` is a property of that construction, not of matter) |

---

## §5 Microscopic Hamiltonian / action (Layer 1 contract)

The formal starting point (`docs/R1B1.md` §2.2):

```
S = S_matter + S_EM + S_interaction,
S_matter = ∫ d⁴x √(−g) ℒ_matter(ψ, g_μν),   S_EM = −(1/4μ₀) ∫ d⁴x √(−g) F_μν F^μν
```

on the §2 metric (flat, with `B²(t) dz²`). Contracts:

1. `ψ` is the *actual selected* set of §3 DOF — selected by the §3 evidence, not by convenience.
2. The interaction sector is built from the physics that survives at `0.13–0.26 n₀` (nuclear + leptonic
   + EM). Ordinary condensed-matter effective parameters (effective masses, band structures, 2DEG
   parameters) may **not** be imported unargued — roadmap prohibition ①②; the Phase-0 acceptance
   criterion.
3. `B(t)` coupling: the geometric background does work on matter; the energy ledger must close (the `K4`
   conflict is the recorded warning). If `B(t)` is external, energy input/output is part of the contract,
   not an afterthought. **Explicit conclusion (round 43, governor):** an externally prescribed `B(t)` can
   provide or absorb energy to/from matter and the EM field — with `∂_t g_μν ≠ 0` there is no
   time-translation Killing symmetry and hence no conserved Killing energy: **local covariant
   conservation is not coordinate-energy conservation of the matter subsystem.** The exchange figure
   `S^t_bg = −(Ḃ/B)(ρ + p_z)` is the connection/measure contribution *moved to the RHS of the coordinate
   energy equation* — **not an independent physical source added to the action** (`B-WORK-TERM`,
   `runs/R1B/r1b1_p1_closure_review_v1.md` §8; the round-43 Dirac-sector analogue is the identity term
   `−(I/2)(Ḃ/B)𝟙`, `r1b1_p1_dirac_closure_v1.md`).
4. From the same action: matter equations of motion, Maxwell equations, the **current operator**
   `Ĵ = −δS/δA` (§9), the energy-momentum tensor, and the particle-number/charge conservation laws. These
   five derivations are Phase 1's deliverable.
5. **UV-completeness clause.** If an effective low-energy model is used anywhere, its applicable energy
   domain and the fate of the integrated-out high-energy spectral weight must be declared and accounted
   (§10). The three recorded costs of skipping this are `THREE-OMEGA-G` (a bare `ω_end` that was a
   budget identity), `V-F-IMPLIED` (an undeclared `v_F = c`), and `G-SPLIT` (two `g`s in one module). An
   isolated, infinitely-extended Dirac cone is not a material f-sum model without high-energy
   completion (`docs/R1B1.md` §5.1).

---

## §6 Equilibrium state and EOS (Layer 2, Phase `R1B1-P2`)

**Static problem.** For each fixed `B` (equivalently each `L_z` in a declared scan that includes the
`K1` window and the EOS basis), solve `δE/δΨ = 0` under the §4 conservation constraints and the declared
weak convention; the same energy functional yields the stress. **Stress is forward-computed from the
microscopic state — an assigned pressure may not be used to declare stability** (`docs/R1B1.md` §3.2;
row 6's NO-GO is model-conditioned, not a free parameter).

**Inheritance.** The predecessor EOS (cold ideal npe gas, `MODEL RESULT`) produced the three-convention
envelope `X_p ∈ [1.62e-3, 4.50e-2]`, `μ_e ∈ [6.73, 24.96] MeV`, `P_tot ∈ [1.84e16, 6.48e16] N/m`, plus
the lower-density bound `n_thr` (`6.15e-6` HYB / `6.82e-6` ALL2D fm⁻³; no such bound in 3D). `R1B1-P2`
must reproduce-or-revise this **convention by convention**, under the envelope citation rule (§1.3).
Reproduction at the registration baseline (`L_z = 1.0 fm`, §2.3 role **A**) and interpretation inside the
`K1` domain (role **B**) are separate acts: the envelope is inherited from **A** and re-derived across
**B**, never transplanted.

**Outputs.** complete particle census (§4.2); EOS `E(n_i, B)` with energy bounded below or a proof it is
not; phase status (the ionic-liquid vs crystal question stays `UNDECIDED` unless `R1B1-P2` decides it
with evidence); bound-state spectrum. Existence of a bound for `μ_e ∝ √n` in 2D (the recorded `n_thr`
mechanism) must be re-derived in the new model, not inherited as a number.

**Acceptance.** at least one stability-checked matter state, **or** a clear proof that the current
candidate model admits none (a NO-GO of the same class as verdict rows 1/6).

---

## §7 Stability and metastability — the `S-STATE` classes

Six acceptance classes (`docs/R1B1.md` §3.4). These are **six classes of evidence that must each be
supplied — not six pre-set pass thresholds**:

| class | must be shown | instrument / status |
|---|---|---|
| `S-STATE-1` | the candidate state satisfies all §4 conservation constraints | census + charge/baryon ledger — Phase 2 |
| `S-STATE-2` | energy is bounded below; a physically acceptable solution exists | the Phase-2 EOS itself |
| `S-STATE-3` | linear perturbations produce no unacceptable growth modes | linearized eigenanalysis; the geometry-side analogue `P2-C6` is still outstanding (report §4 `G3′`) |
| `S-STATE-4` | no immediate dissociation or collapse under nonlinear perturbation | nonlinear dynamics |
| `S-STATE-5` | the state is dynamically reachable along the declared DCC path | Phase 3 (`§8`) — a static solution that the actual compression cannot reach is marked **unreachable**, not passed |
| `S-STATE-6` | if metastable: lifetime exceeds the defined observation timescale | **the observation timescale is `UNRESOLVED`** — it must be declared (from the route's observation definition) before any metastability claim is admissible |

---

## §8 Non-equilibrium evolution (Phase `R1B1-P3`, dynamic reachability)

The dynamic problem `iħ ∂Ψ/∂t = H[B(t)] Ψ` (or the selected relativistic field equations) along the
declared `B(t)` path. Deliverables: the adiabaticity assessment against the compression clock;
non-adiabatic excitation budget; particle escape and capture census; structural destabilization; and the
**rate dependence of the final state** — same final thickness, different paths, different states
(`docs/R1B1.md` §1.2, §3.3). `K5`'s no-scale-separation (`2.96 / 4.72 / 0.33 ns`) is the recorded reason
the quasi-static branch cannot be assumed. Static and dynamic problems cannot substitute for each other.

**Frame requirement (round 43, governor §III).** The geometrically induced field evolution — the
transverse EM term `−(Ḃ/B)E_⊥`, the Dirac measure-compensation identity `−(I/2)(Ḃ/B)𝟙` — is
**geometric redshift/dilution/mixing, not dissipation**: it is a different mechanism from resistive
loss, electron scattering, current relaxation, or absorption-weight transfer, and the optics criteria
(`S4`–`S5`) may not be invoked against it as if it were material loss. The round-42 EM term is a
*coordinate-component* statement; **Phase 3 tracks local orthonormal-frame fields**, not coordinate
components — the frame-referred forms are derived from the round-43 tetrad
(`r1b1_p1_dirac_closure_v1.md` §1, step 1). And `p_z` remains a good quantum number (`[H_D, p_z] = 0`):
the non-adiabatic content is the time-dependent `1/B(t)` mode weights, not z-mode mixing.

**Acceptance.** the static candidate is reachable by the specified DCC path; otherwise explicitly marked
unreachable (`docs/R1B1.md` §7 Phase 3).

---

## §9 Microscopic current operator (Layer 3 contract)

`Ĵ = −δH/δA` — derived from the same Hamiltonian, never posited alongside it (`docs/R1B1.md` §4.2). The
optics object `σ_s,ab(ω, q→0)` is defined as the in-plane `q → 0` response of *this* operator at fixed
projected area; Layer 4 may not substitute a convenient conductivity. The Ward identity (charge
conservation) fixes the transversality of `Π^R` and the contact terms — this is `S6` of the optics spec,
which the current module never constructed (report §7.2: "no `Π^R` is constructed; the Drude form is
written directly").

---

## §10 Kubo response and spectral weight (Layer 3)

The chain is one theory, no stitching: `H → Ĵ → Π^R → σ(ω) → W_total`. `σ_ij(ω) = [Π^R_ij(ω, 0) +
contact] / (i(ω + i0⁺))`, with Fourier, gauge and current conventions declared once and used everywhere
(`docs/R1B1.md` §4.2).

The f-sum **form is a per-model output**: `π n e²/2m` is the non-relativistic continuum form; band,
interacting, non-parabolic and relativistic systems differ. It is `DERIVED` from the declared `H` — never
pre-specified and never stitched from another model (`FSUM-SINGLE-SOURCE`; `FSUM-SPLIT`: a Drude pole
consumes the whole budget by definition — the measured partition of the current module is
`W_intra/W_total = 1.000000000003`, a construction identity).

The four necessary outputs, with tags at delivery time:

| output | admissible source |
|---|---|
| `n_2D^(carrier)` | `DERIVED` from the actual occupation of the solved state (§4.3's slot separation) |
| `g` | `DERIVED`, the degeneracy actually participating, consistent in `k_F`, `E_F`, `W_total` and the interband height (`S15`) |
| `v_F` | `DERIVED` from the band dispersion *if* linear in the declared band; otherwise per-band `|∇_k E|` is reported and a single `v_F` is not forced (`docs/R1B1.md` §4.1) |
| `ω_end` | `DERIVED` from the band/transition structure — never from a budget identity (`S14`/`THREE-OMEGA-G`) |

---

## §11 Relaxation mechanisms and Drude validity

`τ` is an **output** of the solved response, obtained from microscopic scattering, self-energy with
vertex corrections, response poles/peak widths, or memory functions — and its **kind must be declared**:
single-particle lifetime, transport time, a specific current mode's relaxation, or a frequency-band
effective fit (`docs/R1B1.md` §4.4). The recorded cost of not declaring the kind: `τ_tr/τ_sp = 91.548`
vs `138.016` under a kernel change (`TAU-MODEL-DEP`) — the ambiguity is the size of the omission.

Drude reducibility is accepted only as: `S12a` (a single-point `α` certificate is necessary-only — two
poles reach `α = 1` at one frequency) **and** `S12b` (the one-parameter collapse over a declared
frequency domain and tolerance). The measured blind spot (`ALPHA-BLIND`: `α` moves `1.038 → 1.201` while
`σ₁(0)` moves by exactly `1.8`) means Drude-shape evidence **cannot rank the partition** — `f_intra` is
not extractable from the optics side. If the response shows multiple relaxation modes, non-exponential
decay, or significant frequency dependence, the full response is kept — no forced single-pole Drude. A
`τ`-scan remains forbidden as a response (`S13`).

---

## §12 `f_intra` and interband matrix elements

`W_total = W_intra + W_inter`, `f_intra = W_intra/W_total` — but in an interacting system the
intra/inter split may depend on band projection, frequency range, or effective-theory definition, so the
decomposition protocol is fixed in advance (`docs/R1B1.md` §4.3):

1. obtain the full `σ(ω)` from the microscopic current response;
2. identify intra-band vs inter-band transitions by eigenstate/band projection;
3. compute the partial weights;
4. check the two parts sum to the full f-sum;
5. vary basis, truncation and numerical precision, and check the stability of the decomposition.

If the split is not unique, the decomposition dependence or an uncertainty interval is **reported** — an
honest `UNRESOLVED` is preferred to a forced precise value. `f_intra = 1` (or any value inherited from
the current module's construction) is forbidden as input. Interband matrix elements come from the same
eigenstates and fix `A_inter(g)` (`S15`); the module's `e²/(16ħ)` height is the `g = 1` value against a
`g = 2` momentum — the recorded `G-SPLIT` factor `2.000000000000`.

---

## §13 Numerical methods and error control

### 13.1 Methods are chosen per DOF, with applicability gates

| object | candidate methods | gate |
|---|---|---|
| dense-matter structure | nuclear many-body theory, relativistic field theory, interaction-corrected EOS (HNC) | interaction model is `ASSUMED` until Phase 1 declares and justifies it |
| correlated/collective states | ED, DMRG, QMC | applicability at the declared density, `DERIVED` or argued |
| current response | Kubo numerics, spectral-function methods | `Π^R` built from the §9 operator |
| non-equilibrium evolution | real-time many-body dynamics, applicable field solvers | vs the `K5` clocks |
| stability | linearized eigenanalysis, nonlinear dynamics | `S-STATE-3/4` |

Ordinary condensed-matter DFT and 2DEG models are **not** admissible as the foundation until §3's
DOF-survival question is answered for them — maturity of software is not an argument (roadmap
prohibitions ①②; `docs/R1B1.md` §6).

### 13.2 Layered contracts

| layer | content | contract |
|---|---|---|
| `R1B1-L0` | DCC geometry and initial conditions | `B(t)` path, compression protocol, initial composition, conservation constraints — §2's checklist, each item tagged |
| `R1B1-L1` | microscopic matter Hamiltonian | §5's five derivations; gauge consistency, symmetries, dimensions |
| `R1B1-L2` | matter state | §6 + §7 (`S-STATE-1..4`) |
| `R1B1-L3` | microscopic current response | §9–§12 |
| `R1B1-L4` | optical acceptance | f-sum, KK, weight partition, Drude reducibility, `σ_s(ω)` → `S1`–`S15` v1.3 |

Each layer has its own input contract, output contract and **failure state**; an upper layer may not
treat a lower layer's failed or `UNRESOLVED` result as a definite input (`docs/R1B1.md` §6).

### 13.3 Error control

- **floors before thresholds** — every numerical tolerance is set after the instrument floor is measured
  (ledger class 2; `E2`: oscillator `S5` at `1e-10` against a `1e-8` floor; `E5`: `Q2`'s `1e-15` below a
  `6.88e-15` floor);
- **evidence classification** — CHECK / IDENT / NEGCTRL counting per verdict v3 §4; identities are never
  correctness evidence;
- **pre-registration** — every phase that computes registers predictions with kill conditions before
  running; misses stay in the product;
- **traceability** — `E5`'s rule: every empirical number is quoted bound to the product that measured it,
  by file and line.

---

## §14 Falsification conditions and GO/NO-GO

### 14.1 The GO chain

`R1B1-P2` state (stability-checked) → `R1B1-P3` reachable → `R1B1-P4` response (`S1`–`S15`-relevant
outputs tagged) → `R1B1-P5` hands `σ_s(ω)` to `G6`/`DC2` under spec v1.3, **not relaxed for the new
model**. If the real response fails a criterion, the diagnosis is: microscopic model inapplicable /
approximation fails / spec scope needs re-review — parameters are never adjusted to pass
(`docs/R1B1.md` §7 Phase 5).

### 14.2 Valid NO-GO outcomes (each the same class as `G0′` row 1)

1. no bounded-energy, conservation-satisfying state exists under the declared conventions (Phase 2);
2. no candidate state is dynamically reachable along the declared path (Phase 3);
3. no response from a qualified state satisfies `S1`–`S15` (Phase 4 — the optics spec's own
   `NO-GO-ADMISSIBLE` clause).

A NO-GO here is a physical conclusion, not a project failure (report §11).

### 14.3 Model-failure conditions (invalidate the model, not the physics)

- the §3 DOF inventory is proven incomplete — a missing DOF changes the existence or stability verdict;
- the energy ledger fails to close under `B(t)` (the `K4` warning realized);
- a numerical floor exceeds a claimed effect (the instrument, not the physics, produced the verdict).

### 14.4 Prohibitions carried (restated for this line)

No `τ`-scan as response (`S13`) · no bare `ω_end`, no `440.18 MeV` as input (`S14`/`THREE-OMEGA-G`) · no
backward or forward selection of a matter branch · no presupposed sector among A–D · "2D degenerate
electron gas" not citable as the final state before R1-B1 completes (roadmap prohibition ①) · bound-electron
cross-sections not usable for `τ` (②) · no parameter search to manufacture a pass (`docs/R1B1.md` §5.3) ·
every output carries its `SRC-TAG`; every empirical number carries its product (`E5`).

### 14.5 Phase-0 self-audit — the honest open list

| item | tag | discharged by |
|---|---|---|
| `Z_A = 0.522`, `A ≈ 10`, composition behind them | `ASSUMED` | Phase 2 census |
| cold (`T = 0`) approximation inherited from the predecessor EOS | `ASSUMED` | Phase 2/3 energetics under the `K5` clocks |
| `B(t)` path shape, rate, lateral BCs | `UNRESOLVED` | Layer-0 declaration (§2.2), before Phase 3 |
| which DOF survive at the endpoint (central question) | `UNRESOLVED` | Phases 1–2 exit criterion |
| carrier census (`N7`) | `UNRESOLVED` | Phase 2 |
| ν energy budget | `UNRESOLVED` (placeholder non-citable) | Phase 2/3 transport |
| observation timescale for `S-STATE-6` | `UNRESOLVED` | route observation definition |
| `g`, `v_F`, `ω_end`, `f_intra`, `τ`-kind | `UNRESOLVED` | Phase 4 outputs |
| nuclear interaction model | `ASSUMED` until declared | Phase 1 |
| ionic-liquid vs crystal phase | `UNDECIDED` (inherited) | Phase 2 |

---

## §15 The `R1B1-P1` interface (added in v1.1 — governor review, round 41)

### 15.1 Scope order

Theory closure first; no numerical method is selected until closure is certified. `R1B1-P1` theoretical
work may begin now; **numerical computation is not permitted** until §15.3 passes.

**Two closure levels (round 43, governor — binding).** **Kinematic closure** — the checked identities on
the background and field equations (`B-WORK-TERM`, Maxwell structure, the Dirac operator chain,
11/11 in `r1b1_p1_dirac_check_results.txt`) — is **not** **dynamical/action closure** (the five
derivations from the full declared action with every declared field and interaction). A passing
kinematic check may not be cited as action closure, and `P1-CLOSURE-FAIL` lifts only on **dynamical**
closure. Status: *kinematic closure passed (rounds 42–43); dynamical closure not yet ruled* — gated on
`P1-C` plus the §6 declarations of `r1b1_p1_dirac_closure_v1.md`.

### 15.2 Three acceptance tiers

**`P1-A` — degree-of-freedom closure.** Answered explicitly, per degree of freedom: are electrons
retained as explicit degrees of freedom? nucleons? do internal nuclear degrees of freedom require
explicit treatment? is the electromagnetic field retained as a dynamical field? which degrees of freedom
are integrated out — and what do the integrated-out degrees of freedom contribute to the **energy**, the
**stress**, and the **current response**? A bare list ("electrons, nucleons, EM field") is insufficient:
each retention must state its **physical description** — e.g. a nucleon effective theory declares its
energy range and applicable scale explicitly; if those cannot be satisfied, it cannot be the base model.

**`P1-B` — action closure.** `S = S_matter + S_EM + S_interaction`, delivering the five derivations
separately:

| derivation | requirement |
|---|---|
| EOM | matter equations of motion obtained by variation of the action |
| Maxwell | field equations obtained, consistent with the chosen matter current |
| `Ĵ^μ` | obtained from the electromagnetic coupling or by variation of the action |
| `T^μν` | obtained by variation with respect to the metric |
| conservation | explicit conservation relations for charge, baryon number, and total energy-momentum |

plus the mandatory declaration: **is `B(t)` an externally prescribed background, or a dynamical degree
of freedom co-evolving with the matter?** The energy-conservation statement differs between the two —
for an external background, matter energy may exchange with the geometry, and the matter subsystem's own
energy is **not** required to be constant (§2.2's ledger item; the `K4` conflict is the recorded
warning).

**`P1-C` — nuclear interaction model declaration.** Registered fields, all of them: model name and
specific version · degrees of freedom · parameter provenance · range of fitted data · applicable density
interval · applicable energy range · many-body corrections · known errors · whether it remains
applicable within the `K1` geometric range. If the model lacks a credible demonstration of applicability
within the target range, `P1` is flagged `UNRESOLVED` — **a model is not forced to press on**.

### 15.3 The hard veto — `P1-CLOSURE-FAIL`

Entry into numerical computation is **not permitted** if any of the following holds:

1. the degree-of-freedom set is not closed;
2. the action cannot simultaneously yield the matter equations and the electromagnetic equations;
3. the current operator is inconsistent with the Hamiltonian;
4. the energy-momentum tensor cannot be made consistent with the chosen geometric coupling;
5. the conservation laws depend on unstated assumptions;
6. the nuclear interaction model exceeds its declared domain of applicability;
7. there is no treatment for the contribution of integrated-out degrees of freedom to the total spectral
   weight.

**Amendment (round 42, governor review of v1.1 §IV.3).** Item 7's accounting is a **five-point EFT
review**, not a single compensation term: energy and stress contributions · effective corrections to
current operators · effective interactions · conservation laws and Ward identities · optical spectral
weights with high-energy compensation. An `f`-sum compensating term alone does not close an incomplete
low-energy theory. (First applied in `runs/R1B/r1b1_p1_closure_review_v1.md` §3, item 3.)

The purpose of `P1` is genuine theoretical closure — unresolved problems may not be carried inside the
code in order to reach simulation faster.

### 15.4 Three admissible `P1` outcomes

`R1B1-P1` does **not** pre-commit to producing a usable two-dimensional matter model. Exactly three
outcomes are admissible:

1. **theoretical closure** — `P1-A/B/C` pass and `P1-CLOSURE-FAIL` does not fire → register `R1B1-P2`
   (with the `L_z` scan over the `K1` domain, §2.3 role B);
2. **proof that the candidate models are inapplicable** — a recorded demonstration that no declared
   candidate satisfies closure in the target regime;
3. **an explicit statement of which piece of foundational physics is missing** — named, cited, and added
   to the §14.5 open list.

Only with these three outcomes is the Phase 0 → Phase 1 interface genuinely falsifiable.

*Content generated by AI*
