ADIABATICITY PROVENANCE AND FUNCTIONAL ANALYSIS
===============================================

Date: 2026-11-24T03:56:00Z
Directive: G-73-01, Task 1 (round 73)
Registration: runs/G-73-01/g73_01_registration.md
Instrument: src/g73/verify_g73_numbers.py — runs/G-73-01/g73_01_verification.txt
PROVENANCE: NEITHER. This document re-reads archived text and archived constants. It derives no
new physics, and it does not attempt to prove or disprove adiabaticity (G-73-01 §Prohibitions).
Result class: PROVENANCE AND FUNCTIONAL MAP. No survival, visibility, feasibility, route, gate,
threshold, price, terminal-class or RQ claim.

The directive's causal chain was given as

    Smooth 2D-ization  ->  requires  ->  Adiabaticity  ->  depends on  ->  [ ? ]

The trace below finds that each of the three links is a different object from the one the arrow
names, that the record has held three different statuses for the premise, and that the third link's
placeholder is occupied in one place and empty in another. No link is repaired here.

------------------------------------------------------------------------------
1  SUBTASK 1.1 — THE POINT OF INTRODUCTION
------------------------------------------------------------------------------

**Finding:** Adiabaticity was not introduced once. It has three introduction points in this
repository, and they concern two different objects. The earliest is not in the route at all: it is
`D1`, "matter adiabatic response", a module of the macro 3D->2D smooth-reduction programme that
predates the current governance layer. The earliest *formulation*, however, is available only inside
its own retraction — the version that stated it is not in the repository.

**Evidence:**

- `Macro3D_to_2D_Smooth_Reduction_Roadmap.md`, module-dependency paragraph, names it as a
  component of the physical boundary layer: "the physical boundary layer (compactification
  framework, D2 power-law contraction, D1 adiabatic criterion, parameter scans) converges on the
  conditional conclusion of a 'sci-fi boundary'". The block diagram below that paragraph reads
  "D1: adiabatic criterion (complete)".
- `DCC_Macro_2D_Execution_Spec_v1.2.md` §0.2 gives its status and its ceiling in one row:
  "D1: matter adiabatic response | Only preliminary screening parameters | η<1 cannot serve as a
  universal stability theorem".
- The context of introduction is in the same table, one row down: "Matter 2D-reduction transport |
  Incomplete | Cannot claim atoms, chemical bonds or macroscopic objects will automatically adapt".
  Adiabaticity entered to answer *that* — whether matter follows the contraction — not to describe
  the contraction.
- The original formulation, `DCC_Macro_2D_Execution_Spec_v1.2.md` §2.1–§2.2:
  `η_rough = ħ|ȧ_z/a_z|/ΔE(t) = ħβ_C/(ΔE(t)·t)`, with the stricter instantaneous form
  `ε_mn(t) = ħ|⟨m(t)|Ḣ|n(t)⟩| / |E_m(t)−E_n(t)|²`, `m≠n`.
- The rationale is stated as a comparison of rates: the contraction rate `|ȧ_z/a_z|` measured
  against the microscopic gap `ΔE(t)`. Nothing more.
- The earliest formulation is quoted only as a deletion. §2.2: "v1.1's 'β_C>1 guarantees
  adiabaticity' must be deleted and replaced by scanning (β_C, t_0, ΔE(a_z)) for each model."
  `Macro3D_to_2D_Smooth_Reduction_Roadmap_v1.4.md` §2.8 item 3 lists it among texts that "do not
  exist in v1.4 and may no longer be cited in any chapter". No `*v1.1*` file is present in the
  repository, so the first statement of the premise survives only as its own obituary.
- The second introduction point is a different object. `docs/decisions/kinematic_vs_dynamic_unfolding_v1.md`
  §7 measures two response times against `t_rip`: through-thickness `2δ/c_s = 4.30e-13 s` and
  in-plane `R/c_s = 1.80e-4 s`, ratio `R/(2δ) = 4.19e8`.
- The third is the promotion. §12 of the same document: "The smooth 2D-ization branch — the reading
  in which a real 3D body is transformed into an effective-2D one *continuously* — presupposes that
  the transformation is slow compared with the system's internal response, i.e. adiabatic."

**Assessment:** The referent migrates between the first and third points, and the migration is
unmarked. In `D1` adiabaticity is a property of **matter's response to a prescribed geometry**,
quantified by a quantum criterion on a mode tower, and it answers "does the material follow?". In
§12 it is a property of **the transformation's rate**, and it answers "is the conversion smooth?".
Those are different questions with different failure modes, and only the first has a criterion on
file. The word travelled; the criterion did not.

A second, separate provenance fact belongs here because the directive's chain asserts the dependency
outright. The dependency has been voided once already. `Macro3D_to_2D_Smooth_Reduction_Roadmap_v1.4.md`
§2.8 lists as items that "do not exist in v1.4":

> 1. The dichotomy of `η≥1` destroyed region / `η<1` smooth conversion region;
> 2. "`η<1` for all components simultaneously is a prerequisite";

So the premise has held three statuses in this repository: **prerequisite** (spec v1.1), **voided as
a prerequisite** (roadmap v1.4 §2.8), **WORKING-HYPOTHESIS** (§12, round 71). The third is not a
contradiction of the second — §12 says explicitly "not a blocking prerequisite" — but the sequence is
not a monotone refinement either, and a reader of §12 alone would not know that the prerequisite form
had been withdrawn two versions earlier. The withdrawal lives in a Layer-B document
(`Macro3D_to_2D_Smooth_Reduction_Roadmap_v1.4.md`), which `reports/DCC_research_progress_v1.md` names
as the basis of the current `G0′` chain but which is not in the `docs/` tree that carries the live
governance text.

------------------------------------------------------------------------------
2  SUBTASK 1.2 — FUNCTIONAL DECOMPOSITION
------------------------------------------------------------------------------

**Finding:** Of the seven functions that can be attributed to the premise anywhere in the record,
two are load-bearing (`F1`, `F2`), one is load-bearing but open (`F5`), one acts on a letter of a
scene classification (`F6`), and three are empty. The three empty ones are the functions the
directive's arrow assumes.

**Evidence:** Each row cites where the function is exercised, and what the record says happens if
it fails.

| id | function | dependency location | consequence of failure |
|---|---|---|---|
| `F1` | Matter structure retention — atoms and bonds not dissolved by the contraction | roadmap v1.4 §2.2 table; spec v1.2 §2.1–2.2; `D1` | matter arrives 2D but reorganised: `surface_conductivity_v1.md` §4 branch **B**, "non-adiabatic but bound / reorganizable — a new low-dimensional state forms" |
| `F2` | Temperature retention — no violent heating during conversion | roadmap v1.4 §2.2 conclusion 1, which splits it from `F1`: "Structure preservation and temperature preservation must be split into two independent criteria" | object heated; v1.4's own disposition requires "the non-adiabatic heating term of the phonon sector" in the R1-A energy ledger |
| `F3` | Continuity of the geometric 2D-ization, `L_z(t)` | **none** — `a_z(t)` is prescribed by `D2` | none: geometry is an input, so the premise is not consulted |
| `F4` | Global smoothness of the conversion | **none** — already conceded | none: `front_sweep_v1.md` §2 states that smoothness "holds in the advance of the front ... and fails everywhere between layers (all 8.12×10⁹ interfaces are broken)" |
| `F5` | Mode freezing / occupation preservation, `χ√C = 1` | `DCC_P3_Effective_Theory_v1.md` §2; `DCC_P3_mode_freeze.py` | particle production in the `|ṁ|/m² > 1` region near `t_0`; the production spectrum is the open `P3-C1` item |
| `F6` | Supplies the `S` letter of the `{E,S,W}` corner | `scifi_boundary_v1.md` §4 | falls to `{E,¬S,W}`: 41.2 Mt fireball, 99× solar surface brightness, 1–10 s of colour |
| `F7` | Anything at all for `RL-6`, `G0′` row 1, `RL-2`'s relief scene, Phase 1/1b/1c | **none** | none: every one of these is a static or length-ratio statement with no time ordering to be slow or fast |

**Assessment:** `F3` and `F4` are the two functions the word "smooth" invites, and both are empty.
The record's own Layer-B text has already replaced the notion that `F4` could hold:

> Even if the background contraction is strictly adiabatic, matter acquires real internal energy.
> "Smooth" must therefore be redefined as "this internal energy can be carried away by some
> dissipation channel", not as "no excitations". — roadmap v1.4 §2.5

Under that definition adiabaticity is neither necessary nor sufficient for smoothness. What is
necessary is a dissipation channel, and what adiabaticity governs is only how large the excitation
budget that channel must absorb is. So the directive's first arrow is true for the *matter* half of
2D-ization and false for its *geometric* and *global* halves, and the reason is not a defect of the
premise but an earlier, explicit redefinition that §12 does not carry forward.

Two further asymmetries are worth recording because they change what "failure" would mean.
`F1` and `F2` are decided by *different sectors*: v1.4 §2.2 conclusion 1 finds the softest failure is
not electronic but phononic (`η_rough ≈ 0.56` for meV phonons), while "the nucleon sector is safe
(`η ~ 10⁻²`)". And v1.4 forbids using its own table in the reverse direction: the entries "may not be
used in reverse as evidence that 'adiabaticity holds'". The premise therefore has a sector-resolved
answer and no aggregate one — which is why a single binary label has never fitted it.

------------------------------------------------------------------------------
3  SUBTASK 1.3 — PHYSICAL BASIS AUDIT
------------------------------------------------------------------------------

**Finding:** There are two candidate bases, on two different objects. The first is a real
time-dependent oscillator driven by an artificial clock. The second is a real body under a
counterfactual load, measured with an undeclared material parameter. Neither basis is empty, and
neither is the object §12's phrase "counterfactual elastic body" describes.

**Evidence:**

*Basis A — the mode tower (the `D1` lineage).* `DCC_P3_Effective_Theory_v1.md` §2 gives the
effective mass `m_eff(t) = |p_z|/C(t)` and the adiabatic parameter `|ṁ_eff|/m_eff² = |β_C|C/(|p_z|t)`.
This is the standard adiabatic parameter of a time-dependent oscillator: a quantum object, with a
gap, an occupation number and a well-defined adiabatic theorem. It is not an auxiliary invention —
it is the ordinary machinery applied to the contraction. What it rests on is the clock. The
background `B(t) = C(t)^{-1}` is `D2`, and `DCC_Macro_2D_Execution_Spec_v1.2.md` §0.2 records what
`D2` is: "It is an externally specified background, not endogenous dynamics", with `D3` —
"endogenous contraction dynamics" — listed as "Incomplete". So the oscillator is real and its
frequency is chosen.

*Basis B — the loaded plate (§7).* `S5`/`S6` print two times but only one length (`δ = 0.215 nm`,
`docs/decisions/demo_object_ruling_v1.md`) and one ratio (`R/(2δ) = 4.19e8`). Registration §4 fixed
the reconstruction before use: solve the pair
`2δ/c_s = 4.30e-13 s` and `R/c_s = 1.80e-4 s` for `(c_s, R)`. The solution is
**`c_s = 1.000e3 m/s`, `R = 0.180 m`**, and it reproduces the printed ratio as `4.186e8` — a `0.09 %`
deviation (`CK1`, pass at the declared `2e-3`). The reconstruction is therefore accepted, and the
two numbers it produces are the finding.

  - **The body exists; the load does not.** `0.215 nm` is the deposited plate thickness, and
    `R ≈ 0.18 m` is consistent with the recorded plate areas `6×10⁻³–5×10⁻² m²`. So the body §7
    describes is the deposition's own material. What is counterfactual is that it was ever
    compressed: `front_sweep_v1.md` §2.1 states "**D2 performs no deformation** ... there is no
    stored energy to release — hence no rebound, no delamination, no recovery". The correct
    description is a counterfactual *loading* of a real body, not a counterfactual body. §12's
    phrase is too strong in one direction and too weak in the other.
  - **`c_s` is nowhere declared.** It appears in the same record under the same symbol as a value
    5.33 decades larger: `G0′ §2` gives `c_s = c/√2 = 2.1199e8 m/s` for the 2D ultra-relativistic
    gas. The elastic value `1.000e3 m/s` is a soft-condensed-matter sound speed and is the physically
    appropriate one for a polymer-like plate — but it is recovered here, not read off.
  - **The comparison to `t_rip` depends on that undeclared choice, and the ratio does not.**
    `R/(2δ) = 4.19e8` is geometric and survives any `c_s`. The sentence it supports — "There is no
    instant at which that body looks like the kinematic map" — rests on the *comparison*, not the
    ratio. At `c/√2` the two times become `2.0284e-18 s` and `8.4912e-10 s`, both **before**
    `t_rip = 8.2553e-9 s` (`2.457e-10 ×` and `1.029e-1 ×`), and the body would be settled in both
    directions before the conversion ended. The word "brackets" in §7 is a function of an undeclared
    material constant.

**Assessment:** The placeholder in the directive's third link is occupied twice and differently.
`D1` points at a real oscillator on a prescribed background; §7 points at a real plate under a
counterfactual load. Neither is empty, so the premise is not floating free of physics. But the two
bases are not interchangeable: the first can in principle be evaluated from an eigenproblem, the
second from a wave speed, and only the first carries a criterion into the present route. The route
inherited the second, which is the one whose one free parameter is undeclared and whose sign of
conclusion flips with it. That is a provenance statement about the measurement, not a verdict on the
premise — the premise could be true under either basis, and this document does not decide which.

A third observation belongs in this subtask because it is a property of the archived formula rather
than a new assumption. `S4` §2.1 prints `η(t) = (|β_C|C_0/t_0)/|p_z| · (t/t_0)^{β_C−1}` and states
that `η` "decreases monotonically for `β_C<0`". The exponent is `β_C−1 < −1 < 0` (`N32`), so
`η → 0` as `t → ∞` **by construction of the printed form**. The premise is therefore not a global
property of the conversion but a late-time property of it, and the only open question is where the
`η = 1` crossing sits — which `DCC_P3_C5_Scan_Report_v1.md` §7.2 already answers: it is "determined
by parameter choices (β_C, C_0/t_0, the representative p_z) and is completely insensitive to α and
wall velocity; it is not an intrinsic critical point".

------------------------------------------------------------------------------
4  SUBTASK 1.4 — FAILURE MODE ANALYSIS
------------------------------------------------------------------------------

**Finding:** All three of the directive's modes occur in the record, each attached to a different
function, and none of them is the record's own current expectation. The record's own pointer is a
fourth mode the trichotomy omits: **undecidable**.

**Evidence:**

- **Pseudo-failure** — `F3`, `F4`, and the kinematic reading. Removing the premise changes nothing,
  because there is no rate to be slow: `front_sweep_v1.md` §2.1 (no deformation, no stored energy),
  and §12's own dependency table already prints "`C2` smooth 2D-ification, intralayer reading |
  none — identity of the prescribed map" and records that the premise is "**unnecessary** for the
  kinematic one".
- **Soft failure** — `surface_conductivity_v1.md` §4 branch **B**: "non-adiabatic but bound /
  reorganizable — a new low-dimensional state forms". This is a first-class recorded outcome whose
  label is "assigned by computation, not by choice", so soft failure is not a hypothesis about what
  might happen; it is a slot the programme has already built for it.
- **Hard failure** — branch **C**: "bound-state destabilization or structural destruction". The
  measured evidence against it firing is `DCC_P3_C5_Scan_Report_v1.md` §7.2: "the robustly
  destroyed region is **empty** within the reasonable interval" of `(β_C, p_z)`.
- **Undecidable** — branch **D**: "model or the classical approximation fails — **cannot be
  determined**". And the same page says: "`D` is a real outcome and the record's own evidence
  currently points at it (`N7`: particle-number conservation *invalid* at 73.4 MeV)."

**Assessment:** Read through the record's taxonomy, "what happens if adiabaticity fails" resolves to
`D` first, `B` as the fallback, and `C` as the one branch the scan did not find. The directive's
trichotomy assumes failure would be *observable as a state change*; the record's position is that
the criterion itself loses its referent before that can be decided. This is the same failure mode
`N7` records for carriers and `RR-DT` recorded at B8: a referential failure, not a numerical
shortfall. It also explains why the premise has never been given a binary label that held — under
`D` there is no fact of the matter to label.

The classification is therefore not "soft" or "hard" but **sector-dependent and branch-labelled**,
which is precisely how `surface_conductivity_v1.md` §4 requires every result to be reported: "A `σ_s`
without a branch label is `NO-VERDICT`, not a low score."

------------------------------------------------------------------------------
5  SUBTASK 1.5 — ALTERNATIVE ROUTES TO SMOOTH 2D-IZATION
------------------------------------------------------------------------------

**Finding:** Four alternatives exist; three of them are already in the record and required no new
assumption to state. The strongest is not a different limiting process but the record's own
redefinition of smoothness.

**Evidence:** one entry per alternative, with the archive that carries it.

1. **Late-time asymptotic adiabaticity (already a property of the archived formula).**
   `η ∝ (t/t_0)^{β_C−1}` decreases without bound for `β_C<0`, so for any fixed gap the late phase is
   inside the criterion's own adapted band by construction; only the early window near `t_0` is at
   risk. This is not a new mechanism and not a symmetry argument — it is algebra on `S4`'s printed
   formula. Reading: this is the cheapest alternative because it requires no new premise, and it
   narrows the question from "is the conversion adiabatic?" to "how early does `η` fall below the
   band?", which `P3-C5` has already scanned.
2. **Dissipation instead of adiabaticity (the record's own redefinition).**
   Roadmap v1.4 §2.5 defines smooth as "this internal energy can be carried away by some dissipation
   channel", not as "no excitations". Reading: this is the strongest alternative, because it makes
   smoothness a statement about an energy ledger rather than a rate, and the record already requires
   that ledger ("the energy ledger of R1-A must explicitly include the non-adiabatic heating term of
   the phonon sector"). It is the only alternative that neither introduces a premise nor reverses the
   §12 promotion — it makes the promotion *unnecessary* for smoothness while leaving it meaningful
   for the excitation budget.
3. **The opposite idealisation: a sudden quench.** Rather than slow, take `t_rip → 0`. In the sudden
   limit the state does not follow the instantaneous eigenbasis at all, so the object is carried into
   the new geometry with its 3D wavefunction intact. Reading: this is not a route to smooth
   2D-ization but the priced route *away* from it — branch `B`/`C` of `surface_conductivity_v1.md`,
   and in scene language `RR-DT`'s B4 corner `{E,¬S,W}` (41.2 Mt, 1–10 s of colour). Recorded
   because the directive asks for it; it is a failure mode in disguise.
4. **Abandoning "smooth" for "piecewise smooth".** Reading: not an alternative — it is the current
   description. `front_sweep_v1.md` §2 already reports smoothness at the front and failure at all
   `8.12×10⁹` interfaces, and calls the result "not falsifiable by any image at `t ≤ t_rip`". Adopting
   it would change no claim, which makes it the fourth pseudo-alternative alongside pseudo-failure.

No symmetry-protection route is recorded anywhere. The nearest thing to one is item 1, and it is a
statement about a gap that grows rather than about a charge, a topological invariant, or a
superselection rule. A search of the record for such protection returned nothing, and none is
invented here (G-73-01 §Prohibitions: no new physical assumptions).

**Assessment:** the four are not four equivalent routes. Item 1 is algebra on an archived formula and
costs nothing. Item 2 is the record's own Layer-B definition and is the only one that makes
smoothness independent of the premise. Item 3 is a failure mode. Item 4 is the present description.
So the honest count of live alternatives is **two**, and the stronger of them is not a limiting
process at all — it is the redefinition of what "smooth" was supposed to mean.

------------------------------------------------------------------------------
SUMMARY
-------

- **Key Finding 1 — the premise has three introduction points and two objects.** It entered as `D1`,
  "matter adiabatic response", with a quantum criterion `η_rough = ħβ_C/(ΔE·t)`; it re-entered in
  `kinematic_vs_dynamic_unfolding_v1.md` §7 as a classical timescale comparison; it was promoted in
  §12 as a property of the transformation. The word migrated from "does the matter follow?" to "is
  the conversion smooth?" and the criterion did not travel with it.

- **Key Finding 2 — the dependency the directive asserts was already voided once.** Roadmap v1.4
  §2.8 lists as non-existent "the dichotomy of `η≥1` destroyed / `η<1` smooth conversion" and
  "`η<1` for all components simultaneously is a prerequisite". The status history is
  prerequisite → voided → WORKING-HYPOTHESIS. §12's promotion is consistent with the voiding, but a
  reader of §12 alone cannot see it.

- **Key Finding 3 — two of the seven functions are load-bearing, three are empty, and the empty ones
  are the ones the arrow names.** `F1` structure and `F2` temperature depend on the premise;
  continuity of `L_z(t)`, global smoothness, and every static quantity (`RL-6`, `G0′` row 1, the
  `RL-2` relief scene, Phase 1/1b/1c) do not. Under v1.4 §2.5's redefinition of smoothness as
  dissipatability, adiabaticity is neither necessary nor sufficient for it.

- **Key Finding 4 — the basis that carried the word into the live route has one undeclared
  parameter, and the conclusion is sensitive to it.** The §7 timescales are reproducible only for
  `c_s = 1.000e3 m/s` and `R = 0.180 m` (ratio reproduced to 0.09 %). That `c_s` is 5.33 decades
  below the `c/sqrt(2)` used elsewhere under the same symbol; at `c/sqrt(2)` both response times fall
  *before* `t_rip`, and "brackets the conversion" becomes "settles before it". The geometric ratio
  `R/(2δ) = 4.19e8` is unaffected — it is the comparison to `t_rip` that is material-dependent.

- **Key Finding 5 — the record's own answer to "what if it fails" is not soft, hard or pseudo, but
  undecidable.** Branch `D` of `surface_conductivity_v1.md` §4 ("cannot be determined") is where the
  record says its evidence points (`N7`, particle-number conservation invalid at 73.4 MeV); branch
  `B` is the fallback; branch `C` was not found in the scanned `(β_C, p_z)` box.

OPEN QUESTIONS
--------------

- **Q1.** `DCC_Macro_2D_Execution_Spec_v1.2.md` §2.2 deletes "`β_C>1` guarantees adiabaticity" and
  replaces it with a triple scan. No `v1.1` file exists in the repository. Is the deletion text the
  authoritative record of the original formulation, or is v1.1 held elsewhere? This round could not
  settle it by reading.

- **Q2.** Two quantities under the symbol `c_s` differ by 5.33 decades (`c/√2` in `G0′ §2`,
  `1.000e3 m/s` implied in §7). No document declares the elastic value. Which one governs a
  statement that compares a material response time to `t_rip`?

- **Q3.** Roadmap v1.4 §2.5 defines smoothness by dissipatability and requires the phonon
  non-adiabatic heating term in the R1-A energy ledger. No ledger entry carrying that term has been
  located in this round. Does the definition currently have a number behind it?

- **Q4.** v1.4 §2.2 gives `η_rough ≈ 0.56` for meV phonons and `~10⁻²` for nucleons, and §2.3
  restricts the table to a window `B ≳ 2.4×10⁻⁹`. The present route works at `L_z = 1 fm`, i.e.
  `B = 1 fm / 0.07 m = 1.4×10⁻¹⁴`, which is **outside** that window by 5.2 decades. Whether the
  sector-resolved table has any force at the route's operating point is unresolved, and resolving it
  would require a derivation this round is not authorised to make.

- **Q5.** `RR-DT`'s B4 recorded that relaxing adiabaticity selects `{E,¬S,W}` rather than creating a
  branch. If `F2` (temperature) fails while `F1` (structure) holds, the corner reached is `{E,S,¬W}`
  or `{¬E,...}`. No such corner is priced in `scifi_boundary_v1.md` §4. Is that a gap in the scene
  taxonomy or a statement that the combination is impossible?

Content generated by AI
