# Ruling on the proposed `R1 §4.6` — kinematic vs dynamic unfolding

**Received**: 2026-11-22. **Registered verbatim**: `runs/FRONT/kin_dyn_submission_verbatim.md` (`PROPOSED`,
governs nothing).
**Registration of predictions**: `runs/FRONT/kin_dyn_registration.md` (`P1`–`P12`, written before the executor).
**Executor**: `src/route/kinematic_dynamic_check.py`. **Product**: `runs/FRONT/kin_dyn_results.txt`
(`12` checks, `12` passed).

**This submission is different in kind from the first two, and the ruling is too.** Those were about a number;
this is about a **category**, and the category is right. D2 is a relabelling, not a dynamics, and the framework
owes a statement saying so. What fails is the worked example offered to make it concrete, and the labels and
anchors around it.

---

## 1. Verdict

| Element | Verdict | Why |
| --- | --- | --- |
| **The distinction** (kinematic relabelling ≠ dynamical unfolding) | **ACCEPTED — and it is overdue** | correct; and the record says something stronger than the submission does (§2) |
| **The claim "no claim that physical unfolding reproduces `Π`"** | **ACCEPTED, registered** | exactly the discipline this project applies elsewhere; §6 below is its authorised form |
| `§4.6.1` worked example — the projection rule | **REJECTED** | the example's `Π` is not D2's map, and its strain `8.37e8` is the quantity `front_sweep_v1` already corrected (§3) |
| `§4.6.1` — the interface argument | **REJECTED** | traction is continuous at a bonded interface; **strain** is what jumps — the text has them swapped (§4) |
| `§4.6.1` — the `1 : 10` strain ratio | **REJECTED** | that is the *unbonded* ratio, quoted for a body the example declares bonded (§5) |
| `§4.6.1` — "bone-like" / "soft-tissue-like" | **REJECTED as labels** | a contrast of `10` is `3`–`6` decades below the pair it names (§5) |
| `§4.6.2` scope note | **PARTLY ACCEPTED** | "the example is illustrative, not a prediction" is right; "the discrepancy is present at all thicknesses" contradicts it (§6) |
| Cross-reference 1 → `§3` D2 statement | **APPLICABLE — the only one** | `§3` exists and names `D2` (`7` occurrences) |
| Cross-reference 2 → `§7` gap list, new `T5` | **REFUSED** | `§7` is Correction 1, not a gap list; and `T5` is in force in `tier_admission_v1` for a different object |
| Cross-reference 3 → `§4.5.1` | **NOT APPLICABLE** | refused last round; `0` occurrences in `R1` |
| **A timescale result the submission did not compute** | **NEW — and it inverts its conclusion** | §7 |

---

## 2. The distinction is correct, and the record's reason is stronger than the submission's

The submission says D2 *"contains no force, no stress, no constitutive law"*. True, but weaker than what the
mechanism document already says:

> `front_sweep_v1` §2 ②: "the whole layer is translated to its lattice site as a 2D rigid body — **intralayer
> (x,y) identity map → intralayer strain always 0**." ③: "no in-plane bonding is performed. The space between
> pieces is vacuum."

So D2 does not *omit* a constitutive law — it **performs no deformation**. Nothing is stretched, so nothing has
strain energy to release; the pieces are not joined, so there is no interface to delaminate. The zero in the
"stored energy" row is a property of the construction, not an idealisation of the material.

That distinction is not pedantry. It decides whether the missing dynamics is a **gap** (we did not model it) or a
**non-question** (there is no such object). It is the second, and the submission's own framing — *"an external
agent enforces `Π` exactly"* — gets this backwards: no agent enforces a strain field here, because no strain field
is imposed.

---

## 3. The worked example's map is not D2's map

The submission prescribes

```
Π: (r, θ, z) ↦ ( (R/δ) r cos θ , (R/δ) r sin θ )
```

and describes it as *"the same disc of radius `R/δ` array sites"*. But:

| | coefficient | image of `r = R` |
| --- | --- | --- |
| what the prose needs | `1/δ` | `R/δ` sites |
| what the formula has | `R/δ` | `R²/δ` |

The two differ by the factor `R`. *(A count of sites and a length in metres are not comparable, so no numeric
ratio between them means anything — the unit-free coefficient comparison is the only sound statement, and it is
what the table gives.)*

Worse, either version contradicts the mechanism: D2's in-plane map is the **identity** (strain `0`), and a uniform
radial dilation by `R/δ` has in-plane strain `R/δ − 1 = 8.372e8`. That number is within `10%` of `9.28e8` — the
figure `front_sweep_v1` §2 line 49 corrected last round with the sentence *"9.28e8 is the **displacement gradient
of the mapping**, not the strain of the material."*

> The worked example reintroduces, as a strain, exactly the quantity the record corrected one round ago, at the
> same magnitude. An illustration of "kinematic vs dynamic" that smuggles back the kinematic error it is meant to
> separate is not usable as an illustration.

*(That `10%` agreement is a **marginal pass** of `P3` at `9.78%` against my declared `±10%`. The finding rests on
the second row of the table — D2's map implies `0`, the example's implies `8.4e8` — not on the agreement.)*

---

## 4. The interface argument is inverted

> Submission: "the two materials must remain bonded, so radial displacement is continuous but **radial stress is
> not**."

| quantity | at `r = r_c` | why |
| --- | --- | --- |
| radial displacement `u_r` | continuous | perfect bonding, no slip |
| radial traction `σ_rr` | **continuous** | Newton's third law across the interface, absent interface stresses |
| radial strain `ε_rr` | **jumps**, by `μ_1/μ_2 = 10` | `ε = σ/E` with `σ` shared and `E` different |

Traction continuity is not a detail — it is the defining property of a bonded interface, and it is what forces the
strain to be the discontinuous quantity. The submission asserts the reverse and then builds its "mismatch
`Δσ ~ (μ_1 − μ_2) ∂u_r/∂r` concentrates at the interface" on the reversed premise. A stress concentration near the
interface does occur, but from the **constraint** of shared displacement, and `σ_rr` is continuous across it by
construction.

---

## 5. Two mislabels inside the example

**The `1 : 10` strain ratio is the unbonded one.** `ε_2 = σ/μ_2 = 10 σ/μ_1` holds at *equal applied stress*, i.e.
for two free-standing regions. The example simultaneously insists the interface *"must remain bonded"* — which
imposes shared displacement and drives the ratio toward `1`. The bonded body's ratio lies strictly between `1` and
`10`, set by geometry. The summary table quotes the `1 : 10` row as the dynamic prediction while its own
"timing" row and "interface stress" paragraph require the bonded case. **The example contradicts itself**, and
that contradiction is the interesting physics it declined to compute.

**"Bone-like" at `μ_1 = 10 μ_2` is not bone-like.** Cortical bone has shear modulus `~10^9–10^10 Pa`; soft tissue
`~10^3–10^5 Pa`. The implied contrast is `10^4`–`10^7`, i.e. `4`–`7` decades, against the example's `1` decade.
As two unspecified polymers the numbers are fine; the labels overclaim the contrast by `3`–`6` decades. Since the
contrast *is* the mechanism being illustrated, the labels are not decoration.

---

## 6. What is registered, in the authorised form

`docs/decisions/front_sweep_v1.md` is the owner of what D2 is, so this statement is registered as a **scope
clause of the mechanism**, not as a section of the route:

> **D2 performs no deformation.** Each layer is translated as a rigid body to its lattice site and joined
> edge-to-edge, with vacuum between pieces. Intralayer strain is therefore zero *by construction*, not by an
> idealisation of the material. No claim is made that a body driven by its own constitutive law would arrange
> itself the way D2 arranges it. That question is not merely unanswered — it is **unaddressed**, and it is not a
> defect of the deposition, because the deposition does not build a strained body. **Declared**, not measured;
> no frame may depict elastic unfolding, differential strain, or fracture as a consequence of D2.

The last clause is the operative one: it forbids a picture, which is the form this project uses when it wants a
prohibition to bind.

**One sentence of the scope note is refused.** *"The discrepancy is present at all thicknesses; it does not
disappear as `H_eff → δ`"* contradicts the sentence before it — at `H_eff ~ δ` the continuum elastic description is
explicitly at the edge of validity, so `μ` is not defined there and the discrepancy cannot be asserted across a
regime where the model producing it has failed. The honest scope is narrower: **the example illustrates a
structural distinction; it predicts nothing at the project's thickness.** The submission's own first sentence
already says this, and the second sentence takes it back.

---

## 7. The result the submission did not compute, and it inverts its conclusion

The example never evaluates a time, so it cannot notice that its own counterfactual body does not exist at any
instant that looks like the frame. Two responses, both computable from `R`, `δ` and `c_s`:

| response | time | vs `t_rip = 8.2553e-9 s` |
| --- | --- | --- |
| through-thickness (`2δ/c_s`) | `4.30e-13 s` | **`1.92e4 ×` before** the conversion ends |
| in-plane equilibration (`R/c_s`) | `1.80e-4 s` | **`2.18e4 ×` after** it |

and their ratio is `t_r/t_z = R/(2δ) = 4.19e8 = 8.62` decades — **independent of `μ` and `ρ`**, purely geometric.

> For the body the example posits — bonded, compressed to `2δ`, released — the thickness returns `1.9e4` times
> faster than the conversion completes, and the in-plane arrangement settles `2.2e4` times after it. **There is no
> instant at which that body looks like the kinematic map.** The discrepancy is not "sequential versus
> simultaneous propagation"; it is that the counterfactual body is *outside the frame in both directions*.

And then the observation that closes it: **D2 does not build that body.** It builds a relaxed single layer with no
stored energy, so the rebound question never arises for the thing the framework actually deposits. The submission's
"stored energy `0`" row is right — for a reason it did not give, and that reason is the whole answer.

Consequence for the visualisation: no frame at `t ≤ t_rip` can show elastic unfolding **or** refute it. The
kinematic choice is therefore not a distorting idealisation of what is depicted — it is an unfalsifiable-by-image
choice, which is a weaker position than "we idealised and the idealisation is harmless", and it must be stated as
the weaker one.

---

## 8. Labels and anchors

- **`T5` refused.** `tier_admission_v1.md` already carries `` `T5` — `L3` is still empty under `C1` in
  reflection ``. This is the **second label collision in two submissions** (`T4` was the first). A kinematic/
  dynamic conflation is also not a tier: it supplies no scene statistic and no locked threshold, the same
  disqualification as last round.
- **`§7` is not a gap list.** It is `Correction 1 (ledger): "C3 relaxed" in the ladder mislabels a different
  object`. The requested row has no home.
- **`§4.5.1` does not exist** (`0` occurrences) — refused last round, and the cross-reference is anchored to it
  again.
- **`§3` does exist and names `D2`** (`7` occurrences). Cross-reference 1 is the only one of the three that is
  mechanically possible. I have **not** made it: `R1`'s authorised text is the governor's to change (`§5` item 2),
  and the sentence below is drafted for insertion if he wants it.

> For insertion into `R1` §3, if the governor wants it — no numbers, so nothing to contradict:
>
> *The unfolding rule `Π` is kinematic: it relabels material points onto array sites and performs no deformation.
> The framework makes no claim about how a body driven by its own constitutive law would unfold. See
> `front_sweep_v1` §2 and its scope clause.*

---

## 9. My own defects this round

Three, all in the executor, all caught before this document was written and recorded in the product:

1. `C2` first called the formula "one factor `R` larger". Wrong direction, and void — a count and a length are
   not comparable. Replaced with the unit-free coefficient comparison.
2. `count()` ran without `re.MULTILINE`, so every `^`-anchored pattern returned a false zero, including one row of
   `C8`. A first attempt to patch it silently failed to apply, which briefly made the correction note itself false.
3. `r'\bD2\b'` was double-escaped and matched a literal backslash, so `C11` reported `0` occurrences of `D2` and a
   missing `§3` heading regardless of the file. Recomputed: `7` and present.

None of the twelve predictions changed verdict after correction, and no finding in this ruling rests on a
corrected check. But this is the third round running in which the failures are mine rather than the submission's,
and the pattern is now specific enough to name: **I write a proxy statistic, it passes for the wrong reason, and
the pass is reported before the proxy is audited.** The mitigation used here — recompute the three figures
independently before citing them — is what the next round should do first rather than last.

---

## 10. What this does not change

1. `MR1` — zero readable cells. Nothing here creates one.
2. The four tiers and their locked thresholds — untouched; `threshold_lock.json` byte-identical.
3. `Annex B` §B.3 (external bound only) and §B.8 (`H_eff` has one value) — unchanged. Note §B.8 is now *more*
   clearly correct: since D2 performs no deformation, there was never a stacked or strained state for a
   multiplier to describe.
4. `GD10` — still open.
5. `A6-PROPOSED` and `T4-INSERTION` — still `PROPOSED`, still superseded.

---

## 11. Still open

`GD6` (`ME3`'s `φ`, blocks Phase 3) · `GD9` (route objective) · `GD10` (plates per cell) · route governance
(phased v2 vs the matrix) · `MR2` (arrangement-sensitive tier) · `MR3`.

---

*Content generated by AI*

---

## 12. Adiabaticity — status change to `WORKING-HYPOTHESIS` (round 71, G-71-01 §3.1)

**This section does not re-derive §7 and does not weaken it.** It changes how one premise is *carried*, and
records which archived statements depend on it.

**The premise.** The smooth 2D-ization branch — the reading in which a real 3D body is transformed into an
effective-2D one *continuously* — presupposes that the transformation is slow compared with the system's internal
response, i.e. adiabatic. `AX-01` audited that premise and labelled it `ASSUMPTION`
(`runs/AX/ax01_axiom_audit_results.txt`, `AX-S02`, finding `F-004`): it was used, and it was never stated as a
condition. That label is historical and stays in the sealed audit; the *live* status is changed here.

**New status: `WORKING-HYPOTHESIS`.** Any derivation step that needs it must cite it as
`[WORKING-HYPOTHESIS: adiabaticity; see RR-DT-01 §3.1]` and may proceed without proving it. The hypothesis is
not evidence, and passing through this section does not convert it into one.

**What §7 of this document already settles, and why the promotion is not a repair of a defect.** §7's two
timescales — through-thickness return `2δ/c_s = 4.30e-13 s` (`1.92e4 ×` before `t_rip`) and in-plane equilibration
`R/c_s = 1.80e-4 s` (`2.18e4 ×` after it), ratio `R/(2δ) = 4.19e8` — belong to a **counterfactual elastic body**
that D2 does not build. §7 says so in its own words: "D2 does not build that body. It builds a relaxed single layer
with no stored energy." So the measurement that makes the *dynamical* reading non-adiabatic is not a measurement
about the deposition; it is a measurement about a body the framework never posits. The premise is therefore
unstated for the dynamical reading, and **unnecessary** for the kinematic one. That asymmetry is the reason the
programme can carry the hypothesis and keep advancing.

**Dependent statements, and what the hypothesis buys each of them.**

| statement | dependence | status under the hypothesis |
|---|---|---|
| `C2` smooth 2D-ification, intralayer reading | none — identity of the prescribed map | unchanged (crosswalk §8.3) |
| `C2` full-smoothness reading | total — false at `S0` before any relaxation | unchanged; the hypothesis does not make it true |
| the `E∧S∧W` corner of the assumption matrix | `S` is one of its three letters | unchanged; §4 of `scifi_boundary_v1.md` already records that `S` and `W` cannot be had together |
| `RL-2`'s relief scene | none — static geometry | unchanged, `V = ε` |
| any future joint geometry/field/matter solve | total — a solve that assumes a quasi-static sequence | **may proceed** under the tag, and may not report the assumption as satisfied |

**What the hypothesis does not buy.** It does not give the object a 2D ground state, does not move `G0′` row 7,
does not make the `3–5 ns` transient reversible, does not relax `C3`, and does not license a visibility claim. Those
were decided by other arguments and none of them cited adiabaticity.

**Retention clause (G-71-01 §3.1, last bullet).** If a later round disproves the hypothesis, results derived under
it are not discarded: they are retained as the *ideal limit* — the adiabatic approximation of the system — and must
be re-labelled `IDEAL-LIMIT` rather than withdrawn. The branch that survives a disproof is the one §4 of
`scifi_boundary_v1.md` already prices: `E ∧ ¬S ∧ W`, the fireball corner.
