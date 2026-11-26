# H5-B8 — Stage A Pre-registration

**Registered**: 2026-11-26, before any stage-B script was written.
**Scope**: exact conformance check of the adopted route's advance to the B8 boundary. This round registers
**no threshold**; the numbers below are predictions about what the archived products say, quoted with the
file and line that produced them. `CHECK`, `IDENT` and `NEGCTRL` are counted separately.
**Locks**: `b8_route_boundary_lock.json` + `.sha256`, created after this file and the card/prediction were
written and before stage B ran. The lock names every **immutable** input the verdict reads. The adoption
document is deliberately not locked: §6 of it is appended from this cycle's product after stage B, so
including it would make the lock fail by construction. Its pre-run text is quoted in the product by file
and section, and the mark it records is verified through the locked v1 proposal.

## One question, one sentence

Does the adopted route stop at B8 — the unique boundary level of the registered B1–B10 ladder — with its
Phase 1 result capped at constraint-satisfying and no avoidance route adopted?

## Predictions (numeric; each with a kill condition)

| id | prediction | value | source of the expected value | kill condition |
| --- | --- | --- | --- | --- |
| **P1** | number of B-levels marked `boundary YES` in the archived status table | `1`, at level `B8` | `runs/RR-DT/rr_dt_01_record_repair_results.txt`:88–97 | any other count or level |
| **P2** | count of `self-consistent YES` over B1–B7, and B8's `self-consistent` value | `7` and `NO` | same file:88–95 | count ≠ 7 or B8 ≠ NO |
| **P3** | B9 status = `NOT EVALUATED-BEYOND-BOUNDARY`, B10 = `NEVER RELAXED` | `2/2` | same file:96–97; `constraint_relaxation_record.md`:246–260 | either status absent |
| **P4** | at B8: `RL-6 = 2e4`, effective-2D slot `undefined`, `G0′` row 1 `unsayable` | `3/3` | `constraint_relaxation_record.md`:240–243; `rr_dt_01_record_repair_results.txt`:280–291 | any of the three changed |
| **P5** | Phase 1 result-class ceiling is "constraint-satisfying solution", and it explicitly denies evolution/joint class | `1/1` | `runs/P1/phase1_symbolic_constraint_results.txt`:34–38 | ceiling raised or denial absent |
| **P6** | two B8 avoidance routes recorded, zero adopted by the adoption document | `(2, 0)` | `constraint_relaxation_record.md`:228–234; `hard_sf_effective_2d_route_adoption_v1.md` §3 | count ≠ 2 or adoption ≠ 0 |

**Overall kill condition**: P1–P6 must all pass, and every stage-A hash must verify; otherwise the cycle prints
`FALSIFIED` and the B8 advance is not claimed by it. A failed prediction is kept in the product verbatim.

## Negative control and identity (counted separately)

- **NEGCTRL N1**: the same parser looking for `boundary YES` at `B7` must return `0` matches while B8 returns
  `1`; if B7 also returns `1`, the parser is not discriminating and the run is void. Required failure factor:
  `1` level, i.e. B7 count `0` against B8 count `1`.
- **IDENT I1**: parsing the archived table twice must give byte-identical extracted records; identities are
  reported as `IDENT` and are **not** counted as evidence.

## Instrument floor

The instrument is an exact textual parser over archived files. Its floor is `0` mismatches when the input is
unchanged: the same file parsed twice yields the same record (I1), and no numeric tolerance is used. No
branch of this instrument can distinguish a one-character change in a counted field from no change; that
limit is printed in the product.

## Prohibitions

Not `S9` visibility; not the deposit frame as readability; not `440 MeV` as input; not a scanned `τ` as
response; no new threshold; no archived product edited.
