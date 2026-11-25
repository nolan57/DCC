# Matrix reading rules v1

**Status**: `MR1` in force, 2026-11-22, on governor ruling T4 (*written into matrix reading rule 1: reading
precondition plus an explicit "no readable cell"; no new lock*). `MR2`+ are open and numbered for later.

These rules govern how a cell of the constraint × tier matrix may be **read**. They do not govern how a cell is
**computed** — that is `docs/specs/intrinsic_structure_tiers_v1.md` plus Annex A, and the thresholds are in
`runs/MATRIX/threshold_lock.json` and nowhere else.

**Labels.** The rules are `MR1`, `MR2`, `MR3`, not `R1`–`R3`. `R1`–`R4` are the symbol-registry ownership rules, and
registry rule `R3` requires every enumerated label outside the load-bearing set to carry a ≥2-letter prefix. The
first draft of this document used `R1`; that was a violation of `R3` caught before the registry was amended.

---

## MR1 — A cell is not a picture, and the matrix currently contains no readable cell

> **MR1.0** No cell of the matrix may be read as "the scene is readable". The four admitted tiers establish that
> **structure is present in the scene** (`Q0`, `Q1`, `Q2`) and, separately, **legibility through a declared
> observer** (`Q3`). "Readable" — a viewer can tell what they are looking at — is not measured by any of them.

**MR1.1 Why this is a precondition and not a caveat.** It was measured. The layout probe took a canonical tiled
arrangement of a disc and shuffled the same tiles into the same positions: characteristic scale `ξ` fell
`27.55 → 4.53` and `Q2` fell `0.94 → 0.78`, and **both still pass** their locked thresholds (`4.0` and the
`L2` one). The profile therefore survives the destruction of the one property that makes the picture a picture.
A statistic that cannot fall below its threshold when the image is scrambled is not evidence of an image.

**MR1.2 A cell is a profile, never a maximum.** A cell records the 4-tuple `(Q0, Q1, Q2, Q3)` with each tier's
verdict. Collapsing it to "max tier reached" is inadmissible: `M6` of the matrix audit showed no total order
`L0 < L1 < L2 < L3` is compatible with the measured signs, so a maximum is not merely coarse, it is undefined.

**MR1.3 Zero readable cells, stated explicitly.** As of this date the matrix contains **no cell that may be read
as readable**, for two independent reasons:

- **Reflection channel**: `Q3` is `0` of `9` calibration scenes, and the reason is `q = 0` **exactly**, not low
  contrast (`T5`). A declared channel factor of zero makes the legibility tier identically zero. This is the
  intrinsic-side reproduction of audit `M5`: what emptied that column was photons, not the metric.
- **Transmission channel**: `Q3` has never been evaluated on a scene that carries the 2D-ified content. Its
  calibration values are on abstract fields, so no cell may inherit them.

Consequently: **any document that reports a readable cell is in error**, and that includes a document of mine.

**MR1.4 Annex A applies before MR1.2.** A cell is read through the applicability domains first: a `Q0` **pass** at
histogram modal mass `≥ 0.87` is not evidence of organization, and a `Q2` **fail** is never evidence of absence
(`docs/specs/intrinsic_structure_tiers_v1_annex_A.md`). A cell assembled from the two forbidden readings — a
`Q0` pass on an empty field plus a `Q2` fail on a structured one — would report the exact opposite of the truth,
which is why the two prohibitions are prerequisites and not footnotes.

**MR1.5 Any cell claiming a tier must carry its declarations, hash-pinned before the frame.** Metric, threshold,
ensemble and layout convention, locked by digest before the scene is evaluated (matrix audit `§6` items 2, 3, 5;
this is the same discipline as `TIER-LOCK`). A cell without pinned declarations is `NO-VERDICT`, not a low score.

**MR1.6 `MR1.0` is necessitated, not merely observed.** Added 2026-11-22 (`route_terminus_v1.md` §2–§4). The two
reasons in `MR1.3` are empirical — `Q3` is zero, and `Q3` was never evaluated on 2D-ified content. The third is
structural and no measurement can remove it: the deposit is a function of `(M, N)` alone (`DEPOSIT-BLIND`), so **no
statistic on it can be a statement about the object**; and the deposit is one-to-one while an image is
many-to-one, with the gap `2¹⁴` exactly (`DEPOSIT-DICHOTOMY`). A cell of the matrix is therefore a statement about
a **declaration**. This does not retract any admitted cell — a cell's verdict on `Q0`–`Q2` remains what it was —
but it fixes the ceiling: zero readable cells, permanently, for this mechanism.

## MR2 — **closed as a gate** 2026-11-22

Reserved. The obvious candidate: an **arrangement-sensitive** statistic (one that falls below threshold when the
tiles are shuffled) with its threshold declared and locked before measurement. If such a tier is admitted, MR1.0
can be **narrowed** from "no cell may be read as readable" to "only cells whose arrangement-sensitive tier
passes may be read as readable". Until it exists, MR1.0 stands unqualified.

> **Closed 2026-11-22 — `mr2_arap_designation_v1.md`.** The candidate above **cannot be built**, and the reason is
> not statistical. The deposit severs every interface by construction, so *every finite statistic of arrangement is
> a statistic of `σ`, and every statistic of the object is `+∞`* (`MR2-CLOSE`): the 3D and 2D pair-distance
> supports are disjoint (`0.292062 m` vs `0.4001 m`), and the one statistic that *does* separate the deposit from a
> random permutation (`422×` its sampling floor) was decomposed and found to be `99.2%` the four-run partition —
> i.e. `σ`, which `DEMO-1` §4.3 already measures at `1.0000` vs `0.9961` without a threshold.
>
> **`MR1.0` therefore stands unqualified, and may not be narrowed.** The residue is `MR2-D`: a threshold-free
> diagnostic (axial pairs at exactly one `pitch`, interface pairs at `1.2e4 m`), which reports the declared loss and
> admits nothing. `MR2` may not be cited as an admission criterion, and no cell depends on it.

## MR3 — *open*

Reserved for the reading of a cell whose `Q3` is taken in the transmission channel on a scene carrying the
2D-ified content, which is the only configuration in which a readable cell is even conceivable.

---

## Evidence

`runs/MATRIX/structure_tiers_results.txt` (`T4` layout probe, `T5` reflection column), `docs/decisions/tier_admission_v1.md`
(T4, T5), `runs/MATRIX/matrix_audit_results.txt` (`M6`, `M5`), Annex A.

*Content generated by AI*
