# Decision: Which Assumption to Abandon Yields the Most Spectacular Visual Effect (v1)

**Version**: v1 (2026-11-21)
**Status**: **Conclusive statement (CLOSING)**
**Higher-level file**: quantification of the "failure conditions table" in §5 of `docs/decisions/visualization_null_result_v1.md`
**Evidence level**: Branch B fireball quantities are ESTIMATE (Sedov + effective temperature); geometry and optical thickness are CHECK; mutual exclusivity is ARGUMENT
**Convention**: $\Sigma=70\ \mathrm{kg/m^2}$ (70 kg / 1 m²), $E=1.724\times10^{17}\ \mathrm{J/m^2}=41.2\ \mathrm{Mt}$
**Reproduction**: `src/analysis/abandon_assumption_visual_v1.py` → `runs/ANALYSIS/abandon_assumption_visual_v1.txt`

---

## 1. Conclusion

> **Abandon "smooth two-dimensional reduction" for the most spectacular visual effect — a 41 Mt, ~10 s
> colorful fireball with surface brightness about a hundred times the solar surface.**
>
> **But the correlation of this splendor with "two-dimensional reduction" is 0.** What you see is its disintegration,
> not its realization; swap in any other cause of 41 Mt and the picture is completely identical.

If the question is "to see two-dimensional reduction itself", the answer changes to **abandon "effective 2D"** — that yields a 7 cm thick static slab with intact anatomical structure: extremely information-rich and permanently viewable, but it does not emit light and is not spectacular, merely clear.

**These two cannot be had at the same time, and the reason is quantifiable** (§4).

---

## 2. Itemized Numerical Values for the Four Branches

| Branch | Peak visual intensity | Visible duration | Number of structural degrees of freedom | Illuminance at 1 km | Self-luminous |
|---|---|---|---|---|---|
| **A** abandon effective 2D (7 cm slab) | reflects 35% of sunlight (brightness same as a white wall) | infinite | $1.9\times10^8$ pixels for the human eye, but **only 1–2 distinguishable classes** | same as white wall | no |
| **A′** abandon 1 m² (single atomic layer) | visible light $\tau\sim10^{-7}$ (no image); 284 eV $\tau\sim10^{-3}$ (readable) | infinite | $\sim10^{19}$ atoms, monolayer with no thickness structure | below white wall | no |
| **B** abandon smoothness | **99× solar surface** | **~10 s** | $\sim10^{2}$ | $5\times10^{6}$× solar constant | **yes** |
| **C** abandon weak-interaction preservation | 0 (neutrinos escape) | 3 ns | $\sim1$ | 0 | no |

> **"Same as a white wall" describes only brightness, not information.** Branch A contains $\sim10^{11}$ cell-level differences internally,
> and organ colors differ greatly, but all of this lies behind opacity (visible light penetrates 0.09–1.6 mm; slab thickness 70 mm).
> Reflective imaging can only read the surface layer: high resolution × low contrast = nearly zero information.
> Switching channels makes it readable — a side view of the 7 cm edge gives a layered profile, and X-ray CT gives $5.6\times10^8$ voxels.
> See `docs/decisions/assumption_matrix_v1.md` §2.1 and `runs/ANALYSIS/slab_visibility_v1.txt` for details.

### 2.1 The Two Premises of Branch B (Check First, Compute Second)

**Premise one: the slab itself is optically thick.** $n_e=2.20\times10^{43}\ \mathrm{m^{-3}}$ and $L_z=1$ fm give a Thomson optical thickness $\tau=1.46$ — **exactly a thin photosphere**, neither transparent light leakage nor a thick blackbody. Its internal energy therefore leaks out as a blackbody spectrum at $T_{\rm bb}=59.5\ \mathrm{MeV}$, **entirely invisible to the human eye, being in the gamma band**. The expansion timescale $L_z/c=3.3\times10^{-24}$ s, and adiabatic cooling finishes before that.

**Premise two: the visible part is kinetic energy, not internal energy.** The energy is split in half:

| Channel | Energy | Fraction | Visibility |
|---|---|---|---|
| Internal energy → 60 MeV gamma | $8.63\times10^{16}$ J/m² | 50% | **invisible** |
| Kinetic energy → thermalized in air | $8.62\times10^{16}$ J/m² (20.6 Mt) | 50% | **visible fireball** |

Proton kinetic energy is 13.1 MeV with an air range of ~1 m, so the kinetic energy is deposited within a meter-scale gas column → strong shock → fireball.

> **If this is written backwards, the entire conclusion of Branch B must be rewritten.** The first v1 draft mistakenly computed $\tau$ as $10^{-12}$ (an $n_e$ unit-conversion error), concluding that "the slab is transparent and leaks light". Rechecking gave $\tau=1.46$.
> Both paths give the same visible-light conclusion (in both, "the human eye cannot see the slab's own radiation"), but the physical narratives differ.

### 2.2 Fireball Evolution (Sedov, ESTIMATE)

$R(t)=1.15\,(E/\rho)^{1/5}t^{2/5}$, $T_{\rm eff}=(L/4\pi R^2\sigma)^{1/4}$, taking $L=0.5E/t$:

| $t$ | $R$ | $T_{\rm eff}$ | Human eye |
|---|---|---|---|
| 0.001 s | 196 m | $2.4\times10^{5}$ K | bluish/UV |
| 0.1 s | 1.24 km | $3.0\times10^{4}$ K | bluish/UV |
| **1 s** | **3.11 km** | **$1.06\times10^{4}$ K** | **visible color** |
| 3 s | 4.82 km | 6455 K | visible color |
| 10 s | 7.80 km | 3755 K | visible color |
| 30 s | 12.1 km | 2290 K | IR/dark |

**The visible-color window (2500–12000 K) ≈ 1 s – 10 s** is 500 times the human-eye integration time (20 ms). The color sweeps from 10,000 K → 2500 K: white-blue → white → yellow → orange → dark red. This is the entire source of its "spectacle" — **not shape, but a temporal sweep of color temperature**.

---

## 3. Why B Wins: It Is Unique in Three Metrics Simultaneously

| Metric | B | Other three branches |
|---|---|---|
| Self-luminous | yes (unique) | all passive and requiring external illumination, or directly 0 |
| Brightness | 99× solar surface; $5\times10^6$× solar constant at 1 km | brightest is only "same as a white wall" |
| Duration / eye integration | $5\times10^{2}$ | A infinite but static; C is $1.5\times10^{-7}$ |

A special property of B must be noted: **the illuminance at 1 km is already blinding** ($5\times10^6$ solar constants). It is therefore not "a spectacle one can enjoy viewing", but an event "not to be looked at directly — only viewed from afar or through filters". Splendor and "viewability" are separate here as well.

---

## 4. Key Column: How Much of This Splendor Comes from "Two-Dimensional Reduction" Itself

| Branch | Attribution | Explanation |
|---|---|---|
| A | **0%** | the spectacle comes from "a human compressed into a 7 cm slab", which is mere flattening. Any 70 kg object flattened to 7 cm looks the same |
| A′ | **~30%** | a monolayer is genuinely a 2D material (graphene-like), so 2D character is real; but it relies on enlarging the area to 379 km², not on compressing the thickness to 1 fm |
| B | **0%** | a 41 Mt explosion does not care what triggered it. Two-dimensional reduction is entirely absent from the picture |
| C | — | no spectacle to attribute |

**These four 0% values are the most important result of this document.** They show that once any of the three assumptions is abandoned, the mechanism that can still produce "spectacle" **no longer depends on two-dimensional reduction** — it depends either on energy (B), or on chemistry (A), or produces nothing at all (C).

---

## 5. Mutual Exclusivity: Why "Bright and Informative" Is Impossible

| What is wanted | Energy scale | Corresponding physics |
|---|---|---|
| Brightness (self-luminous, visible band) | $\sim 10^{7}$ eV | hot plasma, $T\gtrsim10^{4}$ K |
| Content (color, texture, structure) | $\sim 5$ eV | chemical bonds / interband transitions |

The two differ by **$10^{7}$×**. The same matter cannot be at both energy scales at once: where atoms exist it is not hot enough; where it is hot enough atoms no longer exist.

**This is not a technological limitation, it is the arithmetic of energy scales.** Therefore "splendor" in this problem has two mutually exclusive aesthetics:

- **Aesthetics of energy** (B): bright, fast, detail-free, gone once seen;
- **Aesthetics of structure** (A): dark, static, extremely detailed, requires you to supply the lighting.

There is no third. The Three-Body-style "spectacular yet clear tableau" requires both simultaneously, and is therefore outside the solution space.

---

## 6. Branch A's Optimum Is at 7 cm, Not Thinner

Once "effective 2D" is abandoned, thickness is free, but "splendor" has an internal optimum:

| Density | $L_z$ | Atomic spacing | Result |
|---|---|---|---|
| $1000\ \mathrm{kg/m^3}$ (water) | **7.0 cm** | 2.55 Å | atoms/chemistry/anatomy intact, with color ← **optimum** |
| $7000\ \mathrm{kg/m^3}$ (iron) | 1.0 cm | 1.33 Å | chemical bonds compressed and deformed, color shifted |
| $2.3\times10^{17}$ (nuclear density) | $3.0\times10^{-16}$ m | $4.2\times10^{-15}$ m | no atoms, back to a mirror |

**Thinner and it becomes pressure-ionized (losing color); thicker and it reverts to an ordinary object (losing the premise of "two-dimensional reduction").** The number 7 cm comes purely from $70\ \mathrm{kg}/1\ \mathrm{m^2}/1000\ \mathrm{kg\,m^{-3}}$ and contains no model assumptions (CHECK level).

A′ takes another route: keeping the atomic spacing at 3 Å and instead enlarging the area to **379 km²**: the result is a genuine one-atom-thick film with 2D character, but its absorptance is only 2.3%, a nearly transparent iridescent film. **It is the only visible object for which "2D character is true", and also the only one that is almost invisible.**

---

## 7. Relationship to Existing Documents

| Document | Relationship |
|---|---|
| `assumption_matrix_v1.md` | this document discusses only "abandoning one"; that file exhaustively enumerates all 8 combinations of the three assumptions and gives the complete matrix |
| `visualization_null_result_v1.md` §5 | this document quantifies the "failure conditions" column of that table; it does not overturn its conclusion |
| `scifi_boundary_v1.md` §7.5 | this document adds the item that, beyond the "four knobs", the visual goal also requires self-luminosity |
| `effective_2d_definition_v1.md` | branches A/A′ clearly fall on the "not effectively 2D" side and do not constitute exceptions to that definition |
| `instrument_visualization_v2.py` | the keV spectrum in that file is the "held-down" static case; B is the "not held-down" dynamic case; the two are complementary |
| `three_body_comparison_v1.md` | quantitative comparison of branch A with the dual-vector foil in *The Three-Body Problem*: A (1 m² slab) has "right composition, wrong geometry"; the true Three-Body effect is the 325 km² monolayer with ¬area |

---

## 8. Citation Rules

1. When citing this document, one must not say only "the explosion is the most spectacular"; the **0% attribution** must be given at the same time, otherwise it will be misread as "two-dimensional reduction itself is spectacular".
2. All quantities in branch B are ESTIMATE (Sedov + effective temperature, $\pm$ factor-of-2 order of magnitude) and must not be cited as DCC observational predictions.
3. The 7 cm of branch A is CHECK level and may be cited directly; but it must be noted that "this is no longer two-dimensional reduction".
4. This document must not be used to infer "whether this physical state exists" — it discusses only **visibility**, not existence.

---

Content generated by AI
