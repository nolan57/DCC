# DCC P3-C5 Adiabatic-Criterion Parameter-Sensitivity Scan Report v1.0

**Project**: Dimensional Collapse Conjecture (macroscopic dimensional phase-transition model)
**Document Type**: P3-C5 conclusion-level scan report (takes priority over the P2-C2 spherically symmetric York initial data)
**Date**: 2026-11-20
**Script**: `DCC_P3_C5_adiabatic_scan.py` → stdout archived as `DCC_P3_C5_adiabatic_scan_stdout.txt`
**Dependencies**: D2 background (achieved); does not depend on D3. Once D3 is achieved, a version must be rerun with the true dynamical C(t).
**Prerequisite Status**: Both prerequisites have been filled in (§1); before that, the results were only "conditional conclusions for given p_z".

---

> ## Mandatory Honesty Boundary (Front Page, Must Not Be Omitted)
>
> **This scan is based on a specified contraction background (power-law ansatz C∝t^{−1/2}, A∝B∝t^{+1/2}, a phenomenological scaling extrapolated from the magnetic attractor); D3 has not been achieved; the low-speed wall-velocity group is a phenomenological assumption, not a prediction (P1b controllability FAIL is permanently archived).** If D3 is achieved later, this task must be rerun with the true dynamical C(t).

---

## 0. Verdict Summary

| Item | Result | Status |
|---|---|---|
| Prerequisite confirmation 1 (origin of p_z=0.5) | Representative value, not fixed by a relation; numerically coincides with the η(t0)=1 relation | Filled in |
| Prerequisite confirmation 2 (basis for t*/C(t*)/β_C) | t0=1 and C0=1 are pure normalization; β_C=−1/2 is a phenomenological exponent | Filled in |
| Regression check (α=.5, p_z=.5, β_C=−1/2, t=t0) | η=1.000000000000000, error 0 | PASS |
| Dimensional-consistency assertion | [η]=M^0 | PASS |
| Reproducibility (two runs) | stdout / CSV / drift table byte-for-byte identical; NPZ md5 identical | PASS |
| β_C physical gate | −1/2, −1/3, −2/3 pass; 0, +0.5, −1.5, −2 flagged red and discarded | PASS |
| Drift of the η=1 contour with respect to α | **Always 0 (the formula does not contain α)** | Structural conclusion |
| Drift of the η=1 contour with respect to β_C | p_z^* = \|β_C\|: −1/3→−33.3%, −2/3→+33.3% | Conditional |
| Fraction of the robustly adapted region (α 10 × p_z 20 = 200 points) | 35–55% (β_C slices) | A majority region exists |
| Fraction of the robustly destroyed region | **0% (all slices)** | None |
| Interpretation for the two wall-velocity groups | Pointwise identical (the formula does not contain wall velocity) | Archived separately |

**Termination verdict**: The condition "a robust region occupies the majority of the parameter plane → close out and give a conditional conclusion" is satisfied (the robustly adapted region exists and is the only region with definite verdicts, accounting for 35–55%; the η=1 contour is a single vertical line and does not traverse the whole interval). **This task is closed.** "Coming out critical" is not grounds for rework.

---

## 1. Filling In the Prerequisites (Hard Prerequisites for Scan Validity)

### 1.1 Origin of p_z=0.5: A Representative Value, Not Fixed by a Relation

- **Evidence**: In `DCC_P3_mode_freeze.py`, `pz_list = [0.0, 0.5, 1.0, 2.0, 4.0]`; 0.5 is a sampled representative point chosen from this list, not solved from an independent equation.
- **Relation (numerical coincidence, not an independent constraint)**:
  η(t0) = |β_C|·C0/(p_z·t0) = 1  ⟹  p_z^crit = |β_C|·C0/t0 = 0.5·1/1 = 0.5.
  That is, "0.5" and "critical at t0" have the same numerical value because the frozen β_C=−1/2 and the normalization C0=t0=1 happen to give 0.5; if β_C or the normalization changes, the critical p_z changes accordingly.
- **Reasonable range**: No theoretically constrained interval—the comoving z volume is unspecified and the KK tower spacing is undetermined (P3 Effective Theory §7 domain-of-validity table); therefore the task-default axis A [0.1, 2.0] with 20 logarithmically uniform points is used (covering roughly O(10) on both sides of the critical value).
- **Strength of conclusions**: Before this section was filled in, the scan yielded only "conditional conclusions for given p_z"; it is now filled in, but p_z remains an externally given parameter, so the conclusions still carry the "given p_z" qualification.

### 1.2 Basis for the Values of C(t*) and β_C at t*

- t* ≡ t0 = 1: the normalization starting time of the P3 ansatz.
- C(t0) = C0 = 1: **pure normalization convention** (a common rescaling of the scale factor and time).
- β_C = −1/2: **not a normalization**, but a phenomenological scaling exponent (representative value extrapolated from the magnetic attractor; the vacuum Kasner extrapolation gives −1/3, consistent in sign—P3 Effective Theory §1.1). Changing β_C is a change of model assumption and must not be written as a change of units/gauge.

---

## 2. Scan Target, Formulas, and Axes

### 2.1 Criterion (Over the Whole Trajectory, Not a Single Point)

Over the full wall traversal t∈[t0, 30t0] (1200 points), compute

η(t) ≡ |ṁ_eff| / m_eff² = |β_C|·C(t) / (|p_z|·t),  C(t)=C0(t/t0)^β_C
     = (|β_C|·C0/t0)/|p_z| · (t/t0)^{β_C−1}.

Output η_max, η_min at each point and the η=1 crossing time t_cross (if any):

t_cross = t0 · (|β_C|·C0/(p_z·t0))^{1/(1−β_C)},  exists provided t0 ≤ t_cross ≤ 30t0.

**Interpretation bands**: η<0.9 adapted; η>1.1 non-adiabatic/destroyed; 0.9≤η≤1.1 no discriminating power (operationalization of the user's "η≈1", with a ±10% band).
η(t) decreases monotonically for β_C<0 ⇒ η=1 is crossed at most once.

### 2.2 Axes and Their Sources

| Axis | Range/Values | Source |
|---|---|---|
| A p_z | [0.1, 2.0], 20 logarithmically uniform points | Task default (no theoretically constrained interval, see §1.1) |
| B α | [0.1, 1.0], 10 linear points | Task default; L4 frozen α=0.5 is one of the slices |
| C β_C | −1/2 fixed; −1/3, −2/3 for robustness | Task default; physical gate: β_C<0 and β_C ≥ −2β_AB = −1 (total volume ABC does not recollapse) |

**Wall-velocity grouping**: The relativistic group β_w=0.5 (registered in the P4 Report, a dynamical solution) and the low-speed group β_f=1.416647e−4 (registered in P1b, **a phenomenological assumption, not a prediction**) are run and concluded separately. All outputs for the low-speed group are required to carry a label.

### 2.3 Input Files and Version Hashes (Read at Script Runtime; No Hard-Coded Values)

| File | Use | SHA256 |
|---|---|---|
| `DCC_P3_mode_freeze.py` | C(t) background constants (T0/C0/BETA_C/T_END read via importlib) | b5d20a5f…f594d51 |
| `DCC_P2_1p1_frames.npz` | Wall-trajectory time window (read from NPZ) | d3b42954…57d6b |
| `DCC_P1_results.txt` | Low-speed wall-velocity registration | c346e064…2c14c |
| `DCC_P4_Report_v1.md` | Relativistic wall-velocity registration | 6d7ebbac…cf3a8 |
| `DCC_P0-P4_Roadmap_Plan.md` | Status registration (updated to v2.7 in this round) | f7d91638…f43c6ab |

The full 64-digit hashes are in the stdout archive. **Note**: t∈[0, 5.99] in the NPZ is P2 ADM code time; the η scan uses the P3 ansatz effective window t∈[t0, 30t0]. The two have different normalizations and must not be mixed.

---

## 3. Key Structural Findings (Reported Honestly, No Fabricated Dependencies)

**The formula for η contains neither α nor the wall velocity β_w.** Hence:

1. In the (p_z, α) plane, η_max contours must be **vertical lines**, and the drift with respect to α is **identically 0** (not "happens to be small", but a structural identity).
2. The η curves and the three-band verdicts of the relativistic group and the low-speed phenomenological group are **pointwise identical**. The grouping is still run and concluded separately as required by the task, but "this criterion has no discriminating power with respect to wall velocity" must be stated explicitly—it cannot be used to distinguish the physical pictures of the two wall-velocity groups.
3. α (the coupling in Z=e^{αφ/v}) enters only interface transmission (P3 §4 Fresnel), not the KK mode-freezing criterion. Therefore "the η=1 critical point is stable with respect to α" is a tautology and does not constitute a test of the form of Z(φ).

---

## 4. Four Outputs

### Output 1: Family of Full-Trajectory η(t) Curves

`DCC_P3_C5_eta_curves.png`: 20 p_z facets, each with 3 β_C curves and an η=1 reference dashed line. All curves are seen to decrease monotonically, with at most one η=1 crossing.

### Output 2: η_max Contours in the (p_z, α) Plane + Three-Region Coloring

`DCC_P3_C5_eta_max_contour.png`: three β_C slices; the η=1 contour is a red vertical line; green = robustly adapted (η_max<0.9), light red = robustly destroyed (η_min>1.1, empty in this scan), gray = no-discriminating-power band (0.9≤η≤1.1). The vertical contours show visually that the α-drift is 0.

### Output 3: Verdict Table

`DCC_P3_C5_judgement_table.csv`: 2 wall-velocity groups × 600 parameter points = 1200 rows; columns include wall_group, group_label, p_z, alpha, β_C, η_max, η_min, t_cross, η(t0), verdict. Every row of the low-speed group has group_label = phenomenological assumption, not a prediction.

### Output 4: η=1 Contour Drift

`DCC_P3_C5_contour_drift.txt`:

| β_C | p_z^* (η_max=1) | Drift with α | Drift with β_C (relative to −1/2) |
|---|---|---|---|
| −1/2 | 0.500000 | 0 (constant) | Baseline |
| −1/3 | 0.333333 | 0 (constant) | −0.166667 (−33.33%) |
| −2/3 | 0.666667 | 0 (constant) | +0.166667 (+33.33%) |

**Interpretation**: The contour position is absolutely stable with respect to α, but sensitive to β_C—O(1) changes in β_C (−1/2↔−1/3↔−2/3) shift the critical p_z by about ±1/3. Thus "where the critical point lies" is determined by β_C (the contraction-exponent assumption), not by an intrinsic model constant.

---

## 5. Interpretation Summary (Per Group × Per β_C, 200 Points)

| Wall-Velocity Group | β_C | Adapted | Destroyed | No Discriminating Power |
|---|---|---|---|---|
| Relativistic (dynamical solution) | −1/2 | 45% | 0% | 55% |
| Relativistic (dynamical solution) | −1/3 | 55% | 0% | 45% |
| Relativistic (dynamical solution) | −2/3 | 35% | 0% | 65% |
| Low-speed (**phenomenological assumption, not a prediction**) | −1/2 | 45% | 0% | 55% |
| Low-speed (**phenomenological assumption, not a prediction**) | −1/3 | 55% | 0% | 45% |
| Low-speed (**phenomenological assumption, not a prediction**) | −2/3 | 35% | 0% | 65% |

The η=1 crossing window (t_cross∈[t0,30t0]) corresponds to p_z∈[p_z_lo, |β_C|]:
β_C=−1/2 → [0.003043, 0.500000]; −1/3 → [0.003576, 0.333333]; −2/3 → [0.002302, 0.666667].
The lower end of axis A, 0.1, lies in the crossing window ⇒ within the default interval, p_z≲|β_C| gives crossing/no discriminating power and p_z≳|β_C| gives robust adaptation; **the robustly destroyed region is empty within the default p_z interval** (it would require an extremely small p_z giving η_min>1.1, beyond axis A).

---

## 6. Item-by-Item Check against Acceptance Criteria

| Criterion | Result |
|---|---|
| Reproducibility: two runs byte-for-byte identical | PASS (no differences in stdout/CSV/drift-table diff; NPZ md5 identical; PNG md5 identical across the two runs) |
| Regression: error at the freezing point η=1.0 below numerical precision | PASS (error 0, threshold 1e−12) |
| Unit consistency: explicit declaration + dimensional assertion | PASS (c=ħ=1, [t]=[x]=M⁻¹, [p_z]=M, [A,B,C]=M⁰ ⇒ [η]=M⁰) |
| Front-page honesty boundary | PASS (front page of this report + first line of the stdout archive) |
| Input file paths + hashes, no hard-coded background values in the script | PASS (importlib/NPZ/text reads) |
| Out-of-range β_C flagged red and discarded | PASS (probes 0/+0.5/−1.5/−2 all flagged red) |
| Separate groups and low-speed-group label | PASS |

---

## 7. Conclusion-Level and External-Statement Revisions (Core Deliverable of This Round)

### 7.1 Termination-Condition Verdict

- Condition 1, "a robustly adapted or robustly destroyed region occupies the majority → close out and give a conditional conclusion": **holds**—the robustly adapted region is the only region with definite verdicts, accounting for 35–55% (and reaching 55% in the β_C=−1/3 slice); the η=1 contour is a single vertical line that does not traverse the whole (p_z,α) interval.
- Condition 2, "η=1 traverses the whole reasonable interval with no robust region → not discriminable, register D3 dependency": **does not hold**—a robust region exists and the contour does not traverse the interval.

⇒ **This task is closed. A conditional conclusion may be given externally**, which must carry: the specified-contraction-background label, the D3-not-achieved label, the low-speed-group phenomenological label, and the given-p_z qualification.

### 7.2 Revision of the External Statement "Critical = 1"

The scan shows that **η=1 is only one crossing point in the monotonically decreasing η(t)**: at the freezing point (p_z=0.5, β_C=−1/2), t_cross=t0, meaning η<1 over the whole interval starting at t0; changing β_C or the normalization shifts the critical p_z by ±1/3; changing p_z shifts the crossing time.

- **Withdrawn original statement**: "The current parameters are exactly at the critical point (η=1)", which implied that criticality is an intrinsic property of the model.
- **Reason for withdrawal**: The position of η=1 is determined by parameter choices (β_C, C0/t0, the representative p_z) and is completely insensitive to α and wall velocity; it is not an intrinsic critical point.
- **New statement (may be signed off externally, with the above qualifications)**:
  > Under the specified contraction background (D2, not D3), the adiabatic criterion η=|β_C|C/(p_z t) gives: the critical point is not an intrinsic model constant but a product of parameter choices; under O(1) parameter changes (β_C∈[−2/3,−1/3], p_z∈[0.1,2]) the model can give robust conclusions—for p_z≳|β_C| the p_z≠0 tower freezes robustly and adiabatically (adapted); for p_z≲|β_C| there is a non-adiabatic crossing segment with η>1, while the robustly destroyed region is empty within the reasonable interval. This criterion has no discriminating power with respect to α or wall velocity.

### 7.3 If D3 Is Achieved

This scan must be rerun with the true dynamical C(t); β_C will no longer be freely scanned but determined by the D3 solution; at that point the statement in §7.2 must be rechecked.

---

## 8. Deliverables Checklist

| File | Content |
|---|---|
| `DCC_P3_C5_adiabatic_scan.py` | Scan script (newly added, following the DCC_P3_* naming convention) |
| `DCC_P3_C5_adiabatic_scan_stdout.txt` | stdout archive (including version hashes, prerequisites, regression, acceptance) |
| `DCC_P3_C5_eta_curves.png` | Output 1 |
| `DCC_P3_C5_eta_max_contour.png` | Output 2 |
| `DCC_P3_C5_judgement_table.csv` | Output 3 |
| `DCC_P3_C5_contour_drift.txt` | Output 4 |
| `DCC_P3_C5_adiabatic_scan_data.npz` | Machine-readable full dataset |
| `DCC_P3_C5_Scan_Report_v1.md` | This report |

---

*Content generated by AI*
