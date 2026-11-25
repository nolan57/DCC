# Audit registration — A.6 effective-dimensionality claim

**Registered**: 2026-11-22, before `src/route/eff_dim_audit.py` exists.
**Subject**: the submitted `A.6 Effective-Dimensionality Claim` (proposed to replace the blanket "no claim that
the state is two-dimensional").
**Question put to the executor**: should the freeze-out energy and the effective-2D condition be copied into the
body of the route document?

---

## 0. What is already known, and what is therefore not blind

**Disclosure.** To decide whether the submission deserved a registration at all — as opposed to a one-line
reply — I ran the four-cell arithmetic by hand first:

```
E1 = c/L with the constant chosen among {hbar*c, h*c, pi*hbar*c} and L in {0.215 nm, 0.4307 nm}
```

That arithmetic is reproduced in §2 below as `step 0`. **Consequence: `P1` and `P2` are not predictions.** They are
confirmations of a hand calculation I had already done. Only `P3`–`P8` are blind, and the round will be scored on
those. Registering this openly is more useful than pretending the numbers were unseen — the same class of
disclosure as the `9e20`/`9e14` slip, the `√2` span bound and the unreproducible `0.119`.

The finding is not a prediction in any case: it is a defect that follows from arithmetic anyone can repeat, and the
registration exists to fix **before the code runs** what the code must reproduce, and to separate the parts I
tested from the parts I asserted.

## 1. Facts to be taken from the record, not recomputed

| Fact | Source |
| --- | --- |
| atomic layer spacing `δ = 0.215 nm` | `front_sweep_v1.md` §2 (peels one atomic layer, 0.215 nm) |
| layers `8.12e9`, components/layer `1.457`, plates `1.18e10` | `front_sweep_v1.md` §2; census FROZEN by `gd_rulings_v1.md` |
| array side `90126`, plate spacing `0.4001 m` | `front_sweep_v1.md` §1; reproduced by `front_sweep_frame.py` |
| body height `1.738 m` | `front_sweep_v1.md` §1 |
| `ΔE_z = πħc/L_z` under Model B; Model C is compactification | `effective_2d_definition_v1.md` §2.2 |
| four slots: model, subsystem, `E_occ = max(E_F,k_BT)`, `E_probe` | `effective_2d_definition_v1.md` §1 |
| **two bounds must not be combined into one number; `E ≤ X` must say which bound `X` is** | `effective_2d_definition_v1.md` §3 |
| registered `E_F`: `73.37` / `21.54` / `6.73 MeV` for the three states | `effective_2d_definition_v1.md` §4 |
| `ME4` certifies only "no handles created" | `meff_boundary_v0_2.md` §2 clause 3 |

## 2. Predictions

| # | Prediction | Why | Blind? |
| --- | --- | --- | --- |
| `P1` | A.6's **written** formula `ħc/H_eff` evaluated at A.6's **written** `H_eff = 0.4307 nm` yields `458 eV`, not `2.9 keV`; the ratio is `2π` to `<0.5%` | `ħc` vs `hc` — the symbol and the number disagree by `2π` | **no (step 0)** |
| `P2` | `2.9 keV` is reproduced **only** by `(hc, 0.4307 nm)` or `(πħc, 0.215 nm)`, each to `<1%` | two compensating errors: `δ` doubled, `ħ` dropped | **no (step 0)** |
| `P3` | `k_max(E_1(k)) = k` **identically** for every `k` swept over `[0.1, 1e4]`, to `<1e-12` relative | `k_max = (ħc/E)/δ` and `E_1(k) = ħc/(kδ)` ⇒ the composition is `id` by construction | yes |
| `P4` | registered `N = 1.738/0.215 nm = 8.08e9`, so A.6's `4.04e9` is low by a factor `2.00` to `<0.5%`, and A.6's `δ` high by the same factor | both off by 2, product preserved — invisible in `Nδ = H` | yes |
| `P5` | plates per site `= 1.18e10/90126² = 1.45`, so `k = 1` is **not** the rendered configuration; `k = 1` would require an array of side `1.09e5`, not `90126` | frozen census | yes |
| `P6` | the four-slot test fills **at most 2 of 4** slots (model ambiguous, subsystem absent, `E_occ` absent, `E_probe` present) | §1 of the mandatory convention | yes |
| `P7` | the internal bound `E_F < ΔE_z` **fails** at `ΔE_z = 2.9 keV` by `>1e3` for all three registered `E_F`; so the claim is external-only and "is a 2D system" is false | §3: the internal bound is the tight one (`L_z ≲ 2 fm` vs `250 nm`) | yes |
| `P8` | `2.9 keV` is unaffected (`<1%`) when the two errors are corrected jointly, i.e. the number is stable while both of its inputs are wrong | that is what compensating errors do | yes |

**Falsifiers.** If `P3` fails — i.e. `k_max(E_1(k)) ≠ k` for some `k` — then the "self-consistent point" is a real
selection principle and my central finding is wrong. If `P7` shows the internal bound holds, then the claim is
admissible as written and only the formula needs correcting. Both would change the verdict, not just the wording.

## 3. What the run must decide

Three verdicts, each with a default that is the *unhelpful* one so that passing means something:

1. **Home**: does A.6 belong in the route body (`R1`), in the mandatory convention (`effective_2d_definition_v1`),
   or nowhere? Default: nowhere, unless it survives (2) and (3).
2. **Formula**: is there a single `(constant, L)` pair consistent with all of A.6's own statements? Default: no.
3. **Claim class**: is the surviving statement *measured*, *declared*, or *unfalsifiable at the project's own probe
   energies*? Default: declared. `E_probe` at `2.25 eV` and `284 eV` will be tested against `ΔE_z`.

## 4. Non-claims of this audit

- It does not re-derive `H_eff` from any simulation; `H_eff` is a *declared design parameter* of the render and
  stays one.
- It does not touch the frozen `ME4`, `MR1`, or any threshold in `TIER-LOCK`.
- It does not rule on `GD9` (`FL` objective) or `GD6` (`φ` in `ME3`); both remain open and unrelated.
