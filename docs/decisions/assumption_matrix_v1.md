# Three-Assumption Combination Matrix: Visual Effects of the 8 Combinations (v1)

**Version**: v1 (2026-11-21)
**Status**: **Conclusive statement (CLOSING)**
**Higher-level files**: `abandon_assumption_visual_v1.md` (quantification of abandoning one assumption),
           `visualization_null_result_v1.md` (null result when all three hold)
**Evidence level**: geometry/thresholds are CHECK; fireball and energy partition are ESTIMATE; dependency structure is ARGUMENT
**Reproduction**: `src/analysis/assumption_matrix_v1.py` → `runs/ANALYSIS/assumption_matrix_v1.txt`

---

## 1. Main Table

Let **E** = effective two-dimensional reduction holds, **S** = smooth two-dimensional reduction holds, **W** = weak interaction preservation holds. Fix $\Sigma=70\ \mathrm{kg/m^2}$.

| Combination E/S/W | State of matter | Energy budget | What the eye sees | Duration | Verdict |
|---|---|---|---|---|---|
| ✓✓✓ | 1 fm, 0.30 ρ_nuc, $E_F=73.4$ MeV | 41.2 Mt all locked inside | mirror-like (ΔR=0.001 between the two states), no self-emission | 3–5 ns | **empty** |
| ✓✓✗ | after neutronization $Y_p=0.005$, $E_F=21.5$ MeV | 23.1 Mt → ν (invisible); 18.1 Mt still locked inside | mirror-like, no self-emission; ν burst requires a 10 kt-class detector | 3 ns | **empty** + neutrino burst |
| **✓✗✓** | 1 fm disintegration → thermalization in meter-scale gas column | 20.6 Mt kinetic energy → fireball; 20.6 Mt γ | **41 Mt fireball, 99× solar surface** | **1–10 s color** | **fireball (most spectacular)** |
| ✓✗✗ | ν burst first (3 ns), then disintegration | 23.1 Mt → ν; KE 4.4–15.5 Mt | weaker fireball (2–5× dimmer) | ~1–10 s | weak fireball + ν burst |
| ✗✓✓ | 7 cm, $1000\ \mathrm{kg/m^3}$, atoms intact | no extra energy (not compressed) | passively reflects 35% of sunlight (**brightness** same as a white wall; **information** see §2.1) | infinite | static slab (structure genuine, but unreadable in reflected light) |
| ✗✓✗ | same as above (W has no object: $\mu_e=4.15$ keV) | same as above | same as above | infinite | ≡ ✗✓✓ |
| ✗✗✓ | same as above (S has no object: no degeneracy pressure) | same as above | same as above | infinite | ≡ ✗✓✓ |
| ✗✗✗ | same as above (all three fail) | same as above | same as above | infinite | ≡ ✗✓✓ |

> "No extra energy" in the table means: without compression there is no 41.2 Mt. **The 41.2 Mt is not the energy of the human body,
> it is the degeneracy energy injected by compressing to 1 fm**; without compression it does not exist.

---

## 2. 8 Combinations → 5 Outcomes

| Outcome | Combinations | In one sentence |
|---|---|---|
| Empty (mirror-like, 3 ns) | {111} | all assumptions hold, nothing can be seen |
| Empty + neutrino burst | {110} | energy goes via neutrinos instead; still zero for the eye |
| **41 Mt fireball** | **{101}** | **the only spectacular case** |
| Weak fireball + ν burst | {100} | half the energy is carried away by neutrinos first |
| 7 cm static slab | {011, 010, 001, 000} | the four combinations are **the same thing** |

**The last four combinations are not four different things.** Their physical states are completely identical, because once E is abandoned, S and W lose their objects of action (§3).

### 2.1 Correction: ✗✓✓ Is Not "No Details", but "Details Are Not in the Reflected Light"

The previous version wrote this row as "same as a white wall", which described only **brightness** but was read as **information content**. The two are not the same and must be separated into three independent quantities (settlement in `runs/ANALYSIS/slab_visibility_v1.txt`):

| Quantity | Value | Is it rich |
|---|---|---|
| Brightness | 35% reflectance | same order as a white wall (the only basis for the word "white wall") |
| Resolution (geometric) | the eye can resolve $1.9\times10^8$ points on 1 m² | extremely high |
| Information (statistical) | the values at these points are nearly identical ⇒ about 1–2 bit | **nearly zero** |
| Existing structure (internal) | $\sim10^{11}$ cell-level differences, organ colors differ greatly | extremely high, but invisible |

The bridge is **opacity**. The effective penetration depth of visible light in soft tissue is only $0.09$–$1.6$ mm ($\delta=1/\sqrt{3\mu_a(\mu_a+\mu_s')}$, literature optical parameters), while the slab is 70 mm thick ⇒ **visible light reaches only 2.2% of the depth; the remaining 98% does not exist on the reading surface**. Reflective imaging satisfies $I(x,y)=R_{\rm surface}(x,y)\,L_{\rm env}(x,y)$ — pixels are determined solely by the surface layer, regardless of whether the interior is brain, bone, or empty.

Thus the precise meaning of "white wall" is: **the surface is a skin layer whose composition is statistically nearly uniform, so high resolution does not bring high information** (1.9×10⁸ pixels × 1–2 bit ≈ a sheet of A4 white paper).

The relationship among the three can be summarized in one sentence:

> Resolution is **geometry**, information is **statistics**, brightness is **photometry**.
> ✗✓✓ passes on the first and third but fails only on the second — and the second is what "what you can see" means.

**The details have not disappeared; they merely require switching channels to be read:**

| Channel | Readable content | Cost |
|---|---|---|
| Reflected visible light (front) | monochromatic, nearly uniform epidermis + $\sim2\times10^5$ millimeter-scale folds with shading | none |
| **Side view of 7 cm edge** | layered profile of skin/fat/muscle/bone (700 cm²) | none (just a change of viewpoint) |
| **X-ray transmission / CT** | complete 3D structure with $5.6\times10^8$ voxels | requires a $50$ keV source; $\tau=1.6$, 20% transmission |
| Chemical/fluorescence staining | converts compositional differences into color differences | introduces exogenous labels |

Among these, **the side view is zero-cost**: the same slab looks like a white wall from the front and a geological cross-section from the side. Shape has **redirected** the information, not destroyed it.

---

## 3. Dependency Structure: E Is the Only Energy Source

| Quantity | E holds ($L_z=1$ fm) | ¬E (7 cm) | Ratio |
|---|---|---|---|
| $L_z$ | $10^{-15}$ m | $7\times10^{-2}$ m | $7\times10^{13}$ |
| $n_e$ | $2.2\times10^{-2}\ \mathrm{fm^{-3}}$ | $3.1\times10^{-16}\ \mathrm{fm^{-3}}$ | $7\times10^{13}$ |
| $\mu_e$ | 73.4 MeV (2D) / 171 MeV (3D) | $4.2\times10^{-3}$ MeV | $\sim10^{4}$–$10^{5}$ |
| Degeneracy pressure | $8.6\times10^{16}$ N/m | negligible | — |
| Neutronization threshold 1.293 MeV | far exceeded | off by 300× | — |

Conclusion:

- **¬E ⇒ no MeV-scale energy density ⇒ S has nothing to do** (no degeneracy pressure to explode)
- **¬E ⇒ $\mu_e\ll1.293$ MeV ⇒ W has nothing to do** (neutronization does not occur)

So once ¬E holds, the values of S and W no longer affect any observable. This is why the four combinations degenerate.

---

## 4. Three Boundaries (Calculated)

| Boundary | Condition | Value |
|---|---|---|
| E definition bound | $E_{\rm sub}=E_F$ | $L_z<8.45$ fm |
| E registration bound (K1 threshold) | ratio $\ge4.25$ | $L_z\le1.99$ fm |
| W validity bound | $\mu_e=1.293$ MeV (3D) | $L_z<2.32$ nm |

**The domain of W strictly contains the domain of E** (2.32 nm $\gg$ 8.45 fm). Therefore:

- whenever E holds, W is necessarily valid — so 110 and 111 are two different physical cases;
- the converse does not hold: in the narrow band $8.45\ \mathrm{fm}<L_z<2.32\ \mathrm{nm}$, W is valid while E is not.
  Abandoning W within this band still causes neutronization, but the matter remains MeV-scale plasma with no atoms and no self-emission,
  so it is **still classified visually as "empty"** and is not given a separate row.

---

## 5. The Only Simultaneous Condition

For "the human eye to see it", all three must hold simultaneously:

| Condition | Requirement | Provided by |
|---|---|---|
| (a) MeV-scale energy available for release | degeneracy pressure $8.6\times10^{16}$ N/m | **E holds** |
| (b) it is allowed to be released | the process is unconstrained and does not impose quasi-static conditions | **¬S** |
| (c) energy is not carried away by neutrinos | no neutronization (preserving 44% of the kinetic energy) | **W holds** |

**The only solution is 101.** That is:

> **Visual intensity has no monotonic relationship with "the number of assumptions holding". When all three hold, the result is empty,
> while the only visible combination is "two-dimensional reduction holds but the process does not".**

This is the most counterintuitive item in this document: **the moment you can see it is precisely when two-dimensional reduction has just failed**, not when it holds. In 101, E still holds (the slab really is thin enough for 2D), but S is abandoned (it is disintegrating) — so the picture is "the death of a two-dimensional object", not "a portrait of a two-dimensional object".

---

## 6. Reading and Citation Rules

1. When citing this table, the **combination notation** (E/S/W) must be retained; one must not write only "abandoning smoothness is spectacular", otherwise the premise "E must hold simultaneously" is lost.
2. "✗" must not be read as "the assumption has been falsified". ✗ is a **scenario setting**, not a physical conclusion; the physical conclusion is "the three cannot hold simultaneously in the same scenario" (see `internal_consistency_v1`).
3. The neutrino quantities in rows 110 and 100 are ESTIMATE (the 0.56 coefficient is the 3D UR value); they must not be used as observational predictions.
4. Rows 011/010/001/000 must be cited jointly; splitting them into four independent conclusions is forbidden.
5. This table does not address "whether such a state can exist", only "what the human eye sees if it exists".

---

## 7. Relationship to Other Documents

| Document | Relationship |
|---|---|
| `visualization_null_result_v1.md` | row 111 of this table is its conclusion; this document fills in the other 7 rows |
| `abandon_assumption_visual_v1.md` | detailed calculations for rows 101/011/110 of this table |
| `internal_consistency_v1.py` | explains why 111 is the empty set (K1–K6 conflicts) |
| `scifi_boundary_v1.md` | specification of the four knobs; this table is the exhaustive enumeration of its "visual layer" |
| `instrument_visualization_v2.py` | instrument-visible version of row 111 (keV spectrum) |

---

Content generated by AI
