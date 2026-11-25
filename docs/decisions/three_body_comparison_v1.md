# Three-Body dual-vector foil vs. abandoning effective 2D: unfolding or overlapping

**Status:** CLOSING (conclusive)
**Date:** 2026-11-21
**Settlement:** `runs/ANALYSIS/three_body_comparison_v1.txt`, `src/analysis/three_body_comparison_v1.py`
**Figure:** `runs/ANALYSIS/three_body_comparison_v1.png`

---

## 1. Proposition to be tested

> "The scene after abandoning effective two-dimensional reduction (7 cm slab) is close to the two-dimensionalization effect in *The Three-Body Problem*."

**Conclusion: close in composition, not close in geometry.** Moreover, this "not close" is not a matter of degree but a **branch-attribution issue** — what truly corresponds to the Three-Body effect is not ¬E, but ¬Area.

---

## 2. The criterion is not "thin or not thin," but "unfolded or overlapping"

Volume conservation $A\cdot L=V=0.0700\ \mathrm{m^3}$ always holds, so **area and thickness are not two degrees of freedom but one**. On this hyperbola, "whether it looks like a painting" is determined by one thing:

| Configuration | Number of atomic layers along one line of sight | Information status |
|---|---|---|
| ¬E @ $1\ \mathrm{m^2}$ | $3.25\times10^{8}$ layers | **Overlapping**: the first 1 mm already absorbs everything; the rest is unreadable |
| ¬Area @ $325\ \mathrm{km^2}$ | **1 layer** | **Unfolded**: no layer is occluded |

$$N_{\rm layer}=\frac{L}{d_{\rm atom}}=\frac{0.070}{2.15\times10^{-10}}=3.25\times10^{8}$$

**A "painting" requires every atom to have its own position in the plane.** Stacking 3.25e8 layers on 1 m² yields only "the top face of a slab"; spread out over 325 km², the thickness automatically becomes 0.215 nm, i.e., a **single atomic layer** — that is what a painting is.

---

## 3. Numbers

| Quantity | Value | Notes |
|---|---|---|
| Number of atoms | $7.0\times10^{27}$ | 70 kg / ≈10 amu |
| Mean atomic spacing | 0.215 nm | Inferred from bulk density |
| Unfolded area | $3.25\times10^{8}\ \mathrm{m^2}=\mathbf{325\ km^2}$ | $3.25\times10^{8}$ times $=1\ \mathrm{m^2}$ |
| Thickness after unfolding | 0.215 nm | Exactly one atomic layer |
| Visible optical depth of a single layer | **$6\times10^{-10}$–$7\times10^{-7}$** | Directly multiply tissue $\mu_a/\rho$ by the single-layer column mass (see §3.1, second correction) |
| Reflectance of ¬E @1 m² | 35% (saturated, uniform color) | Bright but patternless |

> The previous version computed the single-layer absorptance as 2.3%; the order of magnitude was right, but the derivation treated $\mathrm{cm^2}$ as $\mathrm{m^2}$; it has been recomputed using $\sigma[\mathrm{m^2}]=3.82\times10^{-25}\,\varepsilon[\mathrm{M^{-1}cm^{-1}}]$.

### 3.1 Second correction: 0.08%–3% is still 4–5 orders of magnitude too high

The premise "chromophores make up 1%–10% of atoms" is wrong. Inverting tissue $\mu_a\approx4.5\ \mathrm{cm^{-1}}$ at 550 nm gives an equivalent chromophore concentration of only $\sim2$ mM, i.e., **chromophores make up only $3.6\times10^{-5}$ of molecules**, not $10^{-2}$. On this basis, 0.08%–3% was overestimated by about 300 times.

The correct approach bypasses the chromophore model and directly multiplies the single-layer column mass by the mass attenuation coefficient:

$$\tau=(\mu_a/\rho)\,\cdot\,(\rho\, d),\qquad \rho d\sim2.2\times10^{-4}\ \mathrm{g/cm^2}$$

| Tissue | $\rho\,d$ (g/cm²) | $\mu_a/\rho$ (cm²/g) | $\tau$ @550 nm |
|---|---|---|---|
| Fat | 1.98e-4 | 0.03 | $6\times10^{-10}$ |
| Muscle | 2.28e-4 | 4.2 | $9.6\times10^{-8}$ |
| Blood | 2.28e-4 | 30 | $6.9\times10^{-7}$ |
| Bone | 3.98e-4 | 2.5 | $1.0\times10^{-7}$ |

**The direction of the conclusion is unchanged, but its strength has changed**: it is not that "contrast is low (0.1%–1%)," but that **the absolute signal of a single layer in visible light is only of order $10^{-7}$, 5 orders of magnitude below the human-eye threshold $10^{-2}$**. The metaphor "a very faint stained-glass window" also overstates it — a stained-glass window at least lets you see color.

The truly readable channel is soft X-rays (284 eV, C K edge), with $\tau\approx1.3\times10^{-3}$, inter-tissue $\Delta\tau\sim10^{-3}$, and $\sim2\times10^{6}$ photons per pixel, accessible to conventional STXM. See `painting_render_v1` for details.

---

## 4. An unexpected result: the single atomic layer is the only configuration that "both has atoms and is 2D"

| Criterion | Value | Conclusion |
|---|---|---|
| Internal self-consistency bound $E_F<E_{\rm sub}$ | $2.30/2.88=0.80$ | **Pass** (margin 1.25 times) |
| External resolvability bound $E_{\rm probe}<E_{\rm sub}$ | $2.5\ \mathrm{eV}/2.88\ \mathrm{keV}=8.7\times10^{-4}$ | **Pass** |

$L=0.215$ nm gives $E_{\rm sub}=\pi\hbar c/L=2.88$ keV, while the single-layer areal density $2.15\times10^{19}\ \mathrm{m^{-2}}$ gives $E_F=2.30$ keV. **Both bounds are satisfied simultaneously** — the only time this occurs among all configurations in the project.

But the subsystem must be labeled (scope rule §1, four slots): the two-dimensionality here belongs to the **atomic layer**; the electron gas merely "happens" not to be excited into subbands, with a margin of only 1.25 times, so a slightly higher density would break it.

---

## 5. 2×2: "Being a painting" requires two independent conditions

|  | Atoms present (color/structure) | No atoms |
|---|---|---|
| **Unfolded (thin)** | **¬Area: 325 km² single atomic layer** ← Three-Body | E: 1 m², 1 fm, mirror |
| **Overlapping (thick)** | ¬E: 1 m², 7 cm slab | Both E and ¬E fail: mirror |

The Three-Body effect falls in the **upper-left cell**. It requires both "unfolded" and "atoms present" to hold simultaneously, which is precisely "giving up 1 square meter" rather than "giving up effective 2D."

---

## 6. Item-by-item comparison with the novel's descriptions

| Novel element | Physical counterpart | Self-consistent? |
|---|---|---|
| Canvas area explodes (solar system → huge plane) | Unfolding, area ×$10^{8}$ | **Self-consistent** |
| Image preserves internal structure (mountains, cities, planetary interiors) | Only unfolding can do this; overlapping cannot | **Self-consistent** |
| Those reduced to 2D die immediately | Consistent with row 1 NO-GO of the seven-row verdict | **Self-consistent** |
| The image has normal shading and color | Single-layer $\tau\sim10^{-7}$ (visible light) | **Not self-consistent** (5 orders of magnitude below the human-eye threshold) |

That is: **Liu Cixin got the area right and the contrast wrong.**

---

## 7. Conclusion

1. The 7 cm slab of ¬E is closest to the Three-Body effect in **composition** (the only one preserving atoms, chemistry, and color),
   but its flattening ratio is $L/\sqrt{A}=0.07$, making it a "slab," not a "painting."
2. The Three-Body effect = **unfolding**, at the cost of area ×$3.25\times10^{8}$ = 325 km²;
   spread out that far, the thickness is naturally 0.215 nm, **so it is itself two-dimensional**.
3. Therefore the correct branch name is **¬Area**, not ¬E.
4. Two costs: the visible-light channel does not exist ($\tau\sim10^{-7}$, see §3.1), and the only readable channel is 284 eV soft X-ray transmission;
   a freely suspended 325 km² single-layer film cannot support itself (a substrate is required).
5. **Contrast requires thickness, a pattern requires unfolding, and both draw on the same volume budget, so they cannot both be had.** This is the source of the entire contradiction.

> In one sentence: the Three-Body novel got the area of two-dimensionalization right and the contrast wrong; the ¬E branch got the contrast right and the area wrong.
> The two are opposite sides of the same coin, separated by a factor of $3\times10^{8}$ in area.

---

## 8. Citation conventions

1. When citing the "Three-Body effect," the area (325 km²) must be stated explicitly; 1 m² must not be assumed.
2. Do not generalize "the single atomic layer is 2D" into "the electron gas is 2D" — the subsystem and the margin (1.25 times) must be labeled.
3. This conclusion does not change `visualization_null_result_v1.md`: with all three hypotheses holding **simultaneously**, the set is still empty; this paper discusses the image after abandoning one of them, which is a quantification of the "failure-condition table."
4. It does not change the seven-row verdict or the branch ordering in `assumption_matrix_v1.md`.
