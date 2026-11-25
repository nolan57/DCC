# Pre-registration — `deposit_serial_v1` conformance

**Registered**: 2026-11-22, before any code in this round ran.
**Spec under test**: `docs/specs/deposit_serial_v1.md`, sha256 `e3c2a555a91b42a5c7036aa0685db17c90e3c4a7443ed66251b735004a6194d9`
(`runs/SERIAL/serial_lock.json`).
**Criteria**: `A1`–`A7` in §4 of the spec, locked **before** these predictions were written and before any
measurement.

---

## Test deposits

| id | `order` | `S` | `cells` | `M` | `N` | `P = M·N` | purpose |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `T12` | `12` | `4096` | `16,777,216` | `4` | `4,194,304` | `16,777,216` | **exhaustive** round trip, full canvas |
| `DEMO-1` | `16` | `65,536` | `4,294,967,296` | `4` | `1,069,767,441` | `4,279,069,764` | full-scale magnitudes, sampled |

`T12` is chosen so that `P = cells` exactly: every cell is a plate, so an exhaustive round trip covers the whole
address space with no vacuum hole to hide an off-by-one at the tail.

## Predictions

| id | prediction | falsified by |
| --- | --- | --- |
| **S1** | `A1` on `T12`: **0** mismatches over all `16,777,216` records. The map is a bijection by construction, so any mismatch falsifies the format, not the tolerance. | `≥ 1` mismatch |
| **S2** | `A1` at `DEMO-1` magnitudes: **0** mismatches over `2,000,000` uniformly sampled addresses, `p` drawn **without replacement** (deduplicated — a with-replacement draw would manufacture birthday collisions, the defect recorded in round 33 `E2`). | `≥ 1` mismatch |
| **S3** | `A2`: exactly `4` bytes per plate; file size exactly `4P = 17,116,279,056` bytes for `DEMO-1`, which is `15.9408 GiB`. | any other figure |
| **S4** | `A3`: contiguity `= 1.000000` **exactly** over all `16,777,215` consecutive pairs of `T12`. The Hilbert curve is a Hamiltonian path on the cell grid, so every consecutive pair is Chebyshev-adjacent, with no exceptions. | any pair at Chebyshev distance `> 1` |
| **S5** | `A4`: median `|Δn| = 1`. Exception: `3` pairs out of `4,279,069,763` have `|Δn| = N−1 = 1,069,767,440`, at `p ≡ N−1 (mod N)`, where `k` increments and `n` wraps. `n`-jumps are therefore **not** the adjacency metric — `A3` is. | median `≠ 1`, or a different exception count |
| **S6** | `A5`: encode throughput in `[150, 1200] MB/s` single-threaded. The encoder is integer-only (`k = p//N`, `n = p%N`, `word = (n<<2)|k`) and never calls `d2xy` — the curve is a property of the *ordering*, not of the encoder. | outside that band |
| **S7** | `A6` ≈ `A5` (decode is the same operations reversed), and `A7`: one full pass over `17.116 GB` in `[15, 150] s`. | outside that band |
| **S8** | The format accepts `N < 2^30` and **rejects** `N ≥ 2^30` at header-write, since `word = (n<<2)|k` would silently overflow into the `k` field. A guard that is absent is a silent-corruption defect, so this is tested rather than asserted. | accepts `N = 2^30` |
| **S9** | `A3` for this format strictly beats raster order. ~~predict raster `≤ 0.997`~~ **AMENDED BEFORE MEASUREMENT**: the archived `0.9961` is a `S = 256` figure and does **not** transfer to `S = 4096`. Raster contiguity is `1 − (S−1)/(cells−1)`, which at `S = 4096`, `cells = 2^24` is `0.999756` — still below `1.000000`, but by `2.4e-4`, not `4e-3`. Predict curve `1.000000`, raster `0.999756`. | curve `≤` raster, or raster `≠ 0.999756` |

> **Amendment note.** `S9` was rewritten **before** any code ran. Its original threshold was copied from a
> different grid size, which is the scale-transfer error this project has already recorded once (round 27 `P10`:
> predicted `8.19`, measured `8.571`, from taking one object's maximum for another's). The comparison it was
> meant to make — curve strictly better than raster — is unaffected; only the magnitude was wrong.

## What each outcome licenses

- `S1`–`S5` hold ⇒ the format conforms and `A1`–`A4` can be cited as met. Since `A1`/`A2` are exact rather than
  toleranced, "met" is a statement about a count, not about a margin.
- `S6`/`S7` hold ⇒ `A5`–`A7` met, and the `15.9408 GiB` deposit is a practical file on the declared hardware.
- `S8` fails ⇒ the format is unsafe at its own boundary and must not be used with `N ≥ 2^30`; this is a defect in
  the spec, and it would be recorded as such rather than fixed silently.
- `S9` fails ⇒ the locality claim (`SFC-INDEX`) does not transfer to this file layout, and `A3` would be measuring
  nothing that distinguishes the format from a raster dump.

## Declarations fixed in advance

- Chunk size for streaming: `8,388,608` records (`32 MiB`), so the working set is cache-friendly and the
  measurement is not dominated by allocation.
- `d2xy` is the standard bit-twiddling form, vectorised over `uint32`; it is used **only** for `A3`/`A4` and `S9`,
  never in the encoder path, because `p` is already the index.
- Throughput is wall-clock, single process, single thread, `numpy` only. No `numba`, no `C`.
- No threshold is moved after measurement. A miss is reported as a miss.
