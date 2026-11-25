# Display conventions v1 — the declaration block every frame must carry

**Created**: 2026-11-22
**Status**: **ACTIVE.** Binding on every rendered frame, figure, plate and animation produced from this repository
from this date.
**Authority**: `docs/decisions/phased_relaxation_route_v2.md` Phase 0 ("establish the sole authorised source of
colour"); `runs/R5/r5l2_sigma_s_results.txt` (frequency-flatness); `docs/specs/meff_boundary_v0_2.md` ME5.
**Enforcement**: validator specified in §5; applied to each frame's `.display.txt` sidecar.

---

## 0. Why this exists (the number that makes it necessary)

In the eye's band the sheet's response is **frequency-flat**:

```
R(1.0 eV) = R(2.0 eV) = R(3.0 eV) = 0.975855        τ = 1e-19 s,  ωτ ≤ 0.304
```

(source: `runs/R5/r5l2_sigma_s_results.txt`, §8 of the v1 ledger, recorded there as an *unregistered observation*.)

Three consequences, in order of strength:

1. **Zero chromatic contrast inside the eye's band.** The response cannot distinguish 700 nm from 400 nm, so no
   physical mechanism in this model assigns different colours to different wavelengths within the visible.
2. Therefore **any colour in an FL1/FL2 frame of the visible band is a declared display convention** — a choice of
   colormap, not a measurement. This is not a caveat to be mentioned once; it is a property of every pixel.
3. Therefore a frame that shows colour without declaring it is making a claim the optics cannot support. That is the
   precise error this document exists to prevent, and it is why Phase 0's deliverable is a declaration block rather
   than an image.

**One thing the number does not forbid.** Frequency-flatness says the *response* is achromatic; it says nothing
against mapping a *physical scalar* (temperature, converted volume fraction, perpendicular energy fraction) to a
colour scale. Such a frame is legitimate **provided the mapping is declared and the scalar is named**. The
prohibition is on colours that imply a spectral measurement that was not made — not on false-colour per se
(`EN2`, an authorised enhancement).

---

## 1. The block

Every frame carries a block of exactly these nine fields, in this order. A sidecar file `<frame>.display.txt`
holds it verbatim; the figure caption repeats `BAND`, `COLOUR` and `FIDELITY` in human-readable form.

```
DISPLAY-DECLARATION v1
FRAME:            <file name>
PROVENANCE:       CHAIN-EVIDENCE | BOUNDARY-INPUT | NEITHER      (per provenance_tags_v1 §P1)
STAGE:            S0 | S1 | S2 | S3 | S4            (v1 ledger §7)
FIDELITY:         FL1 | FL2 | FL3                    (never bare L)
BAND:             <physical band shown, eV or nm>  |  NONE (geometry only)
COLOUR:           DECLARED-CONVENTION | PHYSICAL | NONE
COLOUR-BASIS:     <one sentence; required when COLOUR = DECLARED-CONVENTION>
SCALAR:           <the physical quantity mapped to colour, with units>  |  NONE
TIME:             t_span = <s> ; compression = <×> ; t_rip = <s> ; ratio = <t_span/t_rip>
GEOMETRY:         PRESCRIBED (D2) | SOLVED                (D2 status, v1 ledger §7)
ENHANCEMENT:      EN1 | EN2 | EN3 | EN4 | none           (comma list, each with its basis in §3)
ME5-COROLLARY:    PRESENT | NOT-APPLICABLE               (mandatory PRESENT at FL3)
```

## 2. Rules

**DC1 — no block, no citation.** A frame without a valid block may be viewed but may not be cited, quoted, or
placed in any report. It is not a product.

**DC2 — colour in the eye's band is DECLARED-CONVENTION.** `COLOUR: PHYSICAL` is unavailable for chromatic
content in the visible band until a compliant `σ_s(ω)` exists (**G6** passed with a solved `τ`, not a scanned one).
Asserting it earlier is a false claim, not a strong one. Citing basis: §0, items 1–2.

**DC3 — `COLOUR: PHYSICAL` is not forbidden everywhere.** It is available for (a) a band where the response is
*not* flat and a compliant `σ_s` exists, and (b) any non-chromatic quantity (reflectance, optical depth) rendered
in greyscale. What is forbidden is a *spectral* claim without a spectral calculation.

**DC4 — the block is metadata, never evidence.** Like `BUDGET-1` for `ΔH`: a declaration may not appear in a
PASS/FAIL row, a gate row, a threshold, or an acceptance criterion. It records what a frame *is*, not what is true.

**DC5 — time must be declared against `t_rip`.** `TIME` reports `t_span/t_rip`, not merely a compression factor. If
the ratio exceeds 1, the frame depicts a configuration that cannot persist for the interval it claims to show, and
the frame must say so in the caption — this is ME5's corollary made per-frame rather than per-document.

**DC6 — fidelity labels are `FL1`–`FL3`.** Bare `L1`/`L2`/`L3` are prohibited in new text: `L` carries three live
meanings (optics layers, presentation fidelity, R2-D redshift layers) and the R2-D labels are embedded in file paths
(`pz_l1.py`, `r2d_l2_results.txt`), so the collision cannot be fixed by renaming (registry §3 item 3).

**DC7 — a declared convention may not be *repaired* into physics.** If a later result licenses a physical colour,
the frame is re-issued with a new `COLOUR-BASIS`; the old block is never edited (§9.1) and the change is recorded
as an errata line in the issuing report.

**DC8 — geometry and physics are declared separately.** `GEOMETRY: PRESCRIBED (D2)` is not a defect; it is the
honest statement that S0–S1 use a hand-specified contraction background. `SOLVED` may not appear before S2's
acceptance (flat space stationary at `~1e-12` over `t = 20` with growth *decreasing* under refinement).

**DC9 — `FIDELITY` means faithfulness, and the ladder ascends (`GD7`).** `FL` is closeness to the **unaided retinal
image**, so `FL3` is the maximum and `FL1` the floor — a frame may never be labelled `FL3` on the ground that it is
*more informative*. The two are anti-correlated by construction: the most faithful frame carries no structure of the
object. Consequences binding on captions:

1. A frame labelled `FL2` or `FL3` **must** state, in the caption, that fidelity was bought by discarding
   information. A caption that presents `FL3` as an improvement in what can be *seen of the object* is
   non-compliant — it inverts DC9.
2. An **`FL3` frame must declare its member**, because `FL3` is a family: at `C1` held a faithful reflected-light
   frame shows the object's **absence**; at ¬`C1` it shows the **intact slab**. Without the declaration the frame will
   be read as a depiction of a surviving sheet — the one reading the corollary forbids (`meff_boundary_v0_2`, `GD8`).
3. The member declaration goes in the **caption**, not in the block: adding a block field would invalidate every
   issued block, and `DC7` forbids repairing a block in place.
4. `FL3` may not be claimed at all until a citable frame exists; at present none does (`G1` in
   `route_goal_conformance_v1.md`).

## 3. Enhancement register (basis required)

| id | Technique | Physical basis it must cite | Permitted at |
| --- | --- | --- | --- |
| **EN1** | Band migration | the frame states the band it *would* be seen in and why that band is inaccessible | FL1+ |
| **EN2** | False colour | `SCALAR` names the quantity and its colour map is monotone; no implication of spectral measurement | FL1+ |
| **EN3** | Contrast stretch | the stretch factor and the clip points; no information added beyond monotone remapping | FL1+ |
| **EN4** | Shadowgraph / transmission | the `1.41×` transmission margin (ME5 corollary); reflection channel excluded | FL1+ |
| **EN5** | Time compression | `TIME.ratio` declared; if `> 1` the captions says the configuration is transient (DC5) | FL2+ |

Adding a technique requires a row here first. A frame using an unregistered technique is not a product (DC1).

## 4. What is *not* a display convention

Three things are often confused with this block and are not covered by it:

1. **The claim that a surviving sheet can be photographed in reflected light.** This is a *physical* proposition,
   refuted exactly by ME5 (`2L/c = √2·t_rip > t_rip`). The block's `ME5-COROLLARY: PRESENT` field records that the
   corollary was printed; it does not make the claim true.
2. **The choice of `ε` scalarisation.** `ε := 1 − φ_conv` is a definition (v0.2 §1), registered, not a display
   choice. A frame's colour scale may use it; the frame may not redefine it.
3. **The choice of `Δz_res`.** Under audit V1's Option A this is an *instrument* parameter frozen at Phase 0.
   A display block may not carry it, and FL enhancement may not move it.

## 5. Validator

`src/common/display_lint.py` checks every `*.display.txt` under `runs/`: required fields present, enumerated values
legal, `COLOUR-BASIS` non-empty when `COLOUR = DECLARED-CONVENTION`, `FIDELITY` in `{FL1,FL2,FL3}`, and
`ME5-COROLLARY` present when `FIDELITY = FL3`. It is a report (exit 0), with the same relationship to enforcement
as the other two linters: a violation makes the frame non-citable, not the run invalid.

Negative-tested on planted declarations before first use, in the manner of `provenance_lint`
(the provenance control stayed silent until it was tested; that lesson is not repeated here).

**Known blind spot (2026-11-22, `route_goal_conformance_v1.md` F1).** The validator enumerates `*.display.txt`, so
it checks the blocks that *exist* and cannot see images that have *none*. `DC1` is therefore enforced only from the
side where it is already satisfied. Census at the time of the finding: **27 images, 1 declared, 26 non-citable
(3.7 % coverage)** — including the two figures that already carry the `FL1` and `FL3` endpoint views
(`runs/ANALYSIS/unfold_appearance_v1.png`, `runs/ANALYSIS/painting_render_v1.png`). The fix is to enumerate image
files and report the missing side; until it is applied, no citation of those 26 frames is legal, whatever the text
says about the physics.

---

*Content generated by AI*
