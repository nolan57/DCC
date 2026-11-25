# Registration — adjudication of the proposed `§4.5.1` / `T4` insertion (H_eff ≥ δ)

**Written**: 2026-11-22, **before** `src/route/t4_floor_check.py` existed.
**Subject**: a second submission proposing to insert (A) a `§4.5.1 Lower Bound on H_eff` between the `k_max` table
and the "self-consistent point" paragraph of `R1`'s §4.5, and (B) a fifth tier `T4 — Domain Boundary of the
Framework Itself` after `T3` in `R1`'s §7, plus three cross-reference edits.
**Status of the subject**: not a file in the record. It arrived as message text; it is registered verbatim in
`docs/decisions/t4_heff_floor_ruling_v1.md` §1 and is audited here.

**What this check is for.** The submission reuses four numbers from `A6` (`δ = 4.307e-10 m`, `N = 4.04e9`,
`E ≤ 2.9 keV`, `k = 1`) and adds three new ones (`k_max(ℓ_P) = 3.75e-26`, `V = 5.2e-37 m³`, `n = 5.2e-7`). The
first four were already found defective in `reports/reviews/eff_dim_claim_A6_v1_audit.md`. A repaired argument that
carries unrepaired numbers is the failure mode this check exists to catch, so every number is recomputed rather
than carried over.

---

## Predictions

Tolerances are stated here and are not to be widened after the run.

| # | Prediction | Tolerance |
| --- | --- | --- |
| `P1` | `ħc / δ_A6` (`δ = 4.307e-10 m`) is `458.2 eV`, so the printed equality `ħc/δ = 2.9 keV` is false | ±0.5 eV |
| `P2` | `2900 eV / (ħc/δ_A6) = 6.33`, i.e. `2π` to `0.8%` — the `ħ`/`h` conflation, unchanged from `A6` | ±0.02 |
| `P3` | the `δ` that makes `ħc/δ = 2.9 keV` is `68.0 pm`, requiring `N = 2.56e10`, i.e. `3.16×` the census layer count — so **no** `δ` compatible with `Nδ = H` yields `2.9 keV` from `ħc/δ` | ±0.2 pm, ±0.02e10 |
| `P4` | `k_max(ℓ_P) = ℓ_P/δ` is `3.75e-26` with `δ_A6` and `7.51e-26` with the registered `δ`; both `< 1` | ±2% |
| `P5` | `δ_reg / ℓ_P = 1.3e25`, confirming the submission's "25 orders of magnitude" | ±0.1 dex |
| `P6` | the Planck-regime arithmetic `V = 5.24e-37 m³`, `V/V_0 = 9.3e-36`, `n = 5.2e-7 atoms` is **correct** | ±2% |
| `P7` | `R1` contains **zero** occurrences of `k_max`, `H_eff`, `4.5.1`, or `T4` — so both insertion anchors are absent | exact 0 |
| `P8` | `R1` §4 contains **zero** numeric constants, so a quantitative `§4.5.1` would change the character of the section it enters | exact 0 |
| `P9` | Annex A's highest section is `A.5`, so the requested cross-reference target "annex_A §A.6" does not exist | exact |
| `P10` | Insertion A names **no** bound (`external` / `internal` / `Model B` absent), so it repeats the §3 violation | exact 0 |
| `P11` | Insertion B supplies **0 of 3** admission requirements (scene-referring definition / separation quantity / locked threshold) | exact 0 |
| `P12` | `k` is already registered as plates-per-cell `= 1.4527` in Annex B, so the submission's stacking `k = 1` is a symbol collision | confirmed |
| `P13` | the mechanism documents contain **zero** occurrences of stacking vocabulary (`stack`, `on top of`, `superposed`, `one per site`) | exact 0 |
| `P14` | `T4` is already in force as a reading rule (`MR1`), so Insertion B would give one label two unrelated meanings | confirmed |

**`P6` is the one prediction that gives the submission credit.** If the Planck arithmetic is right, the submission
is not incompetent — it has a correct new result wrapped in a defective old one, which is a different disposition
from `A6`.

---

## What would falsify the disposition

The disposition will be *reject the insertion, keep one statement* unless one of these holds:

- `P7` false (an anchor does exist) → the insertion is mechanically possible and the ruling narrows to arithmetic;
- `P11` ≥ 2 (Insertion B does supply an admission requirement) → `T4` may enter as a tier;
- `P2` ≥ 3 (the `2π` is not the mechanism) → the `458 eV` finding has another cause and needs re-derivation.

Each is reported as it lands, pass or fail.
