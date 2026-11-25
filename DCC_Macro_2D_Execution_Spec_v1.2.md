# DCC: Execution Specification for Smooth Two-Dimensional Reduction of Macroscopic 3D Objects
## v1.2 — Physics Review Revised Edition / Executable Work Plan

**Version Date:** 2026-11-20  
**Scope:** DCC main chain P0–P4 and the dedicated "smooth two-dimensional reduction of macroscopic objects" track  
**Document Nature:** Research Execution Specification, not a physical conclusion that two-dimensionalization has been achieved  
**Baseline Inputs:** `Macro3D_to_2D_Smooth_Reduction_Roadmap` v1.1, DCC P0 directional-stress review results, P1 bubble-wall numerical solution summary  
**Governing Principle:** Do not miswrite specified backgrounds, inverse problems, low-energy effective theories, or visual-rendering results as a forward proof of a complete physical mechanism.

---

# 0. Executive Summary and Current Conclusions

## 0.1 Research Objective

Study whether a matter system originally possessing three macroscopic spatial directions, during the dynamical shrinkage of the spatial scale in one direction (denoted \(z\)), can:

1. Maintain controllable evolution of the matter structure rather than necessarily undergoing catastrophic destruction;
2. Form a low-energy description with two effective spatial dimensions in a finite or asymptotic process;
3. Form self-consistent geometric and dynamical matching between the contracting and non-contracting regions;
4. Provide computable, falsifiable light-propagation, radiative-transfer and observer signals;
5. If the above conditions cannot be satisfied simultaneously, clearly identify at which stage the theory fails.

This specification does not presuppose that the final answer is "smooth two-dimensional reduction". "Matter preserved", "matter reorganized", "structural destruction", "only an effective 2D low-energy theory obtained", and "classical description fails at the degenerate interface" are all allowed research outcomes.

## 0.2 Current Phase Assessment

| Module | Current Status | Conclusions That Can Be Drawn |
|---|---|---|
| P0: directional stress candidates | Important sign corrections exist; complete inhomogeneous solution not established | Maxwell \(F_{xy}\) is worth retaining, but it has not been proven to drive the target bubble-wall geometry |
| P1a: fixed Minkowski static bubble wall | Baseline results reported as meeting targets | Static kink solver initially passes; convergence order still needs verification on a third grid |
| P1b: collective-coordinate friction model | Parameter scan complete | It is a phenomenological velocity model, not a moving-wall solution of the full relativistic field equations |
| D1: matter adiabatic response | Only preliminary screening parameters | \(\eta<1\) cannot serve as a universal stability theorem |
| D2: specified contraction background | Power-law / exponential background settings exist | It is an externally specified background, not endogenous dynamics |
| D3: endogenous contraction dynamics | Incomplete | The stress-budget inverse problem cannot yet replace a forward self-consistent solution |
| Dimensional mapping / compactification | v1.1 contained conceptual and topological errors | Must distinguish compactification, thin-layer confinement, macroscopic compression and genuine dimensional change |
| Matter 2D-reduction transport | Incomplete | Cannot claim atoms, chemical bonds or macroscopic objects will automatically adapt |
| Optics and vision | Several usable formulas exist, but their scope of applicability has been over-extended | Must compute according to specific 2D-material response, geometry and observation conditions |
| Macroscopic geometric enclosure | Incomplete | Requires finite-region initial data, boundaries and matching conditions |

**Overall verdict:** The research program can continue, but statements in v1.1 such as "the conditions for smooth two-dimensional reduction have been determined", "the fiber-bundle mapping is uniquely self-consistent", and "macroscopic objects become nearly invisible phantom membranes" must be downgraded to conditional hypotheses or model-specific results. There is currently no evidence that a macroscopic three-dimensional object can smoothly transform into two-dimensional matter.

## 0.3 Research Route Overview

```text
P0 directional stress and equation sign review
        |
        v
P1 fixed-background bubble-wall baseline ------> G1: numerical baseline frozen
        |
        v
R1 matter response criteria and single-particle models
        |
        +---------------------------+
        |                           |
        v                           v
R2 D3 endogenous geometry dynamics   R3 matter degrees of freedom / effective theory
        |                           |
        +-------------+-------------+
                      |
                      v
R4 finite-region geometry and interface matching
                      |
                      v
R5 light propagation, radiative transfer and observer imaging
                      |
                      v
Gates: GO / CONDITIONAL GO / NO-GO
```

R2 and R3 may run in parallel after a clear common-background assumption is set; R5 may first do test rays and material models, but must not call them verified observational predictions of DCC.

---

# 1. Terminology, Variables and Model Boundaries

## 1.1 Four Physical Situations That Must Be Distinguished

| Name | Definition | Equal to macroscopic 2D-ization? |
|---|---|---|
| Anisotropic geometric contraction | A metric direction's scale factor \(B(t,x)\) decreases | No |
| Finite-thickness thin layer | Matter confined to a very thin but nonzero \(z\)-direction region | No; still generally in 3D space |
| Compactification / dimensional reduction | A direction has compact topology and low-energy observers cannot excite nonzero KK modes | Can yield an effective \(2+1\)-dimensional theory, but does not automatically mean a macroscopic object has been flattened |
| Genuine dimensional change | The dimension or topology of spacetime / matter degrees of freedom changes | Requires additional theory; cannot be inferred from \(B\to0\) alone |

Subsequent reports must state which of these is being studied. These concepts must not be interchanged within one derivation without explanation.

## 1.2 Basic Geometric Notation

In geometric units with \(c=1\), one may start with:

\[
ds^2=g_{ab}(t,x)dx^a dx^b
+A^2(t,x)dy^2+B^2(t,x)dz^2,\qquad a,b\in\{t,x\}.
\]

If \(g_{ab}dx^a dx^b=-dt^2+dx^2\), then:

\[
ds^2=-dt^2+dx^2+A^2dy^2+B^2dz^2.
\]

- \(A(t,x)\): transverse \(y\) scale factor;
- \(B(t,x)\): scale factor of the candidate contraction direction \(z\);
- \(H_A=\partial_t\ln A\), \(H_B=\partial_t\ln B\);
- \(\kappa=8\pi G\);
- \(\phi\): phase-transition / driving scalar field;
- \(Z(\phi)\): Maxwell kinetic coupling function; a healthy Maxwell sector generally requires \(Z(\phi)>0\).

If a spatially homogeneous Bianchi-I test model is used, state explicitly that it is a local or homogeneous baseline and not a finite-region bubble-wall solution.

## 1.3 Coordinate Thickness and Proper Thickness

If \(z\) is a coordinate and \(g_{zz}=B^2\), then on a slice at fixed \(t,x,y\):

\[
d\ell_z=B\,dz.
\]

The proper thickness corresponding to the coordinate interval \(\Delta z\) is:

\[
L_z^{\rm proper}=\int_{z_1}^{z_2}B(t,x,z)\,dz.
\]

Coordinate length, proper length, the compact circumference \(2\pi R\) and material thin-layer thickness must not be conflated.

---

# 2. Necessary Physics Revisions to v1.1

This section is the mandatory revision checklist before execution. Items not closed must not continue to be cited as proven conclusions.

## 2.1 Adiabatic Parameter: From a Single Threshold to a Transition Criterion

v1.1 used:

\[
\eta_{\rm rough}(t)=\frac{\hbar}{\Delta E}
\left|\frac{\dot a_z}{a_z}\right|.
\]

This quantity can serve as a rough screening parameter for "background change rate relative to microscopic energy gap", but it cannot generally imply:

- \(\eta<1\): matter is necessarily stable and smoothly two-dimensionalizes;
- \(\eta\ge1\): matter is necessarily torn apart.

A stricter adiabatic transition parameter should be based on the eigenstates of the instantaneous Hamiltonian \(H(t)\):

\[
H(t)|n(t)\rangle=E_n(t)|n(t)\rangle,
\]

\[
\epsilon_{mn}(t)=
\frac{\hbar\,|\langle m(t)|\dot H(t)|n(t)\rangle|}
{|E_m(t)-E_n(t)|^2},\qquad m\ne n.
\]

Execution requirements:

1. Compute the instantaneous energy spectrum and eigenstates for each matter model;
2. Compute \(\epsilon_{mn}\) between relevant states;
3. Treat minimum energy gaps, level crossings, continuum thresholds and degeneracy points separately;
4. Directly solve the time-dependent Schrödinger equation or the corresponding quantum field equation, measuring excitation probabilities;
5. Define "structure preservation" as measurable state fidelity, bond occupation, bound-state survival rate or other model-specific metrics.

\(\eta_{\rm rough}\ll1\) may serve as a screening condition for entering detailed calculations, not as the final GO condition.

## 2.2 The Power-Law Contraction Exponent Has No Universal \(\beta_C>1\) Threshold

If:

\[
a_z(t)=a_{z0}\left(\frac{t}{t_0}\right)^{-\beta_C},
\]

then:

\[
\left|\frac{\dot a_z}{a_z}\right|=\frac{\beta_C}{t},
\qquad
\eta_{\rm rough}(t)=\frac{\hbar\beta_C}{\Delta E(t)t}.
\]

Whether the evolution is adiabatic depends on \(\Delta E(t)\), the initial time, the time interval and the Hamiltonian matrix elements, not on \(\beta_C\) alone.

For a fixed energy gap, increasing \(\beta_C\) increases the instantaneous contraction rate and is not naturally "more adiabatic". If the gap grows with \(a_z\), the result changes again. Therefore v1.1's "\(\beta_C>1\) guarantees adiabaticity" must be deleted and replaced by scanning \((\beta_C,t_0,\Delta E(a_z))\) for each model.

## 2.3 KK Freeze-Out Condition for a Finite Compact Scale

If the spatial direction is indeed a circle \(S^1\) of radius \(R_z\), then with periodic boundary conditions:

\[
p_n=\frac{n\hbar}{R_z},\qquad n\in\mathbb Z,
\]

and the mode energy of a relativistic free field is:

\[
E_n^2=m^2c^4+c^2\frac{n^2\hbar^2}{R_z^2}+c^2p_\perp^2.
\]

Whether nonzero KK modes can be frozen out depends on whether the available system energy \(E_{\rm probe}\) is far below the first KK excitation gap, not merely on \(R_z\ll\lambda_{\rm visible}\).

For nonrelativistic particles, the energy-level difference is of order:

\[
\Delta E_{\rm KK}\sim\frac{\hbar^2}{2mR_z^2},
\]

with specific values depending on boundary conditions, topology, particle mass and field couplings.

**Important:** Compactification with finite \(R_z\) is "low-energy effective dimensional reduction", not proof that a macroscopic open direction can continuously contract into a compact circle. If the original model has a noncompact \(z\) direction, the KK circle spectrum cannot be applied directly.

## 2.4 Fiber-Bundle Mapping: Correcting Topology and Physical Interpretation

The expression in v1.1:

\[
\Phi(x,y,z)=(x,y;\theta)
\]

while also writing the base space as \((x,y)\) confuses total-space and fiber coordinates in the definition of the mapping. The correct fiber-bundle projection is:

\[
\pi:E\rightarrow B_2,\qquad
\pi(x,y,\theta)=(x,y),
\]

where the fiber is \(\pi^{-1}(x,y)\).

The following claims must be corrected:

- \(S^3\not\cong S^2\times S^1\);
- The Hopf fibration is \(S^1\hookrightarrow S^3\rightarrow S^2\); the total space is \(S^3\), not a direct product;
- A general \(S^1\) principal bundle is not necessarily trivial; whether it can be written as \(B_2\times S^1\) depends on the bundle's topological class;
- Retaining z information in the fiber coordinate \(\theta\) means the information still exists in the total space; it does not mean the z degree of freedom has disappeared;
- "Local trivialization" is a mathematical property of fiber bundles and does not automatically guarantee continuity of chemical bonds, van der Waals forces or hydrogen bonds.

The range of the weak interaction also cannot imply a universal topological lower bound \(R_z\gtrsim5\,\text{Å}\). Whether molecular bonds remain stable must be computed from the actual interaction Hamiltonian and wavefunctions.

## 2.5 Correct Measure for 3D Density to Surface Density

If \(\rho\) is the mass / particle-number density per unit proper three-dimensional volume and \(g_{zz}=B^2\), then in a simple orthogonal slicing:

\[
\Sigma(x,y)=\int \rho(x,y,z)\sqrt{g_{zz}}\,dz
=\int \rho(x,y,z)B(x,y,z)\,dz.
\]

More generally, the full spatial-slice volume element should be used:

\[
dV_3=\sqrt{\det h_{ij}}\,d^3x.
\]

Therefore one cannot directly write \(\Sigma=\int\rho\,dz\) without specifying the density definition and volume measure. Moreover, if the density, wavefunctions and coordinate support of the matter itself change with contraction, \(\rho(x,y,0)L_z\) cannot be treated as a general result.

## 2.6 Optics: 2.3% Is Not a Universal 2D-Material Constant

\[
A\simeq\pi\alpha\simeq2.3\%
\]

is the famous approximate universal absorption of a graphene-type monolayer with nearly massless Dirac carriers in the visible-frequency range under specific conditions. It depends on:

- carrier dispersion and occupation;
- Fermi level, temperature and scattering;
- photon frequency and interband transition conditions;
- polarization and angle of incidence;
- substrate and multilayer / finite-thickness structures.

It cannot be applied directly to arbitrary "two-dimensionalized macroscopic objects".

For an ideal, freely suspended, normally incident, isotropic 2D conducting sheet, one may use the surface conductivity \(\sigma_s(\omega)\):

\[
r=-\frac{Z_0\sigma_s}{2+Z_0\sigma_s},\qquad
t=\frac{2}{2+Z_0\sigma_s},
\]

\[
R=|r|^2,\qquad T=|t|^2,\qquad A=1-R-T.
\]

If \(\sigma_s=e^2/(4\hbar)\), then \(Z_0\sigma_s=\pi\alpha\), giving the approximate 2.3% absorption. But this is a special case of a material model, not a universal result of purely geometric dimensional collapse.

## 2.7 Kirchhoff's Law and Thermal Emission

Kirchhoff's law should be used per frequency, direction, polarization and corresponding thermal-equilibrium condition: the emissivity of a given optical mode equals that mode's absorptivity.

One cannot infer from a single visible-band value \(A\approx2.3\%\) that the total thermal-radiated power over the entire spectrum is always 2.3% of a blackbody. Such an approximation is only valid when the absorptivity is approximately flat over the corresponding spectral range and the applicability conditions hold.

A 2D surface source should use boundary / jump conditions consistent with the chosen definition of radiative intensity; the \(\delta(s)\) surface-source notation must specify units and the normal coordinate.

## 2.8 The Visibility Criterion Cannot Be Determined by \(L_z\le\lambda\) Alone

The following concepts must be separated:

1. Whether the thickness of the third dimension can be resolved by the imaging system;
2. The object's reflection / absorption / scattering contrast for incident light;
3. The object's own thermal radiation;
4. Whether the signal on the human retina exceeds the threshold;
5. Whether the object has sufficient spatial / spectral / temporal contrast with the background.

A thickness smaller than the wavelength does not automatically mean invisible; a thin film can still be detected via surface conductivity, absorption, reflection, scattering and phase changes. The human eye's ~1 arcminute resolving power is only an empirical order of magnitude for specific vision, contrast and illumination conditions, not a fixed pixel-sampling law.

---

# 3. P0/P1 Baseline Integration and G1 Closure

## 3.1 P0 Conclusion Integration

Working conclusions on the current directional-stress candidates:

| Candidate | Current conclusion | Must continue checking |
|---|---|---|
| Maxwell \(F_{xy}\) | Retained; in a local orthonormal frame \(p_x=p_y=+\rho_B,\ p_z=-\rho_B\), giving directionality | Full Maxwell equations, Bianchi identity, Einstein constraints and inhomogeneous solutions |
| Three-form \(H_{txy}\) | With the standard positive-sign kinetic term the pressure direction is opposite to the target trend; temporarily deprioritized | Re-evaluate only if the specific action / duality convention changes |
| Three-form \(H_{xyz}\) | Simple configurations cannot provide the required direction discrimination | Not a first choice |
| Compactification modulus | Promising but must be derived from higher-dimensional reduction | radion kinetic term, potential, normalization and coupling to geometry |
| SSB vector | Conditional candidate | \(A_0\) constraint, longitudinal mode, ghosts, gradient stability and energy lower bound |

Maxwell action candidate:

\[
S=\int d^4x\sqrt{-g}\left[
\frac{R}{2\kappa}
-\frac12(\nabla\phi)^2
-V(\phi)
-\frac14 Z(\phi)F_{\mu\nu}F^{\mu\nu}
\right],\qquad Z(\phi)>0.
\]

The following must hold simultaneously:

\[
\nabla_\mu(ZF^{\mu\nu})=0,\qquad dF=0.
\]

For the minimal ansatz with only \(F_{xy}=f(t,x)\), the Bianchi identity constrains \(\partial_t f\); one cannot solve only the Maxwell equations while ignoring \(dF=0\). Additional field components may be needed in more general dynamical geometries.

## 3.2 Current P1a Results

Reported:

- Static wall position and velocity close to zero;
- Numerical wall thickness 4.167 versus analytic 4.164, error less than 0.1%;
- Energy residual \(8.75\times10^{-7}\);
- Wall surface tension 0.942;
- Residual at two grid points drops from \(8.75\times10^{-7}\) to \(5.37\times10^{-8}\).

Verdict: **Static baseline initially passes, but convergence order has not yet been demonstrated.**

### G1-A: Third-Grid Convergence Test

Execute:

1. Use at least three spatial resolutions \(dx,\ dx/2,\ dx/4\);
2. Keep the physical domain, boundary conditions and time-integration error control consistent;
3. Compute errors separately for wall position, wall thickness, tension and field profile;
4. If an analytic solution exists, compute:
   \[
   p=\log_2\left(\frac{\|u_{dx}-u_{dx/2}\|}
   {\|u_{dx/2}-u_{dx/4}\|}\right);
   \]
5. The decrease ratio of the energy residual must not be used as a substitute for the solution's convergence order.

Acceptance:

- Wall thickness, wall position and tension stabilize with grid refinement;
- Observed order is compatible with the expected order of the discretization scheme;
- Boundary-reflection contamination does not enter the measurement window.

### G1-B: Analytic Check of Wall Surface Tension

Compute:

\[
\sigma_w=\int dx\left[
\frac12(\partial_x\phi)^2+V(\phi)-V_{\min}
\right].
\]

Also check the first-integral relation of the static solution (where applicable):

\[
\frac12(\partial_x\phi)^2\approx V(\phi)-V_{\min}.
\]

Acceptance: numerical integration, analytic kink tension and grid-extrapolated results agree with one another, with the error threshold registered before the run.

## 3.3 Current P1b Results and Parameter Corrections

Collective-coordinate model:

\[
\sigma_w\frac{dv}{dt}=F_{\rm drive}-\eta_{\rm eff}v,\qquad
v_{\rm term}=\frac{F_{\rm drive}}{\eta_{\rm eff}}.
\]

This is a low-speed, phenomenological friction model. It is not complete relativistic bubble-wall dynamics, and the true relativistic limit cannot be derived from the numerical upper-limit treatment with \(\eta=0\).

From existing scan data:

\[
\eta v_{\rm term}\approx0.0106.
\]

Target velocity:

\[
\beta_{\rm target}=\frac{42.47}{299792.458}
\approx1.416\times10^{-4}.
\]

Therefore:

\[
\eta_{\rm target}\approx\frac{0.0106}{1.416\times10^{-4}}
\approx74.9.
\]

**Execution revisions:**

- Correct "\(\eta\approx1.0\) corresponds to 42.47 km/s" to "with the current nondimensionalization and scan table, approximately \(\eta\approx75\)";
- Note \(F_{\rm drive}\), \(\sigma_w\), velocity units and friction-parameter units in the result files;
- 42.47 km/s remains archived as a low-speed phenomenological assumption, not a theoretical prediction;
- A relativistic wall-momentum equation must be established separately for the relativistic-velocity group, defining the friction four-force / energy-momentum exchange.

G1 closure conditions: G1-A and G1-B complete, P1b parameter revision complete. The magnetically sourced driving PDE is not a required G1 closure item and is handed over to R2.

---

# 4. R1: Matter Adiabatic Response and Destruction / Adaptation Criteria

## 4.1 Objective

Answer: given a geometric background \(B(t,x)\), can specific matter degrees of freedom follow the change? Which degrees freeze, which are excited, and which bound states disappear?

R1 must not begin by simulating a complete macroscopic object. Establish verifiable criteria from minimal models first.

## 4.2 R1-1: Free Scalar Field Modes

On a specified background metric, solve:

\[
S_\chi=-\frac12\int d^4x\sqrt{-g}
\left[g^{\mu\nu}\partial_\mu\chi\partial_\nu\chi
+m^2\chi^2\right].
\]

Outputs:

- Mode equations;
- Canonical normalization;
- Instantaneous frequencies;
- Bogoliubov coefficients (if in/out modes are used);
- Particle production / excitation energy;
- Scan plots versus \(B_{\min}\), contraction rate and initial state.

Acceptance:

- The fixed-background static limit agrees with analytic modes;
- Convergence in grid and time step;
- Clear budget for energy / constraint residuals;
- Do not mislabel a reduction in the number of coordinate modes as the automatic disappearance of physical degrees of freedom.

## 4.3 R1-2: Single-Particle Bound States / Hydrogen-Like Atom Model

Two levels:

**Level A: Controlled Potential-Well Model**

- Construct a nonrelativistic Hamiltonian under an anisotropic spatial metric;
- Specify the Laplace–Beltrami form of the kinetic operator;
- Specify whether the potential is a 3D Coulomb field, an effective 2D field, or an externally applied potential;
- Compute the lowest few eigenstates, level spacings, wavefunction distributions and transition probabilities.

**Level B: Electromagnetically Self-Consistent Atom Model**

- Solve the corresponding Maxwell equations and the quantum states of charged particles;
- Compare models where the field still propagates in 3D, where the field is also reduced to 2D, and where finite thickness / substrates exist;
- Must not directly replace the 3D \(1/r\) potential with the 2D \(-\ln r\) without explaining the electromagnetic field's propagation space and boundary conditions.

Output metrics:

- Ground-state energy \(E_0(B)\);
- Minimum energy gap \(\Delta E_{\min}(B)\);
- Probability width along z;
- Excited-state occupation;
- Bound-state survival probability;
- Level crossings / continuum thresholds;
- External-field and radiation energy.

Acceptance:

- Recover the 3D baseline at \(B=1\);
- Recover the corresponding 2D baseline under an explicitly defined 2D field-theory model;
- Cross-validate time evolution against the instantaneous-eigenstate approximation;
- Only when the bound-state survival rate and energy budget reach pre-registered thresholds may one call it "smooth adaptation under this model".

## 4.4 R1-3: Chemical Bonds and Lattice Models

Start with a minimal molecule (two-center binding potential or simplified diatomic model), then a small lattice.

Outputs:

- Bond lengths, bond energies, vibration frequencies;
- Bond-breaking / recombination probabilities;
- Eigenvalues of the lattice dynamical matrix;
- Phonon spectra and imaginary frequencies;
- Defect density and thermalization energy.

The "weak-interaction range of about 3–5 Å" must not be used directly to set a topological lower bound for \(R_z\). Bond stability follows from the actual Hamiltonian and geometric constraints.

R1's summary must classify results as:

- **A: adiabatic follow**;
- **B: nonadiabatic but still bound / recombinable**;
- **C: bound-state destabilization or structural destruction**;
- **D: model / classical approximation fails, unable to judge**.

---

# 5. R2: D3 Endogenous Geometric Dynamics

## 5.1 Objective

Upgrade the externally specified \(B(t)\) into a forward solution determined by the field equations. The completion standard for D3 is not "finding the required stress", but finding a self-consistent solution satisfying all field equations, constraints, boundary conditions and stability conditions.

## 5.2 Minimal Action

Prefer to study first:

\[
S=\int d^4x\sqrt{-g}\left[
\frac{R}{2\kappa}
-\frac12(\nabla\phi)^2
-V(\phi)
-\frac14Z(\phi)F_{\mu\nu}F^{\mu\nu}
\right],
\]

with \(Z(\phi)>0\).

The following must be derived independently from this action:

1. Full Einstein equations;
2. Scalar field equation;
3. Maxwell equations;
4. Bianchi identity;
5. Total energy-momentum conservation;
6. ADM Hamiltonian and momentum constraints.

The stress-budget table must not be used directly as a substitute for the field equations.

## 5.3 Stress-Budget Inverse Problem: Necessary Condition Only

Candidate formula given in v1.1:

\[
p_x+p_y-p_z=
\frac{2}{\kappa}\left[
\gamma^2-\gamma h-\frac12h^2
\right]
\]

where the setting \(H_A=H_B=h\), \(H_C=-\gamma\) must be re-derived and verified under the full conventions.

Execution requirements:

- Specify the metric signature, curvature sign and Einstein-equation conventions;
- Derive this expression from the same set of reduced Einstein equations;
- Perform independent substitution tests for \(h=0\), vacuum, the isotropic limit and the Maxwell source;
- Check consistency between the source stresses \(\rho,p_x,p_y,p_z\) and the geometric equations;
- Label the formula as "inverse-problem relation pending review" until it passes symbolic and numerical unit tests.

**Do not carry over the conclusion that "\(\rho_B=\gamma^2/\kappa\) necessarily satisfies the budget" unless the stress-combination coefficients, Maxwell stress tensor and Einstein equations have been checked term by term and proven.**

## 5.4 Forward Solution Sequence

### R2-A: Homogeneous Bianchi-I Verification

Metric:

\[
ds^2=-dt^2+A^2(t)(dx^2+dy^2)+B^2(t)dz^2.
\]

Tasks:

- First obtain all Einstein components with independent symbolic computation;
- Substitute the scalar field and \(F_{xy}\);
- Solve the ODEs;
- Monitor the Hamiltonian constraint;
- Compare \(H_A,H_B,\rho,p_i\);
- Scan initial conditions and the coupling function \(Z(\phi)\).

Do not proceed to inhomogeneous bubble-wall evolution before the homogeneous test passes.

### R2-B: ADM Constraint-Preservation Test

Use a \(1+1\)-dependent reduced geometry. Define lapse, shift, spatial metric and extrinsic curvature; write the Hamiltonian and momentum constraints and the evolution equations.

Acceptance:

- Initial constraint residual below the registered threshold;
- No exponential drift of the constraint residual during evolution;
- Constraint residual converges under grid refinement;
- Boundary conditions do not inject unregistered constraint error into the computational domain;
- Consistency with the homogeneous-limit solution.

### R2-C: Inhomogeneous Coupling of Scalar Wall + Maxwell

Increase complexity step by step:

1. \(\phi\) on a fixed background;
2. \(\phi+F\) on a fixed background;
3. Dynamical geometry without magnetic flux;
4. Dynamical geometry coupled to magnetic flux;
5. Finite region with absorbing / matching boundaries.

For a single \(F_{xy}\) component, both the Maxwell equations and \(dF=0\) must be checked. If additional electric-field components are needed, they must be explicitly included in the ansatz and solved for; they cannot be ignored afterward.

## 5.5 D3 Go/No-Go

**GO:**

- A regular forward solution exists;
- \(Z>0\), no ghosts;
- Hamiltonian and momentum constraints are controlled;
- \(B\) evolves according to the target law;
- The transverse scale \(A\) behaves in line with pre-registered targets;
- Stress-energy is finite;
- Reproducible with respect to initial conditions and resolution;
- No identified catastrophic instability under linear perturbations.

**CONDITIONAL GO:**

- A stable solution is obtained only within finite time, finite thickness or a finite parameter interval;
- Supports only an effective 2D low-energy description, not \(B=0\);
- Results depend on specific matter sources or external driving.

**NO-GO:**

- Only inverse-problem stresses exist, realizable by no healthy field source;
- Constraints remain out of control;
- Requires \(Z\le0\), negative kinetic energy or unbounded energy;
- Target contraction necessarily accompanied by curvature / stress singularities with no controlled effective theory;
- Transverse geometry cannot satisfy the target conditions.

---

# 6. R3: Compactification, Dimensional Reduction and Macroscopic-Object Mapping

## 6.1 Objective

Establish accurate geometric / topological descriptions, avoiding conflation of "projection", "thin layer", "compactification" and "dimensional change".

## 6.2 Three Models That Must Be Separated

### Model A: Anisotropic Contraction of a Noncompact Direction

\(z\in\mathbb R\), \(B(t,x)\) decreases. Study the dynamics of the metric and matter fields. Cannot be directly called KK compactification.

### Model B: Finite-Thickness Confined Thin Layer

Matter is confined in a potential well of finite width. The third direction still exists, but high-energy excitations may be frozen out. Its effective 2D theory depends on the confining potential and level spacings.

### Model C: Genuine Compact Circle Direction

\(z\sim z+2\pi R_z\), spatial topology contains \(S^1\). A KK expansion can then be performed:

\[
\Psi(x^\mu,z)=\sum_{n\in\mathbb Z}
\psi_n(x^\mu)e^{inz/R_z}.
\]

Low-energy cutoff condition:

\[
E_{\rm probe}\ll \Delta E_{\rm KK,1}.
\]

Model C is the standard reference for effective dimensional reduction, but does not automatically represent Model A or macroscopic-object compression.

## 6.3 Correct Way to Write the Mapping

For a fiber bundle:

\[
\pi:E\to B_2,\qquad \pi^{-1}(q)\simeq S^1
\]

Global structure can only be discussed after the total space, base space, fiber, transition functions and bundle topological class have been specified. Only if the bundle is trivial may one write \(E\simeq B_2\times S^1\).

To execute:

- Give the concrete total space \(E\);
- Give the base space \(B_2\);
- Give the fiber and transition functions;
- Compute Chern classes (for a principal \(S^1\) bundle);
- Verify the claimed topology of the total space;
- Distinguish "information retained in the fiber" from "low-energy non-excitable degrees of freedom".

## 6.4 R3 Outputs

- Selected geometric model and its scope of applicability;
- Relation between coordinate thickness and proper thickness;
- KK spectrum or confined-potential-well spectrum;
- Low-energy effective action;
- Correct integration measures for surface density / surface charge and similar quantities;
- Topological mapping and its proof;
- List of irreducible residual degrees of freedom.

**Acceptance:** No longer use the unproven conclusion "the fiber-bundle mapping is the uniquely self-consistent form". One must explain, via comparison with at least one noncompact-contraction model and one thin-layer model, why a given model is chosen.

---

# 7. R4: Finite-Region Macroscopic Geometry and Interface Matching

## 7.1 Objective

Move from infinite homogeneous or local planar approximations to geometry in which contraction occurs within a finite region. Must answer:

- Is the front shape planar, spherical or otherwise;
- How do contracting and non-contracting regions match;
- Is the front thickness finite;
- Is there surface-layer stress;
- Does the observer's worldline cross the degenerate region.

## 7.2 Execution Steps

1. First establish a finite-width front in a 1+1 reduced model;
2. Specify the lapse, shift, spatial metric and extrinsic curvature of the inner and outer regions;
3. Check matching conditions and constraints;
4. Use appropriate junction conditions for the thin-wall limit; directly solve the field equations for a finite-thickness wall;
5. Then upgrade to axial or spherical symmetry;
6. Check whether the asymptotic region outside the boundary recovers the specified background.

A local planar wall solution must not be directly extrapolated into a spherical front covering the Earth.

## 7.3 Acceptance

- Geometric continuity of inner and outer regions or correct thin-wall jump conditions;
- Energy-momentum conservation;
- Constraint propagation;
- Resolvable front thickness, velocity and curvature;
- No spurious signals generated by finite-region boundaries;
- Computable for observer worldlines.

---

# 8. R5: Light Propagation, Radiative Transfer and Human-Eye Imaging

## 8.1 Layered Models

R5 has four layers that cannot substitute for one another:

**L1 Geometric Optics**

- Given an already-solved spacetime metric;
- Solve null geodesics;
- Compute observer four-velocity, local orthonormal frame, frequency shifts and celestial-sphere direction mapping.

**L2 Material Optics**

- Given a specific material's \(\sigma_s(\omega)\), dielectric function or polarization tensor;
- Solve reflection, transmission, absorption and scattering;
- Specify substrate, angle of incidence, polarization and frequency spectrum.

**L3 Radiative Transfer**

- Given absorption coefficient, emission coefficient, scattering kernel and boundary conditions;
- Solve the radiative-transfer equation;
- Use Kirchhoff relations per mode;
- Distinguish thermal emission from reflected / scattered signals.

**L4 Observer Imaging**

- Optical-system PSF;
- Retinal irradiance;
- Spatial / temporal integration;
- Contrast sensitivity, spectral response and exposure;
- Final visibility judgment.

## 8.2 Geodesics and Frequency Shifts

For a photon wave vector \(k^\mu\) and observer four-velocity \(u^\mu\), the locally measured frequency is:

\[
\omega_{\rm obs}=-k_\mu u^\mu.
\]

Frequency-shift ratio:

\[
\frac{\omega_{\rm obs,2}}{\omega_{\rm obs,1}}
=\frac{(-k\cdot u)_2}{(-k\cdot u)_1}.
\]

When spacetime is nonstationary or the observer moves, Doppler results must not be inferred from the front velocity alone. One must actually integrate the geodesics and specify emitter and receiver four-velocities.

## 8.3 Thin-Sheet Optics

For an ideal freely suspended 2D conducting sheet at normal incidence, one may start with:

\[
r=-\frac{Z_0\sigma_s(\omega)}{2+Z_0\sigma_s(\omega)},\qquad
t=\frac{2}{2+Z_0\sigma_s(\omega)},
\]

\[
R=|r|^2,\quad T=|t|^2,\quad A=1-R-T.
\]

If the material is a graphene-type Dirac monolayer in an applicable spectral range, \(A\approx\pi\alpha\) may be used as a benchmark. Other materials must compute their own surface conductivity / dielectric response.

Oblique incidence, anisotropic sheets, substrates and multilayer structures require appropriate boundary conditions and TE/TM Fresnel / transfer matrices.

## 8.4 Radiative Transfer

General form:

\[
\frac{dI_\nu}{ds}=-\alpha_\nu I_\nu+j_\nu
\]

With scattering, scattering-in / out integral terms must be added. For a 2D surface source, use boundary jump conditions or a unit-consistent surface-source form.

Kirchhoff relations are used at the same frequency, direction, polarization and thermal-equilibrium mode; a single-frequency absorptivity must not be taken directly as a full-band Stefan–Boltzmann ratio.

## 8.5 Human-Eye Imaging

Simplified imaging:

\[
E_{\rm retina}(x',y')=
\iint {\rm PSF}(x'-\xi,y'-\eta)
E_{\rm image}(\xi,\eta)\,d\xi d\eta.
\]

Final visibility must report simultaneously:

- Target / background brightness / color contrast;
- Angular size and spatial frequency;
- Spectrum;
- Temporal variation and exposure;
- Observation distance, pupil and imaging PSF;
- Comparison of retinal signal with the threshold.

"Nearly invisible phantom membrane" must not be used as a general conclusion. Specific results may only be given under specified material conductivity, incidence conditions, background and observer parameters.

## 8.6 R5 Acceptance

- Geometric optics agrees with known static limits;
- Frequency shifts consistent with four-velocity definitions;
- Energy reflection / transmission / absorption conservation;
- Consistent units in radiative transfer;
- Clear parameter provenance for the PSF and human-eye threshold;
- Every rendered frame labeled with input model, validity region, hypothesis layer and uncertainty.

---

# 9. Numerical Engineering Specifications

## 9.1 Every Solver Must Have

- Parameter configuration files (key physical parameters must not be hardcoded in scripts);
- Fixed random seed (if stochastic processes are involved);
- Grid and time-step convergence tests;
- Unit tests and analytic-limit tests;
- Energy / constraint residual logs;
- Machine-readable results (CSV/JSON/HDF5);
- Runtime environment, dependency versions and Git commit;
- Failed runs must also be logged; do not keep only successful results.

## 9.2 Suggested Result Directory

```text
DCC/
  docs/
    DCC_Macro_2D_Execution_Spec_v1.2.md
    decisions/
  src/
    p1_wall/
    matter_transport/
    d3_homogeneous/
    d3_adm/
    optics/
  configs/
  tests/
    analytic_limits/
    convergence/
    constraints/
  runs/
    P1/
    R1/
    R2/
    R3/
    R4/
    R5/
  reports/
    gates/
    figures/
    tables/
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
initial_conditions:
boundary_conditions:
solver:
spatial_resolution:
time_step:
parameters:
observables:
convergence_tests:
constraint_tests:
acceptance_thresholds:
result:                      # PASS / CONDITIONAL / FAIL
known_limitations:
```

Thresholds must be registered before the run; adjusting thresholds after seeing results to manufacture a PASS is prohibited.

---

# 10. Phase Gates and Go/No-Go Decisions

## G1: P1 Baseline Freeze
Prerequisite: P1a third-grid convergence, analytic check of wall tension, P1b friction-parameter revision.  
Result: Freeze the static kink and phenomenological collective-coordinate baseline.  
Does not mean: Magnetically sourced walls, dynamical geometry or DCC bubble walls have been verified.

## G2: Matter-Response Baseline
Prerequisite: At least one controlled model in R1-1, R1-2 completed.  
GO: Reproducible classification of controlled adiabatic / nonadiabatic responses under a given background.  
NO-GO: Gap closure or bound-state disappearance makes the target matter model unable to persist; switch to the "destruction / reorganization" branch.

## G3: D3 Homogeneous Forward Dynamics
Prerequisite: Full Einstein–matter equations and constraints derived.  
GO: A healthy, constraint-controlled directional solution of the target type exists.  
NO-GO: Required stress cannot be realized by a healthy field source, or only via pathological kinetic terms / singular sources.

## G4: Inhomogeneous Finite Front
Prerequisite: G3 passed, ADM constraint framework passed.  
GO: A finite-width front evolves stably and matching conditions hold.  
NO-GO: Boundary / constraint / curvature singularities cannot be controlled.

## G5: Effective 2D Matter and Mapping
Prerequisite: R1 and R3 models mutually consistent.  
GO: Low-energy effective action, degree-of-freedom spectrum, measure and topological definition given.  
NO-GO: Only geometric degeneration obtained without a consistent low-energy matter theory.

## G6: Optics and Observer Predictions
Prerequisite: G4 and G5 passed within at least one explicit model.  
GO: Geodesics, material response, radiative transfer and observer-imaging chain closed.  
Otherwise: Only test-ray / conceptual-rendering results under a specified background may be released; must not be called DCC physical predictions.

---

# 11. Near-Term Execution Checklist (by Priority)

## Sprint 0: Freeze and Correct Existing Results

- [ ] Revise P1b: target 42.47 km/s corresponds to \(\eta_{\rm eff}\approx75\) (under current normalization).
- [ ] Add a third spatial resolution to P1a.
- [ ] Independently check the analytic integral of \(\sigma_w=0.942\).
- [ ] Freeze P1 solver version, parameters, logs and baseline outputs.
- [ ] Change v1.1's \(\beta_C>1\) universal adiabatic threshold to a hypothesis pending verification.
- [ ] Correct the fiber-bundle topology statement and the density-integration measure.
- [ ] Downgrade 2.3% absorption to a graphene-like Dirac sheet benchmark.
- [ ] Delete the statement of "nearly invisible phantom membrane" as a universal conclusion.

## Sprint 1: R1 Minimal Matter Models

- [ ] Build a free-scalar-field mode solver on an anisotropic background.
- [ ] Verify the 3D baseline at \(B=1\).
- [ ] Scan \(B(t)\) and contraction rates.
- [ ] Compute instantaneous energy spectra and \(\epsilon_{mn}\).
- [ ] Directly solve time evolution and compute excitation probabilities.
- [ ] Form four result classes: adaptation / reorganization / destruction / indeterminable.

## Sprint 2: R2 Homogeneous D3 Forward Solution

- [ ] Independently derive Einstein, scalar and Maxwell equations from the action.
- [ ] Independently derive the Maxwell stress tensor and check P0 signs.
- [ ] Derive all Bianchi-I component equations.
- [ ] Review the stress-budget inverse-problem formula.
- [ ] Implement homogeneous ODE solving and Hamiltonian-constraint monitoring.
- [ ] Scan \(Z(\phi)\), \(V(\phi)\) and initial conditions.
- [ ] Evaluate curvature invariants, energy density and linear-perturbation stability.

## Sprint 3: R3 Geometry and Effective Theory

- [ ] Implement the three model classes separately: noncompact contraction, thin-layer confinement, compact circle.
- [ ] Derive KK / bound-state energy spectra.
- [ ] Give correct fiber-bundle data (if used).
- [ ] Compute surface density under the correct proper-volume measure.
- [ ] Compare low-energy effective actions of different models.

## Sprint 4: R4/R5

- [ ] Construct finite-thickness front and inner / outer region matching.
- [ ] Pass the ADM constraint-preservation test.
- [ ] Integrate null geodesics for observer worldlines.
- [ ] Compute \(R,T,A\) using specific material response functions.
- [ ] Solve radiative transfer and imaging PSF.
- [ ] Generate observer views with hypothesis labels.

---

# 12. Deliverables and Report Format

Each phase must deliver at least:

1. **Theory files**: definitions, assumptions, derivations, sign conventions, scope of applicability;
2. **Solvers**: source code, configuration, dependency versions;
3. **Tests**: analytic limits, convergence, conservation / constraints;
4. **Machine results**: CSV/JSON/HDF5;
5. **Figures and tables**: all axes, units and parameters complete;
6. **Review reports**: passed items, failed items, unresolved items;
7. **Decision records**: GO / CONDITIONAL GO / NO-GO and rationale.

Every conclusion must be marked as one of the following:

- **ESTABLISHED**: established by derivation / verification within explicit assumptions;
- **MODEL RESULT**: numerical result under a specified model and parameters;
- **CONDITIONAL**: depends on assumptions not yet verified;
- **OPEN**: unresolved;
- **FALSIFIED**: falsified by counterexamples or tests.

MODEL RESULT or CONDITIONAL must not be rewritten as universal physical laws.

---

# 13. Boundaries of Final Scientific Statements

Before D3, matter transport and finite-region geometry have passed, one may say:

- Field / particle responses were studied on specified anisotropic backgrounds;
- A static scalar bubble-wall baseline was verified on a fixed Minkowski background;
- Friction parameters were scanned with a phenomenological collective-coordinate model;
- Effective 2D low-energy descriptions were established for certain compactification / thin-layer models;
- Test rays and optical responses of specific materials were computed for specified metrics.

One may not say:

- Macroscopic 3D objects have been proven to smoothly two-dimensionalize;
- \(\beta_C>1\) universally guarantees adiabatic matter adaptation;
- \(B\to0\) automatically produces stable 2D matter;
- Fiber-bundle mapping is the only possible two-dimensionalization mapping;
- All two-dimensionalized objects have 2.3% absorption or are nearly invisible;
- 42.47 km/s is a velocity predicted by standard vacuum bubble-wall theory;
- Passing the P1 static wall means DCC dynamical geometry has passed.

---

# 14. Current Decision

**Current recommendation: Continue research, but do not announce that "smooth two-dimensional reduction has been established".**

Priorities:

1. Close the three G1 wrap-up items (P1b parameter revision, P1a third grid, wall-tension check);
2. First complete R1's free-scalar-field and single-particle models to determine whether "matter adaptation" is possible at least in controlled models;
3. Simultaneously re-derive R2's homogeneous Einstein–Maxwell–scalar system from the full action, checking the D3 stress budget;
4. Only after the homogeneous forward solution passes, invest in inhomogeneous ADM bubble-wall solving;
5. Visual models may be developed in parallel, but must be labeled "specified-background test optics" and must not be presented in advance as physical predictions.

**Most important judgment principle:** DCC's goal is not to make a preset \(B(t,x)\) look like two-dimensionalization in an image, but to prove that geometry, matter, interactions, energy-momentum and observer measurements can coexist within one self-consistent set of equations. If the proof fails, the failure itself is a valid research result.
