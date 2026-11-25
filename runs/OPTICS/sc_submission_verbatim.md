# Submission (verbatim, archived) — surface-conductivity route, 2026-11-22

> Source: governor message, 2026-11-22 20:44 (+08). Chinese original; archived unedited as the object of
> adjudication. Headings and emphasis preserved; no correction applied in this file.

---

This problem can be solved, but I think a key theoretical judgment must first be corrected:

**At present, \(\sigma_s\) cannot be defined directly as the yield strength of a material, nor can it be understood as an equivalent parameter compensating for the third-dimensional stress lost in dimensional reduction.**

Both interpretations could lead the DCC model into a wrong physical framework.

What truly needs to be solved is not finding a suitable yield-strength value, but rather:

**In the continuous evolution from three-dimensional space to two-dimensional space, how to define, propagate, and constrain the geometric and physical degrees of freedom in the third-dimension direction, so that the reduced-dimensional system still satisfies the original physical laws.**

Three issues must be distinguished here:

1. Geometric reduction: how does the spatial scale of the object change?
2. Physical reduction: how do the energy, momentum, stress, and internal degrees of freedom of matter respond?
3. Stability: during the above evolution, what conditions can ensure that matter does not undergo unphysical destruction?

These three issues are interrelated, but they cannot be replaced by a single \(\sigma_s\) parameter.

## I. First, correct three problems in the original proposal

### 1. Plane stress is not equivalent to physical reduction from three to two dimensions

The plane-stress condition in classical continuum mechanics:
\(\sigma_{zz}=\tau_{xz}=\tau_{yz}=0\)
is only an approximation for certain thin-plate mechanics problems. It does not mean that the spatial scale of the object's third dimension disappears, nor that the object has completed physical dimensional reduction. If DCC describes a change in the spatial metric, one should start from the three-dimensional spatial metric and its evolution law, rather than imposing the plane-stress assumption in advance.

### 2. The Poisson effect cannot simply be compensated through \(\sigma_s\)

The Poisson effect is a consequence of the material constitutive relation. In a linear elastic, isotropic material:
\(\varepsilon_z= \frac{1}{E} [ \sigma_z-\nu(\sigma_x+\sigma_y) ]\)
where \(E\) is Young's modulus and \(\nu\) is Poisson's ratio. If the spatial metric itself changes, the effective strain felt by the material will also contain a geometric-evolution contribution. Therefore, one cannot compensate for an eliminated spatial dimension simply by adjusting a stress parameter.

### 3. Yield strength is not a universal criterion for dimensional-reduction stability

Yield strength depends on the material, temperature, loading path, and constitutive model. Even if a material undergoes no plastic yielding at all, geometric changes may still cause: lattice-structure instability; molecular-bond breaking; phase transitions; changes in internal excited states; instability of quantum states or field configurations. Conversely, the appearance of local stress does not necessarily mean that matter will be destroyed. Therefore, a single yield threshold cannot represent the dimensional-reduction stability of all materials.

## II. The most important correction: what is your \(\sigma_s\) actually?

In light of the existing DCC roadmap v1.4, a very important conceptual confusion has occurred. Here \(\sigma_s(\omega)\) is:

> \(\sigma_s(\omega)=\text{the frequency-dependent surface conductivity of a two-dimensional material}\)

not \(\sigma_s=\text{the yield strength of a material}\).

| Comparison | Surface conductivity \(\sigma_s(\omega)\) | Yield strength |
| --- | --- | --- |
| Field | Electromagnetism, material optics | Continuum mechanics |
| Physical meaning | Response of two-dimensional carriers to an electric field | Critical stress for plastic deformation of a material |
| Unit (SI) | S | Pa |
| Frequency dependent | Yes | Usually not a simple function of frequency |
| Use in DCC | Compute reflection, transmission, absorption | Study mechanical stability of materials |

Your current G6 is actually the optics and observer-prediction stage. Its prerequisites are G4, G5′, and a self-consistent \(\sigma_s(\omega)\). This has no direct relation to determining yield strength.

Roadmap v1.4 already states explicitly that before a self-consistent surface conductivity is available, one cannot claim that a two-dimensionally reduced object is transparent, nor can one claim that it is opaque. Therefore, the whole line of argument about yield strength, the Poisson effect, and stress compensation in the original question cannot serve as the theoretical basis for resolving the G6 blocker.

## III. The physical relationship that actually needs to be established

It is suggested to reformulate the question as: **starting from the microscopic state of three-dimensional matter, how can one derive the effective two-dimensional surface conductivity that changes with DCC geometric evolution?**

### 1. Start from the three-dimensional electromagnetic response
\(\mathbf J(\omega)= \boldsymbol{\sigma}_{3D}(\omega)\mathbf E(\omega)\). In DCC there is anisotropic geometric evolution, so one cannot assume in advance that the conductivity is always isotropic.

### 2. Establish the current mapping from three to two dimensions
\(\mathbf K_{\parallel}(\omega) = \int dz_{\rm proper}\, \mathbf J_{\parallel}(\omega,z)\)
where \(dz_{\rm proper}\) is the proper length, not the uncorrected coordinate length. If the electric field is approximately uniform across the thickness and the local response can be described by a linear conductivity, then:
> \(\sigma_s(\omega) = \int dz_{\rm proper}\, \sigma_{3D,\parallel}(\omega,z)\)
For a homogeneous material: \(\sigma_s(\omega) \simeq L_z^{\rm proper}\sigma_{3D,\parallel}(\omega)\)
This formula is a baseline relation for the first step, not the final answer. For it to hold, one must check: whether the electric field is uniform across the thickness; whether there is a significant nonlocal response; whether surface and interface states exist; whether the three-dimensional material still retains its original electronic states; and whether geometric evolution introduces additional electromagnetic coupling. In particular, note that if the electronic states have undergone a phase transition or the carrier composition has changed, the conductivity of the original three-dimensional material cannot be carried over.

### 3. Incorporate the DCC metric into the surface conductivity
The metric you currently use is: \(ds^2=-N^2dt^2+A^2dx^2+B^2dy^2+C^2dz^2\). Therefore, the third-dimension proper length element is \(dl_z=C(t,x)\,dz\). If the third-dimension coordinate range is denoted \(\Delta z\), then \(L_z^{\rm proper}(t,x) = \int C(t,x,z)\,dz\), and under a homogeneous approximation \(L_z^{\rm proper}=C\Delta z\). This means that the surface conductivity cannot simply be obtained by multiplying a fixed thickness by a fixed bulk conductivity. One must simultaneously consider: changes in the third-dimension proper thickness; changes in the material's electronic states; carrier density and conservation relations; and the coupling between electromagnetic fields and geometry. More generally, the correct goal should be to start from the three-dimensional microscopic current response, compute the effective two-dimensional response kernel \(K_a(\omega,\mathbf q_\parallel) = \int dz_{\rm proper}\, J_a(\omega,\mathbf q_\parallel,z)\), and then define the effective response tensor according to the actual electric-field distribution: \(K_a= \sigma^{\rm eff}_{s,ab} E_b^{\rm eff}\). Here \(\sigma_s^{\rm eff}\) is not necessarily a local, isotropic scalar; it may also have frequency, wave-vector, time, and direction dependence.

## IV. A genuinely actionable route to a solution

### G6 surface-conductivity solution route
1. **R1**: determine the state of matter after two-dimensional reduction. Determine the final carrier composition, whether electrons exist, whether neutronization occurs, the material phase, and the temperature.
2. **R2**: derive the microscopic electromagnetic response. Starting from the Hamiltonian or field theory of the specific material state, compute the current response function and polarization tensor.
3. **R3**: obtain the effective two-dimensional surface conductivity. Rigorously reduce the third-dimension degrees of freedom to obtain \(\sigma_{s,ab}(\omega,\mathbf q)\), which may be anisotropic and nonlocal.
4. **R4**: connect to the G6 optical model. Compute reflection, transmission, absorption, and scattering, then connect to geodesics, radiative transfer, and observer imaging.

**Task A: first determine the true carrier composition.** Your existing v1.4 has already found that under the specified conditions of fixed area and conserved particle number, the electron chemical potential reaches about \(23.2\,\mathrm{MeV}\), exceeding the electron-capture thresholds of the main nuclides. This means that the original atomic and molecular electronic states cannot be carried over directly to the presumed final state. Therefore: one cannot continue to use the conductivity of an ordinary metal; one cannot continue to use atomic or molecular absorption cross sections; one cannot directly apply graphene's \(e^2/(4\hbar)\); and one cannot directly extrapolate the electronic response of the original three-dimensional material to the final two-dimensional state. Here priority should be given to completing the R1-B1 equilibrium EOS and combining it with the R1-B3 thermodynamic treatment in order to determine the material components that actually exist. Until this step is completed, even numerically very precise subsequent calculations may be computing a material state that does not actually exist.

**Task B: derive the surface conductivity using the Kubo formula.** In the simplified case of translational invariance and linear response:
\(\sigma_{s,ab}(\omega) = \frac{\Pi^R_{ab}(\omega,\mathbf 0)}{i(\omega+i0^+)}\)
The definition of \(\Pi^R\) used here must include the contact term matching the current response (for example, the diamagnetic term), and the specific sign depends on the convention adopted for the response function. More importantly, \(\Pi^R_{ab} = \Pi^R_{ab}(\omega,\mathbf q; T,n,\text{composition},B)\) is not a fixed constant. It is suggested to write it further as:
> \(\sigma_{s,ab}^{\rm DCC} = \sigma_{s,ab}(\omega,\mathbf q; B,T,\mathcal S_{\rm matter})\)
where \(B\): DCC third-dimension scale factor; \(T\): material temperature; \(\mathcal S_{\rm matter}\): the true microscopic state of the matter at hand; \(a,b\): current directions in the two-dimensional plane. It must be emphasized here that \(B\) is a geometric variable, not a direct multiplier of the material conductivity. If the system is not in equilibrium, nonequilibrium linear response or real-time evolution methods are also required.

**Task C: establish physical consistency checks.** Once the surface conductivity is obtained, it must at least pass: charge conservation (Ward identity); causality (correct analytic structure); Kramers–Kronig (real and imaginary parts satisfying dispersion relations); passivity (\(\operatorname{Re}\sigma_s\geq0\)); the spectral sum rule; dimensionality (SI unit S); and energy conservation (a correct energy budget at the optical boundary). One easily overlooked detail: if the two-dimensional reduction process still leaves a finite thickness, one cannot directly assume that it is already an ideal two-dimensional conducting sheet. A finite-thickness three-dimensional thin-film model and an effective two-dimensional sheet-conductivity model should be compared simultaneously. Only after the validity conditions of both have been verified can the three-dimensional model be replaced by a two-dimensional boundary condition.

**Task D: connect to actual optical predictions.** \(r=-\frac{Z_0\sigma_s}{2+Z_0\sigma_s}\), \(t=\frac{2}{2+Z_0\sigma_s}\), \(R=|r|^2\), \(T=|t|^2\), \(A=1-R-T\). These formulas apply only to an ideal free-standing, normally incident, isotropic two-dimensional conducting sheet. A real DCC model may have anisotropy, nonlocal response, finite thickness, and a nonstationary background, requiring an upgrade to the corresponding Maxwell boundary-value problem. Ultimately one must also go through L1 geodesics and observer frequency shifts; L2 material optics; L3 radiative transfer; L4 observer imaging. The calculated reflectance must not be equated directly with the brightness or transparency seen by the human eye.

## V. Specific recommendations for the current DCC project

| Priority | Work item | Deliverable | Decision |
| --- | --- | --- | --- |
| P0 | Verify the physical definition and units of \(\sigma_s\) | Freeze symbols, units, and definitions | Required |
| P1 | R1-B1 material EOS and carrier composition | Final-state material model | Required |
| P2 | Derive the microscopic polarization tensor | \(\Pi^R_{\mu\nu}\) | Required |
| P3 | Three- to two-dimensional response reduction | \(\sigma_{s,ab}\) | Required |
| P4 | Causality, gauge invariance, and energy checks | Verification report | Required |
| P5 | Maxwell optics and G6 interface | R/T/A calculation | Follow-up |

**The G6 surface-conductivity problem should not in turn block research on DCC geometric dynamics.** R2 intrinsic geometric dynamics; R1 material state and effective material model; and R5-L2 material optical response can be advanced in parallel. But one must not treat R5-L2 calculation results as the optical properties of a real two-dimensionally reduced object while R1 has not yet determined the material state.

## VI. One more theoretical trap to guard against

> \(\text{geometrically two-dimensional} \not\Rightarrow \text{materially two-dimensional} \not\Rightarrow \text{electromagnetic response equal to that of a two-dimensional material}\)

Three different outcomes are possible: **Case A** the original material structure is retained; **Case B** the matter reorganizes; **Case C** the matter cannot form a stable final state. All three outcomes should be kept as independent research branches, and one must not designate in advance which one must occur.

## VII. Final conclusions

1. The originally proposed yield-strength interpretation does not hold and must be withdrawn.
2. \(\sigma_s(\omega)\) should be explicitly defined as the effective two-dimensional surface conductivity.
3. The real blocker is that the microscopic electromagnetic response of the matter after two-dimensional reduction has not yet been derived self-consistently.
4. The optimal theoretical route is: material EOS → microscopic polarization tensor → effective two-dimensional surface conductivity → Maxwell optics → G6.
5. \(\sigma_s\) must not be selected backwards in order to obtain an expected visual effect.

Most recommended next step: establish a separate document, "DCC Effective Surface Conductivity Reconstruction — Technical Specification v1.0", with the following questions at its core: Which final-state material model should be used as the starting point? After electrons are removed by neutronization, which charged degrees of freedom remain? How can \(\sigma_s(\omega,q)\) be derived from the finite-density polarization tensor? How can the dynamical DCC metric be incorporated into the response function? When is the two-dimensional surface-conductivity approximation valid? How can one prove that the final response satisfies gauge invariance, causality, and energy conservation?
