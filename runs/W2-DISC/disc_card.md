# Scene / closure card -- W2_DISC

PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (sections 4.2.3, 4.2.6, 4.8, 5.1, 6.1, Appendix D).
PROVENANCE: NEITHER

**Item**: 6.1(3) discretization control. **Type**: TECHNICAL closure, not an O0 artifact.

- baseline mechanism: one atomic layer per slice, delta = 0.215 nm (front_sweep_v1; a mechanism property, not a rendering knob).
- control mechanism: delta x 10 = 2.150 nm, same front law and same map M; registered as a DIFFERENT mechanism id, not a parameter edit (section 4.8).
- scene: row 2 (`C1 C2 not-C3`) at `t_mid` = 4.0993412373e-09 s; z_front = 0.869 m.
- constraints: C1 HELD, C2 HELD, C3 VIOLATED (imported 3 ns transient, unchanged by the control).
- observer: the declared instrumented channel q = 1; tiers T0-T3 from the locked estimators and thresholds.
- seed: none (deterministic phantom and null ensemble seeds 4000..4015).
- predicted direction: plate-scale tiers invariant; array-scale census and its tiers change because site count scales as 1/delta.

