# DCC P2 Symbols and Observables Checklist v1.0

**Project**: Dimensional Collapse Conjecture
**Purpose**: Symbol-review baseline for the P2 project-initiation document (review report v2.0 §9 / item 8 of the closeout checklist)
**Frozen basis**: `DCC_Covariant_Reconstruction_v1.md` §6–§7; `DCC_P0-P4_Roadmap_Plan.md` §6, §14
**Date**: 2026-11-19

---

## 0. Mandatory conventions (must not be rewritten)

Metric:
$$ds^2=-N^2dt^2+A^2dx^2+B^2dy^2+C^2dz^2 .$$

**The contraction direction is controlled by $C$**, and the criterion is $C\to0$.

> ⚠️ **Do not carry over the old P0-era notation**. In the old notation, "$B$ is the contraction direction, with target $B\to0$" has been deprecated.
> If the old notation is copied verbatim, the contraction axis will fall on $\hat y$, cascading contamination into
> $\mathcal R_L=C/A$, the orthonormal-frame pressure $p_{\hat z}=-\rho$,
> and the correspondence between $F_{xy}=f$ (magnetic field along $\hat z$) and the contraction direction.

| Symbol | Meaning | Notes |
|---|---|---|
| $N$ | lapse | |
| $A$ | $x$-direction scale factor | |
| $B$ | $y$-direction scale factor | **not** the contraction direction |
| $C$ | $z$-direction scale factor | **contraction direction; target $C\to0$** |
| $\phi$ | phase-transition order parameter | |
| $Z(\phi)$ | gauge coupling, $Z>0$ | |
| $F_{xy}=f$ | magnetic component (magnetic field along $\hat z$) | source of directional stress |
| $F_{ty}=E$ | electric component | lifts the time-independence constraint of the purely magnetic configuration |
| $A_y$ | vector potential ($E=\partial_tA_y$, $f=\partial_xA_y$) | Bianchi automatically satisfied |
| $P$ | electric flux charge $P=ZBCE/(AN)$ | **longitudinal sector only**, see §3(c) |
| $H_i$ | $\dot a_i/a_i$ | expansion rate in each direction |
| $\kappa$ | $8\pi G$ | |

---

## 1. Seven required observables (roadmap §6.3)

Output at every step or every N steps; none may be omitted.

| # | Symbol | Definition | Interpretation | Threshold/action |
|---|---|---|---|---|
| 1 | $\mathcal R_H$ | $H_z/H_x$ | anisotropic expansion rate (**D1 criterion**) | record time series; $<1$ only indicates D1 |
| 2 | $\mathcal R_L$ | $C/A$, $C/B$ | relative scale evolution | **must convert to physical geodesic lengths** $C\Delta z$ etc.; coordinate values alone are insufficient |
| 3 | $\mathcal K$ | $R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}$ | distinguish physical singularities from coordinate degeneration | interpret together with $\mathcal R_L$ |
| 4 | $\mathcal E$ | $T_{\mu\nu}n^\mu n^\nu$ | local energy density | monitor whether $\rho_B\propto1/Z$ or $1/C^n$ diverges |
| 5 | $\mathcal C_H$ | $\max_x(|\mathcal H|,|\mathcal M|)$ | constraint residual | above threshold means invalid; must converge with resolution |
| 6 | $\mathcal B$ | $\max_x|\partial_tf-\partial_xE|$ | Bianchi residual | $<10^{-8}$ (machine precision expected when using $A_y$) |
| 7 | NEC/WEC | $T_{\mu\nu}k^\mu k^\nu\ge0$, $T_{\mu\nu}n^\mu n^\nu\ge0$ | whether energy conditions must be violated to reach D3 | record violating regions point by point |

Supplement: in $\mathcal C_H$, $\mathcal H$ is the Hamiltonian constraint and $\mathcal M$ the momentum constraint;
P2 must output them at every step, not only check the final state (constraint drift is the primary invalidation signal).

---

## 2. D1/D2/D3 hierarchy (must not be mixed)

| Level | Mathematical condition | Physical meaning | Proven by |
|---|---|---|---|
| **D1** | $H_z<H_x$ | Z-direction expansion weaker than transverse | analytically obtainable in the homogeneous + initially static case |
| **D2** | $H_z<0$ | actual contraction in Z | **must** come from fully coupled numerical evolution |
| **D3 (strict)** | $C<10^{-3}$ and $A,B>10^{-2}$, $H_A,H_B>0$, $C/A,C/B<10^{-2}$ | genuine directional geometric degeneration (absolute contraction of $C$) | supported jointly by D2 + $\mathcal K$ behavior + geodesic length |
| **D3-ratio** (auxiliary) | $C/A<10^{-2}$, $C/B<10^{-2}$, $H_A,H_B>0$, $A,B>10^{-2}$ | relative degeneration; $C$ itself need not $\to0$ | homogeneous first round: reachable in the magnetic sector (27/35) |

**Preserve verbatim**: an acceleration difference gives only D1; if both directions expand but $a_z$ accelerates less, D1 is still satisfied.
Any "Z contraction" claim must reach at least D2 ($H_z<0$).
**Do not pass off D3-ratio as D3**: while $A,B$ grow, $C/A\ll1$ does not mean $C\to0$; the two must be reported separately.

---

## 3. Maxwell equations: three items to confirm before the P2 implementation

### (a) General-metric ν=y component (E-1, **corrected in covariant reconstruction v1.1**)

Recomputed directly from the action (sympy, see `DCC_G1_Closeout_Report_v1.md` §5.3 and `DCC_sympy_derivation.py`):
$$\boxed{\ \partial_t\!\left(\frac{ZAC}{NB}E\right)-\partial_x\!\left(\frac{ZNC}{AB}f\right)=0\ }$$
where $E=F_{ty}$ and $f=F_{xy}$.

The v1.0 reconstruction document wrote
$\partial_t(ZACE/N)-\partial_x(ZNCf/(AB))=0$: the flux term is the same, but the **time term is missing $B$ in the denominator**.
Only when $N,A,B,C$ are constants can this reduce to
$\partial_t(ZE)=(N^2/A^2)\partial_x(Zf)$; in a general metric the divergence form above must be used.

- Minkowski limit ($N=A=B=C=1$): all three agree, so the A4 conclusions are unaffected;
- **The P2 ADM implementation must use the divergence form**, otherwise the flux charge and constraints will be wrong;
- The v1.0 checklist once claimed "an extra $1/B$ in the flux and inconsistent dimensions between the two terms"; both were misjudgments and are corrected in this version.

### (b) Using $A_y$ as the fundamental variable

$E=\partial_tA_y$, $f=\partial_xA_y$ → Bianchi identity automatically satisfied.
A4 has shown that this implementation can drive $\mathcal B$ down to $10^{-15}$.
Evolution equation (general metric): $\partial_t\!\left(\frac{ZAC}{NB}\partial_tA_y\right)=\partial_x\!\left(\frac{ZNC}{AB}\partial_xA_y\right)$;
Minkowski limit ($N=A=B=C=1$) reduces to $\partial_t(Z\partial_tA_y)=\partial_x(Z\partial_xA_y)$.

### (c) Scope of applicability of $ZE=P$

$ZBCE/(AN)=P$ is the Gauss constraint of the **longitudinal ($A_x$) sector**;
the Gauss law for the transverse $A_y$ polarization is an identity ($E_x=0$), and $ZE$ is **not** a conserved quantity.
Treating $ZE=P$ as a transverse constraint would incorrectly forbid propagating modes (A4's wave-packet solution would be misjudged as invalid).

---

## 4. Initial data (from P1a, frozen)

| Quantity | Value |
|---|---|
| $\phi(x)$ | $v\tanh(ax)$, $a=v\sqrt{\lambda/2}=0.707107$ |
| $\sigma_w$ | $0.942809$ (analytic) / $0.942652$ (numerical) |
| $\delta_{0.9}$ | $4.164066$ (analytic) / $4.165033$ (numerical) |
| $\dot\phi(0,x)$ | 0 (static wall) or exact boost solution |
| $\epsilon$ | 0.01 (tilt term $\epsilon\phi/(2v)$, $\Delta V_{\rm vac}=\epsilon$) |
| $\epsilon/\epsilon_c$ | 1.30% ($\epsilon_c=0.7698$), far from reaching spinodal |
| $Z(\phi)$ | $e^{\alpha\phi/v}$, $\alpha=0.5$, $Z\in[0.6065,1.6487]>0$ |

The initial $A,B,C$ and their extrinsic curvatures **may not be freely specified**: they are solved from the Hamiltonian/Momentum constraints (roadmap §6.2-3).

---

## 5. P2 output and acceptance

### 5.1 Output cadence

- Every time step: $\mathcal C_H$, $\mathcal B$;
- Every N steps: full set of seven observables + field profiles;
- Each run: resolution-doubling comparison (at least 2 points), $\delta/\Delta x$ scan, CFL number, termination time.

### 5.2 Closure criteria (roadmap §6.5)

1. $\mathcal C_H$ and $\mathcal B$ bounded throughout and converging with resolution;
2. Total energy-momentum conservation (including $\phi$–Maxwell exchange terms) meets the target;
3. Explicitly answer whether there exists a solution satisfying all constraints with $C$ contracting and $B$ finite (D2);
4. If D2 is achieved: report $Q/P$, $Z(\phi)$ parameter ranges and energy-condition status;
5. If D2 is not achieved: give falsification parameter ranges and trigger the downgrade path;
6. Provide both local-planar and spherically symmetric results together; the local planar solution must not be treated as a global solution.

### 5.3 First-round results (2026-11-19)

| Criterion | Result | Basis |
|---|---|---|
| D2 | **Conditionally achieved** | magnetically driven crossing: iso 6/6, shear 23/35; barrier-top $f_c^{\rm iso}=2.93$, $f_c^{\rm shear}=4.73$; true-vacuum iso has no energy threshold but $t_{D2}\approx1.41/f$; small-$f$ shear is initial Kasner |
| D3-strict | **Not achieved** | homogeneous $C$ freezes/rebounds after contraction; $C/A$ can reach $3\times10^{-3}$ but $C$ does not $\to0$ |
| D3-ratio | **Achieved in magnetic sector (non-monotonic)** | magnetic-iso 6/6 ($f>0$); magnetic-shear 27/35 ($f>0$: 22/30); $f\approx0.5$–$1.0$ window optimal |
| $\mathcal C_H$ | $5\times10^{-6}$ (rtol $10^{-11}$), decreasing to $5\times10^{-10}$ with tolerance | `DCC_P2_homogeneous_results.txt` |
| Conservation | continuity residual $2.8\times10^{-17}$–$5.3\times10^{-15}$ | same as above |
| NEC/WEC | NEC saturated at 0 (magnetic field along Z); WEC $\ge0$ | same as above |
| 1+1 / spherical symmetry | **Not closed** | `DCC_P2_Report_v1.md` §6 |

**First-round deviation (must be recorded)**: the main result is the **homogeneous Bianchi I zero-mode truncation**, taking the two asymptotic values of the P1 profile, $\phi_0=0$ (barrier top) and $\phi_0=-v$ (true vacuum), and **not using** the $x$-dependent profile. The full 1+1 and axisymmetric spherical cases remain incomplete; see `DCC_P2_Report_v1.md` §1.1, §6.

### 5.4 Symbol-review checklist for the project-initiation document

- [ ] No "$B\to0$" statement anywhere in the text; the contraction target is consistently written as $C\to0$;
- [ ] $\mathcal R_L$ uses $C/A$, $C/B$, with geodesic-length conversion noted;
- [ ] All seven observables listed (especially $\mathcal K$, $\mathcal B$, NEC/WEC);
- [ ] Maxwell uses the E-1 corrected form;
- [ ] $A_y$ as fundamental variable, Bianchi guaranteed by construction;
- [ ] $ZE=P$ used only for the longitudinal sector;
- [ ] Initial data cited from `DCC_P1_metadata.md`, not copied by hand;
- [ ] If 42.47 km/s appears, it must carry the annotation "phenomenological assumption group, not a theoretical prediction".

---

## 6. Difference log relative to older documents

| # | Old wording | New wording | Reason |
|---|---|---|---|
| S1 | "monitor $B(t,x)$, target $B\to0$" | $C(t,x)$, target $C\to0$ | old P0 convention, would misalign the contraction axis |
| S2 | $\mathcal R_L=B/A$ | $C/A$, $C/B$ | same as above |
| S3 | $\partial_t(ZACE/N)-\partial_x(ZNCf/(AB))=0$ | $\partial_t(ZACE/(NB))-\partial_x(ZNCf/(AB))=0$ | direct recomputation: time term missing $1/B$; the earlier "inconsistent dimensions" judgment has been withdrawn |
| S4 | $ZBCE/(AN)=P$ as a transverse constraint | longitudinal sector only | transverse Gauss law is an identity |
| S5 | missing direction annotation for $p_{\hat z}=-\rho$ | make explicit that $\hat z$ corresponds to $C$ | prevent directional misalignment |

---

Content generated by AI