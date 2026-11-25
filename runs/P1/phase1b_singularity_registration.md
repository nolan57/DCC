# Phase 1b — pre-registration: coordinate-independent classification of the `f → 0` limit surface

**Written before the instrument is run.** Authorized by G-64-01 (round 64), which removed the
audit veto and permitted this line "with any mathematical tool, no route restriction, no
requirement to attach to an existing RQ item". Technical review only — not an RQ round,
not route execution, not a gate mark.

**Product**: `runs/P1/phase1b_singularity_results.txt`, emitted by
`src/p1_symbolic/phase1b_singularity.py` (`--write`), never transcribed.
**Instrument**: sympy under `/d/Applications/miniconda3/python.exe`.

**Governing inputs**: G-64-01 §3 (the mandate: Kretschmann, a curvature projection onto
timelike/null `u`, geodesic completeness, and a three-way classification); Phase 1
`phase1_symbolic_constraint_results.txt` (the Kasner control `f=t`, Kretschmann `=0`,
`g_zz→0`); `effective_2d_definition_v1.md` §5 reason 2 ("`L_z=0` is a geometric
singularity"); `docs/decisions/G0p_seven_row_verdict_v3.md` row 1 and
`reports/DCC_terminal_answer_v1.md` row `G0′` ("no reverse-on stated — geometric,
convention-independent").

## 1 Scope and fixed conventions

- Metric: `ds² = −dt² + dx² + dy² + f²(t,x) dz²`, `f>0`, signature `(−,+,+,+)`,
  `c=1`. This is the **initial simplified model** `f(t,x)`; the `f(t,x,z)` extension
  and other metrics are out of scope and are not implied.
- The `z` domain topology is **not assigned** by this review (Phase 1 §1). Whether the
  limit surface is a horizon, a pinch, or a boundary depends on that domain; the
  instrument reports the domain-dependent qualification and does not choose.
- No stress-energy, no field equations, no matter model. This review classifies the
  **geometry only**. It says nothing about whether any matter state survives the limit.

## 2 Hand estimates fixed before the run

1. Kretschmann for `f(t,x)`: `K = 4(f_tt² + f_xx² − 2 f_tx²)/f²`. No first-derivative
   terms survive; the `f=t^p` family gives `K = 4p²(p−1)² t^(−4)`.
2. Ricci scalar: `R = 2(f_tt − f_xx)/f`.
3. **The literal `R_abcd u^a u^b u^c u^d` is identically zero for every metric**, because
   `R_abcd` is antisymmetric in `(a,b)` while `u^a u^b` is symmetric. It cannot
   discriminate a singularity. The meaningful observer-curvature quantity is the
   electric tidal tensor `E_ab ≡ R_{a c b d} u^c u^d` (two vectors, not four).
   Reporting the vanishing of the four-`u` contraction is an **IDENT**, not a CHECK,
   and the instrument must not present it as evidence.
4. Comoving `u=∂_t`: `E_zz = −f f_tt`, `E_ab E^ab = f_tt²/f²`.
5. Boosted along `z` with `u=(coshη,0,0,sinhη/f)`: `E_zz = −cosh²η · f f_tt`,
   `E_xx = −sinh²η · f_xx/f`. Null `(t,z)`: `E_xx = −f_xx/f`, `E_zz = −f f_tt`.
6. Kasner control `f=t`: `K=R=E=0` everywhere while `g_zz=t²→0` at `t=0`. The surface
   is at least a **coordinate degeneration**; flatness makes a curvature singularity
   impossible there. Whether `t=0` is a horizon or an extendable regular surface
   depends on the `z` domain and on how the metric is continued for `t<0`.
7. Generic power law `f=t^p`, `p≠0,1`: `K ∝ t^(−4) → ∞` at `t→0` — a genuine
   **curvature singularity**, independent of coordinates and of the `z` domain.
8. Geodesic completeness is decided by the affine parameter, not by `K` alone. For the
   Kasner slice a `z`-directed geodesic reaches `t=0` at finite affine parameter
   (Rindler-type horizon of flat space) yet the spacetime is extendable; for `p≠0,1`
   the divergent tidal tensor at finite affine parameter makes the surface a true
   singularity. The instrument reports both facts without conflating them.
9. Expected result class: **coordinate-invariant classification of the `f→0` limit
   surface for this metric family**, conditional on (i) the metric family and (ii) the
   undeclared `z` domain. It is NOT a matter-survival verdict, NOT a reopening of any
   gate, and NOT a proof that physical `L_z=0` is attainable.

## 3 Predicates (checked by the instrument)

| # | prediction | bar |
|---|---|---|
| `SG1` | `K = 4(f_tt²+f_xx²−2f_tx²)/f²` | exact `simplify == 0` residual |
| `SG2` | `R − 2(f_tt−f_xx)/f = 0` | exact |
| `SG3` | `R_abcd u^a u^b u^c u^d = 0` for arbitrary `u` | exact; **IDENT** (not evidence) |
| `SG4` | comoving `E_zz + f f_tt = 0`; `E_ab E^ab − f_tt²/f² = 0` | exact |
| `SG5` | boosted/null tidal components match §2.5 | exact |
| `SG6` | Kasner `f=t`: `K=R=E=0` while `g_zz=t²→0` | exact zero; degeneration recorded |
| `SG7` | `f=t^p`: `K = 4p²(p−1)² t^(−4)`; `p=1 → 0`, `p=2 → 16 t^(−4)` | exact |
| `SG8` | three-way classifier fires the correct slot on the controls | classification rule, reported |
| `SG9` | no gate / terminal class / threshold / queue / RQ state is written | procedural, verified after run |

## 4 Decision rules fixed before the run

- `CHECK` = symbolic identity; `IDENT` = definition or antisymmetry statement (not
  evidence); `NEGCTRL` = the Kasner and power-law controls. Reported separately.
- Any `SG1`–`SG7` failure is a pre-emission defect: fix the instrument or disclose
  the mismatch in product and registration **before** `--write`. No bar relaxation.
- `OVERALL` is `PASS` only if all seven symbolic predicates pass. `SG8`/`SG9` print
  their own status.
- The classifier has exactly three slots: **CURVATURE-SINGULARITY** (invariant diverges),
  **COORDINATE-HORIZON / EXTENDABLE** (invariants finite, surface reachable, extension exists),
  **UNDETERMINED** (domain or continuation not declared). It may not return a fourth
  verdict, and it may not mark a gate.
- `PROVENANCE: NEITHER` — coordinate-invariant analysis, not chain evidence.

## 5 Pre-emission corrections (disclosed before `--write`)

Two implementation defects were found in dry runs and fixed before the product was emitted;
the registered bars and hand estimates were **not** changed:

- **D1** `kretschmann()` and `ricci_scalar()` used `len(sympy.Matrix)`, which returns the
  element count (16) rather than the row count (4), producing an out-of-range index on the
  first dry run. Fixed to use `.rows`.
- **D2** The first `ricci_scalar()` contracted two lower indices, `rdn[a][b][a][c]`, which is
  not a valid tensor contraction (`SG2` FAILED with an extra `(f²−1)(f_tt+f_xx)/f` term).
  Fixed to `g^(ae) R_{e b a c}`, reproducing the hand estimate `R = 2(f_tt−f_xx)/f` exactly.

Neither correction changed a physics conclusion: the hand estimate was right in both cases,
and no bar was relaxed.

## 6 Prohibitions

- No claim that `f=0` is attained by a physical process; no `f_min`, `ΔE_z`, `300 s`.
- No claim that matter survives or that `L_z=0` is reachable; no Model B/C spectrum.
- No claim about `f(t,x,z)`, BSSN/Z4c, or front stability — those remain Phase 3.
- No edit to `effective_2d_definition_v1.md` §5 or `G0p_seven_row_verdict_v3.md`; any
  consequence for the "`L_z=0` is a geometric singularity" premise or the `G0′` row-1
  reverse-on is **reported, not applied** — it is triggered by the result, not by a
  ruling in this round.
- No archived text is edited; no erratum is created by this review.
