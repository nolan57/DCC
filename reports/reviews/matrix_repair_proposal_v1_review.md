# Review — "matrix repair proposal" (2×4 reconstruction), submitted 2026-11-23

**Object**: an external repair proposal for `docs/decisions/exhaustive_matrix_route_v1.md`, supplied in four parts
(row cut + counterfactual control; column replacement; design-efficiency gate; keyframe rendering).
**Verdict**: **PART I ACCEPTED AS M0/M1B'S REPAIR. PARTS II–IV ARE REGRESSIONS — each proposed column
re-introduces a defect this record already measured, and the efficiency gate rejects the design it is attached to.**
**Nature of this document**: a *reading* against existing measurements. It runs no code, produces no new number,
and establishes no physics. It is therefore not a round and carries no ledger entry.

---

## 0. The premise, before the parts

The proposal opens with two claims that are not its own content but decide how its content is read.

1. *"The matrix route's underlying logic has already run through."* It has not. §2.4 of the route states: **"Nothing
   in this route has been executed. No cell of the 8×4 matrix has been filled."** What ran was `matrix_audit.py`.
   Its 7/7 is confirmation of *the submission's incompleteness*, and the audit says so in its own words: *"they test
   the submission's completeness, not the physics."* Reading a successful falsification as a passed validation is
   defect class `P1` one level up.
2. *"Design flaws are repairable engineering defects, not theoretical infeasibility."* True for 3 of the 9 blocking
   findings, and the split is exact:

| class | findings | what repair costs |
| --- | --- | --- |
| engineering | `M0`, `M1B`, `M8` | three edits; no physics touched |
| column replacement | `M2`, `M3`, `M4` | the *column*, not the cell — already executed in `tier_admission_v1.md` 4/4, and it moved the evaluated object from "constraint combination" to "declared scene", so it cannot be back-filled into an 8×4 |
| theorem | `M5`, `M6`, `M7` | not repairable inside the route's own definitions |

`M1` (row admissibility) is the tenth finding and the audit counted it non-blocking, but it is the one any repair
must answer: **6 of 8 rows are dead because of what `C2` and `C3` are, not because of how the table was written.**

---

## 1. Part I — accepted, with one arithmetic note and one governance note

**Accepted.** The proposal cuts 7 rows and restores `¬C1∧C2∧¬C3`, leaving
`(C1,C2,¬C3)` vs `(¬C1,C2,¬C3)`. Those are exactly the two rows `M-ROW` declares admissible, and the restored row
is exactly the omission `M0`/`M1B` record. This is the correct repair of both findings.

**Arithmetic note.** "4 VOID + 3 UNREALIZED = 7" counts the duplicate: rows 6 and 8 are the same member
`(¬C1,¬C2,¬C3)`, so the printed table holds 2 distinct UNREALIZED members, not 3. The count lands on the right two
rows only because cutting row 8 removes the duplicate. Stated so the next reader does not inherit "3 distinct
UNREALIZED".

**Governance note.** "Directly cut the 7 invalid rows" is a *disposition*, not a deletion. The record's convention
(s9.1) is that an archived document is not edited; a retracted row is retracted by an appended disposition naming
the reason, so that a later reader can see what was removed and why. Deleting them silently would reproduce `M0`
in the other direction — a table that no longer shows what it claims to have covered.

**What the acceptance costs, and it must be said in the same breath.** Two rows cannot support a coverage claim.
§I's sentence — *"every constraint combination is rigorously evaluated"* — is now false by construction, and §IV's
"complete coverage" with it. A 2-row table is a **one-factor, two-level contrast**, not an enumeration. It is a
legitimate object; it is not the object the route was approved to be.

---

## 2. Part II — each replacement column reproduces a measured failure

This is the load-bearing objection. The four replacements are not untested ideas; three of them are quantities this
record has already computed.

### R1 — `L1` → "Wasserstein `W₁` or Hausdorff" is the measurement that produced the reversal

`M3` evaluated both, in the ambient space: `d_H = 2.550e4 m` (registered max placement), `W₁ = 1.380e4 m`
(registered mean). Normalised by `H = 1.75 m`: `d_H/H = 1.4571e4`, `W₁/H = 7.8857e3`. At `¬C1` both are **`0`
exactly**.

The column is therefore **maximal where 2D-ification is complete and zero where it never happened** — the tier's
optimum is the failure of the experiment. The proposal offers as a fix the exact quantity that generated the
finding it is meant to fix. This is not a repair; it is a re-measurement of `M3`.

### R2 — `L0` → "metric-tensor deviation / curvature scalar" is `M3` in tensor clothing, and it is collinear with R1

A deviation between the metric induced by the 3D embedding and the 2D grid metric is a monotone function of the same
placement coordinates that gave `d_H`: maximal at `C1` (`2.550e4 m` spread), zero at `¬C1`. Two consequences:

- It **re-instates `M2`'s defect**: the column is satisfied by the object that was never converted.
- It is **collinear with R1 by construction** (correlation `1.0`, not "high"), which is precisely what the
  proposal's own Part III claims to detect.

There is already an `L0` that passed admission and does not have this defect: `Q0` (fragmentation removal,
`Q0 ≥ 0.50`, hash-locked before evaluation, null passing 0 of 1, controls 6 of 6). Replacing a tier that passed a
three-part admission gate with a re-parameterisation of one that failed is a regression.

### R3 — `L2` → "KL divergence" is known to be `+∞` on this pair, and "von Neumann entropy" has no density matrix

`MR2-CLOSE` measured the pair directly: the 3D pair-distance support is `sup d₃D = 0.292062 m`, the 2D minimum site
separation is `pitch = 0.400100 m`, the supports are **disjoint**, therefore `D_KL = +∞`. Not large — infinite, at
every cell of every row. A column that is `+∞` everywhere is not a low score; it is a column with no values.

Von Neumann entropy requires a density matrix. `D2` performs no deformation (`KIN-DYN`), so no modulus, density or
constitutive response enters the mapping and the record has no state from which to build one. Any `ρ` assembled
from the canvas histogram is a function of `(M, N, σ)` — the `D-9` violation, stated below.

### R4 — `L3` → "`σ_s(ω)` / polarisation tensor" is the reopening condition, not a column

`σ_s(ω)` is `G6`/`DC2`, which `route_terminus_v1.md` §9 names as **the only thing that reopens the line**, and which
is not yet compliant (round 45: model-layer conditionally admissible). So:

- the column is `BLOCKED-ON-INPUT` at every cell today — and it is the *only* column that could carry information
  not already known, so the "computable 2×4" is at best 2×3 with the informative column blocked;
- putting it in a **column** confuses a **payload** with a **criterion**. The tier asks *"can this be read"*; `σ_s`
  answers *"what does this sheet do to light"*. The former is a predicate on the output, the latter a parameter of
  the model. This is the exact category error `D-6` made and `D-6a` withdrew in these words: *"`D-6`'s ground … is
  a category error: `δ_E` is one scalar per configuration, a site holds `(k, n)`."*

Using `σ_s` is the right instinct in the wrong slot. It belongs at `D-9` as the input that would let a site carry a
measured value — not as a column of a table that has no compliant `σ_s` to put in it.

---

## 3. Part III — the efficiency gate rejects the design it is attached to

The proposal offers `D`-efficiency with a 60% threshold as proof that the repaired matrix is information-optimal.
Applied to Part I's own design:

| model retained | design matrix | `|XᵀX|` | `D`-eff |
| --- | --- | --- | --- |
| all three factors | `C2`, `C3` constant across both rows — *this is why they were cut* | `0` (singular) | **0%** |
| `C1` only | `X = [[1,1],[1,0]]`, `XᵀX = [[2,1],[1,1]]` | `1` | `1^(1/2)/2` = **50%** |

Both are below the proposal's own 60% threshold, and no 2-run/2-parameter design can exceed 50%: it is saturated,
residual degrees of freedom `n − p = 0`.

Three further problems, in ascending order of severity:

1. **`D`-efficiency measures how well `X` identifies model coefficients.** The cells are not coefficients of a
   linear model; there is no regression. "Collinearity" between a topological invariant, a distance, an entropy and
   a response cross-section has no referent — they are different functionals, not regressors.
2. **`A`-efficiency minimises the variance of estimates.** There is no error term: the runs are deterministic
   arithmetic on registered constants, so replication returns identical numbers and `Var = 0`. A variance-based
   criterion on a deterministic computation is the same class of error as `M4`'s mutual information without an
   ensemble — and the record has already named that class (`ME3-F1`: an undefined argument, not a tolerance
   question).
3. **A saturated design cannot demonstrate anything about efficiency.** With `n = p` the statistic is fixed by the
   row count, so the 50%/0% result is not a finding about this matrix; it is arithmetic on 2.

The gate cannot "close the design-flaw objection" because it never had purchase on the object.

---

## 4. Part IV — the render depicts a process the model does not contain

"Two rows as two keyframes (3D → 2D)" treats a **counterfactual** as a **time series**. The two rows differ in `C1`
being true or false; they are not two moments. `D2` performs no deformation (`KIN-DYN`), so there is no
intermediate state to interpolate: a two-keyframe animation must invent every in-between frame, and those frames are
exactly what §VI forbids (*"no cell in the matrix may present content that contradicts established NO-GO
conclusions"*). The panel titles "metric evolution" and "entropy change" inherit the same non-existent time axis.

Two further limits, one structural and one of credit:

- **Renderability.** Rendering *this table* is fine and cheap. Rendering the *scene* is closed:
  `DEPOSIT-DICHOTOMY` fixes the gap at `16,384 = 2¹⁴` exactly (injective needs `65,415` sites per side, `4K` shows
  `0.19%`), and no scale factor exists because `sup d₃D = 0.292062 m` lies strictly inside `pitch = 0.400100 m`.
  This is a one-to-one vs many-to-one conflict, not a resolution shortfall.
- **Credit.** A figure whose inputs are declared numbers is `FL1` (`D-3`, `G1`) and may not stand in a measured
  column. It is a legitimate chart; it is not evidence about the object.

The proposal's closing claim — that this becomes "the underlying data source driving a dynamic DCC demonstration" —
therefore describes a chart of declarations. That is a real artefact, but it is the one `route_terminus` §5 already
named: a serialization, not an image.

---

## 5. The `D-9` test, applied once

`route_terminus_v1.md` `D-9`: *"New submissions are read against §2's theorem first: what quantity, other than
`(M, N)`, does your proposal put into a site? A submission that cannot answer that is answering a closed question."*

Answer for the repaired 2×4, on its `C1` row: **none.** The row's scene is the deposit; `DEPOSIT-BLIND` measured six
physically distinct objects giving **one** digest `558d30e08fd32cf6`, `I(canvas ; r₄) = 0` bits, and 10 of the
record's 12 declared parameters never reaching a site. So `Q0`, `Q1`, `Q2` computed on that row are statistics of
`(M, N, σ)`, and `MR1.6` already fixed the ceiling: *"no statistic on it can be a statement about the object."*

This is the finding that survives every row and column repair: the table is computable, and what it computes is a
statement about a **declaration**.

---

## 6. What the proposal gets right, and the one form in which it works

Four things are correct and worth keeping:

1. **The row cut and the control row.** Matches `M-ROW` exactly; the restored row is the missing half of the only
   comparison the matrix could make.
2. **The diagnosis that the defects are column-level.** `M2`–`M6` are column findings; the proposal looks in the
   right place.
3. **The instinct that the response function is where the physics is.** Correct — but as `D-9`'s reopening input,
   not as a column with nothing to fill it.
4. **The willingness to reduce to a contrast.** A 2-row table is more honest than an 8-row table with 6 dead rows,
   provided the coverage claim is withdrawn in the same document.

The one form in which all of this survives intact is the object the record already holds:

- rows stay as an axis, but as **"which violations you are buying"** — `C3` becomes a violation factor `V`, `C2`
  ceases to be a binary and becomes a declared construction, because intralayer strain is identically zero;
- columns become functions of a declared observer `θ`, because `Q3` is a function of `θ` and the record evaluated
  only `θ_eye`, where it is zero by construction;
- a cell is a **profile** `(Q0, Q1, Q2, Q3 | θ)`, never a maximum — `M6` leaves no total order (`MR1.2`);
- the price column is not an efficiency statistic but a physical price: `V`, orders of flux `Φ`, and a fingerprint
  that distinguishes "you are at this rung" from "this is an illustration".

That is `docs/specs/relaxation_ladder_v1.md`, already registered and priced. The 8 rows and the ladder are not two
proposals; they are the same table read along different axes.

---

## 7. Disposition

| part | disposition | reason |
| --- | --- | --- |
| I — row cut + restored control | **ACCEPT as `M0`/`M1B` repair** | correct rows; requires withdrawal of §I/§IV's coverage claim and a disposition record rather than deletion |
| II — `L1` → `W₁`/Hausdorff | **REJECT** | is `M3`'s own measurement: `1.4571e4 H`, `0` at `¬C1` |
| II — `L0` → metric deviation | **REJECT** | `M2` reinstated, and collinear with `L1` at `1.0` |
| II — `L2` → KL / von Neumann | **REJECT** | `D_KL = +∞` on this pair (`MR2-CLOSE`); no density matrix exists |
| II — `L3` → `σ_s(ω)` | **REJECT as column, ACCEPT as `D-9` input** | payload mistaken for criterion (`D-6a`); and the quantity is not yet compliant |
| III — `D`/`A`-efficiency gate | **REJECT** | 0% or 50% against its own 60% floor; no error term; no regression to be efficient about |
| IV — keyframe render | **REJECT as process depiction, ACCEPT as `FL1` chart** | no intermediate state exists (`KIN-DYN`); scene render closed at `2¹⁴` |

**Residual**: the proposal's `C1`-row scene carries no quantity other than `(M, N)`, so the repaired table can be
computed and cannot be about the object. Closing that gap is `G6`/`DC2` — the item `route_terminus` §9 already
named, and the item on which `RL-1` depends.

*Content generated by AI*
