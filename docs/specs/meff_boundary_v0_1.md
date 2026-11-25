# S3→S4 Branch: Effective 2D-ification Space Approximation Boundary (draft v0.1)

> ## SUPERSEDED — 2026-11-22
> Replaced by **`docs/specs/meff_boundary_v0_2.md`** (adopted). Governor rulings **D-A** (boundary-data
> split) and **D-B** (`C_info` dissolved) in `docs/decisions/meff_boundary_disposition_v1.md`.
> All four constraints `C_geo/C_phys/C_info/C_top` are **RETIRED**; the names may not be reused (registry R4).
> **This body is preserved unedited** for the audit trail (§9.1) — including the LaTeX artefacts noted below.

**Registered**: 2026-11-22
**Status**: **SUPERSEDED by v0.2. Not citable.**
**Provenance**: submitted by the project governor as a complete standalone text.
**Audit**: `reports/reviews/meff_boundary_v0_1_audit.md`
**Probe**: `src/s45_branch/meff_boundary_probe.py` → `runs/S45/meff_boundary_probe_results.txt`
(registered first in `runs/S45/meff_boundary_probe_registration.md`)

## Registration notes

1. **Body reproduced verbatim**, including LaTeX macro artefacts in the submission (`\mathcal{M}{text{eff}}`,
   `\mathcal{C}{text{geo}}`, etc., where an underscore appears to have been dropped). These are **not corrected
   here**, because correcting them silently would be editing a submitted text. The audit interprets each symbol
   by its evident intent; a cleaned rendering appears in the audit's appendix.
2. **This registration confers no authority.** Until the audit is closed and a v0.2 is adopted, no product may
   cite this text as a boundary definition, and no constraint in it may be treated as registered (i.e. no
   threshold in it may be used to pass or fail anything).
3. The draft names four constraints `C_geo, C_phys, C_info, C_top`. The ledger
   (`docs/decisions/staged_relaxation_visual_route_v1.md`) already uses `C1, C2, C3`, and roadmap §6.1 uses
   `C1–C4` for four *contrast criteria*. See audit F10. Bare `C1/C2/C3` in any downstream text continues to mean
   the ledger's constraints.

---

## 1. Domain and parameter space

Let the state of a macroscopic 3D object during smooth 2D-ification be described by the parameter space
`mathcal{P} = { mathbf{x}, t, epsilon }`, where `epsilon in [0, 1]` is the continuous 2D-ification parameter
(`epsilon=0` is the ideal 2D state, `epsilon=1` is the full 3D state).

The effective 2D-ification space `mathcal{M}_{text{eff}}` is defined as a subset of `mathcal{P}` satisfying the
following four joint constraints:

`mathcal{M}{text{eff}} = left{ (mathbf{x}, t, epsilon) in mathcal{P} ;middle|; mathcal{C}{text{geo}} wedge mathcal{C}{text{phys}} wedge mathcal{C}{text{info}} wedge mathcal{C}_{text{top}} right}`

## 2. The four boundary constraints

### `mathcal{C}_{text{geo}}`: Geometric and curvature approximation boundary

The radius of curvature `R_{perp}` of local third-dimension undulations must be much larger than the system's
characteristic observation scale `lambda_{text{obs}}`:

`sup_{mathbf{x} in Omega} left| frac{partial^2 z}{partial x_i partial x_j} right| cdot lambda_{text{obs}} leq delta_{text{geo}}`

where `delta_{text{geo}}` is the geometric tolerance threshold. When an increase in `epsilon` causes
`R_{perp} sim lambda_{text{obs}}`, parallax and occlusion effects become non-negligible, the `mathcal{M}_{text{eff}}`
boundary is breached, and a switch to the full 3D description of S4 is required.

### `mathcal{C}_{text{phys}}`: Physical field and degree-of-freedom truncation boundary

The perturbation contribution of the physical field gradient perpendicular to the 2D-ification direction to the
system's total action `S` must be at a perturbative level:

`frac{delta S_{perp}}{S_{parallel}} leq delta_{text{phys}}`

where `S_{perp}` is the field excitation contribution in the third-dimension direction, and `S_{parallel}` is the
dominant action within the 2D plane. This constraint ensures that the 2D-ified equations (such as the dimensionally
reduced equations of motion) maintain physical self-consistency within `mathcal{M}_{text{eff}}`, without introducing
unphysical energy injection or dissipation.

### `mathcal{C}_{text{info}}`: Information entropy and visualization fidelity boundary

The information loss entropy `Delta H` from 3D to 2D projection must be below the visual reconstruction threshold:

`Delta H = H_{text{3D}} - H_{text{2D}} leq delta_{text{info}}`

where `H_{text{3D}}` is the complete information entropy of the 3D object, and `H_{text{2D}}` is the information
entropy carried by the 2D projection. When `Delta H leq delta_{text{info}}`, the lost third-dimension information
(depth, volumetric density) can be reconstructed losslessly or with minimal loss via declared display conventions
(such as texture mapping, shadow encoding), and the 2D visualization remains topologically equivalent to the 3D
physical state.

### `mathcal{C}_{text{top}}`: Topological connectivity boundary

Within the range `epsilon in [0, epsilon_{text{crit}})`, the topological invariants of the object (Euler
characteristic `chi`, genus `g`) must remain consistent with the ideal 2D state:

`chi(epsilon) = chi(0), quad g(epsilon) = g(0)`

When `epsilon geq epsilon_{text{crit}}`, 3D topological phase transitions (such as hole generation, changes in
connectivity) are permitted to occur, at which point `mathcal{M}_{text{eff}}` terminates and the S4 branch formally
takes over.

## 3. Conditions for legitimate citation of the S3→S4 branch

The products of the S4 branch (full 3D description results) may be cited as boundary evidence for the S0→S2
verification chain only if the following conditions are met:

1. **Continuity condition**: The S4 solution must smoothly connect with the S2 solution on the `mathcal{M}{text{eff}}`
   boundary, i.e., `lim{epsilon to epsilon_{text{crit}}^-} Psi_{text{S4}} = lim{epsilon to epsilon_{text{crit}}^-} Psi_{text{S2}}`.
2. **Monotonicity condition**: The volume of `mathcal{M}{text{eff}}` must contract monotonically as `delta{text{geo}}`,
   `delta{text{phys}}`, `delta{text{info}}` are tightened, ensuring the convergence of the approximation range.
3. **Non-circularity condition**: The verification of the S4 branch must not rely on constraints already relaxed in
   the S0→S2 chain (such as C3 weak interaction preservation), avoiding circular reasoning.

## 4. Statement on the relationship with the S0→S2 chain

**Statement**: The S3→S4 branch is not a denial of the 2D-ification hypothesis, but an explicit solution for the
boundary conditions of the effective 2D-ification space `mathcal{M}{text{eff}}`. Any result within `mathcal{M}{text{eff}}`
may serve as a legitimate input for the S0→S2 chain; results outside `mathcal{M}_{text{eff}}` serve only as
references for boundary conditions and must not be used directly to verify the 2D-ification hypothesis itself.

---

*Content generated by AI*
