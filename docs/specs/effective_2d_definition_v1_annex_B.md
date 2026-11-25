# Annex B to `effective_2d_definition_v1` — declared effective thickness and freeze-out energy

**Status**: **Annex, part of v1 by reference, not an amendment.** `docs/conventions/effective_2d_definition_v1.md`
is unchanged; this file supplies the two numbers v1 requires a caller to supply (§1's `E_probe` slot and §3's
`ΔE_z`), for the one object this project actually deposits.
**Origin**: a submission registered as `docs/specs/eff_dim_claim_A6_PROPOSED.md` (**PROPOSED, not adopted**).
**Audit**: `reports/reviews/eff_dim_claim_A6_v1_audit.md`. **Products**: `runs/FRONT/eff_dim_audit_results.txt`.
**Self-limitation.** This annex may not contain a tier threshold. It contains declarations, their scope, and the
list of what they do not settle. If a pass/fail threshold appears here, this annex has become a second lock and is
void.

---

## B.1 The thickness, and why `k` is not a multiplier

**Declared**: `H_eff = δ = 0.215 nm` — **one atomic layer**, and that is true regardless of how many plates a cell
receives.

The registered mechanism (`front_sweep_v1` §2) peels one atomic layer at a time and translates each layer as a rigid
body to its lattice site, "**joined edge-to-edge**". A plate is `0.215 nm` thick with area `6e-3–5e-2 m²`; a deposit
cell is `0.4001² = 0.160 m²`. Several plates therefore fit **inside one cell, side by side**, without occupying any
additional height.

The record contains no stacking step. Searching the mechanism documents for `stack`, `on top of`, `superposed`,
`one per site` returns nothing. So:

```
H_eff = k · δ      is NOT a relation in this model
H_eff = δ          for every k  (plates are coplanar pieces of one layer)
```

`k` — plates per cell — is a **coverage multiplicity**, not a thickness knob. The census value is `1.4527`
(`1.18e10` plates on `90126² = 8.1227e9` cells). Its open question is `GD10`, below, and it does **not** change
`H_eff`. What this fixes about the model's image in thickness is §B.8.

## B.2 The freeze-out energy, with its model declared

v1 §1 makes the model a required slot. **Model B (deep finite well)** is the applicable one: the object is a
material layer, not a compactified dimension, so there is no Kaluza–Klein tower and the gap is the first bound state
of a well.

```
ΔE_z = π ħ c / H_eff = π × 197.327 eV·nm / 0.215 nm = 2.883 keV
```

**Model C** (compactification on a circle) would give `2πħc/L = 5.767 keV`. It is stated here only so that a reader
who applies the wrong formula gets a number they can identify as the wrong formula. A.6 used `ħc/L`, which is
neither, and obtained `458 eV` from its own symbols.

**On `2.9 keV`.** The submission quotes `2.9 keV`, and that figure agrees with this annex to `0.6%`. It is right for
the wrong reason: it equals `hc/0.4307 nm`, i.e. the Model C formula applied to a thickness that is itself `2δ`.
Dropping `π` and doubling `δ` cancel to within the `0.33%` that `δ_A6/(2δ)` actually is. Nothing is repaired by that
agreement — the *number* is usable, the *derivation in the submission is not*, and any reuse of `H_eff = 0.4307 nm`
or of `E_1 = ħc/H_eff` elsewhere will be wrong on its own.

## B.3 Which bound: the external one, and only the external one

v1 §3 forbids combining the two bounds into one number. Named explicitly:

| bound | condition | value here | verdict |
| --- | --- | --- | --- |
| **internal self-consistency** | `E_F < ΔE_z` | `E_F = 6.73–73.37 MeV` vs `ΔE_z = 2.883 keV`; ratio `2.3e3–2.5e4` | **FAILS by 3.4–4.4 decades** |
| **external resolvability** | `E_probe < ΔE_z` | `E_probe = 2.25 eV`, `284 eV` | **holds** |

The internal bound is the tight one (`L_z ≲ 2 fm` per v1 §3); `0.215 nm` is `1.1e5 ×` thicker than that. So:

> **Affirmed**: a probe of energy below `2.883 keV` cannot resolve the residual `z` extent, so the deposit
> **appears** two-dimensional **to that probe**.
>
> **Denied**: that the deposit **is** a two-dimensional system. Its own occupation scale exceeds the gap by three to
> four decades, so the system itself populates the `z` mode. That sentence may not be written, in any document, as a
> consequence of this annex.

## B.4 The slot that is still empty

v1 §1 requires four slots; "2D has no referent" without the subsystem:

| slot | filled? | value |
| --- | --- | --- |
| model | yes | **B**, deep finite well (§B.2) |
| subsystem | **NO** | not supplied. Electrons, nucleons and collective modes give different `E_F`, hence different internal-bound verdicts |
| occupation scale `E_occ` | yes, and it fails | `E_F = 6.73–73.37 MeV` per v1 §4 |
| probe energy `E_probe` | yes | `2.25 eV`, `284 eV`, and any declared `E` (§B.5) |

**Therefore this annex declares a conditional with one open slot, and per §1 that conditional has no truth value
until a subsystem is named.** It is registered in that state deliberately: an incomplete conditional that says so is
worth more than a complete-looking one whose fourth slot was filled by assumption.

## B.5 The consequence worth having

`λ/H_eff` is the number that decides whether a probe could ever test this:

| probe | `E` | `λ` | `λ/H_eff` | could resolve `z`? |
| --- | --- | --- | --- | --- |
| visible (FL / reflection channel) | 2.25 eV | 551 nm | `2563` | no |
| transmission channel | 284 eV | 4.37 nm | `20.3` | no |
| submission's stated falsifier | 12 keV | 0.103 nm | `0.48` | **yes** |
| nuclear | 200 MeV | 6.2 fm | `3e-5` | yes |

Both channels this project images with are **below the freeze-out energy and above the resolution limit at the same
time**. The falsifying probe exists and is out of reach: `ME5` closes the transmission channel wherever `q > 0`.

> The energy that certifies two-dimensionality at `2.883 keV` is the same energy above which this project cannot
> image. **The claim and its test are mutually exclusive in the available channels.**

This is the honest form of the claim. It is weaker than "the state is effectively two-dimensional" and stronger
than nothing, because it cannot be mistaken for a measurement.

## B.6 What this annex does not do

1. **It does not close `ME4`.** `ME4` clause 3 certifies "no handles (genus) created beyond the census" — a
   topological statement about the deposit, frozen, and untouched. `H_eff` is not topological.
2. **It does not create a readable cell.** `MR1.0` stands: zero cells of the matrix may be read as readable.
3. **It does not replace the blanket "no claim that the state is two-dimensional".** That refusal is a *measured*
   statement (`ME4`, `MR1`); this annex is a *declared* one. A declared claim cannot replace a measured refusal, it
   can only sit beside it — and it must carry the word "declared" wherever it is cited.
4. **It does not settle `GD10`** — plates per cell. See below.
5. **It does not make `H_eff` measurable.** v1's four admitted tiers are statistics of a 2-D field: all of them
   unpack `W, H = u.shape`, so a third axis cannot enter (`eff_dim_audit_results` `S10`). The thickness stays
   declared.

## B.7 `GD10` — the question this annex had to raise

The frozen census has more plates than cells:

```
plates 1.18e10   cells 90126² = 8.1227e9   ⇒  1.4527 plates per cell
at one plate per cell: 3.68e9 plates unplaced, array side would be 108628
```

`ΔE_z` is unaffected (§B.1: coplanar), so this does not block the declaration above. It does block any statement
about *site occupancy*, any figure that draws it, and every version of `k` as a thickness. Two admissible repairs,
neither chosen here because the census is frozen:

- **(A)** the array side is `108628²` and one plate occupies one cell — canvas unchanged at `36.06 km`, spacing
  becomes `0.332 m`;
- **(B)** cells hold several plates, and the figure must draw a multiplicity rather than an occupancy.

Registered as `GD10`, open.

---

## B.8 `H_eff` has one value, and the Planck length is not a value it could have

**Status**: added 2026-11-22, in force as part of this annex. Ruling: `docs/decisions/t4_heff_floor_ruling_v1.md`.
Declared, never measured (B.6.5 stands). Contains no threshold.

### B.8.1 The thickness is a single point, not the bottom of a range

A submission (`runs/FRONT/t4_submission_verbatim.md`, Insertion A) proposed writing

```
H_eff = n_z · δ ≥ δ
```

**That form is refused**, and for a reason that makes the claim stronger rather than weaker. The record contains no
stacking step (§B.1: plates are coplanar, joined edge-to-edge; `front_sweep_v1` and `mid_sweep_frame_v1` contain
zero occurrences of `stack` / `on top of` / `superposed` / `one per site`). So a variable multiplier `n_z ≥ 1`
describes a freedom the construction does not have: it implies the deposit *could* be two or three atomic layers
thick if one chose. It could not.

> **The floor is not "no thinner than one layer". The floor is "one layer".** `δ` is not the bottom of the
> range — `δ` is the range.

`δ = h/N` is fixed by the stripping prescription; it is not a parameter, and `H_eff = δ = 0.215 nm` for every
configuration the model admits.

**Naming.** The layer variable here is `n_z`. It is **not** `k`: §B.1 registered `k` as plates per cell
(`1.4527`), a coverage multiplicity. Two quantities under one letter is the collision class `S9` governs.

### B.8.2 The Planck regime is excluded by the quantization, not pushed away by a distance

The record previously carried only a distance — *"25 orders of magnitude above the Planck scale"*, which is correct
(`δ/ℓ_P = 10^25.12`). A distance invites the reading *"far, but on the same axis, so approachable in principle"*.
The quantization gives an exclusion instead:

```
n_max(ℓ_P) = ℓ_P / δ = 1.6159e-35 m / 2.15e-10 m = 7.52e-26  <  1
```

No positive `n_z` satisfies it. **There is no admissible configuration at the Planck thickness**, and this is a
statement about the model's image, not about experimental reach:

| | value | reading |
| --- | --- | --- |
| thinnest admissible thickness | `δ = 0.215 nm` | one atomic layer; not a choice |
| Planck length | `1.6159e-35 m` | `δ/ℓ_P = 1.33e25` |
| `n_max(ℓ_P)` | `7.52e-26` | below one layer ⇒ no configuration |
| relation | — | **`ℓ_P` is not a far point on the thickness axis; it is not a point on that axis** |

> The model cannot thin the deposit toward `ℓ_P` the way a film is thinned toward zero. The thinnest admissible
> configuration is one layer, and `ℓ_P` lies `25` decades below the *unit*, not below the *value*.

**What follows for borrowed authority.** `D_eff → 2` (Padmanabhan et al. 2016) and CDT's spectral dimension
`4 → 2` concern dimensional reduction **at** the Planck scale. Since no configuration of this construction exists
there, those results cannot be evidence for this one — not because the interval is large, but because the two are
not in the same set of admissible thicknesses.

### B.8.3 Two arguments removed from the submission, and why

Both appeared in Insertion B and are **not** carried here:

1. **"Matter vanishes at `ℓ_P`."** Its arithmetic is correct (`V = ℓ_P·A = 5.24e-37 m³`, `V/V_0 = 9.29e-36`,
   `n = V/a³ = 5.24e-7 atoms`), and it is doing no work: `n_max < 1` already excludes the configuration, so a
   volume computation describing what it would contain argues a settled point a second, weaker way. It also invites
   the reading this annex exists to prevent — that `H_eff` is a continuous dial which, turned far enough down,
   yields "no matter", implying a little less turning yields a little less matter. There is no dial.
2. **The micro-black-hole measurement argument.** *"`E ~ E_Planck` concentrated within radius `r` makes the
   Schwarzschild radius `≥ r`"* is the standard heuristic, not an established inequality (it depends on
   centre-of-mass energy and impact parameter, not on `E` alone), and a heuristic cannot carry *"cannot be
   completed in principle"*. It is also moot: no measurement question arises for a configuration that does not
   exist.

A third correction: the submission's comparison row *"probe feasibility: measurable in visible"* reads as though
the visible channel could test the claim. §B.5 measured the opposite — `λ/H_eff = 2563` in the visible, so **both**
project channels sit below freeze-out **and** above their own resolution limit simultaneously. `2.883 keV` is the
energy above which this project cannot image. That row is not carried either.

### B.8.4 What §B.8 does not do

1. It does not make `H_eff` measurable — §B.6.5 stands; all four tiers unpack `W, H = u.shape`.
2. It does not license "the state **is** two-dimensional" — §B.3 stands, the internal bound still fails by
   `2.3e3–2.5e4`.
3. It does not create a readable cell — `MR1.0` stands.
4. It does not close `GD10` — §B.7 stands.
5. It does not restate `T4`. `T4` is in force as `MR1` (reading precondition). This section is a domain statement
   about thickness and is deliberately not numbered as a tier: it supplies no scene-referring definition, no
   separating quantity and no locked threshold, so under the admission rule it could not enter the matrix.

### B.8.5 Evidence

`runs/FRONT/t4_submission_verbatim.md` (submission, verbatim) · `runs/FRONT/t4_floor_registration.md`
(`P1`–`P14`, written before the executor) · `src/route/t4_floor_check.py` ·
`runs/FRONT/t4_floor_results.txt` (14 checks, `11/14` on first encoding, three of the three failures being defects
in my own tests — erratum appended, corrected `14/14`).

---

*Content generated by AI*
