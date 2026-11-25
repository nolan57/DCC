# `GD6` — what `φ` denotes in `ME3`

**Ruling**: 2026-11-22
**Object**: `ME3` as adopted in `docs/specs/meff_boundary_v0_2.md`; `GD6` as registered in
`docs/decisions/route_completion_v1.md` §6.
**Pre-registration**: `runs/ME3/me3_phi_registration.md`, written before any code ran.
**Product**: `runs/ME3/me3_phi_results.txt` (310 lines), archived unedited with `E1`–`E5` appended.

---

## 0. Verdict

**`GD6` is CLOSED, and the answer is neither of the two declarations offered.**

`ME3`'s `φ` is a **velocity potential** — not by choice, but because the criterion's own name fixes it:
"perpendicular **energy** fraction" is an energy only if `φ` is a potential. The material reading was never a
declaration; it was a misreading, and it is what produced the inversion.

Once `φ` is fixed as a potential, `ME3` **has no verdict to give on any state the record contains**. So `ME3`
is **retired** for the `D2` route, `ME3-F1` is **closed** (the symbol is now declared), and `δ_E,max` is
**permanently unregistrable** for this functional — not pending, not open: there is no value to register.

**`8 / 11` predictions held.** `P2`, `P7`, `P8` are refuted, and all three are defects in *my test
specifications*, not in the object under test.

---

## 1. The question underneath the question

`GD6` asked: material field, or velocity potential? Both had been evaluated (`route_completion_v1.md` §4.1):

| declaration | sheet | body | direction |
| --- | --- | --- | --- |
| material field | `1.69e26` | `4.05e-1` | inverted |
| velocity potential | `5.93e-27` | `~1` | intended |

They differ by `(λ/t)⁴ = 2.8e52` and give opposite verdicts on the same state. The referee's instinct is to pick
one. This round tested the presupposition instead: **does any declaration make `ME3` a criterion at all?**

A criterion must be (1) well defined, (2) correctly signed, (3) discriminating, (4) instrumented. Six readings
were possible and every one fails:

| reading of `φ` | defined | signed | discriminating | instrumented | outcome |
| --- | --- | --- | --- | --- | --- |
| material property | yes | **no** (`k = 1.89`) | yes | yes | inverted |
| region indicator (`φ_conv`) | yes | **no** (`k = 0.95`) | yes | yes | inverted |
| geometric: L∞ distance | yes | **no** (`k = 0.43`) | weak | yes | inverted, weakly |
| geometric: Euclidean distance | **no** (divergent) | — | no | no | unbounded |
| velocity potential, rest frame | **no** (`0/0`) | — | no | no | undefined |
| velocity potential, flow `u_x = c` | yes | right sign | **no** (`= 0`) | no | vacuous |

Three failure modes, and they exhaust the space because a scalar on a body is either **static** (a property, an
indicator, or a geometry) or **kinematic** (a potential). The static readings are all `1/t^k` with `k > 0`; the
kinematic reading is identically zero.

---

## 2. Why the static readings are inverted — and it is algebraic, not numerical

`P1` measured that `δ_E` is a **Rayleigh quotient**: invariant under `φ → aφ` to `5.3e-13` across twelve decades
of amplitude. So it is a pure ratio of length scales, and the word "fraction" is not supplied by the formula — a
fraction needs a total, and there is none.

`P3` then showed what the ratio *is*. With `δ_E = C λ^k / t^k`:

```
δ_E ≤ δ_E,max    ⟺    t ≥ t_min := λ (C / δ_E,max)^(1/k)
```

The admissible set is **upward-closed in thickness**. A flatness criterion must be downward-closed. So `ME3`
with any static `φ` is a **minimum-thickness requirement**: it forbids thin objects. Applied to the real object
(`λ = 0.20 m`, `t = 1.540e-14 m`):

| `δ_E,max` | `t_min` | object |
| --- | --- | --- |
| `0.01` | `2.00 m` | FAIL |
| `1` | `0.200 m` | FAIL |
| `100` | `0.0200 m` | FAIL |
| `1e26` | `2.00e-14 m` | FAIL |
| `1.69e26` | `1.5385e-14 m` | **PASS** |

To pass, the sheet must be *thicker* than it is. That is the inversion, stated as a threshold condition rather
than as a number.

`P7` measured the exponent for all three static readings on a `64×64×t` slab:

| reading | `δ_E` at `t=8` | `δ_E` at `t=64` | `k` |
| --- | --- | --- | --- |
| material | `1.0242e0` | `2.1048e-2` | `1.886` |
| indicator | `1.8333e0` | `2.5385e-1` | `0.951` |
| L∞ distance | `2.9403e-1` | `1.1959e-1` | `0.433` |

All positive, so all inverted. **But the exponents differ, and my prediction of `k = 2, 1, 1` was wrong on the
third** — see `E2`. The miss is informative: the L∞ gradient is supported on **cones inside the body**, not on
its surface, so the geometric reading barely sees thickness and barely discriminates.

`P8` failed at the registered 2% tolerance by 30% (`0.3475` against `R/t = 0.5000`). And the Euclidean signed
distance is worse than inexact — by coarea,

```
∫_V (∂_z φ)² dV = ∫_0^∞ ∫_{φ=s} n_z² dA ds
```

which **diverges** in `s`. The geometric class is not "`R/t`, i.e. `ME2` restated"; it is an unbounded volume
integral. My analytic `R/t` was a surface-integral argument applied to a volume integral.

---

## 3. Why the kinematic reading is vacuous

The record's only velocity field is `u^μ = (c,0,0,0)`. Two readings, both degenerate (`P5`):

- **frame** (matter at rest): `∇φ = 0`, so numerator and denominator both vanish → `0/0`, *undefined*;
- **flow** (`u_x = c`): `∂_zφ = ∂_yφ = 0`, `∂_xφ = c ≠ 0` → numerator `0`, denominator `ρc²V > 0` → `δ_E = 0`
  **exactly**.

The archive reports only the second, as "`δ_E = 0` trivially". Reading the first is more natural — a 4-velocity
with no spatial part *is* a rest frame — and it is undefined rather than zero. Either way (`P6`): the value does
not depend on the object. **Variance across a sheet, a body and a column: `0`.** Any positive threshold admits
all three, so nothing can be rejected, so it is not a criterion.

That is the point `GD4` never reached: the branch with the right sign is the branch with no content. The
perpendicular *velocity* of a static configuration is zero, so a criterion for small perpendicular velocity is
satisfied by every configuration, including ones that are not flat at all.

---

## 4. The archive defect this round found

`route_completion_v1.md` §4.1 says, in one paragraph, both of these:

> with `φ = sin(2πx/λ)·sin(πz/t)`, `δ_E = (λ/2t)²`, confirmed on `t = 8, 16, 32, 64`
> … for the real object: `(λ/t)² = 1.687e26`

The tested field gives `(λ/2t)²`; the extrapolation uses `(λ/t)²`. A factor of `4`, and it is the **mode
number**: `sin(πx/λ)` gives `(λ/t)²`, `sin(2πx/λ)` gives `(λ/2t)²`. Recomputed (`P4`):

```
(λ/t)²   = 1.6866e26     <- quoted
(λ/2t)²  = 4.2166e25     <- what the verified field gives
```

The direction is unaffected — both are `∝ 1/t²` — so the inversion stands and the record's conclusion is safe.
But the quoted value silently assumes a lateral mode that was never declared and was not the one tested. Filed
as `E4`: a disclosure defect in the sentence, not a reversal.

---

## 5. My own `D-6` is withdrawn

`route_terminus_v1.md` §6 promoted `GD6` on this ground: "the only open item whose resolution could put a
measured quantity **into a site**."

That is a category error (`P10`). `δ_E` is one scalar per **configuration**; a site holds `(k, n)`. Two objects
whose `δ_E` differs by `4×` (`λ = 0.20` vs `0.40 m`, same `H`) give **one deposit digest**,
`ba6dd50ce0b81bb7`. So `I(site ; δ_E) = 0`, measured here and already implied by `DEPOSIT-BLIND`.

Resolving `GD6` — even in the branch where it resolves cleanly — would have put **nothing** into a site. The
critical path was never `GD6`. It is `G6`/`DC2`, the compliant `σ_s`, which is what `route_terminus_v1.md` §9
already names as the constructive reopening condition. §6 substituted `GD6` for `G6`; the two differ by one
character and by an entire category.

---

## 6. Decisions

- **`D-6a`** *(withdraws `D-6`)* **`GD6` is not the critical path.** A criterion evaluated on the whole
  configuration cannot become a per-site payload. The critical path is `G6`/`DC2` (`σ_s`), as §9 states.
  *Reverse on* a demonstration that `δ_E` — or any configuration-level scalar — varies site by site.
- **`D-10`** **`ME3-F1` is closed.** `φ` is declared: a **velocity potential**. The material reading is
  **withdrawn as a misreading**, not retained as an alternative. *Reverse on* a showing that the ratio is an
  energy under a non-potential `φ`.
- **`D-11`** **`ME3` is retired** for the `D2` route. It is reinstatable only for a **dynamic** unfolding route
  (`KIN-DYN`'s other class), and only with a `u_⊥/u_∥` instrument, neither of which exists. *Reverse on* a
  solved background supplying `u^μ` with a non-zero transverse part.
- **`D-12`** **`δ_E,max` is never registered.** Not "open pending `φ`" — there is no admissible value, because
  the functional is a thickness floor in one branch and identically zero in the other. A future dynamic route
  registers its own threshold on its own criterion. *Reverse on* `D-11`'s reversal.

---

## 7. What this does not decide

- It does not supply a criterion for 2D-ification. It shows `ME3` is not one. **No replacement is proposed
  here**, because a replacement is a new physical criterion and choosing it now would be a further declaration
  made after the numbers are known — the exact move `GD6` was blocked to prevent.
- It does not touch `ME1`, `ME2` or `ME4`. `ME2`'s aspect ratio remains the shape measure of record.
- It does not reopen the deposit line. `D-1` stands; `P10` strengthens it.

## 8. Errata

| id | defect | status |
| --- | --- | --- |
| `E1` | `P2`'s band was wrong **and** its harness used `h_z = 0.25` against a declared unit spacing. A single grid cannot verify a continuum law. | `P2` stays REFUTED; `X1` (post-hoc) supplies the sound test and confirms the law: error `6.79e-2 → 3.93e-3`, contraction `2.07, 2.04, 2.02, 2.01` |
| `E2` | `P7` predicted `k = 2, 1, 1`; measured `1.89, 0.95, 0.43`. The third is a surface argument applied to a volume integral. | stays REFUTED; qualitative claim survives with a weaker exponent |
| `E3` | `P8`'s pass band was first written `[0.6, 1.6]` after the number was known, against a registered 2%. | band restored to 2%; `P8` REFUTED. Third instance of "band wide enough to hide the miss", first caught within the same run |
| `E4` | `route_completion_v1.md` §4.1 quotes `(λ/t)²` while its verified field gives `(λ/2t)²`. | recorded; direction unaffected |
| `E5` | `P9`'s text search matched a table row, not the sentence that establishes the retirement. | claim holds; evidence printing is weak |
