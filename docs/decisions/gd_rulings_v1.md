# Governor rulings on `GD1`, `GD3`, `GD4`, `GD5`

**Registered**: 2026-11-22
**Authority**: project governor, answering `reports/reviews/phased_route_v2_audit.md` §J
**Status**: **ADOPTED.** Binds `Meff` spec v0.2, phased route v2, the crosswalk, and the registry.
**Amends but does not rewrite**: `docs/decisions/phased_relaxation_route_v2.md` (the directive is registered
verbatim and stays verbatim; the amendments live here and in a `§R` pointer inside that document).

---

## 0. The rulings

| Item | Ruling | Effect |
| --- | --- | --- |
| **`GD1`** | **Option B** — reclassify `ME1` out of the gate set; Phase 0's gate becomes `ME4` | `Δz_res` stops being a gate parameter. The blocker is *removed*, not resolved by choosing a value |
| **`GD3`** | Phase 1's target is **`δ_ov` / O6** | Phase 1 becomes an observation-strength declaration, not a physical relaxation (§3) |
| **`GD4`** | **OK** — Phase 3 reassigned to `ME3`; `J^μ` recorded as an OPEN instrument | Phase 3 is the only physical relaxation left (§4) |
| **`GD5`** | **OK** — `τ → τ_conv`; `Λ_max` retired | Phase 2's action must be re-specified; its falsifier becomes decidable (§5) |

---

## 1. `GD1` Option B — `ME1` leaves the gate set and becomes `CM5`

### 1.1 What was decided

`ME1` (`μ_ov ≤ δ_ov` at declared depth resolution `Δz_res`) is **not** a gate on a physical state. It is a
predicate over an observation channel, evaluated at an instrument resolution. It therefore belongs to the
`CM` family and is registered as **`CM5`** — resolution-relative injectivity, a sibling of `CM1` (thickness
distinguishability `d ≪ λ`) with `Δz_res` in place of `λ`. Phase 0's gate becomes **`ME4`** (fragment census).

`ME1` is retained as a **deprecated alias** for `CM5` in text written before this date. New text uses `CM5`.
The definition, the formula, and every number computed under `ME1` are unaffected — only its domain changes.

### 1.2 Why this is the correct kind of fix

Option A would have frozen `Δz_res := 100 μm`, i.e. it would have made the gate decidable by **choosing the
one number that decides it**. Option B removes the number's gate role instead. `ME4` needs no free parameter:
its census is FROZEN (`8.12×10⁹` layers × `1.457` components/layer = `1.18×10¹⁰` plates). So Phase 0 stops
waiting on a threshold that was never registered, and no threshold had to be invented to unblock it.

### 1.3 What Phase 0 can now certify — and it is less than it looks

`ME4` has three clauses. At the baseline state (no conversion yet) each behaves differently:

| `ME4` clause | At S0 baseline | Status |
| --- | --- | --- |
| 1. `N_comp` non-decreasing in swept volume | vacuous on a single state; needs a sweep sequence | **not testable at Phase 0** |
| 2. census match at `φ_conv → 1` | endpoint not reached (`N_comp = 1 ≪ 1.18×10¹⁰`) | **not applicable at Phase 0** |
| 3. no new topology (no handles; contractible) | testable: the body is genus 0, `χ = 2` | **this is what the gate tests** |

So Phase 0's gate certifies **"no handles created"** — a no-tearing condition — and **cannot** certify that a
state is two-dimensional. That is not a regression: `S1a` had already established that `ME1` could never
certify it either (it certifies thinness relative to a stated resolution, and it passes a two-sheet stack whose
gaps are sub-resolution). **We did not lose a test; we removed a false entitlement.**

**Binding wording for every Phase 0 product.** It may state: *no handles created; census endpoint not yet
applicable; resolution-relative injectivity reported separately as `CM5 @ Δz_res = …`.* It may **not** state
that the state is two-dimensional, or that it is a graph.

### 1.4 Consequence for the crosswalk: the gate column is now empty

`C1 ⇒ᵍ ME1 @ Δz_res` is **withdrawn**. `CM5`, being an observation predicate, enters only as `⇒ᵒ`. So:

```
C1  ⇒ᵒ  CM1 @ λ                  (vacuous at optical λ, 7.5 decades of slack)
C1  ⇒ᵒ  CM5 @ Δz_res             (domain Δz_res > d_∥; knife edge at Δz_res = d_∥)
C2  ⊥   {ME} ∪ {CM}
C3  ⊥   {ME}  (⊘ {CM})
```

**No constraint in the set now has a gate expression.** This is a statement about the record, not a defect
introduced by the ruling: `C2` and `C3` never had one, and `C1`'s was the one `S1a` proved could not carry
the weight placed on it.

### 1.5 `Δz_res` is not frozen and stays OPEN

Option A's `100 μm` is **not** adopted. `Δz_res` remains a per-verdict declared parameter, and
`constraint_crosswalk_v1.md` §8.2's requirement stands: every `CM5` verdict states
`(thickness, derived-or-convention, Δz_res)`. A `CM5` verdict carrying only `Δz_res` is incomplete; one
carrying none is not a verdict.

---

## 2. `GD3` — Phase 1's target is `δ_ov` / O6

### 2.1 What is now specified

Phase 1 relaxes `δ_ov`, the tolerance in `μ_ov ≤ δ_ov`. The spec's existing rule governs the relaxation:
`δ_ov = 0` is the physical criterion; a non-zero `δ_ov` is admissible **only as an estimator bias, derived
from the estimator**. So Phase 1's deliverable is a *derivation*, not a number.

### 2.2 The falsifier, registered now (before any derivation)

`δ_ov` must be **independent of the object under test**. If a derivation produces a `δ_ov` that varies with
the test state (plate, stack, intact slab), it is a fitted parameter, not an estimator bias, and Phase 1
fails. This is the checkable content of "derived, not chosen".

### 2.3 What Phase 1 is *not* — and this changes the ladder

With `GD1` Option B, `δ_ov` is a parameter of `CM5`, an observation predicate. Relaxing it changes what an
**observer at a stated resolution** may claim; it does not change what the **branch certifies**. Registry
`S7` said the opposite ("a proxy relaxation is a constraint relaxation in effect") on the premise that
`ME1` was `C1`'s only enforcement. That premise is now false, so `S7` is amended in §6 below.

Phase 1 is therefore registered as an **observation-strength declaration**: `moves: none (proxy: CM5 @ Δz_res;
observation channel)`. It relaxes no constraint in `{C1, C2, C3}`.

---

## 3. `GD4` — Phase 3 is `ME3`, and `J^μ` is an OPEN instrument

Phase 3's target is `ME3` (perpendicular energy fraction), as recommended. Two consequences:

1. **Phase 3 is now the only physical relaxation in the whole route.** `C1` has no gate expression (§1.4),
   `C2` has none (`⊥`), `C3` may only be declared out of scope. The relaxation step that exists is
   `ME3`'s `δ_E,max`, i.e. the `C_phys` successor — not `C1` and not `C2`.
2. **`J^μ` becomes an instrument, so its "hard constraint" is currently a declaration.** The directive says a
   zeroing of the conserved current is a failure and "approximate conservation" is not accepted. With `J^μ`
   OPEN, nothing can test that yet. Under invariant 4 ("no check that has not been run may be pre-registered
   as passed"), Phase 3 is **specifiable but not runnable**: `δ_E,max` is also OPEN. This is recorded, not
   worked around.

---

## 4. `GD5` — `τ_conv` adopted, `Λ_max` retired

`Λ_max` does not exist in adopted `ME5` (0 occurrences); it belongs to the declined alternative, whose rate
*cap* is directionally inverted (it is satisfied by a config `1.06e12 ×` too slow to photograph). Retiring it
removes Phase 2's stated action, so Phase 2 is re-specified:

- **Clock**: `τ_conv` (never bare `τ`, which is the Drude relaxation time).
- **Action**: declare which clock a frame uses and verify `τ_exp ≤ t_rip = √2 L / c`. There is no rate
  constant to calibrate, because adopted `ME5` is an exact identity with none.
- **Falsifier, restated (decidable)**: the route terminates if **no admissible exposure exists** for the
  declared fidelity level — i.e. `τ_exp,min(FL) > t_rip`. The directive's original wording ("if the
  calibration results in a zero sheet survival time") was unsatisfiable rather than strict: `t_rip = √2L/c > 0`
  for every `L > 0`, so it could only fire at `L = 0`. The restatement keeps the intent — no route past an
  unimageable sheet — and makes it fire on a reachable condition.

---

## 5. Net effect on the route

| Phase | Was | Is now | Relaxes a constraint? |
| --- | --- | --- | --- |
| 0 | gate `ME1`, blocked by `Δz_res` | gate `ME4`; certifies **no handles**, not 2D-ness | no |
| 1 | "geometric relaxation `ME1 → ME1′`" | `δ_ov` derivation; observation-strength declaration | **no** |
| 2 | "calibrate `Λ_max`" | declare clock; verify `τ_exp ≤ t_rip` | no |
| 3 | `ME2` (presentational) | `ME3` (physical) — **the only relaxation** | **yes**, once `δ_E,max` and `J^μ` exist |
| 4 | FL1→FL2→FL3 | unchanged; still strictly postponed | no |

The staged-relaxation discipline ("relax one constraint at a time") is unaffected in form and now has exactly
one member. Phases 0–2 are declarations and gates; Phase 3 is the relaxation; Phase 4 is presentation.

---

## 6. Amendments this ruling forces

1. **Registry `S7` is amended.** It asserted that a proxy relaxation is a constraint relaxation *because*
   `ME1` was `C1`'s only enforcement. With `ME1 → CM5`, relaxing `CM5` moves nothing in constraint space.
   New wording in `symbol_registry.md` §5.
2. **Registry entries.** `ME1` → vacated (deprecated alias of `CM5`); `CM5` registered; the `ME` set is now
   four members (`ME2`–`ME5`) and **`ME1` is not a gap to be refilled** — reusing it would recreate the
   conflation the ruling removed.
3. **`ME1′`** (reserved for Phase 1) is **withdrawn**: Phase 1's target is `δ_ov`, a parameter of `CM5`, not a
   relaxed `ME1`. Reusing `ME1′` would describe a successor of a label that no longer exists.
4. **v0.2** carries a reclassification banner on `ME1` and, in the summary table, `CM5` as an observation
   channel entry.
5. **Crosswalk** §2 bridge table and §3 wording updated per §1.4.
6. **Audit §J** records all four items as decided, with this document as the authority.

---

## 7. What this document does not do

- It does not move any threshold. `δ_ov`, `ℓ_samp`, `Δz_tol`, `δ_E,max` remain OPEN; `Δz_res` remains OPEN and
  is now explicitly *not* a gate parameter.
- It does not change any archived run product. `runs/S45/phased_route_checks_results.txt` and
  `crosswalk_checks_results.txt` used `ME1` under its old domain; they remain valid *as records of what was
  computed*, and their labels are read as `CM5` under this ruling. No archived stdout is edited (§9.1, P6).
- It produces no physics result. Evidence level: **RULING** (governance), plus the arithmetic already on file.

---

*Content generated by AI*
