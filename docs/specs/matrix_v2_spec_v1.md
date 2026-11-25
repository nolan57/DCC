# Matrix v2 — reconstructing the 8×4 so that it computes, falsifies and renders

**Status**: **DESIGN PROPOSAL** (executor, 2026-11-23). Supersedes nothing; it is a construction offered to the
record, and it may not be cited as authority until a governor ruling exists.
**Replaces (as an instrument)**: the cell semantics of `docs/decisions/exhaustive_matrix_route_v1.md` §IV — *not*
its row enumeration, which is kept verbatim including its duplicate, because `M0` is a fact about the table and
quietly repairing it would erase the fact.
**Uses**: `docs/specs/intrinsic_structure_tiers_v1.md` (columns, unchanged, admitted 4/4),
`docs/specs/relaxation_ladder_v1.md` (rungs), `docs/decisions/scifi_boundary_v1.md` (the two hard knobs).
**Product**: `src/route/matrix_v2.py` → `runs/MATRIX2/matrix_v2_results.txt`.
**Pre-registration**: `runs/MATRIX2/matrix_v2_registration.md` (written before the code).

---

## 0. The design decision, and the number that forces it

The nominal object is 8 × 4 = 32 cells; with the rung axis it is 8 × 4 × 7 = 224. Neither number is the size of
anything. The reconstruction's first duty is therefore not to fill cells but to **state the rank**, because the
rank is what the 32-cell claim got wrong:

| axis | nominal | effective | why |
| --- | --- | --- | --- |
| rows | 8 | **2** | only `C1` yields a 2D field; among `C1` rows only `C2` changes the scene (severed vs bonded); `C3` is column-invisible — it changes the *price*, not the scene |
| columns | 4 | **3 + 1** | `Q0`, `Q1`, `Q2` are observer-independent; only `Q3` contains `θ` |
| rungs | 7 | **1** | `RL-1`…`RL-6` move contrast, exposure and observer — all of which enter only through `Q3` |

So 224 nominal entries collapse to **20 canonical ones**, and 9 of those carry a value or a prediction today
(the count was registered as 8 and corrected to 9 by the program; see the registration's erratum `E1`).
That compression is the deliverable. A reconstruction that reports 224 cells is reporting the same information
twenty-eight times.

---

## 1. Three axes, three budgets

| axis | what it is | unit of cost |
| --- | --- | --- |
| **row** | *physics budget* — which constraints you pay to hold | a violation factor `V` or a missing model |
| **column** | *question* — which admitted tier you ask | none; the tier is a predicate with a locked threshold |
| **rung** | *measurement budget* — what you spend to see it, from strict theory to the hard-SF boundary | `Φ`, orders of flux |

A cell is therefore a **two-budget** statement, and that is why it cannot be a maximum: `MR1.2` already fixed that
no total order on `L0…L3` exists (`M6`). The cell carries a profile plus the cheapest rung at which the profile
passes, plus what that rung costs.

---

## 2. Row typing — a rule, not an editorial judgement

The original table typed rows by *whether they had been coded*. That is why four were `VOID` and three
`UNREALIZED`: a bookkeeping status, not a physical one. v2 types a row by **which kind of obstacle it meets**, and
the three kinds have three different prices. This is the whole repair of `M1`.

| constraint form | obstacle class | price | source |
| --- | --- | --- | --- |
| `C1` (converted) | **SWITCH** | 0 — this is the experiment | — |
| `¬C1` (not converted) | **NO-FIELD** | no 2D field exists ⇒ every column `NO-SCENE`, not `PASS` | `Q0`–`Q3` are functions of a 2D field |
| `¬C2` (intralayer strain allowed) | **MISSING MODEL** | one constitutive law (a modulus / body `σ`); `KIN-DYN` supplies none | `route_terminus` §6 |
| `C3` (weak preservation asserted) | **HARD KNOB** | `R2`: weak suppression `≥ 10⁵` — called non-negotiable | `scifi_boundary_v1` §1 |

The distinction between the last two is the finding the original matrix could not make: **`¬C2` is not forbidden,
it is merely unmodelled**; `C3` is forbidden. The audit collapsed both into "cannot be instantiated", which is true
of the table and false of the physics.

Typing the eight printed rows (verbatim, duplicate included):

| # | combination | field | scene | obstacle | price | class |
| --- | --- | --- | --- | --- | --- | --- |
| `R1` | `C1∧C2∧C3` | yes | severed | `C3` | `R2` knob (`≥10⁵`) | PRICED |
| `R2` | `C1∧C2∧¬C3` | yes | **severed** | — | **0** | **STRICT** |
| `R3` | `C1∧¬C2∧C3` | yes | bonded | `C3` + modulus | `R2` knob + 1 law | PRICED |
| `R4` | `¬C1∧C2∧C3` | no | — | `¬C1` (+`C3`, moot) | — | NO-SCENE |
| `R5` | `C1∧¬C2∧¬C3` | yes | **bonded** | modulus only | **1 constitutive law** | **LIVE** |
| `R6` | `¬C1∧¬C2∧¬C3` | no | — | `¬C1` | — | NO-SCENE |
| `R7` | `¬C1∧¬C2∧C3` | no | — | `¬C1` (+`C3`, moot) | — | NO-SCENE |
| `R8` | `¬C1∧¬C2∧¬C3` | no | — | duplicate of `R6` | — | NO-SCENE |

**The omitted row**, `¬C1∧C2∧¬C3`, is `NO-SCENE` under this rule. That is worth stating plainly: restoring it adds
**zero** live cells. Under the *original* tiers it was the only row with three `PASS` cells — and it was passing
because nothing had happened, which is why the omission cost the matrix no information and cost the record one
misleading impression. `M0` is a real defect about completeness; it is not a defect about content.

---

## 3. Columns — unchanged, deliberately

`Q0 ≥ 0.50`, `Q1 = ξ/h ≥ 4.0`, `Q2 ≥ 0.50`, `Q3 ≥ 2.0`, all hash-locked before evaluation
(`runs/MATRIX/threshold_lock.json`, lock 59.2 s older than the run). **No column is redefined here.** The previous
proposal's four replacement columns each reproduced a measured failure; this design's contribution is the row and
rung axes, not a fifth attempt at the columns.

Two reading rules carry over unchanged and are load-bearing:

- `MR1.2` — a cell is a profile, never a maximum.
- `MR1.3` — a `Q3` value measured on an abstract field **may not be inherited** by a cell. So `Q3` on any row is a
  *prediction about a scene not yet built*, never a borrowed number.

---

## 4. The cell

```
cell = ( q , verdict , evidential , rung* , V , Φ )
```

- `q`, `verdict` — the tier value and `PASS/FAIL/NO-VERDICT`, or `NO-SCENE`.
- `evidential` — `False` when the pass survives the destruction of arrangement (`MR1.1`: shuffling keeps `Q0`,
  `Q1`, `Q2` above threshold). A `PASS` with `evidential = False` is recorded and **not counted as evidence**.
- `rung*` — the cheapest rung at which the column passes on this row; `BLOCKED` when the input the rung needs does
  not exist; `—` when no affordable rung reaches it.
- `V` — the violation factor the row buys (`R2 ≥ 10⁵` for `C3`; none otherwise).
- `Φ` — orders of flux the rung spends, where the rung is optical.

---

## 5. The grid

Numbers in `Q0`/`Q1`/`Q2` for the bonded scene are the **declared-scene reference** (`TILED` row of
`runs/MATRIX/structure_tiers_results.txt`), admissible only as a prediction target. The severed scene has **no
calibration analogue** — none of the nine declared scenes is a periodic array of isolated plates, which is the one
gap in the calibration set worth naming.

| row | scene | `L0` `Q0≥0.5` | `L1` `ξ/h≥4` | `L2` `Q2≥0.5` | `L3` `Q3≥2` |
| --- | --- | --- | --- | --- | --- |
| `R2` | severed | `FAIL` pred. (`β₀ = 1.1831e10`) | `FAIL` pred. (`ξ/h ≈ 1`, `ξ = pitch`) | `PASS†` pred. (periodic ⇒ locally determined) | `FAIL` at `q=0` (= 0.000); `BLOCKED` at `q=1` |
| `R5` | bonded | `0.9989 PASS†` | `27.55 PASS†` | `0.9417 PASS†` | `6.316 PASS` at `RL-1` (`q=1`), `0.000 FAIL` at `q=0` |
| `R1` | severed | = `R2`, price `R2` knob | = `R2` | = `R2` | = `R2` |
| `R3` | bonded | = `R5`, price `R2` knob + 1 law | = `R5` | = `R5` | = `R5` |
| `R4`,`R6`,`R7`,`R8` | — | `NO-SCENE` | `NO-SCENE` | `NO-SCENE` | `NO-SCENE` |

`†` = passes, not evidential (`MR1.1`).

**The one sentence the grid produces.** The only row in which all four columns pass is `R5` — the row the audit
typed `UNREALIZED` — and it passes at `RL-1`, the cheapest rung in the ladder, whose price is a *convention*
(a declared instrumented observer, gate ≤ 3 ns) and not a field. The row that costs nothing, `R2`, fails three of
four and its single pass is non-evidential. **The matrix, correctly typed, reaches the ladder's conclusion from the
row side**, using the audit's own numbers.

---

## 6. Compression, computed not asserted

`src/route/matrix_v2.py` emits the count: 8 rows × 4 columns × 7 rungs = 224 nominal; 20 canonical
(`2 scenes × 3 observer-independent tiers` + `2 scenes × 7 rungs` on `L3`); **9** of the 20 carrying a value or a
prediction; 5 priced but uncomputed (`R5`'s `L3` at `RL-2…RL-6`); 6 blocked (`R2`'s `L3` above `RL-0`, no
compliant `σ_s`). The registered count said 8 and the program returned 9 — the missing entry was `R2`'s `L3` at
`RL-0`, which is a value (`0.000 FAIL`) and not a blocked entry. Recorded as `E1` in the registration rather than
edited there.

---

## 7. What makes it falsifiable

Four predictions, each with a stated killer. They are pre-registered in
`runs/MATRIX2/matrix_v2_registration.md`, before the code existed.

| id | prediction | falsified by |
| --- | --- | --- |
| `V1` | the severed scene fails `Q0` (`Q0 < 0.5`) | a measured `Q0 ≥ 0.5` on a periodic isolated-plate scene |
| `V2` | the severed scene fails `Q1` (`ξ/h < 4`) | `ξ/h ≥ 4` measured on it |
| `V3` | the severed scene passes `Q2` **and the pass is non-evidential** | `Q2 < 0.5`, or a shuffle that drops it below threshold |
| `V4` | the bonded scene passes `L3` at `q = 1`, `RL-1` | `Q3 < 2.0` measured on a bonded scene carrying the 2D-ified content |

`V4` is the load-bearing one, and it is also the only one that cannot be answered from existing files: `MR1.3`
forbids inheriting `TILED`'s `6.316`. That is not a weakness of the design — it is the measurement the design
exists to demand.

---

## 8. Rendering

Two panels, both `FL1`, both charts of declarations:

1. **The grid** — 8 rows × 4 columns, each cell coloured by class (`PASS` / `PASS†` / `FAIL` / `NO-SCENE` /
   `PRICED`) with `rung*` printed as a digit. This is what a reader can actually use, and it is honest because the
   `PASS†` class is visible.
2. **The price ladder** — `Φ` against rung, with the two hard knobs marked (`R2 ≥ 10⁵`, `R1 ≥ 6.2e23 V/m`) and
   the `2¹⁴` wall at `RL-6`.

What may **not** be rendered: the scene. `DEPOSIT-DICHOTOMY` fixes that at `16,384 = 2¹⁴` exactly, and no scale
factor exists (`sup d₃D = 0.292062 m` inside `pitch = 0.400100 m`). A keyframe animation from `R2` to `R5` would
have to invent every intermediate frame, and there is no intermediate state (`KIN-DYN`).

---

## 9. What this design does not fix

- **`D-9` still bites.** `R2`'s scene is the deposit, and the deposit reads only `(M, N)`: six distinct objects,
  one digest, `I(canvas ; r₄) = 0`, 10 of 12 parameters never reaching a site. So `R2`'s cells are statements about
  a declaration. `MR1.6` is a ceiling, not a bug, and v2 does not lift it.
- **The ladder has one column.** `RL-1`…`RL-6` act only on `Q3`; `Q0`, `Q1`, `Q2` are invariant under every rung.
  Anyone reading the ladder as a seven-row improvement over four tiers is reading it wrong, and this design says so
  in the count.
- **`R5`'s price is ordinary, its result is not.** One elastic modulus buys a *structured* scene — but `MR1.1`
  measured that scrambling the tiles leaves `Q0`, `Q1`, `Q2` above threshold, so "structured" here means
  "tessellated", not "this object". The `PASS†` marks exist to keep that distinction visible in the grid.
- **`C3` and `L3` meet at the same document.** `C3`'s price is `scifi_boundary_v1`'s `R2`; `L3`'s failure is that
  document's §3 (light crosses 1 m in 3.3 ns, the state lives 3–5 ns). The two obstacles are the two hard knobs of
  one boundary, which is why paying one makes the other worse rather than better.

---

## 10. First executable step

Add a **deposit-like scene class** to the calibration set — a periodic array of isolated plates, 50 % fill,
`pitch/h = 1`, `N = 1.1831e10` as a tiling of a small patch — and measure `Q0`, `Q1`, `Q2` on it with the locked
thresholds and the declared null ensemble.

That single run settles `V1`–`V3`, gives `R2` its first real cells, and closes the calibration gap this document
names in §5. It requires no new physics, no `σ_s`, and no governor ruling.

---

## 11. Status — read as a product (appended 2026-11-23, round 52)

The header says this document *"may not be cited as authority until a governor ruling exists."* A ruling now
exists: `docs/decisions/matrix_v2_status_reading_v1.md`, instructed as "read matrix v2 as a 'product' rather than a 'route', and do not write an approval
block for it".

The ruling does not ratify this document; it **types** it. The header's condition is therefore discharged in the
negative — a ruling exists, and it declines the authority the sentence anticipated. What follows from that:

- **This document and its programs are products of rounds 46–47.** Their numbers may be cited as evidence; they
  may not be cited as authority for a decision. The authority to proceed is `PG-03` (Path A), which sits on
  `relaxation_frame_v1.md` §9 and governs the ladder, not this reconstruction.
- **No approval block is owed and none will be added.** There is no downstream build decision waiting on one
  (Test (a), reading §2) and this is not the only place the question is asked (`relaxation_ladder_v1.md` §4 is).
- **Nothing in §§0–10 changes.** The rank count, the 26 canonical cells, the 8.6:1 ratio, `G1`–`G5`, `R5`'s 0/4
  and errata `E1`/`E2` all stand exactly as written. Only the status of the whole is retyped.
- **The 8×4's own verdict stands unchanged.** `NOT VIABLE AS WRITTEN` is not repaired by this document being a
  product rather than a route.

Read §4 of the reading before citing any number here inside a decision; rule 3 is the one that binds — prices,
not reasons.

*Content generated by AI*
