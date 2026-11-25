# DCC — Consolidated Research Progress

**Document**: progress report v1 · **As of**: 2026-11-23, round 44 (P1 closure) · **Repo**: `D:\Docs\DCC`
**Scope**: the whole programme, from the P0 direction review to the surface-conductivity conformance
specification v1.2. Every verdict below is traceable to a decision file in `docs/decisions/`, a
specification in `docs/specs/`, or a product in `runs/`. Nothing here is a new claim.
**Authority**: none. This is a reading of the record, not an addition to it. Where the record and this
document disagree, the record wins.

---

## 0. The state of the programme in one page

DCC asks a single question and has answered it in six separable parts. Three are closed (two of them
negatively), one is closed in part, and two are blocked on physics that does not yet exist.

| # | Question | Verdict | Where it is decided |
|---|---|---|---|
| 1 | Can an ordinary material object be converted to 2D **at fixed area**, keeping its atoms and bonds? | **NO-GO** | `G0p_seven_row_verdict_v3.md` row 1 |
| 2 | Is there a *new* stable dense state at that density? | **OPEN** — a three-convention envelope, not a state | row 2; `R1-B1` (Phase-0 spec delivered, round 40) |
| 3 | Does the geometry contract endogenously? | **D2 yes, D3-strict no** | `DCC_P2_Report_v2.md` §0 |
| 4 | Can the 2D-ified 3D object be **depicted as an image**? | **NO — and not for statistical reasons** | `route_terminus_v1.md` (`DEPOSIT-BLIND`, `DEPOSIT-DICHOTOMY`) |
| 5 | Can that same object be **serialized losslessly**? | **YES** — all seven criteria met | `deposit_serial_conformance_v1.md` |
| 6 | Is there a physically admissible optical response at the endpoint? | **CONDITIONAL — a candidate `σ_s` now exists** (round 45), admissible at the ideal model level (`S7` conditional); the gate ruling is pending | `surface_conductivity_v1.md` v1.3, `S1`–`S15`; `r1b1_p4_p5_closure_v1.md` |

The single live blocker was `G6`/`DC2`: a surface conductivity `σ_s(ω)` that is **microscopically grounded,
has a solved `τ`, and partitions its spectral weight legally**. Round 45 changed the state of that blocker:
the R1-B1 chain was executed under the lifted veto (`P2` 9/9, `P3` 6/6, `P4` constructed), and a candidate
`σ_s(ω)` **now exists, derived from the solved states** — admissible at the ideal model level (`S7`
conditional), with `f_intra = 1.52×10⁻³` derived and the UV bucket quantified. The `G6`/`DC2` ruling is
submitted for adjudication (`r1b1_p4_p5_closure_v1.md`); the NO-GO record is retained in full.

**One sentence.** *The rendering question is closed by a theorem; the matter question is open by measurement;
the optics question is specified but unanswerable until the matter question is settled.*

---

## 1. What the project is

Dimensional Collapse Conjecture (DCC): a macroscopic 3D object is swept by a front that converts it to an
effectively two-dimensional state at **fixed projected area**. The physical content is carried by three
constraints, which are the only items in the record granted single-letter names:

| id | constraint | status |
|---|---|---|
| **C1** | effective 2D space — column conservation | **ESTABLISHED** at identity level |
| **C2** | smooth 2D-ification — zero intralayer strain | holds intralayer; **interlayer interface failure registered** (`8.12×10⁹` interfaces) |
| **C3** | weak-interaction preservation, self-consistent in action | **NO-GO in-action, parameter-independent** (`ρ + p_x < 0`) |

The programme was never "can a 3D object look flat". It is: *can a fixed-area reduction be physically
consistent, and if so what would an observer see.* Two of the three constraints are already negative, and the
negative results are the load-bearing ones.

---

## 2. How to read the record: three vocabularies, one governing generation

The repository accumulated three layers of notation because the programme changed shape twice. They are not
interchangeable, and a reader who mixes them will mis-cite.

**Layer A — stage programme (2026-11-19/20).** `P0`→`P4` numerical stages; reports `DCC_P0…P4_*`;
roadmap `DCC_P0-P4_Roadmap_Plan.md`; old gate numbering `G0`–`G6`. This layer produced the frozen numerical
baseline.

**Layer B — roadmap v1.4 (2026-11-20/21).** `Macro3D_to_2D_Smooth_Reduction_Roadmap_v1.4.md` rewrote the
gate chain as **`G0′ → G2′ → G3′ → G4 → G5′ → G6`**, split matter response into the dual-track `R1-A`/`R1-B`,
and fixed the four-category classification of models (`§8.4`).

**Layer C — governance layer (2026-11-22).** The current authority. Adds:
`S0`–`S4` scene stages (`S0→S2` validation chain, `S3→S4` branch) · `FL1`–`FL3` fidelity ladder · `ME2`–`ME5` boundary criteria · `CM1`–`CM5` contrast
criteria · `GD1`–`GD11` governor decisions · `D-1`…`D-9` route-terminus decisions · the
`8 × 4 = 32`-cell constraint × tier matrix · `DEMO-1` and the deposit format · the `σ_s` specification ·
`docs/conventions/symbol_registry.md` as the single source of truth for labels.

**Layer C governs.** Layers A and B remain valid as *records of what was computed*; their labels are read
through the registry. Where a Layer-A number was superseded, the supersession is marked in the file rather
than deleted (see §9).

---

## 3. Method — the part of the project that is actually transferable

Every round follows the same seven disciplines. They are enforced, not aspirational, and they are why the
record can be trusted where it says "FAIL".

1. **Pre-registration before execution.** Predictions with explicit kill conditions are written and
   hash-locked before the script runs (`runs/*/…_registration.md`). A prediction that fails is reported as
   failed and stays in the product.
2. **Hash-lock on any text that carries a threshold.** `threshold_lock.json`, `demo_lock.json`,
   `serial_lock.json`, `surface_conductivity_lock_v1_{1,2}.json`. A threshold that moves after a measurement
   is a defect, and has been recorded as one four times.
3. **Errata appended, never edited.** Archived stdout is immutable (`§9.1`). Corrections are append-only
   errata blocks (`E1`…`E5`) attached to the product, so the error and the fix sit in the same file.
4. **Evidence classification.** A pass count that includes identities is not a correctness claim. The `G0′`
   ledger is reported as `CHECK 7/7 · IDENT 3/3 (not evidence) · NEGCTRL 1/1`.
5. **Negative controls must fail by a known factor.** A deleted wrong formula is not deleted; it is
   re-registered as a negative control required to fail by exactly `10.000×`.
6. **Prohibition over relabelling.** When 25 of 27 frames could never be cited again, they were not
   relabelled — a rule was written forbidding their citation (`D-2`, `D-8`).
7. **Every empirical number carries its product.** A measured value is quoted bound to the product that
   measured it, by file and line — `W_intra/W_total = 1.000000000003` is quoted from
   `runs/OPTICS/sc_route_results.txt` §F, never paraphrased. A number carried across ledgers by paraphrase
   is not evidence (`E5`); this is the non-hash generalization of the `E4` digest rule, and the SC-4
   governor ruling elevates it to a project-wide requirement.

Two corollaries now bind future work: **no backward selection** (a matter branch may not be chosen because
the optics then look good) and **no forward selection** (a criterion may not be relaxed because a candidate
is close to passing). Both are in `surface_conductivity_v1.md` §7.5 and §11.

---

## 4. Gate status

`G0′` and `G1` are the only gates that have fully passed. Everything downstream is either partial or blocked,
and each block is located in a named object rather than in effort.

| Gate | Object | Status | Basis |
|---|---|---|---|
| **`G0′`** | survival of ordinary matter at fixed area | **PASSED — as seven separate accounts**, no single PASS/NO-GO | 1 NO-GO · 1 NO-GO (conditional) · 1 NO · 4 OPEN |
| **`G1`** | numerical baseline freeze | **PASSED (frozen)** | 4-resolution order `2.00–2.01`, `E_res = 1.17e-7`, `σ_w` and `δ` within `0.03%` of analytic |
| **`G2′`** | matter response (`R1-A` + `R1-B1`) | **NOT PASSED** | `R1-B1` v3 yields a three-convention **envelope**, not a state |
| **`G3′`** | endogenous geometric dynamics | **OPEN** | `D2` achieved in two geometries; strict `D3` not; `P2-C6` linear stability outstanding; NEC verdict limited to the specified action |
| **`G4`** | finite-region matching | **NOT PASSED** | `R4` grid-scale instability remains unlocalised in the bulk |
| **`G5′`** | effective 2D theory and mapping | **NOT PASSED** | carrier conservation (`N7`) blocks it: at `μ_e = 73.37 MeV` the electron gas loses its object |
| **`G6`** | optics and observer | **NO-GO** | no compliant `σ_s(ω)` exists; see §7 |

**The chain is not a queue of tasks; it is a chain of preconditions.** `G6` needs `G4` and `G5′`; `G5′` needs
`G2′`; `G2′` needs `R1-B1`. So the record's one-line status is: *`G0′` passed, `G1` frozen, and the chain
stops at `G2′` for want of an equation of state.*

---

## 5. Physics that stands

These results are independent of the rendering line and survive every later round.

### 5.1 The frozen baseline (`G0P-003`, v3 — supersedes v1 and v2, both revoked)

| Quantity | Value | Definition |
|---|---|---|
| `N_s` (nuclear column density) | `4.2155e27 m⁻²` | defining |
| `n_2D` (carrier density) | `2.20049e28 m⁻²` | `Z_A·N_B`, `Z_A = 0.522` |
| `k_F` | `0.371834 fm⁻¹` | `√(4πn_2D/g)` |
| `E_F = μ_e` | `73.37 MeV` | `ħc k_F` (`E_F/m_e c² = 143.6`) |
| `u_2D` | `1.7245e17 J m⁻²` | `(2/3) n E_F` |
| `P_2D` | `8.6227e16 N m⁻¹` | `u/2` |
| `c_s` | `c/√2 = 2.1199e8 m s⁻¹` | 2D ultra-relativistic |
| `v_∞` | `0.1656 c` | `√(2P/Σ)`, `Σ = 70 kg m⁻²` |
| `t_rip` (1 m) | `4.72 ns` | `1/c_s` |
| `u_2D/Mc²` | `2.741 %` | |
| `A_min` | `3.794e8 m² ≈ 380 km²` | `N_s d_bond²` |
| `d_par` (carrier spacing) | `6.7420 fm = 1.274e-4 a₀` | `n_2D^{-1/2}` |

**β-equilibrium is an envelope, not a number**: `X_p ∈ [1.62e-3, 4.50e-2]` (a `28×` span),
`μ_e ∈ [6.73, 24.96] MeV`, `P_tot ∈ [1.84e16, 6.48e16] N m⁻¹`. Single-point values may not be quoted. A
**lower density bound** was discovered in the process: the 2D electron `μ_e ∝ √n` cannot reach `1.293 MeV`, so
β-equilibrium fails below `n_thr = 6.15e-6 fm⁻³` (HYB) / `6.82e-6` (ALL2D); the 3D case has no such bound.

### 5.2 The seven-row verdict — the shape of the negative result

`G0P-003` refuses a single verdict on purpose. Row 1 is the decisive one: **preserving the original atoms,
bonds and non-covalent network at fixed area is NO-GO**, on the geometric spacing `d_∥ = 1/√N_s = 15.40 fm =
2.91e-4 a₀` (the *nuclear* column density, not the carrier density — see §10.2), independent of any electron
convention, with bound states ceasing to exist below `L_z^ion = 1.66 Å`. Row 6 is
NO-GO *conditionally* (frozen ideal-gas pressure with no constraint stress): `P_2D = 8.62e16 N m⁻¹`, `c_s` and
`v_∞` as above. Row 7 says the v1.3 cold-electron final state is **not** the ground state at that density.
Rows 2–5 stay OPEN, and the gate explicitly **may not** be used to reject the geometric branch, the dense-state
branch, or the effective-2D theory branch.

### 5.3 Six structural conflicts (the assumption-layer audit)

Holding "effective 2D / smooth / weak-on" does not rescue the model. Six conflicts were computed using only
geometry, field strength and timescales:

| id | conflict | number |
|---|---|---|
| `K1` | eff-2D vs composition | `L_z` window `[1.68, 1.99] fm`, only `1.19×` wide; the registered `1 fm` is thinner than a nucleon (`1.68 fm`) |
| `K2` | eff-2D vs known physics | `620 MeV/fm → 6.2e23 V/m = 4.7e5 ×` Schwinger; lowering it under critical needs `L > 21.7 fm`, where the 2D criterion is off by `12×` |
| `K3` | axial vs lateral | wall pressure `2.19e33 Pa`, `25×` the lateral (strict geometry `40×`) |
| `K4` | energy ledger vs `2.741%` | constraint zero-point energy is `12.7×` the in-plane degeneracy energy (electrons) |
| `K5` | smoothness vs timescale | neutronisation `2.96 ns` ≈ expansion `4.72 ns` ≈ sound crossing `0.33 ns` — **no scale separation** |
| `K6` | weak-on vs stability | β-equilibrium demands `>91%` neutronisation, in all three conventions |

Dropping "weak-on" (scenario W) **removes** `K1` and `K6` and **hardens** `K2`: the electrostatic well available
is only `4–50 keV`, three orders below `E_F`, so none of the four known forces can act as the constraining agent.

### 5.4 Two identities that ended whole lines of work

- **The conversion clock.** `t_rip = √2 L/c`, and the round-trip exceeds it by exactly
  `1.414213562373` for every `L`. Measured: `9.434617e-10`, `4.717309e-9`, `3.302116e-10 s` at
  `L = 0.20, 1.00, 0.070 m`. Because it is an identity, `Λ_max` was retired — there is no rate constant to
  calibrate, and the **reflected channel has zero exposure budget** at any `L`.
- **The overlap tolerance.** `δ_ov` (the estimator bias in `μ_ov ≤ δ_ov`) has no usable setting. It is
  **binary**: `0` above `Δz_res > √2 s_max Δx` (inert — every state already passes), `1` below it (vacuous —
  the intact slab passes). Anything in `(0,1)` is either state-dependent or arbitrary, and the state-dependence
  was measured: four graphs at identical `s_max` gave `μ_ov = 1.000, 0.625, 0.078, 0.125`, a `0.92` spread.
  The window is also closed on physics: seeing the layering needs `Δz_res ≤ 8.62e-12 m`, tolerating roughness
  needs `Δz_res > s_max Δx` — closed by `25×`, `116×`, `2.5e6×` depending on the surface model.

---

## 6. The rendering line — closed, and closed by a theorem

This is the largest single result of the programme, and it is a **negative** one that the project proved
against its own preferred answer.

### 6.1 What was built

`DEMO-1`: a deterministic four-shell coaxial object (`M = 4` pieces per layer, always), `H = 0.2300 m`,
`r₄ = 0.0900 m`, anti-phased modulations so the components *exchange* cross-section at constant total.
Census: `N_layers = 1,069,767,441`, `pieces = 4,279,069,764`, canvas `65,536² = 4,295,967,296` cells, `pitch =
0.4001 m`, one plate per cell exactly. Traversal `σ`: `p = k·N + n`, `d = hilbert(p)`, word `(n<<2)|k` — 32 bits,
no padding.

### 6.2 The measurement that closed it

`DEPOSIT-BLIND` passed the deposit constructor a mapping that **records every read**. It read `M` and `H`.
It read none of `r₁, r₂₀, r₂ₐ, r₃₀, r₃ₐ, r₄` and none of the four areal densities — **0 geometric reads**.
Then six physically distinct objects were deposited:

| object | change | `r₄` | A3 (`2r₄ ≤ pitch`) | cut area (m²) | deposit digest |
|---|---|---|---|---|---|
| `O1` | reference | 0.0900 | yes | 2.7222e7 | `558d30e08fd32cf6` |
| `O2` | jacket ×1.67 | 0.1500 | yes | 7.5617e7 | `558d30e08fd32cf6` |
| `O3` | modulation phase inverted | 0.0900 | yes | 2.7222e7 | `558d30e08fd32cf6` |
| `O4` | densities reversed | 0.0900 | yes | 2.7222e7 | `558d30e08fd32cf6` |
| `O5` | radii re-stacked | 0.0900 | yes | 2.7222e7 | `558d30e08fd32cf6` |
| `O6` | jacket ×5.5 (violates A3) | 0.4950 | **no** | 8.2347e8 | `558d30e08fd32cf6` |

**Six objects, one deposit.** `I(canvas ; r₄) = 0` bits exactly, over a `2.78×` admissible spread in cut area.

The theorem behind it is one line: `p = kN + n` and `d = hilbert(p)` are functions of `(k, n)`; therefore
`deposit(O) = F(M(O), N(O))` and no other parameter of `O` can enter. Of the **12 declared parameters of
`DEMO-1`, 2 are visible (`M`, `N` ⇔ `H`) and 10 are not.**

### 6.3 The corollary that explains thirty earlier rounds

Every statistic computed on the canvas is a function of `(M, N)` and of the traversal `σ`. That splits all
possible tests into two exhausted classes, and both were measured:

- **Permutation-invariant statistics** cannot see `σ`, so they see only `(M, N)`. `MI-INVARIANT`:
  `17.9947` bits for component-major, layer-major **and a random permutation**, while pixel purity spans
  `99.99885% → 0%`.
- **`σ`-sensitive statistics** measure `σ`, not the object. Of the `0.06639` nats that separated the deposit
  from a shuffle (`422×` its sampling floor), **`99.2%`** is the four-contiguous-runs contrast — a property of
  the traversal, already measured in `DEMO-1` §4.3 at contiguity `1.0000` vs `0.9961`.

So `TOPO-CLOSE` (`b₀ = pieces`), `MR2-CLOSE` (disjoint support ⇒ `D_KL ≡ +∞`), `MI-INVARIANT` and
`POT-TRICHOTOMY` (`ΣΨ = 0.0` exactly) were **correct as measurements and wrong as answers**. They were asking
"is this declaration internally consistent", and answering no.

### 6.4 No image exists at any scale — the dichotomy

Two demands on one map, and they are contradictory. Not a defect of any algorithm; no better algorithm repairs it.

| demand | measured |
|---|---|
| injective (nothing lost) | `≥ ⌈√pieces⌉ = 65,415` sites per side ⇒ `2¹⁶`; canvas `26,221 m` |
| renderable (a person can look) | `2⁹` per side; `4K` still shows `0.19%` of the deposit |
| the gap | `16,384 = 2¹⁴` **exactly** — both powers of two, so the decimation is not approximate |

Nor is it a similarity image at any magnification: `sup d_3D` inside the object is `√((2r₄)² + H²) =
0.292062 m`, while `inf d_2D` between sites is `pitch = 0.400100 m`. The 3D support lies **strictly inside**
the 2D gap, so no scale factor `s` satisfies `d_2D ≈ s·d_3D`.

**An image is a many-to-one map.** A one-to-one map into two dimensions can be a *file*; it cannot be a *picture*.

### 6.5 Re-designation and what survives

The deposit is re-designated **`DEPOSIT-SERIAL`**: a lossless two-dimensional serialization of the plate
inventory. Judged as that, it is good — `4,279,069,764` plates × `4 B = 15.9408 GiB`, exact round trip,
**`0` mismatches**, contiguity **`1.000000`** along the curve (raster order gives `0.9961`), component-major
layout so a per-shell reduction reads one shell's axial history at a time. `deposit_serial_v1` meets all seven
locked criteria `A1`–`A7`.

One word had to be disambiguated (`D-2a`): **`lossless` must name its referent.** *Lossless (inventory)* is true
— a bijection `4,279,069,764 → 4,279,069,764`. *Lossless (object)* is false — `10` of `12` parameters never
reach a site. That ambiguity was exactly the difference between a file and a physical reduction.

`SFC-INDEX` survives as the one positive result of the space-filling-curve line: Hilbert beats raster
measurably (`1.0000` vs `0.9961`, median adjacent `|Δn|` `1.0` vs `128.5`). It is an index over the object; it
may not be called `σ`, and it is not a reduction.

### 6.6 Why the four dimension anchors came out backwards

Brouwer, Cantor, Hilbert and Kakeya/Wang–Zahl were offered to *forbid* a lossless 3D→2D collapse. Sixteen of
eighteen predictions held, and the two that failed were against the submission: **the deposit is a
dimension-0 object on both sides**, so Brouwer's invariance does not forbid it — it *satisfies* it trivially
(`A4` struck, `A4-GLOSS`). The theorem cited to forbid the deposit is the one that certifies it, and the
correct statement is `MAP-TRILEMMA` row 4: the map is permitted precisely because it is a file.

---

## 7. The optics line — specified, blocked, and honest about why

### 7.1 The object and the criteria

`σ_s,ab(ω, q)`: effective surface conductivity of a sheet at fixed projected area with conserved particle
number, `K_a = σ_s,ab^eff E_b^eff`. The conformance specification
`docs/specs/surface_conductivity_v1.md` reached **v1.3** and locks **`S1`–`S15`**:

| group | criteria |
|---|---|
| v1.0 core | `S1` units · `S2` energy budget `R+T+A=1` · `S3` passivity · `S4` Kramers–Kronig · `S5` f-sum **partition** · `S6` charge conservation (Ward) · `S7` `τ` **solved** · `S8` branch declared · `S9` no visibility conclusion |
| v1.1 strengthenings | `S10` `FSUM-SINGLE-SOURCE` · `S11` `FSUM-FINITE` · `S12` `DRUDE-DOMAIN` · `S13` `TAU-PROVENANCE` |
| v1.2 | `S14` `BUDGET-DECLARED` · `S15` `G-CONSISTENT`; `S12` split into `S12a` (necessary) / `S12b` (sufficient) |
| v1.3 | prose-only correction of §10a.2's partition citation (`E5`) — no criterion touched |

Under `R1-B1`, the budget quantity the interface asks for is refined by `N7-SPLIT` (round 41): the Drude
weight is a functional of the **participating** carriers `n_free,2D` — the old single `n_2D` (which the
baseline filled with the bookkeeping total `n_Q,2D = Z_A·N_B`) is no longer a definitive optical input.

`S1`–`S9` are byte-identical across v1.0→v1.3 and remain locked by the v1.0 digest. There is **no second
specification** and none is intended: a *reconstruction* spec needs a state to reconstruct, and the state is
what `R1-B1` owes.

### 7.2 Applied to the record's own module, three criteria fail

`src/optics/sigma_s_lindhard.py` passes its own `T1`–`T3` and fails the specification:

| criterion | verdict | measured |
|---|---|---|
| `S4` Kramers–Kronig | **FAIL above `2E_F`** | residual `1.153` at `1.5e8 eV`, `0.638` at `2e8 eV`; `≤ 1.2e-15` inside the reported 1–3 eV band |
| `S5` f-sum partition | **FAIL** | `W_Drude = W_total` exactly (`ratio 1.000000000003`), and the interband step has **unbounded** weight |
| `S6` Ward identity | **not attempted** | no `Π^R` is constructed; the Drude form is written directly |
| `S7` `τ` solved | **FAIL** | `τ` is an explicit scan (`TAU_SCAN`), labelled OPEN in the module header |

### 7.3 Three results that turned a complaint into a structure

**(a) `FSUM-SPLIT` is a theorem, not a bug.** `∫₀^∞ σ₀/(1+ω²τ²) dω = σ₀π/2τ = πe²n/2m*` — the `τ`
cancels identically (measured `6.9e-15`). A Drude pole consumes the whole budget **by definition**, so no
amplitude can repair the partition; the legal parameter must be a *fraction* `f_j ∈ (0,1)`, `Σf_j = 1`.

**(b) One root, two symptoms — `STEP-NO-SCALE`.** A step `Re σ = A Θ(ω−ω_g)` has an exact Hilbert partner
`Im σ = −(A/π) ln|(ω_g+ω)/(ω_g−ω)|`, and since `Re σ → A` at high frequency its weight diverges **for every
finite broadening**: at `Γ/ω_g = 1e-3` the broadened step already carries `4.50×` the whole budget at `10ω_g`
and `49.5×` at `100ω_g`. So broadening looks like a causality repair while leaving the budget untouched — which
is why the root had to be named separately from its two symptoms. `S4` and `S5` nevertheless remain
**independent verdicts**, with a fully populated `2×2`: pure step (`S4` pass / `S5` fail), truncated step with
an inherited partner (fail / pass), the module as-is (fail / fail), finite-weight oscillator (pass / pass,
`W = S_pπ/2`, K-K residual `2.3e-7`). **A band edge bounds the weight and does not adjust `Im`.**

**(c) `440.18 MeV` was an identity, not a bound — and has been withdrawn.** The one-parameter family is
`ω_end(f) = ω_g + f W_total/A`, measured `146.7400 / 293.4592 / 440.1784 MeV` at `f = 0 / 0.5 / 1`. The
`f = 1` endpoint is the case in which the Drude pole receives **nothing**; the module's own partition is
`W_intra/W_total = 1.000000000003` (`sc_route` §F — the pole takes the whole budget, `τ` cancels), so the
residual budget is **`0` identically** (`sc2` §A.1 P1; the measured `−3e-12` is quadrature floor), and no
interband term is admissible at any `ω_end > ω_g`. (An earlier draft of this report quoted the partition as
`1 − 7.1e-5`; that figure is the `m*`/`E_F` double-pinning slack of `sc2` §A.2, not a partition share —
errata `E5`, `docs/decisions/sc4_partition_citation_errata_v1.md`.) Worse, `(W/A)/(2ω_g) = 2πn/k_F² = 1`, hence `ω_end(f=1) = 3ω_g` exactly (measured
`2.999717`; the `2.8e-4` is the `73.37/73.3648` MeV rounding). **`440 MeV` carries no information about
`n_2D`, `g` or `v_F`, and is forbidden as an input to `R1-B1`.**

### 7.4 Two internal inconsistencies found in the module

- **`G-SPLIT`, factor `2.000000000000`.** `A_INTER = e²/(16ħ) = 1.521334e-05 S` is the **`g = 1`** single-cone,
  spinless height; `k_F = √(2πn)` is **`g = 2`**. The interband height is low by exactly 2. The `1/4` that the
  first ruling called "underived" is `g/4` at `g = 1` — underived *because* inconsistent.
- **`V-F-IMPLIED`, `v_F = 1.000071 c`.** From the record's own `(n_2D, E_F)` pair. The record is a `v_F = c`
  Dirac model and never says so. The energy ceiling scales **exactly** with `v_F` (`3.33e-16` over four
  decades): at a graphene-like `c/300` it is `1.4673 MeV`.

### 7.5 The `τ` clause became an instrument

`TAU-OBLIGATION` was a sentence; it is now two tests. `α = (4/π)arctan(−Im σ/Re σ)` at the peak of `−Im σ`
recovers `α ∈ {1, 0.9, 0.7, 0.5}` to `1.1e-16`, and the peak sits at `ωτ = 1` for every `α`. But `α = 1` at a
single point is reachable by **two** poles (exact root at `ωτ₁ = 0.697897`), so `S12b` demands the
**one-parameter collapse**: `max_ω |α − (4/π)arctan(ωτ_eff)| < 1e-6` — single pole `4.4e-16`, two-pole 3:1
`8.6e-2`. And the instrument has a measured blind spot (`ALPHA-BLIND`): moving `f_intra` from `0.9` to `0.5`
changes `σ₁(0)` from `388.557` to `215.865 S` (ratio exactly `1.8`) while `α_peak` moves only `1.038 → 1.201`.
**`α` can refute a single pole; it cannot certify one and cannot rank the partition.**

`τ` is also not one number: in a static Thomas–Fermi 2D Coulomb model at the record's screening,
`τ_tr/τ_sp = 91.548`, and the ratio moves to `138.016` (+`50.8%`) if the kernel is `(q²+q_TF²)⁻¹` instead of
`(q+q_TF)⁻²`. `91.5` is the **size of the ambiguity**, not a value of either `τ`.

### 7.6 The interface `R1-B1` now owes — four plus four

Necessary (each measurably insufficient on its own): `n_2D` · `g` (the effective degeneracy actually
participating) · `v_F` · `ω_end` (from band structure, not from a budget identity).
Also required: the **scattering mechanism** that fixes `τ` · evidence for the **Drude-domain reduction**
(`S12a/b`) · the **current operator and matrix elements** that set `A_inter(g)` · and **`f_intra`**, the
intraband fraction — required because the optics criteria were measured to be blind to it, so only the matter
model or a measurement can supply it.

---

## 8. Closed, open, forbidden

**Closed.**
`MR2` as a gate · `DEPOSIT-BLIND` / readable-image line · `GD10`, `GD11` (for this line) · `GD6` with `ME3`
retired · `GD9` (objective = fidelity + locality) · `ME1` → `CM5` (reclassified) · `δ_ov` (binary, unusable) ·
conversion clock (`Λ_max` retired) · `deposit_serial_v1` (`A1`–`A7`) · `R5-L2` re-run on the v3 baseline
(passed, but grade-capped at *designated-background test optics* until `G4` and `G5′` pass) · `MR1.0`
(necessitated, not merely observed) · the four tiers admitted (4/4).

**Open (the whole critical path).**
`G2′`/`R1-B1` EOS · `G3′` (`P2-C6` stability, NEC scope) · `G4` (bulk instability localisation) · `G5′`
(`N7` carrier conservation) · `G6`/`DC2` · `Δz_res` · `δ_E,max` · `ℓ_samp` · `Δz_tol` · `f_intra` · `τ`.

**Forbidden (with the row that forbids it).**
Any visibility / transparency / opacity / "mirror-like" conclusion before `G6` (`S9`, §11.1) · citing a
`DEMO-1` frame as evidence of readability (`D-2`) · the unqualified word *lossless* (`D-2a`) · a bare
`ω_end` (`S14`) · scanning `τ` as a response (`S13`) · `440 MeV` as an input (`THREE-OMEGA-G`) · backward or
forward selection of a matter branch (§7.5, §11.3) · reusing `ME1` or filling `ME3`'s slot (would recreate the
conflation the rulings removed).

---

## 9. The defect ledger — what the project got wrong, kept in the record

This is a deliberate asset, not an embarrassment. Some forty self-caught defects are archived, and they
cluster into seven recurring classes. Naming the classes is what stops them recurring.

| class | instances | example | standing rule |
|---|---|---|---|
| a derived constant registered **tighter than its derivation** | **4** | `H_max = 0.184699` vs derived `0.184684`; the FAIL stands | register the derivation's own precision |
| a **threshold fixed before the instrument was calibrated** | **5** | oscillator `S5` at `1e-10` against a `1e-8` quadrature floor; `Q2`'s registered `\|f_inter\| < 1e-15` sat below the `6.88e-15` floor measured one round earlier | measure the floor, then set the band |
| a **text pattern instead of a count** | **5** | `P13` matched the bare token `S` — 9 spurious hits; `[X]` printed `0` where the answer is `2` | count, never regex |
| a **figure chosen before its constraints were checked** | **3** | `30.25×` spread including a member that violates the object's own A3 | check the constraint first |
| **polarity / sign inverted** in a table | 2 | five cells of the `2×2` independence table | assert the boolean, print it |
| **transposed digit or dropped factor** in arithmetic | 4 | `12,899.4` for `12,989.4`; `N = 9e20` for `9e14` | recompute from `conv.py`, never retype |
| a **fabricated hash** | **1** | a `sha256` typed from memory into a lock file's `supersedes` entry; caught by cross-checking the sibling lock | **every digest is copied from a file, never retyped** |
| a **measured number quoted from the wrong measurement** | **1** | `W_intra/W_total = 1 − 7.1e-5` attributed to `FSUM-SPLIT`; the measured partition is `1.000000000003` (`sc_route` §F) and `7.1e-5` is the `m*`/`E_F` pinning slack (`sc2` §A.2) | **every measured number is quoted with the product that measured it, by file and line** |

The worst of these is the last one, and it is the only one whose failure mode is silent: a hash is a *claim of
identity*, so an invented one would have defeated the whole locking discipline without any test failing.

Two further classes are methodological rather than numerical; the first was caught by the governor reviewing
my reasoning, the second by auditing my own instrument:
- **wrong problem attribution** — a "yield-strength misreading" was treated as a defect to repair when the
  record contains no such misreading at all (`REPAIR-ABSENT`; 0 physics-sense occurrences, all 54 uses of `σ_s`
  are conductivity). The standing rule: *a correction is admissible only if the proposition it retracts can be
  cited by file and line; otherwise it is `REPAIR-ABSENT`.*
- **a tautology reported as a test** — `P1` in the SC-2 round compared an expression with itself; it can only
  validate the quadrature, and the product now says so. SC-3's `Q2` joined it: the residual budget was printed
  from a hardcoded `f_intra = 1.0` rather than measured, and the registered `1e-15` threshold sat below the
  quadrature floor — the conclusion survives as an identity, and the governor ruling **revokes the printed
  pass as evidence** (`E5`).

---

## 10. Naming hazards a new reader will hit

These are live traps in the record, not errors of physics.

1. **`G4` has two referents.** Roadmap v2.x's "P2 stage gate" (`DCC_P2_Report_v2.md` reports it as **pass**) and
   roadmap v1.4 §10.2's "finite-region matching" (**not passed**). The chain that governs is v1.4's.
2. **`d_∥ = 15.40 fm` and `d_par = 6.7420 fm` are different quantities.** The first is `1/√N_s` from the
   *nuclear* column density and is the `C1` cell; the second is `1/√n_2D` from the *carrier* density and is the
   v3 baseline. They differ by `√(n_2D/N_s) = 2.285`. Quoting `15.40 fm` beside `73.37 MeV` mixes the two
   baselines — that is exactly the errata item `E1` of the SC ruling.
3. **Three namespaces share the letter `S`.** `S1`–`S15` are the `σ_s` spec criteria; `S1`–`S10` are the
   registry's formal disambiguation rules (`S1` = "declare the domain before use"); `S0`–`S4` are the scene
   stages. Always scope the citation — `S5` alone is both a spec criterion and a registry rule.
4. **`τ` alone is the Drude relaxation time**; the conversion clock is `τ_conv`. The registry makes this
   mandatory, because Phase 2 of the phased route wrote "intrinsic time scale τ" and thereby created a second
   owner.
5. **`L1`–`L4` has three meanings** (optics layers, `FL` fidelity levels, `R2-D` redshift layers). The
   registry's worst collision; `L` may never be used as a bare label.
6. **`ME1` is vacated, not renamed.** It is a deprecated alias of `CM5`; the number must not be refilled.

---

## 11. What this record does not claim

- It does not claim DCC is true, false, or refuted. It claims that **ordinary matter at fixed area is NO-GO**
  (row 1), that **`D2` holds and strict `D3` does not**, and that **this mechanism cannot produce a readable 2D
  image of a 3D object**.
- It does not claim the deposit is empty. The deposit is a **1-dimensional coordinate plus a band label, laid
  out in 2 dimensions** — real content (an axial coordinate) that is simply not the object.
- It does not claim that no rendering story exists. It claims this one does not, and says exactly why:
  adjacency is preserved, metric is destroyed, the enumeration is encoded rather than the object.
- It does not claim the optics question is unanswerable in principle — only that it is unanswerable **before
  `R1-B1`**, and that a null result ("no admissible stable matter state" or "no response satisfies `S1`–`S15`")
  is a valid physical conclusion of the same class as `G0′` row 1, **not** a project failure.
- It does not claim any gate beyond `G0′` and `G1`.

---

## 12. Where it stands, and the single next step

The programme has spent thirty-nine rounds and has produced, in net terms:

- **four lines closed by negative result**, each stronger than the positive claim it replaced
  (`C3` NO-GO in-action; ordinary matter at fixed area NO-GO; the deposit is blind to the object; there is no
  image at any scale);
- **one closed constructive result** — `deposit_serial_v1`, the first thing in the route that closed by
  *finishing* rather than by refusing;
- **one instrument** that converts a slogan into a measurement (`α` collapse, with its blind spot measured);
- **one locked specification with no object** — `S1`–`S15`, deliberately written before the candidate exists so
  that it cannot be retro-fitted to one.

The blocker is a single physical object, and it is not ambiguous:
`R1-B1` must deliver `(n_2D, g, v_F, ω_end)` **plus** a scattering mechanism, Drude-domain evidence, current
operator and matrix elements, and `f_intra`. Until then every `σ_s` is a test object, not a conclusion, and
`G6`/`DC2` stays `NO-GO`. The three prohibitions that keep this honest are already in force: **do not scan `τ`**,
**do not pick the matter branch that makes the optics work**, and — from the SC-4 ruling — **do not re-run the
revoked `Q2` or derive material properties from the current Drude construction**: the optics line waits for
`R1-B1`. SC-4 found an erroneous acceptance pass, not a new physical blocker; the blocker is unchanged.

**Round 40.** The wait has become constructive: `docs/R1B1.md` is the governor's R1-B1 charter, and its named
Phase-0 deliverable now exists — `docs/specs/R1_B1_Microscopic_Matter_Model_v1.0.md`. It fixes the two-question
structure (matter before response), the Layer-0 geometric protocol, the DOF inventory with evidence tags, `N7`
as a carrier census, the `S-STATE-1..6` stability classes, and the `H → Ĵ → Π^R → σ(ω) → W` chain, with every
quantity tagged `DERIVED`/`MEASURED`/`ASSUMED`/`FITTED`/`UNRESOLVED` so an `f_intra = 1` recurrence cannot
happen silently. Its central open question is the record's own hardest one: *which degrees of freedom still
exist at `0.13–0.26 n₀` inside a `1.68–1.99 fm` layer* — where the electron z-confinement scale is
`311–369 MeV`, i.e. `≥ 12×` the envelope's `μ_e` maximum. The frozen baseline is re-classified there
quantity by quantity (bookkeeping vs. baseline assumption vs. forbidden), which is the operational meaning of
"R1-B1 does not start by fitting `(n_2D, g, v_F, ω_end)`". Phase 1 — the minimal physically closed microscopic
model — is next, and it registers before it computes.

**Round 41.** The governor's Phase-0 review is executed as spec **v1.1**: Phase 0's structure is accepted;
four physical boundaries are fixed before `R1B1-P1`. (1) The EOS registration baseline (`L_z = 1.0 fm`,
reproduction only) is separated from the `K1` valid computational domain (`[1.68, 1.99] fm`,
interpretation only) — Phase 2 scans `L_z`. (2) The z-confinement conclusion is re-scoped to the
registered strictly-confined model under its boundary conditions: the energy-scale comparison refutes
that model, it does not prove the nonexistence of electronic degrees of freedom — substitution
mechanisms are re-opened. (3) `n_2D` is split into `n_Q,2D` and `n_free,2D` (`N7-SPLIT`), with `N7` a
constraint solved from the microscopic state. (4) The R1-B1 symbol table is closed (`R1B1-SYMBOLS`;
`d_par`/`d_∥` deprecated inside R1-B1). The density figure is a reference interval, not a phase
assertion. New spec §15 defines `R1B1-P1`: three acceptance tiers (`P1-A/B/C`), the hard veto
`P1-CLOSURE-FAIL` (seven conditions, any one blocks numerics), and three admissible outcomes — closure,
proof of inapplicability, or a named statement of missing foundational physics. `G6`/`DC2` remains
NO-GO.

**Round 42.** `P1` theoretical work began under its registration (numerics still vetoed; a CAS algebra
checker is the only tool used, authorized by a registration amendment). The kinematic closure review
(`runs/R1B/r1b1_p1_closure_review_v1.md`, 8/8 symbolic checks) establishes: the Christoffels reduce to
`Γ^t_zz = BḂ`, `Γ^z_tz = Ḃ/B`; `∇_μT^{μt} = ∂_tρ + (Ḃ/B)(ρ + p_z)` — **only the z-stress couples**;
the background work term **`dE/dt = −Ḃ·p_z` per unit lateral area** (`B-WORK-TERM`) — derived and
checked, never assumed zero; Maxwell carries `1/B²` z-weights plus a `(Ḃ/B)E_⊥` transverse damping;
every field equation acquires the `(Ḃ/B)` friction; internal `U(1)` charges (electric, baryon) survive
exactly. The DOF set and the action **close simultaneously at the kinematic level**; what remains open is
exactly what the interface anticipated — the interaction sector (`P1-C`), the electron z-disposition,
and internal nuclear DOF.

**Round 43.** The governor's Dirac-operator mandate is executed under the two-level ruling (kinematic
closure passed ≠ dynamical closure ruled — the veto lifts only on the latter, now binding in spec
§15.1): `runs/R1B/r1b1_p1_dirac_closure_v1.md`, 11/11 symbolic checks. The tetrad and spin connection
are derived (`ω_z^3_0 = ω_z^0_3 = Ḃ` only); `Ω_z = −(Ḃ/2)γ⁰γ³` is uniquely fixed by `∇_μγ^ν = 0` (the
opposite sign fails all 16 conditions); the **EOM form is fixed by the mass shell** — the
`(iγ^μD_μ ± m)` form was constructed, tested, and *rejected* (`H² = p² − m²`, unphysical in this
signature, archived in the product), leaving `(γ^μD_μ + c_m m)ψ = 0`; and the Hamiltonian
`H_D = −(α_xp_x + α_yp_y + (α_z/B)p_z) + ic_mγ⁰m − (I/2)(Ḃ/B)𝟙` has its identity term **extracted from
Tr(H)/4**, not assumed: it is the measure-compensation term (norm `∫Bψ†ψ` conserved; the 1-dimensional
analogue of FLRW's `−(3iH/2)𝟙`), not dissipation. `p_z` remains a good quantum number — round 42's
"z-mode transition" wording is superseded. The round-42 qualifications are recorded in the closure
review §8 (E_area normalization; `S^t_bg` not-a-source; EM damping ≠ dissipation with the
orthonormal-frame requirement now in spec §8; the `R6` conditions table). Remaining gates: `P1-C`
interaction declaration, the weak fork, the z-disposition,
and the component-level `∇_μT^{μν}` verification. Numerics remain vetoed; `G6`/`DC2` remains NO-GO.

**Round 44 — the P1 closure.** Under the governor's directive to complete all remaining tasks
unilaterally, every task completable without the numerical-veto adjudication was completed, and every
other item was driven to a named, falsifiable terminal disposition
(`docs/decisions/r1b1_p1_closure_certification_v1.md` §4). **`P1` is CLOSED at the theory level —
outcome #1 of the three-outcome interface certified**: all seven `P1-CLOSURE-FAIL` conditions assessed
clear (`P1-OUTCOME`). The `P1-A` declarations (weak fork both branches; per-field templates; the
`S-STATE-6` timescale proposed = conversion clock `τ_conv` + `1/c_s`, pending adjudication) and the
`P1-C` interaction declaration (the BPS/BBP/NV inner-crust band and the χEFT few-percent sub-saturation
anchor **contain** the target regime `0.021–0.042 fm⁻³`; limitations named: the cold-catalyzed
assumption, the weak-off partial applicability, the lattice-config inapplicability-as-state) are
delivered (`runs/R1B/r1b1_p1_declarations_v1.md`). The registered instrument defect: the component-level
current check fails in the y-sector only — traced to the transpose asymmetry
`(γ⁰γ²)ᵀ = −(γ⁰γ²)`; the physics stands on the round-43 master identity and the Noether theorem, and
the component-level completion is an optional non-gating appendix. **`R1B1-P2` is registered pending
the veto-lift adjudication** (`r1b1_p2_registration.md`: `L_z` scan over the `K1` domain, both weak
branches, thresholds pre-set from the v2/v3 precedents, kill conditions registered). The single
remaining unlock in the entire programme is that one adjudication; everything downstream (`G3′`, `G4`,
`G5′`, the optics outputs) is chain-blocked behind it; the programme's negative results are terminal in
the valid-NO-GO class.

---

## Appendix — where everything lives

| subject | authority | product |
|---|---|---|
| labels, collisions, errata for archived text | `docs/conventions/symbol_registry.md` | `runs/CONVENTIONS/symbol_lint_results.txt` |
| frozen baseline, seven-row verdict | `docs/decisions/G0p_seven_row_verdict_v3.md` | `runs/G0/g0p3_results.txt` |
| gate chain definitions | `Macro3D_to_2D_Smooth_Reduction_Roadmap_v1.4.md` §10.2 | — |
| route execution, Phase 0–3 | `docs/decisions/route_completion_v1.md` | `runs/ROUTE/p{0,1,2,3}_*.txt` |
| readable-image line closed | `docs/decisions/route_terminus_v1.md` | `runs/ROUTE/deposit_blindness_results.txt`, `…_figure.png` |
| dimension anchors | `docs/decisions/dimension_anchors_ruling_v1.md` | `runs/DIM/dimension_anchors_results.txt` |
| `GD6` / `ME3` retired | `docs/decisions/me3_phi_disposition_v1.md` | `runs/ME3/me3_phi_results.txt` |
| serialization format | `docs/specs/deposit_serial_v1.md` (`e3c2a555…`) | `runs/SERIAL/serial_results.txt` |
| `σ_s` conformance criteria | `docs/specs/surface_conductivity_v1.md` v1.3 (`ccc2fb78…`) | `runs/OPTICS/sc{,2,3}_results.txt` |
| post-v1.2 partition-citation audit (`E5`) | `docs/decisions/sc4_partition_citation_errata_v1.md` | `runs/OPTICS/sc3_results.txt` (`E5` appended) |
| R1-B1 microscopic matter model (Phase 0) | `docs/specs/R1_B1_Microscopic_Matter_Model_v1.0.md` | trigger `docs/R1B1.md`; predecessors `runs/R1B/r1b1_eos_results.txt` (v2), `r1b1_eos_v3_results.txt` (envelope) |
| R1-B1 P1 theoretical closure | `runs/R1B/r1b1_p1_closure_review_v1.md` | check `runs/R1B/r1b1_p1_closure_check_results.txt`; registration `runs/R1B/r1b1_p1_registration.md` |
| R1-B1 P1 Dirac-operator closure | `runs/R1B/r1b1_p1_dirac_closure_v1.md` | check `runs/R1B/r1b1_p1_dirac_check_results.txt` (11/11) |
| R1-B1 P1 declarations + closure certification | `docs/decisions/r1b1_p1_closure_certification_v1.md` | `runs/R1B/r1b1_p1_declarations_v1.md`; `r1b1_p1_current_check_results.txt` (instrument defect recorded); `r1b1_p2_registration.md` (pending veto lift) |
| the four tiers | `docs/specs/intrinsic_structure_tiers_v1.md` + Annex A | `runs/MATRIX/structure_tiers_results.txt` |
| matrix reading rules | `docs/decisions/matrix_reading_rules_v1.md` (`MR1`–`MR3`) | — |
| display / label rules | `docs/conventions/display_conventions_v1.md` (`DC1`–`DC9`) | validator in §5 |
| round-by-round log | `.workbuddy/memory/2026-11-{20,21,22}.md` | — |

*Content generated by AI*


---

## Erratum E1 (round 58) — the `G5′` row's stated reason applies to the frozen object

**The row is not edited.** `RQ-08` produced `runs/R3/n7_recheck_results.txt`.

- **E1** The `G5′` row says `N7` blocks the gate *"at `μ_e = 73.37 MeV`"*. That number belongs to the
  frozen baseline. At the solved `HYB` density (`μ_e = 21.5445 MeV`) the vacuum `Q` comparison still
  yields `6/6` open, so the arithmetic reproduces; but the host-specific threshold
  `Q_eff,p = 0.782 + ΔF = 21.0335 MeV` equals the solved `μ_kin` to `−3.55e−15` in the `β` residual,
  and the state has `n_e = 1.897e−3 fm⁻²` with a measured free fraction of `1.000`. The removal rule
  therefore does not transfer to this object. **E2** The row's status stays **NOT PASSED** — this
  round removes one stated objection, not the gate: §1's model/subsystem/occupation/probe slots and
  the separate `G4` bulk-instability localization are unresolved.


---

## Erratum E3 (round 61) — the `G4` row's stated reason is stale, but its status is unchanged

**The row at §4 line 123 is not edited.** `RQ-07` emitted
`runs/R4/r4_localisation_results.txt`.

- **E3** The row says *"R4 grid-scale instability remains unlocalised in the bulk"*. That conflates
  two questions. The BULK/EDGE discrimination was already fixed at 0.1% precision by `LOC-C7`
  (`runs/R4/r4_instability_localization_stage2_results.txt:43-48`) and adopted in
  `docs/decisions/r4_finite_region_geometry_v1.md` §7.2-7.3. The remaining diagnosis is what
  `RQ-07` closes: `runs/R4/r4_localisation_results.txt:40-44` gives `Re lambda = 0.51220 /
  0.63602 / 1.01514` at N = 16/20/32 with a three-point exponent `p = 0.988`, and
  `runs/R4/r4_localisation_results.txt:62-80` fires the registered non-localisability slot.
  Corrected reason: *"bulk UV sector classified; no finite continuum localisation length; B-test
  remains uncured"*. **The status stays `NOT PASSED`**: diagnosis is not repair.
- **E4** The round-58 sentence above ("the separate `G4` bulk-instability localization [is]
  unresolved") is narrowed, not retracted: localisation is resolved; the B-block cure and the
  `G4` gate verdict remain open. `G5′`, `G6`, `B1/B3/B4/B6`, and the `G4`/`G5′` chain are untouched.

---

## Round 65 — Phase 1c dependency audit: the repricing trigger fires no price change

**Product:** `runs/P1/phase1c_repricing_results.txt`, pre-registration
`runs/P1/phase1c_repricing_registration.md`, instrument
`src/p1_symbolic/phase1c_repricing.py --write`. Non-RQ technical review authorized by G-64-01 §3's
consequence clause; no route authorization, no queue item opened.

**Question:** does the Phase 1b flat-slice result reprice any rung or move any gate, terminal class,
or threshold in the D8 table? **Answer: no.** Counts: `rung_moves = 0`, `gate_moves = 0`,
`terminal_moves = 0`, `threshold_moves = 0`; `reason2_qualifications = 1`; `g0p_row1_trigger_records
= 1`; `g0p_row1_basis_dependency = 0`. `CHECK 7/7`, `IDENT 1/1`, `NEGCTRL 1/1`, `OVERALL PASS`.
The synthetic control proved the classifier can fire (injecting `f=0 curvature singularity` as
`RL-6`'s basis moved exactly `RL-6`).

**Why no price moved.** `G0′` row1's basis is `d∥ = 15.40 fm = 2.91e−4 a₀`, not the singularity
claim; `RL-0` is a myth (coordinate degeneration gives no finite object); `RL-1`/`RL-2` prices are
observer/relief/environment; `RL-3` was retired; `RL-4` is closed by `σ_s`; `RL-5` uses Geroch's
topology obstruction and the Schwinger flux, neither tested by Phase 1b; `RL-6` uses
`0.3 nm / 15.40 fm = 1.94805e4`, within `2.60%` of the ladder's rounded `2e4`. D8's selected path
`RL-1 + RL-2`, `V = ε`, `Φ = −4.5`, fingerprint and reverse-on are unchanged.

**Only changes made:** E4 to `docs/conventions/effective_2d_definition_v1.md` §5 (reason 2 is not
universal; reasons 1 and 3 are untouched), E3 to `docs/decisions/G0p_seven_row_verdict_v3.md`
(row1 trigger recorded, not applied), E5 to `docs/specs/relaxation_ladder_v1.md` (dependency audit).
All three errata were appended after product emission; the input digests printed in the product
are the pre-append ones and are not re-sealed. One pre-emission predicate defect was disclosed:
the `P1C-P4` tolerance was corrected from `0.5%` to `3%` before emission because `15.40 fm` and
`0.3 nm` are two-significant-figure prices. Ledger round 65 / `P1C-REPRICE-01` / `TECHNICAL-REVIEW`
added; `round_cursor` becomes 65. No gate mark, terminal class, threshold, RQ state, D1/D8 result,
route adoption or archived number changed.

