# Pre-registration -- W2_C2

PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (sections 4.2.3, 4.2.6, 4.8, 5.1, 6.1, Appendix D).
PROVENANCE: NEITHER

**Cycle type**: artifact cycle  
**Product owed**: `runs/runs/W2-C2/c2_results.txt`

## Numeric predictions (fixed before any stage-B run)

| id | prediction | falsified if |
|---|---|---|
| S1 | det J = 1.0201, area change +2.01% | any other value |
| S2 | full-ledger residual < 1e-12; window deficit about 2% | residual >= 1e-12 or missing outflow |
| S3 | xi ratio in [0.99, 1.03] | ratio outside the interval |
| S4 | T0/T2/T3 PASS at t_mid; canvas profile identical | verdict flip or canvas change |

## Kill condition

If the conservation ledger fails or xi does not scale with s, the branch is recorded as FALSIFIED; the row is not withdrawn and no threshold is re-priced.

## Scope and barred claims

COUNTERFACTUAL(C3) is not claimed: C3 is VIOLATED here. The stretch is a hard-SF priced violation, not a visibility, readability, realizability or identity claim. Frames without their sidecars are not citable.
