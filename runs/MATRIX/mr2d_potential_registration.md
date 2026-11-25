# Registration of predictions — the `MR2-D` / truncated-Morse submission

**Received**: 2026-11-22.
**Verbatim record**: `runs/MATRIX/mr2d_potential_submission_verbatim.md` (`PROPOSED`, governs nothing).
**Written before the executor exists.** This file is the lock: the fifteen predictions below were fixed before
`src/route/mr2d_potential_check.py` was authored, and none may be revised after the product is read.

**Provenance**: `NEITHER`. Adjudication of a submitted claim against the registered record. Establishes no physics,
creates no readable cell, admits no threshold.

---

## 0. What is different about this submission

The previous four argued *for* a construction. This one **concedes** the ruling — it states the three defects of the
ARAP submission accurately (`§I`), abandons the marginal KL, adopts `MR2-D` by name, and quotes the `X1` decomposition
(`99.2%`) correctly. That is new, and it is worth saying plainly: **the diagnosis is accurate.** A submission that
reads the record correctly is entitled to have its replacement tested on its own terms rather than against the old
criteria.

So the test is narrow. The replacement rests on **one** mechanism: replace the topological "do not cut" constraint
with a truncated Morse potential on the set `N_phys` of genuinely-contacting pairs,

```
E_total = E_ARAP + λ Σ_{(i,j) ∈ N_phys} Ψ(d_2D(i,j))
Ψ(d) = D_e (e^{−2α(d−d₀)} − 2e^{−α(d−d₀)})   for d ≤ r_cut,   else 0
```

If that term cannot act on the deposit, the whole document reduces to `MR2-D` (already registered, §5 of the ruling)
plus an engineering appendix. That is what `P1`–`P4` measure.

## 1. Why the potential is expected to be inert, stated before measuring

Three numbers, all locked:

| quantity | value | source |
| --- | --- | --- |
| deposit's minimum separation of distinct pieces | `pitch = 0.4001 m` | `DEMO-1` §2.1 |
| atomic spacing (the physical interaction scale) | `δ = 2.15e-10 m` | `front_sweep_v1` |
| ratio | `pitch/δ = 1.861e9` | `P5` last round |

A Morse potential with a physical stiffness length decays as `e^{−α·d}` with `α ≈ 2 Å⁻¹ = 2e10 m⁻¹`. At
`d = 0.4001 m` that exponent is `8e9`, so the term is zero to every representable precision. The prediction is
therefore that **the potential adds nothing to the map**, and that the only way to make it act is to choose `α` small
enough that it is no longer a physical interface potential — a two-branch refusal, the same form as last round's.

## 2. The predictions

`FAIL` in the predicted-verdict column means *I expect the submission to be wrong on that point*.

| # | prediction | predicted verdict |
| --- | --- | --- |
| **P1** | On the deposit, `Σ Ψ(d_2D)` over `N_phys` is **exactly `0.0`** for a physical Morse parameter set (`α = 2e10 m⁻¹`, `d₀ = δ`, `r_cut = 10δ`), for every `λ` and every `D_e` | **exactly 0** |
| **P2** | A contribution of `1%` of `D_e` requires `α ≤ 5.30/(pitch − d₀) ≈ 13.2 m⁻¹`. A physical `α = 2e10 m⁻¹` exceeds that by `≈ 1.5e9×` | **`α ≤ 13.2 m⁻¹`, shortfall `1.5e9`** |
| **P3** | `r_cut` must be `≥ pitch = 0.4001 m` for any pair to contribute. A physical interaction cutoff is `≤ 1e-9 m`, so `r_cut` must exceed it by `≥ 4.0e8×` | **`r_cut ≥ 0.4001 m`** |
| **P4** | The governing dimensionless group is `Π = α(pitch − d₀)`. For the deposit `Π = 8.0e9`; a potential that acts has `Π ≲ 5` | **`Π = 8.0e9`** |
| **P5** | `d₀` is **omitted** from the submission's parameter list (`D_e`, `α`, `r_cut`), yet it alone fixes the equilibrium distance and is the one parameter that must equal `pitch` | **omitted** |
| **P6** | The trichotomy: (i) `d₀ ≪ pitch` and `α` physical ⇒ `Ψ ≡ 0`; (ii) `d₀ = pitch` ⇒ every nearest pair sits at the minimum, so `∇Ψ = 0` and the term exerts **no force**; (iii) `α` small enough to act ⇒ the term pulls pieces off the locked `pitch` lattice. In all three the term either vanishes or is prohibited | **trichotomy holds** |
| **P7** | `N_phys` (pairs with `d_3D ≤ δ`) is non-empty: `2` axial per piece plus `3` per adjacent shell per layer, giving `≈ 3.2e9` pairs at `DEMO-1` scale | **≈ 3.2e9** |
| **P8** | The fraction of `N_phys` pairs with `d_2D < r_cut` is **exactly `0`** for any physical `r_cut`. The set the potential is defined on is disjoint from the set it can reach | **0** |
| **P9** | `MR2-D` on `DEMO-1` reports axial `d_2D/pitch = 1.0000` and interfaces at `≈ 1.2e4 m` — i.e. **`100%` of true physical interfaces severed**. So the submission's *"as long as true physical interfaces are not severed"* has a **false antecedent** for the object of record, and its "proof" is vacuous | **antecedent false** |
| **P10** | `MR2-D` has no threshold, so it cannot "prove" anything; it reports. The word *"proving"* is unsupported by the metric it names | **cannot prove** |
| **P11** | The `§IV` visualisation ("stress distribution … high stress in red, natural ruptures") is **forbidden by `KIN-DYN` §6**, which names *"differential strain, or fracture"* — verbatim the two things the figure would show | **scope-clause conflict** |
| **P12** | `§IV` and `§V` are at war: `§IV` declines the `4e9` scale, `§V` optimises for it. At `1000` pieces the whole state is `~4 kB`, so bit-packing to `32` bits saves `0` bytes and memory-mapping saves nothing | **ratio `4.3e6`, savings `0`** |
| **P13** | `CG` is a **linear** solver; with the Morse term the objective is nonlinear, so CG cannot minimise `E_total`. For ARAP **alone** the global step is a *constant* sparse system, so the standard method is one prefactored Cholesky, not iterative CG — the baseline the submission compares against is the wrong one | **category error** |
| **P14** | Two `§V` settings are counterproductive for a memory-bound job on `32 GB`: memory compression and page combining both **reduce** page I/O; disabling them increases it. `DisablePagingExecutive = 1` reduces RAM available to the application | **2 of 4 harmful** |
| **P15** | **Verdict**: `PARTIALLY ACCEPTED`. Adopt the staged POC, `MR2-D` as sole diagnostic, and the SFC repositioning (renamed, `SFC-INDEX`). Reject the potential (inert or prohibited), the stress figure (forbidden), and most of `§V` | **PARTIALLY ACCEPTED** |

## 3. What I expect to concede

- **`P1`** could fail if `N_phys` contains a pair at `d_2D` small enough to sit inside the decay length. It should
  not, because the deposit's minimum is `pitch`, but if it does the mechanism is alive and the ruling weakens.
- **`P7`** could be a different count if the interface bookkeeping (annuli sharing a boundary circle) is modelled
  differently than I have. The number is not load-bearing; `P8`'s zero is.
- **`P13`/`P14`** are judgements about engineering practice, not measurements of this record. If I am wrong about the
  Windows settings the submission's implementation plan is better than I credit it, and that part of the ruling
  should be withdrawn.

## 4. The one thing to protect

`MR2-D` was registered last round as a **threshold-free diagnostic**. This submission adopts it and then asks it to
*prove* a preservation claim. That is the exact move — a diagnostic promoted to a certificate — that `MR1.1` was
written to prevent. Whether `MR2-D` survives this round depends on whether it can be kept descriptive.

---

*Content generated by AI*
