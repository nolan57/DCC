# Scene card — W1 / row 2 (`C1 C2 ¬C3`), W1-ROW2-ARTIFACT-01

**Status**: O0-ARTIFACT (pre-registration, stage A). Nothing is rendered yet; the hashes below
are the lock that stage B verifies before drawing.
**Programme**: `docs/program/RESEARCH_PROGRAM_v1.md` v1.1.1, sections 2.5, 2.6, 4.2–4.8, 6.1.
**Created (UTC)**: 2026-11-25T02:54:43Z

---

## 1. Row and scene class

| field | value |
|---|---|
| row | 2 — `C1 C2 ¬C3` |
| scene class | `CONSTRUCTIVE` (no counterfactual is used; `C3` is violated, not held) |
| `C1` | **HELD** — layer→site is a declared bijection; deposit volume = swept volume, residual 0 |
| `C2` | **HELD** — no map is applied; the intralayer (x,y) identity is used, det J = 1 |
| `C3` | **VIOLATED** — a 3 ns transient ends the 2D state; the lifetime is IMPORTED, not derived |

`C3` consequence at each keyframe (the state is fixed; only the consequence moves):

| keyframe | t (ns) | z front (m) | sheets | fragments | decayed fraction of deposit |
|---|---|---|---|---|---|
| `t0` | 0.000 | 0.0000 | 0.0000e+00 | 0.0000e+00 | 0.000 |
| `t_mid` | 4.099 | 0.8690 | 4.0419e+09 | 5.8890e+09 | 0.147 |
| `t_end` | 8.199 | 1.7380 | 8.0837e+09 | 1.1778e+10 | 0.598 |

The 3 ns transient is shorter than the 8.1987 ns sweep, so the last frame cannot show a surviving
deposit: everything swept earlier than `t_end − τ` has already left the 2D state. That is the
`¬C3` consequence, and it is why this row is published as an artifact rather than as a process
that completes.

## 2. Object

- height `H = 1.738 m`; registered volume `0.0601 m^3` (`front_sweep_v1` section 1 self-check).
- cross-section: the registered per-region table, **with the two-leg region counted twice**.
  The reconstruction integrates to `0.06111 m^3` = `1.0168 ×` the registered volume.
- density: declared uniform `1.0e+03 kg/m^3` for the mass ledger only; the field uses the phantom's
  tissue classes.

> **Reconciliation note (new).** `runs/FRONT/mid_sweep_frame_results.txt` N9′ reports the
> reconstruction as `0.04992 m^3`, 16.9% below the registered `0.0601`, and withholds the volume
> fraction for that reason. Counting the calf→thigh table as *per-piece* area (two legs) gives
> `0.06111 m^3`, i.e. `1.7%` above the registered value. The 16.9% gap is the missing factor of two,
> not a defect of the table. N9′ is not edited here (retirement rules: append, do not delete);
> this card records the explanation and stage B carries it into the results text.

## 3. Mechanism

| parameter | value | source |
|---|---|---|
| layer thickness `δ` | `0.215 nm` | `front_sweep_v1` §2 (mechanism property, not a knob) |
| components per layer | `1.457` | `front_sweep_v1` §1, 200² phantom |
| plate census | `1.18e10` | derived: `8.12e9 × 1.457` |
| front law | `z_f = min(H, v t)`, `v = c/√2` | `front_sweep_v1` §2 |
| `t_rip` | `8.198682e-09 s` | derived |
| transient `τ` | `3.0e-9 s` | **IMPORTED** `scifi_boundary_v1` (3–5 ns, lower bound) |

## 4. The map `M` (programme §2.6)

```
u(t) = M[ U(τ), φ(τ); 0 ≤ τ ≤ t ]
```

- **domain**: the swept slab `z ∈ [0, z_f(t)]`; material above the front is absent from `u`.
- **coordinates**: body cross-section `(x,y)` in m about the slice centre; array field in raster site index.
- **single-valued**: yes, by a declared bijection `layer k ↦ site k` (raster order).
- **competition**: none across layers. The `1.457` components are pieces of *one* layer sharing its
  single site, so a site holds 1 or 2 fragments of the same slice.
- **Markov**: no. History enters through the accumulated deposit and the decayed front. With the
  extended state `(deposited field, z_f, z_f − vτ)` the map is instantaneous; minimality is not proved.
- **discards**: mass (ledger), particle number (via mass), energy / momentum / phase (`OUT-OF-SCOPE`),
  per-site fragment multiplicity beyond the mean (recorded as a count, not a field).

## 5. Conservation ledger (programme §4.2.3)

| keyframe | `V_swept` (m³) | `V_deposited` (m³) | `V_decayed` (m³) | `V_live` (m³) | residual |
|---|---|---|---|---|---|
| `t0` | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.0e+00 |
| `t_mid` | 0.025534 | 0.025534 | 0.003766 | 0.021768 | 0.0e+00 |
| `t_end` | 0.061111 | 0.061111 | 0.036533 | 0.024578 | 0.0e+00 |

`C1` is held, so `V_deposited = V_swept` exactly and the residual is 0 by construction, not by
measurement. The decayed volume leaves the 2D domain as a boundary termination; the receiving 3D
reservoir's budget is `OUT-OF-SCOPE` because `τ` is imported. Energy, momentum and phase are not
modelled and are entered here as `OUT-OF-SCOPE` rather than omitted.

## 6. Observer `θ`

| slot | value | unit / domain |
|---|---|---|
| `q` | 1.0 | dimensionless photon budget |
| `band` | declared density channel | none |
| `gate` | 3e-09 | s |
| `aperture` | 0.1 | m |
| `distance` | 1.0 | m |
| `E` | flat, dark, room temperature | none |
| `G` | linear greyscale/violet density transfer, no tone curve | none |

`q = 1` is a declared instrument. `q = 0` (naked-eye reflected channel) is a different cell and is
reported in the profile as `Q3 = 0` by the authority's registration, not by this cycle.

## 7. Predicted profile (frozen before rendering)

| keyframe | field | tier | value | threshold | verdict |
|---|---|---|---|---|---|
| `t0` | plate | T0 | - | 0.50 | NOT-APPLICABLE |
| `t0` | plate | T1 | - | 4.00 | NOT-APPLICABLE |
| `t0` | plate | T2 | - | 0.50 | NOT-APPLICABLE |
| `t0` | plate | T3 | - | 2.00 | NOT-APPLICABLE |
| `t0` | canvas | T0 | - | 0.50 | NOT-APPLICABLE |
| `t0` | canvas | T1 | - | 4.00 | NOT-APPLICABLE |
| `t0` | canvas | T2 | - | 0.50 | NOT-APPLICABLE |
| `t0` | canvas | T3 | - | 2.00 | NOT-APPLICABLE |
| `t_mid` | plate | T0 | 0.997990 | 0.50 | PASS |
| `t_mid` | plate | T1 | 21.859849 | 4.00 | PASS |
| `t_mid` | plate | T2 | 0.909121 | 0.50 | PASS |
| `t_mid` | plate | T3 | 7.286999 | 2.00 | PASS |
| `t_mid` | canvas | T0 | 0.998918 | 0.50 | PASS |
| `t_mid` | canvas | T1 | 39.570019 | 4.00 | PASS |
| `t_mid` | canvas | T2 | 0.780002 | 0.50 | PASS |
| `t_mid` | canvas | T3 | 5.922202 | 2.00 | PASS |
| `t_end` | plate | T0 | 0.998918 | 0.50 | PASS |
| `t_end` | plate | T1 | 19.007245 | 4.00 | PASS |
| `t_end` | plate | T2 | 0.906169 | 0.50 | PASS |
| `t_end` | plate | T3 | 7.562601 | 2.00 | PASS |
| `t_end` | canvas | T0 | 0.998179 | 0.50 | PASS |
| `t_end` | canvas | T1 | 39.865420 | 4.00 | PASS |
| `t_end` | canvas | T2 | 0.739936 | 0.50 | PASS |
| `t_end` | canvas | T3 | 4.493217 | 2.00 | PASS |

Estimator: intrinsic_structure_tiers_v1 v1 (T0 sec.2, T1 sec.3, T2 sec.4, T3 sec.5). Reference ensemble: uniform iid, 16 realisations, seeds 4000..4015.
Threshold lock `sha256 = 1224458d58f179f8…`.

The prediction is a **freeze, not an independent forecast**: it is the same deterministic computation
run before any image is drawn. Its function is to stop the card being adjusted after the frame is
seen (programme §2.5(1)), not to forecast a measurement. Stage B must report any difference.

## 8. Effective-2D slots (programme §4.7)

| slot | value |
|---|---|
| model | Model B surrogate: infinite square well of width L_z = delta, electron mass |
| model status | SURROGATE -- the registered mechanism supplies no confining potential, so this Delta_E_z is a bound on a declared model, not the system's own level spacing |
| subsystem | conduction electrons of the deposited sheet only (declared n_e = 1.0e28 m^-3) |
| `ΔE_z` | `24.404 eV` = 3 pi^2 hbar^2 / (2 m_e L_z^2)  (infinite square well, first excitation) |
| `E_occ` | `max(E_F, k_BT) = 1.6925 eV` |
| `ε_z` | `0.000e+00` = exp(-Delta_E_z / k_B T): Boltzmann occupation of the first z excitation |
| internal bound | **PASS** |
| external excitation | **PASS** (`E_probe = 2.500 eV`) |
| external resolution | **FAIL** (`0.215 nm` vs probe `248.0 nm`) |
| coupling | NOT-MEASURED (no selection rule or matrix element is registered for this state) |
| **label** | **`NOT-MEASURED`** |
| missing slot | model -- no registered Model B/C confining potential for a free-standing atomic layer |

The label is `NOT-MEASURED` because the confining potential is not registered. The three external
checks are reported separately and are not merged: the declared optical probe cannot excite `z`
(`2.5 eV ≪ ΔE_z`) and cannot resolve it (`248.0 nm ≫ 0.215 nm`). Neither fact is turned into
`IS_2D` or `LOOKS_2D`.

## 9. Solver spec

See `row2_solver_spec_v1.md`. In one line: the geometry is **prescribed** (`D2`), the counts are
derived, the tiers are **measured** on the resulting fields, and no reduction equation is solved.

## 10. What this card does not claim

- not a solution of the reduction, and not a matrix cell;
- not a visibility or readability claim (`Q3` is a legibility index in levels, not identity bits);
- not a survival claim: at `t_end` 59.8% of the deposit has decayed;
- not a derivation of the 3 ns lifetime; it is imported and marked as such everywhere;
- not a fragment count with an error bar: `1.18e10` is a model estimate (programme §4.8).

---

*If Stage B's measured profile differs from section 7, Stage B must publish the difference and the
card stands as the falsified prediction. The card is not edited after the lock.*

