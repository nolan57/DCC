# Pre-registration — RR-DT-01: record repair, deferral, dual-track advancement

**Written**: 2026-11-24, before any file under `docs/` was edited for this round and before the
instrument existed.
**Authority**: governor directive G-71-01 (round 71), instruction RR-DT-01.
**PROVENANCE**: NEITHER. This round edits documents and writes a relaxation log. It derives no new
physics except the closed-form arithmetic §4 of the record requires (B1 degree, B3 back-reaction
scale), adjudicates no gate, and authorises no route.
**Instruments**: `src/rr_dt/rr_dt_01_record_repair.py` (`--write`), plus the report-only
`src/common/program_audit.py`.

## 1. Scope, and the one rule that governs every edit

G-71-01 §1 orders three documentation repairs, §2 defers six findings, §3 promotes adiabaticity to
`WORKING-HYPOTHESIS` and opens a relaxation ladder. None of it moves a number.

The repository's own rule (`symbol_registry.md` §9.1, and every erratum in `relaxation_ladder_v1.md`)
is that **an archived product is never edited**: its SHA-256 is registered in
`runs/PROGRAM/round_ledger.jsonl`, and a byte change would break the chain that makes the record an
audit trail. G-71-01 §1.3 names "product files" as annotation targets. Those two rules collide for
exactly the artifacts that carry `K²−K_ijK^ij`.

**Pre-registered resolution (the eligibility rule of this round).** An artifact is edited in place
only if it is not hash-registered. If it is hash-registered, the annotation is carried by (a) this
round's product, which names every such location, and (b) an errata entry in the unsealed document
that owns the same content. The alternative — editing a sealed product — is refused, because the
audit trail is the only reason the product is citable at all.

Every artifact below is therefore classified `EDITABLE` or `SEALED` before any edit, and the
instrument verifies that **no** sealed file moved.

## 2. Repair targets and their acceptance predicates

| id | target | acceptance predicate (machine-checked) |
|---|---|---|
| `R1` | `docs/specs/relaxation_ladder_v1.md` — `RL-6` qualification | file contains the qualification sentence verbatim, adjacent to §2's rung table; the table bytes are unchanged |
| `R2` | `docs/conventions/constraint_crosswalk_v1.md` — forward reference | new `§8.5` names `RL-6`, `relaxation_ladder_v1.md` and the modelling choice of §8.2 |
| `R3` | `docs/decisions/G0p_seven_row_verdict_v3.md` — row 1 basis | row 1's basis cell contains `conditional on fixed (M, A_⊥, m̄)`; the cell no longer asserts independence of every convention |
| `R4` | same file — reverse-on phrase | `§8 (E4)` records the replacement text verbatim and states that the cell lives in a sealed product |
| `R5` | `docs/conventions/symbol_registry.md` §4 — `K²−K_ijK^ij` annotation | the annotation string `[IDENT — no constraint information; see AX-01 HIGH-3]` is present, with all four in-record locations listed |
| `R6` | deferral | the product's deferral block lists exactly the six AX-01 items `F-005`…`F-010`, with their severities, and no more |
| `R7` | Track A | `docs/decisions/kinematic_vs_dynamic_unfolding_v1.md` carries the `WORKING-HYPOTHESIS` relabel and the citation tag `[WORKING-HYPOTHESIS: adiabaticity; see RR-DT-01 §3.1]` |
| `R8` | Track B | `runs/RR-DT/constraint_relaxation_record.md` populates `B1`…`B8`, each with the five required fields; exactly one level is `HARD-SCI-FI-LIMIT`; `B10` is never relaxed |

## 3. Invariants frozen at this moment (checked again at emission)

`I1` every `product` and `registration` path registered in the ledger has the same SHA-256 at
emission as at this moment.
`I2` the `items` and `gates` arrays of `docs/program/round_queue_v1.json` are byte-identical
(cursor and board notes are the only fields this round may touch).
`I3` `reports/DCC_terminal_answer_v1.md` is byte-identical — it is `SEALED` (round 62), so `R4`'s
phrase replacement cannot be applied to it directly.
`I4` no file under `reports/gates/` is modified.
`I5` the three numbers the six deferred findings are about are unchanged: `2e4`/`1.94805e4` (`F-010`),
`Φ = −4.5` (`F-006`), `L_z = 1 fm` (`F-007`).

`I1` is the load-bearing one: it is what converts "I did not edit the sealed products" from a claim
into a measurement.

## 4. Track B: what each level must record, and the stopping rule

For each of `B1`…`B10`: what was relaxed, the degree (quantitative where a number exists on file),
whether the record stays self-consistent, whether the hard-SF boundary is reached, and three
re-evaluations — `RL-6` price, `G0′` clause status, effective-2D criterion.

**Boundary test, fixed before the run.** A level is `HARD-SCI-FI-LIMIT` when the relaxed premise,
combined with a statement the record already asserts, yields `A ∧ ¬A` about the *same* object at the
*same* time — not when it merely weakens a claim, makes a criterion false, or costs more. Weakening
is not contradiction. Naming a level `UNVERIFIABLE` is not naming a boundary.

Order is `B1` upward, no skipping. Evaluation stops at the first level that satisfies the boundary
test; later levels are recorded as `NOT EVALUATED-BEYOND-BOUNDARY` rather than guessed.

## 5. Result-class ceiling

The maximum admissible claim is: *three documentation contradictions are repaired without moving a
number; six findings are deferred by name; adiabaticity is carried as a working hypothesis with its
dependency list; and the relaxation ladder reaches the hard-SF boundary at a named level for a named
reason.* No matter-survival, visibility, gate, threshold, terminal-class, price, route or D-state
claim is admissible, and Track A's results are never presented as evidence that the hypothesis holds.

## 6. What this pre-registration gives up, stated in advance

`R3` edits a decision record whose earlier errata twice wrote "the row is not edited". That
convention protected a *verdict* from being softened by later evidence. `R3` does not touch the
verdict: it narrows a basis description that the same record already contradicts in §8.1 of the
crosswalk. The edit is made under G-71-01 §1.2, is quoted in full in the product, and the earlier
errata sentences are left standing so the departure is visible rather than tidied away.
