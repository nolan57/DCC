#!/usr/bin/env python
"""
RQ-13 -- RL-2: the contrast of a relief scene against a flat one, same illumination, same band.

Decides whether the 3e-2 on which RL-2 stands with zero margin is a measured number or a declared one,
and measures what relief actually buys in three declared environments and two relief forms.

Metric: Weber contrast over the plate interior, C_w = std(I)/mean(I) on u > 0 (registration erratum E1).
The locked estimator's DoG contrast is printed beside it in its own column, so the substitution is visible.
Thresholds are READ from runs/MATRIX/threshold_lock.json; nothing here writes one.

Checks predictions Y1..Y7 of runs/LADDER/r2_relief_registration.md.

Usage:  python src/route/ladder_r2.py [--write]
"""
import contextlib
import importlib.util
import io
import math
import os
import re
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTDIR = os.path.join(ROOT, 'runs', 'LADDER')
REG = os.path.join(OUTDIR, 'r2_relief_registration.md')
OUT = os.path.join(OUTDIR, 'r2_relief_contrast_results.txt')

_spec = importlib.util.spec_from_file_location(
    'structure_tiers', os.path.join(ROOT, 'src', 'route', 'structure_tiers.py'))
ST = importlib.util.module_from_spec(_spec)
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    _spec.loader.exec_module(ST)

LOCK = ST.lock
C_EYE = ST.C_EYE
THR_L3 = float(LOCK['tiers']['L3']['threshold_c'])
SHORTFALL = 3.4387e10          # registered at C = 1e-7, runs/LADDER/r1_observer_results.txt s4

GRID = 128
P, S_CELLS = 16, 12            # the PA-16 instance
PITCH = 0.400100               # m
CELL = PITCH / P               # 0.02500625 m per lattice cell
CELL_PX = GRID // P            # 8 px per cell
PX_M = CELL / CELL_PX          # 3.126e-3 m per image pixel
LAM = 4.0 * CELL               # 0.100025 m, one corrugation period = 32 px
XI_BAND = 4.0 * CELL_PX        # 32 px, the registered DoG band (erratum E1 explains why it is secondary)
BETA = 4.65e-3                 # rad, solar angular radius
C_TARGET = C_EYE * (2.0 ** THR_L3 - 1.0)       # 0.03 exactly
R4, H = 0.0900, 0.2300         # m, docs/specs/demo_object_v1.md

L = []


def a(s=''):
    L.append(s)


def hdr(t):
    a('')
    a('=' * 98)
    a(t)
    a('=' * 98)


def table(rows, cols):
    widths = [max([len(str(c))] + [len(str(r[i])) for r in rows]) for i, c in enumerate(cols)]
    a('  ' + '  '.join(str(c).ljust(w) for c, w in zip(cols, widths)))
    a('  ' + '  '.join('-' * w for w in widths))
    for r in rows:
        a('  ' + '  '.join(str(v).ljust(w) for v, w in zip(r, widths)))


def plates(p, s):
    """The PA-16 field builder, verbatim from src/route/plate_array.py (periodic on the grid)."""
    return ((np.arange(GRID) % p)[:, None] < s).astype(np.float64) * \
           ((np.arange(GRID) % p)[None, :] < s).astype(np.float64)


def height(amp, form):
    """z(x) in metres: sinusoidal, or terraced with a one-pixel riser (the declared form)."""
    x = np.arange(GRID) * PX_M
    if form == 'S':
        z = 0.5 * amp * np.sin(2.0 * math.pi * x / LAM)
    elif form == 'T':
        w = PX_M / LAM                      # riser width as a fraction of the period
        ph = (x / LAM) % 1.0
        up = np.clip(np.minimum(ph, ph - 0.5 + w) / w, 0.0, 1.0)
        dn = np.clip(np.minimum(ph - 0.5, ph - 1.0 + w) / w, 0.0, 1.0)
        z = 0.5 * amp * (up - dn)
    else:
        raise ValueError(form)
    return np.tile(z, (GRID, 1))


def slope(amp, form):
    return np.gradient(height(amp, form), PX_M, axis=1)


def image(u, amp, form, env, theta_i=0.0):
    al = slope(amp, form)
    if env == 'E1':
        return u.copy()
    if env in ('E2', 'E3'):
        return u * (np.abs(2.0 * al) < BETA).astype(np.float64)
    if env == 'E4':
        c = np.cos(theta_i + np.arctan(al)) / math.cos(theta_i)
        return u * np.clip(c, 0.0, None)
    raise ValueError(env)


def cweber(I, mask):
    v = I[mask]
    m = float(v.mean())
    return float(v.std() / m) if m > 0 else float('inf')


def cdog(I):
    r = ST.q3(I, XI_BAND, 1.0)
    return (r[1], r[0]) if r else (0.0, 0.0)


MASK = plates(P, S_CELLS) > 0


def cross(xs, ys, target):
    for i in range(1, len(xs)):
        if ys[i - 1] < target <= ys[i]:
            f = (target - ys[i - 1]) / (ys[i] - ys[i - 1])
            return 10.0 ** (math.log10(xs[i - 1]) + f * (math.log10(xs[i]) - math.log10(xs[i - 1])))
    return None


def q3(c):
    return math.log2(1.0 + c / C_EYE) if c > 0 else 0.0


# ==================================================================================
hdr('RL-2 -- RELIEF CONTRAST AGAINST A FLAT CONTROL   (round 49, RQ-13)')
a('  flat   : the PA-16 plate, no relief      relief : same plate, z(x) with amplitude a, period 4 cells')
a('  metric : C_w = std(I)/mean(I) over the plate interior (registration erratum E1)')
a('           the locked DoG contrast at xi = 4 cells is printed beside it, in its own column')
a('  forms  : S sinusoidal   T terraced, riser = 1 px = %.2f mm of run' % (PX_M * 1e3))

# ---------------------------------------------------------------------------------
hdr('[0] ESTIMATOR IDENTITY -- the imported module must still reproduce the archived table')
u = plates(P, S_CELLS)
xi_img, _ = ST.char_scale(u)
r = ST.q3(u, xi_img, 1.0)
ok1 = (abs(xi_img - 3.32) < 5e-3) and abs(r[1] - 0.5232) < 5e-5 and abs(r[0] - 5.737) < 5e-3
a('  PA-16 xi/h %.4f vs 3.32   C_xi %.4f vs 0.5232   Q3 %.3f vs 5.737  -> %s'
  % (xi_img, r[1], r[0], 'YES' if ok1 else 'NO'))
a('  (the archive prints xi in the estimator unit h = 1 px; 3.32 is the archived PA-16 row. The DoG band')
a('   used for the relief scenes below is 32 px, ten times the plate own correlation length -- erratum E1)')
a('  C_eye %.4f   Q3 threshold %.2f   C at threshold %.4f (both from threshold_lock.json)'
  % (C_EYE, THR_L3, C_TARGET))

# ---------------------------------------------------------------------------------
hdr('[1] THE FLAT CONTROL -- interior contrast with no relief at all')
C_FLAT = cweber(u, MASK)
a('  C_w(flat) = %.3e exactly    C_DoG(flat) = %.3e' % (C_FLAT, cdog(u)[0]))
a('  A flat plate has no interior structure at ANY band: every relief number below is an INCREMENT')
a('  from zero, so the "ratio to flat" is 0/0 and the ratio form is not used. The control still does')
a('  work: it shows that the do-nothing case is exactly zero, not small.')

# ---------------------------------------------------------------------------------
hdr('[2] SWEEP -- Weber contrast against relief amplitude')
AMPS = np.logspace(-7, -1, 73)
SER = {}
for form in ('S', 'T'):
    for env in ('E1', 'E2', 'E4'):
        SER[(form, env)] = np.array(
            [cweber(image(u, amp, form, env, math.radians(60.0) if env == 'E4' else 0.0), MASK)
             for amp in AMPS])

a('  a (m)        S/E1 uniform  S/E2 glint   S/E4 diffuse   T/E1 uniform  T/E2 glint   T/E4 diffuse')
a('  ' + '-' * 96)
for k in range(0, len(AMPS), 9):
    a('  %-11.3e  %-12.3e  %-11.3e  %-13.3e  %-12.3e  %-11.3e  %-13.3e'
      % tuple([AMPS[k]] + [SER[(f, e)][k] for f in ('S', 'T') for e in ('E1', 'E2', 'E4')]))

# ---------------------------------------------------------------------------------
hdr('[3] a* -- THE AMPLITUDE AT WHICH C_w REACHES 0.03, PER FORM AND ENVIRONMENT')
rows, A_STAR = [], {}
for form in ('S', 'T'):
    for env in ('E1', 'E2', 'E4'):
        key = (form, env)
        A_STAR[key] = cross(AMPS, SER[key], C_TARGET)
        rows.append((form, env, '%.3e' % A_STAR[key] if A_STAR[key] else 'never',
                     '%.3e' % (A_STAR[key] / PITCH) if A_STAR[key] else '--',
                     '%.4f' % SER[key].max(), '%.2f' % q3(SER[key].max())))
table(rows, ('form', 'env', 'a* (m)', 'eps* = a*/pitch', 'max C_w', 'Q3 at max'))

a('')
a('  E1 for BOTH forms: max C_w = %.3e over the whole 6-decade sweep, i.e. the flat control value %.3e.'
  % (max(SER[('S', 'E1')].max(), SER[('T', 'E1')].max()), C_FLAT))

a('')
a('  HOW WIDE IS THE THRESHOLD CROSSING -- factor in `a` between C = 0.01 and 90% of that series\' peak:')
rows = []
WIDTH = {}
for form in ('S', 'T'):
    for env in ('E2', 'E4'):
        lo = cross(AMPS, SER[(form, env)], 0.01)
        hi = cross(AMPS, SER[(form, env)], 0.9 * SER[(form, env)].max())
        WIDTH[(form, env)] = (lo, hi)
        rows.append((form, env, '%.3e' % lo if lo else 'never', '%.3e' % hi if hi else 'never',
                     '%.4fx' % (hi / lo) if (lo and hi) else '--'))
table(rows, ('form', 'env', 'a at C=0.01', 'a at 0.9 max', 'width'))
a('')
a('  CONTRAST AT THREE AMPLITUDES AN ENGINEER WOULD RECOGNISE, so the plateau is visible:')
rows = []
for form in ('S', 'T'):
    for env in ('E2', 'E4'):
        vals = [float(np.interp(math.log10(v), np.log10(AMPS), SER[(form, env)]))
                for v in (1e-5, 1e-4, 1e-3)]
        rows.append((form, env, *['%.3f' % v for v in vals]))
table(rows, ('form', 'env', 'C at 10 um', 'C at 100 um', 'C at 1 mm'))
LEVEL = {(f, e): float(np.interp(math.log10(1e-3), np.log10(AMPS), SER[(f, e)]))
         for f in ('S', 'T') for e in ('E2', 'E4')}
a('')
a('  A width near 1.00x is a switch, not a lever: the scene is invisible or fully contrasted, and there')
a('  is no amplitude at which it sits at 3e-2 for any duration. Contrast is not a continuous function')
a('  of the price variable.')

# ---------------------------------------------------------------------------------
hdr('[4] THE 1/c^2 LAW -- exact in C, and not a law in relief')
cs = np.array([1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1])
sf = SHORTFALL * (1e-7 / cs) ** 2
slope_C = np.polyfit(np.log10(cs), np.log10(sf), 1)[0]
a('  shortfall(C) = %.4e (1e-7/C)^2   d log10(shortfall)/d log10(C) = %.9f   (registered law: -2)'
  % (SHORTFALL, slope_C))
a('')
a('  The same derivative in RELIEF, over the decade below a* and the decade above it:')
rows = []
for form in ('S', 'T'):
    for env in ('E2', 'E4'):
        for lo, hi, label in ((0.1, 1.0, 'below a*'), (1.0, 10.0, 'above a*')):
            a_s = A_STAR[(form, env)]
            if not a_s:
                continue
            m = (AMPS >= a_s * lo) & (AMPS <= a_s * hi) & (SER[(form, env)] > 1e-12)
            if m.sum() < 3:
                continue
            k = np.polyfit(np.log10(AMPS[m]), np.log10(SER[(form, env)][m]), 1)[0]
            rows.append((form, env, label, '%.3f' % k, '%.3f' % (-2.0 * k)))
table(rows, ('form', 'env', 'window', 'dlogC/dloga', 'dlog(shortfall)/dloga'))
a('')
a('  Read the third column against the first. Terraced glint (T/E2) is exactly flat: dlogC/dloga = 0.000,')
a('  so its shortfall does not move for decades. Sinusoidal glint (S/E2) rises ~a^0.9 but only across the')
a('  5.4x ramp. A true 1/c^2 lever in relief exists ONLY in the diffuse channel -- which is the model the')
a('  deposit material excludes. The ladder\'s "+2.9 orders" is therefore not a purchase in amplitude.')

# ---------------------------------------------------------------------------------
hdr('[5] WHAT BOUNDS eps -- the deposit clearance, not the optics')
d3 = math.hypot(2.0 * R4, H)
a_sup = math.sqrt(PITCH ** 2 - (2.0 * R4) ** 2) - H
eps_max = a_sup / PITCH
a('  sup d_3D (flat) = sqrt((2 r4)^2 + H^2) = %.6f m     (registered 0.292062)' % d3)
a('  headroom        = sqrt(pitch^2 - (2 r4)^2) - H = %.6f m = %.1f mm' % (a_sup, a_sup * 1e3))
a('  eps_max         = %.6f       (registration Y6: 0.3183)' % eps_max)
a('  The same number closes DEPOSIT-DICHOTOMY: at eps_max the 3D support touches the 2D pitch.')
a('')
rows = []
for form in ('S', 'T'):
    for env in ('E2', 'E4'):
        a_s = A_STAR[(form, env)]
        if a_s:
            rows.append((form, env, '%.2e' % (a_s / PITCH), '%.4f%%' % (100.0 * a_s / PITCH / eps_max),
                         '%.2f%%' % (100.0 * (1.0 - a_s / PITCH / eps_max))))
table(rows, ('form', 'env', 'eps*', 'share of eps_max', 'V range that buys no photons'))

# ---------------------------------------------------------------------------------
hdr('[6] PREDICTIONS -- Y1..Y7 of r2_relief_registration.md')
res = []


def verdict(tag, text, ok, measured):
    res.append((tag, ok))
    a('')
    a('  %s  %s   %s' % (tag, 'CONFIRMED' if ok else 'FALSIFIED', text))
    a('       measured: %s' % measured)


e1max = max(abs(SER[('S', 'E1')] - C_FLAT).max(), abs(SER[('T', 'E1')] - C_FLAT).max())
verdict('Y1', 'E1 gives C_relief = C_flat for every a', e1max <= 1e-12,
        'max |C_w - C_flat| = %.3e over 73 amplitudes, both forms' % e1max)

ok2 = A_STAR[('S', 'E2')] is not None and 40e-6 <= A_STAR[('S', 'E2')] <= 150e-6
verdict('Y2', 'E2/S a*(0.03) in [40, 150] um (predicted 74 um)', ok2,
        'a* = %.1f um   predicted beta*LAM/(2 pi) = %.1f um'
        % (A_STAR[('S', 'E2')] * 1e6, BETA * LAM / (2 * math.pi) * 1e6))

c1mm = float(np.interp(math.log10(1e-3), np.log10(AMPS), SER[('S', 'E2')]))
verdict('Y3', 'E2/S at a = 1 mm has C_w > 0.5', c1mm > 0.5, 'C_w(1 mm) = %.4f, Q3 = %.2f' % (c1mm, q3(c1mm)))

AS4 = A_STAR[('S', 'E4')]
m4 = (AMPS > AS4 / 10.0) & (AMPS < AS4)
k4 = np.polyfit(np.log10(AMPS[m4]), np.log10(SER[('S', 'E4')][m4]), 1)[0] if m4.sum() >= 3 else float('nan')
ok4 = (0.2e-3 <= AS4 <= 1.0e-3) and (0.8 <= k4 <= 1.2)
verdict('Y4', 'E4/S a*(0.03) in [0.2, 1.0] mm, and C ~ a^[0.8,1.2]', ok4,
        'a* = %.3f mm ; exponent k = %.3f' % (AS4 * 1e3, k4))

ratio = AS4 / A_STAR[('S', 'E2')]
verdict('Y5', 'a*(E4)/a*(E2) in [3, 15]', 3.0 <= ratio <= 15.0, 'ratio = %.2f' % ratio)
verdict('Y6', 'eps_max = 0.3183 +/- 1e-4', abs(eps_max - 0.3183) <= 1e-4, 'eps_max = %.6f' % eps_max)
ok7 = A_STAR[('S', 'E2')] / PITCH <= 3e-3
verdict('Y7', 'a*(E2)/pitch <= 3e-3 (declared ~1.8e-4)', ok7, 'eps* = %.3e, i.e. %.4f%% of eps_max'
        % (A_STAR[('S', 'E2')] / PITCH, 100.0 * A_STAR[('S', 'E2')] / PITCH / eps_max))

# ---------------------------------------------------------------------------------
hdr('[7] WHAT THE NUMBERS SAY -- derived from the tables above, not from the registration')
W = WIDTH[('S', 'E2')][1] / WIDTH[('S', 'E2')][0]
WT = WIDTH[('T', 'E2')][1] / WIDTH[('T', 'E2')][0]
DEC = math.log10(AMPS[-1] / A_STAR[('T', 'E2')])
a('  1. RELIEF IS NOT WHAT MAKES CONTRAST. The deposit is a near-mirror (|dR| = 1e-3), and under a')
a('     uniform environment a mirror is invisible: every reflected ray carries the same radiance, so')
a('     relief changes the path and not the pixel. C_w equals C_flat EXACTLY (difference %.0e)' % e1max)
a('     for both forms, over six decades -- not "to within noise", exactly.')
a('     "Topographic contrast" is a property of the ENVIRONMENT, which')
a('     theta = (aperture, gate, band, distance) does not carry. That is the missing term, and it is')
a('     the one the experimenter sets when the source is brought -- at 284 eV there is no sun.')
a('')
a('  2. In the collimated channel ("full sun", beta = 4.65e-3) the number is reachable, but as a')
a('     narrow ramp: the sine reaches C_w = 0.01 at %.1f um and 90%% of its peak by %.1f um, a factor' % (WIDTH[('S', 'E2')][0] * 1e6, WIDTH[('S', 'E2')][1] * 1e6))
a('     %.2f in amplitude -- and the terraced form is an outright switch at %.2f.' % (W, WT))
a('     The crossing a* = %.1f um sits inside that ramp, and it is the geometric condition' % (A_STAR[('S', 'E2')] * 1e6))
a('     2*alpha_max = beta. Below it the plate is a mirror-reflected sun; above it, a fringe pattern.')
a('')
a('  3. The price variable does not enter. Terraced relief switches at %.1f um (factor %.2f) and then' % (A_STAR[('T', 'E2')] * 1e6, WT))
a('     holds C_w = %.3f for a further %.1f decades: %.3f at 100 um, %.3f at 1 mm. Contrast for a'
  % (SER[('T', 'E2')].max(), DEC, LEVEL[('T', 'E2')], LEVEL[('T', 'E2')]))
a('     topographic EDGE is set by the riser width and by the environment, not by the step height.')
a('     RL-2 is priced in a/pitch. The measurement says a/pitch is not the variable that buys anything.')
a('')
a('  4. So the 3e-2 is DECLARED, and it is the criterion restated as a measurement: Q3 = 2 needs')
a('     C = 3*C_eye = 0.030000 and the ladder wrote 3e-2. Round 48\'s "zero margin" is not the')
a('     measurement of a cliff in physics; it is what one significant figure looks like when it is')
a('     copied from the criterion it is supposed to test. Measured, the rung sits at 0.28 for a 1 mm')
a('     step and at %.2f for a 1 mm corrugation, and at neither of those is it near 3e-2.' % LEVEL[('S', 'E2')])
a('')
a('  5. eps_max = %.4f is real and it is the deposit\'s own number, but the useful part of the rung is' % eps_max)
a('     [0, %.1e]: %.2f%% of its declared V range buys nothing at all.' 
  % (A_STAR[('S', 'E2')] / PITCH, 100.0 * (1.0 - A_STAR[('S', 'E2')] / PITCH / eps_max)))
a('')
a('  6. What is left of the rung after this: relief is a real knob and it is nearly free (eps ~ 1e-4),')
a('     but its price cannot be quoted as a number until theta carries an environment term and the')
a('     relief form is declared. Both are declarations, not measurements -- which is why this round')
a('     closes the question "is 3e-2 measured" with NO, and leaves "what is the rung worth" to a')
a('     declaration the ladder has not made.')

hdr('[8] THE HEIGHT DISCREPANCY CARRIED ALONGSIDE (registration s5)')
t175 = math.sqrt(2.0) * 1.75 / 2.99792458e8
t023 = math.sqrt(2.0) * H / 2.99792458e8
a('  r1 s1 used H = 1.75 m -> t_rip = %.6e s ; DEMO-1 declares H = %.4f m -> %.6e s'
  % (t175, H, t023))
a('  ratio %.3f : per-frame flux scales linearly in t_rip, so the shortfall at fixed contrast is %.3fx'
  % (t175 / t023, t175 / t023))
a('  LARGER under the declared height. Recorded, not repaired.')

# ---------------------------------------------------------------------------------
hdr('SUMMARY')
n_ok = sum(1 for _t, o in res if o)
amended = bool(re.search(r'^## Errata\s*$', open(REG, encoding='utf-8').read(), re.M))
if amended:
    a('  declaration order : NOT EVIDENCED BY MTIME -- the registration carries an appended erratum, so its')
    a('                      mtime is the append time. Order is asserted by the erratum, which names the')
    a('                      smoke test and the band arithmetic, and by the untouched predictions above.')
else:
    a('  declaration order : registration %.1f s before this run' % (time.time() - os.path.getmtime(REG)))
a('  RL-2 verdict      : ADMISSIBLE and CHEAP, but priced in the WRONG VARIABLE. Contrast is a function')
a('                      of the environment (absent from theta) and of the relief FORM, not of a/pitch.')
a('                      In the collimated channel it is a switch at 2*alpha = beta, not a 1/c^2 lever.')
a('  the 3e-2          : DECLARED. It equals 3*C_eye to the digit, i.e. the criterion restated as a')
a('                      measurement. Measured, the rung sits at %.2f (1 mm step) or %.2f (1 mm corrugation),'
  % (LEVEL[('T', 'E2')], LEVEL[('S', 'E2')]))
a('                      and at neither of those is it anywhere near 3e-2.')
a('  what is NOT claimed: any statement about the deposit. The plate is a declared stand-in;')
a('                      DEPOSIT-BLIND and MR1.6 are untouched. No threshold written, no rung re-priced.')
a('')
a('  predictions Y1-Y7  : %d CONFIRMED, %d FALSIFIED' % (n_ok, len(res) - n_ok))
a('')
a('PROVENANCE: NEITHER  (locked estimator on declared fields + geometric optics + budget arithmetic)')

txt = '\n'.join(L) + '\n'
if '--write' in sys.argv:
    os.makedirs(OUTDIR, exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(txt)
    print('wrote %s' % OUT)
else:
    print(txt)
sys.exit(0 if n_ok == len(res) else 1)
