# Scene card -- W2-RL1-01

PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (section 6.1 item 6, sections 4.3/4.4/4.7/5.1).
PROVENANCE: NEITHER

**Item**: 6.1(6) `RL-1` measurement: `Q3` at `θ_fast` on the deposit's own 2D-ified scene.

## Stipulated inputs
- object: row 2 (`C1 C2 ¬C3`) at `t_mid` = 4.0993412372709514e-09 s; front z = 0.869 m.
- field: `plate`: tissue-density index of the axial slice at the front; `canvas`: per-site mean layer density.
- mechanism: one atomic-layer slice (`δ = 0.215 nm`); same map `M` as W1-ROW2.
- constraints: `C1` HELD, `C2` HELD, `C3` VIOLATED (imported 3 ns transient).
- observer `θ`: `q` is the declared channel factor; band = declared density channel (no spectral measurement);
  gate = none; aperture = none; distance = none.
- `E`: declared density field; no radiance environment is substituted, and no `E1` zero-contrast default is used.
- `G`: `G_A` specular-coupled, local normal at zero incidence in the surface frame, `δ_v = 0.01` rad. The
  registered `Q3` estimator has no angular variable, so this pose is declared but integrated out; the result is
  a channel contrast, not evidence that the scene is legible from any particular geometry.
- seed: none (deterministic phantom; null seeds 4000..4015).
- effective 2D: NOT-MEASURED; missing slot = registered confining-potential model; no `IS_2D`/`LOOKS_2D` claim.

## Derived outputs owed
`C_xi` on the row-2 plate, `C*` from the registered flux chain, `q(θ_fast)`, `Q3` at `θ_eye`, `θ_ideal` and
`θ_fast`, the full T0-T3 profile against W1-ROW2, and the kill-condition verdict.
