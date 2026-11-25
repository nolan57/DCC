# Registration — `RQ-15`, the price of persistence (`RL-5`)

**Written**: 2026-11-23, before `src/route/ladder_r5.py` existed.
**Question** (`round_queue_v1.json` `RQ-15`): *what does holding the state for `≥ 10 ns` cost, per square metre and
as a field, at the object's own scale?*
**DoD**: field strength, power per m², and the shutdown signature; if the cost is not finite, say so and make `R1`
compulsory.
**Source**: `relaxation_ladder_v1.md` §5 row 4; `scifi_boundary_v1.md` §1 knob `R1`, §3, §5.
**Product**: `runs/LADDER/r5_persistence_cost.md` (emitted by the program, not transcribed).

---

## 1. What is being priced, stated so the rung cannot move after the fact

`RL-5` relaxes **lifetime**: a `3–5 ns` transient becomes a steady state. The ladder prices it at
`6.2e23 V/m` and calls that a price. **This round tests whether an amplitude is a price.**

The distinction the round exists to make:

| quantity | symbol | what it answers |
| --- | --- | --- |
| **amplitude** | `E` | how strong the field must be |
| **stock** | `u·L_z` | how much energy is in the field per m² |
| **flux** | `P/m²` | how much power must be supplied to *keep* it there |
| **signature** | `t_rel`, `t_decay` | what switching off looks like |

An amplitude is a *setting*; a price is a *rate you must pay*. If the field is a static container, the flux is
zero and the rung costs only its stock. If the field is supercritical, the vacuum discharges it and the flux is the
price. **The round's whole content is which of those two the registered field is.**

---

## 2. Inputs, all from the record, none chosen here

| input | value | source |
| --- | --- | --- |
| confinement field | `E = 6.2e23 V/m` (= `620 MeV/fm`) | `scifi_boundary_v1.md` §5, knob `R1` |
| critical field | `E_c = m_e²c³/(eħ) = 1.323e18 V/m` | definition; the record's "`4.7e5 ×` Schwinger" is a check, §5 |
| sheet thickness | `L_z = 1.9e-15 m` (midpoint of `1.7–2.0 fm`) | §5; the interval's effect is printed |
| registered energy, Route M | `3.8e18 J/m²` | §2, §5 |
| registered energy, Route S | `1.7e17 J/m²` | §2 |
| native lifetime | `3–5 ns` | §3, §5 (`W5`) |
| baryon density | `n_B = 0.042 fm⁻³` | §5 (`W1`) |
| hold time | `t_hold = 10 ns` (DoD) and `0.1 s` (the eye) | DoD; `scifi_boundary_v1.md` §3 |
| photon energy for the `Φ` conversion | `2.25 eV` | `relaxation_ladder_v1.md` §3 |
| detection requirement | `9.5390e31 m⁻² s⁻¹` | `relaxation_ladder_v1.md` §3 |

**Model**: the field occupies the slab volume (`1 m² × L_z`). If it fills a larger container, every flux number
scales with that volume — the price is an energy *density* problem, so a bigger container only makes it worse. The
matter's opacity to the pairs is ignored (the pairs are created by the field, not by the target), as is the
back-reaction of the pair plasma on `E`; both omissions work *in the rung's favour*, so the number below is a
floor, not a ceiling.

**Pair-production rate** (Schwinger, spin-½, leading order, no spin degeneracy factor):

```
Γ/V = (E/E_c)² · Σ_{n≥1} n⁻² exp(−nπ E_c/E) / (4π³ λ_C³ τ_C),   λ_C = ħ/(m_e c),  τ_C = ħ/(m_e c²)
```

At `E = E_c` this returns `~4e54 m⁻³s⁻¹`, i.e. the standard "one pair per Compton four-volume, times `e^{−π}`" —
printed in §5 as the convention check. The formula is used at `E/E_c = 4.7e5`, where the exponent is `6.7e-6` and
the sum is `π²/6` to six digits, so the answer is insensitive to the convention: **at five orders above critical,
the exponential suppression is gone entirely.**

---

## 3. Predictions, with bars fixed before the code

| # | prediction | bar |
| --- | --- | --- |
| `P1` | the vacuum discharges the field, so the sustaining flux is set by pair production, not by `stock/t_hold` | `P_drain / (stock/t_hold) > 1e5` at `t_hold = 10 ns` |
| `P2` | the discharge time is many orders below the state's own lifetime | `1e-20 < τ_vac < 1e-16 s`, i.e. at least 7 orders below `3 ns` |
| `P3` | the discharge is **causally** permitted — replenishment is not faster than light across the slab (this is what makes the rung expensive rather than impossible) | `τ_vac / (L_z/c) > 1e3` |
| `P4` | the field's own stock dwarfs the registered energy, which is the state's, not the field's | `100 < (½ε₀E²L_z)/3.8e18 < 1e4` |
| `P5` | holding for `10 ns` requires feeding the slab more mass-energy than it contains | `(P·t_hold)/(M_rest c² per m²) > 1e9` |
| `P6` | the shutdown is a burst, not a fade | field stock `> 100 Gt` TNT equivalent |
| `P7` | the ladder's fingerprint conflates two timescales (field release vs matter decay) | ratio `> 1e10` |
| `P8` | in the ladder's own currency the rung costs more than the shortfall it would relax | `> 20` orders of photon flux vs `9.539e31` |

**Decision rule, fixed now.**

- If `P1` holds → the rung's price is a **flux**, and the verdict is "priced, not measured"; the ladder's table is
  wrong in the same way it was wrong for `RL-2` (`ε` as a dial) and `RL-3` (inverted fingerprint).
- If `P1` fails → the field is a static container, the price is `stock/t_hold`, and `6.2e23 V/m` stands as a price.
- If `P3` fails → the configuration is causally impossible, which is **stronger** than expensive, and the rung is
  `CLOSED-NO-GO` on that ground alone.
- If the cost is finite (it will be) the DoD's "make `R1` compulsory" clause is **not** triggered by
  non-finiteness; the round must then say plainly whether `R1` is compulsory on other grounds, and name them.

---

## 4. What this round does not do

No new physics, no new field value, no threshold moved, no rung re-priced by assertion — only the conversion from
the registered amplitude to a rate. It does not re-derive `6.2e23 V/m` (that is `K2`'s business and its derivation
is a potential difference over a fermi, not a pressure balance); it takes the amplitude as registered and asks what
it costs to hold. No claim about `RL-1`'s `Q3`; no claim about the deposit; erratum to the ladder appended only if
the numbers force one.

---

*Content generated by AI*
