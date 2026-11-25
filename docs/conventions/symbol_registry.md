# Symbol Registry — single source of truth for enumerated labels and reserved symbols

**Created**: 2026-11-22
**Status**: **ACTIVE.** Governs all new text from this date.
**Supersedes**: any prior implicit usage. Errata for archived texts in §4.
**Enforcement**: `src/common/symbol_lint.py` → `runs/CONVENTIONS/symbol_lint_results.txt` (§6)

---

## 0. Why this document exists

The project accumulated at least **six** live collisions between enumerated labels and physical symbols, not the
one that prompted this registry:

| Letter | Meaning A | Meaning B | Meaning C | Severity |
| --- | --- | --- | --- | --- |
| **C** | ledger constraints C1–C3 (physical) | §6.1 contrast criteria C1–C4 | localization **test IDs** `[C1]…[C7]` | high — three-way |
| **L** | optics layers L1–L4 (§6.2) | presentation **fidelity levels** L1–L3 (decision statement, §F.8) | **R2-D redshift layers** L1–L3 (§4: free-particle baseline / collision-thermalisation / full `T^{μν}` feedback) | **highest — three-way, and the R2-D labels are embedded in file paths (`pz_l1.py`, `r2d_l2_results.txt`)** |
| **B** | sweep/compression parameter, `g_zz = B²`, `B_c` | evolution **test IDs** `[B0]…[B7]` | — | medium |
| **K** | trace of extrinsic curvature, `K = γ^{ij}K_{ij}`, `|K|`, `K_STEP` | **already in use**: the sci-fi boundary's four consistency checks `K1`–`K4` (`scifi_boundary_v1.md`, `internal_consistency_v1.py`) | (proposed) contrast mechanisms `K1–K4` | **high — three-way, one of them archived** |
| **P** | gates `P1a`, `P2`, `P2-C2` | probe **check IDs** P1–P6 (`meff_boundary_probe`, 2026-11-22) | — | medium |
| **M** | mass `M`, `M(R)`, `M_STEP` | gate `M4` external review (roadmap §F.8) | **two further owners**: unfolding/painting **modes** `M1` (uniform pack) / `M2` (density-preserving) in `painting_render_v1.py`; **metrics** `M1` peak brightness, `M2` visible duration, `M3` structural freedom, `M4` threshold in `abandon_assumption_visual_v1.py` | **highest — five-way**, and only discovered when the ME check was implemented (§2a) |
| **D** | gates `D2`, `D3`, `D5` | assumption D2 (prescribed background) | **(was) audit decision items `D-1`…`D-5`** — renamed `GD1`–`GD5`, 2026-11-22 | was **medium**: a third owner sat in a table discussing `C2` ordering while `D2` is the crutch that ordering is about. Now low (two owners) |

A registry that fixed only C would leave five of these. The general problem is **not** "two sets collide"; it is
that *labels and physical quantities share single-letter namespaces*. Hence the rule in §1.

## 1. The ownership rule

**R1 — sole ownership.** A single-letter namespace may be used for enumeration **only if that letter has exactly one
owner**. `C` is granted sole ownership to the physical constraint set (C1, C2, C3, and future C4). No other letter
currently qualifies.

**R2 — the letter goes to the load-bearing set.** When two sets collide, ownership is awarded to the set with the
greater citation load and the wider scope — **not** to the older set. This is deliberately not a
first-come-first-served rule.

> **Application here.** The §6.1 contrast criteria are *older* (roadmap v1.1+) than the ledger's constraint set
> (2026-11-22), but the constraints win: they are cited in every gate, every ledger row, and every stage from S0
> onward, whereas the criteria are local to §6.1/R5. **The criteria therefore move, despite being older.** A
> first-come rule would have moved the constraints and broken every gate reference in the repository.

**R3 — every other enumerated label carries a ≥2-letter prefix.** No exceptions. New sets must invent a prefix.

**R4 — subscripts do not rescue a letter.** `C_geo`, `C_phys`, `C_info`, `C_top` are **not** acceptable under R1:
they still occupy `C`. See §3 item 5.

## 2. The registry

| Label | Owner | Meaning | Scope | Status |
| --- | --- | --- | --- | --- |
| **C1** | Constraints | Effective two-dimensional space (column conservation, `d_∥ = 15.4 fm`) | **Global** | ESTABLISHED (identity) |
| **C2** | Constraints | Smooth two-dimensionalization (zero intralayer strain) | **Global** | holds intralayer; interlayer FAIL registered |
| **C3** | Constraints | Weak(non-covalent)-interaction preservation, self-consistent in action | **Global** | **NO-GO** in-action, parameter-independent |
| C4 | Constraints | *reserved*, unused | — | reserved for a future physical boundary only |
| **CM1** | Contrast criteria | Thickness distinguishability: is the third-dimension thickness resolvable? (`d ≪ λ`) | §6.1 / R5 | renamed from §6.1 `C1` |
| **CM2** | Contrast criteria | Optical contrast (reflection / absorption / scattering for incident light) | §6.1 / R5 | renamed from §6.1 `C2` |
| **CM3** | Contrast criteria | Self-emission (the object's own thermal / non-thermal radiation) | §6.1 / R5 | renamed from §6.1 `C3` |
| **CM4** | Contrast criteria | Visual threshold (retinal signal vs threshold; spatial / spectral / temporal contrast) | §6.1 / R5 | renamed from §6.1 `C4` |
| **CM5** | Observation channel | **Resolution-relative injectivity**: `μ_ov ≤ δ_ov` at declared depth resolution `Δz_res` — can an observer at this resolution distinguish two material points in one column? | S0–S4, observation only | **NEW 2026-11-22** (`GD1` Option B): the former `ME1`, reclassified out of the gate set. `ME1` is now a **deprecated alias** |
| **EN1** | Enhancement techniques | Band migration | rendering, S0+ | new namespace (§3 item 2) |
| **EN2** | Enhancement techniques | False colour / pseudo-colour | rendering, S0+ | new namespace |
| **EN3** | Enhancement techniques | Contrast stretch | rendering, S0+ | new namespace |
| **EN4** | Enhancement techniques | Shadowgraph / transmission channel | rendering, S0+ | new namespace |
| **L1–L4** | Optics layers | L1 geometric optics · L2 material optics · L3 radiative transfer · L4 observer imaging | §6.2 / R5 | **retained**; third meaning of `L`, §3 item 3 |
| **R2-D L1–L3** | Redshift layers | L1 free-particle geodesic baseline · L2 collision/thermalisation response · L3 full `T^{μν}` feedback | §4 / R2-D | **retained, path-embedded** — never rename (breaks §9.1); always qualify as "R2-D L1" |
| **FL1** | Fidelity levels | Digital-enhanced discernibility | presentation ladder | originally `L1` in the decision statement |
| **FL2** | Fidelity levels | Natural-band presentation | presentation ladder | originally `L2` |
| **FL3** | Fidelity levels | Naked-eye visible reflection | presentation ladder | originally `L3` |
| **ME2–ME5** | M_eff boundary | parallax at sampling scale · perpendicular energy fraction · fragment census · lifetime | S3→S4 branch | **ADOPTED** 2026-11-22 (ruling D-B); **`ME1` VACATED** by `GD1` Option B → `CM5`. The number must not be refilled: reusing it would recreate the gate/observation conflation the ruling removed. Spec `docs/specs/meff_boundary_v0_2.md` |
| `C_geo` `C_phys` `C_info` `C_top` | — | **RETIRED** — v0.1 draft constraints | historical only | **retired** under R4; may not be reintroduced. `C_info` **dissolved**, not replaced |
| **Q1–Q6** | Probe checks | the six checks of `meff_boundary_probe` | audit only | renamed from `P1–P6` (§3 item 4) |
| — | Gates | `G3′`, `G4`, `G5′`, `G6`, `P1a`, `P2`, `P2-C2`, `P2-C6`, `D5` | gates | unchanged |
| — | Assumption | `D2` = prescribed contraction background | ledger | unchanged |
| — | `B` | sweep / compression parameter, `g_zz = B²`, `Σ = ∫ρ√g_zz dz`, `dΣ/dB = 0` | physical | **physical symbol — never a label** |
| — | `K` | trace of extrinsic curvature `K = γ^{ij}K_{ij}` (CMC slicing) | physical | **physical symbol — never a label** |
| **K1** | Sci-fi boundary checks | Thickness window for `L_z` (`1.7–2.0 fm` with chemistry / `1–4.5 fm` without) | `scifi_boundary_v1.md`, `internal_consistency_v1.py` | **PRE-EXISTING — must not be reused** |
| **K2** | Sci-fi boundary checks | Confinement field strength (≥ `6×10²³ V/m`, or a 2D pocket) | same | **PRE-EXISTING** |
| **K3** | Sci-fi boundary checks | `z`-direction wall pressure (absent on Route S) | same | **PRE-EXISTING** |
| **K4** | Sci-fi boundary checks | Energy / zero-point term (`3.8×10¹⁸ J/m²` Route M / `1.7×10¹⁷` Route S) | same | **PRE-EXISTING** |
| — | `ε` | *contested*: 2D-ification progress parameter (draft v0.1) **vs** potential offset `V(φ, eps)` **vs** mean excitation `ε_mn` | — | **OPEN**, see §3 item 6 |

## 2a. The `M` letter is closed (2026-11-22, found by implementation, not by inspection)

Writing the `ME` namespace check (`symbol_lint.py` rule F) revealed that `M1`–`M4` already has **four distinct
owners** in this repository, not the two assumed when the proposal to use `M1–M5` was made:

| Owner | Where | Meaning |
| --- | --- | --- |
| mass | throughout | `M`, `M(R)`, `M_STEP`, `M_ADM` |
| gate | roadmap §F.8, `D5` | `M4` external review |
| unfolding modes | `src/analysis/painting_render_v1.py` | `M1` uniform pack · `M2` density-preserving mapping |
| visibility metrics | `src/analysis/abandon_assumption_visual_v1.py` | `M1` peak brightness · `M2` visible duration · `M3` structural freedom · `M4` threshold |

Consequences:

1. **The `ME` prefix is not a courtesy, it is the only available construction.** No `M`-prefixed single-letter
   enumeration can be admissible under R3.
2. **The scope qualifier `Constraint:ME4` vs `Gate:M4` is necessary but insufficient** — it separates two of
   the five. Rule **S5** supplies the general form.
3. The two source files' `M1`/`M2` are pre-existing debt, logged here rather than renamed: their labels are
   embedded in archived stdout (§9.1). Any new text referring to them writes "painting mode M2" or
   "visibility metric M3" in prose.

## 2b. Registrations made by the phased route v2 (2026-11-22)

| Label | Owner | Meaning | Status |
| --- | --- | --- | --- |
| **`τ_conv`** | Phased route v2 Phase 2 | the conversion's intrinsic clock — the time over which the front sweeps the object | **registered as the ONLY admissible name for a conversion clock.** Bare `τ` in a conversion context is non-compliant: `τ` is the Drude relaxation time in `src/optics/sigma_s_lindhard.py` (`TAU_SCAN`, OPEN, scanned not solved). Phase 2 as submitted wrote "intrinsic time scale τ"; that is a second owner and is corrected here |
| **`Δz_res`** | v0.2 `ME1` | the declared depth resolution at which `μ_ov` is evaluated — the single parameter that decides `ME1` | **unregistered value, named parameter.** No value assigned; audit V1 establishes that the gate is undecidable until one is. Not on any OPEN list, which was the gap |
| **`Λ_max`** | — | a maximum deformation rate for a rate-cap formulation of `ME5` | **RETIRED.** Belongs to the declined alternative `ME5` (`meff_boundary_v0_2_alt_definitions_DECLINED.md`); not a parameter of adopted `ME5`, which is an exact identity with no rate constant. A rate *cap* bounds duration from below and is satisfied by the un-imageable case (review V5, audit R5: `1.06e12 ×` slower than `t_rip`) |
| **`ME1′`** | Phased route v2 Phase 1 | the relaxed successor of `ME1` | **reserved, no definition.** Phase 1's stated target ("local injectivity neighbourhood radius") is not a parameter of `ME1` and is empty by invariance of domain (audit V2). The label may not be used in a derivation until its target is re-specified |
| **`φ_E`** | `ME3` (v0.2) | the field whose gradient ratio `δ_E` measures | **RELEASED, never used.** `ME3` is retired (`GD6` closed, `me3_phi_disposition_v1.md`), so the reserved name is withdrawn. It may not be reused for a new criterion without a fresh declaration. Distinct from **`φ_conv`** (converted proper-volume fraction) |
| **`GD6`** | `route_completion_v1.md` §6 | what `ME3`'s `φ` denotes | **CLOSED 2026-11-22 — `ME3` RETIRED.** `φ` **is** a velocity potential, fixed by the criterion's own name ("perpendicular *energy* fraction"). The material reading is withdrawn as a **misreading**: measured `k = 1.89 / 0.95 / 0.43` for the material, indicator and geometric readings ⇒ all inverted ⇒ the constraint is a **minimum-thickness floor** (`δ_E ≤ δ_E,max ⟺ t ≥ t_min`). With `φ` a potential, `δ_E ≡ 0` on `u^μ = (c,0,0,0)` ⇒ every state passes ⇒ nothing can be rejected. **No `δ_E,max` exists to register.** `ME3-F1` closed. Ruling `me3_phi_disposition_v1.md` |
| **`GD1`–`GD5`** | `reports/reviews/phased_route_v2_audit.md` §J | governor decision items (not physics, not gates) | **registered, `GD2` withdrawn.** Replaces `D-1`…`D-5`, which added a third owner to `D` alongside gates `D2`/`D3`/`D5` and assumption `D2` — and did so in a table about `C2` ordering, i.e. about the very crutch `D2` names. Live: `GD1` (the only blocking one), `GD3`, `GD4`, `GD5` |
| **`GD7`** | `reports/reviews/route_goal_conformance_v1.md` §5 | **RULED 2026-11-22** — governor: *"FL means 'faithful to what the human eye sees', and FL3 is the maximum"*. `FL` = closeness to the unaided retinal image; the ladder **ascends** | **CLOSED.** Executed in `gd7_gd8_execution_v1.md`; coordinate `FL = −(b+c+p+e)` in `src/route/fl_coordinate.py`; enforcement `DC9`. Measured: `FL3 = 0.0000 > FL2 = −3.1011 > FL1 = −16.1344`. Consequence: `FL` and information are anti-correlated by construction, which is why `FL3`'s frame shows the object's **absence** |
| **`GD8`** | same, §5 | **RULED 2026-11-22** — governor: *"keep 2L/c, and write in 'only when D = L'"*. The corollary keeps `2L/c` and now carries the premise `D = L` | **CLOSED.** Premise written into the corollary (`meff_boundary_v0_2` §2). Costs nothing: naked eye needs `D ≥ 0.25 m`, and `D ≥ L/√2` for every `L ≤ 0.3536 m`, so the conclusion holds **a fortiori**. The per-patch form `D ≤ d/√2` is **not adopted** — an unregistered observation, licensing no frame |
| **`GD9`** | `docs/decisions/gd7_gd8_execution_v1.md` §5 | what is the route's objective? | **CLOSED 2026-11-22** (`deposit_serial_conformance_v1.md` §5, `D-13`). Objective = **fidelity constrained exactly + locality maximised**. Fidelity is not a target to trade — `A1` `0` mismatches, `A2` exactly `4 B/plate`, both by count — and locality is the only free term (`A3` contiguity, `A4` median `|Δn|`). **A quantity that cannot trade against a hard constraint is not a metric of this route** — the reason the 32-cell readability matrix was the wrong instrument. Supersedes the `FL`-vs-information framing: `FL` was a readability objective, and readability is closed (`MR1.0`) |
| **`GD10`** | `reports/reviews/eff_dim_claim_A6_v1_audit.md` §6 | ruling requested: **plates per cell** — the frozen census has `1.18e10` plates on `90126² = 8.1227e9` cells, i.e. `1.4527` per cell, so a one-plate-per-cell reading fills `145%` of cells | **OPEN — exposed while auditing A.6, not by it.** Two admissible repairs, neither taken (census is FROZEN): (A) side `108628²`, spacing `0.332 m`, canvas unchanged at `36.06 km`; (B) cells hold several plates and figures draw a multiplicity, not an occupancy. Does **not** affect `H_eff`, because plates are coplanar (`effective_2d_definition_v1_annex_B` §B.1). Blocks any statement about site occupancy |
| **`GD11`** | `docs/decisions/space_filling_vs_identity_v1.md` §1, §5 | ruling requested: **which site does layer `n_z` go to?** `front_sweep_v1` §2 ② says each layer is carried to "**its** lattice site", a possessive that asserts `σ : n_z → (u,v)` — and **no document defines it**. §5 constrains the order only by transport speed and accepts two families | **OPEN — exposed by the fourth submission, not by my own audit.** `P1`: 38 markdown files under `docs/`, `0` rule-shaped hits (`18` raw `σ`/`Σ` hits, all stress or column density — a form-failure of my encoding). Consequence: any frame drawing site **content** has already chosen `σ` silently; `mid_sweep_fl1.png` draws only occupancy, which is why this was invisible. **Choosing `σ` is a convention, never a derivation** (`front_sweep_v1` §2.1: nothing selects `Π`). **Blocked upstream by `GD10`** — if the side is `108628` the site set changes. Declared in `front_sweep_v1` §2.2, which chooses nothing. **Status 2026-11-22: CLOSED for `DEMO-1` only** (see `SIGMA-DEMO`); the body still has no `σ`. A new object dissolved the `GD10` block rather than answering it — `pieces 4.279e9 ≤ cells 4.295e9` by construction |
| **`FL-COORD`** | `src/route/fl_coordinate.py` | the `GD7` fidelity coordinate: `FL = −(b + c + p + e)`, `b` band offset, `c` contrast distortion, `p` photon deficit, `e` `EN`-operator count | **NEW 2026-11-22.** `FL3 = 0` exactly and uniquely; continuous (`|dFL/d log₁₀g| = 1.0000`), so the rungs are thresholds on a continuum. Equal weights are a **declared convention** (`DC4`), reported and never scored |
| **`EN-BOUND`** | `src/route/goal_conformance.py` | the non-introduction test for enhancement: `levels_display > levels_scalar` **or** map not monotone in the scalar ⇒ CONVICT | **NEW 2026-11-22.** Two branches, negative-tested (2 planted defects convicted, 2 compliant controls passed). Branch (b) is the existing `EN2` requirement made executable; branch (a) is new and convicts interpolation presented as structure. Instrument, not gate (`DC4`) |
| **`MATRIX-ROUTE`** | `docs/decisions/exhaustive_matrix_route_v1.md` | the **PROPOSED** successor route: 8 constraint combinations × 4 distinguishability tiers `L0`–`L3`, drafted as a coverage set rather than a path | **PROPOSED 2026-11-22, NOT ratified — governs nothing.** Audit `reports/reviews/exhaustive_matrix_route_v1_audit.md`: **NOT VIABLE AS WRITTEN**, 9 of 10 findings blocking. `L0`–`L3` form a claim on strings that must not be read as the registered `FL1`–`FL3` (`L3` is a *stricter* predicate than `FL3`: it adds "recognizable as a structured image", which excludes `FL3` member A) |
| **`L0`–`L3`** | `docs/specs/intrinsic_structure_tiers_v1.md` | the matrix's four distinguishability tiers, **redefined 2026-11-22 as intrinsic**: all four now refer only to the scene. `L0` topological organization; `L1` characteristic scale in the scene's own metric; `L2` predictability (self-referenced information); `L3` legibility through a declared observer | **ADOPTED + ADMITTED 2026-11-22** (`docs/decisions/tier_admission_v1.md`). The *extrinsic* definitions of `exhaustive_matrix_route_v1.md` §III are **WITHDRAWN** (they compared the scene to the original object; audit M2–M6). Admission is a machine verdict, not a statement: `(a)` intrinsicality, `(b)` null/control separation, `(c)` hash-locked threshold, each independently negative-tested (`N1`–`N5` all fired). Replaces the earlier `RESERVED` status. **A cell is a 4-tuple, not a maximum** — the tiers are independent (0 of 6 pairs identical) so no total order exists |
| **`TIER-LOCK`** | `runs/MATRIX/threshold_lock.json` + `.sha256` | `(c)` of the admission rule: the four thresholds, the declared constants, and the digest of the spec that declares them | **NEW 2026-11-22.** Digest `5f324e15…`; lock mtime provably earlier than the run (59 s). Editing either the lock or the spec refuses **all four** tiers on `(c)` — verified as `N3`. This is why `T3`'s rename is blocked: the collision lives inside the lock and cannot be repaired without a v2 digest |
| **`M-ROW`** | `runs/MATRIX/matrix_audit_results.txt` M-1 | row admissibility: a combination containing `C3` is **VOID** (`C3` is a parameter-independent NO-GO, so it cannot be satisfied); a combination containing `¬C2` is **UNREALIZED** (`C2` is a theorem of the mechanism — `front_sweep_v1` §2 step ② is an `(x,y)` identity map — so non-zero intralayer strain has no construction) | **NEW 2026-11-22.** Of 8 distinct combinations, **2 admissible** (`C1∧C2∧¬C3`, `¬C1∧C2∧¬C3`), 4 VOID, 2 UNREALIZED. Both rows the proposal names as baselines are dead. Consequence: `C2` is **not a relaxation axis** — there is nothing to relax |
| **`M-TIER`** | same, M-6 | the tier directional test: does the tier score improve as 2D-ification completes? | **NEW 2026-11-22. 0 of 4 increase.** `L0` decreasing (`χ` ratio `1.18e10`), `L1` decreasing (`d_H = 1.46e4 H`), `L2` constant at `0`, `L3` decreasing (empty at `C1`). No total order `L0<L1<L2<L3` is compatible with the measured signs, so "Max Distinguishability" per cell is not computable as specified |
| **`ANNEX-A`** | `docs/specs/intrinsic_structure_tiers_v1_annex_A.md` | the **applicability domains** of `Q0` and `Q2`: where a pass or a fail may be cited as evidence at all | **IN FORCE 2026-11-22** (ruling `T1`/`T2`). Part of `intrinsic_structure_tiers_v1` **by reference but outside its digest**, because editing the digest-covered spec would refuse all four tiers on `(c)` rather than narrow them. Self-limited: may not contain a tier threshold. Digest `560acd8c…3fc07` in a separate sidecar; the lock is byte-identical |
| **`ANNEX-B`** | `docs/specs/effective_2d_definition_v1_annex_B.md` | the declared `H_eff` and `ΔE_z` for the deposited object: `H_eff = δ = 0.215 nm` (**coplanar**, independent of plates per cell), `ΔE_z = πħc/H_eff = 2.883 keV` (Model B), bound **named as external only**; plus **§B.8** the thickness image and the Planck exclusion | **IN FORCE 2026-11-22**, annex to `effective_2d_definition_v1` by reference, not an amendment; **§B.8 added 2026-11-22** (`t4_heff_floor_ruling_v1.md`). Internal bound fails by `2.3e3–2.5e4`; subsystem slot **empty**, so per §1 the conditional has no truth value yet. Self-limited: may not contain a tier threshold |
| **`HEFF-IMAGE`** | `effective_2d_definition_v1_annex_B.md` §B.8 | the model's **image in thickness**: `H_eff = δ` and no other value; `n_max(ℓ_P) = ℓ_P/δ = 7.52e-26 < 1`, so no admissible configuration exists at the Planck thickness | **NEW 2026-11-22.** Declared, never measured (`S10`: all four tiers unpack `W, H = u.shape`). Replaces the earlier *distance* statement ("25 orders of magnitude away", `δ/ℓ_P = 10^25.12`, confirmed) with an **exclusion**: `ℓ_P` is not a far point on the thickness axis, it is **not a point on that axis**. Refuses `H_eff = n_z·δ ≥ δ` as a variable form — the record has no stacking step, so a multiplier grants a freedom the construction lacks. `δ` is not the bottom of the range, it is the range |
| **`n_z`** | §B.8.1 | the **layer** variable along `z` in any statement about stacking | **NEW 2026-11-22.** Registered because the submission used `k` for it, and `k` is already plates-per-cell `= 1.4527` (`ANNEX-B` §B.1) — an `S9`(a) collision. `k` (coverage multiplicity) and `n_z` (layers) may not be interchanged, and neither is a thickness knob |
| **`T4-INSERTION`** | `runs/FRONT/t4_submission_verbatim.md` | the second submission: `R1` `§4.5.1 Lower Bound on H_eff` + `T4` as a fifth tier + three cross-references | **PROPOSED — governs nothing; NOT APPLICABLE AS WRITTEN** (`docs/decisions/t4_heff_floor_ruling_v1.md`, 5 blockers). Both anchors do not exist in `R1` (`k_max`, `H_eff`, `4.5.1`, `T4` = 0 occurrences); `ħc/δ = 2.9 keV` is false by `6.33× = 2π` for the **third** document; names no bound (§3 prohibition); `T4` is already in force as `MR1`. Accepted part re-registered as `HEFF-IMAGE`. Both cut arguments ("matter vanishes", micro black hole) recorded as cut, with reason |
| **`KIN-DYN`** | `docs/decisions/front_sweep_v1.md` §2.1 | the scope clause separating the two: D2 performs **no deformation** (rigid translation + edge-to-edge join + vacuum gaps), so intralayer strain is zero **by construction**; no claim is made that a body driven by its own constitutive law would unfold the way D2 arranges it | **IN FORCE 2026-11-22** (`kinematic_vs_dynamic_unfolding_v1.md`). **Declared, not measured.** No frame may depict elastic unfolding, differential strain, wave propagation or fracture as a consequence of D2. The zero is structural — there is no stored energy to release — and the price is that `Π` is a **chosen** relabelling, not a selected one. Not a tier and not numbered as one |
| **`C3-INSERTION`** | `runs/FRONT/kin_dyn_submission_verbatim.md` | the third submission: `R1` `§4.6` kinematic vs dynamic unfolding, a worked composite-disc example, and three cross-references | **PROPOSED — governs nothing.** Verdict: distinction **ACCEPTED** (registered as `KIN-DYN`); worked example **REJECTED** — its `Π` dilates by `R/δ` (in-plane strain `8.37e8`) while D2's map is the **identity** (`0`), i.e. it reintroduces the `9.28e8` already corrected as a displacement gradient; interface argument **inverted** (traction is continuous, strain jumps); `1:10` strain ratio is the **unbonded** one in a body declared bonded; "bone-like" vs "soft-tissue-like" overclaims contrast by `3–6` decades. `T5` **refused** — already in force in `tier_admission_v1` (second label collision in two submissions); `§7` is Correction 1, not a gap list; `§4.5.1` still does not exist |
| **`SF-CURVE-SUBMISSION`** | `runs/FRONT/sf_curve_submission_verbatim.md` | the fourth submission: `D2` is an identity map, so the algorithm must be a space-filling curve / spiral over Planck cells, yielding an unreadable "data map" | **PROPOSED — governs nothing. PARTIALLY ACCEPTED** (`space_filling_vs_identity_v1.md`). ACCEPTED: the ordering question is real and was unregistered → `GD11`; and the algorithm **measures better than the record's implicit order** (`Hilbert` contiguity `1.0000` vs raster `0.9961`, `ρ` `1.0` vs `256`, median adjacent `|Δn|` `1.0` vs `128.5`). REFUSED: the derivation — the two cited constraints are permutation-invariant, admitting `10^1.14e11` bijections and ranking none (`P4`/`P5`, fifth `S10` instance), and `front_sweep_v1` §2.1 **already** says nothing selects `Π` (`P2`); the Planck grid is `n_max(ℓ_P) = 7.52e-26 < 1`; the voxel reading multiplies a **frozen** census by `5.1e17` (array side `8.63e8 ×`, canvas `208 AU`); projection is criticised where it is used nowhere (`0` hits in `docs/`). `S4` is **inverted** by §3 of the ruling: the curve makes crops more faithful, not less |
| **`SIGMA-DEMO`** | `docs/specs/demo_object_v1.md` §4 | the **declared traversal** for `DEMO-1`: `p = k·N + n` (component-major) → Hilbert index `p`, order 16, exact (side a power of two, no padding) | **IN FORCE, locked 2026-11-22.** The ordering is **component-major because layer-major is annihilated by decimation**: one display pixel spans `16384` sites = `4096` layers × `4` components, an exact number of `4`-cycles, so its component mix is `25.0%` each (`P8`, measured). Component-major gives `99.9985%` single-shell pixels, `3` shell-straddling (`P9`/`P10`). Contiguity `1.000000`. **Cost, declared:** the map is four scrolls, not a mosaic — a cross-section is reassembled by taking the same relative offset in each run. Closes `GD11` **for `DEMO-1` only** |
| **`FOURDIM-V2-SUBMISSION`** | `runs/MATRIX/fourdim_v2_submission_verbatim.md`; ruling `docs/decisions/four_dimension_reanchor_v1.md` | the fifth submission: re-anchors the four dimensions as topological conservation / metric `ε` / channel `I_min` / observer extraction | **PARTIALLY ADOPTED 2026-11-22.** The four *names*, their order and the demand for a declared statistic + pre-locked threshold are **vocabulary** (`FOURDIM-V2`). The four operational contents are **not adopted** — each refused on measurement, not caution. Its diagnosis of my previous verdict is accepted: the *statistics* (`Q0` amplitude-invariant, `Q2` shuffle-passing) were defective, not the dimensions; and its MI claim is right for a position-paired estimator, so my `T2`-based refusal did not transfer |
| **`TOPO-CLOSE`** | ruling `four_dimension_reanchor_v1.md` §2; `runs/MATRIX/fourdim_results.txt` `[A]` | the topological gate `b0`/genus must match 100% | **REFUSED — unsatisfiable by construction.** `b0(deposit) = pieces = M·H/δ = 4,279,069,764` vs `b0(object) = 1`; `σ` permutes sites and cannot create contact across vacuum, so the gate closes for **every** admissible deposit. Genus also fails (`3,209,302,323` vs `0` — `C2`–`C4` plates are annuli), **contrary to my own `P3`** (erratum `E4`). Where it passes it is blind: the object's material is contractible (`χ = 1`, voxel), so a homogeneously painted cylinder scores identically. On the index space it degenerates to the census identity, already in force |
| **`MI-INVARIANT`** | ruling `four_dimension_reanchor_v1.md` §4; `[C]` | `I(2D image; 3D structure)` as a terminal condition | **MEASURED — invariant to the ordering, so it cannot reject a scrambled encoding.** `I = log₂(pieces) − log₂(sites/pixel) = 31.9947 − 14.0000 = 17.9947` bits for component-major, layer-major **and a random permutation**, to four decimals, while pixel purity spans `99.99885% → 0%`. Exact reason: a pixel holds 16,384 pieces however chosen. Also: `H` over area `1.738970` vs over pieces `2.000000` (`0.26`-bit counting-measure ambiguity), and `I ≡ 0` for a homogeneous body (`H(X) = 0`). The quantity that does separate orderings is **purity → `MR2`** |
| **`DEMO-1`** | `docs/specs/demo_object_v1.md` (**hash-locked**, `runs/FRONT/demo_lock.json`, `sha256 afe855c2…4633`) | the declared demonstration object: four coaxial shells, `H = 0.230 m`, `r4 = 0.090 m`, `C2`/`C3` anti-phased, every component full height, array `65536²`, `pieces 4.279069764e9 ≤ cells 4.294967296e9` | **IN FORCE for display only 2026-11-22** (`demo_object_ruling_v1.md`). Replaces the body as the *rendering subject*; changes no physical record (`H = 1.74 m`, `δ`, `1.18e10` plates, `90126²` all stand). Its census is exact by construction, so `GD10` cannot arise — 0.9963 plates per cell. **The components differ only geometrically**: the four declared areal densities are read by nothing (`KIN-DYN`: `D2` performs no deformation). Self-limited: may not contain a tier threshold |
| **`A6-PROPOSED`** | `docs/specs/eff_dim_claim_A6_PROPOSED.md` | the submission that proposed replacing the blanket "no claim that the state is two-dimensional" | **PROPOSED — not adopted, governs nothing.** Written formula yields `458 eV` not `2.9 keV` (`ħ`/`h`, and `δ` doubled with `N` halved so `Nδ = H` hides it); the `k`-selection is an identity (`S10`); the single-number form is the one `effective_2d_definition_v1` §3 **forbids**. Surviving content re-registered in `ANNEX-B` |
| **`MR1`–`MR3`** | `docs/decisions/matrix_reading_rules_v1.md` | how a matrix cell may be **read** (as opposed to computed) | **`MR1` IN FORCE 2026-11-22** (ruling `T4`); `MR2`/`MR3` open — **and `MR2` is where `FOURDIM-V2` (§7) lands: three of the four re-anchored dimensions reduce to it or to the census identity.** **`MR2` is now CLOSED as a gate (`MR2-CLOSE`, 2026-11-22) and survives only as `MR2-D`, a threshold-free diagnostic** — so three of those four dimensions now land on a closed gate, and the critical path does not run through a statistic. `MR1.0`: no cell may be read as "readable"; `MR1.3`: **zero readable cells**, for two independent reasons; `MR1.2`: a cell is a 4-tuple profile, never a maximum. Labelled `MR` and not `R` because `R1`–`R4` are the ownership rules and rule `R3` requires a ≥2-letter prefix. **`T4` is the reading-precondition ruling and may not be reused for any other object** — the 2026-11-22 submission's `T4 — Domain Boundary of the Framework Itself` is refused as a label collision (`T4-INSERTION`) |
| **`LOCKED-PATH`** | `src/common/locked_path_guard.py`, `runs/MATRIX/locked_path_digest.json` | the pair *(digest of `src/route/structure_tiers.py`, digest of `results`)* that makes §5 `S9`(c) checkable | **NEW 2026-11-22.** Four verdicts, all negative-tested: `OK` / `RENAME-ADMITTED` (source moved, numbers identical — the signature of a rename) / `DRIFT` (numbers moved, source still) / `BLOCK` (both moved → needs a new lock, exit 1). Turns the governor's sentence "a rename must not change any locked quantity's computation path" into a measurement |
| **`MR2-PSMI`** | `runs/MATRIX/mr2_arap_submission_verbatim.md` | the fifth submission: `MR2 = D_KL(P_3D‖P_2D)` over pairwise-distance distributions, fed by an ARAP energy and by TPGIM depth channels | **PROPOSED — governs nothing. REJECTED AS A GATE** (`mr2_arap_designation_v1.md`, `15/16` predictions held, `P6` refuted against me). Branch A: `supp(P_3D) = (0, 0.292062]` and `supp(P_2D) ⊆ [0.4001, 37082]` are **disjoint** (`37.0%` clear), so `D_KL = +∞` for every `σ`. Branch B: circular (`E_ARAP` with `R_i = I` **is** the distance discrepancy the statistic measures) and forbidden by `KIN-DYN` §6. `R_i∈SO(2)` applied to a `ℝ³` edge is ill-typed; `docs/` has `0` hits for `triangulat`/`vertex set`, so ARAP's object does not exist here |
| **`MR2-CLOSE`** | ruling `mr2_arap_designation_v1.md` §2, §4, §7 | `MR2` **cannot** be an arrangement-sensitive gate, for a reason independent of which statistic is chosen | **RULING 2026-11-22.** The deposit severs every interface by construction, so **every finite statistic of arrangement is a statistic of `σ`, and every statistic of the object is `+∞`**. Measured: `D_KL(deposit‖random permutation) = 0.06639` nats (`422×` floor) — but `X1` decomposes it and `99.2%` is the four-contiguous-runs contrast, i.e. `σ`; within-shell arrangement contributes `0.82%` = floor noise (expectation exactly `0`, since scrambling within a run preserves the site set). `DEMO-1` §4.3 measures the same property at `1.0000` vs `0.9961` without a threshold. Plus `100%` interface destruction (`d_3D = 0` → `d_2D = 1.2e4 m`). Third independent arrival, after `TOPO-CLOSE` and `MI-INVARIANT`. **Consequence: `MR2` leaves the critical path; `MR1.0` stands unqualified** |
| **`MR2-D`** | same, §7 | the **diagnostic** residue: the 2D separation of *3D-local* (`d_3D = δ`) and *3D-contacting* (`d_3D = 0`) pairs, reported per declared `σ` | **IN FORCE as a diagnostic, NO threshold and no admission power.** For `DEMO-1`: axial pairs land at exactly one `pitch` (`d_2D/pitch = 1.0000` for all four shells, a delta — against `1.9e3–2.4e4 m` if shuffled), interface pairs at `1.2e4 m` (`100%` destroyed). It quantifies `DEMO-1` §4.2's declared loss. **May not be read as a pass, a cell, or a readability claim**; it creates no lock |
| **`KL-FLOOR`** | ruling `mr2_arap_designation_v1.md` §8 | the sampling floor of a two-sample `D_KL` over `B` bins at `N` samples each | **MEASURED, `∝ B/N`.** Ratio to my registered `(B−1)/(2N)` was `1.47, 1.86, 1.99, 1.98, 2.05` at `B = 16…4096` — i.e. the empirical constant is `(B−1)/N`, a factor `2` from what I predicted, and `P7` "passed" only because the band I declared was wide enough to hide it. Operative content: **a perfect map does not score `0`**; at `B = 4096, N = 1e5` it scores `0.0419` nats. Any `MR2` threshold below that is unreachable and any above it is trivially passable |
| **`MR2D-POTENTIAL`** | `runs/MATRIX/mr2d_potential_submission_verbatim.md` | the sixth submission: replace the topological "do not cut" constraint with a truncated Morse potential on `N_phys`, keep `MR2-D` as the sole metric, restage at 500–1000 voxels | **PROPOSED — governs nothing. PARTIALLY ACCEPTED** (`mr2d_potential_ruling_v1.md`, `15/15` predictions held, 2 of 4 of the submission's own §I claims accurate). Headline: **it adds a term that is identically zero to a term that is forbidden** — `Σ Ψ = 0.0` exactly for every physical `(α, r_cut, d₀)`, so `E_total = E_ARAP`, which `KIN-DYN` §6 forbids. §I claim 2 ("spurious stresses") is true of the *previous submission*, false of the record (`D2` has no stress field); the correction therefore repairs the wrong layer |
| **`POT-TRICHOTOMY`** | ruling `mr2d_potential_ruling_v1.md` §4.2 | the exhaustion showing the interface potential cannot act on the deposit | **MEASURED, three branches, no fourth.** (i) `d₀ = δ`, physical `α` ⇒ `Ψ(pitch)/D_e = 0.000000` (underflow; `α` needed for 1% is `≤ 13.236 m⁻¹` against a physical `2e10 m⁻¹` = **`1.51e9×` short**). (ii) `d₀ = pitch` ⇒ `Ψ = −D_e` exactly and **`|force| = 0.000000`**: a constant per pair, no gradient, cannot move the map. (iii) `α = 1 m⁻¹` ⇒ acts, pulling neighbours off `pitch` by `1.861e9×` — prohibited. Governing group `Π = α(pitch − d₀) = 8.00e9`; a potential that acts has `Π ≲ 5`. `r_cut` must be `≥ 0.4001 m` for one pair to contribute: `≥ 4.0e8×` a physical cutoff |
| **`N_phys`** | `MR2D-POTENTIAL` §II | the set of genuinely-contacting pairs (`d_3D ≤ δ`) | **REGISTERED as a symbol; REFUTED as a set the potential can reach.** Non-empty: `3,318` at `POC-1024`, `≈1.387e10` at `DEMO-1` scale (2 axial per piece + 3 per adjacent shell per interface). Its `d_2D` range is `[0.4001, 13.78] m` at POC, so **`0`** of its members lie inside any physical `r_cut` |
| **`DEPOSIT-BLIND`** | ruling `docs/decisions/route_terminus_v1.md` §2; `runs/ROUTE/deposit_blindness_results.txt` `[A]`,`[C]` | the theorem: `D2`'s deposit factors through `(M, N)` only — `deposit(O) = F(M(O), N(O))`, no other parameter of `O` enters | **MEASURED 2026-11-22, `12/12` predictions (`11/12` as registered; `P5` re-read under erratum `E1`).** Constructor passed a read-logging mapping: reads `M`, `H`, **`0`** geometry keys. **Six** physically distinct objects (jacket radius `0.0900→0.1500 m`, cut area `2.78×`; modulation phase inverted; four densities reversed; all radii re-stacked; plus one at `r₄ = 0.4950 m` outside A3) give **one** digest `558d30e08fd32cf6`. `I(canvas ; r₄) = 0` bits. Per site the canvas carries a **band label `k` and an axial coordinate `n`** — and nothing else. `2` of `12` declared parameters visible. Negative controls fire (`H` halved ⇒ different digest; `M = 5` inadmissible). **This is the fact behind the 31 closed gates**: every statistic was a function of the declaration |
| **`DEPOSIT-SERIAL`** | same, §5 | the re-designation: the deposit is a **lossless 2-D serialization of the piece enumeration**, not an image and not a reduction | **IN FORCE 2026-11-22.** Judged as a serialization it is good — `4,279,069,764` plates × `4 B` = `15.9408 GiB`, exact round trip, contiguity `1.000000` (raster `0.9961`), component-major so sequential reads visit one shell's axial history. Displays of it are `FL1` and may not be cited as evidence of readability. `SFC-INDEX` survives as the one positive of that line; it indexes the object and is not `σ` |
| **`DEPOSIT-DICHOTOMY`** | same, §4 | the exhaustion: *injective* and *renderable* are contradictory demands on one map, and no algorithm repairs it | **MEASURED.** Injective needs `⌈√pieces⌉ = 65,415` per side ⇒ `2¹⁶` (canvas `26,221 m`); renderable is `2⁹`; the gap is `2¹⁴ = 16,384` **exactly**, and a `4K` frame still shows `0.19%`. Also **no similarity scale exists**: `sup d₃D = 0.292062 m < inf d₂D = 0.400100 m`, so the 3D support lies strictly inside the 2D gap and no `s` gives `d₂D ≈ s·d₃D` — the deposit is not a blurred image either. An image is many-to-one by definition; the deposit is one-to-one. A one-to-one map into 2-D can be a file, not a picture |
| **`ROUTE-TERMINUS`** | `docs/decisions/route_terminus_v1.md` | the decisions taken under governor delegation: close the readable-image line, re-designate, dispose of `GD6`/`GD9`/`GD10`/`GD11`, decide route governance and `G1` credit | **IN FORCE 2026-11-22** (`D-1`…`D-9`, each with its reversal condition). `GD6` (`φ` in `ME3`) **promoted to the critical path** — the canvas is missing a *coordinate* (`r`), not a metric, so no statistic can be the blocker. Phased v2 governs; the matrix is **frozen as the record of a closed line** (readable, not extendable). `G1` takes **no** credit from a `DEMO-1` frame. `MR1.0` now **necessitated**, not merely unqualified. Falsifier: exhibit one physical quantity other than `(M, N)` that the deposit determines |
| **`POC-1024`** | ruling `mr2d_potential_ruling_v1.md` §6 | the requested micro test case: `M = 4` shells × `256` layers, Hilbert order 5 on `32²`, occupancy `1.0000` | **ADOPTED — as a CODE test only, scope declared.** It **cannot be a scale model**: fixing `pieces` and `M` fixes `H_poc = 256δ = 5.504e-8 m` and `aspect = 3.058e-7` against a locked `1.2778` ([off by `4.179e6×`]). It abandons `pitch/δ = 1.861e9`, which is the entire content of `POT-TRICHOTOMY`. May not be cited about `DEMO-1` physics |
| **`SFC-INDEX`** | ruling `mr2d_potential_ruling_v1.md` §8 | the repositioned role of space-filling curves: a spatial index for neighbourhood search and cache locality, **not** the physical 2D map | **IN FORCE as a term, NOT as `σ`.** It indexes the **object**, not the canvas, so it is a different construction from `SIGMA-DEMO` and **may not be called `σ`**; unnecessary below `~10⁶` pieces, so not part of `POC-1024`. This is the correct use of an SFC and the first role assigned to one that survives the record |
| **`DIM-ANCHOR`** | ruling `dimension_anchors_ruling_v1.md` | the audit of the four dimension theorems offered as the terminus's foundation — Brouwer, Cantor, Hilbert, Kakeya — scored on (a) true, (b) attributed, (c) applicable | **RULING 2026-11-22, `16/18` (`P2`, `P8` refuted against me).** `0` prior occurrences of all four names in `docs/`. `A1` splits: the *invariant* half applies and gives `0 = 0`; the *domain* half begins "if `U` is an **open** subset" and fails on its first word. `A2` is the only anchor that applies — **vacuously, by cardinality**. `A3` is mis-stated (`1→2` described, `3→2` concluded; multiplicity `1` at every finite order). `A4` is a non-sequitur and is **struck**. **Conclusion held; foundation restated.** |
| **`DEPOSIT-DIM0`** | same, §3 | the deposit's topological dimension, and the gap to the dimension it appears to have | **MEASURED.** Domain and codomain are finite discrete spaces ⇒ Lebesgue covering dimension **`0`** on both sides ⇒ the bijection is a homeomorphism, `0 = 0`. Box-counting: slope `2` for `ε ≥ pitch` (occupancy `0.996299`; `P(2×2 box empty) = 1.88e-10`), slope `0` for `ε < pitch` (`N = pieces` constant). **A 0-dimensional space drawn on a 2-dimensional lattice** — the apparent dimension is the embedding's, and decimation `2¹⁶ → 2⁹` is what turns it into a picture. |
| **`MAP-TRILEMMA`** | same, §8 | the exhaustive classification of maps `ℝ³ ⊇ X → ℝ²` | **REGISTERED.** `1` of `3` classical classes is prohibited (continuous injective — Brouwer); a continuous surjection exists (Peano/Hilbert) and a bijection exists (Cantor). The deposit occupies a **fourth row none of them governs**: bijection between finite sets, address only, `0 = 0`. This table is what the four anchors were reaching for and supersedes their framing. |
| **`CARD-ONLY`** | same, §5 | a bijection exists because of cardinality, and its existence carries no geometric information | **MEASURED.** `#injections = C!/(C−N)!`; `log₂ = 1.3089e11` bits ≈ `16.4 GB` **to name one** — the same order as the `15.9408 GiB` deposit it describes. The rule `p = kN + n` costs **`0` bits** (two integers, `62` bits total). The deposit is cheap because `σ` is a *rule*, not a choice: the quantitative reason `σ` cannot be arbitrary data. |
| **`LOSSLESS-REFERENT`** | same, §8; amendment `D-2a` | "lossless" is undefined until its referent is named | **IN FORCE.** w.r.t. the **plate inventory**: exact (bijection, `4,279,069,764 → 4,279,069,764`, `15,897,532` free). w.r.t. the **object**: false (`I(canvas ; r₄) = 0`; `10` of `12` parameters never reach a site). The unqualified word is ambiguous between a true and a false claim, and the ambiguity **is** the difference between a file and a physical reduction. Any use must write `lossless (inventory)` or `lossless (object)`. |
| **`A4-GLOSS`** | same, §7 | the Kakeya gloss offered as an information bound, and struck | **STRUCK 2026-11-22.** The theorem (Wang–Zahl, 24 Feb 2025: `dim_H = dim_M = 3` for Kakeya sets in ℝ³; `n ≥ 4` open) states a property of a **set**, not of a **channel**. Read literally the gloss is **true of the deposit** — it holds no 3D geometry — so it corroborates `DEPOSIT-BLIND` and contradicts `A5`'s "lossless serialization" in the same breath. The deposit also contains **`0`** Kakeya sets: a finite set contains no line segment at all. Not citable. |
| **`ME3-DISP`** | `docs/decisions/me3_phi_disposition_v1.md` | the ruling that closes `GD6` and retires `ME3` | **IN FORCE 2026-11-22.** `8/11` predictions; `P2`, `P7`, `P8` refuted, all three **my** test-specification defects (`E1`–`E3`). Decisions `D-6a`, `D-10`, `D-11`, `D-12`. Also records `E4`: `route_completion_v1.md` §4.1 quotes `(λ/t)²` while its verified field gives `(λ/2t)²` — direction unaffected, mode undeclared. |
| **`SERIAL-CONF`** | `docs/decisions/deposit_serial_conformance_v1.md` | `deposit_serial_v1` conformance | **CONFORMANT 2026-11-22.** Spec locked sha256 `e3c2a555`. `A1` `0` mismatches (exhaustive `16,777,216` + `2,000,000` at `DEMO-1`, deduplicated); `A2` `17,116,279,056 B = 15.9408 GiB`; `A3` `1.000000` (`0` non-adjacent pairs in `16,777,215`) vs raster `0.999756`; `A4` median `1` with `3` wraps; `A5` `429 MiB/s`; `A6` `1,015 MiB/s`; `A7` `38 s`. `7/9` predictions; `S7`/`S8` refuted, both mine |
| **`SERIAL-ASYM`** | same, §3 | the format's encode/decode asymmetry, which I did not predict | **MEASURED.** Encode does `p // N`, `p % N` (integer division, ~20–40 cycles); decode does `w & 3`, `w >> 2` (~1 cycle). Ratio **`2.37×`** in decode's favour. Right way round for a file written once and read many times — and an argument for the bit-field layout that was not made when it was chosen |
| **`SERIAL-WORD`** | `docs/specs/deposit_serial_v1.md` §2 | the record layout | **LOCKED.** `word = (n << 2) \| k`, `k = p // N`, `n = p % N`. All `32` bits used, no padding ⇒ `A1`/`A2` exact by **count**, not by margin. Admissible bound is **`N ≤ 2^30`** (since `n ≤ N−1`), not `N < 2^30` — my `S8` prediction was wrong by one and the guard is correct |
| **`ME3-RETIRED`** | `me3_phi_disposition_v1.md` §0 | `ME3`'s status after `GD6` closed | **RETIRED 2026-11-22.** Reinstatable only for a **dynamic** unfolding route (`KIN-DYN`'s other class) **and** with a `u_⊥/u_∥` instrument; neither exists. `δ_E,max` is **unregistrable**, not open. |
| **`RAYLEIGH-NOFRAC`** | same, §2 | `δ_E` is a Rayleigh quotient, so it carries no amplitude and is not a "fraction" | **MEASURED.** Invariant under `φ → aφ` to `5.3e-13` over `12` decades of `a`. A fraction needs a total; the formula supplies none. So the criterion's name is the only thing that fixes its semantics — which is why the declaration is not a free choice. |
| **`THICK-FLOOR`** | same, §2 | what `ME3` becomes for any static `φ` | **MEASURED.** `δ_E = Cλ^k/t^k`, `k>0` ⇒ `δ_E ≤ δ_E,max ⟺ t ≥ t_min`. The admissible set is **upward-closed in thickness**; a flatness criterion must be downward-closed. At the real object (`λ=0.20 m`, `t=1.540e-14 m`) the quoted `1.69e26` implies `t_min = 1.5385e-14 m` — it passes by *being thicker than it is*. |
| **`SDF-DIVERGENT`** | same, §2 | the Euclidean level-set reading is unbounded | **MEASURED.** `∫_V(∂_zφ)² dV = ∫_0^∞ ∫_{φ=s} n_z² dA ds`, divergent in `s`. The L∞ variant avoids divergence but its gradient lives on **cones inside the body**, so `k = 0.433` — weak thickness dependence, weak discrimination. Neither is `R/t`. |
| **`VEL-VACUOUS`** | same, §3 | the kinematic reading cannot reject anything | **MEASURED.** On `u^μ=(c,0,0,0)`: as a **frame** ⇒ `0/0`; as a **flow** ⇒ `δ_E = 0` exactly. Either way the value is object-independent: variance across a sheet, a body and a column is **`0`**. Any positive `δ_E,max` admits all three. |
| **`D6-RETRACT`** | same, §5; amends `route_terminus_v1.md` | `D-6`'s promotion of `GD6` to the critical path | **WITHDRAWN (`D-6a`).** A category error: `δ_E` is one scalar per **configuration**; a site holds `(k,n)`. Two objects with `δ_E` differing `4×` give **one** deposit digest (`ba6dd50ce0b81bb7`) ⇒ `I(site ; δ_E) = 0`. Resolving `GD6` would have put nothing into a site. The critical path is `G6`/`DC2`, as `route_terminus_v1.md` §9 already says. |
| **`SC-ROUTE`** | `runs/OPTICS/sc_submission_verbatim.md` | the submission arguing `σ_s` is the 2-D **surface conductivity** (S), not a yield strength (Pa) | **PROPOSED — governs nothing. PARTIALLY ADOPTED** (`sc_route_ruling_v1.md`). Its central correction is right and **has no object**: `0` physics-sense occurrences of yield strength / plasticity / Poisson / Young's modulus in `docs/specs/`, `docs/conventions/` or the roadmap, and `0` bound to `σ_s`. Adopted: **Task C** (Ward / K-K / f-sum) — which finds two real defects — the derive-don't-assert direction, and §V's non-blocking rule. Refused: §I.1/§I.2 (`REPAIR-ABSENT`), the metric (`C²dz²`; record has `B²dz²`), `23.2 MeV` (revoked; `73.37`), and the reduction as a route to the target (`REDUCE-DOMAIN`) |
| **`REPAIR-ABSENT`** | `sc_route_ruling_v1.md` §0, §2.3 | a correction whose target reading is not in the record | **MEASURED, 2nd instance** (after round 31's `MR2-D`). §I.1 withdraws a "yield strength" reading that appears nowhere; §I.2 refutes a Poisson compensation that has no constitutive relation to compensate (`E`, `ν` absent; a `D2` deposit has `E ≡ 0`). A true statement against a claim the record never makes — same shape as `A4-GLOSS` |
| **`SC-OWNER`** | same, §1 | the record's owner of `σ_s` | **SETTLED.** Surface/sheet conductivity, SI `S`, *an input not a universal constant* (roadmap §6.4, `S10`). Zero stress-sense uses among all 54 occurrences. The submission's §II table is correct and changes nothing |
| **`SC-B`** | same, §2.1 | the symbol for the third-dimension scale factor | **`B`, and only `B`.** The record writes `B²dz²` in all three of its metric forms (§2.5, l.142, l.146) and `dℓ_z = B dz` (l.162). The submission writes `C²dz²` **and** calls `B` the scale factor — internally inconsistent; the prose is right, the metric is wrong |
| **`FSUM-SPLIT`** | same, §3.1; `runs/OPTICS/sc_route_results.txt` §F | the interband term's spectral weight | **MEASURED DEFECT.** The Drude term alone equals the f-sum total `πe²n_2D/(2m*) = 6.782282e18` at **every** `τ` (ratio `1.000000000003`; `τ` cancels), while the interband step `A·θ(ω−ω_g)` has **unbounded** weight — it alone exceeds the entire budget by `3ω_g`. Thus the amplitude is not "OPEN": the correct constraint is a **partition** `W_intra + W_inter = W_total`. **AMENDED v1.1:** not a bug but a theorem — a Drude pole consumes the whole budget *by definition* (`∫ = σ₀π/2τ = πe²n/2m*`, `τ` cancels, measured `6.9e-15`), so no amplitude can repair the partition. The parameter must be a fraction (`FSUM-FRACTION`) drawn from one declared Hamiltonian (`FSUM-SINGLE-SOURCE`) |
| **`KK-UV`** | same, §3.2 | Kramers–Kronig status of the record's model | **MEASURED DEFECT, band-limited.** A step in `Re σ` requires `Im σ = −(A/π)ln\|(ω_g+ω)/(ω_g−ω)\|`; the module supplies **none**. Residual `1.153` at `1.5e8 eV`, `0.638` at `2e8 eV` — but `≤ 1.2e-15` across the reported **1–3 eV** band, because the model there is pure Drude. Violation confined above `2E_F = 1.4674e8 eV`; diverges as `ω → ω_g`, so no amplitude repairs it, only a decaying lineshape. **AMENDED v1.1:** the root is the missing upper scale (`STEP-NO-SCALE`), and Lorentzian broadening does **not** remove it — `W_inter` grows linearly for every finite `Γ` (`FSUM-FINITE`). The only repair closing both `S4` and `S5` is a finite band edge / oscillator form |
| **`TAU-OBLIGATION`** | same, §5, §8 | what any future `σ_s` must state | **IN FORCE.** The record names the `G6`/`DC2` blocker as "a compliant `σ_s(ω)` with a **solved** `τ`" (2 files). The submission mentions `τ` twice, **both** `τ_xz`/`τ_yz` — shear stress — and *relaxation*/*collision*/*relaxation* **zero** times. A route ending at `σ_s` without saying what fixes `τ` reproduces `R5-L2`. **AMENDED v1.1:** strengthened to `S13`. Solved now means **named** (`TAU-KIND`), **traced** to a mechanism or a pole width, **not scanned** (`NO-TAU-SCAN`); and a Drude form must be *tested* by `DRUDE-DOMAIN`, not assumed |
| **`REDUCE-DOMAIN`** | same, §3, §4 | `σ_s = ∫dℓ_z σ_3D,∥` | **EXACT AND NON-REACHING.** Exact: reproduces `e²n_2Dτ/m*` to `0.0e+00` at `L_z = 1e-9..1e-7 m` (`n_2D := n_3D L_z`), so it **derives** `R5-L2`'s asserted ansatz. Non-reaching: needs many atomic layers, while the target is `d_par = 6.7420 fm = 1.274e-4 a₀` (v3) with bound states gone below `πa₀ = 1.66 Å` — the domain and the destination are disjoint |
| **`SC-SPEC`** | `docs/specs/surface_conductivity_v1.md` (v1.2, sha256 `ce2a5088…`, `runs/OPTICS/surface_conductivity_lock_v1_2.json`; v1.1 = `a005533b…`, v1.0 = `91eca7ac…`) | the conformance specification the submission recommended a reconstruction spec for | **LOCKED `CONDITIONAL`, v1.1 additive.** `S1`–`S9` byte-identical to v1.0; `S10`–`S13` added (`FSUM-SINGLE-SOURCE`, `FSUM-FINITE`, `DRUDE-DOMAIN`, `TAU-PROVENANCE`). Applied at once to the record's module: **S4, S5, S7 FAIL, S6 not attempted** — 3 failures in a module that passes its own `T1`–`T3`. No second specification, by governor decision |
| **`SC-2`** | governor acceptance 2026-11-22 21:01; `runs/OPTICS/sc2_submission_verbatim.md`; `sc2_lineshape_ruling_v1.md` | the acceptance of `PARTIALLY ADOPTED` plus four sharpenings | **ADOPTED, 11/12 predictions.** `P10` missed by `0.0087` and stays missed. Produces no `σ_s`; produces the tests and the cost of each repair |
| **`FSUM-SINGLE-SOURCE`** | `sc2_lineshape_ruling_v1.md` §2 | the total spectral weight must come from one Hamiltonian and its current operator; f-sum formulas from different models may not be spliced | **MEASURED.** `W_total = (e²v_F/8ħ)√(4πng)` ⇒ at fixed `n_2D`, `W(4)/W(2) = 1.414213562373` and `E_F(4)/E_F(2) = 0.707106781187` exactly. The module's `k_F = √(2πn)` **is** the `g = 2` choice and never says so. `S5` is **unstatable** until `(g, v_F, m*)` is declared |
| **`FSUM-FRACTION`** | same, §2.3 | the legal interband parameter | **DIMENSIONAL.** `A_INTER = e²/(16ħ) = 1.521334e-5 S = σ_min/4` exactly (`σ_min = e²/(4ħ) = 6.085337e-5 S`), with the `1/4` underived. A **height in S** cannot satisfy a **partition**; the parameter must be `f_j ∈ (0,1)` with `Σf_j = 1` |
| **`FSUM-FINITE`** | same, §3 | every channel needs an upper energy scale | **MEASURED.** `Reσ → A` as `ω→∞` for every finite broadening ⇒ `W_inter` grows linearly: at `Γ/ω_g = 1e-3` the broadened step already carries `4.50×` the whole budget at `10ω_g` and `49.5×` at `100ω_g`. A Lorentz oscillator instead gives `W = S_pπ/2` finite (`2.2e-16`) with a causal partner (`9.2e-8`). Bound on `R1-B1`: the band edge must lie below `Ω* = ω_g + W_total/A = 440.18 MeV` |
| **`STEP-NO-SCALE`** | same, §3.4 | the shared root of `FSUM-SPLIT` and `KK-UV` | **ONE ROOT, TWO SYMPTOMS.** Both are what the absence of an upper scale does — to the budget and to causality. A broadening parameter looks like it repairs causality while leaving the budget untouched, so the root must be named to forbid that fix |
| **`DRUDE-DOMAIN`** | same, §4.1–4.2; `sc2_results.txt` §C | whether a single-Drude reduction is admissible | **INSTRUMENT (`S12`).** `α = (4/π)arctan(−Imσ/Reσ)` at the peak of `−Imσ`, and the peak sits at `ωτ = 1` for every `α`; recovers `α ∈ {1, 0.9, 0.7, 0.5}` to `1.1e-16`. Sensitivity floor measured: an equal-weight two-pole sum at `τ₂ = 3τ₁` gives `α_eff = 0.9087` (misses `0.9` by `0.0087`, kept as a miss) with arc deviation `13.4%`; `α < 0.9` only for `τ₂/τ₁ ≳ 4`. **Both statistics required** |
| **`TAU-KIND`** | same, §4.3 | which `τ` a response is quoting | **QUANTIFIED.** Static TF 2D Coulomb, `\|V\|² ∝ (q+q_TF)⁻²`: `τ_tr/τ_sp = 91.5` at the record's `q_TF/k_F = 0.014596`, following `→ (2/π)(1/a)` to `1.0e-2` at `a = 1e-4`. Model attached: no dynamic screening, no vertex correction — so `91.5` is the **size of the ambiguity**, not a value of either `τ` |
| **`NO-TAU-SCAN`** | same, §4.4 (`S13`) | `TAU_SCAN` in `sigma_s_lindhard.py` | **FAIL under `S13`.** The scan may survive only as a labelled probe of the functional form (`T2`, `T3`), never as the response. Already labelled OPEN in the module header; the label is now a verdict |
| **`NO-GO-ADMISSIBLE`** | same, §6; spec §11 | what a null result means | **DECISION PRINCIPLE.** `G6` passing is not the objective. A finding of *no admissible stable matter state*, or of *no response satisfying `S1`–`S13`*, is a valid physical conclusion, same class as `G0` row 1's `NO-GO`. Corollary: **no forward selection** either — a matter branch may not be chosen because it makes the optics admissible |
| **`SC-3`** | governor review 2026-11-22 21:12; `sc3_registration.md`; `sc3_budget_ruling_v1.md` | the line-by-line review of SC-2 and its five sharpenings | **ACCEPTED, 14/17.** Three misses kept: `Q6b` (`v_F` 0.993 predicted, 1.000071 measured — my `k_F`), `Q9b` (band), `Q11b` (band). Instrument errors E1–E4 archived. Produces no `σ_s`. **AMENDED SC-4:** `E5` added — `Q2`'s printed pass came from a hardcoded `f_intra = 1.0` and a threshold below the quadrature floor; **governor ruling: `Q2`'s pass is revoked as evidence**, the identity-level conclusion stands (see `BUDGET-ENDPOINT`) |
| **`BUDGET-ENDPOINT`** | `sc3_budget_ruling_v1.md` §2; spec §10a.2 | what `440.18 MeV` is | **AN ENDPOINT, NOT A BOUND.** `ω_end(f) = ω_g + f W_total/A` measured at `f ∈ {0, 0.05, 0.25, 0.5, 0.75, 0.9, 1}` → `146.7400 … 440.1784 MeV`. At the module's own `f_intra = 1` the residual budget is `0.000000e+00`, so the admissible edge is `ω_g`. **AMENDED SC-4 (`E5`):** the zero is an **identity** (`sc2` §A.1 P1 — the module's pole takes the whole budget by definition), not a `1e-15` measurement; the registered threshold sat below the quadrature floor and `sc3_budget_check.py:87-89` hardcoded `f_intra_mod = 1.0`. The measured partition is `W_intra/W_total = 1.000000000003` (`sc_route` §F); `sc3`'s citation `1 − 7.1e-5` was the `m*`/`E_F` pinning slack (`sc2` §A.2), not a partition share. Register: `sc4_partition_citation_errata_v1.md`. **Scope (governor ruling SC-4):** the inadmissibility is a budget contradiction *within the module's construction* — not a claim that real matter lacks interband transitions; real interband response requires re-established redistribution from a microscopic model |
| **`THREE-OMEGA-G`** | same, §2.3; spec §10a.4 | the identity behind the ceiling | **EXACT.** `(W/A)/(2ω_g) = 2πn/k_F² = 1` given `k_F² = 2πn`, `m* = E_F/c²`; measured `2.999717`. `440.18 MeV = 3 × 146.74` carries no information about `n_2D`, `g` or `v_F`; **forbidden as an input to `R1-B1`** |
| **`FSUM-PAIR`** | same, §1; spec §10a.5 | `S4` and `S5` are separate verdicts | **INDEPENDENT, 2×2 POPULATED.** pure step (S4 pass / S5 fail), truncated step with the untruncated `Im` (fail / pass, residual `0.6194`), module as-is (fail / fail), oscillator (pass / pass). A band edge bounds the weight but does not fix `Im` |
| **`G-SPLIT`** | same, §3.2; spec §10a.3 (`S15`) | the two degeneracies inside one module | **MEASURED, FACTOR 2.** `A_INTER = e²/(16ħ)` is the `g = 1` single-cone height; `k_F = √(2πn)` is `g = 2`. Required height at `g = 2` = `3.042669e-05 S` = `2.000000000000 ×`. The underived `1/4` is `g/4` at `g = 1`: underived *because* inconsistent |
| **`V-F-IMPLIED`** | same, §3.3 | the velocity the record never wrote | **MEASURED.** `v_F = E_F/(ħk_F) = 1.000071 c` ⇒ a `v_F = c` Dirac model; `m* = 143.56 m_e` rebuilt vs `143.58` logged. The ceiling scales **exactly** with `v_F` (`3.33e-16` over four decades): at `c/300` it is `1.4673 MeV` |
| **`ALPHA-COLLAPSE`** | same, §4; spec `S12b` | what certifies one relaxation rate | **INSTRUMENT.** `α = 1` at a point is reachable by two poles (exact root at `ωτ₁ = 0.697897`, residual `1e-12`). The certificate is `max_ω \|α − (4/π)arctan(ωτ_eff)\| < 1e-6`: single pole `4.4e-16`, two-pole 3:1 `8.6e-2`. Law: `1 − α_peak = 0.078(ln τ₂/τ₁)²` to 11% for `τ₂/τ₁ ≤ 3` |
| **`ALPHA-BLIND`** | same, §4.4 | what `α` cannot see | **MEASURED NEGATIVE.** `f_intra ∈ {0.9, 0.75, 0.5}` → `σ₁(0) = {388.557, 323.798, 215.865} S` (ratio exactly `1.8`), but `α_peak = {1.038, 1.129, 1.201}`: `\|Δα\| = 0.162`. `α > 1` is a reliable not-one-pole flag; `α` cannot rank the partition |
| **`ACCEPT-NOT-IDENTIFY`** | same, §1, §7; spec §11.4 | what passing the criteria proves | **NOT A MATERIAL.** A `6×5` grid of `(ω_0, Γ)` at fixed `S_p` passes `S4` and `S5`, `30/30`. Passing `S1`–`S15` identifies a 2-parameter family, and leaves `f_intra` free |
| **`TAU-MODEL-DEP`** | same, §5 | `τ_tr/τ_sp = 91.5` | **TWO KERNELS, TWO ANSWERS.** `(q+q_TF)⁻²`: `91.548`; `(q²+q_TF²)⁻¹`: `138.016` — `+50.8%` at the same `q_TF/k_F = 0.007298`. A model output, not a material property |
| **`R1-B1`** | same, §7 | the interface the optics stage is blocked on | **EIGHT ITEMS, 4 + 4.** returns `(n_2D, g, v_F, ω_end)`; must also declare the scattering mechanism, the Drude-domain evidence, current operator/matrix elements, and `f_intra`. Items 1–4 are necessary and measurably insufficient (`Q11`, `Q12`). **AMENDED R40:** delivered via `R1B1-P4` under `docs/specs/R1_B1_Microscopic_Matter_Model_v1.0.md`; all eight items are *tagged outputs* of the microscopic model, never inputs (see `SRC-TAG` and that spec's §4.3 baseline re-classification) |
| **`P1-OUTCOME`** | `docs/decisions/r1b1_p1_closure_certification_v1.md`; declarations `runs/R1B/r1b1_p1_declarations_v1.md` | the `R1B1-P1` outcome under the three-outcome interface | **OUTCOME #1 — THEORETICAL CLOSURE CERTIFIED (round 44).** All seven `P1-CLOSURE-FAIL` conditions assessed clear (with named limitations, not hidden ones): DOF inventory closed; the five derivations hold; `Ĵ`/`T^μν` consistent (Noether-identity level; the component-level current check is a recorded **instrument defect** — y-sector residual traced to `(γ⁰γ²)ᵀ = −(γ⁰γ²)`, physics stands on the round-43 master identity); conservation conditions stated; the `P1-C` interaction class declared with literature-grounded domains (BPS/BBP/NV + χEFT) **containing** the target regime; the five-point integrated-out accounting adopted. **Certifies the theory spec, not a state; the numerical veto is NOT lifted** — `R1B1-P2` registered pending the veto-lift adjudication |
| **`R1B1-PHASES`** | `docs/specs/R1_B1_Microscopic_Matter_Model_v1.0.md` §13.2, §15; trigger `docs/R1B1.md` §7 | the six R1-B1 phases | **`R1B1-P0` spec (v1.1, round 41) → `P1` minimal closed microscopic model → `P2` static state/EOS → `P3` dynamic reachability → `P4` microscopic current response → `P5` into `G6`/`DC2` under `S1`–`S15` v1.3, not relaxed.** Qualified labels mandatory: bare `P0`–`P4` are Layer-A numerical stages. **AMENDED R45: the veto LIFTED (governor) and the staged chain EXECUTED** — `P1` closed (outcome #1, `P1-OUTCOME`); `P2` **9/9 PASS** (bounded, causal, stable states across the `K1` window; the `L_z`-resolved envelope); `P3` **6/6 PASS** (`p_z` exactly conserved; spinor adiabaticity `2.4e21`; one self-caught theorem retraction archived); `P4` the response **constructed from the solved state** — the interface tuple DERIVED (`n_free,2D ~ 1.0e-3 fm^-2, g=2, v_F ~ 0.033c, omega_end ~ 5.1e23 rad/s`), **`f_intra = 1.52e-3`** by the five-step decomposition, the TRK deficit quantified (0.9975 — the five-point item 5 answered); the candidate **ADMISSIBLE (S7 conditional)**. `P5`: the `G6`/`DC2` blocker resolved at the model level — the status flip submitted for adjudication (`r1b1_p4_p5_closure_v1.md`) |
| **`P1-CLOSURE-FAIL`** | same spec §15.3 | the hard veto on `R1B1-P1` numerics | **SEVEN CONDITIONS, ANY ONE VETOES.** DOF set not closed · action cannot yield matter + EM equations simultaneously · `Ĵ` inconsistent with `H` · `T^μν` inconsistent with the geometric coupling · conservation laws rest on unstated assumptions · interaction model exceeds its declared domain · no treatment of integrated-out DOF spectral weight (amended round 42: a **five-point EFT review** — energy/stress · `Ĵ` corrections · effective interactions · conservation/Ward · spectral weight with high-energy compensation; an `f`-sum compensating term alone does not close an incomplete low-energy theory). Purpose: closure, not simulation-as-fast-as-possible |
| **`B-WORK-TERM`** | `runs/R1B/r1b1_p1_closure_review_v1.md` §2 (`R3`), §8; check `r1b1_p1_closure_check_results.txt` §R3 (8/8 VERIFIED) | how the prescribed `B(t)` exchanges energy with matter | **DERIVED AND CHECKED, NOT ASSUMED.** `∇_μT^{μt} = ∂_tρ + (Ḃ/B)(ρ + p_z)` — only the z-stress couples (in-plane scale factors are static); integrated: `dE_area/dt = −Ḃ·p_z·Δz` per unit lateral area over coordinate slice `Δz` (round-42 figure = the `Δz = 1` case — normalization explicit per governor round-42 §I). Coordinate-split form `S^t_bg = −(Ḃ/B)(ρ + p_z)` (the governor's `S^ν_background`) vs local covariant form (no `S` term) — both derived, never mixed; `S^t_bg` is the connection/measure term moved to the RHS, **not an independent source in the action**. Also derived: transverse EM damping `−(Ḃ/B)E_⊥` — **geometric redshift/dilution, NOT dissipation** (coordinate-component statement; Phase 3 tracks orthonormal-frame fields); the `(Ḃ/B)` friction; `1/B²` z-weights. `Ḃ = 0 ⇒ dE/dt = 0`; `B ≡ 1 ⇒` flat recovery — both checked |
| **`DIRAC-KINEMATIC`** | `runs/R1B/r1b1_p1_dirac_closure_v1.md`; check `r1b1_p1_dirac_check_results.txt` (**11/11 VERIFIED**) | the Dirac operator on the `B(t)` background (governor 9-step order, round 43) | **MECHANICALLY DERIVED.** Tetrad `(dt, dx, dy, B dz)`; spin connection `ω_z^3_0 = ω_z^0_3 = Ḃ` only; curved `γ^z = γ³/B`; `Ω_z = −(Ḃ/2)γ⁰γ³` **uniquely fixed** by `∇_μγ^ν = 0` (16/16; opposite sign fails); **EOM form fixed by the mass shell** — `(iγ^μD_μ ± m)` rejected (`H² = p² − m²` unphysical in this signature, archived), physical form `(γ^μD_μ + c_m m)ψ = 0`; `H_D = −(α_xp_x + α_yp_y + (α_z/B)p_z) + ic_mγ⁰m − (I/2)(Ḃ/B)𝟙` with the identity term **extracted from Tr(H)/4** — measure compensation (norm `∫Bψ†ψ` conserved; FLRW `−(3iH/2)𝟙` analogue, `n = 1`), **not dissipation**; `p_z` a good quantum number (`[H_D, p_z] = 0` — no z-mode mixing; round-42 wording superseded); gauge convention `ψ' = e^{+iqλ}ψ`, `A' = A − ∂λ` declared+verified; both limits verified. Kinematic-level only — dynamical closure still gated on `P1-C` |
| **`N7-SPLIT`** | same spec §4.2 (v1.1) | the `n_2D` slot split | **`n_Q,2D ≠ n_free,2D`.** `n_Q,2D` = total charge areal density (bookkeeping `Z_A·N_B`); `n_free,2D` = free-carrier areal density — what the Drude weight is actually a functional of; trapped/bound/ionized components registered separately. Total charge conserved ≠ free electron number conserved (trapping/release/transfer at fixed charge). `N7` is a constraint **solved from the microscopic state**, never a pre-assigned fraction |
| **`R1B1-SYMBOLS`** | same spec §0.3 (v1.1) | the R1-B1 symbol table, binding from `P1` | **`d_carrier` / `d_nuc` / `L_z` / `B(t)` / `n_B` / `N_B` / `n_Q,2D` / `n_free,2D`.** `d_par` and `d_∥` are deprecated inside R1-B1 documents (citable only with verdict-v3 §2 definitions): the `6.7420 fm` / `15.40 fm` / `K1`-window object confusion is fixed at the symbol level, not by prose |
| **`S-STATE`** | same spec §7 | the six stability acceptance classes | **SIX EVIDENCE CLASSES, NOT SIX THRESHOLDS.** 1 conservation · 2 energy bounded · 3 linear stability (geometry-side analogue `P2-C6` still outstanding) · 4 nonlinear · 5 dynamic reachability (Phase 3; a state the compression cannot reach is marked unreachable, not passed) · 6 metastable lifetime vs the declared observation timescale (`UNRESOLVED` — must be declared before any metastability claim). **Fourth live `S` family — never cite bare `S`** |
| **`SRC-TAG`** | same spec §0.1 | the source-type tag on every R1-B1 output | **`DERIVED` / `MEASURED` / `ASSUMED` / `FITTED` / `UNRESOLVED`.** Exists because of `E5`: the module's `f_intra = 1` was a construction input posing as a measured quantity. An honest `UNRESOLVED` always beats a forced value; a tag changes only by recorded re-derivation, never by relabelling |
| **`SC-3-ERR`** | same, §6 | my own errors this round | **E1** polarity inverted in 5 cells (archived); **E2** oscillator `S5` threshold `1e-10` against a `1e-8` quadrature floor (3rd instance); **E3** law test mixed a Dirac numerator with a module denominator (`9.45e-5` spurious); **E4** a fabricated `sha256` in the v1.2 lock's `supersedes`, caught by cross-checking the v1.1 lock, replaced with `a005533bf3c5…` |

## 3. Collisions found beyond the one reported, and their dispositions

1. **`C` three-way (the reported one).** Resolved: constraints keep C; §6.1's criteria → **CM1–CM4**; localization
   test IDs → qualified as `LOC-C1 … LOC-C7` in prose (§4).
2. **The proposed `K1–K4` was doubly unavailable.** (i) Its *content* does not match §6.1 (see §7) — the four
   items listed were the enhancement techniques, not the criteria. (ii) The *label* `K1–K4` was **already in use**
   by the sci-fi boundary's four consistency checks (thickness window, confinement field, wall pressure, energy —
   `scifi_boundary_v1.md` §16–80, `internal_consistency_v1.py`, archived output in `runs/ANALYSIS/`), and `K` is
   additionally the trace of the extrinsic curvature throughout the CMC work. Adopting it would have created a
   *third* meaning for a letter that already had two. Found by `symbol_lint.py`, not by inspection.
3. **`L` — three-way, and the worst of the set.** Three live meanings: optics layers L1–L4 (§6.2), presentation
   **fidelity levels** L1–L3 (decision statement, §F.8), and the **R2-D redshift layers** L1–L3 (§4:
   free-particle geodesic baseline / collision-thermalisation response / full `T^{μν}` feedback). The R2-D labels
   are embedded in **file paths** (`pz_l1.py`, `pz_l2_relaxation.py`, `r2d_l1_results.txt`) and in archived stdout,
   so a global rename would break §9.1 reproducibility — strictly worse than the ambiguity. **Disposition: staged,
   not renamed.** Mandatory in new text: `FL1–FL3` for the fidelity ladder; and always qualify in prose —
   "fidelity L1" / "optics L1" / "R2-D L1". The fidelity ladder was moved first because it is the newest and
   cheapest; §F.8/§F.9 of the roadmap were converted to `FL1`/`FL3` in this round.
4. **`B` — sweep parameter vs module-B test IDs.** The sweep parameter is physical and older; the tests move.
   Disposition: prose says `LOC-B0 … LOC-B7`; archived stdout keeps `[B0]`.
5. **`C_geo/C_phys/C_info/C_top` in the v0.1 draft.** Under R4 these are non-compliant on arrival. The audit
   already recommended replacing them; the registry now makes the *naming* mandatory independently of whether
   the *content* is adopted. **Resolved 2026-11-22:** all four are **retired** (ruling D-B), replaced by
   `ME1`–`ME5`, and `C_info` is **dissolved** — its injectivity content to `ME1`, its magnitude to a
   non-gate budget (`BUDGET-1`). The retired names may not be reused for any content, old or new.
6. **`ε` — three-way and unresolved.** Registered OPEN, with the audit's recommendation (`ε := 1 − φ_conv`, registered
   as converted proper-volume fraction; keep `B` as the physical parameter).

## 4. Errata for archived texts (never edited — §9.1)

| Location | Bare symbol | Means | Does **not** mean |
| --- | --- | --- | --- |
| `runs/R4/r4_instability_localization_results.txt` | `[C1]`…`[C7]` | localization diagnostics | constraints C1–C3 |
| `runs/R4/r4_instability_localization_stage2_results.txt` | `[C6]`, `[C7]` | same | same |
| `runs/R4/r4_axisym_2p1_results.txt` | `[B0]`…`[B7]` | module-B tests | the sweep parameter B |
| `runs/S45/meff_boundary_probe_results_v1_LABELS_P.txt` | `P1`…`P6` | probe checks | gates P1a / P2 |
| roadmap §6.1 as published before 2026-11-22 | `C1`–`C4` | contrast criteria | now `CM1`–`CM4` |
| roadmap §F.7.4 prose (corrected) | `LOC-C1`, `LOC-C4` | localization tests | constraints |
| `runs/P1/phase1_symbolic_constraint_results.txt`, `runs/P1/phase1_symbolic_constraint_registration.md` | `K²−K_ijK^ij` | `0` identically, for every `f(t,x)` in the ansatz — `[IDENT — no constraint information; see AX-01 HIGH-3]` | a constraint that was imposed and passed |

**Registration `R-IDENT-1` (2026-11-24, governor directive G-71-01 §1.3).** The annotation string
`[IDENT — no constraint information; see AX-01 HIGH-3]` attaches to every citation of
`K²−K_ijK^ij = 0` that presents it as a *verified* or *satisfied* constraint in the Phase 1 ansatz
`ds² = −dt² + dx² + dy² + f(t,x)²dz²`. `K_xx = K_yy = 0` and `K_zz = −f f_t` make the two sides equal for
arbitrary `f`, so the term cannot fail and carries no constraint information; the Hamiltonian constraint
reduces to `R⁽³⁾ = 2κρ`. Phase 1's own self-test `SY2` already labels it `IDENT`, and `IDENT` is not counted
as evidence (`G0p_seven_row_verdict_v3.md` §4).

The four in-record locations, and their dispositions under this registry's §9.1 rule that archived output is
never edited:

| location | status | disposition |
|---|---|---|
| `runs/P1/phase1_symbolic_constraint_results.txt` (`K^2 - K_ijK^ij = 0`; `IDENT SY2 PASS`) | `SEALED` (round 63) | annotation carried by `runs/RR-DT/rr_dt_01_record_repair_results.txt`; bytes untouched |
| `runs/P1/phase1_symbolic_constraint_registration.md` (§2 item 2, `SY2` row) | `SEALED` (round 63) | as above |
| `runs/PROGRAM/governor_digest.txt` (round-63 detail line) | `GENERATED` | rewritten from the ledger on every audit run; a hand annotation would be overwritten, so it is carried by the repair record instead |
| `docs/decisions/r4_finite_region_geometry_v1.md` §B2 and §2 | `NOT ANNOTATED` | **reviewed and excluded**: that document's `R + K² − K_ijK^ij − 2κρ` is a *machinery* evaluation on a CMC slice (`K_ij = (K/3)γ_ij`, `K` const), not the ansatz identity, and it is not presented as a constraint the programme satisfied |

The operator's generic definition in `DCC_Covariant_Reconstruction_v1.md` is not an annotation target: it
defines the Hamiltonian constraint, and never reports it as passed.

## 5. Formal disambiguation rules for derivations and audits

**S1 — declare the domain before use.** Every derivation opens by fixing the variable domains, which are
**disjoint by construction**:

- `∀ c ∈ Constraint_Set = {C1, C2, C3}` — predicates over the evolution of `(γ_ij, K_ij, T_μν)` and the ADM
  constraints. A constraint may never be evaluated on an observation channel.
- `∀ m ∈ Contrast_Set = {CM1, CM2, CM3, CM4}` — predicates over observation and rendering channels (source
  term, response, observer). A criterion may never be used as a boundary condition on the metric.
- `∀ e ∈ Branch_Set = {ME1, …, ME5}` — predicates deciding **membership of `ℳ_eff`**, the S3→S4 branch's
  domain. An `ME` predicate may never be a chain constraint, and may enter the S0→S2 solve only as typed
  boundary data (`PROV-3`).

This disjointness is not cosmetic: it is what stops the recurring inference error of using a *visibility* result
to discharge a *constraint* (or the reverse), and now also of using a *branch boundary* to discharge a *chain
constraint*. C3's NO-GO, for example, is a statement about the action and cannot be softened by any CM statement,
because CM predicates have no `T_μν` dependence — nor by any `ME` statement, which delimits only where the
branch's approximation is valid, not what the matter does.

**S1a — exception, registered 2026-11-22: `ME1` is a `CM` predicate.** The disjointness claim above is true of
`C1`–`C3` against `CM1`–`CM4`, and it is **false of `ME1`**. `ME1` is `μ_ov ≤ δ_ov` with `μ_ov` evaluated at a
declared depth resolution `Δz_res`; for any object whose columns hold one material interval it reduces to
`[thickness ≥ Δz_res]`, and `CM1` is `d ≪ λ` — the same predicate under `λ ↔ Δz_res` (audit V2a, 9/9 agreement).
`ME1` therefore measures an object **by an instrument**, which is what the `CM` set is for.

This is recorded as a *defect in the domain assignment*, not in `ME1`'s intent. Two consequences bind new text:

1. Any use of `ME1` states the instrument resolution `Δz_res` and the fact that the verdict is relative to it;
2. `ME1` may not be cited as evidence that an object *is* two-dimensional — only that it is thin compared with a
   stated resolution. The inference "ME1 passes, therefore 2D" is the error S1 exists to block, and `ME1` is the
   one label where S1 does not block it by construction, so it must be blocked by this sentence.

**S2 — bare-symbol rule.** Bare `C1`, `C2`, `C3` are **legal** (sole ownership). Every other enumerated label in
§2 must be written with its prefix. Bare `L1`, `B1`, `K1`, `P2` in new text is non-compliant.

**S3 — conflict detection is a hard check, not an aspiration.** Symbol conflict is itself an audit item. A text
that uses a bare symbol from a namespace it does not solely own is **logically non-compliant and returns for
correction** — including the case where the *same* bare `C1` appears in both a thermal-budget pseudo-colour
derivation (CM domain) and a column-conservation derivation (constraint domain). Enforcement per §6.

**S4 — one letter, one owner, forever.** Adding a second meaning to `C` requires an explicit registry amendment
with a governor decision, not a local convention.

**S5 — qualify the family when families co-occur.** Where labels from two families share a letter in one
passage, write the family on first use: `Gate:M4`, `Constraint:ME4`, `Painting:M2`, `Metric:M3`. The qualifier
is required only where ambiguity is live, but it is required there — a sentence like "M4 fails" is
non-compliant because it does not say which of the five `M4`s it means. (Adopted from the 2026-11-22
submission, which proposed the `Gate:`/`Constraint:` pair for exactly this reason; extended to all `M` families
after §2a showed there are five.)

**S6 — constraints are never written in a gate label.** A relaxation commit declares its subject in constraint
space (`C1`/`C2`/`C3`) or in gate space (`ME1`…`ME5`); if in gate space it also declares the constraint it proxies,
or `proxy: none`. Form: `moves: C1 via ME1@Δz_res` · `moves: ME2 (proxy: none — presentational)`. The crosswalk and
the relation types (`⇒ᵍ`, `⇒ᵒ`, `⊥`) are in `docs/conventions/constraint_crosswalk_v1.md`.

**S7 — a relaxation must be booked where it operates (amended 2026-11-22).** Original wording: *a proxy
relaxation is a constraint relaxation in effect*, because `ME1` was `C1`'s only enforcement for branch products.
`GD1` Option B removed that premise by reclassifying `ME1` as `CM5`, an observation predicate. The rule now
reads: **relaxing a predicate in the `ME` domain is booked as a constraint relaxation** (`moves: C1 via …` or
`proxy: none`); **relaxing a predicate in the `CM` domain is booked as an observation-strength declaration**
(`moves: none (observation channel)`) and may never be cited as evidence that a constraint was relaxed. The
asymmetry is the point: `CM` predicates are evaluated at instrument parameters, so their tolerances are
instruments, not physics. Phase 1 (`δ_ov`) is booked under the second form.

**S8 — `⊥` is a result, not a gap.** Where the crosswalk records `⊥` (no expression of a constraint in the gate
vocabulary), no label may be invented to fill it without a definition that (i) decides the constraint on a pair of
states differing **only** in that constraint's content, and (ii) survives the domain test of the crosswalk §2. A
`CM` label that cannot separate those states is not an expression of that constraint, whatever it is called.

**S9 — a locked symbol cannot be renamed without voiding the lock, and the collision is then a finding, not an
edit. Scope is decided by the digest, not by the symbol.** Registered 2026-11-22; **scope clause added the same
day on governor ruling** (`docs/decisions/t1_t2_t4_s9_execution_v1.md` §4). The four tier quantities were declared
inside `TIER-LOCK` as `Q0`, `Q1`, `Q2`, `Q3`, and `Q1`–`Q3` were already owned by the six checks of
`meff_boundary_probe` (registry §2, "audit only"). Three of four collide. S9 is the **sole** rule for this, applied
in two scopes:

**(a) Locked scope — frozen.** A symbol is *locked* iff it is covered by the sha256 a document records for itself,
here `runs/MATRIX/threshold_lock.json` (`tiers[*].quantity_b`, and the symbols appearing in `tiers[*].definition_a`):
`Q0`, `Q1`, `Q2`, `Q3`. Renaming any of them changes the digest and refuses every tier on `(c)`. Not permitted
under any authority short of a **v2 lock with a new digest**, which requires the governor's instruction and a
pre-registration written before any data are shown.

**(b) Unlocked scope — renaming is free.** Every other symbol, including the `Q1`–`Q3` of `meff_boundary_probe` and
every symbol in `C`/`ME`/`CM`/`S`/`D` families that no digest covers, may be renamed by ordinary registry edit. S9 no
longer blocks a clean namespace: the *probe's* labels are unlocked and may move, while the *tier's* labels may not.
Both owners are still recorded, and in active text a locked symbol must be disambiguated in place (`Q1`-as-tier vs
`Q1`-as-probe-check, or `Q1` with its scope spelled out).

**(c) The coupling that survives (b).** An unlocked rename **must not change the computation path of any locked
quantity**. "Computation path" is made checkable rather than asserted: `src/common/locked_path_guard.py` records the
pair (digest of `src/route/structure_tiers.py`, digest of `runs/MATRIX/structure_tiers_results.txt`) as `LOCKED-PATH`,
and the only admissible change is *source moved, numbers identical* — which is exactly what a rename produces.
Numbers moving while the source stands still is `DRIFT`; both moving is `BLOCK` and requires a new lock. So the
governor's sentence is enforced, not merely written.

The general rule: where a lock exists, a naming defect becomes a versioned finding, never a patch — **but only for
the symbols the lock actually covers.**

**S10 — a construction whose defining relations compose to the identity selects nothing, and may not be registered
as a selection principle.** Registered 2026-11-22 (`reports/reviews/eff_dim_claim_A6_v1_audit.md` §3). The test is
mechanical: substitute the definition into the criterion and check whether the result is the identity in the
argument. If it is, the criterion is satisfied by every value and cannot pick out the one it is presented as
picking out.

Four instances have now been convicted, which is why this is a rule rather than a caution:

| Construction | Composition | Consequence |
| --- | --- | --- |
| `ME2` `δS_eff/δφ = 0` | computes out to the Euler–Lagrange equation | vacuous — it *is* the equation of motion |
| `ME3` `ΔS_vN ≤ κ A_eff` | algebraically identical to `C_info` (relative difference `0.0`) | not a second constraint |
| `ME4` `dχ/dt = 0` "except at phase transitions" | the escape clause accommodates `1000/1000` adversarial cases | unfalsifiable |
| A.6's `k = k_max(E_1(k))` | `k_max = (ħc/E)/δ`, `E_1(k) = ħc/(kδ)` ⇒ `id`, to `2.2e-16` over `k ∈ [0.1, 1e4]` | "the largest `k` at its own freeze-out energy" is true of every `k` |

The rule bites at registration time, before any number is quoted: a submission whose central quantity survives
substitution unchanged is declined as a *definition*, not re-toleranced.

## 6. Enforcement

`src/common/symbol_lint.py` scans `docs/`, `reports/`, the roadmap, and `src/` for every label in §2, classifies
each hit as `OK` (prefixed or sole-owner) / `MUST-FIX` (bare, ambiguous, in active text) / `ARCHIVE` (inside
`runs/`, where §9.1 forbids editing), and prints a per-namespace tally. It is a **report**, not a gate: it produces
no physics verdict and its exit code is always 0.

A second linter enforces the *provenance* split (governor ruling D-A), not the labels:
`src/common/provenance_lint.py` → `runs/CONVENTIONS/provenance_lint_results.txt`. It requires every new run
product to declare `PROVENANCE: CHAIN-EVIDENCE | BOUNDARY-INPUT | NEITHER`, and flags the one error the split
exists to prevent — a branch product promoted to chain evidence. Grandfathering is by frozen manifest
(`runs/CONVENTIONS/provenance_baseline.txt`), not by date.

## 7. Correction to the instruction that produced this registry

Recorded prominently because the failure mode is exactly the one the registry exists to prevent.

The instruction proposed `K1 = Band migration`, `K2 = Pseudo-colour`, `K3 = Contrast stretching`,
`K4 = Shadowgraph / transmission`. **Those four are not the §6.1 criteria.** They are the *enhancement techniques*
listed in the decision statement's L1 row and §1. The actual §6.1 criteria are:

| §6.1 | Actual content | Proposed K-label | Match? |
| --- | --- | --- | --- |
| C1 | Thickness distinguishability (`d ≪ λ`) | K1 = Band migration | **no** |
| C2 | Optical contrast (reflection/absorption/scattering) | K2 = Pseudo-colour | **no** |
| C3 | Self-emission (thermal / non-thermal) | K3 = Contrast stretching | **no** |
| C4 | Visual threshold (retinal signal) | K4 = Shadowgraph / transmission | **no** |

Registering the proposed mapping would have written four wrong definitions into the "single source of truth" — a
registry that mislabels is worse than no registry, because it is authoritative. The four enhancement techniques are
real and are registered separately as `EN1–EN4`.

Additionally, **`K` was not available**, for two independent reasons: (i) `K` is the trace of the extrinsic
curvature throughout the CMC/R4 work (`K = const`, `|K|`, `K_STEP`, `Kcc`), so `K1–K4` would read as four values of
the mean curvature; and (ii) **`K1`, `K2`, `K3`, `K4` are already the four consistency checks of the sci-fi
boundary** — thickness window, confinement field, `z`-wall pressure, energy — defined in `scifi_boundary_v1.md`
(rows R1/R3 and the K-column of its summary table) and computed in `src/analysis/internal_consistency_v1.py`, whose
output is archived. Reusing them would have contradicted a decision record *and* an archived run at once.

**`CM1–CM4` was adopted instead** — the second of the two options offered in the instruction, chosen by applying
the registry's own rule rather than by preference.

## 8. What this registry does not do

- It does not edit archived run outputs (§4 errata instead, per §9.1).
- It does not resolve `K`'s internal overload (trace of `K_ij` vs continuation index `K_STEP`); recommended
  practice is to write `K_tr` where the trace is meant, registered OPEN.
- It does not adopt `ME1–ME5`; that is a content decision on audit F1–F11, separate from naming.
  **Amended 2026-11-22:** `ME1–ME5` **is** now adopted, by governor ruling D-B — but by the content decision,
  not by this registry. The registry supplies the names; `docs/specs/meff_boundary_v0_2.md` supplies the content.
  `ΔH` was demoted to a non-gate budget (`BUDGET-1`): it may be reported, never scored.
- It changes no numerical verdict, no threshold, and licenses no visibility conclusion (§11.1/§11.2 unchanged).

---

*Content generated by AI*
