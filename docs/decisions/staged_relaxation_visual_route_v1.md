# Staged constraint relaxation and presentation-fidelity route v1

**Date**: 2026-11-22
**Status**: **RATIFIED (governor's decision statement, registered verbatim in §1–§6; executor's corrections in §7–§9)**
**Supersedes**: all prior revision drafts and incremental drafts of the visualization route
**Registered by**: AI executor at the governor's instruction ("submit for final decision")
**Products**: `runs/R5/r5l2_sigma_s_results.txt` (v3 baseline), `runs/R5/r5l2_rerun_registration.md`

---

## 1. Goal (verbatim intent)

Present the physical scene of a three-dimensional macroscopic object being swept by a two-dimensionalization
front. Presentation fidelity is **a continuum**, and the project commits to walking the **entire diagonal** of the
constraint-relaxation axis: from *digitally-enhanced discernibility under all constraints* to *naked-eye visible-light
reflection presentation under the minimal constraint set*.

Enhancement (band migration, false colour, contrast stretching, shadowgraph, transmission channel, time compression)
is permitted. **Enhancement must not introduce information that does not exist physically.**

## 2. Constraint set (as registered)

| ID | Constraint | Current status |
|---|---|---|
| **C1** | Effective two-dimensional space (column conservation, $d_\parallel\approx2.91\times10^{-4}a_0$) | ESTABLISHED (identity level) |
| **C2** | Smooth two-dimensionalization (zero intralayer strain) | Holds **intralayer**; interlayer failure registered ($8.12\times10^9$ interfaces) |
| **C3** | Weak-interaction preservation (self-consistent in-action) | **NO-GO established in-action** ($\rho+p_x<0$, parameter-independent) |

## 3. Decision

Abandon "naked-eye visualization satisfying all three constraints in one step". Adopt **staged constraint
relaxation**. Three fidelity levels, each bound to an explicit constraint scope:

| Level | Definition | Constraint scope | Stage |
|---|---|---|---|
| **L1** Digital-enhanced discernibility | band migration, false colour, contrast stretch, shadowgraph/transmission | **C1+C2+C3 all held, zero relaxation** | S0 |
| **L2** Natural-band presentation | image in the physically correct band, enhanced to discernibility | see §7 (correction) | S1–S2 |
| **L3** Naked-eye visible reflection | faithful frame in the eye's eV band, reflection channel | minimal set (C2, then C1 weakened as needed) | S3–S4 |

> **Amendment 2026-11-22 (`docs/decisions/gd_rulings_v1.md`, `GD1` Option B).** The L3 row's "C2, then C1
> weakened" is no longer expressible: `ME1` — `C1`'s only gate proxy — has been reclassified to **`CM5`**, an
> observation-channel predicate, so `C1` now has **no gate expression** and `C2` has none either (`⊥`). The only
> relaxation with a gate expression left in either ladder is Phase 3's `ME3` (`δ_E,max`, the `C_phys` successor),
> and it is specifiable but not yet runnable. The ladder's *ordering* is unaffected; its *vocabulary* is — a
> relaxation commit naming `C1` or `C2` can no longer be registered, and one naming `CM5` is an
> observation-strength declaration, not a constraint relaxation (registry `S7`, amended).

> **Amendment 2026-11-22 (`GD7`) — the fidelity axis now has a direction, and §1's "continuum" is a property.**
> Governor's ruling, verbatim: *"FL means 'faithful to what the human eye sees', and FL3 is the maximum"*. Therefore `FL` is **closeness to the unaided
> retinal image**, and the ladder **ascends**: `FL1` is the floor, `FL3` is the unique maximum.
>
> **The coordinate** (`src/route/fl_coordinate.py`, `runs/ROUTE/fl_coordinate_results.txt`):
> `FL = −(b + c + p + e)`, where `b` is the band offset in decades from the eye's peak (`2.25 eV`), `c` the contrast
> distortion relative to the object's own modulation, `p` the photon-budget deficit, `e` the count of `EN` operators
> applied. Measured on the three rungs: **`FL3 = 0.0000`, `FL2 = −3.1011`, `FL1 = −16.1344`** decades. `FL` is
> continuous in every term (`|dFL/d log₁₀g| = 1.0000` exactly), so `FL1`–`FL3` are **thresholds on a continuum**,
> which is what §1 asserted and never constructed. The equal weighting is a **declared convention** (`DC4`), not
> physics, and is reported rather than scored.
>
> **What the ruling costs, stated plainly.** The most faithful frame is the least informative one, and this is now a
> theorem rather than §9's warning. At `FL3` the frame equals the retinal image, which — because nothing of the sheet
> survives the light round trip — **contains no structure of the object**. `FL` and information are anti-correlated
> by construction, so §9's "presentation fidelity and fidelity to the 2D-ification hypothesis are anti-correlated"
> is recovered as a consequence, at fixed object, rather than as a remark about what happens at ¬`C1`.
>
> **Consequence for the route, registered as `GD9`.** `FL3` is reachable **at zero relaxation** — a faithful
> reflected-light frame of the object's absence needs no constraint given up. So maximising `FL` alone terminates the
> route immediately at the top rung with a vacuous presentation. The goal's phrase *"present the physical scene"*
> carries an information requirement that "maximise `FL`" does not, and the two objectives are anti-correlated.
> Which one the route is scored on is a governor decision (`gd7_gd8_execution_v1.md` §5).

**"Naked-eye is not abandoned" means, concretely:**
1. The visible-reflection module stays on the **critical path**; its blockers (R5-L2 baseline re-run, R5-L3/L4,
   compliant $\sigma_s$, G6, G0↔P2 unit bridge) remain **live registered items**, cleared in order, not parked in a
   distant appendix.
2. The null result is a **live constraint that sets L3's price**: the naked-eye reflection channel requires the final
   state not to tear within the light round-trip, which is possible only in the minimal constraint set. **L3 being
   last is therefore a consequence of the constraint logic, not a priority judgement.**
3. Each promotion registers the relaxation list required at that level and its basis. If a level's relaxation touches
   another established NO-GO, that level is marked **"restricted presentation"** with an explicit statement of what is
   missing — **no silent downgrade**.

**Route:**

- **S0** (C1+C2+C3) → L1: enhanced visualization of the audited bookkeeping — the three-step layer conversion,
  thermal-budget false-colour temperature field, the 2.25 s process (time-compressible). Zero physical relaxation.
  First deliverable.
- **S1** (see §7) → completion of the prescribed-metric bookkeeping, as S0's physical validation baseline.
- **S2** (see §7) → BSSN/Z4c + Gamma-driver self-consistent front. Acceptance: flat space stationary at ~1e-12 over
  t = 20, with growth **decreasing** under refinement (the exact inverse of the B0 signature).
- **S3** (C2 weakened as needed) → interlayer interface discontinuities rendered as texture.
- **S4** (C1 weakened to a minimal set) → L3.

## 4. Floor and discipline

No frame at any level may present falsified content: no picture of intact sheets of ordinary matter being flattened
as a whole and persisting. Every stage product registers **relaxed constraints, retained constraints, enhancement
methods and their physical basis**. Thresholds and acceptance criteria are registered **before** the run, including
the conditions that would falsify prior conclusions.

## 5. Immediate action items

1. **R5-L2 baseline re-run** (v3 baseline, one constant change, thresholds unchanged) — the sole S0 blocker;
   puts the visual input on a compliant baseline rather than a placeholder.
2. **Register this decision as a new clause of the authorised text**, resolving the conflict between §11.1/§11.2's
   prohibition of "mirror-like" wording and the null result's formulation: either authorise the null result to use
   that wording at MODEL RESULT level, or change the null result to a semantically equivalent compliant phrasing
   (choose one, decided by the project governor).

---

## 6. Executor's status report on the two action items

- **Item 1 — DONE.** See §8. `OVERALL: PASS`, all four verdicts pass, one unregistered observation recorded
  (frequency-flat response in the visible band ⇒ zero chromatic contrast).
- **Item 2 — DONE, choosing the second option** (compliant rephrasing), with the trigger for switching to the first
  recorded in §10.

---

## 7. Correction 1 (ledger): "C3 relaxed" in the ladder mislabels a *different* object

**The defect.** §3's L2 row and the S1/S2 route entries say "C3 level-1 / level-2 relaxation" and gloss it as
"prescribed-metric bookkeeping → BSSN self-consistent frontier". But C3 is **weak-interaction preservation**. The prescribed-metric crutch is
**D2** (roadmap §4.2, "specified contraction background, prescribed by hand"). Replacing a prescribed background
with a solved one has nothing to do with weak-interaction preservation.

**Why it matters.** The whole ladder's discipline is "register which constraint was relaxed at each promotion"
(§4). If the ledger assigns the prescribed→solved step to C3, then (a) C3 appears relaxed at S1/S2 when it is not,
and (b) the one genuinely relaxed object — the D2 assumption — is never tracked. The ledger would then be unable to
answer the only question it exists to answer.

**Corrected ledger.** The three columns are *relaxed* (a physical constraint given up), *discharged* (a modelling
assumption replaced by a solved one — a **tightening**, not a relaxation), and *retained*:

| Stage | Relaxed | Discharged | Retained | Product |
|---|---|---|---|---|
| **S0** | — | — | C1, C2, C3 (+ **D2 carried, labelled on every frame**) | L1 |
| **S1** | — | — | C1, C2, C3; D2 **hardened** (bookkeeping completed) | S0's validation baseline |
| **S2** | — | **D2** (prescribed → BSSN/Z4c solved) | C1, C2, C3 | L2 |
| **S3** | **C2** (interlayer interfaces as texture) | — | C1, C3 | restricted |
| **S4** | **C2, C1** (to minimal set) | — | C3 only | L3 |

**Nothing in the route or its ordering changes.** S1 is a hardening step and S2 a discharge step; both are *rigor
increases*, which is exactly why they belong before any relaxation. The corrected reading also makes the ladder
monotone in rigor: S0→S2 strictly tighten, S3→S4 strictly relax.

## 8. Item 1 result — R5-L2 re-run at the v3 baseline (S0 blocker cleared)

**Registration**: `runs/R5/r5l2_rerun_registration.md` (thresholds and four falsifiable expectations fixed
**before** the run). **Product**: `runs/R5/r5l2_sigma_s_results.txt`. **Superseded run archived**, not deleted:
`runs/R5/r5l2_sigma_s_results_v1_REVOKED_BASELINE.txt` (§9.1).

Four changes were forced by the baseline correction; **none is a model change**, and **no threshold moved**:

| Change | From | To | Why forced |
|---|---|---|---|
| `N_2D` | `2.20e27 m^-2` | `2.20e28 m^-2` | §3.4 v3 (revoked value was ×10 low) |
| `E_F_REF_MEV` | `23.20` | `73.37` | §3.4 v3 |
| `MSTAR_FACTOR` | literal `45.4` | **derived** `E_F/(m_ec^2)` = `143.6` | the literal was the pre-v3 value of the module's own declared expression and had silently desynchronised (single-point-of-definition rule, D5 §3 item 3) |
| probe row | `50 MeV` | `200 MeV` | that row exists only to demonstrate the interband switch, whose condition is `ħω > 2E_F`; with `2E_F` = 146.7 MeV the old row falls below threshold |

**Outcome — all four registered expectations met:**

| # | Expectation | Measured | Verdict |
|---|---|---|---|
| E1 | `C0` passes at v3 baseline | `ef_dev = 7.086e-05` (tol 2e-3) | **PASS** |
| E2 | `T1/T2/T3` verdicts unchanged | all PASS; no flip | **PASS** |
| E3 | sheet response `Z0*sigma_s` grows ≈3.16 at fixed τ | 3.162 | **PASS** |
| E4 | `R ≥ 0.999` at 2 eV, τ=1e-16 | `R = 0.999975` | **PASS** |

`OVERALL: PASS`.

**One unregistered observation, recorded as an observation and not as a passed test:** in the eye's band the response
is **frequency-flat**, not merely state-degenerate — `R = 0.975855` at **1.0, 2.0 and 3.0 eV alike** (τ=1e-19),
because `ωτ ≤ 0.304 ≪ 1` makes the Drude form dispersionless across the visible triple. So under this `σ_s` model the
sheet carries **zero chromatic contrast inside the eye's band**. Consequence for S0/L1: **any colour in a rendered
frame is a declared display convention, not a physical inference** (§6.6 already requires this; the number now makes
it sharp, and it is the concrete form of "enhancement must not introduce information that does not exist").

**What this does not establish.** `τ` remains an OPEN input — a `σ_s` at a scanned `τ` is *parameterised*, not
self-consistent; the interband line shape is unknown (switch only); G4/G5′ are open, so every row keeps the
"designated-background test optics" label and **no visibility conclusion is licensed**. Action item 1 is closed as a
*baseline* defect, not as an optics closure.

## 9. Correction 2 (fidelity): the diagonal's endpoint is not a 2D object

**The structural point.** Walking the relaxation axis to its end means weakening C1. But at ¬C1 the object is the
**7 cm slab**: atoms intact, 35 % reflectance, no degeneracy energy, and a front face carrying **~1–2 bit** because
visible light penetrates only 0.09–1.6 mm of a 70 mm thickness. So L3's naked-eye image is legible only via the
*side view* or via C2-derived texture — and at that point the object is **not two-dimensionalized at all**.

Therefore, along this axis, **presentation fidelity and fidelity to the 2D-ification hypothesis are
anti-correlated.** This is inherent in the goal statement (full constraints → minimal constraints) and not a defect,
but it must be written down, because otherwise L3 will later be read as the *success* of 2D-ification when it is in
fact its abandonment.

**Consequence for the closing slogan.** "Each stage's output is the next stage's physical validation baseline" holds
**only for the chain S0 → S1 → S2**, which keeps C1+C2+C3 fixed and merely discharges D2. **S3 and S4 are not
validation baselines for S0–S2** — they are a relaxation branch that trades the hypothesis for visibility, and must
carry a distinct label. Proposed wording, adopted here:

> S0→S1→S2 is a **validation chain** (constraints held, one assumption discharged). S3→S4 is a **relaxation branch**
> (constraints traded for visibility). Products of the branch may not be cited as evidence for the chain.

**Refinement (2026-11-22, adopted after the M_eff boundary draft):** the sentence above was too blunt, and the
draft's §3/§4 supplied the needed distinction. Two categories must be separated:

| Category | Admissible? | Content |
| --- | --- | --- |
| **Boundary data** | **YES** | numbers supplied *into* an S2 solve as outer/asymptotic/Dirichlet data. S2 cannot be solved without them. |
| **Validation evidence** | **NO** | any use of a branch product to argue that the 2D-ification hypothesis, or the S0–S2 chain, is *supported*. |

> **Adopted:** the S3→S4 branch may supply **boundary data** to the S0→S2 solve; it may never contribute to the
> S0–S2 **validation ledger**, nor to any statement about whether 2D-ification works.

**Ratified 2026-11-22 as governor ruling D-A** (`docs/decisions/meff_boundary_disposition_v1.md` §2), with one
condition added, `PROV-3`: boundary data must be **typed** (field, surface, boundary type, regularity),
**non-over-determining** (`n_data` vs `n_dof_predicted`; a solve whose data fix the interior entirely is a
*reconstruction*, not a test) and **derivation-independent** (obtained without assuming C1 or C2). Reason: the
split severs *citation* circularity but not *determination* circularity — Dirichlet data on the whole outer
boundary of an elliptic problem determine the interior, so a labelled split alone would let circularity move
from the citation graph into the boundary-value problem. Enforcement: `docs/conventions/provenance_tags_v1.md`,
`src/common/provenance_lint.py`.

The original sentence is superseded in letter and preserved in intent.

**Also fixed by this:** L2 does not require relaxing C3. "Natural band" is a choice of *observation band*, not of
matter composition. L2's actual dependency is the discharge of D2 (§7) plus a compliant $\sigma_s$ at the chosen
band. Keeping C3 held throughout S0–S2 is what makes the chain a validation chain at all.

## 10. Correction 3 (authorised text): resolution of the "mirror-like" conflict

**Chosen: the second option — compliant rephrasing.** Canonical statement, now authorised at MODEL RESULT level:

> **The naked-eye visible reflected-light channel does not hold.** The two candidate compositions are mutually
> indistinguishable in the eye's band ($|\Delta R|\approx10^{-3}$ at the designated background); the discriminating
> contrast ($|\Delta R|\approx0.53$) lies at $\sim2.5$ keV, outside the eye's response band; and the sheet tears at
> $t_{\rm rip}/(2L/c)=1/\sqrt2$ of the light round-trip **for any size $L$**, so no reflected-light "scene" subsists.
> The transmission channel retains a $1.41\times$ margin and a shadowgraph is **not** excluded. **Digital-enhancement
> channels are not vetoed by this conclusion.**

**"Mirror-like" is withdrawn as a term**, and the claim it carried is retained in the narrowed form "the response in
the eye's band is reflection-dominated because $\omega\ll E_F$".

**Why this option, and not the first.** §11.2's prohibition exists to block one specific illegitimate derivation
(extrapolating $q=k_F$ to optical wavevectors). The null result does not use that derivation, so the prohibition does
not *apply* — but the word "mirror-like" is a quantitative claim that only a compliant $\sigma_s$ can license, and
**no compliant $\sigma_s$ exists yet** (G4 and G5′ open; $\tau$ scanned, not solved; interband line shape unknown).
Authorising the stronger word now would authorise a claim whose input is a placeholder — the reverse of this project's
direction of travel.

**Trigger for revisiting:** once **G6** passes with a solved $\sigma_s(\omega)$, the governor may switch to the first
option (authorise "mirror-like" at MODEL RESULT level). Until then the narrowed phrasing is the only authorised form.

## 11. What this decision does *not* do

- It does not make L1 dependent on BSSN. S0 ships first, exactly as registered.
- It does not relax any CONSTRAINT-gate verdict. C3's in-action NO-GO, C1's identity status and C2's interlayer
  failure all stand unchanged.
- It does not close G4/G5′/G6, and it does not convert any "designated-background test optics" product into a DCC
  observational prediction.
- It does not authorise any frame that shows intact ordinary-matter sheets flattened and persisting (§4 floor).

## 12. Symbol namespace isolation (registered 2026-11-22)

This ledger owns the label **C1, C2, C3** exclusively. That ownership is now a registered rule with a supporting
document, because the repository had accumulated six live collisions between enumerated labels and physical
symbols — not only the reported `C` one.

**Single source of truth: `docs/conventions/symbol_registry.md`.** Rules in brief:

- **R1** A single-letter namespace may enumerate only if that letter has exactly **one** owner. `C` is granted to
  the physical constraints.
- **R2** Ownership goes to the **load-bearing** set, not the oldest. The §6.1 contrast criteria are older than the
  constraint set but are local to R5; the constraints are cited by every gate and every stage. Hence the criteria
  moved: **§6.1 `C1–C4` → `CM1–CM4`**.
- **R3** Every other enumerated label carries a ≥2-letter prefix.
- **R4** Subscripts do not rescue a letter — `C_geo`, `C_phys`, `C_info`, `C_top` are non-compliant on arrival.

**What changed as a consequence**

| Set | Was | Now |
| --- | --- | --- |
| §6.1 contrast criteria | `C1`–`C4` | **`CM1`–`CM4`** (thickness distinguishability / optical contrast / self-emission / visual threshold) |
| Enhancement techniques (this ledger §1, L1 row) | unlabelled | **`EN1`–`EN4`** (band migration / false colour / contrast stretch / shadowgraph) |
| Presentation fidelity levels (this ledger §4) | `L1`–`L3` | **`FL1`–`FL3`** mandatory in new text; interim prose "fidelity L1" vs "optics L1" |
| Localisation diagnostics (roadmap §F.7.4) | bare `C1`–`C7` | **`LOC-C1`–`LOC-C7`** in prose |
| Module-B diagnostics | bare `B0`–`B7` | **`LOC-B0`–`LOC-B7`** in prose |
| Probe checks (`meff_boundary_probe`) | `P1`–`P6` | **`Q1`–`Q6`** (collided with gates `P1a`/`P2`) |
| Proposed M_eff constraints (audit v0.2) | `M1`–`M5` | **`ME1`–`ME5`** (collided with gate `M4` external review, and with mass `M`) |

**Reserved against future misuse.** `B` is the sweep parameter `g_zz = B²`, `K` is the trace of the extrinsic
curvature, `M` is mass — none of these may host a label. Any proposal to reuse `C` for a second meaning requires an
explicit registry amendment with a governor decision (rule S4).

**Formal disambiguation (for derivations and audits).** The two domains are disjoint by construction:
`∀ c ∈ {C1,C2,C3}` are predicates over the evolution of `(γ_ij, K_ij, T_μν)`; `∀ m ∈ {CM1..CM4}` are predicates over
observation and rendering channels. A constraint may never be evaluated on an observation channel and a contrast
criterion may never serve as a boundary condition on the metric. This is what prevents the recurring error of using
a visibility result to discharge a constraint — C3's NO-GO has no `CM` dependence and cannot be softened by any
`CM` statement.

**Conflict detection is a hard check** (`src/common/symbol_lint.py`), not an aspiration: a text using a bare symbol
from a namespace it does not solely own is non-compliant and returns for correction.

**Nothing in this section changes a number, a threshold, or a verdict.** It changes names only.

## 13. Disposition of the M_eff boundary draft (governor rulings D-A, D-B — 2026-11-22)

Both rulings are registered in `docs/decisions/meff_boundary_disposition_v1.md`; the adopted branch spec is
`docs/specs/meff_boundary_v0_2.md`. What changes for **this** ledger:

1. **S2 is now explicitly solvable.** It may take branch **boundary data** under `PROV-3` (§9 above). This
   removes a blocker that would otherwise have surfaced at S2 and been resolved ad hoc.
2. **`C_info` is dissolved** and the v0.1 names `C_geo/C_phys/C_info/C_top` are **retired** (registry R4). The
   branch's constraint set is `ME1`–`ME5`. **No `ME` predicate may be cited as a chain constraint.**
3. **L3's price becomes a gate.** `ME5` requires `τ_exp ≤ √2 L/c` and carries the corollary every L3 product
   must print: *no faithful reflected-light frame of a surviving sheet exists; L3 images a transient.*
4. **Nothing else moves.** The stages, their order, the S0→S2 chain, the S3→S4 branch, and every `C1/C2/C3`
   verdict are unchanged. In particular `C3` remains untouched and its in-action NO-GO remains
   parameter-independent.

---

Content generated by AI
