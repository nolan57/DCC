# DCC P1 Deliverables Metadata Table (A5)

**Project**: Dimensional Collapse Conjecture
**Corresponding Action**: G1-Review v2.0 §10 / Closure Checklist Item 7 (A5)
**Date**: 2026-11-19
**Code**: `DCC_P1_bubble_wall.py`, `DCC_P1_A4_maxwell_L1.py`
**Result Files**: `DCC_P1_results.txt`, `DCC_P1_A4_results.txt`

This table supplies the metadata required by Roadmap §0 discipline clauses and §11 (symbol reproducibility / dimensional checks).
P2 must use the wall profile and parameters in this table as initial data (Roadmap §6.2, step 2).

---

## 1. Parameters and Units

Natural units $c=\hbar=1$. $[\phi]=M^1$, $[V]=M^4$, $[x]=[t]=M^{-1}$, $[Z]=0$, $[A_y]=M^1$, $[F_{\mu\nu}]=M^2$.

| Parameter | Value | Description |
|---|---|---|
| $\lambda$ | 1.0 | Double-well potential strength |
| $v$ | 1.0 | Vacuum expectation value (baseline) |
| $\epsilon$ | 0.01 | Tilt parameter (used in P1b; taken as 0 for the P1a static wall) |
| Tilt-term implementation | $\epsilon\,\phi/(2v)$ | **Actual expression in the code** (`V_pot`). Not $\epsilon\phi/v$ |
| $\Delta V_{\rm vac}$ | $\epsilon=0.01$ | $V(+v)-V(-v)$ |
| $\epsilon_c$ (spinodal) | $4\lambda v^3/(3\sqrt3)=0.769800$ | $\phi_s=v/\sqrt3$ from $V'=V''=0$ |
| $\epsilon/\epsilon_c$ | **1.299%** | Far from reaching spinodal (Report v2.0 gives 1.38% due to rounding with $F=0.0106$) |
| $\alpha$ | 0.5 | $Z(\phi)=\exp(\alpha\phi/v)$ |
| $Z$ range | $[e^{-0.5},e^{0.5}]=[0.6065,\,1.6487]$ | Always $>0$, satisfying the healthy constraint |
| $f$ (background magnetic field) | 0.1 | $F_{xy}=f$, purely magnetic, $E=0$ (for the P1a extension) |
| $a$ (inverse wall width) | $v\sqrt{\lambda/2}=0.707107$ | kink $\phi=v\tanh(ax)$ |
| Wall tension (analytic) | $2\sqrt{2\lambda}\,v^3/3=0.942809$ | |
| Wall width $\delta_{0.9}$ (analytic) | $2\,\mathrm{artanh}(0.9)/a=4.164066$ | $-0.9v\to+0.9v$ |

> **Correction record**: Older `results` wrote the "analytic wall width" as $1/a=1.414214$, inconsistent with the definition of $\delta_{0.9}$, leading to the erroneous comparison "numerical 4.167 vs analytic 1.414". This version consistently uses $\delta_{0.9}$.

---

## 2. Grid, Time Step, and Boundaries

### 2.1 P1a Static-Wall Baseline

| Item | Value |
|---|---|
| Domain | $x\in[-30,30]$, $N_x=1201$ |
| $\Delta x$ / $\Delta t$ | 0.05 / 0.025 |
| CFL | 0.5 |
| Final time $T$ | 10 |
| Output interval | Every 20 steps |
| Boundaries | First-order outgoing at both ends (Sommerfeld / leapfrog form) |
| Initial conditions | $\phi(0,x)=v\tanh(ax)$, $\dot\phi(0,x)=0$, no perturbation |
| Evolution scheme | Second-order leapfrog |

### 2.2 A3 Convergence Test (Moving Wall)

| Scan | Domain | Values |
|---|---|---|
| Joint ($\Delta t\propto\Delta x$) | $[-60,60]$ | $\Delta x=0.2,0.1,0.05,0.025$; $\Delta t=0.5\Delta x$; $T=10$; $u=0.5$ |
| $\Delta x$ independent | $[-60,60]$ | $\Delta x=0.1,0.05,0.025,0.0125$; $\Delta t=0.0025$; $T=10$ |
| $\Delta t$ independent | $[-60,60]$ | $\Delta x=0.1$; $\Delta t=0.08,0.04,0.02,0.01$; $T=10$ |

The initial data are an **exact Lorentz-boosted kink**: $\phi(0,x)=v\tanh(a\gamma x)$, $\phi(-\Delta t,x)=v\tanh(a\gamma(x+u\Delta t))$, $\gamma=1/\sqrt{1-u^2}$.

### 2.3 P1a Magnetic-Source Extension (Diagnostic)

| Item | Value |
|---|---|
| Domain / grid | $[-30,30]$, $\Delta x=0.1$, $\Delta t=0.05$, CFL 0.5, $T=10$ |
| Boundaries | Fixed at a local minimum of $V_{\rm eff}=V+\tfrac12 f^2Z$ (Newton root finding) |
| Status | Wall motion itself is **DEFERRED to P2** (§8(a)); this item serves only as a boundary-attribution diagnostic |

### 2.4 A4 Maxwell (See A4 Report)

| Item | Value |
|---|---|
| Domain | $[-80,80]$ (wave packet) / $[-40,40]$ (static sector) |
| $\Delta x$ | 0.2 / 0.1 / 0.05 (wave-packet convergence); 0.2–0.025 (constraint scan) |
| CFL | 0.5 |
| Boundaries | First-order Mur absorbing (wave packet) / Dirichlet (static sector) |

---

## 3. Observable Definitions

| Observable | Definition | Implementation |
|---|---|---|
| Wall position $x_w$ | $\phi(t,x_w)=0$ | Linear interpolation between neighboring grid points (first zero crossing) |
| Wall width $\delta$ | Width of $\phi$ from $-0.9v$ to $+0.9v$ | Linear interpolation at each of the two thresholds |
| Wall velocity $v_w$ | $\mathrm{d}x_w/\mathrm{d}t$ | Central difference over recorded points |
| Wall tension $\sigma_w$ | $\int[\tfrac12\dot\phi^2+\tfrac12\phi'^2+V(\phi)-V_{\min}]\,\mathrm{d}x$ | Trapezoidal integration (including kinetic energy; $\gamma\sigma$ for a moving wall) |
| Total energy $E$ | $\int[\tfrac12\dot\phi^2+\tfrac12\phi'^2+V(\phi)]\,\mathrm{d}x$ | Trapezoidal integration, with $\phi'$ via `np.gradient(edge_order=2)` |
| Energy residual $E_{\rm res}$ | $\max_t |E(t)-E(0)|/|E(0)|$ | **Maximum over the whole run** (required by A3; older versions reported only the final value) |
| $R_{\rm BPS}$ | $\max_x\left|\tfrac12(\phi')^2-(V-V_{\min})\right|/(V-V_{\min})$ | Inside the wall $|\phi|<0.9v$; three levels: 2nd order / 6th order / analytic |
| $\beta_w$ | Wall velocity in the plasma rest frame / $c$ | Collective-coordinate terminal velocity |

**Boundary note on the energy residual**: The $E_{\rm res}$ of the static-wall baseline reaches a plateau already at $t\approx0$ ($1.17\times10^{-7}$), rather than accumulating over time; the main source is that the discretized kink is not an exact equilibrium state of the discrete equations (an $O(\Delta x^2)$ initial residual). No boundary-reflection contamination is seen within $T=10$.

---

## 4. Raw Convergence Data (A3)

### 4.1 Joint Scan ($\Delta t=0.5\Delta x$)

| $\Delta x$ | $\Delta t$ | L2 error | $x_w$ error | $\delta$ error | $\sigma_w$ error | $E_{\rm res}$ |
|---|---|---|---|---|---|---|
| 0.2 | 0.1 | 1.373e-03 | −1.347e-02 | 7.270e-04 | −3.903e-03 | 5.72e-05 |
| 0.1 | 0.05 | 3.395e-04 | −3.318e-03 | −4.463e-04 | −9.733e-04 | 3.91e-06 |
| 0.05 | 0.025 | 8.461e-05 | −8.257e-04 | −7.331e-05 | −2.431e-04 | 3.28e-07 |
| 0.025 | 0.0125 | 2.113e-05 | −2.061e-04 | 2.906e-05 | −6.074e-05 | 3.10e-08 |

Fitted orders: L2 **2.01**, $x_w$ **2.01**, $\delta$ 1.65, $\sigma_w$ **2.00**.
Richardson apparent orders (L2): 2.02, 2.01.

### 4.2 $\Delta x$-Independent Scan ($\Delta t=0.0025$ fixed)

| $\Delta x$ | L2 error | $x_w$ error | $\sigma_w$ error |
|---|---|---|---|
| 0.1 | 3.440e-04 | −3.362e-03 | −9.682e-04 |
| 0.05 | 8.584e-05 | −8.376e-04 | −2.420e-04 |
| 0.025 | 2.144e-05 | −2.091e-04 | −6.050e-05 |
| 0.0125 | 5.349e-06 | −5.217e-05 | −1.513e-05 |

Fitted orders: L2 **2.00**, $x_w$ **2.00**, $\sigma_w$ **2.00**.

### 4.3 $\Delta t$-Independent Scan ($\Delta x=0.1$ fixed, self-convergence difference)

| $\Delta t$ | CFL | $\|L2\|_{\rm self}$ |
|---|---|---|
| 0.08 | 0.8 | 9.835e-06 |
| 0.04 | 0.4 | 2.341e-06 |
| 0.02 | 0.2 | 5.639e-07 |
| 0.01 | 0.1 | — (reference solution) |

Self-convergence order **2.06**. In this scan, $x_w/\delta/\sigma_w$ are already at the spatial error floor for $\Delta x=0.1$, so their orders cannot be discerned.

> **Note on the order of $\delta$**: The error in $\delta$ crosses zero between $\Delta x=0.1\to0.025$ (−4.9e-4 → +2.9e-5),
> so the value 1.45 given by the loglog fit is meaningless; it should be reported separately on each side of the zero crossing, or a $\delta/\Delta x$ scan should be used instead.
> $x_w$, $\sigma_w$, and L2 all cleanly give second order.

---

## 5. Friction-Law Reference Frame and Calibration Conventions (A1/A2/A5)

- **Reference frame**: $v$ is the wall velocity **in the plasma rest frame**. If P4 rendering needs the Earth-observer-frame velocity, it must additionally be multiplied by the Doppler/Lorentz factor; this $v$ must not be used directly as an observer-frame velocity.
- Collective-coordinate equation: $\sigma_w\,\mathrm{d}(\gamma v)/\mathrm{d}t=\Delta V_{\rm vac}-\eta_{\rm eff}v$.
- Terminal velocity: $v_{\rm term}=(F/\eta)/\sqrt{1+(F/\eta)^2}$; as $\eta\to0$, $v\to1$ (analytic limit, **not** a numerical output).
- **Scan-variable convention**: In this report and in `results`, $\eta\equiv\eta_{\rm eff}/\sigma_w$, and the equivalent driving force is $F_{\rm eff}=\Delta V_{\rm vac}/\sigma_w=\epsilon/\sigma_w=0.010607$.
  - Using $\eta$ as the variable: $\eta_{\rm target}=F_{\rm eff}/\beta_f=\mathbf{74.87}$.
  - Using the absolute friction coefficient $\eta_{\rm eff}$ as the variable: $\eta_{\rm eff,target}=74.87\times\sigma_w=\mathbf{70.59}$.
  - The two differ only by the constant factor $\sigma_w=0.942809$; the physical conclusion is unchanged.
- Target velocity: $\beta_f=42.47/299792.458=1.416647\times10^{-4}$.
- Controllability: $\eta/(\lambda v^4)=74.9\approx75$ lies outside the original scan interval $[0,1]$ and $\gg1$, beyond the domain of validity of weak dissipation → **FAIL**.

---

## 6. Initial Conditions and Randomness

- P1a static: $\phi(0,x)=v\tanh(ax)$ (analytic kink), $\dot\phi=0$, no random perturbation.
- P1a moving: exact boosted kink (see §2.2), no random perturbation.
- P1b: no PDE evolution; direct use of the collective-coordinate terminal-velocity formula.
- A4: Gaussian wave packet $A_y=A_0e^{-(x-x_0)^2/(2w^2)}$, $w=3$, $x_0=-25$, $A_0=1$,
  $E(0)=-\partial_xA_y$ (right-moving wave); static sector $f=Q/Z$, $Q=0.1$, $E=0$.

---

## 7. Deliverables Checklist

| File | Content |
|---|---|
| `DCC_P1_bubble_wall.py` | P1a/P1b solvers, convergence/BPS/phase diagram |
| `DCC_P1_results.txt` | All P1 numerical results and acceptance self-check |
| `DCC_P1_p1a_wall_evolution.png` | Static-wall evolution (6 panels) |
| `DCC_P1_p1a_convergence.png` | A3 convergence (joint / Δt independent) |
| `DCC_P1_p1a_bps.png` | BPS residual vs Δx (2nd order / 6th order / analytic) |
| `DCC_P1_p1b_terminal_velocity.png` | β_w(η) phase diagram (SR/NR + measured/extrapolated partitions) |
| `DCC_P1_p1a_magnetic_source.png` | Magnetic-source extension (fixed boundaries, stable demonstration) |
| `DCC_P1_A4_maxwell_L1.py` | A4 Maxwell solver |
| `DCC_P1_A4_results.txt` | All A4 results and closure criteria |
| `DCC_P1_A4_wave_scattering.png` | Wave-packet scattering snapshots |
| `DCC_P1_A4_constraints.png` | Energy conservation / scattering convergence / static sector |

---

## 8. Known Code Corrections (Relative to the Older `DCC_P1_bubble_wall.py`)

| # | Issue in Older Version | Impact | Correction |
|---|---|---|---|
| C1 | Time labels used `t[:rec_idx]`, inconsistent with "record every N steps" | Horizontal axes of all time-series plots compressed; wall velocities entirely wrong | Record the time corresponding to the actual step number |
| C2 | Main loop `range(1, nt-1)`, so the final state stopped at $T-\Delta t$ | Final values systematically lag by one time step; convergence orders lowered | Loop to `nt` |
| C3 | Moving-wall initial data `kink(x-u·dt)` with $\gamma$ omitted | Initial profile not a boosted kink; ~10% energy error | Use the exact solution including $\gamma$ |
| C4 | Energy velocity used `(φ^{n+1}-φ^n)/(2dt)` | Kinetic energy underestimated by a factor of 4 | Changed to `/dt` (consistent with half time steps) |
| C5 | Analytic wall width used $1/a$ | Incorrect comparison with $\delta_{0.9}$ | Use $2\,\mathrm{artanh}(0.9)/a$ |
| C6 | P1b used $\eta_{\rm eff}=\eta\sigma_w$ without declaring it | Calibration value off by 6% | Explicitly state the scan-variable convention (§5) |
| C7 | Magnetic-source instability attributed to "the wall hitting the boundary" | Incomplete attribution | Controlled experiments identify "boundary conditions lacking the source term" (see results §4) |

> **Concluding reminder**: The "apparent convergence order 4.03" reported in the old version is an artifact caused by C1/C2.
> After correction, the intrinsic order is **2.00–2.01**, consistent with the second-order leapfrog scheme.

---

## 9. Uncovered Items (Handed Over to P2)

1. Two-way reconciliation of the electromagnetic energy injection rate when $Z(\phi)$ evolves in time ($\dot Z\neq0$);
2. Maxwell coefficients in a general metric (E-1...E-8 already corrected in the covariant reconstruction v1.1; P2 implements the divergence form directly);
3. Wall motion driven by the magnetic source (three-system coupling $\phi\leftrightarrow F\leftrightarrow g$);
4. Comparison of the spherically symmetric and local-planar geometries (Roadmap §6.5-6).

---

Content generated by AI
