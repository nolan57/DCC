# `GD7` / `GD8` executed — the fidelity axis has a direction, and the corollary has a scope

**Registered**: 2026-11-22
**Authority**: governor rulings, verbatim —
`GD7` *"FL means 'faithful to what the human eye sees', and FL3 is the maximum"*; `GD8` *"keep 2L/c, and write in 'only when D = L'"*.
**Pre-registration**: `runs/ROUTE/gd7_gd8_registration.md` (six predictions fixed before the run).
**Products**: `src/route/fl_coordinate.py` → `runs/ROUTE/fl_coordinate_results.txt`.
**Texts amended**: `docs/specs/meff_boundary_v0_2.md` (corollary premise + annotation);
`docs/decisions/staged_relaxation_visual_route_v1.md` §3 (`GD7` amendment); `docs/conventions/display_conventions_v1.md`
(`DC9`); `docs/decisions/route_completion_v1.md` §3 (scope annotation).

---

## 0. What was changed, where

| Ruling | Applied as | Where |
| --- | --- | --- |
| `GD7` — `FL` is faithfulness, `FL3` maximal | the coordinate is defined and measured; the ladder's direction is fixed and stated | v1 §3 amendment; `DC9` |
| `GD8` — keep `2L/c`, write in `D = L` | the premise is now **inside** the corollary sentence; the identity is untouched | `meff_boundary_v0_2` §2 |
| `GD8` — not adopting the per-patch form | the per-patch window is demoted to an **unregistered observation**, may not license a frame | `meff_boundary_v0_2` annotation; `route_completion_v1` §3 |

No threshold moved. No archived product was edited — the four amendments are banners, as for `ME1` and `ME3-F1`.

---

## 1. `GD7` gives the word "continuum" a referent

The goal asserts that fidelity **is** a continuum. Before this ruling that was a word; `FL1`–`FL3` were three names
with no measure between them. Under `GD7` the continuum has a definition:

```
FL(I) = −( b + c + p + e )
```

| term | meaning | decades? |
| --- | --- | --- |
| `b` | band offset, `|log₁₀(E_I / 2.25 eV)|` | yes |
| `c` | contrast distortion, `|log₁₀(m_I / m_R)|` | yes |
| `p` | photon-budget deficit, `max(0, log₁₀(N_req/N_avail))` | yes |
| `e` | count of `EN` operators applied | operators |

`FL3` **is** the reference frame, so all four terms vanish and `FL = 0` exactly. The maximum is unique because every
term is a magnitude. Measured on the three rungs, from registered numbers only:

| rung | `b` | `c` | `p` | `e` | **`FL`** |
| --- | --- | --- | --- | --- | --- |
| `FL3` naked-eye reflection | 0.0000 | 0.0000 | 0.0000 | 0 | **0.0000** |
| `FL2` 284 eV transmission | 2.1011 | 0.0000 | 0.0000 | 1 | **−3.1011** |
| `FL1` 550 nm enhanced | 0.0000 | 4.1549 | 9.9795 | 2 | **−16.1344** |

Three things follow, and all three are new:

1. **The ladder ascends**, `FL3 > FL2 > FL1`, exactly as the ruling requires — and it does so on measured terms, not
   by fiat.
2. **`FL2`'s dominant cost is the band migration itself** (`b = 2.1011`), not any physics. The intermediate rung is
   expensive for a reason that belongs to the *observer*, which is consistent with `S1a`'s finding that the `CM`
   domain is instrument-relative.
3. **`FL1` is dominated by photons** (`p = 9.9795`), then by the stretch (`c = 4.1549`). The rung defined by
   enhancement is the rung whose fidelity is destroyed by it.

**Continuity is a property now, not a claim.** `FL` is a sum of continuous terms with `|dFL/d log₁₀ g| = 1.0000`
exactly, so the three rungs are **thresholds on a continuum** and every intermediate value corresponds to a frame
somebody could build. That is what §1 of the route promised and never constructed.

---

## 2. `GD7` does not contradict the corollary — the two constrain different things

This was the risk, and it resolves cleanly. Read the corollary's own words:

> "No **faithful** reflected-light frame of a **surviving sheet** exists."

- the corollary constrains the frame's **content** — it must not show a surviving sheet;
- `GD7` constrains the frame's **fidelity** — it must equal the unaided retinal image.

A frame can satisfy both at once: **maximally faithful, containing no sheet.** So `FL3` is attainable *and* the
corollary stands unweakened. The archived panel D-left of `runs/ANALYSIS/unfold_appearance_v1.png` already displays
exactly this frame, captioned *"what you see is what lies behind it"*.

What `GD7` makes explicit is that the failure mode was never fidelity. It was the unstated hope that **the most
faithful frame is also the most informative one**. `FL3` has `FL = 0` and carries no structure of the object; `FL` and
information are anti-correlated **by construction**. `staged_relaxation_visual_route_v1` §9 had reached this as an
observation about what happens at ¬`C1`; it is now a property of the metric at fixed object.

---

## 3. `GD8` costs the corollary nothing where it matters

`D = L` does not look like a favourable choice, but for the naked eye it is the **best** one. Naked-eye viewing needs
`D ≥ 0.25 m`; the corollary applies whenever `D ≥ L/√2`, which holds for every `L ≤ 0.3536 m`; and for
`L > 0.3536 m` the object subtends more than 126.9° at the near point and cannot be taken in. So inside the
naked-eye domain the corollary holds **a fortiori**, and the premise narrows its scope without narrowing its
conclusion anywhere the route actually operates.

| `L` | `L/√2` | covered at `D = 0.25 m`? | `t_rip` | `2L/c` |
| --- | --- | --- | --- | --- |
| 0.070 m | 0.0495 | yes | 3.302116e-10 s | 4.669897e-10 s |
| 0.200 m | 0.1414 | yes | 9.434617e-10 s | 1.334256e-09 s |
| 0.300 m | 0.2121 | yes | 1.415193e-09 s | 2.001385e-09 s |
| 1.000 m | 0.7071 | no — and not viewable at the near point | 4.717309e-09 s | 6.671282e-09 s |

The per-patch form `D ≤ d/√2` remains true algebra, and remains **unlicensed**: `GD8` chose `2L/c`, and an executor
does not convert a declined correction into permission. It is cited only as a finding about the corollary's structure.

---

## 4. `FL3` is a family, and it must be declared

Both scenes below are faithful reflected-light frames at the naked eye, so both have `b = c = p = e = 0` and `FL = 0`:

| member | constraint set | what the frame shows |
| --- | --- | --- |
| **A** | `C1` held, as registered | the object is **gone** when the light returns |
| **B** | ¬`C1` (the 7 cm slab) | an **intact slab** at 35 % reflectance |

`FL3` is therefore not one image but a two-member family selected by the constraint set, and the members are not
interchangeable: member A presents the 2D-ification by showing its completion; member B presents an object that was
never 2D-ified. An undeclared `FL3` frame will be read as B, which is the reading the corollary forbids.
`DC9` now requires the member in the caption — in the caption and not in the block, because a new block field would
invalidate every issued block, and `DC7` forbids repairing one in place.

---

## 5. What the two rulings jointly expose — `GD9`

`FL3` member A needs **no relaxation at all**. A faithful reflected-light frame of the object's absence is available
at the full constraint set, because the absence is what the light actually carries. So:

> **Maximising `FL` terminates the route immediately, at zero relaxation, with a frame that presents nothing.**

The "diagonal" collapses to a point: the top rung is reachable from the bottom-left corner without moving along the
relaxation axis at all. This is not a defect in either ruling — it is what follows from taking *"fidelity is
closeness to what the eye sees"* seriously.

The goal's operative verb is **"present the physical scene"**, and a frame of absence presents the scene only in the
degenerate sense of presenting its null. So the goal carries an **information** requirement that *"maximise `FL`"*
does not. And `FL` and information are anti-correlated. The route therefore needs a joint objective, and the choice
is not the executor's.

### `GD9` — what is the route's objective?

| option | objective | consequence |
| --- | --- | --- |
| **A** | maximise `FL` | route ends at `FL3` member A, zero relaxation, vacuous presentation — consistent and complete, but it presents nothing |
| **B** | Pareto: maximise `FL` subject to a declared minimum information floor | ladder becomes a **front**; `FL3` qualifies only if its floor is met, and at member A it is not — so the top rung is `FL2` unless the floor is set to zero |
| **C** | maximise information at the highest *admissible* `FL` | the relaxation axis retains its role: relaxing constraints buys information, and `FL` is a constraint rather than the objective |

A and C are the two coherent readings of the goal sentence; B is the formalisation of C. The executor's
**non-binding** reading: the goal's verb is "present", and C is the only option under which the relaxation axis does
any work — under A the axis is inert, and under B it is inert unless the floor is non-zero, in which case B *is* C.
But this is a ruling, not an inference, and no frame will be labelled until it is made.

---

## 6. What this round changed, and what it did not

**Changed.** `FL` has a definition and a direction; the ladder ascends on measured terms (`0`, `−3.10`, `−16.13`);
"continuum" is a proved property; the corollary carries its premise and is a fortiori valid for the naked eye;
`FL3` is identified as a two-member family with a mandatory declaration; and the route's degeneracy under `GD7` is
registered as `GD9`.

**Did not change.** No threshold, no archived product, no state certified two-dimensional, no frame produced. `G1`,
`G3` and `G5`'s product gaps remain exactly as `route_goal_conformance_v1` recorded them — `GD7` and `GD8` were
definitional rulings and cannot supply a depiction. `GD6` still blocks Phase 3.

**Registering `FL` does not licence a claim.** It makes `FL1`–`FL3` measurable. It does not make any existing frame
citable: 26 of 27 still carry no declaration block, so under `DC1` they remain non-products whatever their `FL`.

---

*Content generated by AI*
