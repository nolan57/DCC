# SC-3 — Registration (locked before measurement)

**Round**: 38. **Date**: 2026-11-22. **Predecessor**: `sc2_registration.md`, `sc2_results.txt`,
`docs/decisions/sc2_lineshape_ruling_v1.md`, spec v1.1 `a005533b…`.
**Trigger**: governor's mathematical review of SC-2. It accepts `STEP-NO-SCALE`, accepts the `g = 2`
implication, accepts the two weight ratios, accepts broadening's failure, and then imposes five
sharpenings. Every sharpening is turned into a test below, before any number is computed.

**Standing rule inherited from rounds 36–37**: a proposition is admissible only if the text it corrects
can be cited by file and line in `docs/specs|conventions|roadmap`. If it cannot, the finding is
`REPAIR-ABSENT` and is recorded as such, not silently dropped.

---

## 1. What the governor actually asserts

| # | Assertion | Type |
|---|---|---|
| **S-a** | `STEP-NO-SCALE` is a structural defect; broadening cannot make the weight converge while `Reσ → A`. | physics (already measured in SC-2, re-tested) |
| **S-b** | One root, **two independent acceptance results**. Fixing one symptom must not be taken to imply the other. | specification |
| **S-c** | "Spectral weight depends on the degeneracy" is imprecise: `W = W(n_2D, g, v_F)`. Only *at fixed `n, v_F`* is the `√g` law meaningful. | wording → measurable |
| **S-d** | `A_INTER = e²/(16ħ)` is the **single-channel** Dirac scale; if the model carries `g`, the relation `A_INTER(g)` must be stated, not assumed. | physics |
| **S-e** | `440.18 MeV` is an **upper bound**, and the budget definition (`W_total` vs `W_total − W_intra`) and the `ħ`/unit convention must be fixed before it means anything. | arithmetic + convention |
| **S-f** | `α` is a diagnostic, not a uniqueness proof — one number cannot certify a single pole. `τ_tr/τ_sp = 91.5` is model-dependent. | logic + model |
| **S-g** | `(n_2D, g, v_F, ω_end)` are **necessary but not sufficient**; scattering, vertex corrections, the current operator and matrix elements still decide `σ_s`. | interface |

---

## 2. Predictions (P1–P14), thresholds fixed now

Numbering continues the run-level series; `P` ids are local to SC-3 and are prefixed `Q` where they
would collide with SC-2's `P1–P12` in the results file.

| id | claim | pass condition |
|---|---|---|
| **Q1** | `Ω* = ω_g + W_total/A_INTER` reproduces the ruling's `440.18 MeV`, and `Ω*(f_inter = 0) = ω_g` exactly. | `|Ω*_eV − 4.4018e8| < 4.4e3` eV **and** `|Ω*(0)/ω_g − 1| < 1e-15` |
| **Q2** | The ruling's ceiling already assumes `f_intra = 0`. Under the module's own partition (`FSUM-SPLIT`: `W_intra = W_total`) the residual interband budget is **exactly zero**, so no interband term is admissible at any `ω_end > ω_g`. | `|f_inter| < 1e-15` **and** `slack/W_total < 1e-15` |
| **Q3** | `W_total/A` is a **rad/s**; reading it as an energy is wrong by `1/ħ = 1.5193e15`. The convention is not a rounding matter. | measured ratio `/ (1/ħ_eV)` within `1e-12` |
| **Q4** | `W` does **not** determine `g`: `W(4n, g) = W(n, 4g)` exactly, while `E_F` splits by `4`. The budget fixes only the product `n·g`. | equality to `1e-15`, `E_F` ratio `= 4 ± 1e-9` |
| **Q5** | The module carries **two different `g`**: `k_F = √(2πn)` fixes `g = 2`; `A_INTER = (1/4)σ_min` is the `g = 1` single-cone height. Required height at `g = 2` is `2×`. | ratio `= 2.000000000000` |
| **Q6** | The record's `(n_2D, E_F)` pair, read as a Dirac model, implies `v_F = E_F/(ħk_F) ≈ 0.993 c`. With `v_F = c/300` the same `n_2D` gives `E_F ≈ 0.25 MeV` and the whole ceiling scales by `v_F`, i.e. by `~1/298`. | `v_F/c` within `2e-3` of the prediction; ceiling ratio `= v_F/c` to `1e-3` |
| **Q7** | `S4` and `S5` are **independent**: all four cells of the 2×2 are populated by explicit responses. | four cells, each with the named verdict |
| **Q8** | `α = 1` at a **single** frequency is achievable by a two-pole response ⇒ it is not a certificate. | root of `α−1` found to `1e-12` |
| **Q9** | At the **peak of `−Imσ`**, `α < 1` strictly for any non-degenerate two-pole sum, monotone toward `1` as `τ₂/τ₁ → 1`; `α(3:1) = 0.9087` reproduces. | monotone within `1e-3`; `α ≤ 0.9995` for `τ₂/τ₁ ≥ 1.05` |
| **Q10** | **Constancy** is the sufficient statistic: `max_ω |α−1| ≥ 0.05` for the two-pole vs `< 1e-13` for one pole, at the same `α`-at-peak. | both inequalities |
| **Q11** | `(n, g, v_F, ω_end)` does not determine `σ_s`: two responses with an identical four-tuple, both passing `S4` and `S5`, differ in `α` by `≥ 0.4`. | both pass; `|Δα| ≥ 0.4` |
| **Q12** | Acceptance ≠ identification: an entire `(ω_0, Γ)` grid of Lorentz oscillators at one fixed `S_p` passes `S4` and `S5`. | `100%` of a `6×5` grid passes both |
| **Q13** | `91.5` is model-dependent: replacing the Thomas–Fermi kernel `(q+q_TF)⁻²` with `(q²+q_TF²)⁻¹` moves `τ_tr/τ_sp` by `> 20%`. | relative shift `> 0.20` |
| **Q14** | Spec v1.1 declares the `ω`-unit convention for the f-sum **zero** times, and the ruling's §2.4 sentence "must be cut off below 440 MeV" is true but **not tight**. | count `rad/s` in spec `= 0`; tight bound computed and shown `< 440.18` |

**Kill conditions.** If Q7 shows only three cells populated, the independence claim is weaker than the
governor supposes and the spec must say "S5 ⇒ not-S4 unless…" instead. If Q6 shows `v_F/c = 1.000` rather
than `0.993`, the record's convention is `v_F = c` exactly and the sentence becomes simpler, not weaker.

---

## 3. What this round does not do

- It produces no `σ_s`. Every object below is a test of a criterion, not a candidate response.
- It does not decide `f_intra`. That is `R1-B1`'s job, and Q2 shows why it cannot be guessed: at `f_intra = 1`
  the optics stage is empty.
- It makes no visibility claim, and no statement about `G6`.
- No threshold above may be widened after a measurement. A miss is archived as a miss.
