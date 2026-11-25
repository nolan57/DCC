# Registration — numerical probe of the M_eff boundary draft v0.1

**Date**: 2026-11-22
**Status**: registered **before** execution
**Object under test**: `docs/specs/meff_boundary_v0_1.md` (the S3→S4 branch specification, draft v0.1)
**Product**: `src/s45_branch/meff_boundary_probe.py` → `runs/S45/meff_boundary_probe_results.txt`

## 0. Why a probe at all

The draft states four boundary constraints with tolerance symbols (δ_geo, δ_phys, δ_info) but
**no registered numerical values**, and one topological identity (χ(ε)=χ(0)). Three of its claims are
therefore not currently falsifiable. This probe does not test the *physics* of the branch — it evaluates
the draft's own formulas on the project's own registered object, so that the audit can say
"this constraint is vacuous / unattainable / scale-free" with a number instead of an opinion.

**No physical model is introduced.** Every input is either an identity already established in the record
or a definition from the draft itself.

## 1. Registered inputs (source of every number)

| Symbol | Value | Source |
| --- | --- | --- |
| `A_perp` | 0.040 m² | `docs/decisions/painting_render_v1.md` (`A_c = V/H = 0.070/1.75`) |
| `H_obj` | 1.75 m | same |
| `d_par` | 1.54e-14 m (= 15.4 fm) | roadmap §0.2 / §3.4 |
| `N_s` | 4.22e27 m⁻² | roadmap §0.2 |
| `N_frag` | 1.18e10 | `docs/decisions/front_sweep_v1.md` (1.457 comp/layer × 8.12e9 layers) |
| `a0` | 5.29177210903e-11 m | CODATA Bohr radius |
| `lam_obs` | 550e-9 m | visible band centre (draft's λ_obs, taken at its most favourable value) |
| `c` | 2.99792458e8 m/s | — |

Derived, not asserted: `E_F`, `σ_w`, `P_2D` are **not** used here; the probe is kinematic.

## 2. Registered checks and acceptance criteria

Each check carries a **criterion fixed now**. A check that fails its criterion nominates a defect in the
draft; a check that passes withdraws the corresponding defect.

| # | Question | Quantity | Criterion (falsifies the draft if…) |
| --- | --- | --- | --- |
| P1 | Is `ΔH` as defined *extensive* in base area? | `ΔH/A` in bits·m⁻², then `ΔH` for A and 10A | ratio of `ΔH` for A→10A lies in [9.5, 10.5] ⇒ **extensive confirmed** ⇒ a size-independent `δ_info` is not a well-formed threshold |
| P2 | Can `C_info` ever be met by the registered object? | shortfall `log10(ΔH/δ_info)` for `δ_info ∈ {1, 10³, 10⁶, 10¹²}` bits; critical area `A_crit = δ_info/(ΔH/A)` | if `A_crit(10¹² bit) < 1e-4 m²` ⇒ **no admissible `δ_info` covers the object**, `C_info` is unattainable as written |
| P3 | Are the draft's two statements of `C_geo` the same statement? | for `z=a·sin(kx)`: `λ_obs·max|z''|` vs `λ_obs/R_perp`, `R_perp = 1/(a k²)` | relative difference < 1e-10 ⇒ **they are the same statement**, so `δ_geo` is not an independent knob but a restatement of `R_⊥ > λ_obs/δ_geo` |
| P4 | Is `C_geo` ever *both defined and non-vacuous*? | `δ_geo` for (a) the converted plate (thickness `d_par`, lateral 5 cm) and (b) a 0.5 mm-radius surface ridge | both < 1e-2 ⇒ **vacuous wherever `z(x,y)` is defined** (curvature at visible λ is never marginal for a macroscopic object) |
| P5 | Does `χ(ε)=χ(0)` survive the project's own fragment census? | `χ_3D` (ball) vs `χ_2D` (contractible plates), and the converted fraction at which `χ` must already have changed | if `χ_2D/χ_3D > 1e6` then `C_top` holds only on `φ_conv ∈ [0, 1/N_frag]`, i.e. a set of measure ~1e-10 in `ε` ⇒ **`C_top` is false for essentially the whole branch** |
| P6 | Does any of the four constraints replace the established tearing bound? | `t_rip/(2L/c)` for `L ∈ {0.040^(1/2) m, 1 m}` | ratio = 1 to 1e-12 ⇒ **scale-free**: no geometric/informational/topological tolerance can substitute for an explicit lifetime constraint, which the draft does not contain |

## 3. What this probe cannot decide

- **It does not test `C_phys`.** `δS_⊥/S_∥` cannot be evaluated numerically without committing to a
  foliation and a sector; that objection is made analytically in the audit, not measured.
- **It does not set the correct values of `δ_geo`, `δ_phys`, `δ_info`.** It only shows that three of the
  four constraints, at *any* value, do not do the work the draft assigns them.
- **It says nothing about the branch's usefulness.** A constraint being vacuous is a defect in the
  specification, not evidence against the S3→S4 programme.
- It is a **kinematic arithmetic check at identity level**, not a physics result. Evidence level:
  **IDENTITY / ARITHMETIC**, capped there.

## 4. Discipline

Thresholds above are fixed before execution. Output is stdout only; no file I/O in the probe. All checks
are reported with explicit PASS/FAIL against the criteria in §2, including ones that clear the draft.

**Dependency versions**: python 3.13.12, numpy 2.4.6 (`requirements.txt`).
