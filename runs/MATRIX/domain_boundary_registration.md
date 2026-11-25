# Pre-registration — applicability-domain boundaries for `Q0` (T1) and `Q2` (T2)

**Written before `src/route/domain_boundary.py` existed.** No threshold in
`runs/MATRIX/threshold_lock.json` is touched by this work; the lock is byte-identical before and after.
This is a *characterisation* run, not a re-declaration.

Date: 2026-11-22
Governor ruling executed here: **T1/T2 → registered as applicability-domain boundaries**
("may not be used as evidence" prohibition + known boundary intervals, **no new lock**).

---

## 0. What is being measured, and what is not

T1 and T2 were findings, not defects to repair. The ruling declines to repair them: the definitions stay as
locked, and instead the *domain in which their output may be cited as evidence* is narrowed and written down.
That requires one thing this project did not have: **where the boundary actually is**, measured rather than
guessed. `T1` was demonstrated at a single point (`DITHER`, `σ_u/Δu = 0.119`) and `T2` at a single point
(`DITHER`, `Q2 = −0.153`). One point does not make an interval.

Both quantities are recomputed **verbatim from the executor's own functions**, extracted from
`src/route/structure_tiers.py` by AST and digest-recorded, so the measured bodies cannot drift from the ones
that produced the admitted verdicts. Constants (`GRID`, `BINS`, `CTX`, null ensemble, seed base) are read
from the lock, not re-typed.

## 1. Families

**Family A — near-constant + dither** (`T1`). `u = 0.5` everywhere except a random fraction `m` of cells,
set to `0.5 ± A/2`. Sweep `m` at fixed `A = 0.3`; separately sweep `A` at fixed `m = 0.05`.

**Family B — the same family, read by `Q2`** (`T2`), plus an **alphabet probe**: the same continuous fields
quantised to `B = 16` and `B = 64` levels, each renormalised against its own null at that alphabet.
`B = 16` numbers are **diagnostic only** — `BINS = 64` is locked, and no `B = 16` value may be cited as a
tier verdict.

## 2. Predictions (fixed now; failures to be reported as failures)

| # | Prediction | Rationale |
| --- | --- | --- |
| P1 | `\|Q0(A=0.6) − Q0(A=0.005)\| < 0.02` at `m = 0.05` | `P0` is normalised by `Δu`, and `P0 ∝ A` for a dither family. If so, **no amplitude precondition can ever detect T1** — this is the sharp form of the finding |
| P2 | `P0/A` constant to within 2% across the amplitude sweep | the mechanism behind P1, stated directly |
| P3 | `Q0 ≥ 0.5` for every `m ≤ 0.20` | the false-pass region is wide, not a single bad point |
| P4 | `Q0(m = 1.0) < 0.5` | full-strength dither is no longer "near-constant"; if this fails, `Q0` is inadmissible at **every** `m`, which is a stronger result than the one I expect |
| P5 | rebuilding `DITHER` verbatim (seeds 1236/1237, 5% of cells, `±0.3`) reproduces `Q0 = 0.775` and `σ_u/Δu = 0.119` to `1e-3` | **harness validation, not a prediction about a new draw** — amended pre-run. My first form said "`σ_u/Δu` at `m = 0.05, A = 0.3` equals 0.119", which confuses *same formula* with *same random draw*; a fresh draw gives `≈ 0.109` and would have failed for no informative reason. Rebuilding the exact scene tests the AST-extraction path instead, which is what P5 is for |
| P6 | `Q2(m = 0.95) < 0` | reproduces the T2 inversion |
| P7 | `Q2 ≥ 0.5` for `m ≤ 0.20` | the `Q2` boundary is a modal-mass boundary, not an alphabet artefact |
| P8 | `\|q2(B=16) − q2(B=64)\| > 0.05` on the same `NOISE` field | the 0.138 bias correction does not transfer across alphabets — T2's stated mechanism |
| P9 | the `Q0` and `Q2` crossovers differ by `> 0.1` in `m` | the two tiers have **different** domains, so a single annex entry cannot cover both |

Reported either way: crossover `m*` for each quantity (linear interpolation between the last passing and
first failing `m`), the measured `σ_u/Δu` and modal mass at each point, and the reproduced nulls
`P0(null)`, `q2(null)`.

## 3. What would falsify the annex

If `P4` fails (no crossover, `Q0 ≥ 0.5` at `m = 1`), then `Q0` has **no admissible region at all** and the
annex must say "not evidence, anywhere" rather than name an interval. If `P7` fails, `Q2`'s boundary is not
expressible in `m` and the annex must state the boundary in the alphabet instead. The annex text is written
**after** these numbers and must match them; a mismatch is a defect in the annex, not in the numbers.

## 4. Non-goals

No redefinition, no re-tolerance, no re-lock. `Q0` keeps `≥ 0.50`, `Q2` keeps `≥ 0.50`; the four tiers keep
their admitted status. What changes is only what a pass **may be used to prove**.

---

## Addendum A1 (appended after the main run, BEFORE probe 2 ran)

The main run falsified **P7** (Q2 < 0 across the *entire* sparse-excursion family, from modal mass
`0.9946` down to `0.5014`) and showed **P8** was the wrong statistic: the raw alphabet difference is
`0.0932`, but the null difference is `0.0921`, so the renormalised values agree to `0.0013` — the bias
correction **does** transfer across alphabets, which is the opposite of T2's stated mechanism.

A deterministic fact explains both: `plug_q2` builds a joint table of `CTX x CTX x BINS` cells, i.e.
`16*16*64 = 16384` cells, estimated from `127*127 = 16129` samples. **One cell per sample, before any
smoothing.** (a) So the plug-in conditional entropy is biased upward by construction, and (b) a peaky
histogram makes it worse, because the occupied contexts are few and each is estimated from fewer samples
still. The alphabet was never the culprit.

Probe 2 decides whether the Q2 prohibition is *conditional* (a modal-mass bound) or *unconditional*:
build a near-constant field whose excursion is arranged in `8x8` blocks, so the field is genuinely
predictable (knowing one cell tells you its block), and measure it.

| # | Prediction | Why |
| --- | --- | --- |
| A1-P1 | `Q2 < 0.5` for the block-structured near-constant field | if so, T2 is not about spatial geometry either; the estimator cannot see structure it should see trivially |
| A1-P2 | raw `q2 < 0.05` for that field at the locked `CTX = 16, BINS = 64` | the failure is the table size, not the field |
| A1-P3 | the **same field** at `CTX = 4, BINS = 16` (256 cells, 63 samples per cell) gives raw `q2 > 0.30` | **the causal test**: shrink the table, the structure appears. `CTX`/`BINS` are locked, so this number is diagnostic only and may not be cited as a verdict |

If A1-P3 fails, my mechanism is wrong too and the annex must say Q2's failure is unexplained rather than
attribute it to undersampling.
