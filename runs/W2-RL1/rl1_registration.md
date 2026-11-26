# Pre-registration -- W2-RL1-01

PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (section 6.1 item 6, sections 4.3/4.4/4.7/5.1).
PROVENANCE: NEITHER

**Cycle type**: TECHNICAL closure
**Product owed**: `runs/W2-RL1/rl1_results_v1.txt`

| id | prediction | falsified if |
|---|---|---|
| R1 | `q(theta_fast)` saturates at 1 because `C_xi > C*` | `C_xi <= C*`, giving q < 1 |
| R2 | `Q3_fast = Q3_ideal` to 1e-12; `Q3_eye = 0` exactly | either equality fails |
| R3 | T0-T3 at q=1 reproduce the W1-ROW2 t_mid profile; no verdict flip | any value or verdict differs |
| R4 | shortfall at the measured `C_xi` is < 1 | shortfall >= 1 |

## Kill condition

If the kill condition fires, the cycle records RL-1 as FALSIFIED on this scene; no threshold is re-priced and
the old stand-in result is not substituted.

## Scope and barred claims

This is a channel measurement on the deposit's declared field. It is not a new physics result, not an
effective-2D label, not evidence of legibility from a particular viewing geometry, and not an O0 artifact.
