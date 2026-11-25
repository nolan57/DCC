# DCC Research Roadmap Plan (P0–P4)

**Project**: Dimensional Collapse Conjecture (macroscopic dimensional phase transition model)
**Document Type**: Research roadmap / phase acceptance plan (formal version)
**Version**: Roadmap v2.7
**Date**: 2026-11-20
**Previous Version**: v2.6 (external review corrections) → this version (P3-C5 adiabatic criterion scan: withdrawal of the "critical = 1" intrinsic statement)
**Current Overall Status**: **P0 partially passed; P1a/P1b passed G1/G2; L1 closed; covariant reconstruction v1.1; P2 complete (D2 achieved in homogeneous + 1+1 full coupling; W3 no-flux control closed the causal chain; D3 not achieved; G4 passed); P3/P4 first round complete (mode freeze/energy gap, electromagnetic dimensional conversion, Fresnel transmission coefficients, geodesic rendering pipeline, G5 passed); full chain P0→P4 first-round closed loop. Deepening items: P2-C2/C4/C6, P3-C1…C5 (none change the first-round conclusions); P3-C5 completed and closed (adiabatic criterion scan, see §9/§15 v2.7).**

---

## 0. Document Positioning and How to Read

This file is the DCC project's **only master phase document**, answering three questions:

1. What exactly needs to be computed at each phase (P0–P4);
2. By what standard each phase is judged pass / fail (all acceptance criteria are quantifiable);
3. The **dependency relationships and termination conditions** between phases (under what circumstances work must stop, roll back, or be downgraded).

Supporting files:

| File | Role |
|---|---|
| `DCC_Covariant_Reconstruction_v1.md` | Phase 0 deliverable: unique metric + unified action + all covariant field equations + ADM structure + dimensional table |
| `DCC_sympy_derivation.py` | Machine-generation script for all the above symbolic expressions, one-click reproduction, the single source of truth for formulas |
| `DCC_P2_Symbols_and_Observables_Checklist_v1.md` | P2 project-initiation symbol review baseline (criteria / observables / Maxwell three confirmations) |
| `DCC_P1_metadata.md` | P1 delivery metadata table (single source of truth for P2 initial data) |
| `DCC_P2_Report_v1.md` / `DCC_P2_Report_v2.md` | P2 first round (homogeneous) / second version (homogeneous+1+1+spherical symmetry) reports |
| `DCC_P1_results.txt`, `DCC_P1_A4_results.txt` | P1a/P1b and A4 (L1 closure) numerical results |
| `DCC_P1_A4_maxwell_L1.py` | Maxwell numerical verification script for L1 closure |
| `DCC_P2_homogeneous.py`, `DCC_P2_1p1_wall_1p1.py`, `DCC_P2_wall_sph.py`, `DCC_P2_sph_derivation.py` | P2 three solver suites and spherical derivation |
| `DCC_P2_1p1_results.txt`, `DCC_P2_sph_results.txt`, `DCC_P2_1p1_frames.npz` | P2 numerical results and datasets |
| `DCC_P3_Effective_Theory_v1.md`, `DCC_P3_mode_freeze.py`, `DCC_P3_mode_freeze_results.txt` | P3 effective theory notes and mode-freeze numerical demonstration |
| `DCC_P4_pipeline.py`, `DCC_P4_pipeline_results.txt`, `DCC_P4_observation.png`, `DCC_P4_Report_v1.md` | P4 observer pipeline and results |
| `sympy_stdout.txt`, `sympy_sph_stdout.txt`, `sympy_T_stdout.txt` | Machine derivation stdout archive (JSON blocks = solver inputs) |

**Discipline clauses (apply project-wide)**:

- Any equation must be traceable to the unified action and unique metric; adjusting the metric, symbols or stress tensor to preserve a pre-set conclusion is prohibited.
- Any numerical result must simultaneously report the constraint residual $\mathcal C_H=\max(|\mathcal H|,|\mathcal M|)$; results whose residual drift exceeds the threshold are void.
- Any statement of "contraction" must specify its level (D1/D2/D3, see §7); acceleration differences must not be stated directly as contraction.
- Any physical quantity entering a deliverable must pass automated dimensional verification (§11.1).

---

## 1. Project Definition and Core Scientific Question

The proposition DCC tests is not "can space become two-dimensional", but rather:

> **Can we construct a self-consistent mechanism in which one field determines where the phase transition occurs (the phase-transition front), another physical degree of freedom determines which spatial direction undergoes geometric contraction (direction selection), and both together satisfy the Einstein equations?**

Split into three independently falsifiable sub-questions:

- **Q1 (front)**: Can the dynamics of the phase-transition order parameter $\phi$ self-consistently produce a phase-transition front (bubble wall) with finite thickness and a definite velocity?
- **Q2 (direction)**: Does there exist a directional degree of freedom whose stress-energy tensor gives $T^{\hat y}{}_{\hat y}\neq T^{\hat z}{}_{\hat z}$ in the full (inhomogeneous) bubble-wall geometry, and which drives $C(t,x)$ to contract in the Einstein equations while $B(t,x)$ remains finite?
- **Q3 (self-consistency)**: Does the above configuration satisfy all constraints (Hamiltonian / Momentum / Bianchi / Maxwell), energy conditions and linear stability, and is $C\to0$ a physical singularity or a coordinate degeneration?

**If Q1 and Q2 cannot hold simultaneously, P3 (matter dimensional reduction) and P4 (scientific rendering) can only be built on a specified geometric background, DCC remains at the level of a "geometric hypothesis model", and must not be presented externally as "a theoretical model with a dynamical origin".**

---

## 2. Frozen Theoretical Skeleton (P0 Deliverable, Shared by P1–P4)

### 2.1 Unique Metric

$$ds^2=-N^2(t,x)\,dt^2+A^2(t,x)\,dx^2+B^2(t,x)\,dy^2+C^2(t,x)\,dz^2$$

- $x$ = bubble-wall propagation (normal) direction; $y,z$ = transverse; $\partial_y=\partial_z=0$.
- **Direction convention (unified across the project, mixing prohibited)**: $A$ controls X, $B$ controls Y, $C$ controls Z. **DCC's contraction target is $C\to0$ (Z direction), with $B$ remaining finite.**
- **Do not impose $B=C$**: Y/Z anisotropy is the object of study itself.
- $\sqrt{-g}=NABC$; orthonormal frame $e^{\hat t}=Ndt,\ e^{\hat x}=Adx,\ e^{\hat y}=Bdy,\ e^{\hat z}=Cdz$; physical densities and pressures are read only in the orthonormal frame.
- The synchronous gauge $N=1,\ \beta^i=0$ may be used numerically, but coordinate singularities (geodesic crossing) must be monitored; if necessary, switch to 1+1 ADM with free lapse/shift.

### 2.2 Unified Action

$$S=\int d^4x\sqrt{-g}\left[\frac{R}{2\kappa}-\frac12(\nabla\phi)^2-V(\phi)-\frac14 Z(\phi)F_{\mu\nu}F^{\mu\nu}\right],\qquad \kappa=8\pi G,\ \ \hbar=c=1$$

### 2.3 Physical Division of Labor (P0 Frozen Version)

| Role | Carrier | Responsibility | Prohibitions |
|---|---|---|---|
| Phase-transition order parameter | $\phi(t,x)$ | Determines the distinction between normal and new phases, bubble-wall formation and propagation, front thickness and velocity | Must not claim a single $\phi$ can distinguish Y from Z |
| Directional stress source | Maxwell $F_{xy}=f$ (magnetic field along Z) | Provides anisotropic stress with $p_{\hat x}=p_{\hat y}=+\rho,\ p_{\hat z}=-\rho$ | Must not treat $f$ as an independently specifiable constant background |
| Geometric response | $A,B,C,N$ | Determines the actual scale evolution of each direction from the Einstein equations | Must not manually specify $C=e^{\sigma/M}$ and then infer motion backward |
| Phase-transition coupling | $Z(\phi)$ | Modulates the interaction between flux and the order parameter before/after the transition | **Must have $Z(\phi)>0$**; must not create contraction via $Z\to0$ (that is energy divergence / strong coupling, not energy release) |

### 2.4 Covariant Equations (Summary; full expressions in the reconstruction document)

- Einstein: $G_{\mu\nu}=\kappa\big(T^{(\phi)}_{\mu\nu}+T^{(F)}_{\mu\nu}\big)$
- Scalar: $\Box\phi-V'(\phi)-\tfrac14 Z'(\phi)F_{\mu\nu}F^{\mu\nu}=0$ (the v0 $Q^2/A^3$ term is void)
- Maxwell: $\nabla_\mu\!\left[Z F^{\mu\nu}\right]=0$, Bianchi: $\partial_{[\lambda}F_{\mu\nu]}=0$
- Field configuration $A_y(t,x)$: $f=\partial_x A_y$, $E=\partial_t A_y$; Bianchi gives $\partial_t f-\partial_x E=0$
- Electric flux conservation (constraint, not free initial data): $\dfrac{ZBC}{AN}E=P=\text{const}$
- Exchange conservation: $\nabla_\mu T^{\mu\nu}_{(\phi)}=-\tfrac14 Z'F^2\partial^\nu\phi$, $\nabla_\mu T^{\mu\nu}_{(F)}=+\tfrac14 Z'F^2\partial^\nu\phi$, total is conserved; **must not require the two fields to be independently conserved**

---

## 3. Global Phase Overview

| Phase | Name | Core Task | Prerequisite | Current Status |
|---|---|---|---|---|
| **P0** | Review of directional degrees of freedom | Select the directional degree of freedom; verify stress-energy tensor structure, field equations and constraints, feasibility of geometric response | — | **Partially passed** (Maxwell retained as priority; Phase 0 mathematical foundation complete; L1 closed, L2/L5 pending) |
| **P1a** | Fixed-background bubble wall | Solve for $\phi$ bubble-wall thickness / velocity / energy density on a Minkowski background | P0 | **Complete (G1 passed)**, convergence order 2.00 at four resolutions |
| **P1b** | Bubble wall + friction | Introduce phenomenological friction, solve for terminal velocity; distinguish relativistic solutions from the low-speed assumption group | P1a | **Complete (G2 passed, with qualifications)**, 42.47 km/s marked as uncontrolled extrapolation |
| **P2** | Anisotropic geometric response | ADM coupled evolution, test whether D1→D2→D3 is achievable | P0 leftover items closed + P1a | **Complete** (homogeneous + 1+1 planar periodic slab: D2 achieved; D3 not achieved; see `DCC_P2_Report_v2.md`) |
| **P3** | Matter theory of dimensional transition | Effective theory of 3D matter in the $C\to0$ limit; electromagnetic dimensional conversion; interfacial radiative transfer | P2 reaches D2 | **First round complete** (`DCC_P3_Effective_Theory_v1.md`: mode freeze / energy gap numerical demonstration + electromagnetic dimensional conversion + interface Fresnel coefficients; remaining P3-C1…C4) |
| **P4** | Observer and scientific rendering | Geodesics + frequency changes + radiative transfer, constructing images from actually received light | P3 | **First round complete (1+1 slab pipeline)** (`DCC_P4_pipeline.py`: geodesic frequency shift + transfer, no manual Doppler term; 2+1 axisymmetric imaging pending P2-C2 completion) |

**Mapping to covariant reconstruction Phases 0–3** (for cross-reference when both numbering systems are used):

| Phase (mathematical foundation line) | Corresponding phase | Content |
|---|---|---|
| Phase 0 | embedded in P0 | Fix metric and action, re-derive all equations, dimensional table — **complete** |
| Phase 1 | prerequisite of P1a | Homogeneous system verification: Einstein constraints, scalar equation, flux conservation, Bianchi — **complete** |
| Phase 2 | P1a/P1b | Evolve $f,E$ on a fixed background, check Bianchi constraint and electromagnetic energy conservation — **complete (A4: Bianchi $10^{-15}$, energy conservation $3.6\times10^{-10}$)** |
| Phase 3 | P2 | Full Einstein coupling, constraint-preserving evolution, NEC/WEC, linear stability, D1→D3 |

---

## 4. P0: Review of Directional Degrees of Freedom

### 4.1 Review History (Two Key Corrections, Must Be Retained in the Archive)

| Round | Original judgment | Corrected judgment | Impact |
|---|---|---|---|
| Round 4 review | $F_{yz}=\text{const}$ can select the Z direction | $B_x=F_{yz}$ selects the **X** direction; one should take $F_{xy}\neq0$ ($B$ along Z) | Direction candidates rewritten |
| Round 5 verification | Use the isotropic Friedmann form $\ddot a/a\propto-(\rho+3p)$ to judge direction by direction, eliminating Maxwell | **Incorrect**. In Bianchi I the acceleration in each direction contains shear and cross terms from other directions' pressures; with initially static data $\ddot A/A=+\kappa\rho_B$, $\ddot C/C=-\kappa\rho_B$, i.e. X/Y expand and Z contracts | Maxwell candidate **restored to priority** |
| Round 5 verification | "Flux energy is released" as $Z(\phi)\to0$ | At fixed flux $\rho_B\propto 1/Z\to\infty$, which is **energy divergence / strong coupling**, not release; $Z<0$ gives ghost states | Health condition $Z>0$ enshrined |
| Round 5 verification | Three-form $H_{txy}$ gives $p_z=-\rho_H$ | Actually $p_x=p_y=-\rho_H,\ p_z=+\rho_H$ (Z expands), opposite to the target | Three-form temporarily deprioritized |
| Round 4/6 review | "$B\to0$ means abandoning topological conservation" | Under global hyperbolicity + a non-degenerate metric, Cauchy-surface topology is conserved (Geroch–Bernal–Sánchez, **no extra energy condition required**); $C\to0$ is **metric degeneration**, the classical description reaches its boundary of validity, and the lower-dimensional spacetime beyond the degenerate surface requires an independent definition | Formulation formally rewritten (§4.5) |
| Round 9 review | Treat 5 Einstein components as 5 independent evolution equations; degrees of freedom = number of unknown functions | Switch to ADM decomposition: 2 constraints + 2 gauge + 4 evolution; net dynamical degrees of freedom = geometry 2 + scalar 1 + Maxwell 1 = **4** | Numerical framework switched to ADM |

### 4.2 Candidate-Field Evaluation Matrix (P0 Final)

| Candidate | Direction discrimination | Homogeneous initial geometric stress trend | Field-equation self-consistency | Physical origin | P0 verdict |
|---|---|---|---|---|---|
| Maxwell $F_{xy}$ ($B$ along Z) | Pass | Pass: Z contracts, X/Y expand (D1 level only) | Must simultaneously satisfy $\nabla_\mu(ZF^{\mu\nu})=0$ and $dF=0$; pure magnetic + inhomogeneous geometry is strongly constrained and must be solved together with geometry | Pass (requires explaining the origin and persistence of background flux) | **Retained as priority** |
| Three-form $H_{txy}$ | Pass | Fail: Z expands (opposite direction) | Requires full field equations | Pass | Temporarily deprioritized |
| Three-form $H_{xyz}$ | Fail (isotropic) | — | — | Pass | Temporarily deprioritized |
| Compactification modulus field | Pass | Possible (determined by $V_{\rm eff}$) | Must be derived from higher-dimensional reduction; $C\to0\Leftrightarrow\sigma\to-\infty$ is a runaway boundary, not an ordinary minimum | Fail (unclear macroscopic Z origin) | Conditionally retained (parallel route) |
| SSB vector field | Pass | Possible | Stability unverified ($A_0$ constraint, longitudinal mode, Hamiltonian lower bound, ghost / gradient instability, superluminality) | Conditional | Conditionally retained |

### 4.3 P0 Acceptance Items Already Passed

- **P0-1 Definition of directional candidates**: Passed. The actions, degrees of freedom and direction-selection methods of four candidate classes are clarified; terminology confusion between Maxwell-type two-form field strengths and higher p-form gauge potentials ($B_{\mu\nu}\to H=3\partial B$) has been resolved.
- **P0-2 Anisotropic stress review**: Passed (conditional). In the orthonormal frame a purely magnetic configuration gives $\rho=p_{\hat x}=p_{\hat y}=+\rho,\ p_{\hat z}=-\rho$; the Maxwell spatial stress formula has been corrected to $T_{\hat i\hat j}=\tfrac12\delta_{ij}B^2-B_{\hat i}B_{\hat j}$.
- **P0-3 Dynamics and constraint review (partial)**: The Bianchi identity and electric-flux conservation have been re-derived with the unified metric; the scalar coupling term corrected to $-\tfrac14 Z'F^2$.
- **P0-4 Geometric-response feasibility**: D1 level reached only under **homogeneous + initially static** conditions; the inhomogeneous case is unproven.

### 4.4 P0 Leftover Items (Hard Prerequisites for P2 Startup, Must Be Closed One by One)

| ID | Leftover item | Closure standard | Status |
|---|---|---|---|
| L1 | Solvability of Maxwell constraints in inhomogeneous geometry: do $\partial_t f-\partial_x E=0$ and $\partial_t\!\left(\frac{ZAC}{NB}E\right)-\partial_x\!\left(\frac{ZNC}{AB}f\right)=0$ have nontrivial solutions on a bubble-wall background (**note: v1.1 erratum E-1 corrected the denominator of the time term; in the constant-metric limit it reduces to $\partial_t(ZE)=\frac{N^2}{A^2}\partial_x(Zf)$**) | Provide an analytic special case or numerical evidence of existence | **Closed** (A4: Bianchi $10^{-15}$, static solution $f=Q/Z$ discretely exact to $10^{-13}$) |
| L2 | **Effective acceleration sign** of $C(t,x)$ during the phase-transition interval (non-stationary, inhomogeneous) | Output the $\ddot C/C$ time-series curve in the P2 first-round evolution | **Closed**: both homogeneous (in the D2 case $\ddot C/C>0$ at $H_C^{\min}$, contraction turning around) and 1+1 slab versions have been output (`DCC_P2_Report_v2.md` §2.2, §3.4) |
| L3 | Cosmological and initial-data origin of the background flux $Q/P$ | At least provide a self-consistent initial-data construction (dynamical generation not required) | **Unresolved — external input to the model**. All downstream numerics (P1a/P2 slab initial data f=Q/Z, P3 transfer) assume the flux charge is given; until a dynamical generation mechanism is provided, Q/P must be declared explicitly as external parameters and must not be silently omitted |
| L4 | Specific form of $Z(\phi)$ (requiring $Z>0$, e.g. $Z=e^{\alpha\phi/M}$ only as a candidate) | Freeze a minimal model and perform a health check | **Frozen (retroactively confirmed in v2.6)**: Z(phi)=exp(alpha*phi/v), alpha=0.5, v=1 (values frozen in P1a). Health check: Z stays >0 throughout [0.6065,1.6487] (measured in P1a/P2 runs); the A4/P3 Fresnel coefficients are based on this form. Frozen earlier in P1a; this item retroactively registers it |
| L5 | Higher-dimensional derivation of the modulus-field route (parallel line, does not block P2) | Separate technical report | |

### 4.5 Formal Statement (to Be Written into Project Documents, Must Not Be Rewritten into a Stronger Conclusion)

> The target model of DCC allows the scale factor of some spatial direction to tend to zero, and allows classical non-degenerate Lorentzian geometry to fail at the phase-transition interface. But **a scale factor tending to zero does not automatically prove a change of manifold topology**; the lower-dimensional spacetime beyond the degenerate interface requires an independent definition, and the matching conditions between the higher- and lower-dimensional descriptions, interface singularity, energy accumulation and causal structure all require separate study.

> Carroll–Johnson–Randall 2009 (dynamical compactification of higher-dimensional de Sitter + flux) is positioned as a **reference for the existence of a mechanism**: it proves that constructions of the type "gravity + flux can support a solution with dimensional asymmetry" exist, and **does not constitute** proof that "the macroscopic Z direction we have observed can be compressed by a local bubble wall".

---

## 5. P1: Phase-Transition Bubble-Wall Dynamics

### 5.1 P1a Fixed-Background Bubble Wall (Minkowski Background, No Gravitational Backreaction)

**Equation**: $\Box\phi-\dfrac{dV}{d\phi}=0$, background $\eta_{\mu\nu}$; for connection with P2, also implement a version "containing the $Z(\phi)F^2$ source term".

**Potential prototype (for research, not the final DCC potential)**:

$$V(\phi)=\frac{\lambda}{4}\left(\phi^2-v^2\right)^2+\epsilon\,\frac{\phi}{2v}\quad(\text{double well + slight tilt})$$

**Initial/boundary-value setup**:

- Take the initial $\phi(0,x)$ as a kink / thick-wall analytic approximate profile, with $\dot\phi(0,x)$ given initial velocity (two groups: zero velocity and relativistic velocity);
- Boundaries: outgoing at both ends (or periodic + double-bubble nucleation configuration);
- Resolution must resolve the wall thickness $\delta\sim(\sqrt\lambda\,v)^{-1}$, with a $\delta/\Delta x$ convergence test.

**Outputs**: wall thickness $\delta(t)$, wall velocity $v_w(t)$, wall-surface energy density $\sigma_w$, $\phi$ energy spectrum, total-energy conservation residual.

**Acceptance criteria**:

1. Thin-wall / thick-wall limits agree with analytic results (or public benchmarks), convergence order $\ge 2$;
2. Energy conservation residual $|E(t)-E(0)|/E(0)<10^{-6}$ (frictionless case);
3. The wall does not break up and no grid noise accumulates;
4. Output $\delta,\ v_w,\ \sigma_w$ as initial-data inputs for P2.

### 5.2 P1b Bubble Wall + Friction (Terminal Velocity)

**Equation**: $\Box\phi-V'(\phi)-\tfrac14 Z'F^2=\eta(\phi,T)\,\dot\phi$ (phenomenological friction term, or a simplified model coupled to plasma transport).

**Must answer**:

- No friction → wall accelerates, asymptotically approaching the speed of light;
- Strong friction → a terminal velocity exists, $F_{\rm drive}=F_{\rm friction}$;
- Terminal velocities in the literature are typically **relativistic** ($\beta_w\sim0.1$–$1$).

**Disposition of the identity of $42.47\ \mathrm{km/s}$ (formal decision)**:

| Item | Disposition |
|---|---|
| Definition | $v_f=12\,742\ \mathrm{km}/300\ \mathrm{s}\approx42.47\ \mathrm{km/s}$, $\beta_f\approx1.42\times10^{-4}$ |
| Identity | **Low-speed front phenomenological ansatz group**, used only to satisfy the visual experiment target of "sweeping across Earth in 300 seconds" |
| Prohibition | Must not be stated as "the natural terminal velocity of a standard first-order phase-transition bubble wall under plasma friction" or any theoretical prediction |
| If a physical interpretation is insisted upon | A concrete mechanism making the friction strength orders of magnitude above typical electroweak-phase-transition values must be provided and reviewed as an independent topic |
| Parallel track | A **relativistic bubble-wall experimental group** ($\beta_w\sim0.1$–$1$) must be set up in parallel, with the two groups' results archived separately |

**Scale warning**: If the wall crosses Earth at near-light speed, the crossing time is only $t\approx12\,742\ \mathrm{km}/c\approx0.0425\ \mathrm{s}$, about 3 orders of magnitude different from the original "several minutes" setting — this difference must be written into P4's rendering premises.

**Acceptance criteria**: Provide the phase diagram of $\beta_w$ versus friction strength; specify the friction-parameter interval needed for $\beta_w\sim10^{-4}$ and judge whether it lies within the controllable domain of the effective theory.

**G1/G2 measured conclusions (2026-11-19, see `DCC_P1_results.txt` §3)**:

- Using the relativistic terminal velocity $\beta_w=(F/\eta)/\sqrt{1+(F/\eta)^2}$, scan variable $\eta\equiv\eta_{\rm eff}/\sigma_w$, $F_{\rm eff}=\epsilon/\sigma_w=0.010607$;
- Reaching $\beta_f=1.4166\times10^{-4}$ requires $\eta_{\rm target}=F_{\rm eff}/\beta_f=\mathbf{74.9}$ (absolute friction $\eta_{\rm eff}=70.6$);
- $\eta/(\lambda v^4)\approx75\gg1$, outside the original scan interval $[0,1]$ and far beyond the weak-dissipation domain of validity → **"whether it lies within the controllable domain of the effective theory" is judged FAIL**;
- This FAIL is a **permanently archived conclusion** and will not be rewritten due to later parameter adjustments; $\beta_w\sim10^{-4}$ may only be used when explicitly labeled "phenomenological ansatz group".

---

## 6. P2: Anisotropic Geometric Response (Core Phase)

### 6.1 Numerical Framework: ADM 1+1 Reduction

$$ds^2=-N^2dt^2+A^2(dx+\beta\,dt)^2+B^2dy^2+C^2dz^2$$

- Extrinsic curvature $K_{ij}=-\dfrac{1}{2N}\left(\partial_t\gamma_{ij}-\mathcal L_\beta\gamma_{ij}\right)$, $\gamma_{ij}=\mathrm{diag}(A^2,B^2,C^2)$;
- Evolution variables: $(A,B,C)$, the diagonal components of $K_{ij}$, $\phi$, $A_y$ (or first-order form in $E,f$);
- Division of equations: **Hamiltonian constraint $\mathcal H=0$ (initial data) + Momentum constraint $\mathcal M_i=0$ (initial data) + evolution equations**;
- Use a constraint-preserving scheme (constraint damping / regularization), output $\mathcal C_H$ at every step.

### 6.2 Solution Procedure

1. Freeze $V(\phi)$, $Z(\phi)>0$, flux charge $P$ (or $Q$);
2. Construct $\phi(0,x),\dot\phi(0,x)$ and the wall profile from P1a outputs;
3. Solve $A,B,C$ and their initial extrinsic curvature from the constraint equations (**must not be freely specified**);
4. Evolve Einstein + scalar + Maxwell simultaneously;
5. Record observables (§6.3) and constraint residuals at each step;
6. Convergence: double the grid, scan $\delta/\Delta x$, and require the constraint residual to decrease correspondingly.

### 6.3 Observables (All Must Be Output)

| Symbol | Definition | Interpretation |
|---|---|---|
| $\mathcal R_H$ | $H_z/H_x$ ($H_i=\dot a_i/a_i$) | Anisotropic expansion rate; D1 criterion. **Prerequisite note (v2.6)**: when H_x>0, R_H<1 is equivalent to D1; when H_x<=0 the sign of the ratio loses criterion meaning, and D1 is then read directly via the inequality H_z<H_x (the P2 implementation uses the inequality) |
| $\mathcal R_L$ | $C/A$, $C/B$ | Relative scale evolution; must be converted to **physical geodesic lengths**, not coordinate values |
| $\mathcal K$ | $R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}$ | Distinguish a physical singularity from coordinate degeneration |
| $\mathcal E$ | $T_{\mu\nu}n^\mu n^\nu$ | Local energy density; monitor whether $\rho_B\propto1/Z$ or $1/C^n$ diverges |
| $\mathcal C_H$ | $\max_x(|\mathcal H|,|\mathcal M|)$ | Constraint residual; void if above threshold |
| $\mathcal B$ | $\max_x|\partial_t f-\partial_x E|$ | Bianchi constraint residual |
| NEC/WEC | $T_{\mu\nu}k^\mu k^\nu\ge0$, $T_{\mu\nu}n^\mu n^\nu\ge0$ | Whether energy conditions must be violated to reach D3 |

### 6.4 DCC Criterion Hierarchy (Mixing Prohibited)

| Level | Mathematical condition | Physical meaning | Proven by |
|---|---|---|---|
| **D1** | $H_z<H_x$ | Z-direction expansion weaker than transverse | Already obtained analytically under homogeneous + initially static conditions ($\ddot a_z/a_z-\ddot a_x/a_x=-2\kappa\rho<0$) |
| **D2** | $H_z<0$ | Z direction actually contracts | Must be given by full coupled numerical evolution |
| **D3** | $C\to0$ with $A,B$ finite | Genuine directional geometric degeneration | Must be jointly supported by D2 + $\mathcal K$ behavior + geodesic lengths |

**Note**: An acceleration difference only gives D1; both directions expanding with a smaller $a_z$ acceleration also satisfies D1. Any "Z contraction" conclusion must reach at least D2.

### 6.5 P2 Acceptance Criteria (Go/No-Go Gate)

1. Constraint residual $\mathcal C_H$ and Bianchi residual $\mathcal B$ remain bounded throughout and converge with resolution;
2. Total energy-momentum conservation (including $\phi$–Maxwell exchange terms) residual reaches the set precision;
3. Explicitly answer: **does there exist a solution satisfying all constraints in which $C$ contracts while $B$ remains finite** (D2 achieved or not);
4. If D2 is achieved: report the required $Q/P$, $Z(\phi)$ parameter interval and energy-condition status;
5. If D2 is not achieved: give the falsification scope (which part of parameter space is excluded), and trigger the downgrade path in §12;
6. Give both local planar bubble-wall and spherically symmetric bubble-wall results — **the local planar front solution must not be treated as the global solution of a complete spherical bubble**.

---

## 7. P3: Matter Theory of Dimensional Transition

**Prerequisite**: P2 reaches at least D2 (a self-consistent solution with $H_z<0$ exists).

**Tasks**:

1. **Effective theory of 3D matter in the $C\to0$ limit**: field-mode spectra in Kinnersley-type collapse geometry, mode freeze and energy-gap behavior; confirm the degrees-of-freedom count of the effective description.
2. **Dimensional conversion of the electromagnetic field**: mass spectra and observables of the components of $A_\mu$ as $C\to0$; whether the self-consistent coupling of the background $F_{xy}$ in P2 to the matter electromagnetic field breaks the P3 effective theory.
3. **Radiative transfer at the phase interface**: microscopic inputs for interface transmittance, absorption and scattering; relativistic beaming and frequency shifts must not be superposed directly as "visual effects".
4. **Matching conditions at the degenerate surface**: matching conditions for the higher-/lower-dimensional descriptions on the two sides of $C\to0$, interface stress and possible singular shells.

**Acceptance criteria**: Give explicit results for the observable spectrum in the low-dimensional phase (mode density, energy gap, transport coefficients), and explain its domain of applicability and failure points relative to the P2 geometric solution.

---

## 8. P4: Observer and Scientific Rendering

**Prerequisite**: P3 provides interface radiative-transfer coefficients and the low-dimensional-phase effective theory.

**Tasks**:

1. Solve light-ray geodesics (including geometric jumps across the bubble wall);
2. Compute frequency changes (observer four-velocity + emission-point four-velocity, including gravitational and kinematic contributions);
3. Perform radiative transfer along geodesics to obtain the intensity spectrum actually received by the observer;
4. Construct images/videos from received light; every visual parameter must be traceable to an upstream computed quantity.

**Acceptance criteria**:

1. The rendering pipeline contains **no manually specified Doppler / beaming factors**; all are given by geodesics and radiative transfer;
2. Explicitly mark which frames are in the "classical geometry validity region" and which have entered the hypothetical layer beyond the degenerate surface;
3. Output two sets of results corresponding to the two P1b wall-speed groups (low-speed ansatz group vs. relativistic group), explicitly declaring the former a phenomenological assumption.
4. (Added in v2.6, review break point 4) **Exposure duration vs. visual persistence verdict**: compare the event duration with human-eye integration time (0.05–0.1 s) — the relativistic group (t≈0.0425 s, §5.2) is shorter than visual persistence and can only be perceived as a flash, not a "scene"; the low-speed group lasts long enough but is a phenomenological assumption (P1b FAIL permanently archived);
5. (Added in v2.6, review break point 4) **Surface-brightness order-of-magnitude verdict**: with interface transmission 94% / reflection 6% (P3 §4), image visibility requires explicitly giving the emission / scattering radiative source terms and their contrast with background brightness — "being visible" itself is a premise to be tested, not an already-completed acceptance item.

---

## 9. Phase Dependencies and Parallel Relationships

```
P0 (partially passed)
 ├── Phase 0 mathematical foundation ────── complete
 ├── L1 (Maxwell solvability) ───────── closed (A4)
 ├── L2–L4 ───────────────┐      L2 output from P2 first round
 └── modulus-field parallel line L5     │
                            ▼
                     P1a (fixed-background bubble wall) ── G1 passed
                            │   └── Phase 1 homogeneous verification complete
                            ▼
                     P1b (friction / terminal velocity) ── G2 passed (with qualifications)
                            │
                            ▼
                  P2 (ADM coupled evolution, D1→D2→D3) ── complete (D2 achieved, D3 not reached)
                            │
                            ▼
                     P3 (matter dimensional reduction + interfacial radiative transfer)
                            │
                            ▼
                     P4 (geodesics + radiative transfer + rendering)
```

**P3-C5 To-Do Registration (Added in v2.7, higher priority than P2-C2)**:

| ID | Status | Deliverable | Notes |
|---|---|---|---|
| P3-C5 | **Completed and closed** (2026-11-20) | `DCC_P3_C5_adiabatic_scan.py` + `DCC_P3_C5_Scan_Report_v1.md` + stdout archive + outputs 1–4 | Parameter-sensitivity scan of the adiabatic criterion; both prerequisites backfilled; regression η=1 error 0; two runs byte-for-byte identical; satisfies the termination condition "robust region occupies the majority → close", allowing a conditional external conclusion (carrying the specified-background / D3-not-achieved / phenomenological / given-p_z qualifications). If D3 is achieved, must rerun with dynamical C(t). |

**Key dependency statements**:

- L1 is closed (`DCC_P1_A4_maxwell_L1.py`, Bianchi $10^{-15}$, static solution $10^{-13}$). The P2 startup blockage is removed; E-1…E-8 were corrected in covariant reconstruction v1.1, and the P2 implementation must use the divergence form, otherwise it will "stably solve a set of mutually inconsistent equations".
- L2 (sign of $\ddot C/C$) is closed: both homogeneous and 1+1 slab versions have been output (in the D2 case $\ddot C/C>0$ at $H_C^{\min}$, contraction turning around; near zero in non-D2 cases). Interpretation in `DCC_P2_Report_v2.md` §2.2, §3.4.
- The geometric inputs for P3/P4 must come from P2's numerical solution; if P2 stops at D1, P3/P4 can only be labeled "specified geometric background" and the strength of conclusions is correspondingly downgraded.

---

## 10. Milestones and Deliverables

| Milestone | Deliverable | Reviewer |
|---|---|---|
| M0 (achieved) | `DCC_Covariant_Reconstruction_v1.md` + `DCC_sympy_derivation.py` | Third-party theoretical review passed |
| M1 | P0 leftover items L1–L4 technical memos (including L1 existence evidence) | Internal review |
| M2 | P1a numerical code + convergence test report + wall parameter table | Internal review |
| M3 | P1b phase diagram ($\beta_w$ vs. friction strength) + low-speed-group identity statement | Internal review |
| M4 | P2 evolution dataset + observable time series + D1/D2/D3 verdict report | Third-party review |
| M5 | P3 effective theory notes (mode spectra + interface transfer coefficients) | Internal review |
| M6 | P4 rendering pipeline + traceable parameter table + finished film | Internal review |

**Milestone sign-off status (registered in v2.6)**: M0–M3 and M5 have passed internal review; M4 (P2 deliverables) **not submitted for review** — G4's [pass] is an internal verdict, third-party sign-off pending; the M6 (P4) pipeline part has been delivered, finished film pending after P2-C2.

---

## 11. Cross-Cutting Workflows (Required at Every Phase)

### 11.1 Automated Dimensional and Symbolic Verification

Establish an independent symbolic dimensional table ($c=\hbar=1$, $[x]=[t]=M^{-1}$): $[g_{\mu\nu}]=[N]=0$, $[R]=[G_{\mu\nu}]=M^2$, $[\kappa]=M^{-2}$, $[\phi]=M^1$, $[V]=M^4$, $[Z]=0$, $[A_y]=M^1$, $[F_{\mu\nu}]=M^2$, $[T_{\mu\nu}]=M^4$. Before numerical implementation, a script automatically verifies dimensional consistency of all terms in every equation of motion; scale factors use a dimensionless comoving convention, physical length $=A\Delta x$ etc., and when coordinate normalization changes, $A_y,P$ must be rescaled accordingly.

### 11.2 Symbolic Reproducibility

All analytic expressions are generated from `DCC_sympy_derivation.py`; hand-copying into code is prohibited; new equations are added to the script first, then to the solver.

### 11.3 Energy Conditions and Singularity Monitoring

NEC/WEC, the Kretschmann scalar and geodesic completeness are standard outputs of every evolution; at $C\to0$ one must decide among "physical singularity / coordinate degeneration / effective-theory failure".

### 11.4 Linear Stability

After obtaining a background solution in P2, perform linear perturbations: ghost states (kinetic-energy sign), gradient instability ($c_s^2<0$), $A_0$-type constraint modes, superluminal propagation; if the SSB vector-field route is adopted, this item is a prerequisite for passing.

### 11.5 Documentation Discipline

Every conclusion change must: state the withdrawn original conclusion, the reason for withdrawal, and the conditions of applicability of the new conclusion; silent overwriting is prohibited.

---

## 12. Risk Register and Downgrade Paths

| Risk | Trigger signal | Response / downgrade path | Status (v2.6) |
|---|---|---|---|
| No solution for inhomogeneous Maxwell | L1 remains unclosed for a long time | Introduce extra field components or source terms (field equations must be explicitly modified and explained); or switch to the modulus-field route L5 | **Resolved** (L1 closed: Bianchi 1e-15, static solution 1e-13) |
| D2 unreachable | $H_z$ stays $\ge0$ throughout P2 evolution | Output the falsified parameter interval; reposition DCC as an "anisotropic expansion (D1) model", with P3/P4 downgraded accordingly | **Resolved** (G4: D2 achieved in homogeneous and 1+1 slab cases; W3 no-flux control) |
| $\rho_B$ divergence | $\mathcal E$ or $\mathcal K$ blows up numerically | Check whether $Z\to0$ was misused; switch to a bounded positive coupling $Z(\phi)$; define the effective-theory cutoff scale | Under monitoring (ρ_B bounded in homogeneous/slab runs; E-6 configuration ∝1/C² strong-coupling region not entered) |
| Synchronous-coordinate singularity | $A\to0$ or grid collapse, $\mathcal C_H$ spike | Switch to free lapse/shift gauge or extreme-spacelike-slicing-type conditions  Partially triggered (1+1 slab: synchronous gauge Mom large-scale drift; being addressed in P2-C4) |
| Ghost / gradient instability | Negative-energy modes in linear perturbations | Exclude that candidate and reselect from the P0 candidate matrix  Not assessed (P2-C6) |
| Constraint drift | $\mathcal C_H$ grows with time | Results void; rerun with a constraint-preserving scheme  Under monitoring (homogeneous 5e-6; 1+1 converges with resolution) |
| Conclusions misread as physical predictions | Phenomenological parameters such as $42.47\ \mathrm{km/s}$ mixed into external statements | Mandatorily label every figure / conclusion paragraph with "phenomenological assumption" or "dynamical solution"  Continuously enforced (phenomenological labels, D3-not-achieved labels, frame-validity labels in place) |
| "η=1 exactly at critical" misread as an intrinsic model property (P3-C5) | P3 §2 old statement "p_z=0.5 exactly at boundary 1.0" treated as an intrinsic critical value | Revise per P3-C5: criticality is determined by parameter choices (β_C, normalization, representative p_z); η=1 is only a monotonic crossing point; externally sign only conditional conclusions | **Reworded and signed off (v2.7)**: see §15 v2.7 and `DCC_P3_C5_Scan_Report_v1.md` §7.2; the robust-destruction region is empty in the reasonable interval, the robust-adaptation region occupies 35–55%; still carries the specified-background / D3-not-achieved / phenomenological / given-p_z qualifications |

---

## 13. Current Decision Gates (Go / No-Go)

| Gate | Location | Pass condition | Current verdict |
|---|---|---|---|
| G0 | P0 → P1 | Directional degree of freedom selected, equations self-consistent, dimensional check passed | **Passed** (Maxwell priority, modulus field parallel) |
| G1 | P1a → P1b | Bubble-wall convergence, energy conservation meets target | **Passed** (convergence order 2.00–2.01; $E_{\rm res}=1.17\times10^{-7}$) |
| G2 | P1b → P2 | Terminal-velocity phase diagram complete, low-speed-group identity clear | **Passed (with qualifications)** (phase diagram complete; 42.47 km/s judged an uncontrolled extrapolation and permanently archived) |
| G3 | P0 → P2 | L1, L2 closed | **Passed**: L1 closed (A4); L2 closed (homogeneous + 1+1 slab $\ddot C/C$ both output, since v2.4) |
| G4 | P2 → P3 | D2 achieved and constraint / conservation residuals controlled | **Passed**: D2 achieved in homogeneous (magnetically driven 43/55+10/55, initial Kasner listed separately) and the 1+1 fully coupled system (periodic slab W1/W2 inner and outer regions H_C<0; **W3 no-flux control does not contract** — causal closure); f_c interval reproduced (shear∈(4,5), iso∈(2,3)); C_H homogeneous ~5×10⁻⁶, 1+1 converges with resolution (second order); NEC/WEC satisfied throughout; strict D3 not achieved (power-law contraction); spherical machine-derivation check closed, initial-data elliptic solve (York conformal flatness) is the remaining P2-C2 step; residual handover items P2-C4 (energy accounting), P2-C6 (linear stability) do not block P3 |
| G5 | P3 → P4 | Interface transfer coefficients available | **Passed**: single-wall Fresnel coefficients T=0.940015/R=0.059985 (Z∈[0.61,1.65], normal incidence); finite-wall-thickness transfer matrix and resonance spectrum are P3-C2 |

**P2 prerequisite actions (executed)**: E-1…E-8 were corrected in `DCC_Covariant_Reconstruction_v1.md` v1.1; the P2 project-initiation document (`DCC_P2_Symbols_and_Observables_Checklist_v1.md`) has been synchronized. The P2 first round (homogeneous Bianchi I) has been executed, results in `DCC_P2_Report_v1.md`; full 1+1 and axisymmetric spherical symmetry are still not closed (P2-C1…C6). The divergence-form Maxwell equations must be used in implementation. L1 has been closed by `DCC_P1_A4_maxwell_L1.py`:

- $\alpha=0$ control $R=2\times10^{-11}$ (format correct);
- At $\alpha=0.5$, $R=0.1093$, $T=0.8907$, $1-R-T<10^{-9}$;
- Bianchi residual $9.7\times10^{-16}$, electromagnetic energy conservation $3.6\times10^{-10}$, static flux solution discretely exact to $1.5\times10^{-13}$.

P2 has output $\ddot C/C$ (L2) and seven observables (two sets, homogeneous and 1+1 slab; P2-C3 closed, see `DCC_P2_Report_v2.md`).

---

## 14. Appendix: Quick Reference for Symbols and Conventions

| Symbol | Meaning |
|---|---|
| $N,A,B,C$ | lapse and three spatial scale factors (X/Y/Z); **the Z direction is controlled by $C$** |
| $\phi$ | phase-transition order parameter |
| $V(\phi)$ | double-well potential (prototype, not frozen) |
| $Z(\phi)$ | gauge coupling function, **must be $>0$** |
| $F_{xy}=f$ | magnetic component (magnetic field along Z), source of directional stress |
| $F_{ty}=E$ | electric component, used to lift the time-independent constraint of the purely magnetic configuration |
| $P$ | electric flux charge, $P=\frac{ZBC}{AN}E$; **Gauss constraint only in the longitudinal ($A_x$) sector**, not applicable to transverse $A_y$ polarization (see E-2) |
| $\kappa$ | $8\pi G$ |
| $H_i$ | $\dot a_i/a_i$, directional expansion rates |
| D1/D2/D3 | three-level criteria: anisotropic expansion / actual contraction / geometric degeneration |
| f_c (G4 criterion quantity, added in v2.6) | critical background magnetic field reaching D2 from barrier-top (phi=0) initial data: iso-sector f_c in (2,3), shear-sector f_c in (4,5); the 55 cases in the G4 row = 11 f values × 5 H0 values (see P2 Report v2 §2.1 for the denominator and D2 semantics) |
| $\mathcal R_H,\mathcal R_L,\mathcal K,\mathcal E,\mathcal C_H,\mathcal B$ | observables: anisotropic expansion-rate ratio / relative scale / Kretschmann / local energy density / constraint residual / Bianchi residual |
| $v_f=42.47\ \mathrm{km/s}$ | **low-speed front phenomenological ansatz group**, not a theoretical prediction |
| E (sign convention, v2.6 note) | In this version E=∂tA_y and Bianchi is ∂t f−∂x E=0; early documents before 2026-11-19 and the G1 report used E=−∂tA_y and ∂t f+∂x E=0 — when citing E values across documents the sign is reversed, so conversion per this table is required first |
| E (sign convention, v2.6 note) | In this version E=∂tA_y and Bianchi is ∂t f−∂x E=0; early documents before 2026-11-19 and the G1 report used E=−∂tA_y and ∂t f+∂x E=0 — when citing E values across documents the sign is reversed, so conversion per this table is required first |

---

**End of document. This version of the roadmap supersedes all previous P0–P4 drafts and E0–E5 architectures; in case of conflict, this file and `DCC_Covariant_Reconstruction_v1.md` prevail.**

---

## 15. Revision History

### v2.7 (2026-11-20) — P3-C5 Adiabatic Criterion Scan: Withdrawal of the "critical = 1" Intrinsic Statement

Basis: `DCC_P3_C5_Scan_Report_v1.md`, `DCC_P3_C5_adiabatic_scan.py`, `DCC_P3_C5_adiabatic_scan_stdout.txt`, outputs 1–4. The first two prerequisites (origin of p_z=0.5, basis for t*/C(t*)/β_C) have been backfilled, regression η=1 error 0, reproducibility byte-for-byte identical.

| Location | Change | Reason |
|---|---|---|
| §9 | Added P3-C5 to-do registration (completed and closed, higher priority than P2-C2) | Task specification P3-C5 closed; must rerun after D3 is achieved |
| §12 | Added risk-table row "η=1 exactly at critical misread as intrinsic property", status "reworded and signed off (v2.7)" | The scan changes whether the "destruction / adaptation" conclusion can be signed off |
| P3 effective theory §2 interpretation 1 | "p_z=0.5 exactly at boundary 1.0" rewritten as an account of parameter-choice dependence (see that document's v1.1 revision) | η=1 is only a monotonic crossing point, not an intrinsic critical value |
| §15 | Added this entry | Documentation discipline |

**Change in external statement (explicitly registered because of this scan revision)**:
Withdraw the statement "current parameters are exactly at critical (η=1)", which implied "criticality is an intrinsic property"; the reason for withdrawal is that the location of η=1 is jointly determined by β_C, the normalization C0/t0 and the representative p_z (varying β_C within O(1) shifts the critical p_z by ±1/3), and the η formula does not contain α or wall speed (it has no discriminating power for either).
New statement: under a specified contraction background (D2, not D3), criticality is a product of parameter choices; the model can give robust conclusions under O(1) parameter variations — p_z≳\|β_C\| robustly adiabatically freezes, and the robust-destruction region is empty within the reasonable interval; the criterion has no discriminating power for α or wall speed. All conclusions carry the specified-background / D3-not-achieved / low-speed-group-phenomenological / given-p_z qualifications.

**Termination verdict**: satisfies "robust region occupies the majority → close"; does not fall under "indistinguishable → register D3 dependence".
**Unchanged**: D1/D2/D3 criteria; the 42.47 km/s phenomenological identity; P0/P1/P2 conclusions; covariant document v1.1.

### v2.6 (2026-11-20) — External Review Corrections: 4 Internal Inconsistencies + 6 Completeness Items + Optical Criteria

Basis: external review comments (2026-11-20). All are documentation synchronization/completeness corrections and criterion supplements, **without changing any physical conclusion**.

| Location | Change | Corresponding review item |
|---|---|---|
| §13 G3 | "Conditional pass" upgraded to "pass" (L1, L2 both closed) | Inconsistency 1 |
| §9 / §13 | Deleted the P2-C3 "pending" sentence (closed in v2.4; C̈/C output for homogeneous+1+1 both available) | Inconsistency 2 |
| §9 dependency graph | P2 "can start" → "complete (D2 achieved, D3 not achieved)" | Inconsistency 3 |
| Throughout | `DCC_sympy_derivation.py.py` → `.py` (actual file renamed; old and new output JSON byte-for-byte identical) | Inconsistency 4 |
| §4.4 L3/L4 | Status column completed: L4 freeze retroactively confirmed (Z=e^{αφ/v}, α=0.5), L3 labeled "unresolved, external input to the model" | Completeness 1 |
| §14 symbol table | Added f_c (G4 criterion quantity) and historical note on the E sign convention (opposite sign to pre-2026-11-19 documents) | Completeness 2/7 |
| §10 | M4 third-party sign-off status explicitly registered (not submitted for review) | Completeness 3 |
| §0 | Supporting-file table expanded to a full index (10+ files) | Completeness 4 |
| §12 | Risk register given a status column (2 resolved, 4 under monitoring / not assessed) | Completeness 5 |
| §6.3 R_H | Prerequisite note: when H_x≤0 the ratio loses criterion meaning, D1 read via inequality | Completeness 6 |
| §8 P4 acceptance | Added item 4 (exposure duration vs. visual persistence) / 5 (surface-brightness order of magnitude) | Review break point 4 |
| P3 document §2.1 + `DCC_P3_optical_check.py` | **Optical-indistinguishability criterion** (completing checklist item ①): L_z=(C/C0)L0≤λ_obs≈500nm inequality verdict — P2's reached depth (~0.10) insufficient for macroscopic L0 (7 orders of magnitude short); micron-scale initial thickness achievable (t/t0~4); any L0 achievable after D3 is realized | Review break point 2 (highest-leverage item) |
| P4 report | List of "sayable / unsayable" statement boundaries | Review break points 1/2/3/4 summary |

**Carrying forward the core-question verdict (review §3)**: The current chain can generate an "apparent image when a phase-transition interface sweeps across an observer", but **cannot** be stated as a model prediction of "a two-dimensionalized scene as seen by the human eye" — two of the four break points are hard breaks (D3 not achieved, optical criterion not closed for macroscopic L0), while the other two (finite-region exterior shape, exposure / brightness acceptance) have clear completion paths (§9/§10).

### v2.5 (2026-11-20) — P3/P4 First Round Complete, G5 Passed

Basis: `DCC_P3_Effective_Theory_v1.md`, `DCC_P3_mode_freeze_results.txt`, `DCC_P4_pipeline_results.txt`, `DCC_P4_observation.png`.

| Location | Change | Reason |
|---|---|---|
| §3 | P3/P4 changed to "first round complete"; G5 passed | P3 mode freeze / energy-gap numerical demonstration + electromagnetic dimensional conversion + Fresnel coefficients; P4 geodesic pipeline (no manual Doppler term) |
| §13 G5 | Passed (T=0.940015/R=0.059985; finite-wall-thickness transfer matrix remaining in P3-C2) | Interface transfer coefficients available |
| §15 | Added this entry | Documentation discipline |

**P3/P4 remaining items registered**: P3-C1 (particle-production spectrum), P3-C2 (finite-wall-thickness transfer matrix / resonance spectrum, quantitative analysis of interface energy accumulation), P3-C3 (fermion / full-polarization transport), P3-C4 (axisymmetric 2+1 mode analysis), P2-C2 (spherical initial-data York elliptic solve), P2-C4 (energy accounting / Mom large-scale drift mitigation), P2-C6 (linear stability). All are deepening items and do not change the P2-P4 first-round conclusions.

**Unchanged**: D1/D2/D3 criteria; the 42.47 km/s phenomenological identity; P0/P1/P2 conclusions.

### v2.4 (2026-11-20) — P2 Complete: 1+1 Planar and Spherical Closure, G4 Upgraded to Passed

Basis: `DCC_P2_Report_v2.md`, `DCC_P2_1p1_results.txt`, `DCC_P2_sph_results.txt`, `DCC_sympy_derivation.py` (v1.2 machine-derivation addendum), `DCC_P2_sph_derivation.py`.

| Location | Change | Reason |
|---|---|---|
| Header / §3 | P2 status changed to "complete"; P3 changed to "can start (specified contraction background)" | 1+1 slab D2 achieved + spherical coupling verification |
| §4.4 L2 | Closed (C̈/C output for homogeneous + 1+1 versions) | P2-C3 closed |
| §13 G4 | Upgraded to "passed"; wrote in 1+1 slab results and W3 control, residual handover items | D2 achieved in the fully coupled system; W3 no-flux control closes the causal chain |
| §15 | Added this entry | Documentation discipline |

**Key new technical facts this round (P3/P4 must comply)**:
1. Symbolic derivation fully machine-generated across the chain + automated assertion checks (homogeneous limit / flat slicing / Minkowski zero point); 10 symbolic / implementation errors fixed this round (`DCC_P2_Report_v2.md` §7.2 F-1…F-10); **E-1…E-8 of the v1.1 document are unaffected** (derivation path not passing through Christoffels).
2. 1+1 uses a periodic domain + Z2-symmetric double-wall slab configuration: zero-gradient boundaries and constraint projection are structurally incompatible (report §7.3).
3. The large-scale component of the Mom residual under synchronous gauge + frozen shift cannot be eliminated by (H_B,H_C) corrections — residual P2-C4 item; when citing the P2 background, P3 should use a fitted attractor instead of direct long-time citation.
4. D3 not achieved: C undergoes power-law contraction (homogeneous Kasner extrapolation C∝t^{-1/3}-like); P3's C→0 effective theory must be labeled "specified contraction background" (continuation of the key dependency statement in §9).

**Unchanged**: D1/D2/D3 criterion definitions; the 42.47 km/s "phenomenological assumption" identity; P0/P1 conclusions; covariant document v1.1; `DCC_P2_Report_v1.md` (first-round homogeneous report, retained in archive).

### v2.3 (2026-11-19) — Writing in P2 First-Round Homogeneous Results

Basis: `DCC_P2_Report_v1.md`, `DCC_P2_homogeneous_results.txt`, `DCC_P2_homogeneous_cases.png`.

| Location | Change | Reason |
|---|---|---|
| Header | Version v2.3; status changed to "P2 first round executed: homogeneous D2 conditionally achieved, strict D3 not achieved; 1+1/spherical not closed" | P2 first-round results |
| §13 G4 | Changed to "conditional pass (homogeneous sector only)", writing in $f_c^{\rm iso}=2.93$, $f_c^{\rm shear}=4.73$, $\mathcal C_H\sim5\times10^{-6}$ | Homogeneous scan + tolerance convergence |
| §15 | Added this entry | Documentation discipline |

**Unchanged**: D1/D2/D3 criteria (this version explicitly distinguishes D3-ratio from D3-strict), the 42.47 km/s "phenomenological assumption" identity, P0/P1 conclusions, covariant document v1.1.

**Unclosed items**: P2-C1…C6 (see `DCC_P2_Report_v1.md` §6.4); until complete, it is prohibited to state externally that "geometric dimensional collapse has been confirmed".

### v2.2 (2026-11-19) — Synchronizing Covariant Reconstruction v1.1 Errata

Basis: `DCC_Covariant_Reconstruction_v1.md` v1.1 (E-1…E-8); Maxwell divergence and `Tphi_*` outputs newly added to `DCC_sympy_derivation.py`.

| Location | Change | Reason |
|---|---|---|
| Header | Version v2.2; P2 status changed to "can start (use divergence form)" | E-1…E-8 corrected |
| §4.4 L1 | $\nu=y$ equation changed to divergence form, constant-metric limit noted | E-1: time term missing $1/B$ |
| §13 | Prerequisite action changed to "corrected, use divergence form in implementation" | Documentation correction complete |
| §14 | Cross-reference of $P$ changed from E-1 to E-2 | E-1 is the coefficient, E-2 is the sector attribution |
| Throughout | Withdrew the "dimensional inconsistency" statement | With $N,A,B,C$ dimensionless, both terms are $M^3$ |

**Unchanged**: physical goals of P2/P3/P4, D1/D2/D3 criteria, the 42.47 km/s "phenomenological assumption" identity, energy conditions and downgrade paths.

### v2.1 (2026-11-19) — Absorbing the G1 Acceptance Review v2.0 Patch

Basis: `DCC_G1_Acceptance_Review_Report_v2.md` §12 patch list; `DCC_G1_Closeout_Report_v1.md`; `DCC_P1_A4_results.txt`.

| Location | Change | Reason |
|---|---|---|
| Header / §3 | P1a, P1b statuses changed to complete; P2 changed to "can start" | G1/G2 passed, L1 closed |
| §4.4 L1 | $\nu=y$ equation temporarily changed to $\partial_t(ZE)=\frac{N^2}{A^2}\partial_x(Zf)$ (**corrected to divergence form in v2.2**), marked closed | L1 closed by A4; general-metric coefficients corrected in v2.2 |
| §4.4 L2 | Clarified "output from P2 first round, not a startup prerequisite" | Consistent with the original wording of the L2 closure standard |
| §5.2 | Wrote in $\eta_{\rm target}=74.9$, $\eta/(\lambda v^4)\approx75$, controllability FAIL permanently archived | A1/A2 measurements |
| §9 | Dependency graph updated; L1 closed, L2 postponed | Same as above |
| §13 | G1/G2/G3 verdicts updated; highest-priority action changed to "fix E-1 then start P2" (completed in v2.2) | L1 closed by A4 |
| §14 | $P$ marked as longitudinal-sector only | D5 |

**Unchanged**: physical goals of P2/P3/P4, D1/D2/D3 criteria, the 42.47 km/s "phenomenological assumption" identity, energy conditions and downgrade paths.

**Retained known issues**: None. `DCC_Covariant_Reconstruction_v1.md` has been upgraded to v1.1, E-1…E-8 in §3–§5 all corrected; this file's §4.4 L1 and `DCC_P2_Symbols_and_Observables_Checklist_v1.md` §3(a) have been synchronized to the divergence form.

---

Content generated by AI
