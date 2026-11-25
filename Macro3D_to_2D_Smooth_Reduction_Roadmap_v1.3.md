# Roadmap for Smooth Two-Dimensional Reduction of Three-Dimensional Macroscopic Objects v1.3
## Order-of-Magnitude-Gate-First Edition: Conclusion Downgrades, Error Corrections, and an Executable Research Specification

**Version:** v1.3 (supersedes v1.2, *DCC_Macro_2D_Execution_Spec*, as the execution baseline; it is also the formal revision of v1.1, *Macro3D_to_2D_Smooth_Reduction_Roadmap* (integrated edition))
**Version date:** 2026-11-20
**Scope:** DCC main chain P0–P4 and the special project "smooth two-dimensional reduction of macroscopic objects"
**Document nature:** Research Execution Specification. This file is not a physical conclusion that "two-dimensional reduction has been achieved"; it specifies under what conditions, with which equations, and through which acceptance gates statements of a given strength are permitted.
**Baseline inputs:**
1. *Macro3D_to_2D_Smooth_Reduction_Roadmap* v1.1 (document under review);
2. *DCC_Macro_2D_Execution_Spec_v1.2* (third-party review deliverable; all six of its substantive corrections are adopted here);
3. *DCC Smooth Two-Dimensional Reduction: Technical Assessment of the v1.2 Third-Party Review Comments and v1.3 Revision Directives* (this document was written following its sentence-by-sentence S1–S15 revision list and its five new issues N1–N5);
4. DCC P0 directional-stress review results, P1a static bubble-wall numerical solution, and P1b collective-coordinate friction scan.

**Guiding principle:** Do not miswrite prescribed backgrounds, inverse problems, low-energy effective theories, or visual rendering results as a forward proof of a complete physical mechanism. The actual physical scene and visualization effect after two-dimensional reduction are jointly determined by the solutions of the mapping relations, matter response, geometric dynamics, and the optical and radiative-transfer equations; this specification delivers only the equations, criteria, and numerical thresholds that determine them, and makes no presupposition about their final presented form.

**Evidence-level tags (mandatory throughout):** Every conclusion must be tagged as one of the following; upgrading beyond its level is prohibited:

| Tag | Meaning |
|---|---|
| ESTABLISHED | Established by derivation or verification within explicitly stated assumptions |
| MODEL RESULT | Analytic/numerical result under a specified model and parameters, with an assumption list attached |
| CONDITIONAL | Depends on assumptions that have not yet been verified |
| OPEN | Not yet resolved |
| FALSIFIED | Falsified by a counterexample, order-of-magnitude accounting, or test |

---

# 0. Executive Summary and v1.3 Change Notes

## 0.1 Three Categories of Changes in v1.3 Relative to v1.2

**Category 1: Accept the six substantive corrections from v1.2 and downgrade conclusions in v1.1.** All six corrections were independently verified as valid, and an additional numerical correction ($\eta_{\rm eff}\approx 75$) passed review. Statements in v1.1 such as "the conditions for smooth two-dimensional reduction have been determined," "the fiber-bundle mapping is uniquely self-consistent," "macroscopic objects become a nearly invisible phantom membrane," and "$\beta_C>1$ guarantees adiabaticity" are all void and are rewritten sentence by sentence according to the S1–S15 list in Appendix A.

**Category 2: Add stage gate G0 (analytic order-of-magnitude gate), placed before all numerical investment.** This is the most important structural change in v1.3. v1.2 completed only corrections at the "presentation level" (downgrading overstrong conclusions to assumptions) but performed no accounting at the "magnitude level"; order-of-magnitude accounting is extremely cheap (pure analysis, 1–2 days) yet decisive: under the default premises of v1.1 Model C (unchanged projected area + conserved particle number), atoms and chemical bonds are necessarily destroyed, and the assumption "noncovalent interactions are maintained" is **mutually exclusive** with that premise. This document therefore codifies that accounting as G0 and requires that it be completed before resources are committed to R1.

**Category 3: Incorporate the five new issues N1–N5 from the assessment document.** Of these, N1 (column-density conservation ⇒ invariant optical depth) and N4 (momentum redshift in the contraction direction ⇒ anisotropic heating) overturn, respectively, v1.1's "transparent phantom membrane" conclusion and the completeness of the D3 stress budget; N3 (the $z$-projection of a bounded body is not a fiber bundle) invalidates v1.1's entire argument chain "fiber-bundle projection ⇒ no tearing."

## 0.2 Core Conclusion of v1.3: a Hard Dilemma

v1.3 states up front a conclusion that must be explicitly acknowledged at the document level (MODEL RESULT; derivation in Chapter 3):

> Take a 70 kg human body, mean atomic mass 10 amu, projected area $A=1\ {\rm m}^2$, and conserved particle number; the areal atomic density after two-dimensional reduction is
> $$N_s=\frac{M}{\bar m A}=4.2\times 10^{27}\ {\rm m^{-2}}$$
> The corresponding mean in-plane spacing is $N_s^{-1/2}=15.4\ {\rm fm}=2.9\times10^{-4}\,a_0$, about 3400 times smaller than the Bohr radius and about 1/40 of the areal density of nuclear matter. At this point the electron Fermi wave vector is $k_F=1.18\times10^{14}\ {\rm m^{-1}}$, the Fermi energy is $E_F\simeq \hbar k_F c\approx 23\ {\rm MeV}$ (relativistic dispersion must be used; the nonrelativistic formula gives 535 MeV and fails), the total degenerate-electron energy is $\approx 6.3\times10^{15}\ {\rm J}\approx1.5\ {\rm Mt}$ of TNT (about $8\times10^{5}$ times the chemical binding energy of a human body), and the 2D degeneracy pressure is $P_{2D}\approx3\times10^{15}\ {\rm J/m^2}$.
>
> **Therefore: "unchanged projected area" and "survival of atoms, chemical bonds, and noncovalent networks" are mutually exclusive.** To preserve an atomic spacing of about 3 Å, the required area is
> $$A_{\min}=N_s(3\,\text{Å})^2\approx3.8\times10^{8}\ {\rm m^2}\approx380\ {\rm km^2}\quad(\text{per person})$$
> That is, the area must expand by a factor of $3.8\times10^{8}$ — **and this is precisely Model B, which v1.1 rejected on the grounds of an "energy contradiction."** v1.1's rejection of Model B and its acceptance of Model C cannot both hold: preserving atoms requires accepting area expansion (Model B type), while preserving area requires accepting atomic destruction (Model A type). The only other way out is to abandon particle-number conservation, which is a **new physics assumption** that must be explicitly declared and for which all downstream quantities must be recomputed.

This dilemma was not written out in either v1.1 or v1.2. v1.3 makes it the opening conclusion of Chapter 0 and requires all subsequent chapters, when mentioning "structure preservation," to first declare which branch they stand on.

## 0.3 Current Stage Assessment (v1.3 Revision)

| Module | v1.1 status | v1.3 status | Maximum conclusion permitted |
|---|---|---|---|
| P0 directional-stress candidates | Sign corrections already made | $F_{xy}$ candidate retained; full inhomogeneous solution not established | Maxwell $F_{xy}$ has the required directionality (ESTABLISHED, local orthonormal frame); whether it can drive the target bubble-wall geometry is OPEN |
| P1a static bubble wall | Baseline met | Preliminary pass; convergence order unproven | Static kink solver preliminarily credible (MODEL RESULT) |
| P1b collective-coordinate friction | $\eta\approx1.0$ corresponds to 42.47 km/s | **Corrected to $\eta_{\rm eff}\approx75$** | Low-speed phenomenological velocity model (reviewed ESTABLISHED result + parameter revision) |
| D1 matter adiabatic response | complete (criterion) | **downgraded to a screening quantity** | $\eta_{\rm rough}$ can only screen, not decide GO; the true criterion is $\epsilon_{mn}$ (ESTABLISHED) |
| D2 prescribed contraction background | complete | maintained: externally prescribed | The power-law background is phenomenological input, not an endogenous solution (ESTABLISHED) |
| D3 endogenous dynamics | incomplete | incomplete, with two new prerequisites added | The stress-budget inverse problem is only a necessary condition (CONDITIONAL) |
| Physical boundaries ($L_z,\beta_C$) | legal/illegal regions determined | **removed** | $\beta_C$ has no universal threshold; $L_z$ values are model-dependent and discrete (FALSIFIED: original dichotomy) |
| Mapping relationship | complete (fiber bundle uniquely self-consistent) | **OPEN** | Bounded-body projection is not a fiber bundle; $S^3\not\cong S^2\times S^1$ (ESTABLISHED counterexample) |
| Areal density / column density | $\sigma\approx\rho L_z$ | rewritten with the correct measure; column-density conservation invariant given | $\Sigma=\int\rho\sqrt{g_{zz}}\,dz$; under fixed-area compression $N_s$ and $\tau$ are invariant (MODEL RESULT) |
| Matter 2D-reduction transport | not done | not done, and constrained by the G0 prerequisite | No claim that atoms, chemical bonds, or macroscopic objects adapt automatically |
| Optics and vision | formulas existed but were overgeneralized | split into four layers L1–L4; premature conclusions prohibited | only "prescribed-background test optics" (MODEL RESULT) |
| Macroscopic geometric wrapping | not done | not done | Local planar wall solutions must not be extrapolated into spherical fronts |

**Overall verdict:** The research program may continue, but **"smooth two-dimensional reduction has been achieved" must not be declared**. There is currently no evidence supporting the claim that "a macroscopic three-dimensional object can be smoothly converted into two-dimensional matter"; on the contrary, G0's analytic accounting gives a strong indication in the opposite direction: at fixed projected area, atomic-scale structure is necessarily destroyed. v1.3 handles this by upgrading the indication into a stage gate that must be closed first, rather than writing it into the conclusions.

## 0.4 Highest Verdict Principle

The goal of DCC is not to make some prescribed $B(t,x)$ look like two-dimensional reduction in images, but to prove that geometry, matter, interactions, energy–momentum, and observer measurements can coexist within one self-consistent set of equations. **If the proof fails, the failure itself is a valid research result.**

This yields three execution decisions:

1. **Do not assume in advance that matter can smoothly reduce to two dimensions.** R1 must first answer whether free fields, bound states, and lattices can remain stable; even if geometric contraction holds mathematically, that does not mean matter can follow.
2. **D3 must be proven by forward equations.** The stress-budget inverse problem can only tell us "what stress is needed"; it cannot prove that any physical field can supply it, still less that a forward solution exists and is stable.
3. **Visual models cannot replace physical verification.** Ray tracing and rendering under a prescribed background may be done first, but "test optics results" must be distinguished from "DCC physical predictions"; until a self-consistent $\sigma_s(\omega)$ is available, conclusions in either direction — "transparent" or "opaque" — are prohibited.

---

# 1. Global Assumptions, Terminology, and Model Boundaries

## 1.1 Assumptions That Must Be Explicitly Stated at the Start of the Document

Before any subsequent derivation is invoked, one must first confirm which of the following sets of assumptions applies. **"Unchanged projected area" and "particle number conservation" were implicit in v1.1; from v1.3 onward they must be written explicitly** (revision item S15):

| Assumption ID | Content | Status | Consequence of violation |
|---|---|---|---|
| H1 | There exists a geometric background in which the $z$-direction scale factor $B(t,x)$ can decrease substantially | Phenomenological setting (D2) | The entire study fails |
| H2 | The projected area $A_\perp$ remains unchanged during contraction | **Pending G0 verdict** | Mutually exclusive with "atom survival" (Chapter 3) |
| H3 | The total particle number $N$ is conserved | Assumed by default | If abandoned, $N_s,\sigma_s,\tau$, the gravitational field, and radiation must be recomputed |
| H4 | The noncovalent (soft) interaction network is preserved during evolution | **Falsified under the combination H2 + H3** | See N2 and N5 |
| H5 | A low-energy effective description is applicable ($E_{\rm probe}\ll\Delta E_{\rm KK,1}$ or the bound-state gap) | Verified model by model (R3-1) | It must not be called "effectively two-dimensional" |

## 1.2 Four Physical Situations That Must Be Distinguished

| Name | Definition | Equivalent to macroscopic 2D reduction? | Momentum spectrum |
|---|---|---|---|
| Anisotropic geometric contraction | A metric direction's scale factor $B(t,x)$ decreases | No | $z\in\mathbb R$: continuous spectrum, **no $p_z^{\min}$** |
| Finite-thickness thin layer | Matter confined to a very thin but nonzero $z$-direction region (potential well) | No; generally still in 3D space | Discrete bound spectrum determined by the well |
| Compactification / dimensional reduction | One direction has compact topology; low-energy observers cannot excite nonzero KK modes | Can yield an effective $2+1$ dimensional theory, **does not automatically mean a macroscopic object is flattened** | $p_n=n\hbar/R_z$ |
| Genuine change of dimensionality | The dimensionality or topology of spacetime/matter degrees of freedom changes | Requires additional theory; cannot be inferred from $B\to0$ alone | Depends on the specific theory |

Every subsequent chapter and every result must specify which of these is being studied. **These concepts must not be interchanged without explanation within the same derivation, and spectral conclusions must not be borrowed across models in particular** (v1.1's $p_z^{\min}=2\pi/L_z$ argument failed precisely because of such mixing; see §2.4).

## 1.3 Basic Geometric Notation

Use geometric units with $c=1$, with the line element

$$ds^2=g_{ab}(t,x)\,dx^a dx^b+A^2(t,x)\,dy^2+B^2(t,x)\,dz^2,\qquad a,b\in\{t,x\}.$$

If $g_{ab}dx^a dx^b=-dt^2+dx^2$, then

$$ds^2=-dt^2+dx^2+A^2(t,x)\,dy^2+B^2(t,x)\,dz^2.$$

- $A(t,x)$: transverse $y$ scale factor;
- $B(t,x)$: scale factor of the candidate contraction direction $z$;
- $H_A=\partial_t\ln A$, $H_B=\partial_t\ln B$;
- $\kappa=8\pi G$;
- $\phi$: phase-transition / driving scalar field;
- $Z(\phi)$: Maxwell kinetic coupling function; a healthy Maxwell sector requires $Z(\phi)>0$.

If a spatially homogeneous Bianchi-I test model is used ($A=B=$ functions of $t$ only), it must be noted that this is a local or homogeneous baseline and does not represent a finite-region bubble-wall solution.

## 1.4 Coordinate Thickness and Proper Thickness

If $z$ is a coordinate and $g_{zz}=B^2$, then on a slice of fixed $t,x,y$

$$d\ell_z=B\,dz,\qquad L_z^{\rm proper}=\int_{z_1}^{z_2}B(t,x,z)\,dz.$$

**The following four quantities must not be conflated**: the coordinate interval $\Delta z$, the proper thickness $L_z^{\rm proper}$, the compact circumference $2\pi R_z$, and the material thin-film thickness. In v1.1, $L_z$ carried all four meanings simultaneously; this is a common source of several erroneous conclusions.

## 1.5 Terminology Revision Table

| v1.1 term | v1.3 disposition | Reason |
|---|---|---|
| "weak force / weak interaction" (referring to van der Waals forces and hydrogen bonds) | uniformly replaced by **noncovalent interactions** or **soft interactions** | In Chinese physics usage, "weak interaction" by default means the weak nuclear force (mediated by $W/Z$, $\sim10^{-18}$ m), which is entirely different from van der Waals forces and hydrogen bonds (N5) |
| "the weak interaction has a range of about 3–5 Å" | **removed** | van der Waals forces have an $r^{-6}$ long tail with no hard cutoff; hydrogen bonds are typically 1.5–2.5 Å; covalent bonds 1.0–1.6 Å; $\pi$–$\pi$ stacking about 3.4 Å. Inferring a lower bound on $R_z$ from an "interaction range" has no basis |
| "topological lower bound $R_z\gtrsim5$ Å" | **removed** (S5) | Whether a bond is stable can only be judged from the eigen-spectrum of the actual Hamiltonian (R1-3); no topological constraint follows from the force range |
| areal density $\sigma(x,y)$ | replaced by $\Sigma(x,y)$, with column density $N_s$ distinguished | $\sigma$ conflicts with the notation for conductivity and surface tension; moreover $\Sigma$ (mass/particle areal density) and $N_s$ (column number density) play different roles in N1 |
| "ultrathin film / two-dimensional electron gas" (as an established conclusion) | conditionalized (S11): valid only under specified Model B/C and specified material response | See §2.6 |
| "destruction region / smooth-conversion region" dichotomy | **removed** (S1, S2) | See §2.1 |

---

# 2. Physical Boundary Layer: $L_z$, Contraction Rate, and Adiabaticity

This chapter supersedes Chapter 2 of v1.1. The v1.1 "legal/illegal parameter space" dichotomy is entirely void, replaced by "screening quantity + model-by-model criteria."

## 2.1 Adiabaticity: From a Single Threshold to a Transition Criterion (S1, S2)

The rough screening parameter used in v1.1 was

$$\eta_{\rm rough}(t)=\frac{\hbar}{\Delta E}\left|\frac{\dot a_z(t)}{a_z(t)}\right|.$$

**v1.3 states explicitly: $\eta_{\rm rough}$ may only serve as a screening quantity before entering detailed calculations, not as a universal guarantee of material stability.** Specifically, the following three v1.1 statements are all void:

- ~~"When $\eta\ge1$ compression is too fast and the material structure is torn apart"~~;
- ~~"When $\eta<1$ matter evolves adiabatically into the two-dimensional eigenstate"~~;
- ~~"$\eta<1$ for all components simultaneously is the prerequisite for smooth two-dimensional reduction of macroscopic structure"~~.

**(a) The correct criterion contains the matrix element and the square of the energy gap.** For the instantaneous Hamiltonian $H(t)|n(t)\rangle=E_n(t)|n(t)\rangle$, the failure parameter of the second-order adiabatic expansion is

$$\epsilon_{mn}(t)=\frac{\hbar\,\big|\langle m(t)|\dot H(t)|n(t)\rangle\big|}{\left|E_m(t)-E_n(t)\right|^{2}},\qquad m\ne n.$$

$\eta_{\rm rough}$ is merely a rough estimate obtained by substituting $|\dot H|\sim E\,|\dot a_z/a_z|$. The ratio of the two,

$$\frac{\epsilon_{mn}}{\eta_{\rm rough}}\sim\frac{E_n}{\Delta E}$$

shows that **$\eta_{\rm rough}$ systematically underestimates transition probabilities for highly excited states, band states, and near continuum thresholds**. For macroscopic solids, $E$ can be taken as the Fermi energy scale (eV) and $\Delta E$ as the band gap or level spacing; level spacings in macroscopic samples can reach $\sim10^{-22}$ eV, so the ratio can span $10^{2}$–$10^{23}$ orders of magnitude. Hence there is an orders-of-magnitude gap between "ground-state $\eta\ll1$" and "all components $\eta<1$"; v1.1 was wrong to treat the latter as a sufficient condition.

**(b) Gapless systems make $\eta_{\rm rough}$ itself diverge.** Metals, critical points, and any model in which the gap closes (a quantum phase transition) during contraction have $\eta_{\rm rough}\to\infty$ as $\Delta E\to0$, so the criterion loses its discriminating power. The correct tools are:

- At avoided crossings: Landau–Zener transition probability $P=\exp(-2\pi\Gamma)$;
- For gap-closing continuous transitions: Kibble–Zurek scaling $n_{\rm ex}\propto\tau_Q^{-d\nu/(1+z\nu)}$, where $\tau_Q$ is the characteristic time width over which the gap tends to zero and $\nu,z$ are critical exponents.

**Key corollary: even if background contraction is infinitely slow, the system still leaves a non-negligible excitation density following a power law.** This is the quantitative counterexample direction to "$\eta<1$ means safe" and the reason v1.3 writes the Kibble–Zurek estimate into the G2 prerequisites.

**(c) An analytic benchmark must calibrate the solver.** The one-dimensional infinite moving-wall problem can be solved exactly using Lewis–Riesenfeld invariants, with the excitation number $\langle n\rangle$ an explicit function of the wall velocity. **R1's time-dependent Schrödinger solver must first reproduce the analytic moving-wall result before it may be used for real potential wells** (G2 prerequisite, mandatory item).

## 2.2 Order-of-Magnitude Screening with $\eta_{\rm rough}$: the Lattice Fails First

Take the P1b target velocity $v=42.47\ {\rm km/s}$ and estimate $\hbar/\tau$ from "the time for compression to cross a characteristic scale $L$, $\tau=L/v$":

| Component | Characteristic scale $L$ | Characteristic energy $\Delta E$ | $\hbar/\tau$ (eV) | $\eta_{\rm rough}$ |
|---|---|---|---|---|
| 1s electron | $a_0=0.529$ Å | 13.6 eV | $5.28\times10^{-1}$ | $3.9\times10^{-2}$ |
| Chemical bond | $\sim1$ Å | 5 eV | $2.80\times10^{-1}$ | $5.6\times10^{-2}$ |
| Lattice vibration (phonon) | $\sim1$ nm | 0.05 eV | $2.80\times10^{-2}$ | $\mathbf{5.6\times10^{-1}}$ |
| Nucleon | $\sim1$ fm | 1 MeV | $2.795\times10^{4}$ | $2.8\times10^{-2}$ |

Three conclusions, all contrary to v1.1's intuition (MODEL RESULT, coarse-screening level):

1. **The first to fail is not the electrons but the lattice.** The softest degrees of freedom (meV phonons) have $\eta_{\rm rough}\approx0.56$, already failing the $\ll1$ condition. Even if "atoms are not torn apart," the lattice is still violently excited nonadiabatically and the object is heated during reduction. **"Structure preservation" and "temperature preservation" must be two separate criteria.**
2. **The nucleon sector is safe** ($\eta\sim10^{-2}$), showing that the strong interaction is not the bottleneck; the bottleneck lies entirely in the electromagnetic and soft-interaction sectors. v1.1 treated "preservation of the weak force" as an additional assumption without magnitude accounting — exactly the opposite direction.
3. All entries in the table above are $\eta_{\rm rough}$-level coarse screening and **cannot in reverse be taken as evidence that "adiabaticity holds"** (see §2.1(a)(b)).

**Disposition:** this table is listed as a G2 prerequisite analytic check; R1's energy budget must explicitly include the nonadiabatic heating term of the phonon sector.

## 2.3 The Power-Law Contraction Exponent $\beta_C$ Has No Universal Threshold (S3)

If

$$a_z(t)=a_{z0}\left(\frac{t}{t_0}\right)^{-\beta_C},\qquad \beta_C>0,$$

then

$$\left|\frac{\dot a_z}{a_z}\right|=\frac{\beta_C}{t},\qquad \eta_{\rm rough}(t)=\frac{\hbar\,\beta_C}{\Delta E(t)\,t}.$$

Whether evolution is adiabatic depends on $\Delta E(t)$, the initial time $t_0$, the time interval, and the Hamiltonian matrix elements, **not on $\beta_C$ alone**. For a fixed gap, increasing $\beta_C$ actually increases the instantaneous contraction rate and is not naturally "more adiabatic"; if the gap varies with $a_z$, the conclusion changes again.

**v1.3 removes** v1.1's dichotomy of "legal parameter space $\beta_C>1$ / illegal parameter space $\beta_C\le1$" and instead scans the triple $(\beta_C,\,t_0,\,\Delta E(a_z))$ for each matter model, giving excitation probabilities and energy deposition point by point; no single threshold constitutes a premise.

## 2.4 The $z$-Direction Spectrum Must Be Discussed Model by Model (S4)

v1.1 wrote: "$p_z^{\min}=2\pi/L_z$: the smaller $L_z$, the larger $p_z^{\min}$, the easier it is to satisfy $\eta<1$, and the destruction branch closes." This argument **does not hold**, because it mixes spectra from three different models:

| Model | $z$-direction setting | Momentum spectrum | Does $p_z^{\min}$ exist? |
|---|---|---|---|
| Model A: noncompact anisotropic contraction | $z\in\mathbb R$ | continuous spectrum | **Does not exist** |
| Model B: finite-thickness potential well | $z\in[z_1,z_2]$, confining potential | discrete bound spectrum | Exists, determined by well eigenvalues, not $2\pi/L_z$ |
| Model C: compact circle | $z\sim z+2\pi R_z$ | KK spectrum $p_n=n\hbar/R_z$ | Exists, $p_1=\hbar/R_z$ |

The relativistic free-field mode energy in Model C is

$$E_n^2=m^2c^4+c^2\frac{n^2\hbar^2}{R_z^2}+c^2p_\perp^2,$$

and whether nonzero KK modes can be frozen out depends on whether the system's available energy satisfies

$$E_{\rm probe}\ll\Delta E_{\rm KK,1},$$

not merely on $R_z\ll\lambda_{\rm visible}$. For nonrelativistic particles $\Delta E_{\rm KK}\sim\hbar^2/(2mR_z^2)$; the specific value depends on boundary conditions, topology, particle mass, and field couplings.

**Important qualification:** compactification with finite $R_z$ is "low-energy effective dimensional reduction," **not** proof that an originally macroscopically open direction can contract continuously into a compact circle. If the original model has noncompact $z$ (Model A), the KK circle spectrum must not be applied.

## 2.5 Momentum Redshift in the Contraction Direction and Anisotropic Heating (N4, Entirely Omitted in v1.1)

In the Bianchi-I background $ds^2=-dt^2+A^2(dy^2)+B^2dz^2$, $\partial_z$ is a Killing vector field, the covariant momentum $p_z$ of a free particle is conserved along geodesics, and the physical momentum is

$$p_{\rm phys}=\sqrt{g^{zz}}\,p_z=\frac{p_z}{B}.$$

Therefore, as $B$ decreases, matter is **generically heated**: nonrelativistically $E_z\propto B^{-2}$, relativistically $E\propto B^{-1}$. Two inevitable consequences:

- A longitudinal pressure $p_z$ grows rapidly with contraction and must back-react on the geometry. **This term must be explicitly included in D3's stress budget**, otherwise "required stress" is systematically underestimated. → New task R2-D.
- Even if background contraction is strictly adiabatic, matter acquires real internal energy. Therefore "smooth" must be redefined as "**this internal energy can be carried away by some dissipative channel**," not "there are no excitations."

(ESTABLISHED: a direct consequence of the Bianchi-I geodesic equations.)

## 2.6 Conditional Statement of "Effective Two-Dimensionality" (S11)

The statement permitted in v1.3 is: **under Model C (or the deeply bound limit of Model B), if $E_{\rm probe}\ll\Delta E_{\rm KK,1}$ (or the first bound-excitation gap) holds, then low-energy observers cannot excite $z$-direction degrees of freedom and the system appears effectively two-dimensional to such observers.**

Statements prohibited in v1.3 are: treating "the object appears as an ultrathin film / two-dimensional electron gas" as an unconditional conclusion; calling a reduction in the number of coordinate modes the disappearance of physical degrees of freedom; and simultaneously claiming "information is retained in the fiber coordinates" and "that direction has disappeared" (the two are logically mutually exclusive — retaining information in the total space precisely shows that the degree of freedom has not disappeared, only that it cannot be excited at low energy).

## 2.7 Voided Items in This Chapter

The following **do not exist** in v1.3 and may not be cited in any chapter:

1. The dichotomy of $\eta\ge1$ destruction region / $\eta<1$ smooth-conversion region;
2. "$\eta<1$ for all components simultaneously is a prerequisite";
3. $\beta_C>1$ guarantees adiabaticity, $\beta_C\le1$ destroys matter;
4. $p_z^{\min}=2\pi/L_z$ and its "destruction branch closes" corollary;
5. The topological lower bound $R_z\gtrsim5$ Å;
6. "Strict $L_z=0$ is attainable" or "arbitrarily close to $L_z=0$ automatically gives two-dimensional reduction."


---

# 3. G0: Analytic Order-of-Magnitude Gate (New in v1.3, Placed Before All Numerical Investment)

## 3.1 The Question G0 Must Answer

v1.2 §4.3 required "calculating bound-state survival rates," but that is a numerical task (R1-2) taking weeks. G0 addresses a more upstream question:

> **Before writing any code, does order-of-magnitude accounting alone already rule out the survival of atoms and chemical bonds for "fixed projected area + conserved particle number" reduction?**

If the answer is yes, then R1's "bound-state survival" question has no solution at human-body scale, the scale of R1's resource commitment must be reset, and the research focus should shift to the area-expansion branch or the particle-number-nonconservation branch. **This directional choice must be settled before writing code.**

## 3.2 Inputs, Formula Chain, and Assumptions

**Inputs (default settings of v1.1 Model C):** human-body mass $M=70\ {\rm kg}$; mean atomic mass $\bar m=10\ {\rm amu}$; projected area $A_\perp=1\ {\rm m^2}$; particle number conserved; electron number taken with $Z/A\simeq0.5$.

**Formula chain:**

$$N_s=\frac{M}{\bar m\,A_\perp},\qquad d_\parallel=N_s^{-1/2},\qquad n_{2D}=\frac{Z}{A}N_s,$$

$$k_F=\sqrt{2\pi n_{2D}},\qquad E_F=\hbar k_F c\ \ (\text{ultrarelativistic criterion:}\ \hbar k_F c\gg m_e c^2),$$

$$E_{2D}=N_e\cdot\frac{3}{4}E_F,\qquad P_{2D}=\frac{E_{2D}}{2}\ \ (\text{ultrarelativistic 2D gas}),$$

$$\tau=\sigma_{\rm eff}\,N_s,\qquad \omega_p^{\rm 2D}=\sqrt{\frac{n_{2D}e^2 k_F}{2\varepsilon_0 m_e}},\qquad A_{\min}=N_s\,d_{\rm bond}^2 .$$

**Assumption list (must be reported together with the conclusions):** free electron gas; $T=0$; lattice and electron–electron interactions neglected; band structure and phase transitions neglected; radiation and neutrino losses neglected; area and mass taken at human-body scale. **Evidence-level ceiling: MODEL RESULT.**

## 3.3 Baseline Numerical Table

| Quantity | Value | Notes |
|---|---|---|
| Areal atomic density $N_s$ | $4.2\times10^{27}\ {\rm m^{-2}}$ | $=M/(\bar m A_\perp)$ |
| Mean in-plane spacing $d_\parallel$ | $1.54\times10^{-14}\ {\rm m}=15.4\ {\rm fm}$ | $=N_s^{-1/2}=2.9\times10^{-4}\,a_0$ |
| Comparison: areal density of nuclear matter | $\sim0.16\ {\rm fm^{-2}}$ | This case is $4.2\times10^{-3}\ {\rm fm^{-2}}$, about 1/40 of it |
| Electron areal density $n_{2D}$ | $2.2\times10^{27}\ {\rm m^{-2}}$ | $Z/A\simeq0.5$ |
| Electron Fermi wave vector $k_F$ | $1.18\times10^{14}\ {\rm m^{-1}}$ | $=\sqrt{2\pi n_{2D}}$ |
| $\hbar k_F c$ | $23.4\ {\rm MeV}$ | The nonrelativistic formula gives 535 MeV $\gg m_ec^2$; **relativistic dispersion must be used** |
| Electron Fermi energy $E_F$ | $\approx23.4\ {\rm MeV}$ | Ultrarelativistic |
| Total degenerate-electron energy $E_{2D}$ | $\approx6.3\times10^{15}\ {\rm J}\approx1.5\ {\rm Mt}$ of TNT | About $8\times10^{5}$ times the chemical binding energy of a human body |
| 2D degeneracy pressure $P_{2D}$ | $\approx3\times10^{15}\ {\rm J/m^2}$ | About $3\times10^{15}$ times the solid surface-energy scale ($\sim1\ {\rm J/m^2}$) |
| Area required to preserve 3 Å spacing $A_{\min}$ | $3.8\times10^{8}\ {\rm m^2}\approx380\ {\rm km^2}$ (per person) | Area must expand by a factor of $3.8\times10^{8}$ |

## 3.4 Three Independent Conclusions

1. **Atoms cannot survive.** The in-plane spacing is compressed to 15.4 fm, about 3400 times smaller than the Bohr radius ($5.29\times10^{4}$ fm). Electron clouds overlap completely; atoms, chemical bonds, and noncovalent networks all cease to exist — **there is no room whatsoever for "adiabatic following," because not even a bound state exists to follow.** This makes R1-2 a problem with a trivial solution at human-body-scale parameters.
2. **"Preservation of noncovalent interactions" (H4) and "unchanged projected area" (H2) are mutually exclusive.** To preserve $\sim3$ Å atomic spacing, the area must expand by a factor of $3.8\times10^{8}$. **This is precisely Model B, which v1.1 rejected on the grounds of an "energy contradiction."** In other words, v1.1's rejection of Model B and its acceptance of Model C cannot both hold; this is an either-or hard dilemma (see §0.2).
3. **The only other way out is to abandon particle-number conservation** (e.g., assuming that most of the mass/charge leaves the membrane during reduction). This is a **new physical assumption** that must be explicitly declared, with $N_s$, $\sigma_s$, $\tau$, the gravitational field, and radiation recomputed; it may not be assumed by default or merely mentioned in a footnote.

## 3.5 Column-Density Conservation and Invariant Optical Depth (N1)

The absorption coefficient is $\alpha=n\,\sigma_{\rm eff}$ ($n$ is the volume number density and $\sigma_{\rm eff}$ the effective single-particle cross section), so the optical depth is

$$\tau=\int\alpha\,dz=\sigma_{\rm eff}\int n\,dz=\sigma_{\rm eff}\,N_s ,$$

where $N_s$ is the **column number density**. If compression preserves particle number and projected area, $N_s$ is strictly invariant and **so is $\tau$**.

> **Therefore "it becomes thinner, so it is transparent" is a faulty inference: it treats $\tau$ as a function of thickness, whereas $\tau$ is actually a function of column density.**

Numerical consistency check (70 kg human body, $A_\perp=1\ {\rm m^2}$):

- 3D state: $n_{\rm at}=6.0\times10^{28}\ {\rm m^{-3}}$, volume $0.07\ {\rm m^3}$, mean thickness $0.07\ {\rm m}$ ⇒ column density $4.2\times10^{27}\ {\rm atoms/m^2}$;
- 2D state: $N_s=4.2\times10^{27}\ {\rm atoms/m^2}$.

The two agree, precisely expressing column-density conservation. The corresponding Thomson optical depth is $\tau_T=N_{s,e}\sigma_T\approx0.15$; for resonant/bound-electron scattering ($\sigma\sim10^{-20}\ {\rm m^2}$), $\tau\sim10^{7}$ — **opaque whether compressed or not**.

**Stronger conclusion:** the 2D plasmon frequency of this electron gas (free-electron-gas estimate) is

$$\omega_p^{\rm 2D}=\sqrt{\frac{n_{2D}e^2 k_F}{2\varepsilon_0 m_e}}\approx2.1\times10^{22}\ {\rm rad/s}\ \Rightarrow\ \hbar\omega_p\approx13.5\ {\rm MeV}.$$

The above uses a nonrelativistic effective mass and is an order-of-magnitude estimate; with relativistic dispersion the effective mass increases by a factor $m_ec^2/E_F\approx0.022$, lowering $\omega_p$ by about 6.8 to $\hbar\omega_p\approx2\ {\rm MeV}$, **with the conclusion unchanged**. This frequency is far above visible photon energies ($\sim2\ {\rm eV}$). In the regime $\omega\ll\omega_p$, any conducting film is nearly an ideal reflector.

> **Therefore the zeroth-order prediction derived directly from column-density conservation is "mirror-like/opaque," opposite to v1.1's "nearly transparent phantom membrane."**

This conclusion is MODEL RESULT (free electron gas, $T=0$, interactions and band structure neglected), and neither side has been verified by R1/L2. **This is the most direct reason why visibility must be handed back to the equations and verbal imagination prohibited**: until a self-consistent $\sigma_s(\omega)$ is available, neither "transparent" nor "opaque" may be stated.

## 3.6 Engineering Implementation of G0

| Item | Content |
|---|---|
| Code module | `src/g0_analytic/scale_budget.py` (single file; inputs $M,A_\perp,\bar m,Z/A,v$ and a $\Delta E$ table) |
| Unit test ① | 3D and 2D column densities agree ($4.2\times10^{27}\ {\rm m^{-2}}$, relative error $<1\%$) |
| Unit test ② | Automatically switch to relativistic dispersion when the nonrelativistic and relativistic formulas differ by $>10^2$, and flag this in the output |
| Unit test ③ | Reproduce in-plane spacing $\sim3$ Å for $A=380\ {\rm km^2}$ |
| Unit test ④ | The derivative of $\tau$ with respect to $B$ (compression factor) is zero (numerical verification of column-density conservation) |
| Acceptance | Two people independently recompute $E_F$, $P_{2D}$, $A_{\min}$, and $\tau$ in agreement (relative error $<5\%$); outcome registered as PASS / NO-GO |
| Dependencies | None (pure analysis, 1–2 days) |
| Level ceiling | MODEL RESULT |

## 3.7 G0 Verdict and Branches

- **PASS (fixed-area branch continues)**: only if independent review overturns conclusion 1 of §3.4 (e.g., discovering some unknown mechanism that can maintain bound states at $d_\parallel\sim15\ {\rm fm}$). There is currently no such evidence.
- **NO-GO (expected outcome)**: the "fixed area + preserved noncovalent interactions" branch is declared dead, and the research focus shifts to one of the following two branches, with **assumptions restated at the start of the document**:
  - **Area-expansion branch**: $A_\perp$ expands as $B$ decreases so that $d_\parallel$ remains at atomic scale; expansion dynamics, energy source, and gravitational consequences must be recomputed.
  - **Particle-number-nonconservation branch**: most mass/charge leaves the membrane during reduction; $N_s$, $\sigma_s$, $\tau$, the gravitational field, and radiation must be recomputed, and the fate of the particles explained.

---

# 4. Theoretical Closure: D1–D3 and Endogenous Geometric Dynamics

## 4.1 D1: Adiabatic Criterion → Screening Quantity (Status: Downgraded)

D1's deliverable changes from a "criterion" to a "screening quantity + excitation-probability table for each sector": given $B(t)$, output estimates of $\eta_{\rm rough}$ and $\epsilon_{mn}$, energy deposition, and excitation density for each sector (electrons, chemical bonds, phonons, nucleons). No binary "destruction/smooth" conclusion is given.

## 4.2 D2: Prescribed Contraction Background (Status: Maintained, Artificially Prescribed)

$a_z(t)\propto t^{-\beta_C}$ is an externally prescribed phenomenological background. Its self-consistency comes from treating $L_z,\beta_C$ as input parameters, not from experimental constraints on real extra dimensions. D2's product can serve only as the **target solution** for R2 (the $B(t)$ to be reproduced), not as an established background.

## 4.3 D3: Endogenous Dynamics (Status: Incomplete, with Two New Prerequisites)

D3 must answer whether the target contraction law can be derived endogenously from more fundamental dynamical equations rather than inserted by hand. The completion criterion is not "finding the required stress" but finding a self-consistent **forward solution** satisfying all field equations, constraints, boundary conditions, and stability conditions.

**Minimal action:**

$$S=\int d^4x\sqrt{-g}\left[\frac{R}{2\kappa}-\frac12(\nabla\phi)^2-V(\phi)-\frac14 Z(\phi)F_{\mu\nu}F^{\mu\nu}\right],\qquad Z(\phi)>0 .$$

The following six items must be **derived independently** from this action; the stress-budget table may not be cited directly:

1. The full Einstein equations;
2. The scalar field equation;
3. Maxwell's equations $\nabla_\mu(ZF^{\mu\nu})=0$;
4. The Bianchi identity $dF=0$;
5. Total energy–momentum conservation $\nabla_\mu T^{\mu\nu}=0$;
6. The ADM Hamiltonian and momentum constraints.

**Gravity-side path (CONDITIONAL):** in the Kaluza–Klein framework, compact-dimension dynamics is governed by the modulus (radion) field $\varphi$, whose potential $V(\varphi)$ and kinetic normalization determine the evolution of $a_z(t)$. If $V(\varphi)$ has a suitable barrier, it can drive power-law or exponential contraction.
**Matter-side path (CONDITIONAL):** the projection of the matter-field energy–momentum tensor along the compact direction back-reacts on the modulus field, forming a self-consistent system; the redshift-heating term $p_z(B)$ of §2.5 must be included.

## 4.4 Stress-Budget Inverse Problem: Three Immediately Executable Minimal Consistency Checks (G3 Prerequisites)

The candidate inverse-problem relation cited in v1.1 is

$$p_x+p_y-p_z=\frac{2}{\kappa}\left[\gamma^2-\gamma h-\frac12 h^2\right],$$

where the setting $H_A=H_B=h$, $H_C=-\gamma$ must be rederived and verified under the full conventions. **In v1.3 this equation is uniformly labeled "inverse-problem relation pending review" until it passes the following three checks:**

**Check ① (coefficient consistency in the $h=0$ limit).** For a Maxwell source containing only $F_{xy}$, the P0 result gives $p_x=p_y=+\rho_B$, $p_z=-\rho_B$ in a local orthonormal frame, hence

$$p_x+p_y-p_z=3\rho_B .$$

The inverse-problem formula gives $2\gamma^2/\kappa$ at $h=0$. Substituting v1.1's $\rho_B=\gamma^2/\kappa$ yields a discrepancy of a factor $\mathbf{3/2}$ between the two sides.

> **Conclusion: "$\rho_B=\gamma^2/\kappa$ automatically satisfies the stress budget" has at least failed the coefficient check in the simplest limit.** It must be rederived from the same set of reduced Einstein equations, with the metric signature, curvature sign, and Einstein-equation convention stated explicitly.

**Check ② (energy conditions).** Substitute $\dot H_B$ and $\bar H_B$ of the target $B(t)$ into $R_{\mu\nu}k^\mu k^\nu$ and check whether realizing this contraction requires violation of the null energy condition (NEC). **If it does, no healthy field source ($Z>0$, no ghosts, energy bounded below) can realize it, and D3 falls directly into NO-GO with no need for numerical investment.**

**Check ③ (Bianchi constraint).** For the minimal ansatz $F_{xy}=f(t,x)$, $dF=0$ constrains $\partial_t f$; one cannot solve only $\nabla_\mu(ZF^{\mu\nu})=0$. If additional field components are unavoidable, they must be explicitly included in the ansatz and solved for, not ignored after the fact.

## 4.5 New Task R2-D: Redshift Heating and $p_z$ Back-Reaction

From §2.5, $p_{\rm phys}=p_z/B$ and nonrelativistically $E_z\propto B^{-2}$. Requirements:

- Write the longitudinal component $\partial_t\rho+(\rho+p_z)\theta_z$ of the energy-conservation equation explicitly into the stress budget;
- Give the curve of the ratio $p_z(B)$ to the required external stress;
- **Determine whether this back-reaction makes the target $B(t)$ unattainable.**

R2-D is a G3 prerequisite: D3's stress budget may not be claimed closed until $p_z(B)$ is available.

## 4.6 D3 Go/No-Go Criteria

| Verdict | Condition |
|---|---|
| **GO** | A regular forward solution exists; $Z>0$ with no ghosts; Hamiltonian and momentum constraints controlled; $B$ evolves according to the target law; the transverse scale $A$ behaves as pre-registered; stress-energy finite; reproducible with respect to initial data and resolution; no identified catastrophic instability under linear perturbations |
| **CONDITIONAL GO** | A stable solution is obtained only over finite time / finite thickness / a finite parameter interval; supports only an effective low-energy 2D description, not $B=0$; result depends on a specific matter source or external drive |
| **NO-GO** | Only inverse-problem stress with no healthy field source; constraints persistently out of control; requires $Z\le0$, negative kinetic energy, or unbounded energy; target contraction necessarily accompanied by curvature/stress singularities without a controlled effective theory; transverse geometry cannot satisfy the target conditions; **check ② requires NEC violation** |

---

# 5. Mapping-Relationship Layer: Three Model Classes, the Correct Fiber-Bundle Formulation, and Bounded-Projection Singularities

This chapter supersedes Chapter 4 of v1.1. v1.1's conclusion that "the compactification fiber-bundle mapping is the uniquely self-consistent mathematical form" is **entirely void**, and the module status is downgraded from "completed" to **OPEN** (revision item S14).

## 5.1 Five Errors in v1.1's Mapping Layer

**(a) $S^3\not\cong S^2\times S^1$.** This can be distinguished directly using the fundamental group and homology:

| Invariant | $S^3$ | $S^2\times S^1$ |
|---|---|---|
| $\pi_1$ | $0$ | $\mathbb Z$ |
| $H_1$ | $0$ | $\mathbb Z$ |
| $H_2$ | $0$ | $\mathbb Z$ |
| Trivial $S^1$ bundle? | — | Yes |

The Hopf fibration is $S^1\hookrightarrow S^3\to S^2$, with total space $S^3$ and Chern class $c_1=\pm1$; **it is not a direct product**. v1.1's statement that "the overall topology is $S^2\times S^1$" is an erroneous equality.

**(b) The base space is also wrong.** For a bounded macroscopic object projected along $z$, the base space is the two-dimensional **disk $D^2$ (with boundary)**, not the boundaryless $S^2$. v1.1 treated the "sphere" both as the total space and implicitly as the base space — two manifestations of the same confusion.

**(c) $\Phi:B^3\to D^2$ is not a fiber bundle at all.** Fibers over interior points are open intervals $(0,L_z)$, while fibers over boundary points degenerate to a single point. The topological type of the fiber jumps on $\partial D^2$ ⇒ **the local trivialization condition fails at the boundary**. Therefore v1.1's argument chain "$\Phi$ is a fiber-bundle projection ⇒ continuous manifold deformation ⇒ no tearing" **does not hold for any bounded macroscopic object**. To recover fiber-bundle structure one may only speak of unbounded or periodic spaces ($T^3$, $\mathbb R^3$), and these are no longer "macroscopic objects."

**(d) Periodizing a bounded physical direction glues the front and back surfaces.** Setting $z\sim z+L_z$ so that $z$ becomes $S^1$ is equivalent to imposing periodic boundary conditions: the object's $z=0$ surface and its $z=L_z^-$ surface become neighboring points along the fiber. For a human body, this makes the tip of the nose and the back of the head fiber neighbors whose wavefunctions overlap along the fiber, introducing unphysical cross-body bonding. **This is a physical consequence at the level of model definition, not a matter of coordinate choice.**

**(e) "Information retained in the fiber" and "that direction has disappeared" are logically mutually exclusive.** Information retained in the total space precisely indicates that the degree of freedom has not disappeared, only that it cannot be excited at low energy. "Local trivialization" is a mathematical property and cannot imply the continuity of chemical bonds.

(a–d are ESTABLISHED mathematical/model conclusions; e is logical analysis.)

## 5.2 Correct Fiber-Bundle Formulation

If fiber-bundle language is genuinely to be used, the projection must be written as

$$\pi:E\to B_2,\qquad \pi(x,y,\theta)=(x,y),\qquad \pi^{-1}(q)\simeq S^1,$$

and discussion of the global structure is permitted **only after the following five items have been specified**:

1. The total space $E$ (including boundary);
2. The base space $B_2$ (including boundary);
3. The fiber and transition functions;
4. The topological class of the bundle (for a principal $S^1$ bundle, compute the Chern class $c_1$);
5. A proof of the claimed topology of the total space.

Only when the bundle is trivial ($c_1=0$ and the transition functions admit global trivialization) may one write $E\simeq B_2\times S^1$. A general principal $S^1$ bundle need not be trivial.

## 5.3 Discrete Comparison of the Three Model Classes (Replacing v1.1's Comparison Table)

The "physical self-consistency: high/medium/low" ratings in v1.1's comparison table are **removed**; only testable mathematical and physical properties are listed:

| Property | Model A: noncompact anisotropic contraction | Model B: finite-thickness potential well | Model C: compact circle $S^1$ |
|---|---|---|---|
| $z$-direction setting | $z\in\mathbb R$, $B(t,x)$ decreasing | $z\in[z_1,z_2]$, confining potential | $z\sim z+2\pi R_z$ |
| Mapping form | $\pi(x,y,z)=(x,y)$, fiber is an interval | $\pi(x,y,z)=(x,y)$, fiber is the well interval | $\pi:E\to B_2$, fiber $S^1$ |
| Momentum spectrum | continuous, no $p_z^{\min}$ | discrete bound spectrum (set by well) | KK spectrum $p_n=n\hbar/R_z$ |
| Low-energy effective 2D | not automatic; requires separate proof | depends on bound gap and $E_{\rm probe}$ | valid when $E_{\rm probe}\ll\Delta E_{\rm KK,1}$ |
| Fiber degeneration on bounded objects | present (at boundary) | present (at boundary) | present (if the bounded interval is periodized; see §5.1(d)) |
| Fate of $z$ information | retained in dynamics | retained in bound-state wavefunctions | retained in KK labels (not excitable at low energy) |
| Equivalent to "macroscopic object flattened"? | No | No | No |
| Main open problem | Can matter follow $B(t)$? | Can the well deepen adiabatically? | How is $R_z$ generated dynamically? |

**Model-selection requirement (R3 acceptance):** the unproven claim "the fiber-bundle mapping is the uniquely self-consistent form" may no longer be used. One must justify the choice of a given model by comparison with at least one noncompact contraction model (A) and one thin-layer model (B), and provide each model's low-energy effective action and conditions of applicability.

## 5.4 Correct Measure for Areal Density and Macroscopic Quantities (S9)

If $\rho$ is the mass or particle number density per unit **proper three-dimensional volume** and $g_{zz}=B^2$, then on a simple orthogonal slice

$$\Sigma(x,y)=\int\rho(x,y,z)\sqrt{g_{zz}}\,dz=\int\rho(x,y,z)\,B(x,y,z)\,dz .$$

More generally, the full spatial-slice volume element should be used:

$$dV_3=\sqrt{\det h_{ij}}\,d^3x .$$

It is **prohibited** to write $\Sigma=\int\rho\,dz$ directly without stating the density definition and volume measure; it is **prohibited** to treat $\rho(x,y,0)L_z$ as a general result (if the density, wavefunction, and coordinate support of matter change with contraction, treating $\rho$ as approximately constant along $z$ does not hold).

Consistency requirement with G0: under H2 (fixed area) and H3 (particle number conservation), the derivative of $\Sigma$ with respect to the compression factor $B$ should be zero, i.e., R3-3's output must agree with G0's column-density conservation.

## 5.5 Resolvability Criterion for $z$-Direction Structure

This layer delivers only criteria, not appearance: if adjacent structures in the $z$ direction are separated by $d$ in the imaging plane and the system's operating wavelength is $\lambda$, then for $d\ll\lambda$ the two lie below that imaging system's diffraction limit and cannot be resolved. **Whether they can be resolved and with what signal they appear depends on the solutions of L1–L4 in Chapter 6, not on any preset appearance.**

Note (v1.2 §2.8, retained in v1.3): thickness resolvability, reflection/absorption/scattering contrast, self thermal radiation, and retinal signal exceeding threshold are **four different questions**; the single condition $L_z\le\lambda$ must not be used to answer all four at once.


---

# 6. Physical Model of Visual Presentation: Equations and Criteria Only, No Pictures

This chapter supersedes Chapter 5 of v1.1. Its positioning is unchanged but its constraints are tightened: **this chapter delivers the equations, criteria, and input-quantity list that determine visual signals, not any statement about "what it looks like."** What signal actually appears after two-dimensional reduction is the solution of these equations for given $(B,\rho,\sigma_s,\text{viewing angle},\text{observer})$; this solution is incomplete until the light–matter coupling and radiative-transfer modules are completed.

## 6.1 Four Criteria That Must Be Kept Separate

| Criterion | Content | Answered by layer |
|---|---|---|
| C1 thickness resolvability | Whether the third-dimension thickness can be resolved by the imaging system ($d\ll\lambda$) | L1 + L4 |
| C2 optical contrast | The object's reflection/absorption/scattering contrast for incident light | L2 + L3 |
| C3 self-emission | The object's own thermal / nonthermal radiation | L3 |
| C4 visual threshold | Whether the retinal signal exceeds threshold, and spatial/spectral/temporal contrast with the background | L4 |

**Sub-wavelength thickness does not automatically imply invisibility**; thin films can still be detected through surface conductivity, absorption, reflection, scattering, and phase changes. The roughly 1 arcminute resolution of the human eye is only an empirical scale for particular visual acuity, contrast, and illumination, not a fixed sampling law.

## 6.2 Layered Models L1–L4

R5 is divided into four layers that **cannot substitute for one another**:

- **L1 geometric optics**: given the already-solved spacetime metric, solve null geodesics and compute the observer's four-velocity, local orthonormal frame, frequency shifts, and celestial-sphere direction mapping.
- **L2 material optics**: given a specific material's $\sigma_s(\omega)$, dielectric function, or polarization tensor, compute reflection, transmission, absorption, and scattering, specifying substrate, incidence angle, polarization, and spectral range.
- **L3 radiative transfer**: given the absorption coefficient, emission coefficient, scattering kernel, and boundary conditions, solve the radiative-transfer equation, use Kirchhoff relations mode by mode, and distinguish thermal emission from reflection/scattering signals.
- **L4 observer imaging**: use the optical system's PSF, retinal irradiance, spatial/temporal integration, contrast sensitivity, spectral response, and exposure to reach the final visibility verdict.

## 6.3 L1: Geodesics and Frequency Shifts

For photon wave vector $k^\mu$ and observer four-velocity $u^\mu$, the locally measured frequency is

$$\omega_{\rm obs}=-k_\mu u^\mu,\qquad \frac{\omega_{\rm obs,2}}{\omega_{\rm obs,1}}=\frac{(-k\cdot u)_2}{(-k\cdot u)_1}.$$

When spacetime is nonstationary or the observer is moving, **Doppler results must not be inferred from the front velocity alone**; the geodesic must actually be integrated and the four-velocities of emitter and receiver specified.

## 6.4 L2: Material Optics — $\sigma_s(\omega)$ Is an Input, Not a Universal Constant (S10)

For an ideal, free-standing, normally incident, isotropic two-dimensional conducting sheet, the response can be expressed using the surface conductivity:

$$r=-\frac{Z_0\sigma_s(\omega)}{2+Z_0\sigma_s(\omega)},\qquad t=\frac{2}{2+Z_0\sigma_s(\omega)},\qquad R=|r|^2,\ T=|t|^2,\ A=1-R-T .$$

For multilayers, oblique incidence, anisotropic sheets, or structures containing a substrate, the appropriate boundary conditions and TE/TM Fresnel coefficients or transfer matrices must be used; for a homogeneous film of thickness $L_z$, the standard thin-film formula is

$$R=\left|\frac{r_{01}+r_{12}e^{-2i\delta}}{1+r_{01}r_{12}e^{-2i\delta}}\right|^2,\qquad \delta=\frac{2\pi n L_z}{\lambda},$$

where $n,\kappa$ are the film's refractive index and extinction coefficient and $r_{ij}$ are Fresnel coefficients. The conclusion from this expression is a quantitative solution for $R,T,A$ as functions of $(L_z,\lambda,\theta_{\rm inc},n,\kappa)$: **what it gives is the partition of electromagnetic energy, not "color" or "pattern."**

**On $\pi\alpha\approx2.3\%$ (downgraded to a benchmark note).** This value may be used only when all six of the following premises hold; if even one is missing, it must not be cited:

1. The carriers are approximately massless Dirac fermions (linear dispersion);
2. $\hbar\omega\gg2|E_F|$ (interband transitions open, Pauli blocking off);
3. $T\to0$, and electron–phonon and electron–electron scattering broadening is neglected;
4. The noninteracting (RPA-level) approximation is used, with excitonic corrections not included;
5. A free-standing monolayer with no substrate dielectric environment;
6. Normal incidence with polarization averaging.

Only when $\sigma_s=e^2/(4\hbar)$ does $Z_0\sigma_s=\pi\alpha$, recovering 2.3%.

> **Key constraint: by G0/N2, under H2+H3 the electron system of the reduced object is an ultrarelativistic degenerate electron liquid ($k_F\approx1.2\times10^{14}\ {\rm m^{-1}}$, $E_F\approx23\ {\rm MeV}$), whose $\sigma_s(\omega)$ is determined by its own $k_F$ and plasmon and has no relation whatsoever to the graphene value.** It is therefore prohibited to use 2.3% as a default input or to let it enter any visibility conclusion.

## 6.5 L3: Radiative Transfer and Correct Use of Kirchhoff's Law

The general form is

$$\frac{dI_\nu}{ds}=-\alpha_\nu I_\nu+j_\nu,$$

and scattering requires adding scattering in/out integral terms. For a two-dimensional surface source, one should adopt boundary jump conditions consistent with the chosen definition of radiation intensity or a dimensionally consistent surface-source form; the $\delta(s)$ surface-source notation must specify its units and normal coordinate.

Kirchhoff's law must be applied **mode by mode according to frequency, direction, polarization, and the corresponding thermodynamic equilibrium conditions**: the emissivity of a given optical mode equals its absorptivity. It is **not** permissible to infer from $A\approx2.3\%$ in some visible band that the total thermal-radiated power over the entire spectrum is always 2.3% of a blackbody; such an approximation is allowed only when the absorptivity is approximately flat over the relevant spectral range and the conditions of applicability are met.

## 6.6 L4: Human-Eye Imaging and Quantities That Must Be Reported Together

Imaging is simplified as convolution of the point-spread function with the object-plane irradiance:

$$E_{\rm retina}(x',y')=\iint {\rm PSF}(x'-\xi,y'-\eta)\,E_{\rm image}(\xi,\eta)\,d\xi\,d\eta .$$

Sub-diffraction-limit details ($d\ll\lambda$) are smoothed out in this integral. The final visibility verdict must report all of the following together:

- Brightness/color contrast between target and background;
- Angular size and spatial frequency;
- Spectral distribution;
- Temporal variation and exposure conditions;
- Viewing distance, pupil diameter, and imaging PSF;
- Comparison of the retinal signal with the threshold.

**What false-color or mapping scheme is used (e.g., coloring by $\Sigma$ or by composition) is a conventional display choice, not physical deduction.** This chapter only points out that any visualization must take the above physical quantities as inputs, with its result given by the physics of imaging.

## 6.7 Prohibitions and Rendering-Annotation Requirements in This Chapter

**Prohibited (v1.1 crossed these lines):**

- "Ultratransparent / nearly invisible / ghostly phantom membrane" and all its variants — by N1, $\tau=\sigma_{\rm eff}N_s$ is invariant under fixed-area compression, and "thinner means transparent" is a faulty inference;
- "Mirror-like/opaque" from zeroth-order plasma estimates must likewise not be published as a conclusion — like "transparent," it is unverified by R1/L2;
- Any verbal imagination about color, patterns, or "scroll-like" appearance.

**Mandatory annotation (on every rendered frame and every $R/T/A$ plot):**

$$\text{annotation}=\big(N_s,\ \text{source and assumption level of }\sigma_s,\ \tau,\ \text{incidence conditions},\ \text{background model},\ \text{uncertainty}\big).$$

**Labeling rules (S12, S13):** visual models may be developed in parallel, without being blocked by D3; however, until both G4 and G5 have passed, their products must all be labeled **"prescribed-background test optics"** and must not be called DCC observational predictions. D3 does not block rendering-pipeline development, but it does block any statement at the "physical prediction" level.

---

# 7. P0/P1 Baseline Integration and G1 Closure

## 7.1 Integration of P0 Conclusions

| Candidate | Current conclusion | Must continue checking |
|---|---|---|
| Maxwell $F_{xy}$ | Retained; in a local orthonormal frame $p_x=p_y=+\rho_B,\ p_z=-\rho_B$, giving the required directionality | Full Maxwell equations, Bianchi identities, Einstein constraints, and inhomogeneous solutions |
| Three-form $H_{txy}$ | With the standard positive-sign kinetic term the pressure direction is opposite to the target trend; not a priority for now | Reevaluate only if the specific action/duality convention changes |
| Three-form $H_{xyz}$ | Simple configurations cannot provide the required directional distinction | Not the first choice |
| Compactification modulus (radion) | Promising, but must be derived from higher-dimensional reduction | Radion kinetic term, potential, normalization, and coupling to geometry |
| SSB vector | Conditional candidate | $A_0$ constraint, longitudinal mode, ghosts, gradient stability, energy lower bound |

The Maxwell-action candidate is discussed in §4.3. The following must be satisfied simultaneously:

$$\nabla_\mu\!\left(ZF^{\mu\nu}\right)=0,\qquad dF=0 .$$

For the minimal ansatz containing only $F_{xy}=f(t,x)$, the Bianchi identity constrains $\partial_t f$; one cannot solve only the Maxwell equation and ignore $dF=0$ (i.e., §4.4 check ③).

## 7.2 Current P1a Results and G1-A / G1-B

Reported (MODEL RESULT): the static wall position and velocity are close to zero; wall thickness numerical 4.167 (analytic 4.164, error $<0.1\%$); energy residual $8.75\times10^{-7}$; wall tension $\sigma_w=0.942$; after mesh refinement the residual falls from $8.75\times10^{-7}$ to $5.37\times10^{-8}$.

**Verdict: the static benchmark preliminarily passes, but the convergence order has not been demonstrated.**

**G1-A third-mesh convergence test:**

1. Use at least three spatial resolutions $dx,\ dx/2,\ dx/4$;
2. Keep the physical domain, boundary conditions, and time-integration error control consistent;
3. Compute errors separately for wall position, wall thickness, tension, and field profile;
4. When an analytic solution exists, compute the observed order
   $$p=\log_2\!\left(\frac{\|u_{dx}-u_{dx/2}\|}{\|u_{dx/2}-u_{dx/4}\|}\right);$$
5. **The decay ratio of the energy residual must not be used in place of the solution's convergence order.**

Acceptance: wall thickness, wall position, and tension stabilize under mesh refinement; the observed order is compatible with the discretization scheme's expectation; boundary-reflection contamination does not enter the measurement window.

**G1-B analytic check of wall tension:**

$$\sigma_w=\int dx\left[\frac12(\partial_x\phi)^2+V(\phi)-V_{\min}\right],\qquad \frac12(\partial_x\phi)^2\approx V(\phi)-V_{\min}\ (\text{first integral of the static solution, where applicable}).$$

Acceptance: the numerical integral, analytic kink tension, and grid-extrapolated result agree with one another, with error thresholds registered before the run.

## 7.3 P1b Friction Parameter Correction (Reviewed and Approved)

The collective-coordinate model is a low-speed phenomenological equation:

$$\sigma_w\frac{dv}{dt}=F_{\rm drive}-\eta_{\rm eff}v,\qquad v_{\rm term}=\frac{F_{\rm drive}}{\eta_{\rm eff}} .$$

From the existing scan data, $\eta_{\rm eff}v_{\rm term}\approx0.0106$, and the target velocity is

$$\beta_{\rm target}=\frac{42.47}{299792.458}=1.4166\times10^{-4}\ \Rightarrow\ \eta_{\rm target}=\frac{0.0106}{1.4166\times10^{-4}}=74.8\approx75 .$$

**Execution revisions (implement immediately in Sprint 0):**

- **Correct** "$\eta\approx1.0$ corresponds to 42.47 km/s" to "with the current nondimensionalization and scan table, $\eta_{\rm eff}\approx75$";
- Note $F_{\rm drive}$, $\sigma_w$, the velocity units, and the friction-parameter units in the result files;
- 42.47 km/s remains archived as a **low-speed phenomenological assumption**, not a theoretical prediction;
- This equation is not full relativistic bubble-wall dynamics; **the true relativistic limit must not be extrapolated from the numerical upper bound at $\eta=0$**; the relativistic-velocity group must establish a separate wall-momentum equation and define the friction four-force / energy–momentum exchange.

**G1 closure conditions:** G1-A and G1-B completed, and the P1b parameter revision completed. The magnetically driven PDE is not a required G1 closure item; it is handed over to R2.

---

# 8. Engineering Task List (R1–R5, Ordered by Dependency)

Each item lists: equations / code module / unit tests / acceptance criteria / dependencies / evidence-level ceiling.

## 8.1 R1-1 Free Scalar Field Modes

| Item | Content |
|---|---|
| Equations | $S_\chi=-\frac12\int d^4x\sqrt{-g}\left[g^{\mu\nu}\partial_\mu\chi\partial_\nu\chi+m^2\chi^2\right]$; instantaneous frequency $\omega_k^2(t)$; Bogoliubov coefficients $\beta_k$ |
| Module | `src/r1_free_field/{mode_eq.py, bogoliubov.py, convergence.py}` |
| Tests | Static $B=1$ limit reproduces Minkowski modes; adiabatic limit $\|\beta_k\|\to0$; energy-conservation residual converges with the mesh |
| Acceptance | Three-mesh convergence order consistent with the scheme's expectation; analytic fit to the scaling law of excited-particle number with $\dot B$ |
| Outputs | Mode equations, canonical normalization, instantaneous frequency, particle-production energy, scan plots versus $B_{\min}$ and contraction rate |
| Prohibited | Calling a reduction in the number of coordinate modes the disappearance of physical degrees of freedom |
| Dependencies | G0 |
| Level ceiling | MODEL RESULT |

## 8.2 R1-2 Single-Particle Bound States

**Level A (controlled well model):** Laplace–Beltrami kinetic term + prescribed potential; three-dimensional Coulomb, two-dimensional $-\ln r$, and external potential implemented **separately; mixing is prohibited**; specify the propagation space and boundary conditions of the electromagnetic field.
**Level B (electromagnetically self-consistent atom model):** Maxwell equations self-consistent with the quantum states of charged particles; distinguish the three cases "field remains 3D," "field is reduced," and "finite thickness + substrate."

| Item | Content |
|---|---|
| Module | `src/r1_bounded/{hb_operator.py, spectra.py, tdse.py}` |
| Tests (mandatory) | **Lewis–Riesenfeld analytic solution of the moving infinite deep well**; $B=1$ reproduces hydrogen energy levels; cross-validation of time evolution against the instantaneous-eigenstate approximation |
| Outputs | $E_0(B)$, $\Delta E_{\min}(B)$, $z$-direction probability width, excited-state occupation, bound-state survival rate, level crossings and continuum threshold, external-field and radiation energy |
| Acceptance | Survival rate and energy budget reach **thresholds registered before the run** before one may say "smooth adaptation under this model" |
| Dependencies | R1-1 |
| Level ceiling | MODEL RESULT |

## 8.3 R1-3 Chemical Bonds and Lattice

| Item | Content |
|---|---|
| Equations | Two-center potential → small-lattice dynamical matrix $D_{ij}$; phonon spectrum $\omega(q)$; imaginary-frequency criterion |
| Module | `src/r1_lattice/{dimer.py, dynamical_matrix.py, phonon.py}` |
| Tests | Equilibrium spacing reproduces the given bond energy; $B=1$ phonon spectrum entirely real; record the $B_c$ where an imaginary frequency first appears |
| Outputs | Bond length, bond energy, vibrational frequency, bond-breaking/reforming probability, phonon spectrum and imaginary frequencies, defect density and thermalization energy |
| Acceptance | Provide $B_c$ and the bond-breaking probability curve; classify results into the four categories of §8.4 |
| Prohibited | Using an "interaction range of 3–5 Å" to set a lower bound on $R_z$ |
| Dependencies | R1-2 |
| Level ceiling | MODEL RESULT |

## 8.4 Mandatory Four-Way Classification of R1 Results

Every R1 summary must place its results into one of the following categories; unclassified "adapted / not adapted" conclusions are prohibited:

- **A: adiabatic following**;
- **B: nonadiabatic but still bound / recombinable**;
- **C: bound-state instability or structural destruction**;
- **D: model or classical approximation fails, cannot be decided**.

Combining this with the §2.2 magnitude screening, the phonon sector is expected to fall into B or C at human-body-scale parameters, while the electron and nucleon sectors fall into A.

## 8.5 R2-A Homogeneous Bianchi-I Forward Solution

| Item | Content |
|---|---|
| Equations | $S=\int\sqrt{-g}\,[R/2\kappa-\frac12(\nabla\phi)^2-V(\phi)-\frac14 Z(\phi)F^2]$, $Z>0$; **independently derive symbolically** all Einstein components + the scalar equation + Maxwell's equations + $dF=0$ |
| Module | `src/r2_homogeneous/{symbolic_einstein.py, rhs.py, constraint_monitor.py, scan.py}` |
| Tests | Isotropic limit ($A=B$) reproduces FRW; vacuum limit reproduces Misner oscillatory behavior; $h=0$ stress-budget coefficient check (§4.4 check ①) |
| Acceptance | Hamiltonian-constraint residual below the registered threshold and non-drifting; scan $Z(\phi)$, $V(\phi)$, and initial data; assess curvature invariants, energy density, and linear-perturbation stability |
| Dependencies | G0; in parallel with R1 |
| Level ceiling | MODEL RESULT |

## 8.6 R2-B ADM Constraint Preservation

| Item | Content |
|---|---|
| Module | `src/r2_adm/{adm_decomposition.py, constraints.py, evolver.py}` |
| Acceptance | Initial constraint residual meets target; no exponential drift during evolution; residual converges under mesh refinement; boundaries inject no unregistered error; consistent with the homogeneous-limit solution |
| Dependencies | R2-A |

## 8.7 R2-C Inhomogeneous $\phi+F$ Coupling

**Mandatory sequence:** fixed-background $\phi$ → fixed-background $\phi+F$ → dynamic geometry without magnetic flux → dynamic geometry + magnetic flux → finite-region matching boundaries.
**Acceptance:** every level passes constraint monitoring; $F_{xy}$ satisfies both Maxwell's equations and $dF=0$; if additional components are required, they must be solved explicitly.
**Dependencies:** R2-B.

## 8.8 R2-D Redshift Heating and $p_z$ Back-Reaction (New)

| Item | Content |
|---|---|
| Equations | $p_{\rm phys}=p_z/B$; nonrelativistic $E_z\propto B^{-2}$, relativistic $E\propto B^{-1}$; write the longitudinal energy-conservation component explicitly into the stress budget |
| Acceptance | Give the curve of the ratio $p_z(B)$ to the required external stress; determine whether this back-reaction makes the target $B(t)$ unattainable |
| Dependencies | R2-A |
| Status | **G3 prerequisite**: D3's stress budget may not be claimed complete until this item is closed |

## 8.9 R3-1 Separate Implementation of the Three Model Classes

Implement separately Model A ($z\in\mathbb R$, continuous spectrum), Model B (finite-thickness potential well, discrete bound spectrum), and Model C (compact circle, KK spectrum $E_n^2=m^2c^4+c^2n^2\hbar^2/R_z^2+c^2p_\perp^2$).
**Acceptance:** each model gives a low-energy effective action; the low-energy cutoff condition $E_{\rm probe}\ll\Delta E_{\rm KK,1}$ is explicitly verified; **spectral conclusions must not be borrowed across models**.

## 8.10 R3-2 Fiber-Bundle Data and Bounded-Projection Singularities

**Deliverables:** $E$, $B_2$, fiber, transition functions, Chern class; for $B^3\to D^2$ give an explicit characterization of the fiber-degeneration set $\partial D^2$ and its impact on "no tearing" claims; give a quantitative estimate of the front/back surface gluing caused by periodization $z\sim z+L_z$ (the cross-body wavefunction-overlap amount).
**Acceptance:** the "uniquely self-consistent" conclusion no longer appears; the model choice must be justified after comparison with at least one noncompact model and one thin-layer model.

## 8.11 R3-3 Macroscopic Quantities Under the Correct Measure

**Deliverables:** $\Sigma=\int\rho\sqrt{g_{zz}}\,dz$, surface charge, surface entropy; for each quantity, state the definition of $\rho$ and the slice volume element.
**Acceptance:** consistent with G0's column-density conservation (the derivative of $\Sigma$ with respect to $B$ is zero).

## 8.12 R4 Finite-Region Geometry and Interface Matching

**Execution steps:** ① establish a finite-width front in the $1+1$ reduced model; ② specify the lapse, shift, spatial metric, and extrinsic curvature for the inner and outer regions; ③ check matching conditions and constraints; ④ use junction conditions in the thin-wall limit and solve the field equations directly for finite-thickness walls; ⑤ upgrade to axisymmetry or spherical symmetry; ⑥ check whether the asymptotic region beyond the boundary recovers the prescribed background.

**Prohibited:** directly extrapolating a local planar wall solution into an Earth-covering spherical front.
**Acceptance:** geometric continuity of the inner and outer regions or correct thin-wall jump conditions; energy–momentum conservation; constraint propagation; resolvable front thickness, velocity, and curvature; finite-region boundaries produce no spurious signals; computable along observer worldlines.

## 8.13 R5-L1…L4 Optics and Imaging

| Layer | Equations/inputs | Acceptance |
|---|---|---|
| L1 | Null geodesics; $\omega_{\rm obs}=-k_\mu u^\mu$ | Consistent with known static limits; frequency shifts consistent with four-velocity definitions |
| L2 | Self-consistent $\sigma_s(\omega)$ (Lindhard / transfer matrix); TE/TM Fresnel coefficients | $R+T+A=1$; **defaulting to $\pi\alpha$ is prohibited** |
| L3 | $dI_\nu/ds=-\alpha_\nu I_\nu+j_\nu$ plus scattering terms; mode-by-mode Kirchhoff | Consistent units; single-frequency absorptivity must not be treated as a full-band Stefan–Boltzmann ratio |
| L4 | PSF-convolution imaging + retinal threshold | PSF and threshold have explicit parameter sources; every frame annotated with $N_s$, the $\sigma_s$ source, and the assumption level |

**Level ceiling:** until G4 and G5 pass, all products may only be labeled "prescribed-background test optics."


---

# 9. Numerical Engineering Specifications and Deliverable Requirements

## 9.1 Every Solver Must Have

- A parameter configuration file (key physical parameters must not be hardcoded in scripts);
- A fixed random seed (if stochastic processes are included);
- Mesh and time-step convergence tests;
- Unit tests and analytic-limit tests;
- Energy/constraint residual logs;
- Machine-readable results (CSV/JSON/HDF5);
- Runtime environment, dependency versions, and Git commit;
- **Logs must also be saved for failed runs; successful results alone may not be retained.**

## 9.2 Result Directory Structure

```text
DCC/
  docs/
    Macro3D_to_2D_Smooth_Reduction_Roadmap_v1.3.md
    decisions/                 # GO / NO-GO decision records
  src/
    g0_analytic/               # New: analytic order-of-magnitude gate
    p1_wall/
    r1_free_field/
    r1_bounded/
    r1_lattice/
    r2_homogeneous/
    r2_adm/
    r3_models/
    r4_frontier/
    optics/                    # L1–L4
  configs/
  tests/
    analytic_limits/           # moving-wall Lewis–Riesenfeld, hydrogen atom, FRW, Misner
    convergence/
    constraints/
  runs/
    G0/ P1/ R1/ R2/ R3/ R4/ R5/
  reports/
    gates/ figures/ tables/
```

## 9.3 Registration Template for Each Experiment

```yaml
experiment_id:
date:
git_commit:
model_class:                 # anisotropic / thin-layer / compactified
metric_ansatz:
action:
units:
assumption_flags:            # which of H1..H5 are enabled/abandoned
initial_conditions:
boundary_conditions:
solver:
spatial_resolution:
time_step:
parameters:
observables:
convergence_tests:
constraint_tests:
acceptance_thresholds:       # must be filled in before the run
result:                      # PASS / CONDITIONAL / FAIL
evidence_level:              # ESTABLISHED / MODEL RESULT / CONDITIONAL / OPEN / FALSIFIED
known_limitations:
```

**Thresholds must be registered before the run; adjusting thresholds after seeing the results in order to manufacture a PASS is prohibited.**

## 9.4 Deliverables per Stage

Each stage must deliver at least: ① a theory document (definitions, assumptions, derivations, notation conventions, scope); ② a solver (source code, configuration, dependency versions); ③ tests (analytic limits, convergence, conservation/constraints); ④ machine results (CSV/JSON/HDF5); ⑤ figures and tables (all axes, units, and parameters complete); ⑥ a review report (passed, failed, and unresolved items); ⑦ a decision record (GO / CONDITIONAL GO / NO-GO with rationale).

**MODEL RESULT or CONDITIONAL statements must not be rewritten as universal physical laws.**

---

# 10. Dependency Graph and Stage Gates

## 10.1 Updated Dependency Graph (v1.3)

```text
                  G0 analytic order-of-magnitude gate (new: table of N_s / E_F / P_2D / tau / eta_rough)
                  ├─ PASS  → fixed-area branch continues
                  └─ NO-GO → shift to the "area expansion" or "particle-number nonconservation" branch (requires an explicit new assumption)
                           |
         +-----------------+------------------+
         |                                    |
         v                                    v
   G1 numerical baseline freeze         R1-1 free-field modes
   (P1a third mesh / P1b eta≈75 /            |
    sigma_w analytic check)                    v
         |                                R1-2 bound states (with moving-wall Lewis–Riesenfeld benchmark)
         v                                    |
   R2-A homogeneous Bianchi-I forward solution <----+ (matter response feeds back into the stress budget)
         |                                v
         v                            R1-3 chemical bonds/lattice → B_c
   R2-B ADM constraint preservation          |
         |                                    |
         +--> R2-D redshift heating p_z(B)    v
         |         |                          v
         v         v                  G5 effective 2D matter and mapping (R3-1/2/3)
   R2-C inhomogeneous phi+F  ────────────►        |
         |                                    v
         v                            R5-L1..L4 optics and imaging
   R4 finite region and interface matching  ─────►        |
         |                                    v
         v                                  G6 observer predictions
       G4                            (until now labeled only "prescribed-background test optics")
```

**Stage-gate changes relative to v1.2 (four items):**

1. **G0 added** (pure analysis, placed before all numerical investment);
2. **G2 prerequisites** add the "moving-well Lewis–Riesenfeld analytic benchmark + Kibble–Zurek estimate";
3. **G3 prerequisites** add the three checks of §4.4 ($h=0$ coefficient, NEC, $dF=0$) and the R2-D redshift heating of §4.5;
4. **G6 clarified**: until both G4 and G5 pass, any rendering result may only be labeled "prescribed-background test optics."

## 10.2 Stage-Gate Overview

| Gate | Prerequisites | GO condition | NO-GO consequence |
|---|---|---|---|
| **G0** (new) | None (analytic) | Atoms can survive at fixed area (no evidence currently) | The "fixed area + preserved soft interactions" branch is declared dead; shift to the area-expansion or particle-number-nonconservation branch |
| **G1** | P1a third mesh, $\sigma_w$ analytic check, P1b parameter revision | Static baseline frozen (including convergence-order proof) | Numerical baseline untrustworthy; all downstream work suspended |
| **G2** | R1-1 and at least one controlled model in R1-2 complete; moving-wall benchmark passed | Reproducible classification of adiabatic/nonadiabatic response under a prescribed background | Gap closure or bound-state disappearance → switch to the "destruction/recombination" branch |
| **G3** | Full derivation of the Einstein–matter equations; three checks of §4.4; R2-D gives $p_z(B)$ | A healthy, constraint-controlled target-directionality solution exists | Required stress has no healthy field source, or requires pathological kinetic terms, singular sources, or NEC violation |
| **G4** | G3 passed, ADM constraint framework passed | A finite-width front evolves stably and matching conditions hold | Boundary/constraint/curvature singularities cannot be controlled |
| **G5** | R1 and R3 models mutually consistent | Low-energy effective action, degree-of-freedom spectrum, measure and topology definitions given | Only geometric degeneration obtained, with no consistent low-energy matter theory |
| **G6** | G4 and G5 pass within at least one explicit model | The chain of geodesics, material response, radiative transfer, and observer imaging closes | Only test rays / conceptual renderings under a prescribed background may be published; they must not be called DCC physical predictions |

---

# 11. Scientific Statement Boundaries in v1.3

## 11.1 Statements That May Be Made

- Excitation probabilities and energy deposition of fields/particles have been obtained on prescribed anisotropic backgrounds (MODEL RESULT);
- The static scalar bubble-wall benchmark has passed on a fixed Minkowski background (after G1, MODEL RESULT);
- 42.47 km/s has been normalized to $\eta_{\rm eff}\approx75$ using a phenomenological collective-coordinate model (reviewed; ESTABLISHED numerical consistency);
- Low-energy effective descriptions have been established separately for specified Models A/B/C, with their respective conditions of applicability (MODEL RESULT);
- Test rays and $R/T/A$ have been computed for a specified metric and specified $\sigma_s(\omega)$ (MODEL RESULT, labeled "prescribed-background test optics");
- $S^3\not\cong S^2\times S^1$, bounded-body projection has fiber degeneration at the boundary, and contraction causes $p_{\rm phys}\propto B^{-1}$ heating (ESTABLISHED);
- Under H2+H3, column density and optical depth are conserved (MODEL RESULT, analytic).

## 11.2 Statements That Must Not Be Made

1. Macroscopic three-dimensional objects have been proven to be smoothly reducible to two dimensions;
2. $\beta_C>1$ universally guarantees adiabatic adaptation; $\eta<1$ is a sufficient condition for material stability;
3. $B\to0$ automatically yields stable two-dimensional matter;
4. Fiber-bundle mapping is the only possible mapping (and the projection of a bounded object is not a fiber bundle at all);
5. A reduced object has 2.3% absorptance, or is a "nearly invisible phantom membrane," or is "mirror-like/opaque" — **until a self-consistent $\sigma_s(\omega)$ is available, both the transparent and the opaque directions are prohibited**;
6. Under the premise of "unchanged projected area," the noncovalent interaction network can be preserved (N2 provides the quantitative falsification with $E_F\approx23\ {\rm MeV}$ and $P_{2D}\approx3\times10^{15}\ {\rm J/m^2}$);
7. 42.47 km/s is a theoretical prediction;
8. Passing the P1 static wall implies that DCC dynamic geometry has passed;
9. Finite-thickness compactification equals a macroscopic object being smoothly flattened;
10. A reduction in the number of coordinate modes equals the disappearance of physical degrees of freedom.

---

# 12. Current Decisions and Near-Term Execution List

## 12.1 Decision Recommendations (Six Items)

1. **Accept the six corrections from v1.2 and the numerical revision $\eta_{\rm eff}\approx75$**; downgrade the corresponding v1.1 conclusions according to Appendix A; this v1.3 supersedes v1.2 as the execution baseline.
2. **Execute G0 first (1–2 days, pure analysis)** before deciding the scale of R1's resource commitment. Rationale: if G0's conclusion (atoms are necessarily destroyed at fixed area) is confirmed by independent review, R1's "bound-state survival" question has no solution at human-body scale, and the research focus should shift to the area-expansion branch or the particle-number-nonconservation branch — **this directional choice must be settled before writing code**.
3. **The three G1 closeout items proceed in parallel with G0** (they are mutually independent).
4. **R1 and R2-A proceed in parallel**, but R2-A's stress budget may only be closed after R2-D (redshift heating) provides $p_z(B)$.
5. **R5 may be developed in parallel**, but its products must all be labeled "prescribed-background test optics," and until the self-consistent $\sigma_s(\omega)$ calculation is complete, any visibility/appearance conclusion — including both "transparent" and "opaque" — is prohibited.
6. **The highest verdict principle is unchanged**: the goal is not to make some prescribed $B(t,x)$ look like two-dimensional reduction in images, but to prove that geometry, matter, interactions, energy–momentum, and observer measurements can coexist within one self-consistent set of equations. If it fails, the failure itself is a valid result.

## 12.2 Sprint 0: Freeze, Corrections, and G0 (the only mandatory item at this stage)

- [ ] **G0: implement `src/g0_analytic/scale_budget.py` and pass all four unit tests**
- [ ] **G0: two people independently recompute $E_F$, $P_{2D}$, $A_{\min}$, $\tau$ (relative error $<5\%$), and register PASS / NO-GO**
- [ ] Declare the research branch based on the G0 result (fixed area / area expansion / particle-number nonconservation) and write it into the assumption table at the start of the document
- [ ] Revise P1b: 42.47 km/s corresponds to $\eta_{\rm eff}\approx75$; add notes on units and on $F_{\rm drive}$ and $\sigma_w$
- [ ] Add a third spatial resolution to P1a and compute the observed order $p$
- [ ] Independently check the analytic integral for $\sigma_w=0.942$
- [ ] Freeze the P1 solver version, parameters, logs, and baseline outputs
- [ ] Change the universal adiabatic threshold $\beta_C>1$ into an assumption awaiting verification (completed in this document; synchronize to code comments and configuration)
- [ ] Correct the fiber-bundle topology statement and the density-integration measure (completed in Chapter 5 of this document)
- [ ] Downgrade 2.3% absorption to a graphene-like Dirac sheet benchmark and remove it from all default parameters
- [ ] Delete all statements presenting the "nearly invisible phantom membrane" as a universal conclusion
- [ ] Terminology replacement throughout: "weak force" → "noncovalent / soft interaction"

## 12.3 Sprint 1: R1 Minimal Matter Models (After G0)

- [ ] Build a free-scalar-field mode solver on an anisotropic background (R1-1)
- [ ] Verify the $B=1$ three-dimensional baseline and the adiabatic limit
- [ ] **Implement and reproduce the Lewis–Riesenfeld analytic solution of the moving infinite deep well (mandatory, G2 prerequisite)**
- [ ] Kibble–Zurek excitation-density estimate (G2 prerequisite)
- [ ] Scan $B(t)$ and the contraction rate, computing the instantaneous energy spectrum and $\epsilon_{mn}$
- [ ] Directly solve the time evolution and compute excitation probabilities and energy deposition
- [ ] Form conclusions according to the four categories A/B/C/D

## 12.4 Sprint 2: R2 Homogeneous D3 Forward Solution

- [ ] Derive the Einstein, scalar, and Maxwell equations and $dF=0$ independently from the action
- [ ] Independently derive the Maxwell stress tensor and check the P0 signs
- [ ] **Execute §4.4 check ①: the factor $3/2$ in the $h=0$ limit**
- [ ] **Execute §4.4 check ②: the NEC criterion (may directly yield a D3 NO-GO)**
- [ ] Derive all Bianchi-I component equations, implement the ODE solver, and monitor the Hamiltonian constraint
- [ ] **R2-D: provide the $p_z(B)$ curve and close the stress budget**
- [ ] Scan $Z(\phi)$, $V(\phi)$, and initial data; assess curvature invariants and linear-perturbation stability

## 12.5 Sprint 3: R3 Geometry and Effective Theory

- [ ] Implement Models A/B/C separately and give each a low-energy effective action
- [ ] Derive the KK / bound-state spectra and explicitly verify the low-energy cutoff condition
- [ ] Give the correct fiber-bundle data (if used) and characterize the fiber-degeneration set of $B^3\to D^2$
- [ ] Compute $\Sigma$ with the correct proper-volume measure and check it against G0 column-density conservation
- [ ] Give a quantitative estimate of front/back surface gluing under periodization

## 12.6 Sprint 4: R4 / R5

- [ ] Construct a finite-thickness front and match inner/outer regions, passing the ADM constraint-preservation tests
- [ ] Integrate null geodesics along observer worldlines
- [ ] Compute $R,T,A$ with a self-consistent $\sigma_s(\omega)$ (defaulting to $\pi\alpha$ prohibited)
- [ ] Solve radiative transfer and obtain the imaging PSF
- [ ] Generate observer views with complete assumption labels, all marked "prescribed-background test optics"

---

# Appendix A: Sentence-by-Sentence Revision Comparison Table, v1.1 → v1.3 (S1–S15)

| # | Original v1.1 statement (excerpt) | Disposition | Location in v1.3 |
|---|---|---|---|
| S1 | "When $\eta\ge1$ compression is too fast and the material structure is torn apart; when $\eta<1$ matter evolves adiabatically into the two-dimensional eigenstate" | Downgraded | §2.1: $\eta_{\rm rough}$ is only a screening quantity; the criterion is replaced by $\epsilon_{mn}$, with separate branches for gap closing (Kibble–Zurek) and gapless systems (Landau–Zener) |
| S2 | "$\eta<1$ for all components simultaneously is the prerequisite for smooth two-dimensional reduction of macroscopic structure" | Removed | §2.1(a): replaced by "each sector gives its own excitation probability and energy deposition; no single threshold constitutes a premise" |
| S3 | "Legal parameter space $\beta_C>1$ (guarantees adiabaticity); illegal $\beta_C\le1$ (matter is destroyed)" | Removed | §2.3: $\beta_C$ has no universal threshold; scan $(\beta_C,t_0,\Delta E(a_z))$ model by model |
| S4 | "$p_z^{\min}=2\pi/L_z$; the smaller $L_z$, the easier to satisfy $\eta<1$, and the destruction branch closes" | Rewritten | §2.4: only Model C has a discrete KK spectrum; Model A has no $p_z^{\min}$; moreover compression does work on matter via $p_{\rm phys}\propto1/B$, which must be counted as heating |
| S5 | "To maintain these force networks, the compact-dimension radius $R_z$ must satisfy $R_z\gtrsim5$ Å" | Removed | §1.5 terminology table + §8.3 prohibition: no topological lower bound; bond stability is decided by the Hamiltonian spectrum in R1-3 |
| S6 | "$\mathcal M_3=\mathcal B_2\times S^1$", "the overall topology is $S^2\times S^1$" | Removed | §5.1(a)(b): $S^3\not\cong S^2\times S^1$; Hopf bundle $c_1=\pm1$; the base space should be $D^2$; no global structure may be written before $E,B$, fiber, and transition functions are given |
| S7 | "$\Phi$ is a fiber-bundle projection … continuous manifold deformation, satisfies smoothness" | Downgraded to OPEN | §5.1(c)(d): the bounded-body map $\Phi:B^3\to D^2$ has fiber degeneration at the boundary and is not a fiber bundle; periodization glues front and back surfaces |
| S8 | "The compactification fiber-bundle mapping is the uniquely self-consistent mathematical form" | Removed | §5.3: replaced by separate discussion of Models A/B/C plus model-selection rationale (acceptance requirement of §8.10) |
| S9 | "Areal density $\sigma(x,y)=\int\rho\,dz\approx\rho(x,y,0)L_z$" | Rewritten | §5.4: $\Sigma=\int\rho\sqrt{g_{zz}}\,dz$, with the definition of $\rho$ and the slice volume element stated; $\rho$ may not be assumed approximately constant along $z$ |
| S10 | "The universal absorptance in the monolayer limit is about $\pi\alpha\approx2.3\%$" | Downgraded | §6.4: graphene-type Dirac monolayer benchmark with six premises; in general $\sigma_s(\omega)$ is the input |
| S11 | "The object appears as an ultrathin film / two-dimensional electron gas" (as an established conclusion) | Conditionalized | §2.6: valid only under specified Model B/C and specified material response |
| S12 | "The visual model is an independent branch, not blocked by D3, and can proceed in parallel with D3" | Conditionalized | §6.7: may be developed in parallel, but products may only be labeled "prescribed-background test optics" and must not be called DCC observational predictions |
| S13 | "D3 does not constitute a blocking item for the visual model" | Retained with annotation | §6.7: does not block rendering-pipeline development, but blocks any statement at the "physical prediction" level |
| S14 | Status table "mapping relationship: complete (derivation)" | Downgraded | §0.3 and the start of Chapter 5: changed to **OPEN** (topological errors remain to be corrected) |
| S15 | Implicit assumption "unchanged projected area" | Made explicit | §1.1 assumption table H2/H3; its mutual exclusivity with "atom survival" is accounted for by G0 in Chapter 3 |

---

# Appendix B: Index of New Issues N1–N5

| No. | Issue | Conclusion | Evidence level | Location |
|---|---|---|---|---|
| N1 | Areal-density conservation ⇒ invariant optical depth | $\tau=\sigma_{\rm eff}N_s$; under fixed-area compression $N_s$ is invariant ⇒ $\tau$ is invariant; "thinner means transparent" is a faulty inference; the zeroth-order plasma estimate points in the opposite direction (mirror-like) | MODEL RESULT | §3.5, §6.7 |
| N2 | Degeneracy pressure and energy budget of fixed-area two-dimensional reduction | $d_\parallel=15.4\ {\rm fm}$, $E_F\approx23\ {\rm MeV}$, $E_{2D}\approx6.3\times10^{15}\ {\rm J}$, $P_{2D}\approx3\times10^{15}\ {\rm J/m^2}$ ⇒ "fixed area + atom survival" is mutually exclusive; $A_{\min}=380\ {\rm km^2}$ per person | MODEL RESULT (G0 gate) | §0.2, §3.3, §3.4 |
| N3 | The $z$-projection of a bounded object is not a fiber bundle | Fibers degenerate on $\partial D^2$; $z\sim z+L_z$ glues the front and back surfaces | ESTABLISHED (mathematics) | §5.1(c)(d), §8.10 |
| N4 | Momentum redshift in the contraction direction ⇒ anisotropic heating | $p_{\rm phys}=p_z/B$, nonrelativistically $E_z\propto B^{-2}$; must be included in the D3 stress budget | ESTABLISHED (Bianchi-I geodesics) | §2.5, §4.5, §8.8 |
| N5 | Terminology and order-of-magnitude errors | "Weak force" should be renamed noncovalent / soft interaction; van der Waals forces have an $r^{-6}$ long tail with no hard cutoff and hydrogen bonds are 1.5–2.5 Å ⇒ $R_z\gtrsim5$ Å has no basis | ESTABLISHED | §1.5, §8.3 |

**Additional order-of-magnitude finding (incorporated into the G2 prerequisites):** at 42.47 km/s, $\eta_{\rm rough}$ is 0.039 for 1s electrons, 0.056 for chemical bonds, and 0.028 for nucleons, while **the phonon sector reaches 0.56** — the first to fail is the lattice (nonadiabatic heating), not "atoms being torn apart."

---

# Appendix C: Numerical Verification Records

| Item | Calculation | Result | Verdict |
|---|---|---|---|
| $\beta_{\rm target}$ | $42.47/299792.458$ | $1.4166\times10^{-4}$ | Consistent with v1.2 |
| $\eta_{\rm target}$ | $0.0106/1.4166\times10^{-4}$ | $74.8$ | $\eta_{\rm eff}\approx75$ holds; $\eta\approx1.0$ is void |
| $N_s$ | $70/(10\times1.6605\times10^{-27}\times1)$ | $4.22\times10^{27}\ {\rm m^{-2}}$ | Pass |
| $d_\parallel$ | $N_s^{-1/2}$ | $1.54\times10^{-14}\ {\rm m}$ | Pass ($2.9\times10^{-4}a_0$) |
| $k_F$ | $\sqrt{2\pi\times2.2\times10^{27}}$ | $1.18\times10^{14}\ {\rm m^{-1}}$ | Pass |
| $\hbar k_F c$ | $1.0546\times10^{-34}\times1.176\times10^{14}\times2.998\times10^{8}$ | $3.72\times10^{-12}\ {\rm J}=23.2\ {\rm MeV}$ | Pass (relativistic dispersion must be used) |
| $E_{2D}$ | $2.2\times10^{27}\times\frac34\times23.2\ {\rm MeV}$ | $6.1\times10^{15}\ {\rm J}\approx1.5\ {\rm Mt}$ | Pass |
| $P_{2D}$ | $E_{2D}/2$ | $3.1\times10^{15}\ {\rm J/m^2}$ | Pass |
| $A_{\min}$ | $4.22\times10^{27}\times(3\times10^{-10})^2$ | $3.8\times10^{8}\ {\rm m^2}$ | Pass ($380\ {\rm km^2}$) |
| $\omega_p^{\rm 2D}$ | $\sqrt{n_{2D}e^2k_F/(2\varepsilon_0 m_e)}$ | $2.03\times10^{22}\ {\rm rad/s}$ ($\hbar\omega_p\approx13.4\ {\rm MeV}$) | Pass (about 2 MeV after relativistic correction, conclusion unchanged) |
| $\tau_T$ | $2.2\times10^{27}\times6.65\times10^{-29}$ | $0.146$ | Pass |
| Stress-budget $h=0$ coefficient | Maxwell gives $3\rho_B$; inverse problem gives $2\gamma^2/\kappa$; $\rho_B=\gamma^2/\kappa$ | Factor of $3/2$ difference | **Failed**; listed as G3 prerequisite check ① |
| $\eta_{\rm rough}$ (phonon) | $\hbar v/L$, $L=1$ nm, $\Delta E=0.05$ eV | $0.56$ | The lattice fails first |

---

# Appendix D: Version Change Log

| Version | Date | Main changes |
|---|---|---|
| v1.1 | — | Established the four-layer roadmap (physical boundary / D1–D3 / compactification fiber-bundle mapping / visual model), removing preset descriptive claims about visual appearance |
| v1.2 | 2026-11-20 | Third-party review deliverable: six substantive corrections, four-category model classification, G1–G6 stage gates, five-level evidence tagging, R1–R5 taskization |
| **v1.3** | 2026-11-20 | Adopted all six v1.2 corrections; **added the G0 analytic order-of-magnitude gate** (the hard dilemma that atoms are necessarily destroyed at fixed area); incorporated N1–N5; added the R2-D redshift-heating task; expanded G2/G3 prerequisite checks; downgraded the mapping-layer status from "completed" to OPEN; removed $\beta_C>1$, the $\eta<1$ dichotomy, $R_z\gtrsim5$ Å, $S^2\times S^1$, $p_z^{\min}$, the "phantom membrane," and universal 2.3% absorption; corrected $\eta_{\rm eff}\approx75$; updated the dependency graph and stage gates; appended the S1–S15 sentence-by-sentence comparison and numerical verification records |

---

**Status of this file:** execution baseline (supersedes v1.2).
**Next step:** execute Sprint 0, with G0 as the sole highest priority; only after the G0 verdict is registered may the scale of R1's commitment and the choice of branch be decided.

---

Content generated by AI.
