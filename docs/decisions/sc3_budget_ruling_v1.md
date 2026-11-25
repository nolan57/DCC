# SC-3 — Ruling on the governor's mathematical review of SC-2

**Round**: 38. **Date**: 2026-11-22.
**Submission**: the governor's line-by-line review of `sc2_lineshape_ruling_v1.md` (§1–§5 plus the final
table). It accepts `STEP-NO-SCALE`, accepts the `g = 2` implication, accepts the two weight ratios, accepts
the broadening failure, and imposes five sharpenings, one of which (`g` in `A_INTER`) had not been raised
before.
**Product**: `runs/OPTICS/sc3_results.txt` (17 verdicts, 210 lines). **Registration**:
`runs/OPTICS/sc3_registration.md` (Q1–Q14 locked before the run).
**Verdict**: `ACCEPTED WITH THREE CORRECTIONS TO MY OWN RECORD`. 14/17 predictions. Three missed and stay
missed. Two of the misses were my arithmetic; one was my instrument.

---

## 0. What was reviewed and what it changed

The submission contains no error of physics that I can find. It contains **one question I had not asked**,
and that question turns out to dissolve the number I was most confident about:

> if the model carries a degeneracy `g`, what is `A_INTER` in terms of `g`?

Asked, it answers itself. `A_INTER = e²/(16ħ)` is the **single-cone, spinless** high-frequency height. The
module's `k_F = √(2πn)` is the **`g = 2`** Fermi momentum. So the module carries `g = 1` in its interband
amplitude and `g = 2` in its intraband one, and the mismatch is exactly a factor 2 (§3). The "underived
`1/4`" I reported in round 37 is therefore not underived at all — it is `g/4` at `g = 1`.

Chasing that question to the end produced this round's one genuinely new result:

> **`440.18 MeV = 3 ω_g`, identically** — under the module's own conventions the "derived band edge" is
> three times the threshold and carries no information about the budget at all (§2).

---

## 1. `STEP-NO-SCALE`: root accepted; the two criteria are measured to be independent

The governor accepts the root merge but requires that `S4` and `S5` remain **separate acceptance results**,
because repairing one symptom must not be read as repairing the other. This is stronger than "keep two
rows in a table", and it is testable: are there responses that pass exactly one of them?

There are. `Q7` constructs four and measures each (`sc3_results.txt` §C):

| response | `S4` (causality) | `S5` (weight) | what it is |
|---|---|---|---|
| (i) pure step `Aθ(ω−ω_g)` | **pass** | FAIL | its `Im` is the exact Hilbert partner; the weight diverges (4.50× budget at `10ω_g`) |
| (ii) truncated step with the untruncated partner | FAIL | **pass** | bounded weight (`f_inter = 0.9992`), residual `0.6194` — not causal |
| (iii) the record's module as-is | FAIL | FAIL | step term with a Drude partner and no upper scale |
| (iv) finite-weight oscillator | **pass** | **pass** | `W = S_pπ/2`, `K-K` residual `2.27e-7` |

All four cells are populated. So the implication fails in both directions, and the spec now says so in
words a future reader cannot miss: *neither criterion implies the other; two verdicts, always.*

The governor's second condition — that a finite band edge or an oscillator is not automatically a material
response — is confirmed by `Q12` in the strongest form available: a **6×5 grid** of `(ω_0, Γ)` at one fixed
`S_p` passes both criteria, **30/30**, because `S5` is closed-form in `S_p` and independent of both
parameters. Passing `S1–S13` therefore does not identify a material; it identifies a two-parameter family
of legal responses. Recorded as `ACCEPT-NOT-IDENTIFY` and written into §11.

One measurement note on `S4`: for the oscillator grid, `S4` is judged by **convergence**, not by a
threshold — the residual must fall when the quadrature is refined 4×, because a genuine non-causality would
plateau. Worst residual at `n = 1.6e6` is `9.50e-7`. This is the only honest way to apply a numerical `K-K`
test to thirty responses whose analytic answer is already known.

---

## 2. The budget: `440.18 MeV` was an endpoint, and it is identically `3ω_g`

### 2.1 The family, not the number

`S5` says `W_intra + W_inter = W_total`, i.e. `W_inter = f_inter W_total` with `f_inter = 1 − f_intra`.
Then

```
ω_end(f_inter) = ω_g + f_inter · W_total/A_INTER
```

measured (`Q1`): `146.7400` MeV at `f_inter = 0`, `293.4592` at `0.5`, `440.1784` at `1`. The ruling's
number is the `f_inter = 1` endpoint — the value at which the interband channel consumes the **entire**
budget and the Drude pole gets nothing.

### 2.2 Under the module's own partition the residual budget is exactly zero

`FSUM-SPLIT` measured `W_intra/W_total = 1 − 7.1e-5`. So `f_inter = 0`, residual budget `0.000000e+00`, and
the admissible band edge is `ω_g` itself. **The module's own configuration admits no interband term at
all**, at any `ω_end > ω_g`. This is not a bookkeeping quibble; it is the round's sharpest statement about
the module: the step term and the Drude pole cannot coexist under any partition, and the module contains
both.

### 2.3 The identity

`Q15`. With `k_F² = 2πn`, `m* = E_F/c²`, `ω_g = 2E_F/ħ` and `W/A = 8πħn/m*`:

```
(W/A) / (2ω_g) = 2π ħ² n c² / E_F² = 2πn / k_F² = 1
```

so `ω_end(f_inter = 1) = 3ω_g` **identically**. Measured `2.999717`, the `2.8e-4` being the
`73.37 / 73.3648` MeV rounding already logged in round 37.

The consequence is deflationary and worth stating plainly: my round-37 sentence *"this is the first
quantitative statement in the record of what `R1-B1` has to deliver for the optics stage"* was wrong. The
number is `3 × (threshold)`. It says nothing about any material, because it does not depend on `n_2D`, on
`g`, or on `v_F` — only on the convention that ties `m*` to `E_F/c²`.

### 2.4 Units

`Q3`. `W_total/A` is in `rad/s`. Converted once: `2.934384e8 eV = 293.4384 MeV`. Read as `eV` without the
conversion, the same numeral is `1.519267e15` too large — exactly `1/ħ`, to `1e-12`. So the governor's
second bookkeeping requirement is not a formality: it is a factor of `10^15`.

---

## 3. Degeneracy: the wording, and the factor of two that was hiding in it

### 3.1 Wording

The governor is right that "spectral weight depends on the degeneracy" is imprecise. `Q4` makes it exact
and also shows *how* imprecise: `W ∝ √(n g)`, so

```
W(4n, g) = W(n, 4g)   exactly (ratio 1.0000000000000000)
E_F(4n, g) / E_F(n, 4g) = 4.000000000
```

The budget sees only the **product** `n·g`; `E_F` is the only thing that separates the two. So the correct
form is: *at fixed `n_2D` and `v_F`, `W ∝ √g`; at fixed `g`, `W ∝ √n`; and neither statement stands alone.*

### 3.2 The `A_INTER`–`g` relation, which changes the defect

The per-cone spinless height is `e²/(16ħ)`; a model with degeneracy `g` has `σ_high = (g/4)σ_min`. The
module's `k_F = √(2πn)` fixes `g = 2`, so its interband height should be `3.042669e-05 S = 2.000000000000 ×`
what it is. `Q5`.

So the round-37 finding is **corrected, and worse**:

- round 37: `A_INTER` has dimension `S`, is `σ_min/4`, and the `1/4` is underived;
- round 38: the `1/4` is `g/4` at `g = 1`, and the module's own `k_F` says `g = 2`. The amplitude is
  underived *because it is inconsistent*, not because it is arbitrary.

### 3.3 `v_F`, which the record never wrote

`Q6b` **missed its registered value and the miss is the finding.** I registered `v_F = 0.9929 c` from a
hand-computed `k_F`; the machine says `1.000071 c`. My `k_F` was wrong — `√(2π·2.2e28) = 3.7179e14`, not the
`3.744e14` I used. The kill condition registered for exactly this case was: *"if `v_F/c = 1.000` rather than
`0.993`, the record's convention is `v_F = c` exactly and the sentence becomes simpler, not weaker."* It fired.

The record is a **`v_F = c` Dirac model**, to `7.1e-5`. (Its `m* = 143.58 m_e` is `143.56` when rebuilt as
`ħk_F/v_F`; the `2e-4` is the same `E_F` rounding.)

`Q6a` then measures what that convention is worth: the ceiling is **exactly proportional to `v_F`** —
`ceiling(v)/ceiling(v_record) = v/v_record` to `3.33e-16` across four decades — and at a graphene-like
`v_F = c/300` it is `1.4673 MeV`, not `440.18`. So the entire `440 MeV` statement is a velocity convention
wearing the clothes of a budget.

---

## 4. `α`: a point is not a certificate; the collapse is, and `α` is blind to the partition

### 4.1 A point is not a certificate (measured, not argued)

`Q8`: an equal-weight two-pole sum at `τ₂/τ₁ = 3` attains `α = 1` **exactly**, at `ωτ₁ = 0.697897`, with the
residual of `α − 1` driven to `1e-12` by bisection. So `α = 1` at a frequency is satisfied by a response
with two relaxation rates. The governor's point, made concrete.

### 4.2 What `α` at the peak does certify

`Q9` measured, at the peak of `−Imσ`:

| `τ₂/τ₁` | 1.01 | 1.05 | 1.1 | 1.5 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|---|---|---|
| `α` | 0.999993 | 0.999817 | 0.999272 | 0.987001 | 0.962537 | 0.908743 | 0.815538 | 0.539202 |

Monotone, strictly `≤ 1`, `α(3:1) = 0.9087` reproducing round 37. And it obeys a clean law:

```
1 − α_peak = 0.078 (ln τ₂/τ₁)²      to 11% for τ₂/τ₁ ≤ 3
```

`Q9b` is a **miss I keep**: I registered `α(1.05) ≤ 0.9995`; measured `0.999817`. The band was wrong, not
the claim — at 5% separation the deviation is `1.8e-4`. The law above is what the table actually supports,
and it says a 5% two-rate mixture is invisible to `α` at the peak.

### 4.3 The certificate

`Q10`. The registered form of `Q10` was "`α(ω)` is constant". That is **false for a single pole**:
`α(ω) = (4/π)arctan(ωτ)` runs from 0 to 2. I caught this before running and amended `Q10` in the registration
before any measurement (declared in `sc3_results.txt` §D.2), not after a miss. The correct sufficient
statistic is the **one-parameter collapse**:

```
max_ω | α(ω) − (4/π)arctan(ω τ_eff) |      single pole: 4.441e-16      two-pole 3:1: 8.592e-02
```

So `S12` becomes two clauses: `S12a` `α` at the peak (necessary), `S12b` the collapse residual (sufficient
within the Drude hypothesis). `α` at a point alone certifies nothing.

### 4.4 And `α` cannot see the partition — measured on my own instrument

`Q11b` is a **miss I keep**. I registered `|α(f_intra = 0.9) − α(f_intra = 0.5)| ≥ 0.4`. Measured `0.1622`:

| `f_intra` | `σ₁(ω→0)` [S] | `α` at peak |
|---|---|---|
| 0.90 | 388.557 | 1.038310 |
| 0.75 | 323.798 | 1.128854 |
| 0.50 | 215.865 | 1.200556 |

Two facts fall out, both useful:

1. `σ₁(0)` scales exactly as the Drude fraction (`388.557/215.865 = 1.799998`), so the four-tuple does not
   determine the response — `Q11` holds on the amplitude. That is the non-identifiability the governor
   predicted.
2. `α` moves by only `0.16` and **exceeds 1** for every `f_intra < 1` (a single Drude pole has `α ≤ 1` by
   construction). So `α > 1` is a reliable flag for "interband structure present", but `α` in `(1, 1.2)`
   cannot rank the partitions, and the round-37 claim that `S12` "makes the single-pole question decidable"
   must be weakened to: `S12` **decides against** a single pole; it does not decide **for** one, nor does it
   measure how the budget was split.

This is the cleanest instance in the project of a test that is correct, useful, and insufficient — and it
is the governor's own thesis applied to the instrument I built to enforce it.

---

## 5. `τ_tr/τ_sp = 91.5` is a model output — now with a second model attached

`Q13` kept the round-37 kernel and added one alternative, `|V|² ∝ (q² + q_TF²)⁻¹` (the 2D static form)
instead of `(q + q_TF)⁻²` (Thomas–Fermi):

```
τ_tr/τ_sp :  91.548  (TF)      138.016  (2D)      shift +50.8%
```

Same density, same `q_TF/k_F = 0.007298`, same single-particle lifetime definition. Only the small-`q`
behaviour of the screened potential changed. So `91.5` is not a property of a material and is not portable;
it is the size of the ambiguity **under a named kernel**, and it moves by half when the kernel changes.

---

## 6. The three misses, and the two instrument errors

| # | registered | measured | class |
|---|---|---|---|
| `Q6b` | `v_F = 0.993 c` | `1.000071 c` | **my arithmetic** — wrong `k_F`; the registered kill condition fired and the conclusion is sharper (`v_F = c`) |
| `Q9b` | `α(1.05) ≤ 0.9995` | `0.999817` | **my band** — the claim (`α < 1`, monotone) held; the quantitative band did not |
| `Q11b` | `|Δα| ≥ 0.4` | `0.1622` | **my band** — and the miss is informative: `α` is blind to the partition |

Instrument errors, archived rather than smoothed:

| # | error | evidence |
|---|---|---|
| E1 | section C recorded boolean **polarity** backwards: a large residual was labelled `pass` | `sc3_results_v1_SUPERSEDED_POLARITY.txt`, script `sc3_check_v1_SUPERSEDED.py.txt`. Numbers right, labels wrong. 5 cells mislabelled |
| E2 | oscillator `S5` threshold `1e-10` against a quadrature floor of `~1e-8` | third instance of "threshold picked without measuring the instrument"; fixed by using the closed form for the claim and the quadrature as a `1e-8` cross-check |
| E3 | the `v_F` law test compared a Dirac-computed numerator with a **module**-computed denominator, giving a spurious `9.45e-5` residual | fixed by a Dirac-only reference; residual became `3.33e-16`. Reported here because the first run printed `FAILED` for a law that is exact |
| E4 | **a fabricated digest**: the v1.2 lock file's `supersedes` entry for v1.1 was written with a `sha256` I typed from memory instead of reading `surface_conductivity_lock_v1_1.json`. Caught in the same round by cross-checking the two lock files, and replaced with the real `a005533bf3c5…` | this is the worst class of error in the project: a hash is a *claim of identity*, and an invented one would have silently defeated the whole locking discipline. Every digest in this round's lock is now copied from a file, never retyped |

The pattern in E2 and E3 is the same one flagged in rounds 35–37: **I write the threshold before I know
what the instrument can resolve.** It has now cost four verdicts. The countermeasure adopted from this
round on: any threshold on a numerical artifact must be quoted together with a convergence measurement at
two resolutions, in the same table.

---

## 7. `R1-B1`: four numbers are necessary, and measurably insufficient

The governor asks for a strict distinction among the four outputs and notes they are necessary but not
sufficient (§ final paragraph). `Q11` is the measurement of the insufficiency, so the interface can be
written as a specification with a reason attached rather than a wish:

**`R1-B1` must return, as a tuple:**

1. `n_2D` — carrier sheet density [m⁻²];
2. `g` — the **effective degeneracy actually participating** in the response (not "spin × valley" as a
   slogan: the number that appears in `k_F`, `E_F`, `W_total` and the interband height, the same number in
   all four);
3. `v_F` — the Fermi velocity of the band that carries the current [m/s]; must reproduce
   `E_F = ħk_Fv_F` with the returned `k_F`, or one of the three is wrong;
4. `ω_end` — the effective interband cut-off set by the real band structure or transition spectrum, **with
   its derivation**, not a budget-derived number. `440 MeV` is forbidden as an input: it is `3ω_g` (§2.3).

**and must additionally declare, because the four above cannot supply them** (measured: `Q11`, `Q12`):

5. the scattering mechanism(s) and the `τ` they imply, **named** (`TAU-KIND`) and not scanned;
6. whether the Drude reduction is admissible at all, and the evidence (`S12a` + `S12b`);
7. the current operator and the transition matrix elements (this is what fixes `A_INTER(g)`, i.e. the `g/4`
   factor of §3.2, and with it the whole interband height);
8. the spectral partition `f_intra`, or the experiment that fixes it.

Item 8 is the new obligation, and it is the one the optics stage cannot satisfy by itself: `f_intra` is a
free parameter of the response, not of the material, and both `S5` and `S12` are blind to it (`Q11b`). So
`f_intra` must come from the matter model — a band-resolved joint density of states — or from measurement.

**Until items 1–8 all exist, no `σ_s` is admissible, and `G6`/`DC2` stays `NO-GO`.** No material branch may
be chosen because it makes any of these easier (`NO-GO-ADMISSIBLE`, §11).

---

## 8. The final table of this round

| item | judgement | evidence |
|---|---|---|
| `STEP-NO-SCALE` root merge | accepted | §1, `Q7` 2×2 fully populated |
| `S4`/`S5` kept as two results | **adopted as criteria**; both now clause-level | §1 |
| one root, two symptoms | accepted, with one addition | a band edge bounds the weight but does **not** adjust `Im`: cell (ii) bounds the weight and still fails `S4`. The partner must be recomputed, not inherited |
| `W` depends on `g` only at fixed `n, v_F` | accepted; `W(4n,g) = W(n,4g)` exact | `Q4` |
| `A_INTER` must be tied to `g` | **accepted, and it fires**: `g = 1` vs `g = 2` | `Q5`, factor `2.000000000000` |
| `440.18 MeV` is an upper bound | **accepted and sharpened**: it is `3ω_g` identically | `Q15`, `2.999717` |
| budget definition must be fixed | accepted; `f_inter = 0` under the module's own partition | `Q2`, residual `0` |
| `ħ`/unit convention must be fixed | accepted; the error is `1/ħ = 1.5193e15` | `Q3` |
| broadening cannot bound the weight | re-confirmed | round 37 `B.2`, unchanged |
| `α` is a diagnostic, not a proof | accepted; the certificate is the collapse | `Q8`, `Q9`, `Q10` |
| `τ_tr/τ_sp = 91.5` is model-dependent | accepted; `+50.8%` under one kernel change | `Q13` |
| four outputs necessary, not sufficient | accepted; `f_intra` added as item 8 | `Q11`, `Q12` |
| `P1`'s two failures attributed correctly | accepted; unchanged | round 37 §6 |

**State of the route: unchanged.** `G6`/`DC2` `NO-GO`. `R1-B1` is the single entry point, and it now has two
measurable fences around it: `ω_end < 3ω_g` is forbidden as an input because it is an identity, and
`f_intra` must come with the matter model because the optics tests cannot see it.

---

*Content generated by AI*

---

## Errata `E5` (SC-4, round 39) — §2.2's partition citation

§2.2's sentence *"`FSUM-SPLIT` measured `W_intra/W_total = 1 − 7.1e-5`"* is a **mis-citation**.
FSUM-SPLIT measured `W_intra/W_total = 1.000000000003` at every `τ` (`runs/OPTICS/sc_route_results.txt`
§F, P15; `sc2_results.txt` §A.1 at max rel dev `6.88e-15`), and `7.1e-5` is the **`m*`/`E_F`
double-pinning slack** (`sc2_results.txt` §A.2: module `m*` from logged `E_F = 73.37 MeV` vs rebuilt from
`n_2D` → `73.3648 MeV`), not a partition share. The residual budget is zero **identically** (`sc2` §A.1,
P1 — the module's pole takes the whole budget by definition), not "to `1e-15`": the registered threshold
sat below the quadrature floor, and `sc3_budget_check.py:87-89` hardcoded `f_intra_mod = 1.0` instead of
measuring, so Q2's printed pass could never fail and would have missed on the measured ratio. §2.2's
conclusion stands unchanged — no interband term is admissible at any `ω_end > ω_g`; the admissible edge is
`ω_g` — and §2.3's identity (`3ω_g`) is untouched. Register:
`docs/decisions/sc4_partition_citation_errata_v1.md`.
