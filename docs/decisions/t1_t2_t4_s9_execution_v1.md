# Execution of rulings T1 / T2 / T4 / S9 — applicability domains, reading rule 1, and the two scopes of S9

Date: 2026-11-22
Authority: governor ruling, three items, each marked *no new lock required*.
Status: **executed.** No threshold was re-declared, no tier was re-admitted, no lock was created.

| Item | Ruling | Executed as |
| --- | --- | --- |
| `T1`/`T2` | register as applicability-domain boundaries: prohibition on use as evidence + known boundary interval | `docs/specs/intrinsic_structure_tiers_v1_annex_A.md` (§A.1, §A.2), measured by two runs |
| `T4` | write into matrix reading rule 1: reading precondition + explicit "no readable cell" | `docs/decisions/matrix_reading_rules_v1.md` `R1.0`–`R1.5` |
| `S9` | in force as the sole rule, **distinguishing locked from unlocked symbols** | `docs/conventions/symbol_registry.md` §5 `S9`(a)(b)(c) + `src/common/locked_path_guard.py` |

---

## 1. `T1` — the boundary is on histogram concentration, and no amplitude precondition can reach it

Ruling taken literally: do not repair the estimator, narrow the domain in which its output may be cited.

`Q0` crosses its locked threshold at **modal mass `0.8720`**. Above that line it **rises as the field empties**
(modal `0.9946` → `Q0 = 0.9764`), which is `T1` stated as a domain rather than as an anecdote about `DITHER`.

The important negative result is about the *existing* precondition. `Q0` is invariant to amplitude: over a
`120×` range of dither amplitude the total persistence moves `1.1191e-2 → 1.3175e-2`, and `Q0` only `0.7664 →
0.8016`. The reason is structural, not incidental — `total_persistence` normalises through `quant()`, which maps
the observed span onto `0..1`, so the amplitude is divided out before the persistence exists. **The declared
precondition `σ_u/Δu ≥ 0.01` tests a quantity the pipeline has already made scale-free**, so it can never detect
this defect at any amplitude. The prohibition therefore has to be on histogram concentration, which is what
`0.87` is. This strengthens the finding: `T1` was not "the precondition is set too low", it was "that
precondition cannot function".

## 2. `T2` — three mechanisms; the first two were mine and both are wrong

The registered `T2` said the bias correction "is calibrated at 64-bin uniform and does not transfer". **Wrong**:
on the same `NOISE` field the raw `q2` differs by `0.0932` between 16 and 64 bins, but the nulls differ by
`0.0921`, so the renormalised values agree to `0.0013`. The correction transfers.

My first replacement — `plug_q2`'s joint table is `16×16×64 = 16384` cells against `127×127 = 16129` samples,
one parameter per sample — **is also wrong as a causal account**. Shrinking the table to `256` cells leaves the
raw `q2` at `0.913223`, unchanged to six decimals. The table size moves the **null**, not the measurement.

**The account the data support**: the plug-in bias is *field-dependent* (roughly, on how many table cells the
field occupies), while the renormalisation subtracts a *fixed uniform-field* bias. Where the raw signal is large
(`0.913`) the mismatch costs `0.0137`; where it is small (`0.0041`, a `99.5%`-constant field) the same mismatch
is several times the signal and flips the sign to `−0.1556`.

Hence the prohibition is total on one side: **a `Q2` fail is never admissible evidence; only a pass is**, biased
low by at most `1.4%`. `Q2` may acquit, never convict. Both wrong mechanisms are recorded in Annex A §A.3 rather
than deleted — the same number was explained twice by two different wrong stories, which is how this defect
survived a round.

**The two prohibitions are complementary.** `Q0`'s **pass** is restricted (high modal mass); `Q2`'s **fail** is
restricted (always). A cell assembled carelessly would take `Q0`'s false credit on an empty field and `Q2`'s
false conviction of a structured one — reporting the exact inverse of the truth. That is why Annex A is a
precondition of the reading rules, not a note attached to them.

## 3. `T4` — reading rule `R1`, with the zero stated explicitly

`R1.0` forbids reading any cell as "readable". `R1.3` states **zero readable cells** and gives both independent
reasons: the reflection channel's `Q3` is `0` of `9` because `q = 0` exactly (not low contrast), and the
transmission channel's `Q3` has never seen a scene carrying the 2D-ified content. `R1.2` keeps the cell a
4-tuple profile — no maximum, since `M6` showed no total order fits the measured signs. `R1.4` makes Annex A a
prerequisite. `R1.5` requires pinned declarations before any cell is scored.

`R2` and `R3` are opened as the two things that could ever narrow `R1.0`: an arrangement-sensitive statistic
(one that actually falls below threshold when the tiles are shuffled — the current tiers do not), and a `Q3`
taken in transmission on a 2D-ified scene.

## 4. `S9` — two scopes, and a guard that makes the coupling checkable

The ruling's distinction is now the rule's structure:

- **(a) locked scope** — a symbol is locked iff a document's own sha256 covers it. Here:
  `Q0`, `Q1`, `Q2`, `Q3` inside `threshold_lock.json`. Renaming is **not permitted** at any authority short of a
  v2 lock.
- **(b) unlocked scope** — everything else, explicitly including the `Q1`–`Q3` of `meff_boundary_probe` that
  collided with them. Renaming is **free**. This dissolves the deadlock recorded previously: a clean namespace no
  longer needs a v2 lock, because only the tier-side labels are frozen and the probe-side ones may move.
- **(c) the coupling** — an unlocked rename must not change the computation path of a locked quantity.

Clause (c) is now measured rather than asserted. `src/common/locked_path_guard.py` records `LOCKED-PATH` = the
pair *(digest of `src/route/structure_tiers.py`, digest of `runs/MATRIX/structure_tiers_results.txt`)*, and
admits exactly four verdicts:

| source | numbers | verdict | meaning |
| --- | --- | --- | --- |
| unchanged | unchanged | `OK` | nothing happened |
| moved | unchanged | `RENAME-ADMITTED` | the signature of a rename; re-baseline **with a note** |
| unchanged | moved | `DRIFT` | environment or dependency, not a rename |
| moved | moved | `BLOCK` (exit 1) | a locked quantity changed value → `S9`(a) needs a new lock |

All four were negative-tested on copies, and `BLOCK` returns exit 1. `RENAME-ADMITTED` is deliberately not a
free pass: re-baselining must be accompanied by a note, so a value change cannot be smuggled through in two
commits (rename now, adjust later).

## 5. The structural conflict this ruling walked into, and how it was resolved

The ruling asks for the prohibition to be added **in the spec**. The spec is covered by `spec_sha256` inside the
lock, and the executor refuses every tier on `(c)` when that digest does not match. Editing the spec would not
have narrowed the tiers — it would have **deleted** all four.

Resolution, stated so it can be challenged: the digest exists to prove one thing, that **the definitions and the
thresholds did not move after the data were seen**. Annex A does not move them, so it is placed **outside the
digest's protection** and declared part of v1 by reference, carrying its own digest
(`560acd8c…3fc07`) in a separate sidecar. The lock is byte-identical before and after (`5f324e15…bcc`).

The annex is bound by a self-limiting clause: **it may not contain a tier threshold** — verdict thresholds are
referred to by name only, and domain boundaries are the one numeric content it is allowed. The first draft of
this annex broke that clause in its own invariants list (it restated all four thresholds); that was caught and
removed before the digest was taken.

This is the fourth instance of the same class in this project (PNG cannot hold a text line → `P7`; JSON cannot
hold a comment → `P8`; a symbol inside a digest cannot be renamed → `S9`; a prohibition about a hashed
document cannot go inside that document → this). The pattern: **integrity mechanisms force normative text out of
the documents they protect**, and the honest move is a declared, separately-digested annex, not a quiet edit.

## 6. Corrections disclosed in this round

1. **`tier_admission_v1.md` §5 said `DITHER` clears the precondition at `0.119`. That number is not reproducible
   from any product.** The scene's contrast coefficient is `0.115878`, recomputed deterministically in this
   round. Corrected in place with a banner. The verdict is unaffected (`11.6×` the precondition, not `11.9×`),
   but a number that cannot be reproduced from a product is a defect of the same family as the earlier
   `9e20`/`9e14` and `√2`-span slips, and is recorded as the fourth.
2. **My mechanism for `T2` was wrong twice** (§2). Both are recorded in Annex A §A.3.
3. **Two of the twelve pre-registered predictions were satisfied by statistics that do not test the claim they
   were written for** (`P8` counted a raw-alphabet difference, while the claim was about the renormalised
   correction; `A1-P3` passed and my script's automatic summary drew the wrong inference from it, which is why
   the erratum is appended to the probe-2 results file). A prediction ledger that counts a technically-passing
   wrong statistic as support is how a wrong mechanism gets to live on, so both are marked as form-failures.

**Prediction ledger, honestly**: `3/9` in the main run, `1/3` in probe 2. After removing the two form-failures,
the run contributed **two clean confirmations** (`Q0` at full dither fails; `Q2` negative at high occupancy) and
**two refutations** (the alphabet account; the undersampling account) — and the refutations are what produced
the usable answer. A run that mostly failed its own predictions and still located both boundaries is the
expected shape here: the boundaries were unknown, which is why they were worth measuring.

## 7. What did not change

1. All four tier thresholds — unchanged; the lock digest is identical.
2. All four tiers remain **ADMITTED**. Admission asked whether a tier separates structure from null. It did not
   ask whether every pass is citable, and it never claimed to.
3. No new lock. The ruling's `no` was honoured literally.
4. `docs/specs/intrinsic_structure_tiers_v1.md` — untouched, digest still `c5e23917…a07d8`.
5. Earlier declines stand: no `v2` of the tier definitions was written, and none may be written without a new
   lock plus a pre-registration predating any sight of the data.

## 8. Still open

`GD6` (`ME3`'s `φ`) blocks Phase 3; `GD9` (route objective) is unsettled; the two crosswalk bookkeeping items;
26 of 27 frames still carry no display block and remain non-citable; `R2`/`R3` of the reading rules are reserved
and empty.

*Content generated by AI*
