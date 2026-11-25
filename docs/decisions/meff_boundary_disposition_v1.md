# Disposition of the M_eff boundary draft v0.1 — governor's rulings D-A and D-B

**Date**: 2026-11-22
**Status**: **RATIFIED.** Both rulings adopted. v0.1 superseded by `docs/specs/meff_boundary_v0_2.md`.
**Rulings**: **D-A** adopt the boundary-data / validation-evidence split. **D-B** dissolve `C_info`.
**Audit basis**: `reports/reviews/meff_boundary_v0_1_audit.md` (F1–F11), `runs/S45/meff_boundary_probe_results.txt` (Q1–Q6)
**New arithmetic**: `runs/S45/meff_disposition_checks_registration.md` → `runs/S45/meff_disposition_checks_results.txt` (D1–D5, 5/5 PASS)
**Ratified instrument**: `governor decision statement, 2026-11-22 ("submit for final decision" follow-up)` — conclusions adopted; two corrections and one added condition recorded below.

---

## 1. The two rulings

| ID | Ruling | Adopted | Executor's position |
| --- | --- | --- | --- |
| **D-A** | Split **boundary data** from **validation evidence**; the S3→S4 branch may supply the former to the S0→S2 solve, never the latter | **YES**, no objection to the substance | **One condition added** (§2.3). Without it the split is necessary but not sufficient for what it claims to achieve. |
| **D-B** | **Dissolve** `C_info` rather than repair it: injectivity → `ME1`, entropy change → reportable budget, threshold withdrawn | **YES** | **Two corrections** (§3.4) — of terminology and of attribution — plus the arithmetic that makes the dissolution provably content-preserving (§3.2). |

Both rulings are **governance** decisions. Neither changes a number, a threshold in force, or a verdict.
`C_info` was never in force (v0.1 was "REGISTERED — AUDIT OPEN, not citable"), so D-B retires a draft
clause rather than removing a live gate.

---

## 2. Decision D-A — boundary data is not evidence

### 2.1 The substance

Ledger §9 (adopted earlier the same day) said branch products *"may not be cited as evidence for the
chain"*. That sentence was too blunt: it also forbade the one use that is unavoidable. The S2 solve is a
finite-domain Cauchy problem for a strongly hyperbolic system; it terminates at an outer boundary and
**requires data there**. Refusing branch-produced data makes S2 unsolvable, and a rule that makes the
next stage impossible is not a rule, it is a stop order.

The correct distinction, now ratified:

| Category | Admissible into | Content | Reason |
| --- | --- | --- | --- |
| **Boundary data** | the S0→S2 **solve** | numbers supplied as outer / asymptotic / Dirichlet data on a declared surface | closure of a well-posed problem; without it there is no problem to solve |
| **Validation evidence** | nothing in the S0→S2 **ledger** | any use of a branch product to argue that 2D-ification, or the chain, is *supported* | would be a branch scoring the chain it is not part of |

### 2.2 Where the governor's reasoning is correct, and where it overstates

**Correct.** "The branch may only supply input conditions and must never participate in scoring the
results" is exactly the right line, and it is what makes the ledger answerable to its own question. The
independence argument is sound.

**Overstated — well-posedness is not obtained from the data.** The ruling's first justification says the
split "ensures the well-posedness of the solve". It does not, and the distinction matters:

- Well-posedness (existence, uniqueness, continuous dependence) is a property of the triple
  *(operator, boundary type, function space)*. It is **independent of the values** supplied.
- Supplying *some* numbers at the boundary guarantees only that a closure was chosen. A closure can be
  ill-posed: for the elliptic CMC problem of the R4 round, a Neumann condition on `ψ` at the inner cut
  gave a singular Jacobian in exactly this way; the fix was a Robin row, i.e. a change of *type*.
- Therefore the correct statement is: **the split permits a well-posed closure to be specified, and
  obliges the specification to declare its type. Well-posedness must then be established for that type,
  and cannot be established by the provenance of the values.**

This is not pedantry. If "branch data ⇒ well-posed" were accepted, a later round could cite the split to
skip the well-posedness demonstration altogether.

### 2.3 The added condition — without it, the split does not achieve its purpose

The split severs **citation** circularity. It does not sever **determination** circularity, and the
governor's stated goal ("fundamentally eliminating the self-proving trap") requires both.

**The residual hazard.** Take the CMC problem on a finite annulus. A Dirichlet condition on `ψ` over the
*entire* outer boundary, plus regularity at the inner cut, fixes the interior **uniquely**. If those
Dirichlet values come from the branch, then S2's interior is a *consequence* of the branch's numbers. Any
agreement between S2 and the branch is then a theorem about the data, not a test of the model. The
provenance tag would read `BOUNDARY-INPUT` and the citation rule would be formally satisfied while the
result is exactly as circular as before — circularity would have moved from the citation graph into the
boundary-value problem.

**Condition (registered as `PROV-3` in `docs/conventions/provenance_tags_v1.md`).** Boundary data must be:

1. **typed** — field, surface, and type (Dirichlet / Neumann / Robin / asymptotic), with the regularity
   assumed. A number with no type is not boundary data;
2. **non-over-determining** — it must not fix more interior degrees of freedom than the run purports to
   determine. Declared as a count: `n_data` vs `n_dof_predicted`, with the surplus stated. If `n_data`
   determines the interior entirely, the run is a *reconstruction*, and must be labelled one;
3. **derivation-independent** — obtained without assuming C1 or C2 (column conservation, zero intralayer
   strain), since those are the hypotheses under test. An exact solution, an asymptotic expansion at
   infinity, or a full-3D calculation that nowhere imposes a column structure all qualify; a
   2D-reduced calculation does not.

And the reporting rule: **a solve that uses branch data reports "solution given data D", never
"confirmation of D".** Its result is conditional, and the conditionality survives into every downstream
citation.

### 2.4 What D-A changes in force

- Ledger §9's blunt sentence is superseded in letter, preserved in intent (already amended; now ratified).
- Every run product must carry a `PROVENANCE:` line (§5). Grandfathered: products dated before
  2026-11-22, tagged by the linter as `LEGACY-UNTAGGED`, not retro-edited (§9.1).
- **Nothing else.** D-A licenses no branch product as evidence; it licenses branch *numbers* as *inputs*.

---

## 3. Decision D-B — dissolve `C_info`

### 3.1 The content map (what `C_info` was carrying)

`C_info: ΔH = H_3D − H_2D ≤ δ_info`, with the gloss "the lost third-dimension information can be
reconstructed losslessly or with minimal loss".

| Component | Disposition | Carrier after dissolution |
| --- | --- | --- |
| Injectivity / single-valuedness (`ΔH = 0` case) | **transferred** | **`ME1`** — geometric, dimensionless, testable on any density field |
| The `ΔH` magnitude ("how much is lost") | **demoted to a reportable budget** | no gate; reported with mandatory fields (§5.2) |
| The `δ_info` **threshold** | **withdrawn** | nothing — an arbitrary constant with no physical derivation |
| "Lossless reconstruction" | **withdrawn as a consequence** | it was never a consequence of the inequality (§3.3) |

### 3.2 The arithmetic that makes this provably content-preserving

The governor's argument was qualitative. Five checks (`D1`–`D5`, registered before running) put it on
arithmetic. The decisive one is **D5**, an exhaustive enumeration of all 256 configurations of a
`2×2×2` lattice under the naive fixed-length code:

```
ΔH = N_overlap · log2 V          exactly (max error 0.00e+00 over 256 configs)
ΔH = 0  ⟺  injective            for all 256 configs (0 violations)
```

So the budget's **zero set is exactly injectivity**. Dissolving `C_info` therefore discards only the
choice of code (`log2 V` per overlap) and the choice of resolution — neither of which is physical —
and discards nothing that `ME1` does not carry. Had `D5` failed, this record would have withdrawn the
dissolution recommendation instead.

**D3 gives a sharper statement than the audit had.** `A_crit = δ_info/(ΔH/A)` is exactly linear in
`δ_info` (log–log slope `1.000000000000`). Therefore:

> `C_info`, as written, **is exactly** the statement `A_⊥ ≤ A_crit(δ_info, res)`. It is an upper bound on
> the object's base **area**. Its only non-injectivity content is "the object must be small enough".

That is a cleaner statement of the defect than "unattainable by 8.7 decades", and it is what justifies
"dissolve rather than repair": there is nothing to repair, because the object being constrained is the
object's size, not its fidelity. Repairing would mean choosing `δ_info` to make a size cut tolerable,
which is the "artificially adjusting thresholds" failure the governor named.

**D2** confirms the size dependence is unbounded (slope `1.000000000000` in `log A`), so no
size-independent `δ_info` exists for any object family that varies in size.

### 3.3 One terminology correction (this project cares about the difference)

The ruling says `C_info` "is logically circular". It is not circular — it is a **non sequitur with a
hidden premise**. The inequality presupposes `z = z(x_i)` (graph-ness), and the conclusion
"reconstructable" follows from that presupposition, not from the entropy bound. Circularity would mean
using the conclusion to establish the premise; what happens here is that the premise is supplied silently
by the notation. The distinction is operational: a circular argument cannot be rescued by weakening the
bound, whereas a hidden premise can — by naming it. Which is exactly what `ME1` does.

### 3.4 Two attribution corrections

1. **The carrier is `ME1`, not `M1`, and the lifetime constraint is `ME5`, not `M5`.** Per
   `docs/conventions/symbol_registry.md` §3 and §7, `M1–M5` is unavailable: `M` is mass (`M(R)`,
   `M_STEP`) and `M4` is the external-review gate. The set is `ME1–ME5`.
2. **Injectivity is not "covered by a more fundamental geometric constraint" — it is a *new* constraint.**
   None of v0.1's four constraints tests single-valuedness; `C_geo` and `C_info` both *assume* it
   (audit F1). So the ruling's premise is right but its wording inverts the dependency: `ME1` does not
   exist until this disposition creates it. Recorded because "its content is already covered" would
   otherwise be cited later as evidence that v0.1 was safer than it was.

### 3.5 The digit in "8 orders of magnitude"

`D1` measured the shortfall at `δ_info = 1 Tbit` across the declared resolution pair: **7.16 decades**
at molecular resolution (0.3 nm), **8.70 decades** at atomic (`a₀`) — a spread of 1.54 decades. The
governor's "8 orders" is the correct *order*, at the stricter of the two resolutions. The robust
statement is D3's area cut; the digit is conditional and must be quoted with `(res, δ_info, A_⊥)`.

---

## 4. State of the constraint set after this disposition

| v0.1 clause | State | Now |
| --- | --- | --- |
| `C_geo` | **RETIRED** | `ME2` (slope at declared sampling scale) + `ME1` |
| `C_phys` | **RETIRED** | `ME3` (positive-definite perpendicular energy fraction) |
| `C_info` | **DISSOLVED** (D-B) | `ME1` (injectivity) + reportable budget (§5.2) |
| `C_top` | **RETIRED** | `ME4` (fragment census) |
| — | **NEW** | `ME1` injectivity, `ME5` lifetime |

Adopted constraint set: **`ME1`–`ME5`**, registered in `docs/specs/meff_boundary_v0_2.md`.
The labels `C_geo/C_phys/C_info/C_top` are **retired** and may not be reintroduced (registry R4: a
subscript cannot rescue a letter). Any future reference to them is historical.

## 5. The dismantled gate, and how it is prevented from returning

### 5.1 The rule

**`BUDGET-1`.** `ΔH` may be reported. It may **never** appear in a PASS/FAIL verdict, a gate row, a
threshold, or an acceptance criterion — not in v0.2, not in any later revision, not "for information
only" inside a gate table. Promotion back to a gate requires a new governor decision recorded against
this document by ID.

Why the rule is needed at all: a demoted metric that keeps its number in a table keeps its authority. The
next round would read `ΔH = 4.99e20 bit` in a results file and re-derive the threshold from it. The
budget is retained precisely so that its *magnitude* stays visible — so the prohibition has to be
explicit rather than achieved by deleting it.

### 5.2 Mandatory fields for any reported `ΔH`

A bare `ΔH` is undefined (a deterministic classical state has zero Shannon entropy; what is meant is a
description length). Any report must declare:

| Field | Why |
| --- | --- |
| lateral resolution `ℓ_lat` | `ΔH/A ∝ ℓ_lat^-2` (D1) — the dominant sensitivity |
| depth resolution `Δz` | enters through `log2(H/Δz)` |
| base area `A_⊥` | `ΔH` is extensive (D2); a bare `ΔH` is uninterpretable without it |
| code | the per-point cost, e.g. `log2 V` for the naive fixed-length code |
| overlap count `N_ov` | the physical part; `ΔH = N_ov·log2 V` (D5), so this is the informative number |

Practically: **report `N_ov` and the overlap measure `μ_ov` (which is `ME1`), and report `ΔH` only as a
derived convenience.**

---

## 6. Provenance tags — making D-A enforceable

Specified in `docs/conventions/provenance_tags_v1.md`; enforced by `src/common/provenance_lint.py`
(report, exit 0, per the `symbol_lint` precedent). Summary:

| Tag | Meaning |
| --- | --- |
| `PROVENANCE: CHAIN-EVIDENCE` | produced in the S0→S2 chain; admissible in the validation ledger |
| `PROVENANCE: BOUNDARY-INPUT` | produced by the S3→S4 branch; admissible only as typed boundary data |
| `PROVENANCE: NEITHER` | definitional / arithmetic / audit products |

Hard rule: **a product of the branch may not carry `CHAIN-EVIDENCE`.** The linter flags any file under a
branch directory (`runs/S45`, future `runs/S4*`) whose tag says otherwise, and flags any
`CHAIN-EVIDENCE` product that cites a `BOUNDARY-INPUT` product as its support.

## 7. Consequences for the ladder

- **No stage moves.** S0 remains the first deliverable, S0→S2 remains the validation chain, S3→S4 the
  relaxation branch.
- **S2's solvability is now explicitly licensed** — it may take branch boundary data under `PROV-3`.
  This removes a blocker that would otherwise have appeared at S2 and been resolved ad hoc.
- **L3's price is now a gate, not a sentence.** `ME5` (`τ_exp ≤ √2 L/c`) is the first constraint in the
  branch that *binds on time*, and its consequence — no faithful reflected-light frame of a surviving
  sheet — must appear on every L3 product.
- `C3` is untouched. Its in-action NO-GO is parameter-independent and no `ME` tolerance reaches it.

## 8. What this disposition does not do

- It does not license any visibility conclusion; §11.1/§11.2 of the roadmap are unchanged.
- It does not adopt `δ` values for `ME2`/`ME3`/`ME4`. Those are registered in v0.2 as **OPEN with
  declared measurement protocols**; an unregistered δ is not a threshold.
- It does not make the branch a validation baseline, and it does not reopen C1's identity status or C2's
  interlayer failure.
- It does not re-open the question of whether `M_eff` is a useful object. The architecture was accepted
  by the audit and is unchanged.

## 9. Open items created by this disposition

| # | Item | Owner |
| --- | --- | --- |
| O1 | `ME3`'s δ_phys needs an independent basis — `WEIGHT = 0.05` is a numerics matching factor and must not be inherited (audit F5) | next round |
| O2 | `ME4` census must be re-derived if the fragment count changes; currently `8.12e9` layers / `1.18e10` plates | census owner |
| O3 | The `L` three-way label collision (fidelity / optics / R2-D) remains staged, not renamed | governor |
| O4 | `ME5`'s `L` — for a non-spherical object, which `L` governs the tear? Registered as "the object's largest extent" pending a derivation | next round |
| O5 | `C4` remains reserved and unused; no `ME` item may be promoted into it (it is a constraint slot, not a branch slot) | registry |

---

## 10. Declined re-specification (2026-11-22, after adoption)

A submission arrived the same day proposing a **different** `ME1`–`ME5` and asking whether it was "done". It
was **declined** and registered verbatim at `docs/specs/meff_boundary_v0_2_alt_definitions_DECLINED.md`;
assessment in `reports/reviews/meff_boundary_alt_definitions_review.md` (`V1`–`V6`, `G1`–`G5`), probe
`runs/S45/meff_alt_definitions_results.txt` (6/6).

Summary, recorded here because it bears directly on this ruling:

| Proposed clause | Why declined |
| --- | --- |
| `ME1` = `Φ(p)=Φ(q) ⟺ p=q` on all of `ℳ` | Violated by **every** closed object: `μ_ov(solid ball) = 1.000000`, `μ_ov(converted plate) = 0`. The "excluding singularities" clause would absorb the entire object |
| `ME2` = conserved current from `δS_eff/δφ = 0` | It is the Euler–Lagrange equation (vacuous as a constraint), and it is a **matter-sector** predicate — the `C` domain. `S1` forbids it in `ME` |
| `ME3` = `ΔS_vN ≤ κ·A_eff` | Algebraically `C_info` (rel. diff `0.000e+00`, same `A_crit = 8.013e-11 m²`); reverses **D-B** and violates `BUDGET-1`; in general it is a bound on object height (`H_max = 3.0e-17 m`) |
| `ME4` = `dχ/dt = 0` "except at phase transitions" | The falsified `C_top`, plus an escape clause making it unfalsifiable (`1000/1000` adversarial cases accommodated) |
| `ME5` = `\|∂ℳ_t/∂τ\| ≤ Λ_max` | **Directionally inverted**: a rate cap bounds duration from *below*. Satisfied by a configuration `1.06e12`× too slow to photograph |

Two items were **accepted** from the submission: rule **S5** (scope qualifier `Gate:M4` / `Constraint:ME4`,
generalised to all `M` families) and lint rule **F** over the `ME` namespace. Implementing F also found that
`M1`–`M4` already has **five** owners, not the two the submission assumed — registered as registry §2a.

**No adopted definition changed.** The submission and this ruling's §4 table are consistent: the retired
`C_*` names stay retired, and no proposed clause may be registered under them.

---

*Content generated by AI*
