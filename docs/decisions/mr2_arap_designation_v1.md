# Ruling on the submitted `MR2` — ARAP energy, TPGIM depth channels, KL statistic

**Received**: 2026-11-22. **Registered verbatim**: `runs/MATRIX/mr2_arap_submission_verbatim.md` (`PROPOSED`,
governs nothing).
**Registration of predictions**: `runs/MATRIX/mr2_arap_registration.md` (`P1`–`P16`, written before the executor).
**Executor**: `src/route/mr2_arap_check.py`. **Product**: `runs/MATRIX/mr2_arap_results.txt` (`216` lines,
`15` of `16` predictions held, `1` refuted, `1` constant wrong by `2×`).
**Provenance**: `NEITHER`. This adjudicates a claim against the record. It creates no readable cell.

---

## 0. The one thing to understand before the table

`MR2` was reserved by `matrix_reading_rules_v1.md` for *"an arrangement-sensitive statistic (one that falls below
threshold when the tiles are shuffled) with its threshold declared and locked before measurement"*. The submission
proposes to fill that slot. So the admission criterion is **the record's, not mine**, and the first question is not
whether the mathematics is elegant. It is whether the statistic can fall when the thing it certifies is destroyed.

It cannot, and the reason is a single inequality that needs no measurement:

```
max distance inside the object   √((2r₄)² + H²) = 0.292062 m
min distance between two sites   pitch          = 0.400100 m         (ratio 1.370)
```

**The two distance distributions have disjoint support.** So `D_KL(P_3D ‖ P_2D) = +∞` at every `d` where `P_3D(d) > 0`,
for every admissible `σ`. Everything else in this document is a consequence or a qualification of that line.

---

## 1. Verdict

| Element | Verdict | Why |
| --- | --- | --- |
| **`MR2_PSMI = D_KL(P_3D‖P_2D)` over pair distances** | **REJECTED** | `+∞` identically (§2). A gate that closes for every `σ` carries no information — the `TOPO-CLOSE` pattern, in the metric |
| **ARAP as the mechanism that builds the 2D map** | **REJECTED** | (a) it is an energy-minimising *deformation*, the class `KIN-DYN` §6 forbids depicting as a consequence of `D2`; (b) its object is a vertex set, and the record contains **zero** occurrences of `triangulat`/`triangle mesh`/`vertex set`; (c) `R_i ∈ SO(2)` cannot multiply a `ℝ³` edge — the written term has no value (§3) |
| **TPGIM as "lossless dimensional reduction"** | **REJECTED** | `3 × float32 = 96` bits stored against `88.93` bits needed for the 3D address at `δ`. It stores the point cloud with `8%` overhead: a relabelling, not a reduction (§5) |
| **Inpainting vacant pixels** | **REFUSED** | contradicts `DEMO-1` §4.3, which declares empty sites *vacuum, drawn as such, not as material* (§5) |
| **"Permutation sensitivity"** | **PARTLY CONFIRMED, and it does not help** | the statistic *does* separate the deposit from a random permutation, by `422×` the floor. `X1` shows `99.2%` of that separation is the four-run partition — i.e. it measures `σ`, not the object (§4) |
| **The local / weak-range clause** | **ACCEPTED AS VOCABULARY, REJECTED AS WRITTEN** | vacuous as a marginal (zero samples at every short `ε`, in both spaces); as a **conditional** it separates perfectly — measured, §6 |
| **The three names and their order** | **ADOPTED** | `ARAP → TPGIM → MR2` is a legible decomposition of the problem; adopting the vocabulary binds nothing |
| **A threshold declared and locked before measurement** | **ADOPTED — and it is the submission's real contribution** | it is the discipline `MR2` needed; the submission's own formula has no threshold, which is `P16` |

**`MR2` is closed as a gate** (`MR2-CLOSE`). It survives as a named **diagnostic** with no threshold (`MR2-D`, §7).
`MR1.0` therefore stands **unqualified**: no cell may be read as "readable".

---

## 2. Branch A — measured on the deposit, the statistic is `+∞`

### 2.1 The proof

The deposit maps piece index `p = kN + n` to site `p` by a bijection, so distinct pieces occupy distinct sites. The
nearest distinct sites are 4-adjacent and separated by exactly `pitch`. The object's own extent is bounded by its
circumscribed cylinder:

| quantity | value | source |
| --- | --- | --- |
| `max d_3D` | `√((2r₄)² + H²) = 0.292062 m` | `DEMO-1` §2 |
| `min d_2D` | `pitch = 0.4001 m` | `DEMO-1` §2.1 |
| clearance | `37.0%` | `0.4001/0.292062 = 1.3699` |

`supp(P_3D) = (0, 0.292062]` and `supp(P_2D) ⊆ [0.4001, 37,082]`. Disjoint. Any `d` with `P_3D(d) > 0` has
`P_2D(d) = 0`, and the summand `P_3D log(P_3D/0)` diverges.

This is not a threshold that could be tuned. It holds for **every** `σ`, because `σ` permutes sites and every
permutation of a set with minimum spacing `pitch` has minimum spacing `pitch`. The gate therefore closes for every
admissible deposit — exactly `TOPO-CLOSE`'s argument (`b0 = 4,279,069,764 ≥ 2` for every `σ`), reached from the
metric side.

### 2.2 The number underneath the divergence

The deposit is not approximately non-isometric; it is a dilation by a fixed factor along the axis:

```
dilation = pitch/δ = 0.4001 / 2.15e-10 = 1.8609e9
```

So even the most generous repair — normalise both distributions by their means and bin them — is comparing the shape
of `P_3D` against the shape of `P_2D` *after* a `1.86e9` stretch. That this can be made finite by normalisation is
what `§4` measures, and it is why normalisation does not rescue the statistic: the normaliser is a free parameter
that was not declared, the same defect that killed `Q2` and `Q0`.

---

## 3. Branch B — measured on the ARAP map, the statistic is circular and the map is forbidden

The submission does not say which map `MR2` is evaluated on, which forces both branches to be tested. On branch B:

1. **`E_ARAP` with `R_i = I` *is* the per-edge squared distance discrepancy.** `MR2 = 0` iff the distance
   distributions coincide; `E_ARAP = 0` iff every edge is preserved. They are monotone in the same quantity, and the
   map is *chosen* as the minimiser of `E_ARAP`. A gate whose passing map is defined as the minimiser of its own
   statistic has no failing input. This is the `7`th instance of the pattern first named in `FOURDIM` `P6`:
   *a figure chosen before the quantity is defined.*
2. **`KIN-DYN` §6 is a binding scope clause**, registered at the governor's own acceptance. It says: *"no frame may
   depict elastic unfolding, differential strain, or fracture as a consequence of `D2`."* ARAP carries a stored-energy
   functional and minimises it. That is elastic unfolding by definition. The submission's first pillar is not a
   refinement of the mechanism — it is the exact class the clause forbids.
3. **ARAP's object does not exist in the record.** `docs/` contains `0` occurrences of `triangulat`,
   `triangle mesh`, `vertex set`. The object of record is a continuum of `4.279069764e9` **extended annular plates**;
   a site holds a plate with area, not a vertex. `ARAP` and `TPGIM` describe a triangulated surface no document
   declares — a different object, substituted silently.
4. **The written energy is not a function.** `R_i ∈ SO(2)` is `2×2`; `(v_i − v_j) ∈ ℝ³` is length `3`; the product
   `R_i(v_i−v_j)` raises. The executor confirms the raise. And the group is wrong independently of the type: unfolding
   a 3D shell needs a per-face rotation in `SO(3)` plus a projection, which is why the geometry-image literature this
   borrows from uses `SO(3)` per triangle and a chart, not a plane rotation per vertex.

Neither branch is admissible, and the two fail for *different* reasons — which is the strongest form the negative can
take.

---

## 4. The refutation of `P6`, and what it actually measures

`P6` predicted the statistic would be blind to the traversal. **It is not, and my prediction was wrong.** Measured,
on `200,000` pairs of the locked geometry, normalised, `64` bins:

```
D_KL(P_deposit ‖ P_random permutation) = 0.06639 nats     floor = 0.000158     ratio 422×
```

The Hilbert curve enriches the small-distance tail: measured `min d_2D` is `21.1 m` for the deposit against `32.0 m`
for random site pairs. That is a real capability and it is recorded as one.

**`X1` (post-hoc, labelled as such) asked what it is detecting.** Scrambling the assignment *within* each shell's run,
holding the four runs fixed:

```
D_KL(P_deposit ‖ P_within-shell scramble) = 0.00054 nats     share of the P6 signal = 0.82%
```

The expectation here is **exactly zero**, and structurally so: scrambling within a run leaves that shell's site
*set* unchanged, and `n` was already uniform, so both samples are drawn from the same distribution. The measured
`0.82%` is a floor fluctuation.

> So `99.2%` of the discrimination that refuted my `P6` is the **four contiguous runs versus fully random** contrast
> — a property of the declared `σ`, not of the object.

That is the hinge of the ruling. The property this statistic measures is *"do the runs of the traversal form four
contiguous blocks"*. `DEMO-1` §4.3 already measures that property directly and more cheaply: **contiguity
`1.0000` against raster's `0.9961`**, with no bin count and no sample size. And `DEMO-1` §4.2 states in the
governor's own words that the four-run reading *"does not show the cross-section as it was … a real loss of the
photograph reading"*.

**A statistic that rises when the cross-section is destroyed cannot certify that the cross-section survived.** The
measured interface loss makes this concrete: adjacent shells touch at `d_3D = 0`, and the deposit places them
`12,085`–`12,989 m` apart. All three interfaces, destroyed, `100%`. The statistic scores that arrangement as `422×`
more ordered than randomness.

So `MR2` is not admitted, and the reason is now sharp:
**every finite version of the statistic is a statistic of the encoding; every version that is a statistic of the
object is `+∞`.** This is the same wall as `MI-INVARIANT` (`I = 17.9947` bits identical across three orderings) and
`TOPO-CLOSE` (`b0 = pieces` for every `σ`), reached a third way.

---

## 5. TPGIM: a relabelling with overhead, and a display conflict

| quantity | value |
| --- | --- |
| material volume `πr₄²H` | `0.005853 m³` |
| address bits at `δ`, by volume `log₂(V/δ³)` | `88.93` |
| address bits, separable per coordinate | `89.28` |
| bits stored (3 channels × float32) | `96` |
| **ratio stored / needed** | **`1.080`** (float32), `2.159` (float64) |

An `H×W×3` array is a three-dimensional data structure. Calling it two-dimensional relabels it; it does not reduce it.
This is `GD11`'s identity-map finding in array form, and it is why `SF-CURVE-SUBMISSION` concluded that the deposit is
a reordering into a sequence, not a projection. **"Lossless dimensional reduction" is a contradiction unless nothing
was reduced**, and here nothing was.

The inpainting clause is worse than inelegant. `DEMO-1` §4.3, hash-locked, declares: *"The `0.37%` of sites with
`d ≥ pieces` are **empty** — vacuum, drawn as such, not as material."* Laplacian or nearest-neighbour fill would paint
material into declared vacuum. That is precisely the "false visualisation" the governor prohibited in the visual
dimension one round ago — *enhancements may not introduce physically non-existent information*. A submission cannot
satisfy his own visual criterion and violate it in the same document.

---

## 6. The salvageable content, and it is one idea

The submission's **local clause** is the first proposal in this battery that separates the weak range from the global
structure. It is *written* wrongly — a marginal where a conditional is needed — and `P15` measures the consequence:

| `ε` | 3D pairs `< ε` | 2D pairs `< ε` |
| --- | --- | --- |
| `1e-18` | 0 | 0 |
| `1e-9` | 0 | 0 |
| `δ = 2.15e-10` | 0 | 0 |
| `1e-2` | 141 | 0 |

The 2D count is exactly `0` for every `ε < pitch`: `0.4001 m` is `1.86e9 δ`, so the canvas cannot represent any
short-range pair at all. And the 3D count is `0` too, under uniform pair sampling, because local pairs are a
measure-zero tail of the marginal (`O(δ/diameter) = O(1e-9)`). **A zero count is not a zero divergence** — the
clause's "if `MR2 → 0` at this local scale" is a test on an empty bin.

Inverted into a conditional, it works, and the measurement is exact:

| axial neighbour pair | `d_2D` deposit | `d_2D`/`pitch` | `d_2D` if shuffled |
| --- | --- | --- | --- |
| C1 | `0.400100 m` | `1.0000` | `9,733 m` |
| C2 | `0.400100 m` | `1.0000` | `23,781 m` |
| C3 | `0.400100 m` | `1.0000` | `11,372 m` |
| C4 | `0.400100 m` | `1.0000` | `1,900 m` |

A **delta at exactly one pitch**, against `O(canvas)` for a permutation. The conditional separates perfectly, with no
bin count, no threshold, and no sample-size floor. That is the submission's instinct, and it is correct.

And the cost is measured by the same conditional on interface contacts: `100%` destroyed (§4). So the conditional
statistic reports *axial order preserved, interface order annihilated* — which is the true and useful statement about
`DEMO-1`, and which is the same fact as `b0 = pieces`, arrived at independently.

---

## 7. What `MR2` becomes

`MR2-CLOSE` — **not a gate.** The reason is structural and does not depend on the statistic chosen: the deposit
severs every interface by construction, so *any* arrangement-sensitive statistic that is a statistic of the object
diverges, and any that is finite is a statistic of `σ`. No admission criterion can be met by a statistic whose
subject is the object. `MR2` does not enter the matrix, and **`MR1.0` stands unqualified**.

`MR2-D` — **a diagnostic, no threshold, no admission power.** Its authorised content is exactly the two measured
columns above:

> **`MR2-D`.** For a declared `σ`, report the 2D separation of pairs that are *3D-local* (`d_3D = δ`, axial) and of
> pairs that are *3D-contacting* (`d_3D = 0`, interface). For `DEMO-1`: axial pairs land at exactly one `pitch`
> (`1.0000`), interface pairs at `1.2e4` m, i.e. `100%` of interfaces destroyed. Declared, not measured against a
> threshold; **it may not be read as a pass, a cell, or a readability claim.**

This is the honest form: it is `DEMO-1` §4.2's declared loss, quantified. It adds no lock and creates no cell.

### 7.1 What this does to the critical path

`FOURDIM` §7 landed three of the four re-anchored dimensions on `MR2`. They now land on a closed gate. The
conclusion is not that `MR2` was the wrong statistic but that **the path from zero to one readable cell does not run
through a better statistic at all.** It runs through a map that does not sever interfaces — and `D2` severs them by
construction (`front_sweep_v1` §2 ③: *"no in-plane bonding is performed. The space between pieces is vacuum."*).
Three independent lines now say the same thing: `b0 = 4,279,069,764` (`TOPO-CLOSE`), `I = 17.9947` invariant across
orderings (`MI-INVARIANT`), and `supp(P_3D) ∩ supp(P_2D) = ∅` (`MR2-CLOSE`).

> `MR2` is removed from the critical path. What remains on it is `GD10`, `GD11` (body), `GD6`, `GD9` and route
> governance — none of which any statistic can settle.

---

## 8. My own defects this round

1. **`P6` was wrong**, and wrong in the submission's favour. I predicted shuffle-blindness; the statistic separates
   at `422×` the floor. I did not explain it away — `X1` was added (and labelled post-hoc) to find out *what* it
   separates, and the answer (`99.2%` run partition) is what the ruling rests on.
2. **`P7`'s constant is wrong by `2×`.** I registered `(B−1)/(2N)`; the measured floor is `(B−1)/N` (ratios
   `1.86`–`2.05` across `B = 16…4096`). The prediction "passed" at `1.858` only because I declared a `[0.5, 2.0]`
   band wide enough to hide a factor `2`. The *argument* is unaffected — the floor is `∝ B/N` and a perfect map does
   not score `0` — but the constant I wrote was not the constant I measured.
3. **`P14`'s first run reported a false FAIL** because the bold markers in `**empty** — vacuum` broke my regex. Caught
   and fixed before this document; the finding stands on the literal sentence, quoted in §5.
4. **`P2` is asserted, not measured.** It is a mathematical statement about which group acts on which space, and I
   mark it PASS by argument. It would be dishonest to present it in the same column as the measured rows without
   saying so.

Items 2 and 3 are the recurring pattern named in `KIN-DYN` §9 and again in `FOURDIM`: *a proxy statistic passes — or
fails — for the wrong reason, and the result is reported before the proxy is audited.* The mitigation applied here
was to re-derive the floor at five bin counts and to re-check the two keyword tests against the literal text before
writing. It caught `P14` but not `P7`'s constant, which I noticed only when the ratios printed above `1.9` at every
`B` — a systematic that a single-bin check would have read as noise.

---

## 9. What this does not change

1. `MR1` — **zero readable cells**, unchanged, and now with a third independent reason.
2. The four tiers and `threshold_lock.json` — byte-identical. No threshold was created, moved, or read.
3. `DEMO-1` — hash-locked, untouched. §4.2 and §4.3 are *confirmed* by this round: §4.2's declared loss is measured
   as `100%` interface destruction, and §4.3's vacuum convention is the reason the inpainting clause is refused.
4. `KIN-DYN` §6 — strengthened, not weakened: the first thing to test it against was a submission that violated it.
5. `GD10`, `GD11` (body), `GD6`, `GD9` — untouched and still open.
6. `SF-CURVE-SUBMISSION`'s conclusion — confirmed from a new direction: the deposit is a reordering, so a statistic
   comparing it to 3D distances diverges.

---

## 10. Still open

`GD6` (`ME3`'s `φ`, blocks Phase 3) · `GD9` (route objective) · `GD10` (plates per cell) · `GD11` (body's `σ`) ·
route governance (phased v2 vs the matrix after `§6`'s six amendments) · whether a `DEMO-1` frame counts toward `G1`
(governor's call) · citation repair (`25` of `27` frames uncitable).

---

*Content generated by AI*
