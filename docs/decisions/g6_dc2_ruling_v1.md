# `G6`/`DC2` — status ruling v1 (PROPOSED)

**Date**: 2026-11-23 (round 45 close)
**Status**: **PROPOSED — submitted for adjudication, NOT ratified.** Until a line in §4 is marked, `G6`/`DC2`
reads **NO-GO**, and this document may not be cited as authority.
**Substance**: not new. Everything below exists in `runs/R1B/r1b1_p4_p5_closure_v1.md` §1–§3 and
`runs/R1B/r1b1_p4_response_results.txt`. This document exists for two reasons only: the flip needs a
citable home outside a run product, and it needs a mark.
**Registered by**: AI executor at round 45's close, under the round-44 veto-lift instruction.

---

## §1 What is submitted

| | before round 45 | submitted now |
|---|---|---|
| verdict | `G6`/`DC2` **NO-GO** | **CONDITIONAL-ADMISSIBLE at the model level** |
| ground | "no compliant `σ_s(ω)` exists; the object is absent" | a candidate exists and satisfies the locked criteria at the ideal level |
| `S1`–`S15` | unapplied (no object) | applied; `S7` **CONDITIONAL**, `S9` in force |
| the state it is built from | assumed | solved (`R1B1-P2` 9/9, `R1B1-P3` 6/6) |

The four interface inputs the specification demanded (`surface_conductivity_v1.md` §7.6) are **derived**,
not fitted — the first time in the programme that the tuple is not assumed:

| input | value | status |
|---|---|---|
| `n_2D = n_free,2D` | `1.111 / 1.008 / 0.927 ×10⁻³ fm⁻²` at `L_z = 1.68/1.84/1.99 fm` | DERIVED (`N7-SPLIT`: 4.2–5.0% of the bookkeeping `n_Q,2D`) |
| `g` | `2` | DERIVED |
| `v_F` | `0.0316 / 0.0330 / 0.0342 c` | DERIVED (`ħk_F/m_eff`); resolves `V-F-IMPLIED` |
| `ω_end` | `5.61 / 5.12 / 4.73 ×10²³ rad/s` | DERIVED from the band structure; **not** the withdrawn `440.18 MeV` identity |

and the quantity the optics criteria were measured to be blind to is supplied by the matter model:
`f_intra = 1.52×10⁻³`, with the TRK deficit `1 − f_intra − Σf_1n = 0.9975` quantified as the
UV-compensation bucket.

**What did not change.** The criteria. `S1`–`S9` are byte-identical across v1.0→v1.3 and remain locked by
the v1.0 digest. The flip is not a relaxation of the specification; it is the arrival of an object.

## §2 What a mark would license, and what it would not

**Would**: `G6`/`DC2` reads `CONDITIONAL-ADMISSIBLE`; `RQ-09`'s observer parameters become settable rather
than free; `G3′`/`G4`/`G5′` acquire an optics target to be graded against.

**Would not** — each of these is a prohibition already in force, and none is lifted by a mark:

- **No visibility, transparency, opacity or "mirror-like" statement.** `S9` forbids it and `S9` is
  untouched. A conditional admissibility is a statement about a *criterion*, not about a *scene*.
- No claim beyond the ideal level: `τ = ∞` at the declared level, `S7` conditional.
- No change to `G0′`, `G1`, or any frozen constant.
- No grading of `G3′`, `G4`, `G5′` — this gate does not move them; their own blockers stand.
- No lifting of the prohibitions on `440 MeV` as an input or on scanning `τ` as a response.

## §3 What is not in evidence, and one defect recorded

Four refinements are named, not hidden (`r1b1_p4_p5_closure_v1.md` §3). Each would move a number; none
would move the verdict class:

| refinement | what it would change |
|---|---|
| (i) finite `τ` from e–p impurity scattering | `S7` from CONDITIONAL to PASS; the Drude width |
| (ii) exact Dirac-box `z`-ladder | the `0.9975` deficit, i.e. the partition tail |
| (iii) interaction-level census | `n_free,2D`, hence `f_intra` |
| (iv) the `L_z`-resolved family surface | the input range handed to `R1-B4`/`R3` |

**Defect, recorded and not repaired** (`RP-A2.4`, count-not-infer): §2's enumeration names fourteen of
the fifteen criteria — `S12a/b` share one entry, and **`S2` is the one not named**. `S2` *is* addressed in
the product (`r1b1_p4_response_results.txt:60`, collisionless budget `A = 0` off the ladder lines), so the
gap is in the closure document's list, not in the application. The list is not edited; this note stands
beside it. Consequence for a reader: "all criteria applied" above means *applied*, not *enumerated*.

## §4 Approval block (governor, not executor)

```
[ ] Ratify — G6/DC2 reads CONDITIONAL-ADMISSIBLE at the model level
[x] Ratify with conditions            (state them; they bind the four refinements, not the criteria)
[ ] Hold at NO-GO                     (the candidate is ideal-level; the gate waits for (i)-(iv))
```

Marking one line is the entire interaction. Until then this is a proposal.

## §5 What would reverse it

1. A demonstration that the candidate violates any of `S1`–`S15` at the level claimed — not that it would
   fail at a level it does not claim.
2. A demonstration that the state it is built from is not a solution of `P2` (e.g. a `P2` check found to
   be an identity rather than a state construction).
3. A ruling that `S7`'s conditionality is disqualifying rather than deferring. That is a reading of the
   specification, and it is the governor's, not the executor's.

## §6 What this document does not decide

It does not decide whether DCC is true. It does not decide whether a real object at the endpoint is
visible, transparent or reflective — `S9` reserves that, and the reservation is not a formality: the
matter state is ideal-level and the response is collisionless. It does not re-grade `G2′`; the gate table
in `reports/DCC_research_progress_v1.md` §4 still reads `NOT PASSED`, and the disagreement between that
row and `R1B1-P2`'s 9/9 is registered as `BN-01`, not resolved here.

*Content generated by AI*

---

## §7 Governor mark — 2026-11-23 (`PG-01`)

**Instruction** (governor, 2026-11-23, verbatim): *"1. PG-01 / PG-02 / PG-03: mark immediately"* — "mark
`PG-01`/`PG-02`/`PG-03` immediately."

**Line marked**: §4 line 2, `Ratify with conditions`. The executor marked that line under the instruction, on
the line this document's own recommendation names. The other two lines are left unmarked, so the record shows
a choice rather than an assent to all three. The italic status line in the header still reads `PROPOSED`; it
is left byte-identical (`s9.1`) and is **superseded by this section.**

**The conditions, stated** — these are §3's four refinements, promoted from *named* to *binding*:

| # | condition | what must be produced | what it may move |
|---|---|---|---|
| (i) | finite `τ` from e–p impurity scattering | a `τ` with mechanism and matrix elements — `RQ-03` | `S7` from CONDITIONAL to PASS |
| (ii) | exact Dirac-box `z`-ladder | `f_1n` at exact box boundary conditions — `RQ-04` | the `0.9975` deficit |
| (iii) | interaction-level census | `n_free,2D` as an interval, never a point — `RQ-05` | `f_intra` |
| (iv) | `L_z`-resolved family surface | five `L_z` values with per-cell provenance — `RQ-06` | the input range handed to `R1B4`/`R3` |

Binding means: any downstream document citing `G6`/`DC2` as `CONDITIONAL-ADMISSIBLE` **must name which of
(i)–(iv) it is carrying unresolved.** A citation that quotes the flip without them is reading this mark as a
promotion, and it is not one — the flip is to *admissible subject to four open refinements*, which is what
§1's table already said and what the plain `Ratify` line would have hidden.

**What the mark buys** — §2's "Would" list and nothing more: `RQ-09`'s four observer parameters become
settable (they are now the gate's own conditions rather than free numbers), and `G3′`/`G4`/`G5′` acquire an
optics target to be graded against. In queue terms: `RQ-01` closes, `RQ-09` unblocks.

**What it does not buy** — §2's "Would not" list, unchanged and now load-bearing: `S9` untouched, so no
visibility, transparency, opacity or "mirror-like" statement follows; nothing beyond the ideal level (`τ = ∞`
at the declared level, `S7` conditional); no change to `G0′`, `G1` or any frozen constant; no grading of
`G3′`/`G4`/`G5′`; the prohibitions on `440 MeV` as an input and on scanning `τ` as a response stand. §3's
defect is **not** repaired by the mark — a ratification is not a correction, and "all criteria applied" still
means *applied*, not *enumerated*.

**Reverse-on** (§5) is unchanged. A mark is one character; the three clauses of §5, not a change of mind,
are what would move it.
