# RQ-05 — pre-registration: the interaction-level census (refinement iii)

**Written before the instrument is run.** Round 57. Governing text:
`docs/decisions/g6_dc2_ruling_v1.md` §7 condition (iii) — *"`n_free,2D` as an interval, never a point —
`RQ-05`"*, moving *"`n_free,2D`, hence `f_intra`"*.

**Product**: `runs/R1B/r1b1_p4_census_results.txt` (emitted by `src/r1_dense/r1b1_p4_census.py`, never
transcribed). **Inputs**: `runs/R1B/r1b1_p2_eos_scan_results.txt` P2-5 (the census column);
`runs/R1B/r1b1_p4_response_results.txt` P4-2 (the partition); `runs/R1B/r1b1_p4_tau_results.txt` §3
(`k_Fℓ`, `q_TF`, `r_s`); `conv.beta_eq`, `conv.kF_2`; `docs/specs/R1_B1_Microscopic_Matter_Model_v1.0.md`
§4.2 (the census rows); `docs/R1B1.md` §3.1 (free / bound / trapped / other / reacting).

## 1 The three questions this round must keep apart

1. **What is the census a census of?** `P2-5` prints `n_free,2D` against `n_Q,2D` and a ratio
   `n_free/n_Q`; the ruling's §2 table cites *"`N7-SPLIT`: 4.2–5.0% of the bookkeeping `n_Q,2D`"* as
   `DERIVED`. A ratio can be a census (a fraction of carriers that are free) or a composition ratio (a
   fraction of a charge column that is electron charge). **These are different objects and the round
   must say which one is printed.**
2. **Do bound or trapped states exist at the interaction level?** — a count with a criterion, per
   `R1_B1` §4.2's five rows, not a single `n_2D`.
3. **What does the answer move?** The ruling asserts `n_free,2D → f_intra`. `f_intra` as constructed in
   `P4-2` is `m_e c² / E_z,1`. **That expression contains no `n_free`.** The chain is therefore to be
   tested, not assumed: either the census moves `f_intra` by some route the formula does not show, or
   the ruling's column names the wrong target.

## 2 Definitions fixed before the numbers

- **Mean spacing** `r_s,2D = 1/√(π n)`; **Fermi wavevector** `k_F = √(4π n / g)`, `g = 2` (`conv.kF_2`,
  the registered definition — `BN-19`'s correction, not `P4-1`'s table).
- **Two mass conventions, both evaluated, neither privileged**: (a) `m_eff = E_z,1/c²` (the `P4` model's
  in-plane mass, `≈ 659 m_e`); (b) `m_e` (the frozen model's `v_F = c` dispersion). A criterion whose
  *class* answer depends on which is used is not a criterion.
- **Two `E_F` that the HYB record carries**: `mu_e = ħ c k_F = 15.705 MeV` (the EOS / β-equilibrium
  chemical potential, `conv.eos_e_2D`) and `E_F^disp = (ħ k_F)²/(2 m_eff) = 0.366 MeV` (the in-plane
  dispersion `v_F = ħk_F/m_eff` implies). **The binding criteria use `E_F^disp`**, because a bound state
  is a property of the in-plane Hamiltonian; the `mu_e` value is carried alongside so that a reader who
  quotes 15.7 MeV can see the ratio in that convention too.
- **Binding energies**: 2D hydrogenic, `E_b = 4 Ry*`, `Ry* = m e⁴/(2 ħ² ε²)`, `ε = 1` (the `RQ-03`
  declaration, to be earned in §8).
- **Band parameters of the proton array**: `a = 1/√n_p` (the `RQ-03` convention, kept for comparability),
  `t = ħ²/(2 m a²)`, `W = 4t`, `U = (5/8) e²/(ε a_B*)`.
- **Disorder**: `ℓ = k_Fℓ / k_F` with `k_Fℓ = 22.3` from `RQ-03` — quoted, not recomputed.
- **Trapping criterion (Ioffe–Regel)**: extended if `k_Fℓ ≫ 1`; the trapped fraction is `0` unless
  `k_Fℓ ≲ 1`. The 2D weak-localization channel is **not** assigned a number: its length needs a
  dephasing length, hence a temperature, which the state does not carry (`T = 0`, `P2-8`).

## 3 Predictions (falsifiable; each is checked by the instrument)

| # | prediction | bar |
|---|---|---|
| `P1` | `n_free/n_Q = X_p/Z_A` identically (so the printed ratio is the composition ratio, not a carrier fraction) | rel. dev `< 1e-12` at all five `L_z` |
| `P2` | `k_F × r_s,2D = √2` identically (the two `r_s` normalizations in the record differ by exactly `√2`) | rel. dev `< 1e-12` |
| `P3` | orbit overlap `n a_B*² ≫ 1/4`: no bound state by the Mott criterion | margin `> 20` (m_eff), `> 1e5` (m_e) |
| `P4` | `E_b/E_F^disp < 0.25`: the bound level is inside the occupied band | measured, both conventions |
| `P5` | band, not level: `W/E_b > 3`; metal, not Mott insulator: `U/W < 0.1` | both |
| `P6` | the array is half-filled: exactly one electron per proton per cell | `|ν − 1| < 1e-12` |
| `P7` | `k_Fℓ` recomputed from `RQ-03`'s own `ℓ` reproduces `22.3` | rel. dev `< 1%` |
| `P8` | `f_intra = m_e c²/E_z,1` is **exactly** `n_free`-independent | rel. change `< 1e-15` at `n_free × {0.5, 2}` |
| `P9` | `W_intra ∝ n_free` (linear) while `σ_DC` is **invariant** (because `n_imp = n_free`, so `τ ∝ 1/n_free`) | linear rel. dev `< 1e-12`; `σ_DC` rel. change `< 1e-6` |
| `P10` | no `S1`–`S15` verdict moves: no bound-state pole is added and no weight moves in the partition | all twelve verdicts identical |
| `P11` | this instrument's `τ` reproduces `RQ-03`'s `2.00e-20 s` | rel. dev `< 1%` |
| `P12` | the bound and trapped rows are `0` in all six cells (`3 L_z × 2` mass convention) — the class answer is convention-independent | exactly `0` in `6/6` |

### 3a `P9` restated before the run — the density cancels

A hand estimate on the `RQ-03` kernel (done before any computation, the round-56 lesson) shows the
prediction as first written is wrong, and the error is informative:

```
g_tr = A J2(x) / (2 pi k_F^2),   A ∝ n_imp m,   k_F^2 = 4 pi n_free/g
=>  g_tr ∝ (n_imp/n_free) m J2(x) = m J2(x)      (n_imp = n_free)     [x = q_TF/(2 k_F)]
```

`n_imp` and `k_F²` carry the **same** `n_free`, so the density cancels from the rate outright; what
remains is `m J2(x)` with `x ∝ n^(-1/2)`. `1/τ` is therefore **not** proportional to the density, and the
census cannot move `τ` by the factor it moves `n_free`. `P9` is restated as:

| # | prediction (restated) | bar |
|---|---|---|
| `P9a` | `g_tr / (m J2(x))` is independent of `n_free` (the cancellation above) | rel. dev `< 1e-12` at `n_free × {0.5, 1, 2}` |
| `P9b` | `σ_DC ∝ n_free J2(x)`, i.e. **sub-linear** in `n_free` by the `J2` shift only | `σ_DC(2n)/σ_DC(n)` reported, `1.5 < ratio < 2.0` |
| `P9c` | `τ` moves by **less than** a factor `1.3` under `n_free × 2` | `τ(2n)/τ(n) > 0.75` |

`P10` is likewise tightened to something checkable: the `P4` partition triple (`f_intra`, `Σf_1n`,
deficit) is invariant under `n_free × {0.5, 2}` to `< 1e-15`, hence no criterion keyed to the partition
can move. The reason is structural and is stated in §1 question 3: only `W_TRK ∝ n_free` carries the
density, and it multiplies all three fractions rather than entering any of them.

## 4 Decision rules fixed before the run

- If `P1` holds, the ruling's `DERIVED (N7-SPLIT: 4.2–5.0%)` cell is a **composition ratio** and must be
  re-read as `X_p/Z_A`; the `P2-5` verdict *"the split is realized, not assumed"* is **not** supported by
  the number it prints. The `P2` product is **not edited** (`s9.1`); an erratum is appended and the
  citation consequence is registered.
- If `P3`–`P6` hold, the census's bound and trapped rows are `0` **with a criterion and a margin**, and
  `n_free,2D`'s "interval" is degenerate over the declared convention envelope — a point with four
  margins, not a point by assumption. The document must say so in those words; a degenerate interval
  presented as a wide one would be the failure mode this round is meant to avoid.
- If `P8` holds, refinement (iii) **cannot** move `f_intra`, and the ruling's column is corrected:
  (iii) moves the absolute spectral weight `W_intra` (and nothing in the partition). The correction is
  recorded as an erratum; the mark is not re-opened.
- Any prediction that fails is reported un-re-barred, with the measured value and the reason.
