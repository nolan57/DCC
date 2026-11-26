PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (section 6.1 item 6, sections 4.3/4.4/4.7/5.1).
PROVENANCE: NEITHER
# Solver spec -- W2-RL1-01

1. `C*` is not re-derived from a new model. It is recovered from the registered shortfall at contrast 1e-7:
   `C* = 1e-7 sqrt(S)`, with `S` read from `runs/LADDER/r1_observer_results.txt`.
2. The row-2 plate field at `t_mid` is regenerated from `src/analysis/w1_row2_common_v1.py`. `xi` and `C_xi`
   come from the locked `src/analysis/tiers_core_v1.py` estimators; no threshold is changed.
3. `q(θ_fast) = min(1, (C_xi/C*)^2)`; `Q3 = log2(1 + C_xi q / C_eye)` with `C_eye = 0.01` from the lock.
4. `T0-T3` at `q=1` are compared with `runs/W1-ROW2/row2_prediction_v1.json`; a verdict flip is a kill.
5. No new frame is rendered. No viewing-geometry claim is made because the estimator has no angular variable.
