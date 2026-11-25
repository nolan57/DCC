# Disposition — the 8×4 matrix route, after the return

**Status**: **DISPOSITION RECORD** (executor, 2026-11-23, round 53). Terminal state **CLOSED-NO-GO**.
**Object**: `docs/decisions/exhaustive_matrix_route_v1.md` — registered PROPOSED 2026-11-22, returned 2026-11-23
(`PG-02`).
**Basis**: `reports/reviews/exhaustive_matrix_route_v1_audit.md` (`M0`–`M8`; `P1`–`P7` all confirmed) and its
product `runs/MATRIX/matrix_audit_results.txt`.
**Carries**: no approval block — §0 says why, and what checks it instead.
**Answers**: `RQ-02`.

---

## 0. No approval block — and the table that earns that

This note decides nothing that is not already decided. That is a claim a reader must be able to test, so every
normative sentence in it is listed here with its source. A sentence added later without a source is not binding.

| sentence in this note | source |
| --- | --- |
| "the route is returned, not ratified" | `PG-02` mark, `exhaustive_matrix_route_v1.md` §4 (line 240) |
| "the enumeration was never a set of eight" | audit `M0`: 8 printed rows, 7 distinct, 1 duplicate, 1 absent |
| "four rows have no physical instantiation" | audit `M1a`: `C3` is a parameter-independent NO-GO |
| "two further rows have no instantiation" | audit `M1b`: `C2` is a theorem of the mechanism (`front_sweep_v1` §2 step ②) |
| "the remaining two rows' cells are not fillable" | audit `M2`–`M6`; the cell quantity needs a total order that does not exist |
| "the tiers measure the wrong direction" | audit §4: every tier writes the original on the right-hand side |
| "the five open items stay where they were" | audit §5 and §6 item 6; `exhaustive_matrix_route_v1.md` §2.3 |
| "the coverage claim is withdrawn" | §VI of the object ("every combination… complete coverage") against `M0`+`M1` |
| "phased v2 is not superseded" | `PG-02`: a document never in force supersedes nothing |
| "matrix v2 is a product" | `matrix_v2_status_reading_v1.md` (round 52) |
| "the frame at `PG-03` governs, with the ladder as its price table" | `relaxation_frame_v1.md` §9, marked |

Eleven sentences, eleven sources, zero new decisions. **What checks this file is that table**, in place of a mark:
a mark would ask the governor to agree that a return they ordered has been recorded, which is not a decision — it
is a receipt.

**What this note deliberately does not decide**, and cannot: whether the 8×4 may be revived (that is `PG-02`'s
reverse-on clause, and it is a governor instruction or nothing); whether a future route may be built on the same
instrument; whether `RQ-11`'s terminal answer may cite any of these numbers. Those stay open and stay marked as
open.

---

## 1. The disposition in one paragraph

The route is **returned**, so its matrix was never a governing instrument and no cell of it was ever required; its
32 nominal cells are disposed of in §3 — **16 `VOID`** (a row with no physical instantiation) and **16
`UNREALIZED`** (a cell whose required quantity does not exist: 8 because the row has no instantiation either, 8
because the column measures the wrong direction) — and the **coverage claim is withdrawn** (§4) because the
printed table was never a set of eight; **phased v2 is not superseded** (§7) because a returned document was never
in force; and the instrument that governs the project is named in §8 so this note cannot be read as installing a
successor route of its own.

---

## 2. The enumeration — eight distinct rows, and the two facts about the table

The printed table (`exhaustive_matrix_route_v1.md` §IV) lists eight rows containing **seven distinct members**:
rows 6 and 8 are both `¬C1 ∧ ¬C2 ∧ ¬C3` (row 8 labelled "Zero"), and **`¬C1 ∧ C2 ∧ ¬C3` is absent** (`M0`).

The restoration is the whole point of `M0`'s cheapness: the omitted row is **one of the two rows that survive
`M1`**, so the single comparison the matrix could make is the one the table dropped. Written canonically, with the
printed position kept so the transcription stays auditable:

| # | row (`C1 C2 C3`) | in the printed table | instantiation |
| --- | --- | --- | --- |
| 1 | `C1 ∧ C2 ∧ C3` (Full) | row 1 | none — `C3` is a NO-GO (`M1a`) |
| 2 | `C1 ∧ C2 ∧ ¬C3` | row 2 | **yes** — the only row §VII.1 asks to fill |
| 3 | `C1 ∧ ¬C2 ∧ C3` | row 3 | none, twice (`M1a`, `M1b`) |
| 4 | `C1 ∧ ¬C2 ∧ ¬C3` | row 5 | none — `¬C2` has no construction (`M1b`) |
| 5 | `¬C1 ∧ C2 ∧ C3` | row 4 | none — `C3` (`M1a`) |
| 6 | `¬C1 ∧ C2 ∧ ¬C3` | **absent — restored here** | yes, and it is the control (`¬C1` = no 2D-ification) |
| 7 | `¬C1 ∧ ¬C2 ∧ C3` | row 7 | none, twice |
| 8 | `¬C1 ∧ ¬C2 ∧ ¬C3` (Zero) | rows 6 **and** 8 | none — `¬C2` (`M1b`) |

Two facts are kept rather than repaired, because they are facts about the document under disposal and not defects
of the transcription: the duplicate row `M0`, and the label "Zero" attached to a row that has no instantiation at
all. Repairing the table in this note would erase the evidence that the enumeration was assembled by hand.

The pre-filter (`M1`) is what the object never states: **`C3` cannot be satisfied** (`κ(ρ+p_x) = −γ(γ+h) < 0` for
all `h, γ > 0` — a NO-GO that is *parameter-independent*, so it is not a constraint one can pay to hold), and
**`¬C2` cannot be produced** (`front_sweep_v1` §2 step ② is an `(x,y)` identity per layer, so intralayer strain is
identically zero for every conversion — `C2` is a theorem of the mechanism, not a switch). "Relaxing `C2`", one of
the two axes of the proposed matrix, therefore has no meaning.

---

## 3. The 32 cells

Legend. **`VOID`** — the row has no physical instantiation, so the cell has no subject; §VI of the object forbids
presenting content on it. **`U-1`** — `UNREALIZED`, no instantiation: same defect as `VOID` reached through `¬C2`
rather than through `C3`, and labelled separately because the audit labelled it separately. **`U-2`** —
`UNREALIZED`, subject exists but the cell's required quantity ("max distinguishability", a point on a total order
`L0 < L1 < L2 < L3`) does not: `U-2a` the column quantity is empty or undefined, `U-2b` the row is the control, so
the quantity's subject is the absence of the experiment.

| # | row | `L0` | `L1` | `L2` | `L3` | reason, per cell |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `C1 C2 C3` | VOID | VOID | VOID | VOID | `M1a` |
| 2 | `C1 C2 ¬C3` | U-2a | U-2a | U-2a | U-2a | `M2` / `M3` / `M4` / `M5` respectively |
| 3 | `C1 ¬C2 C3` | VOID | VOID | VOID | VOID | `M1a` (and `M1b`) |
| 4 | `C1 ¬C2 ¬C3` | U-1 | U-1 | U-1 | U-1 | `M1b` |
| 5 | `¬C1 C2 C3` | VOID | VOID | VOID | VOID | `M1a` |
| 6 | `¬C1 C2 ¬C3` | U-2b | U-2b | U-2b | U-2b | `M6`: the control row |
| 7 | `¬C1 ¬C2 C3` | VOID | VOID | VOID | VOID | `M1a` (and `M1b`) |
| 8 | `¬C1 ¬C2 ¬C3` | U-1 | U-1 | U-1 | U-1 | `M1b` |

**Tally: 16 `VOID` + 8 `U-1` + 8 `U-2` = 32.** `VOID` and `U-1` are the same verdict reached by two different
constraints; the distinction is kept because the reasons are not interchangeable — `C3` is forbidden by the action,
`C2` is unavailable in the mechanism.

### 3.1 The two rows with a subject, and what the record holds for them

`U-2` is not a claim that nothing is known. It is a claim that what is known is not a cell of this matrix. Both
rows were measured by the audit, and the numbers are recorded here as **measurements of the scene**, not as
matrix entries:

| row | `L0` | `L1` | `L2` | `L3` |
| --- | --- | --- | --- | --- |
| `C1 C2 ¬C3` (2) | `χ` ratio `1.18e10` (`log₁₀ = 10.07`) — **fails by ten orders** | `d_H = 1.457e4 H`, `W₁ = 7.886e3 H` | undefined without an ensemble; `0` bits for the single realization | empty on two grounds |
| `¬C1 C2 ¬C3` (6) | `χ` ratio `1` — passes | `0.0000` exact | `0` bits | passes, on an object never converted |

Two of the four columns are already fatal before any threshold is chosen: `L2` has no input (no ensemble over
structures is declared, and with one realization `H(Scene) = 0`), and `L3` at `C1` has no exposure budget —
`2H/c = 1.1675e-8 s` against `t_rip(1.75 m) = 8.2553e-9 s`, a factor `√2` short — and no flux:
`7.8747e23` photons m⁻² per frame needed against `2.2900e13` available, a shortfall of **`3.44e10` (10.5 orders)**
at the detector threshold, before the eye's own ~90 photons, and in the channel `L3` forbids.

---

## 4. The coverage claim, withdrawn

> **The coverage claim is withdrawn: the route did not enumerate a set of eight combinations, and four of the
> seven it did print have no physical instantiation, so no reading of this table can report coverage of anything.**

The arithmetic behind that sentence, in one line: **8 printed → 7 distinct → 1 duplicate (`M0`) → 1 absent
(`M0`) → 4 `VOID` (`M1a`) → 2 `U-1` (`M1b`) → 2 with a subject → 1 pair, differing only in `C1`, and the pair is
the one the table dropped.**

The claim fails on its own words twice over. §V demands *"complete coverage"* and §IV asserts `2³ = 8`; the table
supplies neither (it has eight rows, which is not the same thing). And §VI forbids presenting content that
contradicts an established NO-GO — which forbids content on **half the rows**, including row 1 "Full", the row
§VII.1 asks to fill first.

---

## 5. What the matrix was actually measuring, since the disposal should record the reason and not only the verdict

The four tiers, written as the object writes them, all put the original on the right-hand side:

```
L0 :  invariants(scene) = invariants(original)          L2 :  I(scene ; original) >= I_min
L1 :  dist(scene, original) <= eps                      L3 :  appearance(scene) ~ appearance(original)
```

The registered mechanism is `8.12e9` SE(2) rigid translations, "none of which is a deformation"
(`front_sweep_v1` §2). A map that is not a deformation cannot preserve connectivity, metric proximity or optical
appearance — so **0 of 4 tiers increase with 2D-ification** (`M6`): three decrease and one is flat.

That is why the cells cannot be filled even in the two rows with a subject: the column asks "how much of the
original survives", and the answer is known from the theorem before any measurement — the matrix would be
reporting the premise as a finding. The direction that has content is the opposite one, *recoverability given the
conversion law*, and it is already the object of `docs/specs/intrinsic_structure_tiers_v1.md` (`Q0`–`Q3`, admitted
4/4) and of the ladder. **The 8×4 was not badly calibrated; it was asking the other question.**

---

## 6. What the return does not answer

Returning a route does not answer the questions the route was blocked on (`exhaustive_matrix_route_v1.md` §2.3;
audit §5, §6 item 6). All five stay exactly where they were, and this note is not allowed to close them:

| item | state after the return |
| --- | --- |
| `GD6` — what `φ` denotes in `ME3` | **OPEN**; `ME3-F1` stays BLOCKED. Phase 3 disappearing is not an answer |
| `GD9` — the route's objective function | **OPEN**. The object answered it by fiat ("maximum tier per cell"); `M6` shows no total order is compatible with the measured signs, so the fiat does not survive the disposal |
| `GD7` — `FL` means faithfulness to the eye | CLOSED, measured. Note kept: `L3` is a **stricter predicate** than `FL3` (it excludes the faithful absence), an undeclared substitution that is what made `L3 ∧ C1` empty |
| `GD8` — `2L/c`, written `D = L` | CLOSED. Untouched; `L3`'s timing ground rests on it and `D = L` is the most favourable case, so the ground holds *a fortiori* |
| `EN-BOUND` | survives unchanged — it is the executable form of §V's non-introduction clause, which the object kept |

---

## 7. Phased v2 is not superseded

The object's §VII.3 asked to be registered "superseding the Phased Constraint Relaxation route". `PG-02` returned
it, so **the supersession never occurred**: `docs/decisions/phased_relaxation_route_v2.md` and
`docs/decisions/staged_relaxation_visual_route_v1.md` remain in force as they were, and no sentence in this
disposition supersedes them either — an executor note has no such power, and `PG-03`'s mark sits on the relaxation
frame, not on a route replacing them by implication.

This is worth stating flatly because it is the item most easily got wrong by omission: the route that was returned
is the one that would have replaced them, so **returning it is the strongest possible protection of them.**

---

## 8. What does govern — named, so this note cannot install a successor by silence

| layer | document | type | why it is the one |
| --- | --- | --- | --- |
| route | `docs/decisions/relaxation_frame_v1.md` §9, marked `PG-03` (*Select Path A*) | **governing** | the only marked statement about what may be built next |
| price table | `docs/specs/relaxation_ladder_v1.md` §4 | governing via the frame | rungs `RL-0`…`RL-6` with `V`, `Φ`, `B`; erratum `E3`: cheapest path `RL-1 + RL-2` |
| instrument | `docs/specs/intrinsic_structure_tiers_v1.md` | admitted 4/4, thresholds hash-locked | `Q0`–`Q3` with locked bars; `Q3` carries `θ` |
| product | `docs/specs/matrix_v2_spec_v1.md` + `matrix_v2.py` / `matrix_v2r.py` | **product** (`matrix_v2_status_reading_v1.md`) | 26 canonical, 11 content, 8.6:1; citable as evidence, not as authority |
| disposed | `docs/decisions/exhaustive_matrix_route_v1.md` | **returned** | this note |

The chain has no gap and no successor matrix route: the 8×4 is disposed, and matrix v2 is not its replacement but
its *successor as a product*. A reader looking for "the matrix that governs" will not find one, and that is the
correct state, not a missing document.

---

## 9. The numbers this note borrows are prices, not reasons

Under `matrix_v2_status_reading_v1.md` §4 rule 3, every number quoted above is a **measurement of the scene**, and
none of them authorises anything:

| number | what it is | what it is not |
| --- | --- | --- |
| `1.18e10`, `log₁₀ 10.07` | connectivity ratio at `C1` (`M2`) | not a threshold, not a verdict on the conversion |
| `1.457e4 H`, `7.886e3 H` | `d_H`, `W₁` of the registered layout (`M3`) | not the layout's information cost — the audit withdrew that charge itself |
| `3.44e10`, `10.5` orders | flux shortfall inside `t_rip` (`M5`) | not a claim that no channel exists; `RL-0`/`RL-1` are about other channels |
| `0 of 4` | the direction of the tier axis (`M6`) | not a statement about the deposit — the deposit is not in this matrix at all |

---

## 10. Registration, does not buy, reversal

**Registration**: object `docs/decisions/exhaustive_matrix_route_v1.md` (§1 verbatim, §4 block at line 240, §5
governor mark); audit `reports/reviews/exhaustive_matrix_route_v1_audit.md`; audit product
`runs/MATRIX/matrix_audit_results.txt`; this note, entered in `runs/PROGRAM/round_ledger.jsonl` at round 53
(`RQ-02`, `CLOSED-NO-GO`). If the ledger record is missing, this file is a draft and nothing in it binds.

**Does not buy.** That the 8×4's *objective* was wrong — it was, and the salvageable part of it already lives in
`tier_admission_v1.md` (admitted 4/4) and in the ladder. That the route is now forbidden — it is only *not in
force*, and one governor instruction can revive it. That the numbers in §3.1 are correct as physics — they are
arithmetic on registered constants, which is exactly what the audit established and no more.

**Reversal**: `PG-02`'s reverse-on clause — "a governor instruction to revive the coverage claim". Consequence if
taken: this note becomes `SUPERSEDED` in one line, the revived route needs its own approval block *and* the six
amendments of audit §6, and no cell disposed here may be cited as filled without a new registration. The revival is
cheap, which is deliberate: a disposition that were hard to reverse would be a policy.

---

*Content generated by AI*
