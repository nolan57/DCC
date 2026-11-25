# DCC P2 Report v1.0 — Anisotropic Geometric Response (First Round of Homogeneous Bianchi I)

**Project**: Dimensional Collapse Conjecture
**Document type**: P2 first-round results report (in-stage report, not the P2 closeout)
**Date**: 2026-11-19
**Basis**: `DCC_P0-P4_Roadmap_Plan.md` v2.3 §6, §13; `DCC_P2_Symbols_and_Observables_Checklist_v1.md`; `DCC_P1_metadata.md`; `DCC_Covariant_Reconstruction_v1.md` v1.1
**Code**: `DCC_P2_homogeneous.py`, `DCC_P2_L2.py`, `DCC_P2_local_planar.py` (negative-result diagnostic)
**Results**: `DCC_P2_homogeneous_results.txt`, `DCC_P2_L2_results.txt`, `DCC_P2_homogeneous_cases.png`, `DCC_P2_homogeneous_scan_*.png`, `DCC_P2_local_planar_results.txt`

---

## 0. Verdict summary

| Item | Verdict | Basis |
|---|---|---|
| **D1** (anisotropic expansion) | **Pass** | magnetic field $p_z=-\rho_B$, $p_x=p_y=+\rho_B$ gives $H_C<H_A$; D1=True in all magnetic cases |
| **D2** (actual contraction in Z) | **Pass (conditional, sector-dependent)** | barrier top: $f\ge f_c$ (iso 2.93 / shear 4.73). True vacuum iso: no energy threshold, $t_{D2}\approx1.41/f$ ($f\gtrsim7.1\times10^{-4}$ for $t_{\rm end}=2000$). In 12/35 shear cases $H_C(0)<0$, so D2 is initial Kasner, **not counted as magnetically driven**; magnetically driven crossings: 23/35 |
| **D3** (geometric degeneration with $C\to0$) | **Fail (strict)** | in homogeneous models $C$ freezes/rebounds after contraction; $C/A\to$ small but $C$ itself does not $\to0$ |
| **D3-ratio** ($C/A\ll1$) | **Pass (magnetic sector, non-monotonic)** | magnetic-iso 6/6 ($f>0$); magnetic-shear 27/35 ($f>0$: 22/30; $f=0$ controls 5/5). Strongest fields $f=1.5$–$2.0$ cause $C/A$ to rebound |
| **Constraint $\mathcal C_H$** | **Pass (homogeneous)** | $6.7\times10^{-6}$ ($t_{\rm end}=2000$, rtol $10^{-11}$); decreases monotonically with tolerance to $5.1\times10^{-10}$ |
| **Energy-momentum conservation** | **Pass (homogeneous)** | continuity-equation residual $2.8\times10^{-17}$–$5.3\times10^{-15}$ (machine precision) |
| **Bianchi residual $\mathcal B$** | **0 (analytic)** | homogeneous purely magnetic $E=0$, $f={\rm const}$, so $\partial_t f-\partial_xE=0$ holds identically |
| **NEC / WEC** | **Pass (marginal)** | $\mathrm{NEC}_{\min}=0$ (magnetic field along Z exactly saturates); $\mathrm{WEC}\ge0$ |
| **Kretschmann** | **Finite** | effective runs $K_{\max}\sim0.27$–$26$; no physical singularity |
| **L2: $\ddot C/C$** | **Output produced** | §3.6; in D2 cases $\ddot C/C>0$ at the minimum of $H_C$ (turning from contraction) |
| **1+1 planar ADM** | **Not closed** | planar Lichnerowicz not asymptotically flat; gradient-approximation momentum residual $\gg1$ (§6) |
| **Spherical / axisymmetric** | **Not closed** | magnetic field breaks spherical symmetry; a 2D axisymmetric code is required (§6) |
| **P2 gate G4** | **Conditional pass (homogeneous sector only)** | D2 exists and constraints are controlled; but roadmap §6.5 item 6 (two geometries) unmet |

**In one sentence**: **D2 does exist in the magnetic sector of homogeneous Bianchi I** (magnetically driven crossings: iso 6/6, shear 23/35), with the threshold set by the magnetic energy fraction; **strict D3 does not occur** (contraction is transient); full 1+1 planar and spherically symmetric verification is not yet closed, so P2 can only be judged "conditional pass (homogeneous sector only)", and one cannot claim externally that "geometric dimensional collapse has been confirmed".

---

## 1. Scope, conventions, and criteria

### 1.1 Interface with P1

P2 wall profile and parameters follow `DCC_P1_metadata.md` (numerical values are not repeated here):

* kink profile $\phi=v\tanh(ax)$, $a=v\sqrt{\lambda/2}$;
* the definitions and grid for wall thickness $\delta_{0.9}$, wall tension $\sigma_w$, and wall position $x_w$ are given in `DCC_P1_metadata.md` §2–§3;
* P1a static baseline, A3 convergence order, and A4 Maxwell results are in the same table.

**First-round deviation statement (must be recorded)**: the main result of this report is the **homogeneous Bianchi I zero-mode truncation**, which takes the two asymptotic values of the P1 wall profile as homogeneous initial data, respectively:

* $\phi_0=0$ (wall center / barrier top);
* $\phi_0=-v$ (interior of true vacuum).

It **does not** use P1's $x$-dependent profile. Per roadmap §6.2 step 2, the full 1+1 solver must use the P1 profile; that item is incomplete (see §6). Therefore this report cannot claim "P2 has been completed using the P1 wall profile".

### 1.2 Metric and direction conventions

$$ds^2=-N^2dt^2+A^2dx^2+B^2dy^2+C^2dz^2,\qquad N=1,\ \beta=0.$$

**The contraction direction is $C$ (Z direction)**. The magnetic field $F_{xy}=f$, i.e. $B$ along Z; its stress is
$$p_x=p_y=+\rho_B,\qquad p_z=-\rho_B,\qquad \rho_B=\frac{Z(\phi)f^2}{2A^2B^2}.$$
This is precisely the origin of the D1/D2 directionality.

### 1.3 Criteria (used in this report)

| Criterion | Definition | Notes |
|---|---|---|
| D1 | $\exists t:\ H_C<H_A$ and $H_A>0$ | anisotropic expansion |
| D2 | $\exists t:\ H_C<0$ and $(H_A>0\ \text{or}\ H_B>0)$ | directional actual contraction; excludes global crunch |
| D3-ratio | $\exists t:\ C/A<10^{-2},\ C/B<10^{-2},\ H_A,H_B>0,\ A,B>10^{-2}$ | relative geometric degeneration |
| D3-strict | final state $C<10^{-3}$, $A,B>10^{-2}$, $H_A,H_B>0$, $C/A,C/B<10^{-2}$ | strict $C\to0$ |
| valid | $\max|H_i|<10^2$ and $\max|\mathcal C_H|<0.1$ | exclude misjudgment after numerical blow-up |

> **The two readings of D3 must be kept separate.** The roadmap's original wording "$C\to0$ with $A,B$ finite" is not equivalent to "$C/A\to0$" in an expanding universe: $A,B$ can grow while $C$ freezes at a finite value. This report reports both D3-ratio and D3-strict; the former must not be passed off as the latter.

---

## 2. Homogeneous model and equations

### 2.1 Matter

$$\rho=\tfrac12\dot\phi^2+V(\phi)+\rho_B,\qquad
p_\phi=\tfrac12\dot\phi^2-V(\phi),$$
$$p_x=p_y=p_\phi+\rho_B,\qquad p_z=p_\phi-\rho_B.$$

The potential uses a **nonnegative-shifted double well**:
$$V(\phi)=\frac{\lambda}{4}(\phi^2-v^2)^2+\frac{\epsilon(\phi+v)}{2v}+\frac{\epsilon^2}{16\lambda v^4}.$$
The role of the constant term $\epsilon^2/(16\lambda v^4)$ is to lift the minimum of the tilted double well exactly to $0$, avoiding a late-time global crunch caused by $V_{\min}<0$. Take $v=\lambda=1$, $\epsilon=0.01$:
$$V(-v)=\frac{\epsilon^2}{16}=6.25\times10^{-6},\qquad V(+v)=\epsilon+\frac{\epsilon^2}{16}=1.000625\times10^{-2}.$$

The coupling $Z(\phi)=\exp(\alpha\phi/v)$, $\alpha=0.5$, $Z\in[0.6065,1.6487]>0$.

### 2.2 Evolution equations

$$H_A=\frac{\dot A}{A},\quad H_B=\frac{\dot B}{B},\quad H_C=\frac{\dot C}{C},$$
$$\dot H_A=-H_A^2-\tfrac12H_A(H_B+H_C)+\tfrac12H_BH_C-\tfrac{\kappa}{2}(p_y+p_z-p_x),$$
$$\dot H_B=-H_B^2-\tfrac12H_B(H_A+H_C)+\tfrac12H_AH_C-\tfrac{\kappa}{2}(p_x+p_z-p_y),$$
$$\dot H_C=-H_C^2-\tfrac12H_C(H_A+H_B)+\tfrac12H_AH_B-\tfrac{\kappa}{2}(p_x+p_y-p_z),$$
$$\ddot\phi=-(H_A+H_B+H_C)\dot\phi-V'(\phi)-\frac{\alpha}{v}\rho_B.$$

Hamiltonian constraint:
$$H_AH_B+H_BH_C+H_CH_A=\kappa\rho.$$

### 2.3 Kretschmann

$$K=4\sum_i(\dot H_i+H_i^2)^2+4\sum_{i<j}H_i^2H_j^2.$$
The de Sitter test gives $24H^4$, consistent with the analytic value (self-check in the script).

### 2.4 Initial-data modes (critical)

The constraint gives only one equation, so the initial values of $H_A,H_B,H_C$ retain freedom. This report explicitly compares two modes:

| Mode | Initial data | Physical meaning |
|---|---|---|
| **shear** | $H_A=H_B=H_0$, $H_C=(\kappa\rho_0-H_0^2)/(2H_0)$ | given $x,y$ expansion, $z$ solved from constraint; generally carries initial shear |
| **isotropic** | $H_A=H_B=H_C=\sqrt{\kappa\rho_0/3}$ | no initial shear; magnetic field subsequently generates anisotropy **dynamically** |

**Both modes are legitimate constraint solutions.** The D2 conclusion depends on initial data and must be reported separately; one cannot select only one.

---

## 3. Results

### 3.1 Single cases (shear mode, $t_{\rm end}=2000$, rtol $10^{-11}$)

| Case | $\phi_0$ | $\epsilon$ | $f$ | $H_0$ | $H_C^{\min}$ | $t_{D2}$ | final $C/A$ | D2 | D3-strict | D3-ratio | $\mathcal C_H$ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| magnetic-only | $-1$ | 0 | 0.7 | 0.25 | $-2.98\times10^{-2}$ | 1.587 | $2.96\times10^{-3}$ | ✅ | ❌ | ✅ | $6.8\times10^{-6}$ |
| vacuum-only | $-1$ | 0 | 0 | 0.25 | $-1.25\times10^{-1}$ | 0 | $1.33\times10^{-3}$ | ✅ | ❌ | ✅ | $5.9\times10^{-14}$ |
| true-vac start | $-1$ | 0.01 | 0.7 | 0.25 | $-2.97\times10^{-2}$ | 1.587 | $3.19\times10^{-3}$ | ✅ | ❌ | ✅ | $6.3\times10^{-6}$ |
| baseline | 0 | 0.01 | 0.7 | 0.25 | $+3.39\times10^{-4}$ | — | 1.128 | ❌ | ❌ | ❌ | $4.9\times10^{-6}$ |
| no B | 0 | 0.01 | 0 | 0.25 | $+3.39\times10^{-4}$ | — | 1.167 | ❌ | ❌ | ❌ | $4.9\times10^{-6}$ |
| strong B | 0 | 0.01 | 1.5 | 0.25 | $+3.37\times10^{-4}$ | — | 0.867 | ❌ | ❌ | ❌ | $5.0\times10^{-6}$ |
| fast | 0 | 0.01 | 0.7 | 0.40 | $+3.39\times10^{-4}$ | — | 0.708 | ❌ | ❌ | ❌ | $4.9\times10^{-6}$ |

**Reading**:
* True vacuum / purely magnetic ($f=0.7$): $H_C(0)=+0.172>0$, $H_C$ clearly crosses $0$ to $-0.0298$, a **magnetically driven** D2; $C/A$ reaches $3\times10^{-3}$.
* Barrier top: the minimum of $H_C$ is the **late-time asymptotic value** $+3.39\times10^{-4}$, not a transient dip; the magnetic field pushes $H_C$ near zero but **does not cross it**. $f=1.5$ is still insufficient.
* **Criterion distinction**: cases in the shear scan with $H_C(0)<0$ (e.g. f=0, 0.3) are contracting from the start, belonging to Kasner initial data, **not magnetic-field evidence**. This report records "$H_C(0)>0$ and $H_C^{\min}<0$" as a magnetically driven crossing; 23/35 across the full scan.
* vacuum-only ($f=0$) D2 comes from initial data $H_C(0)=-H_0/2<0$, a Kasner-type vacuum solution, not magnetically driven; used only as a control.

### 3.2 Single cases (isotropic mode, $t_{\rm end}=2000$)

| Case | $\phi_0$ | $\epsilon$ | $f$ | $H_C(0)$ | $H_C^{\min}$ | $t_{D2}$ | final $C/A$ | D2 | D3-ratio | $\mathcal C_H$ |
|---|---|---|---|---|---|---|---|---|---|---|
| magnetic-only | $-1$ | 0 | 0.7 | 0.2226 | $-2.62\times10^{-2}$ | 2.085 | $3.36\times10^{-3}$ | ✅ | ✅ | $6.7\times10^{-6}$ |
| vacuum-only | $-1$ | 0 | 0 | 0 | 0 | — | 1.000 | ❌ | ❌ | 0 |
| baseline | 0 | 0.01 | 0.7 | 0.4083 | $+3.39\times10^{-4}$ | — | 0.694 | ❌ | ❌ | $4.9\times10^{-6}$ |
| no B | 0 | 0.01 | 0 | 0.2916 | $+3.39\times10^{-4}$ | — | 1.000 | ❌ | ❌ | $4.9\times10^{-6}$ |
| strong B | 0 | 0.01 | 1.5 | 0.6782 | $+3.38\times10^{-4}$ | — | 0.362 | ❌ | ❌ | $5.0\times10^{-6}$ |

**Key**: even with initial shear removed, the barrier top at $f\le2.0$ still does not reach D2; $H_C^{\min}$ is nearly the same asymptotic value $3.38\times10^{-4}$. This shows that **the negative pressure at the barrier top together with magnetic-energy dilution** jointly keep $H_C$ above zero.

### 3.3 Parameter scan

| Scan | Number of cases | D2 (all) | Magnetically driven crossings | D3-strict | Notes |
|---|---|---|---|---|---|
| magnetic-only (shear, $f\in[0,2]$, $H_0\in[0.15,0.4]$) | 35 | **35** | **23** | 0 | 12/35 have $H_C(0)<0$, so D2 is initial Kasner |
| baseline (shear, same grid) | 35 | **0** | 0 | 0 | all barrier-top cases fail to reach D2 |
| magnetic-iso ($f\in[0,2]$) | 7 | **6** ($f>0$) | **6** | 0 | $f=0$ trivial |
| baseline-iso ($f\in[0,2]$) | 7 | **0** | 0 | 0 | D2 occurs only above threshold (§3.4) |

"Magnetically driven crossing" is defined as $H_C(0)>0$ and $H_C^{\min}<0$; this is the **magnetic-field evidence** for D2. All-D2 counts include the initial-Kasner branch and cannot be taken directly as magnetic-field evidence. All $\mathcal C_H$ in the scan are within $5\times10^{-6}$–$7\times10^{-6}$, with no constraint drift.

### 3.4 D2 thresholds and parameter ranges

**(a) Barrier top ($\phi_0=0$, $V(0)=0.255006$)**: located by bisection (tolerance 0.02):

| Initial-data mode | $f_c$ | $\rho_B/V(0)$ | $\rho_B/(\rho_B+V)$ | $\kappa\rho_B/H_0^2$ |
|---|---|---|---|---|
| isotropic | **2.930** | 16.8 | 0.944 | 2.83 |
| shear ($H_0=0.25$) | **4.732** | 43.9 | 0.978 | 179 |

where $\rho_B=f^2/2$.

**(b) True vacuum ($\phi_0=-v$, $V\approx0$)**: the isotropic mode has **no energy threshold**, but the D2 time is delayed as $f$ decreases. With the $t_{\rm end}=2000$ cutoff, $f_c^{\rm tv}\approx7.1\times10^{-4}$, and

$$t_{D2}\approx\frac{1.41}{f}.$$

| $f$ | $t_{D2}$ | $H_C^{\min}$ |
|---|---|---|
| 0.001 | 1413 | $-2.36\times10^{-5}$ |
| 0.0015 | 942 | $-5.53\times10^{-5}$ |
| 0.002 | 707 | $-7.74\times10^{-5}$ |
| 0.003 | 471 | $-1.16\times10^{-4}$ |
| 0.01 | 141 | $-3.87\times10^{-4}$ |
| 0.7 | 2.085 | $-2.62\times10^{-2}$ |

Thus "any $f>0$ reaches D2" holds only in the sense of **no time limit**; as $f\to0$ D2 is delayed to $t\sim1/f$ — it neither disappears nor reflects a finite energy threshold.

**(c) Initial-data warning for shear**: in shear mode, for $f\lesssim0.35$ ($H_0=0.25$) $H_C(0)<0$ and contraction begins immediately (Kasner branch). Such D2 **cannot** serve as magnetic-field evidence; only the 23/35 cases where $H_C(0)>0$ is subsequently driven negative by the magnetic field qualify.

**Conclusions**:
1. **True vacuum / magnetic sector**: no energy threshold for isotropic ($t_{D2}\propto1/f$); small-$f$ D2 in shear mostly comes from initial Kasner, and magnetically driven crossing requires $f\gtrsim0.5$ ($H_0=0.25$).
2. **Barrier top**: D2 requires magnetic energy to dominate absolutely — isotropic initial data need $\rho_B\gtrsim17V(0)$ (magnetic energy fraction $\gtrsim94\%$); with initial shear, $\rho_B\gtrsim44V(0)$ ($\gtrsim98\%$).
3. **Initial shear raises the threshold**: for the same $f$, shear mode is harder to bring to D2 than isotropic mode, because the constraint including potential energy gives a larger initial $H_C$, and the geometric shear term overwhelms the magnetic drive.
4. **Falsification ranges**: at the barrier top, isotropic initial data with $f<2.93$ (or shear with $H_0=0.25$, $f<4.73$) are excluded by this model. True-vacuum isotropic does not reach D2 within $t_{\rm end}=2000$ for $f<7.1\times10^{-4}$ (extending $t_{\rm end}$ may change this).

### 3.5 D3 analysis

**Strict D3 is 0 in all scans.** The reason is clear:

* after the magnetic field drives $H_C<0$, $\rho_B\propto1/(A^2B^2)$ dilutes as $A,B$ expand;
* the magnetic drive term $-\tfrac{\kappa}{2}(p_x+p_y-p_z)=-\tfrac{\kappa}{2}(p_\phi+g+3\rho_B)$ weakens accordingly;
* $H_C$ rebounds after reaching a negative minimum; $C$ first contracts and then freezes/re-expands (magnetic-only shear: $H_C^{\min}=-0.0298$, final value $+1.04\times10^{-4}$, $C_{\rm fin}=0.365$).

Therefore:
* **D3-ratio** holds ($C/A$ reaches $3\times10^{-3}$, $A,B$ grow);
* **D3-strict** does not hold ($C$ does not $\to0$; absolute scale freezes).

Physical interpretation: the stress of a homogeneous magnetic field along Z is **transient**; achieving permanent $C\to0$ requires sustained directional stress (e.g. the magnetic field confined within the contracting direction, or wall gradient energy continuously supplying it). This is precisely what a full 1+1 wall may provide and the homogeneous model lacks.

**D3-ratio is non-monotonic in $f$** (shear scan, $H_0=0.25$): at $f=0.7$, $C/A=2.96\times10^{-3}$ is minimal; at $f=1.5$ it rebounds to $1.21\times10^{-2}$, and at $f=2.0$ to $2.19\times10^{-2}$. All 5 controls at $f=0$ achieve D3-ratio (Kasner-type initial data), and $f>0$ gives $22/30$. Thus "stronger magnetic field" does not mean "more complete relative contraction"; there is an effective window at $f\approx0.5$–$1.0$.

### 3.6 L2: $\ddot C/C$

$$\frac{\ddot C}{C}=\dot H_C+H_C^2.$$

In an independent run at $t_{\rm end}=400$, rtol $10^{-11}$ (`DCC_P2_L2.py` / `DCC_P2_L2_results.txt`; $\mathcal C_H\sim3.6\times10^{-7}$):

| Case | $\max|\ddot C/C|$ | $\ddot C/C$ at $H_C^{\min}$ | $H_C^{\min}$ | D2 |
|---|---|---|---|---|
| magnetic-only shear | $2.35\times10^{-1}$ | $+9.03\times10^{-4}$ | $-2.98\times10^{-2}$ | ✅ |
| true-vac shear | $2.35\times10^{-1}$ | $+8.55\times10^{-4}$ | $-2.97\times10^{-2}$ | ✅ |
| baseline shear | $4.28\times10^{-1}$ | $-3.96\times10^{-6}$ | $+1.67\times10^{-3}$ | ❌ |
| magnetic-only iso | $2.48\times10^{-1}$ | $+6.86\times10^{-4}$ | $-2.62\times10^{-2}$ | ✅ |
| baseline iso | $3.23\times10^{-1}$ | $-5.48\times10^{-6}$ | $+1.67\times10^{-3}$ | ❌ |
| baseline iso, $f=3$ | $7.42$ | $+2.04\times10^{-3}$ | $-5.69\times10^{-3}$ | ✅ |

**Reading**: in D2 cases $\ddot C/C>0$ at the minimum of $H_C$, i.e. $C$ is turning from contraction to expansion; $\ddot C/C$ remains finite throughout, with no $C\to0$-type acceleration divergence. This confirms again from the L2 side: **the homogeneous model has no genuine geometric-degeneration singularity, only transient contraction**.

### 3.7 Constraint convergence and conservation

**Tolerance convergence** ($H_C$ at $t=5,20$ for magnetic-only shear):

| rtol | $\mathcal C_H^{\max}$ | $H_C(5)$ | $H_C(20)$ |
|---|---|---|---|
| $10^{-7}$ | $6.708\times10^{-6}$ | $-2.973190410\times10^{-2}$ | $-1.353589960\times10^{-2}$ |
| $10^{-9}$ | $1.433\times10^{-7}$ | $-2.973190934\times10^{-2}$ | $-1.353589995\times10^{-2}$ |
| $10^{-11}$ | $4.133\times10^{-9}$ | $-2.973190938\times10^{-2}$ | $-1.353590001\times10^{-2}$ |
| $10^{-12}$ | $5.140\times10^{-10}$ | $-2.973190938\times10^{-2}$ | $-1.353590001\times10^{-2}$ |

Differences: $1.43\times10^{-12}$ ($10^{-12}\to10^{-11}$), $3.76\times10^{-11}$ ($10^{-11}\to10^{-9}$), $5.24\times10^{-9}$ ($10^{-9}\to10^{-7}$). The constraint residual decreases monotonically with tolerance, **with no drift**.

**Energy-momentum conservation** (analytic continuity equation $\dot\rho+(H_A+H_B+H_C)\rho+H_Ap_x+H_Bp_y+H_Cp_z=0$):

| Case | $\max|{\rm cons}|$ | Relative |
|---|---|---|
| magnetic-only shear | $2.78\times10^{-17}$ | $2.8\times10^{-17}$ |
| baseline shear | $1.39\times10^{-16}$ | $1.4\times10^{-16}$ |
| baseline iso, $f=3$ | $5.33\times10^{-15}$ | $5.3\times10^{-15}$ |

**Bianchi residual**: for the homogeneous purely magnetic configuration $E=0$, $f={\rm const}$, $\mathcal B=\max|\partial_t f-\partial_x E|=0$ (an analytic identity, not a numerical coincidence).

**Energy conditions**: all valid cases have $\mathrm{NEC}_{\min}=0$, $\mathrm{WEC}_{\min}=0$. The null mode of the magnetic field along Z exactly satisfies $\rho+p_z=0$ (NEC saturated), not violated; the scalar field and magnetic energy are nonnegative. **D2 does not require NEC violation**.

**Kretschmann**: magnetic-only shear $K_{\max}=0.266$; baseline $K_{\max}=1.51$; strong B $K_{\max}=26.1$; all finite. Before the shift constant was added, a fake crunch with $K\sim10^{24}$ appeared; it was eliminated by the $V\ge0$ correction.

## 4. Physical interpretation

1. **The physical source of D2 is the anisotropic stress of the magnetic field**: $p_z=-\rho_B$ gives a negative contribution to $\dot H_C$, while $p_x=p_y=+\rho_B$ supports $A,B$. In true vacuum this mechanism is undisturbed by the potential: no energy threshold for isotropic, but $t_{D2}\approx1.41/f$, so D2 is delayed indefinitely as $f\to0$; small-$f$ D2 in shear may be merely initial Kasner, so magnetically driven crossing must be judged by $H_C(0)>0\to H_C^{\min}<0$.
2. **The potential is a double-edged sword**: it provides the negative pressure driving expansion ($p_\phi<0$ gives a positive contribution to $\dot H_C$, **opposing** D2) and, via the Hamiltonian constraint at fixed $H_A=H_B$, raises the initial $H_C$ (the geometric shear term $\propto H_C^2$, also **opposing** D2). Hence the barrier top needs magnetic energy at $94\%$–$98\%$ to suffice.
3. **Initial shear raises the threshold**: shear mode raises $H_C(0)$ from $0.41$ to $0.88$ ($f=0.7$), and the magnetic drive cannot overcome it in the short term; isotropic mode lets the magnetic field **dynamically** build anisotropy from zero shear, giving a much lower threshold.
4. **D3 is transient**: magnetic energy dilutes with transverse area and the drive decays; $C$ freezes after contracting to a finite fraction. Strict geometric degeneration requires sustained directional stress, which the homogeneous model cannot provide.

---

## 5. Interface with P1/A4/covariant documents

| Interface | Status | Notes |
|---|---|---|
| P1 wall profile/parameters | **cited, not used in the main result** | §1.1; the $x$-dependent profile is used only in the full 1+1 |
| P1a static baseline | consistent | $v,\lambda,a,\delta,\sigma_w$ consistent with `DCC_P1_metadata.md` |
| A4 Maxwell | consistent (sectors not mixed) | purely magnetic: $f={\rm const}$ (Bianchi identity, flux conservation), $E=0$, $\rho_B=Zf^2/(2A^2B^2)$; A4's $f=QAB/(ZC)$ is an **electric-flux** relation, belonging to another sector |
| Covariant document E-1…E-8 | consistent | in the homogeneous limit the Bianchi identity reduces to $\dot f=0$; magnetic energy evolution $\dot\rho_B=\rho_B[\dot Z/Z-2(H_A+H_B)]$ ($\dot Z=0$ for magnetic-only) |
| L2 ($\ddot C/C$) | **output produced** | §3.6 |
| $\eta$ / $42.47$ km/s | not involved | P2 is a geometric response and contains no phenomenological velocity calibration |

---

## 6. 1+1 planar and spherical symmetry: why not closed

### 6.1 Non-asymptotic flatness of the planar Lichnerowicz equation

Conformally flat, time-symmetric initial data ($A=B=C=\Psi^2$, $K_{ij}=0$) satisfy the momentum constraint, and the Hamiltonian constraint reduces to
$$\Psi''=-\frac{\kappa}{4}\left[\tfrac12(\phi')^2\Psi+V\Psi^5+\frac{Zf^2}{2\Psi^3}\right].$$

In 1D the Green function is **linear**, not decaying. For a localized source, the solution has a "tent" shape in the box: $\Psi$ grows linearly with $|x|$ and cannot approach 1 as $x\to\pm\infty$. Forcing a solution with $\Psi(\pm L)=1$, the first Picard iteration already gives $\Psi_{\rm center}\approx6.8$ and subsequently overflows (`solve_bvp` reports "maximum number of mesh nodes exceeded"), contradicting asymptotic flatness. **The planar wall itself is not asymptotically flat** (its gravitational field is of Rindler type); this is not a numerical bug but physics.

Viable ways forward (not completed):
* periodic box + negative compensating background (making the box average of the source zero), treating the negative cosmological constant as part of the "box";
* use the exact planar-wall metric as background, then superpose scalar/magnetic perturbations;
* local planar patch + full constraint projection (requires shift/lapse gauge).

### 6.2 Failure of the gradient approximation (separate universe)

`DCC_P2_local_planar.py` attempted the approximation of "solving homogeneous equations at each point with local $\rho(x),p_i(x)$ + retaining $\phi''$". Results (global normalization, ${\rm scale}=2\kappa\max|\rho|$):
* $\max|\mathcal M|/{\rm scale}$ is already $1.76$ initially ($>1$), and $4.96\times10^9$ at the final state;
* $\max|R^{(3)}|/{\rm scale}$ grows from $1.8\times10^{-14}$ to $5.1\times10^{10}$.

The script automatically prints `VALIDITY: INVALID` at the final state. **The momentum constraint is violated from the initial data onward**, not a long-time accumulated error.

Reason: $H\delta\sim1$ ($H\sim0.4$, $\delta\sim4$), so gradient terms are of the same order as evolution terms and cannot be treated perturbatively. **This approximation is invalid for this problem**; this negative result is retained as a diagnostic and is not used as D2 evidence.

### 6.3 Spherical symmetry / axisymmetry

$F_{xy}=f$ selects the Z axis and breaks spherical symmetry. A spherical bubble with a uniform magnetic field is **axisymmetric**, requiring a 2D $(r,\theta)$ code rather than a 1D radial one. A spherically symmetric scalar bubble can be done first, but it cannot answer "Z-direction contraction"; the magnetic-field direction must be included.

### 6.4 List of unclosed items (P2 continuation)

| # | Task | Minimum acceptance |
|---|---|---|
| P2-C1 | full 1+1 ADM with planar periodic box + compensating background | constraint residual $\mathcal C_H$ decreases second-order with $\Delta x$; energy conservation |
| P2-C2 | initial data using the P1 profile (§6.2 step 2) | wall position/thickness consistent with P1 |
| P2-C3 | stepwise output of seven observables + $\ddot C/C$ | output every N steps, no missing items |
| P2-C4 | axisymmetric $(r,\theta)$ bubble | spherical limit reduces to scalar bubble; magnetic-field direction explicit |
| P2-C5 | convergence (grid doubling, $\Delta x$ scan) | at least second order; constraints decrease in step |
| P2-C6 | physical singularity / coordinate degeneration / effective-theory breakdown: choose one | must be determined at $C\to0$ |

---

## 7. P2 acceptance checklist (roadmap §6.5)

| # | Acceptance item | Status in this report | Notes |
|---|---|---|---|
| 1 | constraints bounded and convergent; $\mathcal B$ bounded | **homogeneous part passes; 1+1 not done** | $\mathcal C_H$ converges with **time-integration tolerance** ($6.7\times10^{-6}\to5.1\times10^{-10}$); $\mathcal B=0$ analytic; spatial-resolution convergence not measured |
| 2 | energy-momentum conservation (including $\phi$–Maxwell exchange) | **homogeneous pass** | continuity residual $\sim10^{-17}$ |
| 3 | answer D2 | **pass (conditional)** | magnetically driven crossings iso 6/6, shear 23/35; barrier-top threshold §3.4; 12/35 shear are initial Kasner |
| 4 | if D2, give parameter ranges and energy conditions | **pass** | $f_c^{\rm iso}=2.93$, $f_c^{\rm shear}=4.73$; $\rho_B/V$ criterion; NEC saturated |
| 5 | if not, give falsification ranges | **pass** | barrier top $f<f_c$ excluded |
| 6 | two sets of results: local planar + spherical symmetry | **unmet** | §6; main reason P2 cannot be closed out |
| 7 | seven observables + L2 (added in checklist §1) | **homogeneous output** | §3.6–§3.7; 1+1 not done |

**P2 gate G4 verdict**: **conditional pass (homogeneous sector only)**. D2 is achieved and constraints/conservation are controlled, satisfying the literal conditions of G4; but §7 item 6 is unmet, so the P2 stage itself cannot be declared complete. P3 may start on the "effective theory/mode spectrum" side, but any external statement that "geometric dimensional collapse has been confirmed" must wait for P2-C1…C6.

---

## 8. Conclusions

1. **D2 exists**, but it is a **conditional result in the magnetic sector**, not a general conclusion. True-vacuum isotropic has no energy threshold but $t_{D2}\propto1/f$; shear requires $f\gtrsim0.5$ for a clear magnetically driven crossing (small-$f$ D2 is initial Kasner); the barrier top requires magnetic energy at $94\%$–$98\%$.
2. **Strict D3 does not hold**. The directional stress of a homogeneous magnetic field is transient; $C$ freezes/rebounds after contraction; only "relative degeneration" with $C/A\ll1$ holds.
3. **Initial shear is the key hidden parameter for D2**. For the same $f$, the isotropic initial-data threshold $2.93$ is far below the shear threshold $4.73$. This suggests realistic cosmological initial data (if near isotropic) favors DCC.
4. **Constraints, conservation, energy conditions, and Kretschmann are all under control**; the early negative-energy fake crunch was fixed by the $V\ge0$ shift.
5. **1+1 planar and spherical cases are not yet closed**. The non-asymptotic flatness of the planar wall is a physical obstacle, not an implementation detail; spherical symmetry is broken by the magnetic-field direction, requiring axisymmetric 2D. P2 can only be judged "conditional pass (homogeneous sector only)".

---

## Appendix A: Reproduction

```
python DCC_P2_homogeneous.py        # ~10–15 min; writes results + figures (including L2)
python DCC_P2_L2.py                 # ~1 min; independent short L2 run
python DCC_P2_local_planar.py       # negative-result diagnostic; prints VALIDITY: INVALID at final state
```

Key parameters: $v=\lambda=1$, $\alpha=0.5$, $\epsilon=0.01$, $\kappa=1$, $f_0=0.7$; LSODA rtol $10^{-11}$, atol $10^{-13}$, $t_{\rm end}=2000$.

## Appendix B: File list

| File | Contents |
|---|---|
| `DCC_P2_homogeneous.py` | homogeneous Bianchi I + scalar + magnetic-field solver; shear/isotropic initial data; scans; L2 |
| `DCC_P2_homogeneous_results.txt` | single cases + four scan sets + convergence/conservation tables |
| `DCC_P2_homogeneous_cases.png` | baseline-case time series ($H_i$, scale factors, energy, $\mathcal C_H$, $K$, $C/A$, $\ddot C/C$) |
| `DCC_P2_homogeneous_scan_*.png` | $\log_{10}(C/A)$ plots for the four scan sets |
| `DCC_P2_L2.py` | independent short L2 ($\ddot C/C$) run |
| `DCC_P2_L2_results.txt` | L2 results table (6 cases, $t_{\rm end}=400$) |
| `DCC_P2_local_planar.py` | gradient-approximation diagnostic (negative result) |
| `DCC_P1_metadata.md` | wall parameters/grid/observable definitions (cited source) |

---

**This report does not modify the frozen covariant documents.** If later 1+1 results indicate that new field equations or a new $Z(\phi)$ form are needed, follow document discipline: write an erratum first, then change the code.