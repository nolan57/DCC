# Registration — `RQ-03`, the finite `τ` (refinement (i) of `S7`)

**Written**: 2026-11-23, before `src/r1_dense/r1b1_p4_tau.py` existed.
**Question** (`round_queue_v1.json` `RQ-03`): *what is the finite relaxation rate at the solved state, and does it
leave the Drude-domain reduction (`S12a/b`) intact?*
**DoD**: `τ` with its mechanism and matrix elements; `S13` provenance (not a scan); the `α`-collapse test applied
with its blind spot quoted.
**Source**: `runs/R1B/r1b1_p4_p5_closure_v1.md` §1 (`τ = ∞` at the declared ideal level; mechanism declared,
value named as refinement); `docs/specs/surface_conductivity_v1.md` §5 `S7`, §8 (`TAU-OBLIGATION`),
§10 `S12a`, `S12b`, `S13`.
**Product**: `runs/R1B/r1b1_p4_tau_results.txt` (emitted by the program, not transcribed).

---

## 1. What is being fixed, and what would make the answer vacuous

`S7` says a `τ` must be **solved**, not scanned. `S13` says it must be **named**, **traced**, and **not scanned**.
Round 45 delivered the mechanism's name (`e–p impurity scattering`, `X_p ≈ 2.4e-2`) and no number. A name is not a
rate: the round fails if the number comes from anywhere but the state's own tuple.

Three ways this round can be vacuous, each stated in advance so it cannot be discovered late:

| failure mode | what it would look like | what the round does then |
| --- | --- | --- |
| **circularity** | `τ` chosen so that `σ_DC` matches a number the record already likes | no target exists — nothing in the record fixes `σ_DC`, so there is nothing to fit |
| **hidden parameter** | the rate comes out of a quantity not in the state (a fitted screening length, a fitted impurity potential) | every input is printed with its source; the only external number is `α` |
| **premise laundering** | the mechanism is declared "active" although the state contains nothing for it to scatter off | §4 lists the premise as a premise and prices what happens without it |

The third is the one this round expects to matter, and it is not an accident of this material: a *uniform* electron
and proton fluid has no elastic channel at all, because `e–p` scattering conserves the total momentum. A finite
`τ` therefore requires the protons to be **localized** (and, for a finite elastic rate, **disordered**). The ideal
`P2` state is a fluid with no lattice. So the number below is conditional on one structural premise, and §4
computes what the alternatives cost.

---

## 2. Inputs, all from the record or from a registered definition

| input | value (at `L_z = 1.84 fm`) | source |
| --- | --- | --- |
| `n_free,2D` | `1.0081e-3 fm⁻²` | `runs/R1B/r1b1_p2_eos_scan_results.txt` (HYB, `P2` 9/9 PASS) |
| `m_eff` | `E_z,1/c² = πħc/(L_z c²) = 336.9 MeV/c²` | `r1b1_p4_response.py`; the model's own in-plane mass |
| `k_F` | `sqrt(4π n/g)`, `g = 2` → **`0.0796 fm⁻¹`** | `conv.kF_2` (the *registered* definition, `n = g k²/4π`) |
| `v_F` | `ħk_F/m_eff = 0.0466 c` | derived |
| `E_F` | `ħc k_F = 15.70 MeV` | derived; cross-checked against `conv.eos_e_2D` |
| `n_imp` | `= n_free,2D` **identically** (charge neutrality: one proton per electron, `N7-SPLIT`) | `conv.beta_eq`: `n_e_areal = X_p N_B` |
| `X_p` envelope | `[1.62e-3, 4.50e-2]` at `L_z = 1 fm`; recomputed at `1.84 fm` | `runs/ANALYSIS/internal_consistency_v1.txt`; `conv.beta_envelope` |
| `α` | `1/137.036` | registered constant; the only external number used |
| `ε` | `1` (no bound electrons in the layer — declared, not fitted) | this document |
| impurity charge | `Z = 1` (protons are the only positive charge) | `N7-SPLIT` |

**Why `k_F` is taken from `conv.kF_2` and not from the `P4-1` table.** The `P4-1` table prints
`k_F = 0.0563 fm⁻¹` via `sqrt(2πn/g)` — i.e. `sqrt(πn)` — while the registered definition and `conv.kF_2` give
`sqrt(4πn/g) = sqrt(2πn) = 0.0796 fm⁻¹`. The two differ by `√2`, and the `P4` prose already prints `v_F ≈ 0.049 c`
(the corrected value, to its rounding) against a table that prints `0.0330 c`. Prediction `P11` measures this.
The round therefore prints **both** `τ`'s (corrected `k_F`, and the table's `k_F`) rather than silently correcting
a product it does not own.

**The model.** A 2D electron gas in the lowest subband, parabolic with `m_eff`, scattering elastically at `T = 0`
from a random array of unscreened-by-anything-but-electrons Coulomb impurities confined to the same plane:

```
V(q) = 2π e² / (ε (q + q_TF)),     q_TF = 2 m_eff e²/(ε ħ²) = 2 α (m_eff c/ħ)
1/τ_sp = (n_imp m_eff/ħ³) ⟨|V|²⟩_θ                     (quantum lifetime)
1/τ_tr = (n_imp m_eff/ħ³) ⟨|V|² (1 − cos θ)⟩_θ          (transport = the Drude rate)
q = 2 k_F sin(θ/2)
```

`e–e` scattering is excluded from `τ_tr` by momentum conservation in a parabolic band (it contributes to `τ_sp`
only); `e–n` scattering is excluded because the neutron is neutral at this level. The finite-width correction is
computed, not assumed (`P12`).

**Reduction to three integrals**, with `x = q_TF/(2k_F)`:

```
J0(x) = ∫₀^π du /(sin u + x)²,     K1(x) = ∫₀^π du /(sin u + x),     J2 = π − 2x·K1 + x²·J0
1/τ_sp = A·J0/(4πk_F²),   1/τ_tr = A·J2/(2πk_F²),   A = (n_imp m_eff/ħ³)(e²/2ε₀ε)²
τ_tr/τ_sp = J0/(2 J2)        [1/(2 J2/J0) — see the note below]
```

> **Note, added before the product was emitted.** The identity was first written inverted
> (`2 J2/J0`), which is the *rate* ratio `1/τ_tr ÷ 1/τ_sp`, not the time ratio. Corrected here; no
> prediction, bar or decision rule changes, and `P4`'s bar (`< 10`) is stated on the time ratio in
> both versions.

---

## 3. Predictions, with bars fixed before the code

| # | prediction | bar |
| --- | --- | --- |
| `P0` | the integral kernel is right: `J0(1) = 4/3` analytically | `|J0(1)·3/4 − 1| < 1e-9` |
| `P1` | the screening ratio is the interaction strength: `q_TF/k_F = 2 r_s` identically | `|ratio − 1| < 1e-12` |
| `P2` | the state is weakly-to-marginally coupled, so Born is admissible with a stated error | `r_s ∈ [0.14, 0.18]` |
| `P3` | the transport rate is finite and fast | `τ_tr ∈ [3e-21, 3e-20] s` |
| `P4` | the `τ_sp`/`τ_tr` ambiguity is **small at this state**, unlike the record's quoted illustration | `τ_tr/τ_sp < 10` |
| `P5` | the criterion's `91.5` is **not** reproducible at the `q_TF/k_F` it cites: the same integral gives `45.8`, and `91.5` is the value at ≈ half that argument | `computed/91.5 ∈ [0.45, 0.55]` **and** the argument ratio `∈ [0.40, 0.60]` |
| `P6` | the impurity width sits far below the inter-subband gap, so the intra pole stays a separate pole | `ħ/τ_tr ∈ [20, 120] keV` **and** `γ/ω_12 < 1e-3` |
| `P7` | the DC sheet conductance is small but finite | `σ_DC ∈ [1e-4, 1e-2] S` |
| `P8` | `S12b` passes exactly, **and is blind to the identity of the rate**: `κ` is the same to `1e-12` for `τ_tr` and `τ_sp` while `σ_DC` differs by `> 2` | `κ < 1e-14`; `|κ_tr − κ_sp| < 1e-12`; `σ_tr/σ_sp > 2` |
| `P9` | the statistic itself works: the two-pole `3:1` control fails it | `κ_control ∈ [0.05, 0.15]` |
| `P10` | the f-sum is `τ`-independent, so `S5` cannot catch a wrong `τ` either | `|W(τ_tr)/W(τ_sp) − 1| < 1e-9` |
| `P11` | the `P4-1` table's `k_F` is low by exactly `√2` | `|k_F(table)/k_F(conv) − 2^(−1/2)| < 1e-6` |
| `P12` | the 2D reduction is safe: the finite-width form factor is negligible at `2k_F` | `1 − F(2k_F) < 0.01` |
| `P13` | the impurity average is admissible: the electron passes many impurities per collision | `k_F ℓ > 10` |
| `P14` | the prefactor is right (convention check, order of magnitude): a spacerless GaAs 2DEG at `n = n_imp = 1e16 m⁻²`, `m* = 0.067 m_e`, `ε = 13` | `μ ∈ [1e2, 1e6] cm²/V·s` |
| `P15` | the `X_p` convention envelope **cancels** in `τ`, because the scatterers are the carriers | `max/min τ over ALL3D/HYB/ALL2D < 1.5` while `X_p` spans `28×` |

**Decision rules, fixed now.**

- If `P3` holds → `RQ-03` is `CLOSED-CONSTRUCTIVE`: a finite, named, traced rate exists, and `S7`'s conditional
  becomes a number with a premise. If `P3` fails high (`τ > 1e-19 s`) the state is in the clean limit and the
  question moves to the boundary; if it fails low (`τ < 1e-21 s`) the mean free path falls below the impurity
  spacing and the impurity average is not admissible — `BLOCKED-ON-INPUT`.
- If `P4` fails (ratio `> 10`) the round must say that `S13`'s "which `τ`" is the dominant error and that no
  number may be quoted without its name — a stronger conclusion than the number itself.
- If `P5` fails in the *other* direction (`91.5` reproduced at the stated argument) the record's illustration
  stands and the round says so; the solved-state ratio is unaffected either way.
- If `P8` holds → the blind spot is recorded as a **coverage** statement: `S12` certifies *one* rate, `S13`
  certifies *which*, and `S12` cannot do `S13`'s work. `S13` is binary, so a wrong-but-unique rate passes every
  machine-checkable criterion; the guard has to be the derivation.
- If `P11` holds → an erratum is appended to the closure document (the table is a product; `§9.1` forbids
  rewriting it) and `τ` is quoted with the corrected `k_F`, with the table's value printed as a sensitivity.

---

## 4. The premises, named before the numbers

| premise | status | what happens without it |
| --- | --- | --- |
| **Q-1** the protons are **localized** (a static scatterer array, not a co-moving fluid) | *not* in the `P2` state | `τ = ∞`: `e–p` scattering conserves the total `e+p` momentum, so it relaxes no current |
| **Q-2** the array is **disordered** (Poisson), not a perfect lattice | *not* in the `P2` state | `τ = ∞`: a periodic array gives Bloch states and no elastic channel below the first reciprocal vector (`2k_F < G_min`, computed) |
| **Q-3** `Z_imp = 1`, `ε = 1`, `T = 0`, single occupied subband | declared in the `P1`/`P2` model | each is printed with its sensitivity where it has one |

`Q-1` and `Q-2` are the *content* of `S7` here: the mechanism named in round 45 is a mechanism only for a
structure that round 45 did not have. That is not a defect of this round; it is why `S7` was conditional.

---

## 5. What this round does not do

No visibility statement (`S9`), no `σ_s` re-admission, no threshold moved, no rung re-priced, no gate re-marked.
It does not re-derive `m_eff` (the model's own identification `m_eff = E_z,1/c²` is taken as the state's) and it
does not decide `Q-1`/`Q-2` — those are refinement (iii)'s census, `RQ-05`, and the product says so rather than
assuming an answer. `S7` and `S13` are *applied*, not re-defined; if the application conflicts with the criterion's
text, the text wins and the conflict is reported.

---

*Content generated by AI*
