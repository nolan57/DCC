# Pre-registration -- W2_DISC

PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (sections 4.2.3, 4.2.6, 4.8, 5.1, 6.1, Appendix D).
PROVENANCE: NEITHER

**Cycle type**: technical closure  
**Product owed**: `runs/runs/W2-DISC/disc_results.txt`

## Numeric predictions (fixed before any stage-B run)

| id | prediction | falsified if |
|---|---|---|
| D1 | plate sha256 equal; tier ratios = 1.0 +/- floor | any plate byte difference or verdict flip |
| D2 | N_slices, plates and fragments x 0.1 (rel. err < 1e-12) | ratio outside 0.1 +/- 1e-12 |
| D3 | canvas fill x 0.1; xi_canvas rises >= 20% | fill ratio wrong or xi not increased |
| D4 | mass, volume, z_front unchanged (< 1e-12); residual 0 | any drift or nonzero residual |

## Kill condition

If the kill condition fires, the cycle closes with the NEGATIVE result 'the plate result is discretization-dependent'; it is not re-labelled a pass and no threshold is re-priced.

## Scope and barred claims

No frame is claimed, no O0 artifact is claimed, no visibility or realizability claim is made. The control is a different mechanism id (delta x 10), not a rendering of the baseline.
