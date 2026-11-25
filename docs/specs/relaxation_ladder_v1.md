# Relaxation ladder v1 — rungs, prices, fingerprints

**Date**: 2026-11-23
**Authority**: `docs/decisions/relaxation_frame_v1.md` §3. That document says the programme pays in
relaxations; this one is the price list, **registered as a whole before any rung is executed**.
**Status**: SPECIFICATION. Every rung below is a *declaration*; a rung is `EXECUTED` only when a product
in `runs/` measures its fingerprint. Nothing here is a result.
**Rule that binds the whole file**: a rung may not be re-priced after seeing whether it worked. The list
was written first; the order of execution is the queue's, not the list's convenience.

---

## §1 The ordering principle, and why there are two currencies

Physics violations are incommensurable — a `4.7×10⁵×` Schwinger field and a `2×10⁴×` atomic-spacing
deficit cannot be added, and pretending otherwise would be the same defect as collapsing a 4-tuple tier
profile to a maximum (`MR1.2`). So the ladder does **not** produce a scalar cost. It carries two:

- **`V` — the violation factor**, dimensionless, always with the observable that detects it. Used for the
  physics rungs.
- **`Φ` — orders of magnitude of photon flux**, relative to full sun in the same band. Used for the
  optical rungs, because that is the currency the record's own `L3` failure was denominated in
  (`runs/MATRIX/matrix_audit_results.txt` §M-4: shortfall `3.4387×10¹⁰`).

And **`B` — bits delivered to the declared observer**: how many of the object's ~6 identity bits (4 shells
≈ 2, radius ratio ≈ 3, modulation phase ≈ 1) survive to `θ`.

Ordering is by `ΔV` then `ΔΦ` per bit — ordinal, not summed. A rung that buys bits at zero `V` dominates
every rung that buys the same bits at `V > 0`, and there is exactly one such rung.

## §2 The rung table

| rung | what it relaxes | what it buys (`B`) | price (`V`) | fingerprint — how you know you are on it | status |
|---|---|---|---|---|---|
| **`RL-0`** | nothing — strict physics | **0**. Proven empty, three independent grounds | `V = 0` | the image is a near-mirror with `\|ΔR\| = 0.001` between compositions; no scene within the sampling window | **CLOSED-NO-GO** (`visualization_null_result_v1.md`) |
| **`RL-1`** | **the observer**: naked eye (1.65–3.26 eV, ~0.1 s) → declared instrumented channel: gate `≤ 3 ns`, declared band, aperture and distance | **`q` from 0 to 1**, i.e. legibility stops being identically zero. The object becomes *sampleable at all* | **`V = 0`** — no physics is relaxed. This is a branch the spec already defines (`intrinsic_structure_tiers_v1.md` §5: `q = 1` for a declared instrumented channel) and never evaluated | a 0.1 s exposure shows nothing where a sub-3 ns gate shows a frame. Same object, two `θ` | **NOT MEASURED** (free — see §4) |
| **`RL-2`** | **flatness**: `L_z` constant → `L_z(x)` with relief | **geometry enters the image**: edge/shadow contrast and a measurable warp of the reflected environment — i.e. the *shape*, which is the object, not its enumeration | `V = ε = relief/pitch` against `C1`'s identity-level column conservation; the front's own `B(t)` supplies the field, so `ε` is not free invention | the reflected environment is distorted by the known silhouette; contrast vanishes when the relief is flattened, at fixed everything else | **NOT MEASURED** |
| **`RL-3`** | **illumination**: normal ambient → oblique / structured | shadow and grazing contrast at `O(0.1–1)`, with **no** change to the object | **`V = 0`** — illumination is the environment, not the object | contrast collapses to the `RL-0` value under normal incidence | **NOT MEASURED** (free) |
| **`RL-4`** | **opacity**: opaque 2D metal → partial visible transmission (for interference colour) | colour, hence a second independent channel | needs `\|Z₀σ_s\| ≲ 1` at `≈2.25 eV`; the record measures `\|Z₀σ_s\| ~ 10⁴` there (`scifi_boundary_v1.md` §7.5.4) | no colour appears; `R → 1` in the visible | **MEASURED — NOT AVAILABLE.** Closed at this rung by arithmetic, not by effort |
| **`RL-5`** | **lifetime**: `3–5 ns` transient → steady state | the naked eye works at all, i.e. `RL-1` becomes unnecessary; `Φ` improves linearly with integration | `6.2×10²³ V/m` (`4.7×10⁵×` Schwinger) **or** a 2D pocket, which needs a singularity (Geroch) | the confinement field itself; and switching it off reproduces the `3–5 ns` decay | **PRICE MEASURED, UNBUILT** (`scifi_boundary_v1.md` §1) |
| **`RL-6`** | **material**: the same object → same shape, substituted surface | arbitrary contrast and colour, as on any designed surface | `2×10⁴×` atomic spacing (`15.4 fm` vs `0.3 nm`) — `G0′` row 1, the record's strongest NO-GO | the surface's composition differs from the target's: readable in the keV / neutrino channels already specified (`scifi_boundary_v1.md` §7.5.2) | **PRICE MEASURED** |

**Qualification carried on `RL-6`** *(appended 2026-11-24 under governor directive G-71-01 §1.1; the rung
table above is not edited, and no price moves)*

> `RL-6` pricing assumes `d∥` serves as both in-plane column pitch and plate thickness. This identification is a
> modelling choice. If `L_z` is used as the independent thickness parameter, the `RL-6` ratio changes by a factor
> of `15.4`.

- The two roles are not the same length. `d∥ = 15.40194 fm` is derived as the mean **in-plane** column pitch,
  `N_s^{-1/2}` (`constraint_crosswalk_v1.md` §8.1); the plate's thickness is `L_z = 1.0 fm`, a density-inferred
  normalisation (`dimensional_conventions_v1.md` §1). The crosswalk called the identification a modelling choice
  in §8.2; the ladder's price column did not carry that qualification until this block.
- At `L_z = 1 fm` the ratio is `0.3 nm / 1 fm = 3.000e5`, i.e. `15.4 ×` the printed `2×10⁴×`. At the alternative
  carrier length `6.742 fm` it is `4.4497e4`. All three are `NO-GO` against a `1×` bar; what moves is the size of
  the number, not its sign (`runs/AX/ax01_axiom_audit_results.txt`, `C-016`).
- **The price stays `2×10⁴×`,** and its `2.60 %` rounding of `1.94805e4` is unchanged. The qualification is
  descriptive: it says which length the price is denominated in, and what happens if the reader uses the other
  one. It does not re-price the rung, and it does not touch `RL-6`'s `PRICE MEASURED` status.

**`RL-4` is the only rung closed by measurement rather than left open**, and it is worth stating plainly:
visible transmission is not a knob, because a 1.7–2.0 fm sheet is a Drude mirror at eV frequencies. Colour
must be bought at `RL-6`, or produced geometrically (thin-film interference needs a film two orders thicker
than the object allows).

## §3 The flux arithmetic — converting a verdict into a shopping list

`L3` failed at `θ_eye` on two grounds. The first is the channel factor (`q = 0`), bought by `RL-1`. The
second is flux:

```
detection requirement        9.5390e31 m^-2 s^-1
  x t_rip                    7.8747e23 photons m^-2 per frame
full sun at 2.25 eV          2.7740e21 m^-2 s^-1
  x t_rip                    2.2900e13 photons m^-2 per frame
shortfall                    3.4387e10        (10.5 orders)
```

That requirement was computed on a **compositional** contrast: `|ΔR| = 0.001` between the frozen and
neutronized states, in a band where the eye has no response. Two independent things move it, and neither
was in the calculation:

| lever | effect on requirement | orders |
|---|---|---|
| contrast `c` at fixed SNR, `∝ 1/c²` | `1e-3 → 3e-2` (a topographic edge, oblique) | **+2.9** |
| contrast `c`, same law | `1e-3 → 0.3` (grazing incidence on relief) | **+5.0** |
| aperture / integration time, `∝ 1/At` | linear in both; the gate is already `≤3 ns`, so integration is capped by `RL-5`, not by `RL-2` | `+0 … +3` |

So the honest statement is: **`10.5` orders becomes `5.5–7.6` orders before `RL-5`, and the remainder is
bought by aperture, band and persistence — not by any new physics.** Whether the remainder actually closes
is the first measurement this ladder registers; **no rung here is claimed to close it.**

This is the whole difference the frame makes. The old verdict was "empty set". The new verdict is
"`5.5–7.6` orders of flux, in a currency an engineer can buy", which is a *different kind* of statement
and a *weaker* one — the record should say so, and does.

## §4 The cheapest path to the goal, and its exact price

`RL-1` (observer) + `RL-2` (relief) + `RL-3` (oblique illumination) deliver a legible image of the shape at
**`V = ε` and `Φ ≈ 5.5–7.6` orders**, with no confinement field and no material substitution.

Stated as the goal of `relaxation_frame_v1.md` §6: `Q3(θ) ≥ 2.0` with `θ = (aperture, gate ≤ 3 ns, band,
distance)` — **the naked eye is not in the tuple.** That is the rung's price, and it is the only thing the
project has to give up to get a picture: *the observer stops being a human being sitting in a room.*

Everything else it keeps: the object, its shape, its physics (`C1` at identity level up to `ε`), and the
prohibition on claiming more than was measured.

**What the project does not get by this path**: colour (`RL-4` closed by measurement), a steady scene (`RL-5`
unbuilt), and "the same matter" (`RL-6`). Each of those has a price already on the table.

## §5 What must be measured, in order

Three rungs are `NOT MEASURED`, two of them at `V = 0`. The ladder is worthless until at least the free
ones are measured, because a free rung that turns out to buy nothing changes the whole order.

| order | measurement | product | kills the ladder if |
|---|---|---|---|
| 1 | `RL-1`: `Q3` at `θ_fast` on a scene that carries 2D-ified content (never done — `MR1.3`) | `runs/LADDER/r1_observer_results.txt` | `Q3` stays `0` at `q = 1`, i.e. legibility was never about the channel |
| 2 | `RL-2`: contrast of a relief scene vs a flat one, same flux, same band | `runs/LADDER/r2_relief_contrast_results.txt` | relief buys `< 1` order, i.e. the `1/c²` lever is not there |
| 3 | `RL-3`: oblique vs normal, same relief | `runs/LADDER/r3_illumination_results.txt` | oblique buys nothing, i.e. `RL-2` and `RL-3` are one rung, not two |
| 4 | `RL-5`: what persistence costs at the object's own scale, as an engineering number | `runs/LADDER/r5_persistence_cost.md` | the cost is not finite — then `RL-1` is compulsory, not optional |

Measurements 1–3 are cheap and are the reason this frame is worth adopting: they can be run before any
decision about confinement fields.

## §6 Rungs that are not rungs

The record already drew this line and the ladder inherits it (`scifi_boundary_v1.md` §6–§7). These are
**myths**, not expensive rungs — they have no finite knob and no fingerprint, so they cannot be priced and
must not appear on the ladder:

- a zero-thickness perfect mirror (`L_z = 0`) — a degenerate limit, not an object;
- "the person is still a person" at `1 m²` — the myth is not the 2D reduction, it is the survival of the
  person;
- self-binding at `10¹⁶ N/m` — it is always held down, never standing.

Their exclusion is what keeps `RL-5`/`RL-6` from becoming an unbounded wish list.

## §7 What this specification does not decide

It does not claim any rung reaches `Q3 ≥ 2.0`. It does not price `RL-2`'s `ε` (that is measurement 2). It
does not decide `RL-5` versus `RL-1` — it prices both and leaves the choice, which is the governor's, since it
is a choice of what the project is *for*. And it does not touch `S9`: every number above is a property of
a declared scene at a declared `θ`, and none of them is a sentence about what a person would see.

*Content generated by AI*

---

## Errata

**E1** *(appended 2026-11-23 by round 48, `runs/LADDER/r1_observer_results.txt`; §2's rung table is **not** edited)*

§3 attributes the flux requirement to "a **compositional** contrast: `|ΔR| = 0.001`". It is not. The registered
chain evaluates it at `C = 1e-7` — the SNR-3 detector floor — as `P2-3` itself prints (`dtau = 1e-7` →
`N = 9e14` → `9.539e31 m^-2 s^-1`). Round 48 rebuilt the chain from its own numbers and reproduced `3.4387e10`
to `9.8e-6` relative at `1e-7`; at `1e-3` the same chain gives **`343.9`**.

Consequences, all arithmetic, no rung added, removed, reordered or re-priced *after* execution (none of
`RL-1`…`RL-3`'s fingerprints has been measured; this is a correction of a stated price, not a revision of a result):

| §4's claim | corrected | by |
|---|---|---|
| `Φ ≈ 5.5–7.6` orders after `RL-2 + RL-3` | **`−2.42`** orders, i.e. the gate is already open | `3.4387e10 · (1e-7/0.3)² = 3.82e-3` |
| the same at `RL-2` alone (`3e-2`) | **`−0.42`** orders, open | `3.4387e10 · (1e-7/3e-2)² = 0.382` |
| the same at the deposit's own contrast (`1e-3`) | **`+2.54`** orders, a `344 m²` collector (18.5 m aperture) or `344 × t_rip` | `343.9` |

Two further facts belong with this erratum rather than with any rung:

1. **`Φ` was never independent of `Q3`.** The detection gate meets its requirement at `C* = 1e-7·√3.4387e10 =
   1.854e-2`, while `Q3 ≥ 2` needs `C ≥ C_eye(2²−1) = 3e-2`. So `Q3 ≥ 2 ⇒ detection`, by a factor `1.618` in
   contrast (`2.617` in photons). Pricing flux and legibility as two currencies double-counts one wall; §1's
   two-currency scheme survives for `V`, and for `Φ` only as a *restatement* of the `L3` threshold.
2. **`RL-2` lands exactly on the `L3` threshold.** `C = 3e-2` gives `Q3 = log2(1+3) = 2.000000`. The rung is
   therefore sufficient with **zero margin**: any contrast loss puts it under `L3`, and `RL-3` is what buys the
   margin (`Q3 = 4.95`). §2 lists `RL-2` and `RL-3` as separate rungs at the same `V = 0`; the measurement says
   they are not separable in practice — `RL-2` alone passes, and passes by nothing.

Measurement 1 of §5 asked whether the ladder dies at its first rung ("`Q3` stays `0` at `q = 1`"). It did not:
`Q3 = 5.737` on the deposit-like class at `q = 1`, and `0.000` at `q = 0`. The rung is admissible; what §3–§4
mis-stated is its *price*, by eight orders in photons, in the project's favour.

**E2** *(appended 2026-11-23 by round 49, `runs/LADDER/r2_relief_contrast_results.txt`; §2's rung table and
§3's lever table are **not** edited)*

§3 prices `RL-2` by a lever: "contrast `c` at fixed SNR, `∝ 1/c²`; `1e-3 → 3e-2`". Round 49 measured the
middle term, `c(relief)`, which the ladder never defined. Three results, all on declared fields:

1. **`3e-2` is the criterion restated, not a measurement.** `Q3 = 2` requires `C = C_eye(2² − 1) = 0.030000`.
   The ladder's `3e-2` is that number to the digit. `RL-2` therefore passes `L3` because it was priced at the
   pass mark — which is what round 48 recorded as "zero margin" and is better read as "the rung's contrast was
   copied from the threshold it is meant to be tested against".
2. **Contrast is not a function of `relief/pitch`.** With the deposit's own material (a near-mirror,
   `|ΔR| = 1e-3`) under a *uniform* environment, `C = 0` **exactly** at every amplitude across six decades:
   a mirror in an integrating sphere is invisible, whatever its relief. Under a collimated source
   (`β = 4.65e-3`) the sine crosses `C = 0.03` at `a = 68.8 µm` (`ε = 1.7e-4`) and the terraced form at
   `26.6 µm`, but the terraced form then holds `C = 0.280` unchanged for **3.6 more decades** — a topographic
   edge's contrast is set by its riser width and by the environment, not by its height. `V = ε` is arithmetically
   unchanged and prices nothing that was measured.
3. **`θ` is missing a term.** `θ = (aperture, gate ≤ 3 ns, band, distance)` does not carry the environment's
   angular radiance profile, and that profile is what makes `C` nonzero or exactly zero. Since `RL-2` is the
   only rung whose price is a *contrast*, its price is currently a function of an undeclared variable. Adding the
   term is a **tightening** (it can only reduce what may be claimed), so it is recorded here rather than gated:
   from this erratum, any sentence of the form "`RL-2` buys `C`" must read "`RL-2` buys `C` **in environment
   `E`**", and `E` must be named.

What survives: relief is real, it is cheap (`ε ~ 1.7e-4`, `0.054%` of the `ε_max = 0.3182` the deposit's own
clearance allows), and it does put geometry into the image. What does not survive is the claim that its price
is a number. The rung's order in §4 is unaffected — it is still the cheapest path — but `RL-2` cannot be
compared to `RL-5` or `RL-6` on `ΔV` while its `V` is a dial whose useful travel is `5e-4` of its range.

**E3** *(appended 2026-11-23 by round 50, `runs/LADDER/r3_illumination_results.txt`; §2's rung table, §4's
path and §5's order are **not** edited)*

`RL-3` was carried as a rung at `V = 0` with one fingerprint: "contrast collapses to the `RL-0` value under
normal incidence". Round 50 measured all three mechanisms that could make oblique illumination a lever, and
the rung does not survive as one. The table keeps its byte content; the status change is here.

1. **The fingerprint is false, and its two axes are conflated.** Contrast at *normal* incidence in a
   *narrow* environment is `C = 3.3166` (`Q3 = 8.38`), and `C = 0` **exactly** in a *wide* one at **every**
   incidence. So the collapse is a function of the environment's **angular width** `β`, not of its
   **direction** `θ_i`. A sentence that says "normal" and means "uniform" is the same conflation that
   erratum `E2` item 3 found in `θ` itself.
2. **The direction of the dependence is inverted for this material.** Reflection about the local normal is
   an isometry, so the ray deflection is `2 arctan α` and carries no `θ_i`: with the camera in the specular
   position, `C` is identical across `0/45/75°` to `0.0e+00` in float64, over two forms and five amplitudes.
   With the camera fixed at normal incidence the bright set instead *leaves* the surface — onset `3.31°`
   (sine) and `8.88°` (terrace) at `a = 1 mm`, beyond which the plate is uniformly dark and there is no
   image at all. Contrast is therefore **maximal** at normal incidence, and grazing illumination is not a
   contrast lever but a blackout.
3. **Neither other mechanism pays.** Fresnel is a *uniform* gain: it cancels in `std/mean` exactly
   (`1.3e-16` relative, five reflectance values, two incidences), and the gain itself is bounded by
   `1/R(0) − 1 ≈ 4/|Z₀σ_s|` — `5%` at `|Z₀σ_s| = 80`, `0.03%` at the record's own eV value. Multiplied by the
   projected solid angle `cos θ_i = 0.259`, the net is **`−0.61` orders** at `75°`. For a 2-D sheet the loss
   is structural: `R_p → 0` at grazing while `R_s → 1`. Oblique illumination is not free; it is a bill.
   Occlusion is the one mechanism that moves `C`, and it is the object's own geometry: it needs
   `tan θ_i` above the facet's slope and half-shadowed treads at `ε = 3.35e-2`, i.e. **`195×`** the `ε` at
   which the glint channel is already at threshold.
4. **So `RL-3` is retired, not re-priced.** Its price was `V = 0`; the round measures `B = 0` as well —
   separation over incidence `S_θ = 1.000000000` against a pre-registered bar of `2.0`. What remains of the
   row is a **declaration** (which environment the experimenter brings — `docs/specs/theta_environment_v1.md`)
   and a **hazard** (a fixed camera at `45°` on a near-mirror sees a reflected void). §4's "cheapest path"
   therefore reads `RL-1 + RL-2`, and `§5` order 3's kill criterion — "oblique buys nothing, i.e. `RL-2` and
   `RL-3` are one rung, not two" — **fired**, which is what `§5` said would happen if it did.
5. **Scope, stated so the retirement is not over-read.** In `E4` (the diffuse model) oblique *is* a lever:
   `C(75)/C(45) = 3.732` against `tan 75/tan 45 = 3.732`, and `C(0°)` is four hundred times smaller because
   the cosine law is stationary in slope at normal incidence. `E4` is the channel the near-mirror surface
   excludes — the same exclusion erratum `E2` recorded for the `1/c²` lever. The identity of `RL-2` and
   `RL-3` is therefore a statement about this material's channels, not about optics in general.
6. **One arithmetic consequence, in the direction of `E1`.** At the measured `C = 3.3166` the `1/c²` chain
   gives `3.4387e10 · (1e-7/3.3166)² = 3.13e-5`, i.e. `Φ = −4.5` orders: the flux gate is already open by
   four and a half orders at this contrast, two orders beyond `E1`'s `−2.42`. The gate was never the gate;
   `E1` said so and this raises the margin, it does not create a new claim.

**E4** *(appended 2026-11-23 by round 54, `runs/LADDER/r5_persistence_cost.md`; §2's rung table is **not** edited)*

§2 prices `RL-5` as "`6.2×10²³ V/m` (`4.7×10⁵ ×` Schwinger)". Round 54 converts that amplitude into a rate, and
the number in the price column turns out not to be a price.

1. **The amplitude is `4.69×10⁵` times critical, so the field does not persist — it is pumped.** At that ratio the
   Schwinger exponent `πE_c/E = 6.7×10⁻⁶` is gone; the pair drain empties the field in
   `τ_vac = u/(Γ·2m_ec²) = 2.7×10⁻¹⁹ s`. So `RL-5` costs neither the registered stock (`3.8×10¹⁸ J/m²`, the
   state's energy) nor the idealised `stock/t_hold` (`3.2×10²⁹ W/m²` at `10 ns`), but the **sustaining flux
   `1.22×10⁴⁰ W/m²`**, which is independent of how long the state is held.
2. **In the ladder's own currency that is a 26.5-order cost**: `3.38×10⁵⁸` photons m⁻² s⁻¹ at `2.25 eV` against
   the `9.5390×10³¹ m⁻² s⁻¹` requirement — the same requirement whose shortfall §3 restates as `5.5–7.6` orders
   (`E1`: `−2.42` at `1e-7`, `E3`: `−4.5` at the measured contrast). §4's clause "the remainder is bought by
   aperture, band and persistence" is arithmetically false for the last of the three: persistence buys the
   remainder by `3.5×10²⁶`. Aperture and band stand.
3. **The cost is finite, so this is a bill and not a prohibition** — and read that way it is the strongest
   statement available about the naked eye: no frame exists without persistence (a `0.1 s` integration over a
   `3–5 ns` state is empty), and persistence at this amplitude is `26.5` orders out of budget. Two independent
   grounds, one verdict, and the DoD's "if the cost is not finite, make `R1` compulsory" clause is **not**
   triggered — `R1` is compulsory on the first ground instead, and unaffordable on the second.
4. **The fingerprint is half a fingerprint.** Switching off releases `3.23×10²¹ J/m²` (`772 Gt` for `1 m²`) at the
   slab's light-crossing time `6.3×10⁻²⁴ s`; the registered `3–5 ns` matter decay follows `15` orders later. §2's
   fingerprint ("the confinement field itself; and switching it off reproduces the `3–5 ns` decay") names only
   the second observable, so a scene reproducing the burst *without* the decay would satisfy it.
5. **Status unchanged, reason changed.** The row keeps `PRICE MEASURED, UNBUILT` and gains the sentence it was
   missing: *the measured price is a flux, and the branch that has a flux is the branch whose amplitude is
   listed.* The other branch is `S`: zero sustaining flux, `1.7×10¹⁷ J/m²` once, `4.3` orders cheaper in stock and
   unbuildable for a reason that is not a number (Geroch).
6. **Scope.** Nothing here re-derives `6.2×10²³ V/m` — `K2` derives a potential difference over a fermi, not a
   pressure balance, and at that amplitude the field energy density exceeds the state's own `O(10¹⁶) N/m`
   internal pressure by twenty orders. The pair plasma's back-reaction is ignored, which *helps* the rung; no
   `Q3` claim is made. One number is recorded without being resolved: the sheet's rest energy from `n_B` and
   `L_z` is `1.9×` the value implied by §5's "`3.8×10¹⁸ J/m²` = 60 % of rest mass", and every ratio in the
   product uses the larger, so they are lower bounds.

**E5** *(appended 2026-11-24 by round 65, `runs/P1/phase1c_repricing_results.txt`; §2's rung table,
§4's path and earlier errata are **not** edited)*

Phase 1b showed that `f→0` can be a flat, extendable coordinate degeneration for the Kasner slice
and is singular only for the generic contracting family. G-64-01 required a re-evaluation of the
pricing basis; the dependency audit returns `rung_moves = 0`, `gate_moves = 0`,
`terminal_moves = 0`, `threshold_moves = 0` (`CHECK 7/7`, `IDENT 1/1`, `NEGCTRL 1/1`). The product
was emitted before this append; its ladder SHA-256 refers to the pre-append file.

1. `RL-0` stays a myth: coordinate degeneration does not give a finite-thickness object, so a
   zero-thickness perfect mirror is still excluded, not admitted.
2. `RL-1`/`RL-2` prices are the observer channel and relief/environment contrast; `RL-3` was
   retired by E3; `RL-4` is closed by the measured sheet conductivity; none contains an `L_z=0`
   singularity premise.
3. `RL-5`'s singularity branch is Geroch's topology-change/CTC obstruction, not the curvature
   blow-up tested in Phase 1b. The measured Schwinger-flux branch is unchanged.
4. `RL-6`'s basis remains `d∥ = 15.40 fm` against atomic spacing `0.3 nm`; the printed ratio is
   `1.94805e4`, within `2.60%` of the ladder's rounded `2e4`. The price is not re-priced.
5. D8's selected path `RL-1 + RL-2`, `V = ε` and `Φ = −4.5` orders at `C = 3.3166` in a named
   `E`/`G` are unchanged. The only archived sentence qualified is
   `effective_2d_definition_v1.md` §5 reason 2 (its E4); `G0′` row 1 receives a trigger record
   (its E3), not a reopening.
