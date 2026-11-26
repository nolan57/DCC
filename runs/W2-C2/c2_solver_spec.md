PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (sections 4.2.3, 4.2.6, 4.8, 5.1, 6.1, Appendix D).
PROVENANCE: NEITHER
# Solver spec -- W2-C2VIOL-01

1. **What is solved.** No PDE. The row-2 field at each keyframe is pushed forward by the declared dilation; conservation is exact on the finite window by area-overlap apportionment plus an explicit OUTFLOW ledger.
2. **Grid / boundary.** 128^2 cells, unit cell in the registered window; dilation about the origin; cells whose image crosses x>=128 or y>=128 contribute OUTFLOW.
3. **Estimators.** `src/analysis/tiers_core_v1.py`, thresholds from runs/MATRIX/threshold_lock.json. Each cell records estimator id, threshold, q, seed, and source hashes.
4. **Profiles.** T0-T3 on `plate` (stretched) and `canvas` (unchanged, declared out of scope of the dilation) at t0 / t_mid / t_end; t0 cells stay NOT-APPLICABLE because no 2D output exists before the front.
5. **Effective 2D.** Three labels recorded separately; the missing model slot is named, so the label is NOT-MEASURED and no IS_2D / LOOKS_2D claim follows.
6. **Reproduction.** R2 for physical quantities; frame reproduction (R3) not claimed.
