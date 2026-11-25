# Governor reading — matrix v2 is a product, not a route

**Status**: **GOVERNOR READING**, recorded 2026-11-23 (round 52). It is not a proposal and it carries no
approval block; §5 argues why giving it one would create a second locus of authority rather than a stronger
record.
**Instruction (verbatim)**: "read matrix v2 as a 'product' rather than a 'route', and do not write an approval block for it"
**Discharges**: board note `BN-13` (`docs/program/round_queue_v1.json`).
**Subject**: `docs/specs/matrix_v2_spec_v1.md`, `src/route/matrix_v2.py`, `src/route/matrix_v2r.py`,
`runs/MATRIX2/matrix_v2_results.txt`, `runs/MATRIX2/matrix_v2r_results.txt`.

---

## 1. The reading, in one sentence

Matrix v2 and its two programs are **products of rounds 46–47** — a reconstruction, a rank count, and a set of
measurements — not a governing route; **no approval block is owed for them, and none is to be added.**

---

## 2. Why an approval block is not owed — two tests, both negative

A block asks a governor to decide *what may be built next*. Two tests decide whether that question is live.

**Test (a): is a build decision waiting on it?** No. After `PG-02` returned the 8×4 route, the successor's job
was already discharged — `PG-03` selected **Path A**, which governs the *route* (the relaxation frame and the
ladder's execution order). The matrix's numbers now enter decisions only as **prices inside the ladder's rung
table**, and that table is already ratified. There is nothing downstream that a mark on the spec would unblock.

**Test (b): is this the only document where the question is asked?** No. The same content is asked and answered
normatively at `docs/specs/relaxation_ladder_v1.md` §4 as a price table. The matrix spec's contribution is a
*count* (224 nominal → 26 canonical, 8.6:1) and a set of measurements, not a rule about what may proceed.

Both negative ⇒ the document is a product. The asymmetry is worth naming, because it is the whole reason the two
documents are typed differently:

| document | normative content | governed by | type |
| --- | --- | --- | --- |
| `relaxation_ladder_v1.md` | which rung may be bought, in what order | `relaxation_frame_v1.md` §9 — **marked** (`PG-03`) | route |
| `matrix_v2_spec_v1.md` | what the 8×4 computes, at what rank, at what price | `exhaustive_matrix_route_v1.md` — **RETURNED** (`PG-02`) | product |

---

## 3. What BN-13 actually feared, and why a block would not have cured it

`BN-13`'s finding was: *a measured matrix and no governing one.* The hazard is real, but it is not "a document
without a checkbox". It is **a document that governs by being cited while nobody has marked it.** A second
checkbox would not fix that; it would institutionalise it, because the same decision (`PG-03`'s) would then have
two addresses, and where two boxes can answer one question the record loses the property that authority has
exactly one address.

What cures it is a **citation rule**, and that is §4. The reading is therefore not a waiver: it removes a mark
and adds an obligation.

---

## 4. Citation rule (the guard that makes the reading safe)

1. A product **may** be cited as evidence for a proposition — "`R5` passes 0/4", "26 canonical cells", "8.6:1".
2. A product **may not** be cited as authority for a decision — "therefore the route is viable" is not derivable
   from a product. Authority to proceed lives only in a decision document with a marked line.
3. Where a product's numbers do enter a decision, that decision must name them as **prices, not reasons**. Today
   there is exactly one such place (`relaxation_ladder_v1.md` §4) and exactly one such decision (`PG-03`).
4. **Silence from a product is not permission.** This is the same rule as `theta_camera_v1.md` §3: silence
   resolves to the weaker claim, and where no weaker claim exists silence resolves to nothing. An unmarked
   document cannot be read as approved; a product cannot discharge a governance question by not having a block.

Consequence for `BN-13`: the note closes not because the gap was filled but because the gap is **retyped** — there
was never a route to mark, and the route that does govern is marked at `PG-03`.

---

## 5. Why this document itself has no approval block (and why that is not the same loophole)

The instruction is already given, already binding, and already recorded in two places (this file and `BN-13`'s
closure). A block here would ask the governor to decide a second time what they decided once, and would let a
later reader believe the reading was provisional while it was in force.

The check on this document is mechanical instead of procedural: it must be cited by `BN-13`'s closure **and**
entered in `runs/PROGRAM/round_ledger.jsonl` (round 52). If either is missing, this file is a draft and nothing
in it binds.

---

## 6. What changes, and what does not

**Does not change — no number, no verdict, no price:**

- 26 canonical cells, 11 with content, 8.6:1; `G1`–`G5` all confirmed.
- `R5` passes 0/4 (its four earlier passes were borrowed `TILED` values); the headline stays withdrawn.
- Registration errata `E1` (8 vs 9 content cells) and `E2` (plate-array identities) stand as written.
- The 8×4's own verdict — **NOT VIABLE AS WRITTEN** — stands. Product status does not rehabilitate the instrument.

**Does change — one sentence in the spec's header is now discharged in the negative.** It reads *"may not be
cited as authority until a governor ruling exists."* A ruling now exists, and it declines the authority the
sentence anticipated. The condition is met; the expectation is not. §11 of the spec records this, and nothing in
the spec's body is edited (`s9.1`).

**Does not buy:**

- That the numbers are correct. A product's numbers are exactly as good as their pre-registration and provenance,
  which is what `P1`–`P9` police — not what a mark would police.
- That `RQ-02` is closed. The disposition note still owes the 32-cell `VOID`/`UNREALIZED` table; that debt is
  about the *returned* route and is untouched by this reading.
- That no route governs. One does: the frame, marked at `PG-03`. What does not exist is a **matrix** route.

---

## 7. Reversal, and its price

**Reverse on**: a governor instruction to ratify the successor as a governing route. **Consequence**: a block is
written *at that time*, with that date, and the numbers enter decisions from that date forward — never
retroactively, so no citation made under this reading is legitimised by the reversal. The reversal is one
sentence and costs nothing but the sentence; that cheapness is deliberate, because a reading that is expensive to
reverse would be a decision in disguise.

---

*Content generated by AI*
