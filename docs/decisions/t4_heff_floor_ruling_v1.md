# Ruling on the proposed `R1 §4.5.1` / `T4` insertion (the `H_eff ≥ δ` floor)

**Received**: 2026-11-22, as message text. **Registered verbatim**: `runs/FRONT/t4_submission_verbatim.md`
(`PROPOSED`, governs nothing).
**Registration of predictions**: `runs/FRONT/t4_floor_registration.md`, written before the executor existed.
**Executor**: `src/route/t4_floor_check.py`. **Product**: `runs/FRONT/t4_floor_results.txt` (14 checks, plus an
appended erratum covering three of my own defective tests).
**Subject**: a second submission on the same question as `A6` — whether the effective thickness, the freeze-out
energy and the Planck regime belong in the body of the route document `R1`.

---

## 1. Verdict

| Element | Verdict | Why |
| --- | --- | --- |
| **Insertion A** — `§4.5.1 Lower Bound on H_eff` | **NOT APPLICABLE AS WRITTEN** | the section it would extend does not exist (`B1`); its one equality is false by `6.33×` (`B4`); it names no bound (`B5`) |
| **Insertion B** — `T4` as a fifth tier in `§7` | **REFUSED AS A TIER, ACCEPTED AS A DOMAIN BOUNDARY** | supplies `0` of `3` admission requirements (`B3`); the label `T4` is already in force with another meaning (`B2`) |
| **Cross-reference 1** — append to the "self-consistent point" paragraph | **NOT APPLICABLE** | that paragraph is not in `R1` (`B1`) |
| **Cross-reference 2** — add a `T4` row to `§7`'s gap table | **NOT APPLICABLE** | `R1` has no `§7` gap table; `§7` is Correction 1 on the `C3` label |
| **Cross-reference 3** — cite `R1 §4.5.1` from `annex_A §A.6` | **REFUSED** | Annex A's last section is `A.5`; and the citation would run annex → route, inverting the direction every annex in this project uses |
| **The substance** — that `ℓ_P` is outside the model's image | **ACCEPTED, and it is better than what the record had** | `n_max(ℓ_P) = 7.52e-26 < 1` is a *derivation*, not a distance measurement; placed in Annex B §B.8 |

Two of the five blockers are mechanical, three are substantive. None is caution.

---

## 2. `B1` — both anchors are absent, and that is the smallest of the blockers

`R1` (`docs/decisions/staged_relaxation_visual_route_v1.md`) has **13 sections**, `§1`–`§13`. Occurrences of the
strings the insertion is anchored to:

| pattern | occurrences in `R1` |
| --- | --- |
| `k_max` | **0** |
| `H_eff` | **0** |
| `4.5.1` | **0** |
| `T4` | **0** |
| `self-consistent point` | **0** |

So `§4.5` does not exist, the `k_max` table is not in `R1`, and the "self-consistent point" paragraph is not in
`R1`. All three live in `docs/specs/eff_dim_claim_A6_PROPOSED.md` — the document this project declined last round.

The consequence is not merely that the line numbers are wrong. **The submission is anchored to `A6`, not to `R1`.**
Read that way it is coherent: it is a *revision of `A6`* that keeps `A6`'s `δ`, `N`, `k = 1` and `2.9 keV` and
replaces the "self-consistent point" with a lower bound. Revising `A6` is legitimate. Inserting into `R1` is not,
because there is nothing there to insert after.

There is also a small tell in the third cross-reference: it cites `annex_A §A.6`. Annex A ends at `§A.5`. `A.6` is
the *section name inside the declined spec* — which is what the submission is actually editing.

---

## 3. `B4` — the equality is false by `2π`, for the third document running

Insertion A prints one equality that decides everything downstream of it:

> `E ≤ ħc/δ = 2.9 keV`

With its own `δ = 4.307e-10 m`, `ħc/δ = 458.15 eV`. The printed number is `6.3297×` that value, and `2π` is
`6.2832` — agreement to `0.74%`.

The full table, recomputed from constants rather than carried over:

| formula \ `L` | `0.215 nm` (registered) | `0.2142 nm` (`H/`census cells) | `0.4307 nm` (submission) |
| --- | --- | --- | --- |
| `ħc/L` — **what is written** | `917.8` | `921.2` | **`458.2`** |
| `hc/L = 2πħc/L` — Model C | `5766.7` | `5787.9` | **`2878.7`** ← reproduces `2.9 keV` |
| `πħc/L` — Model B, registered | **`2883.4`** ← also reproduces it | `2893.9` | `1439.3` |

This is not a typo that a reader will catch. Last round `A6` printed the same equality and it was found false by
the same factor; the repair changed the sentence *around* the formula and left the formula. **The defect has now
survived two rewrites because each rewrite addressed the argument, not the arithmetic.**

`C3` closes the escape route that might excuse it — "perhaps `δ` is right and only the constant is wrong". Solving
`ħc/δ = 2.9 keV` for the thickness gives `δ = 68.044 pm`, which requires `N = 2.557e10` layers, i.e. **`3.160×`
the layer count the stripping prescription has**. So:

> **No thickness compatible with `Nδ = H` produces `2.9 keV` from `ħc/δ`.** The number `2.9 keV` in this project
> is `πħc/H_eff` (Model B, `Annex B` §B.2). It cannot be reached from `ħc/δ` at any `δ` that also satisfies the
> stripping.

`B5` compounds it: the same single number is stated without naming which bound it is. `effective_2d_definition_v1`
§3 says *"It is **forbidden** to combine the two into a single number… must specify which bound this `X` belongs
to."* Insertion A contains zero occurrences of `external`, `internal`, `Model B` or `subsystem`. Annex B, written
last round, does name it — the correct form exists one file away and the submission did not adopt it.

---

## 4. `B2` + `B3` — `T4` is already in force, and it cannot be a tier anyway

**`B2`.** The governor's round-22 ruling was *"`T4` → write into matrix reading rule 1"*, executed as `MR1.0`–`MR1.5`
in `docs/decisions/matrix_reading_rules_v1.md`. So `T4` today means **the reading precondition and the explicit
"no readable cell"**. Insertion B proposes `T4 — Domain Boundary of the Framework Itself`. That is one label for two
unrelated objects, which is the collision class `S9` was written for. Under `S9`(b) a rename is free, but it must be
the *unlocked* symbol that moves, and here both meanings are in force documents.

**`B3`.** The round-21 rule for a tier is explicit and was the governor's own:

> a tier must supply **(a)** a formal definition referencing only the scene, **(b)** a quantity taking values
> between unstructured and structured, **(c)** a threshold declared before the run and hash-locked. Missing any one,
> the tier may not enter the matrix.

Insertion B supplies **none of the three**, and says so itself: *"not a measurement gap"*, *"derived from the
stripping prescription rather than from any tier output"*, *"not closable by adding tiers"*. A document that
declines all three requirements while asking to be numbered alongside `L0`–`L3` is not a borderline case; it is
disqualified by its own description.

The correct home already exists. Round 22 created exactly two dispositions: *tiers* and **applicability-domain
boundaries** (`T1`/`T2` → Annex A: prohibition + known interval). `T4`'s content is the second kind. It should not
be numbered as a fifth tier.

*(My executor first scored `B3` as "2 of 3 supplied" by counting the string "domain of definition" as a formal
definition. It does not. Recorded as `E2` in the results erratum; the substantive count is `0`.)*

---

## 5. What survives — and why it is worth more than the passage that carried it

Everything above is about the wrapper. Inside it there is one result that is correct **and new**:

```
n_max(ℓ_P) = ℓ_P / δ = 1.6159e-35 / 0.215e-9 = 7.52e-26   < 1
```

No positive integer satisfies it, so **no admissible configuration exists at the Planck thickness.** With the
submission's own `δ` the figure is `3.75e-26` — its arithmetic there is right.

Why this is better than what the record had:

- The previous statement was a **distance**: "25 orders of magnitude above the Planck scale" (`10^25.12`,
  confirmed). A distance invites the reading "far, but on the same axis — presumably approachable in principle".
- The new statement is an **exclusion**: the deposit's thickness is quantized in units of one atomic layer, so the
  Planck length is not a far point on that axis, it is **not a point on the axis at all**. You cannot thin the
  deposit toward `ℓ_P` the way you can thin a film toward zero; the thinnest admissible configuration is one layer,
  and `ℓ_P` lies `25` decades below the *unit*, not below the value.

That is a real gain in kind, not in degree, and it is the thing the governor's second attempt was reaching for.
The submission's Planck-regime arithmetic (`V = 5.236e-37 m³`, `V/V_0 = 9.287e-36`, `n = 5.236e-7` atoms) also
checks out to `0.1%` — so this is not a submission that cannot compute. It is a correct new result carried in a
wrapper with an old defect.

**But one thing in the wrapper must not be carried across: `H_eff = k·δ` as a *variable*.**

`Annex B` §B.1 established that the record contains no stacking step — the plates are coplanar pieces of one layer,
"joined edge-to-edge", and searching the mechanism documents for `stack`, `on top of`, `superposed`, `one per site`
returns nothing (`front_sweep_v1`, `mid_sweep_frame_v1`: `0` hits each, re-confirmed here). So writing
`H_eff = k·δ ≥ δ` **grants a degree of freedom the model does not have**: it implies the deposit could be two or
three layers thick if you chose. It could not. `H_eff = δ` exactly, for every configuration.

That inversion matters, because the correct statement is *stronger*:

> The floor is not `H_eff ≥ δ` with `δ` a minimum. The floor is that `H_eff` has **one value**. `δ` is not the
> bottom of a range; it is the range.

And `k` must be renamed before any of this is citable: `Annex B` registered `k` as **plates per cell = `1.4527`**, a
coverage multiplicity. The submission's `k = 1` is a stacking number. Same letter, different quantity, both in
force — `S9`(a). The layer variable in the corrected text is `n_z`.

---

## 6. Two passages cut, and the reason each is cut

**Cut 1 — "matter vanishes".** The arithmetic is right; the argument is doing no work. At `n_max < 1` the
configuration is already excluded by existence, so a volume computation describing what it would contain is a
second, weaker reason for a conclusion already reached. Worse, it invites the exact misreading this project spends
documents preventing: that `H_eff` is a continuous dial which, turned far enough down, yields "no matter" — implying
that a little less turning yields "a little less matter". Under the model there is no dial. **Removed, not
demoted**: the table row "atoms accommodated: `5.2e-7`" goes with it.

**Cut 2 — the black-hole measurement argument.** `E ~ E_Planck` concentrated within radius `r` makes the
Schwarzschild radius `≥ r` — that inequality is not established by the sentence, and it depends on the probe's
centre-of-mass energy and impact parameter, not on `E` alone. It is the standard heuristic, and a heuristic cannot
carry the phrase *"cannot be completed in principle"*, which is a theorem-strength claim. It is also **redundant**:
no measurement question arises for a configuration that does not exist. **Removed.**

A third, smaller correction: the table row *"probe feasibility: frozen below soft X-ray, **measurable in visible**"*
reads as though the visible channel can test the claim. `Annex B` §B.5 measured the opposite — `λ/H_eff = 2563` in
the visible, so both project channels sit **below** freeze-out and **above** their own resolution limit at the same
time. `2.883 keV` is the energy above which the project cannot image. The row states the reverse of the finding and
is removed with the table.

---

## 7. Where the accepted text goes

**Not `R1`'s body.** Not because `R1` outranks it, but because `R1`'s `§4` ("Floor and discipline") is a
**qualitative** section — `55` words, **zero numeric constants** (`C7`). A `§4.5.1` full of `4.307e-10` and
`2.9 keV` would change the character of the section it enters, and the section is the one that says *no frame may
present falsified content*. A number that contradicts its own formula, sitting in that section, is the worst
possible placement for it.

**Not Annex A.** Annex A governs where `Q0` and `Q2` **outputs** may be cited. The thickness floor is not an
estimator's applicability domain; it is a property of the construction. Filing it there would widen the annex past
its title and past its stated scope.

**Yes: `effective_2d_definition_v1_annex_B.md`, new §B.8.** Annex B already owns `H_eff` and `ΔE_z`, already
establishes coplanarity in §B.1, already lists what it does not do in §B.6, and already handles `GD10` in §B.7. The
floor statement is a continuation of §B.1 and belongs beside it. Annex B is **not** digest-covered (only Annex A
carries a `.sha256` sidecar), so appending a section is an ordinary amendment with a recorded rationale, not a
re-lock. It contains no threshold, so the self-limitation holds.

**And the one shape in which `R1` may mention it.** If the governor wants `R1` to carry a line — and after two
submissions it is reasonable that he does — the legal form is a **pointer with no numbers**:

> The deposit's thickness is one atomic layer and is not a tunable quantity; its lower bound, the quantization that
> produces it, and the exclusion of the Planck regime are declared in `effective_2d_definition_v1` Annex B §B.8.

That sentence cannot contradict itself, cannot be mistaken for a derivation, and cannot be used to certify anything.
I have not inserted it: changes to `R1`'s authorised text are the governor's act (`R1` §5 item 2 is the precedent).
It is drafted and waiting.

---

## 8. What this ruling does not change

1. `MR1` — unchanged. Zero readable cells, for the two reasons already registered. Nothing here creates one.
2. The four tiers and their four locked thresholds — untouched; `threshold_lock.json` byte-identical.
3. `Annex B` §B.3 — the **external** bound only; the internal bound still fails by `2.3e3–2.5e4`, and the
   subsystem slot is still empty, so the conditional still has no truth value.
4. `GD10` — still open, still upstream of any statement about occupancy.
5. The four-tier battery — still blind to `z` (`S10`). The floor is **declared**, never measured; every citation of
   §B.8 must carry the word *declared*.
6. `A6-PROPOSED` — stays `PROPOSED` and stays superseded by Annex B.

---

## 9. Still open

`GD6` (`ME3`'s `φ`, blocks Phase 3) · `GD9` (route objective) · `GD10` (plates per cell) · route governance
(phased v2 vs the matrix after audit §6) · `MR2` (arrangement-sensitive tier — the only path from zero to a
readable cell, and it needs a new lock plus a pre-registration written before any data are shown) · `MR3`.

---

*Content generated by AI*
