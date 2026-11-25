# Pre-registration — four-dimension re-anchoring (`FOURDIM-V2`)

**Written before** `src/route/fourdim_check.py` exists. Thresholds, statistics and falsifiers below are fixed here.
**Object**: `DEMO-1` (locked, `runs/FRONT/demo_lock.json`): `r1 = 0.020`, `r2 = 0.045 ∓ 0.006·sin`, `r3 = 0.070 ± 0.008·sin`,
`r4 = 0.090`, `H = 0.230 m`, `M = 4`, `pieces = 4,279,069,764`, `cells = 4,294,967,296`, side `65536`.

## What is being tested

Four claims, one per dimension, each taken at face value:

| # | claim as submitted | what would refute it |
|---|---|---|
| `A1` | components + genus are 100% consistent between object and 2D projection | component counts differ by any amount on the *material* deposit |
| `A2` | a distance `d` exists with a declarable `ε` | `d` is not determined by the physics (spans > 1 decade across admissible conventions) |
| `A3` | `I(2D; 3D)` rejects noise | `I` cannot separate a scrambled map from the declared one **under the estimator the submission names** |
| `A4` | an observer `O` with unbounded capacity can extract the structure | the witness for `O` is the holder of `σ`, i.e. the criterion is satisfied by an assumption we make |

`A3` is the one where I expect to be wrong. My earlier refusal (`T2`) leaned on `Q2` surviving a shuffle; `Q2` is a
predictability statistic, not a channel mutual information, and the two are not interchangeable. If `I` separates them,
the governor's claim stands on this point and my `T2`-based reason does not transfer.

## Predictions

| id | prediction | falsifier |
|---|---|---|
| `P1` | `b0`(material deposit) `= 4,279,069,764`; `b0`(object solid) `= 1`; gate fails by `4.279e9` | any other count |
| `P2` | object's four shells touch (`edges[k+1] = edges[k+2]`), so its union is a solid cylinder: `(b0,b1,b2) = (1,0,0)`, boundary genus `0` | measured `b1 ≠ 0` |
| `P3` | genus clause passes for **every** deposit of flat plates (`0 = 0`) — it is a tautology, not a test | any deposit of flat plates with genus ≠ 0 |
| `P4` | admissible `d` values span `≥ 5` decades: `0` (index) / `0.0575` (mid-slice `W1`) / `0.115` (mid-slice Hausdorff) / `1.311e4 m` (true scale) | span `< 1` decade |
| `P5` | `H(label) = 1.739 ± 0.001` bits for `DEMO-1` at `z = H/2` | outside band |
| `P6` | `I_aligned = H(label)` to `< 1e-9`, **identically for three arbitrary σ** — i.e. invariant when the key is held | `I_aligned` varies with σ by `> 1e-6` |
| `P7` | `I_naive` at the same coordinates: `< 0.02` bits for the declared scroll σ, `> 1.70` bits for a bullseye layout — full range `[0, H]` from the same physics | both in the same decade |
| `P8` | homogeneous body (one content symbol): `H = 0`, `I ≡ 0` under every estimator | `I > 0` |
| `P9` | `I_min > 1.74` bits is unachievable for `DEMO-1`; ceiling is object-dependent, not mechanism-dependent | `I` exceeds `H(label)` |
| `P10` | with `σ`, inverse recovery `= 1.000000`; without `σ`, no value — so `A4`'s witness is the key holder | recovery `< 1` with the key |

## Declared conventions (fixed here, not after seeing results)

- **label field `Y`**: component index `k ∈ {0,1,2,3}` of the piece occupying a position; `∅` for vacuum. Area fractions
  taken at `z = H/2`.
- **material reading**: the deposit's connected components are the plates (vacuum gaps, `front_sweep_v1` §2).
- **quotient reading**: pieces sharing a declared component label count as one component. Reported separately, because
  it is a statement about `σ` and must not be silently substituted for the material reading.
- **`I_aligned`**: mutual information between the display pixel's content and the object label at the position the key
  maps that pixel to.
- **`I_naive`**: mutual information between the display pixel's content and the object label at the *same image
  coordinates* (the "hold the picture next to the object" estimator, no key).
- **distance**: metres. `W1` = 1-Wasserstein, `d_H` = Hausdorff, both between the mid-sweep slice and the solid.

## Discipline

Results are written to `runs/MATRIX/fourdim_results.txt` and are **not edited** afterwards. Any failed prediction that
turns out to be my encoding error is appended as an erratum with the recomputation shown, as in the last five rounds.
