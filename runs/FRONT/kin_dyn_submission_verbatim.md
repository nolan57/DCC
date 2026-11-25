# Submission 3 — proposed `R1 §4.6`, registered verbatim

**Received**: 2026-11-22. **Registered**: 2026-11-22, before `src/route/kinematic_dynamic_check.py` ran.
**Status**: **PROPOSED — governs nothing, in force nowhere.**
**Ruling**: `docs/decisions/kinematic_vs_dynamic_unfolding_v1.md`.
**Fidelity**: transcribed without correction. The original arrived with LaTeX partially mangled by transport
(`mapsto`, `left(`, `text{eff}`, `delta`, `mu_1`, `,` for thin spaces); it is kept in that state so the register
shows what was received. Where the text contradicts the record, the contradiction is a finding, not a
transcription error.

---

<!-- BEGIN-INSERTION-C -->

## 4.6 Kinematic Unfolding vs. Dynamic Unfolding

The D2 prescription (D2) defines a kinematic mapping: 3-D coordinates (x,y,z) are assigned to 2-D array sites by a
prescribed rule. This is a geometric statement, not a physical one. It contains no force, no stress, no
constitutive law, and therefore no prediction about how matter would actually deform.

This section separates the two, because conflating them would make the D2 prescription look like a dynamical
result.

**Kinematic unfolding (what D2 does).** A projection rule Pi: (x,y,z) mapsto (u,v) assigns each material point to
an array site. The rule is chosen by us. It is instantaneous, simultaneous, and stress-free by construction. No
equation of motion is solved.

**Dynamic unfolding (what physics would do).** A real body compressed to H_eff ~ delta and released would deform
according to its constitutive law. The deformation would be:

- Non-uniform, governed by the local elastic moduli and density;
- Sequential, propagating as a stress wave at the material sound speed c_s, not instantaneously — simultaneity
  across the body would violate causality;
- History-dependent, with plastic dissipation and possible fracture where strain exceeds the failure threshold.

D2 asserts the first. It does not derive the second, and must not be read as a claim that the second would look
like the first.

### 4.6.1 Worked example: composite circular disc

To make the distinction concrete, consider a minimal 2-layer test body: a disc of radius R, total height
H = 2 delta, consisting of two concentric regions with different material properties.

| Region | Radial extent | Material | Shear modulus | Sound speed |
| --- | --- | --- | --- | --- |
| Core | r le r_c = 0.4R | stiff (bone-like) | mu_1 = 10 G | c_{s,1} = sqrt(mu_1/rho) |
| Mantle | r_c < r le R | compliant (soft-tissue-like) | mu_2 = G | c_{s,2} = c_{s,1}/sqrt(10) |

Both regions have the same areal density rho for simplicity, so the contrast is purely elastic.

**Kinematic unfolding (D2).** Apply the prescribed radial projection

    Pi: (r, theta, z) mapsto (u,v) = ( (R/delta) r cos theta , (R/delta) r sin theta )

Both layers are mapped to the same disc of radius R/delta array sites. The core and mantle occupy their original
fractional areas: f_core = (r_c/R)^2 = 0.16, f_mantle = 0.84. The unfolding is simultaneous (t=0 for all material
points), area-preserving in the ratio above, and generates zero strain energy — because no deformation is
computed, only relabelling.

**Dynamic unfolding (physical).** Release the compressed disc. The elastic energy stored per unit volume scales as
w ~ mu (Delta/L)^2 where Delta is the displacement and L a length scale. The restoring stress is
sigma ~ mu d u_r / d r.

Because mu_1 = 10 mu_2, the core resists deformation ten times more strongly than the mantle at equal strain.
Under any isotropic release:

- **Differential strain.** The mantle, being compliant, strains first and further. At equal applied stress the
  mantle strain is varepsilon_2 = sigma/mu_2 = 10 sigma/mu_1 = 10 varepsilon_1. The mantle expands roughly an
  order of magnitude more than the core.
- **Sequential front.** The release propagates outward from the free edge at c_{s,2} in the mantle and
  c_{s,1} = sqrt(10) c_{s,2} in the core. The core therefore leads in wave speed but lags in displacement. The
  unfolding is not simultaneous: the outer mantle begins moving at t ~ 0, the core centre only after the wave
  traverses r_c, i.e. t_c ~ r_c / c_{s,1}.
- **Interface stress.** At r = r_c the two materials must remain bonded, so radial displacement is continuous but
  radial stress is not. The mismatch Delta sigma ~ (mu_1 - mu_2) d u_r / d r concentrates at the interface. Where
  Delta sigma exceeds the interfacial strength, delamination occurs — a failure mode with no counterpart in the
  kinematic map.
- **Final shape differs.** The kinematic map predicts a disc of radius R/delta with a sharp 16%/84% area split.
  The dynamic result predicts a disc whose outer radius is set by the mantle's larger strain, with the core
  occupying a smaller fractional area than 0.16 — the core has been stretched less but compressed relatively by
  the expanding mantle. The area ratio is not preserved.

**Summary of the discrepancy.**

| Quantity | Kinematic (D2) | Dynamic (physical) |
| --- | --- | --- |
| Timing | simultaneous | sequential, t_c ~ r_c/c_{s,1} |
| Core/mantle strain ratio | 1 : 1 | 1 : 10 |
| Area fraction of core | 0.16 (preserved) | < 0.16 (reduced) |
| Stored energy | 0 | int w dV > 0, partly dissipated |
| Failure modes | none | interfacial delamination possible |
| Governing input | projection rule Pi | mu(r), rho(r), c_s(r), boundary conditions |

### 4.6.2 Consequence for the DCC claim

The D2 prescription is therefore an idealised kinematic boundary condition, not a dynamical prediction. It assumes
an external agent enforces the projection Pi exactly, irrespective of the body's internal constitutive structure.

This is acceptable for the roadmap's purpose — the tier battery measures statistics of the deposited 2-D field,
and that field is by definition the output of Pi. But it must be stated explicitly:

> The uniform, simultaneous, centre-symmetric unfolding of D2 is a property of the projection rule, not of the
> matter. A physical body with heterogeneous elastic moduli would unfold non-uniformly, sequentially, and with
> dissipation. The DCC framework does not model this, and makes no claim that physical unfolding would reproduce
> Pi.

The distinction matters for the visualisation goal: a rendering that shows smooth uniform spreading is depicting
the kinematic map. A rendering that depicted physical unfolding would need to solve the elastic equations with
mu(r), rho(r) as inputs, and would show differential strain, wave propagation, and possibly fracture — a
qualitatively different picture.

**Scope note.** At H_eff ~ delta the continuum elastic description used above is itself at the edge of validity —
the disc is only two atomic layers thick, and mu may not be well-defined. The example is therefore illustrative
of the structure of the discrepancy (kinematic vs. dynamic), not a quantitative prediction for the DCC
configuration itself. The discrepancy is present at all thicknesses; it does not disappear as H_eff to delta, it
merely changes regime.

<!-- END-INSERTION-C -->

## Cross-reference updates requested

| Location | Addition |
| --- | --- |
| `§3` D2 statement | Append: "The unfolding rule `Pi` is kinematic; see `§4.6` for the distinction from dynamic unfolding." |
| `§7` gap list | Add row: `T5` \| kinematic/dynamic conflation \| D2 assumes stress-free simultaneous projection; physical unfolding would be sequential, non-uniform, dissipative \| not closable without constitutive model; out of scope for tier battery |
| `§4.5.1` | Append: "The bound `H_eff ≥ δ` applies to the kinematic map. A dynamic treatment would additionally require `δ` to exceed the elastic mean free path for `mu` to be defined." |

---

*Content generated by AI*
