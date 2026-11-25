# Relaxation frame v1 — the project pays in physics, not in truth

**Date**: 2026-11-23
**Status**: **RATIFIED BY GOVERNOR INSTRUCTION.** Not a proposal. The instruction is quoted verbatim in §1
and every consequence below is an execution of it, not an interpretation of it.
**Instruction** (governor, 2026-11-23): *"this is not a strict physics research project, but a project that progressively relaxes physical strictness constraints to achieve the goal"*
— "this is not a strict physics research project, but a project that progressively relaxes physical
strictness to achieve the goal."
**Scope**: this re-frames the *objective*, not the measurements. It changes no number in `docs/`,
no threshold in any lock file, and retires no verdict. Every negative result in the record stays exactly
as measured; what changes is what those results are *for*.

---

## §1 What changed, in one sentence

The programme stops asking *"is this scene physically real?"* and starts asking *"what does this scene
cost?"* — where the cost is paid in declared, priced relaxations, and the goal is fixed in advance.

**What did not change.** `G0′` row 1 (ordinary matter at fixed area: NO-GO). `C3` in-action NO-GO.
`DEPOSIT-BLIND` (`I(canvas ; r₄) = 0`). The deposit dichotomy (`2¹⁴` gap). The four admitted tiers and
their locked thresholds. `S1`–`S15`. The defect ledger. **None of these is softened by this document**;
each one is now a *rung-0 fact* (§5), which is a promotion in status, not a demotion.

## §2 Why this dissolves the deadlock: the fixed variable was in the wrong place

The record spent thirty-two rounds relaxing *physics* while holding *the observer* fixed at "naked eye,
0.1 s integration, 1.65–3.26 eV". Every null result it obtained is conditional on that observer, and
three of them say so explicitly:

- `visualization_null_result_v1.md` §2.3 — "the lifetime is shorter than the light-traversal timescale",
  computed against **the eye's sampling**, not against any law. A 3 ns event is perfectly imageable by a
  ps-gated detector; it is not imageable by a 100 ms retina.
- `docs/specs/intrinsic_structure_tiers_v1.md` §5 — `q = 1` **for a declared instrumented channel**,
  `q = 0` for the naked-eye reflected channel. The spec already provides both branches.
- `matrix_reading_rules_v1.md` `MR1.3` — `L3` is empty because `q = 0` *exactly*, and "the transmission
  channel has never been evaluated on a scene that carries the 2D-ified content."

So `L3` was never shown to be unreachable. It was shown to be **zero at one point of a function that has
another branch the record defined and never evaluated**. `Q3` is a function of the observer tuple `θ`;
the programme evaluated `θ_eye`, where it is zero by construction, and concluded the tier was empty.

**That is the whole deadlock.** The project relaxed the variable that was cheap to relax and held the one
that was never a law.

## §3 The currency: rungs, prices, fingerprints

A **rung** is one declared relaxation. It is admissible only if it carries three things:

1. **what it relaxes**, named as a clause of the record (never as a mood);
2. **its price**, as a dimensionless violation factor *with the observable that would detect it* — a
   relaxation no measurement could distinguish is not a relaxation, it is fiction unmoored;
3. **its fingerprint** — the measurement that tells an observer *which rung they are on*. Without a
   fingerprint the ladder is illustration, and the record's `scifi_boundary_v1.md` already drew that line:
   "hard science fiction" = finite knobs, computable consequences, explicit cost; "myth" = none of these.

The ladder itself is `docs/specs/relaxation_ladder_v1.md`; rungs, prices and fingerprints are registered
there before any of them is executed.

## §4 What happens to the prohibitions — re-scoped, not deleted

This is the clause that decides whether the new frame is a research programme or an excuse. The three
standing prohibitions were written to stop the project from lying to itself. They survive, re-indexed:

| prohibition | old form | form under this frame |
|---|---|---|
| `S9` no visibility conclusion | absolute | **no visibility conclusion at rung 0.** Every visibility statement must carry its rung index and its declared observer tuple `θ`. "It is visible" is still forbidden; "at rung `R2+R3`, `θ = (aperture, gate, band, distance)`, contrast `c = …`, verdict …" is the *required* form. |
| `D-2` no deposit frame as readability | absolute | **no rung-0 frame** may be cited as readability. A frame produced at rung `k` may be cited **with** its rung, its price and its measured loss. |
| no forward / backward selection | absolute | **the ladder is pre-registered as a whole, before any rung is executed**, and a rung may not be re-priced after seeing whether it worked. Forward selection meant "relax until the criterion passes"; under the new frame the criterion is a declared target and the relaxation is the independent variable — the thing that must stay locked is the *queue*, not the criterion. |

The last row is the load-bearing one. The old prohibition existed because relaxing a truth criterion
until a candidate passes is how a physics claim is faked. A price list cannot be faked the same way — but
it can be *re-priced*, which is the same sin one level down. Hence: **ladder first, rungs after.**

## §5 The negative results are promoted, not retired

Every closed NO-GO becomes the price tag of the rung that has to pay for it:

| rung-0 fact | becomes |
|---|---|
| `G0′` row 1 — ordinary atoms at fixed area impossible (`d_∥ = 15.4 fm` vs `0.3 nm`, `2×10⁴`) | the price of the material rung `RL-6` |
| `C3` in-action NO-GO, `ρ + p_x < 0`, parameter-independent | the price of the stability rung `RL-5` |
| `DEPOSIT-BLIND` — `I(canvas ; r₄) = 0` | the price of encoding the object as an enumeration; the reason `RL-2` must put *geometry* into the site |
| the `2¹⁴` dichotomy | the price of injectivity — already paid by `RL-1`, and it was the cheapest thing on the list |
| `L3` empty at `θ_eye` (`q = 0`, flux shortfall `3.4387×10¹⁰`) | the price of the naked eye, denominated in **orders of magnitude of flux**, which §3 of the ladder converts into a shopping list |
| `scifi_boundary` knobs R1–R6 | the hard/optional split: `6.2×10²³ V/m` and `≥10⁵` weak suppression are the two non-negotiables |

**No result is discarded.** A programme that had four theorems and no way forward now has four price tags
and a shopping list.

## §6 What "the goal" now is — stated so it can fail

> **Goal**: a human-legible image of the 3D object — four shells, their radius ratio, the modulation
> phase — produced by a declared physical scene, at a declared observer tuple `θ`, with every relaxation
> on the path named and priced, and a fingerprint that distinguishes the image from an illustration.

Testable, because the record already has the instrument: `Q3` (legibility through a declared observer,
locked threshold `≥ 2.0`) evaluated at `θ ≠ θ_eye`. **The goal is `Q3(θ) ≥ 2.0` at some rung, with the
rung's price printed beside it.** The object's identity is roughly six bits (4 shells ≈ 2, radius ratio
≈ 3, phase ≈ 1); an image that delivers zero of them is a texture, not a depiction.

## §7 What would reverse this frame

1. A demonstration that no rung reaches `Q3 ≥ 2.0` at any `θ` — i.e. the ladder terminates in a wall
   rather than a price. Then the original verdict stands and this frame is recorded as a failed search.
2. A demonstration that the ladder's total price exceeds a declared budget the governor sets. The frame
   says the goal is *paid for*, not *free*; a price above budget is a NO-GO with a number attached, which
   is a better NO-GO than the one we had.

## §8 What this document does not decide

It does not decide that a scene exists at any rung; that is what the ladder is for. It does not license a
visibility sentence — `S9` still forbids them, now with a rung index. It does not lift `S1`–`S15`, does
not reopen `G6`/`DC2` (that is `PG-01`, still awaiting one character), and does not touch the matrix
route's approval block (`PG-02`), whose question this frame does dissolve but whose mark is still the
governor's.

*Content generated by AI*

---

## §9 The one fork this frame does not decide

The frame fixes the *goal* and the *currency*. It does not fix **which rung the project buys to reach
it**, because that is a choice about what the programme is for, not a measurement. Two paths reach the
goal (`docs/specs/relaxation_ladder_v1.md` §4); their prices differ by five orders of magnitude in field
strength and by one human being:

```
[x] Select Path A -- buy RL-1: declared instrumented observer, gate <= 3 ns
                       price  V = epsilon (relief/pitch against C1),  Phi ~ 5.5-7.6 orders of flux
                       keeps  the object, its shape, its physics; gives up the naked eye

[ ] Select Path B -- buy RL-5: persistence to a steady state, naked eye retained
                       price  6.2e23 V/m (4.7e5 x Schwinger) or a 2D pocket (Geroch)
                       keeps  the naked eye; gives up nothing physical, buys an unbuildable field

[ ] Select Path C -- hold at rung 0, record the ladder as priced but unbought
                       price  none; the programme then ends as a priced NO-GO, not an empty one
```

Marking one line governs `docs/specs/relaxation_ladder_v1.md` §5's execution order. Until one is marked,
measurements 1-3 (all `V = 0`) may proceed — they are common to every path — and nothing downstream of
them may.

---

## §10 Governor mark — 2026-11-23 (`PG-03`): Path A

**Instruction** (governor, 2026-11-23, verbatim): *"1. PG-01 / PG-02 / PG-03: mark immediately"*.

**Line marked**: `Select Path A`. The other two are left unmarked. `PG-03` was the gate the queue
recommended A for, and A is the only one of the three whose price is a *convention* rather than a field: B
buys persistence at `6.2×10²³ V/m` (4.7×10⁵ × Schwinger) or a 2-D pocket with a singularity in it, and C
buys nothing and ends the programme as a priced NO-GO. Marking A says the project would rather give up the
naked eye than give up the object.

**What is bought**: `RL-1`, `V = ε`. `Q3` is evaluated at a declared instrumented observer — gate
`≤ 3 ns`, band and aperture declared — and the naked eye leaves the tuple. This is §6's goal restated as an
engineering choice: the object, its shape and its physics are kept; the *human being sitting in a room* is
what gets paid.

**The price the mark does not carry forward.** The line above prints `Φ ≈ 5.5–7.6` orders. That is the
round-45 arithmetic and it is superseded by measurement, so the mark binds the **choice**, not the number:

| correction | source | effect on the price |
|---|---|---|
| `3.4387×10¹⁰` is the chain at `C = 10⁻⁷`, not `10⁻³` | `relaxation_ladder_v1.md` erratum E1 (round 48) | at the record's own `10⁻³` the same chain gives `343.9` = **2.54** orders, 8 orders smaller |
| the measured contrast is `C = 0.280`, not `3×10⁻²` | erratum E2 (round 49), `runs/LADDER/r2_relief_contrast_results.txt` | residual **−4.5** orders at the terraced form's plateau |
| `RL-3` is retired; the path is `RL-1 + RL-2` | erratum E3 (round 50) | two rungs, not three; and `S_θ = 1.000000000` says the third bought nothing |

A path chosen on a corrected price is the same path: A was never selected for being *cheap in photons* — it
was selected because its currency is a convention. What changes is that the bill is now a measurement rather
than a price-list entry, and the bill is affordable in the only sense the frame requires: it is finite and
payable in a declared instrument.

**What it does not buy**: colour (`RL-4`, closed by measurement), a steady scene (`RL-5`, unbuilt), "the same
matter" (`RL-6`). `RL-5` is **not** abandoned by this mark — it becomes the price of the road not taken
(`RQ-15`), an optional entry in the price table rather than a blocker on the path.

**What it does not license**: a visibility sentence. `S9` still forbids them; the required form is now
"at `RL-1 + RL-2`, `θ = (aperture, gate ≤ 3 ns, band, distance; E, G)`, contrast `C = …`, `Q3 = …`,
verdict …". The last two slots exist because the two rounds after this one found them missing —
`theta_environment_v1.md` and `theta_camera_v1.md`.

**Reversal window**: open until the first rung of A is executed, and no rung has been bought yet —
measurements 1–3 are all `V = 0` and common to every path, which is exactly why §9 let them run unmarked.
The next measurement whose *design* depends on A closes the window. After that, re-selecting would be
re-pricing a rung after seeing it work, which §4 forbids in the same breath as forward selection.
