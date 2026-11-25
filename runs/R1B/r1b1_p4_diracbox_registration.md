# RQ-04 — pre-registration: the exact Dirac-box z-ladder (refinement ii)

**Written before the instrument is run.** Round 59. Governing text:
`docs/decisions/g6_dc2_ruling_v1.md` §3 refinement `(ii)` — *"exact Dirac-box `z`-ladder beyond the
Schrödinger-envelope approximation (the UR-box TRK deficit is the five-point answer; the exact
Dirac-box treatment is the refinement)"*; queue `RQ-04` asks whether the `0.9975` deficit survives.

**Product**: `runs/R1B/r1b1_p4_diracbox_results.txt`, emitted by
`src/r1_dense/r1b1_p4_diracbox.py` (`--write`), never transcribed. **Inputs**:
`src/r1_dense/r1b1_p4_response.py` P4-2 (the UR-box ladder and its printed sum/deficit);
`runs/R1B/r1b1_p4_response_results.txt` P4-2; `src/common/conv.py`
(`HBARC`, `M_E`, `beta_eq`, `kF_2`, `LZ_FM`); `configs/g0_prime_v3.json` (capture table, not used
here); `runs/R1B/r1b1_p4_tau_results.txt` (`τ`, `σ_DC`, quoted only).

## 1 What is being compared, and what is not

The archived P4-2 ladder solves a **Schrödinger envelope** in an infinite well: sine wavefunctions,
linear energies `E_n = n E_z,1`, `E_z,1 = πħc/L_z`, and bare-mass oscillator strengths
`f_1n = 2 m_e c² ΔE z_1n²/(ħc)²`. The refinement replaces the z-sector by an exact 1D Dirac
Hamiltonian with **current-conserving (MIT-bag) boundaries**, `|ψ_up| = |ψ_down|` at both walls:

- **S bag** (same sign at both walls): `k_n = nπ/L_z`, like-for-like with the UR box's spectrum;
  upper/lower spinors with `α_n = m_ec²/(E_n + ħck_n)`, `E_n = √((ħck_n)² + (m_ec²)²)`;
- **O bag** (opposite signs, outward normals): `k_n = (n−½)π/L_z` — evaluated as a **sensitivity
  check**, not as a replacement for the like-for-like comparison.

The same oscillator-strength normalisation (`2 m_e c² ΔE |⟨n|z|1⟩|²/(ħc)²`) is applied to both
UR and exact ladders, so the comparison isolates the z-sector treatment. Matrix elements are
computed **analytically** from closed-form integrals `J(q) = ∫₀ᴸ z cos(qz) dz = L sin(qL)/q +
(cos(qL)−1)/q²`; quadrature is used only as an independent cross-check.

**Not claimed**: a revised `σ_s(ω)`. The round recomputes `f_1n` and the deficit; it does not
re-solve the electron state or re-grade `G6`/`DC2`. Ancillary structural findings are registered,
not applied.

## 2 Hand estimates fixed before the run

At `L_z = 1.84 fm`, `E_z,1 = 336.913583 MeV`, `m_e c² = 0.511 MeV` (`m/E = 1.52e−3`):

| quantity | UR box | exact S bag |
|---|---|---|
| `Σ f_1n`, `n = 2…12` | `9.932045695e−4` | `1.291317638e−3` (×`1.300153`) |
| `f_intra = m_ec²/E_1` | `1.516709407e−3` | `M/√(E_z,1²+M²)` (rel shift `−1.15e−6`) |
| deficit | `0.997490086` | `0.997191973` (`Δ = −2.98e−4`) |
| `|z_12|` | `0.33143 fm` | `0.37291 fm` (×`1.1253`) |

The high-`n` ratios grow (`×2.44` at `n = 4`, `×12.4` at `n = 12`) because the UR sine matrix
element falls as `n⁻³` while the Dirac spinor matrix element falls as `n⁻²`; the **sum** is still
dominated by `n = 2`, so the deficit moves only in the fourth decimal. The O-bag sensitivity is
`Δ deficit ≈ 3.6e−7` versus the S bag. These estimates were computed before the instrument existed;
no bar is refitted after the run.

**Pre-run clarification (before emission):** `P4`'s first hand ratio `×1.12526` was formed from the
five-digit rounded `0.37291 / 0.33143`; carried at full precision the same quantities give
`0.37290906 / 0.33143285 = 1.12514`. The registered value is corrected to the full-precision
ratio with its bar unchanged. `P10`'s check is likewise clarified before the run: an analytic zero
(S-bag odd `n`) is compared to quadrature on an absolute floor, not by a relative deviation.

## 3 Predictions (falsifiable)

| # | prediction | bar |
|---|---|---|
| `P1` | the instrument reproduces P4-2's UR sum `9.932045695e−4`, `f_intra = 1.516709407e−3`, deficit `0.997490086` at `NMAX = 12` | rel dev `< 1e−8` |
| `P2` | exact `E_1 = √(E_z,1²+M²)` exceeds `E_z,1` by `3.88e−4 MeV` (rel `1.15e−6`) | rel dev `< 2e−3` |
| `P3` | exact `f_intra = M/E_1` shifts by `−1.15e−6` relatively | rel dev `< 2e−6` |
| `P4` | exact `|z_12| = 0.3729091 fm`, `×1.12526` over the UR value | rel dev `< 1e−5` |
| `P5` | exact S-bag sum (2…12) `1.291317638e−3`, ratio `1.300153` to UR | rel dev `< 1e−6` |
| `P6` | exact deficit `0.997191973`; `Δ = −2.98113e−4`; **survives to three decimals** | both within `1e−6`; rounding to 3 decimals identical |
| `P7` | tail beyond `n = 12` estimated from the `f ∝ n⁻³` asymptote is `< 1e−5` in both ladders | both |
| `P8` | O-bag deficit differs from S-bag by `< 1e−6` — the boundary-sign convention does not move the answer | measured |
| `P9` | parity selection survives: S-bag odd `n` matrix elements are exactly `0`; O-bag odd terms are `O(α)` and `< 1e−9` in `f` | measured |
| `P10` | analytic matrix elements agree with independent numerical quadrature of the spinors (analytic zeros checked on an absolute floor, since a `0/0` relative deviation is meaningless) | rel dev `< 1e−8` on nonzero terms |
| `P11` | no `S1`–`S15` verdict moves: `f_intra + Σf_1n + deficit = 1` remains a declared partition; `S12a/b`, `S5`, `S14` unchanged | all identical (structural) |
| `P12` | `τ` and `σ_DC` are unchanged (`μ_e` and the z-sector refinement are not inputs to `RQ-03`) | structural |

### Decision rules fixed before the run

- If `P1`, `P5`, `P6`, `P10` hold → **CLOSED-CONSTRUCTIVE**: the deficit survives, with a stated
  number for the shift; refinement `(ii)` is discharged and the closure document gains an erratum.
- If `P6` fails (deficit moves in the first three decimals) → **CLOSED-CONSTRUCTIVE** still, but the
  five-point answer is revised and `S5` needs re-adjudication — reported, never hidden.
- If `P10` fails → **BLOCKED-ON-INPUT** for the analytic matrix elements; no verdict emitted.
- Any miss is kept; no bar changes after the run.

## 4 Scope limits and the structural flag registered in advance

- The same-sign bag has a `k = 0` eigenmode at `E = m_ec²` with constant equal upper/lower spinors.
  It is **not** part of P4's occupied-subband construction (which takes `n = 1` as the ground
  subband, `m_eff = E_z,1/c²`). The round will **measure and report** its dipole coupling and the
  in-plane mass implication, but will **not** re-solve the state or revise `σ_s`; that is a board
  note, not a verdict. If the mode were occupied, the Drude weight's mass assumption would change —
  that question belongs to the state, not to this refinement.
- The negative-energy Dirac continuum remains in the declared UV bucket; the deficit is not
  interpreted as an experimentally measurable missing weight.
- Archived text is never edited (`s9.1`); the correction is an appended erratum on
  `runs/R1B/r1b1_p4_p5_closure_v1.md` and a board note.
