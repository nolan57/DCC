# Pre-registration -- W2_C3

PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (sections 4.2.3, 4.2.6, 4.8, 5.1, 6.1, Appendix D).
PROVENANCE: NEITHER

**Cycle type**: technical closure  
**Product owed**: `runs/runs/W2-C3/c3_results.txt`

## Numeric predictions (fixed before any stage-B run)

| id | prediction | falsified if |
|---|---|---|
| C1 | Y_e and n_e fall in ALL3D / HYB / ALL2D | any convention with n_e >= frozen |
| C2 | mu_kin falls; 2D kinetic ratio follows n_e^(2/3) | ratio disagrees beyond rounding |
| C3 | plate and canvas sha256 identical across branches | any byte difference |
| C4 | graph check ABSENT-FROM-GRAPH | any token hit -> NO-OBSERVED-EFFECT instead |

## Kill condition

If a composition token is found in u's generator, GENERATOR-DOES-NOT-CONSUME is refused and NO-OBSERVED-EFFECT is recorded with the missing encoding named.

## Scope and barred claims

No visibility, optical, effective-2D or realizability claim. C3 held is a counterfactual branch; the neutronized branch is not a prediction of a realizable process.
