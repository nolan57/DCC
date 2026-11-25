# Pre-registration — `DEMO-1` census and the declared traversal

**Written 2026-11-22, before `src/route/demo_2d_map.py` exists.** Predictions fixed here so a FAIL is visible as a
FAIL. After the run, corrections go in an erratum appended to the results file; this file is not edited.

Specification: `docs/specs/demo_object_v1.md` (`DEMO-1`).

---

## Predictions

### A. Census — does the construction actually avoid `GD10`?

| id | prediction | expected |
| --- | --- | --- |
| **P1** | pieces, cells, occupancy | `4.279069764e9`, `4.294967296e9`, `0.99629` |
| **P2** | the height cap implied by `one plate per cell` at `S = 2¹⁶`, `M = 4` | `H_max = 0.230854 m`; declared `0.2300 < H_max` |
| **P3** | plates per cell | `0.9963 < 1` ⇒ `GD10` cannot arise |

`P1`–`P3` are the reason a new object was admissible at all. If plates exceed cells, the object has re-created
`GD10` and must be re-declared.

### B. Admissibility of the pieces

| id | prediction | expected |
| --- | --- | --- |
| **P4** | largest piece area vs site area | `1.4335e-2` vs `0.1601 m²` (≥ `10×` clear) |
| **P5** | largest piece extent vs pitch | `0.180 m` vs `0.4001 m` |
| **P6** | the shells never cross | `min(r₃−r₂) = 0.011 m > 0` |
| **P7** | the components trade: span of `C3`'s area along `z` | factor `3.67` |

### C. The ordering decision — this is the substantive one

| id | prediction | expected |
| --- | --- | --- |
| **P8** | under **layer-major** (`p = 4n+k`), the component mix of a 128×128 decimated block | each component `25.0%`, all four within `1%` ⇒ identity annihilated |
| **P9** | under **component-major** (`p = kN+n`), the fraction of decimated blocks that are single-shell | `≥ 0.99` |
| **P10** | blocks straddling a shell boundary | exactly `3` |

`P8` and `P9` are a pair on purpose. If `P8` fails (`layer-major` survives decimation), then §4.1 of the spec is
wrong and the ordering choice has no measured basis — it would be taste, and must be recorded as taste.

### D. Dead constants and the curve

| id | prediction | expected |
| --- | --- | --- |
| **P11** | canvas, mean and max placement at the reused `0.4001 m` pitch | `26,218.6 m`, `10,032 m`, `18,539 m` |
| **P12** | `t_rip = √2H/c`; minimum transport duration at `v ≤ 11.3 km/s`; ratio | `1.0847e-9 s`, `0.888 s`, `8.2e8` |
| **P13** | total cut area `= N·πr₄²` | `2.7222e7 m²` |
| **P14** | contiguity of the exact order-16 Hilbert order over the occupied prefix | `1.0000` exactly |

## Declared falsifiers

- If `P3` fails, `DEMO-1` is inadmissible as specified and `H` must be reduced; the ruling is void until it is.
- If `P9` < `0.90`, component-major is *also* annihilated and no `σ` at this decimation preserves identity — that
  would be a finding against the whole approach, not a reason to pick the other ordering.
- If `P14` < `1.0000`, the `S = 2¹⁶` derivation in §2.1 is wrong and the padding cost was paid for nothing.
