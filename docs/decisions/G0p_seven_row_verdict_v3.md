# G0P-003 Decision Record: Seven-Row Verdict v3 (Superseding G0P-001 / G0P-002)

- **Date**: 2026-11-21
- **Supersedes**: G0P-001 (v1, all numbers revoked), G0P-002 (v2, numbers retained, test integrity revoked)
- **Run record**: `runs/G0/g0p3_results.txt`
- **Registered configuration**: `configs/g0_prime_v3.json` (status=REGISTERED_BEFORE_RUN)
- **Convention statement**: `docs/conventions/dimensional_conventions_v1.md`
- **Code**: `src/g0_analytic/scale_budget_v3.py` + `src/common/conv.py`

## 1. Why the v2 Freeze Was Revoked

The physical core of v2 (2D ultra-relativistic Fermi gas algebra) was correct, but there were four categories of blocking items:

1. **Factor-of-10 error in the handoff line**. `scale_budget_v2.py:345-346` wrote
   `n_e = (n_2D/N_s)*n_B = Z_eff*n_B = 0.2200 fm^-3`; the correct value is `Z_A*n_B = 0.02200 fm^-3`.
   Cause: "electrons per nucleus" was multiplied by "baryon density", whereas `Z_eff` is defined with respect to the nuclear density.
2. **Dimensional conventions incompatible across four modules**, giving four sets of numbers for the same slab, with `X_p` spanning 28×.
3. **"Machine verification" was mostly tautological**. Among v2's 10 tests, T3/T4/T5/T8 were identities,
   T2 was mislabeled (labeling `E_F/m_e c²` as `v_F/c`), and the one genuinely wrong quantity (`n_e`)
   happened to have no test coverage.
4. **Documentation not updated with the code**. §3.2 still contained the wrong formula, and §11.1 (external authorization list)
   retained v1 values without a banner.

## 2. v3 Baseline Values

| Quantity | Value | Source |
|---|---|---|
| `N_s` (nuclear column density) | 4.2155e27 m^-2 = 4.2155e-3 fm^-2 | defining expression |
| `N_B` (baryon column density) | 4.2155e28 m^-2 = 0.042155 fm^-3 | `N_B/L_z` |
| `n_2D` | 2.20049e28 m^-2 = 0.022005 fm^-2 | `Z_A·N_B`, `Z_A=0.522` |
| `k_F` | 0.371834 fm^-1 | `√(4πn_2D/g)` |
| `E_F = μ_e` | 73.37 MeV | `ħc k_F`; `E_F/m_e c²=143.6` |
| `u_2D` | 1.7245e17 J/m^2 = 41.2 Mt/m^2 | `(2/3)n E_F` |
| `P_2D` | 8.6227e16 N/m | `u/2` |
| `c_s` | c/√2 = 2.1199e8 m/s | 2D UR |
| `v_∞` | 4.9635e7 m/s = 0.1656c | `√(2P/Σ)`, `Σ=70 kg/m²` |
| `t_rip(1 m)` | 4.72 ns | `1/c_s` |
| `u_2D/Mc²` | 2.741 % | |
| `τ_T` (frozen state) | 1.4639 | `σ_T n_2D` |
| `Γ_e` | 2.258e-3 | `U_e/E_F` |
| `A_min` | 3.794e8 m² ≈ 380 km² | `N_s d_bond²` |

## 3. Seven-Row Verdict

| # | Objective | Verdict | Basis | Evidence level |
|---|---|---|---|---|
| 1 | Maintain the original atoms/chemical bonds/non-covalent network at fixed area | **NO-GO** | `d_∥=15.40 fm = 2.91e-4 a₀` (geometric; independent of the electron convention, conditional on fixed `(M, A_⊥, m̄)`; scales as `(A_⊥/M)^{1/2}` under variation of these parameters) | MODEL RESULT |
| 2 | New stable high-density state | **OPEN** | R1-B1 v3 three-convention envelope: `X_p∈[1.62e-3, 4.50e-2]`, `μ_e∈[6.73, 24.96] MeV` | OPEN (convention-dependent) |
| 3 | Healthy positive solution for geometric contraction | **OPEN** | D3/R2; N11 input changed to the envelope `P_tot∈[1.84e16, 6.48e16] N/m` | OPEN |
| 4 | Effective 2D low-energy theory | **OPEN** | R1-B4 v3: the domain covers the G0 density but not `n_0` | OPEN(conditional) |
| 5 | Other matter/radiation states | **OPEN** | R1-B2 v3 verdict UNDECIDED; R1-B3 provides only a reference timescale | OPEN |
| 6 | Mechanical self-equilibration of the fixed-area final state | **NO-GO** (condition: frozen-state ideal UR electron-gas pressure + `P_constraint=0`) | `P_2D=8.62e16 N/m`; without constraint `c_s=2.12e8 m/s`, 4.72 ns over 1 m, `v_∞=0.166c` | MODEL RESULT (model-conditioned) |
| 7 | Whether the v1.3 cold-electron-gas final state is the ground state at that density | **NO** | `μ_e∈[6.73,24.96] MeV` exceeds all kinematically allowed Q values in every convention (max 13.37); the `ν` budget is a registered placeholder (`/u_2D=1.125`) | MODEL RESULT |

## 4. Test Ledger (Honest Counting)

| Category | Count | Meaning |
|---|---|---|
| CHECK | 7/7 passed | genuinely independent calculations, usable as correctness evidence |
| IDENT | 3/3 passed | defining identities, **not counted as evidence** |
| NEGCTRL | 1/1 passed | negative control that must fail (`Z_eff·n_B` is off by exactly 10.000×) |

CHECK details: C1 `k_F` closed form vs quadrature; C2 `u` closed form vs quadrature; C3 numerical `c_s²` `dP/du`=0.50000000;
C4 3D Chandrasekhar UR limit `P/u`=0.333333; C5 subband-spacing ratio 8.45 (>3, D=2 holds);
C6 capture-threshold margin 60.00 MeV; C8 β-equilibrium residual 3.55e-15 MeV.

**Convention discipline**: v2's "10/10 PASS" included 4 identities; in v3 only 7 CHECK items can serve as evidence. When citing any pass count, the category must be specified.

## 5. Scope of Validity

- Frozen-state baseline values (first 11 rows of §2) **may be cited**, and must be marked MODEL RESULT.
- β-equilibrium quantities (`X_p`/`μ_e`/`n_e`/`P`) **must be presented as a three-convention envelope**; single-point values are not allowed.
- `ν` energy loss, `Γ_i`, and crystal-phase conclusions **must not be cited** (the first is a placeholder; the latter two have been revoked/UNDECIDED).


---

## 6. Erratum E1 (round 58) — row 7's "in every convention" is false at `ALL2D`

**The row is not edited and its verdict is not re-opened.** `RQ-08`'s product
`runs/R3/n7_recheck_results.txt` evaluates the row's own sentence against the registered
`configs/g0_prime_v3.json` capture table.

- **E1** Row 7 reads *"`μ_e∈[6.73,24.96] MeV` exceeds all kinematically allowed `Q` values in every
  convention (max `13.37`)"*. At the printed lower endpoint `ALL2D μ_e = 6.7331 MeV`
  (`μ_kin = 6.2221 MeV`) the captures on `O16` (`7.12`), `Mg24` (`10.77`) and `C12` (`13.37`) are
  **closed**; exactly three of six (`p`, `Fe56`, `N14`) are open. The `0.511 MeV` convention shift does
  not rescue the clause: `6.7331 < 7.12` either way. The clause is false at the row's own endpoint.
- **E2** The row's verdict — *NO, the v1.3 cold-electron-gas final state is not the ground state* —
  survives on independent grounds: the frozen state alone is `6/6` open with a `59.49 MeV` margin
  after normalization, and `HYB` and `ALL3D` are `6/6` open as well. **Evidence level `MODEL RESULT`
  is unchanged**; only the universal quantifier is withdrawn. Row 2's `μ_e` envelope is not edited.

---

## 7. Erratum E3 (round 65) — row 1 is triggered, not reopened

**The row and its reverse-on cell are not edited.** `runs/P1/phase1c_repricing_results.txt`
(product emitted before this append; its input SHA-256 refers to the pre-append file) checked the
dependency of the row's stated basis on the Phase 1b result.

- **E3** Row 1's basis is the electron-convention-independent distance
  `d∥ = 15.40 fm = 2.91e−4 a₀`; it is **not** the claim that `L_z=0` is a curvature singularity. The
  flat Kasner slice therefore does not remove that basis and does not change the `NO-GO` verdict.
- The reverse-on cell reads “none stated (geometric, convention-independent)”. The discovery that
  one geometric statement is slicing-dependent is recorded as a **trigger**, not as a ruling: the
  verdict, the reverse-on cell, `D1`, `D8`, the selected rung and the queue remain unchanged. A
  governor decision is required to turn this trigger into a reopening.

---

## 8. Erratum E4 (round 71) — the reverse-on's “convention-independent” acquires its condition

**Authority**: governor directive G-71-01 §1.2. Unlike E1–E3, this erratum is accompanied by **one edit inside
§3**: row 1's basis cell now carries the conditional clause. E3's sentence “the row and its reverse-on cell are
not edited” stands as the state of the record until this round; it is left in place so the departure is visible
rather than tidied away.

- **E4** Row 1's reverse-on cell reads “none stated (geometric, convention-independent)”. That sentence is carried
  in `reports/DCC_terminal_answer_v1.md`, which is a **sealed** product (ledger round 62,
  sha256 `23f6813392621b40…`). It is therefore not edited. The replacement is carried here, and the sealed hash is
  preserved:

  > “geometric, conditional on fixed `(M, A_⊥, m̄)`; scales as `(A_⊥/M)^{1/2}` under variation of these
  > parameters”

- **What was wrong**: “convention-independent” is true of the *electron* convention — the row's actual point, and
  the reason it survives §7's E3 — and false of the *object* parameters. `d∥` is fixed only once `(M, A_⊥, m̄)`
  are fixed (crosswalk §8.1); at `M → 10 M` and fixed area the pitch falls to `4.871 fm` and the `RL-6` ratio
  spans `6.16e3 … 6.16e4`. The cell named neither the condition nor the scaling.
- **What moves**: one parenthetical in §3's row 1. **What does not move**: the `NO-GO`, the `MODEL RESULT`
  evidence level, the reverse-on condition itself (`none stated`), `D1`, `D8`, the selected rung `RL-1 + RL-2`,
  the `RL-6` price, and every entry of §4's test ledger. The verdict never rested on the parenthetical: it rests
  on `d∥ = 15.40 fm = 2.91e−4 a₀`, which the substitution leaves untouched.
- Evidence: `runs/AX/ax01_axiom_audit_results.txt` `F-002`, `C-006`, `C-023`; repair record
  `runs/RR-DT/rr_dt_01_record_repair_results.txt`.
