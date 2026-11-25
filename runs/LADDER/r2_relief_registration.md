# `RL-2` pre-registration — the contrast of a relief scene against a flat one

**Registered**: 2026-11-23, before `src/route/ladder_r2.py` exists.
**Queue item**: `RQ-13`, `docs/program/round_queue_v1.json`.
**Authority for the question**: `docs/specs/relaxation_ladder_v1.md` §3 lever table and erratum `E1` item 2;
`runs/LADDER/r1_observer_results.txt` §3b. `RL-2` passes `L3` at `Q3 = 2.000000` **exactly**, i.e. by nothing,
on a contrast (`3e-2`) that no product in `runs/` measures.
**Product**: `runs/LADDER/r2_relief_contrast_results.txt`.

---

## §1 What is being decided

`RL-2` relaxes flatness: `L_z` constant → `L_z(x)`. Its price is declared as `V = ε = relief/pitch`, and its
claim is that relief "buys **+2.9 orders**" of photon flux through the `∝ 1/c²` lever, taking the criterion
contrast from `1e-3` (the near-mirror) to `3e-2` (a "topographic edge, oblique").

Three things are unstated in that sentence, and this round measures all three:

1. **Which environment.** A mirror has no diffuse shading term. Contrast on a specular surface exists only
   where the environment's radiance varies with direction. `θ` = (aperture, gate, band, distance) does not
   carry an environment term, so the rung's price is a function of a variable the rung does not declare.
2. **How contrast scales with `ε`.** The lever is written as a `1/c²` law in contrast, but nothing states
   `c(ε)`. If `c` saturates, the lever cannot be walked in `ε`.
3. **What bounds `ε`.** `ε` is free unless something forbids relief. The deposit's own clearance does:
   `sup d₃D = √((2r₄)² + (H+relief)²) ≤ pitch` (`DEPOSIT-DICHOTOMY`), so relief has a hard ceiling.

## §2 The model, declared before the numbers

Scene = one isolated plate of side `s = 12` cells on a `p = 16` lattice (the `PA-16` instance of
`runs/MATRIX2/plate_array_results.txt`), grid `128`, cell `= pitch/p = 0.02500625 m`. Relief is a
single-scale corrugation normal to the sheet:

```
z(x) = (a/2)·sin(2πx/λ),   λ = 4 cells = 0.100025 m,   α(x) = dz/dx = (πa/λ)·cos(2πx/λ)
```

`s` spans three corrugation periods, so the plate is not one fringe. Contrast is the locked estimator
`structure_tiers.q3(u, ξ, q)`'s `C = std(DoG_ξ u) / mean|u|`, evaluated at a **fixed** band
`ξ = λ = 32 px` for every `a` — the flat and the relief scenes are compared in the same band, which is what
"identical illumination and band" requires. `C_eye = 0.01`, `Q3 = log2(1 + C/C_eye)`, threshold `2.0`
(all read from `runs/MATRIX/threshold_lock.json`; nothing here writes a threshold).

Four environments, all at the same incidence `θ_i`:

| id | environment | image | note |
|---|---|---|---|
| `E1` | uniform dome, `L(θ) = L₀` | `I = u` | a perfect mirror under uniform radiance is invisible — this is an identity, not a model choice |
| `E2` | collimated disc, angular radius `β = 4.65e-3 rad` (solar) | `I = u·1{\|2α\| < β}` | the record's own "full sun" baseline |
| `E3` | collimated, `β = 4.65e-3`, oblique `θ_i = 60°` | `I = u·1{\|2α − 2tanθ_i·…\| < β}` — same as `E2`, geometry only | separates "relief" from "illumination" for `RQ-14` |
| `E4` | Lambertian diffuse (NOT this material) | `I = u·max(0,cos(θ_i+arctan α))/cos θ_i` | the model implicitly assumed by any "topographic shading = 3e-2" statement |

`E4` is carried because it is the model behind the number, not because the deposit is diffuse:
`visualization_null_result_v1.md` §2 fixes the surface as a near-mirror (`|ΔR| = 1e-3`).

## §3 Predictions

| id | prediction | falsified if |
|---|---|---|
| `Y1` | `E1`: `C_relief(a) = C_flat` for **every** `a`, ratio `1.000000` to `1e-12`. Relief under uniform radiance is optically null; the residual contrast is the plate perimeter, identical in both | any `a` at which the ratio departs from 1 by more than `1e-12` |
| `Y2` | `E2`: `a*(C = 0.03)` lies in `[40, 150] µm`. The transition is at `α_max = β/2`, i.e. `a = βλ/(2π) = 74 µm` | `a*` outside that window |
| `Y3` | `E2`: at `a = 1 mm`, `C_relief > 0.5` — the glint channel saturates well below any "relief" an engineer would call relief | `C_relief(1 mm) ≤ 0.5` |
| `Y4` | `E4` at `θ_i = 60°`: `a*(0.03)` in `[0.2, 1.0] mm`, and `C ∝ a^k` with `k ∈ [0.8, 1.2]` in the decade below `a*` | outside either bound |
| `Y5` | `a*(E4)/a*(E2)` ∈ `[3, 15]` — the two models disagree on the number but not by orders | outside |
| `Y6` | clearance ceiling `ε_max = (√(pitch² − (2r₄)²) − H)/pitch = 0.3183` with `r₄ = 0.0900 m`, `H = 0.2300 m` (`docs/specs/demo_object_v1.md`; `sup d₃D = 0.292062 m` is consistent with these two and with nothing else) | computed `ε_max` differs by `> 1e-4` |
| `Y7` | `a*/pitch ≈ 1.8e-4`, so `> 99.9%` of `RL-2`'s declared `V` range `[0, ε_max]` is optically indistinguishable from `ε = 0` | `a*/pitch > 3e-3` |

## §4 What this round does not do

- It does not measure the deposit. `DEPOSIT-BLIND`, `MR1.6` untouched; the scene is a declared plate.
- It does not re-price `RL-2` after the fact (ladder §"rule that binds the whole file"). If the measurement
  contradicts `3e-2`, that becomes an **erratum**, and the rung table stays as written.
- It does not decide `RQ-14` (oblique vs normal). `E3` is included only to keep `E2`'s geometry honest.
- It adds no threshold and revises no tier.

## §5 One factual check carried alongside

`r1_observer_results.txt` §1 states `t_rip = 8.255290e-09 s (H = 1.75 m, the deposit's own height)`.
`DEMO-1` declares `H = 0.2300 m`, giving `t_rip = √2·0.2300/c = 1.0847e-9 s` — a factor `7.611` smaller.
The `3.4387e10` chain's per-frame flux scales linearly in `t_rip`, so the shortfall at fixed contrast would
be `7.611×` **larger** under `H = 0.2300`. This is recorded, not repaired: `RQ-12`'s numbers stand as
printed and the discrepancy is an erratum candidate for whichever height the programme decides is the
deposit's.

---

## Errata

**E1** *(appended before the measurement, 2026-11-23; predictions `Y1`–`Y7` above are untouched)*

§2 fixed the metric as the locked estimator's `C = std(DoG_ξ u)/mean|u|` at `ξ = λ`. A smoke test of the
instrument at `a = 1e-6 m` — three decades below every predicted `a*`, so no threshold had been evaluated when
this was found — returned `C ≈ 1e-3` on an image whose fringe amplitude is 0.56. The reason is arithmetic:
`DoG_ξ` uses `σ = ξ/2 = 2 cells` on a structure whose period is `4 cells`, attenuating the fundamental by
`exp(−2π²σ²/λ²) = 7.2e-3`. The registered metric would therefore report a corrugation at 0.7% of its own
amplitude, and would report *zero* for the terraced form. That is a filter artefact, not a measurement.

**Metric actually used**: the Weber contrast over the plate interior,
`C_w = std(I)/mean(I)` on the mask `u > 0`. This is the quantity `C_eye = 0.01` is a threshold *for*, and it is
the one the predicted numbers in `Y2`/`Y4` were derived from (geometric optics, not filter output). The
registered `DoG` value is still printed for every case, in its own column, so the substitution is visible rather
than silent. Because the erratum predates the run, the product reports the ordering from this block, not from
mtime.

**Added to the model** (not to the predictions): the relief *form* is carried as a second axis, `S` (sinusoidal)
and `T` (terraced — the literal "topographic edge" of the ladder's own phrase, riser width declared as one
pixel). The ladder prices `RL-2` by amplitude alone; if contrast depends on form, that is a finding about the
price variable, and it cannot be stated without the axis.

---

**E2** *(`RETRO-DECLARED`, appended 2026-11-23 after the run; `Y1`–`Y7` above and `E1` are untouched, and the
product `runs/LADDER/r2_relief_contrast_results.txt` is not edited)*

`docs/specs/theta_camera_v1.md` (round 51) makes the viewing geometry `G` a mandatory slot of `θ`. Recovered
from `src/route/ladder_r2.py`, this round used **two different poses in one table**, and neither was written
down:

| columns | `θ_i` passed to `image()` | pose recovered | label |
|---|---|---|---|
| `E1`, `E2`, `E3` | `0.0` (`ladder_r2.py:177`, the `else` branch) | camera coaxial with the source, i.e. on the specular ray | `G_A` at the degenerate point — indistinguishable from `G_B` there |
| `E4` | `60.0` (the `if env == 'E4'` branch) | source at 60°, camera left on the surface normal — which is exactly what the `1/cos θ_i` normalisation asserts | `G_B` |

**Why nobody noticed.** At `θ_i = 0` the mirror of the normal *is* the normal, so `G_A` and `G_B` coincide.
The table's three largest columns sit on that degeneracy; only the `E4` column leaves it, and `E4` was already
excluded on independent grounds (the diffuse model, `r3` §6). So the missing slot had no observable
consequence in `E1`–`E3` — which is the reason it was missing, not a reason it did not matter. Round 50 broke
the degeneracy and the difference turned out to be a blackout.

**What E2 narrows (this is the substantive part).** `C = 0.280` held for 3.6 decades under `G_A`. Under a
fixed camera the same scene keeps it only while the specular window is on the plate, i.e. within **3.31°** of
normal incidence (`runs/LADDER/r3_illumination_results.txt` §2). The correct citation is therefore:

> `C = 0.280` (terraced, `E2`, `β = 4.65e-3`) is the contrast seen by a **source-tracking camera**; a fixed
> camera sees it within `3.31°` of the normal and sees a blackout beyond.

**What E2 does not do.** It does not move `Y1`–`Y7`, does not re-price `RL-2` (`V = ε` stands — the plateau is
set by riser width and environment, and neither is a camera), and does not re-open `E1`'s metric substitution.
The plateau is a property of the scene; it is now a property of the scene *as viewed from somewhere*, which
is what `θ` was always supposed to mean.
