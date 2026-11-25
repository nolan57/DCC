# R1B1-P4/P5 — refinement (iv): the `L_z`-resolved family surface

**Round 60** — `RQ-06`, product of `src/r1_dense/r1b1_p4_family_surface.py` (`--write`). Pre-registration: `runs/R1B/r1b1_p4_family_surface_registration.md`.

`PROVENANCE: NEITHER` — a compilation/arithmetic receipt over state inputs. It establishes no chain evidence, re-grades no criterion and writes no gate mark.

---

## 1 The surface R1-B4/R3 receive

Five cells, fixed baryon column `N_B = 0.042155 fm⁻²`, HYB convention, `g = 2` (spin, single occupied subband). Every number is state-derived at its own `L_z`; none is transcribed from P4-1.

| `L_z` [fm] | `n_free,2D` [fm⁻²] | `g` | `v_F/c` | `ω_end` [rad/s] | `ω_end(S14)` [MeV] |
|---|---|---|---|---|---|
| 1.68 | 1.11061e-03 | 2 | 0.04467 | 5.6061e+23 | 370.4713 |
| 1.76 | 1.05704e-03 | 2 | 0.04566 | 5.3513e+23 | 353.6941 |
| 1.84 | 1.00810e-03 | 2 | 0.04661 | 5.1186e+23 | 338.3755 |
| 1.92 | 9.63244e-04 | 2 | 0.04755 | 4.9053e+23 | 324.3330 |
| 1.99 | 9.26959e-04 | 2 | 0.04834 | 4.7328e+23 | 312.9717 |

`ω_end` in the fifth column is the **band edge** `πc/L_z`, carried forward from the P4-1 table because that is what the archive hands off. The sixth column is the form `S14` actually requires (§4). Both are state-derived; they differ by `0.40–0.47%` because `f_inter W_total/A ≈ 1.46 MeV` is small against `E_z,1 ≈ 311–369 MeV`.

## 2 Per-cell provenance

Each cell states which product derived each input, and which erratum qualifies it. `EXEMPT-LEGACY` means the archived P4-1 file is cited only as evidence of a defect, never as the authority for a corrected number (BN-04/P9 digest).

| `L_z` | input | value | source and qualification |
|---|---|---|---|
| 1.68 | `n_free,2D` | 1.11061e-03 | `r1b1_p2_eos_scan_results.txt` P2-5; `beta_eq` at fixed `N_B`, HYB; `n_e = X_p·N_B`. E4: **not** 4.2–5.0% of `n_Q` (that is `X_p/Z_A`). |
| 1.68 | `g` | 2 | P4-1 declaration: spin, one occupied subband. BN-35/E7: the same-sign MIT bag admits a `k=0` mode; `g = 2` holds only if it is unoccupied. |
| 1.68 | `v_F` | 0.04467 c | corrected: `ħ k_F/m_eff`, `k_F = conv.kF_2(n)`, `m_eff = E_z,1/c²`. E2: P4-1 printed 0.0316 c (low by `√2`). |
| 1.68 | `ω_end` | 5.6061e+23 rad/s | band edge `πc/L_z` = `E_z,1/ħ`, state-derived. P4-1 prose `3.1–3.7e23` belongs to `L_z = 2.55–3.04 fm` (outside K1). |
| 1.76 | `n_free,2D` | 1.05704e-03 | `r1b1_p2_eos_scan_results.txt` P2-5; `beta_eq` at fixed `N_B`, HYB; `n_e = X_p·N_B`. E4: **not** 4.2–5.0% of `n_Q` (that is `X_p/Z_A`). |
| 1.76 | `g` | 2 | P4-1 declaration: spin, one occupied subband. BN-35/E7: the same-sign MIT bag admits a `k=0` mode; `g = 2` holds only if it is unoccupied. |
| 1.76 | `v_F` | 0.04566 c | corrected: `ħ k_F/m_eff`, `k_F = conv.kF_2(n)`, `m_eff = E_z,1/c²`. P4-1 printed no row at this `L_z` (three-row table). |
| 1.76 | `ω_end` | 5.3513e+23 rad/s | band edge `πc/L_z` = `E_z,1/ħ`, state-derived. P4-1 prose `3.1–3.7e23` belongs to `L_z = 2.55–3.04 fm` (outside K1). |
| 1.84 | `n_free,2D` | 1.00810e-03 | `r1b1_p2_eos_scan_results.txt` P2-5; `beta_eq` at fixed `N_B`, HYB; `n_e = X_p·N_B`. E4: **not** 4.2–5.0% of `n_Q` (that is `X_p/Z_A`). |
| 1.84 | `g` | 2 | P4-1 declaration: spin, one occupied subband. BN-35/E7: the same-sign MIT bag admits a `k=0` mode; `g = 2` holds only if it is unoccupied. |
| 1.84 | `v_F` | 0.04661 c | corrected: `ħ k_F/m_eff`, `k_F = conv.kF_2(n)`, `m_eff = E_z,1/c²`. E2: P4-1 printed 0.0330 c (low by `√2`). |
| 1.84 | `ω_end` | 5.1186e+23 rad/s | band edge `πc/L_z` = `E_z,1/ħ`, state-derived. P4-1 prose `3.1–3.7e23` belongs to `L_z = 2.55–3.04 fm` (outside K1). |
| 1.92 | `n_free,2D` | 9.63244e-04 | `r1b1_p2_eos_scan_results.txt` P2-5; `beta_eq` at fixed `N_B`, HYB; `n_e = X_p·N_B`. E4: **not** 4.2–5.0% of `n_Q` (that is `X_p/Z_A`). |
| 1.92 | `g` | 2 | P4-1 declaration: spin, one occupied subband. BN-35/E7: the same-sign MIT bag admits a `k=0` mode; `g = 2` holds only if it is unoccupied. |
| 1.92 | `v_F` | 0.04755 c | corrected: `ħ k_F/m_eff`, `k_F = conv.kF_2(n)`, `m_eff = E_z,1/c²`. P4-1 printed no row at this `L_z` (three-row table). |
| 1.92 | `ω_end` | 4.9053e+23 rad/s | band edge `πc/L_z` = `E_z,1/ħ`, state-derived. P4-1 prose `3.1–3.7e23` belongs to `L_z = 2.55–3.04 fm` (outside K1). |
| 1.99 | `n_free,2D` | 9.26959e-04 | `r1b1_p2_eos_scan_results.txt` P2-5; `beta_eq` at fixed `N_B`, HYB; `n_e = X_p·N_B`. E4: **not** 4.2–5.0% of `n_Q` (that is `X_p/Z_A`). |
| 1.99 | `g` | 2 | P4-1 declaration: spin, one occupied subband. BN-35/E7: the same-sign MIT bag admits a `k=0` mode; `g = 2` holds only if it is unoccupied. |
| 1.99 | `v_F` | 0.04834 c | corrected: `ħ k_F/m_eff`, `k_F = conv.kF_2(n)`, `m_eff = E_z,1/c²`. E2: P4-1 printed 0.0342 c (low by `√2`). |
| 1.99 | `ω_end` | 4.7328e+23 rad/s | band edge `πc/L_z` = `E_z,1/ħ`, state-derived. P4-1 prose `3.1–3.7e23` belongs to `L_z = 2.55–3.04 fm` (outside K1). |

## 3 Admissible range

**Declared admissible: the five solved cells at `L_z ∈ {1.68, 1.76, 1.84, 1.92, 1.99} fm`, inside the registered K1 window `[1.68, 1.99] fm`.**

That interval is the *frozen-density* K1 window: at `n_e = 0.022 fm⁻²`, `E_sub/E_F ≥ 3` gives `L_z ≤ 1.995 fm` and the nucleon-fit bound `2r_p = 1.68 fm` gives the lower edge — width `1.19×`, with the lower edge a physical judgment, not a theorem. At the solved density (`n_free ≈ 1e−3 fm⁻²`, `22×` lower) the same two-sided test gives an upper edge `L_z ≈ 80.30 fm`, a factor of `≈ 40` wider. The receipt therefore makes three distinctions a downstream citation must keep:

1. `[1.68, 1.99] fm` is the **registered** K1 window, not the solved state's 2D ceiling;
2. only the five solved `L_z` are **certified cells** — interpolating the tuple to an unsolved thickness is a new state solve, not a table lookup;
3. outside K1 the archive has no state, so neither the tuple nor the response may be cited.

## 4 The S14 form that P4 did not compute

`S14` (`BUDGET-DECLARED`) forbids a bare `ω_end` and requires `ω_end = ω_g + f_inter·W_total/A` with one declared `ω` convention. P4-1 recorded `S14 PASS` with the bare band edge — the exact form the clause fails. This product does not re-open that mark (`s9.1`: a ratification is not a correction); it supplies the form.

Convention: `g = 2` consistently in `A_inter = (g/4)σ_min = e²/(8ħ)` and `W_total = πe²n_free/(2m_eff)` with `m_eff = E_z,1/c²`; therefore `W_total/A = 2ħk_F v_F = 4πħ²n_free/m_eff` and `f_intra + f_inter = 1`. `ω_g = E_z,1/ħ` is the first inter-subband line — the state-derived gap, not the frozen `2E_F` identity that yields `440.18 MeV`. Unit convention: MeV (energy, ħω), rad/s shown alongside.

| `L_z` | `W_total/A` [MeV] | `f_intra` | `f_inter` | `ω_g` [MeV] | `ω_end(S14)` [MeV] | rel. to bare |
|---|---|---|---|---|---|---|
| 1.68 | 1.47270 | 0.0013848 | 0.9986152 | 369.0006 | 370.4713 | +0.0040 |
| 1.76 | 1.46842 | 0.0014508 | 0.9985492 | 352.2278 | 353.6941 | +0.0042 |
| 1.84 | 1.46410 | 0.0015167 | 0.9984833 | 336.9136 | 338.3755 | +0.0043 |
| 1.92 | 1.45977 | 0.0015827 | 0.9984173 | 322.8755 | 324.3330 | +0.0045 |
| 1.99 | 1.45599 | 0.0016404 | 0.9983596 | 311.5181 | 312.9717 | +0.0047 |

## 5 What the handoff does and does not move

With `(i)` (`τ`), `(ii)` (Dirac ladder) and `(iii)` (census) discharged in rounds 56–58, this closes `(iv)`: **all four conditions of `PG-01` are now discharged**. No `S1`–`S15` verdict, `τ`, `σ_DC`, `G6`/`DC2` mark or `G5′` status moves. The `k = 0` subband question (BN-35), the `Q-1`/`Q-2` disorder premise (BN-22) and the `S15` dispersion convention (BN-27) remain open questions about the state.

## 6 Predictions

| # | verdict | type |
|---|---|---|
| `P1` | CONFIRMED | CHECK |
| `P2` | CONFIRMED | CHECK |
| `P3` | CONFIRMED | CHECK |
| `P4` | CONFIRMED | CHECK |
| `P5` | CONFIRMED | CHECK |
| `P6` | CONFIRMED | CHECK |
| `P7` | CONFIRMED | CHECK |
| `P8` | CONFIRMED | CHECK |
| `P9` | CONFIRMED | CHECK |
| `P10` | CONFIRMED | CHECK |
| `P11` | CONFIRMED | CHECK |
| `P12` | CONFIRMED | CHECK |
| `P13` | CONFIRMED | STRUCTURAL |
| `P14` | CONFIRMED | STRUCTURAL |

**14/14 predictions confirmed.** 

## 7 Structural notes (measured, not applied)

**Pre-emission predicate corrections** (registration amended before `--write`, all disclosed): P2 bar `1e−5 → 1e−4` (P2-5 prints five digits; rounding floor `5e−5`); P4 second clause `1e−4 → 3e−3` (archived `0.0330 c` has three digits); P5 uses the full-precision hand estimates instead of four-digit roundings; P7's inverted inequality corrected. No measured number and no full-precision comparison bar changed.

- `k_F × mean spacing = √2` exactly, so E2's `√2` and the two `r_s` normalizations (0.1566 vs 0.2214) are the same factor seen twice (BN-26, BN-27).
- `S15`'s identity `E_F = ħk_F v_F` is a **linear-dispersion** identity. With the parabolic subband `m_eff = E_z,1/c²`, `E_F^disp = ħ²k²/(2m_eff) = 0.366 MeV` and `v_F = ħk/m_eff`: the identity gives `2 E_F^disp = 0.732 MeV`, off by `2×`. With `μ_e = ħck_F = 15.705 MeV` it is off by `21.45×`. P4 recorded `S15 PASS`; this receipt names the convention defect but moves no verdict.
- State-derived 2D crossover `L_z = 80.2974 fm` versus frozen `1.995 fm` — the K1 window is a property of the state used to derive it, not a universal thickness bound.

*Content generated by AI*
