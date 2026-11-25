B3 NUMERICAL ANALYSIS — INDEPENDENT REVIEW OF TWO FIGURES
========================================================

Date: 2026-11-24T03:56:00Z
Directive: G-73-01, Task 2 (round 73)
Registration: runs/G-73-01/g73_01_registration.md
Instrument: src/g73/verify_g73_numbers.py — runs/G-73-01/g73_01_verification.txt
Subject: `runs/RR-DT/constraint_relaxation_record.md`, level **B3** ("L_z is not an external control
parameter"), figure (i) `ΔL = 4.20e-2 m in t_rip` and figure (ii) `ρ_req = 3.232e46 J/m³ = 1.3e12 ρ_nuc`.
PROVENANCE: NEITHER. Re-reads archived constants and the archived constraint equation at two declared
relief amplitudes. Derives no new physics and adopts no level.
Result class: ARITHMETIC AND INTERPRETATION. Per G-73-01 §Prohibitions, **no engineering feasibility
judgement is made**. Ratios against known magnitudes are reported; the verdict on them is not.

------------------------------------------------------------------------------
1  SUBTASK 2.1 — PROVENANCE OF `ρ_req = 3.232e46 J/m³`
------------------------------------------------------------------------------

**Finding:** The figure is a two-line computation applied to one archived equation, and its inputs are
all on file except one — the relief amplitude `ε`, which is on file as a measurement but not as a
derivation. It is a *peak* value, not an average, and it takes both signs.

**Evidence:**

The chain, written out:

1. `Phase 1` solves the Hamiltonian constraint of `ds² = −dt² + dx² + dy² + f(t,x)² dz²` and prints
   `κρ_req = −f_xx/f` (`runs/P1/phase1_symbolic_constraint_results.txt`).
2. B3 chooses `f = L_z(1 + ε cos kx)`, so `f_xx = −L_z ε k² cos kx` and
   `−f_xx/f = εk² cos(kx)/(1 + ε cos kx) ≈ εk² cos(kx)` to `O(ε)`.
3. `ρ_req = (c⁴/8πG)·εk² cos(kx)`; the peak is `(c⁴/8πG)·εk²`.
4. With `ε = 1.7e-4`, `λ = 2π/k = 1.0e-3 m`, `k²ε = 6.7113e3 m⁻²` (`N15`) and
   `c⁴/8πG = 4.81545e42 Pa·m²` (`N14`):

       ρ_req(peak) = 3.23181e46 J/m³ = 2.01714e14 MeV/fm³ = 1.3418e12 ρ_nuc   (N16, N17, N19)

   with `ρ_nuc = 0.16 fm⁻³ × m_N c² = 2.4086e34 J/m³` (`N18`, convention declared in registration §2;
   a binding-corrected normalisation moves this by 1.8 % and does not touch the `1.3e12`).

Embedded assumptions, each named with its status:

| assumption | status |
|---|---|
| `Λ = 0` in the constraint | recorded as an undeclared premise at `B1` and deferred as `AX-01` F-005; its effect here is additive and 78.8 orders below the scale used, so it cannot move the figure |
| the source is comoving dust-like in the constraint, i.e. only `ρ` enters | **holds by construction, not by choice**: `f` is static in B3's reading, so `f_t = 0` and the momentum constraint's `κj_x = ∂_x(f_t/f)` vanishes identically. No flux is needed to support a static relief |
| linearisation in `ε` | explicit; error `O(ε) = 1.7e-4`, i.e. 4 digits |
| `y` is flat, the modulation is 1-D in `x` | follows from the ansatz; a 2-D relief would cost more, not less, per unit amplitude |
| the pressure that supplies the sign is not specified | `Phase 1`'s own NOT-a-joint-solution caveat; B3 states it, and B7 later converts it from a defect into a specification |
| `ε = 1.7e-4` | measured against the declared contrast, per the optics rung; it is an input, not a derived number |

**Assessment:** The arithmetic is reproducible to all printed digits and rests on one archived
equation. What it does *not* contain is any statement about which field supplies the stress: the
constraint fixes `ρ` and nothing else. So the figure is best read as a **required source**, exactly as
`Phase 1` says, not as an energy budget of any object.

Two details matter for interpretation and are easy to lose. First, the value is the **peak** of
`ρ_req(x)`; the spatial average over a period is zero, and the *magnitude* is what alternates. Second,
the alternating sign is in the **energy density itself**, not in a stress component — the troughs need
`−3.23181e46 J/m³` and the crests `+3.23181e46 J/m³`, because `f_xx` changes sign with `cos kx`.

------------------------------------------------------------------------------
2  SUBTASK 2.2 — PHYSICAL MEANING
------------------------------------------------------------------------------

**Finding:** The most informative way to state the figure is not in nuclear densities but as an energy
scale and a curvature scale, and both are surprisingly mild in one respect and extreme in another.

**Evidence:**

- **As an energy scale (frame-independent).** `ρ_req^(1/4) = 198.4 GeV` (`N20`), corresponding to a
  length `ħc/ρ^(1/4) = 9.9e-19 m`. As a thermal radiation density, `ρ_req` equals the radiation energy
  density of a bath at `kT = 86.0 GeV` for `g_* = 86.25` (`N21`), i.e. the electroweak epoch. For
  comparison the same formula at `160 GeV`, `g_* = 106.75`, gives `4.797e47 J/m³`, which is `1.17`
  decades *above* `ρ_req` — so the figure sits just below the electroweak-scale radiation density and
  matches it at roughly `85–90 GeV`.
- **As a curvature scale (the punchline).** `ρ_req` is what a curvature of `k²ε = 6.7113e3 m⁻²`
  costs, i.e. a radius of curvature of `1.221e-2 m` (`N23`) — **1.2 centimetres**. The conversion
  factor is the whole story: `(c⁴/8πG)/ρ_nuc = 1.9993e8` (`N39`), so **one inverse square metre of
  extrinsic curvature costs `2.0e8` nuclear energy densities**. Geometrically gentle and energetically
  enormous are not in tension; they are the same statement about a large constant.
- **What "alternating sign" means.** Positive on crests, negative in troughs, equal magnitude. It is
  not an alternating stress tensor and not an oscillation in time — the relief is static. It is a
  static, spatially alternating energy density.
- **Counterparts in known physics, as `log10` ratios only** (registration §2.1 anchors; no verdict
  attached):

  | configuration | density (J/m³) | orders below `ρ_req` |
  |---|---|---|
  | Casimir vacuum, 1 nm gap | `−4.33e8` | 37.9 |
  | Casimir vacuum, 1 µm gap | `−4.33e-4` | 49.9 |
  | quark-gluon plasma, `12 GeV/fm³` | `1.92e33` | 13.2 |
  | neutron-star core, `5 n₀` | `1.20e35` | 11.4 |
  | electroweak-epoch radiation | `~4.8e47` | −1.2 (above) |
  | Planck density | `4.63e113` | 67.2 (above `ρ_req`) |

**Assessment:** The positive half of the required source has an exact cosmological counterpart: at
`kT ≈ 86 GeV` the universe's radiation density is `ρ_req`. Nothing in the present universe reaches it —
the densest known matter, a neutron-star core, is 11.4 orders below, and the densest laboratory state,
a QGP, is 13.2 below. The negative half has no counterpart of comparable magnitude in any recorded
process; the record's own nearest reference class, the Casimir effect, is 37.9 to 49.9 orders below
depending on gap. `RR-DT` B7's remark is the accurate one: no theorem in the record forbids it, only
theorems that assume its absence.

The single number that should travel with this figure is `N39`, not `1.3e12`. `1.3e12 ρ_nuc` invites the
reading "a trillion times denser than nuclear matter", which is true but misses that the density is
being asked to do something geometric and tiny. `2.0e8 ρ_nuc per m⁻²` states the exchange rate.

------------------------------------------------------------------------------
3  SUBTASK 2.3 — MAGNITUDES OF ACHIEVED ENERGY DENSITY
------------------------------------------------------------------------------

**Finding:** Recorded as ratios. No judgement is offered, per G-73-01 §Prohibitions.

**Evidence:** See the table in §2. The two closest entries are `11.4` decades (neutron-star core) and
`13.2` decades (QGP). The highest laboratory electromagnetic energy density in the table, a focused
`1e22 W/cm²` beam, is `3.34e17 J/m³` (`X3`), `29.0` decades below (`N35`). The only entry above
`ρ_req` is the early universe at `≳ 90 GeV`, and the entry above that, Planck density, is `67.2`
decades further up (`N38`) — so `ρ_req` is not near any fundamental ceiling; it sits in the middle of
a 67-decade gap between the electroweak scale and the Planck scale.

**Assessment:** The figure is bracketed from below by every present-day object and from above by
nothing in the record except the very early universe. That is a statement about where it sits on the
scale, which is what the subtask asks for. Whether it is reachable is not addressed here.

------------------------------------------------------------------------------
4  SUBTASK 2.4 — THE RELIEF EFFECT
------------------------------------------------------------------------------

**Finding:** The relief is the mechanism by which a spatial modulation of `L_z` becomes an image, and
its cost is **linear in the modulation depth and quadratic in the inverse wavelength**. There is no
threshold in either variable, so the cost cannot be stepped under — only moved by scale.

**Evidence:**

- `ρ_req ∝ ε/λ²` (`CK5r`, `CK6r`): doubling `ε` doubles the cost; halving `λ` quadruples it. Verified
  at a decade of wavelength: `1e-2 m → 1e-3 m` multiplies `ρ` by exactly `100.0000`.
- Wavelengths at which the cost meets a known density:
  `λ = 1158 m` for `ρ = ρ_nuc` (`N22`); `λ = 518 m` for `ρ = 1.2e35 J/m³` (neutron-star core);
  `λ = 1.0e-3 m` gives `1.34e12 ρ_nuc`, `1.0e-2 m` gives `1.34e10`, `1.0e-1 m` gives `1.34e8`,
  `1.0 m` gives `1.34e6`.
- What the 1 mm scale is: it is the **relief wavelength on the object**, i.e. the length over which
  `L_z` varies, with `ε = 1.7e-4` its fractional depth. It is not an experimental standoff and not the
  scene scale — the scene is `L = 1.75 m` (from `t_rip = √2L/c`, `N29`) and the body's radius is
  `R ≈ 0.180 m`. So the relief is structure at `1/180` of the body's radius.
- The optical side is cheap: `ε = 1.7e-4` is a small fractional thickness modulation, which is why
  `RL-2`'s relief branch is not expensive *in contrast*. The finding of B3 is that the same `ε` is
  expensive *in stress*, and that the stress requirement is set by `λ`, not by `ε` alone.

**Assessment:** The relief effect and its cost are not proportional to the same thing. Contrast is
governed by `ε`; stress is governed by `ε/λ²`. A relief that is optically adequate at 1 mm is
energetically `1.34e12 ρ_nuc`; the same contrast at 1 m costs `1.34e6 ρ_nuc`, a factor `1e6` less for
the same image. The scaling therefore has one free lever — the wavelength — and it is a strong one:
six decades of cost per three decades of wavelength.

------------------------------------------------------------------------------
5  SUBTASK 2.5 — PROVENANCE OF `ΔL = 4.20e-2 m`
------------------------------------------------------------------------------

**Finding:** The figure comes from constant acceleration over one conversion time, and the conversion
time is a scene light-crossing time, not a property of the sheet. The growth law is **quadratic**, not
linear and not exponential, and the printed number is one of three estimates that differ by a factor
of 42.

**Evidence:**

1. `P_2D = 8.6227e16 N/m` and `Σ = 70 kg/m²` are both printed in `G0′ §2`, with `P_2D = u_2D/2` and
   `u_2D = 1.7245e17 J/m²`.
2. `a = P_2D/Σ = 1.2318e15 m/s²` (`N01`), i.e. `1.256e14 g`.
3. `t_rip = 8.2553e-9 s`. It is a scene quantity: `√2·1.75/c` reproduces it exactly (`N29`), and the
   same document uses `t_rip(1 m) = 1/c_s = 4.72 ns`. So `t_rip = L/c_s` with the 2D gas sound speed.
4. `ΔL = ½at² = 4.1974e-2 m` (`N02`), hence `ΔL/L_z = 4.197e13` (`N05`).

Growth law. With `a` constant, `L_z(t) = L_z0 + ½at²`: quadratic, i.e. `ΔL ∝ t²`, equivalently
`t ∝ √ΔL`. It is not linear and it is not exponential. The constant-`a` assumption is the load-bearing
one, and it fails once the thickness dilutes the 2D density (`u ∝ 1/L_z`), which is precisely the
regime the estimate is describing. So `4.20e-2 m` is an **upper-bracket** estimate within the
constant-pressure reading: with dilution the growth is slower than `t²` but still unbounded.

Three estimates at the same `t_rip`, for the spread: `½at² = 0.0420 m`; `v_∞t = 0.4098 m` with
`v_∞ = √(2P/Σ) = 4.9635e7 m/s`; `c_s t = 1.7500 m`. Spread `9.76×` between the first two (`0.99`
decades), `41.7×` end to end.

Two self-consistency checks pass. The speed reached is `0.0339c` (`N03`), so the non-relativistic
treatment is valid to `γ−1 = 5.76e-4`, i.e. `0.058 %` (`N04`, `CK2r`). And `ΔL` is `1.696 %` of the
light-crossing distance `c·t_rip = 2.4749 m` (`CK3r`), so the sheet stays thin compared with the scene.

**Assessment:** The number is an estimate, and the record presents it as one. Its robust content is not
`4.2 cm` but the conjunction: `ΔL ≫ L_z` by `≥13` orders under **every** estimate, and `ΔL` is
macroscopic (`cm` to `m`) under **every** estimate. What varies with the model is one decade; what does
not vary is the conclusion that `L_z` is not a parameter that outlives one conversion time.

The acceleration itself deserves a note, because `P_2D` is the *areal* 2D pressure of the degenerate
gas and its natural direction is in-plane. B3 assigns it to the thickness. That assignment is
consistent with `G0′` row 6, which uses the same `P_2D` to conclude that the fixed-area final state is
not mechanically self-equilibrated, and it is licensed by the fixed-area premise: if the area cannot
grow, the only remaining degree of freedom is the thickness. Stated plainly, the identification is
`P` → normal stress, and it holds only under that premise.

------------------------------------------------------------------------------
6  SUBTASK 2.6 — WHAT THE GROWTH MEANS
------------------------------------------------------------------------------

**Finding:** It is neither tearing nor a phase transition. It is the removal of confinement, and it
sweeps every length scale from sub-nuclear to macroscopic on a `√t` schedule — so the interesting part
is not the endpoint but the crossing times.

**Evidence:** With `t = √(2ΔL/a)`, the time to grow the thickness *by*:

| growth | time | fraction of `t_rip` |
|---|---|---|
| 10 fm | `4.03e-15 s` | `4.88e-7` |
| 1 nm | `1.27e-12 s` | `1.54e-4` |
| 1 µm | `4.03e-11 s` | `4.88e-3` |
| 1 mm | `1.27e-9 s` | `0.154` |
| 1 cm | `4.03e-9 s` | `0.488` |
| 4.2 cm | `8.26e-9 s` | `1.000` |

`t_rip = 8.26 ns`. The growth is `4.197e13×` in thickness (`N05`). The sheet is atomically thick
(`0.1 nm`) at `4.03e-13 s` (`N30`) — `2.0e4` times before the conversion ends — and a millimetre thick
at `15.4 %` of `t_rip`.

**Assessment:** The growth is best described as a **de-confinement sweep**: each factor of `10` in
thickness costs `√10 = 3.16` in time, so the object crosses nuclear, atomic, mesoscopic and
millimetre scales in five decades of time and then stops at `t_rip` because the clock stops, not
because the growth stops. This is why "phase transition" and "tearing" are the wrong pictures: no
barrier is crossed and nothing breaks. `L_z` is simply no longer held, and the object relaxes from a
`1 fm` film to a `cm` slab.

The duration is `8.26 ns` at the 1.75 m scene, and the record's own `t_rip(1 m) = 4.72 ns` shows the
duration is a property of the scene size, not of the sheet.

------------------------------------------------------------------------------
7  SUBTASK 2.7 — COMPATIBILITY WITH THE DCC MODEL
------------------------------------------------------------------------------

**Finding:** The growth does not make the DCC model wrong; it fixes its scope. The effective-2D
criterion fails at `L_z = 8.4492 fm` — an `8.4×` increase — which is reached `4.21e-7` of the way into
`t_rip`. So on the unconfined reading the model is valid for `3.5` femtoseconds of an `8.26`
nanosecond conversion, a factor `2.4e6` short of the whole event.

**Evidence:**

- The internal slot is `E_F ≪ ΔE_z` with `ΔE_z = πħc/L_z`. At `L_z = 1 fm`, `ΔE_z = 619.921 MeV`
  (`N06`), comfortably above `E_F = 73.37 MeV`. The slot fails when
  `L_z ≥ πħc/E_F = 8.4492 fm` (`N07`).
- Time to reach it from `1 fm`: `t = √(2·7.4492 fm/a) = 3.4778e-15 s` (`N08`), i.e. `4.2127e-7` of
  `t_rip` (`N09`).
- At the `ALL2D` endpoint, `E_F = 6.2221 MeV` and the slot survives to `L_z = 99.632 fm` (`N10`),
  reached at `1.2655e-14 s`, `1.533e-6` of `t_rip` (`N11`).
- B3's own note already reached the same conclusion: "effective 2D therefore survives B3 only on the
  confined branch, i.e. it inherits R1/K2 rather than the map."

**Assessment:** Three statements follow, and they are all scope statements rather than refutations.

1. **The model's `L_z = 1 fm` is not an arbitrary normalisation sitting inside a wide window; it sits
   `8.4×` below the window's edge.** That is why the growth destroys the criterion so quickly: there
   was almost no headroom to begin with. An increase of one order of magnitude already crosses it.
2. **The growth does not invalidate the model, because the model never claimed `L_z` was free.** It
   claimed `L_z` was *held*, and B3 is precisely the relaxation of that claim. Under the relaxation the
   object stops being 2D in a few femtoseconds; under the confinement branch (`RL-1`/`RL-2`) it does
   not, at the costs quantified in §4.
3. **The validity window is not "extremely brief" in absolute terms — `3.5 fs` is long compared with
   `L_z/c = 3.3e-24 s` — but it is brief compared with the event.** The relevant ratio is `4.2e-7`, and
   it is the number that should be quoted if the question is temporal scope.

------------------------------------------------------------------------------
8  SUBTASK 2.8 — SCALE AND SIGNATURE
------------------------------------------------------------------------------

**Finding:** `4.2 cm` is macroscopic and would change the object's *kind*, not merely its size: the
aspect ratio moves from `1.2e-9` to `0.117`, so a film becomes a thick disc. The growth completes at
`t = t_rip`, which is the last instant at which the record allows the object to be imaged.

**Evidence:**

- Aspect ratio, thickness over diameter: `2δ/(2R) = 1.194e-9` before (`N41`), `ΔL/(2R) = 0.1166` after
  (`N24`). A change of `8` decades.
- Scale: `4.2 cm` is `1.696 %` of the light-crossing distance in `t_rip` (`2.4749 m`), and `1.7 %` of
  the `1.75 m` scene.
- Mass scale: `Σ·πR² = 7.125 kg` (`N40`) at `R = 0.180 m`. So the sheet is a `7 kg` object of `0.1 m²`
  area, and `4.2 cm` is a macroscopic dimension of it.
- The clock: `RR-DT` B4 and `scifi_boundary_v1.md` §3 both place the object's observable lifetime at
  `3–5 ns`, against light-crossing `3.3 ns/m`. `t_rip = 8.26 ns` is the same order.

**Assessment:** The growth is not a perturbation on the object; it is the end of it. Three consequences
follow without any feasibility judgement.

- **Signature.** A `7 kg`, `0.1 m²` slab at `cm` thickness is a different optical and mechanical object
  from a `0.43 nm` film: the interference and thin-film relations the optics rungs use presuppose
  `L_z ≪ λ`, and at `L_z = 4.2 cm` versus `λ ≈ 500 nm` that presupposition has reversed by five
  decades. Whatever the object would look like, it would not be computed by the film formulae.
- **Timing.** The maximum thickness is reached exactly at `t_rip`, the last admissible instant. So no
  image taken within the record's own clock can show the object after it has finished thickening — the
  growth and the observation window end together. That is a structural coincidence of the two
  definitions (`t_rip = L/c_s`; growth over `t_rip`), not a designed feature.
- **Control.** The one control variable the record names is the confining stress: B3 states that "`L_z`
  is therefore not a parameter that survives one conversion time unless a confining stress of order
  `P_2D` acts". `P_2D = 8.6227e16 N/m`. Section 4 above prices one class of confining stress pattern;
  the uniform (relief-free) confinement is not priced anywhere, and this round does not price it.

**One structural remark about the pair.** The two B3 figures are not two independent facts; they are
the two horns of one dilemma, and that is their analytic content. Figure (i) prices **not confining**:
`4.2 cm` in one conversion time. Figure (ii) prices **confining with a 1 mm relief**: `1.3e12 ρ_nuc`
with alternating sign. Between them they leave exactly two untested options — confine uniformly with
no relief, or confine with a relief at kilometric wavelength — and neither has a number in the record.
That is a map of the open space, not a verdict on it.

------------------------------------------------------------------------------
SUMMARY
-------

- **Key Finding 1 — `1.3e12 ρ_nuc` should travel with its exchange rate, not its multiple.**
  `ρ_req = 3.23181e46 J/m³ = 2.01714e14 MeV/fm³`, reproducible from `κρ = −f_xx/f` at `ε = 1.7e-4`,
  `λ = 1 mm`. The illuminating ratio is `(c⁴/8πG)/ρ_nuc = 2.0e8`: one inverse square metre of extrinsic
  curvature costs two hundred million nuclear energy densities. A `1.2 cm` radius of curvature is what
  is being bought.

- **Key Finding 2 — as an energy scale the figure is electroweak, not astronomical.**
  `ρ_req^(1/4) = 198.4 GeV`, matching the radiation density of a `kT ≈ 86 GeV` bath. It is `11.4`
  decades above a neutron-star core and `13.2` above a QGP, but `67.2` decades below Planck — it sits
  inside a wide gap, not against a ceiling. The positive half has an exact cosmological counterpart;
  the negative half has none above the Casimir scale (`37.9–49.9` decades below).

- **Key Finding 3 — the relief cost is linear in depth and quadratic in inverse wavelength, with no
  threshold.** `ρ ∝ ε/λ²` exactly (`100.0000×` per decade of `λ`). Reaching nuclear density needs
  `λ = 1158 m`; the 1 mm relief is `1.3e12` because of `λ`, not because of `ε`. Contrast is set by `ε`;
  cost is set by `ε/λ²` — the two are decoupled, which is why the relief is optically cheap and
  mechanically expensive at the same time.

- **Key Finding 4 — `4.20e-2 m` is a quadratic ballistic estimate whose conclusion is estimate-free
  but whose value is not.** `a = P_2D/Σ = 1.2318e15 m/s²` over `t_rip = 8.2553e-9 s` gives `½at²`;
  three estimates at the same clock span `0.0420 / 0.4098 / 1.7500 m`. `ΔL/L_z = 4.197e13` and "the
  growth is macroscopic" hold under all three; the printed number holds under one (constant pressure).

- **Key Finding 5 — the growth is a de-confinement sweep, and the model's validity window is
  `4.2e-7` of the event.** `t ∝ √ΔL` crosses 10 fm at `4.03e-15 s`, atomic thickness at `4.03e-13 s`,
  1 mm at `1.274e-9 s`. The effective-2D slot fails at `L_z = 8.4492 fm` — only `8.4×` above the
  operating point — after `3.4778e-15 s`, i.e. `3.5 fs` of an `8.26 ns` conversion. The model is not
  refuted; its scope is the confined branch, and its unconfined window is a few femtoseconds.

OPEN QUESTIONS
--------------

- **Q1.** `P_2D` is an *areal, in-plane* 2D pressure; B3 assigns it to the thickness. That holds under
  the fixed-area premise, which `G0′` row 6 also assumes. Is the fixed-area premise itself derived
  anywhere, or is it a condition of the row-6 comparison that B3 inherited without restating?

- **Q2.** The constant-`a` estimate ignores pressure dilution (`u ∝ 1/L_z`). Under dilution the equation
  becomes `L̈ = a₀L_z0/L`, whose first integral is `L̇² = 2a₀L_z0 ln(L/L_z0)` — sub-ballistic and still
  unbounded. No number for this branch exists in the record. What is the dilution-corrected `ΔL(t_rip)`?

- **Q3.** Uniform confinement (relief-free) has no price anywhere. B3 prices `P_2D = 8.62e16 N/m` as the
  stress needed to hold a *flat* `L_z`, but the energy budget of sustaining it for `t_rip` is not
  computed. Is that a gap or a deliberate omission?

- **Q4.** The relief cost was computed as a peak energy density with alternating sign. If the negative
  half cannot be supplied, the achievable relief is not `ε = 1.7e-4` at 1 mm but a rectified pattern —
  `ρ ≥ 0` only — which is a different `f`. No such solution is on file, and this round does not
  construct one.

- **Q5.** `t_rip` appears twice in the record with two definitions that agree only because
  `c_s = c/√2`: `√2L/c` (`ME5`, `8.2553e-9 s` at `L = 1.75 m`) and `L/c_s` (`4.72 ns` at `L = 1 m`).
  Both are used as "the conversion time". Are they the same clock, or the same formula applied to two
  different scenes?

- **Q6.** The thickening completes at `t = t_rip` because both are defined against the same `L`. If the
  scene were larger, the growth would continue past the observation window; if smaller, the object
  would still be thin when the clock stops. Neither case is examined, and the coincidence in the
  present scene is therefore not informative either way.

Content generated by AI
