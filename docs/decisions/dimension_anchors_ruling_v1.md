# Ruling — the four dimension anchors (`DIM-ANCHOR`)

**Decision date** 2026-11-22 · **Submission** `runs/DIM/dimension_anchors_submission_verbatim.md`
**Registration** `runs/DIM/dimension_anchors_registration.md` (`P1`–`P18`, locked before measurement)
**Measurement** `src/route/dimension_anchor_check.py` → `runs/DIM/dimension_anchors_results.txt` (361 lines)
**Verdict** **`ADOPTED AS FRAMING, WITH THREE AMENDMENTS`** — `16 / 18` predictions held; `P2` and `P8` refuted against me.

---

## 1. What was asked

Four classical theorems were offered as the mathematical foundation of `route_terminus_v1`'s conclusion:
Brouwer's dimensional invariance, Cantor's bijection, Hilbert's space-filling curve, and the Kakeya theorem.
The conclusion: *a lossless physical collapse 3D → 2D is strictly prohibited; a one-to-one map into 2D can be a
file, not a picture; therefore the DCC adopts lossless serialization.*

The submission asks to be read as **`GO`** — authorisation to proceed on that basis. What it did not do is ask the
one question that decides whether four theorems about spaces apply to a deposit. So this ruling asks it per anchor:
**(a) is the mathematics as stated true, (b) is the attribution correct, (c) is the deposit inside the hypothesis.**

Question (c) is the whole ruling, and it had never been asked in thirty-two rounds.

## 2. The measurement

| anchor | true as stated | attributed | applies to the deposit | measured basis |
| --- | --- | --- | --- | --- |
| `A1` Brouwer | **yes**, in two halves that behave differently | 1911 / 1912 (see §4) | **invariance: yes. domain: no** | domain has empty interior in ℝ³ |
| `A2` Cantor | yes, but about cardinality | 1877 ✓ | **yes — vacuously** | a finite pair satisfies it |
| `A3` Hilbert | true of the curve, **false as stated** | 1891, unnamed | no | multiplicity `1` at every finite order |
| `A4` Kakeya | theorem yes, **gloss is a non-sequitur** | 24 Feb 2025 ✓ | no | contains no line segment at all |

`0` occurrences of any of the four names in `docs/` — this foundation is new to the record, not a restatement of
something already ruled on (`P3`).

## 3. The decisive finding: the deposit is 0-dimensional

`A1` is a theorem about spaces. The deposit's domain is a set of `4,279,069,764` plate indices; its codomain is a
set of `4,279,069,764` occupied cells of a `65,536²` grid, minimum separation `pitch = 0.4001 m`. **Both are finite
discrete spaces, hence both of Lebesgue covering dimension 0.** Any bijection between discrete spaces is a
homeomorphism — in a discrete space every subset is open, so continuity of `f` and `f⁻¹` is free.

So `dim = 0` on both sides: **the deposit satisfies the invariant-dimension theorem at `0 = 0`.** It is not an
exception to `A1`; it is an instance of half of it, in the trivial dimension.

That is not a technicality, it is the topological form of `DEPOSIT-BLIND`:

> By the time you have a deposit, the 3-dimensional continuum is gone. Its dimension is 0.
> There is nothing left for a dimension theorem to protect.

And the deposit nevertheless **looks** two-dimensional, which is measurable and is why the anchors felt applicable.
Box-counting on the occupancy: at `ε ≥ pitch`, `N(ε)` tracks `(canvas/ε)²` — the log-log slope is exactly `2`,
because `P(one cell empty) = 0.003701` and `P(2×2 box empty) = 1.88e-10` (`0.20` expected empty `2×2` boxes over the
whole canvas). At `ε < pitch`, `N(ε) = pieces` constant, slope `0`. **A 0-dimensional space drawn on a 2-dimensional
lattice.** The apparent dimension is the embedding's; the decimation from `2¹⁶` to `2⁹` is what converts the first
fact into a picture, and that is the only place "no picture" comes from.

## 4. `A1` — two halves, and only one of them is cited correctly

| half | statement | applies here |
| --- | --- | --- |
| invariant | dimension is a topological invariant | **yes** — gives `0 = 0` |
| domain | `U ⊆ ℝⁿ` open, `f` injective continuous ⇒ `f(U)` open, `f` a homeomorphism; hence for `n > m` **no continuous injective** `f: U → ℝᵐ` | **no** — `U` is a finite set, interior empty, inscribed ball radius `0` |

The submission cites the first half as the slogan and needs the second half as the mechanism. The second half's
hypothesis begins with the word *open*, and the deposit's domain has Lebesgue measure `0` in ℝ³. The slogan survives;
the prohibition does not transfer.

**Attribution.** `Math. Ann. 70, 161–165` (dimension) was *submitted June 1910, published February 1911*;
`Math. Ann. 71, 305–315` (domain) is 1912 — the zbMATH review of the 1912 paper says so explicitly. So the
submission's "1910" is the **submission year**, not a fabricated citation. Not false; under-specified. Recorded as a
provenance note, `P5` passes.

## 5. `A2` — the one anchor that applies, and it is the one that matters

`P2` predicted **0 of 4**. Measured: **1 of 4**, and the ruling is that the refutation is the finding.

`A2`'s hypothesis is not a continuum requirement. It is **cardinality**: two sets of equal cardinality admit a
bijection. A finite pair satisfies that vacuously. So `A2` does not merely apply — it applies *trivially*, which is
exactly the deposit's epistemic position, and it produces the two measured facts that define the deposit:

- **cardinality preserved exactly** — `4,279,069,764 → 4,279,069,764` distinct cells, `15,897,532` free;
- **structure destroyed** — interfaces at `d₃D = 0` land at `d₂D = 12,401.7 / 12,085.3 / 12,989.4 m`, reproduced
  exactly from the archive.

The cost is measurable too, and it is worth naming: the number of injections is `C!/(C−N)!`, so **naming one costs
`log₂ = 1.3089e11` bits ≈ `16.4 GB`** — the same order as the `15.9408 GiB` deposit it describes. The rule
`p = kN + n` costs **0 bits**. A bijection exists because of counting; the deposit is cheap because it is a *rule*,
not a choice. That is `CARD-ONLY`, and it is the sharpest statement anyone has made about why `σ` must be a rule.

`A2`'s 3D framing, though, is decoration: the same bijection exists between any two sets of cardinality `𝔠`, so a
ball and a line are equally good examples. The theorem is about cardinality and cannot be about dimension, since it
holds in every dimension. (`P9`.)

## 6. `A3` — mis-stated, and the deposit uses the part that is not

As written: *"a continuous surjective mapping from a **one**-dimensional interval onto a **two**-dimensional unit
square … multiple **three**-dimensional points will inevitably map to the same two-dimensional coordinate."*

The map described is `1 → 2`. The conclusion drawn is about `3 → 2`. Non-injectivity of a space-filling curve is a
property of the **parameter** — many `t` give one `(x, y)` — not of three-dimensional points. (`P11`.)

And the finite object the deposit actually uses is a **bijection**: `4^k` indices onto `4^k` cells, exhaustive `0`
collisions to order 6, max multiplicity **1**, and `20,000` samples round-tripped exactly at order 16. (`P10`, `P12`.)
Non-injectivity is exclusively a continuum-limit phenomenon; at order `k` it does not exist. So `A3` is not an
obstacle to this record — and the wall it was cited for (nothing collides) is a wall about resolution, not about
continuity.

## 7. `A4` — a non-sequitur that, read literally, refutes `A5`

The theorem is real: Wang–Zahl, 24 February 2025, 127 pages, every Kakeya set in ℝ³ has `dim_H = dim_M = 3`;
`n ≥ 4` remains open. (`P14`.)

But it states a **dimension**, and a dimension is a property of a set, while an information bound is a property of a
channel. The statement relates the two nowhere. So `A4` supports `A5` only through a bridge the submission supplies
and the theorem does not.

Worse, the bridge crosses itself:

- Taken **literally** — *"impossible to compress the full three-dimensional information into a purely
  two-dimensional container"* — the gloss is **true of the deposit**, because the deposit contains no 3D geometry
  (`I(canvas ; r₄) = 0`, six objects → one digest). It corroborates `DEPOSIT-BLIND`.
- But then it **cannot** also support *"the DCC adopts a lossless serialization route"*, because the serialization
  is exactly a 2D container.

`A4` and `A5` pull in opposite directions and cannot be used in one sentence. (`P16`.) Separately: a Kakeya set
contains a unit line segment in every direction, a segment has cardinality `𝔠`, and the deposit has `4,279,069,764`
points — **a finite set contains no line segment at all**, so the deposit holds `0` Kakeya sets, fewer than the three
other anchors apply to.

## 8. `A5` — the conclusion, adopted with three amendments

The conclusion is **right**, and its stated foundation is not what establishes it. Three amendments, each forced by
a measurement:

1. **"strictly prohibited" → "no continuous injective map".** Prohibited: `1` of `3` map classes. A continuous
   surjection exists (Peano 1890 / Hilbert 1891) and a discontinuous bijection exists (Cantor 1877) — both cited in
   the same paragraph. The unqualified prohibition is refuted by its own supporting anchors. (`P17`.)
2. **"lossless" requires a declared referent.** With respect to the **plate inventory**: exact (bijection).
   With respect to the **object**: false (`0` bits on `10` of `12` parameters). The unqualified word is ambiguous
   between a true and a false claim — and the ambiguity is precisely the difference between a file and a physical
   reduction. (`P15`.) Registered as `LOSSLESS-REFERENT`; `route_terminus_v1` `D-2` is amended to `D-2a`.
3. **"no picture" is arithmetic, not topology.** Injective needs `⌈√pieces⌉ = 65,415` per side ⇒ `2¹⁶`; renderable
   is `2⁹`; cell ratio `2¹⁴ = 16,384` exactly; a 4K frame shows `0.19%`. Every number there is a count of sites. The
   four anchors establish *no embedding*; the picture prohibition is `route_terminus_v1` §4, which uses none of them.
   (`P18`.)

The **three-row trilemma** is the correct form of what the four anchors were reaching for, and it is now the
registered object `MAP-TRILEMMA`:

| map class `ℝ³ ⊇ X → ℝ²` | exists? | what survives | authority |
| --- | --- | --- | --- |
| homeomorphism / continuous injective | **no** | dimension preserved | Brouwer 1911 / 1912 |
| continuous surjection | yes | many-to-one, forced | Peano 1890 / Hilbert 1891 |
| bijection, no regularity | yes | distance destroyed | Cantor 1877 |
| **bijection between finite sets** | **yes** (`4,279,069,764`) | **address only, `0 = 0`** | **the deposit** |

The deposit is a fourth row that none of the three authorities governs — and `A2` is what says the fourth row is
non-empty.

## 9. What this ruling changes

Nothing in `route_terminus_v1` is reversed, and no readable cell is created (`PROVENANCE: NEITHER`). Three changes:

- `D-2` gains **`D-2a`**: "lossless" must name its referent; without one the claim is either trivially true or false.
- The **foundation** of the terminus is restated: not four theorems that forbid the deposit, but the trilemma plus
  the resolution gap plus `DEPOSIT-BLIND`. `A2` is the only anchor of the four that does any work, and it works
  because it is the weakest statement in mathematics.
- `A4` is **struck** from the foundation. A theorem about a set's Hausdorff dimension may not be cited as an
  information bound in this record.

## 10. My own defects

`P2` and `P8` are refuted, and both refutations are recorded unedited in `[H]`:

- **`E1`** — the executor's reference list carried a **transposed digit** (`12,899.4` for `12,989.4`), so the first
  run printed `rep = False` against data that matches exactly. The registration was right; the harness was wrong.
  Fifth instance of *"a constant in the harness is wrong while the registered claim is fine"*.
- **`E2`** — my first bijection check drew `200,000` indices **with replacement** and then tested the image for
  collisions. The three "collisions" were the sampler's birthday repeats (expected `4.7`). Deduplicating the inputs:
  `199,997 → 199,997`. Recorded because the original line printed `COLLISION`, and a reader would have concluded `σ`
  was broken.
- **`E3`** — `P2`'s first form regex-matched the anchor **strings** for `continu|open`, scoring `A4` as
  non-continuous because the word "continuum" never appears in "a unit segment in every direction". The string is not
  the hypothesis. **Fourth round with a text test standing in for a mathematical one.**
- **`E4`** — `P8`'s mean band `[1.1e4, 1.4e4] m` was derived from `n = 0` and measured `14,430 / 13,078 / 14,439`.
  The band was too tight; the archived `MR2-D` figure is a single-layer sample of `1.07e9` and understates by
  `5–16%`. The qualitative claim (4 decades of destruction) is untouched.
- **`E5`** — `P18` first printed `65536 // 512 = 128 = 2⁷` (a linear ratio) while its own prose said `2¹⁴` (a cell
  ratio), and printed "4K shows `0.01%`" using `512²` instead of `3840×2160` (`0.19%`).
- **`E6`** — `P10` had no `verdict()` call in the first run, so the tally printed `17` instead of `18`. A missing
  verdict is indistinguishable from a passing one in a tally; the counts are now checked against the number of
  `verdict()` calls.

## 11. What this document does not decide

It does not decide whether "serialization" is the **right** route — only that no dimension theorem forbids it. It
does not touch `GD6` (still the critical path: the canvas is missing a *coordinate*, and a theorem about dimension
does not supply one). It establishes no physics, sets no threshold, and cannot move `G1`. A citation audit that
concludes "the citations are nearly right" is not progress on the model; it is hygiene, and it is recorded as such.

---

*Content generated by AI*
