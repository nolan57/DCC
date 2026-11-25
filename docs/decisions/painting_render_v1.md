# What That 325 km² "Painting" Actually Looks Like: Rendering, Photon Budget, and Three Upper Limits

**Module**: `src/analysis/painting_render_v1.py`
**Outputs**: `runs/ANALYSIS/painting_render_v1.txt` / `.png`, `runs/ANALYSIS/painting_limits_v1.png`
**Date**: 2026-11-21
**Upstream**: `three_body_comparison_v1.md` (¬area branch → 325 km² monolayer)

---

## 0. In One Sentence

The Three-Body painting **exists, has the right size, right structure, and right position**, but its contrast lies in a channel that only single-photon counters can enter, and the bandwidth of that channel is determined by the atom count (ten years at 1 mm resolution, $2\times10^{14}$ years at atomic resolution). **The human eye has never seen it.** And the reason is not "a bland image" but **photon starvation** — this verdict differs in technical meaning from all previous "white wall" statements; see §5.

---

## 1. The Unfolding Map: Not Magnification, but Tiling

The map is a **bijection**: each atom gets a lattice site in the plane. The geometry is therefore completely pinned down by volume conservation:

| Quantity | Value | Notes |
|---|---|---|
| Volume | 0.0700 m³ | $M/\rho$ |
| Number of atoms | $7.0\times10^{27}$ | ≈10 amu average |
| Average atomic spacing $d$ | 0.2154 nm | $(V/N)^{1/3}$ |
| Unfolded area | $3.249\times10^{8}\ \mathrm{m^2}=\mathbf{324.9\ km^2}$ | $N d^2$ |
| Square side length | 18.03 km | |
| Number of tomographic pieces | $8.12\times10^{9}$ | $A/A_c$, $A_c=V/H=0.040\ \mathrm{m^2}$ |
| **Single square tile** | **0.200 m × 0.200 m** (average) | lateral **1:1, no magnification**; thorax tiles ~0.32 m, leg tiles ~0.10 m |
| Arrangement | 90126 × 90126 | |

**This is the most important conclusion of this section**: the unfolding **does not** magnify the human image; it cuts the body into $6.5\times10^{8}$ tomographic slices, lays each slice out 1:1 as a square tile (the area being that slice's own cross-section), then arranges the tiles into an 18 km square.

> **Convention correction (2026-11-21 11:58)**: the average cross-sectional area was initially taken as $0.5\ \mathrm{m^2}$
> (0.71 m square), 12.5 times larger than the true value. The correct value is given by $A_c=V/H=0.070/1.75=0.040\ \mathrm{m^2}$
> (side length 0.20 m). Corrections carried over: number of pieces $6.5\times10^8\to8.1\times10^9$,
> array $25492^2\to90126^2$. $\tau$, the optical upper limit, and the photon budget are **all unaffected**
> (they depend only on $d$ and $V$, not on how the tiles are laid).

So the answer to "what do you see standing on the painting" is: **one 0.20 m tomographic slice, not a person**. The whole "human" exists only in the **ordering** of the tiles (reading through 8.1 billion pieces).

> Adjacent tiles therefore differ by only 0.215 nm — **visually identical**. To see anatomical changes (1 mm scale),
> one must sample one tile in every $10^{-3}/d=4.6\times10^{6}$. In other words, the human form exists only in a **4.6×10⁶-fold decimation**,
> while the original is a 4.6×10⁶-fold redundant sequence. This explains better than "how much larger the area is" why it is not a painting.

---

## 2. Optical Thickness of Each Square Tile

$\tau=(\mu/\rho)\cdot(\rho d)$, with monolayer column mass $\rho d\sim2.2\times10^{-4}\ \mathrm{g/cm^2}$.

| Tissue | $\rho$ | $\tau$@550nm | $\tau$@284eV | $\tau$@532eV | $\tau$@4keV |
|---|---|---|---|---|---|
| fat | 0.92 | $6.0\times10^{-10}$ | $1.96\times10^{-3}$ | $3.9\times10^{-4}$ | $7.2\times10^{-7}$ |
| muscle | 1.06 | $9.6\times10^{-8}$ | $1.47\times10^{-3}$ | $1.9\times10^{-3}$ | $1.0\times10^{-6}$ |
| blood | 1.06 | $6.9\times10^{-7}$ | $1.44\times10^{-3}$ | $1.9\times10^{-3}$ | $1.0\times10^{-6}$ |
| bone | 1.85 | $1.0\times10^{-7}$ | $2.61\times10^{-3}$ | $2.4\times10^{-3}$ | $3.9\times10^{-6}$ |
| lung | 0.26 | $1.7\times10^{-8}$ | $3.5\times10^{-4}$ | $4.8\times10^{-4}$ | $2.5\times10^{-7}$ |

Two orders coexist: visible light $10^{-10}$–$10^{-7}$, soft X-rays $10^{-4}$–$10^{-3}$. **Both are far below 1** — the painting absorbs less than one part in a thousand of the light in any channel.

---

## 3. Hard Upper Limit: The 2D Condition Locks the Optical Thickness

Number of layers $N_L=V/(Ad)$, $\tau=N_L\tau_1$. The 2D condition $E_F<E_{\rm sub}$ gives

$$\frac{V\sqrt{2\pi N}}{\pi A^{3/2}}<1\ \Longleftrightarrow\ A>279\ \mathrm{km^2}$$

| Configuration | $N_L$ | $\tau$ |
|---|---|---|
| This configuration, 325 km² | 1.00 layer | $1.24\times10^{-3}$ |
| 2D boundary, 280 km² | **1.16 layers** | $1.8\times10^{-3}$ |

$$\boxed{\text{effective 2D reduction}\ \Longleftrightarrow\ \tau\le 0.18\%}$$

It is not a fabrication problem but a **definitional problem**: density requires thickness, and thickness means not 2D. The human-eye threshold is 1%, while the thickest qualifying painting is only 0.18%, lower by 5.5× — **the contrast criterion already fails before the photon budget is considered**.

---

## 4. Two Unfolding Maps Must Be Explicitly Chosen

| Map | Planar density | Image content | 2D verdict |
|---|---|---|---|
| **M1 dense packing** | $2.15\times10^{19}\ \mathrm{m^{-2}}$ everywhere | uniform; the density map is entirely lost, only composition remains | passes everywhere ($E_F=2.30$ keV, ratio 0.80) |
| **M2 column-density preserving** | $n(x,y)=\rho(x,y)d/m_{\rm atom}$ | carries a radiograph | lung 0.41 / fat 0.77 / muscle 0.82 / **bone 1.09 not 2D** |

"Smooth effective two-dimensional reduction" corresponds to **M2** — only it can produce a "painting". But M2 **locally violates the 2D criterion in bone regions** (bone column density gives $E_F=3.12$ keV $>$ 2.88 keV). **The brightest part of the image is precisely the only part that is not 2D.** This is the structural finding of this module, reported as P4.

---

## 5. The Failure Mode Is Photon Starvation, Not Insufficient Contrast (Verdict Correction)

The correct convention for imaging contrast: $T=e^{-\tau}\simeq1-\tau$, so the relative contrast for **transmitted light** $=|\Delta T|/T=|\Delta\tau|$ (the absolute difference), **not** $\Delta\tau/\bar\tau$.

| Probe | $\bar\tau$ | $\Delta\tau$ (between tissues) | Photons per pixel (SNR=3) | Interpretation |
|---|---|---|---|---|
| Visible 550 nm | $1.1\times10^{-7}$ | $6.9\times10^{-7}$ | $1.9\times10^{13}$ | short by 5 orders of magnitude in photons |
| **Soft X 284 eV** | $1.2\times10^{-3}$ | $2.3\times10^{-3}$ | $1.8\times10^{6}$ | **feasible (conventional STXM)** |
| Soft X 532 eV | $1.3\times10^{-3}$ | $2.0\times10^{-3}$ | $2.2\times10^{6}$ | feasible |
| Hard X 4 keV | $9.6\times10^{-7}$ | $3.7\times10^{-6}$ | $6.8\times10^{11}$ | marginal |

**This is a substantive update to the "white wall" verdict**: the previous statement was "contrast is too low (1–2%)"; the correct statement is "**the relative ratios between tissues are tens of times; what is missing is absolute signal**". Under visible light the image exists, the shape is right, and the contrast ratios are beautiful — it just takes $2\times10^{13}$ photons per pixel to pull it out of Poisson noise, whereas the human eye requires an absolute modulation of $10^{-2}$.

Therefore:

- **284 eV soft X-ray transmission** = the only real carrier of this painting. Monochromatic, extremely thin, structurally complete, like a low-dose chest radiograph.
- **Visible light** (reflected or transmitted, any angle, any magnification) = a uniform gray film. $\tau\sim10^{-7}$.

---

## 6. Viewing-Distance Ladder: The Two Failures Are Independent

$s=2.9\times10^{-4}D$ (1′ resolution).

| Viewing distance | Resolvable | What is seen | Recognizable |
|---|---|---|---|
| 25 cm | 73 μm | cell-level detail within a tile | no ($\Delta\tau=10^{-7}$) |
| 1 m | 0.29 mm | same as above | no |
| 2.5 km | 0.73 m | one square tile (one complete slice) | no |
| 18 km | 5.2 m | tens to thousands of square tiles | no (uniform gray field) |

To resolve a single atom (0.215 nm), the viewing distance would need to be $7.4\times10^{-7}$ m — 4 orders of magnitude shorter than the near-point focal distance. Moreover, soft X-rays are absorbed within a few micrometers of the cornea, so placing an eye in the beam would only show uniform fluorescence.

**The resolution failure and the contrast failure are independent**: even with an atomically resolving eye, $\Delta\tau=10^{-7}$ would still be invisible; even with unlimited photons, 0.215 nm cannot be resolved from 18 km away.

---

## 7. Readout Time and Information Content

| Resolution | Number of pixels | Scanning ($10^6$ px/s) | Total photons | Photons ($10^{13}$ ph/s) |
|---|---|---|---|---|
| 1 cm | $3.2\times10^{12}$ | 0.1 yr | $5.7\times10^{18}$ | 0.02 yr |
| 1 mm | $3.2\times10^{14}$ | **10.3 yr** | $5.7\times10^{20}$ | 1.8 yr |
| 1 μm | $3.2\times10^{20}$ | $1.0\times10^{7}$ yr | $5.7\times10^{26}$ | $1.8\times10^{6}$ yr |
| 0.215 nm | $7.0\times10^{27}$ | $2.2\times10^{14}$ yr | $1.2\times10^{34}$ | $3.9\times10^{13}$ yr |

Two independent budgets (scanning rate / photon budget) give 10 years vs 2 years at 1 mm, differing by 6× — the same order of magnitude, which is mutual confirmation: **the constraint is not device speed, but the total photon count**.

Information content: phantom class-distribution entropy $H=0.80$ bit/pixel; at 100 μm voxels, the effective information of the human body is $7.0\times10^{10}$ voxels × 0.80 bit = **7.0 GB**. Meanwhile there are $7.0\times10^{27}$ addressable positions → **redundancy ratio $10^{18}$**.

> This painting is not "a painting waiting to be admired", but a redundant encoding of "one atomic position per bit".
> It is more like a read-only medium with atoms as storage cells than an image.

---

## 8. Corrections to Existing Documents

| Document | Original value | Correction | Impact |
|---|---|---|---|
| `three_body_comparison_v1.md` §3 | monolayer visible absorption 0.08%–3% | $6\times10^{-10}$–$7\times10^{-7}$ | **overestimated by 4–5 orders of magnitude** (the premise "chromophores make up 1%–10% of atoms" is wrong; the real value is $3.6\times10^{-5}$) |
| same, §6/§7 | "very faint stained-glass window" | "no visible-light channel exists" | the metaphor overpraises: a stained-glass window at least shows color |
| `abandon_assumption_visual_v1.md` §2 table | A′ absorption 2.3% (very faint iridescence) | visible light $10^{-7}$; 284 eV $10^{-3}$ | branch ranking unchanged |

**The direction of the conclusion is unchanged; its strength has changed**: the ¬area branch is still the only branch that "is a painting", but the evidence for it being a painting has shifted from "low contrast" to "photon starvation". This makes it still valid in **instrument visualization** (following `scifi_boundary_v1.md` §7.5), but completely invalid in human-eye visualization.

---

## 9. Failure Conditions (When This Conclusion No Longer Holds)

1. **One must not replace "transmitted-light contrast" with "relative fluctuation of $\tau$"**: the latter would give a false 180%, while the former is what the eye/detector sees ($=\Delta\tau$).
2. **M1 and M2 must not be mixed**: under M1 a "density map" does not exist ($\S4$), and under M2 bone regions are not 2D. Reporting "the content of the painting" must state that M2 is used.
3. **$\mu/\rho$ is an order-of-magnitude estimate** (NIST/CXRO ±2×). $\tau$ fluctuates by 2× up or down, and $\Delta\tau$ and the photon count by 4×, **without changing any verdict** (even the nearest threshold differs by more than one order of magnitude).
4. **The phantom is synthetic**: the anatomical structure is used to demonstrate contrast grading and is not cited as medical data.
5. The conclusion applies only to $M=70$ kg and $\rho=10^3\ \mathrm{kg/m^3}$. $N_L\propto V/A$; a change in mass shifts $\tau$ but **does not change the upper limit $N_L\le1.16$** (it is dimensionless).

---

## 10. Verdict Summary

| # | Verdict | Type | Result |
|---|---|---|---|
| P1 | unfolding is tiling, not magnification | CHECK | PASS |
| P2 | single-layer visible $\tau\sim10^{-7}$ | ESTIMATE | PASS (corrected old value) |
| P3 | 2D locks $\tau\le0.18\%$ | CHECK | PASS |
| P4 | M2 breaks 2D in bone regions | CHECK | PASS |
| P5 | photons are missing, not contrast | ARGUMENT | PASS |
| P6 | no human-eye channel | ARGUMENT | PASS |
| P7 | the two budgets are of the same order | CHECK | PASS |
| P8 | redundancy ratio $10^{18}$ | CHECK | PASS |

**8/8 PASS.** The answer to the visualization subproblem is thus refined from "empty" to "**there exists a soft X-ray transmission image, 18 km in size, with $7\times10^{27}$ pixels, whose bandwidth is limited by the atom count**".
