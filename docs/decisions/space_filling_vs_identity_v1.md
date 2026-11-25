# Space-filling curves vs the identity map — the ordering question is real, the physics is not

**Registered**: 2026-11-22
**Submission**: `runs/FRONT/sf_curve_submission_verbatim.md` (**PROPOSED — governs nothing**)
**Pre-registration**: `runs/FRONT/sf_curve_registration.md` (`P1`–`P15`, fixed before the executor)
**Products**: `src/route/sf_curve_check.py` → `runs/FRONT/sf_curve_results.txt` (13/15, both failures mine)
**Amended**: `docs/decisions/front_sweep_v1.md` §2.2 (gap declared, `σ` **not** chosen)

---

## 0. Verdict

**PARTIALLY ACCEPTED.** The submission finds a real gap that four prior submissions and seven audits
missed, and its proposed algorithm survives measurement better than my own prediction said it would. Its
*argument* does not survive at all, and its stated grid does not exist.

| Proposition | Verdict |
| --- | --- |
| **S1** — `D2` is an identity map + relabelling, no deformation, no stress | **already in force** as `KIN-DYN` (`front_sweep_v1` §2.1). Nothing added |
| **S2** — therefore the algorithm is "lossless rearrangement", not projection | **true, and trivially so** (`P15`): `D2` already is one. As a *criterion* it selects nothing |
| **S3a** — the order of layers onto sites is a question that must be answered | **ACCEPTED — new.** Registered `GD11` |
| **S3b** — the answer is a space-filling curve, dictated by physics | **half** — the curve measures better; the *dictation* is refused. It contradicts a clause in force |
| **S3c** — the grid is Planck cells, thickness `ℓ_P` | **REFUSED** — `n_max(ℓ_P) = 7.52e-26 < 1`; no admissible configuration |
| **S4** — the result is an unreadable map needing software rollback | **inverted** — it is the *most* locally faithful of the three candidates measured |

The routing is: **`σ` is a display parameter with a measurable locality, not a physical consequence.**

## 1. What the submission got right, and it is not small

`front_sweep_v1` §2 step ② says each layer is carried "to **its** lattice site". The possessive asserts a
map `σ : n_z → (u, v)` from layer index to site coordinates. **No document defines it.** `P1` searched 38
markdown files under `docs/` for a rule and found none (`18` raw symbol hits, `0` of them rule-shaped — all
were stress `σ` or column density `Σ`; the raw count is a form-failure of my encoding, see §6).

§5 constrains the *order* only by transport speed, and accepts two different families ("both are
acceptable"). So the mechanism document specifies every layer's *destination region* and never specifies
its *destination*. Any frame that draws a site's **content** — as opposed to a symbol for occupancy —
has already answered the question silently.

That is now `GD11`. It was not visible before because the only frame of the deposit (`mid_sweep_fl1.png`)
draws occupancy, not content: the renderer computes `1.4527` plates/cell and saturates, and never assigns
a layer to a site.

Two further credits:

- **The critique of projection is correct and pointless.** `P3` finds **0** occurrences of `orthographic`,
  `perspective projection`, `Hilbert`, `space-filling`, `spiral`, `serpentine` or `raster` anywhere in
  `docs/`. The record never used projection. And `D2` is not one anyway: `z` survives as the site *index*,
  so "orthographic projection loses depth information" is not a defect `D2` has. The objection answers a
  method nobody proposed.
- **The algorithm is better than the record's implicit order**, measured in §4 below.

## 2. What is refused, and the first refusal needs no argument from me

The submission says the choice is "dictated by the physical constraints of information conservation and
zero deformation". `front_sweep_v1` §2.1, in force since yesterday, says:

> "`Π` is ours, and nothing in the mechanism selects it over any other relabelling with the same piece
> census."

`P2` confirms that sentence is present, once. The submission's central inference is the **negation of a
clause already governing the mechanism** — and that clause was written for a different purpose.

### 2.1 The two cited constraints are permutation-invariant, so they rank nothing

Information conservation ⇔ the piece→site map is injective. Zero deformation ⇔ each piece moves rigidly,
i.e. the map permutes *pieces*, not points. Both hold for **every** permutation. The admissible set is the
full symmetric group:

```
pieces N              = 1.18e10            (census, FROZEN)
log10(N!)             = 1.1372e11
admissible bijections = 10^1.14e11
```

`P4` and `P5` confirm it: three randomly sampled bijections satisfy both constraints, as all of them do. A
principle that admits `10^1.14e11` arrangements and orders none of them cannot "dictate" one. This is the
**fifth** instance of the selection-vacuity class (`S10`: an identity presented as a selection).

The premise `S1` is right and needs no support; the inference `S2 → S3` is a non-sequitur, because the
constraints are satisfied *before* any curve is applied.

### 2.2 The grid does not exist

`S3` fixes the unit at "every Planck-scale grid cell (or voxel)" with "a thickness of one Planck length",
and `S4` repeats that "the size of all physical units remains constant (i.e., the Planck scale)". Annex B
§B.8.2 was registered one round ago for exactly this:

```
n_max(ℓ_P) = ℓ_P/δ = 1.6159e-35 / 2.150e-10 = 7.516e-26  <  1
```

No positive layer count satisfies it. The Planck thickness is not a fine grid the model declines to use;
it is a thickness at which the model **has no configuration**. Compared with the registered deposit:

| | registered | submission's unit | factor |
| --- | --- | --- | --- |
| site pitch | `0.4001 m` | `ℓ_P` | `2.48e34` |
| thickness | `0.215 nm` | `ℓ_P` | `1.33e25` |

This is the **second** text to reintroduce the Planck grid after it was excluded, and the first to
reintroduce it while citing the same paragraph's subject matter.

### 2.3 The voxel reading, priced

`S3` is written at voxel resolution. Priced at the deposit's own finest lattice, `a = δ = 0.215 nm`:

| quantity | value |
| --- | --- |
| voxels per plate | `5.127e17` |
| pieces if each voxel is a piece | `6.05e27` |
| array side required at `0.4001 m` | `7.778e13` sites |
| canvas required | `3.112e13 m` = **`208 AU`** |
| versus the frozen canvas (`36.06 km`) | `8.63e8 ×` |

Reading `S3` literally multiplies the **frozen** piece count by `5.1e17` and the array side by `8.63e8`.
A submission cannot change a frozen census as a detail of its algorithm; that is the same category as the
`H_eff = n_z·δ` form refused last round.

More importantly the voxel reading **destroys the premise it invokes**. A rigid-body translation preserves
shape; scattering a plate's pixels onto Hilbert indices does not. So under the voxel reading the plate
stops being a body, and `front_sweep_v1` §2 ②'s "intralayer strain always 0" no longer follows from
anything — the zero becomes vacuous rather than structural, which is precisely the demotion `KIN-DYN`
was written to prevent. The submission slides between two readings:

- **voxel-level** ("every Planck-scale grid cell"): breaks rigidity, `5.1e17 ×` the census…
- **piece-level** ("rearranging them"): keeps rigidity, and then the cited constraints select nothing (§2.1).

Neither reading carries the argument.

### 2.4 Two smaller refusals

**"Size of all physical units remains constant."** False of the registered census, by a factor of `8.571`
(plate areas `6.3e-3` to `5.4e-2 m²`). It is true only of the hypothetical voxel grid. *(My prediction
said `8.19`; see §6, my error.)*

**"Concentric rings or spiral bands … cannot be recognized by the naked eye."** The rings are an artifact
of `σ`, not a consequence of anything physical: since `σ` is free, they are achievable by choosing it and
refutable by nothing. That makes them unfalsifiable as stated, which is the same defect the matrix route
died of. And "spherically symmetric expansion" does not fit the object: the body is `1.74 m` tall with a
maximum radius of `0.131 m`, an aspect of `13:1`. A radial traversal of it is cylindrical, not spherical.

## 3. The consequence the submission did not draw: `S4` contradicts `S3`

`S4` says the result is a "data map" that "cannot be directly recognized by the naked eye" and must be
"rolled back … using specific image processing software". But a Hamiltonian-path `σ` — which is what a
Hilbert curve is — puts **consecutive layers on adjacent sites**. So any square crop of the array is a
*locally contiguous* block of material. Measured over all 4-adjacent site pairs:

| `σ` | median `|Δn|` | p90 | contiguity |
| --- | --- | --- | --- |
| raster | `128.5` | `256` | `0.9961` |
| **Hilbert** | **`1.0`** | **`45`** | **`1.0000`** |
| spiral | `1.0` | `907` | `0.9980` |

A Hilbert-ordered array is *more* locally faithful than the raster order it would replace, not less. So the
proposed algorithm produces the **opposite** of the appearance the submission predicts. `S4` is not a
discovery about the algorithm; it is a guess about unfamiliar pictures, and the measurement reverses it.

The honest statement is weaker and still useful: `σ` decides **how legible a crop is**, and a curve buys
isotropy at the price of one large jump (`21845` layers, where the curve passes near itself). That is a
display property.

## 4. What the measurement says, stated so it can be used

`P11`–`P13` passed and `P14` failed, and `P14`'s failure is the informative one: I predicted contiguity
would tie at `1.000` for all three candidates. It does not. Raster loses `0.39%` at row-end wraps, the
spiral `0.20%` at ring seams, and **Hilbert is the only true Hamiltonian path of the three**.

| statistic | raster | Hilbert | spiral |
| --- | --- | --- | --- |
| contiguity | `0.9961` | **`1.0000`** | `0.9980` |
| anisotropy `ρ` | `256.0` (= `S`) | **`1.0`** | `1.5` |
| median `|Δn|`, all adjacent pairs | `128.5` | **`1.0`** | `1.0` |
| p90 `|Δn|` | `256` | **`45`** | `907` |
| max `|Δn|` | **`256`** | `21845` | `1015` |

At the registered side `90126`, raster's anisotropy is `90126 : 1` — one step along a row moves
`0.215 nm` of body height, one step down a column moves `19.4 µm`. Both are far below any anatomical
feature, so nothing is *distorted* by it; but the two axes are not equivalent, and a crop is a
`215 nm × 1.94 mm` sliver rather than a block.

So over the four statistics measured, **Hilbert dominates raster** except on the single largest jump and on
raster's exact one-layer row step. The submission's algorithmic instinct is correct. Its derivation is not.

## 5. What is registered, and what is deliberately left open

**`GD11`** (`σ` undefined) is registered open. It is **not** closed here, and no `σ` is chosen, for two
reasons:

1. Choosing `σ` is a **convention**, like `DC4`'s declared weighting in the `FL` coordinate. It may be
   declared, never derived — §2.1 says so in the mechanism document's own words.
2. `GD10` (plates per cell) is upstream of it. If the side is `108628`, the site set changes and so does
   every `σ`. Choosing an ordering before the array has a definite size would be choosing against a
   moving target.

What §2.2 of `front_sweep_v1` does is **declare the gap**: it states that `σ` is not defined by the
mechanism, that no frame drawing site content may be drawn until it is declared and locked, and that
§5's transport constraint does not determine it. It chooses nothing.

A side effect worth recording: `GD10` reading (B) — several plates per cell — is **geometrically
admissible**. `1.4527 × 0.0237 m² = 3.44e-2 m²` against `0.1601 m²` of cell, i.e. `21.5%` coverage, `4.6×`
clear. So `GD10` is a labelling question, not a capacity question, and reading (B) does not require
overlapping plates.

## 6. My own defects, disclosed

Two of fifteen predictions failed and **both failures were mine, both cutting against me**:

- **`P1` was a form-failure.** Predicted "0 hits" for a raw `\bsigma\b|\bσ\b` count; it returned `18`,
  every one of them stress `σ` or column density `Σ`. The claim survives on a rule-shaped query, but the
  prediction passed only because I never checked what the pattern matched. Same class as `P8`/`P11` in the
  `T4` round.
- **`P10` predicted `8.19`, measured `8.571`.** I used the abdomen range's upper end (`0.0516 m²`) as the
  maximum plate area; the thorax row (`0.0540 m²`) is larger. The tested claim is unaffected.
- **`P14` was simply wrong**, and it was wrong in the direction that flatters the submission rather than
  me. The falsifier I declared for this case fired and I accepted it.
- **The closing narrative was a static string and contradicted the run twice** — first "tie on contiguity"
  (false per `P14`), then "median rises to 123.5–339.7" (that was the *mean*; the median is `1.0`). Both
  are now f-string interpolations. Fourth instance of this class; it is why every summary line in this
  product is derived rather than written.
- **`grid_spiral` crashed** on even `S` (negative indices). Fixed with a bounds guard, disclosed because a
  crash is the only reason the spiral numbers can be trusted.

Effect on the disposition: none. Every refusal rests on a check that passed on its first encoding — `P2`,
`P4`, `P5`, `P6`–`P8`, `P9`.

## 7. Evidence

`runs/FRONT/sf_curve_submission_verbatim.md` (submission, verbatim) ·
`runs/FRONT/sf_curve_registration.md` (`P1`–`P15`) · `src/route/sf_curve_check.py` ·
`runs/FRONT/sf_curve_results.txt` (`13/15`, erratum `E1`–`E5` appended, run not edited).

*Content generated by AI*
