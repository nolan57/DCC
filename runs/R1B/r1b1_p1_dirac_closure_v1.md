# R1B1-P1 — Dirac-Operator Closure v1 (round 43)

**Status**: second `R1B1-P1` theoretical product, under `runs/R1B/r1b1_p1_registration.md` (`IN PROGRESS —
THEORETICAL`). **Numerics remain vetoed** (`P1-CLOSURE-FAIL`); the only tool is the CAS algebra checker
(`src/r1_dense/r1b1_p1_dirac_check.py` → `runs/R1B/r1b1_p1_dirac_check_results.txt`, **11/11 symbolic
identities VERIFIED**, CHECK/IDENT classified in the product).
**Mandate** (governor, round 42): *"The next step only advances the Dirac operator and the variational
consistency of the same action. No simulation code, no EOS, no conductivity, and the numerical veto is
not lifted."* The 9-step order below is the governor's own.
**Two-level ruling recorded** (governor, round 42): the round-42 results are **kinematic** — background
geometric kinematics, anisotropic fluid conservation structure, `B-WORK-TERM`, Maxwell geometric
structure — all *Passed*; the microscopic Dirac operator, nuclear interaction closure, and the full
microscopic action closure were ruled *Incomplete*. **Kinematic closure ≠ dynamical closure; the
`P1-CLOSURE-FAIL` veto lifts only on dynamical closure** (spec §15 amendment, this round).

---

## §1 Step results (the governor's 9 steps, in order)

| step | result | check |
|---|---|---|
| 1. orthonormal tetrad | `θ^a = (dt, dx, dy, B dz)`; `e_3 = (1/B)∂_z` — declared, inverse verified | D2 |
| 2. spin connection | **only two nonzero forms**: `ω_z^{3}{}_0 = ω_z^{0}{}_3 = Ḃ` — Cartan and tetrad-postulate agree | C3 |
| 3. curved Dirac operator | `γ^μ = e^μ_aγ^a` with `γ^z = γ³/B`; `{γ^μ, γ^ν} = 2g^μν` (C2); spinor connection **`Ω_z = −(Ḃ/2)γ⁰γ³`** — uniquely fixed by `∇_μγ^ν = 0` over all 16 (μ,ν) (the opposite sign fails) | C4 |
| 4. minimal EM coupling | `D_μ = ∂_μ + Ω_μ + iqA_μ` — gauge convention `ψ' = e^{+iqλ}ψ`, `A'_μ = A_μ − ∂_μλ` declared and verified | C9 |
| 5. Dirac equation → Hamiltonian | **EOM form fixed by the mass shell**: `(iγ^μD_μ ± m)ψ = 0` is **REJECTED** — in this signature it gives `H² = p² − m²` (unphysical, archived in the check product); the physical form is **`(γ^μD_μ + c_m m)ψ = 0`** | C5 |
| 6. `Ĵ` and `T^μν` from the same action | `j^μ = −ψ†γ⁰γ^μψ` (real, `j^t = ψ†ψ`); `T^μν` variation formula cited with all ingredients verified (`∇_μ`, `γ^μ`, `D_μ`, `√−g`); component-level `∇_μT^{μν} = F^{νλ}J_λ` is the registered `P1-B` remainder | — |
| 7. local U(1) gauge invariance | the `±iq∂_μλ` terms cancel exactly for all four `μ` (Ω commutes with the scalar phase) | C9 |
| 8. covariant current conservation | **norm/continuity master identity**: `H† − H = I(Ḃ/B)𝟙`, so `Ḃ𝟙 + iB(H† − H) = 0` — `d/dt∫B ψ†ψ d³x = 0` on solutions; spatial part standard with checked ingredients | C7 |
| 9. limits | `B ≡ 1`: flat Dirac Hamiltonian `−α·p + ic_mγ⁰m` recovered (C8a); `Ḃ = 0`: static anisotropy, z-kinetics weighted `1/B`, no identity term (C8b) | C8 |

**The fixed Hamiltonian** (`c_m = ±1` conventional — particle/antiparticle labeling, a chiral rotation):

```
H_D(t) = −(α_x p_x + α_y p_y + (α_z/B(t)) p_z) + i c_m γ⁰ m − (I/2)(Ḃ(t)/B(t))·𝟙
```

The `Ḃ`-term is a **pure identity** — the measure-compensation term: it makes `∫B ψ†ψ d³x` conserved
and is the exact 1-dimensional analogue of the FLRW `−(3iH/2)𝟙` (same `(n/2)H` structure, `n = 1`).

## §2 What the mass-shell rejection adds

The `(iγ^μD_μ ± m)` form is not a typo risk to be warned about — it was **constructed, tested, and
rejected by the checker**: in this signature it yields `H² = p² − m²` (archived in the results file).
The physical form `(γ^μD_μ + c_m m)ψ = 0` was then verified: flat mass shell `H_flat² = (p²+m²)𝟙` for
both `c_m` (C5), and the on-background decomposition (C6) is exact:

```
H = −(α_x p_x + α_y p_y + (α_z/B)p_z) + ic_mγ⁰m − (I/2)(Ḃ/B)𝟙
```

with `Tr(H)/4 = −(I/2)(Ḃ/B)` — the identity coefficient read off the trace, so nothing is assumed about
the `Ḃ`-term's form; it is *extracted*.

## §3 The convention set (fixed by the master checks, documented once)

| item | fixed value | fixed by |
|---|---|---|
| signature, `c` | `(−,+,+,+)`, `c = 1` (restoration mechanical) | declared |
| γ-representation | Dirac rep as coded | C1 |
| EOM form | `(γ^μD_μ + c_m m)ψ = 0` | C5 mass shell (the `(iγ^μD_μ ± m)` form rejected) |
| spinor connection | `D_μ = ∂_μ + Ω_μ`, `Ω_μ = (1/4)Σ_{a<b}ω_{μab}[γ^a,γ^b]` | C4 (`∇_μγ^ν = 0`, 16/16; the opposite sign fails) |
| gauge | `ψ' = e^{+iqλ}ψ`, `A'_μ = A_μ − ∂_μλ`, `D_μ = ∂_μ + Ω_μ + iqA_μ` | C9 declared+verified |
| `c_m = ±1` | mass-sign labeling | conventional (chiral rotation) — IDENT-level |

## §4 Physics readings — with the round-42 qualifications carried

- **The identity term is measure compensation, not dissipation** (governor §III, carried): it is not
  resistive loss, scattering, current relaxation, or absorption-weight transfer. It makes the
  `B`-weighted norm conserved; the matter subsystem's coordinate energy is **not** conserved under the
  prescribed geometry — that is `B-WORK-TERM`, and the two statements must not be conflated.
- **No z-mode mixing** — a round-42 wording correction (governor's frame-mechanics caution): `B(t)`
  depends on `t` only, so `[H_D, p_z] = 0` and **`p_z` remains a good quantum number**. The non-adiabatic
  content is the explicitly time-dependent `1/B(t)` weight in the mode energies plus the measure term —
  Phase 3's subject, with the operator structure now closed (round-42's "Ḃ drives transitions between
  z-modes" is superseded by this precise statement).
- **Frame dependence** (governor §III): the round-42 transverse damping `−(Ḃ/B)E_⊥` is a
  *coordinate-component* statement. Phase 3 must track **local orthonormal-frame fields** (spec §8
  amendment, this round). The Dirac-sector analogue — the identity term — is frame-safe: it is the
  measure compensation itself.

## §5 The z-handling of the three conventions (declared, per governor round-42 §"next step")

The operator above is the **ALL3D kinematic template**: every field carries z-kinetics with the `1/B(t)`
weight. The conventions are **not** three parameter values of one operator:

- **ALL3D** — the template as derived; all species 3D-in-z.
- **ALL2D** — z-kinetics replaced by a *declared confinement model* per field (a different operator,
  not a parameter); the confinement zero-point cost enters the `K4` ledger; if the confinement is
  obtained by **integrating out** z-modes rather than postulating 2D fields, the integrated sector owes
  the veto-item-7 five-point accounting (effective potential, `Ĵ` corrections, spectral weight).
- **HYB** — per-species assignment of the two templates above.

The `P1-A` declaration must state, per field, which template it uses and — for any integrated sector —
the five-point accounting. Nothing here pre-selects a convention.

## §6 Remaining `P1` items (named, with dependencies)

1. **`P1-C`** — the nuclear interaction model declaration: the gate on dynamical closure (`UNRESOLVED`
   admissible per the interface).
2. **Weak-fork declaration** (`P1-A`): electron-number conservation vs. ν-sector — both branches close
   kinematically; the choice is physics, not convenience.
3. **Component-level `∇_μT^{μν} = F^{νλ}J_λ`** for the Dirac field — the registered `P1-B` remainder
   (all ingredients verified; the variation formulas cited).
4. **Electron z-disposition** — `UNRESOLVED` per spec §3.2 (re-scoped); the operator here is the tool it
   will be examined with.

## §7 Status for adjudication

| item | status |
|---|---|
| kinematic closure (round 42) | **passed** (recorded, not expanded) |
| Dirac sector — operator, EOM form, Hamiltonian, identity term, gauge, limits | **verified, 11/11** |
| dynamical/action closure (full) | **not yet ruled** — gated on `P1-C` + the §6 declarations |
| numerics | **vetoed**, unchanged |
| `G6`/`DC2` | NO-GO, unchanged |

*Content generated by AI*
