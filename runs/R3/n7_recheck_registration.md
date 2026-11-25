# RQ-08 — pre-registration: does `N7` still block at the state-derived `μ_e`?

**Written before the instrument is run.** Round 58. Governing text:
`docs/conventions/effective_2d_definition_v1.md` §4 (the `N7` prerequisite check) and §7 rule 2
(*"forbidden to use 'effectively 2D' for an electron gas before performing the `N7` carrier check"*),
as quoted in `docs/decisions/sc_route_ruling_v1.md` §1 (`P8`) and recorded as blocking `G5′` in
`reports/DCC_research_progress_v1.md` §G rows.

**Product**: `runs/R3/n7_recheck_results.txt`, emitted by `src/r3/n7_recheck.py` (`--write`), never
transcribed. **Inputs**: `configs/g0_prime_v3.json` (`capture_Q_MeV_kinetic`, convention line);
`src/common/conv.py` (`frozen_state`, `beta_eq`, `eos_e_2D`, `eos_e_3D`, `N_B_FM2`, `M_E`, `M_N`, `M_P`);
`runs/R1B/r1b1_p2_eos_scan_results.txt` (P2-1 solved `μ_e`, P2-5 `L_z` window);
`runs/R1B/r1b1_p4_census_results.txt` (`RQ-05`: free fraction, four margins);
`runs/R1B/r1b1_p4_tau_results.txt` (`RQ-03`: `τ`, `σ_DC`);
`runs/R1B/r1b1_p4_p5_closure_v1.md` §5c–§5d (why the `4.6%` is not a census).

## 1 The three questions that must be kept apart

1. **Arithmetic**: does therozen-baseline comparison reproduce at the state-derived `μ_e`?
   The frozen baseline: `μ_e = 73.373 MeV` against `Q ∈ {0.782 … 13.37}`. Solved: `HYB μ_e = 21.5445 MeV`,
   `ALL3D 24.9566`, `ALL2D 6.7331`, and the five `L_z = 1.68…1.99 fm` states `15.059…16.484`.
2. **Convention**: the `Q` table is kinetic (`μ_e − m_e`, F-G0-8 / `g0_prime_v3.json`); `conv.eos_e_3D`
   returns a **total** energy while `conv.eos_e_2D` returns `ħck` (**kinetic**, despite being used by
   `beta_eq` in the total-chemical-potential slot). The round must not compare one against the other
   without normalizing, and must say what the `0.511 MeV` shift does to each verdict.
3. **Inference**: `N7` says `μ_e > Q` ⇒ *"the carriers themselves are removed … the low-energy
   effective description loses its object"*. The solved state has a nonzero electron population by
   construction and `RQ-05` measured the free fraction to be `1.000`. So either the antecedent is not
   the right threshold for this object, or the implication is false. **The round decides which.**

## 2 Definitions and hand estimates fixed before the run

- `Q` kinetic: p `0.782`, Fe56 `3.69`, N14 `5.88`, O16 `7.12`, Mg24 `10.77`, C12 `13.37 MeV`.
  Normalized electron energy `μ_kin ≡ μ_e − m_e`, `m_e = 0.511 MeV`, applied uniformly.
- Beta equilibrium from `conv.beta_eq`: `μ_n − μ_p = μ_e`, with `μ_n = M_N + E_F,n`,
  `μ_p = M_P + E_F,p`, `M_N − M_P = 1.293 MeV`. Define `ΔF ≡ E_F,n − E_F,p`.
- **Hand estimate (done before coding)**: a Fermi-surface e + p can capture only if the daughter
  neutron can be placed above its own Fermi sea, so the *host-specific* threshold is
  `Q_eff,p = 0.782 + ΔF`, not `0.782` alone. Since `μ_e = 1.293 + ΔF`, `μ_kin = 0.782 + ΔF = Q_eff,p`
  identically at equilibrium. Expected: `HYB ΔF = 21.5445 − 1.293 = 20.2515`,
  `Q_eff,p = 21.0335`, `beta_res ≈ 0`. **The solved state sits at the capture threshold, not above it.**
- Frozen `μ_kin = 72.862`; `ALL2D μ_kin = 6.222` (open: p/Fe/N; closed: O/Mg/C);
  the `0.511 MeV` shift is **less** than ALL2D's distance to either neighbour (N14 `0.342`,
  O16 `0.898`), so no classification depends on it.

## 3 Predictions (falsifiable, checked by the instrument)

| # | prediction | bar |
|---|---|---|
| `P1` | `conv.frozen_state().EF_2D` reproduces `73.372975 MeV`; all six frozen captures open | rel dev `< 1e-8`; `6/6` |

**Pre-run clarification (before any instrument run):** `P1`'s bar was first written `1e-9`. The
registered comparison value is printed to six decimals, so the rounding residual alone is
`3.13e-9`; the bar is loosened to `1e-8` *before* the run, not after a miss. No other bar is touched.
| `P2` | `HYB μ_e` reproduces P2-1's `21.5445 MeV` | rel dev `< 1e-4` |
| `P3` | naive solved-HYB comparison is still `6/6` open, min margin `μ_kin − Q(C12) = 7.663 MeV` | `6/6`, margin within `1e-3` |
| `P4` | `ALL3D` naive: `6/6` open, min margin `11.0756 MeV` | `6/6`, margin within `1e-3` |
| `P5` | `ALL2D` naive: exactly `3/6` open (p, Fe56, N14); O16/Mg24/C12 **closed** — refutes G0p-v3 row 7's "in every convention" | exactly `3/6` |
| `P6` | all five `L_z` states are `6/6` open; thin margin `1.178 MeV` at `L_z = 1.99` | `5/5`, min margin within `2e-3` |
| `P7` | normalization identity: `μ_e − m_e = 0.782 + ΔF` in all three modes (two independent routes through `conv`) | max rel dev `< 1e-10` |
| `P8` | Pauli-shifted proton threshold at solved HYB is `Q_eff,p = 21.0335`, **equal** to `μ_kin` | rel dev `< 1e-6`; `beta_res` `< 1e-6` |
| `P9` | residual carriers are present: `n_e,areal(HYB) > 0` and `RQ-05`'s free fraction is `1.000` with margins `>= 10×` | both |
| `P10` | naive `N7` implication is falsified at the solved state: antecedent `TRUE` (`6/6` open), consequent `FALSE` (carriers present) | logical, both readings printed |
| `P11` | `τ` and `σ_DC` do not move: `μ_e` is not an input to `RQ-03` | rel dev `< 1e-12` vs `2.00e-20 s`, `8.63e-4 S` |
| `P12` | no `S1`–`S15` verdict moves and the `P4-1` partition is unchanged | all identical |
| `P13` | `ΔF` spans `5.440…23.664 MeV` across conventions; the naive margin is convention-dependent by `18.224 MeV` (`4.35×`) | envelope within `1e-3` |
| `P14` | this instrument writes **no** gate mark: `G5′` stays NOT PASSED pending `G4`/`R1-B4` | queue marks unchanged |

### Decision rules fixed before the run

- If `P3`, `P8`, `P9`, `P10` all hold → **CLOSED-CONSTRUCTIVE**: the block is reproduced as threshold
  arithmetic but is a **frozen-baseline artefact** when transferred to the equilibrated state; `N7`
  must be phrased with the host-specific (Pauli-shifted) threshold. `G5′` is **not** passed by this.
- If `P8` fails (e.g. `μ_kin` materially exceeds `0.782 + ΔF`) → the block survives; verdict
  **CLOSED-NO-GO** for the carrier question and the gate remains blocked with a number.
- If `P5` fails → withdraw the G0p-v3-row-7 finding; no erratum to that document.
- Any prediction miss is reported and kept; no bar is re-fitted after the run.

## 4 Scope limits registered in advance

- This round re-evaluates the **carrier-conservation threshold**, not the effective-2D conditional's
  other three slots (model / subsystem / probe), and not the `G4` bulk instability.
- It does not claim that capture *never occurs*: at `T = 0` and exact equilibrium the net rate is
  zero; a displaced state still captures. The claim is only about the state the EOS produced.
- Archived text is never edited (`s9.1`); corrections are appended errata on
  `docs/conventions/effective_2d_definition_v1.md` and `docs/decisions/G0p_seven_row_verdict_v3.md`.
