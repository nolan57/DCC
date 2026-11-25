# Hard-SF Effective 2D Route Candidate v2.1 — Technical Revision Edition

**Date**: 2026-11-23
**Status**: **CANDIDATE — TECHNICAL REVISION; conditionally accepted as a candidate research framework; not approved to enter the formal implementation chain**
**Authority**: none. This file implements the governor's verdict of "conditionally accept v2, first make technical revisions." It is not a governing route, does not authorize formal numerical implementation, and does not move any gate, terminal class, threshold, or governance status.
**Relation to v2 / v1**: v2.1 only revises the technical premises of `hard_sf_effective_2d_route_candidate_v2.md`; it **does not replace, withdraw, or mark** v1 or v2. v1's unmarked block remains the sole `AWAITING-GOVERNOR` item, `D1 = OPEN 1`. To maintain that status, this file **sets no approval checkbox block**.
**Record**: BN-46 (records only the fact of receipt, with no status change).
**Relation to D8**: `reports/DCC_terminal_answer_v1.md` and the round queue terminal status are unchanged; `RQ-11` is not reopened; no queue, ledger, lock, or threshold is created.

---

## 0. Summary of Verdict Implementation

The governor's verdict is read as: **v2 passes structural integrity; four technical premises must be revised; route execution is not approved for now.** Therefore this round does only four things:

1. Add to Phase 1 the declaration requirements for the `z`-direction coordinate domain, boundary conditions, and their evolution, and distinguish the `f(t,x)` initial simplified model from the `f(t,x,z)` extended model;
2. Strictly bind the third-dimensional energy levels to the declared model, subsystem, boundary conditions, and dispersion relation, reporting the momentum lower bound and the energy interval separately;
3. Distinguish geometric trial solutions / constraint-satisfying solutions / evolution solutions / joint solutions, and state explicitly that BSSN/Z4c does not automatically resolve `G4`;
4. Add an "input completeness" criterion to Phase 4's numerical reconstruction.

Not done, and not permitted: treating v2.1 as a governing route; running formal numerical simulations predicated on route approval; assigning or locking `f_min`, `ΔE_z`, `300 s`; approving new physical fields, energy budgets, or planetary-scale mechanisms; changing `D1`, `D8`, existing gates, terminal classes, or queues.

---

## 1. Four Technical Revisions

### 1.1 Phase 1 — Spatial Domain and Boundary Conditions Must Be Declared First

v2's proper thickness definition is retained:

$$L_z(t,x)=\int_{z_1}^{z_2}\sqrt{g_{zz}}\,dz=\int_{z_1}^{z_2}f(t,x,z)\,dz .$$

But this expression has a definite meaning only after the domain and boundaries of `z` are declared. Phase 1 must add the following declarations; any missing item is judged as not implementable:

| Required declaration | Allowed treatment | Prohibited |
|---|---|---|
| `z` domain topology | Finite interval `[z₁,z₂]`; non-compact `ℝ`; compact circle `z∼z+2πR_z` | Mixing the three without explanation |
| Boundary nature | Physical wall / periodic boundary / other explicit conditions; write out item by item | "default boundary" |
| Whether boundaries change with time | Specify the evolution law for `z₁(t),z₂(t)` or `R_z(t)` | Assuming static by default |
| Effect of boundaries on eigenmodes | Show how boundary conditions enter the spectral problem | Using `f_min>0` in place of a spectral conclusion |

**Core prohibition**: `f_min>0` only guarantees a non-degenerate metric; it **does not imply a finite `L_z`**. If `z∈ℝ` and there is no non-compactification mechanism, the integral generally diverges and cannot be written as a finite thickness. A finite proper thickness must be determined jointly by the full integral **and** an explicit spatial domain.

**Geometric model switching prohibition**:

- `ds²=−c²dt²+dx²+dy²+f²(t,x)dz²` is the **initial simplified model** (`f` does not depend on `z`, hence `L_z=f(t,x)·(z₂−z₁)`);
- `f(t,x,z)` is the **extended model** allowing spatial inhomogeneity, for which the integral expression must be used;
- Switching between the two within the same calculation requires first declaring the switching point, physical rationale, and new boundary conditions.

### 1.2 Phase 2 — Energy Gap Formula Bound to model / subsystem / boundary / dispersion

The v2 statement "`ΔE_z=πħc/L_z`, and Model C's `p_z^min=πħc/L_z`" is **superseded in v2.1**. It is checked below against the precise definitions in existing records; the following only cites records, **modifying no archived text and adding no symbols**:

| Model | Settings and spectrum in the record | Formula location in the record | Treatment in this candidate |
|---|---|---|---|
| Model A: non-compact anisotropic contraction | `z∈ℝ`, continuous spectrum, **no `p_z^min` exists** | Roadmap v1.4 §1.2:131; §2.4:276 | No minimum momentum or energy gap may be assigned; decreasing `f` does not constitute spectral freezing |
| Model B: finite-thickness potential well | `z∈[z₁,z₂]`, bound spectrum determined by potential-well eigenvalues, **not `2π/L_z`** | Roadmap v1.4 §2.4:277; deposit's registered interval `ΔE_z=πħc/H_eff` (Annex B §B.2:38–44; `t4_heff_floor_ruling_v1.md`:69) | Use this registered expression only after declaring `H_eff` and the potential-well boundaries; it must not be generalized into a universal formula |
| Model C: compact circle | `z∼z+2πR_z`, `p_n=nħ/R_z`, hence `p₁=ħ/R_z`; if written with circumference `L_circ=2πR_z` then `p₁=2πħ/L_circ` | Roadmap v1.4 §2.4:278; Annex B §B.2:46 gives the energy expression `2πħc/L` | `p₁` is **momentum**; energy is given by the dispersion: `E_n²=m²c⁴+c²n²ħ²/R_z²+c²p_⊥²` (§2.4:282); non-relativistic approximation `ΔE_KK∼ħ²/(2mR_z²)` (§2.4:284) |

**Recorded fact of the dimensional issue**: `effective_2d_definition_v1.md` §5:80 contains `p_z^min=πħc/L_z`; the right-hand side has dimensions of energy, not momentum. This is a **recorded and named dimensional mismatch**; this candidate only cites it faithfully, neither unilaterally changing the existing definitions of Model B / Model C to fix the dimensions nor inventing replacement symbols.

**New mandatory rules added in Phase 2**:

1. Third-dimensional excitation energy levels must be **derived** from the declared subsystem, boundary conditions, and dispersion relation; expressions from a particular model may not be copied;
2. The **momentum lower bound** and the **energy interval** must be reported in separate columns; the former has units of momentum, the latter units of energy;
3. Before model / subsystem / boundary / dispersion are fixed, it is prohibited to use `ΔE_z` to draw any numerical conclusion about `E_occ<ΔE_z` or `E_probe<ΔE_z`;
4. Borrowing spectral conclusions across models is prohibited (`eff_dim_claim_A6_PROPOSED.md`:104 records such mixing as a defect; Roadmap §1.2:136 also prohibits it).

### 1.3 Phase 1 / Phase 3 — A Geometric Trial Solution Is Not a Physical Joint Solution

 Governor adopts the phase ordering but requires classification of results. Phase 1–3 outputs must be classified according to the table below and must not be described beyond their class:

| Result type | Conclusions that may be drawn | Conclusions that may not be drawn |
|---|---|---|
| **Geometric trial solution** | Mathematical properties of the given metric (curvature, non-degeneracy, `f→L_z` conversion) | That a real physical mechanism can be realized |
| **Constraint-satisfying solution** | Specific initial data satisfy the constraint equations | That a front can form persistently |
| **Evolution solution** | An evolution exists under the declared equations | That the driving field has an acceptable energy price |
| **Joint solution** | Geometry, fields, and matter are self-consistent on the same background | That planetary-scale conversion is already feasible |

**Phase 3 is the first stage that genuinely judges whether the overall mechanism holds**; the mathematical existence in Phase 1 must not be taken as a physical conclusion of Phase 3.

**BSSN/Z4c is not an automatic fix**: adopting this formulation still requires item-by-item declaration of the specific equations, gauge choice, constraint propagation properties, and numerical boundary conditions. `RQ-07`'s conditional theorem applies only to the frozen ADM sector with zero shift, 1+log, and second-order FD; after adopting BSSN/Z4c or a fixed formulation, front localization must be re-proved, and `G4` may not be claimed resolved merely because the formulation was changed.

### 1.4 Phase 4 — Input Completeness of Numerical Reconstruction

v2's three-column separation (direct measurement / physical model inference / display enhancement only) is retained, and an input completeness criterion is added:

- Numerical reconstruction may generate images of internal structures that the device cannot directly display, but their content must be results **inferable by the model under the existing input constraints**;
- If an internal quantity is not directly probed, but model parameters, boundary conditions, and observational data suffice to constrain it, it may be labeled **physical model inference**, with the parameters used and the sources of constraints written explicitly;
- If a parameter required by the model has never entered the physical record and has no independent constraint, it may not be turned into a physically grounded structure through finer rendering;
- This criterion is consistent with the treatment of the `10/12` site parameters that never entered the deposit, `D-1`/`D-2` FROZEN, and `DEPOSIT-BLIND`, and does not change existing statuses.

---

## 2. Five-Phase Implementation Order and Dependency Rules

 Governor's technical implementation recommendations are incorporated as-is (technical recommendations only, not governance status changes):

1. **Phase 1 — Finite-Scale Geometry**: first resolve the spatial domain, boundary conditions, metric non-degeneracy, ADM constraints, and front evolution; output a geometric solution or an explicit failure result.
2. **Phase 2 — New Stable Two-Dimensional State of Matter**: depends on Phase 1 inputs; first confirm the model and subsystem, then derive the third-dimensional energy levels, complete the `N7` check, and the two energy bounds; do not assume ordinary matter survives.
3. **Phase 3 — Joint Solution**: the core physical verdict point; test whether geometry, driving fields, and matter can jointly satisfy the equations, and compute the actual energy cost.
4. **Phase 4 — Observer and Information**: depends on the joint physical result; evaluate natural optics, active probing, and numerical reconstruction separately, distinguishing measurement, inference, and enhancement.
5. **Phase 5 — Visual Products**: terminal products; only convert the results of the first four phases into images and animations, observing the `FL1`/`FL2` and `EN1`–`EN5` disciplines.

**Dependency rule**: Phase 1–3 may have local analytical iterations, but phase dependencies may not be skipped. If Phase 2 finds that a certain state of matter requires different geometric boundary conditions, this may be fed back to Phase 1 as a **new candidate problem**; Phase 2's state-of-matter assumptions may not be treated as geometric facts already proved in Phase 1.

---

## 3. Visual Simulation: Goal Retained, Product Commitment Not Retained

Visual simulation remains a formal research goal, but is approved only as a goal, not as a product commitment with an established physical basis. Three categories of results must be kept separate:

| Category | Prerequisite for validity | May not be inferred from the preceding/following category |
|---|---|---|
| Geometric visualization | Phase 1 yields a valid geometric solution; maps `f(t,x)`, `L_z(t,x)`, front position | Must not be taken as a state of matter being established |
| State-of-matter visualization | Phase 2 and Phase 3 hold; maps density, energy, excitation level, etc. | Must not be taken as the scene an observer sees |
| Observer-perspective simulation | Phase 4 gives results for a specific observer, channel, and information conditions | May not be inferred directly from the first two categories |

When natural optics cannot directly see certain two-dimensional internal structures, **scientific reconstruction images** may still be generated from validated physical models and actual measurement data; these must be labeled as numerical reconstruction, not as the scene actually seen by an observer.

---

## 4. Phase 1's First Concrete Task (Pure Symbolic and Constraint-Closure Review)

Following the governor's next-step recommendation, Phase 1's first task is **not to write numerical simulation code**, but first to prove: under an explicit spatial domain, boundary conditions, and declared stress-energy sources, whether the given finite-thickness metric admits constraint-satisfying non-degenerate initial data, and whether it can maintain finite curvature under the chosen evolution formulation.

List of symbolic derivation questions for this review (**not to be written into the formal queue**):

1. For the three domains `z∈[z₁,z₂]`, `z∈ℝ`, `z∼z+2πR_z`, write out the `L_z` integral of `g_zz=f²` and its convergence conditions respectively;
2. How boundary conditions (physical wall / periodic / other) enter the `z`-direction eigenvalue problem; what coupling terms arise when boundaries are time-dependent;
3. The difference in ADM constraint equations between the `f(t,x)` and `f(t,x,z)` models, and what the switching conditions are;
4. Given the declared stress-energy sources, whether the constraint equations close; when a source is unsatisfied, which terms must enter the budget (N6 `p_z` backreaction and N11 `P_2D` constraint stress are mandatory terms);
5. Gauge choice, constraint propagation, and numerical boundary conditions of the chosen evolution formulation (BSSN/Z4c or a fixed formulation);
6. Finite-curvature criteria and singularity kill conditions;
7. Which of the four classes in §1.3 this geometric trial solution belongs to, and whether it can be upgraded to a constraint-satisfying solution;
8. What equations and data are still missing to upgrade to an evolution solution and a joint solution, respectively.

**If this cannot be established, the subsequent states of matter, joint solution, and visual products have no reliable geometric foundation. First prove that space can evolve in this way, then study how matter can exist within it, and only finally study what an observer can see.**

---

## 5. Work Allowed and Disallowed in This Round

**Allowed**:

- Make the above four technical revisions to v2, forming v2.1;
- Organize the mathematical definitions, spatial domain, boundary conditions, and ADM initial data needed for Phase 1 (listed in this file's §1.1 and §4; the review has not yet been performed);
- Independently check the energy-level definitions and dimensions of Model B / Model C (checked and recorded in this file's §1.2; archived definitions not changed);
- Prepare the list of symbolic derivation questions for Phase 1, without writing it into the formal queue.

**Disallowed**:

- Do not treat v2.1 as a governing route;
- Do not run formal numerical simulations predicated on route approval;
- Do not assign or lock pending-registration parameters such as `f_min`, `ΔE_z`, `300 s`;
- Do not approve any new physical fields, energy budgets, or planetary-scale mechanisms;
- Do not change `D1`, `D8`, existing gates, terminal classes, or queues.

---

## 6. Unchanged Items and Reverse-on

Unchanged: the definitions and historical verdicts of `C1/C2/C3`; the four slots and two bounds; `𝓜_eff`'s `ME2`–`ME5` membership (still `membership undetermined, δ_i OPEN`); the gate statuses of `G0′` row 1, `G2′`, `G3′`, `G4`, `G5′`, `G6`; `DEPOSIT-BLIND`, `D-1`/`D-2`; matrix v2's product identity; `PG-01/02/03` markings; D8 terminus; queues and ledgers.

If this candidate is later adopted by the governance layer, any of the following will trigger reverse-on:

1. Phase 1 proves that under explicit domains and boundaries no constraint-satisfying non-degenerate initial data exist, or curvature cannot be kept finite;
2. Phase 2 proves that under the declared model no stable effective two-dimensional state of matter exists, or `N7` fails, or the four slots cannot be filled;
3. Phase 3's joint solution is infeasible, or front localization still fails in a fixed formulation;
4. Phase 4 shows that no distinguishable information exists in the declared observer channel, or the route can only hold by relying on a visibility conclusion;
5. Phase 5 uses visual success to retroactively prove Phase 1–4;
6. The governor withdraws the route, or a new budget shows the total price exceeds the declared ceiling.

---

## 7. Marking Notes (Not to Be Filled In This Round)

This file is an **unsubmitted candidate after technical revision** and has no approval checkbox block; this is not an omission, but serves to keep `D1 = OPEN 1` and the governance status unchanged. If the governance layer decides to adopt it, a separate governance action must handle both v1's unmarked block and this candidate's adoption marking. Until then, v1 remains the sole `AWAITING-GOVERNOR` item, and v2.1 may only be read as a technical-revision candidate.

Silence is not consent. Until marked, this file does not enter the verification chain.

*Content generated by AI*
