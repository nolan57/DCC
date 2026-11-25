# SC-4 — Partition-Citation Errata (`E5`), post-v1.2 audit

**Round**: 39 (SC-4). **Date**: 2026-11-22. **Trigger**: the governor's post-v1.2 audit directs one
prioritized arithmetic item — reconcile `W_intra/W_total = 1 − 7.1e-5` with "the residual budget is
strictly `0.000000e+00`", and do not write both figures into the specification simultaneously.
**Method**: every number below is copied from the product that measured it, cited by file and line
(the non-hash form of the `E4` rule). **Authority**: none; this document re-grades a citation and an
instrument, and retracts nothing else.

---

## 1. The finding

The sentence *"FSUM-SPLIT measured `W_intra/W_total = 1 − 7.1e-5`"* (`runs/OPTICS/sc3_results.txt:20`,
§A.2; `src/optics/sc3_budget_check.py:86`) is a **mis-citation**. FSUM-SPLIT never measured that ratio,
and no measurement of it exists in the record. The two figures carried side by side since v1.2 are two
different quantities from two different ledgers:

| figure | what it actually is | where measured |
|---|---|---|
| `W_intra/W_total = 1.000000000003` | **the partition**: the Drude pole's weight against the f-sum budget, at every `τ`; residual `−3e-12`, the instrument's floor | `runs/OPTICS/sc_route_results.txt:195-198` (§F, P15); again `runs/OPTICS/sc2_results.txt:12-19` (§A.1) at max rel dev `6.88e-15` |
| `7.1e-5` | **the `m*`/`E_F` double-pinning slack**: the module's `m*` is built from the logged `E_F = 73.37 MeV`, while `k_F` is built from `n_2D`, which gives `73.3648 MeV`; `(73.37 − 73.3648)/73.3648 = 7.087e-5` | `runs/OPTICS/sc2_results.txt:44-46` (§A.2, `W(2)/W_total = 1.000071`) |

The `7.1e-5` is one number with one meaning, and it appears wherever a quantity carries one or two
factors of the pinning slack: `v_F = 1.000071 c` (`sc3_results.txt` §B.3), `W(2)/W_total = 1.000071`
(`sc2` §A.2 — the module's weight against the weight rebuilt from `n_2D`: a *pinning* ratio, not an
intra/total partition), `1.000142 ≈ 2 × 7.1e-5` (`sc3` §B.3, rebuilt at `v_F = 1.000071 c`), and
`1.4e-4 ≈ 2 × 7.1e-5` in `Q15`'s `2.999717` away from `3`. None of these is a partition share.

## 2. The instrument defect behind the printed zero

`src/optics/sc3_budget_check.py:87-89` does not measure the residual; it sets it:

```python
f_intra_mod = 1.0
f_inter_mod = 1.0 - f_intra_mod
allowed = f_inter_mod * W_TOTAL
```

The registered kill condition (`runs/OPTICS/sc3_registration.md:37`, Q2: `|f_inter| < 1e-15` **and**
`slack/W_total < 1e-15`) was therefore tested against a constant and could never fail. Three
consequences, all recorded:

- The printed `residual budget = 0.000000e+00` is true **by construction**. As an identity-level
  statement it is nevertheless correct: the module writes the Drude pole directly with
  `σ₀ = e²n₂Dτ/m*`, so `∫₀^∞ Re σ dω = σ₀π/2τ = πe²n₂D/(2m*)` exactly — `W_intra = W_total`
  **identically** (`sc2_results.txt:16-23`, P1: "FSUM-SPLIT is an identity, not a numerical accident…
  the comparison is algebraic, not empirical"). The measured `1.000000000003` is the instrument's floor
  showing through, not a deviation of the model.
- The registered pass condition was unreachable by any instrument in the record: the best measured floor
  is `6.88e-15` (`sc2` §A.1) and the §F tail-corrected floor is `3e-12`. Had the script used the measured
  ratio, `|f_inter| = 3.0e-12 > 1e-15` and `slack/W_total = 3.0e-12 > 1e-15` — Q2 would have **missed**
  its own registered threshold. The hardcode converted a would-be registered miss into a printed pass.
- A scan of `sc3_budget_check.py` confirms `Q2` is the **only** SC-3 verdict whose pass inputs are
  constants; every other verdict tests computed quantities.

## 3. The governor's three reconciliation hypotheses

| # | hypothesis | verdict |
|---|---|---|
| 1 | `1 − 7.1e-5` is an approximation; the unrounded actual ratio is `1` | **holds, refined**: the partition ratio *is* exactly `1` — at identity level (`sc2` P1), never as a rounding of `7.1e-5`. The `7.1e-5` was never an approximation of this ratio; it is a different quantity |
| 2 | the two statements use different total weights or budget definitions | **holds, sharpened**: not two definitions of one budget but two different quantities — a parameter-pinning slack vs a partition residual |
| 3 | `f = 0` is not the residual interband spectral-weight fraction | **not needed**: `f_inter` in `ω_end(f) = ω_g + f·W_total/A` *is* the interband share of `W_total` (`sc3_budget_ruling_v1.md` §2.1); the `f = 0` endpoint `ω_g` is consistent with the measured partition to `3e-12` (edge shift `−3e-12 × W/A ≈ −0.9 meV`) |

Plus a fourth cause neither hypothesis covers: the printed zero was **set, not measured** (§2).

## 4. Re-grade

- **Q2's conclusion survives, and it is a strict mathematical conclusion**: under the module's own
  construction the residual budget is `0` *identically* (the module's pole takes the whole budget by
  definition), so no interband term is admissible at any `ω_end > ω_g` with any `A > 0`; the admissible
  edge is `ω_g`. The governor's arithmetic objection was the correct instinct — the two sentences as
  written could not both be measurements of one quantity — and the resolution is that only one of them
  (`0`) was ever about the partition, while `7.1e-5` was mis-cited from the pinning ledger.
- **The printed precision is retracted**: "HOLDS (`f_inter = 0 to 1e-15`)" claimed a precision no
  instrument in the record has; the registered `1e-15` threshold sits below the measured floor.
- **Unaffected**: the `3ω_g` identity (`Q15`), the `440.18 MeV` withdrawal and its prohibition
  (`THREE-OMEGA-G`), the `S14`/`S15` criterion texts (byte-identical through v1.3), the `f_intra` scan
  (`Q11`/`ALPHA-BLIND`), and the 2×2 (`Q7`/`FSUM-PAIR`).
- **The `R1-B1` obligation is unchanged**: `f_intra` must come from the matter model or an independent
  measurement; the optics criteria remain measured-blind to it.

## 5. Errata register — every carrier of the mis-citation

| site | text carried | disposition |
|---|---|---|
| `runs/OPTICS/sc3_results.txt:20` | "FSUM-SPLIT measured W_intra/W_total = 1 - 7.1e-5" | archived stdout immutable; **`E5` appended** to the product |
| `src/optics/sc3_budget_check.py:86-95` | same prose line; hardcoded `f_intra_mod = 1.0` | **repair required before any reuse**: read the measured ratio (cite `sc_route` §F) or re-measure it, test the kill condition against the measured value, and re-run only under a new pre-registration |
| `docs/decisions/sc3_budget_ruling_v1.md:82` (§2.2) | "`FSUM-SPLIT` measured `W_intra/W_total = 1 − 7.1e-5`" | **`E5` appended** |
| `docs/decisions/sc2_lineshape_ruling_v1.md:305` | same figure | **`E5` appended** |
| `docs/specs/surface_conductivity_v1.md:265` (§10a.2) | "record's own measured partition (`W_intra/W_total = 1 − 7.1e-5`, round 37)" | **corrected in place, v1.2 → v1.3**, relocked (`runs/OPTICS/surface_conductivity_lock_v1_3.json`); `S1`–`S15` byte-identical |
| `docs/conventions/symbol_registry.md` (`BUDGET-ENDPOINT`) | "the residual budget is `0.000000e+00`" (as a `1e-15` result) | **AMENDED SC-4** in place |
| `reports/DCC_research_progress_v1.md:335` (§7.3c) | same figure | corrected in place |
| `runs/OPTICS/sc3_registration.md:37` | "`FSUM-SPLIT`: `W_intra = W_total`" | **correct as written** — the error entered between registration and product |

## 6. Ledger

- **a threshold fixed before the instrument was calibrated** — instance 5: `Q2`'s `1e-15` was registered
  below the `6.88e-15` floor already measured in `sc2` §A.1 one round earlier.
- **a tautology reported as a test** — instance 2: `Q2`'s instrument tested a constant.
- **new class — a measured number quoted from the wrong measurement** — instance 1: the `7.1e-5` pinning
  slack quoted into the partition slot. Standing rule (the non-hash generalization of the `E4` rule):
  **every measured number is quoted with the product that measured it, by file and line; never
  paraphrased across ledgers.** A number quoted without its product is not evidence.
- Relation to `E4` (the fabricated hash): same silent failure family — a value filled in from memory or
  from the wrong context, defeating the discipline without any test failing. `E4`'s rule covered
  digests; this rule covers measurements.

---

## 7. Governor's final ruling on SC-4 (2026-11-22, round 39)

**SC-4 trace conclusion: accepted. `G6`/`DC2`: NO-GO maintained.** The governor withdraws the previous
query on whether `7.1e-5` could be a residual spectral-weight fraction: against the primary sources, that
explanation does not hold.

The governor formalizes the three-way distinction that must no longer be conflated:

| value | actual meaning | evidentiary nature |
|---|---|---|
| `7.087e-5` | `E_F/m*` double-pinning slack | calculated (`sc2_results.txt:44-46`) |
| `1.000000000003` | `W_intra/W_total` | measured (`sc_route_results.txt:195-198`) |
| `0.000000e+00` | allowed residual after hardcoding `f_intra = 1` | **not a measurement** |

| item | final judgement |
|---|---|
| physical meaning of `7.1e-5` | clarified — a pinning slack |
| `W_intra/W_total` | measured `1.000000000003` |
| `Q2`'s zero residual budget | generated by hardcoding, not a measurement |
| `Q2`'s original acceptance | **invalid; cannot serve as independent evidence of a pass** |
| Drude weight exhausting the budget | a model-construction identity |
| positive interband spectrum under the current budget | not permitted |
| real matter's `f_intra` | must come from the `R1-B1` microscopic response |
| v1.3 errata and lock | procedural direction correct |

Two of the governor's rulings are registered as obligations:

1. **The traceability rule is elevated to a project-wide requirement.** Every empirical number must be
   bound to the measurement product that generated it, cited by exact file and line; a value paraphrased
   from another ledger may not be treated as an original measurement. This addresses evidentiary
   identity, not only numerical accuracy. (Registered as discipline 7 of the progress report §3 and as
   the standing rule of the new defect class.)
2. **The logical boundary on §4's conclusion.** The proof establishes a budget contradiction *within the
   current module's construction* — it does not show that real matter lacks interband transitions. Real
   matter may well have an interband response; producing it requires re-establishing the intra/inter
   spectral-weight redistribution from a microscopic model, and the current construction — which
   allocates the entire budget to the Drude term by definition — cannot be reused for that purpose.

**Next step.** Not a re-run of the old `Q2`, and no further derivation of material properties from the
current Drude model. `E5` is retained; `Q2`'s passing validity is revoked; the optics line waits for
`R1-B1` to supply a microscopic model from which the spectral-weight redistribution can genuinely be
computed. This round found an **erroneous acceptance pass, not a new physical blocker**: the physical
blocker remains the absent `R1-B1` state.

*Content generated by AI*
