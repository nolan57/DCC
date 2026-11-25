# Tier redefinition — pre-registration

**Registered**: 2026-11-22, before `runs/MATRIX/threshold_lock.json` existed and before `src/route/structure_tiers.py`
existed.
**Instruction**: *"Redefine the four tiers as intrinsic-structure criteria that do not refer to the original object; each tier must provide all three of (a) a formal definition referring only to the scenario itself;
(b) a quantity taking values between 'unstructured' and 'structured'; (c) a threshold declared before the run and hash-locked. If any of the three is missing, the tier may not enter the matrix."*
**Spec**: `docs/specs/intrinsic_structure_tiers_v1.md` (§2–§5 are the four `(a)` blocks; §0 is the admission rule).

Nine predictions. Each is stated so that it can fail, and each names what its failure would mean.

---

## A1 — the null must fail `L0`, `L1`, `L2`

On `NOISE` and `NOISE-S` (i.i.d. uniforms, seeds fixed): `Q0 ≈ 0`, `Q1 ≈ 1`, `Q2 ≈ 0`.

- `Q0 ≈ 0` is nearly a tautology (`Q0` is defined by subtracting the null's own mean), so it is a **self-consistency
  check of the implementation**, not a discovery. If `Q0` comes out far from 0 on the null, the persistence code is
  wrong, not the physics.
- `Q2 ≈ 0` is **not** a tautology even with the renormalisation: it verifies that the estimator-bias correction
  actually removes the bias. If raw `q₂(NOISE) > 0.15` and `Q2` afterwards is still `> 0.05`, the correction is
  insufficient at this sample size and `L2` must raise `|Λ|` or lower the context count before admission.

## A2 — `BLANK` must return **no verdict**, never a maximum

`P0(BLANK) = 0` (no components have non-zero lifetime), so the naive `Q0 = 1 − 0/P0(𝒩) = 1` — a blank frame would
score **maximal organization**. The declared precondition `σ_u/Δu ≥ 0.01` must catch this and return **no verdict**
on `L0` and on `L3`.

Predicted: `Q0` is computed as a diagnostic and reported, but the verdict is `NO-VERDICT (degenerate)`, and the
admission test treats no-verdict as **not a pass**. If `BLANK` passes `L0`, the precondition is broken and `L0` is
refused.

## A3 — `DITHER` passes `L2` and fails `L0`, `L1`

Dither = constant field with `5%` of cells flipped by `±3` bins.

- `Q1`: neighbours are independent given the flips, and almost all variance is in the sparse flips, so
  `R(1) ≈ 0` ⇒ `ξ ≈ 1` ⇒ **fail**.
- `Q0`: many tiny components, lifetimes `≈ 3` bins out of `Δu = 3` bins — so lifetimes are *not* tiny relative to
  the range. Predicted `P0` comparable to or above the null's ⇒ **fail**. (This is the one prediction in this file
  whose sign I am least sure of; see A9.)
- `Q2`: the field is a constant plus sparse outliers, so neighbour context predicts the common case ⇒ **pass**.

Purpose: `DITHER` is the separator that stops `L2` from being a restatement of `L0`/`L1`.

## A4 — `STEP` passes `L0` and `L2`, and **passes** `L1`

- `Q0`: one step ⇒ a handful of fully persistent components ⇒ `P0 = O(1/|Λ|)` ⇒ **pass**.
- `Q1`: a monotone ramp has autocorrelation `R(ℓ) ≈ 1 − ℓ/W`, which is non-negative everywhere; averaged over axes
  with the constant direction it crosses `1/e` only at `ℓ ≈ 1.26 W ≈ 161` cells. So `ξ` is the **field width**, not
  a small number, and `Q1` **passes**.

This prediction is deliberately counter-intuitive and I am stating it before the run: **a step edge has a
"characteristic scale" equal to the whole field, and `L1` accepts it.** If that happens, it is not a bug — it means
`Q1` measures "a scale exists", not "a *local* scale exists", and the spec must say so.

## A5 — `GRATING` passes `L0`, `L1`, `L2`

Period `32` cells. `ξ`: `R(ℓ) = cos(2πℓ/32)` on the varying axis, `1` on the constant axis, so the axis-average
crosses `1/e` at `ℓ ≈ 9` ⇒ **pass**. Four crests, fully persistent ⇒ `P0 ≈ 4/|Λ|` ⇒ **pass**. Highly predictable
from the left neighbour ⇒ **pass**.

## A6 — `TILED` passes all four tiers (instrumented channel)

`TILED` is the only calibration scene that models the registered geometry (constant tiles on a lattice, global
structure present only under the canonical order). Predicted: `Q0`, `Q1`, `Q2` all pass, and `Q3 > 2` with `q = 1`.

If `TILED` fails a tier that `GRATING` passes, the tier is responding to the arrangement rather than to structure,
and the layout convention must be declared as a `DC` item before that tier can be used.

## A7 — `L3` is empty under reflection on **every** scene, and `q = 0` is the reason

The registered reflection channel has **zero exposure budget** (`2L/c` exceeds `t_rip` by `√2`; `p2_clock_results`
P2-2), so the channel factor is `q = 0` exactly, hence `Q3 = log₂(1 + 0) = 0` identically, on every scene —
including `TILED`.

Predicted: **0 of 9** scenes reach `L3` under reflection, and the failure is `Q3 = 0` by the factor `q`, not by
`C_ξ` or `ξ`. This reproduces the audit's M5 from the *intrinsic* side, which is the point: M5 was never about the
metric being extrinsic, it was about photons.

Under the instrumented (`q = 1`) channel, structured scenes with `ξ ≥ 2` pass and `NOISE` returns no verdict.

## A8 — all four tiers are ADMITTED

Each of `L0`–`L3` will have `(a)` free of intrinsic-reference tokens, `(b)` demonstrated numerically (null fails,
≥1 control passes), and `(c)` a threshold whose hash verifies. Predicted: **4 of 4 ADMITTED**.

## A9 — at least one pair of tiers is redundant, and the report must name it

`L0` (fragmentation), `L1` (scale), and `L2` (predictability) are three different measurements, but on a small
calibration set they can still agree everywhere. Predicted: **at least one pair has the same YES/NO profile on all
nine scenes.**

If confirmed, the finding is: *admission on `(a)(b)(c)` is necessary but not sufficient — a tier whose verdict is a
function of another admitted tier adds a column and no information, and must be either dropped or given a
separating calibration scene before it enters a matrix.* This is reported as a finding, not used to refuse a tier,
because the governor's rule is about form, not about independence.

---

## Negative tests (must all fire)

| # | planted defect | required outcome |
| --- | --- | --- |
| `N1` | delete the threshold of `L1` from the lock | `L1` REFUSED, part `(c)` |
| `N2` | write `L0`'s `(a)` as "preserves the χ of the original object" | `L0` REFUSED, part `(a)` |
| `N3` | edit one threshold in the lock after hashing | all tiers REFUSED, part `(c)` — hash mismatch |
| `N4` | a tier whose quantity does not separate (null passes, no control passes) | REFUSED, part `(b)` |
| `N5` | `BLANK` scene | `L0`/`L3` return NO-VERDICT, not PASS |

`N1`–`N3` are tested by mutating an in-memory copy of the lock, never the lock on disk (the lock is the object under
test; editing it to test it would be the defect it exists to prevent).

## Method

`src/route/structure_tiers.py`, `numpy` only, all seeds declared. Verdicts are built from flags — no hand-written
closing sentence. Output `runs/MATRIX/structure_tiers_results.txt`.

**Order of operations, auditable by file mtime**: spec → this registration → `threshold_lock.json` → its `.sha256`
→ the script → the run. The lock must be older than the results file; the script asserts it.
