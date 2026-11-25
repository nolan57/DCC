# DCC Effective Surface Conductivity — Conformance Specification v1.3

**Status**: `CONDITIONAL` — the acceptance criteria below are **locked**; the object they apply to
(`σ_s` at the DCC endpoint) **does not yet exist**. v1.0 written 2026-11-22; v1.1, v1.2 and v1.3 amendments the same day.
**Ruling**: `docs/decisions/sc_route_ruling_v1.md` (v1.0), `sc2_lineshape_ruling_v1.md` (v1.1),
`sc3_budget_ruling_v1.md` (v1.2), `sc4_partition_citation_errata_v1.md` (v1.3).
**Registration**: `runs/OPTICS/sc_route_registration.md`, `sc2_registration.md`, `sc3_registration.md`.
**Product**: `runs/OPTICS/sc_route_results.txt`, `sc2_results.txt`, `sc3_results.txt`.

> **Version note — v1.2 in one line.** `S1`–`S13` unchanged in text except `S12`, which is split into `S12a`
> (necessary) and `S12b` (sufficient) because `α` at one frequency is measured to be reachable by a *two-rate*
> response. §10a adds `S14` (the budget must be declared as a fraction, in one unit convention) and `S15` (one
> `g`, in four places). §10a.4 corrects a v1.1 sentence that called `440.18 MeV` a bound: it is identically
> `3ω_g`. §11 gains clause 4: passing `S1`–`S15` does not identify a material.

> **Version note — v1.3 in one line.** A prose-only citation correction, no criterion touched: §10a.2's
> partition figure is `W_intra/W_total = 1.000000000003` (`runs/OPTICS/sc_route_results.txt` §F — the Drude
> pole takes the whole budget, `τ` cancels), leaving a residual of `−3e-12`, i.e. zero to the quadrature
> floor. The v1.2 sentence's `1 − 7.1e-5` was the `m*`/`E_F` double-pinning slack (`sc2` §A.2), mis-cited
> into the partition slot. `S1`–`S15` are byte-identical to v1.2; no threshold moved. Errata: `E5` in
> `docs/decisions/sc4_partition_citation_errata_v1.md`.

> **Version note — what v1.1 changes, and what it does not.** `S1`–`S9` in §5 are **byte-identical** to v1.0 and
> remain locked by the v1.0 digest. v1.1 is **additive**: §10 adds `S10`–`S13`, which are *strengthenings* of
> requirements the v1.0 text named but did not test (`S5`'s partition, `S7`'s "solved" `τ`). Nothing in §10
> weakens or re-tolerances anything in §5 — a candidate must pass §5 **and** §10. §11 records the null-result
> clause. No second specification exists and none is intended: the reconstruction spec is still blocked on
> `R1-B1`.

> **Why this is a conformance spec and not a reconstruction spec.** The governor recommended a
> *Reconstruction — Technical Specification v1.0*. A reconstruction needs a state to reconstruct from. The
> record's own gate `N7` (inside `G5′`) says that at `μ_e = 73.37 MeV` the electron gas **loses its object**,
> so the state does not exist until `R1-B1`'s β-equilibrium EOS is done — which the submission also says
> (`Task A` first). What *can* be fixed now, and is fixed here, is the set of tests any candidate must pass.
> This spec therefore constrains without presupposing, which is the only form available before `R1-B1`.

---

## §1 Object

`σ_s,ab(ω, q)` — the effective surface conductivity of a sheet at **fixed projected area** with **conserved
particle number**, defined by the response of the surface current `K_a` to the tangential electric field
`E_b^eff`:

```
K_a = σ_s,ab^eff (ω, q) E_b^eff
```

`σ_s` is an **input to the optics stage, not a universal constant** (roadmap §6.4, `S10`). SI unit: **S**
(siemens), dimensionally `A·V⁻¹` in 2D. It is **not** a stress, a pressure, a yield strength, or an elastic
modulus; those have unit Pa and no owner named `σ_s` anywhere in this record (`SC-OWNER`).

---

## §2 The five quantities that may not be conflated

The roadmap §2.5 already forbids conflating four; `σ_s` adds a fifth distinction of the same kind.

| symbol | meaning | note |
|---|---|---|
| `Δz` | coordinate interval along the third dimension | a coordinate, not a length |
| `L_z^proper = ∫B(t,x,z)dz` | proper thickness | `dℓ_z = B dz` — **`B` is `g_zz^{1/2}`, and only `B`** |
| `2πR_z` | compact circumference | not a thickness |
| `L_z^film` | material thin-film thickness (the `L_z` in the thin-film Fresnel formula) | not a proper length |
| `σ_s` | surface conductivity | S |

**Symbol rule `SC-B`.** The third-dimension scale factor is `B`. The record writes `B²dz²` in all three of
its metric forms (§2.5, l.142, l.146). A submission that writes `C²dz²` and then calls `B` the scale factor is
internally inconsistent and is corrected here without further comment.

---

## §3 The reduction, and its measured domain

```
σ_s(ω) = ∫ dℓ_z  σ_3D,∥(ω, z)          [uniform field through the thickness]
       ≃  L_z^proper · σ_3D,∥(ω)        [homogeneous]
```

**Exactness (`REDUCE-DOMAIN`, `P17`).** With the 3D Drude form, `L_z·e²n_3Dτ/m* = e²n_2Dτ/m*` identically,
because `n_2D := n_3D L_z^proper`. Measured deviation `0.0e+00` at `L_z = 1e-9, 1e-8, 1e-7 m`. So the reduction
**derives** the 2D Drude ansatz that `R5-L2` previously asserted.

**Domain (`REDUCE-DOMAIN`).** The formula requires `σ_3D` — hence many atomic layers. The record's target is
`d_par = 6.7420 fm = 1.274e-4 a₀` (v3) with bound states ceasing below `L_z^ion = πa₀ = 1.66 Å`. The formula's
validity domain and the destination are disjoint. Any use of it at the endpoint must say so.

**Admissibility of the sheet limit** — the five conditions of the submission, evaluated:

| condition | status at the v3 baseline |
|---|---|
| field uniform through the thickness | not evaluable — `L_z^proper` is a definition with no registered value, only the `L_z = 1 fm` convention |
| local response (`q → 0`) | **holds** — `q_opt/k_F = 3.389e-8` (archived, `R5-L2`) |
| no surface/interface states | vacuous — at `d_par ≪ a₀` there is no surface in the usual sense |
| 3D electronic states retained | **FALSE** — `G0` row 1 is NO-GO; `N7` removes the carriers |
| geometry introduces extra EM coupling | not quantified anywhere in the record |

So the sheet description is **geometrically** admissible and **materially** inadmissible. That asymmetry is the
whole content of `G6`'s blockage.

---

## §4 Matter branch — declared, never presupposed

Every `σ_s` result must carry a branch label from roadmap §8.4, **assigned by computation, not by choice**:

| | |
|---|---|
| **A** | adiabatic following — the original electronic structure survives |
| **B** | non-adiabatic but bound / reorganizable — a new low-dimensional state forms |
| **C** | bound-state destabilization or structural destruction |
| **D** | model or the classical approximation fails — **cannot be determined** |

**`D` is a real outcome and the record's own evidence currently points at it** (`N7`: particle-number
conservation *invalid* at 73.4 MeV). Presupposing `A` is forbidden (roadmap §8.4, prohibition ③). A `σ_s`
without a branch label is `NO-VERDICT`, not a low score.

---

## §5 Acceptance criteria (LOCKED)

Any candidate `σ_s` must pass all nine. A miss is reported as a miss; values are never re-toleranced after
measurement.

| id | criterion | test | threshold |
|---|---|---|---|
| **S1** | units | `σ_s` carries SI `S`; every term of the response has the same dimension | exact |
| **S2** | energy budget | `R + T + A = 1` and `A = Z₀ Re(σ_s)|t|²` independently | `< 1e-12` |
| **S3** | passivity | `Re σ_s(ω) ≥ 0` for `ω > 0` in a passive equilibrium state | exact, all `ω` |
| **S4** | Kramers–Kronig | `Im σ(ω) = -(2ω/π) P∫₀^∞ Re σ(ω')/(ω'²-ω²) dω'` | `< 1e-6` relative, **across the whole reported band** |
| **S5** | f-sum **partition** | `W_intra + W_inter = πe²n_2D/(2m*)`, each `W = ∫Re σ dω` over its own support, **finite** | partition closes `< 1e-6`; no term may diverge |
| **S6** | charge conservation | Ward identity satisfied by the same `Π^R` used for `σ_s` | reported, not tolerated |
| **S7** | `τ` is **solved** | the response states what fixes the relaxation time; a scanned `τ` fails | binary |
| **S8** | branch declared | §4 label present and computed | binary |
| **S9** | no visibility conclusion | the product makes no transparent/opaque claim; label rule per §11.1/§11.2 | binary |

`S5` is stated as a **partition**, not an independent amplitude, because the record's Drude channel already
consumes the entire weight (see §6).

---

## §6 What the record's current module returns

Measured against `src/optics/sigma_s_lindhard.py` at `n_2D = 2.20e28 m⁻²`, `E_F = 73.37 MeV`,
`m*/m_e = 143.6`, `τ ∈ {1e-19, 1e-18, 1e-16} s`:

| id | result |
|---|---|
| **S1** | PASS |
| **S2** | PASS — `R+T+A=1` max dev `0.000e+00`; `A_def` vs `A_indep` `3.79e-16` |
| **S3** | PASS by construction — `Re σ = σ₀/(1+ω²τ²) + A`, both terms `≥ 0`; **never tested**, only true |
| **S4** | **FAIL above `2E_F`** — residual `1.153` at `1.5e8 eV`, `0.638` at `2e8 eV`; `≤ 1.2e-15` in the reported 1–3 eV band (`KK-UV`) |
| **S5** | **FAIL** — `W_Drude = W_total` exactly (`ratio 1.000000000003`), and the interband step has **unbounded** weight (`FSUM-SPLIT`) |
| **S6** | **NOT ATTEMPTED** — no `Π^R` is constructed; the Drude form is written directly |
| **S7** | **FAIL** — `τ` is an explicit scan (`TAU_SCAN`), labelled OPEN in the module header |
| **S8** | **ABSENT** — no §8.4 label |
| **S9** | PASS — "no visibility / mirror / transparency conclusion of any kind" is enforced on every row |

**Three failures and one omission, in a module that passes its own three tests.** That is the finding: `T1`–`T3`
test the arithmetic of `R,T,A`, not the legality of the response function.

### §6.1 The prescribed repair

Replace the interband term `A·θ(ω−ω_g)` with a **decaying lineshape** `A·φ(ω−ω_g)` normalised so that
`∫A φ dω` equals the interband share of the f-sum, and supply the `Im σ` partner of that lineshape. A constant
step is the one lineshape that cannot be causal — no choice of amplitude repairs it, because the residual
diverges as `ω → ω_g` (§6, `S4`). This repair is a **form** requirement and holds for every matter branch
`A/B/C/D`; it does not presuppose which one obtains.

---

## §7 Prohibitions

1. **No visibility conclusion** before `G6` — neither "transparent" nor "opaque" (roadmap §1.4, §11.1/§11.2).
2. **No `πα ≈ 2.3%` default.** Permitted only if all six premises of §6.4 hold; none does here.
3. **No graphene value.** `e²/(4ħ)` and the benchmark `e²/(16ħ)` are *amplitudes without a lineshape* and may
   not be asserted as the response.
4. **No bulk-plasmon extrapolation.** `q_opt c ≪ ω_p`: the plasmon is above the light cone and non-radiative.
5. **No backward selection.** `σ_s` may never be chosen to produce a desired appearance (`S9`, and the
   submission's own §VII.5).
6. **No promotion of `R5-L2` results.** Until `G4` and `G5′` pass, every product is
   "designated-background test optics".
7. **No reconstruction before `R1-B1`.** This spec's §5 can be *tested* on a hypothetical response; it cannot
   be *satisfied* by one at the endpoint until the matter state exists.

---

## §8 The `τ` obligation (`TAU-OBLIGATION`)

The record names the `G6`/`DC2` blocker as *"a compliant `σ_s(ω)` with a **solved** `τ`"*
(`docs/conventions/display_conventions_v1.md`; `docs/decisions/route_completion_v1.md`), and elsewhere:
*"`τ` remains an OPEN input — a `σ_s` at a scanned `τ` is parameterised, not solved."*

Therefore `S7` is not a formality. Any route that ends at `σ_s` without saying what fixes `τ` reproduces
`R5-L2` exactly, with a better derivation and the same missing number.

The Kubo route does determine `τ` in principle — `τ` is the imaginary part of the self-energy on the
Fermi surface, so `Π^R` at finite density contains it. **A compliant submission must say so explicitly**, and
must state which branch (§4) supplies the self-energy.

---

## §9 What this specification does not do

- It does not choose a matter branch.
- It does not fix `L_z^proper`, which the record has as a definition and not as a measured value.
- It does not produce `R`, `T`, `A`, or any observer-level quantity.
- It does not close `G6`, and cannot: `G6`'s precondition includes `G4` and `G5′`, neither of which is passed.
- It does not retro-fit a criterion to a known number. `S4`, `S5` and `S7` were written from the check they
  name, and then applied — in that order, with the results in §6 reported as found.

---

## §10 Amendment v1.1 — four criteria (`S10`–`S13`)

Added after the governor's acceptance of `PARTIALLY ADOPTED` and the measurement round `SC-2`
(`runs/OPTICS/sc2_results.txt`, 11/12 predictions, one kept miss). Each criterion is stated as a test with a
threshold, and each was applied to the record's module before being written down.

| id | criterion | test | threshold |
|---|---|---|---|
| **S10** | **`FSUM-SINGLE-SOURCE`** — one Hamiltonian, one current operator, one budget. The total spectral weight and every channel's share must derive from the same model, and that model's conventions `(g, v_F, m*)` must be stated. `W_j = f_j W_total`, `f_j ∈ (0,1)`, `Σf_j = 1`. | declare the tuple `(g, v_F, m*, W_total)`; show every channel as a fraction; any channel whose amplitude descends from a different model is inadmissible | binary; `\|Σf_j − 1\| < 1e-6` |
| **S11** | **`FSUM-FINITE`** — every channel's `Re σ` must decay faster than `ω^{-1}` at high frequency, equivalently it must possess a finite upper scale (a band edge, or an oscillator form). A step — sharp or broadened — has no such scale. | `W_j = ∫ Re σ_j dω` finite, computed with the decay included; report the upper scale `ω_end` that carries the share | every `W_j` finite; no channel may require an unbounded support |
| **S12a** | **`DRUDE-DOMAIN` (necessary)** — a single-Drude form is an *assertion* that the current correlator has one relaxation rate. It must be tested, not assumed. | `α = (4/π)arctan(−Im σ/Re σ)` at the peak of `−Im σ`, plus the maximum radial deviation from the single Debye arc | `α = 1` to `< 1e-2` **and** arc deviation `< 1e-2`; else the full `Π^R` (i.e. `S6`) is mandatory. **`α > 1` is an automatic fail** (impossible for one Drude pole) |
| **S12b** | **`DRUDE-DOMAIN` (sufficient)** — `α` at a point is not a certificate: an equal-weight two-pole sum at `τ₂/τ₁ = 3` attains `α = 1` exactly at `ωτ₁ = 0.697897`. The certificate is the **one-parameter collapse**. | `κ = max_ω \|α(ω) − (4/π)arctan(ω τ_eff)\|` over one decade either side of the peak, with `τ_eff` fitted | `κ < 1e-6` (single pole measures `4.4e-16`; two-pole 3:1 measures `8.6e-2`) |
| **S13** | **`TAU-PROVENANCE`** — `τ` must be **named** (single-particle / transport / optical), **traced** to a microscopic scattering mechanism or to the width of a pole in the response function, and **not scanned**. | state which `τ`; give the mechanism or the pole; a `τ` that appears only as a free parameter is a fail | binary |

**Why `S12` needs two statistics.** Measured on a pre-registered control (`C.2`/`C.2b`): an equal-weight
two-pole sum with `τ₂ = 3τ₁` gives `α_eff = 0.9087` — a 9% depression, which passes a naive `α ≠ 1` test if the
tolerance is loose — while its arc deviation is `13.4%`. `α` falls below `0.9` only for `τ₂/τ₁ ≳ 4`. The two
statistics have different sensitivities and both are required.

**Why `S13` needs "which `τ`".** For a static Thomas–Fermi 2D Coulomb kernel at the record's own
`q_TF/k_F = 0.0146`, `τ_tr/τ_sp = 91.5`. The number is model-dependent and is not a value of either `τ`; it is
the size of the ambiguity. A `τ` without a name is not a number.

**Subordination.** `S5` (partition closes) is **unstatable** until `S10` is met, because "the total" has no value
until the model tuple is fixed: at fixed `n_2D`, `W_total(g = 4)/W_total(g = 2) = √2` exactly. A candidate that
reports `S5` without `S10` is reporting a partition of an undefined budget. Likewise `S7` is subsumed by `S13`:
`solved` now means *named, traced, and not scanned*.

**The bound `S11` puts on `R1-B1`.** For the record's amplitude `A_INTER = e²/(16ħ)`, a step consuming the whole
budget would have to terminate at `ω_end = ω_g + W_total/A = 440.18 MeV`. So `R1-B1` must deliver an interband
band edge below that, together with `(n_2D, g, v_F, m*)`. Before v1.1 the optics stage had no such interface;
it now has four named inputs.

> **CORRECTED in v1.2 — see §10a.4.** `440.18 MeV` is not a bound a material could meet: it is the
> `f_inter = 1` endpoint of a one-parameter family, and it is *identically* `3ω_g` under this module's own
> conventions (`2.999717`, the `2.8e-4` being the `73.37/73.3648` rounding). It is forbidden as an input.
> The paragraph above is left standing as written, because it is what v1.1 said.

---

## §10a Amendment v1.2 — two closures and one correction (`S14`, `S15`)

Added after the governor's mathematical review of `SC-2` and the measurement round `SC-3`
(`runs/OPTICS/sc3_results.txt`, 14/17 predictions, three kept misses). Each criterion was applied to the
record's module before being written down.

| id | criterion | test | threshold |
|---|---|---|---|
| **S14** | **`BUDGET-DECLARED`** — a partition is a statement about fractions of one budget, so the budget must be declared, in one unit convention, before any share is quoted. | declare `W_total` **with its `ω` convention** (`∫ σ₁ dω` over `rad/s` or over `eV`, and say which); declare `f_intra`, `f_inter` with `f_intra + f_inter = 1`; quote any band edge as `ω_end = ω_g + f_inter W_total/A`, never as a bare number | `\|f_intra + f_inter − 1\| < 1e-9`; the unit convention stated in words; a bare `ω_end` is a fail |
| **S15** | **`G-CONSISTENT`** — one degeneracy, in four places. `g` must appear in `k_F`, `E_F`, `W_total` **and** the interband height with the same value, and `v_F` must reproduce `E_F = ħk_F v_F`. | exhibit the tuple `(g, v_F, k_F, E_F, m*, W_total, A_inter)` and show each is the same `g`; state `A_inter(g) = (g/4)σ_min × (selection rules)` | all four `g` identical; `v_F` from `E_F/(ħk_F)` within `1e-3` of the declared `v_F`, or one of the pair is wrong |

**§10a.1 Why `S14` has a unit clause.** `W_total/A_INTER` is in `rad/s`; converted once it is `293.4384 MeV`.
The same numeral read as `eV` is `1.519267e15` too large — that is exactly `1/ħ`, to `1e-12`. A spec that
does not fix the convention cannot distinguish a `10^15` error from a `10^-3` one.

**§10a.2 Why `S14` needs `f_inter` in the bound.** `S5` gives `ω_end(f_inter) = ω_g + f_inter W_total/A`, a
one-parameter family: `146.7400 MeV` at `f_inter = 0`, `293.4592` at `0.5`, `440.1784` at `1`. A bare
`440.18` is the `f_inter = 1` endpoint — the case in which the Drude pole receives **nothing**. Under the
record's own measured partition (`W_intra/W_total = 1.000000000003`, `runs/OPTICS/sc_route_results.txt` §F;
the Drude pole takes the whole budget, `τ` cancels) the residual is `−3e-12`, i.e. zero to the quadrature
floor: the admissible edge is `ω_g` itself, and the module's step term is inadmissible at every
`ω_end > ω_g`. **[Corrected in v1.3 — the v1.2 sentence quoted the partition as `1 − 7.1e-5`, which is the
`m*`/`E_F` double-pinning slack of `sc2` §A.2, not a partition share; errata `E5`.]**

**§10a.3 Why `S15` is not bookkeeping.** `A_INTER = e²/(16ħ)` is the **single-cone, spinless** height, i.e.
`g = 1`; the module's `k_F = √(2πn)` is `g = 2`. The interband height is therefore low by exactly
`2.000000000000`. The `1/4` that v1.1 called "underived" is `g/4` at `g = 1` — underived because
inconsistent. And the record's `(n_2D, E_F)` pair implies `v_F = 1.000071 c`: a Dirac model at the speed of
light, never declared.

**§10a.4 Correction to a v1.1 sentence.** v1.1 said a step consuming the whole budget "would have to
terminate at `ω_end = ω_g + W_total/A = 440.18 MeV`, so `R1-B1` must deliver an interband band edge below
that". The arithmetic is right and the conclusion is wrong twice over:

1. `440.18 MeV` is **not a bound that a material could meet**; it is the `f_inter = 1` endpoint, and any
   `f_inter < 1` gives a lower edge (§10a.2).
2. Worse, it is an **identity**: with `k_F² = 2πn`, `m* = E_F/c²`, `ω_g = 2E_F/ħ`,
   `(W/A)/(2ω_g) = 2πn/k_F² = 1`, so `ω_end(f_inter = 1) = 3ω_g` exactly (measured `2.999717`; the
   `2.8e-4` is the `73.37 / 73.3648` MeV rounding). The number is `3 × 146.74` and contains no information
   about `n_2D`, `g`, or `v_F`.

**Consequence for `R1-B1`: `440 MeV` is forbidden as an input.** `ω_end` must come from band structure, and
the ceiling scales exactly with `v_F` (measured to `3.33e-16` over four decades): at a graphene-like
`v_F = c/300` it is `1.4673 MeV`, not `440.18`.

**§10a.5 `S4` and `S5` are independent — with witnesses.** `S4` (causality) and `S5` (weight) are separate
verdicts and neither implies the other. Four responses populate all four cells:

| response | `S4` | `S5` | why |
|---|---|---|---|
| pure step `Aθ(ω−ω_g)` | pass | FAIL | exact Hilbert partner; weight `4.50×` budget at `10ω_g` |
| truncated step, untruncated partner | FAIL | pass | `f_inter = 0.9992` fits; residual `0.6194` |
| the record's module as-is | FAIL | FAIL | Drude partner, no upper scale |
| finite-weight oscillator | pass | pass | `W = S_pπ/2`; `K-K` residual `2.3e-7` |

Repairing one symptom therefore repairs nothing else: a band edge bounds the weight but does **not** adjust
`Im`; the causal partner must be recomputed, not inherited.

---

## §11 Null results are results (`NO-GO-ADMISSIBLE`)

> `G6` passing is not the objective. The objective is an optical response with no free parameter that satisfies
> `S1`–`S13`. If the computation shows that **no admissible stable matter state exists**, or that **no response
> function satisfies `S1`–`S13`**, that is a valid physical conclusion and not a project failure — the same class
> of conclusion as `G0` row 1's `NO-GO`.

1. An admissible null result is reported in the same format as a positive one: branch label `D` (§4), the
   measured failure, and no apology.
2. A null optical result does **not** license a dimensional claim, and a dimensional impossibility does not
   license a null optical claim. The two failures are independent and each must be established on its own.
3. The prohibition on backward selection (§7.5) has a companion: **no forward selection** — the matter branch may
   not be chosen because it makes the optics come out admissible.
4. **Acceptance is not identification.** Passing `S1`–`S15` does not pick out a material. Measured: a `6×5`
   grid of `(ω_0, Γ)` at one fixed `S_p` passes both `S4` and `S5`, **30/30**, because `S5` is closed-form in
   `S_p` and blind to both parameters. And a response with identical `(n_2D, g, v_F)` can carry any split
   `f_intra` while `σ₁(ω→0)` changes by the same factor — so the four-tuple plus the criteria still leave one
   free parameter (`f_intra`) that only the matter model or a measurement can fix.

---

*Content generated by AI*

