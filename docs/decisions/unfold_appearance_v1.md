# What a human body looks like after being unfolded into slices: five levels of view

**Module**: `src/analysis/unfold_appearance_v1.py`
**Products**: `runs/ANALYSIS/unfold_appearance_v1.png` (main figure), `.txt`
**Date**: 2026-11-21
**Upstream**: `painting_render_v1.md` (geometry and optical thickness)

---

## 0. Why this figure is needed

The previous version gave numbers (8.1e9 tiles, 18 km, τ≤0.18%), which read abstractly. This version draws "unfolding" using a synthetic full-body tomographic phantom, while separating three **views that are easily confused with one another**:

| View | What it is | Who can see it |
|---|---|---|
| A: 18 km overhead view | Far field of normalized τ | No one can see a human figure (only a 1D gradient) |
| B: Neighboring 3×3 | The 9 tiles actually adjacent on the painting | Identical → no visible variation |
| C: Decimated array | 1 tile sampled out of every 4.6e6 | This is "unfolded body slices," but a synthetic view |
| D: Single tile, two channels | One tile in two channels | Naked eye = gray; 284 eV = anatomical image |
| E: Atomic scale | 0.215 nm per pixel | Only a scanning probe |

**Mistaking C for what the naked eye sees is the easiest error to make in this project.** C is a "design drawing"; B/D are the "actual objects."

---

## 1. Geometry (scope corrected)

| Quantity | Value |
|---|---|
| Volume | 0.0700 m³ |
| Body height $H$ | 1.75 m |
| **Mean cross-sectional area $A_c=V/H$** | **0.0400 m² (side length 0.200 m)** |
| Number of slices $N_s=A/A_c=V/(Hd)$ | $8.12\times10^{9}$ |
| Unfolded height $N_s d$ | 1.750 m (= body height, self-check) |
| Array | 90126 × 90126, 18.03 km square |
| Anatomical difference between adjacent tiles | $d=0.215$ nm |
| **Decimation ratio (1 mm scale)** | $10^{-3}/d=4.6\times10^{6}$ |

> Correction: $A_c$ was earlier taken as 0.5 m² (0.71 m square), 12.5 times too large.
> τ, the optical upper bound, and the photon budget do not depend on $A_c$, so **all conclusions are unaffected**; only the tile size and count need to change.

---

## 2. Key conclusion: the human figure exists only at 4.65 million-fold decimation

Adjacent tiles differ by 0.215 nm. For anatomical structure to change visibly (1 mm), $4.6\times10^{6}$ tiles must be skipped. The properties of this painting are therefore:

- **At the original scale**: millions of tiles are identical, forming a periodic gray film;
- **After 4.6e6-fold decimation**: a sequence of slices from the top of the head to the ankle finally emerges (View C);
- **At 18 km distance**: the entire 1.75 m is laid out into 90,000 horizontal bands and redshifted into a **1D gradient** (View A), with about 20% contrast — and that is after normalization; the raw visible-light $\tau=10^{-7}$ means in practice nothing can be seen.

**So "the Three-Body painting" does not hold at any single scale**: up close everything is identical, from afar there is only one dimension, and the only scale at which a human body can be discerned is a synthetic view never presented in the original image.

---

## 3. How many pixels are in one tile

| Quantity | Value |
|---|---|
| Tile width / atomic spacing | $9.3\times10^{8}$ atoms |
| Number of pixels within a tile (1 atom = 1 pixel) | $8.6\times10^{17}$ |
| Resolvable by the human eye at 1 m | 73 μm → 2740 × 2740 points per tile |
| Information magnification | $1.1\times10^{11}$ |

What the naked eye can read is $10^{-11}$ of a tile.

---

## 4. The two channels of a single tile

| Channel | Image | Interpretation |
|---|---|---|
| Visible-light reflection/transmission | Uniform gray surface ($\tau=1.1\times10^{-7}$) | **Not "dark," but "empty"** — what you see is what lies behind it |
| 284 eV soft X-ray transmission | Lungs dark, heart dark, bones white, chest wall gray ($\tau=1.2\times10^{-3}$) | Structure intact, Δτ~10⁻³, 2e6 photons per pixel |

This is the first time in the project that "painting" and "seeing" are split into two side-by-side figures: **the same tile, with nothing in the left image and an anatomical map in the right.**

---

## 5. Failure conditions

1. View C is **decimated synthesis**, not something any observer can see; taking it as what the naked eye sees is an error.
2. The phantom is programmatically generated (piecewise geometry); the anatomical shapes serve only to demonstrate contrast grading and must not be cited medically.
3. The grayscale window (vmin 0.10 / vmax 1.30, γ=0.9) is to make soft tissue distinguishable; it does not change any numerical conclusion.
4. The 20% contrast of View A is a **post-normalization** quantity; the raw signal strength is still constrained by $\tau\le0.18\%$.

---

## 6. Verdict

| # | Verdict | Type | Result |
|---|---|---|---|
| U1 | Decimation ratio $4.6\times10^{6}$ | CHECK | PASS |
| U2 | The five views are not interchangeable | ARGUMENT | PASS |

**In one sentence**: unfolding a human body yields not a portrait but an atomic-level redundant record that requires 4.65 million-fold decimation to read out a human figure; and at any real scale of this record, what the naked eye sees is a field of gray.
