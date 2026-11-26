# Hard-SF Effective 2D Route Proposal v1 — Restructured Assessment of an External Proposal

**Date**: 2026-11-23
**Status**: **PROPOSED — not approved, does not constitute a route, does not move any gate / terminal class / threshold**
**Authority**: none. This file receives and assesses an external proposal, restructuring it into a candidate route that can be adjudicated; until a governance marking is applied, it is only a proposal.
**AMENDED 2026-11-26**: the governor marked §7 line 1 (`Accept as the governing successor route`). The status
line above is retained as the pre-mark record; the live disposition, scope, v2/v2.1 technical content and B8
boundary are in `docs/decisions/hard_sf_effective_2d_route_adoption_v1.md`. No other line of this file is changed.
**Relation to D8**: The terminal status of `reports/DCC_terminal_answer_v1.md` and the round queue remains unchanged. This proposal does not reopen RQ-11, nor change any `CLOSED-*` to in-progress.

---

## 1. One-Sentence Verdict

The direction of the external proposal is **mostly compatible with the record**: changing the goal from "three-dimensional space becoming two-dimensional with strictly `L_z = 0`" to "an effective two-dimensional state with `L_z > 0` but extremely small and the third-dimensional degrees of freedom frozen" — this is precisely the terminological boundary already enforced in `docs/conventions/effective_2d_definition_v1.md` §5; it cannot count as a new discovery, but can serve as the starting point of a new route.

However, the proposal's **specific labels and several physical commitments cannot be adopted directly**: `M1`–`M5` already have four or more occupancies in the symbol registry; `C1/C2/C3` cannot be redefined; "atomic and chemical structures remain stable" at fixed area has already been NO-GO by `G0′` row 1; numerical reconstruction cannot reopen `DEPOSIT-BLIND`; Earth-scale compression over roughly 300 seconds requires a new rung that is declared and priced, rather than a narrative parameter written into the goal.

Therefore: **receive it as a proposal, reject its namespace and part of its overcommitments, restructure it into a five-phase candidate route, and await the governor's marking.**

---

## 2. Item-by-Item Assessment of the External Proposal

| External proposal item | Verdict | Basis and treatment |
|---|---|---|
| Change the goal to finite-thickness effective 2D, without requiring strictly `L_z = 0` | **COMPATIBLE — already enforced, not a new conclusion** | `effective_2d_definition_v1.md` §5:74–84 already states: `L_z` is extremely small but nonzero; `L_z = 0` is metric degeneracy and framework failure. `relaxation_ladder_v1.md` §2:35 and `visualization_null_result_v1.md`:120 also prohibit treating the degenerate limit as a physical state. |
| `f_min > 0`, metric always non-degenerate | **COMPATIBLE** | Consistent with the above boundary; must be written as a condition under the ADM initial constraints and evolution equations, not merely as a numerical example. |
| `f_min = 1e−6 ~ 1e−9` as a numerical exploration example | **HOLD** | The proposal itself states it is not a derived result. It may not become a threshold; if it enters the route, the measurement/probe scale and kill conditions must be declared first, then assessed in a separate round. |
| Redefine the original `C1/C2/C3` as geometry / matter / observer | **REJECT — namespace conflict** | `C1/C2/C3` are the only legitimate constraint labels (`constraint_crosswalk_v1.md`:14–19). `C3` is fixed as "weak interaction preserved, in-action NO-GO"; it cannot be renamed "observer obtains information". Observer conditions use descriptive phase names and do not occupy the `C` family. |
| Use `M1`–`M5` as the minimal constraint set | **REJECT — symbol conflict** | `symbol_registry.md`:85–103 records at least four occupancies of `M1`–`M4` (gate, painting mode, visibility metric, etc.), and `M5` is adjacent to `CM5` and easily confused with it. This proposal instead uses the **ordinal phase names Phase 1–5**; they are phase numbers, not new symbols. |
| Matter remains stable with structures intact at fixed area | **REJECT as stated; can be restructured as a new-state-of-matter problem** | `G0′` row 1 is already NO-GO: `d_∥ = 15.40 fm ≪ πa₀ = 1.66 Å`, ordinary atoms/chemical bonds cannot exist at this pillar spacing; `C3` is also a parameter-independent in-action NO-GO. A "new state of matter" may be studied, but it cannot be claimed that original material structures are automatically stable at small `L_z`. |
| `ΔE_z ≫ k_BT`, and consider `E_available`; cite the internal / external two bounds | **COMPATIBLE — already enforced, four slots must be completed** | `effective_2d_definition_v1.md` §1 requires model + subsystem + `E_occ < ΔE_z` + `E_probe < ΔE_z`; §3 prohibits merging the two bounds; §4 requires first passing the N7 carrier conservation check. Writing only the temperature condition is insufficient to judge "it is a two-dimensional system". |
| Smooth front `f(t,x)=f_min+(1−f_min)S(t,x)` | **COMPATIBLE as design premise; unresolved** | A continuous front is a necessary condition, but G4 is already `NOT PASSED`: RQ-07 gives a conditional theorem that this zero-shift, 1+log, second-order FD ADM sector has no finite continuous localization length. The new route must redo front stability in BSSN/Z4c or a fixed formulation, and may not reuse results from the frozen ADM sector. |
| Scalar field + Maxwell action as a driving candidate | **HOLD as candidate** | Can serve as a starting point; must prove sustained contraction, stress distribution, energy exchange, matter stability, and absence of singularities, and must not arbitrarily tune stress signs. Without these, it is only a candidate action, not a hard-SF mechanism. |
| Hard-SF positioning with known physics as skeleton and new physics as core | **COMPATIBLE with a price tag** | `relaxation_frame_v1.md` §3 requires each rung to have `V`, `Φ`, and a fingerprint; a new field without a price is only a mythic-style relaxation, not hard SF. RL-5's persistence has already been priced at `1.22×10⁴⁰ W/m²`, 26.5  orders over budget; a new mechanism must either explain why it is not the same bill or give a new price. |
| "sweeping across Earth in about 300 seconds" | **HOLD — new threshold** | This is a new scenario parameter; it must be registered, linked to front speed / energy budget, and assessed in an independent round; it may not be introduced and evaluated in the same round. |
| Dual channel of natural optics + numerical reconstruction | **PARTIAL** | Compatible with `RL-1`'s instrumented channel; however, the estimator for `Q3 = 5.737` lacked `G` at the time and was only a channel statement (`BN-14`); `C = 0.280` depends on `E` and camera pose (`theta_camera_v1.md`). A rerun after adding `G` is needed. Numerical reconstruction must not reopen `D-1`/`D-2` or produce a visibility sentence. |
| Four categories of visual effects A–D | **ALLOWED as FL1/FL2 display products** | Grids, field-quantity maps, front maps, and observer perspectives may all serve as displays driven by declared scalars such as `f`, density, and energy; `display_conventions_v1.md` must be observed: `BAND`/`COLOUR`/`FIDELITY`, EN1–EN5, and `FL3` may not be obtained through enhancement. They are displays, not evidence of readability. |
| "the `10/12` site parameters that never entered the deposit cannot be made up through enhancement" | **COMPATIBLE — original constraint in the record** | `route_terminus_v1.md` D-2a; `I(canvas;r₄)=0`. Numerical enhancement can only process existing measurements, noise, and finite resolution; it cannot recover information that never entered the deposit. |

---

## 3. Restructured Candidate Route

This proposal adopts five **ordinal phases**. They are not gates and carry no pass status by themselves; an adjudicable output arises only after each phase is completed. The ordering follows the principles of "ladder first, rungs after" and "consistency check of geometry / matter / observer on the same background".

### Phase 1 — Finite-Scale Geometry and Front

**Question**: With `f_min > 0` and a non-degenerate metric, can a smooth, finite reduction front be constructed?

**Required outputs**:
1. Metric family `ds² = −c²dt² + dx² + dy² + f²(t,x)dz²`, `f ∈ [f_min, 1]`, `f_min > 0`;
2. Continuity, gradient, and curvature upper bounds of `S(t,x)`;
3. Explicit formulation of ADM initial constraints, evolution equations, and stress-energy conservation;
4. Matching conditions of fields on both sides of the front and kill conditions.

**kill**: appearance of `f = 0`, metric degeneracy, unbounded curvature, inability to close constraints, or failure of front localization that cannot be migrated to a fixed formulation.

**Reverse-on**: only through this route's own reverse-on or a new governor directive; geometric feasibility may not be inferred backwards from visual effects.

### Phase 2 — New State of Matter Rather Than Survival of Original Matter

**Question**: Given `f_min`, `L_z`, and field couplings, does a stable, labelable effective two-dimensional state of matter exist?

**Required outputs**:
1. Explicit state label: frozen / HYB / ALL2D or a newly created state, and explain its envelope relationship with `G0′` row 2;
2. The four slots model + subsystem + `E_occ` + `E_probe`;
3. Report the internal bound `E_occ < ΔE_z` and the external bound `E_probe < ΔE_z` separately;
4. N7 carrier conservation check;
5. Energy, pressure, stability, and allowed new field couplings; stress signs may not be used for tuning.

**kill**: ordinary matter being required to survive again on the fixed-area branch; or a missing slot among the four; or N7 failure; or only an observation proxy without internal self-consistency.

**Important boundary**: this phase studies a **new state of matter**, not the revival of `G2′`; `G2′` remains `NOT PASSED`, and `BN-01` still requires the governor's terminal-class decision.

### Phase 3 — Joint Solution of Spacetime and Matter

**Question**: Can geometric contraction and matter response be simultaneously self-consistent on the same background, rather than being elegant separately and then stitched together?

**Required outputs**:
1. A solution using BSSN/Z4c, or an explicit explanation of why the ADM frozen sector is usable;
2. Stress and energy exchange consistent with the Phase 2 state of matter;
3. A positive result for front localization or a finite localization length; if delocalization is obtained, its UV-sector identity and whether it affects this route must be stated explicitly;
4. A statement of the relationship with PG-01's four conditions `(i)–(iv)`; when citing `G6/DC2`, it must be stated which conditions are carried.

**kill**: inability to provide a joint solution; or R4's B-block being treated as resolved when it is not fixed; or treating `S3→S4` branch outputs as verification evidence for `S0→S2`.

**Boundary**: do not move the gate statuses of G3′/G4/G5′; this phase produces only candidate evidence.

### Phase 4 — Observer Channels and Information Classification

**Question**: What can the declared observer receive, and which parts are measurement, inference, or display enhancement?

**Required outputs**:
1. Complete `θ = (aperture, gate, band, distance, E, G)`;
2. A three-column information table of direct measurement / model inference / display enhancement;
3. Compute `C`, `Q3`, and corresponding fingerprints separately for natural optics and active probing;
4. Rerun of `BN-14`'s `G`-in-estimator (if the route is approved, as a new item rather than reopening RQ-12);
5. Draft per-frame `BAND`/`COLOUR`/`FIDELITY` declarations.

**kill**: contrast sentences without `E` or `G`; treating FL1 as readability; treating numerical reconstruction as physical information recovery; producing a visibility sentence.

**Boundary**: `S9` still prohibits visibility conclusions; `D-1`/`D-2` remain FROZEN; `CM5` can only indicate indistinguishability at a certain resolution, not that the state is two-dimensional.

### Phase 5 — Visual Products

**Question**: How to convert the passed Phase 1–4 results into four categories of visual products without creating false evidence?

**Products**:
1. Geometric grid contraction animation (driven by `f(t,x)`);
2. Spatial/interior progress maps of the front sweeping across Earth (driven by the front solution);
3. Field-quantity maps of the two-dimensional state of matter (density, energy, excitation level, residual `L_z`, with each scalar named);
4. Observer-perspective simulation (natural optics and reconstruction channels labeled separately).

**Mandatory labeling**: all are `FL1`/`FL2` display products; `EN1`–`EN5` declared frame by frame; no claim of recovering the `10/12` site parameters that never entered the deposit; not to be used for gate passage.

---

## 4. Relationship with Existing Routes / Gates

- **Do not reopen** any gate status of `G0′`, `G1`, `G2′`, `G3′`, `G4`, `G5′`, `G6`.
- **Do not revoke** `C1`'s identity-level status, `C2`'s inter-layer failure, or `C3`'s in-action NO-GO.
- **Do not** change `DEPOSIT-SERIAL` back to image; do not treat numerical reconstruction as `I(canvas;q)>0`.
- **Do not** treat matrix v2 as a route; if its numbers are cited, they serve only as evidence, and the citation rules are in `matrix_v2_status_reading_v1.md` §4.
- **Do not automatically create** new queues; only after the governor's marking are new items and locks generated by phase. `PG-03`'s Path A is not replaced by this proposal; a route change requires a new governor marking.
- **New-threshold policy**: `f_min`, `300 s`, any `ΔE_z` value, and any `Q3/C` target must be independently registered before being evaluated; this standard introduces no thresholds.

---

## 5. What This File Does Not Decide

It does not prove hard-SF two-dimensional reduction feasible, does not approve new physical fields, does not assign a value to `f_min` or 300 seconds, does not change the markings of `PG-01/02/03`, does not move any terminal class, does not produce a visibility sentence, does not turn visual effects into evidence, and does not turn a route proposal into a governing route.

---

## 6. Reverse-on

If this proposal is approved, any of the following will trigger reverse-on:

1. Phase 1 proves that a front with finite `f_min > 0` cannot satisfy the ADM constraints or develops an irreparable singularity;
2. Phase 2 proves that under the declared model no stable effective two-dimensional state of matter exists, or N7 carrier conservation fails;
3. Phase 3's joint solution is infeasible, or the front is unstable and cannot be migrated to a fixed formulation;
4. Phase 4 shows that no distinguishable information exists in the declared observer channel, or that a visibility conclusion is needed for the route to hold;
5. The governor directs withdrawal of this route, or a new budget shows its total price exceeds the declared ceiling.

---

## 7. Governor block (not to be filled in by the executor)

```
[x] Accept as the governing successor route
[ ] Accept with amendments
[ ] Return for revision
```

**Cost of not deciding**: this file remains PROPOSED; the D8 terminal queue is unchanged; all visual effects may only serve as FL1/FL2 display research and cannot enter the verification chain.

**Mark location**: one of the three lines in this section, one character. No mark = not approved; silence is not consent.

---

## 8. Governor mark transcribed (2026-11-26)

The single character above was marked by the project governor's instruction of 2026-11-26
("将 hard-SF 有效 2D 正式采纳为路线"). It is transcribed in place, in this authoritative file, as
`COMPLETION_PROTOCOL_v1.md` §3.1 requires; the executor did not infer approval from silence. The two
alternative lines remain unmarked. `v2` and `v2.1` are adopted as this route's binding technical content by
`hard_sf_effective_2d_route_adoption_v1.md`, which also fixes the mark's scope, the B8 boundary, and the
reverse-on clauses. This mark closes `D1`'s only `AWAITING-GOVERNOR` item; it does not move any gate,
threshold, terminal class, RL price, or the sealed D8 answer.

*Content generated by AI*
