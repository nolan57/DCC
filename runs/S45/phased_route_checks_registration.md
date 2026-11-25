# Pre-registration — checks on the phased relaxation directive (2026-11-22)

**Registered before execution.** Thresholds and falsification conditions fixed here; no parameter may be
adjusted after seeing a result. Output: `runs/S45/phased_route_checks_results.txt`.

**Subject**: the governor's directive *"2D-ification Frontier Visualization — A Route of Phased Constraint
Relaxation and Presentation Fidelity"* (Phase 0–4, four invariants). Registered verbatim at
`docs/decisions/phased_relaxation_route_v2.md`.

**Question the checks answer**: is each phase's *gate* decidable, and does each phase's *relaxation target* name an
object that exists in the adopted specification `docs/specs/meff_boundary_v0_2.md`?

**Registered inputs** (all from the record, none chosen here):

| Symbol | Value | Source |
| --- | --- | --- |
| `d_∥` | `15.40e-15 m` | roadmap §3.4; registry §2 (`C1`) |
| `A_⊥` (2D state) | `324.9e6 m²` | `unfold_is_real_v1.md` |
| `H_slab` (¬C1 object) | `0.070 m` | `staged_relaxation_visual_route_v1.md` §9 |
| `N_layers` | `8.12e9` | census, v0.2 ME4 |
| `N_plates` | `1.18e10` | census, v0.2 ME4 |
| `χ(intact)` / `χ(2D)` | `2` / `1.18e10` | v0.2 ME4, Q5 |
| `c` | `2.99792458e8 m/s` | CODATA (SI) |

**Model used for `μ_ov`** (v0.2 ME1, unchanged): over a column, `μ_ov = 1` when two material points exist with
`|z₁ − z₂| ≥ Δz_res`, else `0`; averaged over `A_⊥`. For the three registered objects the column content is
one interval, so `μ_ov = [thickness ≥ Δz_res] · coverage`, with `coverage = 1` (fully covered columns).

---

## Checks

**R1 — where does ME1 switch, and what margin does the ideal 2D state have?**
Evaluate `μ_ov(Δz_res)` for the ideal sheet (`thickness = d_∥`) at `Δz_res = {d_∥/10, d_∥, 10d_∥, 1e3 d_∥}`.
*Registered expectation*: `μ_ov = 1` at the first two, `0` at the last two, i.e. a step at `Δz_res = d_∥`.
*Falsifies the claim "the gate is evaluable as written"* if the switch location differs from `d_∥` by more than
one part in `1e-12`, **or** if the ideal state does not sit exactly on the step.

**R2 — is ME1 vacuous at macroscopic resolution?**
Evaluate ME1 for the **¬C1 object** (the intact `0.070 m` slab, no conversion at all) at
`Δz_res = {1e-6, 1e-3, 1e-1} m`.
*Registered expectation*: `μ_ov = 0` (ME1 **PASSES**) at `Δz_res = 1e-1 m`.
*This is the falsifier for non-vacuity (v0.2 C-2.2, `ℳ_eff ≠ 𝒫`)*: if an entirely un-2D-ified object passes the
2D-ness gate, the gate does not test 2D-ness.

**R3 — do the ME and CM domains stay disjoint for `ME1`?**
`CM1` (contrast criterion, §6.1) is "is the third-dimension thickness resolvable? (`d ≪ λ`)". `ME1` is
"`thickness < Δz_res`". Enumerate {ideal sheet, 2-sheet stack, intact slab} × {scale = `d_∥/2`, `d_∥`, `2d_∥`}
and compare the two verdict maps under the identification `λ ↔ Δz_res`.
*Registered expectation*: `9/9` agreement, i.e. the two predicates are the **same predicate**.
*Significance if confirmed*: registry §5 asserts `ME` and `CM` are "disjoint by construction" and that a
constraint can never be evaluated on an observation channel. R3 tests that assertion directly.

**R4 — is Phase 1's rollback trigger attributable?**
ME4 requires `N_comp` non-decreasing and the census matching `1.18e10` plates, and v0.2 records
`χ(2D) = 1.18e10 ≠ χ(intact) = 2`. Count the minimum number of `χ` discontinuities any ME4-compliant trajectory
must contain, and state whether Phase 1's rule ("jump in `χ` ⇒ roll back") can distinguish a jump caused by
relaxation from a jump required by the physics.
*Registered expectation*: `≥ 1` discontinuity is unavoidable, so the rule requires a counterfactual (relaxed vs
unrelaxed run at the same stage) that the directive does not specify.

**R5 — does the adopted ME5 contain `Λ_max`, and can its falsification clause fire?**
Grep the adopted spec for `Λ_max` / `Lambda`; evaluate `t_rip = √2 L / c` for `L = {0.20, 1.00, 0.070, 1e-3} m`;
compute the fastest conversion admitted by a rate cap `Λ_max = 1e-3 s⁻¹` and its ratio to `t_rip(L = 0.20 m)`.
*Registered expectation*: `Λ_max` absent from the adopted spec (it belongs to the declined alternative ME5);
`t_rip > 0` for every `L > 0`, so "zero sheet survival time" is satisfiable only at `L = 0`; and the fastest
cap-admitted conversion is `≫ 1` times slower than `t_rip`, i.e. the cap admits only un-photographable cases.

**R6 — does relaxing ME2 move ME1?**
Take the ideal sheet at `Δz_res = d_∥` (`μ_ov = 1`, FAIL). Relax the ME2 tolerance `Δz_tol` by factors
`f = {1.001, 1.01, 1.1, 2}` and ask what `Δz_res` the presentation can then justify (`Δz_res' = f·Δz_res`), and
hence `μ_ov'`.
*Registered expectation*: `μ_ov` flips to `0` already at `f = 1.001`. If so, Phase 3 — labelled "relax ME2" —
relaxes **ME1** as a side effect, which is exactly what the directive's own General Principle declares invalid.

**R7 — is the invariant "VIOLATION = 0" defined?**
Check whether the token `VIOLATION` exists in `src/common/symbol_lint.py` and whether `MUST-FIX` exists in
`src/common/provenance_lint.py`; report each tool's blocking class and its count.
*Registered expectation*: neither token is shared, so the invariant names a field that one of the two tools does
not emit; the enforceable form must be stated per tool.

---

## Falsification

If R2 does **not** show the intact slab passing, my principal claim (ME1 is vacuous at macroscopic resolution)
is withdrawn, not re-interpreted. If R3 does not give `9/9`, the domain-collision claim is withdrawn. If R1's
switch is not at `d_∥`, the "zero margin at the ideal state" claim is withdrawn. Each check is reported with its
own verdict; a failed prediction is recorded as `PREDICTION FAILED` and stands.

---

## R8 — added 2026-11-22, registered **before** running it

**Why added.** R1–R7 locate the Phase 0 blocker but supply nothing. `Δz_res` has one candidate value already in the
record that is *not* chosen for ME1's benefit: the S0 bookkeeping's own voxel size, `100 μm`
(`docs/decisions/painting_render_v1.md`, phantom resolution). R8 tests whether that value makes the gate decidable
and non-vacuous at once.

**Check.** With `Δz_res = 1.0e-4 m`, evaluate ME1 for the ideal sheet, the 2-sheet-thick stack and the intact slab,
and report the two margins `Δz_res/d_∥` and `H_slab/Δz_res`.

*Registered expectation*: ideal sheet `μ_ov = 0` (PASS); intact slab `μ_ov = 1` (FAIL); both margins `≫ 1`.
*Falsifier*: if the intact slab also passes at `100 μm`, Option A fails and V1 has no resolution that preserves
non-vacuity.
