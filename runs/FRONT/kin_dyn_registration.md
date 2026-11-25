# Registration — adjudication of proposed `R1 §4.6` (kinematic vs dynamic unfolding)

**Written**: 2026-11-22, **before** `src/route/kinematic_dynamic_check.py` existed.
**Subject**: a third submission: a new `§4.6 Kinematic Unfolding vs. Dynamic Unfolding`, a worked example on a
two-layer composite disc (`§4.6.1`), a consequence section (`§4.6.2`), and three cross-references.
**Registered verbatim**: `runs/FRONT/kin_dyn_submission_verbatim.md` (`PROPOSED`, governs nothing).

**Why this one is different from the first two.** `A6` and the `H_eff ≥ δ` insertion were both about a number.
This one is about a *category distinction*, and the distinction is right: D2 is a relabelling, not a dynamics.
The audit therefore separates three questions that the submission does not separate — is the distinction correct,
is the worked example correct, and does the example test the right counterfactual.

---

## Predictions

| # | Prediction | Tolerance |
| --- | --- | --- |
| `P1` | the prescribed map `Π: (r,θ,z) ↦ ((R/δ) r cosθ, (R/δ) r sinθ)` has image radius `R²/δ = 1.51e8`, while the prose says `R/δ = 8.37e8` — the formula and its own description differ by the factor `R` | ±2% |
| `P2` | `Π` implies an in-plane strain of `R/δ − 1 = 8.372e8`, whereas D2's registered in-plane map is the **identity** (`front_sweep_v1` §2 step ②), i.e. `0` | ±2% |
| `P3` | `8.372e8` is within `10%` of the `9.28e8` that `front_sweep_v1` §2 line 49 **already corrected** as "the displacement gradient of the mapping, not the strain of the material" — so the example reintroduces a corrected confusion | ±10% |
| `P4` | at a **bonded** interface, displacement and **traction** are continuous and **strain** jumps by `μ_1/μ_2 = 10`; the submission states the reverse ("displacement continuous but radial stress is not") | confirmed |
| `P5` | `t_radial / t_through-thickness = R/(2δ) = 4.19e8`, **independent of `μ` and `ρ`** — purely geometric | ±2% |
| `P6` | `t_radial / t_rip = 2.2e4` at `c_s = 1000 m/s`, i.e. the radial response is `4.3` decades slower than the conversion — so no radial dynamics is depictable in any frame at `t ≤ t_rip` | ±10% |
| `P7` | the submission's "core/mantle strain ratio `1:10`" is the **unbonded** (equal-stress) ratio; the bonded body it posits imposes a ratio strictly between `1` and `10`, so the summary table's own rows contradict each other | confirmed |
| `P8` | `T5` is already in force in `tier_admission_v1.md` (`"L3 is still empty under C1 in reflection"`), so the proposed `T5` is a label collision | confirmed |
| `P9` | `R1` contains no `§4.5.1` (0 occurrences), so the first and third cross-references are anchored to a refused section | exact 0 |
| `P10` | `R1` has no `§7` gap list — `§7` is "Correction 1" on the `C3` label | confirmed |
| `P11` | the labels "bone-like" (`10 GPa`) vs "soft-tissue-like" (`1 GPa`) misstate their contrast by `≥3` decades; soft-tissue shear moduli are `kPa`-scale, `10^4`–`10^6` below bone, not `10` | ≥3 decades |
| `P12` | the sentence "simultaneity across the body would violate causality" treats the map as a physical process, which is the conflation the section exists to forbid | confirmed |

`P5` and `P6` are the two predictions that can produce something new rather than a defect. If they hold, the
submission's own conclusion inverts: the kinematic/dynamic discrepancy is real but **not depictable** on the
conversion timescale.

---

## What would change the disposition

- `P2` false (D2's in-plane map is not the identity) → the worked example's `Π` may be legitimate and the
  ruling narrows to the continuity error;
- `P6` ≥ 1 (radial response faster than or comparable to `t_rip`) → the discrepancy would be observable and the
  scope note's warning becomes operative rather than moot.
