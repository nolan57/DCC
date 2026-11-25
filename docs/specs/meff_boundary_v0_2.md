# S3→S4 Branch: Effective 2D-ification Space Approximation Boundary (v0.2)

**Registered**: 2026-11-22
**Status**: **ADOPTED** — replaces draft v0.1 (`docs/specs/meff_boundary_v0_1.md`, superseded).
**Authority**: governor rulings D-A and D-B, `docs/decisions/meff_boundary_disposition_v1.md`
**Derivation**: `reports/reviews/meff_boundary_v0_1_audit.md` (F1–F11); `runs/S45/meff_boundary_probe_results.txt` (Q1–Q6); `runs/S45/meff_disposition_checks_results.txt` (D1–D5)
**Evidence level**: IDENTITY / ARITHMETIC for the derivations. **This specification asserts no physical result.**

> **Read this first.** v0.2 defines an object and its membership test. **It cannot yet pass anything**:
> three of the five constraints have `OPEN` tolerances, and an unregistered tolerance is not a threshold.
> A product that needs `M_eff` membership today must report "membership undetermined, δ_i OPEN" — it may
> not substitute a convenient number.

---

## 1. Domain and parameter

State: `𝒫 = {(𝐱, t, ε)}` with `𝐱 ∈ ℝ³`, `t` the coordinate time, and `ε` the 2D-ification parameter,
`ε ∈ [0,1]`, `ε = 0` the ideal 2D state, `ε = 1` the full 3D state.

**`ε` is registered as `ε := 1 − φ_conv`**, where `φ_conv` is the **converted proper-volume fraction**,

```
φ_conv(t) := (1/V_0) ∫_{Ω_conv(t)} √γ d³x ,        V_0 := ∫_Ω √γ d³x
```

with `Ω_conv(t)` the region whose material has been processed by the front. This is a **measure-based**
choice, made because the sweep parameter `B` already obeys a measure theorem (`Σ = ∫ρ√g_zz dz` conserved in
`B`); a fraction defined by volume is the only scalarisation consistent with it.

**Three declarations that must accompany every use of `ε`:**

1. **Direction.** `B` (`g_zz = B²`) increases 3D→2D; `ε` **decreases** 3D→2D. Hence `dε/dB < 0` and every
   sign inherited from a `B`-derivative is inverted. Write `dε/dB` explicitly wherever a sign matters.
2. **Non-uniqueness.** The physical state is a field `B(t, 𝐱)`; `ε` is its scalarisation, and the map is
   not unique (volume fraction, mass fraction, column-weighted fraction, projected-area fraction all
   differ). `ε_crit` is therefore meaningful **only relative to the registered definition above**.
   Products quoting `ε_crit` quote the definition.
3. **Symbol hygiene.** `B` remains the physical parameter. `V(φ; eps)` keeps `eps` in code; prose writes
   `V(φ; eps)`. `ε_mn` (R1-A mean excitation) is unrelated. Per registry §3 item 6, `ε` is **not**
   reused for anything else.

**Membership:**

```
ℳ_eff := { (𝐱, t, ε) ∈ 𝒫  |  ME1 ∧ ME2 ∧ ME3 ∧ ME4 ∧ ME5 }
```

---

## 2. The constraint set — `ME2`–`ME5` (adopted) plus `CM5` (observation channel)

> **Amended 2026-11-22.** `ME1` was adopted with v0.2 and then reclassified to `CM5` by `GD1` Option B
> (`docs/decisions/gd_rulings_v1.md`). The adopted gate set is **`ME2`–`ME5`**; `ME1` is a vacated number and
> must not be refilled. Its definition is retained below, retitled, because every citation and every archived
> product refers to it and because the formula is unchanged.

Summary, then each in full.

| id | Name | Replaces | Tolerance status |
| --- | --- | --- | --- |
| ~~**ME1**~~ | **RECLASSIFIED → `CM5`** (2026-11-22, `docs/decisions/gd_rulings_v1.md` GD1 Option B). An observation predicate evaluated at an instrument resolution is not a gate on a physical state | — | `δ_ov` **OPEN**, natural value `0`; `Δz_res` **OPEN** |
| **ME2** | Parallax at the declared sampling scale | `C_geo` (retired) | `Δz_tol`, `ℓ_samp` **OPEN**, presentational |
| **ME3** | Perpendicular energy fraction | `C_phys` (retired) | `δ_E` **OPEN**, needs own basis |
| **ME4** | Fragment census | `C_top` (retired) | **FROZEN** — registered census numbers |
| **ME5** | Lifetime | *new* — the decisive omission | **FROZEN** — exact, scale-free |
| **CM5** | Resolution-relative injectivity (`= ` former `ME1`) | observation channel | `δ_ov`, `Δz_res` **OPEN** |

> **RECLASSIFIED 2026-11-22 (`GD1`, Option B).** This is now **`CM5`** — an observation-channel predicate,
> not a member of the gate set. The statement, the formula and every number computed under it are unchanged;
> only its domain changes. `ME1` survives as a deprecated alias in pre-ruling text, and `ME1` may **not** be
> reused as a new gate label. Phase 0's gate is now `ME4` (`gd_rulings_v1.md` §1). The binding consequence:
> a `CM5` verdict may never be cited as evidence that a state *is* two-dimensional — only that it is
> indistinguishable from a graph at a stated `Δz_res`.

### ME1 — Injectivity (now `CM5`)

**Statement.** At the declared depth resolution `Δz_res` and material threshold `ρ_thr`, define the
overlap measure

```
μ_ov := (1/A_⊥) · |{ (x,y) ∈ A_⊥ : ∃ z₁, z₂ with |z₁ − z₂| ≥ Δz_res and ρ(x,y,z₁) > ρ_thr and ρ(x,y,z₂) > ρ_thr }|
```

and require `μ_ov ≤ δ_ov`.

**Why this is the core.** Relaxing C1 ("effective two-dimensional space") means allowing the object to
stop being a single-valued height field `z = z(x_i)`. Single-valuedness **is** injectivity of the
projection. No other constraint in v0.1 tested it; `C_geo` and `C_info` both *assumed* it (audit F1).
`μ_ov = 0` ⟺ the occupied set is a graph at the declared resolution.

**Why the resolution is inside the definition.** A converted plate has thickness `d_∥ = 15.4 fm`. At any
optical depth resolution `Δz_res ≫ d_∥` a column through it holds one distinguishable material point, so
`μ_ov = 0` — the plate *is* a graph, correctly. The same statement at `Δz_res = 1 fm` would fail. Injectivity
is therefore resolution-relative, and pretending otherwise would make the constraint either vacuous or
impossible depending on an undeclared parameter.

> **Amendment (2026-11-22, `constraint_crosswalk_v1.md` §8.2).** `d_∥` is the **mean in-plane spacing**
> (column pitch), so using it as the plate's *thickness* is a modelling choice, not a derivation. The record
> elsewhere treats the sheet thickness as a declared convention and quotes `P_{2D}` at a stated `L_z`
> (`8.6e25 Pa` at `L_z = 1 nm`; `8.6e31 Pa` at `L_z = 1 fm`). The *structure* of this definition is unaffected
> — `Δz_res` alone decides `μ_ov` for a one-interval column, and the switch sits wherever the thickness is —
> but the *numbers* are thickness-conditional. Every `ME1` verdict must therefore state
> `(thickness, derived-or-convention, Δz_res)`; one carrying only `Δz_res` is incomplete.

**Tolerance.** `δ_ov = 0` is the criterion, and it is exact — any overlap means non-graph. A
non-zero `δ_ov` is admissible **only** as an estimator bias for a finite-resolution measurement, and must
be derived from that estimator. `GD3` assigns this derivation to Phase 1, with the registered falsifier that
`δ_ov` must be **independent of the test state** (`gd_rulings_v1.md` §2.2). Registering `δ_ov > 0` to make an object pass is the failure mode this
project has already committed once (the A5 bogus PASS) and is prohibited.

**Protocol.** Direct evaluation on any density field already in the repository; no new machinery.

### ME2 — Parallax at the declared sampling scale

**Statement.** With `ℓ_samp` the lateral sampling scale of the presentation and `Δz_tol` the acceptable
depth error,

```
ℓ_samp · ‖∇z‖_∞ ≤ Δz_tol
```

**Why not curvature at `λ_obs`.** `C_geo`'s form `sup|∂²z|·λ_obs ≤ δ_geo` was **identical** to
`λ_obs/R_⊥` (Q3: relative difference `0.0`) — one statement written twice, so it offered no independent
handle — and it evaluated to `3.4e-18` for a converted plate and `1.1e-3` for a fingertip ridge (Q4), i.e.
it passed by 4–18 orders of magnitude everywhere it was defined, and was *undefined* on the un-converted
bulk, the only place it would matter. Curvature also does not control occlusion; injectivity does (ME1).

**Why `Δz_tol` is presentational and must be labelled so.** It is not a physical constant. It is the depth
error a viewer at the declared sampling scale will accept, and it therefore belongs to the fidelity level
(FL1/FL2/FL3), not to the physics. Products using ME2 state which fidelity level's `Δz_tol` they used.

**Tolerance.** `ℓ_samp` and `Δz_tol` **OPEN**. `ℓ_samp` is set by the presentation (pixel pitch, aperture);
`Δz_tol` is set by the declared fidelity level. Neither may be back-solved from a desired verdict.

> **BLOCKED 2026-11-22 — finding `ME3-F1`: `φ` is undeclared, and the two natural declarations give opposite
> verdicts.** `docs/decisions/route_completion_v1.md` §4. With `φ` = the material field, `δ_E ∝ (λ/t)²`, so the
> converted sheet sits at `1.69e26` and the intact body at `4.05e-1` — **inverted**, and diverging as the sheet
> thins. With `φ` = a velocity potential, the sheet sits at `5.93e-27`. The two differ by `(λ/t)^4 = 2.8e52`.
> `δ_E,max` therefore cannot be registered, Phase 3 cannot run, and Phase 4 cannot start. Requires `GD6`
> (open items). No value was written in to make anything pass — including the `1e-2` that `P3b`'s failure withdrew.

> **RETIRED 2026-11-22 — `ME3` is withdrawn, and `ME3-F1` is CLOSED rather than resolved.** Ruling:
> `docs/decisions/me3_phi_disposition_v1.md`. `φ` **is** declared — it is a **velocity potential**, fixed by the
> criterion's own name ("perpendicular *energy* fraction" is an energy only if `φ` is a potential). The material
> reading is withdrawn as a **misreading**: measured, it makes the constraint algebraically a **minimum-thickness
> requirement** (`δ_E ≤ δ_E,max ⟺ t ≥ t_min`), i.e. a flatness prohibition, with exponent `k` in `(0,2)` for the
> material, indicator and geometric readings alike (`1.89 / 0.95 / 0.43`). With `φ` a potential, the ratio is
> identically zero on every state the record contains (`u^μ = (c,0,0,0)`), so every state passes and nothing can
> be rejected. **No `δ_E,max` exists to register** — not open, unregistrable. `ME3` is reinstatable only for a
> *dynamic* unfolding route with a `u_⊥/u_∥` instrument, neither of which exists. The clause below is kept as the
> record of why it was adopted; it is not a live criterion.

### ME3 — Perpendicular energy fraction

**Statement.**

```
δ_E := ∫ ρ (∂_z φ)² d³x  /  ∫ ρ [ (∂_x φ)² + (∂_y φ)² ] d³x   ≤  δ_E,max
```

**Why not an action ratio.** `δS_⊥/S_∥` is a ratio of an **indefinite** quantity: for a free scalar the
integrand is `½(φ̇² − (∇φ)²)`, so both numerator and denominator can be zero, negative, or either sign, and
the ratio can diverge through zero in a way that carries no information about whether the perpendicular
sector is perturbative. `S_∥` is additionally undefined without a declared foliation and sector. The
positive-definite form above is bounded in `[0,∞)`, vanishes for a strictly 2D configuration, and is
**measurable with existing code**: the `WEIGHT` machinery in `axisym_2p1_evolution.py` already implements
exactly this perpendicular weighting.

**Tolerance.** `δ_E,max` **OPEN**, and it must be registered on its own grounds.

> **Do not inherit `WEIGHT = 0.05`.** That constant was introduced as a *numerics matching factor* so the
> evolution's matter source matched the York module's `scale = 0.05`. It is numerically the only
> perpendicular weighting in the record and it is **not** a physical threshold (audit F5). Adopting it
> would give ME3 a tolerance that was chosen for an unrelated purpose.

### ME4 — Fragment census

**Statement.** Let `N_comp(t)` be the number of connected components of the converted region. Require:

1. **monotonicity** — `N_comp` is non-decreasing in swept proper volume;
2. **census match** — at `φ_conv → 1`, `N_comp` equals the registered census: `8.12×10⁹` layers ×
   `1.457` components/layer = `1.18×10¹⁰` plates;
3. **no new topology** — no handles (genus) are created beyond those the census already contains; each
   census plate is contractible (`χ = 1`).

**Why not `χ(ε) = χ(0)`.** The draft required `χ(ε) = χ(0)` on `ε ∈ [0, ε_crit)`. But
`χ(ideal 2D state) = 1.18×10¹⁰` while `χ(intact body) = 2` (ratio `5.9×10⁹`, Q5), so the condition fails
once `1/N_frag = 8.5×10⁻¹¹` of the object has converted — it holds on a set of measure `~10⁻¹⁰` of the
branch — and it is **directionally inverted**, since `χ` must *increase* from 2 toward `1.18×10¹⁰` as
`ε` decreases. It also applies a *global* invariant to an object converted *locally* with a moving
boundary, which is why "the topological invariants of the object" is not a well-defined function here
(audit F3, F11).

**Tolerance.** FROZEN — the census numbers are registered and audited. ME4 is a bookkeeping identity, not
a tolerance question. If the census is revised, this clause is revised with it (open item O2).

**Scope limitation, declared not discovered.** `ℳ_eff` is the **converted** region, so it **excludes the
front** — the one place 2D-ification is happening. The branch therefore renders completed sheets, not the
conversion; the process belongs to S0–S2. Every branch product carries this limitation.

### ME5 — Lifetime

**Statement.** The frame must be acquired inside the tearing time:

```
τ_exp ≤ t_rip = √2 L / c = L / c_s ,      c_s = c/√2
```

with `L` the object's largest extent (see open item O4).

**Why it cannot be omitted.** `t_rip/(2L/c) = 1/√2` **exactly, for every `L`** (Q6: `0.707106781187` at
`L` = 0.20, 1.00, 0.070 m; D4 verifies the identity `√2L/c = L/c_s` to `1e-15`). None of v0.1's four
constraints contained a time scale, so a state could satisfy all four and still be unimageable because
the exposure cannot complete before the sheet comes apart. **This is the constraint that governs L3, and
it was absent.**

**The corollary, which must appear on every L3 product.** The reflected-light channel requires a round
trip `2L/c = √2 · t_rip > t_rip`. Therefore:

> **No faithful reflected-light frame of a surviving sheet exists** — *for an observer at distance
> `D = L`* (`GD8`, 2026-11-22). L3 must image a *transient*, and must say so on the frame. The
> transmission channel retains its `1.41×` margin and a shadowgraph is not excluded.

**Tolerance.** FROZEN — exact and scale-free; needs no materials model and no optics model.

> **Annotation 2026-11-22 (`GD7`, `GD8`) — the text above is unchanged in substance; its scope is now stated.**
> **`GD8` (governor):** *"keep 2L/c, and write in 'only when D = L'"* — keep `2L/c`, write in that it holds only at `D = L`.
> Applied: the premise is now inside the corollary, above. The identity `2L/c = √2 t_rip` is untouched.
>
> **Why the premise costs nothing.** The corollary says less than it appeared to, but its conclusion is unchanged
> where it matters, because `D = L` is the **most favourable** geometry, not a convenient one. Naked-eye viewing
> needs `D ≥ 0.25 m`, and `D ≥ L/√2` holds for every `L ≤ 0.3536 m`; for `L > 0.3536 m` the object subtends more
> than 126.9° at the near point and cannot be taken in. So within the naked-eye domain the corollary applies
> **a fortiori** (`fl_coordinate_results` F-5).
>
> **What is *not* adopted.** The per-patch form `2D/c ≤ d/v_front ⇔ D ≤ d/√2` (`route_goal_conformance_v1` F3)
> remains an **unregistered observation**. `GD8` kept `2L/c`; therefore the per-patch window may not license any
> frame and is cited only as a finding about the corollary's algebraic structure, never as permission.
>
> **Interaction with `GD7`.** `GD7` makes fidelity mean closeness to the unaided retinal image, so `FL3` is the
> maximum. That does **not** conflict with the corollary: the corollary constrains the *content* of a faithful
> frame (no surviving sheet), `GD7` constrains its *fidelity*. A frame can be maximally faithful and show no
> sheet — `FL3` is attainable, and what it shows is the object's absence (`fl_coordinate_results` F-4, F-6).
> Evidence: `runs/ROUTE/fl_coordinate_results.txt`; `docs/decisions/gd7_gd8_execution_v1.md`.

---

## 3. Dissolved: `C_info`

`C_info` is **not** replaced by an `ME` item. Its content is split per ruling D-B:

| Component | Where it went |
| --- | --- |
| `ΔH = 0` case (injectivity) | **ME1**. Proven exactly: `ΔH = 0 ⟺ injective` on all 256 configurations of a `2×2×2` lattice, with `ΔH = N_ov·log2 V` (D5, error `0.00e+00`) |
| `ΔH` magnitude | **reportable budget**, never a gate (`BUDGET-1`) |
| `δ_info` threshold | **withdrawn** — an arbitrary constant with no derivation |
| "lossless reconstruction" | **withdrawn as a consequence** — it never followed from the inequality |

**What the inequality actually said.** Since `A_crit = δ_info/(ΔH/A)` is exactly linear in `δ_info`
(log–log slope `1.000000000000`, D3), `C_info` as written **is exactly** `A_⊥ ≤ A_crit`, an upper bound on
the object's base **area**. Its non-injectivity content is "the object must be small enough". With a
one-terabit budget `A_crit = 8.01×10⁻¹¹ m²`, while the registered object's base is `5×10⁸` times larger;
the shortfall is `8.70` decades at atomic resolution and `7.16` at molecular (D1), and grows without bound
in area (slope `1.000000000000`, D2).

**Reporting rule.** Any reported `ΔH` carries `(ℓ_lat, Δz, A_⊥, code, N_ov)`. Report `N_ov` and `μ_ov`;
report `ΔH` only as a derived convenience. `BUDGET-1`: `ΔH` may never appear in a PASS/FAIL verdict, gate
row, threshold, or acceptance criterion.

---

## 4. Citation rules for branch products

Replaces v0.1 §3. The v0.1 conditions 1–3 were partly not evaluable, near-vacuous, and misplaced
(audit F7, F8); these have content.

**C-1 — Continuity across the boundary (registered as a future acceptance test).**
On **gauge-invariant scalars** only — the two curvature invariants and the ADM constraint residuals —
with the comparison gauge declared,

```
lim_{ε→ε_crit⁻} 𝒮_S2 = lim_{ε→ε_crit⁺} 𝒮_S4
```

Three corrections to v0.1's form: the S4 side is a **right** limit (v0.1 wrote two left limits, which
tests nothing); component-wise equality is meaningless because S0–S2 use zero shift + 1+log while S2 will
use a Gamma-driver, so the coordinates differ and component comparison would pass or fail for gauge
reasons; and **status: NOT CURRENTLY EVALUABLE** — no `Ψ_S2` exists. Per the project's discipline an
unverifiable acceptance criterion is registered as such, not presented as a gate.

**C-2 — Non-vacuity, non-triviality, sensitivity.** Replacing "`ℳ_eff` contracts monotonically as the δ's
tighten", which is true by construction for any inequality of the form `Q ≤ δ` and therefore cannot fail,
and which presumes a measure on `𝒫` that is not declared (and not natural, since `𝒫` mixes coordinates
with a dimensionless parameter):

1. `ℳ_eff ≠ ∅` at the declared δ's;
2. `ℳ_eff ≠ 𝒫` — at least one `ME` item actually bites;
3. report `∂ log Vol(ℳ_eff) / ∂ log δ_i` for each `i`, so a reader can see which tolerance controls the
   regime.

**C-3 — Non-circularity.** Corrected from v0.1, which named "C3 weak-interaction preservation" as a
constraint *relaxed* in the S0→S2 chain. Two errors there: S0→S2 **strictly tighten** (the only change is
that D2 is *discharged*, a strengthening), so there is no relaxed constraint to be circular about; and C3
is not relaxable — its in-action NO-GO is parameter-independent, so it can only be declared out of scope,
never traded. The conditions with content are:

1. **S4 must not borrow D2** — the prescribed contraction background is exactly what S2 discharges;
2. **S4 must not cite L3 display conventions as physical evidence** — a colour in an L3 frame is a
   declared convention, and the frequency-flat response result makes this sharp rather than stylistic;
3. **boundary data supplied to S2 obey `PROV-3`** — typed, non-over-determining, derivation-independent
   (`docs/conventions/provenance_tags_v1.md`). A solve using branch data reports "solution given data D",
   never "confirmation of D".

---

## 5. Relationship with the S0→S2 chain

**Adopted wording** (replacing v0.1 §4's "not a denial of the 2D-ification hypothesis", which lacked the
qualifier the anti-correlation finding requires):

> The branch characterizes the **boundary** of the 2D-ification hypothesis. Its interior (`ε → 1`, `¬C1`)
> lies **outside** the hypothesis — at that end the object is the 7 cm slab with atoms intact, ~1–2 bit on
> its front face, not two-dimensionalized at all — and every product must be labelled accordingly. The
> branch may supply **boundary data** to the S0→S2 solve; it may never contribute to the S0→S2
> **validation ledger**, nor to any statement about whether 2D-ification works.

---

## 6. What v0.2 does not do

1. **It passes nothing.** `δ_ov`, `ℓ_samp`, `Δz_tol`, `δ_E,max` are OPEN. No object is certified as in or
   out of `ℳ_eff` by this document.
2. **It adopts no δ chosen to make a constraint pass.** Q4's `1.1e-3`, Q2's shortfall and D1's spread are
   the numbers to beat, not to accommodate.
3. **It inherits no tolerance from an unrelated purpose** — specifically not `WEIGHT = 0.05` (F5).
4. **It licenses no visibility conclusion.** Roadmap §11.1/§11.2 stand. Branch products remain
   designated-background test optics at best.
5. **It does not reopen C3.** The in-action NO-GO is parameter-independent; no `ME` tolerance reaches it.
6. **It does not render the process.** See ME4's scope limitation.

---

## 7. Open items

| # | Item |
| --- | --- |
| O1 | `δ_E,max` basis for ME3, independent of `WEIGHT = 0.05` |
| O2 | `ME4` census re-derivation if the fragment count changes |
| O3 | `L` three-way label collision — staged, not renamed (registry §3 item 3) |
| O4 | `ME5`'s `L`: largest extent is a placeholder pending a derivation for non-spherical geometry |
| O5 | `C4` reserved, unused; no `ME` item may be promoted into it |
| O6 | `μ_ov` estimator bias at finite resolution, and whether it can be made zero by construction |
| O7 | **`GD6` — CLOSED 2026-11-22.** `ME3`'s `φ` is a **velocity potential**, fixed by the criterion's name. The material reading is withdrawn (it makes the constraint a minimum-thickness floor, `k ∈ (0,2)` for all three static readings). With `φ` a potential, `δ_E ≡ 0` on every state in the record, so `ME3` is **retired**. Ruling: `me3_phi_disposition_v1.md` |
| O8 | `ME3`'s `φ` as a *symbol*: distinct from `φ_conv` (converted proper-volume fraction). **`φ_E` is released** — `ME3` is retired, so the reserved name is withdrawn unused and must not be reused for a new criterion without a fresh declaration |

---

## 8. Addendum after the phased-route audit (2026-11-22)

Two findings bear on `ME1` and are recorded here rather than editing §2, which stands as adopted.

**8.1 — `Δz_res` is the parameter that decides `ME1`, and this document does not register it.** §2 declares it
per use. For any object whose columns hold one material interval, `μ_ov = [thickness ≥ Δz_res]`, so the verdict is
a function of an unregistered number: the intact 7 cm slab passes at `Δz_res = 0.1 m` and fails at `1e-3 m`, while
the ideal sheet fails at `Δz_res = d_∥` because the criterion is `≥` and its two faces are exactly `d_∥` apart
(audit V1/R1/R2). `O6` is therefore larger than an estimator-bias question: **`ME1` has no attained minimum**, and
its pass set is the open interval `(d_∥, ∞)`. Until `Δz_res` is registered, `ME1` cannot be a gate.

**8.2 — `ME1` is a `CM`-domain predicate.** Under registry S1a, `ME1` and `CM1` are the same predicate with
`λ ↔ Δz_res`. `ME1`'s stated intent (single-valuedness of the projection) is geometric, but every non-vacuous
formalisation of it is resolution-relative, and a resolution is an instrument property. Consequences for use:

- A product citing `ME1` states `Δz_res` and declares the verdict relative to it;
- `ME1` may not be cited as evidence that an object *is* two-dimensional, only that it is thin relative to a
  stated resolution.

**8.3 — what is unchanged.** `ME2`–`ME5`, the `C_info` dissolution, the citation rules of §4, and every OPEN
tolerance stand exactly as adopted. No value was supplied to make anything pass.

---

## 9. Tolerance status after `RQ-09` (2026-11-23) — measurement only

This section **registers no threshold** and changes no adoption. It records what round 55
(`runs/OPTICS/observer_params_results.txt`) measured about the four OPEN tolerances, so that a later ruling has
the arithmetic in front of it. §1–§8 are byte-identical; nothing here is a ruling, and no object is certified in
or out of `ℳ_eff`.

**9.1 — `Δz_res` is a function of `θ`, not a free parameter.** With `Δz = λ/(2NA²)` over the declared `1–3 eV`
band it is `[207 nm, 62.0 µm]` (2.477 decades); with a range gate it is `c·δt/2`. §8.1's statement that the pass
set is the open interval `(d_∥, ∞)` is correct as algebra and misleading as instrumentation: `μ_ov` is *constant*
over the whole admissible band — the plate is a graph by `7.13` decades, the slab is not by `3.05` — so the
parameter cannot be turned anywhere it can be read. The only channel that makes the slab a graph needs
`δt > 467 ps`, i.e. a `0.45 m` depth resolution on a `0.18 m` object, which is coarser than the object. In
particular the archived "the intact slab PASSES `ME1` at `Δz_res = 0.1 m`" is reproduced and `0.1 m` is `1613×`
the coarse end of the optical band: that PASS is not attainable by any passive instrument at the declared band.
`Δz_res` is therefore **channel-selecting**, and a product must name the channel rather than a number.

**9.2 — `ℓ_samp` and `Δz_tol` are one parameter.** `ME2` contains neither name alone; it contains
`Δz_tol/ℓ_samp = s_max`. Joint rescaling `(k, k)` leaves the criterion identical to `1e-15` and moving one name
alone flips it. Counted as two, registered as OPEN twice, it is one dimension-free number: the largest slope the
presentation can draw. It is also **form-conditional** (the switch sits at `ε = 6.2×10⁻³` for the terraced form
and `6.3×10⁻²` for the sine, a factor `32/π`), so a single registered value would be a threshold for one form.

**9.3 — `δ_E,max` is unregistrable, now by measurement and not only by ruling.** `O7` retires `ME3`; round 55
exhibits the dichotomy behind that retirement. With `φ` a potential, `δ_E ≡ 0` on `u^μ = (c,0,0,0)` and **every**
threshold passes **every** state. With `φ` the signed distance, `δ_E = R/t` exactly (`me3_phi` P8), so the
criterion reads `t ≥ R/δ_E,max` — a thickness floor. There is no value that fails an object without being a
thickness, so no value can be registered *as an energy criterion*.

**9.4 — the consequence this document cannot draw for itself.** `ME2`'s tolerances are presentational **in this
document's own words** (§2 `ME2`, "not the physics … belongs to the fidelity level"). `GD1` Option B moved `ME1`
out of `ℳ_eff` with the sentence *"an observation predicate evaluated at an instrument resolution is not a gate on
a physical state."* That sentence applies to `ME2` word for word, and applying it consistently would leave
`ℳ_eff = ME4 ∧ ME5` — both **FROZEN**, i.e. a decidable membership set as of today. Reclassifying a gate is a
governor act (`GD1` was one, and was an *Option B*), so the finding is recorded as board note `BN-17` and **not
performed here**. Until it is ruled on, `ME2` remains a gate with a tolerance that is a function of the viewer.

---

*Content generated by AI*
