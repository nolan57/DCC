# Pre-registration -- W2-COUNT-01

PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (sections 2.5 item 10, 2.6, 4.8).
PROVENANCE: NEITHER

**Cycle type**: TECHNICAL closure
**Product owed**: `runs/W2-COUNT/count_results_v1.txt`

| id | prediction | falsified if |
|---|---|---|
| N1 | M contract has history functional, domain, units/coordinates, single-valuedness, discard ledger | any element absent |
| N2 | weighted mean components/layer = 1.457 +/- 0.002 | outside the interval |
| N3 | weighted spread is nonzero and labelled derivation spread | spread = 0 or mislabelled |
| N4 | counts are recomputed with derivation and label | any count lacks derivation or label |

## Kill condition

If the weighted mean misses 1.457 +/- 0.002, the cycle records a count-derivation defect against front_sweep_v1;
it does not silently reprice the component rule.

## Scope and barred claims

No claim that the phantom is a real body, that the fragment count is observed, or that the count error is a
physical measurement uncertainty. The spread is a derivation property of the registered region table.
