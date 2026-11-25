# DCC G1 Closeout Report (A1–A5 + A4/L1)

**Project**: Dimensional Collapse Conjecture
**Document Type**: Stage Closeout Report (G1 Closeout)
**Date**: 2026-11-19
**Basis**: `DCC_G1_Acceptance_Review_Report_v2.md` (hereinafter "the review report") §4–§11, Appendix B
**Code**: `DCC_P1_bubble_wall.py`, `DCC_P1_A4_maxwell_L1.py`
**Results**: `DCC_P1_results.txt`, `DCC_P1_A4_results.txt`, `DCC_P1_metadata.md`

---

## 0. Verdict

| Gate | Review Report's Original Verdict | This Report's Verdict | Basis |
|---|---|---|---|
| **G1 (P1a)** | Pass (item 7 pending test) | **Pass (frozen)** | Four-resolution order determination 2.00–2.01; $E_{\rm res}=1.17\times10^{-7}$; $\sigma_w$, $\delta$ deviate from analytic values by < 0.03% |
| **G1 (P1b)** | Conditional Pass (A1/A2 pending) | **Pass (with domain-of-applicability limitations)** | η scanned up to 300; relativistic recomputation; calibration/controllability archived as FAIL |
| **Overall G1 verdict** | Conditional Pass | **Pass** (A1, A2, A3, A5 all closed) | See §2 |
| **G2 (P1b→P2)** | Conditional Pass | **Pass (with qualifications)** | Phase diagram complete, identity clear; §5.2 "controllable range" item permanently recorded as FAIL and written into archive |
| **G3 (L1)** | **Not Passed (blocking item)** | **Closed (existence)** | A4: Bianchi $10^{-15}$, energy conservation $3.6\times10^{-10}$, nontrivial static solution $f=Q/Z$ discretely exact to $10^{-13}$ |

**In one sentence**: P1's numerical foundation can now be frozen; the L1 existence problem has been closed on a fixed Minkowski background, and the initiation blockage for P2 is removed.
The pre-initiation symbol review for P2 (E-1…E-8) has been completed in `DCC_Covariant_Reconstruction_v1.md` v1.1; the remaining work is to code the divergence form during P2 implementation.

---

## 1. Actions Covered by This Report

| # | Action | Status | Evidence Location |
|---|---|---|---|
| A1 | Full-range η scan up to ~75, labeling extrapolation and uncontrollability | ✅ | `results` §3; `DCC_P1_p1b_terminal_velocity.png` |
| A2 | Relativistic recomputation and replotting; 0.999→0.727 at η=0.01; reference-frame declaration | ✅ | `results` §3; figure caption |
| A3 | Three/four-resolution Richardson, separated Δt/Δx, per-observable order determination, $E_{\rm res}$ definition | ✅ | `results` §2; `DCC_P1_p1a_convergence.png` |
| A5 | Metadata table, BPS pointwise residual, reference frame | ✅ (including one indicator-definition recommendation) | `DCC_P1_metadata.md`; `DCC_P1_p1a_bps.png` |
| A4 | Maxwell existence on a fixed background (L1/G3) | ✅ | `DCC_P1_A4_results.txt` |
| §12 | Roadmap §3/§5.2/§9/§13 patches | ✅ | Roadmap v2.1 + revision history |
| §9 | Change P2 monitoring quantities to $C\to0$, complete the seven items | ✅ | `DCC_P2_Symbols_and_Observables_Checklist_v1.md` |

---

## 2. Key Results of A1/A2/A3/A5

### 2.1 A3: The Convergence Order Is Finally Clean (and Old Data Was Found to Be an Artifact)

The "apparent order 4.03" of the old report is not reproducible. Two inherited code errors were identified:

1. The time label used `t[:rec_idx]`, while recording was "once every N steps"—all time-series horizontal axes were compressed and wall velocities were entirely wrong;
2. The main loop stopped at `nt-2`, so the final state was actually $T-\Delta t$—final values systematically lagged by one step.

After correction, using a **boosted kink with an exact solution** ($u=0.5$) for order determination, the results are:

| Scan | L2 | $x_w$ | $\sigma_w$ | $\delta$ |
|---|---|---|---|---|
| Joint $\Delta t=0.5\Delta x$ | **2.01** | **2.01** | **2.00** | 1.65* |
| $\Delta x$ independent ($\Delta t=0.0025$) | **2.00** | **2.00** | **2.00** | 1.45* |
| $\Delta t$ independent (self-convergence difference) | **2.06** | — | — | — |

\* The error of $\delta$ crosses zero between $\Delta x=0.1\to0.025$, making the loglog fit meaningless; see metadata table §4.3.

Conclusion: the scheme is simply second-order convergent as a second-order leapfrog, consistent with theory. The 4.03 of the old report is an artifact of the time axis / final-state lag, **not a scheme advantage**.

Corrections made at the same time:

- Initial-velocity initialization omitted the Lorentz factor $\gamma$, and the initial profile used an uncontracted kink → energy error ~10%;
- Energy diagnostic used $(\phi^{n+1}-\phi^n)/(2\Delta t)$, underestimating kinetic energy by a factor of 4;
- "Analytic wall thickness 1.414" is $1/a$, which is not the same quantity as $\delta_{0.9}=4.164$.

### 2.2 A1/A2: η Calibration and Controllability

| Quantity | Value |
|---|---|
| $\beta_f$ | $42.47/299792.458=1.416647\times10^{-4}$ |
| $F_{\rm eff}=\epsilon/\sigma_w$ | 0.010607 |
| $\eta_{\rm target}=F_{\rm eff}/\beta_f$ | **74.87** (review report 74.82; 0.07% difference, from rounding $F$ to 0.0106) |
| Absolute friction $\eta_{\rm eff,target}$ | $74.87\,\sigma_w=70.59$ |
| $\eta/(\lambda v^4)$ | $\approx75$ → extrapolation, beyond the weak-dissipation domain of applicability |

- η=0.01: $0.999\to\mathbf{0.7276}$ (old value inflated by 37.3%);
- η=0: labeled "analytic limit $v\to1$", no longer a numerical output;
- η≥0.05: maximum NR–SR deviation 2.23% (at η=0.05), low-velocity-group conclusion robust;
- The phase diagram has been replotted as $\log\eta$–$\log\beta$, with shading distinguishing measured $[0,1]$ from extrapolated $[1,300]$.

**Archival formulation** (consistent with and stronger than review report §4.3):

> 42.47 km/s cannot be realized within the friction parameter space of the current effective theory; reaching this velocity requires a strong-dissipation extrapolation with $\eta/(\lambda v^4)\approx75$, beyond the controllable range of the collective-coordinate phenomenological model. This velocity belongs only to the low-velocity-front phenomenological hypothesis group.

### 2.3 A5: The BPS Indicator—A Threshold Issue That Must Be Clarified

The review report recommends listing
$$\mathcal R_{\rm BPS}=\max_x\frac{|\tfrac12(\phi')^2-(V-V_{\min})|}{V-V_{\min}}<10^{-6}$$
as the 7th acceptance indicator. This report tested three cases:

| Object | $\Delta x=0.05$ | Convergence Behavior |
|---|---|---|
| Analytic profile + analytic derivative | $1.3\times10^{-15}$ | Machine precision |
| Analytic profile + 6th-order difference | $7.5\times10^{-9}$ | 6th order |
| Analytic profile + 2nd-order difference | $1.17\times10^{-3}$ | 2nd order |
| **solver profile + 2nd-order difference** | $5.54\times10^{-4}$ | Limited by solution error |

**Conclusion**: The BPS identity holds strictly at the analytic level ($10^{-15}$), and the potential implementation is correct;
but treating $10^{-6}$ as an acceptance threshold for a **numerical profile** is unattainable with a second-order solver at $\Delta x=0.05$—
it measures the difference-operator error, not physical correctness. To use this threshold, one of two options must be chosen:

- (i) Define it on an analytic reference profile (currently passes, and can detect potential-implementation errors);
- (ii) Use ≥6th-order differences on the numerical profile, or refine the grid to $\Delta x\sim10^{-3}$.

**Recommendation**: retain the indicator but split it into two rows—"analytic identity (threshold $10^{-6}$)" and "numerical-profile convergence diagnostic (report the order, no absolute threshold)".
This report follows this approach and has not lowered the threshold without authorization.

---

## 3. A4 / L1: Maxwell Existence on a Fixed Background

### 3.1 Implementation

- Background: Minkowski, $N=A=B=C=1$; $\phi(x)=v\tanh(ax)$, $a=0.707107$.
- Fields: $A_y(t,x)$, $E=\partial_tA_y$, $f=\partial_xA_y$ → Bianchi automatically satisfied.
- Equation: $\partial_t(Z\partial_tA_y)-\partial_x(Z\partial_xA_y)=0$ (conservative flux form, face-averaged $Z$).
- Scheme: second-order leapfrog; boundaries: first-order Mur; Dirichlet for the static sector.
- Discrete energy uses the staggered-time form, strictly conserved for static $Z$.

### 3.2 Results

| Test | Value | Threshold | Verdict |
|---|---|---|---|
| Bianchi residual $\max|\partial_tf-\partial_xE|$ | $9.7\times10^{-16}$ | $<10^{-8}$ | PASS |
| Electromagnetic energy drift ($t\le60$) | $3.6\times10^{-10}$ | $<10^{-6}$ | PASS |
| $1-R-T$ ($\Delta x=0.05$) | $-6.5\times10^{-10}$ | — | PASS |
| $\alpha=0$ control reflection | $2.1\times10^{-11}$ | — | Scheme correct |
| Static magnetic flux $\max|\partial_x(Zf)|$ (analytic initial data) | $1.8\times10^{-5}$ | — | 2nd-order convergence |
| Static magnetic flux (discretely exact initial data) | $1.5\times10^{-13}$ | — | Exact steady state |
| Longitudinal sector $\max|\partial_x(ZE)|$ | $5.6\times10^{-16}$ | — | Exact |

Scattering: at $\alpha=0.5$, $R=0.1093$, $T=0.8907$, converging to $10^{-7}$ as the grid is refined;
the sharp-interface theoretical value $((Z_--Z_+)/(Z_-+Z_+))^2=0.2136$; the finite-width wall lies below this value, as expected.
At $\alpha=0$, $R=2\times10^{-11}$—reflection comes entirely from the $Z$ gradient, not a numerical artifact.

**Nontriviality**: $f$ and $E$ are both nonzero and evolving; a static solution $f=Q/Z$ exists ($Q=0.1$, $E_{\rm EM}=0.449$), varying spatially, with nonzero energy, and cannot be written as pure gauge $\partial_\mu\Lambda$. **The L1 existence criterion is satisfied.**

### 3.3 Three Formula Corrections to Read First

**(a) The Appendix B equation omitted $Z$ in the flux term.**
The report writes $\partial_t(Z\partial_tA_y)-\partial_x(\partial_xA_y)=0$;
Covariant Reconstruction §3 gives $\partial_t(ZE)-\partial_x(Zf)=0$ in Minkowski.
The two agree only when $Z$ is spatially uniform. This implementation uses the latter; the former would miss the flux modulation inside the wall.

**(b) Under a general metric, the time term of the ν=y component is missing a factor $1/B$ (E-1).**
Direct recomputation from the action (sympy, see §5.3):
$$\partial_t\!\left(\frac{ZAC}{NB}E\right)-\partial_x\!\left(\frac{ZNC}{AB}f\right)=0.$$
The reconstruction document §3 writes $\partial_t(ZACE/N)-\partial_x(ZNCf/(AB))=0$: **the flux term is the same, but the time term's denominator is missing $B$**.
Only when $N,A,B,C$ are constants can it be reduced to $\partial_t(ZE)=(N^2/A^2)\partial_x(Zf)$; under a general metric, the divergence form above must be used.

| Old Formulation (v1.0 Closeout Report) | Problem | Correction |
|---|---|---|
| "The flux has an extra $1/B$" | The difference is actually in the time term, not the flux term | Time term's denominator is missing $B$ |
| "The two terms have inconsistent dimensions ($M^2$ vs $M^3$)" | When $N,A,B,C$ are dimensionless both terms are $M^3$ | Delete that judgment; this is a pure coefficient error |
| "After multiplying by $N/(AC)$ it becomes $\partial_t(ZE)-\dots$" | $N/(AC)$ depends on $t$ and cannot be moved inside the derivative | This simplification holds only for a constant metric |

The Minkowski limit is unaffected, so the A4 conclusion is unaffected; **but P2's ADM implementation must use the divergence form**.
E-1 has been corrected in `DCC_Covariant_Reconstruction_v1.md` v1.1.

**(c) "The electric-flux constraint $ZBCE/(AN)=P$" belongs to the longitudinal sector (E-2).**
The Gauss law for the transverse $A_y$ polarization is an identity ($E_x=0$); $ZE$ is not a conserved quantity.
A4 verifies separately: transverse (propagating mode + static $f=Q/Z$) and longitudinal ($E=P/Z$, $f=0$).
Treating $ZE=P$ as a transverse constraint would erroneously forbid the propagating mode.

### 3.4 What A4 Did Not Do

- Did not introduce the Einstein equations or $A,B,C$ evolution (these belong to P2);
- Did not let the wall move over time ($\dot Z\neq0$)—the energy-injection rate is therefore identically 0 and the two-way reconciliation closes trivially;
- Did not implement general-metric coefficients (E-1 has been corrected in Covariant Reconstruction v1.1; P2's first round will use the divergence form directly).

All of these are within Appendix B's "explicitly out of scope" list and do not constitute gaps in L1 closure.

---

## 4. Correction of the Attribution of the Magnetic-Source Extension

The old version of `results` wrote "simulation unstable (wall driven by the source term hit the boundary)". Controlled experiments give a more precise conclusion:

1. With a simple outgoing boundary plus source term, $f=0.1$ diverges at the **right endpoint** after $T\approx2.6$ ($\phi$ exceeding $10^2$),
   while the interior wall structure remains intact ($\phi_{\max}=1.000$, $x_w\approx0$)—the instability is at the boundary, not the wall;
2. Adding a sponge layer alone does not fix it: the boundary point lacks the equilibrium state of the source term, and damping only slows the divergence;
3. After changing the boundary to a local minimum of $V_{\rm eff}$ (Dirichlet), the same parameters evolve stably to $T=10$,
   with the wall slowly shifting rightward, $x_w=+0.248$, $v_w\approx0.049$;
4. $V_{\rm eff}'$ still has 3 zeros at $f\le0.3$—**bistability is not destroyed**,
   so the instability cannot be attributed to collapse of the potential structure.

Therefore the review report §8 attribution to a "simple absorbing boundary" holds, but the mechanism should be stated as **the boundary condition does not contain the source term**, not merely reflection.
Wall motion itself ($\phi\leftrightarrow F\leftrightarrow g$) remains DEFERRed to P2 per §8(a).

---

## 5. List of Differences from the Review Report / Frozen Documents

| # | Item | Review Report / Document | This Report | Handling |
|---|---|---|---|---|
| D1 | $\eta_{\rm target}$ | 74.82 | 74.87 (using the analytic $\sigma_w$) | Adopt 74.9; difference 0.07% |
| D2 | $\epsilon/\epsilon_c$ | 1.38% | 1.30% ($\epsilon=0.01$) | Adopt 1.30%; 1.38% comes from $F=0.0106$ |
| D3 | Appendix B equation | $\partial_x(\partial_xA_y)$ | $\partial_x(Z\partial_xA_y)$ | Adopt the correction |
| D4 | General-metric ν=y coefficient | $ZACE/N$, $ZNCf/(AB)$ | Divergence form $\partial_t(ZACE/(NB))=\partial_x(ZNCf/(AB))$ | E-1 already corrected in Covariant Reconstruction v1.1; P2 uses divergence form |
| D5 | $ZE=P$ | Treated as a Maxwell constraint | Longitudinal sector only; transverse is an identity | Included in the P2 checklist |
| D6 | BPS threshold | $<10^{-6}$ | Unattainable for numerical profiles; attainable for analytic profiles | Recommend splitting into two rows |
| D7 | Attribution of magnetic-source instability | Simple absorbing boundary reflection | Boundary condition lacks the source term (more precise) | Archive |
| D8 | Convergence order 4.03 | Insufficient evidence / mismatch | Artifact of old data; true value 2.00 | Archive |

D1–D2 are rounding/normalization conventions and do not change any physical conclusion.
D3–D5 are formula issues that would cause actual errors in P2 and must be confirmed item by item in the P2 initiation document.

### 5.3 Independent Verification of E-1

For $g=\mathrm{diag}(-N^2,A^2,B^2,C^2)$, $A_\mu=(0,0,A_y(t,x),0)$, taking $N,A,B,C,Z,A_y$ all as functions of $(t,x)$, directly compute
$\nabla_\mu(ZF^{\mu\nu})$:

```
ν=t : 0
ν=x : 0
ν=z : 0
√-g Z F^{ty} = -Z A C E / (N B)
√-g Z F^{xy} = +Z N C f / (A B)
⇒ ∂_t(ZACE/(NB)) = ∂_x(ZNCf/(AB))
```

**Note**: The v1.0 closeout report once treated $N,A,B,C$ as constants and obtained $\partial_t(ZE)=(N^2/A^2)\partial_x(Zf)$. That expression is only the constant-metric limit, not the general expression; the general expression must retain the divergence form.
This computation can be reproduced with one click (the `div_*` and `sqrtg*Z*F^{ty/xy}` outputs of `DCC_sympy_derivation.py`, or the appendix of this document).

---

## 6. Remaining Risks and Handover

| Risk | Current Status | Assignment |
|---|---|---|
| General-metric Maxwell coefficient written incorrectly | Located and corrected (E-1…E-8, Covariant Reconstruction v1.1) | Closed; P2 uses divergence form |
| Energy injection with $\dot Z\neq0$ | Not measured; identically 0 for a static wall | P2 |
| Magnetically driven wall motion | Can be stably demonstrated, but three-system coupling not done | P2 |
| Grid/boundaries for fast walls | A4's Mur gives R≈$10^{-11}$ at $c=1$; relativistic walls need retesting | P2 |
| BPS threshold convention | Two-row scheme given, pending review confirmation | Reviewer |
| 42.47 km/s misread | Labeled "phenomenological assumption" in three places | Ongoing |

**P2 initiation condition check**:

1. L1 closed — ✅ (§3 of this report);
2. L2 ($\ddot C/C$ sign evidence) — pending P2's first-round output, not an initiation prerequisite;
3. P1a complete — ✅;
4. §14 symbol review — ✅ (`DCC_P2_Symbols_and_Observables_Checklist_v1.md`); E-1…E-8 already corrected in Covariant Reconstruction v1.1.

---

## 7. Reproduction

```bash
python DCC_P1_bubble_wall.py        # P1a/P1b: about 5 s
python DCC_P1_A4_maxwell_L1.py      # A4/L1: about 3 s
```

Environment: Python 3.11+, numpy ≥ 2.0 (`np.trapezoid`), matplotlib ≥ 3.8.
All randomness is absent (no random-seed dependence).

---

## Appendix: Maxwell Coefficient (E-1) Verification Script

```python
import sympy as sp
t, x = sp.symbols('t x', real=True)
N = sp.Function('N')(t, x); A = sp.Function('A')(t, x)
B = sp.Function('B')(t, x); C = sp.Function('C')(t, x)
Z = sp.Function('Z')(t, x); Ay = sp.Function('Ay')(t, x)
g = sp.diag(-N**2, A**2, B**2, C**2)
coords = [t, x, sp.Symbol('y'), sp.Symbol('z')]
Amu = [0, 0, Ay, 0]
F = sp.Matrix(4, 4, lambda m, n: sp.diff(Amu[n], coords[m]) - sp.diff(Amu[m], coords[n]))
Fup = sp.simplify(g.inv() * F * g.inv())
sqrtg = N * A * B * C
for nu in range(4):
    expr = sum(sp.diff(sqrtg * Z * Fup[mu, nu], coords[mu]) for mu in range(4))
    print(coords[nu], sp.simplify(expr / sqrtg))
print('sqrtg Z F^ty =', sp.simplify(sqrtg * Z * Fup[0, 2]))
print('sqrtg Z F^xy =', sp.simplify(sqrtg * Z * Fup[1, 2]))
```

---

Content generated by AI