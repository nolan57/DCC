# `θ`'s camera slot — declaration v1 (`RQ-19`)

**Date**: 2026-11-23 (round 51)
**Status**: **DECLARED.** A tightening, not a relaxation. It adds no threshold, no rung price, no tier, and
retires no verdict.
**Authority**: governor instruction 2026-11-23 — *"3. Approve RQ-19, but adopt a two-step strategy of 'declare first, then retro-apply'"*
(approve `RQ-19`, but by the two-step strategy: declare first, then retro-apply). The two steps are §0 and §5.
**Fills**: erratum E1 of `docs/specs/theta_environment_v1.md` — `R0` contains the camera and `θ` does not
name it.
**Reads with**: `theta_environment_v1.md` (the `E` slot), `docs/specs/intrinsic_structure_tiers_v1.md` §5
(`q`, `θ`), `runs/LADDER/r3_illumination_results.txt` (the measurement that made the gap observable).

---

## §0 The two steps, and why the order is load-bearing

| step | what it is | what it may do | what it may never do |
|---|---|---|---|
| **A — declare** (this round, §1–§4) | the slot becomes mandatory for every registration written *from now on* | make an unnamed camera unreadable | be waived retroactively by silence |
| **B — retro-apply** (§5) | each prior round's pose is *recovered from its code* and tagged `RETRO-DECLARED` | **qualify** a prior number by naming its precondition | **rescue** a falsified prediction, move a verdict, or be cited as a pre-registration |

The order matters because the reverse order is the loophole. If the retro step came first, a round could
compute a number, notice which camera makes it work, and then declare that camera — which is `BN-07`'s
inverse solution with a different noun. Declared first, the slot is a constraint the next round must satisfy;
applied after, it is only a description of what happened, and a description cannot be a licence.

**The anti-laundering clause.** A `RETRO-DECLARED` pose:
1. may **add a precondition** to a claim ("this `C` holds for a source-tracking camera");
2. may **narrow** a claim's scope;
3. may **not** flip `FALSIFIED` to `CONFIRMED`, may not move a tier verdict, and may not be cited in a new
   document as though it had been registered before the run.

---

## §1 The gap, stated exactly

`R0` (`theta_environment_v1.md` §2) is `I(x) = R·L_e(r(x))`. Two of its three symbols are already in `θ`:
`L_e` is the `E` slot, and `R` is a material response at a declared band. The third — `r(x)`, the *reflected
ray direction* — is a statement about where the camera is, and **`θ` has no slot for it.** `r` is the
mirror map, so `R·L_e(r(x))` silently asserts "the camera sits on the specular ray, at every point, at every
incidence".

That assertion is not harmless. Round 50 measured both halves of it (`r3_illumination_results.txt` §2–§3):

| geometry | contrast `C` | the image |
|---|---|---|
| camera on the specular ray, `θ_i` = 0 / 45 / 75° | `3.3166` at all three, bit-identical (`0.0e+00`) | exists at all three |
| camera fixed on the surface normal, `θ_i` = 0 / 45 / 75° | `3.3166` at 0°, then **no image** | vanished at **3.31°** (sine) / **8.88°** (terrace) |

Same scene, same `θ`, same `E`: one column has a number and the other has a blackout. `S_θ = 1.000000000`
between them for `C`, and `S_θ` is undefined for the second because the denominator is zero. **A tuple that
cannot distinguish these two rows is not a complete description of the observer**, which is what `θ` claims
to be.

## §2 The slot

```
θ = ( aperture, gate, band, distance ;  E , G )
                                          ^
                                          G = ( n̂_v , δ_v )   viewing direction, acceptance half-angle
```

`G` carries **direction and acceptance only**. `distance` is already `θ₄` and `aperture` is already `θ₁`, so
the honest statement is not "the camera was missing" but "**the camera's orientation was missing** — the two
slots that were never needed for a scalar gate". `n̂_v` is declared in the **surface frame** (the local normal
plus one in-plane axis, so that azimuth is meaningful for an anisotropic relief), `δ_v` in radians as a
half-angle of the acceptance cone.

## §3 The two canonical geometries — and why the gap went unseen for two rounds

| label | rule | realisable when | measured consequence |
|---|---|---|---|
| `G_A` **specular-coupled** | `n̂_v` = mirror of the illumination direction about the local normal at each point | camera and source are co-rotated, or the surface is a point | `C` exists at every incidence and is *independent* of incidence for a specular surface |
| `G_B` **fixed** | `n̂_v` = one fixed direction (canonically the global normal) while the source moves | any real instrument | `C` exists only while the specular window overlaps the surface: a blackout beyond 3.31°/8.88° |

**The degeneracy.** At `θ_i = 0` the two coincide: the mirror of the normal is the normal. That is why
rounds 48 and 49 could run with no camera slot and nothing broke — and why the slot only became *observable*
when round 50 moved off axis. A parameter that is invisible at the only point where it was evaluated is not
evidence that it is absent; it is evidence that the evaluation never left the degenerate point. This is the
same structure as `q` before `RQ-12`: one point of a function, read as the function.

## §4 The default rule — and why it differs from `E`'s

| slot | unnamed reads as | why |
|---|---|---|
| `E` | **`E1`** — constant radiance, `C ≡ 0` | `E1` is a *zero member*: it is the environment that buys nothing, so silence is read as the weakest claim |
| `G` | **unreadable — the sentence is refused** | there is no zero member. A camera cannot be absent, and "no direction" is not a pose. Any default would be a *choice of pose*, i.e. an undeclared assumption, which is the thing this document exists to forbid |

So the two slots get opposite rules from one principle: **silence resolves to the weaker claim, and where no
weaker claim exists, silence resolves to nothing.** A registration that computes a contrast and does not name
`G` is not defaulted to `G_A` and is not defaulted to `G_B`; it is returned.

**The cost of that rule, stated.** Rounds 48 and 49 predate it, so they are unreadable under §4 *until* §5
supplies their poses — and a retro-declared pose is a description, not a registration. The consequences are
narrower than they look, and are stated in §5 rather than argued away.

## §5 Step B — retro-application, recovered from the code

Each pose below was **read out of the program**, not chosen. The tag on each row is the whole point of the
step.

| round | estimator | `G` it actually used | recovered from | status |
|---|---|---|---|---|
| 48 — `r1_observer_results.txt` | `Q3` at `q ∈ {0, 1}`; `q` is a scalar gate/budget factor | **absent** — the estimator has no angular variable at all | `src/route/ladder_r1.py` (`Q_INSTR`, `Q_REFL`; no `theta` beyond the band/gate) | `RETRO-DECLARED: ABSENT` |
| 49 — `r2_relief_contrast_results.txt`, `E1`–`E3` columns | single-bounce specular composition, evaluated at `θ_i = 0` | **`G_A` at the degenerate point** (coaxial source and camera; equals `G_B` there) | `src/route/ladder_r2.py:177` — `math.radians(60.0) if env == 'E4' else 0.0`; `image()` carries no camera term | `RETRO-DECLARED: G_A (degenerate)` |
| 49 — same file, `E4` column | diffuse cosine `cos(θ_i + arctan α)/cos θ_i` at `θ_i = 60°` | **`G_B`** — source moves, camera stays on the normal (that is what the `1/cos θ_i` normalisation is) | same line: `60.0` is passed only for `E4` | `RETRO-DECLARED: G_B` |
| 50 — `r3_illumination_results.txt` | explicit `G_A` / `G_B` branches | **both, declared and compared** | `src/route/ladder_r3.py` §2–§3 | `PRE-REGISTERED` — the only round where `G` is a controlled variable |

**What §5 surfaces, and it is not decoration.** Two of the four rows *disagree with each other inside one
table*: round 49's `E1`–`E3` columns are `G_A` and its `E4` column is `G_B`. The table is therefore not one
scene photographed one way; it is two geometries in adjacent columns, and its `E4` row was already excluded on
independent grounds (the diffuse model is the one this near-mirror surface is not — `r3` §6). The declaration
does not change that exclusion; it explains why the column was always going to be incommensurable.

**What it narrows, and this is the real product of step B.** Round 49's headline — `C = 0.280` held for 3.6
decades — was measured under `G_A`. Under `G_B` the same scene keeps that contrast only while the specular
window is on the surface, i.e. within **3.31°** of normal incidence (round 50's measurement). So:

> `C = 0.280` at the terraced form is a statement about a **source-tracking camera**, and about a fixed
> camera only within 3.31° of the normal.

That is a precondition, not a refutation: the plateau is a property of the riser width and the environment,
and neither of those is a camera. But the number may no longer be quoted as though any instrument would see
it. `RL-2`'s `V = ε` is not re-priced; the *scene* the rung describes just acquired a second declared slot.

**And one honest admission.** Round 48 (`r1`) is the weakest row here: `G` is not merely undeclared, it is
**absent from the estimator**, because `q` lumps the whole channel into one scalar. Its `Q3 = 5.737` is a
statement about *the channel* (`q = 1` vs `q = 0`) and remains exactly as measured; it is **not** evidence
that any viewing geometry supports that number, and nothing in this document converts it into such evidence.
Escaping the degeneracy for `RL-1` would take a re-run with `G` in the estimator — that is `RQ-20`, not this
document.

## §6 What this declaration does not do

1. **No threshold, no price, no tier.** `G` is descriptive geometry; it cannot move `Q0`–`Q3` thresholds or
   any rung's `V`.
2. **No verdict moves.** `r2`'s `Y1`–`Y7` stand; `r3`'s `Z1`–`Z7` stand, including `Z5`'s `FALSIFIED`, which
   §0's clause 3 explicitly forbids this document from touching.
3. **No visibility sentence is licensed.** `S9` still forbids them; `G` is one of the slots that a
   *permitted* sentence must fill, not a permission.
4. **No claim that `G_A` is physical.** `G_A` is realisable only by co-rotating camera and source; for an
   extended object it is not a single instrument at all. It is retained because two rounds used it and
   because it is the upper bound on what a camera can see.
5. **No re-opening of the matrix route.** `PG-02` returned it (`BN-13`); this document is a `θ` declaration.

## §7 What would reverse it

1. A demonstration that `G` is **derivable** from the other slots — e.g. that `aperture` plus `distance`
   already fix `n̂_v` for every admissible instrument. If so the slot is redundant and should be removed, not
   defaulted.
2. A measurement in which `G_A` and `G_B` give the **same** `C` at an off-axis incidence on a surface whose
   bright set stays on the plate — i.e. the blackout is an artefact of the window model rather than of the
   geometry. That would collapse §3's table and with it the reason for the slot.

---

*Content generated by AI*
