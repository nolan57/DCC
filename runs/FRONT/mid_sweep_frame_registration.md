# Pre-registration — the mid-sweep frame

**Written before `src/route/front_sweep_frame.py` existed.** The frame is a *presentation product* under
`GEOMETRY: PRESCRIBED (D2)`; it establishes no physics and is not a matrix cell.

Ruling: governor said **GO** on item 1 of "what is next" — draw the frame the goal names, the one artifact the
project has never produced: a 3D object with the front **part-way through it**.

---

## 0. Why this frame and not another one

`staged_relaxation_visual_route_v1` §1 requires: *"a 3D macroscopic object being swept by a 2D-ification front"*.
The census says this has never been depicted: the 27 images in the repo are either the **unfolded end state**
(`unfold_appearance_v1.png`, `painting_render_v1.png` and the rest of `runs/ANALYSIS/`), or plots
(`runs/ROUTE/s0_frame_fl1.png` is `μ_ov` versus `Δz_res/t` with `t_span = 0 s`). **Zero images show the front at
an intermediate position.** That absence is a missing *product*, not a missing measurement, so it needs no
relaxation and no ruling about physics.

## 1. What the registered mechanism forces the frame to show

`front_sweep_v1` §0 and §2 are unambiguous and they forbid the obvious picture:

- The front peels **one atomic layer at a time**, `0.215 nm` per peeling.
- Each peeled layer is **translated as a rigid body to its lattice site** — average placement distance **13.8 km**,
  maximum **25.5 km**, on a square array of `90126²` sites — and joins its neighbours edge-to-edge. No in-plane
  bonding; the space between plates is vacuum.
- Intralayer strain is **exactly zero**; all displacement is taken up by broken interfaces.

So the converted material **does not remain where the object was**. The object is *consumed* and reassembled
kilometres away. A single frame of "an object turning into a sheet in place" would be false, and it is the picture
everyone draws. The frame must therefore show **two places at once**, and must say that they cannot share a scale.

This is the same conclusion `GD8`/`F3` reached from the optics side (the reflected channel is near-field
sub-field only) and that `M5` reached from the photon side. Here it comes from the kinematics.

## 2. Declared conventions (each is a choice, and is labelled as one)

| Item | Declaration | Why |
| --- | --- | --- |
| Front normal | along the slab's length; the front is a plane | `GEOMETRY: PRESCRIBED (D2)`. Nothing in the frame depends on the direction of the normal; a plane is a plane |
| Object | the registered slab: `A = 1 m²`, `H = 0.070 m`, `70 kg` (`ρ = 1000 kg/m³`) | the best-characterised case in the route work; `t_rip` is registered for it |
| Thickness gain | `z` exaggerated **×8** | `0.070 m` against `1 m` is unreadable at 1:1. Declared on the image itself, not only in text, so it cannot be separated from the figure |
| Plate tokens | **symbols, not to scale**; the drawn count is **not a census** | `1.63e8` plates cannot be drawn. The token size carries no measurement |
| Fill order on the array | row-major from one corner | the registered record does not fix an order; declared so it is not read as a solved result |
| Far panel | the **whole** array at true scale, plus a magnified inset of an `8×8`-site patch | one panel cannot show both `0.07 m` and `7.2 km` |
| Time | a **single instant** at converted volume fraction `0.5` | the goal asks for "as the front sweeps"; one instant at half is the named moment |

## 3. Numeric predictions (derived, falsifiable, fixed now)

Derived from registered constants only: `H = 0.070 m`, layer `a_L = 0.215 nm`, array `90126²`, max placement
`25.5 km`, `t_rip = 3.302116e-10 s` (registered for `L = 0.070 m`).

| # | Quantity | Predicted | Derivation |
| --- | --- | --- | --- |
| `N1` | layers in the slab | `3.2558e8` | `H / a_L = 0.070 / 2.15e-10` |
| `N2` | fragments (one plate per layer) | `3.2558e8` | the slab's layer cross-section is one rectangle ⇒ `1` component/layer |
| `N3` | array side | `18044` | `ceil(√N2)` |
| `N4` | site spacing | `0.4001 m` | `25500 / ((90126/2)·√2)` |
| `N5` | canvas side | `7.221 km` | `N3 · N4` |
| `N6` | farthest plate from centre | `5.105 km` | `(N5/2)·√2` |
| `N7` | mean plate distance | `≈ 1.38 km` | `0.3826 × (N5/2)` for a uniform square |
| `N8` | front speed | `c/√2 = 2.1199e8 m/s` | `H / t_rip` with `t_rip = √2H/c` — exact, not a fit |
| `N9` | converted mass at `f = 0.5` | `35 kg` | `0.5 × 70 kg` |
| `N10` | plates deposited at `f = 0.5` | `1.628e8` | `0.5 × N2` |

`N8` is worth its own line: the front advances at `0.707 c`, which is not a choice but the arithmetic of
`t_rip = √2·L/c` applied to `L = H`. If the script prints anything else, the derivation or the registration is
wrong.

## 4. What the frame asserts

1. The object is consumed from one face; the un-swept remainder is intact and still `0.070 m` thick.
2. The front is a plane, and it is at `f = 0.5` — half the mass has been converted.
3. Converted material has **left**: it is not a sheet lying on the object.
4. Where it went: an array `7.22 km` across whose sites are `0.400 m` apart, one plate each.
5. Distance is the reason no single photograph exists, and the frame says so on its face.

## 5. What the frame refuses to assert

1. That the converted state is **two-dimensional as a graph or a sheet**. `ME4` certifies *no handles created*;
   it forbids "the state is a graph". The plates are disconnected; `χ = N_comp`.
2. That this is what a **camera** would record. `q = 0` in the reflected channel (`T5`): zero photons. This is
   `FL1`, digital, false-colour.
3. That the front position is **solved**. It is prescribed (`D2`).
4. Any **census** from the drawn tokens.
5. Any **readability** claim, in the matrix sense of `MR1.0`. The frame is a depiction, not a cell.
6. Any **rate of the array filling** or order beyond the declared convention.

## 6. Falsifiers

The frame is withdrawn if any of the following is observed: a plate drawn on the object's remaining material; a
drawn count presented as a census; `N8 ≠ c/√2` beyond `1e-6`; a caption claiming a camera could record it; a
claim of two-dimensionality stronger than `ME4`'s.

---

## Addendum A1 — the object is the registered body, not the slab (appended pre-run, no code executed yet)

Choosing the object forced a decision I got wrong in §2, and it has to be corrected before the frame exists.

The slab (`A = 1 m²`, `H = 0.070 m`) is the best-characterised object in the *route* work, which is why I wrote it
into §2. But the array geometry cannot be borrowed for it: a slab's plate **is** its whole `1 m²` cross-section, so
a plate has side `1 m` and cannot sit on the registered `0.400 m` spacing. Borrowing that spacing would have mixed
two objects, and deriving a new one would have invented a number.

The registered kinematics belong to the **body phantom** of `front_sweep_v1` §1: `z ∈ [0, 1.738] m`,
`∫A dz = 0.0601 m³`, `1.457` components/layer, `1.18e10` plates, array `90126²`, spacing derived `0.4001 m`,
mean placement `13.8 km`, maximum `25.5 km`. So the frame depicts **the body**, and every far-field number on it is
a registered number rather than a derived analogue.

Two consequences, both improvements:

1. **No aspect exaggeration is needed** and none is used. The body is `1.738 m` tall and `~0.26 m` wide — true
   proportions are legible, so §2's `z ×8` row is withdrawn rather than declared. A frame with no geometric
   distortion is strictly better than one that needs a disclaimer.
2. **The converted fraction is a computed quantity, not `0.5`.** At `f = 0.5` by *height* the front sits at
   `z = 0.869 m`, but the legs are thin, so the converted *volume* fraction is smaller. Nothing on the frame will
   say "half converted"; the frame prints the volume fraction it computes.

### Revised predictions (these supersede §3; the slab values are withdrawn)

Cross-section model: piecewise-linear between the registered per-segment end values, with the registered step at
each segment boundary. This is a **declared reconstruction** of a table, not a measurement, and it carries its own
consistency check: its integral must land near the registered `0.0601 m³`.

| # | Quantity | Predicted | Basis |
| --- | --- | --- | --- |
| `N1` | layers | `8.084e9` | `1.738 / 2.15e-10`; registered peelings `8.12e9` → agreement within `0.5%` is itself a check |
| `N2` | plates | `1.18e10` | registered |
| `N3` | array side | `90126` | registered |
| `N4` | site spacing | `0.4001 m` | `25500 / ((90126/2)·√2)` |
| `N5` | canvas side | `36.06 km` | `N3 · N4` |
| `N6` | farthest plate | `25.50 km` | `(N5/2)·√2` — recovers the registered maximum |
| `N7` | mean plate distance | `13.80 km` | `0.3826 · N5` (mean radius of a uniform square, side `N5`) |
| `N8` | front speed | `c/√2 = 2.1199e8 m/s` | `1.738 / t_rip`, `t_rip = √2·1.738/c` |
| `N9` | `∫A dz` under the declared model | within `5%` of `0.0601 m³` | consistency of the reconstruction |
| `N10` | converted volume fraction at `z_f = 0.869 m` | `0.40 – 0.48` | legs are thinner than the torso |

`N7` also corrects my own §3 row, which wrote `0.3826 × half-side`. The constant is the mean radius of a uniform
square **of side `N5`**; with the half-side it gives `6.9 km` and would have contradicted the registered `13.8 km`
for no reason. With the side it returns exactly `13.80 km`.

### One more non-claim, added to §5

7. **The frame makes no claim about support or motion.** The un-converted remainder is drawn **in its initial
   position**. Whether it would stand, fall, or fail is not established here, and the frame does not depict it.
   This is why the object is drawn as an outline of its cross-sections rather than as a scene with a ground.

---

## Addendum A2 — the converted *volume* fraction is refused, and that is the point (still pre-run)

A1 said the frame would print the converted volume fraction. It cannot, honestly. The registered table in
`front_sweep_v1` §1 gives a **range** of cross-sectional areas per segment (`0.0063–0.0221`, `0.0464–0.0516`,
`0.0202–0.0303`), not a profile. Any curve through those ranges is a reconstruction, and the reconstruction is
testable: integrating my piecewise-linear reading gives about `0.050 m³` against the registered `0.0601 m³` — roughly
`17%` low, because the true profile is fuller than linear interpolation between range endpoints.

So the frame prints **`f = z/H = 0.500`**, which is definitional and needs no model, and it **refuses** to print a
volume fraction. The refusal is stated on the frame. A number I cannot derive from the registered record is worse
than no number, and this project has already paid for that mistake four times.

| # | Prediction about the refusal | Basis |
| --- | --- | --- |
| `N9'` | the piecewise-linear reconstruction integrates to `0.045–0.056 m³`, i.e. `7–25%` below the registered `0.0601` | legs are long and thin; linear interpolation between `0.0063` and `0.0221` under-fills the calf |

`N10` (volume fraction at `z_f`) is **withdrawn**, not failed — it is not computed at all. The scalar on the frame is
`converted fraction of height`, `SCALAR: converted fraction of object height (dimensionless)`.
