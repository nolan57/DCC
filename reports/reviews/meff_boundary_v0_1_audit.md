# Audit — M_eff boundary specification, draft v0.1

**Audited text**: `docs/specs/meff_boundary_v0_1.md` (S3→S4 branch, draft v0.1, submitted 2026-11-22)
**Method**: clause-by-clause comparison against the registered record, plus a pre-registered arithmetic probe
(`runs/S45/meff_boundary_probe_registration.md` → `runs/S45/meff_boundary_probe_results.txt`, 6/6 criteria met).
**Evidence level**: IDENTITY / ARITHMETIC. This audit adds **no** physics result and **no** numerical verdict.
**Closure**: **CLOSED 2026-11-22.** Rulings D-A and D-B in `docs/decisions/meff_boundary_disposition_v1.md`;
adopted spec `docs/specs/meff_boundary_v0_2.md`; see §E for the disposition table and two corrections to this
audit's own wording.

---

## Verdict

The draft is **well-aimed and structurally sound, but three of its four constraints do not do the work assigned
to them, and the one thing that actually governs L3 is absent.**

| # | Constraint | Verdict | Governing evidence |
| --- | --- | --- | --- |
| — | Overall architecture (4 constraints over `(x,t,ε)`, boundary + citation rules) | **ACCEPT** | correct target: it addresses exactly the ledger's S4 row ("C2, C1 relaxed to minimal set; C3 only held") |
| `C_geo` | geometric / curvature | **REJECT as formulated** — not independent, and vacuous wherever defined | Q3 identity to 0.0; Q4 δ_geo = 3.4e-18 (plate) / 1.1e-3 (fingertip ridge) |
| `C_phys` | action-ratio truncation | **REJECT as formulated** — ratio of an indefinite quantity; needs a positive-definite norm | analytic (F5) |
| `C_info` | information loss | **REJECT as formulated** — unattainable by 8.7 decades; "lossless reconstruction" is not implied | Q1 ratio exactly 10.0; Q2 ΔH = 4.99e20 bit |
| `C_top` | topological invariance | **REJECT — falsified by the project's own census** and directionally inverted | Q5 χ ratio 5.9e9; holds on measure 8.5e-11 |
| §3 | citation conditions | **PARTIALLY ACCEPT** — condition 3 is right in spirit, conditions 1–2 are not currently evaluable / near-vacuous | F6, F7, F8 |
| §4 | relationship statement | **ACCEPT with a required qualifier** | F6 |
| — | lifetime / survival of the sheet | **MISSING — the decisive omission** | Q6, exactly 1/√2 for every L |

**Bottom line**: the draft specifies a boundary for a *mathematical* approximation regime, but the boundary that
actually binds L3 is a **clock**, and none of the four constraints mentions time except through ε.

---

## A. What the draft gets right (recorded before the criticisms, because it is real)

1. **It found a genuine gap in the registered ledger.** §9 of `staged_relaxation_visual_route_v1.md` says branch
   products "may not be cited as evidence for the chain" — without distinguishing *boundary data* from
   *validation evidence*. The draft's §3/§4 draws exactly that distinction, and it is needed: S2's solve will
   require outer/asymptotic data, and refusing that data outright would make S2 unsolvable. **The distinction is
   correct and I am adopting it** (F6).
2. **It makes `M_eff` a first-class object with an explicit membership test.** The ledger previously said only
   "C1 weakened to a minimal set" and never defined the minimal set. That is a real advance in specificity.
3. **It demands registered tolerances before use.** Three of the four constraints are written with explicit δ's
   rather than prose adjectives. The defect is that the δ's are unnumbered, not that they exist.
4. **Condition 3 (non-circularity) is the correct instinct**, even though its example is misplaced (F7).

---

## B. Findings

### F1 — CRITICAL: no constraint tests single-valuedness, and that is the whole content of relaxing C1

`C_geo` and `C_info` both presuppose a height field `z = z(x_i)`. Writing `z(x_i)` **assumes** that the object is
a graph over the base — i.e. that every column contains exactly one surface point. That assumption is precisely
what the 3D object violates, and it is the boundary the branch exists to locate.

Consequences:

- `C_geo` bounds the *curvature of an already-assumed graph*. A function with small second derivative can still
  be steep; a graph can still have total occlusion where it doubles back. Curvature is a shading/parallax
  smoothness criterion, not an occlusion criterion.
- Occlusion is **all-or-nothing**, not a tolerance: at 550 nm with a diffraction-limited aperture the sampling
  scale is ~λ/2 ≈ 275 nm, while any macroscopic object has height variation ≫ 275 nm. So the correct occlusion
  statement is not "R_⊥ ≫ λ_obs is nearly satisfied" but "the object overlaps itself completely at the sampling
  scale" — a discrete fact about injectivity.
- `C_info` inherits the same defect: ΔH is defined as the information the *projection* loses, which is only
  meaningful once you have agreed the projection is of a graph.

**Required fix**: add an explicit injectivity constraint (ME1 in §C) and demote `C_geo` to a slope criterion at the
declared sampling scale. Note this also makes the draft's `C_info` claim — "the 2D visualization remains
topologically equivalent to the 3D physical state" — simply false as written: a 2D projection is not topologically
equivalent to a 3D body (they differ in the top homology group's rank by construction). What is true is that a
*graph* is homeomorphic to its embedded image, which is F1's condition, not an entropy condition.

### F2 — CRITICAL: `C_info` is unattainable by 8.7 decades, and its "lossless reconstruction" clause does not follow

Measured (Q1, Q2), at the registered object (`A_⊥ = 0.040 m²`, `H = 1.75 m`):

| quantity | value |
| --- | --- |
| ΔH/A at atomic resolution (a₀) | `1.248×10²² bit·m⁻²` |
| ΔH/A at molecular resolution (0.3 nm) | `3.60×10²⁰ bit·m⁻²` |
| ΔH for the registered object (atomic) | `4.99×10²⁰ bit` |
| extensivity check, A → 10A | ratio **10.000000** |

Three separate defects:

1. **ΔH is extensive.** Since a size-independent `δ_info` is compared against a quantity ∝ area, the constraint
   changes meaning with object size. It is not a threshold on *fidelity*; it is a threshold on *area*.
2. **Unattainable.** With a one-terabit budget the constraint admits base areas ≤ `8.0×10⁻¹¹ m²` = `8×10⁻⁵ mm²`.
   The registered object's base is `5×10⁸` times larger. Shortfall is 8.7 decades at δ_info = 10¹² and 20.7
   decades at δ_info = 1. So **the draft's `C_info` is not a boundary that the object can approach; it is a boundary the object
   is born outside of**, for every δ_info anyone would choose.
3. **"Lossless reconstruction" is a non-sequitur.** Reconstructability is not a function of ΔH's magnitude. A
   projection is many-to-one; ΔH = 0 holds **iff** the map is injective **iff** the object is already a graph.
   So the clause "ΔH ≤ δ_info ⇒ can be reconstructed losslessly" is either redundant (it restates injectivity,
   F1) or false (it claims a small-but-nonzero loss permits lossless recovery, which no coding theorem grants for
   a *deterministic* state).

Also: the entropy of a deterministic classical state is zero. What the draft wants is not Shannon entropy `H` but
a **description length** at a declared resolution — which is exactly what the probe computed. That must be said,
because otherwise `H_3D` has no definition at all and the inequality compares two undefined quantities.

**Required fix**: `ΔH/A ≤ δ_info` per unit base area, with the resolution pair (lateral, depth) declared, and the
reconstruction clause replaced by injectivity + a declared bit budget.

### F3 — CRITICAL: `C_top` is falsified by the project's own fragment census, and is directionally inverted

The draft requires `χ(ε) = χ(0)` on `ε ∈ [0, ε_crit)`, with `ε = 0` the ideal 2D state.

- `front_sweep_v1.md` establishes **1.18×10¹⁰ plates** (1.457 components/layer × 8.12×10⁹ layers), each a
  contractible tomographic slice, with vacuum between them.
- `χ(ideal 2D state) = χ(0) = 1.18×10¹⁰`; `χ(intact 3D body) = 2`.
- Ratio **5.9×10⁹** (Q5). `χ` has already changed at converted fraction `1/N_frag = 8.5×10⁻¹¹`.

So on the draft's own interval `[0, ε_crit)`, `χ(ε) = χ(0)` fails as soon as conversion begins — it holds only on
a set of measure ~10⁻¹⁰. Worse, the condition is **inverted**: because `ε=0` is the *fragmented* 2D state and
`ε=1` is the *intact* body, `χ` must go from 2 to 1.18×10¹⁰ as ε decreases, i.e. the constraint as written can
only hold near ε = 0 and is violated toward ε → 1 — the opposite of the draft's intent to describe the approach to
S4.

This is not a tolerance question. It is a direct contradiction with an ESTABLISHED (internally audited) part of
the record, and it arises because a *global* invariant is being applied to an object that is being converted
*locally* — part of it 3D, part 2D, with the boundary moving.

**Required fix**: replace with a **fragment census** — `N_comp(t)` monotone in swept volume, matched to the
registered counts, with a prohibition on creating handles/genus beyond those the census already contains.

### F4 — MAJOR: `C_geo` is not an independent knob, and is vacuous in every regime where it is defined

- **Not independent (Q3).** For `z = a sin(kx)`, `λ_obs·max|z''| = λ_obs/R_⊥` **exactly** (relative difference
  0.0). The draft's inequality and its prose sentence ("R_⊥ must be much larger than λ_obs") are therefore the
  same statement. `δ_geo` is not a tolerance on curvature; it is a rewriting of `R_⊥ > λ_obs/δ_geo`. Fine as a
  definition, but it provides no second, independent handle.
- **Vacuous where defined (Q4).** For the converted plate (lateral 5 cm, thickness `d_∥ = 15.4 fm`),
  `δ_geo = 3.4×10⁻¹⁸`. For a fingertip-scale ridge (R = 0.5 mm), `δ_geo = 1.1×10⁻³`. To make the constraint bite
  at `δ_geo ~ 0.1` one needs `R_⊥ ~ 5.5 μm` — i.e. surface structure three orders of magnitude finer than the
  finest visible detail of the object. So `C_geo` passes by 4–18 orders of magnitude everywhere it can be
  evaluated, and is *undefined* (not violated) on the un-converted bulk, which is the only place it would matter.
- **Wrong scale.** Occlusion/parallax at the resolution limit is governed by the *sampling* scale (aperture +
  pixel), not by the diffraction wavelength. Using λ_obs makes the criterion maximally permissive by construction.

**Required fix**: a slope criterion `|∇z| ≤ tan θ_max` at a declared sampling scale `ℓ_samp`, plus F1's
injectivity. Delete the `sup_Ω |∂²z|·λ_obs` form.

### F5 — MAJOR: `C_phys` compares two quantities that are not positive

`δS_⊥/S_∥ ≤ δ_phys` uses the **action**, which is indefinite for a Lorentzian field theory. For a free scalar the
integrand is `½(φ̇² − (∇φ)²)`, so both numerator and denominator can be zero, negative, or of either sign depending
on the field configuration; a ratio of them can diverge through zero and its sign carries no information about
whether the perpendicular sector is "perturbative". `S_∥` is also undefined without a chosen foliation and a
chosen sector ("dominant action within the 2D plane" is not a functional of the state alone).

**Required fix**: use a **positive-definite perpendicular energy fraction**,

`δ_phys := ∫ ρ (∂_z φ)² / ∫ ρ [(∂_x φ)² + (∂_y φ)²]`,

which is bounded in [0, ∞), vanishes for a strictly 2D configuration, and — importantly — is *measurable with the
code already in the repository* (the `WEIGHT` machinery in `axisym_2p1_evolution.py` implements exactly this
perpendicular weighting).

**Caution on inheriting a number**: `WEIGHT = 0.05` is **not** δ_phys. It was introduced as a *numerics matching
factor* so that the evolution's matter source matched the York module's `scale = 0.05`. It happens to be the only
perpendicular weighting in the record, but it was not registered as a physical threshold and must not be adopted as
one. δ_phys has to be registered on its own grounds.

### F6 — MAJOR (governance): §3's citation rule contradicts §9 of the ledger — and is right to

Ledger §9 (adopted 2026-11-22): *"S3 and S4 are not validation baselines for S0–S2 … Products of the branch may
not be cited as evidence for the chain."* Draft §3: products *"may be cited as boundary evidence for the S0→S2
verification chain"*. These cannot both stand as written.

Resolution — the draft's distinction is the correct one, and the ledger's sentence was too blunt:

| category | admissible? | what it is |
| --- | --- | --- |
| **Boundary data** | **YES** | numbers supplied *into* an S2 solve as outer/asymptotic/Dirichlet data. S2 cannot be solved without them. |
| **Validation evidence** | **NO** | any use of a branch product to argue that the 2D-ification hypothesis, or the S0–S2 chain, is *supported*. |

**Adopted wording**: *the S3→S4 branch may supply boundary data to the S0→S2 solve; it may never contribute to the
S0→S2 validation ledger, nor to any statement about whether 2D-ification works.* The ledger's §9 sentence is
thereby superseded in letter and preserved in intent.

Separately, §4's opening — *"not a denial of the 2D-ification hypothesis"* — needs the qualifier that the ledger's
anti-correlation finding requires: at `ε → 1` (`¬C1`) the object is the 7 cm slab with atoms intact, ~1–2 bit on
its front face, and it is **not two-dimensionalized at all**. So the branch does not deny the hypothesis *at its
interior*, but its **endpoint is outside the hypothesis**. Recommended: replace with *"the branch characterizes the
boundary of the hypothesis; its endpoint (¬C1) lies outside it and must be labelled as such on every product."*

### F7 — MODERATE: conditions 1 and 3 are not currently evaluable, and condition 3's example is misplaced

1. **No `Ψ_S2` exists.** S2 (BSSN/Z4c + Gamma-driver) has not been built; the R4 round that would have produced it
   was blocked, and the instability round only established that a strongly hyperbolic reformulation is *justified*
   (F.7.4). So `lim Ψ_S4 = lim Ψ_S2` is a criterion with one undefined side. That is acceptable **as a registration
   of a future acceptance test**, but it must be labelled *not currently evaluable* rather than presented as a
   gate. Per the project's own discipline, an unverifiable acceptance criterion must be registered as such.
2. **Gauge dependence.** Ψ is a 10+2 component object `(γ_ij, K_ij, φ, Π)`. S0–S2 run zero shift + 1+log lapse;
   S2 will run a Gamma-driver shift, so the *coordinates differ* and component-wise equality is meaningless.
   Equating components would compare two different coordinate systems and pass or fail for gauge reasons.
   The condition must be stated on gauge-invariant scalars (e.g. the two curvature invariants, and the constraint
   residuals), with the comparison gauge declared.
3. **Both limits are taken as `ε → ε_crit⁻`**, but S4 takes over at `ε ≥ ε_crit`. The S4 side should be
   `ε → ε_crit⁺`; as written the condition equates two left-limits, which does not test continuity across the
   boundary at all.
4. **Condition 3's example is misplaced.** It names "C3 weak interaction preservation" as a constraint *relaxed in
   the S0→S2 chain*. Two problems: (a) under the ledger's correction 1, S0→S2 strictly **tighten** — the only thing
   that changes is that D2 (prescribed background) is **discharged**, which is a strengthening, not a relaxation;
   so there is no relaxed constraint in S0–S2 to be circular about; (b) C3 is not relaxable — its in-action NO-GO
   is parameter-independent (`ρ + p_x < 0`), so it can only be *declared out of scope*, never traded away.
   The correct non-circularity conditions are: **S4 must not borrow D2** (the prescribed background is precisely
   what S2 discharges), and **S4 must not cite L3 display conventions as physical evidence**.

### F8 — MODERATE: conditions 2 is close to vacuous as stated

"The volume of `M_eff` must contract monotonically as the δ's are tightened" is true **by construction** if each
constraint set is nested in its δ — which it is, since each is an inequality of the form `Q ≤ δ`. Tightening δ can
only remove points. So the condition verifies a property of the definition and cannot fail. It also presumes a
measure on `𝒫`, which is not declared (and `𝒫` mixes coordinates with a dimensionless parameter, so "volume" is
not a natural notion).

**Required fix**: replace with the three conditions that actually have content —

1. **non-vacuity**: `M_eff ≠ ∅` at the declared δ's;
2. **non-triviality**: `M_eff ≠ 𝒫` at the declared δ's (i.e. at least one constraint actually bites);
3. **reported sensitivity**: `∂ log Vol(M_eff) / ∂ log δ_i` for each i, so a reader can see which tolerance
   controls the regime.

### F9 — MAJOR: the branch has no lifetime constraint, and the project's sharpest L3 result is exactly a lifetime

Q6: `t_rip/(2L/c) = 1/√2 = 0.707106781187` **exactly, for every L** (computed for L = 0.20, 1.00, 0.070 m; ratio
identical to 12 digits). The sheet tears at 70.7 % of the light round-trip time, scale-free, from `c_s = c/√2`
alone — no materials model, no optics model.

None of `C_geo, C_phys, C_info, C_top` contains a time scale. A state can satisfy all four and still be
unimageable, because the exposure cannot complete before the sheet comes apart. This is the constraint that
*governs L3*, and it is absent.

**Required fix**: add `C_life`: the frame must be acquired inside `t_rip`, i.e. exposure `τ_exp ≤ t_rip = √2 L/c`
— and note the consequence already registered in the null result: since the reflection channel needs a round trip
`2L/c > t_rip`, **no faithful reflected-light frame of a surviving sheet exists**; L3 must therefore image a
*transient*, and must say so. A branch that omits this constraint will silently produce "L3 satisfied" verdicts for
configurations that cannot be photographed.

### F10 — MODERATE (definitional + naming): ε is triply overloaded, inverted w.r.t. the registered parameter, and non-uniquely scalarised

- **Direction inverted.** The registered sweep parameter is `B` (`g_zz = B²`), increasing 3D→2D, with `Σ` conserved
  in `B` (measure theorem). The draft's `ε` *decreases* 3D→2D. Every derivative and every ε_crit inherits an
  inverted sign relative to the rest of the repository. This must be declared explicitly or it will produce sign
  errors.
- **Symbol collision, already live.** `eps` is the explicit symmetry-breaking / vacuum offset in
  `V(φ, eps)` (`DCC_P2_homogeneous.py`), and `ε_mn` is the mean excitation amplitude in the R1-A scan. A third `ε`
  in the same codebase is a hazard of the same class as the `m*/m_e` desynchronisation found in the R5-L2 re-run.
- **Scalarisation is non-unique.** The physical state is a *field* `B(t,x,z)`; `ε` is asserted as a single number.
  The map (field → scalar) is not given, and different natural choices (converted volume fraction, mass fraction,
  column-weighted fraction, area fraction of the projected footprint) give different `ε_crit`. So the location of
  the `M_eff` boundary would be a property of an undeclared choice. The repository already contains the matching
  warning in a different context ("the mapping is not unique, so the actual picture carries an irreducible
  convention component"); this draft reproduces the hazard.

**Required fix**: keep `B` as the physical parameter; define `ε := 1 − φ_conv` with `φ_conv` **registered** as the
converted proper-volume fraction (a measure-based choice, consistent with the measure theorem), and state that
`ε_crit` is only meaningful relative to that registered definition. Reserve `ε` for this use by renaming nothing —
instead, always write `V(φ; eps)` for the potential offset in prose.

- **Naming (minor but real).** This is now the *third* constraint vocabulary: ledger `C1/C2/C3`; roadmap §6.1
  `C1–C4` for contrast criteria (Thickness distinguishability, Optical contrast, Self-emission, Visual threshold);
  and now `C_geo/C_phys/C_info/C_top`. The §6.1 collision **predates** this draft and is the more dangerous one
  (a reader encountering "C1" in an optics context and "C1" in the ledger). Recommendation: never write the new
  set in bare form; always subscript it. At the next revision, rename §6.1's four to **K1–K4**.

### F11 — MINOR: scope — `M_eff` excludes the front, so the branch cannot render the process

If the four constraints are read literally, `M_eff` is the *converted* region (where `z` is single-valued and
`smooth`), which grows as the front sweeps. Two consequences that must be declared rather than discovered later:

1. `M_eff` **excludes the front itself** — the one place the 2D-ification is actually happening. So S4 can render
   completed sheets, not the conversion. Since the project's goal is the *process*, this is a scope limitation on
   the branch, not on the project (S0–S2 carry the process).
2. Because `M_eff` is a *growing region*, "the topological invariants of the object" (`C_top`) is not a
   well-defined function — which is the deeper reason `C_top` cannot work as written (F3).

---

## C. Proposed v0.2 constraint set

Replaces `C_geo, C_phys, C_info, C_top` while keeping the draft's architecture (a joint constraint set over
`(x,t,ε)`, plus citation rules) intact.

| id | replaces | statement | why it is checkable |
| --- | --- | --- | --- |
| **ME1** Injectivity | *new* — the missing core of C1 | overlap measure `μ_ov := |{(x,y) : ∃ z₁≠z₂, ρ>ρ_thr}| / A_⊥ ≤ δ_ov` | direct test on any density field; `μ_ov = 0` ⟺ graph |
| **ME2** Slope at sampling scale | `C_geo` | `‖∇z‖_∞ ≤ tan θ_max` with `(ℓ_samp, Δz_res, θ_max)` declared | replaces curvature-at-λ_obs; actually controls parallax/occlusion |
| **ME3** Perpendicular energy fraction | `C_phys` | `∫ρ(∂_zφ)² / ∫ρ[(∂_xφ)²+(∂_yφ)²] ≤ δ_phys` | positive-definite; measurable by existing `WEIGHT` machinery |
| **ME4** Fragment census | `C_top` | `N_comp(t)` monotone in swept volume and equal to the registered census (`8.12×10⁹` layers, `1.18×10¹⁰` plates); no handles beyond census | the census numbers already exist and are audited |
| **ME5** Lifetime | *new* — the decisive omission | exposure `τ_exp ≤ t_rip = √2 L/c`; state that faithful reflected-light imaging of a surviving sheet is impossible | exact, scale-free, needs no materials model |
| — | `C_info` | **DISSOLVED**, not replaced: its content is (i) description length per unit base area at declared resolution — a *budget*, reportable but not a gate — and (ii) injectivity, which is ME1. Keeping it as a separate gate would preserve an unattainable constraint. | Q1/Q2 |

`ε` redefined as `ε := 1 − φ_conv` (F10). §3 conditions restated per F7/F8. §4 qualifier per F6.

---

## D. What v0.2 must not do

1. **Must not adopt a δ value that makes a constraint pass by construction.** F4's 1.1e-3 and F2's 8.7 decades are
   the numbers to beat, not to accommodate.
2. **Must not inherit `WEIGHT = 0.05` as δ_phys** (F5).
3. **Must not license any visibility conclusion.** §11.1/§11.2 are unchanged by this audit; the branch's products
   remain "designated-background test optics" at best, and the null result's narrowed phrasing stands.
4. **Must not be read as reopening C3.** C3's in-action NO-GO is parameter-independent; no tolerance on ME3 touches
   it.

---

## E. Items for the governor

**All three items CLOSED 2026-11-22.** Disposition: `docs/decisions/meff_boundary_disposition_v1.md`.
Follow-up arithmetic: `runs/S45/meff_disposition_checks_results.txt` (D1–D5, 5/5 PASS).

| # | Item | Ruling | Executor's note added at closure |
| --- | --- | --- | --- |
| 1 | Adopt F6's boundary-data / validation-evidence split | **ADOPTED (D-A)** | The split is necessary but not sufficient: it severs *citation* circularity, not *determination* circularity. Condition `PROV-3` added (typed / non-over-determining / derivation-independent). Also: supplying data does **not** confer well-posedness — that is a property of *(operator, boundary type, function space)*, independent of the values, and must still be shown. |
| 2 | Dissolve `C_info` (recommended) or retain as a reportable budget | **DISSOLVED (D-B)** | Shown content-preserving: `ΔH = 0 ⟺ injective` exhaustively (D5), so the budget's zero set **is** `ME1`. `ΔH` retained as a non-gate budget under `BUDGET-1`. The defect is sharper than stated here: since `A_crit ∝ δ_info` exactly (D3), `C_info` **is** an upper bound on base area. |
| 3 | Rename §6.1's `C1–C4` | **DONE** — as `CM1–CM4`, not `K1–K4` | `K1–K4` was unavailable: `K` is the extrinsic-curvature trace and `K1–K4` are the sci-fi boundary's four checks. See `docs/conventions/symbol_registry.md` §3 item 2 and §7. |

### E.1 Two corrections to this audit's own wording, found at closure

1. **F2 said "'lossless reconstruction' is a non-sequitur."** Precise: it is a **non sequitur with a hidden
   premise**, not a circle. The inequality presupposes `z = z(x_i)`; the conclusion follows from that premise.
   Operational difference: a circle cannot be rescued by weakening the bound, a hidden premise can be rescued by
   naming it — which is exactly what `ME1` does.
2. **F10's recommendation ("rename §6.1's four to `K1–K4`") was wrong.** Recorded here rather than silently
   corrected, because this audit is itself part of the record.

### E.2 Verification that the closure does not overreach

`D5` was registered with a falsification clause: had any of the 256 configurations shown `ΔH = 0` with overlap,
or `ΔH > 0` injective, the dissolution recommendation would have been **withdrawn**. It was not. The check is
exhaustive on the smallest non-trivial lattice, so it establishes the identity for the naive code as a
combinatorial fact, not a sample.

---

## Appendix — cleaned rendering of the submitted formulas

`𝒫 = {(𝐱, t, ε)}`, `ε ∈ [0,1]` (0 = ideal 2D, 1 = full 3D)

`ℳ_eff = {(𝐱,t,ε) ∈ 𝒫 | C_geo ∧ C_phys ∧ C_info ∧ C_top}`

`C_geo:  sup_{𝐱∈Ω} |∂²z/∂x_i∂x_j| · λ_obs ≤ δ_geo`
`C_phys: δS_⊥ / S_∥ ≤ δ_phys`
`C_info: ΔH = H_3D − H_2D ≤ δ_info`
`C_top:  χ(ε) = χ(0),  g(ε) = g(0)  on  ε ∈ [0, ε_crit)`

§3: `lim_{ε→ε_crit⁻} Ψ_S4 = lim_{ε→ε_crit⁻} Ψ_S2` (see F7 on the ⁻/⁺ asymmetry).

---

*Content generated by AI*
