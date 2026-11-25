> This report integrates all previous derivations and presents a complete research roadmap for the "smooth two-dimensional reduction" of three-dimensional macroscopic objects.
> **v1.1 (2026-11-20)**: Completed the four unfinished modules — D3 endogenous dynamics (stress-budget inverse problem + three-way scaling + Go/No-Go), light–matter coupling QED (universal monolayer absorption of 2.3%), two-dimensional radiative transfer (Kirchhoff surface source), and the human-eye visibility criterion (nearly invisible phantom membrane); and interfaced with the first-round results of the DCC main chain P0–P4 (D2 achieved, optical criteria quantified, mode freeze-out numbers).
> The roadmap consists of four layers: the bottom layer is the **physical boundary**, which determines under what extra-dimensional thickness $L_z$ and what contraction rate $\beta_C$ macroscopic structures can be smoothly reduced to two dimensions; above it is the **theoretical closure D1–D3**, which asks whether the contraction law can be derived endogenously from more fundamental dynamics; above that is the **compactification fiber-bundle mapping**, which gives the strict mapping from three-dimensional points to two dimensions and reasons about the reduced structure accordingly; the top layer is the **physical model of visual presentation**, which establishes the mathematical and physical quantities that determine visual signals and imaging.
> The principle throughout is that the actual physical appearance after reduction and the human-eye visualization effect are uniquely determined by the underlying mapping relationship and the solutions of the equations of optics, radiative transfer, and so on; this report only gives the equations and criteria that determine them, and makes no preset assumptions about their final presented form.

---

## 0. Document Nature and Execution Status (Read This Section First)

**This document is a research program (planning), not an execution report.**

| Item | Status |
|---|---|
| Program document (the modules/criteria/methods of this file) | **Complete** (v1.1: all modules have content, quantitative criteria, and Go/No-Go) |
| R1 contraction-law inverse problem and stress budget | **Not started** |
| R2 stress-source physics (material realization of the smooth window) | **Not started** |
| R3 matter 2D-reduction transport (atoms/electrons/chemical bonds) | **Not started** |
| R4 macroscopic geometric wrapping (2+1 axisymmetric York initial data) | **Not started** (prerequisite: DCC main-chain P2-C2 is also not started) |
| R5 optical acceptance and rendered imagery | **Not started** |
| D3 self-consistent forward solution (core task of the program) | **Not started** (§3(iii) of this file gives only methods and criteria) |

**Therefore: this program does not constitute any conclusion that "two-dimensional reduction has been achieved/is achievable"** — what it answers is:
"to verify/falsify smooth two-dimensional reduction of macroscopic objects, what needs to be done in what order,
and with what criteria each step is judged." R1's three-way stress-budget scaling (§3(iii)) is currently the only completed
**analytical** work (the P2 magnetic configuration is too slow, the E-6 configuration is singular, and the smooth window remains to be constructed),
and its Go/No-Go is the first gate of the entire program, with the possibility of being falsified.

---

The module dependency relationships of the roadmap are as follows: the physical boundary layer (compactification framework, D2 power-law contraction, D1 adiabatic criterion, parameter scans) converges on the conditional conclusion of a "sci-fi boundary"; D3 endogenous dynamics is the only unfinished node in the boundary layer, responsible for upgrading the artificially prescribed contraction law into a theoretical necessity; the mapping-relationship module (compactification fiber-bundle mapping) lies below the theoretical closure and above the visual model, serving as the core link between the underlying physics and the top-level visuals; the visual model is an independent branch that relies only on the completed state of "matter already adiabatically reduced to two dimensions," is not blocked by D3, and can proceed in parallel with D3.

```
[Physical boundary] ─────────────────────────────────────┐
  │  Range of L_z, contraction rate β_C, adiabatic parameter η  │
  └──────────────────────────────────────────────────────┘
                           │
                           ▼
[Theoretical closure] ───────────────────────────────────┐
  │  D1: adiabatic criterion (complete)                        │
  │  D2: power-law background (complete)                       │
  │  D3: endogenous dynamics (incomplete, driven by modulus V(φ))│
  └──────────────────────────────────────────────────────┘
                           │
                           ▼
[Mapping relationship] ──────────────────────────────────┐  ← core module
  │  Compactification fiber-bundle mapping Φ(x,y,z) = (x,y; θ)  │
  │  Weak-force preservation: R_z ≳ 5 Å (local triviality)     │
  │  Effective 2D: R_z ≪ λ (global triviality)                  │
  │  Structural inference: z info encoded in θ; macroscopic      │
  │     resolvability judged by the diffraction limit           │
  └──────────────────────────────────────────────────────┘
                           │
                           ▼
[Visual model] ──────────────────────────────────────────┐
  │  Observer geometry + thin-film optical equations: R, T, δ    │
  │  Imaging and visualization: determined by R/T/δ, the          │
  │     diffraction limit, and radiative transfer equations,      │
  │     with no preset presentation form                         │
  └──────────────────────────────────────────────────────┘
```

The following table summarizes the current status of each module and the questions it can answer:

| Module | Status (v1.1 update) | What it can answer / what is missing |
|---|---|---|
| Compactification framework (phenomenological setting) | Conditional | $L_z$ extremely small but nonzero, defining "effective two dimensions" |
| D2 power-law contraction background $a_z(t)$ | Complete (artificially prescribed) | Gives $\beta_C$, $\eta \propto t^{-(\beta_C+1)}$ |
| D1 adiabatic criterion $\eta$ | Complete | Given $p_z$ and the compression rate, decides "conversion / destruction" |
| P3-C5/C5b parameter scan | Complete | Which components fall into the destruction / adaptation regions under $(L_z,\beta_C)$ |
| D3 endogenous dynamics | Framework complete (stress budget + three-way scaling + Go/No-Go; self-consistent forward solution not realized) | Inverse-problem formula $p_x{+}p_y{-}p_z=(2/\kappa)[\gamma^2-\gamma h-h^2/2]$; transverse saturation requirement; candidate-source verdict |
| Mapping relationship (compactification fiber-bundle mapping) | Complete (derivation) | Strict mapping from 3D points to 2D and the 2D-reduced structure (areal density, topology, resolvability criterion) |
| Observer geometry | Complete | View-angle-dependent optical visibility criterion (geometric optics) |
| Thin-film optics ($L_z\sim\text{nm}$) | Complete (equations) | Quantitative solution for reflection/transmission from $R,T,\delta$, with no preset appearance |
| Light–matter coupling QED | Complete (analytic) | Universal monolayer absorption $A=\pi\alpha\approx2.3\%$, $T\approx97.7\%$, $R\sim10^{-4}$; KK tower activated above the gap |
| Radiative transfer | Complete (2D Kirchhoff) | Surface source $j_\nu=A_\nu B_\nu(T_s)$; thermal emission $\approx2.3\%$ of a blackbody (weak thermal source) |
| Human-eye visualization | Complete (criteria) | Imaging chain + visibility verdict summary (nearly invisible phantom membrane) + exposure/persistence |

---

## II. Physical Boundary of Smooth 2D Reduction: $L_z$ and Contraction Rate

### (i) Core Criterion: the Adiabatic Parameter $\eta$

Whether a matter component is destroyed depends on the competition between the compression rate and that component's energy gap $\Delta E$. Define the adiabatic parameter:

$$\eta(t) = \frac{\hbar}{\Delta E}\left|\frac{\dot{a}_z(t)}{a_z(t)}\right|$$

When $\eta \ge 1$, compression is too fast and the material structure is torn apart (destruction region); when $\eta < 1$, matter evolves adiabatically into a two-dimensional eigenstate (smooth-conversion region). Having $\eta<1$ for all components simultaneously is the prerequisite for smooth two-dimensional reduction of macroscopic structure.

### (ii) Power-Law Contraction Law and Contraction Exponent $\beta_C$

Let the $z$-direction scale factor contract according to a power law:

$$a_z(t) = a_{z0}\left(\frac{t}{t_0}\right)^{-\beta_C},\quad \beta_C > 0$$

Substitution into the criterion gives $\eta(t) \propto t^{-(\beta_C+1)}$. To keep $\eta<1$ throughout a finite time interval, the contraction exponent $\beta_C$ must be sufficiently large (very fast early on, slowing later), or the initial time $t_0$ sufficiently early. In D2, this contraction law is an artificially prescribed phenomenological background.

### (iii) The Value of $L_z$: Effective 2D Rather Than $L_z = 0$

Physical two-dimensional reduction is not the mathematical singularity $L_z = 0$, but an "effectively two-dimensional" state in which $L_z$ is extremely small yet nonzero: when $L_z \ll$ the probe wavelength and the characteristic material scale, the quantized $z$-direction kinetic energy levels $\Delta E_z \sim \hbar^2/(m L_z^2)$ tend to infinity, all nonzero KK modes are frozen out, and the system effectively behaves as two-dimensional. Strict $L_z = 0$ would degenerate the metric and invalidate the framework, so it is physically unreachable.

The corresponding minimum momentum is $p_z^{\min} = 2\pi/L_z$: the smaller $L_z$, the larger $p_z^{\min}$, the easier it is to satisfy $\eta < 1$, and the destruction branch closes.

### (iv) Legal / Illegal Parameter Space (Sci-Fi Boundary)

- **Legal parameter space**: $\beta_C > 1$ (guarantees adiabaticity) and $L_z$ extremely small (on the order of nanometers or less, guaranteeing effective two-dimensionality) → smooth two-dimensional reduction.
- **Illegal parameter space**: $\beta_C \le 1$ (matter is destroyed); or macroscopic $L_z$ (degrading into an ordinary thin plate, not genuine two-dimensional reduction).

---

## III. Theoretical Closure: D1–D3 and Endogenous Dynamics

### (i) D1 Adiabatic Criterion (Complete)

Gives the definition of $\eta$ and the partition criterion; for given $L_z$ and $\beta_C$, it determines whether any component falls into the adaptation region or the destruction region. It is the criterion core of the entire roadmap.

### (ii) D2 Power-Law Contraction Background (Complete, Artificially Prescribed)

Prescribes the phenomenological contraction background $a_z(t) \propto t^{-\beta_C}$ and derives from it the power-law time dependence of $\eta$. Its self-consistency comes from treating $L_z$ and $\beta_C$ as external input parameters, not from experimental constraints on real extra dimensions.

### (iii) D3 Endogenous Dynamics (Completed in v1.1: Stress-Budget Method + Three-Way Scaling + Go/No-Go)

D3 must answer whether the power-law contraction law can be derived endogenously from more fundamental dynamical equations rather than inserted by hand. The theoretical paths include the **gravity side** (in the Kaluza–Klein framework, compact-dimension dynamics is controlled by the modulus field $\varphi$, whose potential $V(\varphi)$ determines the evolution of $a_z(t)$) and the **matter side** (the projection of the matter-field energy–momentum tensor along the compact dimension back-reacts on the modulus field, forming a self-consistent system). If D3 proves that a contraction law with $\beta_C > 1$ is the natural solution of some class of scalar-field potentials, then "smooth two-dimensional reduction" is upgraded from an artificial setting to a theoretical necessity. D3 does not constitute a blocking item for the visual model and can proceed in parallel with it.

**Completed in v1.1: the stress-budget inverse-problem method (interfacing with the P2 machine equation chain).**
The machine derivation of the DCC main chain (`DCC_sympy_derivation.py`, M/b JSON) has given the evolution equation in the collapse direction;
for the prescribed contraction law $a_z=C_0e^{-\gamma(t-t_0)}$ ($H_C\equiv-\gamma$, $\dot H_C=0$), the required anisotropic stress difference can be **algebraically inverted**
(the inverse problem is linear and requires no iteration):

$$p_x+p_y-p_z=\frac{2}{\kappa}\Big[\gamma^2-\frac{\gamma}{2}(H_A+H_B)-\tfrac12 H_AH_B\Big].$$

**Three-way scaling** (stress-budget table; $H_A=H_B\equiv h$):

| Configuration | Stress scaling | Contraction law | Smoothness criterion (S1–S4) | Verdict |
|---|---|---|---|---|
| P2 magnetic flux ($\rho_B$ independent of C, $f$=const) | $2\rho_B\propto(AB)^{-2}$ decaying | $H_C\to0$, $C\propto t^{\beta}$ power law | S1–S3 pass, timescale infeasible (macroscopic $4\times10^{12}t_0$) | **Too slow** |
| E-6 inhomogeneous flux ($f=QAB/(ZC)$) | $\rho_B=Q^2/(2ZC^2)$ diverges as $C\to0$ | $H_C$ diverges, singular at finite $t_c$ | S1/S4 fail | **Too violent (singular)** |
| **Smooth window (target of this section)** | bounded $\to 2\gamma^2/\kappa$ (as transverse saturation $h\to0$) | $C\propto e^{-\gamma t}$ exponential | S1–S4 can all pass (if a stress source exists) | **Target state** |

**Transverse saturation requirement** (key v1.1 finding): in the budget formula, the transverse expansion rate $h$ must tend to zero
(as $h\to0$ the required stress reduces to the constant $2\gamma^2/\kappa$, i.e., a "magnetic-type source with constant $Z$-direction tension density
$\rho_B=\gamma^2/\kappa$"); for $h\neq0$ the required stress decays with the opposite sign of $h$ —
**without transverse saturation, no bounded stress can realize smooth exponential contraction**. Transverse saturation is naturally consistent with the goal of "preserving the object's transverse dimensions" (the object is flattened rather than torn apart).

**Candidate stress sources** (to be judged in stage R2):
1. Flux constancy: after transverse saturation, $f=$const gives $\rho_B=$const — one must prove $h\to0$ is
   self-consistent (the P2 homogeneous run measured $H_A\propto t^{-2}\to0$, a favorable direction);
2. $Z(\varphi)$ rolling tune: scan the sign/magnitude of $\alpha$ so that $\rho_B$ grows to the target value during collapse;
3. Frozen-matter feedback: after the $p_z\neq0$ tower freezes out, $w_{\rm eff}$ changes (carried over from P3 §2).

**Go/No-Go criterion**: if one of the above candidates yields a
**complete self-consistent forward solution** with transverse saturation and constant $\rho_B=\gamma^2/\kappa$
(not a prescribed background) → D3 is closed and "smooth two-dimensional reduction" is upgraded to a theoretical necessity;
if all candidates fail → the program terminates at the "singular degeneration surface" statement (DCC roadmap §4.5).

---

## IV. Mapping Relationship: the Compactification Fiber-Bundle Mapping

The strict mapping from three-dimensional points to two dimensions is the core module connecting the underlying physics to the top-level visuals. Under the joint constraints of "effective two-dimensionalization," "smooth evolution," and "weak-force preservation," this mapping must mathematically be a **fiber bundle mapping (Fiber Bundle Mapping)**.

### (i) Core Mapping Relationship: the Compactification Fiber-Bundle Mapping

Within the compactification framework, three-dimensional space $\mathcal{M}_3$ is not simply "flattened"; rather, it is projected by a mapping $\Phi$ onto a two-dimensional base space $\mathcal{B}_2$, while each point carries a compact fiber $S^1$.

**1. Mathematical definition**

Let the three-dimensional spacetime manifold be $\mathcal{M}_3 = \mathcal{B}_2 \times S^1$, where $S^1$ is a circle of radius $R_z = L_z / 2\pi$. The mapping $\Phi: \mathcal{M}_3 \to \mathcal{B}_2$ is defined as:

$$\Phi(x, y, z) = (x, y)$$

where $z \in [0, L_z)$ is the coordinate on the compact dimension.

**2. Topological constraint for weak-force preservation**

The interaction range of weak interactions (such as van der Waals forces and hydrogen bonds) is about $3\text{–}5\ \text{Å}$. To maintain these force networks, the compact-dimension radius $R_z$ must satisfy:

$$R_z \gtrsim 5\ \text{Å}$$

This means that the mapping $\Phi$ must be **locally trivial (Locally Trivial)** at the microscopic level: within any neighborhood larger than $R_z$, $\Phi$ is homeomorphic to the product map $\text{id}_{\mathcal{B}_2} \times \text{id}_{S^1}$, thereby ensuring that the weak-force network evolves continuously along the compact dimension without breaking.

**3. Quantum constraint for effective two-dimensionalization**

When $R_z$ is compressed to the nanometer scale ($R_z \ll \lambda_{\text{visible}}$), the quantized $z$-direction kinetic energy levels $\Delta E_z \sim \hbar^2/(m R_z^2)$ tend to infinity and all nonzero KK modes are frozen out. At this point the mapping $\Phi$ appears **globally trivial (Globally Trivial)** at macroscopic probe scales, and the system effectively behaves as two-dimensional.

### (ii) Structural Inference: Information Encoding and Resolvability Criterion

Based on the mapping relationship above, the structural features after two-dimensional reduction can be rigorously derived. Only the physical quantities and criteria that determine the structure are given here, with no preset assumption about their final presentation to the human eye.

**1. Information encoding and resolvability criterion**

Structural information originally along the $z$ direction (such as the three-dimensional configuration of molecules) is encoded into the fiber coordinate $\theta = z/R_z \in [0, 2\pi)$. Whether this $z$-direction structure can be resolved under macroscopic probing is determined by the diffraction-limit criterion of the imaging system: when the separation $d$ of adjacent structures in the imaging plane satisfies $d \ll \lambda$ (the operating wavelength), they fall below the diffraction limit and cannot be resolved by that imaging system; whether they can be resolved and with what signal they appear depends on the solutions of the optical and imaging equations of Chapter V below, not on any preset appearance.

**2. Density distribution**

The areal density $\sigma(x, y)$ after two-dimensional reduction is obtained by integrating the original three-dimensional density $\rho(x, y, z)$ along the fiber:

$$\sigma(x, y) = \int_0^{L_z} \rho(x, y, z)\, dz \approx \rho(x, y, 0)\cdot L_z$$

Since $L_z$ is extremely small but nonzero, $\sigma(x, y)$ is finite and no density explosion such as that of orthogonal projection (Model A) occurs.

**3. Topological properties**

The mapping $\Phi$ is a fiber-bundle projection whose topological properties are determined by the topology of the original three-dimensional manifold. For example, after a three-dimensional sphere $S^3$ is reduced to two dimensions, its base space $\mathcal{B}_2$ is homeomorphic to the two-dimensional sphere $S^2$, the fiber is $S^1$, and the overall topology is $S^2 \times S^1$. This is completely different from the topological tearing in area-preserving unfolding (Model B).

### (iii) Comparison of the Three Mapping Models and Their Physical Self-Consistency

Under the joint assumptions of "effective two-dimensionalization," "smooth two-dimensional reduction," and "weak-force preservation," the three candidate mappings can be checked one by one. The comparison examines only the mathematical and physical properties of the mappings themselves (bijectivity, continuity of the force network, topological continuity, and the macroscopic resolvability criterion for $z$ information), without presupposing anything about their visual appearance.

| Feature | Model A: orthogonal projection | Model B: area-preserving unfolding | Model C: adiabatic compactification (fiber-bundle mapping) |
|---|---|---|---|
| **Mathematical form** | $\Phi(x,y,z)=(x,y)$ | $\Phi:\mathbb{R}^3\to\mathbb{R}^2$ (bijective) | $\Phi(x,y,z)=(x,y;\theta)$ |
| **Overlap** | inevitable overlap | no overlap | no overlap (distinguished by $\theta$) |
| **Fate of $z$ information** | discarded (information destroyed) | spread entirely into the base space | encoded in the fiber $\theta$ |
| **Weak forces** | network breaks (rejected) | breaks at cuts (tearing) | evolves continuously on the fiber (preserved) |
| **Smoothness** | contains overlap, not satisfied | requires topological tearing, not satisfied | continuous manifold deformation, satisfied |
| **Macroscopic resolvability of $z$ information** | none (information destroyed) | spread into base space, detectable in principle | encoded in $\theta$, resolvability decided by the diffraction-limit criterion |
| **Physical self-consistency** | low | medium (requires an extra expansion mechanism) | high (naturally derived from compactification) |

- **Weak-force preservation rejects Model A**: orthogonal projection discards the $z$ coordinate, so molecular pairs originally bound along $z$ by weak forces either overlap (Coulomb-repulsion explosion) or are pulled apart; the weak-force network necessarily breaks.
- **Smooth two-dimensional reduction rejects Model B**: area-preserving unfolding requires introducing "seams" (Seams), corresponding to macroscopic rupture of chemical bonds and the weak-force network; it also requires expansion in the $x,y$ directions to accommodate $z$ information, which is energetically contradictory to the adiabatic evolution of $L_z$ contraction.
- **Effective two-dimensionalization + weak-force preservation fits Model C**: information is encoded in $\theta$, the weak-force network evolves continuously along the compact dimension; for extremely small $R_z$ the object is macroscopically effectively two-dimensional, and the resolvability of $z$ information is left to the diffraction-limit criterion.

### (iv) Conclusion: the Mapping Relationship Determines Structure

Under the joint constraints of "effective two-dimensionalization," "smooth two-dimensional reduction," and "weak-force preservation," **the compactification fiber-bundle mapping $\Phi(x,y,z) = (x, y; \theta)$ is the unique self-consistent mathematical form**. It guarantees both microscopic continuity of the weak-force network (via encoding in the fiber coordinate $\theta$) and macroscopic effective two-dimensionalization (via freezing of KK modes when $R_z \ll \lambda$). What follows rigorously are the structural quantities of the reduced object — the areal density $\sigma(x,y)$, the fiber topology $S^2\times S^1$, and the diffraction-limit criterion for whether $z$-direction structure can be resolved. As for the final presentation of these structures to the human eye, that is determined by the optical and imaging equations of the next chapter; this chapter makes no preset assumption about visual appearance.

---

## V. Physical Model of Visual Presentation

Between "matter has been adiabatically reduced to two dimensions" and "what signal the observer receives" lie the physical equations of optics and radiative transfer. This chapter does not presuppose what a two-dimensional object "looks like"; it only establishes the equations and criteria that determine visual signals: given the structural quantities supplied by the mapping relationship ($\sigma(x,y)$, fiber scale $R_z$, $\theta$ encoding) and the incident/radiative conditions, the visual signal is the solution of these equations, not a pre-agreed picture. Its microstructural basis is precisely the fiber-bundle mapping of Chapter IV — weak forces remain intact along the compact dimension, so the reduced object retains structural quantities instead of collapsing into a structureless two-dimensional distribution.

### (i) Observer Geometry: View-Angle-Dependent Visibility Criterion

In pure geometric optics, a strictly zero-thickness plane has no reflection, no refraction, and no emission; light passes straight through and it is optically invisible. A finite but extremely small thickness makes it an ultrathin film, and visibility becomes a function of the observation geometry (incidence angle, grazing angle). What this layer provides is a geometric criterion for "how much light participates in the interaction at a given viewing angle"; it contains no preset assumption about color or form.

### (ii) Thin-Film Optics: Quantitative Equations for Reflectance and Transmittance

When $L_z$ is compressed to the nanometer scale, the object behaves as an ultrathin film / two-dimensional electron gas. Its normal-incidence optical response is given quantitatively by the thin-film equations:

$$R = \left|\frac{r_{01} + r_{12} e^{-2i\delta}}{1 + r_{01} r_{12} e^{-2i\delta}}\right|^2,\quad T = 1 - R - A,\quad \delta = \frac{2\pi n L_z}{\lambda}$$

where $\delta$ is the phase thickness, $n,\kappa$ are the film's refractive index and extinction coefficient, and $r_{ij}$ are Fresnel coefficients. In the monolayer limit the universal absorptance is about $\pi\alpha \approx 2.3\%$ (determined by the fine-structure constant $\alpha$). The conclusion here is a quantitative solution for $R,T,A$ as functions of $(L_z,\lambda,\theta,n,\kappa)$: different thicknesses, wavelengths, and viewing angles yield the corresponding reflected/transmitted power distributions. What is given is the partition of electromagnetic energy, not "color" or "pattern" — the latter requires the imaging and human-eye response of the next chapter and is determined by these quantities, not preset.

### (iii) Light–Matter Coupling and Radiative Transfer (Completed in v1.1)

**1. Light–matter coupling: universal 2D conductivity and absorption (analytic QED result)**

If the carriers of the reduced matter retain Dirac-type dispersion (the $p_z=0$ sector), their two-dimensional conductivity is given universally by QED as $\sigma_{2D}=\alpha/(Z_0)$ ($Z_0=377\,\Omega$ is the vacuum impedance), corresponding to
**universal monolayer absorption**:

$$A=\pi\alpha\approx2.29\%,\qquad T=\frac{1}{1+\tfrac12\pi\alpha}\approx97.7\%,\qquad
R\approx\Big(\frac{\tfrac12\pi\alpha}{1+\tfrac12\pi\alpha}\Big)^2\approx1.3\times10^{-4}.$$

That is, a smoothly two-dimensionally reduced macroscopic object is a **nearly transparent, nearly nonreflective "phantom membrane"** — the optical contrast is only
~2.3% (the famous result for graphene monolayers applies directly here). In the frequency range above the gap ($2\Delta m\sim2|p_z|/C$),
absorption is activated according to the KK tower — the gap separates "which frequencies are visible" from "which have decoupled."

**2. Two-dimensional thermal emission and radiative transfer (the Kirchhoff connection)**

The radiative transfer equation along the normal through the thin film is:
$$\frac{dI_\nu}{ds}=-\alpha_\nu I_\nu+j_\nu,\qquad j_\nu^{2D}=A_\nu\,B_\nu(T_s)\ \delta(s)$$
(Kirchhoff: emissivity = absorptivity; $\delta(s)$ denotes a surface source). The thermal emission surface brightness of the reduced object at temperature $T_s$
is $A_\nu B_\nu(T_s)$ — if $A_\nu\approx\pi\alpha$ is frequency-flat, the total emission is
$P/A\approx\pi\alpha\,\sigma_{SB}T_s^4\approx2.3\%$ of a blackbody at the same temperature — **a weak thermal source**.

**3. Visibility verdict (carried over from review breakpoint 4)**

- Reflection contrast: $R\sim10^{-4}$ (near zero) — a slight "dimming silhouette" against a bright background;
- Thermal-emission contrast: $2.3\%$ (same temperature) — a weak hot spot against a dark background (detectable in infrared, nearly invisible in visible light);
- Exposure/persistence: relativistic-group event duration 0.0425 s < human-eye integration 0.05–0.1 s → flicker;
  the low-speed group's 300 s is a phenomenological assumption (P1b FAIL archived permanently);
- **Conclusion**: a smoothly two-dimensionally reduced macroscopic object is **optically nearly invisible** — this is itself
  the most important quantitative conclusion of this section (more physically informative than "what it looks like");
  making the object "visible" requires scattering contrast under external illumination or active illumination — handed over to the imaging module for parameterization.

### (iv) Human-Eye Visualization: Imaging Criteria and Visibility Conclusion (Completed in v1.1)

Imaging chain: incident light field → $\text{PSF}$ convolution → retinal irradiance → 1-arcminute sampling:

$$E_{\text{retina}}(x',y') = \iint \text{PSF}(x'-\xi,\,y'-\eta)\, E_{\text{obj}}(\xi,\eta)\, d\xi\, d\eta$$

Details below the diffraction limit are smoothed out here — combined with the diffraction-limit criterion of Chapter IV, the "$z$ information" retained by the reduced object
cannot in principle be resolved by the human eye (encoded in the fiber coordinate $\theta$).

**Summary of explicit visibility/invisibility criteria (carried over from v2.6 review breakpoint 4)**:

| Criterion | Quantitative conclusion |
|---|---|
| Optically unresolved (third dimension) | $L_z\le\lambda_{\rm obs}$: attainable for micrometer-scale initial thickness (t/t₀~4, exponential background); not attained for macroscopic initial thickness (7 orders of magnitude short, power law) |
| Optically invisible (object itself) | $A\approx2.3\%$, $R\sim10^{-4}$, thermal emission $2.3\%$ of a blackbody — nearly invisible "phantom membrane" |
| Exposure/persistence | Relativistic group 0.0425 s < 0.05–0.1 s → flicker does not constitute a scene; low-speed group 300 s is a phenomenological assumption (P1b FAIL) |
| Surface brightness | $2.3\%\times\sigma_{SB}T^4$ (same temperature) — weak thermal source; active illumination or temperature contrast is required for imaging |

**Statement boundary** (following the sayable/unsayable list in §5 of the DCC main-chain P4 report):
"Sayable" — the apparent image reconstructed from geodesics plus radiative transfer under a prescribed contraction background (D2 level) and the flat-plate approximation;
each frame is labeled with the effective region / assumption level. "Unsayable" — model predictions of the appearance of a two-dimensionally reduced macroscopic object
(D3 not achieved + macroscopic optical criteria not closed + matter transport unverified).

### (v) Methodological Note for This Chapter

As in the previous chapters, this chapter delivers only "the equations and criteria that determine vision"; the deliverables are $R,T,A(\lambda,\theta,L_z)$, the radiative-transfer solution, and the imaging integral, not a verbal imagination of the appearance of a two-dimensional object. What signal actually appears after reduction is the solution of the above equations for given $(L_z,\beta_C,\rho,\theta,\text{viewing angle})$; until the light–matter coupling and radiative-transfer modules are completed, this solution is incomplete, and therefore this report explicitly makes no predictive description of the final visual form.

---

## VI. Current Conclusions and Remaining Work

The roadmap has now formed a complete four-layer framework: the **physical boundary** gives a conditional conclusion — if $L_z$ is sufficiently small and $\beta_C$ sufficiently large, a three-dimensional macroscopic structure can be smoothly reduced to two dimensions; in the **theoretical closure**, D1 and D2 are complete, and D3 endogenous dynamics has established the stress-budget method (inverse-problem formula, three-way scaling, transverse-saturation requirement, candidate sources, and Go/No-Go), with the self-consistent forward solution remaining as the core task; the **mapping relationship** establishes the compactification fiber-bundle mapping $\Phi(x,y,z)=(x,y;\theta)$ as the unique self-consistent mapping and rigorously gives the structural quantities of reduction (areal density, topology, diffraction-limit resolvability criterion); the **visual model** has completed all equation modules (observer geometry, thin-film optics, QED universal absorption $A=\pi\alpha\approx2.3\%$, 2D Kirchhoff radiative transfer, imaging integral, and visibility verdict), and the equation system for visual signals **is closed**.

**The most important quantitative conclusion of v1.1**: a smoothly two-dimensionally reduced macroscopic object is a **nearly invisible phantom membrane** — monolayer absorption $2.3\%$, reflection $\sim10^{-4}$, thermal emission $2.3\%$ of a blackbody — it hardly changes the appearance of the world optically; the optical unresolvability of the third dimension is attainable for **micrometer-scale initial thickness** (exponential contraction background, $t/t_0\sim4$), but unattainable under a power law for **macroscopic initial thickness** (7 orders of magnitude short) and can only be achieved after D3 realizes an endogenous solution with $C$ going to 0.

Three remaining tasks, mutually independent:

1. **Complete the D3 self-consistent forward solution** (stress budget → candidate sources → forward evolution; the Go/No-Go framework is in place) — upgrade the exponential contraction law from "stress-budget feasible" to "dynamically realized";
2. **Matter 2D-reduction transport** (smooth evolution spectra of atoms/electrons/chemical bonds in the collapse direction) — the criterion for the integrity of object structure (the hardest physical problem in the program);
3. **Macroscopic geometric wrapping** (2+1 axisymmetric York initial data, shared with DCC main-chain P2-C2) — finite-region geometry and boundaries.

All three can proceed in parallel. The mapping-relationship module has already provided the structural-quantity basis for the visual model; progress on D3, matter transport, and geometric wrapping does not change the conclusions of the mapping layer or the optical equations.

**Interface with the DCC main chain**: this program corresponds to the D5 stage after DCC roadmap v2.6; prerequisite = P2 reaching D2 (already satisfied); the D3 self-consistent forward solution shares the machine equation chain with DCC main-chain P2-C4 (large-scale Mom drift mitigation); results are written back into roadmap v3.x (new D5 stage chapter). Constraint carried over: until D3 is realized, all statements about "two-dimensional scenes" must be labeled "prescribed contraction background + phenomenological scaling" (following the sayable/unsayable list in §5 of the DCC P4 report).
