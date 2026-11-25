# `deposit_serial_v1` — conformance, and the operational form of `GD9`

**Ruling**: 2026-11-22
**Spec**: `docs/specs/deposit_serial_v1.md`, sha256 `e3c2a555a91b42a5c7036aa0685db17c90e3c4a7443ed66251b735004a6194d9`
**Pre-registration**: `runs/SERIAL/serial_registration.md` (one amendment, pre-measurement, disclosed)
**Product**: `runs/SERIAL/serial_results.txt` (197 lines), archived unedited with `E1`–`E3` appended

---

## 0. Verdict

**The format conforms. All seven locked criteria — `A1`–`A7` — are met. `GD9` is closed.**

`7 / 9` predictions held. The two misses, `S7` and `S8`, are both **mine**, and neither is a defect in the
format: `S8` mis-stated a boundary by one, and `S7` assumed a symmetry the format does not have — and should not.

This is the first thing in the route that closes by finishing rather than by refusing.

## 1. The format

A plate is one little-endian `uint32`:

```
word = (n << 2) | k        k = p // N,  n = p % N        p = kN + n
```

`2` bits for the component, `30` bits for the axial index. For `DEMO-1` (`M = 4`, `N = 1,069,767,441`) that is
**all 32 bits used, no padding, no slack** — which is why `A1` and `A2` are exact rather than toleranced.

The only nontrivial claim is `p = kN + n`: it makes `(k, n) ↔ p` a bijection and costs **zero stored bits**
(`CARD-ONLY`). Since `p` is also the Hilbert index, file order *is* curve order, and locality is free.

## 2. What was measured

| id | criterion | threshold | measured |
| --- | --- | --- | --- |
| `A1` | round trip exact | `0` mismatches | **0** — exhaustive over `16,777,216`, plus `2,000,000` at `DEMO-1` |
| `A2` | bytes per plate | exactly `4` | **`17,116,279,056 B` = `15.9408 GiB`** |
| `A3` | contiguity | `1.000000` | **`1.000000`** — `0` non-adjacent pairs in `16,777,215` |
| `A4` | median `|Δn|` | `≤ 1` | **`1`**, with `3` wraps |
| `A5` | encode | `≥ 10 MB/s` | **`429.1 MiB/s`** |
| `A6` | decode | `≥ 10 MB/s` | **`1,015.4 MiB/s`** |
| `A7` | full pass | `≤ 1800 s` | **`38.0 s`** encode, `16.1 s` decode |

`A1` is exactness by **count**, not by rate. A bijection on `[0, P)` either gives `P` distinct words and `P`
distinct recoveries or it does not; "99.999%" would be a category error dressed as a tolerance. `T12` was chosen
so that `P = cells` exactly, so the exhaustive test covers the whole address space with no vacuum tail in which
an off-by-one could hide.

`A3 = 1.000000` is not a good score, it is a **definition**: the Hilbert curve is a Hamiltonian path on the cell
grid, so consecutive addresses land on Chebyshev-adjacent cells with no exceptions. The comparison against raster
is the only informative part, and it is a much smaller gap than the record previously implied:

| ordering | contiguity | non-adjacent pairs |
| --- | --- | --- |
| Hilbert | `1.000000` | `0` |
| raster | `0.999756` | `4,095` |

The archived `0.9961` belongs to a `S = 256` grid. At `S = 4096` the analytic value is
`1 − (S−1)/(cells−1) = 0.999756`, measured exactly. **I amended `S9` before measuring**, because the original
threshold had transferred a figure across grid sizes — the same class of error as round 27's `P10`.

`A4` is a weak criterion and the run says so: `|Δn|` is large exactly at a component boundary, where `n` wraps
while the curve still moves one cell. It is kept because a large `|Δn|` usefully signals "a boundary was
crossed"; it is not an adjacency metric, and `A3` is.

## 3. The asymmetry — a property of the format I had not predicted

I predicted decode ≈ encode, on the reasoning that "decode is the same operations reversed." Measured:

```
encode   k = p // N ,  n = p % N      integer division, ~20-40 cycles   ->   429 MiB/s
decode   k = w & 3  ,  n = w >> 2     two bit operations, ~1 cycle      -> 1,015 MiB/s
```

**`2.37×` in decode's favour.** The format is deliberately asymmetric: the **writer** pays the division once, the
**reader** pays almost nothing. For a `15.94 GiB` file written once and read many times, that is the right way
round — and it is an argument for the bit-field layout that I had not made when I chose it.

So `S7` is refuted and the refutation is the finding. `A7` itself passed: `38.0 s` against a `1800 s` ceiling.

## 4. The boundary, and my off-by-one

`S8` predicted that `N ≥ 2^30` would be rejected. Measured: `N = 2^30` is **accepted**, and that is correct.

`n` ranges over `0 … N−1`, so `N = 2^30` gives `n_max = 2^30 − 1`, and

```
(2^30 − 1) << 2 | 3  =  2^32 − 1   exactly
```

The admissible bound is `N ≤ 2^30`, not `N < 2^30`. The guard enforces exactly that, and the spec's wording bounds
`n`, not `N`, so the spec is right and my prediction was wrong by one. `N = 2^30 + 1` is rejected correctly.

The demonstration I wrote to show the corruption evaluates `n = 2^30` — an input the guard makes unreachable. It
is **vacuous**, and it is left in the run as the record of the mistake, together with a broken sentence in it that
compares `1` to `1`.

## 5. `GD9` — the objective, now operational

`D-7` said the objective is **fidelity + locality**. The format shows what that means concretely:

- **fidelity is not optimised, it is constrained.** `A1` exact, `A2` exact. There is nothing to trade. A
  serialization that loses a plate is not a worse serialization, it is not a serialization.
- **locality is the objective.** Maximise `A3`, minimise `A4`.

That asymmetry is why the 32-cell matrix was the wrong instrument. The matrix scored **readability**, which is not
in the objective and cannot be met (`MR1.0`, `0` of `32`). The objective's two terms are one hard constraint and
one ordering, both measurable in a single pass over the file. **A quantity that cannot trade against a hard
constraint is not a metric of this route.**

`GD9` is closed in this form. It is not closed by declaring fidelity and locality acceptable — it is closed by
showing that one is a constraint, the other is an ordering, and both have locked numbers.

## 6. Decisions

- **`D-13`** **`GD9` closed.** Objective = (fidelity constrained exactly) + (locality maximised), with
  `A1`/`A2` as the constraint and `A3`/`A4` as the ordering. *Reverse on* a route that admits a fidelity target
  rather than a fidelity constraint — i.e. one that will trade a lost plate for a smaller file.
- **`D-14`** **`deposit_serial_v1` is the format of record** for `DEPOSIT-SERIAL`. Its acceptance criteria are
  locked by digest; a future implementation is conformant only if it reproduces `A1`–`A7` against that digest.
  *Reverse on* a revision of the spec, which must be a new version with its own lock, not an edit.

## 7. What this does not buy

Restated so the result cannot be quoted for more than it is:

- **The word carries `(k, n)` and nothing else.** `10` of `12` declared parameters are still absent
  (`DEPOSIT-BLIND`). The `G6`/`DC2` blocker is untouched, and it remains the critical path (`D-6a`).
- **The deposit is not readable** (`D-2`). `A3` measures adjacency of *records*, not of anything visible. The
  locality is in the file and stays in the file.
- **No body `σ`.** `GD11` remains parked for a body-depositing line.

## 8. Errata

| id | defect | status |
| --- | --- | --- |
| `E1` | `S8` mis-stated the admissible bound by one (`N ≤ 2^30`, not `N < 2^30`); its corruption demo evaluates an unreachable input and is vacuous; its closing sentence is a formatting bug. Also `header_check`'s message says `1073741823` where the check fires at `1073741825`. | guard and spec both correct; prediction REFUTED; not repaired, so the run stays the record |
| `E2` | `S7` assumed decode ≈ encode. Encode divides, decode shifts; measured `2.37×`. | REFUTED; the asymmetry is the finding |
| `E3` | `S9`'s original threshold transferred raster contiguity across grid sizes (`0.9961` at `S=256` → `0.999756` at `S=4096`). | amended **before** measurement; disclosed in the registration |
