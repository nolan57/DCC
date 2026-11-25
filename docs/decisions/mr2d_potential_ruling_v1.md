# Ruling on the `MR2-D` + truncated-Morse submission

**Received**: 2026-11-22. **Verbatim**: `runs/MATRIX/mr2d_potential_submission_verbatim.md` (`PROPOSED`, governs
nothing).
**Registration of predictions**: `runs/MATRIX/mr2d_potential_registration.md` (`P1`–`P15`, written before the executor).
**Executor**: `src/route/mr2d_potential_check.py`. **Product**: `runs/MATRIX/mr2d_potential_results.txt`.
**Provenance**: `NEITHER`. Adjudication. Creates no readable cell, moves no threshold.

---

## 0. The whole ruling in one line

> The correction **adds a term that is identically zero to a term that is forbidden**.

`E_total = E_ARAP + λ Σ Ψ`. Measured: `Σ Ψ = 0.0` exactly for every physical parameter set (`P1`). And `E_ARAP` is
the object `KIN-DYN` §6 forbids. So `E_total` is unchanged from the submission that was rejected last round, with an
extra term that evaluates to zero.

That is not a dismissal — §2 concedes more than the previous four rounds did — but it is the answer.

---

## 1. Verdict

| Element | Verdict | Why |
| --- | --- | --- |
| **The diagnosis in §I, claim 1** (support disjointness ⇒ `KL` diverges) | **ACCEPTED, accurate** | it is `P4` of the last ruling: `0.292062 m < 0.4001 m`. Quoted correctly, including `MR2`'s rejection |
| **§I claim 2** ("spurious stresses" from forced connectivity) | **REJECTED — true of the *previous submission*, false of the record** | `D2` performs no deformation, so `E ≡ 0` by construction and there is no stress field. `docs/` contains `0` occurrences of "spurious stress". The claim describes `E_ARAP`, which the last submission introduced — §3 |
| **§I claim 3** (vertex set / extended plates / `SO(2)` on 3D edges) | **ACCEPTED, accurate** | matches `P1`–`P3` of the last ruling. `docs/specs/`: `triangulat` `0`, `vertex set` `0`, `shell` `5`, `pieces` `10` |
| **The truncated Morse potential** | **REJECTED** | inert for every physical `(α, r_cut, d₀)`; its only non-inert branch contradicts the locked `pitch`. Three-branch exhaustion, §4 |
| **`r_cut` as the mechanism that "permits rupture"** | **REJECTED** | `r_cut` must be `≥ 0.4001 m` before one pair contributes — `≥ 4.0e8×` a physical interaction range. It "permits" the rupture by being too short to notice it |
| **`N_phys`** | **ADOPTED as a symbol, REFUTED as a set that the potential can reach** | non-empty (`3,318` at POC), and **`0`** of its members lie inside any physical `r_cut` |
| **`MR2-D` as sole diagnostic** | **ACCEPTED, unchanged** | already in force. But it may not "prove" — §5 |
| **"…proving that as long as true physical interfaces are not severed…"** | **REFUTED** | the antecedent is **false** for `DEMO-1`: `100%` of interface contacts are severed. A vacuously true implication proves nothing |
| **SFC repositioned as an index** | **ACCEPTED under a new symbol `SFC-INDEX`** | correct call, and it is a *different object* from `SIGMA-DEMO`; it may not be called `σ` |
| **The staged POC (500–1000 voxels)** | **ACCEPTED — as a code test only** | it cannot be a scale model: one locked constant must move by `4.18e6×` (§6) |
| **The stress figure** ("high stress in red, natural ruptures") | **REFUSED** | `KIN-DYN` §6 names *"differential strain, or fracture"*. Second submission in two rounds to draw the forbidden picture |
| **`§V` engineering** | **LARGELY REJECTED** | optimises for a scale `§IV` declines; the 32-bit budget is `10` bits short; `CG` is a linear solver; `2` of `4` Windows settings are counterproductive |

**Verdict: `PARTIALLY ACCEPTED`.** The reading of the record is the best in five submissions. The replacement
mechanism does nothing.

---

## 2. What this submission gets right, and it is not small

1. **It accepts the ruling instead of arguing with it**, and states the three defects accurately — two of three
   verbatim correct (`A1`, `A3`).
2. **It quotes the `X1` decomposition correctly**: *"99.2% of this discriminative ability stems from partitioning data
   into contiguous blocks rather than a genuine understanding of physical structure."* That is my measurement,
   restated without softening, and it draws the right conclusion from it — SFC is not the physical algorithm.
3. **It repositions SFC correctly.** Indexing is what a space-filling curve is genuinely good for. That is a better
   use than the one the fourth submission proposed, and it is the first time an SFC has been assigned a role that
   survives contact with the record.
4. **It proposes to stop solving `4.29e9` sites.** That is the correct engineering instinct, and it is the one
   recommendation in this document I would act on first.

A submission that reads the record accurately deserves its replacement tested on its own terms. `P1`–`P8` do that.

---

## 3. The premise, and why the layer is wrong

The submission's §I claim 2 says the old framework *"forcibly maintained connecting edges in vacuum regions or
between voxels without physical contact, thereby generating spurious stresses during dimensionality reduction."*

**This is true — of the submission I rejected last round.** `E_ARAP` was an energy functional imposed on a body that
had none, and any such functional generates a stress field with artefacts at every interface it cannot satisfy.

**It is false of the record.** `KIN-DYN` §6, registered at the governor's acceptance:

> *"D2 performs no deformation. Each layer is translated as a rigid body to its lattice site and joined
> edge-to-edge, with vacuum between pieces. Intralayer strain is therefore zero **by construction**."*

There is no stress field in `D2`, so nothing was forced and nothing became spurious. Measured: `0` occurrences of
"spurious stress" anywhere in `docs/`.

So the correction repairs the previous submission's error rather than the record's state. It moves from *an energy
that deforms* to *an energy that does not act* — and the record's position was **no energy at all**. The right move
was to delete the functional, not to add a second term to it.

> `E_total = E_ARAP + λΣΨ`, with `ΣΨ = 0`, is `E_ARAP`. The submission ends exactly where the last one was rejected.

---

## 4. Why the potential cannot act — three numbers, then an exhaustion

### 4.1 The three numbers

| quantity | value | what it means |
| --- | --- | --- |
| nearest `N_phys` pair at `d_2D` | `0.4001 m = 1.861e9 δ` | the deposit holds every neighbour one `pitch` away |
| `α` needed for a `1%` contribution | `≤ 13.236 m⁻¹` | against a physical `α = 2e10 m⁻¹` — short by **`1.51e9×`** |
| `r_cut` needed for one pair to contribute | `≥ 0.4001 m` | against a physical cutoff `≤ 1e-9 m` — short by **`≥ 4.0e8×`** |
| dimensionless group `Π = α(pitch − d₀)` | **`8.00e9`** | a potential that acts has `Π ≲ 5` |

The `α` sweep, with the cutoff lifted so nothing is truncated:

| `α` (m⁻¹) | `Σ Ψ / D_e` |
| --- | --- |
| `2.0e10` (physical) | `0.000e+00` |
| `1.0e9` | `0.000e+00` |
| `1.0e7` | `0.000e+00` |
| `1.0e4` | `0.000e+00` |
| `1.0e2` | `-8.58e-15` |
| `1.324e1` | `-1.02e+01` |
| `1.0` | `-9.09e+02` |

Four orders of magnitude of `α` give **exactly zero** in double precision. The term is not small — it is absent. To
make it present you need `α ≈ 1–10 m⁻¹`, i.e. a spring with a `10 cm` stiffness length. That is not an interface
potential; it is a macroscopic elastic tie, and it is exactly what `KIN-DYN` removed.

### 4.2 The exhaustion

Three branches, computed at `d = pitch`:

| branch | `Ψ(pitch)/D_e` | force at `pitch` | consequence |
| --- | --- | --- | --- |
| **(i)** `d₀ = δ`, `α` physical | `0.000000` | `0.000000` | term vanishes |
| **(ii)** `d₀ = pitch` | `−1.000000` | **`0.000000`** | every nearest pair sits *at* the minimum: a constant `−D_e` per pair and **zero force**. It cannot move the map. Any displaced pair is pulled *back* onto `pitch` — re-imposing a lattice the lattice already has |
| **(iii)** `α = 1 m⁻¹` | `−0.891` | `0.442` | acts, and pulls neighbours off `pitch` toward `δ`, contradicting a locked constant by `1.861e9×` — prohibited |

There is no fourth branch: `d₀` must be either near `δ` (then (i) or (iii)) or exactly `pitch` (then (ii)), and `α` is
either physical (i) or not (iii). **Every branch is inert or prohibited.**

`d₀` is not in the submission's tuning list — it names `(D_e, α, r_cut)` — and `d₀` is the only parameter that decides
which branch you are in. That omission is `P5`, and it is why the tuning phase proposed in §IV.2 would tune three
knobs while the switch that matters stays unset.

---

## 5. `MR2-D` promoted to a certificate

The submission calls `MR2-D` *"the only formulation capable of clearly distinguishing smooth unfolding from brute-force
destruction, **proving** that **as long as** true physical interfaces are not severed, local weak-force relationships
can be perfectly preserved."*

Both halves fail:

1. **The antecedent is false.** Measured, and reported last round: `100%` of interface contacts are severed —
   `d_3D = 0 → d_2D ≈ 1.2e4 m`. So the implication is vacuously true and certifies nothing. An implication whose
   antecedent never holds cannot distinguish a correct map from an incorrect one.
2. **`MR2-D` has no threshold.** It was registered to be *descriptive*. A metric with no threshold cannot "prove" a
   preservation claim — it reports a separation. The word *"proving"* is unsupported by the metric that names it.

This is the exact move `MR1.1` exists to prevent: a statistic that survives a scramble being read as evidence of an
image. `MR2-D` survives this round **only** as a diagnostic, and its two columns stay what they are:

| pair class | `d_2D` (POC) | `d_2D/pitch` | `d_2D` (`DEMO-1`) |
| --- | --- | --- | --- |
| axial (`n`, `n+1`), all four shells | `0.400100 m` | `1.0000` | `0.400100 m` |
| interface (`d_3D = 0`) | `6.402–6.813 m` | `16.0–17.0` | `≈ 1.2e4 m` |

---

## 6. The POC is a code test, not a scale model — and that is fine if it is declared

The request is 500–1000 voxels. Fixing `pieces = 1024` and `M = 4` fixes `N_layer = 256`, which then fixes the height:

```
H_poc = 256 δ = 5.504e-8 m        (locked H = 0.2300 m)
aspect_poc = H_poc / 2r₄ = 3.058e-7     (locked aspect = 1.2778)     off by 4.179e6×
```

or keep `H = 0.23` and let the spacing float: `H/N_layer = 8.984e-4 m = 4.179e6 δ`.

**At 1024 pieces one locked constant must move by `4.18e6×`.** The POC necessarily abandons `pitch/δ = 1.861e9`, and
that ratio is the entire content of `P1`–`P4`. So the POC can validate code paths, data structures and solver
convergence — and it cannot validate the physics of `DEMO-1`, because in the similar regime (`Π = 8e9`) the potential
is a step function that evaluates to zero.

> Either the POC is not similar to `DEMO-1`, or it reproduces the null result. Both branches leave `§4` standing.

That is not a reason to refuse the POC. It is a reason to **declare its scope in the specification**, which is what
`DEMO-1` did for itself (`self-limitation: may not contain a tier threshold`). A POC that claims to validate the
physics will be quoted as having done so.

---

## 7. `§IV` against `§V`, and the engineering claims

**Scale.** `§IV` declines the `4.29e9` scale; `§V` optimises for it. Ratio `4.18e6`. At `1024` pieces the entire
state is `4.0 kB`; bit-packing to "32 bits (4 bytes)" saves **zero bytes**, because 32 bits *is* 4 bytes. Memory
mapping and octrees save nothing at that size. The appendix is written for the problem the document says it is not
solving.

**The bit budget does not close.** `6` bits/axis `×3` + normal `3` + material `7` = `28`, leaving `4`. But `6` bits
addresses only `64` positions per axis; at `65536` sites per axis position alone needs `48` bits. With `64³` chunks
(`16,324` chunks, `14` bits of index) the requirement is **`42` bits**, i.e. `10` short of the claim.

**`CG` is the wrong solver for half the objective.** With the Morse term the objective is nonlinear, so plain CG (a
linear solver) cannot minimise it — nonlinear CG can, and is memory-light, but that is a different algorithm from the
one named. And for ARAP alone the global step is a **constant** sparse system, so the standard method is one
prefactored Cholesky plus a back-substitution per iteration; no iterative solve is needed. A sparse Hessian is also
not a dense `(3N)²` matrix — sparse Cholesky on a voxel graph is routine. The baseline the comparison rejects is a
strawman.

**Two of four Windows settings are counterproductive here.**

| setting | submission | what it actually does for a memory-bound job on `32 GB` |
| --- | --- | --- |
| `MemoryCompression` | disable | compression **reduces** page I/O; disabling it **increases** it. Trades a cheap CPU cost for an expensive disk cost |
| `PageCombining` | disable | dedups identical pages — a *large* win for a voxel grid full of identical empty blocks. Disabling removes it |
| `DisablePagingExecutive = 1` | set | pins kernel code in RAM, **reducing** memory available to the application on a `32 GB` box |
| pagefile on non-system NVMe, fixed size | set | sound — but SSD random access is `~10³×` slower than RAM; it is not a substitute for fitting the working set |

---

## 8. What is adopted

1. **`SFC-INDEX`** — the repositioning, under a new symbol. A space-filling index is a legitimate cache-locality tool,
   *but it indexes the object*, not the canvas; it is a different construction from `SIGMA-DEMO` and **may not be
   called `σ`**. It is also unnecessary below `~10⁶` pieces, so it is not part of the POC.
2. **`POC-1024`** — the micro test case: `M = 4` shells × `256` layers, Hilbert order 5 on `32²`, occupancy `1.0000`.
   **Declared scope: code validation only; not a scale model; may not be cited about `DEMO-1` physics.**
3. **`N_phys`** — registered as the symbol for the genuinely-contacting pair set. It is non-empty and it is the right
   object to count. It is *not* a set the potential can reach (`0` members inside any physical `r_cut`).
4. **`MR2-D`** — unchanged: threshold-free, descriptive, no admission power, may not be read as a pass.
5. **The diagnosis in §I** — claims 1 and 3 are accurate and are now the record's own summary of what was wrong with
   the ARAP submission.

Explicitly **not** adopted: `E_total`, `Ψ`, `λ`, `D_e`, `α`, `r_cut`, `d₀`, the stress figure, and `§V` in the form
submitted.

---

## 9. My own defects this round

1. **`P7`'s number is wrong by `4.33×`.** I predicted `3.2e9` `N_phys` pairs at `DEMO-1` scale; the structure I
   described (`2` axial + `3` per adjacent shell per interface) implies `1.387e10`. I multiplied by `N_layer` once
   where the interface term needs it three times. The qualitative claim held; the registered figure did not.
2. **`A3` first reported a false FAIL** because I counted "vertex set" across the whole corpus — and *my own previous
   ruling* puts that phrase in `docs/` while rejecting it. A whole-corpus count cannot answer a question about what
   the record declares. Fixed by restricting to `docs/specs/` (`0`, `0`, `shell 5`, `pieces 10`).
3. **`A2`'s framing needed a correction I made only while writing §3.** My first pass called the "spurious stresses"
   claim *invented*. It is not invented — it is true of the previous submission. The ruling is sharper for saying so,
   and the verdict (the correction repairs the wrong layer) is the same.

Item 2 is the third round running in which a keyword test failed because the corpus contained my own adjudication
text. The structural lesson, now recorded: **a check about what the record says must be scoped to the documents that
*say* it, not to the documents that discuss it.** `docs/specs/` is the speaker; `docs/decisions/` is the commentary.

---

## 10. What this does not change

1. `MR1` — zero readable cells. `MR2-CLOSE` stands; `MR2-D` stays descriptive.
2. `KIN-DYN` §6 — now tested twice in two rounds, and violated twice. It is doing its job.
3. `DEMO-1` — hash-locked, untouched. Its §4.2 declared loss is confirmed again: `100%` interface destruction.
4. The four tiers and `threshold_lock.json` — byte-identical (`5f324e15…`).
5. `GD10`, `GD11` (body), `GD6`, `GD9` — untouched, still open.
6. No physics is established by this document, and none was claimed.

---

## 11. Still open

`GD6` (`ME3`'s `φ`, blocks Phase 3) · `GD9` (route objective) · `GD10` (plates per cell) · `GD11` (body's `σ`) ·
route governance (phased v2 vs the matrix) · whether a `DEMO-1` frame counts toward `G1` · citation repair.

**One question this round raises that the governor owns:** the POC is now the only concrete build proposal on the
table, and it is a *code* test that cannot settle a *physics* question. If the purpose of building it is to make
progress on `G1`, it will not. If the purpose is to establish the data structures and solver for a later, correctly
scaled run, it is the right first step and should be scoped as such before any code is written.

---

*Content generated by AI*
