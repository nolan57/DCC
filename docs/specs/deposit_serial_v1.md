# `deposit_serial_v1` — serialization format and acceptance criteria

**Status**: **LOCKED** on creation. Thresholds in §4 are declared before any measurement; a measurement that
misses one is reported as a miss, not as a reason to move the threshold.
**Owner**: route terminus (`docs/decisions/route_terminus_v1.md`, `D-2`, `D-7`).
**Supersedes**: nothing. This is the first format document for the deposit.

---

## 1. What this file is, and what it is not

It is the **storage format** for `DEPOSIT-SERIAL`: the lossless two-dimensional serialization of a plate
inventory. It is **not** an image format, and nothing in it may be cited as evidence of readability
(`D-2`, `LOSSLESS-REFERENT`). Its "lossless" refers to the **plate inventory** only — see `D-2a`.

The distinction is operational: an image is many-to-one by decimation; this format is one-to-one by
construction, and that is precisely why it is a file (`MAP-TRILEMMA`, row 4).

## 2. The record

A plate is fully specified by two integers:

| field | symbol | range | bits |
| --- | --- | --- | --- |
| component index | `k` | `0 … M−1` | `ceil(log2 M)` |
| axial index | `n` | `0 … N−1` | `ceil(log2 N)` |

**Address.** `p = k·N + n`. This is `σ`'s rule, and it is the only nontrivial claim in the format: it makes
`(k,n) ↔ p` a bijection on `[0, M·N)` with **zero** stored bits (`CARD-ONLY`).

**Word.** A plate is one `uint32`, little-endian:

```
word = (n << 2) | k          requires  n < 2^30   and   k < 2^2
```

For `DEMO-1`: `M = 4` ⇒ `2` bits for `k`; `N = 1,069,767,441 < 2^30` ⇒ `30` bits for `n`. Total **32 bits**,
fully used, no padding. `M = 4` and `N < 2^30` are format preconditions, checked at header write.

**File order.** Record `i` of the file is the plate at address `p = i`, for `i = 0 … P−1`. Since `p` is also the
Hilbert index, consecutive words are **curve-adjacent** — that is the locality the format exists to provide
(`SFC-INDEX`).

## 3. Vacuum

`cells = S²` with `S = 2^order`. Cells `p ∈ [P, cells)` are **not yet deposited** and are **not stored**. The
reader reconstructs them: `p < P` ⇒ plate, `p ≥ P` ⇒ vacuum.

So the file size is `4P` bytes, not `4·cells`. For `DEMO-1` that is `15.9408 GiB` against a `16.0000 GiB`
full-canvas array — the `0.37%` gap is the occupancy deficit `1 − 0.996299`.

## 4. Acceptance criteria — locked

| id | criterion | threshold | kind |
| --- | --- | --- | --- |
| **A1** | round-trip exactness `decode(encode(x)) = x` | **`0` mismatches** — not a rate | hard |
| **A2** | bytes per plate | **exactly `4`** | hard |
| **A3** | contiguity of consecutive records on the curve | **`1.000000`** | hard |
| **A4** | median `|Δn|` between consecutive records | **`≤ 1`** | hard |
| **A5** | encode throughput, one thread, sequential | **`≥ 10 MB/s`** | floor |
| **A6** | decode throughput, one thread, sequential | **`≥ 10 MB/s`** | floor |
| **A7** | full deposit, one pass, either direction | **`≤ 1800 s`** | derived from `A5`/`A6` |

`A1` is exactness by *count*, because the map is a bijection by construction: a single mismatch is a bug, and
"99.999%" would be a category error presented as tolerance. `A2` is exact for the same reason — the two fields
sum to `32` bits with no slack.

`A5`/`A6` are floors chosen from the hardware, not from hope: `17.1 GB` at `10 MB/s` is `28.5 min`, which fits a
`32 GB` / no-GPU machine comfortably. They are deliberately set an order of magnitude below what a vectorised
pass should reach, so that a miss is diagnostic rather than marginal.

## 5. The objective (`GD9`), stated operationally

`D-7` fixed the route's objective as **fidelity + locality**. In this format that is:

- **fidelity** is not optimised — it is **constrained**: `A1` exact, `A2` exact. There is nothing to trade.
- **locality** is the **objective**: maximise `A3`, minimise `A4`.

That asymmetry is the answer to why the 32-cell matrix was the wrong instrument. The matrix scored *readability*,
which is not in the objective and cannot be met (`MR1.0`); the objective's two terms are one constraint and one
ordering, and both are measurable on a single pass over the file. A metric that cannot trade against a hard
constraint is not a metric of this route.

## 6. What this format does not solve

- It does not put a physical quantity into a site. A word carries `(k, n)` and nothing else — `10` of `12`
  declared parameters remain absent (`DEPOSIT-BLIND`). The `G6`/`DC2` blocker is untouched.
- It does not make the deposit readable. `D-2` stands.
- It does not define a body `σ`. `GD11` remains parked for a body-depositing line.
