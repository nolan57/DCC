# Audit — "exhaustive constraint enumeration and distinguishability mapping" (PROPOSED)

**Date**: 2026-11-22
**Object**: `docs/decisions/exhaustive_matrix_route_v1.md` (registered **PROPOSED**, not ratified)
**Pre-registration**: `runs/MATRIX/matrix_audit_registration.md` — predictions `P1`–`P7` fixed before the code existed
**Product**: `src/route/matrix_audit.py` → `runs/MATRIX/matrix_audit_results.txt`
**Verdict**: **NOT VIABLE AS WRITTEN.** 9 of 10 section findings block ratification. 7 of 7 predictions confirmed.

---

## 1. Verdict in one paragraph

The submission proposes to replace a linear route with a coverage set: 8 constraint combinations × 4 tiers of
distinguishability. Its §II is a faithful transcription of the registered constraint table and passes. Everything
else fails, and it fails for one structural reason that is worth stating before the individual findings: **every
tier compares the 2D scene to the original object, and 2D-ification is precisely the operation that destroys that
comparison.** `L0` compares connectivity to the original — the conversion disconnects it into `1.18e10` pieces.
`L1` compares metric proximity — the layout spreads it over `324.9 km²`. `L3` compares optical appearance — the
sheet has zero exposure budget and a `3.4e10` flux shortfall. `L2` compares information — and information about the
original is exactly what a deterministic, irreversible conversion cannot add. A matrix whose columns all measure
*similarity to the pre-conversion state* cannot register a process whose success consists in *ceasing to be similar
to it*. It can only register the process's absence. That is what the audit measures: 0 of 4 tiers increase with
2D-ification.

---

## 2. What the submission gets right

Credit is due where it is due, and three things here are better than the route they propose to replace.

1. **§II is accurate.** All three constraint statuses transcribe the registered record exactly (`C1` identity-level
   with `d_∥ = 2.91e-4 a₀`; `C2` intralayer holds / `8.12e9` interfaces broken; `C3` in-action NO-GO,
   `ρ + p_x < 0`, parameter-independent). No drift.
2. **§VI "No Falsified Imagery" is stated more sharply than anywhere else in the project**: no cell may contradict
   an established NO-GO. That is the correct form of the invariant, and it is the clause that kills row 1 (§3 M1).
3. **§V "Negative Verification"** makes a null result a valid matrix entry. This is the discipline the previous
   route lacked in its final rounds, and it is why the audit could be run at all.
4. **§VI "Threshold Integrity"** is the right rule. It is the *other* clause in the document that contradicts it
   (§3 M8) — the rule is sound, its neighbours are not.

---

## 3. Findings

### M0 — the enumeration is not the enumeration it claims

§IV claims `2³ = 8` combinations and §V demands "complete coverage". The table prints **eight rows containing
seven distinct members**: rows 6 and 8 are both `¬C1 ∧ ¬C2 ∧ ¬C3` (row 8 carrying the label "Zero"), and
`¬C1 ∧ C2 ∧ ¬C3` is absent.

Cheap to fix, but not cosmetic: the omitted row is **one of the two rows that survive §3 M1**, so the single
comparison the matrix could make is the one the table drops. Transcribed verbatim in the registration, not repaired
by the executor — an enumeration edited by the auditor is no longer the governor's enumeration.

### M1 — 8 rows reduce to 2, and one of the two axes is not an axis

- **`C3` is VOID, not `TBD`.** `C3` is registered as an in-action NO-GO that is *parameter-independent*
  (`κ(ρ+p_x) = −γ(γ+h) < 0` for all `h, γ > 0`). A NO-GO constraint cannot be *satisfied*. So all 4 rows
  containing `C3` have no physical instantiation. §VI's own rule forbids presenting content on them.
- **`¬C2` is UNREALIZED.** `C2` is "zero intralayer strain", and the registered mechanism achieves it by
  construction: `front_sweep_v1` §2 step ② is an `(x,y)` **identity map** per layer, so intralayer strain is
  *identically* zero for every conversion. There is no construction on record that produces non-zero intralayer
  strain, so `¬C2` has nothing to instantiate. **`C2` is a theorem of the mechanism, not a switch.** "Relaxing
  `C2`" — one of the two axes of the proposed matrix — has no meaning.
- Surviving: **2 of 8** — `C1∧C2∧¬C3` and `¬C1∧C2∧¬C3`. They differ only in `C1`, so the matrix is a **one-bit
  comparison**, and the printed table contains only 1 of the 2 (M0). **As printed it has no pair at all.**
- Both rows the submission singles out are dead: `Full` (row 1, §VII.1's first action item) is **VOID**;
  `Zero` (row 8, "minimal constraint baseline") is **UNREALIZED**.

### M2 — `L0` fails at the Full row, by `1.18e10`

Original object: `V = 0.070 m³`, `H = 1.75 m`, `A_c = 0.040 m²` — one solid column, contractible, `β₀ = 1`, `χ = 1`.
2D scene under `C1`: `1.18e10` mutually disconnected plates with vacuum between them (`front_sweep_v1` step ③:
"no in-plane bonding is performed"). Each plate is contractible, so `β₀ = χ = 1.18e10`.

`χ` ratio `= 1.18e10` (`log₁₀ = 10.07`). `L0` is declared "the absolute minimum threshold for physical
self-consistency"; it is violated by ten orders of magnitude **at the row §VII.1 asks to fill first**.

And `L0` cannot be rescued there. `unfold_is_real_v1` §4 rules that any adjacency is a choice of the layout
permutation and calls "being a painting" *"a measure-zero encoding choice, not a physical conclusion"*. So `L0` at
`C1` passes only on an object that physics does not supply.

### M3 — `L1` scores best where the 2D-ification did not happen, and under §III it is identically satisfied

*Positional metrics, both candidates, ambient embedding:* `d_H = 25.5 km` (registered maximum placement) `=
1.457e4` object-heights; `W₁ = 13.8 km` (registered mean) `= 7.886e3`. At `¬C1` both are **exactly 0**. So `L1`
decreases strictly as 2D-ification completes; its optimum is the failure of the experiment.

*The "metric selected individually for each combination to best fit" clause, taken literally:* for **any** layout
map `f`, the pullback metric `g* = f*(δ)` makes `f` an isometry, so `d(original, scene) = 0` identically — for every
layout, including every failed one. A tier whose metric **and** threshold may be chosen per cell, after seeing the
cell, is satisfied by every cell. So under §III, `L1` is not merely non-discriminating: it is **identically
satisfied**. That is exactly what §VI's "Threshold Integrity" clause exists to forbid, and both clauses are in the
same document (M8).

> **Self-correction, disclosed.** The audit's first reading charged `L1` the `log₂(N!) = 3.79e11` bits of the layout
> permutation, on the grounds that the fitting metric must smuggle them in. That charge was **misplaced**. The
> experimenter does not spend those bits: one *rule* ("row-major, 90126 wide") describes the layout in ~34 bits. The
> number is real, the charge is not. `L1` fails because a per-cell metric is unfalsifiable, not because it costs
> information. The permutation still matters, but in a different place: presenting the arranged picture *as* the
> physical scene is a §V "no falsified imagery" question, not an `L1` question. The scope note is in the product so
> the wrong reason does not outlive the right conclusion.

### M4 — `L2` is undefined, and its maximiser is the submission's own declared failure

`I(Scene; Structure) ≤ H(Structure)`. The scene is a deterministic function of the structure (one object, one
conversion law), so `H(Scene|Structure) = 0` and **`I = H(Scene)`**. Three cases, all fatal:

| case | consequence |
| --- | --- |
| no ensemble over structures declared | mutual information is defined on a **joint distribution**; the project has one object. `I` is **undefined** — not small, not zero. This is the `ME3-F1` class (undefined argument), not a tolerance question |
| the single registered realization | `H(Scene) = 0` bits ⇒ `I = 0` at **every** cell ⇒ any `I_min > 0` fails every cell identically. Non-discriminating |
| over any reachable scene alphabet | `max I = max H(Scene)`, attained by a **uniform noise field** — which §V lists as a *negative* entry: "a 'null image' or 'structureless noise' result is a valid matrix entry" |

So `L2`'s argmax is `L2`'s own declared failure. The tier cannot be fixed by a tolerance; it needs an ensemble
declaration, which is a physical commitment the document does not make.

### M5 — `L3` is empty wherever `C1` holds, on two independent grounds

**Timing.** `t_rip(1.75 m) = √2·1.75/c = 8.2553e-9 s` (cross-checked against the registered `t_rip(1.0 m) =
4.717309e-9 s`; ratio exactly `1.75`). Reflection needs a round trip `2H/c = 1.1675e-8 s`, exceeding `t_rip` by
`√2`. **Zero exposure budget in reflection** — the frozen `ME5` corollary. No frame exists, naked-eye or otherwise.

**Flux.** Detection in `t_rip` needs `9.539e31 m⁻² s⁻¹` (registered) `× 8.2553e-9 s = 7.8747e23` photons m⁻² per
frame. Full sun at 2.25 eV gives `2.7740e21 m⁻² s⁻¹ × 8.2553e-9 = 2.2900e13`. **Shortfall `3.44e10` (10.5
orders)** — and that is the *detector* threshold, before the eye's own ~90-photon requirement, and it is at the
channel `L3` forbids (the only channel that fits inside `t_rip` is 284 eV transmission, i.e. band migration).

So `L3` at `C1` is empty twice over. `L3` at `¬C1` is trivially satisfied — by a scene in which the phenomenon
did not occur. On the charitable reading (`L3` presupposes a 2D scene, so `¬C1` rows are unscorable), `L3` is
unreachable outright.

### M6 — no tier increases with 2D-ification

| tier | at `¬C1` | at `C1` | direction |
| --- | --- | --- | --- |
| `L0` | PASS (`χ` ratio 1) | FAIL (ratio `1.18e10`) | decreasing |
| `L1` | `0.0000` exact | `1.46e4 H` | decreasing |
| `L2` | `0` | `0` | constant |
| `L3` | PASS (intact object) | FAIL (two grounds) | decreasing |

**0 of 4.** The cell value is "Max Distinguishability", which needs a total order `L0 < L1 < L2 < L3`. Three columns
run the other way and one is flat. **No such order exists on the measured signs**, so the matrix cannot be filled
as specified — not for lack of physics, but because of what the columns measure.

### M7 — Phase 2 has no falsifier, and its literal reading is self-defeating

§IV Phase 2 sets: unlimited number and type, "not pre-defined", "determined dynamically", terminate on first `L3`.

- **No falsifier.** The search space is unbounded and unparameterised, so "this constraint set cannot reach `L3`"
  has no test. Same class as the withdrawn `ME4` clause "except at phase transitions", which accommodated
  `1000/1000` adversarial cases and was declined for exactly that reason.
- **And it terminates at zero cost anyway.** From M5, `L3` is reached at `¬C1`. So §IV's trigger — "if and only if
  all 8 combinations fail to reach `L3`" — is false, Phase 2 never runs, and the route concludes: *do not perform
  the experiment*. Adding no constraint at all reaches the terminal condition.

Both branches are unacceptable and they are simultaneous: strict reading ⇒ unbounded search; literal reading ⇒
self-defeat.

### M8 — §III and §VI contradict, and only one can survive

> §III `L1`: "The specific metric and its threshold are **selected individually for each** constraint combination
> to best fit its physical characteristics."
> §III `L2`: "This threshold is **dynamic and declared independently for each** constraint combination."
> §VI: "Thresholds for `L1` and `L2` must be **declared before** the evaluation of the scene to prevent post-hoc
> fitting."

A threshold chosen per cell, to best fit that cell, *is* post-hoc fitting. **Adjudication (executor's, for the
governor): keep §VI, delete both §III clauses.** §VI is the invariant that makes a matrix cell mean anything, and
M3 shows the fitting clause is not merely permissive but total (pullback metric ⇒ `L1 ≡ 0`). Consequence, stated
so it is not a surprise: with §VI alone the metric must be fixed once, globally — and then M3 says which way it
scores.

---

## 4. Why the failure is one failure, not nine

`M2`, `M3`, `M5` are the same defect in three columns. Write the tiers as they are written:

```
L0 :  invariants(scene)  =  invariants(original)
L1 :  dist(scene, original) ≤ ε
L2 :  I(scene ; original) ≥ I_min
L3 :  appearance(scene)  ≈  appearance(original)      [naked eye]
```

Each line puts the original on the right-hand side. The process under study is a dimensional reduction whose
registered mechanism is `8.12e9` **SE(2) rigid translations** — "none of which is a deformation"
(`front_sweep_v1` §2). A map that is not a deformation cannot preserve connectivity, cannot preserve metric
proximity, cannot preserve optical appearance. The invariants of the *original* are, by construction, exactly what
the process does not carry forward.

So the matrix is not badly calibrated; it is **measuring the wrong arrow**. It asks "how much of the original
survives", and the answer is already known from the theorem (`unfold_is_real_v1` §5.1, invariance of dimension:
no continuous injection `ℝ³ → ℝ²`): **nothing survives unchanged, and that is not a result — it is the premise.**

What the tiers would have to measure is the *other* direction: not "how close to the original", but "how much of
the structure is **recoverable from the new state by an observer who is given the conversion law**". That question
has an answer that is not zero — `unfold_is_real_v1` §3 records that a tile *is* the slice, unstretched, and that
"the lungs, heart, and spine can be recognized in the rendered image" — and that answer is what the project has
been chasing since round 1. It is also exactly what the previous round's `GD7` found from the other end: fidelity
to the retinal image and recoverable information are **anti-correlated**, so a single "distinguishability" number
cannot serve both.

---

## 5. Relation to the open decisions this submission would inherit

| decision | state | what approval would do to it |
| --- | --- | --- |
| `GD6` — what `φ` denotes in `ME3` | **OPEN**, blocks Phase 3 | Phase 3 disappears rather than being answered; `ME3-F1` stays BLOCKED |
| `GD9` — the route's objective function | **OPEN** | answered by fiat: "maximum tier per cell". M6 shows no total order on `L0…L3` is compatible with the measured signs, so the fiat does not resolve it |
| `GD7` — `FL` means faithfulness to the eye | CLOSED, measured | `L3` is a **stricter predicate** than `FL3` ("recognizable as a structured image" excludes `FL3` member A, the faithful absence). The substitution is undeclared; it is what makes `L3` unreachable at `C1` |
| `GD8` — keep `2L/c`, write in `D = L` | CLOSED | untouched; `L3`'s timing ground rests on it, and `D = L` is the *most favourable* case, so the ground holds *a fortiori* |
| `EN-BOUND` | instrument, negative-tested | survives unchanged — it is the executable form of §V's non-introduction clause, which the submission keeps |

The `GD7`/`L3` row is the one to look at. `FL3` was reachable at `C1` precisely because a maximally faithful frame
may show *nothing* (`GD7` §3: "a frame can be maximally faithful, containing no sheet"). `L3` adds "recognizable as
a structured image", which excludes that frame — so `L3 ∧ C1` becomes empty, and the ladder loses the only rung
`C1` could reach.

---

## 6. Minimum amendments for a ratifiable version

Not a redesign. Six edits, each traceable to one finding, and each cheap:

1. **Fix the table** (M0): eight distinct rows; add `¬C1 ∧ C2 ∧ ¬C3`; delete the duplicate. Then state the
   admissibility pre-filter (M1) explicitly, so the matrix is 2 rows, not 8 — the document must not claim coverage
   of a set with four void and two unrealized members.
2. **Replace §III's four tiers** (M2–M6) with one question asked at increasing strength: *recoverability given the
   conversion law*, not *similarity to the original*. Concretely: `L0'` = the conversion law is invertible on the
   scene up to the declared layout convention; `L1'` = the recovery map is stable under the declared measurement
   noise; `L2'` = the recovered structure's mutual information with the original, **with an ensemble declared**;
   `L3'` = the recovered structure is naked-eye visible *in the recovered form*, not in the raw state.
3. **Keep §VI, delete §III's per-cell metric/threshold clauses** (M8). Fix one metric globally, before any cell.
4. **Bound Phase 2** (M7) or delete it: an unbounded, unparameterised search with a reachable success condition is
   not a research phase, it is a hope. If it stays, it needs a declared finite candidate list and a listed failure
   condition per candidate.
5. **Declare the layout convention as a `DC` item** (M3 scope note, §4). The arranged picture is a convention; the
   project's own display conventions already know how to declare one. Without that declaration, every frame of an
   arranged scene contradicts §V's "no falsified imagery" the moment it is labelled "the physical scene".
6. **Carry `GD6` and `GD9` forward by name** (§5), or strike them explicitly. Superseding a route does not answer
   the questions the route was blocked on.

---

## 7. On the closing question — drafting `L1`/`L2` evaluation scripts

The submission ends by offering to draft the core framework of `L1` (metric) and `L2` (information) evaluators for
direct matrix filling. **The answer is: not yet, and the reason is not caution.**

An evaluator is a machine that turns a cell into a number. `L1`'s specification permits the metric to be chosen per
cell, and M3 shows that choice has a fixed point: the pullback metric along the layout, under which the distance is
`0` for every cell. So the proposed `L1` evaluator would not be an instrument — it would be a **certifier of
success for whatever it is shown**. Building it first, then filling cells, is the failure mode this project has
already paid for twice (the `ME4` escape clause; the `S45` probe whose labels were reused). `L2`'s evaluator has the
complementary problem: without a declared ensemble it has no input, and with one it is maximised by noise.

What can be built now, and is worth building, is the **refusal harness**: a checker that takes a cell and returns
`NO-VERDICT` unless the metric, the threshold, the ensemble and the layout convention are already declared and
hash-pinned before the scene is shown. That is a small program, it is falsifiable, and it is the only form of
`L1`/`L2` evaluation that the current text can honestly support. I will build it on request — after §6 items 2, 3
and 5 are decided, since it has to pin those declarations and cannot invent them.

---

## 8. What has not been done

- No cell filled. No frame produced. No threshold moved. No archived product edited.
- This route is **PROPOSED**; `docs/decisions/phased_relaxation_route_v2.md` and
  `staged_relaxation_visual_route_v1.md` remain in force, and `GD6`/`GD9` remain the blocking items they were.
- The audit establishes no physics: every number is a registered constant or arithmetic on one.

---

## 9. Registration

| item | where |
| --- | --- |
| decision text, verbatim, as PROPOSED | `docs/decisions/exhaustive_matrix_route_v1.md` §1 |
| registration record | same, §2 |
| predictions `P1`–`P7` | `runs/MATRIX/matrix_audit_registration.md` |
| executable audit | `src/route/matrix_audit.py` |
| results, `M0`–`M8`, 7/7 predictions | `runs/MATRIX/matrix_audit_results.txt` |
| this audit | `reports/reviews/exhaustive_matrix_route_v1_audit.md` |

**PROVENANCE: NEITHER** (audit arithmetic on registered inputs; establishes no physics).
