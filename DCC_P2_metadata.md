# DCC P2 Deliverables Metadata Table v1.0 (First Round: Homogeneous Bianchi I)

**Project**: Dimensional Collapse Conjecture
**Corresponding Phase**: P2 first round (Roadmap v2.3 §6, §13 G4)
**Date**: 2026-11-19
**Code**: `DCC_P2_homogeneous.py` (main body), `DCC_P2_local_planar.py` (negative-result diagnostics)
**Results**: `DCC_P2_homogeneous_results.txt`, `DCC_P2_homogeneous_cases.png`, `DCC_P2_homogeneous_scan_*.png`, `DCC_P2_local_planar_results.txt`
**Report**: `DCC_P2_Report_v1.md`

This table completes the metadata for the P2 first round in accordance with Roadmap §11 (symbol reproducibility / dimensional checks / energy-condition monitoring).
The P1 wall profile and parameters remain as specified in `DCC_P1_metadata.md`; this table does not duplicate their numerical values.

---

## 1. Parameters and Units

Natural units $c=\hbar=1$. $[\phi]=M^1$, $[V]=M^4$, $[x]=[t]=M^{-1}$, $[Z]=0$, $[A_y]=M^1$, $[F_{\mu\nu}]=M^2$. The scale factors $A,B,C$ use the dimensionless comoving convention.

| Parameter | Value | Description |
|---|---|---|
| $\lambda$ | 1.0 | Double-well potential strength |
| $v$ | 1.0 | Vacuum expectation value |
| $\alpha$ | 0.5 | $Z(\phi)=e^{\alpha\phi/v}$ |
| $\epsilon$ | 0.01 | Tilt parameter (barrier-top case) |
| $\kappa$ | 1.0 | $8\pi G$ |
| $f_0$ | 0.7 | Baseline magnetic flux ($F_{xy}=f$, $E=0$) |
| $V(\phi)$ | $\frac{\lambda}{4}(\phi^2-v^2)^2+\frac{\epsilon(\phi+v)}{2v}+\frac{\epsilon^2}{16\lambda v^4}$ | Nonnegative shifted double well |
| $V(-v)$ | $\epsilon^2/16=6.25\times10^{-6}$ | True vacuum |
| $V(+v)$ | $\epsilon+\epsilon^2/16=1.000625\times10^{-2}$ | False vacuum |
| $V(0)$ | $0.255006$ | Barrier top (used for $f_c$ normalization) |
| $\epsilon_c$ | $4\lambda v^3/(3\sqrt3)=0.769800$ | spinodal |
| $\epsilon/\epsilon_c$ | 1.299% | Far from reaching spinodal |

**Correction record**: Earlier versions used $V=\frac{\lambda}{4}(\phi^2-v^2)^2+\epsilon(\phi+v)/(2v)$, whose true minimum $V_{\min}<0$ ($\approx-6.25\times10^{-6}$) produced a spurious crunch at $t\sim872$ ($K\sim10^{24}$). Adding the constant term $\epsilon^2/(16\lambda v^4)$ in this version gives $V\ge0$, and the spurious crunch disappears. This correction does not change the qualitative D2/D3 conclusions.

---

## 2. Initial-Data Modes

State variables of the homogeneous model: $(\ln A,\ln B,\ln C,H_A,H_B,H_C,\phi,\dot\phi)$, with initial values $A=B=C=1$.

| Mode | Formula | Use |
|---|---|---|
| shear | $H_A=H_B=H_0$, $H_C=(\kappa\rho_0-H_0^2)/(2H_0)$ | Expansion prescribed in $x,y$; $z$ solved from the Hamiltonian constraint; includes initial shear |
| isotropic | $H_A=H_B=H_C=\sqrt{\kappa\rho_0/3}$ | No initial shear; anisotropy generated dynamically by the magnetic field |

Both modes satisfy $H_AH_B+H_BH_C+H_CH_A=\kappa\rho_0$ exactly.

**Scan grid**:
* shear: $H_0\in\{0.15,0.2,0.25,0.3,0.4\}$, $f\in\{0,0.3,0.5,0.7,1.0,1.5,2.0\}$;
* isotropic: $f$ as above ($H_0$ determined by $\rho_0$).

**D2 counting convention (important)**: This table separates "all D2" from "magnetically driven crossing":

* All D2: $H_C^{\min}<0$ (including the initial Kasner branch with $H_C(0)<0$);
* Magnetically driven crossing: $H_C(0)>0$ and $H_C^{\min}<0$ (the magnetic field drives the expanding Z direction into contraction).

Results: in the shear scan, 35/35 are all D2, of which 23/35 are magnetically driven (12/35 have $H_C(0)<0$); in the isotropic scan, 6/6 cases with $f>0$ are all magnetically driven. Barrier-top thresholds: $f_c^{\rm iso}=2.93$, $f_c^{\rm shear}=4.73$; the true-vacuum isotropic case has no energy threshold, with $t_{D2}\approx1.41/f$ ($f\gtrsim7.1\times10^{-4}$ for $t_{\rm end}=2000$).

**Single cases**: $\phi_0\in\{0,-v\}$, $\dot\phi_0=0$, $\epsilon\in\{0,0.01\}$, $f\in\{0,0.7,1.5\}$, $H_0=0.25$ (shear) or isotropic.

**Deviation statement**: The above initial data are **zero-mode truncations** of the two asymptotic values of the P1 profile ($\phi_0=0$ and $\phi_0=-v$), not the $x$-dependent kink of P1. The full 1+1 case remains unfinished (see Report §6).

---

## 3. Numerical Settings

| Item | Value |
|---|---|
| Integrator | `scipy.integrate.solve_ivp`, LSODA |
| rtol / atol | $10^{-11}$ / $10^{-13}$ (convergence tests additionally use $10^{-7}$–$10^{-12}$) |
| $t_{\rm end}$ | 2000 (single cases/scans); 400 (independent L2 run); 50 (tolerance convergence) |
| max_step | 0.5 |
| Events | $H_C=0$ (non-terminating); $C=10^{-3}$ (terminating); $\max|H_i|=10^3$ (terminating, blow-up guard) |
| dense_output | True (for interpolation) |
| Platform | Python 3.11+, numpy 2.4.6, scipy 1.18.0, matplotlib 3.11.0 |

**Convergence test** (magnetic-only shear, $t=5,20$): see Report §3.7; $\mathcal C_H$ decreases from $6.7\times10^{-6}$ to $5.1\times10^{-10}$ as rtol is reduced, with no drift.

---

## 4. Observable Definitions

| Symbol | Definition | Implementation |
|---|---|---|
| $\mathcal R_H$ | $H_C/H_A$ | Pointwise; recorded as NaN when $H_A\approx0$ |
| $\mathcal R_L$ | $C/A$, $C/B$ | Pointwise |
| $\mathcal K$ | $4\sum_i(\dot H_i+H_i^2)^2+4\sum_{i<j}H_i^2H_j^2$ | Analytic expression; de Sitter self-check $24H^4$ |
| $\mathcal E$ | $\rho=\frac12\dot\phi^2+V+\rho_B$ | Pointwise |
| $\mathcal C_H$ | $|H_AH_B+H_BH_C+H_CH_A-\kappa\rho|/(|{\rm lhs}|+|{\rm rhs}|+H_A^2+H_B^2+H_C^2)$ | Pointwise maximum |
| $\mathcal B$ | $\max|\partial_t f-\partial_x E|$ | Homogeneous purely magnetic case: $E=0$, $f={\rm const}$, hence $\mathcal B=0$ |
| $\ddot C/C$ | $\dot H_C+H_C^2$ | Evaluated pointwise from the $H_C$ derivative in the RHS |
| NEC | $\min(\rho+p_x,\rho+p_y,\rho+p_z)$ | Pointwise |
| WEC | $\min(\rho,\mathrm{NEC})$ | Pointwise |
| Conservation | $\dot\rho+(H_A+H_B+H_C)\rho+H_Ap_x+H_Bp_y+H_Cp_z$ | Analytic derivative, pointwise |

**D criteria**: see Report §1.3 (D1, D2, D3-ratio, D3-strict, valid).

---

## 5. Raw Data Locations

| Data | File |
|---|---|
| 12 single cases + 4 scan sets + convergence/conservation | `DCC_P2_homogeneous_results.txt` |
| Baseline case, 7-panel time series | `DCC_P2_homogeneous_cases.png` |
| L2 ($\ddot C/C$) independent table | `DCC_P2_L2_results.txt` (`DCC_P2_L2.py`) |
| Scan heat maps | `DCC_P2_homogeneous_scan_{magnetic-only,baseline,magnetic-iso,baseline-iso}.png` |
| Gradient-approximation negative result | `DCC_P2_local_planar_results.txt`, `.png` |

---

## 6. Coordinates and Geodesic Lengths

* Coordinates are comoving; physical lengths are $L_x=A\Delta x$, $L_y=B\Delta y$, $L_z=C\Delta z$.
* $\mathcal R_L=C/A$ is a **comoving coordinate ratio**; to obtain the physical geodesic-length ratio, it must be multiplied by $\Delta z/\Delta x$. This report assumes $\Delta x=\Delta z$ by default, so the coordinate ratio is the physical ratio.
* $H_i=\dot a_i/a_i$ is defined with respect to coordinate time $t$ ($N=1$).
* The magnetic field $f=F_{xy}$ is a coordinate component; the physical field is $B_z=f/(AB)$, with $\rho_B=Zf^2/(2A^2B^2)$.

---

## 7. Unclosed Items (in Sync with Report §6.4)

| # | Task | Status |
|---|---|---|
| P2-C1 | Full 1+1 ADM with a planar periodic box / compensating background | Not done |
| P2-C2 | Initial data using the P1 profile | Not done |
| P2-C3 | Seven observables + step-by-step output of $\ddot C/C$ (1+1) | Not done |
| P2-C4 | Axisymmetric $(r,\theta)$ bubble | Not done |
| P2-C5 | 1+1 grid convergence | Not done |
| P2-C6 | Singularity / coordinate-degeneration verdict at $C\to0$ | Not done |

**Until P2-C1...C6 are completed, P2 cannot be closed out; externally it may only be stated that "D2 exists in the homogeneous sector, while strict D3 has not been reached."**

Content generated by AI
