# Audit — phased relaxation route v2 (governor's directive)

**Date**: 2026-11-22
**Subject**: `docs/decisions/phased_relaxation_route_v2.md` (registered verbatim, §1)
**Method**: each phase gate is checked for *decidability* and each relaxation target for *existence in the adopted
specification*. Seven predictions registered before execution
(`runs/S45/phased_route_checks_registration.md`), results in `runs/S45/phased_route_checks_results.txt`. All seven
confirmed, plus R8 added and registered before running it.
**Evidence level**: ARITHMETIC / IDENTITY. **No physics result, no numerical verdict, no threshold changed.**

---

## A. Verdict summary

| # | Finding | Phase | Severity |
| --- | --- | --- | --- |
| **V1** | `Δz_res` alone decides ME1, is unregistered, and is absent from the directive's prohibited list. The ideal 2D state sits *exactly on* ME1's step (zero margin) | 0 | **blocking** |
| **V2** | Phase 1's target — "local injectivity neighbourhood radius" — is not a parameter of ME1, and by invariance of domain the object it names does not exist | 1 | **blocking** |
| **V3** | Phase 1's rollback rule fires on a `χ` jump that ME4 *requires*, and has no attribution rule | 1 | **blocking** |
| **V4** | Phase 2 "unfreezes" ME5, which is FROZEN and exact; `Λ_max` is not a parameter of the adopted ME5 (0 occurrences) but of the **declined** alternative | 2 | **blocking** |
| **V5** | Phase 2's falsification clause cannot fire (`t_rip > 0` for every `L > 0`); its clock `τ` collides with the Drude `τ` | 2 | high |
| **V6** | Phase 3 names ME2 but describes `C_phys`→`ME3`'s content, and the predicate it specifies is `C`-domain (S1 violation) | 3 | **blocking** |
| **V7** | The ladder's *order* contradicts the ratified v1 ladder: it relaxes `C1`/`ME1` first and contains **no `C2` relaxation at all** | route | **governor decision** |
| **V8** | Invariant 3 names a field one of the two tools does not emit | invariants | low (fixed §F) |

**The structural reading.** Read literally, Phases 1–3 act on `Δz_res` and `Δz_tol` — two depth *scales of
measurement* — not on physics. That is the General Principle's own prohibition ("display conventions must not be
used to mask physical gaps") applied one level up: the route's relaxation axis, as written, is a *rendering* axis
carrying constraint labels. Phase 3 is the exception: it clearly *intends* a physical relaxation and merely names
the wrong object. So the repair is not to abandon the ladder but to re-letter its rungs (V2, V6) and to register
the one parameter that is doing all the work (V1).

---

## B. V1 — Phase 0's gate is decided by an unregistered parameter

**The defect.** ME1 is `μ_ov ≤ δ_ov` with `μ_ov` evaluated at a *declared* depth resolution `Δz_res`. For any
object whose columns contain one material interval — which is every object in the record, since the converted
state is `1.18e10` **coplanar** plates — this reduces to

```
μ_ov = [ thickness ≥ Δz_res ]
```

so **the entire content of ME1 is a comparison between the object's thickness and `Δz_res`.** `Δz_res` is declared
per use (v0.2 ME1) and is not on the directive's list of OPEN parameters (`δ_ov`, `ℓ_samp`/`Δz_tol`, `δ_E,max`).
The prohibition therefore guards every parameter *except* the one that decides the gate.

**Measured (R1, R2).**

| Object | `μ_ov` at `Δz_res = 10⁻⁶ m` | `10⁻³ m` | `10⁻¹ m` |
| --- | --- | --- | --- |
| ideal 2D sheet (`15.4 fm`) | 1 (FAIL) | 1 (FAIL) | 0 (PASS) |
| **intact 7 cm slab, zero conversion** | 1 (FAIL) | 1 (FAIL) | **0 (PASS)** |

The resolutions the two objects need differ by `6.49e12`. At `Δz_res = 10 cm` an entirely un-2D-ified body passes
the 2D-ness gate; at `Δz_res = 1.54e-14 m` the *ideal* state fails. **Both verdicts are available to the same
object**, and no registered rule picks between them.

**The second half, which is worse.** The switch is at `Δz_res = d_∥` — the plate's own thickness — and the ideal
state sits *on* it, with margin exactly zero, because the criterion is `≥` and the column's two faces are exactly
`d_∥` apart. So ME1 is not merely resolution-dependent; at its only non-vacuous setting it has **no attained
minimum**: the pass set is the open interval `(d_∥, ∞)`. A constraint whose satisfaction requires an arbitrary
coarsening beyond a knife edge cannot be a gate; it is a calibration knob.

**Consequence for Phase 0.** The gate is undecidable as written, and the phase's own prohibition forbids doing the
one thing that would make it decidable (choosing a `Δz_res`). This is not a contradiction in the governor's
intent — it is a gap in the *specification*, one level below the directive.

### Proposed resolution (needs one governor ruling)

**Option A (recommended).** Register `Δz_res` **once**, as an *instrument* parameter of the S0 product, derived
from the bookkeeping data's own voxel size — `100 μm`, already in the record (`painting_render_v1.md`) — and
declare that Phase 4's FL enhancement may change *rendering* but may never change `Δz_res`. R8 evaluates this:

| Object | `μ_ov` at `Δz_res = 100 μm` | verdict |
| --- | --- | --- |
| ideal 2D sheet | `0.0` | PASS |
| 2-sheet stack | `0.0` | PASS |
| **intact 7 cm slab** | `1.0` | **FAIL** |

Decidable, and **non-vacuous**: ME1 separates the 2D state from the intact body by `4.5e12` in thickness. Nothing
is chosen to make a check pass — the voxel is a property of the data S0 already has, and it is *coarser* than the
plate by `6.5e9`, i.e. the value is unhelpfully coarse for ME1, not conveniently fine. The gate is then frozen: it
is evaluated once at Phase 0 and cannot be re-evaluated at Phase 1 (which is what makes Phase 1 a *relaxation*
rather than a re-measurement).

**Option B.** Reclassify ME1 out of the gate set, on the ground that a resolution predicate is an observation
predicate (V2a below) and therefore cannot be a member of the `ME` domain at all. Phase 0's gate would then be
ME4's census bookkeeping.

**Option C.** Take ME1 at `Δz_res = d_∥` and accept that the ideal state fails. This terminates the route at
Phase 0 and is reported only for completeness.

**Why A and not B.** B is correct about the physics and would dissolve a constraint the governor has already
adopted; A preserves it with its content intact and fixes only the missing declaration. But A is a *decision* —
it registers a parameter — so it is not mine to make.

### V2a — and ME1 is not in the `ME` domain anyway

A second finding, independent of the above. Registry §5 asserts the `ME` and `CM` domains are "disjoint by
construction" and that "a constraint may never be evaluated on an observation channel". `CM1` is *thickness
distinguishability: is the third-dimension thickness resolvable? (`d ≪ λ`)*. R3 evaluates both predicates over
three objects × three scales: **9/9 agreement**, and the agreement is structural, not statistical — both are
`[thickness < scale]` under `λ ↔ Δz_res`.

So `ME1` **is** `CM1` with a different letter. The disjointness claim in registry §5 fails for exactly the
constraint that Phase 0's gate depends on. This does not make ME1 wrong; it makes its *domain assignment* wrong.
`μ_ov` is a measurement of an object by an instrument, which is what the `CM` set is for.

---

## C. V2 — Phase 1's target does not exist

**"Only the relaxation of the local injectivity neighborhood radius is permitted."**

ME1's parameters are `Δz_res`, `ρ_thr` and `δ_ov`. There is no neighbourhood radius. And the object the phrase
names is not merely absent from the specification — it is mathematically empty: by **invariance of domain**, no
non-empty open subset of `ℝ³` admits a continuous injection into `ℝ²`. Hence for every point `p`, the largest
neighbourhood on which the projection is injective has empty interior, i.e. **radius zero**.

A quantity that is zero at every point cannot be relaxed downward. Phase 1 as written therefore has no admissible
relaxation, and its label `ME1′` is registered in the route document as **reserved with no definition** until its
target is re-specified in terms ME1 actually possesses.

**What Phase 1 can legitimately relax**, in increasing order of cost:

1. `δ_ov`: `0 → δ_bias`, where `δ_bias` is a *derived* finite-resolution estimator bias (v0.2 O6) — a presentational
   relaxation, since it changes what counts as "one material point".
2. `Δz_res`: upward — but per V1 this is a re-measurement, and per R6 it is also ME2's `Δz_tol` (V6a).
3. Nothing else. ME1 has no third handle.

Note that option 2 is exactly what the directive's own General Principle calls invalid, because it moves a second
constraint (ME2) in the same commit. Option 1 is the only clean relaxation of ME1, and its permissibility depends
on O6 being closed.

---

## D. V3 — Phase 1's rollback rule is unattributable

Phase 1: *"ME4 topological invariants remain piecewise constant. If the relaxation causes a jump in the Euler
characteristic, roll back immediately."*

ME4 requires `N_comp` non-decreasing to the census `1.18e10` plates, and v0.2 records `χ(2D) = 1.18e10` against
`χ(intact) = 2`. So **any** ME4-compliant trajectory contains at least one `χ` discontinuity — at least one, and
possibly `8.12e9` of them, one per layer interface. R4 confirms the count is `≥ 1` by construction.

Therefore the rollback rule must distinguish a jump *caused by the relaxation* from a jump *required by the
physics*, and it has no instrument for doing so. As written it is either:

- **vacuous** — every jump is attributed to fragmentation, so it never fires; or
- **lethal** — it fires at the first fragmentation event, i.e. at the correct physics, terminating the route.

The missing element is an **ablation**: the same stage run with and without the relaxed `ME1′`, differenced. That is
a well-defined experiment and the directive can adopt it in one sentence; without it the rule is undecidable.

---

## E. V4–V5 — Phase 2 touches a frozen exact identity

**V4.** Phase 2 is "the only phase permitted to touch ME5". Adopted ME5 is:

```
τ_exp ≤ t_rip = √2 L / c,        tolerance: FROZEN — exact and scale-free
```

It has **no `Λ_max`** (R5: zero occurrences of `Λ_max`/`Lambda` in `meff_boundary_v0_2.md`). `Λ_max` is a parameter
of the **declined** alternative ME5 (`meff_boundary_v0_2_alt_definitions_DECLINED.md`), whose review found it
*directionally inverted*: a rate **cap** bounds the duration from **below**, and R5 quantifies it — at
`Λ_max = 10⁻³ s⁻¹` the fastest admitted conversion is `1.06e12 ×` *slower* than `t_rip`. It is satisfied precisely
by the case L3 cannot image.

So "unfreezing" ME5 to calibrate `Λ_max` would re-import a retired, falsified formalisation. There is nothing in
ME5 to calibrate: it is an identity, `t_rip/(2L/c) = 1/√2` exactly, for every `L`.

**V5.** Phase 2's falsification clause — *"if the calibration results in a zero sheet survival time, this route
terminates"* — cannot fire. R5: `t_rip = √2L/c > 0` for every `L > 0`; zero requires `L = 0`, i.e. a point object.
A clause that can only trigger for an object with no extent is not a falsification condition.

**Also registered**: `τ` in Phase 2 ("the intrinsic time scale τ") would be a **second owner** of `τ`, which is
already the Drude relaxation time (`src/optics/sigma_s_lindhard.py`, `TAU_SCAN`, OPEN, scanned not solved). Under
R3 the new clock is registered as **`τ_conv`**.

**What survives of Phase 2**: the *intent* — the conversion needs a clock, and L3's survival window must be stated
on every frame. That intent is already discharged by ME5's corollary, which requires no calibration and forbids
nothing that is permitted.

---

## F. V6 — Phase 3 relaxes the wrong constraint, and in the wrong domain

Phase 3 is titled "Physical Quantity Boundary Relaxation (ME2)" and targets "the controlled scope of the Noether
symmetry breaking boundary", with the hard constraint that one non-trivial `J^μ` survive.

1. **ME2 is not that.** Adopted ME2 is *parallax at the declared sampling scale*: `ℓ_samp·‖∇z‖_∞ ≤ Δz_tol`. It is
   explicitly **presentational** — v0.2 says `Δz_tol` "belongs to the fidelity level (FL1/FL2/FL3), not to the
   physics".
2. **The intended object is ME3.** The adopted lineage maps `C_phys → ME3` (perpendicular energy fraction). A
   `Noether`-flavoured relaxation belongs to ME3, not ME2.
3. **The predicate as specified is `C`-domain.** A conserved current is a property of the matter sector, i.e. of
   `(γ_ij, K_ij, T_μν)` — the `C` domain. `S1` forbids it from being an `ME` predicate. This is the same defect the
   alt-definitions review recorded as **V4**: `δS_eff/δφ = 0` *is* the Euler–Lagrange equation and constrains
   nothing; conservation follows from a symmetry *transformation*, not a field variation.
4. **"At least one non-trivial `J^μ` retained" is the right instinct with no instrument.** Nothing in the record
   computes `J^μ` for this system. Stating it as a hard constraint is safe (it cannot be passed falsely) but it is
   not yet evaluable; it would need a registered current and a registered tolerance on its norm.

### V6a — why Phase 3 cannot be isolated from Phase 1

ME2's `Δz_tol` and ME1's `Δz_res` are both depth scales of the same observation. R6 quantifies the coupling: the
ideal sheet at `Δz_res = d_∥` fails ME1 (`μ_ov = 1`); relaxing the presentation tolerance by **0.1 %** permits
`Δz_res → 1.001 d_∥`, at which `μ_ov = 0` — **ME1 flips**. So Phase 3, as specified, incidentally relaxes ME1.

That is precisely the commit the General Principle declares invalid. The two constraints are not independent, and
the resolution is structural: whichever of `Δz_res`/`Δz_tol` is registered first owns the depth scale, and the
other must be *defined* as a function of it. Under Option A, `Δz_res` is frozen at `100 μm` at Phase 0 and
`Δz_tol` is then free — but only because ME1 no longer depends on it.

---

## G. V7 — the ordering conflict, which the executor does not resolve

| Source | First relaxation | Second relaxation | `C2` relaxed? |
| --- | --- | --- | --- |
| `staged_relaxation_visual_route_v1.md` §3 (ratified) | `C2` (S3, interlayer texture) | `C1` (S4) | yes |
| this directive, Phases 1–3 | `ME1`/`C1` | `ME2`/`ME3` | **absent** |

The ratified ladder relaxes the *cheapest* constraint first and keeps the most expensive for last; that ordering is
what made S3 a texture stage and S4 the naked-eye stage. The directive relaxes the `C1` object at Phase 1 and has
no `C2` phase at all. Both orderings can be argued; they cannot both be in force.

**I have not chosen.** Choosing would be exercising a governor's authority. The route document records the conflict
as open (§6) and every downstream artefact cites the route's phases with an explicit "ordering open (V7)" tag.

**One observation, offered as input rather than as a ruling**: the directive's General Principle — one constraint
per commit, FL never ahead of physics — is *better served* by the ratified order, because under it each relaxation
has a pre-existing physical product to be compared against (S3's texture arises from C2's registered interlayer
failure), whereas relaxing `C1` at Phase 1 leaves Phases 2–3 with nothing physical to relax.

---

## H. V8 — invariant 3, restated so it can be checked

`VIOLATION` appears 7× in `provenance_lint.py` and 0× in `symbol_lint.py`; the latter emits `MUST-FIX`. So
"the VIOLATION count for symbol_lint.py must be 0" names a field that tool does not produce. Enforceable form
(now in the route document §5, executed by `src/common/commit_gate.py`):

```
commit_gate = symbol_lint:     MUST-FIX(A,C,D) == 0
           ∧ provenance_lint: blocking(VIOLATION + MISSING + INCOMPLETE) == 0
```

Archived `runs/` hits are excluded from the symbol count because §9.1 forbids editing them — a gate that included
them would be permanently red for an unfixable reason. Current state: `0` and `0`. **F remains advisory**, since
`M1`–`M4` have five legitimate pre-existing owners (registry §2a) and a gate cannot retroactively invalidate them.

---

## I. What this audit does not do

- It does not change a threshold. `δ_ov`, `ℓ_samp`, `Δz_tol`, `δ_E,max` are still OPEN, and no value was supplied.
- It does not change a verdict: `C1` identity, `C2` interlayer failure, `C3` NO-GO, ME1–ME5, D-A, D-B all stand.
- It does not resolve V7, and it does not adopt Option A. Both are governor decisions.
- It does not evaluate any phase. It determines whether a phase *can* be evaluated — by locating, for each gate,
  the parameter or definition it is missing. Four of four gates are missing one.

---

## J. Decisions requested

**Label note (added 2026-11-22).** These items were first written `D-1`…`D-5`. That was a namespace error: `D`
already has two owners — gates `D2`/`D3`/`D5` and assumption `D2` (prescribed background, registry §2). A third
owner in the same table that discusses `C2` ordering, while `D2` is the crutch that ordering is about, is precisely
the collision class this project has renamed three times already (`P1–P6→Q1–Q6`, `M1–M5→ME1–ME5`, `C1–C4→CM1–CM4`).
Renamed to **`GD1`–`GD5`** (*governor decision*, R3-compliant two-letter prefix, previously unowned).

| # | Decision | Default if none |
| --- | --- | --- |
| **GD1** | Adopt Option A (`Δz_res := 100 μm`, frozen at Phase 0, FL may not move it) or Option B (reclassify ME1 as `CM`-domain and use ME4 for Phase 0's gate) | Phase 0 stays blocked; no S0 product can be issued with a gate verdict |
| ~~**GD2**~~ | ~~Resolve V7: ratified order (`C2` then `C1`) or directive order (`ME1` first, `C2` absent)~~ **WITHDRAWN by §K** — only one relaxation exists, so there is no ordering left to choose. Replaced by two bookkeeping items (crosswalk §5.6). | none — closed |
| **GD3** | Re-specify Phase 1's target as `δ_ov`/O6 (recommended) or as `Δz_res` (accepting that it moves ME2 too, and is therefore invalid by the General Principle) | Phase 1 stays undecidable |
| **GD4** | Reassign Phase 3 from ME2 to ME3, and record `J^μ` as an OPEN instrument rather than a gate | Phase 3 stays mislabelled |
| **GD5** | Accept the `τ → τ_conv` rename and the `Λ_max` retirement | The collision is recorded but unfixed |

**ALL FOUR LIVE ITEMS WERE RULED on 2026-11-22** — `GD1` = Option B, `GD3` = `δ_ov`/O6, `GD4` = accepted,
`GD5` = accepted. Authority: `docs/decisions/gd_rulings_v1.md`. The table below is kept as the record of what
was asked; its "default if none" column no longer applies. `GD1` Option B removes the blocker rather than
choosing a value, and it empties the gate column of the crosswalk (§1.4 of the ruling): with `CM5` in the
observation channel, no constraint in `{C1, C2, C3}` has a gate expression, and Phase 3 (`ME3`) becomes the
route's only physical relaxation — specifiable, not yet runnable.

**What is not waiting on a decision.** Phase 0's other deliverable — the colour convention declaration block — has
no dependency on any of the above and is delivered with this audit:
`docs/conventions/display_conventions_v1.md`. It makes the frequency-flatness finding enforceable rather than
advisory, which is the part of Phase 0 that does not need ME1.

---

*Content generated by AI*

---

## K. Addendum — V7 recharacterised after the crosswalk (2026-11-22)

The governor instructed a re-registration of `C1`/`C2` in the `ME`/`CM` system. The legal form is a **bridge**, not
a rename (`docs/conventions/constraint_crosswalk_v1.md`; checks X1–X6). Three findings bear on V7:

1. A rename is forbidden by `S1` in both directions and would delete `C2`'s content — `S_A` and `S_E`, differing
   only in intralayer strain, are **indistinguishable** to every `ME`/`CM` proxy (X2). The literal instruction
   would have produced a `C2` label that cannot see `C2`.
2. Only `1 of 3` chain constraints has a gate expression (X5), so V7's "two orders of one list" framing was wrong:
   the two ladders order **different lists**.
3. `S3` is not a relaxation under either reading of `C2` (crosswalk §5.2), and Phase 1 **is** `S4` under `S7`.

**Effect on V7's status**: the *conflict* is withdrawn — there is exactly one relaxation, so no ordering freedom
remains. Two bookkeeping rulings replace it (does S3 keep the word "relaxed"; is `C2` intralayer-only or full
smoothness), recorded as crosswalk §5.6. **No finding in §A–J changes**; V7's severity drops from *governor
decision* to *bookkeeping*.
