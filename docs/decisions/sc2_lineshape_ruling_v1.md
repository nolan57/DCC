# Ruling — `SC-2`: the acceptance holds, and the three sharpenings cost more than they look

**Submission**: governor message of 2026-11-22 21:01 (+08) — acceptance of `PARTIALLY ADOPTED`, with four
sharpenings and one decision. Archived verbatim at `runs/OPTICS/sc2_submission_verbatim.md`.
**Registration**: `runs/OPTICS/sc2_registration.md` (`P1`–`P12`, locked before measurement; `P11` amended before
the run, with the amendment visible).
**Product**: `runs/OPTICS/sc2_results.txt` (226 lines). **11 / 12 predictions hold; one misses and stays missed.**

**Verdict: `ADOPTED`.** The spec is amended to v1.1 (`S1`–`S9` untouched, `S10`–`S13` added). No second
specification is created. `G6`/`DC2` remain blocked, and the block is now stated as an **entry condition**, not as
a gap.

| | |
|---|---|
| **Accepted from the governor** | the correction of problem statement (§1); `FSUM-SINGLE-SOURCE` (§2); `KK` repair by line shape, not amplitude (§3); `DRUDE-DOMAIN` + no `τ` scan + `τ` provenance (§4); the pause (§5); `NO-GO-ADMISSIBLE` (§6) |
| **Sharpened by measurement** | the budget is a function of `(g, v_F)` and the record fixes `g = 2` silently; a broadened step does **not** bound the weight; `τ_tr/τ_sp = 91.5` at the record's own screening |
| **Registered as an error of mine** | `P1` failed twice, both times in my instrument; `P10` missed by 0.0087; the miss is kept |

---

## 0. Headline

> The governor's four points are not four opinions. Three of them are constraints that the record's module
> violates **measurably**, and one of them — the `τ` clause — turns a phrase ("a solved `τ`") into a test that
> can be run on any future candidate. The consequence is that `S5`, the f-sum partition, is not merely
> unsatisfied: **it is unstatable** until a single Hamiltonian fixes the degeneracy, and `S4` is not repairable
> by any choice of amplitude or broadening.

The problem statement the governor wrote is the right one, and I adopt its wording:

```
how to obtain a sigma_s(omega) that is microscopically grounded,
has a solved relaxation time, and has a legal spectral partition
```

with the three requirements conjunctive. Nothing in this round produces such a `σ_s`, and nothing here moves
`G6` closer to passing except by making the entry condition precise.

---

## 1. The error attribution: accepted, and diagnosed

The governor's acknowledgement is exact: treating a "yield-strength misreading" as the thing to correct was a
**wrong problem attribution**, and `REPAIR-ABSENT` is the right designation. I record the *class* rather than the
instance: this was the second occurrence in two rounds of the defect registered in round 31 as `MR2-D` — *a
correction that repairs the previous submission's premise rather than the record's state*. The first was the
truncated-Morse potential, which corrected a `σ_s` reading nobody held; the second was the yield strength. The
pattern is not carelessness about physics; it is that a correction is cheapest to write against one's own last
paragraph, and that paragraph is not the record.

The operational consequence, now a standing scope rule: a correction is admissible only if the proposition it
retracts can be **cited by file and line** in `docs/specs/`, `docs/conventions/` or the roadmap. `REPAIR-ABSENT`
is the label for a correction that fails that test, and it is not a criticism of the physics.

---

## 2. `FSUM-SPLIT` becomes a provenance requirement (measured: `P1`–`P4`)

The governor's addition — *the total weight must come from the actually chosen Hamiltonian and its current
operator; f-sum formulas from different models may not be spliced* — is stronger than the defect I reported, and
the measurement shows why.

**2.1 The pole saturates the budget by definition.** `∫₀^∞ σ₀/(1+ω²τ²)dω = σ₀π/(2τ) = πe²n/(2m*)`, with `τ`
cancelling. Measured to `6.9e-15` at all three scanned `τ`. So `W_Drude = W_total` is not an arithmetic slip in
the module; it is what a Drude pole *is*. **The repair cannot be an amplitude**: any interband term added on top
is a second draw on a budget already spent.

**2.2 The budget is a function of the degeneracy, and the record fixes it silently.** With `n = gk_F²/(4π)`,
`E_F = ħk_Fv_F`, `m* = p_F/v_F`:

```
W_total(g) = (e^2 v_F / 8 ħ) √(4πng)          E_F(g) = ħ v_F √(4πn/g)
```

At fixed `n_2D`: `W(4)/W(2) = 1.414213562373` and `E_F(4)/E_F(2) = 0.707106781187` — exact. The module's
`k_F = √(2πn)` **is** the `g = 2` choice (`g = 2 ⇔ k_F² = 2πn`), and nothing in the module or the spec says so. A
budget that moves by `√2` under a convention the record never declared is not a budget; it is a placeholder.

**2.3 The interband amplitude cannot carry a fraction.** `A_INTER = e²/(16ħ) = 1.521334e-5 S` equals `σ_min/4`
with `σ_min = e²/(4ħ) = 6.085337e-5 S`, the 2D Dirac universal value — ratio `0.2500000000000000`. The `1/4` is
underived anywhere in the record. And the object has dimension **S**: a *height*, not a *fraction*. `S5` asks for
`W_intra + W_inter = W_total`, which is a statement about fractions of one budget. A height cannot satisfy it.

**2.4 The consequence is a derived band edge.** If a step is kept, `W_inter = A(Ω − ω_g)`, so the termination at
which it would consume the *whole* budget is

```
Ω* = ω_g + W_total/A_INTER = 440.18 MeV = 4.4018e8 eV
```

Any step model that closes `S5` must therefore be cut off **below 440 MeV**, and where the cut-off is cannot be
supplied by `A`. It is the band structure. This is the first quantitative statement in the record of *what*
`R1-B1` has to deliver for the optics stage: not merely a density, but an interband band edge and a degeneracy.

**Registered**: `FSUM-SINGLE-SOURCE` (the one-Hamiltonian requirement), `FSUM-FRACTION` (the legal parameter is
`f_j ∈ (0,1)` with `Σf_j = 1`, not a height in S). `S5` is subordinate to `S10`.

---

## 3. `KK-UV` becomes a line-shape requirement, and the two defects share a root (measured: `P5`–`P8`)

**3.1 The partner is exact.** For `Re σ = Aθ(ω−ω_g)`, `Im σ = −(A/π)ln|(ω_g+ω)/(ω_g−ω)|`, with the sign
convention of `S4` confirmed. Round 36's residual reproduces: **1.1530** at `1.5e8 eV`, `0.6384` at `2e8`, and
`1.0e-15`-level inside the reported 1–3 eV band. The ratio is `A`-independent — `A` cancels — so **no choice of
amplitude repairs it**, exactly as the governor says.

**3.2 Broadening is not the cure, and this is measurable.** For `Re σ = A[½ + arctan((ω−ω_g)/Γ)/π]`, the weight
to `Ω` is

```
F(Ω) − F(0),   F(ω) = A[ ω/2 + (Γ/π)( z·atan z − ½ ln(1+z²) ) ],   z = (ω−ω_g)/Γ
```

and `Re σ → A` as `ω → ∞` for **every** finite `Γ`, so the weight diverges linearly:

| `Γ/ω_g` | `W(10ω_g)/W_total` | `W(100ω_g)/W_total` | growth |
|---|---|---|---|
| `1e-3` | `4.500` | `49.51` | `11.0×` |
| `1e-2` | `4.497` | `49.50` | `11.0×` |
| `1e-1` | `4.466` | `49.43` | `11.1×` |

Even at `Γ/ω_g = 10⁻³` the broadened step has already spent **4.5× the entire spectral weight** by `10ω_g`. So
broadening regularises the log (it helps `S4` locally) and leaves `S5` exactly as broken as before. The
governor's instinct — "must modify the line shape, not the amplitude" — is right, and broadening alone is the
wrong line-shape change.

**3.3 What does close both.** A Lorentz oscillator, `σ = S_p(−iω)/((ω₀²−ω²)−iγω)`, has `W = S_pπ/2` **finite**
(measured `2.034685e18` vs analytic, `2.2e-16`) and a causal partner by construction (K-K round trip `9.2e-8`
over `0.5`–`5ω₀`). Band-limiting is therefore the single repair that closes `S4` **and** `S5`; amplitude and
broadening close neither.

**3.4 And here the two defects rejoin.** With `S_p` fixed by `f_inter`, the interband term stops being an input
and becomes a **strength fraction** of the same `πe²n/(2m*)`:

```
Σ_j f_j = 1,   f_j = n_j/n
```

which is precisely `FSUM-SINGLE-SOURCE`. The governor calls `FSUM-SPLIT` and `KK-UV` two defects of different
nature; I agree they are two *symptoms* with two separate repairs at the level of `S4` and `S5`, but they have
**one root**: the module has no upper energy scale. `FSUM-SPLIT` is what the missing scale does to the budget;
`KK-UV` is what it does to causality. Registering the root matters because it forbids the cheap fix: a
broadening parameter would look like it addresses causality while leaving the budget untouched.

**Registered**: `KK-LINESHAPE`, `FSUM-FINITE` (every channel needs `Re σ → 0` faster than `ω^{-1}`, equivalently
a finite band edge or oscillator form), `STEP-NO-SCALE` (the shared root).

---

## 4. `TAU-OBLIGATION` becomes an instrument (measured: `P9`–`P12`)

The governor's clause is the most valuable thing in the acceptance, and it is testable. Three parts:

**4.1 "Prove the reduction, or compute the full response."** A `σ_s` written as one Drude pole asserts that the
current correlator has a single relaxation rate. That assertion has a measurement: at the frequency of peak
`−Im σ`, a Cole-Cole response satisfies

```
α = (4/π) arctan( −Im σ / Re σ ),      peak of −Im σ at ωτ = 1 for every α
```

recovered to `1.1e-16` for `α ∈ {1.0, 0.9, 0.7, 0.5}`. `α = 1` is a single pole; `α < 1` is a depressed arc,
which is what a *distribution* of rates produces — the governor's "multiple relaxation modes / non-exponential
decay" made quantitative. So `DRUDE-DOMAIN` is decidable, and `α` must be reported with the response.

**4.2 The instrument has a sensitivity floor, and I got it wrong.** `P10` predicted `α_eff < 0.9` for an
equal-weight two-pole sum with `τ₂ = 3τ₁`. Measured: **`α_eff = 0.9087`**, a miss by `0.0087`. The arc deviation
(13.4%) does fire. A pre-registered calibration then gives the crossing:

| `τ₂/τ₁` | 1.0 | 1.5 | 2.0 | 3.0 | 5.0 | 10 | 30 |
|---|---|---|---|---|---|---|---|
| `α_eff` | 1.000 | 0.987 | 0.963 | 0.909 | 0.816 | 0.539 | 0.446 |
| arc deviation | `3e-16` | `2.0e-2` | `5.7e-2` | `1.3e-1` | `2.5e-1` | `4.3e-1` | `6.5e-1` |

`α` alone under-detects mild multi-mode response; the radial deviation is the strong statistic. The criterion must
carry **both**, and `P10` stays failed rather than being re-toleranced.

**4.3 "`τ` must trace to a mechanism or a pole width."** It must also be *named*, because `τ` is not one number.
Transport and single-particle rates differ by the angular weight `(1−cos θ)`:

```
τ_tr/τ_sp = ∫|V|²dθ / ∫(1−cos θ)|V|²dθ ,   |V(q)|² ∝ (q+q_TF)⁻²
```

with `q_TF/k_F = 0.014596` from the record's own `n_2D`, `m*`, `g = 2` — measured **`τ_tr/τ_sp = 91.5`**, and the
asymptotic law `(2/π)(1/a)` holds to `1.0e-2` at `a = 10⁻⁴`. The model is static Thomas–Fermi with no dynamic
screening and no vertex correction, so `91.5` is not a value of either `τ`; it is the **size of the ambiguity**.
A submission that says "`τ = 10⁻¹⁶ s`" without naming which `τ` has not said anything — and the locked spec never
asked (count of `transport` in `surface_conductivity_v1.md` = **0** — counted against **v1.0**, digest
`91eca7ac…`, at the moment of the run; §10 of v1.1 puts the word in, and the current file counts `1`. The
number is a timestamp, not a claim about the amended text.)

**4.4 No scan.** `TAU_SCAN` in the module is an explicit scan and its own header labels it OPEN. Under the new
criterion it is not a weak input, it is a **FAIL**, and the scan may survive only as a labelled probe of the
*functional form* (`T2`, `T3`), never as the response.

**Registered**: `DRUDE-DOMAIN` (`S12`), `TAU-KIND` / `TAU-PROVENANCE` (`S13`), `NO-TAU-SCAN` (`S13`, binary).

---

## 5. The decision: pause, and amend in place

The governor's decision is adopted without amendment:

- **Keep** `docs/specs/surface_conductivity_v1.md`. No second specification.
- **Amend it in place** to v1.1, additively: `S1`–`S9` text unchanged and still locked by the v1.0 digest; the
  four new criteria enter as `S10`–`S13` with their own digest. A criterion that supersedes nothing cannot
  silently weaken what it was added to.
- **Do not** disguise conformance as reconstruction; **do not** bypass `N7`; **do not** scan `τ`; **do not**
  presuppose transparent or opaque. These four were already prohibitions §7.1, §7.7 and §7.5; they are now also
  the four ways a future submission can fail on page one.

The gate chain is unchanged and is now written with its entry condition explicit:

```
R1-B1  matter state + beta-equilibrium EOS   <-- THE ENTRY POINT, nothing starts before it
  |    must deliver: n_2D, g, v_F, m*, and the interband band edge w_end
  v
microscopic scattering -> full current response (or a PROVED single-pole reduction)
  |    must deliver: which tau, its mechanism, and alpha
  v
spectral partition + Kramers-Kronig   (S10, S11, S12, S13)
  |
  v
a self-consistent sigma_s(omega) at the endpoint   <-- S1-S9 become testable on a real object
  |
  v
G6 / DC2
```

**`R1-B1` is now specifiable from the optics side.** Before this round it only had to produce an EOS. It now has
four concrete outputs the optics stage cannot proceed without: `n_2D`, `g`, `v_F`/`m*`, and `ω_end`. §2.4 gives
the last one a hard bound (`ω_end < 440 MeV`), and §2.2 gives the degeneracy a measurable consequence
(`√2` in the budget). That is the useful residue of this round: `R1-B1` has an interface.

---

## 6. `NO-GO-ADMISSIBLE`

Adopted as a decision principle, and it is the one that protects the project from itself:

> `G6` passing is not the objective. The objective is an optical response with no free parameter that satisfies
> all the physical constraints. If the computation shows that **no admissible stable matter state exists**, or
> that **no response function satisfies `S1`–`S13`**, that is a valid physical conclusion and not a project
> failure. It is the *same kind* of conclusion as `G0` row 1's `NO-GO`, which the record already accepts.

Three consequences, all binding:

1. An admissible null result is **reported in the same format as a positive one** — with the branch label `D`,
   the measured failure, and no apology.
2. `MAP-TRILEMMA` and the injection/render gap are unchanged: a null optical result does not license a
   dimensional claim, and a dimensional impossibility does not license a null optical claim. The two failures
   are independent and each must be established on its own.
3. The prohibition on backward selection (`S9`, §7.5) now has a companion: **no forward selection either** — the
   matter branch may not be chosen because it makes the optics come out admissible. §8.4's rule that the branch
   is *computed* covers this; `NO-GO-ADMISSIBLE` states the cost of obeying it.

---

## 7. Errors in this round

Recorded because they are the reason to trust the rest.

| where | what | disposition |
|---|---|---|
| `P1`, run 1 | `rel dev 2.14e+00` — a spurious `π` in the quadrature prefactor | archived as `sc2_results_v1_SUPERSEDED_PREFACTOR.txt`; the `2.14` is `π − 1`, which is how it was diagnosed |
| `P1`, run 2 | `rel dev 3.18e-07` — `trapezoid` over a midpoint grid drops half a cell at each end | archived as `sc2_results_v2_SUPERSEDED_ENDPOINT.txt`; replaced by the midpoint rule |
| `P1`, conclusion | the check compares `πe²n/(2m*)` with `σ₀π/(2τ)`, which are the *same expression* | stated in the product: `P1` measures only the quadrature. Its content is algebraic, and the product says so |
| `P10` | `α_eff = 0.9087 > 0.9`, a miss by `0.0087` | kept as FAILED; the calibration `C.2b` was added to measure the instrument, and is labelled as not re-testing `P10` |
| `P11` | pre-registered as ">100", which was an unevaluated estimate with the wrong constant (`1` instead of `2/π`) | amended **before** the run, with the amendment printed in the registration |
| figure/table | `B.4`'s first rendering truncated three cells | fixed; the truncation is invisible in the archived run and is noted here rather than silently |
| time ordering | `P12` counted `transport` in the spec **before** v1.1 added it (count `0` then, `1` now) | stated in §4.3; the results file is left as produced, because at run time it was true |

`P1` deserves the note it gets in the product. A prediction whose two sides are algebraically identical can only
ever measure the instrument, and it failed twice while doing exactly that. It is kept, with the audit trail
inline, because deleting it would remove the only evidence that the quadrature was ever checked.

---

## 8. What this ruling does not do

- It does not produce `σ_s`, `R`, `T`, `A`, or any observer-level quantity. No visibility conclusion.
- It does not choose a matter branch, a degeneracy, or a band edge.
- It does not close `G6`, and does not move any gate except by sharpening `R1-B1`'s deliverable list.
- It does not create a second specification: v1.1 is an addition to v1.0, and `S1`–`S9` are byte-identical.

*Content generated by AI*

---

## Erratum — appended round 38, not edited in place

The governor's review of this ruling accepted §1–§3 and questioned §2.4's number. The review was right, and
measurement (`runs/OPTICS/sc3_results.txt`, `Q1`, `Q2`, `Q15`) settles it.

**What §2.4 said.** "`Ω* = ω_g + W_total/A_INTER = 440.18 MeV`; any step model that closes `S5` must be cut off
below 440 MeV."

**What is true.**

1. The formula is the `f_inter = 1` endpoint of `ω_end(f_inter) = ω_g + f_inter W_total/A`, with
   `f_inter = W_inter/W_total` and `f_intra + f_inter = 1`. Measured: `146.7400 MeV` at `f_inter = 0`,
   `293.4592` at `0.5`, `440.1784` at `1`. "Below 440" is therefore true and almost empty: the tight bound is
   `ω_g + f_inter W_total/A`, and `f_inter` was never declared.
2. Under this module's own partition (`FSUM-SPLIT`, `W_intra/W_total = 1 − 7.1e-5`) the residual interband
   budget is **exactly zero**, so the admissible edge is `ω_g` — the module's step term is inadmissible at
   every `ω_end > ω_g`.
3. The number is an **identity**: with `k_F² = 2πn`, `m* = E_F/c²`, `ω_g = 2E_F/ħ`,
   `(W/A)/(2ω_g) = 2πn/k_F² = 1`, hence `ω_end(f_inter = 1) = 3ω_g` exactly. Measured `2.999717`; the `2.8e-4`
   is the `73.37 / 73.3648` MeV rounding. So `440.18 MeV` contains **no information** about `n_2D`, `g`, or
   `v_F`. §2.4's sentence *"the first quantitative statement in the record of what `R1-B1` has to deliver"* is
   withdrawn: `3 × (threshold)` is not a requirement on a material.
4. The unit clause matters: `W/A` is in `rad/s`; read as `eV` the same numeral is `1/ħ = 1.5193e15` too large,
   measured to `1e-12`.

**Not withdrawn.** §2.1–§2.3 stand: the Drude pole saturates the budget by definition; `W ∝ √(ng)` so `g = 2`
is implied by `k_F = √(2πn)`; and the interband amplitude's dimension is `S`, not a fraction. §2.3's claim
that the `1/4` is "underived" is **sharpened, not retracted**: it is `g/4` at `g = 1`, while the same module's
`k_F` is `g = 2` (factor `2.000000000000`). The amplitude is underived because it is inconsistent.

**Consequence carried into v1.2.** `440 MeV` is forbidden as an input to `R1-B1`; `ω_end` must come from band
structure, and `f_intra` must come from the matter model, because the optics criteria are measured to be blind
to it (`S14`, `S15`, `§10a.2`, `§10a.4`).

*Content generated by AI*

---

## Errata `E5` (SC-4, round 39) — item 2's partition citation

Item 2 above quotes the module's partition as "`FSUM-SPLIT`, `W_intra/W_total = 1 − 7.1e-5`". That is a
**mis-citation**: FSUM-SPLIT measured `W_intra/W_total = 1.000000000003` (`runs/OPTICS/sc_route_results.txt`
§F, P15), and `7.1e-5` is the **`m*`/`E_F` double-pinning slack** (`sc2_results.txt` §A.2), not a partition
share. The residual interband budget is zero **identically** (`sc2` §A.1, P1), so item 2's conclusion — no
interband term admissible at any `ω_end > ω_g`; admissible edge `ω_g` — stands unchanged, while the quoted
figure and the `1e-15` precision printed in `sc3_results.txt` are retracted (`sc3_budget_check.py:87-89`
hardcoded `f_intra_mod = 1.0`). Register: `docs/decisions/sc4_partition_citation_errata_v1.md`.
