# Route terminus — the deposit is a serialization, not an image

**Registered**: 2026-11-22
**Authority**: governor delegation — *"from here on you decide; there are no new ideas on this side"* ("from here on you decide;
there are no new ideas on this side"). Every decision below is mine to make and mine to defend; §8 states the
reversal condition for each.
**Measurements**: `runs/ROUTE/deposit_blindness_results.txt` (predicted in
`runs/ROUTE/deposit_blindness_registration.md`, locked before the run, 3 errata appended, run unedited).
**Figure**: `runs/ROUTE/deposit_blindness_figure.png`.
**Scope**: this closes one rendering line. It makes no claim about the DCC model as physics, changes no frozen
constant, and touches none of `R1`–`R4`, `S1`–`S10`, `P1`–`P8`, `DC1`–`DC9`.

---

## 1. The question that should have been asked thirty rounds ago

Thirty-one rounds adjudicated **statistics computed on the deposit**: tiers, thresholds, mutual information,
KL divergences, potentials, topological invariants. Every gate closed. Each closing was argued on its own
grounds, and each argument was correct — `TOPO-CLOSE` (`b₀ = pieces`), `MR2-CLOSE` (disjoint supports,
`D_KL = +∞`), `MI-INVARIANT` (`17.9947` bits for *every* ordering), `POT-TRICHOTOMY` (`ΣΨ = 0` exactly).

A pattern that survives thirty-one independent justifications is usually not thirty-one facts. It is one fact
seen from thirty-one directions. So this round asked the question underneath:

> **Is `D2`'s deposit a function of the object at all?**

`DEMO-1` §4 declares `p = k·N + n`, `d = hilbert(p)`. Both expressions read `k`, `n` and nothing else.

## 2. `DEPOSIT-BLIND` — the measurement

The deposit constructor was passed a mapping that **records every read**. It read `M` and `H`. It did not read
`r₁, r₂₀, r₂ₐ, r₃₀, r₃ₐ, r₄` or the four areal densities. `P1`: **0** geometric reads.

Six physically distinct objects were then deposited:

| object | change from `O1` | `r₄` (m) | A3 (`2r₄ ≤ pitch`) | cut area (m²) | deposit digest |
| --- | --- | --- | --- | --- | --- |
| `O1` | reference | 0.0900 | yes | 2.7222e7 | `558d30e08fd32cf6` |
| `O2` | jacket radius ×1.67 | 0.1500 | yes | 7.5617e7 | `558d30e08fd32cf6` |
| `O3` | modulation phase inverted | 0.0900 | yes | 2.7222e7 | `558d30e08fd32cf6` |
| `O4` | four densities reversed | 0.0900 | yes | 2.7222e7 | `558d30e08fd32cf6` |
| `O5` | all radii re-stacked | 0.0900 | yes | 2.7222e7 | `558d30e08fd32cf6` |
| `O6` | jacket ×5.5 (outside A3) | 0.4950 | **NO** | 8.2347e8 | `558d30e08fd32cf6` |

**Six objects, one deposit.** `I(canvas ; r₄) = 0` bits exactly, across a `2.78×` admissible spread in cut area
(`30.25×` counting `O6`, which `demo_object_v1` §3 A3 forbids — erratum `E3`; the claim is read on the admissible
five).

The negative controls establish that the test has power: halving `H` changes the deposit (`N' = 534,883,720`,
`pieces' = 2,139,534,880`, different digest), and `M = 5` at `H = 0.2300` is inadmissible
(`5,348,837,205 > 4,294,967,296` cells, `H_max = 0.184684 m`).

**The theorem, one line.** `p = kN + n` and `d = hilbert(p)` are functions of `(k, n)`; `k ∈ [0, M)` and
`n ∈ [0, N)`; therefore `deposit(O) = F(M(O), N(O))` and no other parameter of `O` can enter.

**What the canvas carries.** Per site: the shell index `k` and the layer index `n` — i.e. a **band label and an
axial coordinate**. `n` determines `z` to `δ`; `k` names which annulus. What it does not carry: the radius
(the modulation — the object's entire shape), the areal density, the interface contact, the material. Of the
**12 declared parameters of `DEMO-1`, 2 are visible (`M`, `N` ⇔ `H`) and 10 are not** (`P8`).

The axial coordinate is real content and I will not understate it: the deposit is a `1`-dimensional coordinate
plus a label, laid out in `2` dimensions. It is not empty. It is simply not an object.

## 3. The corollary — why the thirty-one gates closed

> A statistic is a function of the canvas. The canvas is a function of `(M, N)`. Therefore every statistic on the
> canvas is a function of `(M, N)` and of the traversal `σ`.

That splits every possible test into two exhausted classes, and both were measured:

- **Permutation-invariant statistics** do not see `σ`, so they see only `(M, N)`. `MI-INVARIANT`: `17.9947` bits
  for component-major, layer-major **and a random permutation**, while pixel purity spans `99.99885% → 0%`.
- **`σ`-sensitive statistics** measure `σ`. `MR2-CLOSE` `X1`: of `0.06639` nats distinguishing the deposit from a
  shuffle, **`99.2%`** is the four-contiguous-runs contrast — a property of the traversal, which `DEMO-1` §4.3
  already measures at contiguity `1.0000` vs `0.9961`, with no threshold.

So the thirty-one verdicts were **correct as measurements and wrong as answers**. They were not asking "can this
object be read"; they were asking "is this declaration internally consistent", and answering no.

## 4. The dichotomy — no image exists at any scale

Two demands were imposed on one map, and they are contradictory. This is not a defect of any candidate algorithm
and no better algorithm repairs it.

| demand | measured |
| --- | --- |
| injective (nothing lost) | needs `≥ ⌈√pieces⌉ = 65,415` sites per side ⇒ `2¹⁶`; canvas `26,221 m` at `pitch` |
| renderable (a person can look at it) | `2⁹` per side; `4K` still shows `0.19%` of the deposit |
| the gap | `16,384 = 2¹⁴` **exactly** — both sides are powers of two, so the decimation is not approximate |

**An image is a many-to-one map.** Photographs integrate along sight lines and accept the loss. The deposit is
one-to-one and refuses it. A one-to-one map into two dimensions can be a *file*; it cannot be a *picture*.

Nor can the deposit be read at a different scale. `sup d₃D` inside the object is `√((2r₄)² + H²) = 0.292062 m`;
`inf d₂D` between two sites is `pitch = 0.400100 m`. The 3D support lies **strictly inside the 2D gap**, so
`d₂D/d₃D` is unbounded below the pitch separation: **no scale factor `s` satisfies `d₂D ≈ s·d₃D`** (`P10`). The
deposit is not a similarity image of the object at any magnification, not even a blurred one.

## 5. Re-designation: `DEPOSIT-SERIAL`

The deposit is a **lossless two-dimensional serialization of the piece enumeration**. Judged as that, it is good:

- `4,279,069,764` plates × `4 B` = `15.9408 GiB`, exact round trip;
- contiguity **`1.000000`** along the curve (raster order gives `0.9961`);
- component-major layout ⇒ sequential reads visit **one shell's axial history at a time**, which is the
  access pattern a per-shell reduction wants.

Judged as an image, it is empty. Both statements are true and they do not conflict; the error was to use the
second word for the first object.

**`SFC-INDEX` survives** as the one positive result of the space-filling-curve line: the Hilbert layout is
measurably better than raster (`1.0000` vs `0.9961` contiguity, median adjacent `|Δn|` `1.0` vs `128.5`). It is an
index over the object. It may not be called `σ`, and it is not a reduction.

## 6. The actual critical path: a missing input, not a missing statistic

To carry the object, a site must hold a **measured per-site quantity**. The record has none, and the reason is
already in force: `D2` performs no deformation (`KIN-DYN`), so no modulus, density or constitutive response enters
the mapping; and a per-component reflectance would need a compliant `σ_s`, which does not exist (`G6`, `DC2`).

So the canvas is missing a **coordinate**, not a metric. It has `z`; it lacks `r`. No statistic can supply a
coordinate, which is why `MR2` was never the blocker.

~~**`GD6` (`φ` in `ME3`) is promoted to the critical path** — it is the only open item whose resolution could put a
measured quantity into a site.~~ **WITHDRAWN 2026-11-22 (`D-6a`).** This sentence confused a *criterion* with a
*payload*: `ME3` is one scalar per configuration, and `I(site ; δ_E) = 0` was measured in
`me3_phi_disposition_v1.md` §5. The critical path is `G6`/`DC2` — the compliant `σ_s` named in §9 — and `GD6` is
now closed with `ME3` retired.

## 7. Dispositions

| item | disposition | reason |
| --- | --- | --- |
| readable-2D-image line | **CLOSED** | structural (§2, §4), not statistical. Not parked — closed. |
| `GD10` plates/cell | **CLOSED for `DEMO-1`**, parked for the body | inapplicable by construction (`0.9963` plates/cell). For the body it returns only if a line deposits the body, which needs a body `σ`. |
| `GD11` body `σ` | **CLOSED for this line** | the body is never drawn, so no traversal is owed. Reopens first if any future line draws it. |
| `GD6` (`φ` in `ME3`) | **PROMOTED — critical path** | §6. |
| `GD9` route objective | **DECIDED** | objective is serialization fidelity + locality, not readability. The 32-cell matrix is therefore the wrong instrument for it. |
| route governance | **DECIDED** | phased v2 governs. The matrix is frozen as the record of a closed line: readable, not extendable. |
| `G1` credit for `DEMO-1` frames | **NO** | they are `FL1` — a declared convention over a quantity no instrument measured. Putting a declared number in a measured column is the same class of error as §2. |
| 25/27 uncitable frames | **DISCHARGED BY RULE** | under `D-2` no deposit frame may be cited as evidence of readability, so the citation debt is closed by prohibition rather than by relabelling 25 files. A future line needing one re-enters it as new work with a new label. |
| `MR1.0` | **STANDS, now necessitated** | not merely unqualified: no cell can be readable, because readability needs a metric correspondence the deposit does not have (§4). 0 of 32. |

## 8. Decisions

- **`D-1`** The readable-image line is closed. *Reverse only if* §9's falsifier is met.
- **`D-2`** The deposit is re-designated `DEPOSIT-SERIAL`. Displays of it are `FL1` and may not be cited as
  evidence of readability. *Reverse on* a measured per-site quantity in the canvas.
- **`D-2a`** *(amendment 2026-11-22, `dimension_anchors_ruling_v1.md` §8)* **"lossless" must name its referent.**
  `lossless (inventory)` is true — a bijection, `4,279,069,764 → 4,279,069,764` distinct cells. `lossless (object)`
  is **false** — `I(canvas ; r₄) = 0`, `10` of `12` declared parameters never reach a site. The unqualified word was
  ambiguous between a true and a false claim, and the ambiguity is exactly the difference between a file and a
  physical reduction. *Reverse on* a demonstration that a site carries any quantity other than `(k, n)`.
- **`D-3`** `G1` takes no credit from a `DEMO-1` frame. *Reverse on* an instrument reading of the same scene.
- **`D-4`** Phased v2 governs; the matrix is frozen. *Reverse on* a governor instruction to reopen it — this is a
  governance choice, not a measurement, and it is the most reversible decision here.
- **`D-5`** `GD10`/`GD11` closed for this line, parked for the body. *Reverse on* a body-depositing line.
- **`D-6`** `GD6` is the critical path. *Reverse on* a demonstration that a site can carry a measured quantity
  through some channel other than `σ_s`.
- **`D-6a`** *(withdraws `D-6`, 2026-11-22, `me3_phi_disposition_v1.md` §5)* **`GD6` is not the critical path.**
  `D-6`'s ground — "the only open item whose resolution could put a measured quantity into a site" — is a
  **category error**: `δ_E` is one scalar per configuration, a site holds `(k, n)`, so `I(site ; δ_E) = 0`.
  Measured: two objects with `δ_E` differing `4×` give one deposit digest. §6 above substituted `GD6` for `G6`;
  the critical path is `G6`/`DC2` (`σ_s`), which §9 had already named. *Reverse on* a demonstration that a
  configuration-level scalar varies site by site.
- **`D-7`** `GD9` objective = fidelity + locality. *Reverse on* a redefinition of the route's goal.
- **`D-8`** Citation debt discharged by prohibition. *Reverse on* a request for any specific frame.
- **`D-9`** No further submission is adjudicated against `MR2` or any arrangement statistic. New submissions are
  read against §2's theorem first: *what quantity, other than `(M, N)`, does your proposal put into a site?*
  A submission that cannot answer that is answering a closed question.

## 9. What would reopen the line

One exhibit falsifies `DEPOSIT-BLIND` and everything above it: **a physical quantity, other than `M` and `N`,
that the record's deposit determines.** `I(canvas ; q) > 0` for some `q` would move that `q` out of the
ten-invisible column and the theorem would fail on that quantity.

The line reopens constructively when a site can carry a measured value — i.e. when `G6`/`DC2` yields a compliant
`σ_s`. Then the deposit becomes a *field*, and the image question becomes askable again, on a different object.

## 10. My own defects, recorded

- **`E1`** `P5`'s registered constant `H_max = 0.184699` is wrong; derived `0.184684`. `P5` recorded FAIL and the
  FAIL stands. **Fourth** instance of "a derived constant registered tighter than its derivation supports."
- **`E2`** `demo_2d_map.py` calls `d2xy(order=16, q)` over a `2¹⁸` index range; the last 7 iterations run on an
  exhausted accumulator and exchange `x↔y` each time, so the round-28 canvas panel is drawn on the **transpose**
  of the order-9 curve (`262,144/262,144` indices exact). No conclusion of that round changes — transposition
  preserves the bijection, 4-adjacency, the single-shell fraction and the straddle counts, all computed on the
  same grid. A convention defect, recorded, not repaired.
- **`E3`** `P7` as registered cited a `30.25×` cut-area spread, one member of which violates the object's own A3
  check. The admissible spread is `2.78×`, and the collision holds there too. **Third** instance of "a figure
  chosen before its constraints were checked."
- **Figure, first draft** — per-shell brightness normalization made `O1` and `O6` visually indistinguishable, i.e.
  the encoding hid the very difference the panel existed to show; plus white labels on ochre (round 28 recurring).
  Rebuilt: the third panel is now the *object*, the one panel the deposit does not contain.

## 11. What this document does not decide

It does not decide whether the DCC claim is true. It decides that **one mechanism, `D2`, cannot produce a readable
2D image of a 3D object**, and says exactly why: it preserves adjacency and destroys metric, and it encodes the
enumeration rather than the object. If the framework has a rendering story, that story is not this one.

*Content generated by AI*
