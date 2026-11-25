# Review — "focus on RQ-16 and visualisation" (external advice, 2026-11-23)

**Object reviewed**: a three-part suggestion received after `RQ-16` was queued: (i) render the periodic isolated-plate
array "natively in Swift"; (ii) map the measured `Q0`, `Q1`, `Q2` onto the array's geometric parameters and material
properties, driving "a dynamic 3D demo"; (iii) use a mosaic/pixelation effect to show *structure exists but detail is
lost*.

**Status of the advice**: not adopted as written. One of its three parts is right in direction and wrong in
mechanism, one is impossible, one converts the record's only honest remaining instrument into a picture.

**Evidence base**: `runs/MATRIX2/plate_array_results.txt` (run today, `RQ-16`, closed `CLOSED-CONSTRUCTIVE`).
So the advice was evaluated *after* the measurement existed, not before — the order the advice itself would have
inverted.

---

## §1 What the run returned

| id | `p` | `s` | fill | `P0` | `Q0` | `ξ/h` | `Q2` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PA-8` | 8 | 6 | 0.5625 | `0.015625` | `0.7230` | `1.66` | `0.5155` |
| `PA-16` | 16 | 12 | 0.5625 | `0.003906` | `0.9307` | `3.32` | `0.7718` |
| `PA-32` | 32 | 24 | 0.5625 | `0.000977` | `0.9827` | `6.64` | `0.8991` |
| `PA-16f` | 16 | 11 | 0.4727 | `0.003906` | `0.9307` | `3.67` | `0.7899` |
| `SHUF-16` | — | — | 0.5625 | `0.040405` | `0.2836` | `0.63` | `−0.1601` |

Three laws fall out, all measured, none predicted correctly (5 of 6 registered predictions were falsified —
`W1`–`W5`; only `W6` survived):

```
Q0 = 1 - 1/(p^2 * P0_null)      -- counts LATTICE CELLS, blind to fill (PA-16 = PA-16f = 0.9307)
Q1 = 0.207 * p                  -- is the pitch, in cells; threshold 4.0 at p ~ 19.3
Q2 = 0.52 -> 0.90               -- rises with pitch; reports the lattice's local predictability
```

And the shuffle kills all three. **The passes are evidential** — the opposite of `TILED` under `MR1.1`, and the
opposite of what `V3` predicted.

---

## §2 Part (ii) is the one that decides the rest: it inverts the arrow

`Q0`, `Q1`, `Q2` are **outputs** of `(geometry, h)`. The advice proposes to use them as **inputs** to the geometry.
With the laws above that is a solved equation, not a design:

| desired verdict | equation | free knob |
| --- | --- | --- |
| `L1` PASS | `0.207 p ≥ 4` | `p ≥ 19.3` cells |
| `L0` PASS | `1/p² ≤ 0.02820` | `p ≥ 5.96` cells |
| `L2` PASS | `Q2(p) ≥ 0.5` | `p ≥ ~7` cells |

So "make the array show all four tiers green" is one choice: `h = pitch/19.3`. No physics enters, and the picture
is drawn to satisfy the verdict it is then used to illustrate — a closed loop. In the record's defect taxonomy this
is the mirror of *threshold before calibration*: here the **scene** is calibrated to the threshold. Same defect,
opposite direction, and it is the one defect the `L0`–`L3` admission gate was built to prevent (`(a)` definition
refers only to the scene; `(c)` threshold declared before evaluation — a scene chosen to hit `(c)` satisfies the
letter of `(a)` and defeats its purpose).

Second, smaller point: `Q0`/`Q1`/`Q2` are not material properties. `Q2` moves 0.5155 → 0.8991 across the sweep with
the material constant. Mapping them onto "material properties" would assert a material dependence the run does not
contain.

---

## §3 Part (i): a 3D animated demo depicts an object that does not exist

- **The third dimension is not modelled.** `sup d₃D = 0.292062 m` inside `pitch = 0.400100 m`; `D2` performs no
  deformation (`KIN-DYN`). Any 3D animation is therefore required to invent the in-between frames — the exact
  category `§VI` of `exhaustive_matrix_route_v1.md` forbids as falsified imagery, and the reason the route's own
  Phase 2 was unfalsifiable (`M7`).
- **The deposit cannot be depicted at all.** `DEPOSIT-BLIND`: six physically distinct objects give one digest
  `558d30e08fd32cf6`, `I(canvas ; r₄) = 0` bits, 10 of 12 declared parameters never reach a site. A "demo of the
  deposit" is a demo of an object the record cannot distinguish from five others.
- **What may be depicted is the declared scene**, which is what the run measured: a `128 × 128` array of square
  plates at declared `p`, `s`. That is a legitimate figure — labelled `FL1` (`D-3`/`G1`: a declared chart, not a
  measurement column), with the numbers printed on it.

On the stack: this is the third external proposal to assert what the operator's toolchain is (previously Swift
video work; the workspace is C++/OpenCV). The cost is not taste, it is provenance: every product in `runs/` is
Python + plain text with a `PROVENANCE:` line, and an image emitted by a renderer with no numeric trace cannot be
audited or re-derived. If a renderer is wanted, the auditable minimum is: **the generator writes the array and a
JSON of the measured numbers; the renderer draws only those, prints the numbers on the image, and stamps the
source path.** Then the picture is a view of a product, not a product.

---

## §4 Part (iii): right direction, wrong instrument, and today's run moves the target

"Structure exists but detail is lost" is the correct *shape* of the programme's situation — `MR1.1` said the passes
were "tessellation, not a portrait". But the measured result sharpens it in a way the mosaic metaphor gets wrong:

1. The mosaic metaphor supposes a **portrait** exists at fine detail and is destroyed. For this class nothing is
   destroyed: `Q0` never saw the detail (`P0` is fill-blind), `Q1` *is* the lattice spacing, and `Q2` is
   local predictability. There is no high-detail object underneath to be pixelated away.
2. The mosaic metaphor also implies the passes are weak evidence, as they were for `TILED`. Here they are not: the
   shuffle drops `Q0` 0.9307 → 0.2836, `Q1` 3.32 → 0.63, `Q2` 0.7718 → −0.1601. **The array's structure is real and
   detectable**; what it is not is a statement about *which object*.
3. Legitimate mosaic: band-limit the **declared scene** at the **measured** `ξ` and print both numbers. That is a
   true statement ("at scale `ξ = 3.32 h`, this is what the declared array looks like"), and it is a chart.
   Illegitimate: apply a mosaic as a visual metaphor over a rendered object, which asserts a measurement that was
   never taken.

The honest visual for "structure without identity" is therefore not a pixelated portrait but the **canonical /
shuffled pair** — same marginal, same histogram, one passes three tiers and one fails three. That figure makes the
point with no invented object in it.

---

## §5 Disposition

| part | verdict | what it becomes |
| --- | --- | --- |
| (i) Swift 3D demo | **rejected as specified** | an `FL1` three-panel figure, `runs/MATRIX2/plate_array_figure_v1.png`: declared array, shuffle control, and the three measured laws — drawn from `runs/MATRIX2/plate_array_results.txt`, numbers printed on the panels, display declaration in the `.display.txt` sidecar |
| (ii) `Q` → geometry/material mapping | **rejected** | the arrow is reversed: the `Q`'s are outputs of `(geometry, h)`. Adopting it makes the scene an inverse solution |
| (iii) mosaic | **direction accepted, mechanism replaced** | band-limit at the measured `ξ`, on the declared scene, labelled — not a filter over an imagined object |

**One correction to my own prior work, recorded because the run forces it**: `matrix_v2_results.txt` §6 states that
`R2` "fails three of four and its single pass is non-evidential". Measured on the deposit's own class that is wrong —
`R2` reads `PASS/PASS/PASS` at `p = 32` and `PASS/FAIL/PASS` below, and the passes are evidential. Erratum `E2` in
`runs/MATRIX2/matrix_v2_registration.md` records it; the product is retained unedited.

*Content generated by AI*
