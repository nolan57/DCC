# Goal-conformance check — pre-registration

**Registered**: 2026-11-22, **before `src/route/goal_conformance.py` was run.**
**Authority**: governor question — "check this — isn't this the goal of the roadmap?" + the goal sentence, against
`docs/decisions/staged_relaxation_visual_route_v1.md` §1.
**Product**: `runs/ROUTE/goal_conformance_results.txt`.

---

## 0. What this check is, and is not

It is **not** a re-quotation of the goal. Quoting a goal back to the governor answers nothing. The goal makes four
claims that are mechanically checkable — *there is a depiction*; *fidelity is a continuum*; *the diagonal is walked*;
*enhancement adds nothing* — plus one that is a channel claim (*naked-eye reflection at the minimal set*). This
registration fixes, in advance, what would count as satisfying each and what would count as failing.

## 1. Predictions

| id | Prediction | Falsifier |
| --- | --- | --- |
| **C1** | **Zero of the five goal requirements has a product.** `G1` (a depiction) — the only declared frame has `BAND: NONE` and `SCALAR: occupancy indicator`, i.e. a diagnostic, not a scene. `G2` (continuum) — no coordinate exists. `G3` (diagonal) — zero executed relaxations. `G5` (non-introduction) — no instrument | any requirement with a citable product |
| **C2** | **`DC1` coverage is 1 frame out of ≥20.** Only `s0_frame_fl1.png` carries a `.display.txt`. `display_lint.py` enumerates sidecars, so it cannot see images that lack one | coverage above 25 % |
| **C3** | **The ME5 corollary carries an unstated premise `D = L`.** The frozen identity `2L/c = √2 t_rip` is correct and is not attacked. The *inference* to "no reflected frame for any `L`" needs the optical path to equal the object size. Per-patch form: `2D/c ≤ d/v_front ⇔ D ≤ d/√2`; the admissible set is the annulus `d ≥ √2 D`; its non-emptiness is exactly `D < L/√2`; the registered statement is the `D = L` slice, where coverage is `1 − √2 = −0.414` | an algebraic error in `2D/c ≤ d/v_front`, or a registered statement of `D` anywhere in v0.2/route |
| **C4** | **The fidelity axis is not ordered, because two readings give opposite orders.** Reading A (how much is shown) makes `FL2` dominate `FL3` on both the time and flux deficits; Reading B (distance from the unaided retinal image) makes `FL3` the unique maximum. Every quantitative criterion in the repository measures Reading A; the goal sentence states Reading B | one reading that both is what the criteria measure and orders `FL3` last |
| **C5** | **The non-introduction clause is testable with two branches**, and both must convict on planted defects: (a) display levels > scalar levels (interpolation as structure); (b) map non-monotone in the scalar. Both compliant controls must pass | either branch silent on its planted defect, or a compliant control convicted |

## 2. Thresholds, fixed now

| Quantity | Threshold | Basis |
| --- | --- | --- |
| `DC1` coverage | "one frame only" if `declared ≤ 1` | the count is the count; the band is a reporting convenience |
| corollary window | admissible iff `D < L/√2 = 0.70710678 L` | exact algebra, no tolerance |
| Pareto dominance | strict on both coordinates | standard |
| `EN-BOUND` | `levels_display > levels_scalar` **or** map not monotone ⇒ CONVICT | branch (b) is the repository's existing EN2 rule, made executable; branch (a) is new |
| instrument trust | all planted cases behave as labelled | negative-test discipline, as for `provenance_lint` |

## 3. Prohibitions carried in

1. **The frozen identity is not edited.** `2L/c = √2 t_rip` stays true. `C3` attacks an inference, and if it succeeds
   the correction is registered as **`GD8`** for the governor, never applied by the executor, because `ME5` is frozen.
2. **No `ME5` verdict is softened.** If `C3` fails, the corollary stands exactly as written.
3. **No new physics.** `C3` uses `v_front = L/t_rip = c/√2`, which is the definition already in the Phase 2 product,
   not a new front speed.
4. **`G4`'s "UNRESOLVED" is not a verdict of feasibility.** It says the requirement is not decidable from the
   registered text, which is a weaker and correct statement than either "possible" or "impossible".

## 4. What a failure of each prediction would mean

- `C1` fails → the route is further along than this audit believes; the review is withdrawn.
- `C2` fails → `DC1` is being honoured in practice and the validator gap is cosmetic.
- `C3` fails → the corollary is safe and `GD8` is withdrawn.
- `C4` fails → a single coherent fidelity metric exists and `GD7` is withdrawn.
- `C5` fails → the instrument is untrusted and no `EN-BOUND` claim may be made this round.
