# Ruling — `SC-ROUTE`: the correction is right and has no object; two of its checks find a real defect

**Submission**: governor message of 2026-11-22 20:44 (+08), archived verbatim at
`runs/OPTICS/sc_submission_verbatim.md`.
**Registration**: `runs/OPTICS/sc_route_registration.md` (17 predictions, locked before measurement).
**Product**: `runs/OPTICS/sc_route_results.txt` (309 lines). **17 / 17 predictions hold.**

**Verdict: `PARTIALLY ADOPTED`.**

| | |
|---|---|
| **Adopted** | `σ_s` is the surface conductivity (restatement, not a correction); **Task C's three missing checks**, which bite; the demand that `σ_s` be *derived* rather than asserted; §V's non-blocking rule |
| **Refused** | the premise that `σ_s` was ever read as a yield strength; the metric as written; the `23.2 MeV` figure; §I.2's Poisson argument; the reduction as a route to the target |
| **New in the record** | `FSUM-SPLIT` and `KK-UV` — two real defects in `src/optics/sigma_s_lindhard.py`, found by applying the submission's own checklist |

---

## 0. The headline

> The submission's central move is to correct a misreading of `σ_s`. The misreading is **not in this
> record**: `docs/specs/`, `docs/conventions/` and the governing roadmap contain **0** occurrences of
> *yield strength*, *yield*, *plasticity*, *Poisson* or *Young's modulus* in any physics sense, and **0** lines
> that bind any of them to `σ_s`.

So the sentence "the yield-strength interpretation proposed earlier does not hold and should be withdrawn" is true, and it withdraws a decision that was never
taken. This is the second instance of the defect class recorded in round 31 (`MR2-D`: *the correction repairs
the previous submission's error rather than the record's state*); it is now registered as `REPAIR-ABSENT`.

**But** — and this is why the verdict is not simply "refused" — the submission carries two things that are not
restatements: a checklist the record does not satisfy, and a derivation the record never made. Both survive.

---

## 1. What the record already had (6 of the submission's propositions)

The submission presents five tasks (`P0`–`P5`) and four named tasks (`A`–`D`). Most are already built:

| submission | record | measured |
|---|---|---|
| Task D: `r=-Z₀σ_s/(2+Z₀σ_s)`, `t=2/(2+Z₀σ_s)`, `R,T,A` | **verbatim** at roadmap §6.4 | `P4` — all five present |
| Task D implemented | `rta()` in `sigma_s_lindhard.py`, `R+T+A=1` tested as `T1` | `P5` — archived, max dev `0.000e+00` |
| Task C: compare finite film vs effective sheet | **already mandated** in the same §6.4 (thin-film formula, `δ=2πnL_z/λ`) | `P6` |
| `dz_proper` vs `dz` | **already mandatory**, naming **four** quantities: coordinate interval, proper thickness, compact circumference, film thickness | `P7` — the submission proposes two |
| Task A: fix the carrier population first | **already gate `N7`**, inside `G5′`'s acceptance row, and ranked **first** among the approximation failures | `P8` |
| §VI: do not presuppose which branch | **already §8.4**, with **four** categories `A/B/C/D`, and its pre-classification already deleted for exactly this reason | `P9` — the submission's three are weaker |

`P8` is the sharpest of these. The submission calls Task A "most easily overlooked" (most easily overlooked). The record
writes:

> **N7:** if `μ_e` exceeds the electron-capture threshold of the nuclide hosting the carriers, then the
> "carriers" themselves are removed and any low-energy effective description based on an electron gas loses
> its object. R3/G5′ must first perform a **carrier-conservation check**.

and, in its assumption list, ranks it ①: *"conservation of particle number and particle species (**N7: invalid
at `μ_e = 73.4 MeV`, the primary source of approximation failure**)"*. It is the first thing the record says,
in the section the submission cites.

---

## 2. Three corrections the submission needs

### 2.1 The metric — `C²dz²` is not the record's, and contradicts the submission's own prose

The record writes the third-dimension scale factor three times, always as `B`:

```
roadmap l.142   ds² = g_ab dx^a dx^b + A²(t,x) dy² + B²(t,x) dz²
roadmap l.146   ds² = -dt² + dx² + A²(t,x) dy² + B²(t,x) dz²
roadmap l.162   dℓ_z = B dz,   L_z^proper = ∫ B(t,x,z) dz
roadmap §2.5    ds² = -dt² + A²(dy²) + B² dz²
```

The submission writes `ds² = -N²dt² + A²dx² + B²dy² + C²dz²` and then `dl_z = C(t,x)dz` — consistent
internally — **but its symbol list says "`B`: DCC third-dimension scale factor"**. So the submission's metric puts `C` on
`dz` while its own prose says `B` is the scale factor. One of the two is a slip; the record's convention makes
the prose right and the metric wrong.

This matters beyond bookkeeping: `L_z^proper = ∫ dl_z` is the quantity the submission's whole reduction
integrates over, and it is the quantity §2.5 already warns must never be conflated with three others.

### 2.2 `23.2 MeV` is a revoked baseline

`P10`. The module header states it explicitly: *"The 2026-11-21 run used the pre-v3 values (`n_2D = 2.20e27`,
`E_F = 23.20 MeV`), which are **REVOKED**"*. The current value is `E_F = 73.37 MeV` — **3.162×** the quoted one.

The number is stale; the conclusion it supported is not. `μ_e = 23.20 MeV` "exceeds the capture thresholds of
all registered nuclides" was row 7 of `G0p_seven_row_verdict_v1.md`; at `73.37 MeV` the thresholds are exceeded
**more deeply**, so *"the electron gas object is gone"* is more true, not less. The submission's Task A survives
its own stale input.

### 2.3 §I.2's Poisson argument is a non-sequitur

The submission's second correction is that "the Poisson effect cannot simply be compensated through `σ_s`", with the elastic relation
`ε_z = [σ_z - ν(σ_x+σ_y)]/E`. This is true, and it is aimed at nothing: the record contains **no** constitutive
relation, **no** `E`, **no** `ν`, and **no** stress field for a `D2` deposit (`E ≡ 0` by construction — the
`KIN-DYN` finding). There is no Poisson effect to compensate.

This is the same shape as `A4` in round 33: a true statement offered against a claim the record does not make.
Registered as `REPAIR-ABSENT` alongside §I.1.

---

## 3. The one thing the submission gets right that the record did not: Task C bites

`P13`: of the seven checks in Task C, **Ward, Kramers–Kronig and the f-sum rule are absent** from
`src/optics/sigma_s_lindhard.py`. The module tests three things — `R+T+A=1` (`T1`), the dissipation-free limit
(`T2`), and monotonicity of `Re σ_s` in `τ` (`T3`). It never asks whether the response is causal or whether its
spectral weight is legal.

Applying those two checks to the module's own function produces **two real defects**.

### 3.1 `FSUM-SPLIT` — the interband term has infinite spectral weight

The 2D f-sum rule fixes the total:

```
∫₀^∞ Re σ(ω) dω = π e² n_2D / (2 m*)  =  6.782282e18 S·rad/s
```

The module's Drude term **already equals this exactly**, at every `τ`:

| `τ` (s) | ∫ Re σ_D dω | πe²n/2m* | ratio |
|---|---|---|---|
| `1e-19` | 6.782282e18 | 6.782282e18 | `1.000000000003` |
| `1e-18` | 6.782282e18 | 6.782282e18 | `1.000000000003` |
| `1e-16` | 6.782282e18 | 6.782282e18 | `1.000000000003` |

It is exact for a reason: `σ₀ = e²nτ/m*`, so `∫σ₀π/(2τ) = πe²n/(2m*)` and `τ` cancels. The Drude channel
consumes the entire budget.

The module then adds `A = e²/(16ħ) = 1.5213e-5 S` as a **frequency-independent step** above `2E_F`. Its
integral is `A(Ω−ω_g)`, unbounded:

| cutoff | interband weight alone | total / f-sum |
|---|---|---|
| `1 w_g` | 0 | 1.0000 |
| `2 w_g` | 3.39e18 | 1.5001 |
| `3 w_g` | **6.78e18** | 2.0001 |
| `100 w_g` | 3.36e20 | 50.5070 |

**By `ω = 3ω_g` the interband channel alone has contributed more than the whole f-sum budget.** So:

> The interband amplitude is not "an OPEN model input". The total spectral weight is **already fully
> allocated**, so opening the interband channel must **debit** the Drude weight:
> `W_intra + W_inter = πe²n_2D/(2m*)`.

That converts an unspecified parameter into a **partition with one free number**, which is a much stronger
constraint than the module's `SIGMA_INTER_0` with an admitted-unknown line shape.

### 3.2 `KK-UV` — the interband term is not causal, above 146.74 MeV only

Kramers–Kronig requires an `Im σ` partner for every step in `Re σ`. For a step `A·θ(ω−ω_g)` the partner is
exactly `Im σ = −(A/π) ln|(ω_g+ω)/(ω_g−ω)|`; the module supplies **none**. Both pieces of the quadrature were
validated separately before use (Drude to `6.4e-7`, the step term to `6.2e-6` relative).

| `ħω` (eV) | module `Im σ` (S) | K-K residual (S) | relative |
|---|---|---|---|
| 1 | 64.12 | 6.60e-14 | `1.0e-15` |
| 3 | 162.9 | 1.98e-13 | `1.2e-15` |
| `1e2` | 28.30 | 6.60e-12 | `2.3e-13` |
| `1e6` | 2.84e-3 | 6.60e-08 | `2.3e-05` |
| `1e8` | 2.84e-05 | 8.06e-06 | 0.284 |
| `1.5e8` | 1.89e-05 | 2.18e-05 | **1.153** |
| `2e8` | 1.42e-05 | 9.07e-06 | 0.638 |
| `3e8` | 9.47e-06 | 5.18e-06 | 0.547 |

**In the band the module actually reports — 1, 2, 3 eV — the model is pure Drude and K-K holds to `1e-15`.**
The violation lives entirely above `2E_F = 1.4674e8 eV`, five orders of magnitude above the eye band. The
residual diverges logarithmically as `ω → ω_g`, so no choice of `A` repairs it: the *form* is inadmissible, not
the amplitude.

This is the precise repair instruction: replace the constant step with a **decaying lineshape** normalised to
its share of the f-sum. A constant is the one lineshape that cannot be causal.

---

## 4. The reduction is exact, and it does not reach the destination

### 4.1 It derives the record's ansatz (`P17`)

`σ_s = ∫ dℓ_z σ_3D,∥` with the 3D Drude form gives `L_z·e²n_3Dτ/m* = e²n_2Dτ/m*` **identically**, because
`n_2D := n_3D L_z^proper`. Measured deviation `0.0e+00` at `L_z = 10⁻⁹, 10⁻⁸, 10⁻⁷ m`.

So the submission converts `R5-L2`'s **asserted** 2D Drude form into a **derived** one. That is a genuine
credit — the first derivation the ansatz has had. It is also, as an identity, content-free about the object: it
is the definition of column density restated.

### 4.2 Its validity condition (d) is false at the target (`P16`)

The submission lists five conditions for the reduction to hold, the fourth being *"whether the three-dimensional material still retains its original electronic state"*.
The record answers that condition directly, as row 1 of its seven-row verdict:

> | 1 | Maintain the body's original atoms, chemical bonds, and non-covalent network at fixed area | **NO-GO** |
> under the specified model assumptions `d∥ = 15.40 fm = 2.91×10⁻⁴ a₀ ≪ a₀`; and bound states cease to exist
> once `L_z < L_z^ion = 1.66 Å`

| baseline | `n_surface` (m⁻²) | `d_par = n^{-1/2}` | `d_par/a₀` |
|---|---|---|---|
| v1.4 (revoked) | 4.2155e27 | 15.4019 fm | 2.911e-04 |
| **v3 (current)** | 2.2000e28 | 6.7420 fm | **1.274e-04** |

The reduction is exact where `σ_3D` exists — many atomic layers — and the endpoint is at `d_par ≈ 1.3e-4 a₀`
with `L_z` below `1.7 Å`, i.e. one layer or less. **The bridge's far end is exactly where `σ_3D` stops being a
defined object.** The submission says so itself (condition d), which is to its credit; it then proceeds as if
the formula were the route.

---

## 5. The omission: `τ`

The record states the `G6`/`DC2` blocker in a specific form — *"a compliant `σ_s(ω)` with a **solved** `τ`"* — in
`docs/conventions/display_conventions_v1.md` and `docs/decisions/route_completion_v1.md`, and repeats it
elsewhere as `"τ remains an OPEN input — a σ_s at a scanned τ is parameterised, not solved"`.

The submission's route (Kubo → `Π^R` → `σ_s`) would in principle **determine** `τ`. But the submission never
mentions `τ`: its only two uses of the word are `τ_xz` and `τ_yz`, the **shear-stress components** in its
plane-stress argument. It uses *relaxation*, *collision*, *relaxation* **zero** times.

So the one quantity the record says is missing is the one quantity the checklist omits. A Task C that ends at
"Ward, K-K, passivity, f-sum, units, energy" would accept a `σ_s` at a *scanned* `τ` — which is precisely the
object the record already has and already refuses as non-compliant.

**Registered: `TAU-OBLIGATION`.** Any future `σ_s` submission must state what fixes `τ`. Without it, the route
reproduces `R5-L2`.

---

## 6. Defects of mine, standing in the record

- **`E1` — I quoted the revoked baseline in the very prediction that criticised it.** `P16` registered
  `"d∥ = 15.40 fm = 2.91e-4 a₀"`: `15.40 fm` is `1/√(4.2155e27)`, the v1.4 value, whose companion is
  `23.203 MeV` — the number I faulted the submission for in `P10`. At v3 the figure is `6.7420 fm = 1.274e-4 a₀`.
  The claim tested (`d_par/a₀ < 1`) holds on both baselines, so `P16` is a PASS; the *figure* was wrong, and
  the errata section says so rather than editing the registration.
- **`E2` — a text pattern scoring a false positive.** `P13`'s "dimensional check" row matched the bare token
  `S` anywhere in the source (9 hits, all spurious). The three genuinely absent checks are Ward, K-K and f-sum.
- **`E3` — two quadrature defects, both caught in-run and repaired:** (a) my first K-K grid truncated at
  `400/τ`, so the Drude validation came out short by exactly `2/(4000π) = 1.592e-4` — truncation, not physics.
  Replaced by the substitution `ω' = Su/(1−u)` (infinite range, no truncation error). The same defect then
  reappeared in the f-sum (`ratio 0.999841`), where the tail is added analytically. Both now close at
  `1.000000000003`. (b) At `ω = 0.5ω_g` a grid point landed exactly on the pole and printed `nan`, false-failing
  the step validation. Midpoint grid.
- **`E4` — a text pattern standing in for a counted quantity, for the fifth round.** Section [X]'s first
  version printed `0` files where the answer is `2`, because the record writes the phrase as `*solved* \`τ\``
  (markdown emphasis, Unicode `τ`) and my pattern expected the LaTeX token `\tau`.

---

## 7. What the gate can now say, and what it cannot

**Can.** `σ_s` is the surface conductivity and always was; the record's optics module satisfies energy
conservation but violates the f-sum rule and (in the UV) causality; the Drude channel already holds the whole
spectral weight; the reduction derives the ansatz and does not reach the target; `τ` is the missing quantity.

**Cannot.** Produce a number for `σ_s` at the DCC endpoint. That needs `R1-B1`, which the record already gates
at `G5′` through `N7`. The submission's own ordering (`Task A` first) agrees. **`G6` is not closable from here
by any amount of optics.**

---

## 8. Disposition

| item | status |
|---|---|
| `REPAIR-ABSENT` | registered — §I.1 and §I.2 correct readings the record never held |
| `SC-OWNER` | registered — `σ_s` = surface conductivity, input not constant, SI `S` |
| `FSUM-SPLIT` | registered — interband term double-counts; the constraint is a partition |
| `KK-UV` | registered — step term not causal above `2E_F`; needs a decaying lineshape |
| `TAU-OBLIGATION` | registered — any `σ_s` before a stated `τ` reproduces `R5-L2` |
| `REDUCE-DOMAIN` | registered — `σ_s = ∫dℓ_z σ_3D,∥` valid for `L_z ≫ a₀`, target is `≲ πa₀` |
| Task C | **adopted** — Ward, K-K, f-sum enter the record as required checks |
| Task B | **adopted in direction** — derive, don't assert; it works, and P17 shows it |
| §V non-blocking | **adopted** — already the record's position |
| the correction of §II | **refused as a correction, adopted as a statement** |
| the metric of §III.3 | **refused** — `C²dz²` is not the record's; `B²dz²` is |
| Spec `v1.0` as recommended | **written, scoped conditionally** — `docs/specs/surface_conductivity_v1.md` |

The spec is written as a **conformance specification**, not a reconstruction: it fixes the acceptance criteria
any candidate `σ_s` must satisfy, keeps the matter branch open per §8.4, and records what each criterion
currently returns. It cannot specify the reconstruction, because the state to reconstruct from does not exist
yet — which is the submission's own first task, and the record's `N7`.

**Gate: PASS** — MUST-FIX 0 / provenance blocking 0 / display 0.
