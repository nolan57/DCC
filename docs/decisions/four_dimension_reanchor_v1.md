# Four-dimension re-anchoring — ruling (`FOURDIM-V2`)

**Status**: **PARTIALLY ADOPTED.** The four dimension names, their order, and the demand that each carry a declared
statistic plus a pre-locked threshold are **registering as vocabulary** (`FOURDIM-V2`, below). The four operational
contents, as written, are **not adopted**: each is measured below to be either unsatisfiable by construction,
convention-dependent over five decades, invariant to the thing it claims to test, or satisfied by assumption.

**Submission**: `runs/MATRIX/fourdim_v2_submission_verbatim.md`
**Pre-registration**: `runs/MATRIX/fourdim_registration.md` (`P1`–`P10`, falsifiers declared before the executor)
**Run**: `src/route/fourdim_check.py` → `runs/MATRIX/fourdim_results.txt` (7/10; three FAILs, all mine, erratum inside)
**Object**: `DEMO-1`, locked at `runs/FRONT/demo_lock.json` (`sha256 91098fbe…`)

No threshold is declared by this document. No tier is renamed. No cell is filled. `MR1` stands unqualified.

---

## 1. What the governor is right about, and what my previous assessment got wrong

Two corrections go against me, and they are not small.

**First: the dimensions were not refuted; the statistics were.** My previous verdict said "0 of 4 tiers increase with
2D-ification" and let that read as a verdict on the four dimensions. It was a verdict on `Q0`, `Q1`, `Q2`, `Q3` —
specifically on `Q0` being amplitude-invariant (a 120× amplitude change moved `P0` by `1.1e-2`) and `Q2` surviving a
full tile shuffle (`0.94 → 0.78`, both passing). Those are defects of the *chosen statistics*. A dimension whose
implementing statistic is insensitive has not thereby been shown empty. The governor's diagnosis — "criteria
undefined or lacking consensus" — describes the record more accurately than "not validated" did.

**Second: the mutual-information claim is right, and my `T2`-based refusal does not transfer.** I had refused a noise
test on the ground that `Q2` survived scrambling. `Q2` is a predictability statistic. A position-paired mutual
information does reject a scrambled *image*, and if I had said otherwise I would have been wrong. That concession is
recorded here rather than buried, because the finding in §5 is narrower than the one I would have made a round ago.

---

## 2. Topological gate — **unsatisfiable by construction**, and blind when it is satisfied

The criterion: components and genus of the object must match the 2D projection 100%, any violation terminating the
evaluation.

| reading | `b0` | `b1` (holes) | outcome |
|---|---|---|---|
| object, material (voxel, 132³) | `1` | `0` | — |
| deposit, material (as built) | `4,279,069,764` | `3,209,302,323` | **FAIL** |
| deposit, quotient by declared label | `4` | `3` | **FAIL** (genus) |
| idealised projection (disc) | `1` | `0` | PASS — and blind |

**The gate closes on every admissible deposit, and no `σ` can reopen it.** `D2` severs every interface
(`front_sweep_v1 §2`: all `8.12e9` interfaces broken), so the deposit is a set of separated plates:

    b0(deposit) = pieces = M · N_layer = M · H/δ = 4 × 1,069,767,441 = 4,279,069,764

against `b0(object) = 1`. `σ` permutes sites; permutation cannot create contact across vacuum. Since `N_layer = 1.07e9`
for this object, `b0 ≥ 2` for any object thicker than two layers. The gate is therefore not mis-thresholded — it is
**incompatible with the construction it is asked to certify**. A criterion that fails every instance carries no
information, which is the same defect as a criterion that passes every instance.

The genus clause fails too, and my prediction said it would not (erratum `E4`): `C2`, `C3`, `C4` plates are **annuli**,
each with a through-hole, so `b1(deposit) = 3 × N_layer = 3,209,302,323` against `0`.

**And where it does pass, it is blind.** The object's material is a solid cylinder — the four shells share their
interfaces — so it is contractible: `(b0, b1, b2) = (1, 0, 0)`, verified by a voxel Euler characteristic that was first
shown to fire on a planted defect (`χ` = 1 for one voxel and for a 2×2×2 block). A homogeneously painted cylinder
scores identically. The only structure `DEMO-1` has — four components — is a *label*, not a topological feature. The
one reading that passes both clauses is the idealised continuous projection, which discards the deposit entirely.

---

## 3. Metric gate — five and a half decades, none of them an error

| convention | `d` (m) | fixed by | what it measures |
|---|---|---|---|
| index space, key held | `0` | bijection | nothing (an identity) |
| mid-slice vs solid, `W1` | `5.75e-2` | `H/4` | the object's height |
| mid-slice vs solid, Hausdorff | `1.15e-1` | `H/2` | the object's height |
| true scale, half canvas | `1.311e4` | `canvas/2` | the array's size |
| true scale, Hausdorff sup | `1.854e4` | `canvas/√2` | the array's size |

Span `5.51` decades, and `0` is also admissible, which makes the ratio unbounded. `ε` cannot be declared before a
scale **and** an embedding are declared, and both are ours: the map is a bijection on pieces, so fidelity on the index
space is `0` by construction; on the physical plane the two sets differ in extent by `1.1e5`, so the distance equals
the scale factor. Neither is an error of the deposit.

---

## 4. Information gate — the one that does not do what it claims

The criterion says it "inherently rejects random noise or scrambled outputs". Measured, at the level where scrambling
is a choice — the ordering:

| ordering | pixel purity | `I(pixel; piece)` | `H(piece)` | `H(piece\|pixel)` |
|---|---|---|---|---|
| component-major (declared) | `99.99885%` | `17.9947` | `31.9947` | `14.0000` |
| layer-major | `0%` | `17.9947` | `31.9947` | `14.0000` |
| random permutation | `0%` | `17.9947` | `31.9947` | `14.0000` |

**Identical to four decimals.** The reason is exact, not empirical: a display pixel holds `16,384` pieces no matter how
they were chosen, so `H(piece | pixel) = log₂ 16,384 = 14` bits for every ordering. Hence

    I = log₂(pieces) − log₂(sites per pixel) = injectivity + decimation

which is a restatement of `pieces ≤ cells` and of the display decimation — nothing about structure. A **randomly
permuted** deposit scores the same as the declared one. The quantity that separates them is **purity** (`99.99885%`
against `0%`), which is an arrangement property, not mutual information.

The claim is true only for a corrupted *image* — pixels permuted after encoding — which tests a corruption applied
after the fact, not the encoding. And the pairing that would make it sensitive requires the key at **sub-pixel**
resolution, i.e. the piece list, which the image has already discarded. Decimation destroys exactly the information
the criterion needs.

Two further defects:

- **Counting measure is undeclared.** `H` over area is `1.738970` bits; over pieces it is `2.000000`. A `0.26`-bit
  (13.1%) spread, deterministic, because the map counts pieces while the areas differ by `8.0×`.
- **The physical channel is silent.** The deposit carries one content symbol per plate (`KIN-DYN`: `D2` performs no
  deformation, so no modulus or density enters; no compliant per-component reflectance exists — `G6`/`DC2`). So
  `H(X) = 0` and `I ≡ 0` for a homogeneous body. Any information at all comes from *declaring* four labelled
  components, and those labels are a false-colour convention (`EN2`, `FL1`).

My registered ceiling was wrong here (`P9`, erratum `E3`): I bounded `I` by `H(label) = 1.739` when the criterion's
`Y` is the structure, whose entropy is `31.99` bits. Measured `I = 17.99 > 1.74`, so the registered prediction is
refuted and withdrawn.

---

## 5. Visual gate — satisfied by construction, therefore not a test

The criterion: there must exist an observer `O` (naked eye **or infinite computational capacity**) and an extraction
method `M` that recovers the structure.

With unbounded computation, `σ` is invertible. Verified: Hilbert round trip exhaustively at order 6 (all `4,096`
points) and on `20,000` sampled pieces at order 16 — recovery `1.000000`. Without the key there is no pairing, so the
criterion has no value: not false, undefined.

So the witness for "there exists an observer `O`" is **the holder of `σ`**, which is the author. An existence claim
quantified over an unbounded class, whose only witness is our own convention, cannot discriminate anything — the same
shape as `S10`, now in a fourth register. And the second clause ("must not introduce physically non-existent
information") is unevaluable until a compliant per-component reflectance exists (`G6`/`DC2`); it cannot be applied to
any frame yet, `DEMO-1`'s false colour included.

---

## 6. Why the "strictly progressive hierarchy" cannot be exercised

The submission orders the four as gate → intermediate → terminal → empirical verification. Under the **material**
reading the gate closes on every deposit (§2), so nothing downstream is ever reached. Under the **idealised** reading
the gate and metric pass vacuously and the information tier collapses to `H(label)` or `0` (§4). There is no reading
under which all four are exercised in order on a real deposit. The hierarchy is well-formed as a *specification*; it
has no instance.

---

## 7. What would actually work — and it lands on one missing statistic

Three of the four reduce, once made operational, to something the record already has or already lacks:

1. **Topology**, declared on the *index space* with the quotient explicit, becomes the identity
   `pieces = M · N_layer = M · H/δ` — the census, already frozen and already in force. Its content is arithmetic, not
   topology. Declared on the material it is unsatisfiable. There is no third option.
2. **Metric**, declared in a stated unit, has only one non-vacuous content at `H_eff = δ`: the in-plane error, which is
   zero by the identity map and therefore an identity again.
3. **Information**, declared with its pairing, is either (a) the piece-count identity above, or (b) an
   **arrangement-sensitive** measure — which is exactly `MR2`.
4. **Visual** is satisfied by construction until a physical signal exists (`G6`/`DC2`).

So the re-anchoring converges on a single sentence: **the whole battery needs one arrangement-sensitive statistic with
a threshold locked before measurement, and that is `MR2`.** Four independent formulations of the criterion keep landing
on the same gap, which is evidence about the gap, not about the formulations.

That is a better outcome than the submission claims for itself, and a worse one than "the framework stands". The
framework's *vocabulary* stands. Its four operational contents do not, and no amount of threshold-setting repairs a
criterion that returns the same number for a coherent map and a random permutation.

---

## 8. What this ruling does not do

- It declares **no** threshold, **no** `ε`, **no** `I_min`. None of the four could be locked against a quantity that is
  convention-dependent, and locking one would manufacture the appearance of discipline.
- It renames **no** tier and admits **no** new one. `L0`–`L3` keep their locked names and thresholds
  (`runs/MATRIX/threshold_lock.json`).
- It fills **no** cell. `MR1.0` ("no cell may be read as readable") stands unqualified, and `MR1.3`'s two independent
  reasons are untouched.
- It does not withdraw any part of the four-dimension idea. `FOURDIM-V2` is registered as vocabulary so that later
  documents can use the names without inheriting the four failed operational contents.

## 9. Registry effects

`FOURDIM-V2-SUBMISSION` (PROPOSED, partially adopted), `TOPO-CLOSE` (the impossibility: `b0(deposit) = M·H/δ > 1`, so
the topological gate closes for every deposit), `MI-INVARIANT` (measured: `I` identical across three orderings while
purity spans the full range). `MR2`'s row gains a note that this ruling lands on it.

*Content generated by AI*
