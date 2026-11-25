# Pre-registration — `GD6`, `φ` in `ME3`

**Registered**: 2026-11-22, before any code in this round ran.
**Object under test**: `ME3` as adopted in `docs/specs/meff_boundary_v0_2.md`,

```
delta_E := Int rho (d_z phi)^2 d3x  /  Int rho [ (d_x phi)^2 + (d_y phi)^2 ] d3x  <=  delta_E,max
```

**The question of record** (`route_completion_v1.md` §6, `GD6`): is `phi` the material field, or a velocity
potential? The two give `1.69e26` and `5.93e-27` on the same state.

**What I am testing instead.** Whether the question has an answer at all. `GD6` presupposes that *some*
declaration makes `ME3` a criterion. That presupposition is testable and it is not the same question.

**Commitment.** These predictions are fixed here. The run is archived unedited, and a failed prediction stays
failed in the record.

---

## Predictions

| id | prediction | falsified by |
| --- | --- | --- |
| **P1** | `delta_E` is a **Rayleigh quotient**: invariant under `phi -> a*phi` for any `a != 0`, to `1e-12` relative. Hence `delta_E` carries no amplitude information and cannot be a "fraction" of anything without a normalisation the formula does not supply. | any `a`-dependence above `1e-12` |
| **P2** | For a **static** scalar on a slab of thickness `t`, `delta_E ~ lambda^k / t^k` with `k > 0`. Concretely, on the lattice with the fundamental lateral mode, the attenuation-corrected residual of `delta_E` against `(lambda/t)^2` is in `[1.000, 1.015]` for `t = 8,16,32,64`. | residual outside that band |
| **P3** | `ME3` with a static `phi` is **algebraically a minimum-thickness criterion**: `delta_E <= delta_E,max` is equivalent to `t >= t_min(delta_E,max)`, monotonically. It therefore *forbids thin objects*, i.e. it is a flatness prohibition. The identity holds on the lattice to `1%`. | any state where the criterion passes a thinner object than one it fails |
| **P4** | The archive's `1.69e26` uses `(lambda/t)^2`, but its *verified* test field is `sin(2*pi*x/lambda)*sin(pi*z/t)`, for which the exact result is `(lambda/2t)^2`. Ratio `4`. Both are `~1/t^2`, so the **direction is unaffected**; the quoted number's lateral **mode is undeclared**. Recomputation gives `1.6866e26` (fundamental mode) and `4.2166e25` (second mode). | either number not reproducing |
| **P5** | Branch II (velocity potential) on the record's only velocity field `u^mu = (c,0,0,0)`: reading it as a **frame** (matter at rest) gives `grad phi = 0`, hence `0/0`; reading it as a **flow** (`u_x = c`) gives numerator `0` and denominator `rho c^2 V > 0`, hence `delta_E = 0` **exactly**. The archive reports only the second. Both readings are degenerate. | a reading that produces a finite, object-dependent value |
| **P6** | Therefore the velocity branch **discriminates nothing**: `delta_E` is the same (`0`, or undefined) for every object, so **no state can fail** and `delta_E <= delta_E,max` is satisfied by all states for every positive threshold. Variance across three distinct objects = `0`. | non-zero variance |
| **P7** | **Exhaustion, no fourth branch.** Every reading of `phi` is static or kinematic. The static readings are three — material property, converted-region indicator (`phi_conv`), geometric level set (signed distance) — and **all three exponentiate positively** in `1/t`: `k = 2` (material), `k = 1` (indicator), `k = 1` (signed distance). All are inverted. The kinematic reading is degenerate (P5). | a fourth class, or a static reading with `k <= 0` |
| **P8** | Signed-distance reading on a solid cylinder of radius `R`, thickness `t`: `|grad phi| = 1` a.e., numerator `= 2*pi*R^2` (the two faces, `n_z = +-1`), denominator `= 2*pi*R*t` (the rim, `n_z = 0`), so `delta_E = R/t` **exactly**. Measured on a discretised cylinder to `2%`. | measured value off `R/t` by more than `2%` |
| **P9** | Phase 3 was **already deleted**, not blocked, by `exhaustive_matrix_route_v1.md` §`GD6` ("Phase 3 is deleted rather than answered"). So retiring `ME3` removes no live deliverable and blocks no live phase; it *formalises* a deletion already made. | a live phase that depends on `ME3` |
| **P10** | My own `D-6` — "`GD6` is the critical path … the only open item whose resolution could put a measured quantity into a site" — is a **category error**. `delta_E` is one scalar per *configuration*; a site holds `(k,n)`. Therefore `I(site ; delta_E) = 0`, and this is **already measured**: `DEPOSIT-BLIND` found one digest for six geometrically distinct objects. Test: two objects with `delta_E` differing by `2^k` give one deposit digest. | a non-zero `I(site ; delta_E)`, or two digests |

## What each outcome licenses

- If `P1`–`P4`, `P7` hold: `ME3` is **inverted for every static `phi`**, so `GD6`'s "material" branch is not a
  declaration choice but a misreading, and `GD6`'s dichotomy is **not exhaustive** — there is a third static
  reading, and it fails the same way.
- If `P5`–`P6` hold: the kinematic branch is **degenerate**, so the one reading with the right sign is
  non-discriminating.
- `P5` + `P6` + `P7` together ⇒ **no declaration makes `ME3` a criterion** ⇒ `GD6` closes as **neither**, and the
  defect is located in the functional, not the symbol.
- If `P10` holds: `D-6` is withdrawn, and the critical path returns to `G6`/`DC2` — the item §9 already named.

## Declarations fixed in advance

- Lattice: 2nd-order central differences, interior points only, unit spacing.
- `lambda = 8` cells for the scaling test (matching `p3_me3_results.txt`, so the attenuation constant is
  comparable).
- Slab objects for `P3`/`P7`: `64 x 64 x t`, `t` in cells.
- No constant is back-solved from a desired verdict. If a number is needed to make something pass, it is not
  registered.
