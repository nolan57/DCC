# "Is this really how it unfolds?" — A ruling on the status of unfolding (unfold_is_real v1)

**Date**: 2026-11-21 12:5x  **Status**: OPEN (answers Q1–Q4, changes no existing conclusion)
**Upstream**: `unfold_appearance_v1.md` (rendering), `three_body_comparison_v1.md` (area), `internal_consistency_v1.md` (K5)
**Recalculation**: `src/analysis/unfold_is_real_v1.py` → `runs/ANALYSIS/unfold_is_real_v1.txt` (6/6 PASS)

---

## 0. In one sentence

> **The area is computed, the interior of each slice is unchanged, the order is not given by physics, and the process is not "unfolding" but "cutting."**
> This painting is not a flattened person but a sequentially archived tomographic record: 8.1 billion mutually disconnected slices, each 1:1 undeformed.

---

## 1. The precise form of the question

"Is this really how it unfolds (under the current hypotheses)?" must be split into four separately decidable sub-propositions, otherwise it cannot be answered:

| Sub-proposition | Verdict | Basis |
|---|---|---|
| Q1: Is the area 325 km² derived from the hypotheses? | **The order of magnitude is; the specific value comes from "single atomic layer"** | Three inequalities bracket the window [280, 339] km² |
| Q2: Is the interior of each square tile unchanged? | **Yes, zero deformation** | The mapping within a slice is the identity; tile area = slice area |
| Q3: Is "arranged head-to-foot into a human figure" determined by physics? | **No, it is an encoding convention** | Physics gives only the set of fragments, not an ordering |
| Q4: Can the process be continuous (smooth)? | **No, ruled out at the theorem level** | No continuous injection from R³ to R² exists |

---

## 2. Q1: The area is arithmetic, not a painting

The three constraints each give one inequality:

1. **Require 2D**: E_F(A) < E_sub(A), where E_F ∝ A^(−1/2) and E_sub ∝ A (since L_z = V/A). Solving A³ = 2NV²/π gives **A > 279.5 km²**.
2. **Require atoms to survive**: E_sub = πħc/L_z < E_bind ≈ 3 keV, giving L_z > 0.2066 nm, i.e., **A < 338.8 km²**.
3. **Do not impose a density change**: A·L_z = V.

The window is **[280, 339] km², only 1.21 times wide**. The only physically meaningful choice within the window is L_z equal to the atomic spacing d (any thinner and no atomic layer exists), giving **A = V/d = N d² = 324.9 km²**. Thus: the order of magnitude 10⁸ m² is forced by arithmetic (neither 1 m² nor 10¹² m²); the specific value 325 comes from the single additional choice of a "single atomic layer." **This step contains no assumption about "how to arrange" things.**

---

## 3. Q2: The interior of each slice is unchanged

Each square tile is 0.200 m × 0.200 m with area 0.0400 m², exactly equal to the cross-sectional area of one slice (A_c = V/H = 0.070/1.75). The mapping within a slice is the identity:

$$(x,y,z)\ \longmapsto\ \big(0.2\,i(z)+x,\ 0.2\,j(z)+y\big)$$

The 8.62×10¹⁷ atoms inside a tile, spanning 9.28×10⁸ atoms per side, all remain in place. **The lungs, heart, and spine can be recognized in the rendered image precisely because a tile is the slice itself, unstretched.**

---

## 4. Q3: The order is not physics

The complete list given by physics is only: 8.12×10⁹ mutually disconnected tiles + 0.04 m² each + total area 324.9 km². The numbering order of the tiles is a permutation π. Readable arrangements (adjacent numbers placed adjacent) occupy a constant number among the 8.12×10⁹! permutations, with fraction < 1/N! ≈ 0.

> **"Being a painting" is a measure-zero encoding choice, not a physical conclusion.** All the information is present, but reading it requires knowing that permutation.

This was not stated explicitly before: `three_body_comparison_v1` said "unfolding gives a pattern," implicitly assuming "laying out in order." It is now explicit: the pattern comes from the arrangement convention, not from unfolding itself.

---

## 5. Q4: The process cannot be continuous (theorem)

### 5.1 Theorem

**No continuous injection from R³ to R² exists.**

Proof (one sentence): if f is a continuous injection, then f continuously bijects the unit sphere S² onto f(S²) ⊂ R², so S² embeds homeomorphically in R²; but S² cannot be embedded in R² (Hurewicz–Wallman, invariance of dimension). Contradiction. ∎

**Corollary**: between "each atom occupies one lattice site, with no overlap" (a bijection) and "the process is continuous" (smoothness), the **feasible set is empty**. This is not a matter of "how many times off" — there is not a single one.

### 5.2 Since it must break, count it precisely

| Quantity | Value |
|---|---|
| Adjacent atom pair across layers: initial spacing | 0.2154 nm |
| Same pair: final spacing | 0.200 m (tile side length) |
| **Stretch factor** | **9.28×10⁸** |
| **Number of fracture surfaces** | **8.12×10⁹** |
| Area of each fracture | 0.0400 m² |
| **Total fracture area** | **3.249×10⁸ m² = 324.9 km²** |

The total fracture area exactly equals the area of the painting — because each cut exposes the full cross-section of one slice. This is not a coincidence; it is two ways of saying the same thing.

### 5.3 Cost: bond-breaking energy

Broken bonds ≈ 2.8×10²⁸ × 4 eV ≈ **1.8×10¹⁰ J**; total energy of the 2D Fermi gas u₂D·A = 5.3×10³ J/m² × 3.25×10⁸ m² ≈ 1.7×10¹² J. Ratio **1.0×10⁻²**.

> **Cutting does not pose an energetic obstacle. The obstacle lies in strain, not in energy.**

### 5.4 Relation to K5

`internal_consistency_v1`'s K5 is "smoothness ↔ timescale separation: no separation" (dynamical). This item is its **geometric version**, and stronger: K5 says "there is no time to split into two stages," while this item says "not even one continuous mapping exists." It is recommended to register it as **K5b (geometric)**: smooth deformation + no overlap = infeasible.

---

## 6. Three candidate mappings

| Configuration | Process | Atomic occupation | Area (m²) | E_F (keV) | Outcome |
|---|---|---|---|---|---|
| **M-A flattening** (preserve x,y, L_z→0) | Continuous | Overlapping (bijection fails) | 4.0×10⁻² | 2.07×10⁵ | Atoms disintegrate |
| **M-B isometric unfolding** (this figure) | Fractures at 8.1×10⁹ places | Bijection | 3.25×10⁸ | 2.30 | Atoms intact |
| **M-C random permutation** (same physical quantities as M-B) | Fracture | Bijection | 3.25×10⁸ | 2.30 | Atoms intact but no image |

The E_F of M-A uses A = A_c (the harshest convention); even with the most permissive A = 1 m², E_F is still 41 MeV, another 4 orders of magnitude higher — **the conclusion is insensitive to the choice of region**. M-A also has a second cause of death: L_z→0 makes E_sub diverge, so every electron is injected with energy ≥ E_sub.

The three hypotheses + "structure presentation" leave only M-B / M-C. The two have identical physical quantities, differing only in the order of the tiles.

---

## 7. The fourth implicit hypothesis (must be pointed out)

All of the above rests on **A·L_z = V (volume conservation)**. **Volume conservation is not one of the three hypotheses**; it is a habit of three-dimensional geometry. Abandon it → the area does not grow → one falls straight back onto the M-A flattening branch → atoms disintegrate. So the route of "unfolding" truly presupposes two additional items:

1. **Allow area growth** (equivalent to allowing volume conservation);
2. **Do not require the object to survive** (already made explicit in this project, see §0 of the roadmap).

Item 2 has already been stated explicitly in this project; item 1 had not previously been stated separately — it is now added.

---

## 8. Final positioning of the rendered figure

`unfold_appearance_v1.png` is not a process snapshot but an **archival figure**:

- View C (18×18 array): the archive catalog after 4.64×10⁶-fold decimation, the only view in which a human figure can be read;
- View B (3×3 neighbors): adjacent tiles differ by only 0.215 nm and are mutually disconnected — **adjacency means fracture**;
- View A (18 km overhead): only head-to-foot 1D information remains;
- View D-left/right: the same tile, empty under visible light and an anatomical image at 284 eV.

> **Closing in one sentence**: under the three hypotheses, "unfolding" is not a flattened person but cutting the object along 8.1 billion atomic planes and translating each slice by no more than 25 km into its own cell. Within a slice is anatomy; between slices is vacuum. This is both why it can preserve structure and why it cannot be "smooth."

---

## 9. Open items / next steps

- [ ] Whether to merge K5b into `internal_consistency_v1` (requires rerunning that module)
- [ ] Information readability of M-C (random permutation): given the permutation, how many photons are needed to reconstruct the human figure? Is it the same as for M-B? (Expected: the same, because the photon budget depends only on τ)
- [ ] Topology of the fracture surfaces: with 8.12×10⁹ parallel planar cuts, after cutting is each slice connected or broken into multiple "organ blocks"?
