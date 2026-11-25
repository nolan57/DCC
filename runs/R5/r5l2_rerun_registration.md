# R5-L2 re-run registration — v3 baseline (S0 blocker clearance)

**Date**: 2026-11-22
**Authorising document**: `docs/decisions/staged_relaxation_visual_route_v1.md` §6 item 1
**Supersedes run**: `runs/R5/r5l2_sigma_s_results.txt` (executed 2026-11-21 02:10, **before** G0P-003 v3)
**New run**: `runs/R5/r5l2_sigma_s_results.txt`; superseded file archived as
`runs/R5/r5l2_sigma_s_results_v1_REVOKED_BASELINE.txt` (§9.1: superseded runs are archived, never deleted)

---

## 1. Why

The 2026-11-21 run hard-codes the **pre-G0P-003-v3** baseline:

| Constant | Old (revoked) | New (v3, §3.4) | Factor |
|---|---|---|---|
| `N_2D` | `2.20e27 m^-2` | `2.20e28 m^-2` | ×10 |
| `E_F_REF_MEV` | `23.20` | `73.37` | ×3.162 |
| `MSTAR_FACTOR` | `45.4` | `143.6` (derived) | ×3.162 |

The stamped `C0 G0 consistency 5.533e-07 PASS` therefore validated the revoked chain. It is self-consistent
with the pre-v3 numbers, not with §3.4. Found 2026-11-22 during a goal-level audit.

## 2. What changes, and what does not

**Changes (all forced by the baseline correction; none is a model change):**

1. `N_2D`, `E_F_REF_MEV` → v3 values.
2. `MSTAR_FACTOR` is now **derived** (`E_F_REF_MEV / 0.51099895`) instead of a literal. The module header
   already declared `m*/m_e = E_F/(m_e c^2)`; the literal had silently stayed at the pre-v3 value. This is a
   §9 "single point of definition" fix, not new physics. If the literal were merely rescaled instead, a future
   baseline edit could desynchronise it again.
3. `C0` reference print `k_F = ... (logged 1.176e14)` → `3.718e14`.
4. `HBARW_ROWS_EV` last row `5.0e7` (50 MeV) → `2.0e8` (200 MeV). **Forced**: that row exists solely to
   demonstrate the interband switch, whose condition is `ħω > 2E_F`; with `2E_F` moving from 46.4 MeV to
   146.7 MeV, the old 50 MeV row would fall below threshold and the switch would no longer be demonstrated.
   The row is a switch demonstration only and is not a reachable-probe claim (unchanged note).

**Does not change (registered before the run):**

- every threshold: `TOL_T1_CONSERV = 1e-12`, `TOL_T2_ALIMIT = 1e-6`, `TOL_EF_CONSIST = 2e-3`;
- the model form `σ_s = (e² N_2D τ/m*)/(1 − iωτ)` + interband switch, the benchmark interband amplitude
  `e²/16ħ`, the τ scan `{1e-19, 1e-18, 1e-16} s` (τ remains an OPEN input);
- the prohibitions: no default `πα`, no bulk-`ω_p` extrapolation, **no visibility/mirror/transparency conclusion**;
- the grade cap: every row stays labelled "designated-background test optics".

## 3. Registered expectations and falsifiers

The decision record says this re-run makes "the visual input rest on a compliant baseline". That claim is
**falsifiable**, so the falsifier is registered here:

| # | Expectation | Falsified if |
|---|---|---|
| E1 | `C0` passes at the v3 baseline | `ef_dev ≥ 2e-3` (would mean §3.4's own chain is inconsistent) |
| E2 | `T1/T2/T3` verdicts unchanged (they are structural identities / monotonicity, baseline-independent) | any verdict flips |
| E3 | `|Z₀σ_s|` grows by ≈3.16 at fixed τ (`σ ∝ N_2D/m* ∝ E_F`) | ratio outside [2.5, 4.0] |
| E4 | In the visible rows `R → 1` more strongly than before (≥ 0.999 at τ = 1e-16) | `R < 0.999` at 2 eV, τ = 1e-16 |

E3/E4 are the ones that matter for the visual route: they are the quantitative content the S0/L1 layer would cite.

## 4. Outcome (added after the run — the expectations above were fixed first)

| # | Registered expectation | Measured | Verdict |
|---|---|---|---|
| E1 | `C0` passes at the v3 baseline | `ef_dev = 7.086e-05` (tol 2e-3) | **PASS** |
| E2 | `T1/T2/T3` unchanged | `T1` PASS (max dev 0.00e+00), `T2` PASS (`A = 2.459e-08` at τ=1e-13), `T3` PASS | **PASS** — no verdict flipped |
| E3 | `\|Z₀σ_s\|` grows ≈3.16 at fixed τ | 3.162 (old `Re σ = 1.2501e+02` → new `3.9528e+02` S at 2 eV, τ=1e-16) | **PASS** |
| E4 | `R ≥ 0.999` at 2 eV, τ=1e-16 | `R = 0.999975` | **PASS** |

`OVERALL: PASS`. Verdicts `C0/T1/T2/T3` all PASS; this is a baseline correction, not a re-derivation of the model.

### 4.1 An unregistered observation worth carrying into S0

In the eye's band the response is **frequency-flat**, not merely state-degenerate: `R = 0.975855` at **1.0, 2.0 and 3.0 eV alike** (τ=1e-19), because `ωτ ≤ 0.304 ≪ 1` makes the Drude form dispersionless across the visible
triple. So under this σ_s model the sheet carries **zero chromatic contrast within the eye's band** — which is
stronger than the `|ΔR| = 0.001` state-to-state figure. Consequence for L1/S0: **any colour in a rendered frame is
a declared display convention, not a physical inference** (§6.6 already says this; the number now makes it sharp).
This was not a registered expectation and is therefore recorded as an observation, not a passed test.

## 5. What this re-run does NOT establish

- It does **not** produce a visibility conclusion, and may not be cited as one (§6.7, §8.13 cap).
- It does **not** close G6: `G4` and `G5′` are still open, so the "designated-background test optics" label stays.
- `τ` remains an OPEN input. A σ_s at a scanned τ is not "self-consistent"; it is *parameterised*. The
  self-consistent piece requires R5-L3/L4 and a physical collision-rate model.
- The interband **line shape** remains unknown; only the on/off switch is modelled.

## 6. Dependency versions

python 3.13.12, numpy 2.4.6 (per `requirements.txt`).
