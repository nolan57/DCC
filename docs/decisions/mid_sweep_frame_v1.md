# The mid-sweep frame v1 — the artifact the goal names

Date: 2026-11-22
Product: `runs/FRONT/mid_sweep_fl1.png` + `.display.txt` (block `OK` under `display_lint`)
Pre-registration: `runs/FRONT/mid_sweep_frame_registration.md` (P-ledger, addenda A1 and A2, all fixed before code)
Executor: `src/route/front_sweep_frame.py` → `runs/FRONT/mid_sweep_frame_results.txt`
Authority: governor **GO** on item 1 of "what is next"

---

## 1. What was missing, and why it was missing

`staged_relaxation_visual_route_v1` §1 asks for *"a 3D macroscopic object being swept by a 2D-ification front"*.
A census of all 27 images in the repository found **zero** that show the front at an intermediate position: they are
the unfolded end state, or they are plots. `G1` of `route_goal_conformance_v1` recorded this as a **missing product
class**, not a missing measurement — which is why it needed no relaxation and no new ruling.

## 2. What the registered mechanism forced, and how it contradicts the obvious picture

The natural image — an object flattening into a glowing sheet where it stands — is **false**, and it is the picture
everyone draws. `front_sweep_v1` §2 says the front peels one atomic layer at a time and each layer is
**translated as a rigid body to its lattice site**, on a square array, mean placement `13.8 km`, maximum `25.5 km`.
The material does not stay. It is consumed here and deposited there.

So the frame shows **two places at one instant** and states on its face that they cannot share a scale. Its central
claim is arithmetic, not pictorial:

> The object is `1.74 m`; the deposit array is `36.1 km` across. **The two halves of the process are `2.1e4` apart.**

Seven derived predictions were fixed before the script existed and **seven were confirmed** (`N1`, `N4`–`N9'`). Three
of them are consistency checks against the registered record rather than new results, and they are worth naming
because they say the registered array geometry is self-consistent: the derived site spacing `0.4001 m` returns the
registered maximum placement `25.500 km` exactly, and `0.3826 × canvas` returns the registered mean `13.797 km`
against `13.8`. The front speed comes out as `c/√2 = 2.119853e8 m/s`, which is not a fit — it is `H/t_rip` with
`t_rip = √2H/c`, i.e. the closed form of `ME5`'s identity.

## 3. Two pre-run corrections, both because the first choice was wrong

1. **The object changed from the slab to the registered body.** The slab is better characterised for the *route*, but
   its plate **is** its whole `1 m²` cross-section, so a plate has side `1 m` and cannot sit on the registered
   `0.400 m` spacing. Borrowing that spacing would have mixed two objects; deriving a new one would have invented a
   number. The body carries every far-field constant natively. Consequence: **no aspect exaggeration is needed or
   used** — the withdrawn `z ×8` declaration is replaced by true proportions, which is strictly better than a frame
   that needs a disclaimer.
2. **The converted volume fraction is refused, and the refusal is the honest output.** The registered table gives
   per-segment *ranges* (`0.0063–0.0221`, `0.0464–0.0516`, `0.0202–0.0303`), not a profile. The declared
   piecewise-linear reconstruction integrates to `0.04992 m³`, **16.9% below** the registered `0.0601 m³` — so it is
   not the phantom. The frame therefore prints `f = z/H = 0.500`, which is definitional, says on its face that the
   volume fraction is not shown, and says why. That was prediction `N9'`, and it passed.

## 4. What the frame asserts, and what it refuses

Asserts: the object is consumed from one face; the front is a plane at `z = 0.869 m`; converted material has **left**;
it went to an array `36.1 km` across with `0.400 m` spacing; scale separation is why no single photograph exists.

Refuses: that the state is **two-dimensional, a graph, or readable** (`ME4` certifies only "no handles created";
`MR1.0`; `MR1.3` still reports **zero readable cells**); that a **camera** could record it (`q = 0` in the reflected
channel, `T5`); that the front position is **solved** (`D2`); that the drawn plates are a **census** (they are
symbols — `1.63e8` reached the front, `1.18e10` exist in total); any claim about **support or motion** (the remainder
is drawn in its initial position, and whether it would stand is not established here).

The drawing honours its own falsifier: the plate plume is placed beyond `0.19 m` while the silhouette's maximum radius
is `0.131 m`, so **no plate is drawn on the remaining material** — the first draft failed exactly this and was
re-rendered.

## 5. What it changes in the project's state

`G1` stays **`PARTIAL`**, with its character changed: the sweep is now depicted; the unfolded end state remains the
only `FL3` candidate. The amendment is written into `route_goal_conformance_v1.md` §5 rather than rewriting `G1`'s row.

More usefully, a **third independent route** now reaches the conclusion that `F3`/`GD8` reached from optics and `M5`
from photons: **`G1`'s single frame cannot exist.** Optics says the reflected channel is near-field sub-field only;
photons say the exposure budget is empty; kinematics says the two halves are `2.1e4` apart. The frame does not crop
that away — it is the subject.

## 6. Still true after this

No threshold changed. No frozen text edited. `TIER-LOCK`, `LOCKED-PATH` and the four admitted tiers untouched. Commit
gate **PASS** (`MUST-FIX 0 / provenance 0 / display 0`). `GD6` still blocks Phase 3, `GD9` is unsettled, and 25 of
27 images still carry no block.

---

## 7. Correction 2026-11-22 — the array panel's label was wrong about its own quantity

Found while auditing the submitted A.6 (`reports/reviews/eff_dim_claim_A6_v1_audit.md` §6). The code computed
`fill = plates_deposited / N_PLATE_REG` — the fraction of **plates** — and the panel labelled it "`%` of `90126²`
sites filled". Two different quantities, one label. The block is the authority here (it declares
`SCALAR: … deposit-site occupancy (binary)`), so the figure was corrected, not the block.

Corrected: `cells holding ≥ 1 plate = min(1, f × 1.4527)` = **72.5%** at `f = 0.5`, where the old label printed
49.9%.

The arithmetic then exposed a prior question that had never been asked, and it concerns a **frozen** census: with
`1.18e10` plates and `90126² = 8.1227e9` cells, there are **1.4527 plates per cell**, so a one-plate-per-cell reading
gives `145%` of cells filled. Either the side is `108628` or cells hold several plates. Registered **`GD10`** (open);
`H_eff` is unaffected, because plates are coplanar (`effective_2d_definition_v1_annex_B` §B.1).

The last caption line — "no claim that the state is two-dimensional … `ME4` certifies only no handles created" —
**stands**. A submission proposing to replace it was registered PROPOSED and not adopted; see `F10` of the audit for
why a declared claim cannot replace a measured refusal.

*Content generated by AI*
