# RQ-06 — pre-registration: the `L_z`-resolved family surface (refinement iv)

**Written before the instrument is run.** Round 60. Governing text:
`docs/decisions/g6_dc2_ruling_v1.md` §7 condition `(iv)` — *"`L_z`-resolved family surface; five
`L_z` values with per-cell provenance — `RQ-06`; what it may move: the input range handed to
`R1B4`/`R3`"*; queue `RQ-06` asks *"What is the input surface R1-B4/R3 receive, and what is its
admissible range?"*

**Product**: `runs/R1B/r1b1_p4_family_surface.md`, emitted by
`src/r1_dense/r1b1_p4_family_surface.py` (`--write`), never transcribed. **Inputs**:
`runs/R1B/r1b1_p4_response_results.txt` P4-1/P4-5 (the archived four-input tuple, tagged
`EXEMPT-LEGACY` under P9/BN-04); `runs/R1B/r1b1_p2_eos_scan_results.txt` P2-5 (the five states);
`src/common/conv.py` (`HBARC`, `M_E`, `beta_eq`, `kF_2`, `LZ_FM`); the closure document's errata
E2 (`k_F` low by `√2`), E4 (`4.2–5.0%` is `X_p/Z_A`), E7 (the `k = 0` bag mode).

## 1 What this product is, and what it is not

It is a **handoff receipt**: one row per scanned `L_z`, carrying the four inputs the ruling names
(`n_free,2D`, `g`, `v_F`, `ω_end`) plus a per-cell provenance field, and one explicit admissibility
statement. It does **not** re-solve a state, re-grade `S1`–`S15`, or write a gate mark. The
`G6`/`DC2` flip is untouched; with `(i)`–`(iii)` now discharged, closing `(iv)` removes the last
condition named in `PG-01`.

Three archive defects have to be carried into the receipt rather than silently inherited:

1. **E2**: P4-1's `k_F` is low by `√2` (`sqrt(πn)` instead of `conv.kF_2`'s `sqrt(2πn)`), so its
   `v_F` column is low by `√2`. The receipt prints the corrected `v_F` and the archived value beside
   it. P4's own prose (`v_F ~ 0.049 c`) is closer to the corrected number than its table is.
2. **ω_end**: P4-1's *table* gives `πc/L_z` = `5.61/5.12/4.73e23 rad/s`; its *prose* gives
   `3.1–3.7e23 rad/s`, which is `πc/L_z` at `L_z = 2.55–3.04 fm` — outside K1. The receipt uses
   the table values, names the prose as a different-state number (BN-08 class), and additionally
   supplies the form `S14` requires.
3. **S14**: the criterion forbids a bare `ω_end` ("a bare `ω_end` is a fail") and requires
   `ω_end = ω_g + f_inter W_total/A` in one declared unit convention. P4 recorded `S14 PASS`
   with the bare band edge. The receipt does **not** re-open that mark (a ratification is not a
   correction, `s9.1`); it supplies the missing form so a downstream document has something
   admissible to cite.

## 2 Hand estimates fixed before the run

At the five scanned `L_z`, from `beta_eq` with `conv` patched exactly as `r1b1_p2_eos_scan.py`
does (fixed column `N_B = 0.042155 fm⁻²`, HYB):

| `L_z` | `n_free,2D` | `k_F` (correct) | `v_F/c` (correct) | `πc/L_z` [rad/s] | `ω_end(S14)` [MeV] |
|---|---|---|---|---|---|
| 1.68 | `1.1106e−3` | `0.08354` | `0.04467` | `5.606e23` | `370.4713` |
| 1.76 | `1.0570e−3` | `0.08150` | `0.04566` | `5.351e23` | `353.6941` |
| 1.84 | `1.0081e−3` | `0.07959` | `0.04661` | `5.119e23` | `338.3755` |
| 1.92 | `9.6324e−4` | `0.07780` | `0.04755` | `4.905e23` | `324.3330` |
| 1.99 | `9.2696e−4` | `0.07632` | `0.04834` | `4.733e23` | `312.9717` |

**The S14 form**, with `g = 2` consistently in `A_inter = (g/4)σ_min = e²/(8ħ)` and
`W_total = πe²n_free/(2m_eff)` (`m_eff = E_z,1/c²`), gives
`W_total/A = 4πħ²n_free/m_eff = 2ħk_Fv_F` = `1.4727 … 1.4560 MeV` across the window; with
`f_intra = m_ec²/E_z,1 = 1.38–1.64e−3` and `f_inter = 1 − f_intra`, the edge is `ω_g + f_inter
W/A` where `ω_g = E_z,1/ħ` is the first inter-subband line (the state-derived gap, not the frozen
`2E_F` identity). It sits `0.40–0.47%` above the bare `πc/L_z` — same scale, different declaration.

**Admissibility.** K1 was derived at the *frozen* density (`n_e = 0.022 fm⁻²`): `E_sub/E_F ≥ 3`
gives `L_z ≤ 1.995 fm`, and the nucleon-fit lower bound `2r_p = 1.68 fm` gives the window
`[1.68, 1.99] fm` — width `1.19×`. At the *solved* density (`n_free ≈ 1e−3 fm⁻²`, `22×` lower),
the same `E_sub/E_F ≥ 3` condition holds to `L_z ≈ 80.30 fm`. The receipt therefore declares the
five scanned cells admissible **as cells**, and the interval `[1.68,1.99] fm` admissible only as
the *scanned/frozen-registered* window — it does not claim the state's physical 2D ceiling is
`1.99 fm`, and it does not license interpolation in `L_z` to thicknesses not solved. These
estimates were computed before the instrument existed; no bar is refitted after the run.

## 3 Predictions (falsifiable)

| # | prediction | bar |
|---|---|---|
| `P1` | five `L_z` reproduce the registered scan grid `[1.68,1.76,1.84,1.92,1.99]` | exact |
| `P2` | `n_free,2D` reproduces P2-5's five values to the printed `1e−5` relative | `< 1e−5` |
| `P3` | corrected `k_F = conv.kF_2(n)`; ratio to P4-1's printed `k_F` is `√2` to `1e−3` | `< 1e−3` |
| `P4` | corrected `v_F/c = ħk_F/m_eff` at 1.84 fm = `0.04661`; archived `0.0330` | `< 1e−4` |
| `P5` | `f_intra = m_ec²/E_z,1` = `1.385/1.451/1.517/1.583/1.640 ×10⁻³` | `< 1e−5` |
| `P6` | band edge `πc/L_z` reproduces P4-1's three printed values to `1e−4` relative | `< 1e−4` |
| `P7` | P4 prose `3.1–3.7e23 rad/s` maps to `L_z = 2.545–3.038 fm`, entirely outside `[1.68,1.99]` | both bounds |
| `P8` | `W_total/A (g=2) = 2ħk_Fv_F` = `1.4727…1.4560 MeV` — half the frozen `g=1` budget identity | `< 1e−5` |
| `P9` | `ω_end(S14) = E_z,1 + f_inter W/A` = `370.4713…312.9717 MeV`; rel to bare edge `+0.40…0.47%` | `< 1e−5` |
| `P10` | `f_intra + f_inter = 1` to machine zero in all five cells | `< 1e−12` |
| `P11` | state-derived `E_sub/E_F ≥ 3` crossover at `L_z ≈ 80.30 fm`, vs frozen `1.995` — factor `≈ 40` | `< 1e−2` relative |
| `P12` | all five scanned cells satisfy `E_sub/E_F ≥ 3`; worst `20.69` at `L_z=1.99` | measured |
| `P13` | the decoded `g` column is `2` in all five cells, with the `k=0` mode (BN-35) flagged as conditional | measured |
| `P14` | no `S1`–`S15` verdict, gate mark, `τ`, or `σ_DC` moves; the product writes no decision document | STRUCTURAL |

**Decision rule**: a prediction falsified after the run is reported with its measured value; no
bar is loosened post hoc. Any pre-run correction is written into this file *before* the instrument
is executed and disclosed in the product.

**Pre-emission correction (before `--write`)**: the first dry run exposed four defects in the
*predicates*, not in the physics, and all are corrected here before emission:

- `P2` — the comparison values are P2-5's **five-digit** printed densities, whose rounding floor
  is `5e−5`; the registered `1e−5` bar was unattainable (measured worst `3.66e−5` at `1.76 fm`).
  Bar corrected to `1e−4`, the precision floor of the cited value.
- `P4` — the archived `0.0330 c` is printed to three digits, giving a `√2`-ratio rounding floor
  of `~1.5e−3`; the `1e−4` bar is corrected to `3e−3` for that clause. The full-precision first
  clause (`0.04661 c`) keeps its `1e−4` bar.
- `P5` — the registered `f_intra` estimates were rounded to four digits; the hand-computed
  full-precision values (`1.384822/1.450766/1.516709/1.582653/1.640354 ×10⁻³`) replace them with
  the `1e−5` bar unchanged.
- `P7` — the predicate was written inverted (`l_lo < 1.68`); the correct test is
  `1.99 < l_lo < l_hi`, with `l_lo = 2.5455`, `l_hi = 3.0381` fm. Predicate corrected, value and
  bar unchanged.

No measured number changes and no bar is loosened against a full-precision comparison value.

## 4 Provenance of the handoff itself

`PROVENANCE: NEITHER` — a compilation/arithmetic receipt over state inputs; it establishes no new
chain evidence. Each cell carries a source string naming the product and the clause that derived
it; the archived P4-1 table is cited as `EXEMPT-LEGACY` evidence of the *defect*, never as the
authority for a corrected number.
