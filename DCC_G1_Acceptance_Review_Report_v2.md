# DCC Project G1 Acceptance Review Report v2.0 (Merged Revised Edition)

**Project**: Dimensional Collapse Conjecture (macroscopic dimensional phase transition model)
**Document Type**: Stage Acceptance Review Record (Decision Gate Review)
**Version**: G1-Review **v2.0** (merged revised edition, supersedes v1.0)
**Date**: 2026-11-19
**Superseded File**: `DCC_G1_Acceptance_Review_Report.md` (G1-Review v1.0)
**Merged Sources**: This report v1.0 (internal independent recalculation review) + third-party theoretical review comments (P1 results verification)
**Review Target**: P1 deliverables (`DCC_P1_bubble_wall.py`, `DCC_P1_p1a_wall_evolution.png`, `DCC_P1_p1b_terminal_velocity.png`, `DCC_P1_results.txt`)
**Review Basis**: `DCC_P0-P4_Roadmap_Plan.md` §3 / §4.4 / §5 / §6.3 / §6.5 / §9 / §13 / §14; `DCC_Covariant_Reconstruction_v1.md` (frozen metric, action, and sign conventions)
**Review Method**: Based on numerical results submitted by P1 + independent analytic recalculation (source files not accessed; they are not in this workspace); all recalculation formulas are in Appendix A and can be reproduced with one click

---

## 0. Acceptance Conclusion (Verdict First)

| Gate | Verdict | Notes |
|---|---|---|
| **G1 (P1a bubble wall solver)** | **Pass** | Wall position / wall velocity / wall thickness / energy residual / wall tension all five meet the criteria; two physically independent observables (integral-type σ_w, geometric-type δ) simultaneously agree with analytic values to < 0.1%, constituting a cross-validation of the solver. **New**: the pointwise residual of the BPS local relation is analytically 0; recommended as the 7th acceptance indicator (§2.3) |
| **G1 (P1b terminal velocity)** | **Conditional Pass** | Low-velocity group (η ≥ 0.05) is robust and usable, β_w ∝ 1/η scaling law holds; **the relativistic group (η ≤ 0.01) is a saturation artifact of the non-relativistic model and must be recomputed**; **the friction calibration at 42.47 km/s is wrong by about a factor of 75 (should be η ≈ 74.8), and this point is an extrapolation outside the scanned interval, beyond the weak-dissipation domain of applicability** |
| **Overall G1 verdict** | **Conditional Pass** | σ_w, δ, and the wall profile are allowed as P2 initial-data inputs. Closure conditions are A1–A5 in the §11 checklist; **among these, A1/A2/A3/A5 belong to P1's own closeout and do not block P2 initiation** |
| **G2 (P1b → P2)** | **Conditional Pass** | Terminal-velocity phase diagram completed, low-velocity group identity clarified (phenomenological assumption); however, the §5.2 requirement "determine whether the friction parameter falls within the controllable range of the effective theory" is **judged not satisfied** (η/(λv⁴) ≈ 75); accordingly G2 can only pass with qualifications |
| **G3 (P0 → P2, L1/L2)** | **Still not passed — remains the sole blocking item for the entire project** | Completion of P1 **does not release** G3. The closure action is clearly defined as A4 (§8), and **does not require full ADM**; it can be completed within the P1 framework |

**Relationship to the third-party review**: The two sides agree on all core numerical conclusions (§1 point-by-point verification table). On the basis of the third-party review, this report adds three items that must be addressed—(i) the **controllability verdict** for η ≈ 75 (not merely changing a number); (ii) the P1a magnetic-source extension must be **split into two things**, one of which cannot be DEFERRed to P2; (iii) the third party's P2 monitoring quantities use an old notation already deprecated in v1.0; copying it would cause a **contraction-axis mismatch**.

---

## 1. Consistency Check Between the Two Review Sources

| Verdict Item | Third-Party Review | This Report v1.0 | Independent Recalculation (This Round) | Conclusion |
|---|---|---|---|---|
| Target β_f | 1.416×10⁻⁴ | 1.4166×10⁻⁴ | **1.41665×10⁻⁴** | Consistent ✅ |
| Inverted F_drive | ≈ 0.0106 | ε = 0.0106 | First three rows η·β_w constantly 0.01060 | Consistent ✅ |
| **η_target** | ≈ 74.9 | ≈ 74.8 | **74.82** | Consistent ✅ |
| Actual velocity corresponding to η = 1 | 0.011c | ≈ 3300 km/s | **3297.7 km/s** | Consistent ✅ |
| Non-relativistic equation cannot describe η→0 | Yes (velocity upper-limit cutoff) | Saturation artifact, not a physical prediction | Consistent | Consistent ✅ |
| Relativistic reformulation | d(σγv)/dt = F − F_fric | v = (F/η)/√(1+(F/η)²) | η=0.01 → **0.7274**; η=0.001 → 0.9956 | Consistent ✅ |
| Deviation in η ≥ 0.05 interval | — | ≤ 2% | Max 2.2% (η=0.05) | Consistent ✅ |
| Insufficient evidence for convergence order | Yes (only 2 points) | Yes (Richardson needed) | Apparent order **4.03**, inconsistent with second-order leapfrog | Consistent ✅ |
| σ_w needs analytic verification | Suggested adding integral | **Added** 2√(2λ)v³/3 = 0.942809 | 0.942809 | Consistent ✅ |
| Pointwise check of BPS local relation | **Raised by third party** | Not mentioned in v1.0 | Analytic residual **3.7×10⁻¹³** (i.e., 0) | Adopted, see §2.3 |
| Six-tier itemized acceptance table | **Raised by third party** | v1.0 only "conditional pass" | — | Adopted, see §3 |
| G1 | Conditional Pass | Conditional Pass | — | Consistent ✅ |
| Positioning of 42.47 km/s | Phenomenological assumption, positioning unchanged | Must not be described as a theoretical prediction | — | Consistent ✅ |
| P1a magnetic-source extension | **DEFERRED (left to P2)** | **Attribution incomplete, should be moved forward** | See §8 split ruling | **Substantive disagreement** |

**Two points provided by the third party beyond v1.0 and already adopted**:

1. **Pointwise check of the BPS local relation** (one tier stronger than integral-type σ_w; integration can cancel errors against each other, pointwise residuals cannot);
2. **Six-tier itemized acceptance table** (PASS / INCOMPLETE / CONDITIONAL / NEEDS FIX / NOT VALIDATED / DEFERRED), more actionable than a single "conditional pass".

---

## 2. P1a Independent Recalculation: Strong Evidence for Solver Correctness

### 2.1 Analytic Benchmark

For the double-well potential frozen in roadmap §5.1 (taking the static-wall limit with tilt term ε → 0):

$$V(\phi)=\frac{\lambda}{4}\left(\phi^2-v^2\right)^2$$

The kink analytic solution is $\phi=v\tanh(ax)$, $a=v\sqrt{\lambda/2}$; the analytic wall tension and thickness are:

$$\sigma_w=\frac{2\sqrt{2\lambda}\,v^{3}}{3},\qquad \delta_{0.9}=\frac{2\,\mathrm{artanh}(0.9)}{a}$$

**Recalculation results (λ = v = 1)**:

| Quantity | Analytic Value | Numerical Quadrature Check | P1 Reported Value | Deviation |
|---|---|---|---|---|
| $a$ (inverse wall thickness) | 0.707107 | — | — | — |
| $\sigma_w$ | **0.942809** | 0.942809 | 0.942 | < 0.1% |
| $\delta_{0.9}$ | **4.164066** | — | 4.167 | < 0.1% |

### 2.2 Interpretation

1. Two **physically independent** observables (integral-type wall tension, geometric-type wall thickness) simultaneously agree to within 0.1% for the same parameter set λ = v = 1—this cannot be achieved by parameter tuning; it constitutes a **cross-validation** of the leapfrog scheme, boundary treatment, and φ=0 interpolation tracking. The P1a solver is judged correct.
2. The wall-thickness definition (−0.9v → +0.9v) is consistent with the analytic formula, indicating that "δ = 4.164" is an analytic benchmark rather than a fitted value; the half of acceptance criterion §5.1-1 stating "agrees with the analytic result" is **satisfied**.
3. Energy residual 8.75×10⁻⁷ < 10⁻⁶, wall position and wall velocity ≈ 0 (no drift for a static wall), no accumulation of grid noise—acceptance criteria 2 and 3 of §5.1 pass.
4. σ_w = 0.9428 and δ = 4.164 are delivered together, satisfying acceptance criterion 4 of §5.1. **These two items + the wall profile are the entirety of P1's valid output to P2.**

### 2.3 New 7th Acceptance Indicator: Pointwise Residual of the BPS Local Relation (Adopted from Third Party)

For a static kink, the first-order equation in BPS form gives a pointwise identity:

$$\frac12(\partial_x\phi)^2 = V(\phi)-V_{\min}$$

For $V=\frac{\lambda}{4}(\phi^2-v^2)^2$, $\phi=v\tanh(ax)$, $a=v\sqrt{\lambda/2}$, both sides are $\frac{\lambda v^4}{4}\,\mathrm{sech}^4(ax)$, **strictly equal analytically**. In this round, numerical verification on 25 grid points gives a maximum relative residual = **3.7×10⁻¹³** (machine-precision level).

**Therefore it is recommended to list the following as the 7th acceptance indicator for P1a** (one tier stronger than integral-type σ_w):

$$\mathcal R_{\rm BPS}=\max_x\frac{\left|\tfrac12(\partial_x\phi)^2-\left(V(\phi)-V_{\min}\right)\right|}{V(\phi)-V_{\min}}<10^{-6}$$

Rationale: integral-type σ_w allows positive and negative errors to cancel each other, whereas pointwise residuals do not; it can simultaneously detect scheme errors, interpolation errors, and errors in the potential implementation.

---

## 3. Six-Tier Itemized Acceptance Table (Adopting the Third-Party Format, with Items Added This Round)

| # | Acceptance Item | Tier | Recommended Handling | Assigned Action |
|---|---|---|---|---|
| 1 | P1a static-wall analytic consistency (σ_w, δ) | **PASS** | Retain, use as P2 initial data | — |
| 2 | P1a energy conservation (8.75×10⁻⁷ < 10⁻⁶) | **PASS** (per current threshold) | Retain, but the E_res definition must be added | A3 |
| 3 | P1a wall-thickness verification (error < 0.1%) | **PASS** | Retain | — |
| 4 | P1a BPS pointwise residual R_BPS | **PASS** (analytically 0; numerical test pending) | Add as the 7th acceptance indicator | A5 |
| 5 | P1a convergence order | **INCOMPLETE** | Add 3rd and 4th resolutions + separated Δt/Δx scan | A3 |
| 6 | P1a wall-tension analytic check | **PASS** (0.942809, closed this round) | CONDITIONAL from v1.0 lifted | — |
| 7 | P1b collective-coordinate model (phenomenological level) | **PASS** | Retain, must be labeled as a phenomenological model | A5 |
| 8 | P1b low-velocity parameter calibration (42.47 km/s) | **NEEDS FIX** | Correct to η ≈ 74.8 and label as out-of-interval extrapolation | A1 |
| 9 | P1b friction-parameter controllability (§5.2 requirement) | **FAIL** | η/(λv⁴) ≈ 75 exceeds the weak-dissipation domain of applicability, judged uncontrollable | A1 |
| 10 | P1b relativistic velocity description | **NOT VALIDATED** | Recompute and replot with relativistic momentum; not a physical prediction | A2 |
| 11 | Friction-law reference-frame declaration | **MISSING** | Declare v as the wall velocity in the plasma rest frame | A5 |
| 12 | Deliverable metadata (parameters/grid/boundaries/definitions) | **MISSING** | Complete the metadata table | A5 |
| 13 | Magnetic-source-driven **wall motion** (φ ↔ F ↔ g three-system coupling) | **DEFERRED** | Left to P2 (agreeing with third party) | P2 |
| 14 | **Solvability** of the Maxwell constraint system on a fixed background (L1/G3) | **NOT DONE** | **Move forward to P1 closeout**, do not DEFER | **A4** |

> **Tier definitions**: PASS = passed; INCOMPLETE = insufficient evidence but the result is not necessarily wrong; CONDITIONAL = conditional pass; NEEDS FIX = contains an error that must be corrected; NOT VALIDATED = the current method cannot yield a valid conclusion; DEFERRED = explicitly postponed with an assigned stage; MISSING = item absent from deliverables; FAIL = judged not to satisfy the acceptance criterion.

---

## 4. Required Fix A1: Friction Calibration Error at 42.47 km/s (~75×) + Controllability Verdict

This is the **only substantive numerical error** found in this round of review; it directly affects the parameter calibration of the "low-velocity front hypothesis group" in the roadmap §5.2 resolution table.

### 4.1 The Force Law Itself Is Correct

Computing η·β_w row by row from the P1b table:

| η | β_w (reported) | η·β_w |
|---|---|---|
| 0.05 | 0.212 | 0.01060 |
| 0.10 | 0.106 | 0.01060 |
| 0.20 | 0.053 | 0.01060 |
| 0.50 | 0.021 | 0.01050 |
| 1.00 | 0.011 | 0.01100 |

η·β_w is strictly constant at 0.0106 for the first three points—indicating that the numerical implementation strictly conforms to v_term = F_drive/η, and **F_drive = ε = 0.0106**. This is completely consistent with the collective-coordinate theoretical value F_drive = ΔV_vac (see the normalization discussion in §4.4). **P1b's force law itself is correct and internally self-consistent.**

### 4.2 Calibration Error

Target β_f = 42.47 km/s ÷ c = 42.47/299792.458 = **1.41665×10⁻⁴**; inverting gives

$$\eta_{\rm target}=\frac{\varepsilon}{\beta_f}=\frac{0.0106}{1.41665\times10^{-4}}=\boxed{74.82}$$

The report states "η ≈ 1.0". Comparing with the report's own table: η = 1.0 gives β_w = 0.011, i.e., **v ≈ 3298 km/s**, differing from 42.47 km/s by a factor of **74.8 (nearly 2 orders of magnitude)**.

### 4.3 Controllability Verdict (Not Elaborated by Third Party; This Report Judges FAIL)

The third party's proposed handling is "correct the results file, phase diagram, and text description". **This handling is insufficient**—it would launder an uncontrollable parameter into a "numerically correct" uncontrollable parameter. A verdict must be added:

- The target point η ≈ 74.8 lies **outside** the scanned interval [0, 1], being an **extrapolation** rather than a measurement;
- In natural units (λ = v = 1), η has dimensions of M⁴, and **η/(λv⁴) ≈ 74.8**. The premise of the collective-coordinate model is that "friction does not change the internal structure of the wall" (weak dissipation); η/(λv⁴) ~ 10² is far beyond the domain of applicability of this premise;
- The roadmap §5.2 acceptance criterion explicitly requires "determining whether it falls within the controllable range of the effective theory"—**this item is judged not satisfied (FAIL)**.

**Therefore the correct formulation for the low-velocity group should be**:

> 42.47 km/s cannot be realized within the friction parameter space of the current effective theory; reaching this velocity requires a strong-dissipation extrapolation with η/(λv⁴) ≈ 75, beyond the controllable range of the collective-coordinate phenomenological model.

This is **consistent in direction with** the existing roadmap §5.2 resolution (which forbids describing it as a theoretical prediction) **and upgrades the "prohibition" to "unrealizable within the current theoretical framework"**—a stronger conclusion than v1.0.

### 4.4 Incidental Finding: Tilt-Term Normalization and ε_c Self-Consistency (New This Round; Source Files Must Be Checked)

The potential prototype given in roadmap §5.1 is

$$V(\phi)=\frac{\lambda}{4}(\phi^2-v^2)^2+\epsilon\,\frac{\phi}{2v}$$

With this normalization, the energy-density difference between the two vacua is ΔV_vac = ε (consistent with the inverted F_drive = ε = 0.0106 in §4.1 ✅). But under the same normalization, the spinodal critical slope should be

$$V'=0,\ V''=0\ \Rightarrow\ \phi_s=\frac{v}{\sqrt3},\qquad \varepsilon_c=\frac{4\lambda v^{3}}{3\sqrt3}=\mathbf{0.7698}$$

However, both the v1.0 report and the third party cite ε_c = 0.3849 = 2λv³/(3√3), a value corresponding to a tilt term of **εφ/v** (in which case ΔV_vac = 2ε ≠ ε). The two normalizations **cannot both hold**.

| Tilt-Term Convention | ΔV_vac | ε_c | ε/ε_c | Self-Consistent with Inverted F_drive = 0.0106? |
|---|---|---|---|---|
| εφ/(2v) (roadmap §5.1 original text) | ε | **0.7698** | **1.38%** | ✅ Self-consistent |
| εφ/v | 2ε | 0.3849 | 2.75% | ❌ Contradicts F_drive = ε |

**Handling**: The physical conclusions are unaffected (under both conventions ε/ε_c ≪ 1, and the §5 verdict likewise passes), but the **archived numbers must be unified**. Require the A5 metadata table to explicitly state the actual implementation of the tilt term in the P1 source code, and accordingly correct ε_c and ε/ε_c to **0.7698 / 1.38%** (if the source code indeed uses εφ/(2v)).

### 4.5 Required Action A1

Add a scan over η ∈ {1, 3, 10, 30, 75, 100, 300}, providing the full-range β_w(η) curve; mark on the plot the intersection of the horizontal line β_f = 1.42×10⁻⁴ with η ≈ 74.8, and **use shaded regions to mark the measured interval [0,1] and the extrapolated interval [1, ∞)**; update the calibration conclusion in `DCC_P1_results.txt` and the controllability verdict in §4.3.

---

## 5. Required Fix A2: The P1b Relativistic Group Is a Saturation Artifact of the Non-Relativistic Model

The collective-coordinate equation used is

$$\sigma\,\frac{dv}{dt}=F_{\rm drive}-\eta_{\rm eff}\,v$$

is of **non-relativistic** form. The v_term = F/η it gives is necessarily truncated to 1 by the program when F/η ≳ 1—therefore β_w = 1.000 (η=0) and β_w = 0.999 (η=0.001, 0.01) in the report **are not physical predictions, but outputs of the saturation cutoff**. Roadmap §5.2 requires "a relativistic bubble-wall experimental group must be set up at the same time"; currently this group has no valid results.

**Correction**: change the momentum to the relativistic form σ·d(γv)/dt = F − η v; the terminal condition gives γv = F/η, i.e.,

$$v_{\rm term}=\frac{F/\eta}{\sqrt{1+(F/\eta)^2}},\qquad F=\varepsilon=0.0106$$

| η | Reported Value (Non-Relativistic, Truncated) | Relativistic Corrected Value | Deviation |
|---|---|---|---|
| 0.001 | 0.999 | **0.9956** | Truncation artifact, must be recomputed |
| 0.01 | 0.999 | **0.7274** | **Severely distorted (reported value inflated by 37%)** |
| 0.05 | 0.212 | 0.2074 | 2.2% |
| 0.10 | 0.106 | 0.1054 | 0.6% |
| 0.20 | 0.053 | 0.0529 | 0.2% |
| 0.50 | 0.021 | 0.0212 | < 0.1% |
| 1.00 | 0.011 | 0.0106 | 3.8% (reported value includes rounding) |
| 74.82 | — | 1.42×10⁻⁴ | Low-velocity target point (extrapolation, see §4.3) |

**Interpretation**:

- In the η ≥ 0.05 interval the deviation between the two is ≤ 2.2%; **the low-velocity-group conclusion is robust**, and the β_w ∝ 1/η scaling law holds and is usable.
- In the η ≤ 0.01 interval the reported values are unusable. **The qualitative conclusion "no friction → wall accelerates and asymptotically approaches the speed of light" still holds** (v_term → 1 as η → 0), but the phase diagram must be replotted with the corrected formula, and β_w at η = 0.01 must be changed from 0.999 to **0.727**.
- **Reference-frame declaration (required by both third party and v1.0; upgraded this round to a mandatory A5 deliverable)**: the v in the friction law σ d(γv)/dt = F − η v must be the wall velocity in the **plasma rest frame**. The current report does not declare a reference frame; if not written clearly, the P4 rendering stage will mix Doppler factors across frames (using the plasma-frame wall velocity as the Earth-observed frame velocity).

**Required action A2**: recompute and replot the P1b phase diagram with the corrected formula (horizontal axis η logarithmic, vertical axis β_w logarithmic, overlay both non-relativistic and relativistic curves, marking the separation point F/η ~ 1); state the reference-frame convention in the figure caption and results; change the η=0 row to the annotation "analytic limit v→1" instead of a numerical output.

---

## 6. Validity Check: Wall Structure Not Destroyed by the Driving Force (Passed; Must Be Archived)

The premise of the collective-coordinate approximation is that "the wall maintains a rigid kink shape under driving". This requires quantitative verification: the **depinning (spinodal) critical slope** of the tilted potential is given by V′ = V″ = 0, φ_s = v/√3. With the roadmap §5.1 tilt-term normalization (εφ/2v):

$$\varepsilon_c=\frac{4\lambda v^{3}}{3\sqrt3}=0.7698$$

while the actual ε = 0.0106, i.e., **ε/ε_c = 1.38% ≪ 1** (if the source code uses εφ/v normalization, it is 0.3849 / 2.75%; the conclusion is the same under both conventions, see §4.4).

**Interpretation**: The potential tilt is far from reaching the spinodal, the false vacuum has not been washed out, and the internal structure of the kink is essentially undeformed; therefore (i) the linear force law F_drive = ε is valid; (ii) substituting the P1a static wall's σ_w = 0.9428 into the dynamical equations is self-consistent. **This is the sole supporting evidence for the credibility of the P1b low-velocity-group results; it was not mentioned by the third party, and this report requires it to be written into the archive.**

---

## 7. Required Supplement A3: Insufficient Convergence Evidence (Evidence Gap in G1 Acceptance Criterion 1)

The report states: E_res drops from 8.75×10⁻⁷ to 5.37×10⁻⁸ (Δx halved), giving an apparent convergence order

$$p=\frac{\ln(8.75\times10^{-7}/5.37\times10^{-8})}{\ln 2}=4.03$$

**Problems**:

1. There are only 2 resolution points, insufficient to give a convergence order (the report honestly marked it as None)—roadmap §5.1-1 requires "convergence order ≥ 2"; **the current evidence only supports "at least 2nd order", so no tier can be assigned**. The third party and this report agree.
2. The apparent 4.03 order **does not match** the second-order leapfrog scheme and must be explained; otherwise it may be a residual-definition issue rather than a scheme advantage. The three most likely causes are:
   - The residual is dominated by **initial-data discretization error** (interpolation/truncation error of the kink profile on the grid) rather than evolution error—in which case it does not reflect the scheme's order;
   - leapfrog is a **symplectic scheme**, with bounded oscillating energy error and no drift; the residual within a short time window may exhibit higher-order cancellation;
   - Δt and Δx are halved simultaneously, mixing the two errors so they cannot be separated.
3. **Energy residual ≠ solution error** (emphasized by the third party): E_res is jointly affected by initial conditions, Δt, boundary absorption, residual definition, and error cancellation; convergence order cannot be claimed on its basis alone.

**Required action A3**:

- Add third and fourth resolutions (Δx/4, Δx/8), determine order by three-point Richardson extrapolation;
- **Separated time-step convergence test**: fix Δx and scan Δt (reporting the CFL number), then fix Δt and scan Δx;
- **Determine the order separately for wall position x_w, wall thickness δ, and wall tension σ_w** (third-party requirement); order cannot be determined only for E_res—different observables may have different orders;
- Clarify the definition of E_res (is it max_t |E(t)−E(0)|/E(0) or the final value? Does the integration interval include contamination from boundary reflections?);
- Report the composition of the total energy E (gradient + potential + boundary-flux correction term), confirming that no boundary leakage is mistakenly counted as "conservation".

---

## 8. Ruling on the Substantive Disagreement: The P1a Magnetic-Source Extension Must Be Split into Two Things

The third party judges **DEFERRED (left to P2)**, on the grounds that it has become a φ ↔ F_{μν} ↔ g_{μν} three-system coupling requiring a constraint-preserving framework first. v1.0 judges the **attribution incomplete and that it should be moved forward to P1 closeout**.

**The root of the disagreement is that two things have been mixed into one; separating them removes the conflict:**

| | Content | Mathematical Nature | ADM Needed? | Assignment |
|---|---|---|---|---|
| **(a)** Magnetic-source-driven **wall motion** | φ is driven by Z′F² and reacts back on geometry; nonlinear three-system coupling | Nonlinear hyperbolic + Einstein coupling | **Yes** | This is what the third party DEFERRed → **this report agrees** |
| **(b)** **Solvability** of the Maxwell constraint system on a fixed background | Given the already-computed φ(t,x) profile (Minkowski, N=A=B=C=1), evolve ∂_t f − ∂_x E = 0 and ∂_t(ZAC E/N) − ∂_x(ZNC f/AB) = 0 | **Linear** hyperbolic system, background does not react back | **No** | This is what v1.0 moved forward → **missed by the third party** |

**(b) is precisely the closure action for G3 in roadmap §13**—"prove that the inhomogeneous Maxwell constraint system has nontrivial solutions on the bubble-wall background" (corresponding to the §4.4 leftover item **L1**). It is a linear initial-boundary-value problem, costing about 1.5× that of P1a.

**Consequence (the reason this split is necessary)**: If the entire magnetic-source problem were DEFERRed to P2 as the third party proposed, G3 could not be closed before P2 starts; and roadmap §9 explicitly states "P2 must not start full coupled evolution before L1 is closed"—together, these two rules would **lock the project at P1**. Therefore (a) can be DEFERRed, (b) cannot.

**On the attribution of "instability caused by the wall hitting the boundary"**: that is **reflection from a simple absorbing boundary**, unrelated to whether the Einstein equations are coupled; it is a numerical boundary problem, not a gravitational-constraint problem. The sourced (φ, f, E) system is first-order hyperbolic, and reflected waves hitting the wall cause growth—this would equally occur on a fixed Minkowski background. Therefore the attribution that "one must wait for P2's ADM framework to solve it" does not hold.

**The numerical scheme for action A4 (the G3/L1 closure task) is given in Appendix B.**

---

## 9. Required Correction: The Third Party's P2 Monitoring Quantities Use Deprecated Notation (Would Cause Contraction-Axis Mismatch)

Third-party §VI writes "P2 monitors B(t,x), A(t,x)" and formulates the target as B → 0. This is an **old convention from the P0 era** (when B was the contraction direction).

Covariant Reconstruction v1.0 and roadmap §14 have **frozen** it as:

$$ds^2=-N^2dt^2+A^2dx^2+B^2dy^2+C^2dz^2,\qquad A\!\to\!X,\ B\!\to\!Y,\ \boxed{C\!\to\!Z},\qquad \text{contraction target } C\to0$$

**If P2 is implemented verbatim as in the third-party text, the contraction direction would be written onto the Y axis—an axis mismatch**, with cascading contamination:

- $\mathcal R_L = C/A$ (relative scale) would be written as $B/A$;
- the direction label of the orthonormal-frame pressure $p_{\hat z}=-\rho$ would be wrong;
- the correspondence between $F_{xy}=f$ (magnetic field along $\hat z$) and the contraction direction would be wrong—this is the landing point of all of P0's directional arguments.

**In addition, the third party's P2 monitoring checklist is missing three mandatory observables** (roadmap §6.3 has 7 items in total; the third party lists only $\mathcal H$ and $\mathcal M_x$):

| Symbol | Definition | Interpretation | Listed by Third Party? |
|---|---|---|---|
| $\mathcal R_H$ | $H_z/H_x$ | Anisotropic expansion rate (D1 criterion) | ❌ |
| $\mathcal R_L$ | $C/A$, $C/B$ (must convert to physical geodesic lengths) | Relative scale evolution | ❌ |
| $\mathcal K$ | $R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}$ | **Distinguish physical singularity from coordinate degeneration** | ❌ |
| $\mathcal E$ | $T_{\mu\nu}n^\mu n^\nu$ | Monitor whether ρ_B ∝ 1/Z or 1/C^n diverges | ❌ |
| $\mathcal C_H$ | $\max_x(\lvert\mathcal H\rvert,\lvert\mathcal M\rvert)$ | Constraint residual; results invalid if over threshold | ✅ (in the form of H, M_x) |
| $\mathcal B$ | $\max_x\lvert\partial_t f-\partial_x E\rvert$ | Bianchi constraint residual | ❌ |
| NEC/WEC | $T_{\mu\nu}k^\mu k^\nu\ge0$ etc. | Whether energy conditions must be violated to reach D3 | ❌ |

**Handling**: The P2 initiation document must be implemented according to the roadmap §14 symbol table and the §6.3 seven-item checklist; the third-party text's B→0 formulation must not be carried over. At the same time, the §6.4 tiered criteria must be retained verbatim: **the acceleration difference gives only D1; any "Z contraction" conclusion must reach at least D2 (H_z < 0)**.

---

## 10. Required Supplement A5: Archival Discipline and Metadata Gaps

`DCC_P1_results.txt` currently provides result values but lacks the following mandatory metadata, not satisfying roadmap §0 discipline clauses and §11 (sympy reproducibility / dimensional checks):

| Missing Item | Requirement |
|---|---|
| Parameter table | Specific values of λ, v, ε and **unit conventions** (natural units, v = 1 as baseline); **actual implementation of the tilt term** (εφ/2v or εφ/v, determining the ε_c value in §4.4); explicit form of Z(φ) and the Z > 0 check |
| Grid and time step | N_x, Δx, domain length L, Δt, CFL number, end time T, output interval |
| Boundary-condition type | Specific implementation at each end (absorbing / Sommerfeld parameters / periodic), and whether characteristic decomposition is included |
| Observable definitions | δ (−0.9v→+0.9v), x_w (φ=0 linear interpolation), integration interval and integrand of σ_w, definition of E_res, composition of E |
| Raw convergence-test data | E_res, x_w, δ, σ_w at all resolution points (for third-party recomputation of convergence order) |
| Friction-law reference frame | Declare v as the wall velocity in the plasma rest frame; dimensions and normalization of η (η/(λv⁴)) |
| Randomness / initial conditions | Analytic form of φ(0,x) and whether perturbations are added |

**Action A5**: Complete the above metadata tables and archive them together with the P1 deliverables. **P2 is to use the P1a wall profile as initial data; without metadata, integration is impossible** (roadmap §6.2 step 2).

---

## 11. Merged G1 Closure Checklist (8 Items, with Proposing Party and Closure Criteria)

| # | Action | Proposing Party | Priority | Closure Criterion |
|---|---|---|---|---|
| **1** | **A4: Close G3/L1** — fixed Minkowski background + existing φ(t,x); solve the (f,E) linear system and provide evidence of a nontrivial solution | This report (the third party's DEFER here needs correction per the §8 split) | **Highest; the only unlock for P2** | Output (f,E) time series, Bianchi residual B < 10⁻⁸, electromagnetic energy-conservation residual < 10⁻⁶, and explicit evidence of a nontrivial (not identically zero, not pure gauge) solution |
| **2** | **A1: Full-range η scan up to ~75**, **explicitly labeled as out-of-interval extrapolation + beyond the weak-dissipation domain of applicability** | Both parties (third party provides the numbers, this report adds the controllability verdict) | High | β_w(η) curve covers η ∈ [1,300], marking measured/extrapolated partitions and the η=74.8 intersection; write the conclusion "unrealizable within the current effective theory" into results |
| **3** | **A2: Relativistic recomputation and replotting** v=(F/η)/√(1+(F/η)²), 0.999 → **0.727** at η=0.01 | Both parties | High | New phase diagram + overlay of both curves + reference-frame declaration archived |
| **4** | **A3: Three/four-resolution Richardson**, **separated Δt/Δx scans**, give the E_res definition; determine order separately for x_w/δ/σ_w | Both parties | Medium | Convergence-order table (≥3 points) + orders of each observable + independent Δt scan |
| **5** | σ_w analytic check (**0.942809, closed this round**) + **new BPS pointwise residual R_BPS** | Raised by third party, analytic value supplied by this report | Medium | R_BPS < 10⁻⁶ numerical verification archived, listed as the 7th acceptance indicator |
| **6** | Label all of P1b as a "collective-coordinate phenomenological model", declare the friction-law reference frame | Both parties (reference frame supplied by this report) | Medium | Consistent in three places: figure caption + results + roadmap §5.2 |
| **7** | **A5: Complete metadata** (parameters/units/tilt-term convention/grid/CFL/boundaries/observable definitions/raw convergence data) | This report | Medium | §10 table filled in item by item; ε_c corrected to 0.7698 or 0.3849 per the actual convention |
| **8** | **Change P2 monitoring quantities to C→0 per §14**, complete the §6.3 seven observables (K, B, NEC/WEC, R_H, R_L, E) | This report (third-party notation needs correction) | **Prerequisite for P2** | P2 initiation document passes symbol review |

**G1 closure condition**: Completion of items 2–7 freezes the P1 baseline (all 4 closeout items listed by the third party are covered).
**P2 initiation condition**: Completion of item 1 (A4) + completion of the item 8 symbol correction. **The third party's 4 closeout items do not include item 1; following them would lock the project at P1.**

---

## 12. Status Update Patch for the Roadmap (Recommended to Write Directly into the Corresponding Sections)

### 12.1 §3 Global Phase Overview Table

| Item | Original Status | Updated |
|---|---|---|
| P1a | Not started | **Complete, G1 passed** (solver cross-validated against analytic benchmark; σ_w=0.9428, δ=4.164 can be fed directly to P2) |
| P1b | Not started | **Complete, G1/G2 conditional pass**; to become a formal pass after A1/A2 corrections |
| P2 | Not started | Still not started; prerequisites refined as "**L1 closed (moved forward to P1 closeout per A4) + L2 pending P2's first-round output + P1a complete + §14 symbol review passed**" |

### 12.2 §5.2 Resolution Table (Low-Velocity Front Identity Handling)

| Item | Original Formulation | **Corrected To** |
|---|---|---|
| Friction calibration | "η ≈ 1 can realize β_w ~ 10⁻⁴" | **η = 74.82** (inverted from ε=0.0106, β_f=1.41665×10⁻⁴) |
| Controllability | Not judged | **η/(λv⁴) ≈ 75, lying outside the scanned interval [0,1], an extrapolation beyond the weak-dissipation domain of applicability → judged unrealizable within the current effective theory** |
| Relativistic group | β_w ≈ 0.999 | **should be 0.727 at η=0.01**; recompute all η≤0.01; change the η=0 row annotation to "analytic limit" |
| Reference frame | Not declared | **v is the wall velocity in the plasma rest frame** (P4 rendering must convert accordingly) |

### 12.3 §13 Decision-Gate Table

| Gate | Original Verdict | **Updated** |
|---|---|---|
| G1 | Not assessed | **Conditional Pass** (closure conditions: A1, A2, A3, A5; BPS pointwise residual listed as the 7th acceptance indicator) |
| G2 | Not assessed | **Conditional Pass (with qualifications)**: phase diagram complete, identity clear, but the §5.2 "controllable range" item judged FAIL |
| G3 | Not passed (blocking item) | **Still the sole blocking item**; closure path clearly defined as **A4** (numerical experiment on Maxwell existence on a fixed background), **does not depend on ADM**, can be completed within the P1 framework |

### 12.4 §9 Dependency-Graph Correction

The original dependency graph hangs P2 after P1b, labeled "L1, L2 closed", but does not state that L1 can be closed within P1. Suggested revision:

```
P1a (fixed-background bubble wall)── complete, G1 passed
   ├── P1b (friction/terminal velocity)── conditional pass, pending A1/A2
   └── A4: Maxwell existence on fixed background (= L1 closed = Phase 2)── not started ← current highest priority
                      │
                      ▼
               G3 closed ──→ P2 (ADM coupled evolution, D1→D2→D3)
```

---

## 13. One-Sentence Summary

The two reviews are **consistent on all core numerical conclusions**: P1's core deliverables (a bubble-wall solver cross-validated against an analytic benchmark and meeting energy-conservation criteria, plus two inputs σ_w = 0.9428 and δ = 4.164 that can be fed directly to P2) are **of acceptable quality; G1 receives a conditional pass**; P1b has two items that must be corrected—**the friction calibration at 42.47 km/s is wrong by about a factor of 75 (should be η = 74.82, and is an out-of-interval extrapolation beyond the weak-dissipation domain of applicability)**, and **the relativistic group is a model saturation artifact (the true value at η = 0.01 is 0.727, not 0.999)**.

On the basis of the third party, this report adds three items that must be addressed: **(i)** η ≈ 75 is not merely "a wrongly written number"—the parameter itself is unusable; the roadmap §5.2 "controllable range" criterion should be recorded as **FAIL**, upgrading "forbidden to describe as a theoretical prediction" to "unrealizable within the current effective theory"; **(ii)** the P1a magnetic-source extension must be split into "wall motion (can be DEFERRed to P2)" and "solvability of Maxwell on a fixed background (cannot be DEFERRed)", the latter being precisely the G3/L1 closure action; DEFERring the whole thing as the third party proposed would interlock with roadmap §9's dependency clause and lock the project at P1; **(iii)** the third party's P2 monitoring quantities carry over the old B→0 notation deprecated in v1.0; copying it would write the contraction direction onto the Y axis; it must be changed to **C→0** per §14 and the §6.3 seven observables completed.

There is one additional internal-consistency issue newly identified this round: the roadmap §5.1 tilt term εφ/(2v) and the cited ε_c = 0.3849 **cannot both hold** (the former gives ε_c = 0.7698, ε/ε_c = 1.38%); the archived numbers must be unified after checking the source code—the physical conclusions are unaffected.

**The sole highest-priority action in the near term remains A4 (close G3/L1)**; do not start the full Einstein-coupled PDE solver until it is complete.

---

## Appendix A: All Recalculation Formulas in This Report (Independently Reproducible)

Potential $V=\frac{\lambda}{4}(\phi^2-v^2)^2$, kink $\phi=v\tanh(ax)$, $a=v\sqrt{\lambda/2}$, λ = v = 1:

- Inverse wall thickness: $a=\sqrt{\lambda/2}=0.707107$
- Wall tension: $\sigma_w=\int_{-\infty}^{\infty}\left[\tfrac12(\partial_x\phi)^2+V\right]dx=\dfrac{2\sqrt{2\lambda}\,v^3}{3}=0.942809$ (numerical quadrature gives the same value; P1 reports 0.942)
- Wall thickness (−0.9v → +0.9v): $\delta_{0.9}=2\,\mathrm{artanh}(0.9)/a=4.164066$ (P1 reports 4.167)
- BPS pointwise identity: $\tfrac12(\partial_x\phi)^2=V(\phi)=\dfrac{\lambda v^4}{4}\mathrm{sech}^4(ax)$; maximum relative residual over 25 grid points $=3.7\times10^{-13}$
- Driving-force inversion: $\varepsilon=\eta\beta_w$, first three rows of the P1b table give 0.01060 / 0.01060 / 0.01060 → $F_{\rm drive}=\varepsilon=0.0106$ (consistent with $\Delta V_{\rm vac}=\varepsilon$)
- Target velocity: $\beta_f=42.47/299792.458=1.41665\times10^{-4}$
- Friction calibration: $\eta=\varepsilon/\beta_f=0.0106/1.41665\times10^{-4}=74.82$; dimensionless $\eta/(\lambda v^4)=74.82$
- Actual velocity at η=1: $0.011\times c=3297.7\ \mathrm{km/s}$ (differs from 42.47 km/s by a factor of 74.8)
- Relativistic terminal velocity: $v=\dfrac{F/\eta}{\sqrt{1+(F/\eta)^2}}$ → η=0.001: 0.9956; η=0.01: 0.7274; η=0.05: 0.2074; η=0.10: 0.1054; η=0.20: 0.0529; η=0.50: 0.0212; η=1.00: 0.0106
- Spinodal critical slope ($V'=V''=0\Rightarrow\phi_s=v/\sqrt3$, slope $=-\tfrac{2\lambda v^3}{3\sqrt3}=-0.3849$):
  - Tilt term $\epsilon\phi/(2v)$ (roadmap §5.1 original text) → $\varepsilon_c=4\lambda v^3/(3\sqrt3)=0.7698$, $\varepsilon/\varepsilon_c=1.38\%$
  - Tilt term $\epsilon\phi/v$ → $\varepsilon_c=2\lambda v^3/(3\sqrt3)=0.3849$, $\varepsilon/\varepsilon_c=2.75\%$
- Apparent convergence order: $p=\ln(8.75\times10^{-7}/5.37\times10^{-8})/\ln2=4.03$ (only 2 points, insufficient to assign a tier, and inconsistent with a second-order scheme)

---

## Appendix B: Action A4 — Numerical Scheme for the G3/L1 Closure Task (Phase 2)

**Objective**: In the fixed-background limit of the locked metric, prove that the inhomogeneous Maxwell constraint system has nontrivial solutions on the bubble-wall background.

**Background**: Minkowski, $N=A=B=C=1$; $\phi(t,x)$ directly takes the wall profile already computed by P1a (including its slow evolution; if the wall is static, $\phi=\phi(x)$).

**Evolution system** (first-order linear hyperbolic, background does not react back):

$$\partial_t f-\partial_x E=0\qquad(\text{Bianchi})$$

$$\partial_t\!\left(\frac{Z(\phi)AC}{N}E\right)-\partial_x\!\left(\frac{Z(\phi)NC}{AB}f\right)=0\ \xrightarrow{\;N=A=B=C=1\;}\ \partial_t\!\left(ZE\right)-\partial_x f=0$$

Add the electric-flux constraint $\dfrac{ZBC}{AN}E=P=\text{const}$ (used for **verification**, not as an evolution equation).

**Recommended implementation**:

1. **Take $A_y(t,x)$ as the basic variable** (potential function), set $E=\partial_t A_y$, $f=\partial_x A_y$, then the Bianchi identity is **automatically satisfied**—this is the cleanest way to eliminate constraint drift (Covariant Reconstruction §3 also adopts this configuration).
2. Obtain the single second-order equation $\partial_t(Z\,\partial_t A_y)-\partial_x(\partial_x A_y)=0$, using a second-order leapfrog (same scheme as P1a, facilitating reuse of the verified solver skeleton).
3. **Boundaries**: switch to characteristic-decomposition outgoing conditions or Sommerfeld conditions $(\partial_t\pm c_{\rm eff}\partial_x)A_y=0$, or apply PML directly. **This is the true cause of the instability in the P1a magnetic-source case; the simple absorbing boundary must be replaced.**
4. **Driving**: take $Z(\phi)$ from the roadmap L4 candidates (e.g., $Z=e^{\alpha\phi/M}$, with an explicit check that $Z>0$); differing $Z$ on the two sides of the wall acts as a source, radiating nontrivial $(f,E)$.
5. **Control group**: $\alpha=0$ ($Z\equiv1$) should give a free-wave solution, serving as a scheme-correctness benchmark.

**Mandatory observables** (write into results and figures):

| Quantity | Definition | Threshold |
|---|---|---|
| $\mathcal B$ | $\max_x\lvert\partial_t f-\partial_x E\rvert$ | $<10^{-8}$ (should reach machine precision with the potential-function implementation) |
| Electric-flux residual | $\max_x\lvert ZBC\,E/(AN)-P\rvert/\lvert P\rvert$ | $<10^{-8}$ |
| Electromagnetic energy residual | $\lvert E_{\rm EM}(t)-E_{\rm EM}(0)\rvert/E_{\rm EM}(0)$ (positive definite for $Z>0$) | $<10^{-6}$ |
| Nontriviality criterion | $\max_{t,x}\lvert(f,E)\rvert$, and cannot be written as pure gauge $\partial_\mu\Lambda$ | Give explicit numerical value |
| Energy-injection rate | $\int Z'(\phi)\,\dot\phi\,(\cdots)dx$, reconciled with wall energy loss | Two-way conservation closure |

**Convergence**: two points Δx/2, Δx/4 suffice to demonstrate scheme convergence (a linear problem, with lower requirements than the P1a nonlinear case); CFL number and end time must be reported.

**Closure criterion**: all five items above meet their criteria → **L1 closed → G3 released → P2 obtains legitimate initiation conditions**.

**Cost estimate**: about 1.5× that of P1a (reusing the verified leapfrog skeleton + interpolation-tracking code, adding the $Z(\phi)$ coefficient and PML/Sommerfeld boundaries).

**Explicitly out of scope**: do not introduce the Einstein equations, do not evolve $A,B,C$, do not apply constraint damping—those belong to P2. This task only answers "whether the Maxwell sector has solutions on the bubble-wall background".

---

**End of document. This v2.0 supersedes G1-Review v1.0; where it conflicts with v1.0, this file takes precedence. Updates to roadmap §3 / §5.2 / §13 / §9 are to be executed per the §12 patch.**

---

Content generated by AI
