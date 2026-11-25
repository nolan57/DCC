# `RL-1` — `Q3` at `θ_fast` on a scene that carries content

**Round**: 48 (queue item `RQ-12`)
**Written**: 2026-11-23, **before** `src/route/ladder_r1.py` exists in its final form
**Spec**: `docs/specs/relaxation_ladder_v1.md` §2 (`RL-1`), §5 measurement 1; `docs/specs/intrinsic_structure_tiers_v1.md` §5
**Why this and not something else**: `MR1.3` records that the instrumented channel was never evaluated on a scene carrying
2D-ified content. `L3`'s emptiness at `C1` is therefore a statement about `θ_eye` only — `q = 0` by construction. This is
the first round that evaluates a `θ` with `q > 0` on the deposit's own scene class.

---

## 1. What is being measured

`Q3 = log₂(1 + C_ξ · q / C_eye)`, with `ξ`, `C_ξ` from the locked estimators and `q` the channel factor. Three
declarations of `q` are computed on the same scenes:

| declaration | `q` | what it means |
|---|---|---|
| `θ_eye` | `0` | the naked-eye reflected channel — the frozen corollary (`2H/c = √2·t_rip`) |
| `θ_ideal` | `1` | the spec's normalisation: a declared instrumented channel with an adequate budget |
| `θ_fast` | `q(θ)` derived | the 284 eV transmission channel, with `q` limited by the **registered** photon chain |

`q(θ_fast) = min(1, (C_ξ / C*)²)` where `C*` is the scene contrast at which the registered requirement is exactly met.
This is not a new formula: it is `N = (SNR/C)²` inverted against the registered `N_available`, both taken from
`runs/ROUTE/p2_clock_results.txt`.

## 2. The arithmetic the round turns on

The registered chain (`p2_clock_results.txt` P2-3, P2-4):

```
N_required(1e-7) = (3 / 1e-7)^2      = 9.000e14  photons per resolution element
flux_required                        = 9.539e31  m^-2 s^-1
t_rip                                = 8.2553e-9 s
=> N_required per frame              = 7.8747e23  m^-2
full sun @ 2.25 eV                   = 2.7740e21  m^-2 s^-1  -> 2.2900e13 m^-2 per frame
implied resolution element           = 9.000e14 / 7.8747e23 = 1.143e-9 m^2  (side 33.8 um)
N_available per element              = 2.2900e13 * 1.143e-9 = 2.617e4
shortfall(1e-7)                      = 9.000e14 / 2.617e4   = 3.4387e10      <- the registered number
```

Therefore, **for any scene contrast `C`**:

```
shortfall(C) = 3.4387e10 * (1e-7 / C)^2
C*           = the C at which shortfall = 1  =  1e-7 * sqrt(3.4387e10) = 1.854e-2
```

## 3. Predictions (registered before the program runs)

| id | prediction | falsified if |
|---|---|---|
| `X1` | `L3` returns **NO-VERDICT** at `p = 8` because `ξ/h = 1.66 < 2`, while `L0` (`0.7230`) and `L2` (`0.5155`) both **PASS** on the same scene | `L3` returns a number at `p = 8`, or `L0`/`L2` fail there |
| `X2` | at `θ_ideal`, `Q3 ≥ 2` at **both** `p = 16` and `p = 32`, i.e. `C_ξ ≥ 0.03` | either falls below `2.0` |
| `X3` | at `θ_eye`, `Q3 = 0.000` exactly at every pitch that has a verdict | any non-zero value |
| `X4` | `3.4387e10` belongs to contrast **`1e-7`**; evaluated at the record's own compositional contrast `1e-3` the same chain gives **`343.9`** (2.54 orders), i.e. the ladder's attribution to `1e-3` is **8 orders** too large | the program cannot reproduce `3.4387e10` from the `1e-7` row, or the `1e-3` value is not `343.9` |
| `X5` | the legibility threshold (`C ≥ 0.03` for `Q3 = 2` at `q = 1`) sits **above** the detection threshold `C* = 1.854e-2`, by a factor `1.618` in contrast / `2.618` in photons — so the flux gate **cannot bind independently of `L3`** | `C* > 0.03`, or the ratio is not `1.618 ± 0.001` |
| `X6` | at the plate class's **measured** `C_ξ`, `q(θ_fast)` saturates at `1`, hence `Q3(θ_fast) = Q3(θ_ideal)` on every pitch with a verdict | any pitch where `C_ξ < C*`, i.e. `q < 1` |

**The two predictions at risk are `X2` and `X6`** — both depend on a `C_ξ` that has never been measured on this class.
`X1`, `X4`, `X5` are arithmetic on numbers already in the record; they are registered so that a reader can see I did not
choose them after seeing the table.

## 4. What the round is *not* allowed to claim

- Not a new physics result. Every number is either a locked estimator applied to a declared synthetic field, or
  arithmetic on `runs/ROUTE/p2_clock_results.txt`.
- Not a claim about the deposit. The plate class is a **declared stand-in** for the deposit's geometry (`s/p = 0.75`
  vs the deposit's `0.7300`); `DEPOSIT-BLIND` still holds and `MR1.6` still caps every verdict at `(M, N, σ)`.
- Not a licence to re-price a rung *because it worked*. §5 re-prices §3 of the ladder spec **because its arithmetic
  contradicts its own prose**, and that re-pricing applies to every rung equally, before any of them is executed.
- Not a scene for `V4`. The plate class is **severed** (isolated plates, no bond); `V4` needs a *bonded* scene and
  `KIN-DYN` supplies no constitutive law. `V4` stays unanswered after this round.

## 5. Product owed

`runs/LADDER/r1_observer_results.txt` — identity check against the archived estimator constants; the budget table; the
`Q3` table at three `q`; the `shortfall(C)` table; the corrected `Φ` for `RL-1`/`RL-2`/`RL-3`; `X1`–`X6` each
`CONFIRMED` or `FALSIFIED`.

---

## Erratum E1 — the camera slot (RETRO-DECLARED, 2026-11-23)

**Appended**, not registered: `X1`–`X6` above are untouched, and this entry may not be read as though the pose
below had been declared before the run.

`docs/specs/theta_camera_v1.md` (round 51) makes the viewing geometry `G = (n̂_v, δ_v)` a mandatory slot of `θ`.
This round does not have one, and not by oversight:

**The pose.** **Absent.** `src/route/ladder_r1.py` carries `q` as a scalar gate/budget factor (`Q_INSTR = 1`,
`Q_REFL = 0`) and no angular variable anywhere — no `θ_i`, no `n̂_v`, no acceptance. The estimator cannot
express a viewing direction, so the round did not leave `G` undeclared; it *integrated it out*.

**What that costs `Q3 = 5.737`.** Nothing, as a measurement — and everything, as a claim. The number is a
statement about the **channel** (`q = 1` vs `q = 0`) on a fixed scene: legibility is nonzero once the gate
budget is adequate, which is what `MR1.3` had never been tested on. It is **not** a statement that any viewing
geometry supports 5.737, because the estimator has no geometry in it. Under `theta_camera_v1.md` §4 this
registration would now be *refused*; under §0 clause 3 the retro-declaration may not repair it, so the
consequence is recorded rather than removed:

> `r1_observer_results.txt` §3 may be cited for `Q3(q)` and for the `C*`/flux chain. It may **not** be cited
> as evidence that the scene is legible from anywhere.

Escape, if the programme wants it, is a re-run with `G` inside the estimator — `RQ-20`, not this note.
