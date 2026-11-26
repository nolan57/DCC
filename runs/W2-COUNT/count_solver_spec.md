PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (sections 2.5 item 10, 2.6, 4.8).
PROVENANCE: NEITHER
# Solver spec -- W2-COUNT-01

1. The `M` contract is written from §2.6 and the W1 front law; it is not inferred from appearance.
2. The component table is parsed from `runs/ANALYSIS/front_sweep_v1.txt` lines 11-17; no count is retyped.
3. The mean is weighted by each region's z-width, the only registered layer-density weight.
4. The spread is the same weighted standard deviation; it is reported as derivation spread, not promoted to a
   measurement error of the physical phantom.
5. `N_slices` and `N_frag` are recomputed at t_mid from `src/analysis/w1_row2_common_v1.py`; both remain
   MODEL/MECHANISM counts with their derivation attached.
