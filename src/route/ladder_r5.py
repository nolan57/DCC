"""RQ-15 -- what persistence costs (RL-5), at the object's own scale.

Registration: runs/LADDER/r5_persistence_registration.md (written before this file).
Product     : runs/LADDER/r5_persistence_cost.md   (emitted by --write, never transcribed by hand)

The round converts one registered amplitude (6.2e23 V/m) into the three quantities a price needs:
stock (J/m^2), flux (W/m^2), and signature (what switching off looks like).
"""
import math
import os
import sys

OUT = []


def a(s=''):
    OUT.append(s)


def hdr(s):
    a('')
    a('=' * 78)
    a(s)
    a('=' * 78)


def table(rows, cols):
    w = [max([len(str(c))] + [len(str(r[i])) for r in rows]) for i, c in enumerate(cols)]
    a('  ' + '  '.join(str(c).ljust(w[i]) for i, c in enumerate(cols)))
    a('  ' + '  '.join('-' * w[i] for i in range(len(cols))))
    for r in rows:
        a('  ' + '  '.join(str(r[i]).ljust(w[i]) for i in range(len(cols))))


# ---------------------------------------------------------------------------------
# registered inputs (every one traceable; no free parameter in this round)
E_REG   = 6.2e23          # V/m, scifi_boundary_v1.md s5 (R1). 620 MeV/fm in V/m.
E_CRIT  = 1.323e18        # V/m, m_e^2 c^3 / (e hbar)
LZ_LO, LZ_HI, LZ = 1.7e-15, 2.0e-15, 1.9e-15   # m, s5 window, midpoint taken
U_REG_M = 3.8e18          # J/m^2, Route M registered energy
U_REG_S = 1.7e17          # J/m^2, Route S registered energy
N_B     = 0.042           # fm^-3, s5 (W1)
M_E     = 9.1093837e-31   # kg
C       = 2.99792458e8
HBAR    = 1.054571817e-34
EPS0    = 8.8541878128e-12
Q_E     = 1.602176634e-19
ALPHA   = 7.2973525693e-3
MEV     = 1.602176634e-13  # J
J_PER_MT = 4.184e15        # J per megaton TNT
T_LIFE_LO, T_LIFE_HI = 3e-9, 5e-9
T_HOLD  = 10e-9            # DoD
T_EYE   = 0.1              # s, s3
H_NU    = 2.25 * Q_E       # J, ladder s3
REQ     = 9.5390e31        # m^-2 s^-1, ladder s3

MC2 = M_E * C * C
LAM = HBAR / (M_E * C)      # Compton wavelength
TAU_C = HBAR / MC2          # Compton time

# ---------------------------------------------------------------------------------
hdr('[1] ONE AMPLITUDE, THREE PRICES -- and why the round exists')

a('  The ladder (s2) prices RL-5 as "6.2e23 V/m".  That is a setting, not a rate.  A price needs three')
a('  quantities and the table below fixes them before any arithmetic:')
a('')
table([('amplitude', 'E', 'V/m', 'how strong'),
       ('stock', 'u*L_z', 'J/m^2', 'how much is stored'),
       ('flux', 'P/A', 'W/m^2', 'what must be supplied to keep it there'),
       ('signature', 't_rel, t_decay', 's', 'what switching off looks like')],
      ('quantity', 'symbol', 'unit', 'what it answers'))
a('')
a('  If the field is a static container the flux is 0 and the rung costs its stock.  If it is supercritical')
a('  the vacuum discharges it and the flux IS the price.  Which one it is, is the round.')

# ---------------------------------------------------------------------------------
hdr('[2] THE FIELD, AND HOW FAR ABOVE THE VACUUM IT SITS')

ratio = E_REG / E_CRIT
u_field = 0.5 * EPS0 * E_REG ** 2
stock = u_field * LZ
stock_lo, stock_hi = u_field * LZ_LO, u_field * LZ_HI

a('    E        = %.4g V/m' % E_REG)
a('    E_c      = %.4g V/m      (m_e^2 c^3 / (e hbar))' % E_CRIT)
a('    E/E_c    = %.3e            -> %.1f orders above critical' % (ratio, math.log10(ratio)))
a('')
a('  The record states "4.7e5 x Schwinger"; this reproduces it (%.3e).  That is a consistency check on the'
  % ratio)
a('  input, not a result.')
a('')
a('  energy density  u = eps0 E^2 / 2 = %.4e J/m^3' % u_field)
a('  stock over the slab  u*L_z = %.4e J/m^2   (L_z = %.2f fm; window %.2f-%.2f fm gives %.2e - %.2e)'
  % (stock, LZ * 1e15, LZ_LO * 1e15, LZ_HI * 1e15, stock_lo, stock_hi))
a('')
a('  For scale: the field pressure eps0 E^2/2 = %.3e Pa.  The registered internal pressure of the state is'
  % u_field)
a('  O(1e16) N/m in the record\'s own 2-D convention (s6 item 3, "P_tot ... of order 1e16 N/m").  Read as')
a('  N/m^2 that is %.0f orders below the field\'s energy density.  So the amplitude is not a pressure balance;'
  % math.log10(u_field / 1e16))
a('  it is a specification of an energy density.  That is precisely why it cannot be a price.')

# ---------------------------------------------------------------------------------
hdr('[3] THE VACUUM\'S ANSWER -- Schwinger pair production at five orders above critical')

a('  Convention (fixed in the registration): spin-1/2, leading order, no spin degeneracy factor.')
a('')
a('    Gamma/V = (E/Ec)^2 * sum_{n>=1} n^-2 exp(-n pi Ec/E) / (4 pi^3 lam_C^3 tau_C)')
a('')


def gamma_schwinger(E):
    x = E_CRIT / E
    s = sum((1.0 / n ** 2) * math.exp(-n * math.pi * x) for n in range(1, 400))
    return (E / E_CRIT) ** 2 * s / (4 * math.pi ** 3 * LAM ** 3 * TAU_C)


g_crit = gamma_schwinger(E_CRIT)
g = gamma_schwinger(E_REG)
s_sum = sum((1.0 / n ** 2) * math.exp(-n * math.pi * E_CRIT / E_REG) for n in range(1, 400))

a('    check at E = Ec : %.3e m^-3 s^-1   (the standard estimate (1/(lam^3 tau)) e^-pi/(4 pi^3) = %.2e)'
  % (g_crit, math.exp(-math.pi) / (4 * math.pi ** 3) / (LAM ** 3 * TAU_C)))
a('    sum at E/Ec=%.1e: %.6f  (pi^2/6 = %.6f; the exponential is exp(-%.2e), i.e. gone)' % (ratio, s_sum, math.pi ** 2 / 6, math.pi * E_CRIT / E_REG))
a('    Gamma/V        : %.4e m^-3 s^-1' % g)
a('')
P_V = g * 2 * MC2          # W/m^3
tau_vac = u_field / P_V
P = P_V * LZ               # W/m^2
a('    pairs per m^3 per s      : %.3e' % g)
a('    energy drain per m^3     : %.4e W/m^3   (2 m_e c^2 per pair)' % P_V)
a('    discharge time u/(P/V)   : %.3e s' % tau_vac)
a('    light crossing L_z/c     : %.3e s' % (LZ / C))
a('    ratio tau_vac/(L_z/c)    : %.3e   -> causal replenishment is PERMITTED' % (tau_vac / (LZ / C)))
a('')
a('  This is the rung\'s whole geometry.  The field is not a container that persists; it is a region whose')
a('  contents turn over every %.0e s.  Holding it is therefore a pumping problem, and a pump has a price.' % tau_vac)

# ---------------------------------------------------------------------------------
hdr('[4] THE PRICE, PER SQUARE METRE')

P_static = stock / T_HOLD
P_static_eye = stock / T_EYE
a('  (a) if the field were static (idealise pair production away), the bill is only the stock:')
a('        stock / t_hold(10 ns) = %.3e W/m^2' % P_static)
a('        stock / 0.1 s (eye)   = %.3e W/m^2' % P_static_eye)
a('')
a('  (b) with pair production (the physics), the bill is the drain, independent of t_hold:')
a('        P/A = (P/V) * L_z = %.4e W/m^2' % P)
a('')
a('  (c) the ratio -- what the idealisation costs you:')
a('        P_drain / P_static(10 ns) = %.3e   (%.1f orders)' % (P / P_static, math.log10(P / P_static)))
a('        P_drain / P_static(0.1 s) = %.3e   (%.1f orders)' % (P / P_static_eye, math.log10(P / P_static_eye)))
a('')
a('  The first line is the rung\'s honest price: %.2e W/m^2, sustained, per square metre of sheet.' % P)
a('  For a sense of it: %.1e x the solar constant at Earth (1.36e3 W/m^2), and ~%.0f x the bolometric'
  % (P / 1.36e3, P / 1e37))
a('  luminosity of the whole Milky Way (~1e37 W) -- per square metre.')

# ---------------------------------------------------------------------------------
hdr('[5] THE SAME PRICE IN THE LADDER\'S OWN CURRENCY (Phi = orders of photon flux, 2.25 eV)')

phi_req = REQ
phi_cost = P / H_NU
orders = math.log10(phi_cost / phi_req)
a('    detection requirement (ladder s3)  : %.4e m^-2 s^-1' % phi_req)
a('    sustaining flux as 2.25 eV photons : %.3e m^-2 s^-1' % phi_cost)
a('    ratio                              : %.3e  =  %.1f orders' % (phi_cost / phi_req, orders))
a('')
a('  The ladder\'s whole argument is that 10.5 orders of shortfall become 5.5-7.6 before RL-5, and that the')
a('  remainder is bought with aperture, band and persistence.  Persistence, priced as a flux, is %.1f orders' % orders)
a('  -- i.e. buying persistence to close a 6-order gap costs %.1f orders.' % orders)
a('')
a('  This is the round\'s sharpest number and it needs no interpretation: the rung that would relax the')
a('  integration limit is %.1e times more expensive, in the ladder\'s own unit, than the shortfall it'
  % (phi_cost / phi_req))
a('  relaxes.')

# ---------------------------------------------------------------------------------
hdr('[6] THE MASS BILL, OR: WHAT 10 ns COSTS IN KILOGRAMS')

# rest mass per m^2, two ways, both printed because they disagree
m_rest_reg = U_REG_M / 0.60                      # the record says 3.8e18 is 60% of rest mass
n_per_m2 = N_B * 1e45 * LZ                       # fm^-3 -> m^-3, times thickness
m_rest_nb = n_per_m2 * 939.565 * MEV
a('  Rest energy per m^2 of sheet, two routes to the same number:')
a('    from the record\'s "60%% of rest mass" : 3.8e18 / 0.60 = %.3e J/m^2' % m_rest_reg)
a('    from n_B = %.3f fm^-3 and L_z        : %.3e J/m^2   (%.2f x the above)' % (N_B, m_rest_nb, m_rest_nb / m_rest_reg))
a('')
a('  They differ by %.1fx; the round uses the LARGER (%.2e J/m^2) everywhere below, so every ratio that'
  % (m_rest_nb / m_rest_reg, m_rest_nb))
a('  follows is a LOWER bound.  The discrepancy is recorded, not resolved -- it is a question about the')
a('  record\'s energy bookkeeping, not about persistence.')
a('')
for th, tag in ((T_HOLD, '10 ns (DoD)'), (T_EYE, '0.1 s (eye)')):
    E_fed = P * th
    kg = E_fed / C ** 2
    a('    t_hold = %-12s energy %.3e J/m^2 = %.3e kg/m^2 = %.1e x the sheet\'s rest mass'
      % (tag, E_fed, kg, E_fed / m_rest_nb))
a('')
a('  At 10 ns the slab must be fed %.0e times its own mass-energy.  At 0.1 s, %.0e times.  A configuration'
  % (P * T_HOLD / m_rest_nb, P * T_EYE / m_rest_nb))
a('  that must be fed its own rest mass a trillion times over in ten nanoseconds is not a container being')
a('  held; it is a factory whose product is the field.')

# ---------------------------------------------------------------------------------
hdr('[7] THE SHUTDOWN SIGNATURE')

t_release = LZ / C
a('  Switching the field off releases the stock %.3e J/m^2.  The release is bounded above by the light-' % stock)
a('  crossing time of the slab, %.2e s; the matter then disassembles on the registered %.0f-%.0f ns (W5).'
  % (t_release, T_LIFE_LO * 1e9, T_LIFE_HI * 1e9))
a('')
a('    burst energy            : %.4e J/m^2   = %.3e Mt TNT  = %.2f Gt'
  % (stock, stock / J_PER_MT, stock / J_PER_MT / 1e3))
a('    burst duration (upper)  : %.2e s        (L_z/c)' % t_release)
a('    matter decay            : %.0f-%.0f ns     (registered; unchanged by this round)' % (T_LIFE_LO * 1e9, T_LIFE_HI * 1e9))
a('    ratio decay/release     : %.2e  = %.1f orders' % ((T_LIFE_HI / t_release), math.log10(T_LIFE_HI / t_release)))
a('')
a('  So the signature is not "the 3-5 ns decay".  It is a prompt electromagnetic burst at the light-crossing')
a('  time, followed %.0f orders later by the matter decay the record already registers.  Two separable' % math.log10(T_LIFE_HI / t_release))
a('  observables, one of which was never priced.  The ladder\'s fingerprint for RL-5 ("the confinement field')
a('  itself; and switching it off reproduces the 3-5 ns decay") names only the second.')
a('')
a('  For 1 m^2 the burst is %.2f Gt; the two branches of the record\'s own algebra (Route M 3.8e18 J/m^2 of'
  % (stock / J_PER_MT / 1e3))
a('  matter energy, Route S 1.7e17) are three orders below the FIELD\'s stock, which is the number that')
a('  actually leaves when you switch off.')

# ---------------------------------------------------------------------------------
hdr('[8] THE OTHER BRANCH: ROUTE S, OR WHY THE RUNG HAS NO CHEAP DOOR')

a('  Route S (a 2-D pocket, no confinement field) has no field to discharge: its sustaining flux is exactly 0,')
a('  because nothing is being held against the vacuum.  Its price is a one-off %.2e J/m^2 and a topology:' % U_REG_S)
a('  Geroch forbids opening such a pocket without a singularity or CTC.')
a('')
table([('M -- compress matter', '6.2e23 V/m', '%.2e' % stock, '%.2e' % P, 'a pump at 1e40 W/m^2'),
       ('S -- 2-D pocket', 'none', '%.2e' % U_REG_S, '0', 'a singularity (Geroch)')],
      ('route', 'amplitude', 'stock J/m^2', 'flux W/m^2', 'what you must actually obtain'))
a('')
a('  Route S is %.1f orders cheaper in stock than Route M\'s field and infinitely cheaper in flux.  Its price'
  % math.log10(stock / U_REG_S))
a('  is not a number at all, which is why it does not appear in the ladder as a flux either.')

# ---------------------------------------------------------------------------------
hdr('[9] WHAT THE NUMBERS SAY')

a('  1. THE 6.2e23 V/m IN THE LADDER IS AN AMPLITUDE, NOT A PRICE.  The field at five orders above critical')
a('     cannot persist: the vacuum turns it over in %.1e s.  What the rung costs is a pumping rate,' % tau_vac)
a('     %.2e W/m^2, and that number appears nowhere in the record.' % P)
a('')
a('  2. THE PRICE IS FINITE.  The DoD\'s "if the cost is not finite, make R1 compulsory" clause is therefore')
a('     NOT triggered.  The stronger statement is available anyway: the cost is finite and it is %.1f orders' % orders)
a('     above the shortfall it would relax, in the ladder\'s own unit.  R1 is compulsory for the naked-eye')
a('     path -- no frame exists without persistence -- and R1 at this amplitude is unaffordable.')
a('')
a('  3. CAUSALITY IS NOT THE OBJECTION; POWER IS.  tau_vac/(L_z/c) = %.1e, so replenishment has time to be'
  % (tau_vac / (LZ / C)))
a('     causal.  The rung is not forbidden, it is priced.  That distinction is the difference between a')
a('     NO-GO and a bill, and the ladder has been treating it as the former by omission.')
a('')
a('  4. THE FINGERPRINT IS HALF A FINGERPRINT.  A prompt %.0e s burst, then the %.0f-%.0f ns decay: %.0f orders'
  % (t_release, T_LIFE_LO * 1e9, T_LIFE_HI * 1e9, math.log10(T_LIFE_HI / t_release)))
a('     apart.  The ladder\'s stated fingerprint names only the matter decay, so a scene that reproduced the')
a('     burst without the decay (or vice versa) would pass it.')
a('')
a('  5. WHAT THIS DOES TO THE ORDER.  Nothing moves.  Measurements 1-3 (all V = 0) are still first, and RL-5')
a('     was never on the cheapest path (s4 lists it as something the path does NOT get).  What changes is the')
a('     reason RL-5 is off the path: not "unbuilt", but "%.1f orders out of budget".  RL-1 stops being a' % orders)
a('     convenience and becomes the only door -- which is what s4 already said, now with a number.')
a('')
a('  6. WHAT IS NOT CLAIMED.  No re-derivation of 6.2e23 V/m (K2 derives a potential difference over a fermi,')
a('     not a pressure balance); no claim that the pair plasma\'s back-reaction is negligible (it is ignored,')
a('     and ignoring it helps the rung); no claim about Q3, the deposit, or RL-1\'s gate.  The mass')
a('     bookkeeping discrepancy in s6 is recorded and left open.')

# ---------------------------------------------------------------------------------
PRED = []


def verdict(tag, text, ok, measured):
    PRED.append((tag, ok))
    a('')
    a('  %s  %s' % (tag, 'CONFIRMED' if ok else 'FALSIFIED'))
    a('       %s' % text)
    a('       measured: %s' % measured)


hdr('[10] PREDICTIONS P1-P8 (bars fixed in the registration, before the code)')

verdict('P1', 'the sustaining flux is set by pair production, not by stock/t_hold; bar > 1e5',
        P / P_static > 1e5, 'P_drain/P_static = %.3e' % (P / P_static))
verdict('P2', 'the discharge time is many orders below 3 ns; bar 1e-20 < tau_vac < 1e-16 s',
        1e-20 < tau_vac < 1e-16, 'tau_vac = %.3e s (%.1f orders below 3 ns)'
        % (tau_vac, math.log10(3e-9 / tau_vac)))
verdict('P3', 'causal replenishment is permitted; bar tau_vac/(L_z/c) > 1e3',
        tau_vac / (LZ / C) > 1e3, 'ratio = %.3e' % (tau_vac / (LZ / C)))
verdict('P4', 'the field\'s stock dwarfs the registered energy; bar 100 < ratio < 1e4',
        100 < stock / U_REG_M < 1e4, '%.4e / 3.8e18 = %.1f' % (stock, stock / U_REG_M))
verdict('P5', 'holding 10 ns feeds more than 1e9 x the sheet\'s rest mass; bar > 1e9',
        P * T_HOLD / m_rest_nb > 1e9, '%.3e x' % (P * T_HOLD / m_rest_nb))
verdict('P6', 'the shutdown is a burst; bar > 100 Gt',
        stock / J_PER_MT / 1e3 > 100, '%.1f Gt (%.2e J/m^2)' % (stock / J_PER_MT / 1e3, stock))
verdict('P7', 'the fingerprint conflates two timescales; bar ratio > 1e10',
        T_LIFE_HI / t_release > 1e10, '%.1e' % (T_LIFE_HI / t_release))
verdict('P8', 'the rung costs > 20 orders of photon flux vs the requirement',
        orders > 20, '%.1f orders' % orders)

# ---------------------------------------------------------------------------------
hdr('SUMMARY')
n_ok = sum(1 for _t, o in PRED if o)
REGF = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                    'runs', 'LADDER', 'r5_persistence_registration.md')
a('  registration order : %s' % ('registration present, %.0f s older than this run'
                                 % (__import__('time').time() - os.path.getmtime(REGF))
                                 if os.path.exists(REGF) else 'REGISTRATION MISSING'))
a('  the rung           : NOT a field you hold.  %.2e W/m^2 sustained, per m^2, because the vacuum' % P)
a('                       turns the field over in %.1e s.' % tau_vac)
a('  the price in Phi   : 26.5-order flux above the 9.5390e31 m^-2 s^-1 requirement -- against a shortfall')
a('                       of 10.5 orders (E1: 5.5-7.6 restated as -2.42 at 1e-7).  The rung costs 26.5.')
a('  verdict            : PRICE MEASURED -- and the price is a FLUX.  The ladder\'s "6.2e23 V/m" is the')
a('                       amplitude of the branch that has a flux; the flux itself was never computed.')
a('  R1                 : compulsory for the naked-eye path (no frame without persistence), and out of')
a('                       budget by %.1f orders.  Finite cost, unaffordable rung.' % orders)
a('  what is NOT claimed: no new field value, no threshold moved, no claim about Q3 or the deposit; the')
a('                       mass-bookkeeping discrepancy (s6) recorded and left open.')
a('')
a('  predictions        : %d CONFIRMED, %d FALSIFIED' % (n_ok, len(PRED) - n_ok))
a('')
a('PROVENANCE: NEITHER  (Schwinger rate on a registered field + unit arithmetic; establishes no physics)')

TEXT = '\n'.join(OUT) + '\n'
if '--write' in sys.argv:
    dest = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                        'runs', 'LADDER', 'r5_persistence_cost.md')
    head = ('# RL-5 — the price of persistence, at the object\'s own scale\n\n'
            '**Round**: 54 (`RQ-15`).  **Registration**: `runs/LADDER/r5_persistence_registration.md`.\n'
            '**Instrument**: `src/route/ladder_r5.py` — this file is emitted by it, not transcribed, so every\n'
            'number below is the program\'s output.\n'
            '**Inputs**: `scifi_boundary_v1.md` §1/§3/§5; `relaxation_ladder_v1.md` §2/§3/§5. No free parameter.\n\n'
            '```text\n')
    with open(dest, 'w', encoding='utf-8') as f:
        f.write(head + TEXT + '```\n\n*Content generated by AI*\n')
    print('wrote %s (%d lines)' % (dest, TEXT.count('\n') + 1))
else:
    print(TEXT)
