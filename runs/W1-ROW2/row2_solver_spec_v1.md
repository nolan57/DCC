# Solver spec — W1 / row 2, W1-ROW2-ARTIFACT-01

**Status**: pre-registration, stage A. `docs/program/RESEARCH_PROGRAM_v1.md` v1.1.1 §5.3 splits
card / manifest / solver spec / run record; this is the third.

## 1. What is solved, and what is not

| object | treatment |
|---|---|
| 3D body state `U` | **prescribed**: the registered synthetic phantom; no equation of motion |
| front `φ` | **prescribed law** `z_f = min(H, v t)`, `v = c/√2`; no front equation solved |
| 2D output `u` | **derived** by the map `M` of the card §4 |
| tiers `T0–T3` | **measured** on `u` with the locked estimators |
| effective-2D label | **computed** on a declared surrogate potential, then withheld (`NOT-MEASURED`) |
| `C3` decay | **declared overlay** with an imported `τ`; not solved |

No PDE is integrated. No conservation law is enforced beyond the identity `V_deposited = V_swept`.
The frame is a presentation of this computation (`GEOMETRY: PRESCRIBED (D2)`), and `R3` frame
reproduction is **not** claimed.

## 2. Fields handed to the estimators

| field | grid | definition |
|---|---|---|
| `plate` | 128×128 | tissue-density channel `ρ_class/ρ_max` of the axial slice at `min(z_f, 1.70 m)` |
| `canvas` | 128×128 | per-site mean layer density over the array raster; a block is filled iff the front has passed it |

The two fields answer different questions: `plate` is what one deposited sheet carries; `canvas` is
what the assembled array carries at 36 km scale. They are not two renderings of one quantity.

## 3. Estimator identity (programme §4.3)

| item | value |
|---|---|
| authority | `docs/specs/intrinsic_structure_tiers_v1.md` v1 (T0 §2, T1 §3, T2 §4, T3 §5) |
| implementation | `src/analysis/tiers_core_v1.py`, a verbatim extraction of `src/route/structure_tiers.py` |
| grid / bins | 128×128 / 64 |
| T2 context | 16 levels |
| T3 smoothing | DoG with `σ = ξ/2` and `2ξ`, `C_eye = 0.01` |
| null ensemble | 16 uniform realisations, seeds 4000…4015 |
| null means | `P0 = 5.639903e-02` (sd `4.69e-04`), `Q2 = 0.138201` (sd `7.67e-04`) |
| threshold lock | `runs/MATRIX/threshold_lock.json`, sha256 `1224458d58f179f8d3cbcec7ea65f6df5c1fe72fe88169ca313b0bbf5bc5a20d` |
| lock's own record | `5f324e1513c5df0a8c60539c0c50af6ea23bd14924932115b2c926ebbc12b1cc` |

## 4. Fragment-count provenance (programme §4.8)

| required item | value | status |
|---|---|---|
| phantom coverage | `z ∈ [0.012, 1.738] m`, full body | REGISTERED |
| pixels per layer | 200×200 | REGISTERED |
| sample size (layers counted) | not stated in the registered record | **UNREGISTERED** |
| per-region mean | 2.00 (calf→thigh), 1.00 elsewhere | REGISTERED |
| per-region variance | not stated | **UNREGISTERED** |
| weighting of leg / neck / head | thickness-weighted mean over the table → 1.457 | DERIVED here |
| boundary rule (4-connected, slice plane) | 4-connected components in the axial section | REGISTERED |

Because sample size and variance are unregistered, `1.18e10` is labelled a **MODEL ESTIMATE**, not a
counted total, and no error bar is claimed. Stage B prints this label next to every occurrence.

## 5. Discretization declaration (programme §4.8)

- baseline: one atomic layer per slice, `δ = 0.215 nm`, `N_slices = H/δ = 8.0837e+09`.
- control: `δ × 10` or a continuous front — **not run** in this cycle; programme item 6.1(3) remains OPEN.
- consequence: publication item 7 fails, so the cycle is `O0-ARTIFACT`.

## 6. Determinism and seeds

- the phantom is analytic (no RNG);
- the null ensemble is seeded (`4000 + k`, `k = 0…15`);
- the figure has no stochastic element; identical inputs must give byte-identical PNGs at a fixed
  matplotlib version (recorded in the run record).

