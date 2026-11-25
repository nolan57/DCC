# `GD7` / `GD8` execution — pre-registration

**Registered**: 2026-11-22, **before `src/route/fl_coordinate.py` was run.**
**Rulings** (governor, verbatim): `GD7` — *"FL means 'faithful to what the human eye sees', and FL3 is the maximum"*;
`GD8` — *"keep 2L/c, and write in 'only when D = L'"*.
**Product**: `runs/ROUTE/fl_coordinate_results.txt`. **Record**: `docs/decisions/gd7_gd8_execution_v1.md`.

---

## 0. What the two rulings settle, and what they newly expose

`GD7` fixes the *direction* of the ladder: fidelity means closeness to the unaided retinal image, so `FL3` is the
maximum and the ladder **ascends**. `GD8` fixes the *scope* of the corollary: `2L/c` stands, and it is a statement
about `D = L` only.

Taken separately neither is contentious. **Taken together they change what `FL3` can contain**, and that is the thing
this round has to compute rather than assume. Under Reading A, `FL3` was the least informative rung; under Reading B
it is the most faithful — and the corollary says what a faithful reflected-light frame of a *surviving* sheet would
have to show. The two statements are only compatible if "faithful" and "shows the sheet" are different requirements.
That is the question.

## 1. Predictions

| id | Prediction | Falsifier |
| --- | --- | --- |
| **F1** | **The four coordinates of a faithfulness metric are all computable from registered numbers**, with `FL3 = 0` exactly and unique: band offset `b`, contrast distortion `c`, photon-budget deficit `p`, enhancement intrusion `e` | any coordinate requiring an unregistered input |
| **F2** | **The rungs order `FL3 = 0 > FL2 ≈ −3.10 > FL1 ≈ −16.13`** (decades). `FL2`'s dominant cost is the band migration itself (`b = log10(284/2.25) = 2.101`), not the physics; `FL1`'s is the photon deficit plus the stretch (`c = log10(1e-2/7e-7) = 4.155`) | a non-monotone order, or a rung whose largest term is not the one named |
| **F3** | **`FL` is continuous in every coordinate**, so "continuum" is satisfied by construction rather than by declaration: sweeping the enhancement gain from 1 to 1.43e4 moves `FL` continuously from −11.98 to −16.13 with no step | any jump, or a coordinate that is only defined at the three rungs |
| **F4** | **`GD7` dissolves the apparent conflict with the corollary.** The corollary forbids *"a faithful reflected-light frame of a surviving sheet"* — it constrains the **content**, not the **fidelity**. A frame can be maximally faithful and contain no sheet. So `FL3` is attainable **and** the corollary stands | a faithful reflected frame that must contain the sheet — i.e. if "faithful" entails "sheet visible" |
| **F5** | **`GD8`'s premise covers naked-eye viewing a fortiori**: naked eye ⇒ `D ≥ 0.25 m` (near point); `D ≥ L/√2` holds for every `L ≤ 0.354 m`; for `L > 0.354 m` the object cannot be taken in at the near point. So `D = L` is the *most favourable* case and the corollary's conclusion holds for all naked-eye `D` | any `(L, D)` with `L ≤ 0.354 m`, `D ≥ 0.25 m`, `D < L/√2` |
| **F6** | **`FL3`'s content is channel-dependent and must be declared**: at `C1` held the faithful frame shows the object's **absence**; at `¬C1` it shows the **intact slab**. Both have all four coordinates zero. `FL3` is therefore a family indexed by which constraint was relaxed, not a single image | a single `FL3` frame that is faithful and shows a surviving sheet |

## 2. Thresholds, fixed now

| Quantity | Value | Basis |
| --- | --- | --- |
| eye peak | `E = 2.25 eV` (550 nm) | declared display convention |
| eye contrast threshold | `m_eye = 1e-2` (Weber) | declared; the value `painting_render_v1` already uses for "1 %" |
| sheet modulation at 550 nm | `m_R = 7e-7` | `painting_render_v1.png` panel (c), registered |
| `FL` normalisation | decades summed over four coordinates, equal weight | **declared convention, not physics** — same status as `ΔH` under `BUDGET-1` (`DC4`) |
| naked-eye near point | `D = 0.25 m` | declared |

## 3. Prohibitions carried in

1. **No physics changes.** Both rulings are about definitions and scope; nothing here touches a threshold, a
   coefficient or a state.
2. **`GD8` is applied as ruled, not as I derived it.** The per-patch form (`D ≤ d/√2`) is recorded as an
   **unregistered observation** and may not license any frame. If `F4` fails, that is stated and no workaround is
   invented.
3. **`FL3` may not be produced this round.** The ruling fixes its meaning; it does not create a frame. Any claim that
   `FL3` is *delivered* would need a citable frame with a declaration block, and none exists.
4. **The normalisation is disclosed as a convention.** If `FL`'s ordering depended on the weighting, that is a
   finding about the metric, not a result about physics.

## 4. What each failure would mean

- `F1` fails → `GD7` cannot be executed; `G2` stays open and the ruling is only a statement of intent.
- `F2` fails → the ladder does not ascend; `FL3` is not the maximum and `GD7` is inconsistent with the numbers.
- `F3` fails → "continuum" is a word, not a property, and the ladder is discrete.
- `F4` fails → `GD7` and `GD8` are jointly inconsistent, and the route cannot be completed as specified.
- `F5` fails → `GD8`'s premise does not cover the naked eye, and the corollary's scope needs widening.
- `F6` fails → `FL3` is a single well-defined image and the family structure is absent.
