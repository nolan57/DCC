# RL-5 — the price of persistence, at the object's own scale

**Round**: 54 (`RQ-15`).  **Registration**: `runs/LADDER/r5_persistence_registration.md`.
**Instrument**: `src/route/ladder_r5.py` — this file is emitted by it, not transcribed, so every
number below is the program's output.
**Inputs**: `scifi_boundary_v1.md` §1/§3/§5; `relaxation_ladder_v1.md` §2/§3/§5. No free parameter.

```text

==============================================================================
[1] ONE AMPLITUDE, THREE PRICES -- and why the round exists
==============================================================================
  The ladder (s2) prices RL-5 as "6.2e23 V/m".  That is a setting, not a rate.  A price needs three
  quantities and the table below fixes them before any arithmetic:

  quantity   symbol          unit   what it answers                       
  ---------  --------------  -----  --------------------------------------
  amplitude  E               V/m    how strong                            
  stock      u*L_z           J/m^2  how much is stored                    
  flux       P/A             W/m^2  what must be supplied to keep it there
  signature  t_rel, t_decay  s      what switching off looks like         

  If the field is a static container the flux is 0 and the rung costs its stock.  If it is supercritical
  the vacuum discharges it and the flux IS the price.  Which one it is, is the round.

==============================================================================
[2] THE FIELD, AND HOW FAR ABOVE THE VACUUM IT SITS
==============================================================================
    E        = 6.2e+23 V/m
    E_c      = 1.323e+18 V/m      (m_e^2 c^3 / (e hbar))
    E/E_c    = 4.686e+05            -> 5.7 orders above critical

  The record states "4.7e5 x Schwinger"; this reproduces it (4.686e+05).  That is a consistency check on the
  input, not a result.

  energy density  u = eps0 E^2 / 2 = 1.7018e+36 J/m^3
  stock over the slab  u*L_z = 3.2334e+21 J/m^2   (L_z = 1.90 fm; window 1.70-2.00 fm gives 2.89e+21 - 3.40e+21)

  For scale: the field pressure eps0 E^2/2 = 1.702e+36 Pa.  The registered internal pressure of the state is
  O(1e16) N/m in the record's own 2-D convention (s6 item 3, "P_tot ... of order 1e16 N/m").  Read as
  N/m^2 that is 20 orders below the field's energy density.  So the amplitude is not a pressure balance;
  it is a specification of an energy density.  That is precisely why it cannot be a price.

==============================================================================
[3] THE VACUUM'S ANSWER -- Schwinger pair production at five orders above critical
==============================================================================
  Convention (fixed in the registration): spin-1/2, leading order, no spin degeneracy factor.

    Gamma/V = (E/Ec)^2 * sum_{n>=1} n^-2 exp(-n pi Ec/E) / (4 pi^3 lam_C^3 tau_C)

    check at E = Ec : 4.749e+54 m^-3 s^-1   (the standard estimate (1/(lam^3 tau)) e^-pi/(4 pi^3) = 4.70e+54)
    sum at E/Ec=4.7e+05: 1.642387  (pi^2/6 = 1.644934; the exponential is exp(-6.70e-06), i.e. gone)
    Gamma/V        : 3.9209e+67 m^-3 s^-1

    pairs per m^3 per s      : 3.921e+67
    energy drain per m^3     : 6.4201e+54 W/m^3   (2 m_e c^2 per pair)
    discharge time u/(P/V)   : 2.651e-19 s
    light crossing L_z/c     : 6.338e-24 s
    ratio tau_vac/(L_z/c)    : 4.182e+04   -> causal replenishment is PERMITTED

  This is the rung's whole geometry.  The field is not a container that persists; it is a region whose
  contents turn over every 3e-19 s.  Holding it is therefore a pumping problem, and a pump has a price.

==============================================================================
[4] THE PRICE, PER SQUARE METRE
==============================================================================
  (a) if the field were static (idealise pair production away), the bill is only the stock:
        stock / t_hold(10 ns) = 3.233e+29 W/m^2
        stock / 0.1 s (eye)   = 3.233e+22 W/m^2

  (b) with pair production (the physics), the bill is the drain, independent of t_hold:
        P/A = (P/V) * L_z = 1.2198e+40 W/m^2

  (c) the ratio -- what the idealisation costs you:
        P_drain / P_static(10 ns) = 3.773e+10   (10.6 orders)
        P_drain / P_static(0.1 s) = 3.773e+17   (17.6 orders)

  The first line is the rung's honest price: 1.22e+40 W/m^2, sustained, per square metre of sheet.
  For a sense of it: 9.0e+36 x the solar constant at Earth (1.36e3 W/m^2), and ~1220 x the bolometric
  luminosity of the whole Milky Way (~1e37 W) -- per square metre.

==============================================================================
[5] THE SAME PRICE IN THE LADDER'S OWN CURRENCY (Phi = orders of photon flux, 2.25 eV)
==============================================================================
    detection requirement (ladder s3)  : 9.5390e+31 m^-2 s^-1
    sustaining flux as 2.25 eV photons : 3.384e+58 m^-2 s^-1
    ratio                              : 3.547e+26  =  26.5 orders

  The ladder's whole argument is that 10.5 orders of shortfall become 5.5-7.6 before RL-5, and that the
  remainder is bought with aperture, band and persistence.  Persistence, priced as a flux, is 26.5 orders
  -- i.e. buying persistence to close a 6-order gap costs 26.5 orders.

  This is the round's sharpest number and it needs no interpretation: the rung that would relax the
  integration limit is 3.5e+26 times more expensive, in the ladder's own unit, than the shortfall it
  relaxes.

==============================================================================
[6] THE MASS BILL, OR: WHAT 10 ns COSTS IN KILOGRAMS
==============================================================================
  Rest energy per m^2 of sheet, two routes to the same number:
    from the record's "60% of rest mass" : 3.8e18 / 0.60 = 6.333e+18 J/m^2
    from n_B = 0.042 fm^-3 and L_z        : 1.201e+19 J/m^2   (1.90 x the above)

  They differ by 1.9x; the round uses the LARGER (1.20e+19 J/m^2) everywhere below, so every ratio that
  follows is a LOWER bound.  The discrepancy is recorded, not resolved -- it is a question about the
  record's energy bookkeeping, not about persistence.

    t_hold = 10 ns (DoD)  energy 1.220e+32 J/m^2 = 1.357e+15 kg/m^2 = 1.0e+13 x the sheet's rest mass
    t_hold = 0.1 s (eye)  energy 1.220e+39 J/m^2 = 1.357e+22 kg/m^2 = 1.0e+20 x the sheet's rest mass

  At 10 ns the slab must be fed 1e+13 times its own mass-energy.  At 0.1 s, 1e+20 times.  A configuration
  that must be fed its own rest mass a trillion times over in ten nanoseconds is not a container being
  held; it is a factory whose product is the field.

==============================================================================
[7] THE SHUTDOWN SIGNATURE
==============================================================================
  Switching the field off releases the stock 3.233e+21 J/m^2.  The release is bounded above by the light-
  crossing time of the slab, 6.34e-24 s; the matter then disassembles on the registered 3-5 ns (W5).

    burst energy            : 3.2334e+21 J/m^2   = 7.728e+05 Mt TNT  = 772.79 Gt
    burst duration (upper)  : 6.34e-24 s        (L_z/c)
    matter decay            : 3-5 ns     (registered; unchanged by this round)
    ratio decay/release     : 7.89e+14  = 14.9 orders

  So the signature is not "the 3-5 ns decay".  It is a prompt electromagnetic burst at the light-crossing
  time, followed 15 orders later by the matter decay the record already registers.  Two separable
  observables, one of which was never priced.  The ladder's fingerprint for RL-5 ("the confinement field
  itself; and switching it off reproduces the 3-5 ns decay") names only the second.

  For 1 m^2 the burst is 772.79 Gt; the two branches of the record's own algebra (Route M 3.8e18 J/m^2 of
  matter energy, Route S 1.7e17) are three orders below the FIELD's stock, which is the number that
  actually leaves when you switch off.

==============================================================================
[8] THE OTHER BRANCH: ROUTE S, OR WHY THE RUNG HAS NO CHEAP DOOR
==============================================================================
  Route S (a 2-D pocket, no confinement field) has no field to discharge: its sustaining flux is exactly 0,
  because nothing is being held against the vacuum.  Its price is a one-off 1.70e+17 J/m^2 and a topology:
  Geroch forbids opening such a pocket without a singularity or CTC.

  route                 amplitude   stock J/m^2  flux W/m^2  what you must actually obtain
  --------------------  ----------  -----------  ----------  -----------------------------
  M -- compress matter  6.2e23 V/m  3.23e+21     1.22e+40    a pump at 1e40 W/m^2         
  S -- 2-D pocket       none        1.70e+17     0           a singularity (Geroch)       

  Route S is 4.3 orders cheaper in stock than Route M's field and infinitely cheaper in flux.  Its price
  is not a number at all, which is why it does not appear in the ladder as a flux either.

==============================================================================
[9] WHAT THE NUMBERS SAY
==============================================================================
  1. THE 6.2e23 V/m IN THE LADDER IS AN AMPLITUDE, NOT A PRICE.  The field at five orders above critical
     cannot persist: the vacuum turns it over in 2.7e-19 s.  What the rung costs is a pumping rate,
     1.22e+40 W/m^2, and that number appears nowhere in the record.

  2. THE PRICE IS FINITE.  The DoD's "if the cost is not finite, make R1 compulsory" clause is therefore
     NOT triggered.  The stronger statement is available anyway: the cost is finite and it is 26.5 orders
     above the shortfall it would relax, in the ladder's own unit.  R1 is compulsory for the naked-eye
     path -- no frame exists without persistence -- and R1 at this amplitude is unaffordable.

  3. CAUSALITY IS NOT THE OBJECTION; POWER IS.  tau_vac/(L_z/c) = 4.2e+04, so replenishment has time to be
     causal.  The rung is not forbidden, it is priced.  That distinction is the difference between a
     NO-GO and a bill, and the ladder has been treating it as the former by omission.

  4. THE FINGERPRINT IS HALF A FINGERPRINT.  A prompt 6e-24 s burst, then the 3-5 ns decay: 15 orders
     apart.  The ladder's stated fingerprint names only the matter decay, so a scene that reproduced the
     burst without the decay (or vice versa) would pass it.

  5. WHAT THIS DOES TO THE ORDER.  Nothing moves.  Measurements 1-3 (all V = 0) are still first, and RL-5
     was never on the cheapest path (s4 lists it as something the path does NOT get).  What changes is the
     reason RL-5 is off the path: not "unbuilt", but "26.5 orders out of budget".  RL-1 stops being a
     convenience and becomes the only door -- which is what s4 already said, now with a number.

  6. WHAT IS NOT CLAIMED.  No re-derivation of 6.2e23 V/m (K2 derives a potential difference over a fermi,
     not a pressure balance); no claim that the pair plasma's back-reaction is negligible (it is ignored,
     and ignoring it helps the rung); no claim about Q3, the deposit, or RL-1's gate.  The mass
     bookkeeping discrepancy in s6 is recorded and left open.

==============================================================================
[10] PREDICTIONS P1-P8 (bars fixed in the registration, before the code)
==============================================================================

  P1  CONFIRMED
       the sustaining flux is set by pair production, not by stock/t_hold; bar > 1e5
       measured: P_drain/P_static = 3.773e+10

  P2  CONFIRMED
       the discharge time is many orders below 3 ns; bar 1e-20 < tau_vac < 1e-16 s
       measured: tau_vac = 2.651e-19 s (10.1 orders below 3 ns)

  P3  CONFIRMED
       causal replenishment is permitted; bar tau_vac/(L_z/c) > 1e3
       measured: ratio = 4.182e+04

  P4  CONFIRMED
       the field's stock dwarfs the registered energy; bar 100 < ratio < 1e4
       measured: 3.2334e+21 / 3.8e18 = 850.9

  P5  CONFIRMED
       holding 10 ns feeds more than 1e9 x the sheet's rest mass; bar > 1e9
       measured: 1.015e+13 x

  P6  CONFIRMED
       the shutdown is a burst; bar > 100 Gt
       measured: 772.8 Gt (3.23e+21 J/m^2)

  P7  CONFIRMED
       the fingerprint conflates two timescales; bar ratio > 1e10
       measured: 7.9e+14

  P8  CONFIRMED
       the rung costs > 20 orders of photon flux vs the requirement
       measured: 26.5 orders

==============================================================================
SUMMARY
==============================================================================
  registration order : registration present, 119 s older than this run
  the rung           : NOT a field you hold.  1.22e+40 W/m^2 sustained, per m^2, because the vacuum
                       turns the field over in 2.7e-19 s.
  the price in Phi   : 26.5-order flux above the 9.5390e31 m^-2 s^-1 requirement -- against a shortfall
                       of 10.5 orders (E1: 5.5-7.6 restated as -2.42 at 1e-7).  The rung costs 26.5.
  verdict            : PRICE MEASURED -- and the price is a FLUX.  The ladder's "6.2e23 V/m" is the
                       amplitude of the branch that has a flux; the flux itself was never computed.
  R1                 : compulsory for the naked-eye path (no frame without persistence), and out of
                       budget by 26.5 orders.  Finite cost, unaffordable rung.
  what is NOT claimed: no new field value, no threshold moved, no claim about Q3 or the deposit; the
                       mass-bookkeeping discrepancy (s6) recorded and left open.

  predictions        : 8 CONFIRMED, 0 FALSIFIED

PROVENANCE: NEITHER  (Schwinger rate on a registered field + unit arithmetic; establishes no physics)
```

*Content generated by AI*
