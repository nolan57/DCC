# Tier redefinition executed — `(a)(b)(c)` admission, 4 of 4 admitted, 3 predictions failed

**Date**: 2026-11-22
**Authority**: governor's instruction, verbatim — *"Redefine the four tiers as intrinsic-structure criteria that do not refer to the original object; each tier must provide all three of: (a)
a formal definition referring only to the scenario itself; (b) a quantity taking values between 'unstructured' and 'structured'; (c) a threshold declared before the run and hash-locked. If any of the three is missing, the tier
may not enter the matrix."*
**Spec**: `docs/specs/intrinsic_structure_tiers_v1.md` (**hash-locked, not edited after the run** — see §5)
**Pre-registration**: `runs/MATRIX/tier_redefinition_registration.md` (`A1`–`A9`, `N1`–`N5`)
**Lock**: `runs/MATRIX/threshold_lock.json` + `.sha256`, written 59 s before the run
**Product**: `src/route/structure_tiers.py` → `runs/MATRIX/structure_tiers_results.txt`

---

## 1. Verdict

**All four tiers are ADMITTED.** Each has `(a)` `(b)` `(c)` independently verified, each check is machine-produced,
and each check was shown to fire on a planted defect before being trusted.

| tier | quantity | (a) intrinsic | (b) separating | (c) locked | verdict |
| --- | --- | --- | --- | --- | --- |
| `L0` | fragmentation removed, `Q0` | OK | OK — null fails, 6/6 controls pass | OK `≥ 0.50` | **ADMITTED** |
| `L1` | characteristic scale, `Q1 = ξ/h` | OK | OK — null fails, 5/6 pass | OK `≥ 4.0` | **ADMITTED** |
| `L2` | predictability, `Q2` | OK | OK — null fails, 4/6 pass | OK `≥ 0.50` | **ADMITTED** |
| `L3` | legible levels, `Q3` | OK | OK — null fails, 4/6 pass | OK `≥ 2.0` | **ADMITTED** |

Gate health, none of which is a formality:

- **Hash lock verified** (lock and spec both), and the lock's mtime is older than the run by 59 s — the declaration
  is provably prior to the evaluation.
- **`N1`–`N5` all fired**: deleted threshold → REFUSED on `(c)`; definition citing "the original 3D object" →
  REFUSED on `(a)`; threshold set below the null → `(b)` fails; `BLANK` → NO-VERDICT.
- **0 of 6 tier pairs identical** on the 9-scene profile. The four columns are not restatements of each other.

*(Note on tier names: `Q1`, `Q2`, `Q3` collide with a pre-existing owner — see `T3` and registry `S9`. The names in
this document are the names **inside the lock**, which cannot be changed without voiding it.)*

---

## 2. What the quantities actually measured

| scene | `Q0` | `ξ/h` | `Q2` | `C_ξ` | `Q3` (instrumented) | `Q3` (reflection) |
| --- | --- | --- | --- | --- | --- | --- |
| `NOISE` | −0.0075 | 0.63 | 0.0016 | — | n/v | n/v |
| `NOISE-S` | −0.0023 | 0.64 | 0.0006 | — | n/v | n/v |
| `BLUR` | 0.9939 | 10.04 | **0.4736** | 0.0161 | **1.385** | 0.000 |
| `DITHER` | **0.7752** | 0.63 | **−0.1529** | — | n/v | n/v |
| `RAMP` | 0.9989 | 38.63 | 0.6674 | 0.2916 | 4.915 | 0.000 |
| `STEP` | 0.9989 | 40.46 | 1.0000 | 0.5497 | 5.806 | 0.000 |
| `GRATING` | 0.9952 | 9.37 | 0.9399 | 0.4624 | 5.562 | 0.000 |
| `TILED` | 0.9989 | 27.55 | 0.9417 | 0.7867 | 6.316 | 0.000 |
| `BLANK` | 1.0000 → **n/v** | 0.00 | n/v | — | n/v | n/v |

The null ensemble gives `P0(𝒩) = 5.6399e-2` and `q₂(𝒩) = 0.1382`. **That second number is the whole reason `Q2`
carries a renormalisation**: plug-in conditional entropy reports `0.138` of "predictability" on pure i.i.d. noise.
Without the correction, `L2` would have been measuring its own estimator.

Two thresholds sit uncomfortably close to a datum and must be left there:
`BLUR` lands at `Q2 = 0.4736` against a locked `0.50`, and at `Q3 = 1.385` against a locked `2.0`. Both are declared
FAIL. **I did not move either threshold.** Moving `0.50 → 0.47` would flip a verdict after seeing it, which is the
single thing the lock exists to prevent; it is recorded here as the demonstration, not as a defect.

---

## 3. Three predictions failed. They are results, not noise.

### `A3` failed on both legs — `DITHER` should have failed `L0` and passed `L2`. It did the opposite.

| leg | predicted | measured | what it means |
| --- | --- | --- | --- |
| `L0` | FAIL | **PASS, `Q0 = 0.7752`** | see `T1` |
| `L2` | PASS | **FAIL, `Q2 = −0.1529`** | see `T2` |

### `A9` failed — I predicted at least one redundant pair. There were none.

| pair | profiles |
| --- | --- |
| `L0` vs `L1` | differ on `DITHER` (`L0` pass, `L1` fail) |
| `L1` vs `L2` | differ on `BLUR` (`L1` pass, `L2` fail) |
| `L2` vs `L3` | differ on `BLUR` (`L2` fail, `L3` fail) and `DITHER` (fail vs no-verdict) |

**This is a better outcome than I predicted and I am not going to claim credit for it**: the calibration set was
designed to separate the tiers, so a 0/6 result confirms the design rather than revealing a hidden property. The
honest statement is: *on these nine scenes, the three structural quantities are independent; on a wider scene family
they may not be.*

---

## 4. Findings

### `T1` — `Q0`'s normalisation by `Δu` rewards a field that is almost constant

`Q0` measures total persistence **divided by the scene's own dynamic range**. For `DITHER` (95% of cells at one
level, 5% flipped by ±3 bins) every component's lifetime spans the whole of that tiny range, so `P0 ≈ O(1/|Λ|)` and
`Q0 = 0.775` — the tier calls it *organized*. `BLANK` is the same failure at the limit, and is caught only by the
`σ_u/Δu ≥ 0.01` precondition, which `DITHER` clears at `0.116`.

> **Correction 2026-11-22.** This paragraph originally said `DITHER` clears the precondition at `0.119`. **That
> number is not reproducible from any product** — it appears nowhere in
> `runs/MATRIX/structure_tiers_results.txt` (which never printed a contrast column), and the scene's coefficient
> recomputes deterministically to **`0.115878`** (`src/route/domain_boundary.py` §[2], where the verbatim `DITHER`
> is rebuilt and returns `Q0 = 0.775194`, matching the admitted value). The verdict is unaffected: `11.6×` the
> precondition rather than `11.9×`, still a clear pass. Recorded as the fourth instance of a stated number that no
> product supports, after `9e20`/`9e14`, the `√2` span bound, and the `3.79e11` bits charged to `L1`. See
> `docs/decisions/t1_t2_t4_s9_execution_v1.md` §6.

So `L0`'s `(b)` holds by the letter of the rule while part of its discrimination is an artefact of a small
denominator. Two candidate repairs, neither applied (see §5): normalise by `σ_u` instead of `Δu`, or raise the
precondition on relative contrast. **Whichever is chosen moves `DITHER`'s `L0` verdict, so it cannot be adopted
without a new lock.**

### `T2` — `Q2`'s bias correction is calibrated at one alphabet and does not transfer

`Q2 = (q₂ − q₂(𝒩))/(1 − q₂(𝒩))` removes the finite-sample bias **measured on 64-bin uniform data**. On a
near-binary field the marginal entropy is small and the ratio `H(u|c)/H(u)` behaves differently, so `Q2(DITHER) =
−0.1529` — the tier reports a field that is 95% constant as **less predictable than noise**. That is not a
threshold problem; a threshold cannot repair a quantity that goes the wrong way for a whole scene class.

This is the second time in this project that a bias correction worked exactly where it was calibrated and failed one
step outside. It is recorded so the next one is calibrated twice.

### `T3` — symbol collision inside the lock

`Q1`, `Q2`, `Q3` are already owned by the six checks of `meff_boundary_probe` (registry §2, "audit only"). The tier
quantities took the same names. `Q0` is free; the other three are not, so three of four collide.

**The lock is why this is a finding rather than an edit.** Renaming the quantities means editing
`threshold_lock.json`, which voids `5f324e15…` and refuses every tier on `(c)` by construction — which is the
mechanism doing its job. Until a v2 lock exists, the tiers' quantities must be written `Q0`,`Q1`,`Q2`,`Q3` **with
their scope stated**, and the registry now records both owners (`S9`).

### `T4` — the tiers respond to arrangement, but do not certify readability

Post-admission probe (exploratory, licensed nothing):

| arrangement | `Q0` | `ξ/h` | `Q2` |
| --- | --- | --- | --- |
| `TILED` canonical | 0.9989 | 27.55 | 0.9417 |
| `TILED` shuffled | 0.9600 | **4.53** | 0.7805 |

The order matters — `ξ` drops sixfold under shuffling — so the tiers do measure the arrangement, and audit §6 item 5
(the layout convention must be a declared `DC` item) is confirmed as necessary.

But **the shuffled scene still passes `L1` (`4.53 ≥ 4.0`) and `L2` (`0.78 ≥ 0.50`)**. So the admitted tiers certify
*"has structure at a scale"*, not *"the structure is readable"*. Anyone reading a matrix cell as the latter would be
over-reading it. State this on every cell.

### `T5` — `L3` is still empty under `C1` in reflection, and now we know why

**0 of 9 scenes** reach `L3` with the reflection channel, and the reason is `q = 0` exactly, not `C_ξ` and not `ξ`.
The exposure budget is zero (`2L/c` exceeds `t_rip` by `√2`), so the channel factor kills `Q3` before contrast is
consulted.

This reproduces the matrix audit's `M5` **from the intrinsic side**. That was the point of the exercise: `M5` was
never a complaint that the metric referred to the original object, it was photon physics. A correctly written
intrinsic tier does not rescue `L3`; it explains the emptiness.

---

## 5. What I did not do, and why

**I did not write a v2 spec with `T1` and `T2` repaired.** I have now seen the numbers. A `Q0` normalised by `σ_u`
chosen today would be chosen because I know it moves `DITHER` from 0.775 to something below 0.5, and a `Q2`
calibrated per alphabet would be calibrated on the very scene that exposed it. That is fitting, not declaring — the
defect the governor's `(c)` requirement exists to make impossible.

A v2 needs: the governor's instruction, a **new** lock with a **different** digest, and a pre-registration written
before any data are shown. I will draft it on instruction.

**I did not edit the spec.** Its digest is inside the lock; editing it would refuse all four tiers. The findings live
here instead, which is the correct direction — findings point at a locked document, they do not enter it.

---

## 6. What this changes for the matrix

1. **Four columns exist**, all admitted, all hash-locked, none redundant on the calibration family.
2. **A cell is a profile, not a maximum.** `L0`–`L3` measure organization, scale, predictability and legibility —
   three independent things plus one that is empty under `C1` in reflection. There is no total order, so "Max
   Distinguishability" is still not computable, exactly as the audit's `M6` said. The matrix must report the
   4-tuple.
3. **The row set is unchanged**: 2 of 8 combinations are realizable (`M-ROW`). So the matrix is now **2 rows × 4
   admitted columns**, and one of its eight cells (`L3` in reflection) is known to be empty before anything runs.
4. **`L3` needs a channel label on every cell.** With `q = 0` it is empty in reflection and non-empty in an
   instrumented channel. A cell that does not name its channel is not a result.

---

## 7. Registration

| item | where |
| --- | --- |
| definitions, `(a)(b)(c)` per tier, hash-locked | `docs/specs/intrinsic_structure_tiers_v1.md` |
| thresholds + digest | `runs/MATRIX/threshold_lock.json`, `.sha256` |
| predictions `A1`–`A9`, negative tests `N1`–`N5` | `runs/MATRIX/tier_redefinition_registration.md` |
| executable gate | `src/route/structure_tiers.py` |
| results, 4/4 admitted, 6/9 predictions, 6/6 defects caught | `runs/MATRIX/structure_tiers_results.txt` |
| this record | `docs/decisions/tier_admission_v1.md` |

**PROVENANCE: NEITHER** (tier evaluation against a declared null; establishes no physics).
