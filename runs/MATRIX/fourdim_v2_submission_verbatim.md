# Four-dimension re-anchoring — submission, verbatim

**Status**: PROPOSED. Registered as received 2026-11-22T18:12+08:00. No alteration, no condensation.
The ruling on it is `docs/decisions/four_dimension_reanchor_v1.md`, written after the run, not before.

---

The previous assessment is rejected. The four-dimensional scoring framework has not been invalidated; rather, the
evaluation criteria for each dimension were either undefined or lacked consensus. To establish a rigorous foundation
for the physical self-consistency audit and realistic visualization of the DCC model, the criteria for the four
dimensions of "structural distinguishability" are hereby re-anchored as follows:

**Topological Distinguishability (Baseline Threshold):**
Defined as the Topological Invariant Conservation Rate. The number of connected components and the genus (number of
holes) of the original 3D macroscopic object must be 100% consistent with the 2D projection. Any violation of
topological invariants results in an immediate failure, terminating all subsequent evaluations.

**Metric Distinguishability (Intermediate Evaluation):**
Defined as the Metric Space Distance Threshold. The distance (e.g., Hausdorff or Wasserstein) between the 2D
projection and the original 3D structure must be less than a pre-declared threshold ε. The metric function and ε must
be locked prior to measurement to prevent post-hoc selection bias.

**Information-theoretic Distinguishability (Terminal Condition):**
Defined as the Channel Mutual Information Lower Bound. Treating the 2D projection as an information channel, the
mutual information I(2D image; 3D macroscopic structure) must exceed a pre-declared minimum threshold I_min. This
objective criterion inherently rejects random noise or "scrambled" outputs that lack structural information,
resolving the previous flaw where noise could pass the evaluation.

**Visual Distinguishability (Final Verification):**
Defined as the Observer Extraction Success Rate. There must exist an observer O (naked eye or infinite computational
capacity) and an extraction method M capable of identifying the macroscopic structure from the image. Digital
enhancements (e.g., pseudo-color, contrast stretching) are strictly prohibited from introducing physically
non-existent information; otherwise, the result is deemed a "false visualization" and scores zero.

These four dimensions form a strictly progressive hierarchy: Topological as the baseline gate, Metric for
intermediate comparison, Information-theoretic as the terminal quantitative condition, and Visual as the final
empirical verification.
