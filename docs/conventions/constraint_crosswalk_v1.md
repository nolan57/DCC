# Constraint ↔ gate crosswalk v1 — how `C1`/`C2` are cited in the `ME`/`CM` system

**Created**: 2026-11-22
**Status**: **ACTIVE.** Governs every text that cites a chain constraint in a gate context.
**Authority**: governor instruction ("re-register C1/C2 in the ME/CM system, bypassing the retired naming family,
then talk about ordering"); registry rules R1–R4, S1–S5; `docs/specs/meff_boundary_v0_2.md`.
**Checks**: `runs/S45/crosswalk_checks_registration.md` → `runs/S45/crosswalk_checks_results.txt` (X1–X6).
**Effect on physics**: none. No threshold, verdict, or number moves.

---

## 0. What is being re-registered, and what is not

**Disambiguation first (rule S1).** `C1`/`C2` here are the **ledger constraints** — effective two-dimensional
space, and smooth 2D-ification. They are not the localisation test IDs (`LOC-C1…LOC-C7`) and not the §6.1 contrast
criteria (`CM1…CM4`).

**The retired family is a different set of labels.** `C1`/`C2`/`C3` are the sole legal owners of `C` under R1/R2;
the retired v0.1 labels were *different* names (`C_`-subscripted) that R4 removed. So nothing about `C1`/`C2` needs
bypassing — they were never in the retired family, and no text in this document names a retired label. Verified:
`symbol_lint` rule D reports **0** hits here.

**What is being decided** is narrower and harder: whether `C1`/`C2` can be *written as* `ME`/`CM` labels. Two
operations are available:

| Operation | Form | Legal? |
| --- | --- | --- |
| **(a) rename** | `C1 → ME1`, `C2 → CM2` | **NO** — §1 |
| **(b) bridge** | keep `C1`/`C2`; register their *test expressions* at declared scales | **YES** — §2 |

---

## 1. Why the rename is refused — three independent reasons

**1.1 It is forbidden by `S1` in both directions.**
Registry §5 defines `ME` as predicates deciding membership of `ℳ_eff`, the **S3→S4 branch's** domain, and states:
*"An `ME` predicate may never be a chain constraint."* `C1` is cited by every S0–S2 gate. Renaming it to `ME1`
would make each of those citations an `ME` predicate used as a chain constraint — non-compliant on its face.
Symmetrically, `CM` holds observation/rendering predicates and `S1` states *"a constraint may never be evaluated
on an observation channel"*; `C2` is a statement about strain in matter, so a `CM` name would place a matter
predicate in the observation domain.

**1.2 It would delete `C2`'s content rather than rename it.** `S_A` (ideal sheet) and `S_E` (same sheet with an
intralayer strain field) differ **only** in strain. Every `ME`/`CM` proxy returns an identical verdict on the pair
(X2). So `C2` is *invisible* to the gate vocabulary: any `CM` label it were given would be a predicate that cannot
see the thing it is named after. Corroborated textually — the word `strain`, standing alone, occurs **0** times in
the adopted spec (X3).

**1.3 The blast radius is 160 citations.** `C1`/`C2` appear **132** times across 13 documents plus **28** in the
roadmap (X6). Registry `R2` awarded `C` to the constraints *precisely because* of that load — "cited by every gate
and every ledger row". A rename would re-register all 160, and every one would then violate `S1`. The rule that
chose the name is the rule that forbids changing it.

**1.4 `C3` cannot be expressed at all.** It is an in-action statement; the adopted spec contains no `T_μν`, no
`S_eff`, and no weak-interaction predicate (X4). `S1` forbids it an `ME` form regardless. `C3` may only be declared
*out of scope*, never traded.

---

## 2. What is registered instead — the bridge

Each constraint gets a **test expression** at a declared scale, with its logical relation and its domain. The
notation is directional and distinct from equality:

```
C1  ⇒ᵒ  CM1 @ λ               observation proxy (necessary, not sufficient)
C1  ⇒ᵒ  CM5 @ Δz_res          observation proxy (domain Δz_res > d_∥)   [was ⇒ᵍ ME1]
C2  ⊥   {ME} ∪ {CM}           no expression exists
C3  ⊥   {ME}  (⊘ {CM})        no expression, and forbidden one by S1
```

> **AMENDED 2026-11-22 (`GD1` Option B).** The `⇒ᵍ` row is **withdrawn**: `ME1` is now `CM5`, an observation
> predicate, so `C1` has no gate expression and **no constraint in the set has one**. The table below is kept
> as the record of the pre-ruling bridge; read every `ME1` as `CM5` and every `⇒ᵍ` as `⇒ᵒ`. Consequences in
> `docs/decisions/gd_rulings_v1.md` §1.4–§1.5, including why `Δz_res` is *not* frozen.

| Constraint | Gate expression | Relation | Domain of validity | What the expression loses |
| --- | --- | --- | --- | --- |
| **`C1`** | ~~`ME1 @ Δz_res`~~ → `CM5 @ Δz_res` (observation) | `C1 ⟹ CM5`, converse **false** | `Δz_res > d_∥` **only** (§3) | column conservation; the proxy sees only thickness. Passes a stack whose gaps are sub-resolution and a thin slab that conserves nothing |
| **`C1`** | `CM1 @ λ` | `C1 ⟹ CM1`, converse false | all `λ ≫ d_∥` — i.e. **vacuously** at optical `λ` (§3.3) | as above, plus 7.5 orders of magnitude of slack |
| **`C2`** | — | ⊥ | — | everything. No expression exists (X2) |
| **`C3`** | — | ⊥ / ⊘ | — | everything, and one is forbidden |

**X1's registered prediction partially failed and the claim is weakened accordingly.** At `Δz_res = d_∥` there are
**2** states with `C1` true and `ME1` false — because the ideal state's two faces are exactly `d_∥` apart and the
criterion is `≥`. So `C1 ⟹ ME1` is **not** unconditional: it holds on `Δz_res > d_∥` and fails at the knife edge.
The bridge is therefore registered with its domain attached, as promised in the pre-registration's falsification
clause, rather than being asserted unconditionally.

---

## 3. Where both proxies degenerate (this is the substantive finding)

**3.1 The gate proxy has a knife edge.** `ME1` is satisfied for the ideal state only on `Δz_res > d_∥`
(`runs/S45/phased_route_checks_results.txt` R1). So the bridge exists *exactly* on the gate's satisfiable domain
and nowhere else. Any statement of the form "`C1` holds because `ME1` passed" must carry the resolution, or it is
silent about the one parameter that decides it.

**3.2 The gate proxy is weaker than `C1` in a second way.** At `Δz_res = 100 μm`, `S_D` — a **two-sheet stack** —
passes `ME1` (X1 table). A resolution that cannot see a `4.6e-14 m` gap cannot see layering either, so `ME1` cannot
detect the very structure `C1` forbids. `ME1` certifies thinness, not single-valuedness, whenever the layering is
below the resolution.

**3.3 The observation proxy is vacuous at optical wavelengths.** `CM1` is `d ≪ λ`; with `λ = 500 nm` and
`d_∥ = 15.4 fm`, `λ/d_∥ = 3.2e7`. It passes by **7.5 orders of magnitude** for every candidate object. To make
`CM1` bite one needs `λ ≈ d_∥`, i.e. `E = hc/d_∥ ≈ 80.5 MeV` — a photon that destroys the object it is resolving.
This is the same degeneracy the audit recorded for the retired curvature criterion (Q4: passed by 4–18 orders) and
it is not repaired by renaming.

**Conclusion of §3.** `C1` has **no non-degenerate test at any scale present in the record**: the depth-resolution
test is unsatisfiable at its natural scale and vacuous above it, and the optical test is vacuously satisfied. This
is a statement about the *observability* of `C1`, and it is why the branch's membership question (audit V1) cannot
be settled by choosing a resolution — there is no resolution at which the test both bites and passes.

---

## 4. Rules (added to the registry as S6–S8)

**S6 — constraints are never written in a gate label.** A relaxation commit declares its subject in constraint
space (`C1`/`C2`/`C3`) or in gate space (`ME1`…`ME5`), and if in gate space it also declares the constraint it
proxies, or `proxy: none`. Form: `moves: C1 via ME1@Δz_res` / `moves: ME2 (proxy: none — presentational)`.

**S7 — a proxy relaxation is a constraint relaxation in effect.** Relaxing `ME1` does not change `C1`, but it
changes what the branch *certifies*, and for branch products certification is the only enforcement `C1` has.
Therefore `ME1`'s relaxation is recorded as `moves: C1 (proxy)` and may not be counted as a presentational step.

**S8 — `⊥` is a result, not a gap.** Where §2 records `⊥`, no label may be invented to fill it without a
definition that (i) decides `C2` on a pair differing only in strain, and (ii) survives the domain test of §2. A
`CM` label that cannot separate `S_A` from `S_E` is not a `C2` expression.

---

## 5. Ordering — the question that the bridge answers

The ordering conflict (audit V7) was: v1 relaxes `C2` then `C1`; v2 relaxes `ME1` first and has no `C2` step.
The bridge changes what the question is.

**5.1 Only one third of the diagonal is walkable in gate space.** `X5`: `1 of 3` constraints has an `ME` proxy. A
ladder indexed by `ME` labels therefore cannot be the constraint-relaxation diagonal — it can take at most one of
its steps, and that step (`C1` via `ME1`) is `S4`'s object.

**5.2 `S3` is not a relaxation under either reading of `C2`.** This is new and it dissolves the conflict rather
than adjudicating it. The registry defines `C2` as *zero intralayer strain*, while `S3` is described as rendering
**interlayer** discontinuities as texture. So:

- if `C2` means **intralayer** (§ the registry's words), `S3` does not touch `C2` at all — it relaxes nothing;
- if `C2` means **full smoothness** (intra **and** inter), then `C2` is already false for every real object
  (`8.12e9` broken interfaces, registered), so `S0` already fails it — and `S3` relaxes something that was never
  true.

Under the first reading `S3` is a **presentation** step; under the second it is an **admission**. Neither is a
constraint relaxation, and under neither does it belong *before* or *after* `C1` on a relaxation axis. **The
record contains no `C2` relaxation to order.**

**5.3 What the ladder actually contains, once re-registered:**

| Step | Subject (S6) | Category | Why |
| --- | --- | --- | --- |
| `S0` | — | baseline | `C1`+`C2`+`C3` held; `D2` carried and labelled |
| `S1` | — | tightening | bookkeeping completed |
| `S2` | `D2` discharged | **tightening** | prescribed → solved; rigor increases |
| `S3` | `C2` (proxy: none) | **presentation** | interlayer texture; buys no physics (§5.2) |
| `S4` | `C1` via `ME1` | **relaxation** | the only step that trades a constraint for visibility |
| — | `ME2` (`Δz_tol`) | **presentation** | explicitly fidelity-level-relative (v0.2 ME2) |

**5.4 The order is then forced up to the placement of presentation steps.** Tightenings precede relaxations
(otherwise a relaxation would be measured against an unrepaired baseline). There is exactly one relaxation, so
"which constraint first" has a one-element answer and no ordering freedom. Presentation steps buy no physics, so
their position is a rendering decision, not a ladder position — they may be interleaved anywhere after `S2`
without changing what the ladder establishes.

**5.5 Consequence for the directive's phases.** Phase 1 (`ME1 → ME1′`) **is** `S4` under S7 — not a distinct
earlier rung. Phases 2 and 3 move no constraint (§audit V5, V6). Phase 4 is presentation. So the directive's
five-phase ladder, re-registered through the bridge, is: *baseline → tighten → present → one relaxation → present*.
It is not a competing order; it is the same order with the rungs renamed to what they move.

**5.6 What is still the governor's to decide.** Two things, and only two:

1. **Whether `S3` keeps the word "relaxed".** Under §5.2 it is presentation or admission. Calling it a relaxation
   makes the ledger record a purchase that was not made. I recommend re-labelling it; the ruling is yours.
2. **Whether `C2`'s definition is intralayer-only (as the registry says) or full smoothness.** The two readings
   have different consequences for `S0`'s claim of "zero relaxation" (§5.2). I have not chosen.

---

## 6. If a rename really is wanted — the legal form

The only rename that does not violate `S1` is a **new ≥2-letter prefix for the constraint set itself**, e.g.
`PC1`–`PC3` (*physical constraint*), applied globally with the same blast-radius accounting as §1.3. That moves the
constraints *out of* `C` without moving them *into* `ME`/`CM`, so it satisfies R3 and leaves `S1` intact. It is
not what this document does, because it changes nothing semantically — it is cosmetics for 160 citations — and
because `C1`/`C2`/`C3` are not the family that needed bypassing. Say the word and it can be executed in one round.

---

## 7. What this document does not do

- It changes no threshold and no verdict. `C1` identity, `C2` interlayer failure, `C3` NO-GO, `ME1`–`ME5`, D-A,
  D-B all stand.
- It does not create an expression for `C2`. `⊥` is registered as a result (S8). (`CM5` exists as of 2026-11-22,
  but it is `C1`'s second observation proxy, not an expression of `C2` — crosswalk §2 amendment.)
- It does not settle audit `GD1` (`Δz_res`). §3 makes that decision harder to avoid, not easier: the gate's domain is
  now an explicit part of the bridge.
- It does not rule on §5.6. Both items remain open, and §5 is an analysis, not a decision.

---

## 8. What each status cell says — and one correction to the `ME1` input (2026-11-22)

Added when the governor asked for the constraint set to be stated plainly. No threshold moves; two cells are
qualified and one input is corrected.

### 8.1 `C1` — the number is conditional, and the label is not a test

`d_∥ = N_s^{-1/2}` is the **mean in-plane spacing** (`roadmap` v3 quantity table), i.e. the column pitch, not a
property of the material. It is fixed only once `(M, A_⊥, m̄)` is fixed: with the reference object
(`M = 70 kg`, `A_⊥ = 1 m²`, `m̄ = 10 amu`) it is `15.4 fm`. It scales as `(A_⊥/M)^{1/2}`. Quoting `2.91e-4 a_0`
without the reference object is therefore incomplete, exactly like quoting `A_crit` without `δ_info`.

"**ESTABLISHED (identity level)**" means: it follows from the definition of column density plus particle-number
conservation. It is **not** a dynamical result and it is **not** a passed test. §3.3 is the reason this distinction
is load-bearing — there is no non-degenerate test of `C1` anywhere in the record.

### 8.2 `C1b` — the quantity at `ME1`'s switch is convention-bearing (correction)

`ME1` compares `Δz_res` against a **thickness**. v0.2's definition identifies that thickness with the converted
plate's `d_∥ = 15.4 fm`. But `d_∥` is an *in-plane* quantity (§8.1), so the identification is a **modelling
choice**, not a derivation. The record knows this elsewhere and says so: `P_{2D}` is quoted **at a stated `L_z`**
(`8.6e25 Pa` at `L_z = 1 nm`; `8.6e31 Pa` at `L_z = 1 fm`) — six decades of spread in the same sheet.

Consequence, stated carefully:

- The **structure** of audit V1 does not depend on this. `Δz_res` alone decides `ME1` for any one-interval column,
  and the switch sits wherever the thickness is.
- The **numbers** do. The `6.49e12` resolution ratio and the `4.5e12` sheet-vs-slab separation are conditional on
  `thickness = 15.4 fm`. At `L_z = 1 nm` the ratio becomes `1.0e8`, and the ordering (sheet PASS, stack PASS, intact
  slab FAIL) is unchanged at `Δz_res = 100 μm`.
- **Registered requirement**: every `ME1` verdict must state `(thickness, its status as derived-or-convention,
  Δz_res)`. A verdict carrying only `Δz_res` is incomplete, because the quantity it is compared to is a choice.

### 8.3 `C2` — the cell is honest only under one of two readings

| Reading of `C2` | Does "holds intralayer" work? | What the `8.12e9` parenthetical then is |
| --- | --- | --- |
| zero **intralayer** strain (the registry's words) | **yes** — and it is an identity of the prescribed map (each layer is a rigid in-plane translation, `front_sweep_v1.md` §②) | **not a `C2` failure at all**; it belongs to the breakage ledger (`K5b`), not to `C2` |
| full smoothness (intra + inter) | **no** — `C2` is already **false** at `S0`, before any relaxation | the actual reason it is false |

So the cell is correct under the narrow reading and self-contradictory under the wide one. This is the open
bookkeeping item of §5.6, and it is the reason `S3` is not a relaxation under either reading.

### 8.4 `C3` — "parameter-independent" means *sign*, and it is a model result

Two witnesses, both sign-definite:

- `κ(ρ + p_x) = −γ(γ + h) < 0` for all `h, γ > 0` (`runs/R2/R2A_registration_v1.md`);
- for the prescribed background `(1/2, 1/2, −1/2)`: `t² κ(ρ + p_x) = −(1 + t²)/4 < 0` for all `t`.

No value of the free parameters makes it positive, which is what "parameter-independent" asserts. It must keep
"**in-action**" and "MODEL RESULT": this is a no-go *within the specified action* (Maxwell source), not a statement
about nature. Its correct downstream consequence is that the background can only ever be **prescribed** — which is
assumption `D2`, and why the ledger's earlier attribution "prescribed metric → `C3`" was corrected to `D2`
(`staged_relaxation_visual_route_v1.md` §7).

### 8.5 `RL-6` now carries §8.2's qualification — forward reference (2026-11-24, G-71-01 §1.1)

§8.2 above corrects `ME1`'s switch by naming the identification `thickness = d∥` a **modelling choice**. The same
choice is the denominator of `RL-6`'s price, and until this round the ladder's price column carried no such
qualification. It does now: `docs/specs/relaxation_ladder_v1.md` §2, the block immediately below the rung table,
states that `RL-6` assumes `d∥` serves as both in-plane column pitch and plate thickness, and that using `L_z`
as the independent thickness changes the ratio by `15.4 ×` (`2×10⁴` → `3.000e5`).

- The forward reference runs **ladder → here**, and this subsection is the reverse pointer. Reading either §8.2 or
  the ladder's qualification without the other leaves the same gap `AX-01` F-001 recorded.
- No number moves: `RL-6` stays `2×10⁴×`, `ME1` keeps its `REGISTERED REQUIREMENT` of §8.2, and the `1×` bar's
  ordering (`sheet PASS / stack PASS / intact slab FAIL` at `Δz_res = 100 μm`) is unchanged at every one of the
  three candidate lengths.
- Evidence: `runs/AX/ax01_axiom_audit_results.txt` `F-001`/`C-005`/`C-016`; repair record
  `runs/RR-DT/rr_dt_01_record_repair_results.txt`.

---

*Content generated by AI*
