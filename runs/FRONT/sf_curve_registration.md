# Pre-registration — adjudicating the space-filling-curve submission

**Written 2026-11-22, before `src/route/sf_curve_check.py` exists.** Predictions are fixed here so that a
FAIL is visible as a FAIL. Nothing in this file may be edited after the run; corrections go in an erratum
appended to the results file.

Submission: `runs/FRONT/sf_curve_submission_verbatim.md` (PROPOSED).

---

## 0. What the submission claims, reduced to four propositions

| # | proposition | type |
| --- | --- | --- |
| **S1** | `D2` is an identity map + relabelling, with no deformation and no stress | premise |
| **S2** | therefore the algorithm is "lossless rearrangement of information", not projection | inference |
| **S3** | the applicable algorithms are space-filling curves / spiral traversal, at Planck-cell resolution | conclusion |
| **S4** | the resulting image is a structured, software-only-readable "data map" | consequence |

`S1` is already `KIN-DYN` (`front_sweep_v1` §2.1, in force). The audit therefore has to ask whether `S2`→`S3`
follows, and whether `S3` is even admissible.

## 1. The question the submission actually raises, which the record does not answer

`front_sweep_v1` §2 step ② says each layer is "translated to **its** lattice site". The possessive is doing
work: it presumes a mapping `σ : n_z → (u, v)` from layer index to site coordinates that **no document
defines**. §5 constrains the *order* only by transport speed and accepts two different families. So `σ` is
genuinely underspecified, and any frame that draws site **content** (as opposed to occupancy) has already
chosen it implicitly.

**This is the part of the submission that is right, and it was not previously registered.**

## 2. Predictions

Each row was fixed before the executor was written. "Pass" means the measured value matches the prediction.

### A. Anchors and presuppositions (text checks on `docs/`)

| id | prediction | expected |
| --- | --- | --- |
| **P1** | no document supplies a layer→site assignment rule | `0` hits |
| **P2** | `front_sweep_v1` §2.1 contains the sentence denying selection of `Π` | `1` hit |
| **P3** | the record contains no projection vocabulary at all (`orthographic`, `perspective projection`, `Hilbert`, `space-filling`, `spiral`, `serpentine`, `raster`) | `0` hits |

`P2` is the decisive one: if §2.1 is in force, `S2`→`S3` is negated by a clause already governing the
mechanism, not by a new argument of mine.

### B. Does the selection principle select? (vacancy test, `S10` class)

| id | prediction | expected |
| --- | --- | --- |
| **P4** | number of bijections satisfying *both* cited constraints (injectivity ⇒ information conserved; per-plate rigid translation ⇒ zero deformation) | `log10 N! = 1.14e11` with `N = 1.18e10` |
| **P5** | randomly sampled bijections satisfy both constraints | `3 / 3` |

If `P4` and `P5` pass, the cited constraints are invariant over the whole symmetric group, so they cannot
rank one traversal above another, and `S2`→`S3` is a non-sequitur.

### C. The voxel reading, priced

`S3` is written at voxel resolution ("every Planck-scale grid cell (or voxel)"). Priced at the deposit's own
in-plane resolution `a = δ = 0.215 nm`:

| id | prediction | expected |
| --- | --- | --- |
| **P6** | pieces if every voxel is its own piece | `6.05e27` (> `1e27`) |
| **P7** | array side required, at the registered `0.4001 m` pitch | `7.78e13` sites → `3.11e13 m` (`208 AU`) |
| **P8** | factor by which that exceeds the frozen canvas (`36.06 km`) | `8.6e8` |

`P6`–`P8` are the cost of reading `S3` literally. Note the census is **FROZEN**: a proposal that changes the
site count by `17` decades changes a frozen quantity.

### D. The grid `S3` assumes

| id | prediction | expected |
| --- | --- | --- |
| **P9** | `n_max(ℓ_P) = ℓ_P/δ` | `7.52e-26 < 1` ⇒ no admissible configuration |
| **P10** | registered unit sizes are *not* uniform, so "size of all physical units remains constant" is false of the record | plate-area span factor `8.19` |

### E. What the algorithm would actually buy (the steelman, measured)

Implement three candidate `σ` on an `S×S` square and measure two quantities per candidate:
`ρ` = median `|Δn|` between vertically adjacent sites ÷ median `|Δn|` between horizontally adjacent sites
(anisotropy of the z-mapping), and the fraction of `|Δn| = 1` pairs that land on 4-adjacent sites
(contiguity).

| id | prediction | expected |
| --- | --- | --- |
| **P11** | raster `ρ = S` exactly | `256` at `S = 256` |
| **P12** | Hilbert `ρ ≤ 2` | pass |
| **P13** | spiral `ρ ≤ 3` | pass |
| **P14** | contiguity `= 1.000` for **all three** | pass ⇒ contiguity cannot discriminate |

If `P11`–`P14` pass, the submission's algorithm is not *unselected by accident*: it **dominates** the trivial
order on `ρ` and **ties** it on contiguity. That is a real merit the submission never claims, and it is a
display merit, not a physical one.

### F. Already satisfied

| id | prediction | expected |
| --- | --- | --- |
| **P15** | D2's map is already injective, so "information conservation" is satisfied without change | pass (`front_sweep_v1` §2 ② + census) |

## 3. Declared falsifiers of my own reading

- If `P2` = 0, then §2.1 does not say what I think it says and the negative selection argument falls; the
  submission's derivation would have to be judged on `P4`/`P5` alone.
- If `P14` fails for any candidate, then contiguity *does* discriminate and the steelman in `E` is wrong.
- If `P8` < `1e6`, the voxel reading is affordable and my central refusal is wrong.
