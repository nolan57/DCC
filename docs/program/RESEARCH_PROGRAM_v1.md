# DCC Research Programme v1.1.1

**Version**: v1.1.1 (2026-11-25). v1: 2026-11-24; v1.1: 2026-11-25. File name retained for citation stability.
**Status**: **ADOPTED** — owner directive of 2026-11-24. v1.1 incorporated the first review; **v1.1.1** incorporates
the second review (`R1–R14`) as a local revision, without changing the goal, the line structure, or the governance
authority.
Item-by-item dispositions: Appendix D (`M1–M20`) and Appendix E (`R1–R14`).
**Supersedes**: (a) the *goal statements* of `G0p_seven_row_verdict_v3` row 1, `relaxation_frame_v1` §6, and
`exhaustive_matrix_route_v1` §I; (b) the *structure* of the 8×4 matrix in `exhaustive_matrix_route_v1` §IV,
replaced by §4 of this document. It does **not** supersede their measurements, prices, verdicts, or audit
findings; those are retained under Appendix A.
**Does not supersede**: `COMPLETION_PROTOCOL_v1` (gate bookkeeping), the constraint definitions in
`constraint_crosswalk_v1`, the tier definitions and thresholds in `intrinsic_structure_tiers_v1`, or the prices
in `relaxation_ladder_v1`.
**Review**: §5.5. A conformance review is mandatory every 5 working cycles or 14 days, whichever comes first.

Normative keywords: **MUST**, **MUST NOT**, **SHOULD**, **MAY**. A clause without a keyword is descriptive.

---

## 0. Why this document exists

The record contains four different statements of "the goal", written at different times, and the later ones
silently replaced the earlier one:

| # | statement | where | what it actually asks |
|---|---|---|---|
| P | front + direction + Einstein equations | `DCC_P0-P4_Roadmap_Plan.md:48–58` | a mechanism question |
| **O0** | **a 3D macroscopic object swept by a 2D-ification front, presented** | `staged_relaxation_visual_route_v1.md` §1 (RATIFIED 2026-11-22) | **the Layer-1 goal** |
| G0′ | ordinary matter surviving at fixed area | `G0p_seven_row_verdict_v3.md:47` | H2 ∧ H3 ∧ H4, a *derived* question |
| PG-03 | a human-legible image: `Q3 ≥ 2` (legibility) and ≈6 bits (identity content, a separate quantity) | `relaxation_frame_v1.md:93–100` | O0 **plus** a recognizability threshold |

`Q3` is a legibility index in distinguishable levels. The `≈6 bits` is the identity content of the four-shell
object (4 shells ≈ 2, radius ratio ≈ 3, phase ≈ 1). They are different quantities: `Q3 = 2` does **not** mean
6 bits, and a scene can pass one and fail the other.

The drift was not a change of mind. It was three substitutions, each locally reasonable:

1. a **model assumption** (fixed projected area) became a **constraint** (G0′ row 1);
2. a **derived number** (slice count) became a **result** and then a **goal**;
3. a **stronger derivative** (recognizability) became **the** goal.

This programme restores O0 as the Layer-1 goal, keeps the other three as *derived lines with their own names*,
and changes the working method so the same substitution cannot happen again without a visible break.

---

## 1. The derivation axiom

> **A1.** Every element of a presentation is the output of a declared physical deduction from a declared
> constraint set, mechanism, and observer. The researcher stipulates **the constraint set and the mechanism**;
> the researcher does **not** stipulate the image.

This is the load-bearing rule of the programme. It has four operational consequences.

### 1.1 What may be stipulated, and what may not

| may be stipulated (input) | must be derived (output) |
|---|---|
| which constraints hold, are violated, or are out of domain | the field `u(x,y,t)` and every rendered frame |
| the mechanism: mapping, front law, layer thickness `δ`, placement law | the number of slices and fragments |
| the object: shape, size, internal structure | the deposit area and site spacing |
| the observer tuple `θ` and the enhancement operators | the tier values `T0–T3` |
| the initial and boundary conditions | the cost, the lifetime, the shutdown signature |
| the declared discretization | the consequences of every violation |

**Test (three layers, not one).** A change of a stipulated item is checked at three separate levels:

| level | what is checked | conclusion if it fails |
|---|---|---|
| **consumption** | the parameter enters the computation graph, equation, or state update | the input is genuinely unused (`GENERATOR-DOES-NOT-CONSUME`) |
| **sensitivity** | a pre-declared output changes with the declared sign and order of magnitude | the model lacks the declared dependence |
| **visibility** | the change exceeds the numerical and display resolution at the declared `θ` | this observer cannot see it |

For the sensitivity layer, declare the pair `(p_j, O_i)` and the expected sign of `S_ij = ∂O_i/∂p_j` **before**
the run. A zero or below-resolution `S_ij` is a legitimate result when it was predicted; it is a defect only
when the declaration said it should be non-zero.

**Numerical definition.** `S_ij` MUST be computed by a declared method — analytic, automatic differentiation, or
finite difference. A finite-difference estimate MUST report `Δp_j`, the noise floor, and the truncation error.
Because `S_ij` carries units `O_i/p_j`, cross-parameter comparison MUST use a declared normalization, e.g.
`Ŝ_ij = (p_j/O_i)·∂O_i/∂p_j` where `O_i ≠ 0`, or an absolute-scale normalization otherwise. The scene card
declares which form is used; this is a reporting requirement, not a universal pass/fail gate.

**Byte-identical is not proof of non-consumption.** A parameter may act only on a region the current frame does
not show, on a symmetry that leaves the chosen observable invariant, or below output precision. Byte-identity
supports `GENERATOR-DOES-NOT-CONSUME` only together with evidence that the parameter is absent from the
computation graph (unused variable, untaken branch, no read). Otherwise record `NO-OBSERVED-EFFECT` and state
the test that would separate the two.

### 1.2 Enhancement is an operator, not a licence

Digital enhancement is permitted, but "enhancement" covers three different kinds of operation, and they carry
different obligations:

| class | examples | obligation |
|---|---|---|
| **display map** | false colour, brightness, contrast stretch, gamma | declare the transfer function, its domain, and whether it is lossy or invertible |
| **measurement operator** | shadowgraph, phase contrast, band migration, transmission channel | declare the forward model that produces the signal; it is an observation, not a filter |
| **time remap** | time compression, loop, interpolation | declare the factor, the interpolation rule, and whether any frame is synthesised |

Two rules apply to all three:

1. **Physical-source constraint.** The output MUST NOT contain a physical quantity or structure that is absent
   from the scene. A lossy display map may discard information; it may not create it.
2. **Processing declaration.** The operator MUST be named, parameterised, and listed in the
   `DISPLAY-DECLARATION` block, with its domain and its loss.

An operator that adds structure not present in the field is a hand-drawn image, not a result. Note that
"information-conserving" is too strong for a display map: a clipped contrast stretch is lossy and still legal.
The correct requirement is **source fidelity plus declared loss**, not invertibility.

### 1.3 The frame is the unit of work

For **O0 progress**, the unit is a published frame with a scene card and either a measured profile or an explicit
`NOT-MEASURED` profile slot — not a ledger row, not a verdict, not a gate. A cycle that produces no frame, no
corrected drift, and no closure of a declared technical item produced nothing.

"Closure of a declared technical item" is a first-class product: a proved conservation law, a converged
discretization study, a defined estimator, or a demonstrated non-computability. Such a cycle MUST NOT be
presented as an O0 artifact (see §5.1).

### 1.4 Negative results are content

A violation is a legitimate scene. `C2`-inter breaking, `C3` neutronization, a 3 ns shutdown — these are things
the presentation **shows**. They are not obstacles to the presentation and MUST NOT be hidden to make a frame
look better.

---

## 2. Layer 1 — O0

### 2.1 Statement

> **O0.** Given a macroscopic 3D object and a 2D-ification front, produce a reproducible presentation of the
> **transformation process — including the front's time evolution — and its result**, with the scene, the
> probe, and the per-constraint status all declared.

### 2.2 Decomposition

| component | requirement |
|---|---|
| **scene** | object, front geometry and law, mechanism, discretization, initial state, units, coordinate convention |
| **constraints** | `C1`, `C2`, `C3` each labelled HELD / VIOLATED / OUT-OF-DOMAIN, with the ground |
| **process** | at minimum `t0` (before), `t_mid` (mid-sweep), `t_end` (after); plus a continuous sequence or a time-compressed animation with a declared factor |
| **result** | the end state, including the deposit geometry |
| **observer** | `θ = (q, band, gate, aperture, distance; E, G)`; instruments and enhancement allowed |
| **effective-2D label** | per `(subsystem, probe)`: `IS_2D` / `LOOKS_2D` / `NOT_2D`, or `NOT-MEASURED` with the missing slot named |
| **reproducibility** | manifest, solver spec, run record, declared reproduction level `R1–R4` (§5.3) |

### 2.3 Explicit non-requirements

O0 does **not** require any of the following. Their absence is not a failure of O0.

- fixed projected area (`H2`);
- particle-number conservation (`H3`);
- survival of atoms, chemical bonds, or the non-covalent network (`H4`);
- naked-eye visibility;
- a steady state;
- recognizability of the original object;
- a particular number of slices;
- `C1 ∧ C2 ∧ C3` all holding simultaneously.

### 2.4 What "under the constraints" means

In O0 the constraints are **scene conditions**, not a pass/fail examination. "Under `C1/C2/C3`" means:

> the scene is generated with each constraint in a declared state, and the presentation shows the consequence of
> that state.

It does **not** mean "all three hold". A scene with `C3` violated is an O0 scene. A scene with `C2` violated by a
declared non-isometric mapping is an O0 scene.

This is the clause that dissolves the old ambiguity in `staged_relaxation_visual_route_v1` L1 ("C1+C2+C3 all
held"), which was written when `C3` was already a NO-GO.

### 2.5 Acceptance

Two different bars must not be conflated.

**O0 minimum acceptance** — a submission is an O0 artifact if and only if all five hold:

1. the scene card and manifest are complete and hash-locked before rendering;
2. at least three keyframes exist, covering `t0`, `t_mid`, `t_end`;
3. every frame carries its `DISPLAY-DECLARATION`, an effective-2D label, and a `T0–T3` profile slot — measured
   or `NOT-MEASURED` with the missing slot named;
4. every constraint's state and consequence is visible in the frame or its caption;
5. a third party can reproduce the declared target: `R2` for the physical quantities; `R3` for the frame itself
   if frame reproduction is claimed.

A submission that claims only `R2` MUST NOT say its frame was reproduced.

**Research publication acceptance** — in addition to the five above:

6. the `T0–T3` profile is reported with estimator identity and version (§4.3);
7. discretization error or convergence evidence is reported for every cited quantity;
8. the conservation / non-conservation ledger is reported (§4.2.3–4.2.4);
9. the price ledger is complete for every relaxation used (§3.5);
10. `M` is stated as a history functional or with a proved Markov extended state (§2.6), and every slice/fragment
    count is labelled as counted or modelled, with its derivation and error (§4.8).

An artifact may pass O0 minimum and fail publication. It MUST then be labelled `O0-ARTIFACT`, not `RESULT`.
Failure mode for both: an image that cannot be regenerated from its card, or that contains a quantity absent
from the scene.

### 2.6 State space — the map O0 has to write down

A presentation is a deduction only if the three objects below are defined and the map between them is written
down. This is the clause that prevents `u(x,y,t)` from being drawn by hand.

| object | symbol | content |
|---|---|---|
| **3D body state** | `U(x,y,z,t)` | the physical state the mechanism consumes: density, composition, temperature, fields, structure |
| **front state** | `φ(x,y,z,t) = 0` (or equivalent) | position, normal, thickness, speed, and the law that advances it |
| **2D output** | `u(x,y,t)` | the deposited / reduced state and the field the observer samples |

The **map** `M` MUST be stated as a history functional unless the state is proved Markov:

```
u(t) = M[ U(τ), φ(τ); 0 ≤ τ ≤ t ]
```

If the map is instantaneous, the scene card MUST name the extended state variables (deposited field, interface
state, any path-dependent internal variable) that make it so. A map that ignores history without proving
Markov-ness is not defined. `M` MUST also state:

- its domain (which `z` interval is being reduced at time `t`);
- its units and coordinate convention;
- whether it is single-valued, and what happens where two layers compete for one site;
- what it discards (mass, energy, momentum, particle number, phase, …), and where each discarded quantity is
  entered in the conservation ledger (§4.2.3–4.2.4).

`u` MUST NOT be an independent input. If a frame's `u` cannot be recomputed from `U`, `φ`, and `M`, the frame
is an illustration (A1). A level-set form is permitted but not required; any explicit front description with a
stated normal and speed is acceptable.

---

## 3. Layer 2 — the relaxation spectrum

### 3.1 Layer 2 is derived from Layer 1

Layer 2 asks: *how far can the scene be pushed, and at what price?* It is not a second goal and it does not
replace O0. It supplies O0 with branches and prices.

The spectrum runs from **strict physical self-consistency** to the **hard science-fiction boundary**. It is a
**partial order of declared relaxations**, not a scalar axis:

```
strict ── one relaxation ── two relaxations ── … ── hard-SF boundary
                                                        │
                                                        └── beyond: myth
```

`λ = 0` and `λ = 1` are retained only as **endpoint labels**, not as a computed score. No scalar `λ` is defined,
because violating `C1` and violating `C2` have no universal order and no common unit. Each relaxation carries
its own price vector (§3.5); combinations are recorded as a set, with any interaction stated explicitly (§3.2.1).

The boundary is already drawn in the record and is adopted here verbatim in substance
(`scifi_boundary_v1.md` §7, `relaxation_frame_v1.md:55`):

> **hard science fiction** = finite knobs, computable consequences, explicit cost.
> **myth** = none of these.

### 3.2 The price record

Every relaxation MUST carry three obligations, recorded as four fields (`relaxation_frame_v1.md` §3):

1. **what it relaxes**, named as a clause of the record — never as a mood;
2. **its price**, in a native unit and, where possible, as a dimensionless indicator, **with the observable that
   would detect it**;
3. **its fingerprint** — the measurement that tells an observer which branch they are on.

A relaxation without a fingerprint is illustration. It MAY be narrated; it MUST NOT enter the matrix as a cell.

### 3.2.1 Combining relaxations

When two or more relaxations are active, the scene card MUST state:

- whether they are **independent** (prices add or multiply in the declared currency) or **coupled**;
- whether one **implies** the other (a non-isometric map changes area, which changes a column density);
- whether one **cancels** part of another, and on which observable;
- the **combined fingerprint**: the measurement that distinguishes the combination from each factor alone.

If no combined fingerprint exists, the combination is not a matrix row; it is a narrative branch.

The combination rule MUST be exactly one of four types:

1. **independent price vectors** — components are kept separate and no total is formed;
2. **declared physical composition law** — addition or multiplication is allowed only where the quantities share
   a space and the law is written down;
3. **coupled computation** — the joint mechanism is run; the prices are not combined algebraically;
4. **no combined fingerprint** — narrative branch, not a row.

### 3.3 Any constraint may be violated

`C1`, `C2`, `C3` are stipulations, not facts. All eight combinations are admissible rows **when all three
constraints have a referent**; where one is out-of-domain, the scene occupies a face of the cube (§4.2.1):

- a **HELD** constraint is the strict branch;
- a **VIOLATED** constraint is a declared branch whose consequences are computed and shown;
- an **OUT-OF-DOMAIN** constraint is one with no referent in that scene (e.g. `C2` where no layer mapping
  exists). This is a domain statement, not a verdict.

What is **not** permitted is an **unpriced** violation: one whose consequences are neither computed nor shown.

### 3.4 Where the spectrum ends

Beyond the hard-SF boundary the programme may still *say* things, but it may not *claim* them:

- no cell in the matrix;
- no tier value;
- no price;
- no frame presented as a deduction.

This is not a moral restriction. It is the definition of "computable": past the boundary there is no solver,
no knob, and no fingerprint, so there is nothing for a cell to contain.

### 3.5 Relation to the record's prices

The existing prices are retained and re-used, not re-derived:

| item | price | status |
|---|---|---|
| `RL-5` persistence | `6.2e23 V/m` (4.7e5 × Schwinger) or a 2D pocket (Geroch) | measured, unbuilt |
| `RL-6` same matter | `2e4×` atomic spacing (`15.4 fm` vs `0.3 nm`) | measured |
| `RL-4` visible transmission | `\lvert Z_0\sigma_s\rvert ~ 1e4` at 2.25 eV | closed by measurement |
| `RL-1` instrumented observer | `V = 0` | **not measured — free, highest priority** |
| `RL-2` relief | `V = ε` | not measured |
| `RL-3` oblique illumination | `V = 0` | not measured |

**Price record schema.** The numbers are retained as written. What this programme adds is a uniform *record*
around them, not a re-pricing:

```
(clause_relaxed, Π_raw, Π, O_detect, F)
```

- `Π_raw` — the price in its **native unit** (for `RL-5`, `6.2e23 V/m`; for `RL-6`, `2e4` atomic spacings);
- `Π` — the **dimensionless** comparison indicator (for `RL-5`, `E/E_Schwinger = 4.7e5`), or `UNSPECIFIED`
  where no defensible ratio exists;
- `O_detect` — the observable that would detect the violation, with band and conditions fixed;
- `F` — the fingerprint that distinguishes the branch.

`Π_raw` and `Π` MUST NOT be conflated: a dimensional field and a dimensionless ratio are different records.
Every ladder row MUST be transcribed into this schema before it is cited in a matrix cell. Transcribing is not
re-deriving: if a field is missing in the source, write `UNSPECIFIED` and cite the gap; do not invent it.

These prices are inputs to Layer 2. They are not the Layer-1 goal.

### 3.6 Three lines, one goal

| line | question | status |
|---|---|---|
| **A — presentation (O0)** | what do the process and the result look like, and what does each constraint do to them? | **main line** |
| **B — identity** | does the image resemble the original object, and at what price? | separate line; MUST NOT set acceptance for A |
| **C — feasibility and price** | is the mechanism self-consistent, and what does each relaxation cost? | supporting line; feeds A with branches and prices |

A line may fail without failing the programme. **Only Line A failing fails O0.** Line B's `Q3 ≥ 2` and Line C's
`G2′–G6` chain are not gates on Line A, and a NO-GO in either is not a NO-GO of the presentation.

---

## 4. The research matrix v3

### 4.1 Axes

```
rows    : the 8 combinations of (C1, C2, C3)          — stipulated
columns : the 4 intrinsic tiers T0–T3                  — measured
depth   : the observer tuple θ                          — declared
time    : keyframes t0 / t_mid / t_end (+ sequence)     — derived
cell    : one profile entry with status and provenance  — derived
```

**Rows are chosen; cells are derived.** A cell MUST NOT be filled by hand.

### 4.2 Rows

| # | row | status | scene |
|---|---|---|---|
| 1 | `C1 C2 C3` | `COUNTERFACTUAL(C3)` | 2D-ified, `C2` held, `C3` held — must be marked counterfactual because `C3` is in-action NO-GO |
| 2 | `C1 C2 ¬C3` | `CONSTRUCTIVE` | baseline: 2D-ified, neutronized / 3 ns transient |
| 3 | `C1 ¬C2 C3` | `VIOLATION(C2) + COUNTERFACTUAL(C3)` | declared non-isometric map (stretch / shear / tear) |
| 4 | `C1 ¬C2 ¬C3` | `VIOLATION(C2)` | non-isometric map, neutronized |
| 5 | `¬C1 C2 C3` | `VIOLATION(C1) + COUNTERFACTUAL(C3)` | column conservation broken by a declared source/sink; layers still exist |
| 6 | `¬C1 C2 ¬C3` | `VIOLATION(C1)` | non-conserving sweep, neutronized |
| 7 | `¬C1 ¬C2 C3` | `VIOLATION(C1,C2) + COUNTERFACTUAL(C3)` | non-conserving + non-isometric |
| 8 | `¬C1 ¬C2 ¬C3` | `VIOLATION(C1,C2)` | non-conserving + non-isometric, neutronized |

Notes:

- **No row is `VOID`.** The old `VOID` label was a verdict about *one mechanism*, written as a verdict about the
  *scene*. Rows 3, 4, 7, 8 were never empty; they lacked a mechanism.
- **`¬C1` means column conservation is violated, not that there is no 2D-ification.** A declared source, sink, or
  loss mechanism produces a 2D scene whose columns do not balance. That is a scene, and it is measurable.
- **`¬C2` requires a declared non-isometric mapping.** "Non-zero strain has no construction under rigid
  translation" is true and irrelevant: it is a statement about one mechanism.
- **The untransformed object is not a row.** It is the `t0` keyframe of every row. A `REF-3D` calibration scene
  MAY be measured outside the eight; it MUST NOT be counted as a ninth row.

#### 4.2.1 `OUT-OF-DOMAIN` is not a third truth value

The eight rows enumerate `{HELD, VIOLATED}³` for constraints that have a referent. `OOD` is an **applicability
vector** recorded beside the row, not a third value inside it:

- a scene with one `OOD` constraint occupies a **face** of the cube, not a corner;
- `OOD` MUST NOT be written as `HELD` (untested) or as `VIOLATED` (failed);
- no cell may be reported in the `OOD` constraint's column for that scene.

The row identifier therefore has the form `(C1, C2, C3; OOD = {…})`.

#### 4.2.2 Two status fields, never one

Row status and cell status answer different questions and MUST be stored separately:

```yaml
scene_class:        CONSTRUCTIVE | COUNTERFACTUAL | VIOLATION   # what kind of scene is this?
measurement_status: PASS | FAIL | REFUSED | NOT-APPLICABLE | NOT-MEASURED   # did this measurement run?
```

A `PASS` on a `COUNTERFACTUAL` row means "the conditional computation met its threshold". It MUST NOT be read
as "the scene is physically realizable". The row's `scene_class` travels with every cell.

A parenthesised constraint names the reason for the class — `COUNTERFACTUAL(C3)`, `VIOLATION(C2)`. The class is
the word outside the parenthesis; the parenthesis is not a fourth value.

#### 4.2.3 Conservation under a non-isometric map

A declared map such as `(x,y) → (1.01x, 1.01y)` has `det J = 1.0201`: lengths grow by 1%, areas by 2.01%. If
the row also claims `C1` held, the conserved quantity MUST be transformed with the map, not left in the old
coordinates. For a column density `Σ`:

```
Σ'(x') = Σ(x) / |det J|,        ∫ Σ' dA' = ∫ Σ dA
```

Every `¬C2` scene card MUST report:

- the map and its Jacobian;
- the area change;
- the transformation rule for the conserved quantity;
- any source/sink term;
- the numerical error of the conserved integral before and after.

`C1 ∧ ¬C2` is admissible; "`C1` held" as a label without the transformation law is not.

This is the pushforward for a **locally invertible** map. A `tear` that produces disconnected regions, a fold,
or a multi-valued map is **not** covered. For a non-injective map:

```
u(x) = Σ_{x' ∈ M⁻¹(x)} Σ(x') / |det J(x')|
```

and tear boundaries MUST be assigned a measure (zero-width interface or a declared finite width). Where
`det J = 0`, the single-density formula MUST NOT be applied; the cell states the degenerate-set treatment.

#### 4.2.4 The `¬C1` source/sink must be written

"Column conservation broken by a declared source" is not yet a mechanism. The `¬C1` scene card MUST state:

```
∂Σ/∂t + ∇₂·J₂ = S(x,y,t)
```

with the physical origin, units, spatial distribution, and time dependence of `S`, and the conservation ledger
that shows the imbalance. If `S` represents exchange with a 3D reservoir outside the reduced domain, the
reservoir's own budget MUST be recorded; otherwise the equation records the failure of conservation without
accounting for the exchanged quantity. `S = 0` returns the row to `C1` held.

#### 4.2.5 Counterfactual rows are conditional computations

A row with `C3` held is `COUNTERFACTUAL`: the known in-action NO-GO (`ρ + p_x < 0`) is fixed by assumption. Its
scene card MUST state:

- **which type of counterfactual it is**, from the three below;
- which solver implements it;
- which outputs are conditional deductions and which would be measurable in a real scene;
- that the result MUST NOT be cited as a prediction of a realizable process.

| type | construction | what may be claimed |
|---|---|---|
| **off-shell background** | fix `ρ + p_x < 0` as a prescribed background; do not require it to solve the original equations | the geometry / observable consequences of that background; **not** a solution |
| **conditional solution** | add an explicit constraint or boundary condition and solve the conditional system | a conditional result, with the constraint and domain stated |
| **modified dynamics** | add a source term or mechanism that makes the condition hold | a result of the **new** equations, with its own price; "original equations unchanged" is forbidden |

If the conditional system has no solution, record `NO-SOLUTION`; do not synthesise a trajectory to produce a
frame. "Original equations unchanged" is compatible only with the first two types, and only when the
corresponding mathematical object is written down.

#### 4.2.6 The `C3` state vector

`C3` acts through named state variables, not through a label. The `C3` branch MUST declare, at minimum:

| variable | symbol | why it matters |
|---|---|---|
| electron fraction | `Y_e`, `Z/A` | composition; drives `n_e` |
| electron density / Fermi energy | `n_e`, `E_F` | the internal effective-2D bound |
| conductivity / optical response | `σ_s(ω)` | `T3` and the visible channel |
| lifetime | `t_life` | 3–5 ns transient vs steady |
| neutrino luminosity | `L_ν` | energy and radiation channel |

The consumption test MUST compare these variables, not only `u(x,y,t)`. A byte-identical `u` with a different
`Y_e` means `u` does not encode composition — not that `C3` is invisible.

If a `C3` branch claims a quantitative neutronization, optical response, or shutdown, it MUST declare the closure
scope of the chain:

```
Y_e, n_b → n_e = Y_e n_b → EOS → E_F, μ_e, P_e → σ_s(ω) → optical response
L_ν(t) → E_ν = ∫ L_ν dt → energy ledger → t_life
```

`t_life` is derived from the dynamics and the energy ledger, not an independent input. For a mixture, `Y_e` is the
abundance-weighted electron fraction, not one nuclide's `Z/A`. Items outside the declared scope are marked
`OUT-OF-SCOPE`, not silently omitted.

### 4.3 Columns — the intrinsic tiers

Use `intrinsic_structure_tiers_v1` (T0–T3). These refer to the **scene**, never to the original object.

| tier | quantity | threshold | measures |
|---|---|---|---|
| **T0** | `Q0 = 1 − P0(u)/P0(𝒩)` | `≥ 0.50` | topological organization / fragmentation |
| **T1** | `Q1 = ξ/h` | `≥ 4.0` | characteristic scale present |
| **T2** | `Q2` (renormalized conditional entropy) | `≥ 0.50` | neighbourhood predictability |
| **T3** | `Q3 = log₂(1 + C_ξ·q/C_eye)` | `≥ 2.0` | legibility through a declared observer |

`P0` is the persistence functional of `intrinsic_structure_tiers_v1` §2. In `T3`, `C_ξ = std(u_ξ)/mean(u)` is
dimensionless and `C_eye = 0.01` (Weber contrast threshold), so the ratio is dimensionless by construction; the
cell's estimator record fixes the remaining conventions.

Rules:

- report a **profile**, not a maximum — the tiers are not a total order;
- `T3` MUST name `q` and `θ`; `q = 1` for a declared instrument, `q = 0` for the naked-eye reflected channel;
- `T3` with no characteristic scale (`ξ/h < 2`) returns **no verdict**, not zero;
- thresholds are locked before evaluation and MUST NOT be re-priced after seeing a result.

**Tier definition contract.** This programme does not redefine the tiers; it requires each cell to be
recomputable from its own record. Every `T0–T3` cell MUST carry:

- the estimator identity and version (section of `intrinsic_structure_tiers_v1`), not just the letter `T0`;
- the reference ensemble `𝒩` and its seed;
- the grid, binning, and any smoothing scale;
- the threshold and its lock hash;
- for `T3`, the expanded `θ` (units and domains), not the opaque symbol.

**Version pinning.** The estimator identity includes the authority's version. If the authority publishes a new
estimator, an existing cell keeps pointing at the version it used; it MUST NOT be silently recomputed under the new
definition while retaining its old cell id. Re-measurement is a new cell with a recorded id and a version bump.

If any of these is missing, the cell is `NOT-MEASURED`, not `PASS`.

`Q3` is a **legibility index** in distinguishable levels. It is not the identity content of the object. The
`≈6 bits` in §0 is a separate quantity and MUST NOT be inferred from `Q3 ≥ 2`.

**`q = 0` is a channel result, not a scene verdict.** The authority defines `q` from the declared photon budget;
for the naked-eye **reflected** channel it is exactly `0` because that budget is zero
(`intrinsic_structure_tiers_v1` §5; `matrix_reading_rules_v1` `MR1.3`). Substituting `q = 0` gives `Q3 = 0`
identically: that channel delivers no distinguishable levels, whatever the scene. The programme MUST NOT invent a
non-zero baseline for it — that would be an unpriced relaxation. Other naked-eye channels (emission,
transmission, shadowgraph) are different `θ` and MUST be evaluated on their own budgets; "naked eye" is not a
single channel.

**Contrast calibration.** `C_ξ` is the band-limited RMS contrast of the DoG-filtered field, not a universal Weber
contrast. `C_eye = 0.01` is the Weber threshold under the declared viewing geometry (`DC4`). `θ` enters through
`q` (photon budget) and through `u_ξ` (band and point-spread); `band`, `gate`, `aperture`, and `distance` MUST be
shown to affect one of those two, or the cell is mis-specified.

`T3` is computable for `ξ/h ≥ 2`; `T1`'s threshold is `4.0`. A profile with `T1 = FAIL` and a valid `T3` is
legitimate and MUST NOT be collapsed to "no structure". If `ξ/h < 2`, `T3` returns `NO-VERDICT`, not `0`.

### 4.4 The observer axis

Every `T3` cell carries `θ = (q, band, gate, aperture, distance; E, G)`. The same scene at two `θ` is two cells.
`q = 0` is not a failure of the scene; it is one probe's result.

`θ` MUST be expanded in the manifest with units and domains. `E` and `G` MUST be defined there (environment and
camera/transfer model, respectively); they MUST NOT be used as opaque symbols in a cell.

### 4.5 The time axis

Minimum three keyframes:

| keyframe | content |
|---|---|
| `t0` | before the front arrives |
| `t_mid` | front at an intermediate position (the `mid_sweep_frame_v1` slot) |
| `t_end` | after the sweep; deposit geometry |

Plus **either** a frame sequence **or** a time-compressed animation with a declared compression factor. Both are
permitted; both MUST state which.

Every frame carries its own profile **slot** — a measured `T0–T3` profile or `NOT-MEASURED` with the missing
slot named — plus its effective-2D label, `C3` annotation, and `θ`.

### 4.6 Where `C3` lives

`C3` is not "invisible". It is a row axis **and** a process annotation, and it can change `T3` and the
effective-2D label if the optical response is recomputed.

| `C3` consequence | T0 | T1 | T2 | T3 | effective 2D | time |
|---|---|---|---|---|---|---|
| `ρ + p_x < 0` (action-level) | no | no | no | no | possibly | possibly |
| neutronization (`Z/A`, `n_e`, `E_F`) | no | no | no | **yes**, if `σ_s` recomputed | **yes** | **yes** |
| neutrino escape | no | no | no | possibly | no | **yes** |
| 3 ns shutdown | no | no | no | no | no | **yes** |

So the correct statement is:

> `C3` has no slot in `T0–T2` **when the field carries only geometry/density**. It has a slot in `T3`,
> in the effective-2D label, and on the time axis.

The row's constraint state is fixed for the whole scene; a frame records the **consequence** at that time. A
`t0` frame in which the front has not arrived does not make `C3` absent — it makes the consequence not yet
manifest. Store `constraint_state` (scene) and `constraint_consequence(t)` (frame) separately.

If two `C3` branches produce a byte-identical `u(x,y,t)`, that is evidence that `u` does not encode composition.
It becomes `GENERATOR-DOES-NOT-CONSUME` only if the C3 variables of §4.2.6 are also unchanged and absent from the
computation graph; otherwise record `NO-OBSERVED-EFFECT` and say which encoding is missing.

### 4.7 The effective-2D label

Effective 2D reduction is a **four-slot conditional**, not a property (`effective_2d_definition_v1` §1):

```
(model) ∧ (subsystem) ∧ (E_occ < ΔE_z) ∧ (E_probe < ΔE_z)  ⇒  z excitation is suppressed at the probe's scale
```

The two bounds are separate and MUST NOT be merged:

| bound | condition | meaning |
|---|---|---|
| internal | `E_occ < ΔE_z` | the system does not excite `z` above `ε_z` → **is** 2D |
| external | `E_probe < ΔE_z` | the probe cannot excite a `z` mode |

`E_occ` is defined by the source specification as `max(E_F, k_B T)` **for the declared subsystem**. That is a
degenerate-electron occupation scale, not a universal upper bound on every internal excitation. If the subsystem
has ionic, lattice, collective, non-degenerate, or strongly coupled modes that can couple to `z`, the cell MUST
declare the actual occupation scale and justify the substitution; otherwise the label is `NOT-MEASURED`. `ΔE_z`
MUST name the subsystem and the Hamiltonian whose lowest `z` excitation it is.

The external side records three checks, not merged into one:

- **excitation**: can the probe excite a `z` mode? (`E_probe < ΔE_z`)
- **resolution**: can the probe spatially resolve `z`? (point-spread, wavevector, geometry)
- **coupling**: do selection rules and matrix elements keep the probe coupled to `z` even below `ΔE_z`? This one
  is recorded in the manifest, not added as an extra gate.

A probe can fail resolution while passing excitation, or the reverse. `LOOKS_2D` requires the resolution
question to be answered, not only the energy inequality.

Three different claims MUST NOT be merged:

| claim | object | criterion |
|---|---|---|
| **geometric thinning** | the body | `L_z` small compared with the body's other scales |
| **effective 2D** | a subsystem, a probe | the four-slot condition above |
| **visual flatness** | the image | the rendered frame looks flat at `θ` |

A thin deposit may fail the internal bound; a system with live `z` modes may still `LOOKS_2D`. Each frame carries
all three labels separately.

Labels per `(subsystem, probe)`:

- `IS_2D`: both bounds hold;
- `LOOKS_2D`: external holds (excitation **and** resolution), internal fails;
- `NOT_2D`: external fails;
- `NOT-MEASURED`: one of `model`, `subsystem`, `E_occ`, `E_probe`, or `ε_z` is undeclared.

**Tolerance.** `IS_2D` means "the `z` excitation is suppressed below a declared tolerance `ε_z`", not "the
probability is strictly zero". Every label MUST state `ε_z` (an occupation fraction or a response upper bound)
and how it is computed from `ΔE_z`, `T`, coupling, and the distribution. A finite-temperature Boltzmann weight
`e^{-ΔE_z/k_BT}` is suppressed, not zero; the label reports the size of the suppression.

`L_z = 0` is not "completion"; it is the point where the space description fails. Effective 2D is `L_z` small
but non-zero, and the smallness is measured against `ΔE_z`, not against a visual impression.

### 4.8 Slice count and discretization

**The number of slices is not part of the goal.** It is a derived quantity:

```
N_slices ≈ H / δ      (δ = declared layer thickness)
```

Valid when `H` is the thickness along the front's advance direction, `δ` is constant, and the front–body geometry
admits a layer decomposition. Otherwise the count is computed from the actual layer decomposition, not from
`H/δ`.

The current mechanism (`front_sweep_v1` §2) gives `δ = 0.215 nm`, `H = 1.74 m`, hence `8.1e9` cells and
`1.18e10` fragments. Those numbers are correct **for that mechanism** and are reported as its output.

`δ` is not a free rendering knob: it is fixed by the mechanism's physics (here, one atomic layer). A different
`δ` is a **different mechanism**, and must be declared as one — not presented as another rendering of the same
scene. The same rule applies to the front law and the map `M`: changing either is a mechanism change with a new
mechanism id and a version bump, not a parameter edit.

The fragment count is a second, independent derivation:

```
N_frag = N_slices × ⟨components per layer⟩
```

`front_sweep_v1` §1 measures `⟨components/layer⟩ = 1.457` on the registered phantom, giving `1.18e10`; the extra
pieces come from the two-leg cross-section and the neck/head splits. A fragment count without its component
rule is not a result.

`1.457` is measured on the registered phantom. Its use for the full body is an **extrapolation** unless the
phantom covers the body's cross-sections and the per-layer component count is stationary. The solver spec MUST
state the phantom's coverage, the sample size, the mean and variance, the weighting of the two-leg / neck / head
regions, and the boundary rule. Until then, `1.18e10` is a **model estimate**, not a counted total.

The programme MUST declare the discretization explicitly, and SHOULD run at least one control:

| branch | what it tests |
|---|---|
| baseline: one atomic layer per slice | the registered mechanism |
| control: continuous front, or `δ` × 10 | whether "cutting" is an artifact of discretization |

Changing `δ` changes the slice count and the interface count. It does **not** change the effective-2D criterion.

The control is judged on quantities, not appearance: deposited mass/area, fragment count, fragment topology,
front position, conserved integrals, and the `T0–T3` profile. A control that only looks similar is not a
convergence test; report the difference and its trend.

### 4.9 Cell schema

```yaml
cell:
  row:                C1_C2_notC3        # constraint combination
  scene_class:        CONSTRUCTIVE | COUNTERFACTUAL | VIOLATION
  ood:                []                 # constraints with no referent here
  time:               t_mid              # keyframe id
  tier:               T0                 # T0..T3
  estimator:          {id: ..., version: ..., params: ...}
  quantity:           0.00               # measured value
  threshold:          0.50               # locked
  observer:           scene-intrinsic    # or expanded theta for T3
  measurement_status: PASS | FAIL | REFUSED | NOT-APPLICABLE | NOT-MEASURED
  provenance:         {script: ..., sha256: ..., seed: ..., card: ...}
```

`measurement_status` vocabulary is fixed:

- `PASS` / `FAIL` — evaluated against the locked threshold;
- `REFUSED` — the tier itself failed admission (null passed, or no control did);
- `NOT-APPLICABLE` — no referent in this scene;
- `NOT-MEASURED` — in scope, not yet run.

`NOT-APPLICABLE ≠ FAIL ≠ REFUSED ≠ NOT-MEASURED`. Collapsing them is the error that produced `U-1`.
`scene_class` is not a measurement status; it answers a different question (§4.2.2).

### 4.10 Matrix discipline

1. Rows are stipulated; cells are derived.
2. Thresholds are locked before evaluation.
3. No per-cell choice of metric.
4. No constraint added after seeing a cell. A new constraint (`C4`, `C5`, …) creates a **new row set** with a
   version bump, registered before execution.
5. `C3` is a row axis and a process annotation; it is not a static shape axis.
6. Every cell carries time, observer, and provenance.
7. An empty column is a legitimate result. An empty column is not a reason to add a constraint.

---

## 5. Research method

### 5.1 The cycle

Replace the audit-first loop with a fast, artifact-first loop:

```
1 DECLARE   one page: scene, mechanism, constraint states, theta, predicted profile
2 DERIVE    script + parameters + seed; hash the declaration before running
3 RENDER    frames at t0 / t_mid / t_end (+ sequence)
4 MEASURE   T0-T3, effective-2D label, cost
5 PUBLISH   frame + scene card + profile table + DISPLAY-DECLARATION
6 REVIEW    conformance check against this programme (Appendix C)
```

Three cycle types are recognised; only the first produces an O0 artifact:

| type | product | publishable as O0? |
|---|---|---|
| **artifact cycle** | frame + card + profile slot (measured or `NOT-MEASURED`) | yes |
| **technical closure cycle** | a proved conservation law, a converged discretization study, a defined estimator, a demonstrated non-computability | no — label `TECHNICAL` |
| **governance cycle** | conformance review, drift correction | no |

The 1–3 day target applies to artifact cycles. A technical closure cycle has no fixed duration; it ends when the
declared question is answered. A cycle that cannot close in its window is scoped too large; split it.

### 5.2 Locked versus free

| locked (changes need a version bump) | free (changes every cycle) |
|---|---|
| this programme | object variants |
| `C1/C2/C3` definitions | mechanism parameters |
| tier definitions and thresholds | `δ`, mapping, front law — changed only as a declared **mechanism** change |
| the derivation axiom | rendering, enhancement choices |
| the status vocabulary | order of work |
| each cell's `θ` once published | which row to run next |

**Speed comes from moving the audit from *before every step* to *attached to every artifact*.** Fast does not
mean unfalsifiable; it means the falsification travels with the frame.

### 5.3 Audit, demoted to a checkpoint

The old mode — pre-register every step, hash every sentence, treat the ledger as the product — is retired as the
**operating** mode. It is retained as a **checkpoint** at three moments:

1. before a claim leaves the programme (external claim);
2. at each conformance review (§5.5);
3. whenever a definition or threshold changes.

Provenance is layered; a one-page card is the entry point, not the whole model.

| layer | content |
|---|---|
| **scene card** | one page: object, mechanism, constraints, `θ`, parameters, predicted profile |
| **manifest** | machine-readable: full parameters, equations, units, boundary conditions, dependencies |
| **solver spec** | discretization, numerical method, tolerances, stability and convergence evidence |
| **run record** | code version/commit, solver version, dependency versions, RNG and version, input hashes, environment |
| **frame sidecar** | `DISPLAY-DECLARATION`, `θ`, enhancement operators |

Reproduction levels, declared per artifact:

| level | target |
|---|---|
| **R1** | the model and computation can be re-executed |
| **R2** | key physical quantities agree within tolerance |
| **R3** | frames and profile agree within a declared output tolerance |
| **R4** | bit-identical |

O0 minimum acceptance requires **R2** unless the card declares otherwise; `R4` is never required by default.
GPU reductions and image encoding can make `R4` unattainable for reasons that are not scientific; that is why it
is not the default.

`R2` covers the **physical quantities**; it does not certify the frame. A claim that the frame itself was
regenerated requires **R3**. A claim that only the physics was reproduced MUST say so and MUST NOT say the image
was reproduced.

### 5.4 Prohibited moves

These are the historical drift patterns, named so they can be caught in review.

| # | move | historical instance |
|---|---|---|
| 1 | promoting a model assumption to a constraint | fixed area → `G0′` row 1 |
| 2 | promoting a derived number to a goal | slice count; `d∥` |
| 3 | promoting a stronger derivative to the goal | recognizability / `Q3 ≥ 2` |
| 4 | reading "no construction under mechanism M" as "no scene" | `¬C2` → `U-1` |
| 5 | reading "no slot in the model" as "physically invisible" | `C3` "column-invisible" |
| 6 | letting the audit become the product | ledger rows outnumbering frames |
| 7 | adding constraints after seeing results | `C4, C5, …` in the old Phase 2 |
| 8 | choosing a metric per cell | old matrix `L1` |
| 9 | claiming visibility without `θ` | `S9` violations |
| 10 | hand-editing a frame and calling it a result | enhancement without declaration |

A review that finds one of these MUST log it as a deviation (§8) and stop the affected workstream until it is
corrected.

### 5.5 Cadence and conformance review

| review | frequency | scope | output |
|---|---|---|---|
| **cycle review** | every cycle | Appendix C, variant by cycle type | PASS / DRIFT, one line |
| **conformance review** | every 5 cycles or 14 days | Appendix C, all items | signed checklist + corrective actions |
| **programme review** | quarterly, or on a `D3/D4/D5` event | this document | amendment or reaffirmation |

A conformance review MUST answer, in writing:

1. Which frames were published this period, and which O0 requirement does each close?
2. Which cells moved from `NOT-MEASURED` to a verdict?
3. Was any derived quantity treated as a goal? (drift #2)
4. Was any model assumption promoted to a constraint? (drift #1)
5. Was any mechanism limitation written as a scene impossibility? (drift #4)
6. Did any claim appear without `θ`, tier, and provenance? (drift #9)
7. Is the matrix still 8 rows, or did a constraint get added without a version bump? (drift #7)

A "no" to 3–7, together with either a non-empty answer to 1–2 or a recorded `TECHNICAL` closure, is a **PASS**.
Anything else is a **DRIFT** with a corrective action and a date.

A period with no new cell verdict is not automatically a DRIFT. If the period closed a declared technical item
(§5.1), the review records `TECHNICAL` and the item; only an unexplained absence of both a frame and a closure
is a DRIFT. Governance identifies deviation from the programme; it does not penalise unfinished science.

The checklist is applied by cycle type: an **artifact** cycle answers items 1–6; a **technical closure** cycle
answers items 3–13; a **governance** cycle answers items 6–12. A missing frame is not a DRIFT in the last two.

---

## 6. Workstreams

| id | workstream | question | first product |
|---|---|---|---|
| **W1** | front kinematics and time series | what does the process look like frame by frame? | 3-keyframe sequence + time-compressed animation |
| **W2** | constraint branches | what do `¬C1`, `¬C2`, `¬C3` scenes look like? | non-conserving branch; `s = 1.01` stretch branch; neutronized branch |
| **W3** | tier measurement | what is the `T0–T3` profile of each frame? | profile table per row × keyframe |
| **W4** | observer and enhancement | what does each `θ` deliver? | `θ` matrix; `DISPLAY-DECLARATION` on every frame |
| **W5** | effective-2D labelling | is it 2D, does it look 2D, or neither? | per-frame label with the four slots |
| **W6** | price and boundary | what does each relaxation cost? | `RL-1`, `RL-2`, `RL-3` measurements (expected low-cost; confirm after the measurement spec) |
| **W7** | identity line (separate) | does the image resemble the original? | external `L0–L3` line, retained but not the goal |

W7 is explicitly **not** the main line. It is kept because the record built it and because a recognizability
claim may be wanted later. It MUST NOT set the acceptance criterion for W1–W6.

### 6.0 Dependency order

The workstreams are not parallel peers. The dependency graph is:

```
state space (§2.6) ──► W1 front kinematics ──► W2 constraint branches ──► W3 tiers
                              │                        │                     │
                              └──────────────► W5 effective-2D ◄─────────────┘
                                                       │
                              W4 observer/display ◄────┘
                                                       │
                              W6 price ◄───────────────┘
                                                       │
                                                       ▼
                                             O0 publication bundle
```

`T3` depends on `W4` (it needs `θ`); `T0–T2` depend on the field only. `W6` takes its prices and fingerprints
from the concrete violation mechanisms built in `W2`, not from the ladder text alone.

### 6.1 Near-term plan (next 3 cycles)

1. **Scene card** for row 2 (`C1 C2 ¬C3`): `δ`, placement law, `θ`, predicted profile.
2. **Three keyframes** `t0 / t_mid / t_end` with `T0–T3` and effective-2D labels; `t_mid` reuses
   `mid_sweep_frame_v1`.
3. **Discretization control**: continuous front or `δ × 10`; compare deposited mass/area, fragment count and
   topology, front position, conserved integrals, and the tiers — not appearance.
4. **`¬C2` branch**: `(x,y) → (1.01x, 1.01y)`; report the Jacobian, area change, conserved-integral error, and
   the tiers against row 2 at `t_mid` (§4.2.3).
5. **`C3` consumption test**: compare `u(x,y,t_mid)` **and** `Y_e`, `n_e`, `E_F`, `σ_s`, lifetime, and neutrino
   channel for held vs neutronized; a byte-identical `u` alone is not evidence of non-consumption (§4.2.6).
6. **`RL-1` measurement**: `Q3` at `θ_fast` on a scene that carries 2D-ified content — never done.

Items 3–5 are cheap and independent; they can run in parallel.

---

## 7. Deliverables

Every published item is a bundle, not a file:

| artifact | content | format |
|---|---|---|
| **scene card** | object, mechanism, constraints, `θ`, parameters, seed, hash | one page, YAML + prose |
| **frame** | PNG with `DISPLAY-DECLARATION` sidecar | `.png` + `.display.txt` |
| **profile** | `T0–T3` × row × keyframe, with status and provenance | CSV |
| **cost note** | price record for every relaxation used | Markdown |
| **review** | Appendix C checklist | Markdown, signed |

A frame without a scene card is an illustration and MUST NOT be cited.

---

## 8. Governance

### 8.1 Deviation classes

| class | meaning | action |
|---|---|---|
| **D1 wording** | the text says something the programme does not | owner authorises; fix in place; no science change |
| **D2 reclassification** | a result belongs to another line | move it in Appendix A; no re-run |
| **D3 goal drift** | a derived goal is being used as the goal | stop the workstream; revert; log |
| **D4 definition change** | `C1/C2/C3` or a tier changes | version bump; re-run affected cells |
| **D5 constraint addition** | a new constraint enters the matrix | new row set; version bump; register before execution |

D1 and D2 still require owner authorisation: "fix in place" describes the edit, not the authority. D2 moves a
result between lines and never alters the underlying data. D3–D5 MUST NOT be approved by an executor or by a
routine cycle review.

### 8.2 Amendment

Only the owner may amend this programme. An amendment MUST be written and MUST include a **"what this orphans"**
section listing every cell, price, or frame whose meaning changes.

### 8.3 Retirement

A claim is retired by adding a line to Appendix A with the superseding document. Deleting a claim is not
permitted; the record's value is that its mistakes remain legible.

---

## 9. What this programme does not claim

- that any row is physically realizable;
- that the ladder closes, or that any rung is bought;
- that the object is recognizable;
- that the deposit geometry is unique;
- that `C3` can be held (it cannot, in-action);
- that `C1`'s `d∥ = 15.4 fm` is a constraint rather than a number conditioned on `H2`;
- that the slice count is a result of the goal rather than of the mechanism.

---

## Appendix A — disposition of existing record objects

| object | disposition | reason |
|---|---|---|
| `C1/C2/C3` definitions | **KEEP** | the constraint vocabulary; `C1`'s `d∥` is conditioned on `H2`, the constraint is not |
| `front_sweep_v1` slice geometry | **KEEP** | the result geometry for the current mechanism |
| `deposit_serial_v1` 7/7 | **KEEP** | addressable encoding of the result |
| `unfold_is_real_v1` "cutting, not unfolding" | **KEEP** | a substantive O0 finding; conditional on the discrete mechanism |
| `mid_sweep_frame_v1` | **KEEP** | the first `t_mid` frame; object `1.74 m`, array `36.1 km`, separation `2.1e4` |
| `unfold_appearance_v1.png`, `painting_render_v1.png` | **KEEP** | endpoint images at two `θ` |
| `P4_pipeline` | **KEEP** | the observer chain |
| `route_goal_conformance_v1` G1–G5 | **KEEP** | the direct audit of O0; 0/5 at the time |
| `G0′` seven rows | **RECLASSIFY** | `H2 ∧ H3 ∧ H4` question, not O0 |
| `RL-5`, `RL-6` prices | **RECLASSIFY** | price of persistence / same matter; not required by O0 |
| `G2′–G6` feasibility chain | **RECLASSIFY** | mechanism feasibility line, not the goal |
| `PG-03` `Q3 ≥ 2` / 6 bit | **RECLASSIFY** | a stronger derivative goal; W7 |
| `B3` constraint stress | **RECLASSIFY** | critical only under steady-state / fixed-area branches |
| `exhaustive_matrix_route_v1` 8×4 | **SUPERSEDE** | rows and columns both replaced by §4 |
| `exhaustive_matrix_route_v1_disposition` | **KEEP** | the audit that killed the old matrix; its findings remain valid |
| `matrix_v2_spec_v1` | **KEEP as input** | `C3` "changes the price, not the scene" is a model-closure statement, now scoped |

The supersede of `exhaustive_matrix_route_v1` is **structural**: its rows and columns are replaced by §4. Its
audit findings, measured prices, and disposition verdicts remain in force. "Superseded" never means "all
conclusions void".

---

## Appendix B — glossary

| term | meaning |
|---|---|
| **O0** | the Layer-1 goal: reproducible presentation of the 2D-ification process and result |
| **H2 / H3 / H4** | fixed projected area / particle-number conservation / survival of atoms, bonds, network |
| **held / violated / out-of-domain** | the three admissible states of a constraint in a scene |
| **price record** | four fields: clause relaxed, `Π_raw`, `Π`, `O_detect`, `F` |
| **hard-SF boundary** | finite knobs, computable consequences, explicit cost |
| **myth** | none of the three; narratable, not renderable as a deduction |
| **T0–T3** | intrinsic tiers: organization, scale, predictability, legibility |
| **`θ`** | observer tuple `(q, band, gate, aperture, distance; E, G)` |
| **`IS_2D` / `LOOKS_2D` / `NOT_2D`** | internal bound holds / only external bound holds / neither |
| **`ε_z`** | declared suppression tolerance for the `z` excitation; `IS_2D` means below `ε_z`, not strictly zero |
| **`q = 0`** | the naked-eye reflected channel's registered channel factor: zero exposure budget, so `Q3 = 0` identically |
| **`GENERATOR-DOES-NOT-CONSUME`** | an input is shown absent from the computation graph (unused variable, untaken branch); byte-identity alone is not sufficient |

---

## Appendix C — conformance checklist

Apply by cycle type (§5.1): **[A]** artifact, **[T]** technical closure, **[G]** governance. Answer PASS / DRIFT;
any DRIFT needs a corrective action and a date. A missing frame is not a DRIFT for `[T]` or `[G]`.

1. **[A]** **Frames.** At least one frame was published this period, with scene card and `DISPLAY-DECLARATION`.
2. **[A]** **O0 coverage.** The frames cover `t0`, `t_mid`, `t_end`, or the gap is stated.
3. **[A/T]** **Derivation.** Each frame's stipulated inputs and derived outputs are separated on its card; for a
   technical closure, the declared question's inputs and derived outputs are separated in the closure record.
4. **[A/T]** **Constraints.** Every constraint is labelled HELD / VIOLATED / OUT-OF-DOMAIN with a ground.
5. **[A/T]** **Effective 2D.** Every frame carries a per-`(subsystem, probe)` label, or `NOT-MEASURED` with the
   missing slot named.
6. **[A/T/G]** **Provenance.** Manifest, solver spec, and run record are present at the declared level.
7. **[all]** **No goal drift.** No derived quantity is being used as the goal (slice count, `d∥`, `Q3`, area).
8. **[all]** **No constraint inflation.** No model assumption has been promoted to a constraint.
9. **[all]** **No scene/impossibility collapse.** No mechanism limitation is written as a scene impossibility.
10. **[all]** **No unpriced violation.** Every violated constraint has a price and a fingerprint, or is marked
    narrative.
11. **[all]** **Matrix integrity.** Still 8 rows, or a version bump records the change.
12. **[all]** **Vocabulary.** `NOT-APPLICABLE`, `FAIL`, `REFUSED`, `NOT-MEASURED` are not collapsed.
13. **[T]** **Closure record.** The declared question is answered, or explicitly recorded open with the reason and
    the next test.

## Appendix D — disposition of the 2026-11-25 review

Dispositions for v1.1; retained for traceability. v1.1.1 items are in Appendix E.

Review items `M1–M20`. No item was rejected outright. `M5` is **modified**: the programme does not duplicate the
tier definitions, because a duplicate would create a second source of truth; it requires recomputability
instead. `M14` is **modified**: `R4` is not the default, because bit-identity is not a scientific requirement.

| id | issue | disposition | where |
|---|---|---|---|
| M1 | A1 sensitivity test too strong | **ACCEPT** — replaced by consumption / sensitivity / visibility | §1.1 |
| M2 | 3D state, front, `u` map undefined | **ACCEPT** — state space `U`, `φ`, `u`, `M` added | §2.6 |
| M3 | C1/C2 conservation under non-isometric map | **ACCEPT** — Jacobian and transformation law required | §4.2.3 |
| M4 | `E_occ` vs `E_F` | **ACCEPT** — `E_occ = max(E_F, k_BT)`; `E_F` is the `T→0` case | §4.7 |
| M5 | T0–T3 definitions incomplete | **MODIFY** — no duplication; estimator identity + recomputability contract | §4.3 |
| M6 | C3 causal mapping incomplete | **ACCEPT** — C3 state vector and multi-variable consumption test | §4.2.6 |
| M7 | counterfactual rows lack computational identity | **ACCEPT** — four required card fields | §4.2.5 |
| M8 | OOD not encoded in the eight rows | **ACCEPT** — OOD is an applicability vector | §4.2.1 |
| M9 | row status and cell status mixed | **ACCEPT** — `scene_class` and `measurement_status` split | §4.2.2, §4.9 |
| M10 | `1.18e10` fragments underived | **ACCEPT** — component rule added | §4.8 |
| M11 | "information-conserving" enhancement imprecise | **ACCEPT** — source fidelity + declared loss | §1.2 |
| M12 | `λ` has no metric | **ACCEPT** — partial order; endpoints only | §3.1 |
| M13 | price triple not uniformly applied | **ACCEPT** — 4-tuple schema; no re-pricing | §3.5 |
| M14 | hash/seed insufficient for reproduction | **MODIFY** — layered manifest + `R1–R4`; `R2` default | §5.3 |
| M15 | scene card too thin | **ACCEPT** — card / manifest / solver / run record split | §5.3 |
| M16 | O0 acceptance inconsistent with publication | **ACCEPT** — minimum vs publication split | §2.5 |
| M17 | W1–W7 dependencies implicit | **ACCEPT** — dependency graph added | §6.0 |
| M18 | 1–3 day cycle pressures theory | **ACCEPT** — three cycle types | §1.3, §5.1 |
| M19 | supersedes scope ambiguous | **ACCEPT** — goal vs matrix structure separated | header, App. A |
| M20 | D1 authority ambiguous | **ACCEPT** — D1/D2 owner-authorised; D3–D5 never executor-approved | §8.1 |

**Evidence boundary.** The review could not inspect the four authoritative sources the programme does not
supersede. This revision therefore does not alter their content; it adds contracts that point at them. A
cross-check of `constraint_crosswalk_v1`, `intrinsic_structure_tiers_v1`, `relaxation_ladder_v1`, and
`COMPLETION_PROTOCOL_v1` against the clauses cited here remains a `TECHNICAL` item under §5.1.

## Appendix E — disposition of the second review (`R1–R14`)

Two items (`R1`, `R5`) are **not** accepted as formula changes. In both cases the formula or definition is the
authority's registered object; changing it inside this programme would create a second source of truth, which §1
forbids. The underlying clarity problem is accepted and fixed by scoping, not by rewriting the authority.

| id | issue | disposition | where |
|---|---|---|---|
| R1 | `q = 0` makes `Q3 = 0` for the naked-eye reflected channel | **MODIFY** — registered result (zero exposure budget); channel verdict vs scene verdict; other naked-eye channels are separate `θ`; no invented baseline | §4.3 |
| R2 | counterfactual "fixed condition, unchanged equations" | **ACCEPT** — three types: off-shell / conditional / modified; `NO-SOLUTION` record | §4.2.5 |
| R3 | `R2` cannot certify frame regeneration | **ACCEPT** — `R2` physical, `R3` display | §2.5, §5.3 |
| R4 | O0-ARTIFACT vs per-frame `T0–T3` | **ACCEPT** — artifact: profile or `NOT-MEASURED`; RESULT: computed profile | §1.3, §2.5 |
| R5 | `E_occ < ΔE_z` has no freezing tolerance | **MODIFY** — keep the authority's `E_occ`; add subsystem scope + `ε_z` suppression tolerance | §4.7 |
| R6 | `M` ignores history | **ACCEPT** — history functional; Markov only with a named extended state | §2.6 |
| R7 | Jacobian rule for tear / non-injective maps | **ACCEPT** — branch-sum pushforward; degenerate-set treatment | §4.2.3 |
| R8 | `1.457` extrapolated to all layers | **ACCEPT** — model estimate; coverage, sample size, variance required | §4.8 |
| R9 | C3 EOS / energy / neutrino chain | **ACCEPT as scope** — declare closure scope; full microphysics not required for O0 | §4.2.6 |
| R10 | `Π` dimensional vs dimensionless conflict | **ACCEPT** — `Π_raw` + `Π` | §3.5 |
| R11 | T3 contrast / `θ` calibration | **ACCEPT** — DoG band-limited contrast; `θ` enters via `q` and `u_ξ` | §4.3 |
| R12 | cycle review not matched to cycle type | **ACCEPT** — conditional checklist | §5.5, App. C |
| R13 | W6 "all cheap" unsupported | **ACCEPT** — expected low-cost, to be confirmed | §6 |
| R14 | "price triple" vs four-field schema | **ACCEPT** — "price record", four fields | §3.2, App. B |

**Points from the review body outside `R1–R14`.** Also incorporated, because they close the same gaps:

- estimator **version pinning** — an authority update does not silently rewrite an old cell (§4.3);
- `¬C1` source `S` that exchanges with a 3D reservoir carries the **reservoir budget** (§4.2.4);
- probe **coupling** (selection rules, matrix elements, wavevector) is recorded in the manifest, not added as a
  gate (§4.7);
- changing `δ`, the front law, or `M` is a **mechanism change** with a new id and a version bump (§4.8).

**Why `R1` and `R5` are modified, not accepted.** `q = 0` for the naked-eye reflected channel is not a modelling
choice in this programme; it is the registered photon-budget result (`intrinsic_structure_tiers_v1` §5,
`MR1.3`). A non-zero baseline would silently overturn a measured zero. `E_occ = max(E_F, k_B T)` is likewise the
authority's definition; the correct fix is to state its subsystem scope and add the tolerance that turns
"cannot be excited" into a testable "suppressed below `ε_z`", not to redefine the slot in a second document.

**Effect on the review's HOLDs.** The HOLD on formal effective-2D labels becomes conditional: a label may be
published once `ε_z` and the subsystem scope are declared. The HOLD on C3 counterfactual RESULT remains until the
counterfactual type is chosen and, for the conditional type, a solution or `NO-SOLUTION` is recorded.

*Content generated by AI*
