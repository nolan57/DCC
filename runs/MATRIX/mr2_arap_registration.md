# Registration of predictions — the `MR2` / ARAP / TPGIM / KL submission

**Received**: 2026-11-22. **Verbatim record**: `runs/MATRIX/mr2_arap_submission_verbatim.md` (`PROPOSED`, governs
nothing).
**Written before the executor exists.** This file is the lock: the sixteen predictions below were fixed before
`src/route/mr2_arap_check.py` was authored, and none may be revised after the product is read.
**No threshold is registered here**, because the submission declares none. That absence is itself `P16`.
**Self-limitation.** This file may not admit a tier, close a gate, or create a matrix cell. It states what is
expected to be measured.

**Provenance**: `NEITHER`. This is an adjudication of a submitted claim against the registered record. It
establishes no physics and creates no readable cell.

---

## 0. What the submission is, in one sentence, and where it lands

It proposes to *supply* `MR2` — the tier `matrix_reading_rules_v1.md` §`MR2` reserved for *"an arrangement-sensitive
statistic (one that falls below threshold when the tiles are shuffled) with its threshold declared and locked
before measurement"* — by composing three pieces: an ARAP energy that constructs a smooth 2D map, a TPGIM depth
channel that makes that map "lossless", and `MR2_PSMI = D_KL(P_3D ‖ P_2D)` over pairwise-distance distributions as
the statistic.

So the admission criterion is **already written down by the record, not by me**: the statistic must fall below its
threshold when the tiles are shuffled. `P6` and `P14` test exactly that and nothing else.

## 1. The two branches the submission must choose between, and why the choice is forced

`P4` decides one branch and `P3` + `P11` decide the other. Stated before measuring so that neither result can be
read as the other:

| branch | map `MR2` is evaluated on | what the record already says |
| --- | --- | --- |
| **A** | the DCC deposit (`σ`, Hilbert order 16) | the deposit severs every interface, so its pieces are ≥ `pitch` apart while the object's are ≤ `2r₄ ⊕ H` apart |
| **B** | the ARAP-relaxed map | that map is a **deformation**, and `KIN-DYN` §6 forbids exactly that class of depiction |

The submission does not say which. Both are tested. If both fail, the submission has no admissible reading.

---

## 2. The predictions

`FAIL` in the *predicted verdict* column means *I expect the submission to be wrong on this point*.

| # | prediction | predicted verdict |
| --- | --- | --- |
| **P1** | `R_i (v_i − v_j)` with `R_i ∈ SO(2)` and `(v_i − v_j) ∈ ℝ³` is **ill-typed** — a `2×2` matrix cannot multiply a 3-vector, and the executor raises on the operation | **FAIL** (defect confirmed) |
| **P2** | `SO(2)` is the wrong group regardless of the type error: unfolding a 3D shell into a plane needs a per-face 3D rotation (`SO(3)`) plus a projection, not a plane rotation | **FAIL** |
| **P3** | `docs/` contains **`0`** occurrences of `triangulat`, `triangle mesh`, `vertex set`. `DEMO-1` is a continuum of `4.279069764e9` **extended annular plates**, so ARAP's object (a vertex set `V`) does not exist in the record | **0 hits ⇒ object mismatch** |
| **P4** | Branch A: `max d_3D = √((2r₄)² + H²) = 0.29206 m` **<** `min d_2D = pitch = 0.4001 m`. Supports are **disjoint** ⇒ `D_KL(P_3D‖P_2D) = +∞` exactly, for **every** `σ` | **+∞, always** |
| **P5** | The deposit dilates axial distance by `pitch/δ = 1.861e9`; within `1%` of `1.861e9` | **1.861e9** |
| **P6** | Branch A, the admission test: `D_KL(P_deposit ‖ P_random-permutation)` on normalised pair distances is **at or below `3×` the sampling floor** `(B−1)/(2N)`, i.e. the statistic cannot see the traversal at all | **≤ 3× floor ⇒ shuffle-blind** |
| **P7** | The sampling floor is real and equals `(B−1)/(2N)`: two samples drawn from the *same* distribution give `D_KL` within a factor `[0.5, 2.0]` of it, at `B = 64`, `N = 1e5` | **floor confirmed** |
| **P8** | Therefore "driving `MR2` toward zero" is unattainable: at `B = 4096`, `N = 1e5` the floor is `≈ 0.0205` nats **for a perfect map**. Bin count and sample count, both undeclared, set the verdict | **free parameters set the verdict** |
| **P9** | A brute-force search over `6`-element subsets of `{0..20}` finds a pair of **distinct, non-congruent** sets with *identical* pairwise-distance multisets (homometric). Their `D_KL = 0.0` exactly, while their Hausdorff distance `> 0` | **found ⇒ statistic has a non-trivial kernel** |
| **P10** | `D_KL` is asymmetric: `D_KL(P‖Q)/D_KL(Q‖P) ≥ 3` on the shattered case, so the declared direction is a free choice that changes the number | **≥ 3** |
| **P11** | Branch B: `E_ARAP` with `R_i = I` **is** the per-edge squared distance discrepancy, and `MR2` is a monotone functional of the same discrepancy. The test is the optimiser's own objective, so no input fails it — the `7`th instance of *a figure chosen before the quantity is defined* | **circular** |
| **P12** | `KIN-DYN` §6 forbids depicting *"elastic unfolding, differential strain, or fracture as a consequence of `D2`"*. ARAP is an energy-minimising deformation with a stored-energy functional, i.e. the forbidden class verbatim | **scope-clause conflict** |
| **P13** | TPGIM is **not** dimensional reduction: `3` float32 channels = `96` bits per site, against `log₂(V/δ³) = 88.93` bits for the 3D address at `δ` resolution; ratio `∈ [1.0, 1.2]`. It stores the point cloud with overhead | **no reduction** |
| **P14** | The inpainting clause ("Laplacian or nearest-neighbour fill for vacant pixels") contradicts `DEMO-1` §4.3, which declares empty sites are **vacuum, drawn as such, not as material**. Filling them paints material where the record says there is none | **display-convention conflict** |
| **P15** | The weak-range clause is **vacuous** as written: `min d_2D = 0.4001 m = 1.861e9 δ`, so for any physically short `ε` the marginal count of pairs with `d_2D < ε` is exactly `0` — an empty bin, not a zero | **exactly `0` samples** |
| **P16** | **Verdict**: not admissible as a tier. The three names, the scale-separation instinct, and the requirement of a pre-locked threshold are adoptable as vocabulary; the statistic as written is `+∞` (branch A) or circular (branch B) | **REJECTED AS A GATE** |

## 3. What I expect to have to concede, stated in advance

Three of the sixteen could go the other way, and I record them now so that a favourable result is not read as
vindication:

- **`P6`** could fail if the deposit's pair-distance distribution is measurably *not* the random one. The Hilbert
  curve preserves locality, so a shell's pieces occupy a contiguous run of sites; if that produces a detectable
  skew, the statistic is not shuffle-blind and the ruling weakens to "blind at the pair level, not in general".
- **P10`** could come out near `1`, in which case the asymmetry objection is not an objection.
- **`P9`** could find no homometric pair in `{0..20}`, in which case the kernel statement is unsupported and I will
  say so rather than widening the search until it agrees with me.

## 4. The one thing the submission gets right, and it is not small

Its **local clause** — isolate short-range pairs and test them separately — is the first proposal in this battery
that separates the weak range from the global structure. `P15` says the clause is *written* wrongly (a marginal
where a conditional is needed). It does not say the instinct is wrong. If the conditional version separates the
declared traversal from a random permutation, the submission has supplied the *form* of `MR2` even though its
formula is not it. That is registered here as the salvageable content, before the measurement that could support
it.

---

*Content generated by AI*
