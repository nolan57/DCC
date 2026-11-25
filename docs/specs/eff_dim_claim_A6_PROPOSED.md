# A.6 Effective-Dimensionality Claim — registration of the submission

**Status**: **PROPOSED — registered, not adopted.** This file governs nothing. It does not license a frame, does not
close a decision, and does not amend `docs/conventions/effective_2d_definition_v1.md`.
**Received**: 2026-11-22. **Registered**: 2026-11-22.
**Self-description**: offered as a replacement for "the blanket 'no claim that the state is two-dimensional'".
**Audit**: `reports/reviews/eff_dim_claim_A6_v1_audit.md`. **Registration of predictions**:
`runs/FRONT/eff_dim_audit_registration.md` (written before `src/route/eff_dim_audit.py` existed).

---

## 1. Verbatim text, as submitted

<!-- BEGIN-VERBATIM -->

### A.6 Effective-Dimensionality Claim (replaces the blanket "no claim that the state is two-dimensional")

**Prescribed geometry parameter.** The stacking number k (layers deposited per array site) and the effective slab
thickness H_eff are linked by

    H_eff = k · δ,   δ = H/N = 1.74 m / 4.04e9 = 4.307e-10 m

The configuration rendered in `fig2_effective_dimensionality.png` uses **k = 1**, hence **H_eff = δ = 0.43 nm**. This
value was implicit in the render and is now declared explicitly.

**Freeze-out energy.** The KK gap associated with H_eff is

    E_1 = ħc / H_eff = 2.9 keV

Below this probe energy all non-zero modes along z are frozen and only the zero mode is populated; the system
behaves as effectively two-dimensional. Above this energy the z-structure is resolvable and the claim lapses.

**Stacking bound.** For a probe of available energy E,

    k_max(E) = (ħc / E) / δ

| E | H_eff = ħc/E | k_max |
|---|---|---|
| 2.5 eV (visible) | 5.0e-7 m | 1160 |
| **2.9 keV (self-consistent point)** | **4.3e-10 m** | **1** |
| 12 keV (atomic) | 1.0e-10 m | 0.23 — claim fails |
| 200 MeV (nuclear) | 1.0e-15 m | 0.002 — claim fails |

The rendered configuration sits exactly at the self-consistent point k = k_max(2.9 keV) = 1. It is the largest
stacking number that remains effective-two-dimensional at its own freeze-out energy.

**Positioning against known thin-film systems.** H_eff = 0.43 nm places this configuration in the regime of
**material two-dimensionality**, not quantum-gravitational dimensional reduction:

| System | Thickness |
|---|---|
| Pb quantum well (QWIP) | 8.5 nm |
| InAs quantum film | 5–50 nm |
| CaTiO3 / SrTiO3 quantum well | 3.1 nm |
| Sb thin film (quantum confinement) | 10–20 nm |
| **This configuration** | **0.43 nm** |
| Planck-scale compactification | 1e-35 m |

The configuration is thinner than any engineered quantum well but **25 orders of magnitude above the Planck scale**.
Its freeze-out energy (2.9 keV) is correspondingly **22 orders of magnitude below the Planck energy**. Claims of the
type D_eff → 2 (Padmanabhan et al. 2016) or spectral dimension 4 → 2 (CDT) concern the latter regime and are **not**
evidence for the former.

**Scope of the claim.**

- Affirmed: at probe energies E < 2.9 keV, z-direction degrees of freedom are frozen; the state is effectively
  two-dimensional.
- Denied: at E > 2.9 keV, z-structure is resolvable; the two-dimensional claim does not hold.
- Not addressed: L_z = 0 is a mathematical limit, not a physical state. It is not claimed, not reachable, and would
  constitute a metric degeneracy rather than a completed two-dimensionalisation.

**Coverage gap.** None of the four admission tiers (L0 persistent homology, L1 axial autocorrelation length, L2
conditional entropy, L3 DoG contrast) is sensitive to H_eff or to k. All four are statistics of the deposited 2-D
field and are blind to residual z-extent. The claim above is therefore **declared, not measured** — it rests on the
D2 prescription and on the KK estimate, not on any tier output. Closing this gap requires a tier that measures
z-residual directly; no such tier exists in the current battery.

<!-- END-VERBATIM -->

**Fidelity note.** Transcribed without correction, including the arithmetic. Where the text contradicts the record,
the contradiction is the finding (§3), not a transcription error.

## 2. What the submission gets right

Stated first and without qualification, because three of these are better than what the project already had:

1. **`H_eff` was implicit and is now explicit.** That is a real gap being closed. A render that has a thickness but
   does not declare it is unreproducible, and `DC1` exists precisely to stop that.
2. **The coverage-gap paragraph is correct and self-implicating.** A.6 says in its own words that none of the four
   tiers is sensitive to `H_eff`, that the claim is *declared, not measured*, and that closing the gap requires a
   tier that does not exist. That is the honest form, and it is the strongest paragraph in the submission.
3. **The scope's third bullet reproduces §5 of the mandatory convention correctly** — `L_z = 0` is a metric
   degeneracy, not a completed reduction. No new work needed; it is already registered, and restating it is harmless.
4. **The `D_eff → 2` / CDT paragraph gets the distinction right**: those programs concern Planck-scale spectral
   dimension, and this configuration is 25 orders of magnitude away from it. Correctly refusing to borrow their
   authority is a discipline the project has already demanded elsewhere.

## 3. Collisions with the registered record

| # | A.6 says | Record says | Class |
| --- | --- | --- | --- |
| `X1` | `δ = 4.307e-10 m`, `N = 4.04e9` | `δ = 0.215 nm`, `N = 8.08e9` (`8.12e9` registered). Both off by exactly `2`, so `Nδ = H` still holds and the error is invisible in the product | factor-2 pair, cancelling |
| `X2` | `E_1 = ħc/H_eff = 2.9 keV` | `ħc/0.4307 nm = 458 eV`. `2.9 keV` is `2π ×` that | `ħ`/`h` conflation |
| `X3` | `ΔE_z` from "the KK gap", i.e. Model C | `effective_2d_definition_v1` §2.2: Model B (deep finite well) is `πħc/L_z`; Model C is compactification. The object is a material slab — Model B — but the formula used is a KK one | model unstated, and mixed |
| `X4` | "Below this probe energy … the system behaves as effectively two-dimensional" — one number | §3: "**It is forbidden** to combine the two into a single number. Any expression of the form 'effective 2D domain `E ≤ X`' must specify which bound this `X` belongs to" | direct violation of a mandatory clause |
| `X5` | four slots: none filled except `E_probe` | §1 requires model, subsystem, `E_occ`, `E_probe`; "2D has no referent" without a subsystem | incomplete conditional |
| `X6` | `k = 1` is "the rendered configuration" | frozen census: `1.18e10` plates on `90126² = 8.12e9` sites ⇒ `k = 1.453`; `k = 1` would need a `1.09e5`-side array | contradicts frozen census |
| `X7` | "layers deposited per array site" ⇒ stacking ⇒ `H_eff = kδ` | `front_sweep_v1` §2: each layer is "joined **edge-to-edge**". Plates tile the plane; the record contains no stacking step | mechanism mis-described |
| `X8` | "replaces the blanket 'no claim that the state is two-dimensional'" | that refusal is `ME4` clause 3 (FROZEN: only "no handles created") and `MR1.0` (measured). A declared claim cannot replace a measured refusal; it can only sit beside it | category error |
| `X9` | "It is the largest stacking number that remains effective-two-dimensional at its own freeze-out energy" | `k_max(E_1(k)) = k` is an identity — see `P3`. Every `k` is the largest such number for its own freeze-out energy | vacuous predicate |

`X9` is the same class as the three vacuous definitions declined in round 11 (`ME2` computed out to be the
Euler–Lagrange equation; `ME3` algebraically identical to `C_info`), and the same class as the `ME4` "except at
phase transitions" escape clause.

## 4. Disposition

Held as **PROPOSED**. Not copied into the route body. The corrected statement, with the errors repaired and the
bound named, is registered separately as `docs/specs/effective_2d_definition_v1_annex_B.md`, which is an annex to
the mandatory convention and **not** an amendment to `R1`.

Rationale for keeping it out of `R1`'s body is in `reports/reviews/eff_dim_claim_A6_v1_audit.md` §5 and rests on
three findings, not on caution: the written formula does not yield the written number (`X2`); the "self-consistent
point" selects nothing (`X9`); and the clause it would have to occupy is forbidden by §3 of the very convention it
is about (`X4`).

---

*Content generated by AI*
