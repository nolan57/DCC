# Goal conformance of the staged route — review v1

**Date**: 2026-11-22
**Trigger**: governor question — "check this — isn't this the goal of the roadmap?" — with the goal sentence restated.
**Question being answered**: is the route's objective the presentation of a 2D-ification scene along a
constraint-relaxation diagonal, and does the executed route reach it?
**Registration**: `runs/ROUTE/goal_conformance_registration.md` (predictions fixed before the run).
**Product**: `runs/ROUTE/goal_conformance_results.txt` (`src/route/goal_conformance.py`).

> **Status update 2026-11-22, same day (`docs/decisions/gd7_gd8_execution_v1.md`).** Two of this review's five gaps
> were closed by governor ruling. **`G2` (continuum) is now satisfied** — `GD7` fixed `FL` as faithfulness and the
> coordinate is defined and measured (`FL3 = 0.0000 > FL2 = −3.1011 > FL1 = −16.1344`, continuous). **`G4`'s
> "UNRESOLVED" is resolved as to its premise**: `GD8` kept `2L/c` and wrote in `D = L`, which covers the naked eye a
> fortiori. What remains open is `G1` (no citable depiction — **partially closed 2026-11-22, see §5**), `G3` (zero relaxations) and `G5`'s missing gate
> integration — plus a **new** decision, `GD9`, created by `GD7`: maximising `FL` terminates the route at zero
> relaxation, so the objective needs a joint form. The findings below stand as recorded; §0's tally is superseded on
> `G2` and `G4` only.

---

## 0. Answer

**Yes — that is the goal, and it is registered verbatim, not paraphrased.** It stands at
`docs/decisions/staged_relaxation_visual_route_v1.md` §1, in the governor's own words:

> "Present the physical scene of a three-dimensional macroscopic object being swept by a two-dimensionalization
> front. Presentation fidelity is **a continuum**, and the project commits to walking the **entire diagonal** of the
> constraint-relaxation axis: from *digitally-enhanced discernibility under all constraints* to *naked-eye
> visible-light reflection presentation under the minimal constraint set*. Enhancement (band migration, false
> colour, contrast stretching, shadowgraph, transmission channel, time compression) is permitted. **Enhancement must
> not introduce information that does not exist physically.**"

The ladder that expresses it is the same document's §3 (`FL1` / `FL2` / `FL3`), and v2's Phase 4 (`FL1 → FL2 → FL3`)
is that ladder. So the objective has not drifted, and no document contradicts it.

**But the route has not reached it, and the previous round's "route executed as far as it can be" was a true
statement about the *ladder* and a false one about the *goal*.** Of the five things the goal requires, **zero are
fully satisfied**: one is partial, two are absent, one is undecidable from the registered text, and one now has an
instrument where it had none.

| Requirement | Status | The gap, in one line |
| --- | --- | --- |
| **G1** depict a 3D object swept by a 2D front | **PARTIAL** | depictions exist — but they show the *unfolded end state*, not the sweep, and none is citable |
| **G2** fidelity is a continuum | **ABSENT** | `FL1`–`FL3` are labels; no coordinate, and the two candidate readings order them oppositely |
| **G3** walk the entire diagonal | **ABSENT** | **0** executed constraint relaxations |
| **G4** naked-eye reflection at the minimal set | **UNRESOLVED** | the corollary that "refutes" it carries an unstated premise (`D = L`) |
| **G5** enhancement adds no non-existent information | **INSTRUMENT** | built and negative-tested this round; was declaration-only |

The important part is not the score. It is that **four of the five gaps are not effort gaps** — they are a missing
metric (`G2`), a missing product class (`G1`), an ambiguity in a word (`G4`/`GD8`), and a missing test (`G5`). Only
`G3` is a work gap, and `G3` is blocked by the same two things.

---

## 1. What was measured, and why quoting the goal is not a verification

Restating a goal proves nothing. The goal contains four mechanically checkable claims and one channel claim, and
none of them had ever been evaluated:

| check | what it asks | method |
| --- | --- | --- |
| **G-1** | does each requirement have an artefact at all? | census of products per requirement |
| **G-2** | can the existing frames be cited under the project's own rule? | image census vs `.display.txt` sidecars |
| **G-3** | is the corollary's refutation of `G4` sound as written? | algebraic re-derivation of the premise |
| **G-4** | is the fidelity axis *ordered*? | Pareto order on the registered deficits |
| **G-5** | can "no information added" be tested? | two-branch instrument + negative test |

## 2. Findings

### F1 — Depictions exist, and they were never made citable

`runs/ANALYSIS/unfold_appearance_v1.png` contains, as panel D-left, an actual frame titled *"what the naked eye sees
(reflected visible light)"*, and as panel D-right *"what the 284 eV detector sees"*. `painting_render_v1.png`
contains the same tile mapped at 550 nm / 284 eV / 4 keV. **The two endpoints of the goal's diagonal are already
pictured.**

Two things disqualify them, and neither is a physics failure:

1. **They are not citable.** Only `runs/ROUTE/s0_frame_fl1.png` carries a `DISPLAY-DECLARATION` block. **26 of 27
   images have none** (`DC1`: *"a frame without a valid block may be viewed but may not be cited, quoted, or placed
   in any report. It is not a product."*). DC1 coverage is **1/27 = 3.7 %**.
2. **They show the wrong moment.** Both depict the *unfolded spread* — 70 kg over 325 km², the state after the front
   has passed. The goal asks for *the front passing*. That is `G3`'s missing product, and it is a different
   object from the one on file.

**A validator defect accompanies this.** `display_lint.py` walks `*.display.txt`, so it validates the blocks that
exist and is **structurally blind to images that have none**. DC1 is therefore enforced only from the side where it
is already satisfied. This is the same shape as the earlier `provenance_lint` defect (a control that stays silent
until tested), and it should be fixed by enumerating images and reporting the missing side.

### F2 — The fidelity axis has no coordinate, and its two readings reverse it

The goal's word is *continuum*. There is no continuum: `FL1`, `FL2`, `FL3` are three names. Two readings are
available, and **they order the ladder in opposite directions** — computed from Phase 2's own numbers, no new physics:

| channel | time deficit (decades) | flux deficit (decades) |
| --- | --- | --- |
| transmission 284 eV | 0.0000 | 1.9795 |
| transmission visible | 0.0000 | 9.9795 |
| reflection visible | 0.1505 | 9.9901 |

- **Reading A — fidelity = how much the frame shows.** 284 eV transmission *strictly dominates* reflection-visible
  on both coordinates. So `FL2` is the Pareto maximum and **`FL3` is strictly dominated**: the ladder **descends**
  toward its declared end point.
- **Reading B — fidelity = how close the frame is to the unaided retinal image.** Unmet conditions out of four:
  `FL1` 4/4, `FL2` 2/4, `FL3` 0/4. The ladder **ascends**.

Every quantitative criterion in the repository — CNR, photon counts, exposure budget — measures **Reading A**. The
goal sentence states **Reading B** ("to naked-eye visible reflection presentation"). `staged_relaxation_visual_route_v1` §9
already registers a related point (*"presentation fidelity and fidelity to the 2D-ification hypothesis are
anti-correlated"*), but §9 attributes the anti-correlation to the **object changing** at ¬C1. This finding is
sharper and independent of §9: **the ladder reverses even at fixed object**, because "fidelity" itself has two
opposite senses. Anti-correlation is a consequence, not the mechanism.

Reading A's verdict is robust to `F3`: the flux coordinate does not depend on the observation distance, and
transmission-visible also dominates reflection-visible there. The ordering reversal does not go away when the
geometric error is corrected.

### F3 — The corollary's refutation of `G4` rests on an unstated premise `D = L`

The frozen identity is correct and is **not** attacked:

```
t_rip = √2 L / c         2L/c = √2 t_rip          (ratio 1.414213562373, every L)
```

The **inference** is what carries a premise. `L` appears twice: once as the *object size*, which sets the
destruction path `√2 L`; once as the *optical path*, `2L`. The optical path for a camera at distance `D` is `2D`,
and it equals `2L` **only when `D = L`**. `D` is an observation geometry, and no registered text states it.

Per patch — a patch at distance `d` from the tear origin converts at `d/v_front`, with `v_front = L/t_rip = c/√2`
(the Phase 2 definition, not a new front speed) — the condition is

```
2D/c ≤ d/v_front    ⇔    D ≤ d/√2
```

so the admissible set is the annulus `d ≥ √2 D`: strictly **beyond 54.7356° off the camera axis**, non-empty **iff
`D < L/√2`**. Covered fraction of the radial extent is `1 − √2 D/L`:

| `D/L` | admissible | covered fraction |
| --- | --- | --- |
| 0.05 | yes | +0.9293 |
| 0.25 | yes | +0.6464 |
| 0.50 | yes | +0.2929 |
| 1/√2 = 0.7071 | boundary | 0.0000 |
| **1.00** | **no** | **−0.414214** |

**The registered corollary is the `D = L` row, and its covered fraction is negative.** A negative admissible extent
is not a physical impossibility; it is the signature of an observation geometry outside the window. Reading it as
"impossible for any `L`" substitutes a parameter choice for a result — the fifth instance of this project's
recurring defect class (cf. `P0d`'s `t − h_v`, `ME1`'s knife edge, `Λ_max`'s reversed inequality).

**What this does not do.** It does not make naked-eye reflection feasible. At `L = 0.20 m` the maximum camera
distance is `0.1414 m` and the frame covers at most 65 % of the radial extent; an observer beyond `0.1414 m` sees
nothing of the sheet, and a *naked-eye* observer is necessarily far. So `G4` remains **unresolved**, not "possible".
The correct statement is: *reflection is admissible for a near-field sub-field frame, and for nothing else* — exactly
the same qualifier Phase 2 already attached to transmission at 284 eV. **Both channels are sub-field-only**, which is
one constraint, not two.

Because `ME5` is frozen, this is registered as **`GD8`** and not applied.

### F4 — `G3` has zero executed steps, and the reason is structural

Phase 1 booked `δ_ov` under registry `S7`'s **second** form — an *observation-strength declaration*
(`moves: none (observation channel)`), not a constraint relaxation — when `GD1` Option B moved `ME1` to `CM5`. So
the ladder's executed relaxations number **zero**. Phase 3 would be the first, and it is blocked on `GD6`.

This is not a scheduling problem: after `GD1` Option B, `C1` and `C2` have **no gate expression**, so no relaxation
naming either can be registered. The ladder's vocabulary cannot describe its own far half.

### F5 — "Enhancement must not introduce information" was declarable but not testable

`EN1`–`EN5` require a declared *basis*; nothing tested *non-introduction*. The instrument built this round has two
branches and was negative-tested on four cases:

| test | levels | ΔH (bits) | monotone | verdict | branch |
| --- | --- | --- | --- | --- | --- |
| compliant `EN2` monotone ramp | 4 | +0.0000 | yes | PASS | — |
| compliant `EN3` affine stretch | 4 | +0.0000 | yes | PASS | — |
| **defect** bilinear resample ×4 | 16 | +0.3473 | yes | **CONVICT** | a (levels) |
| **defect** non-monotone palette | 4 | +0.0000 | no | **CONVICT** | b (map) |

Branch (b) is the repository's **existing** `EN2` requirement ("monotone colour map"), made executable. Branch (a)
is the missing half, and it convicts the commonest real defect in this kind of work: **interpolation presented as
physical structure**. Both branches fire on their planted defect and neither fires on the controls.

`F5` is an instrument, not a gate (`DC4` applies: a declaration may not appear in a PASS/FAIL row). It is what `G5`
needed and did not have.

---

## 3. Two self-corrections inside this round

Disclosed rather than absorbed, per the discipline applied to `p0`'s finite-box artefact and Phase 2's `9e20`/`9e14`:

1. **Registered prediction `C1` said "zero of five requirements has a product". It failed.** `G1` has depictions
   (F1). The claim is **narrowed** to "zero *fully* satisfied, one partial", and the reason the first look missed
   them is that a chart and a depiction are indistinguishable in a filename census — it took opening the files.
2. **The first `G-5` interpolation case produced only 8 levels** and convicted at `+0.116` bits, because it was a
   coarse four-neighbour blur, not a resample. Replaced with an actual bilinear upsample (`16 levels, +0.347`). The
   verdict did not change; the demonstration did, and a weak demonstration would have licensed a false confidence in
   the instrument's sensitivity.

---

## 4. What this changes, and what it does not

**Changes.** The route's status is no longer "executed as far as it can be". It is: **the ladder is executed to its
decidable limit; the goal is not reached; four of the five gaps are missing instruments or missing rulings, not
missing work.** `G4` moves from *refuted* to *unresolved* — a weaker claim that is the true one.

**Does not change.** No threshold. No archived product. No `ME5` wording. `δ_ov`, `Δz_res`, `ℓ_samp`, `Δz_tol`,
`δ_E,max` remain OPEN. `GD6` still blocks Phase 3. No state is certified two-dimensional. No visibility conclusion
is licensed — `F1` and `F3` are statements about *citable artefacts and observation geometry*, not about what the
object looks like.

---

## 5. Two decisions this needs from the governor

Both are ambiguities in the *goal text*, not in the physics, and neither can be resolved by the executor.

### `GD7` — what does `FL` mean?

- **Reading B (retinal faithfulness).** `FL3` is the maximum; the ladder ascends; the coordinate is distance from the
  unaided retinal image, which is computable from band, PSF, CNR and the applied `EN` set. Under this reading the
  diagonal is walkable and `FL1→FL3` is a monotone path of **decreasing** information and **increasing** faithfulness.
- **Reading A (information).** `FL2` is the maximum and `FL3` is dominated. The "diagonal" must then be replaced by a
  **Pareto front**, and the goal sentence's "to naked-eye reflection" is a *constraint*, not an optimum.

The goal's wording is Reading B. Every criterion in the repository is Reading A. **One sentence settles it**; until
then `G2` cannot be built, because the sign of the axis is undecided.

### `GD8` — does the corollary stand as `2L/c`, or as `2D/c`?

- **Keep `2L/c`.** Then the corollary silently asserts `D = L` and should say so; `G4` is refuted for that geometry
  and `FL3` is unreachable, which makes Phase 4's terminal rung a presentation of an impossibility rather than of a
  scene.
- **Correct to `2D/c`.** Then the corollary becomes `D < L/√2`, reflection is admissible for a near-field sub-field
  frame, and `FL3` changes from *impossible* to *sub-field, near-field only* — the same qualifier transmission
  already carries.

`F3` shows the second is the correct algebra. But `ME5` is frozen text, so the choice is the governor's.

---

## 6. What is executable without either ruling

In dependency order, none of it blocked by `GD7`/`GD8`/`GD6`:

1. **Close the `DC1` census gap** — make `display_lint` enumerate images and report the 26 missing blocks. Cheap,
   mechanical, and it is the difference between "26 frames" and "26 non-products".
2. **Issue declaration blocks for the frames that deserve citation** — starting with
   `unfold_appearance_v1.png` (D-left/D-right are the two endpoints) and `painting_render_v1.png`. Their `BAND`,
   `COLOUR`, `SCALAR`, `ENHANCEMENT` fields are all recoverable from `painting_render_v1.txt`.
3. **Build the `EN-BOUND` check into `commit_gate.py`** as an advisory, in the same relationship as `symbol_lint`.
4. **Produce the missing `G3` product** — a frame of the *front passing*, not the spread. This needs no relaxation:
   it is an `FL1` frame at the S0 constraint set, which is exactly what `G3` lacks.

Items 1–3 are this round's instruments applied. Item 4 is the only one that adds a new depiction, and it is
remarkable that the route's most conspicuous gap is a frame it was always allowed to make.

---

## 5. Amendment 2026-11-22 — item 4 above is done, and it narrows `G1` rather than closing it

`runs/FRONT/mid_sweep_fl1.png` now exists: the object with the front **mid-sweep**, at `GEOMETRY: PRESCRIBED (D2)`,
`FL1`, false colour, with a valid block (`display_lint`: OK). Pre-registration, predictions and the two pre-run
corrections are in `runs/FRONT/mid_sweep_frame_registration.md`; the record is
`docs/decisions/mid_sweep_frame_v1.md`. Seven of seven derived predictions were confirmed, including that the frame's
own arithmetic returns the registered site spacing, maximum placement and mean placement.

**`G1` stays `PARTIAL`, with its character changed: the sweep is now depicted, and the unfolded end state remains the only `FL3` candidate.** Three
things it does not fix, stated so the amendment is not read as a closure:

1. It is **not** a matrix cell and does not create a readable cell (`MR1.0` stands; `MR1.3` still reports zero).
2. It is **not** `FL3` and cannot be: at `f = 0.5` the object still exists, so the frame is not a faithful
   reflected-light view of a surviving sheet, and the reflection channel has `q = 0` regardless (`T5`).
3. Its geometry is **prescribed, not solved** (`D2`), so it depicts the process as the registered mechanism
   describes it, not as a simulation produces it.

**What the frame adds that is not a picture.** The process has two halves **`2.1e4` apart in scale** — the object is
`1.74 m`, the deposit array is `36.1 km` across with a mean placement of `13.8 km`. That is the kinematic statement
of the same thing `F3`/`GD8` found from the optics (`D = L` is near-field sub-field only) and `M5` found from the
photons. Three independent routes now say it: **`G1`'s single frame cannot exist, for reasons that are geometric
before they are optical.** The frame says so on its face rather than cropping it away.

---

*Content generated by AI*
