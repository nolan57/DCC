# Registration — RQ-16, the periodic isolated-plate scene class

**Written before** `src/route/plate_array.py` existed. Predictions `W1`–`W6` below are fixed as of this file's
mtime; the product's mtime must be later and the discrepancy positive. If the file carries an `## Errata` block,
mtime is the append time and the ordering is asserted by the erratum text, not by the clock (the `S4` lesson).

**Object**: `docs/program/round_queue_v1.json` item `RQ-16`; closes `V1`–`V3` of
`runs/MATRIX2/matrix_v2_registration.md` and answers `matrix_v2_spec_v1.md` §10.

**Nature of the run**: adds one declared scene *class* to the calibration set and measures the three
observer-independent tiers on it with the locked estimators and the locked thresholds. It establishes no physics.
`PROVENANCE: NEITHER`.

---

## §1 The scene, declared without a free parameter

A scene is a `128 x 128` field `u` on cells of side `h = 1` (the same grid and the same `h` as all nine
calibration scenes; `threshold_lock.json` `declared_constants.grid` and `cells_side_h`).

```
u[i,j] = 1 if (i mod p) < s and (j mod p) < s  else 0        square plates, lattice pitch p, side s
fill fraction  f = (s/p)^2        (declared, not requested: a scene does not "have" 50 % fill)
```

Four instances, `p` chosen to divide the grid so the array is exactly periodic (no edge defect):

| id | `p` (cells) | `s` (cells) | `f` | why this one |
| --- | --- | --- | --- | --- |
| `PA-8`  | 8  | 6 | 0.5625 | finest pitch the estimator can see |
| `PA-16` | 16 | 12 | 0.5625 | reference |
| `PA-32` | 32 | 24 | 0.5625 | coarsest pitch, same geometry |
| `PA-16f` | 16 | 11 | 0.4727 | fill control: pitch fixed, fill lowered |

**Why `f = 0.5625` and not literally 0.50.** `s` and `p` are integers, so `s/p = sqrt(0.5)` is unavailable;
the nearest integer pairs give 0.4727 and 0.5625. `RQ-16` asked for "50 % fill, `pitch/h = 1`", which is
over-determined: fill fixes `s/p`, and `pitch/h = 1` fixes `p = h = 1`, at which `s` has no integer value with
`f < 1`. **The delivered pair is `f = 0.5625` with `p/h` swept 8/16/32**, and the fill clause is met to
`0.0625` while the pitch clause is replaced by a sweep, because a pitch of one cell is a uniform field.

**Why this is the deposit's class.** The deposit's own geometry is `sup d3D = 0.292062 m` inside
`pitch = 0.400100 m` (`runs/MATRIX/mr2_arap_results.txt` line 45), i.e. `s/p = 0.7300`,
`f = 0.5330`. The reference instance is `s/p = 0.7500`, `f = 0.5625` — within 2.7 % and 3.0 points of the
deposit's measured ratios. This is the closest a declared integer scene can come, and the difference is stated
rather than absorbed.

`PA-16f` exists because `V1` and `W3` below must not be confounded by fill: 0.4727 vs 0.5625 at the same pitch
separates "the verdict is about `f`" from "the verdict is about `p`".

---

## §2 The measurement, named exactly

Estimators are **imported from `src/route/structure_tiers.py`, not re-implemented**; the import re-derives
`P0(null)` and `q2(null)` from the same 16 seeds (4000–4015), and the product prints those two numbers so the
reproduction is checkable against `runs/MATRIX/structure_tiers_results.txt` to the last digit.
Thresholds are **read from `runs/MATRIX/threshold_lock.json`**, never written into the new file.

Shuffle control: pixel permutation, `numpy.random.default_rng(9999)`, applied to `PA-16` only.

---

## §3 Predictions

`W1` — **`Q0 < 0` on all four instances, in `[-9.2, -8.7]`, and identical across the pitch sweep to within
0.05.** Basis: superlevel filtration of a two-level field gives every plate one component of lifetime `1.0`,
so `P0 = f` and `Q0 = 1 - f/P0(null) = 1 - 0.5625/0.05639903 = -8.974`.
*Falsifier*: any `Q0 >= 0.5`, or a pitch-dependence larger than 0.05.

`W2` — **`Q1` scales with `p` and crosses the locked threshold `4.0` inside the sweep:
`Q1(PA-8) ≈ 3.8`, `Q1(PA-16) ≈ 7.6`, `Q1(PA-32) ≈ 15.2`, each within ±20 %.** Basis: the axis-averaged
autocorrelation of a duty-cycle-0.75 square wave falls as `1 - l/s` and crosses `e^-1` at `l ≈ 0.474 p`.
*Falsifier*: all three on the same side of 4.0.

`W3` — **`Q2 >= 0.95` on all four instances, pitch-invariant to within 0.03.** Basis: a periodic array is
determined by its 16-level west/north context, so `H(u|context) ≈ 0` and `Q2 → 1`.
*Falsifier*: any `Q2 < 0.5`.

`W4` — **the shuffle control leaves `Q0` unchanged (`|ΔQ0| <= 0.02`) and destroys `Q2` (`Q2 < 0.10`).**
Basis: for a two-level field `P0` is fixed by the marginal, hence by `f` alone; `Q2` is not.
*Falsifier*: `|ΔQ0| > 0.5`, or shuffled `Q2 >= 0.5`.

`W5` — **`L0`'s pass set and the deposit's class are disjoint.** From `Q0 = 1 - f/P0(null)`, `Q0 >= 0.5`
requires `f <= 0.5 P0(null) = 0.02820`: no scene whose minority phase is *spatially isolated* and covers more
than **2.82 %** of the area can pass `L0`, at any pitch, on any grid. *Falsifier*: an isolated-plate instance
with `f > 0.0282` that passes `L0` — i.e. `Q0 >= 0.5` anywhere in this product.

`W6` — **the `L1` verdict in `matrix_v2_spec_v1.md`'s `R2` row is a property of `h`, not of the scene.**
Passing `L1` at one pitch and failing at another, for the same geometry, is the demonstration.
*Falsifier*: a single verdict for all three pitches.

### What `W1`–`W6` decide among the already-registered predictions

| id | registered | predicted outcome here |
| --- | --- | --- |
| `V1` | severed `Q0 < 0.5` | **CONFIRMED** if `W1` holds (it predicts ≈ `-8.97`) |
| `V2` | severed `ξ/h < 4`, "`ξ = pitch`, `h = pitch` ⇒ ≈ 1" | **FALSIFIED as stated**: `ξ/h >= 4` at `p = 16` and `p = 32`. `V2` had no scale in it, and the scale is the whole content |
| `V3` | severed `Q2 >= 0.5` **and the pass is non-evidential** | **first half CONFIRMED, second half FALSIFIED** if `W4` holds: a shuffle kills `Q2`, so the pass *is* evidential. `V3` imported the non-evidentiality of `TILED` (`MR1.1`) into a scene where it does not hold |

`V2` failing is the informative event, and it is not repaired here: a prediction amended after the run is not a
prediction. It is superseded by `W2`/`W6`, which carry the scale.

---

## §4 The visualisation question this run settles

The deposit is a periodic array of isolated plates. If `Q0` cannot separate that array from its own shuffled
version (`W4`), then **no rendering that shows "the deposit's structure" can be evidence for `Q0`** — `Q0` is
blind to arrangement by construction. Which is why the honest deliverable of this run is a *table*, and any
picture it licenses is a picture of a declared field, labelled `FL1`.

---

## §5 What this run does not do

- No `sigma_s`, no `Q3`, no observer — `Q0`–`Q2` are observer-independent and `Q3` is `BLOCKED-ON-INPUT`.
- No new threshold, no lock edit, no change to `structure_tiers.py`.
- No claim about the deposit's *content*: `DEPOSIT-BLIND` stands, `MR1.6` stands. The scene is a declared
  analogue, not the deposit.

*Content generated by AI*
