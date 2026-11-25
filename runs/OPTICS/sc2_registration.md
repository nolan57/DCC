# Registration — `SC-2`: lineshape, provenance, and the `τ` obligation, 2026-11-22

**Rule.** Predictions are fixed before any measurement in this round. A prediction that fails is reported as
failed and stays in the results file. No threshold is widened after a number is seen.

**What this round is.** The governor accepted `PARTIALLY ADOPTED` (`docs/decisions/sc_route_ruling_v1.md`) and
returned four sharpenings. Two of them are *new constraints*, not restatements, and neither has been tested
against the record's module:

| governor's point | what it adds | test here |
|---|---|---|
| `FSUM-SPLIT` is a budget duplication, **and** the total weight must come from the actual Hamiltonian and its current operator — f-sum formulas from different models may not be spliced | `FSUM-SINGLE-SOURCE` | §A |
| a step's KK partner is a `ln` singularity; the **line shape** must acquire threshold broadening *and* high-frequency decay, then KK must be re-verified | `KK-LINESHAPE`, `FSUM-FINITE` | §B |
| Kubo does not guarantee a unique scalar `τ`; a single-Drude reduction must be *proved* valid, else the full current response must be computed; `τ` may not be scanned, and must trace to a scattering mechanism or a pole width | `DRUDE-DOMAIN`, `TAU-KIND` | §C |
| do not bypass `R1-B1`; a null result ("no admissible matter state / no admissible response") is a valid physical conclusion | `NO-GO-ADMISSIBLE` (wording, not measurement) | ruling §4 |

Nothing in §A–§C requires `R1-B1`: every quantity is either an identity of the model already in the record, or a
property of a test instrument that must be validated *before* a candidate exists. That is the point — the tests
can be built now, the object cannot.

**Instruments are validated before they are applied.** Each quadrature is first run on a response whose closed
form is known (Drude for the KK round-trip, an exact Cole–Cole locus for `α`), and the validation residual is
printed next to the result. Round 36's KK kernel (`src/optics/sc_route_check.py`, `kk_im`) is reused verbatim so
that the residual reported here is comparable with `S4` there.

---

## §A Provenance of the spectral weight (`FSUM-SINGLE-SOURCE`)

| id | prediction | falsified by |
|----|-----------|--------------|
| **P1** | `∫₀^∞ Re σ_Drude dω = πσ₀/(2τ) = πe²n_2D/(2m*)` **identically, at every `τ`** — so `FSUM-SPLIT` is a theorem about the Drude pole, not a defect in the code. Ratio to `W_total` is `1` within `1e-12` at all three scanned `τ`. | any ratio off by more than `1e-12` |
| **P2** | The record's `W_total` is not a property of the material but a function of the degeneracy convention: `W_total(g) = (e²v_F/8ħ)·√(4πng)`, so at fixed `n_2D`, `g=4` gives `W_total` larger by `√2` and `E_F` smaller by `√2`. The module's `k_F = √(2πn)` **fixes `g = 2`**. | `W(4)/W(2) ≠ √2` |
| **P3** | `A_INTER = e²/(16ħ)` equals `σ_min/4` with `σ_min = e²/(4ħ)`, ratio `0.25` to `<1e-15`. It has dimension **S**, so it cannot carry a weight *fraction*; the factor `1/4` is underived. | ratio ≠ 1/4, or a dimension statement that lets S carry a fraction |
| **P4** | A step of height `A` terminated at `Ω` carries `W_inter = A(Ω−ω_g)`; the termination at which it would consume the **whole** budget is `Ω* = ω_g + W_total/A_INTER` and is `< 4.5e8 eV`. | `Ω* ≥ 4.5e8 eV` |

## §B Lineshape (`KK-LINESHAPE`, `FSUM-FINITE`)

| id | prediction | falsified by |
|----|-----------|--------------|
| **P5** | The step's KK partner is exactly `−(A/π)ln|(ω_g+ω)/(ω_g−ω)|`; the residual reported as `S4` in round 36 reproduces at `1.5e8 eV` as `1.153 ± 0.005`. | residual outside that band |
| **P6** | Lorentzian broadening of the threshold does **not** bound the interband weight: for `Γ/ω_g ∈ {1e-3, 1e-2, 1e-1}`, `W_inter(Ω)/W_total` still grows without bound in `Ω` and exceeds `1` at `Ω = 10ω_g`. | any `Γ` for which the ratio saturates |
| **P7** | A Lorentz **oscillator** has finite weight `π n_j e²/(2m*)`, an exact causal partner, and a KK round-trip residual `< 1e-6` over five decades. | round-trip worse than `1e-6` |
| **P8** | Composite: band-limiting closes `S4` **and** `S5`; broadening alone closes neither; rescaling the amplitude alone closes neither. | any single-parameter repair that closes both without a band edge |

## §C The `τ` instrument (`DRUDE-DOMAIN`, `TAU-KIND`)

| id | prediction | falsified by |
|----|-----------|--------------|
| **P9** | A single-pole diagnostic exists that needs no fitting: at the frequency of peak `−Im σ`, a Cole–Cole response `σ₀/(1+(iωτ)^α)` satisfies `α = (4/π)·arctan(−Im σ/Re σ)`. Recovers `α = 1` to `<1e-12` and `α = 0.7` to `<1e-9`. | recovery error above those |
| **P10** | The same diagnostic **discriminates** multi-mode relaxation: an equal-weight two-pole sum with `τ₂ = 3τ₁` returns `α_eff < 0.9` and a maximum radial deviation from the single arc `> 1e-2`. | `α_eff ≥ 0.9` or deviation `< 1e-2` |
| **P11** | `τ` is not one number. For a static Thomas–Fermi 2D Coulomb kernel `|V(q)|² ∝ (q+q_TF)^{-2}`, `τ_tr/τ_sp` is monotone decreasing in `a = q_TF/(2k_F)`, tends to `1`, and follows `τ_tr/τ_sp → (2/π)(1/a)` as `a → 0`. | deviation from that law `> 5%` at `a = 1e-3` or `1e-4`, or non-monotone |

> **`P11` amended before measurement.** As first written it asserted "exceeds `100` at the record's screening".
> That number was an estimate I had not evaluated, and the asymptotic constant is `2/π ≈ 0.637`, not `1` — so
> the estimate was already known to be doubtful. The claim is replaced by the asymptotic law itself, which is
> what §C needs (the *scaling*, not a round number), and the value at the record's screening is reported rather
> than thresholded. Amended 2026-11-22, before the script was run.
| **P12** | The locked spec (`surface_conductivity_v1.md`, `S1`–`S9`) never asks **which** `τ` (single-particle / transport / optical): count of `transport` = `0`. | count `≥ 1` |

`P11` is stated against the *record's* screening parameter, and its number is a property of the model, not of the
material: the static-TF kernel is itself an approximation with no dynamic screening and no vertex correction. The
number is therefore reported with its model attached, and what it establishes is only the *magnitude* of the
ambiguity, not the value of either `τ`.

---

## Scope rule

Text checks are scoped to `docs/specs/` + `docs/conventions/` (the speaker). `docs/decisions/` is commentary and is
excluded, because rulings quote rejected phrases while rejecting them (rule established round 31, after `A3`
false-FAILed on my own quotation).

*Content generated by AI*
