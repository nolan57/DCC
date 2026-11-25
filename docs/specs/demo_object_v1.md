# `DEMO-1` — the declared demonstration object, and the declared traversal `σ`

**Registered**: 2026-11-22
**Authority**: governor directive — *"the 2D rendering demonstrations will no longer use human body slices as
examples. Instead, a simplified object composed of distinct material components will be adopted … the rendering
will be explicitly executed using a space-filling curve algorithm."*
**Status**: **IN FORCE for display only.** This object replaces the body as the *rendering subject* and changes no
physical record. The body's constants (`H = 1.74 m`, `δ = 0.215 nm`, `1.18e10` plates, array `90126²`) are
untouched and remain in force wherever they were used.
**Self-limitation.** This specification may not contain a tier threshold, a pass/fail criterion, or a matrix cell.
It declares a geometry and a traversal. If a threshold appears here, this file has become a second lock and is void.

---

## 1. Why a new object is the only way to declare `σ`

`GD11` was registered open and **blocked upstream by `GD10`**: the body's census is frozen with `1.4527` plates
per cell, so the body does not have a definite site set, and a traversal chosen against an indefinite site set is
chosen against a moving target.

A new object dissolves that. Its census is computed from its own geometry, at declaration time, and is
**constructed to satisfy one plate per cell exactly**. `GD10` therefore cannot recur here — not because it was
answered, but because the condition that produced it (more plates than cells) never arises.

`GD11` remains **open for the body**. It is closed for `DEMO-1` by §4 below.

## 2. The object: four coaxial shells, all full height

Axi-symmetric, `z ∈ [0, H]`, radius `r`, four components separated by three declared radii:

| id | region | material role | areal density | radius law |
| --- | --- | --- | --- | --- |
| **C1** | `0 ≤ r < r₁` | core, dense | `ρ_A = 4.0e3 kg/m²` | `r₁ = 0.0200 m` (constant) |
| **C2** | `r₁ ≤ r < r₂` | shell, light | `ρ_A = 1.2e3` | `r₂(z) = 0.0450 − 0.0060 sin(2πz/H)` |
| **C3** | `r₂ ≤ r < r₃` | shell, heavy | `ρ_A = 7.5e3` | `r₃(z) = 0.0700 + 0.0080 sin(2πz/H)` |
| **C4** | `r₃ ≤ r ≤ r₄` | jacket | `ρ_A = 2.0e3` | `r₄ = 0.0900 m` (constant) |

Every component spans the full height with non-zero cross-section. **This is the design constraint that makes the
census exact**: each layer contains exactly `M = 4` pieces, always, with no layer where a component appears or
disappears. A sphere-in-a-block would give `M(z)`, hence a non-square piece count and a re-run of `GD10`.

The two modulations are **anti-phased on purpose**: where `C3` swells, `C2` thins. So the components *trade*
cross-section along the axis while the total is constant (`πr₄²`, identically). A monotone taper would show a
gradient; an anti-phased pair shows an **exchange**, which is the structural fact this object exists to display.

### 2.1 The five numbers, and which of them are derived

| quantity | value | status |
| --- | --- | --- |
| `M` | `4` | **declared** — four distinguishable components |
| `S` | `65536 = 2¹⁶` | **derived from one requirement:** an exact Hilbert curve needs a power-of-two side. A padded `2¹⁷` would give `25%` occupancy and a `52 km` canvas; `2¹⁶` is the smallest that holds `4` shells |
| `H` | `0.2300 m` | **declared**, but capped by derivation: `H ≤ S²δ/M = 0.230854 m` (§3) |
| `r₄` | `0.0900 m` | **declared** — sets the aspect at `H/2r₄ = 1.28` |
| pitch | `0.4001 m` | **reused** from the registered lattice (`mid_sweep_frame_v1` §2), because it is the number the transport budget was computed with and it already exceeds the largest piece's extent (`0.180 m`, §3) |

Derived, not chosen: `N`, pieces, cells, occupancy, canvas, `t_rip`, cut area — all in §3.

## 3. Census, and the four admissibility checks

```
δ          = 0.215 nm                     (registered, front_sweep_v1; the atomic layer)
H          = 0.2300 m
N          = floor(H/δ) = 1,069,767,441   layers
M          = 4                            pieces per layer, every layer
pieces     = M·N        = 4,279,069,764
cells      = S²         = 4,294,967,296
occupancy  = pieces/cells = 99.63%        -> 0.996 pieces per cell, ONE plate per cell
```

The reverse direction is what fixes the height:

```
H_max = S²·δ/M = 4,294,967,296 × 2.15e-10 / 4 = 0.230854 m
H = 0.2300 m  ->  pieces = 99.63% of cells  (the 0.37% residue is vacuum, not a defect)
```

| check | condition | value | verdict |
| --- | --- | --- | --- |
| **A1** one plate per cell | `pieces ≤ cells` | `4.279e9 ≤ 4.295e9` | PASS — `GD10` cannot arise |
| **A2** each piece fits its site | `max A_k ≤ pitch²` | `A₃,max = 1.4335e-2` vs `0.1601 m²` | PASS, `11×` clear |
| **A3** each piece's extent fits the pitch | `2r₄ ≤ pitch` | `0.180 ≤ 0.4001 m` | PASS, `2.2×` clear |
| **A4** shells never cross | `r₂ < r₃` for all `z` | `max r₂ = 0.051`, `min r₃ = 0.062` | PASS, `11 mm` apart at worst |

Dead constants, for the record: `canvas = S·pitch = 26,221.0 m`; `mean placement = 0.3826·canvas = 10,032 m`;
`max placement = canvas/√2 = 18,541 m`; `t_rip = √2H/c = 1.0847e-9 s`; total cut area `= N·πr₄² = 2.7222e7 m²`.

## 4. `σ` — the declared traversal, and why it is component-major

```
piece index      p = k·N + n            k = component (0..3), n = layer (0..N-1)
site             d = p                  Hilbert index, order 16
coordinates      (x, y) = d2xy_16(p)
```

### 4.1 The ordering had to be chosen by measurement, not by taste

`GD11` requires `σ` to be declared and locked. Two orderings are conceivable, and they are **not** equivalent
under the decimation that any figure must apply:

- **layer-major** (`p = 4n + k`): four consecutive sites are the four components of one cross-section. The map is
  then a mosaic of complete cross-sections — and it is **annihilated by decimation**. A display pixel covering
  128×128 sites spans 4096 layers × 4 components, an exact integer number of 4-cycles, so it contains all four
  components in equal measure and resolves to a flat average. Measured in `P3`: each component occupies
  `25.0%` of a decimated block, to within `1%`.
- **component-major** (`p = kN + n`): each shell's `N` layers occupy one contiguous run of the curve. Measured in
  `P4`: `≥ 99%` of decimated blocks are single-shell. Identity survives decimation.

The decimation is not optional. `4.29e9` sites against `512² = 262,144` display pixels is a factor of `16,384`, and
a 4K frame (`8.29e6` px) still shows `0.19%` of the deposit. **The map cannot be drawn 1:1, ever**, and `σ` is
therefore a legibility decision at a fixed decimation.

> **`σ` is component-major: four scrolls, one per shell.** A cross-section is reassembled by taking the site at the
> same relative offset in each of the four runs — an exploded view, not a mosaic.

### 4.2 What this costs, stated plainly

The map does **not** show the cross-section as it was. It shows four separate axial histories. That is a real loss
of the "photograph" reading, and it is taken deliberately: the alternative preserves the cross-section and loses
the structure to the averaging that any renderable image imposes. A map that is a faithful mosaic at 512² does not
exist, and this specification does not pretend otherwise.

### 4.3 The exact curve, and the residue

`S = 2¹⁶` is a power of two, so the Hilbert curve needs no padding: all `65536²` indices are used and consecutive
indices are 4-adjacent everywhere. Contiguity is `1.0000`, against the raster order's `0.9961` (`sf_curve_results`).
The `0.37%` of sites with `d ≥ pieces` are **empty** — vacuum, drawn as such, not as material.

## 5. What this specification does not do

1. It does not close `GD11` for the **body**. That object still has no declared `σ`, and `front_sweep_v1` §2.2
   still forbids drawing its site content.
2. It does not answer `GD10`. It makes `GD10` inapplicable to `DEMO-1` by construction.
3. It makes no claim that the deposit is two-dimensional (`Annex B` §B.3 stands), that any cell is readable
   (`MR1.0`), or that the map is a measurement of anything. **`DEMO-1` is a declared geometry.**
4. It does not license a `FL3` label. The map is `FL1`: a declared-convention rendering of a quantity no
   instrument measured.
5. It changes no threshold, no tier, and no frozen text.
6. **It does not make the components physically distinct.** The four areal densities in §2 are declared and
   **read by nothing**: `D2` performs no deformation (`KIN-DYN`), so no modulus, density or constitutive
   response enters the mapping. The components differ *geometrically* — which piece sits where — and that is
   the only sense in which they are distinct here. A map coloured by density would imply a physical
   significance the mechanism does not give it. Making the distinction physical requires a per-component
   reflectance entering the signal chain, which needs a compliant `σ_s` and does not exist (`G6`, `DC2`).

*Content generated by AI*
