# The demonstration object changes, and `σ` is declared for it

**Registered**: 2026-11-22
**Authority**: governor directive — the rendering demonstrations stop using human-body slices; a simplified
object of distinct material components is adopted; the rendering is executed with a space-filling curve.
**Specification**: `docs/specs/demo_object_v1.md` (**hash-locked**: `runs/FRONT/demo_lock.json`,
`sha256 afe855c2…4633`).
**Pre-registration**: `runs/FRONT/demo_obj_registration.md` (`P1`–`P14`, fixed before the renderer).
**Products**: `src/route/demo_2d_map.py` → `runs/FRONT/demo_2d_map.png` (+ `.display.txt`, block `OK`) and
`runs/FRONT/demo_2d_map_results.txt` (`12/14`; both failures mine, erratum appended).

---

## 0. Executed, and one half is stronger than it was asked to be

Both parts of the directive are carried out. The part that was asked as a *presentation preference* turned
out to be a *structural necessity*, and the part that was asked as an *algorithm choice* turned out to be
unavailable — the algorithm is admitted, the reason is not.

| part of the directive | what happened |
| --- | --- |
| stop using body slices | **done**, and it was the only way to unblock `σ` (§1) |
| a simplified object with distinct components | **done** — four coaxial shells, but "distinct" is narrower than it sounds (§5) |
| render with a space-filling curve | **done** — exact order-16 Hilbert, contiguity `1.0000`; but the curve had to be **component-major**, which changes what the map shows (§4) |

## 1. The new object is not a preference — it is what unblocked `GD11`

`GD11` (which site does layer `n_z` go to?) was registered yesterday and **blocked upstream by `GD10`**: the
body has `1.18e10` plates on `8.1227e9` cells, so its site set is not definite, and a traversal chosen against
an indefinite site set is chosen against a moving target.

A new object dissolves that without answering `GD10`:

```
pieces 4,279,069,764   ≤   cells 4,294,967,296      ->  0.9963 plates per cell
```

**`GD10` cannot arise here because the condition that produced it never arises.** The `0.37%` residue is
vacuum. `GD11` is therefore **closed for `DEMO-1`** by declaration, and **remains open for the body** —
`front_sweep_v1` §2.2 still forbids drawing the body's site content.

The body's physical record is untouched: `H = 1.74 m`, `δ = 0.215 nm`, `1.18e10` plates, array `90126²` all
stand wherever they were used. Only the *rendering subject* changed.

## 2. Why four coaxial shells, and why every one spans the full height

If a component vanishes over some `z` range — a sphere inside a block — then the pieces-per-layer is `M(z)`,
the piece count is no longer a square, and the array side must be padded. That re-creates `GD10` in a new
guise. So the design constraint is:

> **every component spans the full height with non-zero cross-section**, hence exactly `M = 4` pieces in every
> layer, hence `pieces = 4N` exactly.

That bought an exact census and cost a shape. The shape that keeps structure visible under this constraint is
nested shells, with `C2` and `C3` **anti-phased**: `r₂(z) = 0.045 − 0.006 sin`, `r₃(z) = 0.070 + 0.008 sin`.
Where `C3` swells, `C2` thins. `C3`'s cross-section swings by a factor **`3.671`** along the axis while the
total is `πr₄²` **identically** (flat to `0.000 ppm`, `P7`). An exchange of material between components at
constant total is the structural fact this object exists to display; a monotone taper would show a gradient
instead.

## 3. The height is derived from the array, not chosen freely

`S = 65536 = 2¹⁶` is fixed by one requirement: an **exact** Hilbert curve needs a power-of-two side, and any
padding throws away contiguity (`P14`: `1.000000`, exhaustive at order 10 and sampled at order 16). A `2¹⁷`
side would give `25%` occupancy and a `52 km` canvas; `2¹⁶` is the smallest that holds four shells. Then

```
H_max = S²·δ/M = 0.230854 m        declared H = 0.2300 m  (99.96% of the cap)
N = 1,069,767,441   t_rip = √2H/c = 1.0850e-9 s
canvas = 26,221.0 m   mean placement 10,032 m   max 18,541 m
```

| check | value | verdict |
| --- | --- | --- |
| each piece fits its site | `A₃,max = 1.4335e-2` on `0.1601 m²` | PASS, `11.2×` clear |
| each piece's extent fits the pitch | `0.180` on `0.4001 m` | PASS, `2.2×` clear |
| shells never cross | `min(r₃−r₂) = 11.0 mm` | PASS |
| one plate per cell | `0.9963` | PASS — `GD10` cannot arise |

## 4. `σ` is declared component-major, and the choice was forced by measurement

`GD11` requires `σ` declared and locked. Two orderings were possible and they are **not** equivalent, because
the decimation is not optional:

```
4,294,967,296 sites  /  512² = 262,144 display pixels  =  1 : 16,384
even a 4K frame (8,294,400 px) shows 0.19% of the deposit
```

- **layer-major** (`p = 4n + k`) makes the map a mosaic of complete cross-sections, and the decimation
  **destroys it**: one display pixel spans `4096` layers × `4` components, an exact number of `4`-cycles, so
  its component mix is `25.0% / 25.0% / 25.0% / 25.0%` — measured, to the digit (`P8`). No renderable pixel
  can carry component identity under layer-major. That is arithmetic, not a preference.
- **component-major** (`p = kN + n`) puts each shell's `N` layers in one contiguous run: `99.9985%` of
  display pixels are single-shell (`P9`), with exactly **3** straddling a shell boundary and **1** at the
  empty boundary (`P10`).

> **Declared: `σ : p = k·N + n → Hilbert index p`, order 16.** Locked in `demo_lock.json`.

### 4.1 What this costs, and it is not small

**The map is four scrolls, not a mosaic.** It does not show any cross-section as it was. A cross-section is
reassembled by taking the site at the same relative offset in each of the four runs — the right-hand panel of
the figure does exactly that. This is a genuine loss of the photograph reading, taken deliberately, because
the alternative preserves the cross-section and loses the components to averaging. **No map at this
decimation can have both**, and the specification says so rather than implying one was found.

## 5. Where the directive's own framing does not survive: "distinct material components"

The four components differ **geometrically** — which piece sits where — and in no other way. The four areal
densities in the spec are declared and **read by nothing**: `D2` performs no deformation (`KIN-DYN`), so no
modulus, density or constitutive response enters the mapping. A body and a block of foam with the same
cross-sections produce the same map.

So this figure illustrates **structural distribution**, which it does well, and **not** physical properties,
which it cannot. Colouring by density would have implied a physical significance the mechanism does not
grant. Making the distinction physical needs a per-component reflectance entering the signal chain — that
needs a compliant `σ_s`, which does not exist (`G6`, `DC2`). Recorded in the spec as a limitation, not
buried here.

## 6. What the figure refuses

`FL1`, `EN2` (false colour), `GEOMETRY: PRESCRIBED (D2)`, `ME5-COROLLARY: NOT-APPLICABLE`, block `OK` under
`display_lint`. It does **not** claim the deposit is two-dimensional (`Annex B` §B.3 — the internal bound
still fails by `2.3e3–2.5e4`), does not create a readable cell (`MR1.0`), and does not claim the map is a
measurement of anything.

**`G1` is unchanged.** The demo is a new product class — a *declared* object, mapped by a declared traversal —
not a repair of `G1`, which was audited against the body's route. Whether a `DEMO-1` frame may count toward
`G1` is a governor question and is **not decided here**.

## 7. My defects

**Predictions: 12/14, both failures mine** (§6 of the results, erratum `E1`–`E2`):

- **`P1`** predicted occupancy `0.99629`, measured `0.996299`, tolerance `5e-6` — I rounded the ratio to five
  decimals and then tested it tighter than that rounding. The two quantities that matter were exact to the
  unit. **Third occurrence in three rounds.**
- **`P11`** predicted canvas `26,218.6 m`; it is `65536 × 0.4001 = 26,221.0 m`. Hand arithmetic, `9e-5`
  relative. It had already been copied into the spec as a "dead constant" and has been corrected there.

**The figure took five renders.** Disclosed because the failures were of different kinds and only one was
cosmetic:

1. cutaway shell labels used leader lines anchored at `r = 0`, so every leader crossed all four shells; map
   annotations were placed on dark regions in faint grey and collided with the panel title; the right panel
   was letterboxed to a thin strip (`aspect='equal'` inside a tall, narrow box).
2. the shell legend was clipped off the bottom of the figure; asymmetric alpha made the mirrored half read as
   a different object.
3. the panel caption collided with the footer; a white `C2` label sat on the ochre field.
4. **the "not yet deposited" tint was too close to the darkest component** (`0.86 × colour + 0.14 × white`),
   so in `C1` the pale region was effectively invisible — an *encoding* failure, not decoration: the figure
   would have shown a fully-deposited quadrant that was half empty.
5. shell labels at axes-fraction `0.972` landed at `z = 0.2347 m`, **above the material** (`ylim` is
   `1.05 H`, the fills stop at `H`), so white labels were drawn on the background and only the one dark label
   appeared. Fixed by using data coordinates.

## 8. Still open

`GD10` (open, unaffected), `GD11` (**open for the body**; closed for `DEMO-1`), `GD6` (`φ`, blocks Phase 3),
`GD9` (objective), route governance, `MR2`. The body's `σ` remains undeclared, so no body frame may draw site
content.

*Content generated by AI*
