# W2 conformance review v1 (cycles 74–79, §5.5 / Appendix C)

PROVENANCE: NEITHER

Programme authority: `docs/program/RESEARCH_PROGRAM_v1.md` v1.1.1 (sha256 `f634f8cb07f9…`).
Review date: 2026-11-26. Reviewer: executor, under the standing decision authority for this programme.
Scope: the six cycles appended at ledger rounds 74–79. This is a governance product; it establishes no physics
and does not edit any authority, lock, or archived product.

---

## 1. Cycle reviews (§5.5: one line, Appendix C variant by cycle type)

| round | cycle | type | Appendix C items | one-line verdict |
|---|---|---|---|---|
| 74 | `W2-DISC-01` | technical closure | 3–13 | **PASS** — δ×10 control closes; plate field byte-identical, conservation residual 0 |
| 75 | `W2-C2VIOL-01` | artifact | 1–6 | **PASS** — three keyframes + sequence, card and sidecars present, `NOT-APPLICABLE` at t0 stated |
| 76 | `W2-C3TEST-01` | technical closure | 3–13 | **PASS** — declared question answered; `n_e^(2/3)` scaling falsified and recorded (finding F1) |
| 77 | `W2-XCHECK-01` | technical closure | 3–13 | **DRIFT** — citation defect X4 in the stage-A check (finding F2); X1–X3 pass |
| 78 | `W2-RL1-01` | technical closure | 3–13 | **PASS** — `q(θ_fast)=1`, `Q3_fast=Q3_ideal`, profile matches W1-ROW2 |
| 79 | `W2-COUNT-01` | technical closure | 3–13 | **PASS** — five-element `M` contract and weighted count derivation close |

A failed pre-registered prediction is a scientific finding, not a governance drift: the closure question is
answered either way. Only X4, an over-specified check statement, is classified DRIFT.

## 2. Appendix C checklist by cycle type

`A` = artifact cycle (items 1–6), `T` = technical closure (items 3–13), `—` = item not applied to that type.

| # | item | DISC `T` | C2 `A` | C3 `T` | XCHK `T` | RL1 `T` | COUNT `T` |
|---|---|---|---|---|---|---|---|
| 1 | Frames published with card + sidecar | — | PASS | — | — | — | — |
| 2 | `t0`/`t_mid`/`t_end` coverage or gap stated | — | PASS | — | — | — | — |
| 3 | Inputs / derived outputs separated | PASS | PASS | PASS | PASS | PASS | PASS |
| 4 | Constraints HELD / VIOLATED / OUT-OF-DOMAIN with ground | PASS | PASS | PASS | PASS | PASS | PASS |
| 5 | Effective-2D label or `NOT-MEASURED` + missing slot | PASS | PASS | PASS | PASS | PASS | PASS |
| 6 | Manifest, solver spec, run record present | PASS | PASS | PASS | PASS | PASS | PASS |
| 7 | No derived quantity as goal | PASS | PASS | PASS | PASS | PASS | PASS |
| 8 | No constraint inflation | PASS | PASS | PASS | PASS | PASS | PASS |
| 9 | No scene/impossibility collapse | PASS | PASS | PASS | PASS | PASS | PASS |
| 10 | No unpriced violation | PASS | PASS | PASS | PASS | PASS | PASS |
| 11 | Matrix still 8 rows | PASS | PASS | PASS | PASS | PASS | PASS |
| 12 | Status vocabulary not collapsed | PASS | PASS | PASS | PASS | PASS | PASS |
| 13 | Closure question answered / recorded open | PASS | — | PASS | PASS | PASS | PASS |

Evidence notes for the non-trivial cells:

- **Item 1–2 (C2 artifact).** Four PNGs at `runs/W2-C2/`: `c2_t0.png`, `c2_t_mid.png`, `c2_t_end.png`,
  `c2_sequence.png`. Each has a `.display.txt` sidecar with one `DISPLAY-DECLARATION` block; checked manually
  because `display_lint.py` walks only existing sidecars. The `t0` row is `NOT-APPLICABLE` (no 2D output before
  the front arrives), which is the stated gap, not a missing frame.
- **Item 5.** Every cycle keeps effective-2D at `NOT-MEASURED` and names the missing slot (registered
  confining-potential model). No `IS_2D` / `LOOKS_2D` / visibility claim is made.
- **Item 10.** `C3` remains VIOLATED with an IMPORTED 3 ns transient and an explicit price/fingerprint slot kept
  separate from `sigma_s` (`NOT-MEASURED`) and `L_nu` (`OUT-OF-SCOPE`). `C2` violation in the artifact is a
  stipulated non-isometric pushforward with `det J = 1.0201` and a booked outflow, not an unpriced violation.
- **Item 11.** `runs/ANALYSIS/assumption_matrix_v1.txt` prints eight rows; `runs/MATRIX/matrix_audit_results.txt`
  line 23 reports `rows printed: 8`. No constraint was added and no version bump was required.
- **Item 13.** All five technical closures answer their declared question. `W2-C3TEST-01` answers it by falsifying
  its own prediction; `W2-XCHECK-01` answers it by locating a citation defect. Neither is left open.

## 3. Conformance review — the seven required answers (§5.5)

1. **Frames published this period and the O0 requirement each closes.** `W2-C2VIOL-01` publishes four frames.
   They close O0 minimum items 2 (three keyframes), 3 (declared profile slots and sidecars), 4 (constraint state
   and consequence on each frame), and 5 (R2 reproduction only, explicitly no frame reproduction). They do not
   claim publication acceptance: the original row-2 gaps on discretization and count derivation are closed by
   the separate technical cycles below.
2. **Cells moved `NOT-MEASURED` → verdict.** None in the assumption matrix. Instead five `TECHNICAL` closures are
   recorded, which §5.5 treats as a valid period outcome.
3. **Derived quantity used as a goal? No.** Slice/fragment counts, `d∥`, `Q3`, and area are reported as outputs
   with their derivation; none is promoted to the goal (item of drift #2).
4. **Model assumption promoted to a constraint? No.** The stretch `s = 1.01`, `δ×10`, and `q = 1` remain declared
   instrument settings; no new `C4`/`C5` was introduced (drift #1).
5. **Mechanism limitation written as a scene impossibility? No.** Effective 2D stays `NOT-MEASURED`; the missing
   potential model is named. No `¬C2 → U-1` or "column-invisible" collapse (drift #4).
6. **Claim without θ, tier, and provenance? No.** Every cycle declares its band/gate/distance/`E`/`G` slots, its
   tier level, and exactly one provenance declaration. The `Q3` result in `W2-RL1-01` is explicitly a channel
   contrast because the registered estimator has no angular variable (drift #9 avoided).
7. **Matrix still 8 rows? Yes** (evidence above; drift #7 avoided).

**Verdict: PASS.** Answers 3–7 are all "no", answer 1 is non-empty, and five `TECHNICAL` closures are recorded.
Two findings are carried forward with corrective actions below; neither changes the verdict because neither is a
prohibited move under §5.4.

## 4. Findings and corrective actions

### F1 — `W2-C3TEST-01` C2: falsified prediction (scientific finding, no governance correction)

The pre-registered `n_e^(2/3)` scaling of `mu_kin` did not hold across the registered beta-equilibrium
conventions. The result is recorded in `runs/W2-C3/c3_results_v1.txt`; no threshold or convention was re-priced
and the held/neutronized states remain separate.

- **Corrective action:** none to the archived product. Any future test of the scaling must be registered as a
  new convention with its own prediction; no retro-active substitution of the old stand-in result.
- **Date:** 2026-11-26. **Status:** recorded, closed.

### F2 — `W2-XCHECK-01` X4: citation defect (DRIFT, D1 wording class)

Stage A asked `docs/program/COMPLETION_PROTOCOL_v1.md` to contain a report-only / exit-code statement. The
programme does not cite such protocol text; the check was over-specified. X1–X3 confirm the clauses that are
actually cited (crosswalk identifiers, tier thresholds, ladder rungs).

- **Corrective action (erratum E1, recorded here):** the X4 check is narrowed to what the programme actually
  cites — the protocol cross-check is a structural read, and any report-only status belongs to the instrument,
  not to protocol wording. Future cross-check registrations MUST NOT assert protocol text the programme does
  not cite. No authority, lock, or archived product is edited; the stage-A registration is hash-locked and is
  therefore left intact.
- **Date:** 2026-11-26. **Status:** recorded, closed.

## 5. Sign-off

Signed by the executor under the standing decision authority for this programme. No governor block was filled,
no authority was amended, and no gate mark was changed. Report-only instruments were re-run and their stdout is
archived at `runs/W2-AUDIT/instrument_stdout_v1.txt`; all eight returned exit code 0.
