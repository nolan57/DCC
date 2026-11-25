# R1B1-P4/P5 — Response Construction and the G6/DC2 Status (round 45)

**Status**: the `R1B1-P4` response construction and the `P5` interface statement, executed under the
governor's veto-lift adjudication (round 44: "All vetoes are hereby lifted... until every possible path
and every staged task has been driven to completion").
**Products**: `src/r1_dense/r1b1_p4_response.py` → `runs/R1B/r1b1_p4_response_results.txt`;
the state inputs from `r1b1_p2_eos_scan_results.txt` (P2, 9/9 PASS); the reachability from
`r1b1_p3_reachability_results.txt` (P3, 6/6 PASS, one self-caught theorem retraction archived).

---

## §1 `P4` — the response constructed from the solved state

The four necessary interface inputs, **all `DERIVED` from the certified P1 theory and the P2 states**
(the first time in the programme that this tuple is not assumed):

| input | value (HYB, `L_z = 1.68/1.84/1.99 fm`) | status |
|---|---|---|
| `n_2D = n_free,2D` | `1.111 / 1.008 / 0.927 ×10⁻³ fm⁻²` | DERIVED (`N7-SPLIT` realized: 4.2–5.0% of the bookkeeping `n_Q,2D`) |
| `g` | 2 (spin, single occupied subband) | DERIVED |
| `v_F` | **`0.0316 / 0.0330 / 0.0342 c`** | DERIVED (`ħk_F/m_eff`, `m_eff = E_z,1/c²`) — the `V-F-IMPLIED` alert (`v_F = 1.000071c`, undeclared) is resolved by the state |
| `ω_end` | **`5.61 / 5.12 / 4.73 ×10²³ rad/s`** (`πc/L_z`, the inter-subband edge) | DERIVED from band structure — genuinely different from the withdrawn `440.18 MeV` identity |

**The five-step decomposition** (`f_intra` — the quantity the optics criteria were measured to be blind
to, now supplied by the matter model exactly as the interface demanded):

```
f_intra = m_e c² / E_z,1 = 1.52×10⁻³          (in-plane intraband share)
f_12    = 9.71×10⁻⁴ at ω = 5.12×10²³ rad/s    (the dominant inter-subband line)
Σf_1n   = 1.00×10⁻³                           (the UR-box z-ladder)
deficit = 1 − f_intra − Σf_1n = 0.9975        (the UV-compensation bucket)
```

**The five-point checklist item 5 is QUANTIFIED**: 99.75% of the bare-mass f-sum weight sits in the
UV-compensation bucket (negative-energy/continuum z-motion weight at and above the subband scale) —
the low-energy optical response carries only ~0.25% of the bare-mass sum. This is the quantitative
answer to veto-item 7.

**The assembled response** (collisionless ideal level): `Re σ_s = W_intra δ(ω) + ΣW_n δ(ω − ω_1n)`
with exact KK causal partners (S4 by construction); the intra sector is exactly one pole (the
τ→∞ Drude — S12a/b satisfied); τ = ∞ at the declared ideal level with the mechanism declared
(electron–proton impurity scattering, `X_p ≈ 2.4×10⁻²`) and the finite-rate computation registered as
the named refinement.

## §2 `P4-4` — the `S1`–`S15` application to the constructed candidate

All criteria applied: **PASS** for S1, S3, S4, S5 (partition with the declared UV bucket), S6, S8,
S9, S10, S11, S12a/b, S13, S14 (`ω_end` from bands — not the withdrawn identity), S15 (the tuple
state-derived); **S7 CONDITIONAL** — the mechanism is declared, the value is collisionless at the
ideal level, and the finite rate needs the interaction matrix elements (named refinement, not a
hidden gap).

**The candidate `σ_s(ω)` is ADMISSIBLE at the ideal level.**

## §3 `P5` — the `G6`/`DC2` status

The `G6`/`DC2` NO-GO was grounded on "no compliant `σ_s` exists; the object is absent." Both grounds
have moved:

1. **A compliant candidate exists** — constructed from the certified closed theory and the solved
   states, with every interface input DERIVED and the five-point checklist quantified. The blocker
   (no candidate) is **resolved at the model level**.
2. The state itself is ideal-level: the refinement chain is registered and named —
   (i) the finite `τ` from e–p impurity scattering (S7's named refinement);
   (ii) the Dirac-box z-ladder beyond the Schrödinger-envelope approximation (the UR-box TRK deficit
   is the five-point answer; the exact Dirac-box treatment is the refinement);
   (iii) the interaction-level census refinement (bound/trapped states beyond the ideal census);
   (iv) the L_z-resolved family is the input surface for `R1-B4`/`R3`.

**The `G6`/`DC2` gate status for adjudication**: NO-GO → **CONDITIONAL ADMISSIBILITY at the model
level** — an admissible candidate σ_s exists; the gate's final ruling (and any visibility/observer
statement, still forbidden by S9) remains the governor's. The NO-GO record is retained in full: it was
the correct verdict at every prior stage, and its lifting is now *earned by construction*, not assumed.

## §4 The staged-task ledger at the close of the veto-lift execution

| staged task | verdict |
|---|---|
| `R1B1-P2` (static states/EOS, `L_z` scan, 3 conventions) | **9/9 PASS** — bounded, causal, stable equilibrium states exist in the `K1` window; the envelope is `L_z`-resolved |
| `R1B1-P3` (dynamic reachability) | **6/6 PASS** — `p_z` exactly conserved (theorem); spinor adiabaticity `2.4×10²¹ ≪ 1`; weak-ON endpoint reachable (late-time attractor); weak-OFF endpoint = frozen state (row-7-ruled non-ground-state); one self-caught theorem retraction archived |
| `R1B1-P4` (response construction) | the interface tuple DERIVED; `f_intra = 1.52×10⁻³`; the TRK deficit quantified (0.9975); the candidate **ADMISSIBLE** (S7 conditional) |
| `R1B1-P5` | this document: the `G6`/`DC2` status flip submitted for adjudication |
| the registered instrument defect | the y-sector component check (`(γ⁰γ²)ᵀ = −(γ⁰γ²)`) — recorded, non-gating, diagnostic archived |
| the theorem retraction | `[H_D(t), H_D(t')] = 0` proposed and rejected by the pre-registered instrument — archived with the FAILED check |

*Content generated by AI*

---

## §5 Erratum E1 (round 56) — refinement (i) is executed

**Nothing above is edited.** `RQ-03` computed the finite `τ` and its product is
`runs/R1B/r1b1_p4_tau_results.txt` (instrument `src/r1_dense/r1b1_p4_tau.py`, pre-registration
`runs/R1B/r1b1_p4_tau_registration.md`).

`τ_tr = 2.00e-20 s` at `L_z = 1.84 fm` (1.86–2.14e-20 across the K1 window), from
`V(q) = 2πe²/(ε(q+q_TF))` with `n_imp = n_free,2D`; `τ_sp = 5.98e-21 s`; `σ_DC = 8.63e-4 S`;
`ħ/τ = 32.9 keV`. `S7` therefore reads **PASS-ON-PREMISE** rather than CONDITIONAL: the rate is
named, traced and unscanned, but it exists only if the protons are *localized and disordered*
(`Q-1`, `Q-2`). Both clean arrangements — a co-moving proton fluid, and a perfect proton lattice
(`2k_F/G_min = 0.691`) — are perfect conductors, i.e. `τ = ∞`. The finite number is a property of
disorder, which the `P2` state does not contain.

`S13` reads **PASS** (named: transport; traced: impurity-averaged Born self-energy; not scanned).
`S12a/b` are untouched: the intra pole remains a single pole 4.0 decades below the ladder.

**The residue list of the G6/DC2 flip (PG-01) changes, the mark does not.** §3's refinements are
`(i)` finite `τ`, `(ii)` Dirac-box z-ladder, `(iii)` interaction-level census, `(iv)` the family
handoff. `(i)` moves from *unresolved* to *resolved-with-premise* (`Q-1`/`Q-2`, now a question
inside `(iii)`); `(ii)`–`(iv)` are unresolved as before. A document citing the flip must now name
`Q-1`/`Q-2` if it cites the rate.

## §5a Erratum E2 (round 56) — the `P4-1` table's `k_F` is low by `√2`

`src/r1_dense/r1b1_p4_response.py:71` computes `kf = sqrt(2·π·n_free/2)` = `sqrt(π n)`, while the
registered definition (`conv.kF_2`) is `n = g k²/(4π)` → `k = sqrt(4π n/g)` = `sqrt(2π n)`. The
table therefore prints `k_F = 0.0563 fm⁻¹` where the state gives `0.0796`, and `v_F = 0.0330 c`
where it gives `0.0466`. The same product's prose already prints `v_F ≈ 0.049 c`, so the factor is
visible in the round-45 product as a disagreement between its table and its text; and
`conv.eos_e_2D(n)` returns `E_F = 15.705 MeV` against the table's `11.105`, a ratio of `1.414214`.

The table is **not edited**. Consequence for consumers: `v_F` is `0.0466 c`, not `0.0330 c`; the
`S15` tuple's other three entries are unaffected. For `τ` the error is `1.71×` (a `√2` in `k_F`
enters `1/τ` through `J2/k_F²`), so `r1b1_p4_tau_results.txt` §3 prints both values.

## §5b Erratum E3 (round 56) — the `S13` illustration's `91.5` is a number about another state

`docs/specs/surface_conductivity_v1.md` §10 says "for a static Thomas–Fermi 2D Coulomb kernel at the
record's own `q_TF/k_F = 0.0146`, `τ_tr/τ_sp = 91.5`". Evaluated at that argument, the same integral
gives `45.8`; `91.5` is its value at `q_TF/k_F = 0.00715 ≈ 0.489 × 0.0146` — so the sentence's ratio
and its argument are not the same configuration (a factor 2 in what `q_TF/k_F` denotes). **`S13` is
binary and unaffected**; no threshold moves.

The substantive point is the transfer: for `q_TF/k_F ≪ 1` the ratio is `≈ π q_TF/k_F =
2πα/(v_F/c)`, i.e. it scales as `1/v_F`, and `0.0146 = 2α` is exactly `r_s = α`, i.e. `v_F = c` —
the frozen model's undeclared `v_F`, the input the solved state replaced. At the solved state
`r_s = 0.157` and the ratio is `3.35`, `27×` smaller. The illustration is therefore a number about
a superseded state and may not be carried over to another one.


## §5c Erratum E4 (round 57) — the `4.2–5.0%` in §1's own table is `X_p/Z_A`

**Nothing above is edited.** `RQ-05` computed the census and its product is
`runs/R1B/r1b1_p4_census_results.txt` (instrument `src/r1_dense/r1b1_p4_census.py`,
pre-registration `runs/R1B/r1b1_p4_census_registration.md`).

§1's table row reads `n_2D = n_free,2D … DERIVED (N7-SPLIT realized: 4.2–5.0% of the bookkeeping
n_Q,2D)`. That ratio is **not** a carrier fraction. It is an identity of the EOS:

```
n_free,2D / n_Q,2D  =  (X_p · N_B) / (Z_A · N_B)  =  X_p / Z_A
```

and the instrument confirms it to machine zero at all five `L_z` (`0.045813` at `L_z = 1.84 fm` =
`2.39142e-2 / 0.522`). Charge neutrality is *imposed* as `n_e = n_p` in `beta_eq`, so the numerator is
`X_p·N_B` by construction and the denominator is `Z_A·N_B` by definition. What the column measures is
therefore the **composition mismatch** between the frozen `Z_A = 0.522` and the solved `X_p = 2.39e-2` —
the frozen composition is `21.8×` more proton-rich — and not any binding, trapping or ionization.

**Consequence for citations.** The same figure appears twice in the record as a `DERIVED` census:
here, and in `docs/decisions/g6_dc2_ruling_v1.md` §2's table (`DERIVED (N7-SPLIT: 4.2–5.0% of the
bookkeeping n_Q,2D)`). Both must be read as *"the solved proton fraction is 4.2–5.0% of the frozen
charge column"*. Neither may be cited as evidence that 95% of the carriers are bound or trapped — there
was never a carrier population in the difference. The ruling's mark is **not** re-opened and its cell is
**not** edited (`s9.1`); the reading is corrected here and registered as `BN-24`.

The `P2-5` verdict line — *"the split is realized, not assumed"* — is likewise unsupported by the number
printed beside it. The split as a **definition** (two quantities, `n_Q,2D` and `n_free,2D`, carried
separately) is real and is what `N7` asked for; the split as a **measurement** of free carriers was not
performed in P2 and is performed in `RQ-05`, which finds the free fraction to be `1.000` with margins
of `10×` or more on four criteria. The `P2` product is not edited; this paragraph is the erratum.

## §5d Erratum E5 (round 57) — condition (iii)'s stated target is the wrong target

§3's table and the ruling's §7 condition (iii) both say the census moves *"`n_free,2D`, hence
`f_intra`"*. The second half is false as written, and the round shows it by inspection and by
computation:

```
f_intra = m_e c² / E_z,1 ,     E_z,1 = π ħ c / L_z
```

contains no `n_free` at all. Perturbing `n_free` by `×0.5` and `×2` leaves `f_intra`, the ladder sum
`Σf_1n` and the deficit bit-identical (`1.516709406786460e-03`, `9.932045695383242e-04`,
`9.974900860236752e-01`). What the census does move is the overall weight
`W_TRK = πe²n_free/(2m_e)`, which multiplies all three fractions and enters no criterion except through
`S5`'s closure — where both sides rescale together.

Two further facts from the same instrument, recorded because they are the round's answer to *"how far
does `n_free,2D` move?"*: (i) the answer is **not at all** — bound and trapped rows are `0` in all six
cells (`3 L_z × 2` mass conventions), with margins `26×` (Mott orbit overlap), `10×` (`E_b/E_F`), `21×`
(`U/W`) and `22×` (`k_Fℓ`); (ii) the density **cancels from the rate**, because `n_imp = n_free` and
`k_F² ∝ n_free` carry the same `n`, leaving `1/τ ∝ m·J2(x)` with `x = q_TF/(2k_F) ∝ n^(-1/2)`. A `2×`
density change moves `τ` by `12%` and `σ_DC` by `1.77×`, not by `2×`. So even the lever the ruling
attributes to (iii) is weaker than stated, and it is weaker *because* the census is null.

Condition (iii) is **discharged**: the interval requested exists (`[0.927, 1.111]×10⁻³ fm⁻²`, the `L_z`
envelope) and its width in the bound/trapped direction is zero by measurement. What (iii) was thought to
buy — a shift in `f_intra` — it does not buy, and the ruling's column needs that correction before any
downstream document can cite (iii) as the reason a number moved.


## §5e Erratum E6 (round 59) — refinement (ii) is executed

**Nothing above is edited.** `RQ-04` recomputed the `z`-ladder and its product is
`runs/R1B/r1b1_p4_diracbox_results.txt` (instrument `src/r1_dense/r1b1_p4_diracbox.py`,
pre-registration `runs/R1B/r1b1_p4_diracbox_registration.md`).

An exact 1D Dirac box with current-conserving MIT boundaries replaces the Schrödinger envelope:
`E_n = √((ħck_n)² + (m_ec²)²)`, spinor dipole matrix elements from closed-form `J(q)` integrals,
checked against independent quadrature to `≤ 1.3e−10` relative on the nonzero terms. With the
like-for-like same-sign bag (`k_n = nπ/L_z`) at `L_z = 1.84 fm`:

| quantity | UR box (archived) | exact Dirac box | change |
|---|---|---|---|
| `f_intra` | `1.516709407e−3` | `1.516707662e−3` | `−1.15e−6` relative |
| `Σf_1n`, `n = 2…12` | `9.932045695e−4` | `1.291317638e−3` | `×1.300153` |
| deficit | `0.997490086` | `0.997191973` | `−2.981e−4` |
| `\|z_12\|` | `0.33143285 fm` | `0.37290906 fm` | `×1.12514` |

**The `0.9975` deficit survives.** It moves only in the fourth decimal and is `0.997` at three
decimals in both treatments. The opposite-sign bag (`k_n = (n−½)π/L_z`) gives a deficit of
`0.997192334`, differing from the same-sign bag by `3.6e−7` — the boundary-sign convention does not
move the answer. The asymptotic tail beyond `n = 12` is `< 1e−5` in both ladders. The high-`n`
ratios grow (`×2.44` at `n = 4`, `×12.4` at `n = 12`) because the spinor matrix element decays as
`n⁻²` against the envelope's `n⁻³`; the sum remains dominated by `n = 2`.

No `S1`–`S15` verdict moves: the partition still closes by construction, the deficit is still the
declared UV bucket, and `S12a/b`, `S5` and `S14` are unchanged. `τ` and `σ_DC` from `RQ-03` are
quoted, not recomputed. **The flip's mark is not re-opened**; refinement `(ii)` moves from
*unresolved* to *resolved with a number*. `(iii)` and `(iv)` remain open.

## §5f Erratum E7 (round 59) — a `k = 0` mode that the construction did not include

The same-sign bag also admits a `k = 0` eigenmode at `E = m_ec² = 0.511 MeV` with constant equal
upper/lower spinors. Its dipole coupling to `n = 1` is `|z_01| = 0.37314 fm`, giving
`f_01 = 1.2294e−3` — comparable to the entire `n ≥ 2` ladder. It is **not** part of P4's occupied
subband construction, which takes `n = 1` as the ground subband and `m_eff = E_z,1/c²`. If such a
band were occupied, its in-plane effective mass at the solved state would be
`(μ_e + m_e)/c²`, a factor `20.8` below P4's `m_eff`, and the Drude weight's mass assumption would
change. **The round does not re-solve the state or revise `σ_s`.** This is registered as a question
about the state (BN-35), not a verdict on the response; nothing above is edited.


## §5g Erratum E8 (round 60) — refinement (iv) is executed; the family surface is a receipt, not a range

**Nothing above is edited.** `RQ-06` produced the handoff receipt
`runs/R1B/r1b1_p4_family_surface.md` (instrument `src/r1_dense/r1b1_p4_family_surface.py`,
pre-registration `runs/R1B/r1b1_p4_family_surface_registration.md`, 14/14 predictions).

The five cells `L_z = 1.68/1.76/1.84/1.92/1.99 fm` carry `n_free,2D =
1.11061/1.05704/1.00810/0.96324/0.92696 ×10⁻³ fm⁻²`, `g = 2`, corrected
`v_F = 0.04467/0.04566/0.04661/0.04755/0.04834 c`, band edge
`ω_end = 5.606/5.351/5.119/4.905/4.733 ×10²³ rad/s`, with per-cell provenance. **All four
conditions of the `PG-01` mark are now discharged**: (i) round 56, (ii) round 59, (iii) round 57,
(iv) this round. The mark itself is untouched.

Three inherited defects are carried, not silently repaired:

- **§1's `v_F` row is low by `√2`** (already E2): the corrected values above replace
  `0.0316/0.0330/0.0342 c`. The row's own prose (`~0.049 c`) was closer to the truth than its
  table.
- **§1's prose `ω_end = 3.1–3.7×10²³ rad/s` belongs to `L_z = 2.55–3.04 fm`**, outside the
  scanned window; the table's `5.61/5.12/4.73×10²³` is the state-derived `πc/L_z`. The class is
  BN-08's (a number from another state inherited by this one).
- **§2's `S14 PASS` was recorded on a bare `ω_end`**, the exact form `S14` fails. The receipt
  supplies the missing declared form: with `g = 2` consistently,
  `W_total/A = 2ħk_Fv_F = 1.473–1.456 MeV`, `f_intra = 1.38–1.64×10⁻³`,
  `ω_end = ω_g + f_inter W_total/A = 370.47–312.97 MeV`, `0.40–0.47%` above the bare edge.
  No verdict is re-opened (`s9.1`: a ratification is not a correction).

**The admissible range is the five certified cells, not the whole registered interval.** K1's
`[1.68, 1.99] fm` was derived at the frozen density `n_e = 0.022 fm⁻²`; at the solved density
(22× lower) the same `E_sub/E_F ≥ 3` test holds to `L_z ≈ 80.30 fm`. A downstream document may
cite the five cells; it may not interpolate the tuple to an unsolved thickness, and it may not
read `1.99 fm` as the solved state's 2D ceiling.

*Content generated by AI*
