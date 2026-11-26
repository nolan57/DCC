PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (sections 4.2.3, 4.2.6, 4.8, 5.1, 6.1, Appendix D).
PROVENANCE: NEITHER
# Solver spec -- W2-DISC-01

1. **What is solved.** No equation of motion. The registered phantom is sampled; the control replaces one layer by a ten-layer z-window average at the same front position. Counts are recomputed from N = z_f / delta and N_frag = N x 1.457.
2. **Fields.** `plate`: tissue-density index of the axial slice at z_f. `canvas`: per-site mean layer density downsampled to 128^2; its fill is z_f/(H) in the baseline and 10x smaller in the control because the site census is 10x smaller.
3. **Estimators.** `src/analysis/tiers_core_v1.py` verbatim, thresholds and constants read from runs/MATRIX/threshold_lock.json; grid 128^2, bins 64, context 16, DoG sigma = xi/2 and 2 xi.
4. **Floor.** The deterministic repeat of the baseline field is the instrument floor (byte-identical, tier ratios exactly 1). A control difference at or below that floor is NO-OBSERVED-EFFECT, not a pass awarded after seeing the number.
5. **Judged quantities.** deposited mass/volume, front position, sheet/plate/fragment census, conserved-integral residual, and both fields' T0-T3 profiles. Appearance is not evidence.
6. **Status vocabulary.** PASS / FAIL / REFUSED / NOT-APPLICABLE / NOT-MEASURED stay distinct; a NO-VERDICT tier is not a FAIL.
