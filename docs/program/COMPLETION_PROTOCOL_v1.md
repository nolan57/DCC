# Programme completion protocol v1 — intermediate audit, iteration, interaction

**Date**: 2026-11-23, after round 45 (`runs/R1B/r1b1_p4_p5_closure_v1.md`)
**Status**: **OPERATING PROTOCOL** — this document governs *how* rounds are run, audited and handed to
the governor. It governs no physics, changes no threshold, and licenses no conclusion. Where it and a
ratified decision disagree, the decision wins.
**Why it exists**: the record is 45 rounds deep and its discipline is real but *tacit* — it lives in
forty self-caught defects (`reports/DCC_research_progress_v1.md` §9) and in the habits of whoever ran the
last round. A discipline that exists only in habits does not survive a change of executor, a long gap,
or a single rushed round. This file makes it explicit, and §4 makes most of it executable.

**Labels used here** — `RP-A*` (audit checkpoints), `RQ-*` (queue items), `PG-*` (governor gates),
`BN-*` (board notes). All
carry a ≥2-letter prefix per registry rule `R3`; none collides with an existing label (checked against
`docs/conventions/symbol_registry.md`).

---

## §0 What "complete" means — the programme's definition of done

The programme does not complete by producing a positive result. It completes by becoming
**decision-complete**: every line terminal, nothing pending adjudication, nothing citable that is not
traceable. Eight conditions, six of them machine-checked by `src/common/program_audit.py`:

| # | condition | check | kind |
|---|---|---|---|
| **D1** | zero unmarked governor blocks — no document is `PROPOSED` with an empty mark | `PG-*` count = 0 | machine |
| **D2** | zero lock-integrity violations — every `.sha256` verifies, every `*lock*.json` has its sidecar | hard | machine |
| **D3** | zero broken product citations — every `runs/…` path named in `docs/` exists | hard | machine |
| **D4** | every item that reaches a closed state carries a round-ledger record | ledger | machine |
| **D5** | zero round-ledger breaks (hash chain intact) | ledger | machine |
| **D6** | every queue item is terminal: `CLOSED-*`, `RETIRED-*`, or `BLOCKED-ON-INPUT` | queue | machine |
| **D7** | every `BLOCKED-ON-INPUT` names the missing physics by file and quantity — never "more work needed" | queue | manual |
| **D8** | the terminal answer exists: one paragraph stating what DCC is, is not, and what would reopen it | report | manual |

**Amended 2026-11-23 by `docs/decisions/relaxation_frame_v1.md`**: "complete" now means *the ladder is
terminated* — either a rung reaches the goal with its price printed, or every rung is priced and the total
exceeds budget. `D8`'s terminal answer therefore has a fixed form: the rung, its `V`, its `Φ`, its
fingerprint, and the reverse-on. Nothing else in this section changes.

**The one-sentence target.** Every line ends in one of four states — *closed constructive*, *closed
NO-GO*, *retired as identity*, *blocked on named physics* — and no line ends in "in progress".
`BLOCKED-ON-INPUT` is a terminal state, not a failure: it is the same class as `G0′` row 1, and the
record already says so (`reports/DCC_research_progress_v1.md` §11, last bullet).

---

## §1 Mid-course audit (intermediate audit) — three checkpoints, one object

The unit of audit is not the document and not the round; it is the **round tuple**:

```
RQ-nn | question (one sentence) | prediction (number + kill condition)
      | registration digest | in-force locks | product path | verdict | defect class | next
```

A round that cannot fill this tuple is not a round; it is reading. Reading is allowed and unlogged.

### §1.1 `RP-A1` — pre-registration audit (before any code exists)

Run *before* the script is written. Seven checks; each one exists because it has already caught
something in this record.

| # | check | pass condition | catches class |
|---|---|---|---|
| `RP-A1.1` | one question, one sentence | the question has a single noun it is about | wrong-problem attribution (`REPAIR-ABSENT`) |
| `RP-A1.2` | the prediction is a **number**, not a direction | e.g. "`1.18e10`, fail if `< 1e9`", not "should be large" | figure-before-constraint |
| `RP-A1.3` | kill condition stated | the exact measurement that would refute it, in the same units | tautology-as-test |
| `RP-A1.4` | every threshold has a **measured floor** first | the quadrature/instrument floor is quoted from a prior product | threshold-before-calibration (5 instances) |
| `RP-A1.5` | one negative control that must fail by a known factor | a deleted wrong formula re-registered as a required failure | fabricated evidence |
| `RP-A1.6` | product path + provenance tag declared now | `runs/<DIR>/<name>_results.txt`, tag chosen (`CHAIN-EVIDENCE` / `BOUNDARY-INPUT` / `NEITHER`) | untraceable number |
| `RP-A1.7` | no forbidden citation | not `S9` (visibility), not `D-2` (deposit frame as readability), not `440 MeV` as input, not a scanned `τ` as response | prohibition breach |

Then hash-lock the registration if it carries a threshold (`threshold_lock.json` pattern). **A1 is the
only checkpoint that cannot be repaired later** — everything downstream can be appended as erratum; a
prediction written after the run cannot.

### §1.2 `RP-A2` — landing audit (after the run, before any prose)

Six checks, run against the *product file*, cold, before writing a single sentence of interpretation.

| # | check | pass condition | catches class |
|---|---|---|---|
| `RP-A2.1` | the run is unedited | stdout appended, never rewritten; a crashed run is kept | silent repair |
| `RP-A2.2` | every number quoted carries `file:line` | no paraphrase across ledgers | number from wrong measurement |
| `RP-A2.3` | every FAIL stays in the product | `FAIL` printed where it happened, counted in the verdict line | selective reporting |
| `RP-A2.4` | `IDENT` separated from `CHECK` | the ledger reads `CHECK n/n · IDENT m/m (not evidence) · NEGCTRL k/k` | identities counted as evidence |
| `RP-A2.5` | the instrument's floor is printed | the branch that *cannot* be distinguished is shown, not implied | tautology-as-test |
| `RP-A2.6` | the verdict is one of the four terminal classes | see §2.3 | "in progress" as an outcome |

### §1.3 `RP-A3` — acceptance audit (before the decision document is written)

Five checks on the *record*, not the physics.

| # | check | pass condition |
|---|---|---|
| `RP-A3.1` | registration predates product | recorded in the round ledger (see §4.3 — `mtime` is **not** evidence; the 2026-11-21 bulk copy destroyed it) |
| `RP-A3.2` | locks intact | `program_audit.py --check-locks` returns 0 |
| `RP-A3.3` | citations resolve | `program_audit.py --check-citations` returns 0 |
| `RP-A3.4` | the decision document says what it does **not** decide | one explicit section; every accepted decision carries a *reverse-on* clause |
| `RP-A3.5` | supersession is declared, not implied | if it replaces a rule, the old rule is named and its orphans listed |

### §1.4 Audit independence, honestly stated

There is one executor and it is also the auditor. Pretending otherwise would be the exact defect this
protocol exists to prevent. Three substitutes are in force, and none of them is as good as a second
reader — that is recorded rather than hidden:

1. **Temporal independence** — `RP-A1` locks the prediction before the instrument exists. The audit
   cannot be retrofitted to the answer because the answer was not known when the audit was written.
2. **Cold re-read** — `RP-A2` is performed on the raw product before any prose exists. The question
   asked is not "does this support my claim" but "what would have to be true for this number to be
   an artefact", and the answer must name a measurable test.
3. **Adversarial sweep every five rounds** — re-read the last five rounds looking only for the ten
   defect classes of §9. Output is a defect list or `none found` **plus the weakest link named**. A
   sweep that finds nothing and names no weak link has failed.

---

## §2 Sustained iteration (continuous iteration) — the round queue

### §2.1 States

```
QUEUED → REGISTERED → EXECUTED → AUDITED → {CLOSED-CONSTRUCTIVE | CLOSED-NO-GO | RETIRED-IDENTITY}
                                        ↘ BLOCKED-ON-INPUT      (terminal, names the missing physics)
                                        ↘ BLOCKED-ON-GOVERNOR   (terminal until a mark; see §3)
FROZEN  — closed by a ratified decision; reopens only through that decision's reverse-on clause
```

`WIP = 1`. One item may be `REGISTERED` or `EXECUTED` at a time. Parallelism here does not buy speed —
every parallel round so far has produced at least one cross-contamination defect.

### §2.2 The item contract

An item enters the queue with: `id`, `title`, `question`, `source` (file §), `product` (path), `DoD`
(what the product must contain), `terminal` (which of the four terminal classes are admissible), and
`blocked_by` (ids, or a governor gate). Nothing else. An item with no `DoD` cannot be executed, only
discussed.

### §2.3 Terminal classes — the only four ways a line ends

| class | meaning | example in record |
|---|---|---|
| `CLOSED-CONSTRUCTIVE` | a thing exists that did not | `deposit_serial_v1` `A1`–`A7`; four tiers admitted 4/4 |
| `CLOSED-NO-GO` | refused by a theorem or a measured impossibility | `DEPOSIT-BLIND`; `C3` in-action |
| `RETIRED-IDENTITY` | the question dissolved — the quantity was an identity, not a bound | `440.18 MeV`; `Λ_max`; `δ_ov` |
| `BLOCKED-ON-INPUT` | a named physical object does not yet exist; the missing item is cited | `R1-B1` before round 45 |

"No progress" is not a class. If a round ends there, the round failed `RP-A1.2` and is logged as a
defect, not as an outcome.

### §2.4 Three standing prohibitions on iteration

1. **Never introduce a threshold and evaluate it in the same round.** The threshold round and the
   evaluation round are different rounds, with a lock between them.
2. **Never let a downstream success choose an upstream branch.** No backward selection (matter branch
   chosen because the optics then look good), no forward selection (criterion relaxed because a
   candidate is close). Both are in force from `surface_conductivity_v1.md` §7.5, §11.
3. **Never re-open a line to rescue it.** A line reopens only through its own *reverse-on* clause.

### §2.5 Budget and rollover

Closure budget: **12 rounds** from round 45. Checkpoints at rounds 49, 53, 57 — at each checkpoint the
queue is re-priced: any item not `AUDITED` converts to `BLOCKED-ON-INPUT` with the missing physics
named, or is dropped with a one-line reason. A budget that is not enforced is a wish; the checkpoints
are the enforcement.

If an item is still `QUEUED` at round 57, it does not roll over silently — it is written into the
terminal answer of §0 `D8` as *not attempted, and why*.

---

## §3 Interaction surface (interaction) — five surfaces, one character

The governor's time is the scarcest resource in this programme and the record spends it badly: a
decision currently arrives as 200 lines of audit with a checkbox buried in §4. Five surfaces replace
that.

### §3.1 Surface 1 — the one-character mark

Every gate is a block of the form

```
[ ] Ratify as written
[ ] Ratify with amendments
[ ] Return for revision
```

and the executor **never** fills it (`exhaustive_matrix_route_v1.md` §4 states the rule; the executor
honouring it is what made the audit citable at all). Approval = changing one `[ ]` to `[x]`, in place,
in the authoritative file. No new file, no separate channel, no inference from silence. **An unmarked
block is not authority, forever** — not "implicitly approved", not "probably fine".

For decisions the record never anticipated a block for (`BN-*`, §5), the equivalent is **one sentence
that names the note id** — `BN-04: amend` or `BN-01: leave as written`. Naming the id is what makes the
decision citable; an unnamed "ok" is not recorded as anything.

### §3.2 Surface 2 — the six-line digest

Generated, not written by hand (`program_audit.py --digest` → `runs/PROGRAM/governor_digest.txt`), one
block per open gate, each block exactly six lines:

```
PG-01  G6/DC2 status flip            [source: runs/R1B/r1b1_p4_p5_closure_v1.md §3]
  ask    : NO-GO → CONDITIONAL-ADMISSIBLE at model level?
  basis  : candidate σ_s derived from solved states; S7 conditional, f_intra = 1.52e-3
  cost   : optics line stops at P5; G3′/G4/G5′ cannot be graded
  mark   : docs/decisions/exhaustive_matrix_route_v1.md:240  (one character)
  if no  : stays NO-GO; no other line is blocked by this refusal
```

The governor reads six lines per gate and one character per gate. Detail stays in the record and is
read only on request.

### §3.3 Surface 3 — the five interrupt triggers

The executor stops and asks **only** when one of these is true. Everything else proceeds under the
standing delegation.

| # | trigger | why it cannot be delegated |
|---|---|---|
| `I1` | the action would change a hash-locked artifact or a locked threshold | the lock's whole purpose is that it cannot move |
| `I2` | the finding contradicts a **ratified** decision | requires revoking authority, which is the governor's |
| `I3` | a line would be declared terminal (`CLOSED-*`, `NO-GO`) | terminal classes are conclusions of the record |
| `I4` | two clauses of the record conflict and both are load-bearing | §III vs §VI of the matrix route is the type case; the audit says which physics permits, the governor says which governs |
| `I5` | two admissible models remain with no measured discriminator | a choice of physics by preference is not a measurement |

### §3.4 Surface 4 — the delegation envelope

**The executor decides alone**: which round runs next, how an instrument is built, what a defect class
is, when a theorem retires a line, how an audit is worded, which erratum is appended, and every
`BLOCKED-ON-INPUT` attribution.

**The executor never decides**: an approval mark, a terminal class for a governor-owned line, a
threshold move, a reversal of a ratified decision, the wording of a visibility conclusion (`S9`), or
"which physics is true".

### §3.5 Surface 5 — the ask format

When `I1`–`I5` fires, the ask is one block, never a discussion: **decision**, **basis** (file §),
**cost of not deciding**, **recommendation with its reverse-on clause**, **the mark location**. If the
governor says nothing, the recommended path is *not* taken; the block stays open and the queue item
converts to `BLOCKED-ON-GOVERNOR`.

---

## §4 The instruments

### §4.1 Files

| path | role |
|---|---|
| `docs/program/COMPLETION_PROTOCOL_v1.md` | this protocol |
| `docs/program/round_queue_v1.json` | the queue: items, states, blockers, DoD, terminal classes |
| `src/common/program_audit.py` | the auditor: lock, citation, authority, queue, ledger, DoD |
| `runs/PROGRAM/program_audit_results.txt` | its product (generated) |
| `runs/PROGRAM/governor_digest.txt` | the six-line digest (generated) |
| `runs/PROGRAM/round_ledger.jsonl` | append-only, hash-chained round records |

### §4.2 Commands

```
python src/common/program_audit.py              # board + DoD, stdout only
python src/common/program_audit.py --write      # also write the two products under runs/PROGRAM/
python src/common/program_audit.py --check-locks      # exit 1 on any digest mismatch
python src/common/program_audit.py --check-citations  # exit 1 on any unresolvable runs/ path
```

### §4.3 The round ledger, and why `mtime` is not evidence

`program_audit.py`'s ordering check is **advisory**, and says so: the 2026-11-21 bulk copy reset
timestamps across dozens of files, so `registration.mtime < product.mtime` is true for some rounds and
false for others *for reasons unrelated to execution order*. A check that cannot distinguish "the
registration was written after the run" from "the file was copied" must not be a gate.

The durable instrument is `runs/PROGRAM/round_ledger.jsonl`: one record per completed round,

```json
{"round": 46, "id": "RQ-03", "registration_sha256": "...", "product_sha256": "...",
 "verdict": "CLOSED-CONSTRUCTIVE", "prev": "<sha256 of previous record>", "utc": "..."}
```

Hash-chained, so a later edit to any past record breaks every subsequent link (`D5`). From round 46
forward this — not `mtime` — is the ordering proof.

### §4.4 What the instruments cannot do

They cannot tell whether a number is *right*; they can only tell whether it is *traceable*. Every
physics verdict stays with `RP-A2` and the adversarial sweep. A green board with an unaudited round is
worse than a red board, because it looks finished.

---

## §5 The board at round 45 (what is actually pending)

| item | state | source |
|---|---|---|
| `PG-01` `G6`/`DC2` status flip → `CONDITIONAL-ADMISSIBLE` | **AWAITING-GOVERNOR** | `runs/R1B/r1b1_p4_p5_closure_v1.md` §3 |
| `PG-02` matrix route §4 approval block (3 lines, none marked) | **AWAITING-GOVERNOR** | `docs/decisions/exhaustive_matrix_route_v1.md` §4 |
| the four matrix tiers, intrinsic form | **CLOSED-CONSTRUCTIVE** 4/4 | `docs/decisions/tier_admission_v1.md` |
| readable-image line | **FROZEN** (`D-1`, `D-4`); reverse-on = a per-site measured quantity | `docs/decisions/route_terminus_v1.md` §9 |
| `R1B1-P2/P3/P4` | **CLOSED 9/9, 6/6, admissible** | `runs/R1B/r1b1_p{2,3,4}_*` |
| `G3′`, `G4`, `G5′` | `BLOCKED-ON-INPUT`, chain-blocked behind `PG-01` | `reports/DCC_research_progress_v1.md` §4 |
| the nine queued refinements | `QUEUED` / `BLOCKED-ON-GOVERNOR` | `docs/program/round_queue_v1.json` |

**Two characters stand between the programme and `D1 = 0`.** Neither of them is mine to type.

Two further items are decisions the executor may **not** take, and neither has a block on disk — because
the record never anticipated them:

| note | decision | why it is not a gate |
|---|---|---|
| `BN-01` | re-grade `G2′` against `R1B1-P2`'s 9/9 solved states: the gate table still reads `NOT PASSED` | a terminal class (`I3`), not a checkbox; one sentence naming `BN-01` is enough and the ledger records it |
| `BN-04` | the commit gate has been **red since round 41**: `provenance_lint` blocking `= 12`, all of them rounds 41–45 products with no `PROVENANCE` line | an `I4` conflict — `s9.1` forbids editing archived stdout and no sidecar rule exists for text products; the repair is a convention amendment |

`BN-04` is the finding that most justifies this document's existence: an invariant written into a ratified
route (`phased_relaxation_route_v2` §5, invariant 3) has been violated for five consecutive rounds, and
nothing in the record noticed, because the gate is run by hand and the hand stopped running it. From
round 46 the audit is what runs it.

---

## §6 What this document does not decide

It decides nothing about DCC. It does not declare a round complete, does not convert a
`BLOCKED-ON-GOVERNOR` into a `CLOSED`, and does not weaken any prohibition in §8 of the progress
report. It is a container for the existing discipline, made explicit so that it survives the next
executor — including the possibility that the next executor is the same one, tired, at round 60.

*Content generated by AI*
