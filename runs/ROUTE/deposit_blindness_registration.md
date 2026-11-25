# `DEPOSIT-BLIND` — is the deposit a function of the object, or of the enumeration?

**Registered**: 2026-11-22, **before measurement**.
**Authority**: governor delegation — *"from here on you decide; there are no new ideas on this side"* ("from here on you decide;
there are no new ideas on this side").
**Status**: predictions locked. Nothing below may be edited after `deposit_blindness_results.txt` exists.

---

## 0. Why this and not another submission

Thirty-one rounds have adjudicated *statistics* computed on the deposit. Every one closed. The pattern is now
itself the finding, and it suggests the tests were aimed one layer too high: a statistic is a function of the
canvas, so if the canvas does not contain the object, no statistic on it can find the object. This round asks the
prior question and asks it in a form that can fail:

> **Is `D2`'s deposit a function of the object, or only of the object's enumeration?**

The question is decidable by construction, not by threshold. If the deposit is a function of `(M, N)` alone, then
every gate that closed did so for one reason, and the reason is not statistical.

## 1. The claim under test

`DEMO-1` (`demo_object_v1.md`, hash-locked `afe855c2…4633`) declares:

```
piece index   p = k·N + n        k = component 0..3,  n = layer 0..N-1
site          d = hilbert(p)     exact Hilbert curve, order 16
```

**Claim.** The map `O ↦ deposit` factors through `(M, N)`:

```
deposit(O) = F(M(O), N(O)),   F independent of every other parameter of O
```

**Consequence if true.** `N = floor(H/δ)`, so `deposit(O) = F(M, floor(H/δ))`: the canvas is a function of the
object's **height** and **shell count** and of nothing else. All four radius laws and all four areal densities
— ten declared parameters — are absent from it.

## 2. Predictions (locked)

Notation: `O1…O6` are six objects with **identical** `(M, N) = (4, 1,069,767,441)` and different everything else.
`NC1`, `NC2` are negative controls that must **change** the deposit, so that a "collision" result is not vacuous.

| id | statement | mechanism | expected |
| --- | --- | --- | --- |
| **P1** | The deposit **constructor** reads no object parameter | pass the constructor a `Tripwire` mapping that raises on any read; it must complete without raising | `0` reads |
| **P2** | The **painter** does read object parameters, and at ≥3 distinct keys | same tripwire on the painting path | raises; keys include two or more of `r1, r2_0, r2_a, r3_0, r3_a, r4` |
| **P3** | `O1…O6` give **byte-identical** deposits | digest over `10⁶` sampled sites + 8 boundary sites | all 6 digests equal |
| **P4** | `NC1` (H halved) changes the deposit | `N' = floor(0.1150/δ) = 534,883,720`, `pieces' = 2,139,534,880` | digest differs |
| **P5** | `NC2` (M=5 at H=0.2300) is **infeasible** | `pieces = 5·N = 5,348,837,205 > cells = 4,294,967,296` | rejected; `H ≤ 0.184699 m` |
| **P6** | The painted figure's brightness is **100% object-supplied**, and the only canvas-supplied brightness is `n/N` | hold hue (`k`) and the brightness *encoding* fixed; substitute `n/N` for `area`; count distinct sources | `0` of the painted values come from the canvas alone |
| **P7** | `I(canvas ; r₄) = 0` bits across a `30.25×` spread in cut area | `O1` vs `O2`: `r₄ = 0.0900 → 0.4950`; cut area `2.7222e7 → 8.2357e8 m²` | `0` bits; digest equal (⊂ P3) |
| **P8** | Visible / total declared parameters = `2 / 12` | visible `(M, N)`; invisible `r₁, r₂₀, r₂ₐ, r₃₀, r₃ₐ, r₄, ρ₁…ρ₄` | `2/12` |
| **P9** | The injective-vs-visible dichotomy reduces to an exact decimation factor | side ≥ `⌈√pieces⌉ = 65,414.6` ⇒ `2¹⁶`; display `2⁹`; ratio `2¹⁴` | `16,384` exactly |
| **P10** | No single scale factor relates the deposit to the object | `sup d₃D = √((2r₄)²+H²) = 0.292062 m`; `inf d₂D = pitch = 0.4001 m`; supports disjoint | no `s` exists; `sup/inf = 0.7300` |
| **P11** | The surviving positive is a serialization, not an image: `4.279e9` plates × 4 B | `4,279,069,764 × 4 B` | `15.9409 GiB` |
| **P12** | My round-28 canvas panel was a **legitimate** read of `k` and `n`, and an **illegitimate** source for brightness | `shell_of = dc // N_LAYER` (canvas); `area_of = areas(...)` (object) | both true; recorded as a self-defect of *presentation*, not of code |

## 3. Falsifiers

The claim dies if any of these hold, and I will report it unedited if so:

1. **P1 raises.** Any read at all means a geometric channel exists and the blindness claim is false.
2. **P3 splits.** One differing digest among `O1…O6` means the constructor is object-sensitive.
3. **P4 or P5 fails.** Either the negative control does not move (test has no power) or `M` is not free
   (the parameter space is not 2-dimensional).
4. **Hilbert self-check fails.** If the vectorised `d2xy` disagrees with a scalar reference at `n = 8, 16`, the
   figure is invalid and nothing above it may be read.

## 4. Scope limits, declared now

- `P3`'s digest is over a **sample** (`10⁶` of `4.295e9` sites) plus boundary sites, not the whole canvas: the
  full array is `34 GiB`. The structural claim rests on `P1`, which is exhaustive; the digest is corroboration.
- No physical claim is made. `DEMO-1` remains a declared geometry; `Annex B` §B.3 stands.
- This registration may not contain a threshold. It contains none.

*Content generated by AI*
