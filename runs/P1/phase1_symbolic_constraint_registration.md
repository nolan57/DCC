# Phase 1 — pre-registration: pure symbolic ADM constraint-closure review

**Written before the instrument is run.** Technical review only; not an RQ round, not route execution.
Authorized by the governor's “GO” after the v2.1 conditional acceptance. The permitted task is the
Phase 1 **pure symbolic and constraint-closure review**, not a numerical simulation.

**Product**: `runs/P1/phase1_symbolic_constraint_results.txt`, emitted by
`src/p1_symbolic/phase1_constraint_closure.py` (`--write`), never transcribed.
**Instrument**: sympy 1.14.0 under `/d/Applications/miniconda3/python.exe`.

**Governing inputs**: `docs/decisions/hard_sf_effective_2d_route_candidate_v2_1.md` §1.1, §1.3, §4;
`DCC_Covariant_Reconstruction_v1.md`:72 (signature `(-,+,+,+)`, `ℏ=c=1`, `κ=8πG`),
:161 (`K_ij=−(1/(2N))∂_t γ_ij`), :163–164 (Hamiltonian / momentum constraints);
`DCC_Macro_2D_Execution_Spec_v1.2.md`:90–108 (plane-symmetric `B(t,x)` = z scale factor);
`Macro3D_to_2D_Smooth_Reduction_Roadmap_v1.4.md`:100–105 (inverse problem is necessary, not sufficient),
:277–284 (Model B/C spectra must not be mixed).

## 1 Scope and fixed conventions

- Metric under review: `ds² = −c²dt² + dx² + dy² + f²(t,x)dz²`, with `f>0`; set `c=1`, `N=1`,
  shift `β^i=0`, so `g_zz=f²`. This is the **initial simplified model**: `f` does not depend on `z`.
  The `f(t,x,z)` extension is **out of scope** for this review.
- `z` domain is **not assigned** by this review. The instrument reports the domain-dependent
  qualification only; it does not choose `[z₁,z₂]`, `ℝ`, or `S¹`.
- No stress-energy source is declared. Therefore the instrument derives the **required** source
  `(ρ_req, j_x,req)` and does **not** claim that any physical field supplies it.
- Symbol hygiene: `f` here is the metric scale factor only; it is never the Maxwell `F_xy`.

## 2 Hand estimates fixed before the run

These are analytic hand estimates; the instrument must reproduce them or disclose the mismatch
as a pre-emission defect. `H_z ≡ ∂_t f / f`.

1. Spatial metric `γ_ij=diag(1,1,f²)` with `f=f(t,x)` gives
   `R⁽³⁾ = −2 f_xx / f` (no `f_x²` term survives).
2. With `K_ij=−½∂_t γ_ij`: `K_zz=−f f_t`, `K = −H_z`, `K_ijK^ij = H_z²`, hence
   `K²−K_ijK^ij = 0`.
3. Hamiltonian constraint `R⁽³⁾+K²−K_ijK^ij−2κρ=0` therefore reduces to
   `κρ_req = −f_xx/f`.
4. Momentum constraint `D_j(K^j_i−δ^j_iK)−κj_i=0` gives
   `κj_x,req = ∂_x H_z = ∂_x(f_t/f)` and `j_y=j_z=0`.
5. Vacuum requires simultaneously `f_xx=0` and `∂_x(f_t/f)=0`. Homogeneous `f=f(t)` always
   satisfies this, so the homogeneous slice is constraint-vacuum; this is **not** evidence that
   a contracting front can be sourced.
6. Kasner control `f=t`: the 4D spacetime should be flat (Kretschmann `=0`) while `g_zz→0` at
   `t=0`. This separates coordinate degeneration from curvature singularity.
7. Expected result class: **constraint-satisfying solution with a required source**, at best.
   It cannot be an evolution solution or a joint solution, because no field equations or matter
   model are supplied.

## 3 Predicates (checked by the instrument)

| # | prediction | bar |
|---|---|---|
| `SY1` | `R⁽³⁾ + 2 f_xx/f = 0` identically | exact `simplify == 0` |
| `SY2` | `K_zz = −f f_t`, `K = −H_z`, `K_ijK^ij = H_z²`, `K²−K_ijK^ij = 0` | all exact |
| `SY3` | Hamiltonian residual vanishes iff `κρ = −f_xx/f` | exact |
| `SY4` | `κj_x = ∂_x(f_t/f)`; `j_y = j_z = 0` | exact |
| `SY5` | vacuum equivalence: `ρ=0 ∧ j_x=0 ⇔ f_xx=0 ∧ ∂_x(f_t/f)=0` | logical, both directions printed |
| `SY6` | homogeneous `f=f(t)`: `ρ_req=j_x,req=0` | exact |
| `SY7` | Kasner control `f=t`: 4D Kretschmann `=0` while `g_zz→0` at `t=0` | exact zero; degenerate limit recorded |
| `SY8` | required source is **not** identified with any declared field; result class ≤ “constraint-satisfying solution” | reporting rule; no numeric bar |
| `SY9` | no gate mark, terminal class, threshold, queue item or ledger-linked RQ state is written by this instrument | procedural, verified after run |

## 4 Decision rules fixed before the run

- `CHECK` = symbolic identity passes; `IDENT` = definition/convention statement, not evidence;
  `NEGCTRL` = Kasner control. They are reported separately; no `IDENT` counts as a `CHECK`.
- Any `SY1`–`SY7` failure is a pre-emission defect: fix the instrument or disclose the mismatch
  in the product and registration **before** `--write`. Bar relaxation after a miss is forbidden.
- `OVERALL` is `PASS` only if all seven symbolic predicates pass. `SY8`/`SY9` are reporting and
  procedural predicates and are printed with their own status.
- `PROVENANCE: NEITHER` — this is a symbolic review; it is not chain evidence and adjudicates no gate.

## 5 Prohibitions

- No numerical simulation, no `f_min`, `ΔE_z`, `300 s` or any other threshold assignment.
- No Model B/C spectrum borrowing; no claim about bounded `z` eigenmodes from this metric alone.
- No claim that a healthy field supplies `ρ_req` or `j_x,req`; no claim of front formation,
  forward existence, stability, NEC/WEC satisfaction, or SI pressure value.
- No `Kretschmann` claim for general `f(t,x,z)`; only the declared `f(t,x)` model and the `f=t` control.
- No archived text is edited; no erratum is created by this review unless a later governing action requires one.
