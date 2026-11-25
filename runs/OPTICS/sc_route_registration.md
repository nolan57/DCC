# Registration — `SC-ROUTE` submission (surface conductivity), 2026-11-22

**Rule.** Predictions below are fixed before any measurement in this round. Each is a statement about the
**record**, checkable by reading or computing. A prediction that fails is reported as failed and stays in the
results file; nothing is re-worded after seeing a number. Tolerances are derived from the quantity, never rounded.

**Scope rule in force (round 31).** A check about *what the record says* is scoped to `docs/specs/` +
`docs/conventions/` + the governing roadmap — the **speaker**. `docs/decisions/` is commentary and is excluded,
because my own rulings quote rejected phrases while rejecting them.

**The question.** The submission's central claim is that `σ_s` has been misread in this project as a *yield
strength* (Pa), and that it is really a frequency-dependent **surface conductivity** (S). Its §VII.1 states the
yield-strength reading "does not stand and should be retracted" (does not hold, must be withdrawn). Before anything else: **was that ever
this record's reading?** If not, the correction is right in itself and repairs a document that does not exist.

---

## Section 1 — Does the misconception exist in the record?

| id | prediction | falsified by |
|----|-----------|--------------|
| **P1** | In the speaker scope, `σ_s` is identified with yield strength / plasticity / elasticity **0 times**. The submission's §I targets a reading that this record never held. | any hit pairing `σ_s` with Pa, yield, plastic, Poisson, Young's modulus |
| **P2** | The record's sole owner of `σ_s` is the frequency-dependent surface conductivity, SI unit S, declared **an input, not a constant** (§6.4, `S10`). | an owner with different units, or a constant-valued `σ_s` |

## Section 2 — Does the record already contain the submission's machinery?

| id | prediction | falsified by |
|----|-----------|--------------|
| **P3** | The submission's metric `ds²=-N²dt²+A²dx²+B²dy²+C²dz²` is **not** the record's, and is **internally inconsistent**: its own §III.3 writes `dl_z = C dz` while its symbol table calls `B` "the third-dimension scale factor". The record writes `dℓ_z = B dz`. | the record's line 162 reading `dℓ_z = C dz` |
| **P4** | Task D's `r`, `t`, `R`, `T`, `A` formulas appear **verbatim** in the roadmap §6.4. | any of the five absent |
| **P5** | Task D is already implemented (`rta()`), and `R+T+A=1` is already tested (`T1`). | no implementation, or no conservation test |
| **P6** | Task C's "compare finite film vs effective sheet" is already mandated by the same §6.4 (thin-film formula). | absent |
| **P7** | The proper-vs-coordinate disambiguation is **already mandatory**, listing **four** quantities (coordinate interval, proper thickness, compact circumference, film thickness) — the submission proposes **two**. | absent, or fewer than four |
| **P8** | Task A (fix the carrier population first) is **already a gate condition** (`N7`, inside `G5′`). The submission calls it "the easiest to miss" (most easily overlooked). | `N7` absent from the `G5′` gate |
| **P9** | §VI's "do not presuppose which branch" is **already mandated** (§8.4), with **four** categories `A/B/C/D`; the submission's three-way split is weaker, and its pre-classification was deleted for exactly this reason. | §8.4 absent, or has fewer than four categories |
| **P10** | The submission's `μ_e ≈ 23.2 MeV` is a **revoked** baseline. The current value is `73.37 MeV`. | 23.20 still current in `src/optics/` |
| **P11** | `G6`'s precondition is quoted correctly (G4, G5′ + self-consistent `σ_s(ω)`). | different precondition |
| **P12** | "both transparent and opaque forbidden" is quoted correctly. | only one direction forbidden |

## Section 3 — Is the gap the submission names actually a gap?

| id | prediction | falsified by |
|----|-----------|--------------|
| **P13** | Of the seven checks in Task C, **Ward, Kramers–Kronig and the f-sum rule are absent** from the record's only optics module. The gap is real. | any of the three present |

## Section 4 — Applied to the record, do the submission's own checks bite?

These are the round's decisive measurements. `Re σ` and `Im σ` are taken from the registered module's own function
`sigma_s(hbarw_ev, tau)`, at the registered `τ` scan, `n_2D = 2.20e28 m⁻²`, `E_F = 73.37 MeV`, `m*/m_e = 143.6`.

| id | prediction | falsified by |
|----|-----------|--------------|
| **P14** | **Kramers–Kronig is violated, but only above the interband threshold** `ħω = 2E_F = 146.74 MeV`. In the band the module reports (1–3 eV, i.e. `5.1e-8` of threshold) the model is Drude-only and K-K holds to `<1e-12` relative. So the defect is real and **confined to a band that carries no optical claim**. | violation ≥1e-6 in-band, or no violation above threshold |
| **P15** | **The Drude term alone saturates the f-sum rule**: `∫₀^∞ Re σ_D dω = πe²n_2D/(2m*)` to `<1e-12` relative. Therefore the added interband constant **double-counts spectral weight**, and its integral **diverges** (`∫Re σ dω = ∞`). The interband amplitude is not an "open input" — the total weight is already fully allocated. | Drude integral ≠ f-sum, or the interband weight converges |
| **P16** | The submission's validity condition (d) — "the 3D material still holds its original electronic states" — is **false at the record's own target**, by the record's own verdict: `d∥ = 15.40 fm = 2.91e-4 a₀`. So the reduction formula's domain excludes the regime it is wanted for. | `d∥/a₀ ≥ 1`, or the record's row 1 not a NO-GO |
| **P17** | **The reduction is exact and it derives the record's ansatz**: with `σ_3D,∥` the 3D Drude form, `σ_s = L_z^proper σ_3D,∥` equals `e²n_2Dτ/m*` identically, because `n_2D := n_3D L_z^proper`. So the submission converts `R5-L2`'s asserted form into a derived one — a real credit, in the regime where `σ_3D` exists. | deviation > 1e-12 |

---

## What a verdict can and cannot say

- It **can** say whether the misconception exists, whether the machinery is already built, and whether the three
  missing checks bite.
- It **cannot** produce a number for `σ_s` at the DCC endpoint, because that needs `R1-B1`, which the record
  already gates at `G5′`. The submission says the same thing (`Task A` first). Any round claiming to *close* `G6`
  from here would be computing a property of a material state that has not been established.
- It **cannot** choose among cases A/B/C. `§8.4` forbids presupposing the branch, and this round will not.

## Registered before measurement

`runs/OPTICS/sc_route_registration.md`, 2026-11-22. Executor: `src/optics/sc_route_check.py`.
Output: `runs/OPTICS/sc_route_results.txt`.
