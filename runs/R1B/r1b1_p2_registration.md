# R1B1-P2 — Registration (static matter states / EOS) — PENDING VETO LIFT

**Round**: 44 (registration prepared at P1 closure). **Date**: 2026-11-23.
**Predecessor**: `docs/decisions/r1b1_p1_closure_certification_v1.md` (P1 outcome #1 — theoretical
closure certified), spec v1.1 §15.4, `runs/R1B/r1b1_p1_declarations_v1.md` (P1-A/P1-C),
`runs/R1B/r1b1_eos_results.txt` v2 (threshold precedents), `r1b1_eos_v3_results.txt` (envelope).
**Status**: `REGISTERED — PENDING VETO LIFT — NOT STARTED`. Per the governor's standing rulings
(rounds 41–43), **numerical computation is vetoed until the veto-lift adjudication**; this registration
is the interface's outcome-#1 deliverable and is executed only on that ruling.
**Domain**: the `L_z` scan over the `K1` valid computational domain `[1.68, 1.99] fm` (spec §2.3 role B),
with the registration baseline `L_z = 1.0 fm` (role A) reproduced for cross-check only; both weak-fork
branches (per the `P1-A` declaration), reported separately.

---

## 1. Predictions (thresholds fixed now; from the v2/v3 instrument precedents)

| id | claim | pass condition |
|---|---|---|
| **P2-1** | the predecessor β-equilibrium EOS endpoints are reproduced at the registration baseline, per convention | β-equilibrium residual `< 1e-6 MeV`; `μ_e` envelope endpoints within `±0.01 MeV` of the v2/v3 values (`24.96`, `6.73` MeV per convention) |
| **P2-2** | the energy functional is bounded below across the scan; a physically acceptable equilibrium exists | an energy minimum exists for every scanned `L_z` in both weak branches; **kill → if none exists in a branch, that branch records NO-GO** (valid outcome, same class as `G0′` row 1) |
| **P2-3** | causal sound speed | `c_s² < 1` at every scanned point |
| **P2-4** | monotone pressure | `P(n_B)` monotone increasing across the scan |
| **P2-5** | the composition census (`N7-SPLIT` implemented) | `X_p ≥ 0` everywhere; the free/bound/trapped census table delivered per `L_z`; `n_Q,2D` vs `n_free,2D` reported separately, never equated |
| **P2-6** | the three-convention envelope (ALL3D / HYB / ALL2D) reproduced-or-revised **per convention** — single-point values forbidden (roadmap citation rule) | envelope endpoints reported per convention; any revision of a v3 endpoint is reported with its cause |
| **P2-7** | stability classes `S-STATE-1..4` per candidate state | conservation ledger closes; energy bounded; linearized spectrum without unacceptable growth modes; no immediate dissociation under nonlinear perturbation |
| **P2-8** | the `P1-C` interaction framework applied strictly within its declared domain | any quantity computed outside the declared domain (density/temperature/non-equilibrium excursion) is flagged and excluded, and the model is marked for revision — never silently used |
| **P2-9** | z-subband structure at the `K1` window | subband-spacing ratio `> 3` at every scanned `L_z` (verdict v3 §4 C5 precedent: `8.45` at the baseline), so the effective-2D reduction is self-consistent at the scanned thicknesses |

**Kill conditions (registered now).** (i) No bounded-energy state in a branch → that branch's NO-GO is
recorded as a valid physical conclusion. (ii) Interaction-domain excursion → flag, stop, revise the
declaration — no silent domain-stretching. (iii) Any numerical floor exceeding a claimed effect →
instrument repair before the claim (ledger rule). (iv) `S-STATE-3` growth modes → the state is marked
unstable and the result stands.

## 2. What this phase does not do

- It produces no `σ_s`, no `f_intra`, no `τ` (those are `R1B1-P4`).
- It makes no visibility claim and no statement about `G6` beyond the standing NO-GO.
- It does not relax `S1`–`S15` v1.3, does not touch the inherited prohibitions (spec §14.4), and does
  not widen any threshold above after a measurement.

## 3. Entry condition

Execution begins only on the governor's **numerical-veto-lift adjudication**. Everything else — the
scan grid, the branches, the thresholds, the kill conditions — is fixed by this registration before
any computation, per the pre-registration discipline.
