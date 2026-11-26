# Hard-SF Effective 2D Route Candidate v2 — Candidate File Revised per Feedback

**Date**: 2026-11-23
**Status**: **CANDIDATE — REVISION; no governor marker submitted; does not constitute route approval**
**Authority**: none. This file only receives and implements governor feedback on `hard_sf_effective_2d_route_proposal_v1.md`; it is not a governing route, and does not move any gate, terminal class, threshold, or governance status.
**AMENDED 2026-11-26**: adopted as technical content of the governing hard-SF route by
`docs/decisions/hard_sf_effective_2d_route_adoption_v1.md`; the status and authority lines above are retained as
the pre-adoption record. This file still carries no approval block of its own.
**Record**: BN-45 (records only the fact of receipt; no status change).
**Relation to v1**: What v2 revises is v1's **candidate content**; it does not replace, withdraw, or mark v1. The unmarked governor block at the end of v1 remains the only `AWAITING-GOVERNOR` item (`D1 = OPEN 1`). To keep `D1` and governance status unchanged, v2 **deliberately sets no approval checkbox block**; if v2 is to be adopted in the future, the governor must separately perform the single governance action of "mark v2 + dispose of v1", which is not done in this round.
**Relation to D8**: The terminal status of `reports/DCC_terminal_answer_v1.md` and the round queue is unchanged; `RQ-11` is not reopened, no `CLOSED-*` is changed to in-progress, and no queue entry or ledger record is created.

---

## 0. Nature of This Revision

Governor feedback is read as: **accepting the main assessment conclusions and requesting revision of the candidate route**. Thus:

- Do not restore the rejected `M1`–`M5` designations;
- Do not redefine `C1/C2/C3` or change their historical verdicts;
- Do not write `f_min`, any `ΔE_z` value, or approximately `300 s` as established thresholds;
- Do not take ordinary-matter stability as a default premise;
- Do not treat numerical reconstruction as proof of real physical visibility;
- Do not approve any new physical field or energy budget in advance;
- Do not automatically create new queues, and do not change existing route governance status.

This round does only one thing: rewrite v1's five-phase candidate route into a research structure **capable of answering five actual research questions step by step**, and spell out, for each phase, the research question, required physical inputs, computational methods, deliverables, and failure conditions.

---

## 1. Research Objectives and Five Actual Target Questions

The research objective is unchanged: **under hard-SF new-physics assumptions, explore an effectively two-dimensional world with finite thickness and frozen internal excitation in the third dimension, and study its matter states, spacetime evolution, and the visual information available to a declared observer.** This is not "an animation of gradually thinning a three-dimensional object"; the animation is only an end-stage display product.

The research objective consists of the following five questions, all marked with idempotent ordinal numbers, **without occupying any existing symbol or namespace**:

| No. | Actual Target Question |
|---|---|
| (i) | Can three-dimensional space undergo extreme contraction of one spatial direction without metric degeneration? |
| (ii) | Under such a geometric background, does a stable effectively two-dimensional matter state exist? |
| (iii) | Can spacetime, the driving field, and matter be mutually consistent simultaneously within the same background? |
| (iv) | What physical information can the two-dimensionally reduced matter state retain, and by what means can an observer receive that information? |
| (v) | Can a visual simulation of the reduction process and the two-dimensional world ultimately be generated from verified physical calculations? |

These five questions are **constrained in order**: a positive answer to (v) cannot replace a negative or missing answer to any of (i)–(iv).

---

## 2. Terminology, Symbols, and Threshold Discipline

### 2.1 Retain Existing Definitions

- `C1` (effectively two-dimensional space — cylinder conservation) remains at **identity level**, with no dynamical meaning added;
- `C2` (smooth 2D-ization / zero intralayer strain) retains its historical verdict;
- `C3` remains a parameter-independent in-action NO-GO;
- "Effectively two-dimensional" always uses the four-slot definition in `docs/conventions/effective_2d_definition_v1.md`:

  $$\text{model}\ \wedge\ \text{subsystem}\ \wedge\ E_{\rm occ}<\Delta E_z\ \wedge\ E_{\rm probe}<\Delta E_z\ \Longrightarrow\ \text{for this probe, }z\text{ degrees of freedom cannot be excited}$$

  where `E_occ = max(E_F, k_BT)`; the **intrinsic self-consistency bound** and the **external resolution bound** must be listed separately and must not be merged into a single number; the `N7` carrier-conservation check must be passed before discussing the two-dimensionality of electrons.

- `𝓜_eff` remains the set of states defined in `docs/specs/meff_boundary_v0_2.md`, parameterized by `ε = 1 − φ_conv` and adjudicated by `ME2`–`ME5`. Today the `ME2/ME3` tolerance is still `OPEN`, so any deliverable requiring membership must report "membership undetermined, δ_i OPEN"; `CM5` is only an observation channel and cannot determine whether a state is two-dimensional.

### 2.2 `f_min` and `L_z` Must Be Distinguished

This is an explicit requirement newly added in this revision:

| Object | What It Is | What It Is Not |
|---|---|---|
| `f(t,x)` | The z-direction scale factor in the metric `ds² = −c²dt² + dx² + dy² + f²(t,x)dz²`; `f_min > 0` is the **non-degeneracy condition** | Not the thickness itself, not an effective-2D criterion |
| `L_z(t,x)` | The **proper thickness** in the z direction: `L_z = ∫_{z₁}^{z₂} √g_zz dz = ∫ f(t,x,z) dz` | Not a dimensionless factor; not equal to `f_min` |

If `f` does not depend on `z` inside the box, then `L_z(t,x) = f(t,x)·L_z,0`, where `L_z,0 = z₂ − z₁` is the coordinate span; if `f` depends on `z`, the integral expression must be evaluated point by point and a single-point `f` must not be substituted. The energy gap is given by the record convention: Model B's first excitation interval is `ΔE_z = πħc/L_z`, and Model C's `p_z^min = πħc/L_z`. Therefore a smaller `f` is only a geometric input; only when all four slots are filled and both bounds hold separately can one say "this system is two-dimensional for this probe".

### 2.3 Threshold and Naming Discipline

- `f_min`, `300 s`, any `ΔE_z` value, and any `Q3/C` target: all are **inputs pending registration**; this file does not assign values, lock them, or evaluate them; scales and kill conditions must be registered independently before evaluation.
- Do not introduce any new symbols; use only the idempotent ordinals `Phase 1`–`Phase 5` and `(i)`–`(v)`. Do not reuse `M1`–`M5`, `C1/C2/C3`, or `Q1`–`Q6` (`runs/S45` has already occupied them).

---

## 3. Five-Phase Research Structure

The five phases are a **research organization order**, not gates, and do not carry pass status. For each phase, the research question, physical inputs, computational methods, deliverables, and failure conditions must be written out first, and then the governor decides whether to proceed to the next phase. Phase exits are not gate markers and do not modify any gate table row.

### Phase 1 — Finite-Scale Geometry and Front

- **Research question**: With `f_min > 0` and a non-degenerate metric, can a smooth, finite, propagatable reduction front be constructed? (corresponds to (i))
- **Required physical inputs**: metric family and coordinate domain, boundary conditions for `f`, candidate forms of `S(t,x)`, ADM initial data, a declaration of the stress-energy source (not approved), and a curvature upper-bound criterion.
- **Computational method**: solve constraints and evolution in the declared evolution formulation (BSSN/Z4c or a repaired formulation); compute `L_z = ∫√g_zz dz` point by point, not treating `f` as the thickness; perform field matching on both sides of the front.
- **Deliverables**: the solution family `f ∈ [f_min,1]`; `∇f` and curvature upper bounds; proof of ADM constraint closure; a list of matching conditions and kill conditions; an `f → L_z` conversion table.
- **Failure conditions**: occurrence of `f = 0`, metric degeneration, unbounded curvature, failure of constraints to close, inability of the front to propagate stably, or only a geometric animation with no computational solution.
- **Must not do**: infer geometric feasibility backward from visual effects; reuse front-localization conclusions from the frozen ADM sector (`RQ-07`'s conditional theorem holds only for that sector).

### Phase 2 — Novel Stable Two-Dimensional Matter States

- **Research question**: Under the Phase 1 geometry and declared field couplings, do stable, labelable effectively two-dimensional matter states exist? (corresponds to (ii))
- **Required physical inputs**: sources for model (B or C), subsystem, `E_occ`, `E_probe`, and `ΔE_z`; an inventory of the matter state's degrees of freedom; candidate field couplings (not approved); the criterion texts for `ME2`–`ME5`.
- **Computational method**: fill the four slots item by item; compute the intrinsic bound `E_occ < ΔE_z` and the external bound `E_probe < ΔE_z` separately; give priority to the `N7` carrier-conservation check; compute energy levels, stability, stress, and energy exchange within the declared model; for `𝓜_eff`, report verdicts only for the defined portion.
- **Deliverables**: matter-state labels (frozen / HYB / ALL2D or newly created descriptive labels, using no new symbols); a list of retained/changed properties; stability and stress ledger; membership verdict or "membership undetermined, δ_i OPEN".
- **Failure conditions**: ordinary matter being required to survive again in the fixed-area branch; missing slots; `N7` failure; only observational proxy signals without an internal self-consistency check; substituting "can be detected" for "stably exists".
- **Boundaries**: accept the NO-GO of `G0′` row 1; do not revive `G2′`; neither prematurely exclude nor prematurely acknowledge a new matter state.

### Phase 3 — Joint Solution of Spacetime, Fields, and Matter (Critical Phase)

- **Research question**: Can geometric contraction, the driving field, and the matter response be mutually consistent simultaneously in **the same background**? (corresponds to (iii))
- **Required physical inputs**: the Phase 1 geometric solution, the Phase 2 matter-state stress and energy exchange, candidate actions for the driving field (not approved), and an energy-budget declaration (not priced).
- **Computational method**: solve the geometric equations, field equations, and matter response simultaneously in the same background `B(t)`; use BSSN/Z4c or explain why the frozen ADM sector is usable; check curvature, singularities, and numerical stability during front propagation; judge whether `RQ-07`'s delocalization result affects this route according to UV-sector identity.
- **Deliverables**: the joint solution or a proof of its nonexistence; a stress/energy-exchange closure ledger; positive/negative results for front localization or a finite localization length; a statement of relation to `PG-01` conditions `(i)–(iv)`.
- **Failure conditions**: constructing separate elegant models and then stitching them together; no solution to the joint equations; the B-block being treated as resolved when it is not repaired; unacceptable curvature, singularities, or numerical instability; citing `G6/DC2` without its binding conditions.
- **Boundaries**: this phase is the **critical phase** for judging whether the mechanism is jointly self-consistent; it produces only candidate evidence and does not move the gate status of `G3′/G4/G5′`.

### Phase 4 — Observer Channels and Information Classification

- **Research question**: What can the declared observer receive, and which parts are measurement, inference, or display enhancement? (corresponds to (iv))
- **Required physical inputs**: the full `θ = (aperture, gate, band, distance, E, G)`; channel definitions for natural optics and active probing; the Phase 2 matter-state scalars; the Phase 3 geometric solution.
- **Computational method**: compute `C`, `Q3`, and fingerprint separately for the natural-optics and active-probing channels; supplement the `G`-in-estimator rerun from `BN-14` (if the route is approved, as a new entry rather than reopening `RQ-12`); classify all information into three columns.
- **Deliverables**: the three-column information table (see §4); numerical statements qualified by channel/environment/posture; per-frame `BAND`/`COLOUR`/`FIDELITY` drafts.
- **Failure conditions**: contrast sentences without `E` or `G`; producing a visibility sentence; treating `FL1` as readability; treating numerical reconstruction as physical information recovery; claiming to have filled in `10/12` parameters that never entered the deposit.
- **Boundaries**: `S9` still forbids visibility conclusions; `D-1`/`D-2` remain FROZEN; `CM5` can only indicate indistinguishability at a given resolution.

### Phase 5 — Visual Product Generation

- **Research question**: How can the results that have passed Phases 1–4 be converted into visual products without fabricating false evidence? (corresponds to (v))
- **Required physical inputs**: `f(t,x)`, the front solution, the Phase 2 matter-state scalars, and the Phase 4 channel-classification results.
- **Computational method**: map declared physical scalars to display channels; generate annotation blocks frame by frame; render real-physical-observation route A and numerical-reconstruction route B separately.
- **Deliverables**: four classes of display products — (1) geometric grid contraction; (2) front-swept area progress; (3) two-dimensional matter-state field maps (density, energy, excitation level, residual `L_z`, each scalar named separately); (4) observer-viewpoint simulations (A/B labeled separately).
- **Failure conditions**: `FL3` being claimed without a citable frame; an empty `COLOUR-BASIS`; `ENHANCEMENT` without item-by-item justification; treating Phase 5 success as reverse evidence that Phases 1–4 hold.
- **Mandatory labels**: all are `FL1`/`FL2` display products; write `FIDELITY`, `BAND`, `COLOUR`, `COLOUR-BASIS`, and `ENHANCEMENT` per `display_conventions_v1.md` (`EN1`–`EN5`); they must not be used for gate passage.

---

## 4. Two Independent Visualization Research Routes and the Three-Column Information Table

We accept that "information that never entered the physical record cannot be recovered by numerical enhancement", and also that rendering cannot reopen `DEPOSIT-BLIND` or produce a visibility sentence. However, two **mutually independent** routes are retained (`A`/`B` are descriptive channel names within this file, not symbols):

### A. Real Physical Observation Route

Natural optics, active probing, and other channels that can genuinely receive physical signals. Report only signals actually received and their `θ`; when insufficient, explicitly report insufficiency and do not fill gaps with the model.

### B. Numerical Reconstruction Route

Taking **actual measurement data** and **verified physical models** as inputs, reconstruct the spatial structure, matter distribution, energy distribution, and evolution processes of the two-dimensional matter state. It is an independent scientific visualization product and must not be passed off as natural optical observation, nor claim to recover lost physical information.

Both routes must label every item of information in three columns:

| Column | Meaning | Prohibited |
|---|---|---|
| **Direct measurement** | Physical signals actually received by the detector, with `θ` and channel | Writing model output as measurement |
| **Physical-model inference** | Quantities inferred from measurements by a verified model, stating the model and premises | Treating as direct observation; inferring two-dimensionality when slots are missing |
| **Numerical enhancement for display only** | Finite resolution, noise, time compression, false color, etc., with EN justification given item by item | Claiming increased physical information; reopening `D-1`/`D-2` |

---

## 5. Planetary Scale as a Long-Term Goal, Not a Current Threshold

The scenario of sweeping across the Earth in about `300 s` is **retained as a long-term research goal**; deleting it from the research objectives would be wrong. But it is not a physical threshold for the current phase, and must not be used to justify project approval or to claim that the mechanism holds.

The order of scaling up advances step by step according to evidence:

1. Whether a local finite-scale mechanism can hold;
2. Whether the conversion front can propagate stably;
3. Whether it can be extended to a larger range;
4. What energy and field conditions large-scale extension requires;
5. Whether a mechanism exists that can support planetary-scale conversion.

All new field mechanisms and energy budgets must be **declared and priced independently**; unpriced new-physics assumptions must not be used to bypass existing budgets. `relaxation_frame_v1.md` §3 requires each rung to give `V`, `Φ`, and fingerprint; `RL-5`'s persistence has been priced at `1.22×10⁴⁰ W/m²`, about 26.5 orders over budget. A new mechanism must either explain why it is not the same bill or give a new price and accept independent evaluation. This file approves no field or budget.

---

## 6. Relation to Existing Authoritative Records / What This File Does Not Decide

- Do not reopen any gate status of `G0′`, `G1`, `G2′`, `G3′`, `G4`, `G5′`, or `G6`; do not move the markers of `PG-01/02/03`; do not change any terminal class.
- Do not revoke `C1`'s identity-level status, `C2`'s interlayer failure, or `C3`'s in-action NO-GO; do not treat matrix v2 as a route (it is only a product).
- Do not change `DEPOSIT-SERIAL` back to image; do not treat numerical reconstruction as `I(canvas;q)>0`; do not produce a visibility sentence; do not treat `FL1/FL2` as evidence.
- Do not create new queue entries, write ledger entries, change thresholds, or occupy new symbols; `PG-03`'s Path A has not been replaced.
- Do not prove hard-SF two-dimensional reduction feasible; do not approve new physical fields; do not assign values to `f_min`, `ΔE_z`, or `300 s`.

---

## 7. Reverse-on

If this candidate content is adopted by the governance layer in the future, any of the following conditions triggers reverse-on:

1. Phase 1 shows that a front with finite `f_min > 0` cannot satisfy the constraints or develops an irreparable singularity;
2. Phase 2 shows that no stable effectively two-dimensional matter state exists under the declared model, or `N7` fails, or the four slots cannot be filled;
3. Phase 3's joint solution is infeasible, or the front is unstable and cannot be migrated to a repaired formulation;
4. Phase 4 shows that no distinguishable information exists in the declared observer channels, or that the route can only hold by relying on a visibility conclusion;
5. Phase 5 attempts to use visual success to prove Phases 1–4 in reverse;
6. The governor withdraws the route, or a new budget shows that the total price exceeds the declared cap.

---

## 8. Marker Notes (Not Filled In This Round)

This file is a **revision candidate with no marker submitted**, and therefore has no approval checkbox block; this is not an omission, but serves to leave `D1` and governance status unchanged. If the governance layer decides to adopt it, it must handle v1's unmarked block and v2's adoption marker together in **a separate governance action**; until then, v1 remains the only `AWAITING-GOVERNOR` item, and v2 can only be read as a revision candidate.

Silence is not consent. Until marked, this file does not enter the verification chain.

*Content generated by AI*
