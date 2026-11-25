# RQ-07 — pre-registration: localisation length and three-resolution grid scaling

**Written before the instrument `src/r4_frontier/r4_localisation.py` exists.** Round 61.
Queue: `docs/program/round_queue_v1.json` item `RQ-07`; product:
`runs/R4/r4_localisation_results.txt`. Governing open item:
`docs/decisions/r4_finite_region_geometry_v1.md` §7.4 ("N ≥ 32 spectrum not run; smooth bulk mode
vs under-resolved bulk mode not distinguished").

## 1 One question

Does the already-localised **BULK** R4 instability possess a finite, resolution-independent
localisation length, or is it a UV/short-wavelength sector with no finite continuum length?

This does **not** re-open BULK vs EDGE. `runs/R4/r4_instability_localization_stage2_results.txt`
fixed BULK at 0.1% precision via unconfounded seeded amplification, and
`docs/decisions/r4_finite_region_geometry_v1.md` §7 adopted it. The stale gate-table phrase
"remains unlocalised in the bulk" is corrected by erratum, not by changing the gate table.

## 2 What the product is, and what it is not

It is a numerical diagnosis of the imported production semi-discrete operator
(`axisym_2p1_evolution`, zero shift, 1+log, 2nd-order FD, KO_EPS = 0 for the Jacobian as in the
registered stage-1 spectrum). It measures a localisation length, tests three resolutions, and states
which pre-registered classifier fires.

It is **not** a B-test repair: B1/B3/B4/B6 stay FAIL. It does not move G4, G5′, G6, any S-criterion,
any ratified decision, or any approval mark. It makes no physical-scale statement: all lengths are
in κ = 1 code units under the roadmap §8.12 prohibition. Product tag is `PROVENANCE: NEITHER`
(diagnostic/arithmetic product; it establishes no chain evidence).

## 3 Definitions fixed now

Let `v` be the leading right eigenvector restricted to the interior block, with field index `f`
and spatial indices `(i,j)` in ρ and z. Define

- `p_ij = Σ_f |v_fij|² / Σ_(f,i,j) |v_fij|²`, so `Σ_ij p_ij = 1`;
- radial marginal `q_i = Σ_j p_ij`, so `Σ_i q_i = 1`;
- **primary localisation length** `ξ_cells = 1 / Σ_i q_i²`, `ξ = h · ξ_cells` (code units);
- secondary 2D IPR length `ℓ_cells = 1 / sqrt(Σ_ij p_ij²)`, `ℓ = h · ℓ_cells`;
- peak-relative radial RMS width `σ_r = h sqrt(Σ_i q_i (i − i_peak)²)`, reported but not used in
  the classifier (a boundary-peaked mode is asymmetric);
- per-direction alternation `alt_ρ`, `alt_z` and 10%-edge masses from the repaired stage-2 metric;
- the old 2D checkerboard index is printed **only** as the negative control of defect A1.

Domain radial span `L = R_DOM − RHO_IN = 20` code units. Grids N = 16, 20, 32 give
h = 1.25, 1.00, 0.625; the smallest physically resolvable length at each grid is h.

## 4 Numerical floors quoted before the run

These are prior measured floors, not values from this run:

| Floor | Source | Value |
|---|---|---|
| Jacobian vs directional derivative | `r4_instability_localization_results.txt` C3 | relative `1.0e−9` |
| FD-step independence of leading Re λ | same product, C5 | relative `3.6e−10` |
| prior two-resolution scaling | `r4_finite_region_geometry_v1.md` §7.1 | `Re λ ∝ h^(−0.97)` from N=16/20 only |
| smallest resolvable length | grid geometry `h = (R_DOM−RHO_IN)/N` | `h = 1.25 / 1.00 / 0.625` |
| old-checker collapse for one-direction alternation | registration addendum A1 | `O(1/N)` (≤ 0.0625 at N ≥ 16) |

The classifier bands below are wider than all numerical floors by ≥ 8 orders of magnitude; the
finite-size/sparsity band, not roundoff, is the limiting uncertainty. Three points fix a power law
but do not license a precision exponent.

## 5 Predictions and kill conditions (numbers, fixed before the run)

| # | Prediction | Bar / kill condition |
|---|---|---|
| `P1` | Matrix-free Jacobian vs dense finite-difference Jacobian at N=12 agrees | relative error `< 1e−6` (prior floor `1e−9`); kill if ≥ |
| `P2` | Recomputed leading Re λ at N=16 and N=20 reproduces archived `+0.51220`, `+0.63602` | relative deviation `< 1%` each (prior FD floor `3.6e−10`); kill if outside |
| `P3` | Leading Re λ is positive at all three grids; at N=32 (h=0.625) the 1/h-consistent value is `1.00` (corrected before emission from `0.84`, which used h=0.75) | band `[0.63, 1.27]` **retained unchanged** from the original registration; kill if nonpositive at any grid or outside band at N=32 |
| `P4` | Three-point log–log fit `Re λ ∝ h^(−p)` gives `p ≈ 0.97` | UV band `p ∈ [0.75, 1.25]`; kill if outside. Reported as scaling consistency, not a measured continuum exponent |
| `P5` | Synthetic mass smooth in ρ with a 3:1 z alternation (`w_j ∝ 1 + 0.5·(−1)^j`) gives repaired `alt_z = 0.5` while the old checker index is `≈ 0` for even N | `alt_z / checker ≥ 5` at every N (analytic floor ≥ 5e11 with the 1e−12 checker floor); this negative control **must fail the old metric** by that factor |
| `P6` | `Σq_i = 1`, field-mass sum `= 1`, and `ξ_cells ≥ 1` | identities to `1e−12`; counted as IDENT, never as evidence |
| `P7` | No verdict, gate, threshold, ratified sentence or product outside `runs/R4/` and the named errata moves | structural; any move is a defect |

## 6 Finite-width vs UV classifier (fixed before the run)

**Finite-width constructive slot (F).** All three must hold:
`F1` `p` outside the UV band (growth saturates), `F2` `ξ(N=16,20,32)` agrees within a max/min
factor `≤ 1.5`, and `F3` `ξ ≥ 2h` at every grid and `ξ/L ≤ 0.5` at N=32 (resolved, interior, not
domain-filling). Then report a finite `ξ` with its resolution spread.

**UV non-localisability slot (U).** Both must hold:
`U1` `p ∈ [0.75, 1.25]` and `Re λ > 0` at all three grids (growth diverges as h→0), and
`U2` at least one of: `ξ(16)/ξ(32) ≥ 1.5` (physical width shrinks), `ℓ(32) < 2·0.625`
(sub-grid 2D width), or `ξ(32)/L ≥ 0.5` (domain-filling rather than interior-localised).
Then the theorem-slot statement is: a finite-width smooth localized continuum eigenmode would have a
resolution-independent growth rate and a width that converges above the grid floor; `U1` contradicts
the former and `U2` contradicts the latter, so **no finite continuum localisation length exists for
this sector of the operator under test**. This is a conditional non-localisability result for the
ADM operator, not a claim about all formulations, and not a statement that a cure exists.

**If neither F nor U fires**, the terminal class is `BLOCKED-ON-INPUT`, naming the missing input as
a fourth spectral resolution N=64 (the unresolved gap is finite-size, not a physics choice).
No bar is refitted after the run. A falsified prediction is reported with its measured value.

## 6b Pre-emission correction (before any product was written)

A dry run, retained in the round record but not emitted as a product, exposed two defects in the
*registration's derived arithmetic and synthetic predicate*, not in the measured physics:

1. **Grid spacing.** `Grid.h = (R_DOM−RHO_IN)/N = 20/32 = 0.625`, not `0.75`. The hand estimate
   for `Re λ(N=32)` was therefore `0.84` under an incorrect h; at h=0.625 the 1/h-consistent value
   is `1.00`. **The registered band `[0.63, 1.27]` is retained unchanged** — it was fixed before the
   run, and a post-run re-centring would be a goalpost move. The sub-grid clause of `U2` is corrected
   from `2·0.75 = 1.5` to `2·0.625 = 1.25` because that is a definitional consequence of the grid,
   not a fitted threshold.
2. **Negative control.** The first synthetic pattern gave uniform z mass, so neither the old nor
   the repaired alternation metric was exercised (`alt_z = 0`). It is replaced by a 3:1 z
   alternation with analytic `alt_z = 0.5` and old-checker `≈ 0` for even N. The registered bar
   `alt_z/checker ≥ 5` is unchanged. This is the A1 defect control, not physics evidence.

No measured eigenvalue, no physics classifier bar, and no terminal rule changes. Both corrections
are disclosed in the emitted product.

## 7 Prohibitions

- No B-test verdict changes; locating or classifying the mode is not curing it.
- No G4/G5′/G6 gate mark is written; this product supplies evidence, not authority.
- Product stdout is never edited. Corrections are append-only errata under §9.1; failed sub-runs
  are retained.
- No physical-scale extrapolation; κ = 1 code units only.
- Matrix v2 (`docs/specs/matrix_v2_spec_v1.md`) remains a **product**, not a route: it is not cited
  as authority and no approval block is added to it.

## 8 Provenance

`PROVENANCE: NEITHER` — diagnostic/arithmetic product. Inputs are the imported production operator
and the archived stage-1/stage-2 products; no boundary data and no chain certification is claimed.
