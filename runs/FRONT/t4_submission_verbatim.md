# Submission 2 — proposed `R1 §4.5.1` and `T4`, registered verbatim

**Received**: 2026-11-22. **Registered**: 2026-11-22, before `src/route/t4_floor_check.py` was run.
**Status**: **PROPOSED — governs nothing, in force nowhere.** No line of this file is normative.
**Ruling on it**: `docs/decisions/t4_heff_floor_ruling_v1.md` (written after the run).
**Fidelity**: transcribed without correction, including arithmetic. Where the text contradicts the record, the
contradiction is a finding, not a transcription error — the same rule applied to `A6`.

---

## Insertion Point A — proposed `R1` §4.5.1

<!-- BEGIN-INSERTION-A -->

### 4.5.1 Lower Bound on H_eff

The single-layer thickness δ = H/N = 4.307e-10 m is not a free parameter. It is fixed by the stripping
prescription: N is the number of layers the object is divided into, and δ is the thickness of one such layer.
Since the stacking number k must be a positive integer, the effective z-thickness is bounded below:

    H_eff = k · δ ≥ δ = 4.307e-10 m

Equivalently, the stacking bound k_max(E) = (ħc/E)/δ imposes a hard cutoff. For any probe energy E, a valid
configuration exists only if k_max(E) ≥ 1, i.e. only if

    E ≤ ħc/δ = 2.9 keV

**Consequence.** H_eff < δ admits no valid deposition configuration. The DCC two-dimensionalisation therefore
cannot be pushed below δ; below this scale the model does not produce "thinner matter" but no configuration at
all. δ is the atomicity floor of the DCC construction — the thickness of one indivisible stripped layer.

This bound is independent of the tier battery. It follows from the stripping prescription alone and holds
regardless of whether any tier is sensitive to z.

<!-- END-INSERTION-A -->

## Insertion Point B — proposed `R1` §7, new entry `T4`

<!-- BEGIN-INSERTION-B -->

### T4 — Domain Boundary of the Framework Itself (H_eff ≥ δ)

**Nature.** Unlike T1/T2 (tiers inverting within specific domains) and T3 (tiers blind to a dimension), T4 is not
a measurement gap. It is a boundary of the model's domain of definition, derived from the stripping prescription
rather than from any tier output.

**Statement.** The stacking number k must be a positive integer. Since H_eff = k·δ with δ = 4.307e-10 m fixed by
the stripping, the effective z-thickness satisfies

    H_eff ≥ δ

Equivalently, the stacking bound k_max(E) = (ħc/E)/δ requires k_max ≥ 1 for any valid configuration, hence
E ≤ ħc/δ = 2.9 keV.

**Quantum-gravity regime is unreachable.** Pushing H_eff to the Planck length ℓ_P = 1.616e-35 m gives

    k_max = ℓ_P / δ = 1.616e-35 / 4.307e-10 = 3.75e-26

Since k_max < 1, no positive integer k satisfies the condition. There is no legal deposition configuration at the
Planck scale.

**Quantitative consequence — matter vanishes.** At H_eff = ℓ_P, the available volume for a macroscopic object of
cross-section A = L² = (0.18 m)² is

    V = ℓ_P · A = 1.616e-35 × 0.0324 = 5.2e-37 m³

against an original volume V_0 = L²·H = 0.0564 m³, i.e. V/V_0 = 9.3e-36. The number of atoms this volume can
accommodate, at lattice scale a ≈ 1e-10 m, is n = V/a³ = 5.2e-37 / 1e-30 = 5.2e-7. Fewer than one atom. At the
Planck scale the configuration does not contain thin matter — it contains no matter.

**Measurement is also impossible.** Resolving ℓ_P requires probe energy E ~ ħc/ℓ_P = E_Planck = 1.22e28 eV.
Concentrating this energy within a radius r makes the Schwarzschild radius of the region ≥ r, forming a micro
black hole that absorbs the probe. The measurement cannot be completed in principle.

| Quantity | k = 1 (materials regime) | Planck regime |
| --- | --- | --- |
| H_eff | 0.43 nm | 1.6e-35 m |
| k_max | 1 (valid) | 3.75e-26 (no valid integer) |
| Atoms accommodated | ~1 atomic layer | 5.2e-7 (fewer than one) |
| Probe feasibility | frozen below soft X-ray, measurable in visible | probe forms black hole; measurement impossible in principle |
| Physical state | effective 2-D matter | no matter, no measurement, no spatial definition |

**Relation to T3.** T3 states that the four tiers are insensitive to z. T4 states that z has a physical lower
bound set by δ, below which the framework has no solution. Together:

- δ is the atomicity floor of DCC (thickness of one stripped layer).
- H_eff < δ has no solution.
- The Planck regime lies 25 orders of magnitude below δ and is unreachable within the DCC framework.

Padmanabhan et al. (2016) D_eff → 2 and CDT spectral dimension 4 → 2 concern the Planck regime and therefore
cannot serve as evidence for DCC two-dimensionalisation. The two are not in the same physical interval.

**Closure condition.** T4 is not closable by adding tiers. It is a structural property of the stripping
prescription. It can only be relaxed by redefining δ — i.e. by changing N or the stripping rule — which would be a
change to D2 itself, not a patch to the tier battery. Until then, the DCC claim is bounded: effective
two-dimensionality holds for δ ≤ H_eff and E ≤ 2.9 keV. Below δ, the model has no solution; the limit is not
"completed two-dimensionalisation" but the simultaneous disappearance of matter and spatial definition.

<!-- END-INSERTION-B -->

## Cross-reference updates requested

| Location | Addition |
| --- | --- |
| `§4.5` self-consistent-point paragraph | Append: "k = 1 is also the minimal valid configuration; see §4.5.1 for the H_eff ≥ δ bound." |
| `§7` gap summary table | Add row: `T4` \| domain boundary, not measurement gap \| `H_eff ≥ δ`; Planck regime unreachable (`k_max = 3.75e-26`) \| not closable by tiers; requires redefining D2 |
| `annex_A §A.6` | Add cross-reference: "See `R1` §4.5.1 and `T4` for the lower bound `H_eff ≥ δ` and the unreachability of the Planck regime." |

---

*Content generated by AI*
