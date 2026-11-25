# Audit of the A.6 effective-dimensionality claim

**Subject**: `docs/specs/eff_dim_claim_A6_PROPOSED.md` (registered PROPOSED, verbatim).
**Products**: `runs/FRONT/eff_dim_audit_registration.md` (predictions, written before the executor existed),
`src/route/eff_dim_audit.py`, `runs/FRONT/eff_dim_audit_results.txt`.
**Question answered** (asked by the governor): should the freeze-out energy and the effective-2D condition be
copied into the body of the route document `R1`?

**Answer: no — and the reason is not caution.** Three of the submission's own numbers do not survive being read
together (§2), one of its central constructions is an identity (§3), and the clause it would occupy is forbidden by
§3 of the very convention it is about (§4). What survives is worth registering, and it is registered as
`docs/specs/effective_2d_definition_v1_annex_B.md` — an annex to the mandatory convention, not a line in a route.

**Audit score: 9 of 10 checks pass, 1 fails on its own stated tolerance.** The one failure is mine, not the
submission's, and it is disclosed rather than repaired (§6).

---

## 1. What the submission gets right

1. **`H_eff` was implicit and is now explicit.** A render that has a thickness but never declares it is
   unreproducible, and this is the gap `DC1` exists to close. This is a real contribution.
2. **The coverage-gap paragraph is correct, and executable.** A.6 says none of the four tiers is sensitive to
   `H_eff`. Checked structurally (`S10`): `total_persistence`, `char_scale` and `plug_q2` all unpack
   `W, H = u.shape` and index with `divmod(idx, H)`, `fft2`, `q[:-1, 1:]`. A third axis raises
   `ValueError: too many values to unpack`. **The tier battery has no slot for a z-axis.** A.6 is right, and this
   is the paragraph that should have stopped the claim rather than qualified it.
3. **The third bullet of "Scope" reproduces §5 of the mandatory convention correctly** — `L_z = 0` is a metric
   degeneracy, not a completed reduction.
4. **The `D_eff → 2` / CDT paragraph refuses borrowed authority correctly.** Those programs concern Planck-scale
   spectral dimension; 25 orders of magnitude away is 25 orders of magnitude away.

## 2. Three numbers that do not agree with each other

`S0` evaluates `E_1 = c/H_eff` for every plausible constant against both the declared thickness and the registered
one. Units: eV.

| formula \ `L` | `L = 0.215 nm` (registered) | `L = 0.4307 nm` (A.6) |
| --- | --- | --- |
| `ħc/L` — **what A.6 writes** | 917.8 | **458.2** |
| `hc/L = 2πħc/L` — Model C | 5766.7 | **2878.7** ← reproduces the quote |
| `πħc/L` — registered Model B | **2883.4** ← also reproduces the quote | 1439.3 |

**`F1` — the written formula does not yield the written number.** A.6 writes `E_1 = ħc/H_eff` and `H_eff = 0.4307
nm`; those two, together, give **458 eV**, not 2.9 keV. The quoted figure is `6.33 ×` what the written formula
produces — `2π` to 0.7%, and the residual 0.7% is exactly the `2.0033` of `F2`.

**`F2` — `δ` and `N` are both wrong by the same factor, so the relation A.6 prints hides it.** Registered `δ` is
`0.215 nm` and `N = H/δ = 8.084e9` (census `8.12e9`, 0.45% apart — the frame's own `N1` check). A.6 uses
`δ = 0.4307 nm` (high by `2.003`) and `N = 4.04e9` (low by `2.000`). Their product is still `H`, so `Nδ = H`
passes while both inputs are wrong. This is the third instance in this project of a factor that cancels because
*two* quantities carry it — after the `√2` span bound and the `9e20`/`9e14` exposure slip.

**`F3` — the quoted 2.9 keV is right by accident.** It is reachable two ways, and A.6 chose neither: `(hc, 0.4307
nm)` or `(πħc, 0.215 nm)`. Both are internally inconsistent with A.6's symbols — the first drops `π` from Model B
*and* uses the compactification constant on a material slab; the second repairs `δ` while keeping `ħ`. So the number
survives to 0.6% while both of its inputs are wrong (`S8`). **A number that reproduces under wrong inputs is not
evidence of the right inputs** — it is evidence that the inputs were never checked against each other.

## 3. `F4` — "the self-consistent point" is an identity, so it selects nothing

`k_max(E) = (ħc/E)/δ` and `E_1(k) = ħc/(kδ)`. Composed, `k_max(E_1(k)) = k` **identically**. `S3` sweeps
`k ∈ [0.1, 1e4]` under all three constants: the worst relative deviation is `2.2e-16`, i.e. floating-point zero.

Therefore:

> "The rendered configuration sits exactly at the self-consistent point `k = k_max(2.9 keV) = 1`. It is the largest
> stacking number that remains effective-two-dimensional at its own freeze-out energy."

is true of **every** `k`. `k = 1160` is equally "the largest stacking number that remains effective-two-dimensional
at its own freeze-out energy" — its own freeze-out energy being `2.5 eV`. A predicate satisfied by every value of
its argument cannot select the value it is presented as selecting.

This is the fourth instance of the vacuity class. `ME2` computed out to be the Euler–Lagrange equation; `ME3` was
algebraically identical to `C_info` (relative difference `0.0`); `ME4`'s "except at phase transitions" accommodated
`1000/1000` adversarial cases. The pattern is consistent enough to be a rule, and it is registered as **`S10`**.

## 4. `F5` — the claim occupies a clause the mandatory convention forbids

`effective_2d_definition_v1.md` §3, verbatim: *"**It is forbidden** to combine the two into a single number. Any
expression of the form 'effective 2D domain `E ≤ X` MeV' must specify which bound this `X` belongs to."*

A.6 states **one** number and never names a bound. Both bounds are tested against it (`S7`):

| state | `E_F` | `E_F / ΔE_z` | internal bound |
| --- | --- | --- | --- |
| frozen | 73.37 MeV | `2.53e4` | **FAILS** |
| HYB equilibrium | 21.54 MeV | `7.43e3` | **FAILS** |
| ALL2D equilibrium | 6.73 MeV | `2.32e3` | **FAILS** |

The internal bound requires `L_z ≲ 2 fm`; `0.215 nm` is `1.1e5 ×` thicker. So at `ΔE_z = 2.9 keV` the system
**itself** excites the z degree of freedom by four orders of magnitude. The only bound A.6 meets is the **external**
one — the loose one, `10^5 ×` looser by §3's own estimate. The correct sentence is "**appears** 2D to a probe below
`2.88 keV`", and "the state **is** effectively two-dimensional" is false as written.

**`F6` — two of four slots filled, and one of them is a false positive.** By keyword scan of the verbatim text
(`S6`): *subsystem* absent, *`E_occ`* absent, *`E_probe`* present, *model* present only because the string
"compactif" appears — in a **comparison-table row about the Planck scale**, not as a declaration for this object.
Per §1, "2D has no referent" without a subsystem, so the conditional has **no truth value** as submitted; it is not
merely incomplete.

## 5. `F7` — `k = 1` contradicts the census, and `H_eff = kδ` assumes a step the mechanism does not contain

`S5`, from the frozen census: `1.18e10` plates on `90126² = 8.1227e9` sites ⇒ **`k = 1.4527`**, not `1`. At
`k = 1` exactly, `3.677e9` plates are unplaced, and the array would need side `108628`, not `90126`.

That is the smaller problem. The larger one: **the record contains no stacking step.** `front_sweep_v1` §2 says
each layer is "translated as a rigid body to its lattice site and **joined edge-to-edge**"; a plate is `0.215 nm`
thick and `6e-3–5e-2 m²` in area, and a site cell is `0.4001² = 0.16 m²`. Two plates per cell fit **coplanar**.
Searching the mechanism documents for `stack`, `on top of`, `superposed`, `one per site` returns **nothing**.

So `H_eff = kδ` is not a relation in this model. The deposit is one atomic layer thick however many coplanar
pieces a cell receives — `H_eff = δ = 0.215 nm`, independent of `k`. **`k` is not a degree of freedom A.6 may vary;
it is a coverage multiplicity, and the object it multiplies does not stack.**

This is the finding that changes the answer to the governor's question. A.6's `k` is presented as a knob that trades
thickness against probe energy. There is no such knob in the registered mechanism.

## 6. `F8` — disclosure: my own frame has a label defect on this exact quantity

While checking `F7` I found a defect in `runs/FRONT/mid_sweep_fl1.png`, issued last round by me.
`src/route/front_sweep_frame.py:76` computes `fill = plates_deposited / N_PLATE_REG` — the fraction of **plates**
deposited — and line 197 labels it `"%.1f%% of %d^2 sites filled"`. Those are not the same quantity. The printed
`49.9%` is the fraction of plates; the site occupancy at that instant is `0.4991 × 1.4527 = 72.5%`.

The issued block declares `SCALAR: … deposit-site occupancy (binary)`, so the block is the authority and the figure
must match it. Corrected by re-rendering (the block is unchanged — no field moves, so `DC7` is not engaged).

**And the arithmetic exposes a prior question nobody had asked**: at full conversion the census gives
`145.3% of sites filled` under a one-plate-per-site reading. A fraction above 1 is not a rounding artefact; it means
the frozen census (`1.18e10` plates) and the frozen array side (`90126²`) cannot both hold under
one-plate-per-site. Either plates share cells, or the side is `108628`. **This is upstream of A.6's `k` and it is
registered as `GD10`.** A.6 does not resolve it — it assumes the one value (`k = 1`) that the census excludes.

## 7. `F9` — the one consequence worth keeping, which A.6 does not draw

If `ΔE_z = 2.88 keV` (`S9`), then both of the project's imaging channels sit below it, and their own wavelengths are
too long to see the residual thickness:

| probe | `E` | `λ` | `λ/H_eff` | z resolvable? |
| --- | --- | --- | --- | --- |
| visible (FL / reflection) | 2.25 eV | 551 nm | `2563` | **no** |
| transmission channel | 284 eV | 4.37 nm | `20.3` | **no** |
| A.6's own falsifier | 12 keV | 0.103 nm | `0.48` | yes |
| nuclear | 200 MeV | 6.2 fm | `0.00003` | yes |

So the claim is not merely true at the project's probes — **no probe the project uses can test it.** The falsifier
exists (12 keV) and is out of reach: `ME5`'s photon budget closes the transmission channel above the energies where
`q > 0`.

> **The number that certifies two-dimensionality at 2.9 keV is the same number that makes the claim untestable at
> every energy this project can afford.**

That is the honest form of A.6's claim, and it is stronger than the claim A.6 made, because it cannot be mistaken
for a measurement.

## 8. `F10` — "replaces the blanket no-claim" is a category error

The refusal A.6 proposes to replace has two owners and neither is A.6's to move:

- `ME4` clause 3 (**FROZEN**): "no handles (genus) are created beyond those the census already contains."
- `MR1.0` (**measured**): zero cells in the matrix may be read as readable.

A **declared** claim cannot replace a **measured** refusal; it can only sit beside it and be labelled as declared.
If it replaces it, every reader takes the frame as certified 2D — which is the exact over-reading that `MR1` was
written to prevent, and that `DC1`'s block exists to make impossible.

Concretely: `mid_sweep_fl1.png` still certifies only "no handles created". Nothing in this audit changes that.

## 9. Disposition, and the answer to the question

**Do not copy A.6 into `R1`'s body** — on three findings, not on caution:

1. The written formula yields `458 eV`; a body text carrying `E_1 = ħc/H_eff = 2.9 keV` is a formula that
   contradicts its own value, and the value is the part that will be quoted (`F1`).
2. The "self-consistent point" is an identity, so as a *route* line it would appear to justify a design choice it
   cannot justify (`F4`).
3. The clause it would occupy is forbidden by `effective_2d_definition_v1` §3, which the route does not outrank
   (`F6`).

**What is registered instead**, in `docs/specs/effective_2d_definition_v1_annex_B.md`:

- `H_eff = δ = 0.215 nm`, **coplanar**, independent of plates-per-cell (`F7`);
- `ΔE_z = πħc/H_eff = 2.883 keV`, **Model B declared**, matching the convention's own formula rather than A.6's;
- the bound **named**: external only; internal fails by `2.3e3–2.5e4` (`F5`);
- the slot that is missing stated as missing: no subsystem, so the conditional has no truth value yet (`F6`);
- the probe-blindness consequence, which is the part that is new and useful (`F9`);
- and an explicit list of what it does **not** do (`F10`).

The annex is a separate file, not an amendment, for the same reason Annex A was: the mandatory convention is not
digest-covered, but the tier thresholds are, and a document that must remain citable across a lock should not be the
document that carries a claim about what has *not* been measured.

## 10. Prediction ledger, honestly scored

| # | Prediction | Result |
| --- | --- | --- |
| `P1` | written formula → `458 eV`; ratio `2π` to `1e-12`... to `<0.5%` | **FAILED** — ratio `6.3297` vs `6.2832`, i.e. **0.74%** |
| `P2` | only two (formula, `L`) pairs reproduce the quote | confirmed |
| `P3` | identity holds to `<1e-12` over `k ∈ [0.1, 1e4]` | confirmed, `2.2e-16` |
| `P4` | `N` low by `2.00`, `δ` high by `2.00` | confirmed, `0.4998` / `2.0033` |
| `P5` | `k = 1.45` from the census; array would need side `1.09e5` | confirmed |
| `P6` | at most 2 of 4 slots | confirmed, 2 — and one is a false positive (`F6`) |
| `P7` | internal bound fails by `>1e3` | confirmed, `2.3e3–2.5e4` |
| `P8` | quote within 1% of corrected, `>5×` the as-written | confirmed, `0.6%` / `6.3×` |
| `S9` | both project probes below freeze-out | confirmed |
| `S10` | tiers cannot accept a 3-D field | confirmed |

**`P1` failed on my own tolerance and I did not move it.** `0.74% > 0.5%`, so the check reports FAIL and the ledger
says FAILED. The mechanism (`2π`) is confirmed; what failed is the precision I wrote into the prediction, and the
residual is fully decomposed: `2π × (δ_A6/2δ_reg) = 2π × 1.00165`, the same `2.0033` that `P4` measures from the
other side. Relaxing `0.5%` to `1%` after seeing the run would be the exact move this project has convicted three
times, so the failure stands in the product and is reported in the headline count.

Two things this round learned that were not asked for: the frame's label defect (`F8`, my own), and the
plates-versus-sites inconsistency in a **frozen** census (`F8`/`GD10`), which is upstream of the question the
governor asked and had to be raised before `k` could mean anything.

---

*Content generated by AI*
