# Registration — the four dimension anchors (`DIM-ANCHOR`)

**Registered** 2026-11-22, before any measurement in `src/route/dimension_anchor_check.py` ran.
**Object of record** the locked `DEMO-1` deposit (`docs/specs/demo_object_v1.md`, sha256 `afe855c2…4633`):

| constant | value |
| --- | --- |
| `M` shells | `4` |
| `S` grid side | `65,536` |
| `H` height | `0.2300 m` |
| `δ` layer pitch | `2.15e-10 m` |
| `pitch` site pitch | `0.400100 m` |
| `N` layers/shell | `1,069,767,441` |
| `pieces = M·N` | `4,279,069,764` |
| `cells = S²` | `4,294,967,296` |
| free cells | `15,897,532` |
| `σ` rule | `p = k·N + n`, cell = `hilbert₁₆(p)` |

## The claim under adjudication

Four mathematical anchors are offered as the foundation of `route_terminus_v1`'s conclusion:

1. **Brouwer (1910)** — homeomorphic spaces have equal dimension ⇒ no homeomorphism ℝ³ → ℝ².
2. **Cantor (1877)** — a bijection exists between a solid 3-ball and a plane, but destroys relative position.
3. **Hilbert** — a continuous surjection `[0,1] → [0,1]²` exists but cannot be injective; 3D points collide.
4. **Kakeya (2025)** — 3D omnidirectional information has an incompressible dimensional lower bound; no folding fits it into a 2D container.

Conclusion offered: *a lossless physical collapse 3D → 2D is strictly prohibited; a one-to-one map into 2D can be a file, not a picture; therefore the DCC adopts lossless serialization.*

Adjudicated on three questions per anchor, in this order: **(a) is the mathematics as stated true; (b) is the attribution correct; (c) does the deposit lie inside the anchor's hypothesis.** Question (c) is the one that decides the conclusion, and it has not been asked before this round.

## Predictions

### A. Scope — the question that decides everything

- **P1** The deposit's domain (`4,279,069,764` plate indices) and codomain (`4,279,069,764` occupied grid cells, min separation `pitch`) are both **finite discrete** spaces, hence both of Lebesgue covering dimension **0**. A bijection between discrete spaces is a homeomorphism. Therefore the deposit **satisfies** Brouwer at dimension 0 (`0 = 0`); it is an *instance* of the theorem, not an exception to it.
- **P2** Each of the four anchors has a **continuum** (or an open subset of ℝⁿ) in its hypothesis. The deposit has none — it is a finite set. Therefore **0 of 4** anchors has the deposit inside its hypothesis class, and the deposit violates none of them.

### B. Brouwer

- **P3** `docs/` contains **0** occurrences of "Brouwer" — the anchor is new to the record, not a restatement of something already ruled on.
- **P4** The hypothesis of invariance of domain is *"`U ⊆ ℝⁿ` open"*. The deposit's domain has **empty interior in ℝ³**: the largest open ball inside it has radius `0`, and the largest ball containing no second site has radius `pitch/2 = 0.200 m`. So the hypothesis fails on the first word.
- **P5** The standard citations are **1911** (invariance of *dimension*, Math. Ann. 70) and **1912** (invariance of *domain*, Math. Ann. 71); **1910 is not the standard year.** Recorded as a provenance note, not a mathematical defect.

### C. Cantor

- **P6** The existence of an injection is guaranteed by **cardinality alone**, with no geometry involved. The number of injections is `C!/(C−N)!`, so *naming* one costs `log₂(C!/(C−N)!)` ≈ **1.31e11 bits (≈16.4 GB)** — the same order as the deposit it describes. The rule `p = kN + n` costs 0 bits. Predicted band `1.25e11 … 1.40e11` bits.
- **P7** The deposit is one such injection and preserves cardinality **exactly**: `4,279,069,764` distinct cells occupied, `15,897,532` free.
- **P8** "Structure shattered" reproduces the archived `MR2-D` interface row exactly at `n = 0`: `d₃ = 0 → d₂ ∈ {12,401.7, 12,085.3, 12,989.4} m`. Over a sample of `n` the mean stays inside `[1.1e4, 1.4e4] m`. (Note: the archived figure sampled `n = 0` only; this round measures its representativeness.)
- **P9** The "3D solid sphere → plane" framing adds **nothing**: the same bijection exists between any two sets of cardinality `𝔠`, so the theorem's content is cardinality, not dimension. Its 3D-ness is decoration.

### D. Hilbert

- **P10** At finite order `k` the Hilbert index map is a **bijection** — `4^k = (2^k)²` exactly, exhaustively `0` collisions for `k ≤ 6`, and `0` collisions by sampling at `k = 16`. The finite Hilbert curve is therefore also a homeomorphism between 0-dimensional spaces.
- **P11** The statement is dimension-mis-stated: the Hilbert curve is `1D → 2D`. Non-injectivity is a property of the **parameter**, not of three-dimensional points. As written, the sentence describes a map that does not exist in the sentence.
- **P12** Non-injectivity is **exclusively** a continuum-limit phenomenon: maximum multiplicity `= 1` at every finite order measured. It therefore does not touch the deposit, which uses the finite bijection as an index.
- **P13** Consequence: Hilbert's non-injectivity is not an obstacle to this record. The obstacle to rendering is resolution (`2¹⁶` vs `2⁹`), already recorded in `route_terminus_v1` §4.

### E. Kakeya

- **P14** The theorem is real as of **24 Feb 2025** (Wang–Zahl, `dim_H = dim_M = 3` for Kakeya sets in ℝ³; `n ≥ 4` still open), but its object is a **set's Hausdorff/Minkowski dimension**. It contains **no** statement about maps, channels, information, folding, or containers. The gloss is an interpretation, not a corollary.
- **P15** "Lossless" is **referent-dependent**, and both readings are measurable: with respect to the **plate inventory** it is exact (bijection, `P7`); with respect to the **object** it is false (`I(canvas ; r₄) = 0` bits; six objects → one digest, `DEPOSIT-BLIND`). The unqualified word is ambiguous between a true and a false claim.
- **P16** Taken **literally**, the Kakeya gloss is *true of the deposit* — precisely because the deposit carries no 3D geometry — so it **corroborates `DEPOSIT-BLIND`** and cannot simultaneously support unqualified "lossless serialization". Also: a finite set contains **no line segment**, so the deposit contains no Kakeya set in any direction (`0`), and the theorem applies to it even less than the other three.

### F. The conclusion

- **P17** "Strictly prohibited" holds for **1 of 3** map classes: continuous-injective (Brouwer). It is false for continuous-surjective (Peano 1890 / Hilbert 1891) and false for discontinuous-bijective (Cantor 1877). The unqualified prohibition is therefore an overstatement that the three anchors, taken together, refute.
- **P18** "No picture exists" is a **resolution** fact (`2¹⁶` vs `2⁹`, gap `2¹⁴`), not a topological one. The four anchors establish *no embedding*; the picture prohibition comes from `route_terminus_v1` §4, which does not use any of them.

## What would make this registration wrong

| if | then |
| --- | --- |
| the deposit's map is not a bijection | `P1`, `P7`, `P10` fall, and `DEPOSIT-BLIND`'s proof line is void |
| `log₂(C!/(C−N)!)` lands outside `[1.25, 1.40]e11` | `P6`'s figure is wrong (the qualitative claim may survive) |
| any anchor's hypothesis is satisfied by a finite set | `P2` falls and the scope argument collapses |
| the interface distances do not reproduce | `P8` falls; `MR2-D`'s archive and this run disagree |
| multiplicity `> 1` at finite order | `P12` falls; the Hilbert curve is not a bijection at finite order |

## Provenance

`NEITHER` — this adjudicates the **validity of citations**, not the object. It establishes no physics, sets no threshold, and creates no readable cell. It cannot move `G1`.
