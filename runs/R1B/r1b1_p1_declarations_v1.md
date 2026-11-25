# R1B1-P1 — Declarations v1 (round 44): P1-A, P1-C, and the closure certification inputs

**Status**: third `R1B1-P1` theoretical product. **Numerics remain vetoed**; nothing here computes a
state — it declares, with evidence tags, everything the closure certification (§ of
`docs/decisions/r1b1_p1_closure_certification_v1.md`) needs.
**Trigger**: governor directive (round 44): complete all remaining tasks unilaterally — executed within
governance: every task completable without the veto lift is completed here; everything else is driven to
a named, falsifiable terminal disposition.

---

## §1 `P1-A` — degree-of-freedom closure (declared)

| DOF | template (spec §5 of the Dirac closure) | status |
|---|---|---|
| electrons | **ALL3D template retained as the working declaration** — the operator is derived and verified (`DIRAC-KINEMATIC`); the ALL2D confinement alternative would carry the `K4` zero-point cost and is not selected by this declaration | explicit; the z-disposition question is a **state question (Phase 2/3)**, not a set-closure question — carried `UNRESOLVED` with its tool now built |
| nucleons | ALL3D template; structureless at the kinematic level — **declared approximation**, adequacy a Phase-2 output | explicit |
| internal nuclear DOF | not required by the declared interaction class below (§2) at the declared densities; if the Phase-2 census contradicts this, the declaration is revised, not silently dropped | declared-with-condition |
| EM field | dynamical, fully verified (round-42/43 products) | closed |
| neutrinos | **the weak fork is declared, both branches, with consequences** — the choice between them is physics (Phase 2), not convenience: (i) *weak-off*: electron number conserved; the composition is frozen non-equilibrium; the β-equilibrium sequence does not apply; (ii) *weak-on*: β-processes convert `n ↔ p + e⁻ + ν̄_e`; the ν-sector must then be declared either dynamical (lepton number conserved) or free-escape (an open loss channel; the ν budget remains a non-citable placeholder, verdict v3 §5) | fork declared |
| collective/geometric DOF | geometric `B(t)` prescribed (§2 spec); back-reaction is `G3′`'s question | declared |

**`S-STATE-6` timescale — proposed definition (resolves the last `UNRESOLVED` in the S-STATE table,
subject to adjudication):** the metastability reference timescale is the **conversion clock**
`τ_conv = √2 L/c` (an identity; `Λ_max` retired) together with the dynamical relaxation scale
`1/c_s` — the candidate final state must be metastable over the front-sweep duration and its own
relaxation time, otherwise "the final state" is undefined. Rationale: these are the only
observer-independent timescales the record contains; the rendering route (the alternative source of an
"observation timescale") is closed by theorem.

## §2 `P1-C` — nuclear interaction model declaration (declared, with named limitations)

**Declared candidate class**: the cold, sub-saturation neutronized-matter frameworks used for
neutron-star crusts, anchored as follows (literature-grounded, this round):

| framework | declared domain | source |
|---|---|---|
| Baym–Pethick–Sutherland (1971) outer-crust EOS | cold catalyzed matter below neutron drip `≈ 4.3×10¹¹ g/cm³` | [ADS: BPS 1971](http://ui.adsabs.harvard.edu/abs/1971ApJ...170..299B/abstract) |
| Baym–Bethe–Pethick (1971) / Negele–Vautherin (1973) inner-crust EDF | inner crust from neutron drip to the crust-core transition — the NV local EDF was constructed for exactly this band; later work takes the boundary at `0.1 fm⁻³` | [Chamel & Haensel 2008 review; NV, Nucl. Phys. A207](https://arxiv.org/abs/nucl-th/0611043) |
| chiral EFT neutron matter (NN+3N) | few-percent truncation uncertainty at and below `n₀`, growing above `2n₀` — the anchor for the uniform-matter sector | [Göttling et al., arXiv:2512.19593](https://arxiv.org/pdf/2512.19593); [Tews et al. review](https://link.aps.org/doi/10.1103/r314-6r62) |

**Applicability against the target regime** (`n_B = 0.021–0.042 fm⁻³ ≈ 3.5–7×10¹³ g/cm³`, the `K1`
window): **inside the declared domains** — this is inner-crust density, between neutron drip
(`≈ 2.6×10⁻⁴ fm⁻³`) and half saturation; χEFT's reliable band covers it.

**Named limitations (each a condition, not a hidden assumption):**

1. **Cold catalyzed assumption**: the fitted equilibrium sequences assume `T = 0` β-equilibrated matter.
   `K5`'s no-scale-separation makes the DCC compression violently non-adiabatic — under **weak-off** the
   composition is frozen non-equilibrium and the *equilibrium sequence* does not apply (the nucleon
   interaction sector retains applicability; the sequence does not). Under **weak-on** the equilibrium
   framework applies with the neutronization history computed, not assumed.
2. **State-structure inapplicability**: the crust models assume a 3D nuclear lattice; the DCC endpoint
   is a `1.68–1.99 fm` layer with the fixed baryon column — the models supply the **interaction/EDF
   anchor**, not the final-state configuration (that is `R1B1-P2`'s computation).
3. **Many-body corrections and known errors**: EDF-level (HFB-anchored) with χEFT few-percent anchor
   uncertainties at these densities; the neutron-drip and crust-core boundary values carry model
   spread (e.g., `0.08–0.1 fm⁻³` for the crust-core boundary across the cited works).
4. **Applicability within the `K1` geometric range**: the interaction is local (EDF/NN) — the geometry
   enters through the state, not the interaction; the `L_z` quantization and the anisotropic background
   are `Layer-0/2` inputs, and the `√−g` measure and `1/B²` z-weights are carried by the verified
   kinematic operator (`DIRAC-KINEMATIC`).

**Verdict**: the interaction sector is **declared with credible applicability** — `P1-C` does **not**
end `UNRESOLVED`. This is a declaration of the interaction/EDF anchor and its domain; it is not an EOS
(the EOS is `R1B1-P2`, numerics).

## §3 Source-tag audit of this declaration

`P1-C` domain figures: `MEASURED` (external literature, cited above). The target-regime densities:
`DERIVED` (`N_B/L_z`, spec §3.1). The weak-fork consequences: `DERIVED` from the declared conventions
(spec §4.1). `S-STATE-6` timescale: `DERIVED` (record identities) + `ASSUMED`-pending-adjudication
(the *choice* of reference timescale). Nothing untagged.

*Content generated by AI*
