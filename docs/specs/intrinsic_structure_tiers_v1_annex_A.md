# Annex A to `intrinsic_structure_tiers_v1` — applicability domains of `Q0` and `Q2`

**Status**: in force as part of `intrinsic_structure_tiers_v1` **by reference**, added 2026-11-22 on governor
ruling T1/T2 (*registered as applicability-domain boundaries; prohibition on use as evidence plus a known
boundary interval; no new lock*).

**Why this is an annex and not an edit.** `intrinsic_structure_tiers_v1.md` is covered by `spec_sha256` inside
`runs/MATRIX/threshold_lock.json`, and `src/route/structure_tiers.py` refuses every tier on `(c)` when that
digest does not match. Editing the spec would therefore not narrow the tiers — it would **delete** them. The
digest exists to prove one thing: *the definitions and thresholds did not move after the data were seen*. This
annex does not move them. It restricts what a pass or a fail **may be used to prove**, which is a different
object, and it is deliberately placed outside the digest's protection so that the protection keeps its meaning.
The lock file is byte-identical before and after (verified: `5f324e15…bcc`).

**The annex may not contain a tier threshold.** If a number that decides `PASS`/`FAIL` appears here, this annex
has become a second, unprotected lock and is void. Domain boundaries are the entire point of the annex and are
permitted and required; **verdict thresholds are not, and are referred to by name only.**

---

## A.1 — `Q0` (tier `L0`, topological organization)

> **Prohibition.** A `Q0` **pass** may not be cited as evidence of topological organization when the scene's
> histogram **modal mass exceeds `0.87`**. Below that line a pass is admissible; a fail is admissible everywhere.

**The measured boundary.** Sweeping a near-constant-plus-dither family at fixed amplitude, `Q0` crosses its
locked threshold (`L0.threshold_c`) at modal mass **`0.8720`** (interpolated between modal `0.8987` →
`Q0 = 0.5856` and modal `0.8007` → `Q0 = 0.2712`). Above the crossover, `Q0` **rises as the field becomes more
constant**: modal `0.9946` → `Q0 = 0.9764`. That is the defect stated as a domain: the estimator pays for
emptiness.

**Why no existing precondition can substitute.** `Q0` is **invariant to amplitude**. Over a `120×` range of
dither amplitude (`0.005` to `0.60`) the total persistence moves only `1.1191e-2` → `1.3175e-2` and `Q0` only
`0.7664` → `0.8016` (spread `0.0243`). `total_persistence` normalises through `quant()`, which maps the observed
span onto `0..1`, so the amplitude is divided out *before* the persistence is computed. The declared
precondition `σ_u/Δu ≥ 0.01` therefore cannot detect this defect at any amplitude — it is testing a quantity
the pipeline has already made scale-free. The bound has to be on **histogram concentration**, which is what
`0.87` is.

**What is *not* claimed.** The region below `0.87` is not thereby validated; it is merely not prohibited. A
`Q0` fail there (`NOISE`, `DITHER` at higher occupancy) is admissible as evidence of *no* topological
organization, and the admitted calibration set supports that side.

## A.2 — `Q2` (tier `L2`, predictability)

> **Prohibition.** A `Q2` **fail** may not be cited as evidence of absent structure. Only a **pass** is
> admissible, and a pass is biased low by at most `1.4%` (measured). In one sentence: **`Q2` may acquit, never
> convict.**

**Why this is the whole of it.** `Q2` fails exactly when the raw `q2` does not exceed `q2(null) = 0.138201`, and
in that regime the reported number is dominated by the null subtraction rather than by the scene. Measured on a
field that is `99.5%` constant — one a neighbour reproduces almost always — raw `q2 = 0.0041` and `Q2 = −0.1556`.
A negative predictability score on a nearly constant field is not a finding about the field.

**The admissible side, with its error.** On a near-constant field whose excursion is arranged in `8×8` blocks
(modal mass `0.9375`, neighbours agree in `98.62%` of pairs): raw `q2 = 0.913223`, `Q2 = 0.899307`. The
same field under a 256-cell table, where the null is `0.002495` instead of `0.138201`, gives `0.913006`. So the
pass is **correct in sign and low by `0.0137`** — an over-correction, `1.4%`. That is tolerable for a pass and
fatal for a fail, because the over-correction is a fixed `0.138`-scale subtraction while the fail-side signal is
`0.004`-scale.

## A.3 — Corrections to the T2 mechanism (three attempts, two wrong)

The defect was originally attributed to the alphabet (`T2`: "the bias correction is calibrated at 64-bin uniform
and does not transfer"). **That is wrong**, and the measurement says so: on the same `NOISE` field the raw `q2`
differs by `0.0932` between `B = 16` and `B = 64`, but the nulls differ by `0.0921`, so the renormalised values
agree to `0.0013`. The correction transfers across alphabets.

My first replacement — that `plug_q2`'s joint table (`16×16×64 = 16384` cells) exceeds the `127×127 = 16129`
samples, i.e. one parameter per sample — **is also wrong as a causal account**: shrinking the table to `256`
cells leaves the raw `q2` at `0.913223`, unchanged to six decimals. The table size moves the *null*, not the
field's measurement.

**The account the data support**: the plug-in bias is *field-dependent* (roughly, on how many table cells the
field occupies), while the renormalisation subtracts a *fixed uniform-field* bias. Where the raw signal is large
(`0.913`) the mismatch is `0.014`; where it is small (`0.004`) the same mismatch is several times the signal and
flips the sign. Both earlier accounts are recorded here rather than deleted, because a wrong mechanism that
explains the same number is how this defect survived one round already.

## A.4 — Invariants this annex does not touch

1. The four tier thresholds (`L0`–`L3`, `threshold_c`) — **unchanged and not restated here**, by the rule above.
   The lock remains their only home.
2. All four tiers remain **ADMITTED** (`docs/decisions/tier_admission_v1.md`). Admission asked whether a tier
   *separates* structure from null; it did not ask whether every pass is citable, and it never claimed that.
3. `runs/MATRIX/threshold_lock.json` and its `.sha256` are unchanged. No new lock was created.
4. The two prohibitions are **one-sided** and **complementary**: `Q0`'s pass is restricted, `Q2`'s fail is
   restricted. A matrix cell built from these tiers inherits both, which is why the reading rules
   (`docs/decisions/matrix_reading_rules_v1.md`) cite this annex before allowing any cell to be read.

## A.5 — Evidence

`runs/MATRIX/domain_boundary_results.txt` (9-point modal sweep, amplitude sweep, alphabet probe, prediction
ledger 3/9), `runs/MATRIX/domain_boundary_probe2_results.txt` (block-structured field, table-size probe,
prediction ledger 1/3, plus the appended erratum), registrations in
`runs/MATRIX/domain_boundary_registration.md` (P1–P9 and addendum A1), executor `src/route/domain_boundary.py`
and `src/route/domain_boundary_probe2.py`.

*Content generated by AI*
