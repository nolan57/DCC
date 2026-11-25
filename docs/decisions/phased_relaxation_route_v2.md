# Phased constraint relaxation and presentation fidelity — route v2 (governor's directive)

**Date**: 2026-11-22
**Status**: **REGISTERED VERBATIM** (§1–§5). Executor's phase-status audit: `reports/reviews/phased_route_v2_audit.md`
(V1–V8). Checks: `runs/S45/phased_route_checks_registration.md` → `runs/S45/phased_route_checks_results.txt`.
**Supersedes**: nothing. **Amends**: `docs/decisions/staged_relaxation_visual_route_v1.md` — §6 below states exactly
what moves and what does not.
**Authorised text**: this document is the governing text for the phased route. Where it conflicts with
`staged_relaxation_visual_route_v1.md` §3's stage order, **both stand** until the governor rules on the conflict
(audit V7) — the executor does not resolve a governor-level ordering question by choosing a side.

---

## 1. Directive (verbatim)

> **Directive: 2D-ification Frontier Visualization — A Route of Phased Constraint Relaxation and Presentation
> Fidelity**
>
> General Principle. The sole legitimate method for advancing this route is to relax only one constraint at a
> time, and after each relaxation, all ME gates and symbol linting must be re-run. Any commit that "incidentally"
> relaxes a second constraint is deemed invalid. Presentation fidelity (FL) must not precede its corresponding
> physical phase—i.e., display conventions must not be used to mask physical gaps that have not yet been closed.
>
> Phase 0 — Baseline Closure (S0/FL1)
> - Objective: Establish the sole authorized source of color. All frequency-flatness displays must be marked as
>   declared display conventions per §8, and must not be cited as physical evidence.
> - Deliverable: S0 baseline product + color convention declaration block.
> - Gate: ME1 (injectivity) must pass; ME5 takes effect as a hard gate—no image claiming to be a "faithful
>   reflected-light frame of a surviving sheet" may be produced in this phase.
> - Prohibition: While δ_ov, ℓ_samp/Δz_tol, and δ_E,max remain OPEN, no convenient δ values may be written in to
>   force checks to pass.
>
> Phase 1 — Geometric Relaxation (ME1 → ME1′)
> - Relaxation Target: Only the relaxation of the local injectivity neighborhood radius is permitted.
> - Must Maintain: ME4 topological invariants remain piecewise constant. If the relaxation causes a jump in the
>   Euler characteristic, roll back immediately.
> - Reporting Format: May only be stated as "solution given data D"; stating it as "confirmation of D" is
>   prohibited (PROV-3).
>
> Phase 2 — Evolution Clock Calibration (ME5 Unfrozen)
> - Precondition: Phase 1 passes, and the corollary of ME5 has been explicitly annotated on all L3 products.
> - Action: Calibrate Λ_max for the intrinsic time scale τ. This is the only phase in this route permitted to
>   touch ME5.
> - Falsification Clause: If the calibration results in a zero sheet survival time, this route terminates;
>   adjusting display parameters to circumvent this is not permitted.
>
> Phase 3 — Physical Quantity Boundary Relaxation (ME2)
> - Relaxation Target: The controlled scope of the Noether symmetry breaking boundary.
> - Hard Constraint: At least one non-trivial conserved current J^μ must be retained. A zeroing of the conserved
>   current is deemed a failure; "approximate conservation" is not accepted.
>
> Phase 4 — Presentation Fidelity Enhancement (FL1 → FL2 → FL3)
> - Strictly Postposed: This phase only commences after Phases 0–3 are fully closed.
> - Naming Discipline: FL1–FL3 must be used; bare L is prohibited (L still carries the triple semantics of
>   optical layer and R2-D redshift layer; per existing rulings, it remains unrenamed, but qualification is
>   strictly enforced).
> - Prohibition: Retrospectively modifying any frozen physical parameters under the pretext of FL enhancement is
>   prohibited.
>
> Invariants Throughout
> 1. C_geo/C_phys/C_info/C_top are permanently retired and must not return in any form.
> 2. ΔH serves solely as a reportable quantity under BUDGET-1 and never participates in scoring.
> 3. Before each phase commit, the VIOLATION count for symbol_lint.py and provenance_lint.py must be 0.
> 4. No check that has not been run may be pre-registered as passed.

## 2. Phase status at registration (executor's assessment)

Decidability is a property of the *gate*, not of the physics. "OPEN" means the gate cannot be evaluated without a
parameter the directive itself forbids supplying.

| Phase | Gate | Relaxation target names an object in v0.2? | Decidable today? | Blocking finding |
| --- | --- | --- | --- | --- |
| **0** | ME1 passes; ME5 hard | — (no relaxation) | **NO** | V1: `Δz_res` — the parameter that *alone* decides ME1 — is unregistered and is not on the prohibited list |
| **1** | ME4 piecewise constant; rollback on `χ` jump | **NO** — "local injectivity neighbourhood radius" is not a parameter of ME1 | NO | V2, V3 |
| **2** | Phase 1 passes | **NO** — `Λ_max` belongs to the declined alternative ME5 | NO | V4, V5 |
| **3** | J^μ retained | **NO** — described content is `C_phys`→`ME3`, not `ME2`; the predicate is `C`-domain | NO | V6 |
| **4** | — | — | Blocked by 0–3 | — |

**Nothing in this table changes a registered threshold.** `δ_ov`, `ℓ_samp`, `Δz_tol`, `δ_E,max` remain OPEN,
exactly as the directive requires, and no value was supplied to make anything pass.

## 3. What is adopted without reservation

1. **The General Principle.** One constraint per commit, with a manifest of which constraint moved; and FL must not
   outrun the physics. This is stricter than the existing ledger and it is the right rule.
2. **ME5 as a hard gate from Phase 0 onward** — the corollary is already FROZEN and exact, so applying it
   immediately is free and correct.
3. **The "sole authorised source of colour" requirement.** The frequency-flatness result
   (`runs/R5/r5l2_sigma_s_results.txt`, §8 of the v1 ledger: `R = 0.975855` at 1.0, 2.0 and 3.0 eV alike) makes
   any chromatic content a declared convention. This is now enforced by
   `docs/conventions/display_conventions_v1.md`, delivered with this registration.
4. **PROV-3 reporting form** ("solution given data D") — already binding.
5. **Invariants 1, 2 and 4** — already binding, restated here.
6. **Invariant 3, once its vocabulary is fixed** (V8). It is currently stated in a field that one of the two
   tools does not emit, so as written it cannot be checked.

## 4. Amendments to the record made by this registration

| Item | Change | Authority |
| --- | --- | --- |
| `τ` | Phase 2's "intrinsic time scale τ" would be a **second owner**: `τ` is the Drude relaxation time in `src/optics/sigma_s_lindhard.py` (`TAU_SCAN`, OPEN, scanned not solved). Phase 2's clock is registered as **`τ_conv`** | registry R3 |
| `Λ_max` | **Retired.** It exists only in the declined alternative ME5 (`meff_boundary_v0_2_alt_definitions_DECLINED.md`) and in the alternative's review V5 as a directionally inverted form. It is not a parameter of adopted ME5 | audit V4 |
| `Δz_res` | Registered as a **named, currently-unregistered parameter** that decides ME1 (audit V1). No value assigned | v0.2 O6 |
| Gate vocabulary | Invariant 3 restated per tool in §5 | audit V8 |
| `ME1'` | Registered as a **reserved label** for Phase 1's relaxation, with no definition until Phase 1's target is specified in terms ME1 actually has | audit V2 |

## 5. Enforceable form of invariant 3

The two tools do not share a violation vocabulary (R7: `VIOLATION` appears 7× in `provenance_lint.py` and 0× in
`symbol_lint.py`). The gate is therefore stated per tool and executed by `src/common/commit_gate.py`:

```
commit_gate = (symbol_lint:     MUST-FIX(A,C,D) == 0)      # F stays advisory: M1-M4 have pre-existing owners
           and (provenance_lint: blocking(VIOLATION + MISSING + INCOMPLETE) == 0)
```

Archived hits under `runs/` are **excluded** from the symbol count because §9.1 forbids editing them; a gate that
included them would be permanently red through no fixable cause (`runs/CONVENTIONS/symbol_lint_results.txt` records
the archived tally separately). This is a definition, not a relaxation: the count it gates is the same count the
tools already report.

## 6. Relationship to `staged_relaxation_visual_route_v1.md`

**Unchanged**: the S0→S2 validation chain, the S3→S4 relaxation branch, every `C1/C2/C3` verdict, ME1–ME5 as
adopted, the D-A boundary-data split, and the authorisation status of every claim.

**Added**: the phase gates, the one-constraint-per-commit rule, the colour declaration requirement.

**In open conflict, awaiting a ruling** (audit V7): v1's ladder relaxes **C2 first (S3)** and **C1 second (S4)**;
this directive's Phase 1 relaxes the `ME1`/`C1` object **first** and contains **no C2 relaxation at all**. The two
orders are not compatible as written. The executor has not chosen between them.

### 6.1 Amendment after the crosswalk (2026-11-22) — the conflict is narrower than it looked

`docs/conventions/constraint_crosswalk_v1.md` re-registers `C1`/`C2` in the `ME`/`CM` system as a **bridge**
(`C1 ⇒ᵍ ME1@Δz_res`, `C1 ⇒ᵒ CM1@λ`, `C2 ⊥ {ME}∪{CM}`), not as a rename — a rename is forbidden by `S1` in both
directions and would delete `C2`'s content, which no `ME`/`CM` predicate can see. Three consequences for the
ordering question:

1. **Only one third of the constraint diagonal is expressible in gate space** (`1 of 3`; X5). An `ME`-indexed
   ladder cannot walk that diagonal, so this directive's phases cannot be a re-ordering of v1's ladder — they are an
   ordering of a different, smaller list.
2. **There is no `C2` relaxation to order.** Under the registry's definition (`C2` = zero **intralayer** strain),
   S3 — which renders **interlayer** discontinuities — does not touch `C2`; under the wider reading (intra **and**
   inter), `C2` is already false for every real object, so S0 already fails it. Under either reading S3 is a
   **presentation** step or an **admission**, never a constraint relaxation (crosswalk §5.2).
3. **Phase 1 is S4.** Under registry `S7`, relaxing `ME1` is recorded as `moves: C1 (proxy)`, because for branch
   products certification is the only enforcement `C1` has. So the directive's Phase 1 and v1's S4 are one step,
   not two, and there is exactly **one** relaxation in either ladder.

**What remains yours to rule** (crosswalk §5.6): whether S3 keeps the word "relaxed" in the ledger, and whether
`C2`'s definition is intralayer-only as the registry states or full smoothness. Both change the *bookkeeping*, not
the physics. The ordering itself now has a one-element answer and no freedom left in it.

---

## R. Rulings on the open items (2026-11-22)

The directive text above is **unchanged** — it is the governor's text and is registered verbatim. The four open
items of `phased_route_v2_audit.md` §J were ruled the same day; the authority is
**`docs/decisions/gd_rulings_v1.md`**, and these are the operative statements that replace the corresponding
clauses above.

| Item | Ruling | The clause it replaces |
| --- | --- | --- |
| `GD1` | **Option B** — `ME1` reclassified to **`CM5`**; **Phase 0's gate is `ME4`** (fragment census, FROZEN). `Δz_res` is *not* frozen and is no longer a gate parameter | Phase 0's "Gate: ME1 (injectivity) must pass" |
| `GD3` | Phase 1's target is **`δ_ov` / O6**, derived from the `μ_ov` estimator, with the falsifier "`δ_ov` independent of the test state" | Phase 1's "relaxation of the local injectivity neighborhood radius" |
| `GD4` | **Accepted** — Phase 3 is `ME3`; `J^μ` is an OPEN instrument | Phase 3's "ME2" |
| `GD5` | **Accepted** — `τ → τ_conv`; `Λ_max` retired; Phase 2 re-specified as *declare the clock and verify `τ_exp ≤ t_rip`* | Phase 2's "calibrate `Λ_max`" |

**Two structural consequences, which supersede parts of §5–§6 below.**

1. **§3's analysis was conditional on `ME1` being a gate, and that premise is now withdrawn.** With `CM5` in the
   observation channel, the whole crosswalk reads: `C1 ⇒ᵒ {CM1, CM5}`, `C2 ⊥`, `C3 ⊥`. **No constraint has a gate
   expression**, so `S7`'s "a proxy relaxation is a constraint relaxation" no longer applies to Phase 1 — Phase 1
   relaxes what an observer may claim, not what the branch certifies, and is registered `moves: none
   (observation channel)`. `S7` is amended in the registry.
2. **Phase 3 is now the only physical relaxation in the route** (`ME3`'s `δ_E,max`, the `C_phys` successor), and
   it is specifiable but not yet runnable, since `δ_E,max` is OPEN and `J^μ` is an instrument that does not exist.
   So the ladder currently contains **zero executable relaxations** — which is an accurate description of the
   state, not a failure of the directive.

The ordering question is now fully closed: there is one relaxation, it is Phase 3, and it is neither `C1` nor
`C2`. The two bookkeeping items of crosswalk §5.6 remain yours and remain bookkeeping only.

---

## S. Execution record (2026-11-22)

The route was executed as far as it goes. Authority and full detail:
**`docs/decisions/route_completion_v1.md`**; products in `runs/ROUTE/`; pre-registration honoured including where
predictions failed.

| Phase | Verdict | Note |
| --- | --- | --- |
| 0 | **DELIVERED** | `ME4` clause 3 PASS; frame + display block; certifies no tearing, not 2D-ness |
| 1 | **PASS-WITH-NARROWING** | `δ_ov` derived; admissible set `{0,1}`; 0 inert, 1 vacuous; no usable setting |
| 2 | **PASS** | `t_rip` exact; sub-field exposure admissible at 284 eV; reflected frame still impossible |
| 3 | **CLOSED — NO DELIVERABLE** *(was BLOCKED)* | `GD6` closed 2026-11-22 (`me3_phi_disposition_v1.md`): `φ` declared a velocity potential, `ME3` **retired**. The block was in the criterion, not the symbol — every static reading is inverted (`k ∈ (0,2)`), so the constraint is a minimum-thickness floor; the kinematic reading is `≡ 0`, so it rejects nothing. Phase 3 has no target and is deleted |
| 4 | **NOT STARTED** | strictly postponed behind Phase 3 |

**The route stops in Phase 3 because of a defect in the spec, not in the route.** One governor decision is needed
to continue: **`GD6`** — what field `φ` denotes in `ME3` (`route_completion_v1.md` §6). Nothing else in Phases 0–2
is waiting.

---

*Content generated by AI*
