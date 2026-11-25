# Matrix route audit — pre-registration

**Registered**: 2026-11-22, before `src/route/matrix_audit.py` existed.
**Object audited**: `docs/decisions/exhaustive_matrix_route_v1.md` (PROPOSED, not ratified).
**Inputs**: registered numbers only — `front_sweep_v1.md` §2 (census `8.12e9` layers × `1.457` = `1.18e10` plates,
average placement `13.8 km`, maximum `25.5 km`), `unfold_is_real_v1.md` §3–§5 (§4 permutation is not physics; §5.1
invariance of dimension), `p2_clock_results.txt` (`t_rip(1.75 m)`, flux `9.539e31 m^-2 s^-1` at 2 eV,
`I` = `9.000e14` per resolution element), `fl_coordinate_results.txt` (`FL3 = 0`).

Seven predictions. Each is stated so it can fail.

---

## P1 — row admissibility

The 8 rows will not reduce to 8.

- `C3` is registered as an in-action NO-GO that is **parameter-independent** (`κ(ρ+p_x) = −γ(γ+h) < 0` for all
  `h, γ > 0`). A NO-GO constraint cannot be *satisfied*, so every row containing `C3` is not `TBD` but **VOID**.
  Predicted: **4 rows VOID**.
- `¬C2` requires a conversion with non-zero intralayer strain. The registered mechanism has intralayer strain
  *identically* zero (`front_sweep_v1` §2 step ②: "intralayer (x,y) identity map → intralayer strain always 0"), so
  `¬C2` has **no registered realization**. Predicted: the remaining 4 rows are **UNREALIZED**, not `TBD`.
- Predicted surviving rows: **2** — `C1∧C2∧¬C3` and `¬C1∧C2∧¬C3`.

**Failure condition**: if any row with `C3` can be instantiated, or if a construction with non-zero intralayer
strain is on record, P1 fails.

## P2 — `L0` is refuted, not `TBD`, and refuted at the Full row

Original object: `V = 0.070 m³`, `H = 1.75 m`, `A_c = 0.040 m²` — a solid column, contractible, so `β₀ = 1`,
`χ = 1`. 2D scene under `C1`: `1.18e10` mutually disconnected plates with vacuum between them
(`front_sweep_v1` step ③: "no in-plane bonding is performed"), each contractible, so `β₀ = χ = 1.18e10`.

Predicted: **`L0` fails at `C1` by a factor `1.18e10`** (`log₁₀ = 10.07`), and `L0` at `¬C1` is trivially exact.
So the matrix's `L0` column is **anti-monotone** in 2D-ification.

Predicted secondary: `L0` can be *made* to pass at `C1` only by fixing the layout permutation `π`, which
`unfold_is_real_v1` §4 rules "a measure-zero encoding choice, not a physical conclusion".

**Failure condition**: if `χ` is preserved, or if the disconnect is avoidable under `C1`.

## P3 — `L1` is anti-monotone and its "optimized metric" clause is the mechanism

Predicted: with Hausdorff, `d_H(original, 2D layout) ≈ 25.5 km` (the registered maximum placement distance),
normalized by `H = 1.75 m` → **`1.46e4` object-heights**; with Wasserstein-1 the registered *average* `13.8 km`
→ **`7.9e3`**. At `¬C1`, both are **exactly 0**.

So `L1` decreases strictly as 2D-ification completes: the tier scores **best where the 2D-ification did not
happen**.

Predicted: the only way to make `L1(C1)` small is a metric that compares *labels* rather than positions, i.e. one
that encodes `π`. Its information content is `log₂(N!)` with `N = 1.18e10` → **`3.79e11` bits**.

**Failure condition**: if `L1` at `C1` is small under a positional metric, or if the `π`-encoding cost is ≪ `1e11`
bits.

## P4 — `L2` is identically zero (or undefined), and its maximum is structureless noise

`I(Scene; Structure) ≤ H(Structure)`. With `Scene = f(Structure)` deterministic, `H(Scene|Structure) = 0`, so
`I = H(Scene)`. Predicted:

- If no ensemble over structures is declared: **`I` is undefined** (mutual information needs a joint distribution
  over an ensemble; the project has one object). This is the `ME3-F1` class — an undefined argument — not a
  tolerance problem.
- With the single registered realization: `H(Scene) = 0` bits (discrete), so **`I = 0` at every cell**, hence below
  any `I_min > 0`: `L2` fails everywhere, identically. Non-discriminating.
- Over the reachable scene alphabet: `I = H(Scene)` is **maximised by a uniform noise field**, which §V of the
  submission itself lists as a *negative* (failure) entry. Predicted: **`L2`'s argmax is the submission's own
  failure mode.**

**Failure condition**: if `I` is non-zero and discriminating between the two surviving rows without an ensemble.

## P5 — `L3` is empty wherever `C1` holds, on two independent grounds

- **Timing** (frozen corollary, `ME5`): reflection has *zero* exposure budget — `2L/c` exceeds `t_rip` by
  `√2` at every `L`. No reflected-light frame exists, naked-eye or instrumented.
- **Flux**: `t_rip(1.75 m) = √2·1.75/c = 8.2553e-9 s`. To detect in `t_rip` the visible channel needs
  `9.539e31 m^-2 s^-1` (registered, `p2_clock_results` P2-3/P2-4) → `7.8747e23` photons m⁻² per frame.
  Full-sun illumination at 2.25 eV is `2.7740e21 m^-2 s^-1` → `2.2900e13` photons m⁻² per frame. Predicted
  shortfall: **`3.44e10`** — ten to eleven orders of magnitude, *before* the eye's own threshold and before `L3`'s
  own prohibition on enhancement (which removes the 284 eV channel, the only channel that fits).

> **Pre-run correction, disclosed.** As first written this section used `t_rip = 3.893e-9 s` and derived
> `3.71e22 / 1.08e13 / ≈3.4e9`. That `t_rip` was wrong: `√2·1.75/c = 8.2553e-9 s` (cross-checked against the
> registered `t_rip(1.0 m) = 4.717309e-9 s`, ratio exactly `1.75`). The sequence "3.893 → 3.4e9" was internally
> consistent but built on the wrong `t_rip`; the corrected numbers are `8.2553e-9 / 7.8747e23 / 2.2900e13 / 3.44e10`.
> Corrected **before `matrix_audit.py` existed and before any run**, and recorded rather than quietly repaired.
> The prediction's substance (ten-plus orders, therefore unreachable) is unchanged by the correction, which is
> exactly why it is worth disclosing that the first numbers were wrong: the conclusion was robust, the arithmetic
> was not, and only the arithmetic was re-derived.

Predicted: **`L3` is unreachable at `C1` and reachable only at `¬C1`** — i.e. only in rows where the scene is not
2D-ified. And on the charitable reading (`L3` presupposes a 2D scene, so `¬C1` rows are not scorable), `L3` is
**unreachable outright**.

**Failure condition**: if any `C1`-holding row yields a naked-eye structured frame.

## P6 — no tier in the matrix is monotone increasing in 2D-ification

Predicted count: **0 of 4**. `L0`, `L1`, `L3` strictly decreasing; `L2` constant at 0 (or undefined).

Consequence predicted in advance: the matrix's cell value "Max Distinguishability" requires a total order on
`L0…L3`, and no such order is compatible with the measured signs. So the matrix cannot be filled as specified —
not because the physics is unavailable, but because every column measures something that 2D-ification *destroys*.

**Failure condition**: if ≥ 1 tier increases with 2D-ification.

## P7 — Phase 2 has no termination criterion

§IV Phase 2 sets: unlimited constraint count and type, dynamically chosen, terminate on first `L3`. Predicted:

- The search space is unbounded and unparameterised → **no falsifier exists** for "this constraint set cannot
  reach `L3`". This is the same class as the withdrawn `ME4` "except at phase transitions" clause, which
  accommodated `1000/1000` adversarial cases.
- Termination on first `L3` interacts with P5: if `¬C1` counts as a row, `L3` is reached **without adding any
  constraint at all**, at zero cost, by not performing the experiment. Predicted: **the route terminates at
  Phase 1 on the row where the phenomenon is absent.**

**Failure condition**: if Phase 2 admits a bound on its search or on its own failure.

---

## Method

`src/route/matrix_audit.py`, pure arithmetic on the registered constants above; no new physics, no fitting.
Output `runs/MATRIX/matrix_audit_results.txt`. Verdicts are derived from computed flags, never from a
hand-written closing string (the defect that appeared twice in this project and is not repeated here).
