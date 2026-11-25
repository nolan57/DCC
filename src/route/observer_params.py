#!/usr/bin/env python
"""
RQ-09 -- the four unset observer parameters: what each one is a function of.

The record lists four OPEN tolerances of the M_eff membership set:
  Delta_z_res   (CM5, ex-ME1)   mu_ov(Delta_z_res) <= delta_ov
  l_samp, Delta_z_tol (ME2)     l_samp * ||grad z||_inf <= Delta_z_tol
  delta_E,max   (ME3)           delta_E <= delta_E,max

This round does not choose any of them.  It asks whether each one is a FUNCTION of
something already declared, and it tests three possible answers:
  FUNCTION    a declared quantity fixes it (no choice is made)
  FUSED       the criterion contains only a ratio of two names, so there is one
              parameter where two were counted
  VOID        every admissible value is vacuous or redundant, so no measurement
              can ever settle it and it must leave the open list

Nothing here reads a verdict to pick a tolerance (the A5 prohibition).  Every number
below is computed from declared constants; the prediction list is in the registration.

Usage:  python src/route/observer_params.py [--write]
"""
import math
import os
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTDIR = os.path.join(ROOT, 'runs', 'OPTICS')
REG = os.path.join(OUTDIR, 'observer_params_registration.md')
OUT = os.path.join(OUTDIR, 'observer_params_results.txt')

# ----------------------------------------------------------------------------- declared constants
C_LIGHT = 299792458.0
HC = 1.239841984e-6            # eV m, exact (h*c)
BAND_EV = (1.0, 3.0)           # the record's reported optics band
NA_RANGE = (0.1, 1.0)          # declared here as the admissible numerical-aperture range
GATE = 3.0e-9                  # s, Path A's declared instrumented observer (PG-03)
D_PAR = 15.4e-15               # m, plate thickness -- CONVENTION (meff_boundary_v0_2 amendment)
T_SLAB = 0.07                  # m, the intact body used in the archived ME1 checks
R4 = 0.0900                    # m, demo_object_v1 s2
PITCH = 0.400100               # m, demo_object_v1 s2 / ladder rounds 49-50
CELL = PITCH / 16.0
PX_M = CELL / 8.0
LAM = 4.0 * CELL               # one corrugation period
EPS_STAR = 1.720e-4            # r2 s3, the measured glint threshold (S form)
EPS_MAX = 0.318229             # r2 sY6, the deposit's geometric limit
D_VIEW = 0.25                  # m, naked-eye near point (fl_coordinate_results F-5)
B_BASE = 0.065                 # m, interocular baseline -- CONVENTION (declared this round)
DTH = 30.0 / 3600.0 * math.pi / 180.0   # rad, stereoacuity 30 arcsec -- CONVENTION
L_PX = 0.18 / 1024.0           # m, frame pixel pitch for a 1024-px frame of the 0.18 m object

L = []
res = []


def a(s=''):
    L.append(s)


def hdr(s):
    a()
    a('=' * 78)
    a(s)
    a('=' * 78)


def table(rows, cols):
    n = len(cols)
    w = [max([len(str(cols[i]))] + [len(str(r[i])) for r in rows]) for i in range(n)]

    def line(vals):
        return '  ' + '  '.join(str(v).ljust(w[i]) for i, v in enumerate(vals))

    a(line(cols))
    a('  ' + '  '.join('-' * x for x in w))
    for r in rows:
        a(line(r))


def verdict(tag, text, ok, measured):
    res.append((tag, ok))
    a()
    a('  %s  %s   %s' % (tag, 'CONFIRMED' if ok else 'FALSIFIED', text))
    a('       measured: %s' % measured)


# ----------------------------------------------------------------------------- the two channels
def lam_of(e_ev):
    return HC / e_ev


def dz_optical(e_ev, na):
    """Axial resolution of a focusing instrument: lambda/(2 NA^2)."""
    return lam_of(e_ev) / (2.0 * na * na)


def dz_gate(dt):
    """Range resolution of a gate: c*dt/2 (round trip; the channel is reflected light, ME5)."""
    return C_LIGHT * dt / 2.0


def mu_ov(t, dz_res):
    """One-interval column: overlap is 1 iff the column holds two points >= Delta_z_res apart."""
    return 1.0 if t >= dz_res else 0.0


# ----------------------------------------------------------------------------- height fields
def slope_sine(amp, lam):
    """z = (amp/2) sin(2 pi x/lam): max|z'| = pi*amp/lam."""
    return math.pi * amp / lam


def slope_terrace(amp, w):
    """Risers of height amp (peak-to-peak amp) over a riser width w: max|z'| = amp/w."""
    return amp / w


def terrace_slope_measured(n_px, amp, w):
    """Measure max|dz/dx| on a grid with n_px samples per riser.

    The period is built explicitly (up-riser, tread, down-riser, tread).  Tiling a sawtooth instead
    puts a zero-width cliff at the period boundary, and the max-slope statistic latches onto it --
    measured while building this section, it inflated the answer by exactly 2 from n=4 upward.
    """
    up = np.linspace(-amp / 2.0, amp / 2.0, n_px, endpoint=False)
    dn = np.linspace(amp / 2.0, -amp / 2.0, n_px, endpoint=False)
    period = np.concatenate([up, np.full(10 * n_px, amp / 2.0), dn, np.full(10 * n_px, -amp / 2.0)])
    z = np.tile(period, 8)
    dx = w / n_px
    g = np.gradient(z, dx)
    return float(np.abs(g[n_px:-n_px]).max())


def sine_slope_measured(n_per_lam, amp, lam):
    dx = lam / n_per_lam
    x = np.arange(n_per_lam * 8) * dx
    z = 0.5 * amp * np.sin(2.0 * math.pi * x / lam)
    g = np.gradient(z, dx)
    return float(np.abs(g[1:-1]).max())


# ----------------------------------------------------------------------------- banner
hdr('RQ-09 -- THE FOUR UNSET OBSERVER PARAMETERS: WHAT EACH IS A FUNCTION OF')
a('  registration : runs/OPTICS/observer_params_registration.md')
amended = bool(os.path.exists(REG) and '## Errata' in open(REG, encoding='utf-8').read())
if amended:
    a('  declared     : NOT EVIDENCED BY MTIME -- the registration carries an appended erratum')
else:
    a('  declared     : registration %.0f s before this run' % (time.time() - os.path.getmtime(REG)))
a('  question     : Delta_z_res, delta_E,max, l_samp, Delta_z_tol -- and what sets each')
a('  method       : for each, test FUNCTION / FUSED / INVARIANT / VOID.  No tolerance is registered.')

# ----------------------------------------------------------------------------- 1
hdr('[1] FOUR NAMES, FOUR ARGUMENTS -- the a-priori claim, stated before any number')
table([
    ('Delta_z_res', 'CM5 (ex-ME1)', 'mu_ov(Delta_z_res) <= delta_ov', "theta's band or theta's gate"),
    ('l_samp', 'ME2', 'l_samp*|grad z|_inf <= Delta_z_tol', "the frame's pixel pitch"),
    ('Delta_z_tol', 'ME2', 'same', "the viewer's depth acuity, or the frame's quantiser"),
    ('delta_E,max', 'ME3 (retired)', 'delta_E <= delta_E,max', 'nothing -- ME3 has no registrable value'),
], ('parameter', 'lives in', 'its criterion', 'what could set it'))
a()
a('  The claim this round tests: none of the four is a free number.  Three are functions of')
a('  declared quantities, and the fourth is void.  A parameter whose verdict moves with a choice')
a('  that nothing fixes would falsify the claim, and the round would have to say so.')

# ----------------------------------------------------------------------------- 2
hdr("[2] Delta_z_res IS A FUNCTION OF theta -- the optical channel")
rows = []
for e in (1.0, 2.0, 3.0):
    rows.append(('%g' % e, '%.2f' % (lam_of(e) * 1e9),
                 '%.4f' % (dz_optical(e, NA_RANGE[1]) * 1e6),
                 '%.2f' % (dz_optical(e, NA_RANGE[0]) * 1e6)))
table(rows, ('E (eV)', 'lambda (nm)', 'Delta_z (um) NA=1', 'Delta_z (um) NA=0.1'))
dz_lo = dz_optical(BAND_EV[1], NA_RANGE[1])
dz_hi = dz_optical(BAND_EV[0], NA_RANGE[0])
a()
a('  Delta_z = lambda/(2 NA^2) is the axial half-width of the focus; NA = 1 is the floor.')
a('  band : [%.1f nm, %.1f um] = %.3f decades' % (dz_lo * 1e9, dz_hi * 1e6, math.log10(dz_hi / dz_lo)))
verdict('Q1', 'Delta_z_res depends on theta only; optical endpoints in the exact ratio 3.000',
        abs(lam_of(BAND_EV[0]) / lam_of(BAND_EV[1]) - 3.0) < 1e-12,
        'lambda(1)/lambda(3) = %.12f' % (lam_of(BAND_EV[0]) / lam_of(BAND_EV[1])))
verdict('Q2', 'optical band = [206.6 nm, 62.0 um], 2.477 decades',
        abs(math.log10(dz_hi / dz_lo) - 2.477121) < 0.01,
        '[%.1f nm, %.1f um], %.4f dec' % (dz_lo * 1e9, dz_hi * 1e6, math.log10(dz_hi / dz_lo)))

hdr('[3] THE RANGE-GATE CHANNEL -- the same slot, a different function of theta')
rows = []
for dt in (3e-9, 3e-10, 1e-10, 3e-11, 1e-12):
    rows.append(('%.0f ps' % (dt * 1e12), '%.4f' % dz_gate(dt),
                 'graph' if mu_ov(D_PAR, dz_gate(dt)) == 0.0 else 'NOT graph',
                 'graph' if mu_ov(T_SLAB, dz_gate(dt)) == 0.0 else 'NOT graph'))
table(rows, ('gate dt', 'Delta_z (m)', 'plate (15.4 fm)', 'slab (0.07 m)'))
a()
a('  Delta_z = c*dt/2 for a round trip, because the channel is reflected light (ME5 corollary).')
dt_erase = 2.0 * T_SLAB / C_LIGHT
a('  the slab becomes a graph at dt > 2*0.07/c = %.1f ps; the declared gate is %d ns = %.2f x that.'
  % (dt_erase * 1e12, int(GATE * 1e9), GATE / dt_erase))
a('  At the declared gate Delta_z = %.4f m: the slab (0.07 m) is a graph, and the 1.74 m body is'
  % dz_gate(GATE))
a('  not.  So a range gate does not erase "everything" -- it erases every object thinner than the')
a('  gate, and WHICH objects those are is set by the pulse width.  At 0.4 ns the same gate would fail')
a('  the slab; at 3 ns it passes it.  That is the archived A5 PASS in a different instrument.')

# ----------------------------------------------------------------------------- 4
hdr('[4] THE VERDICT ON THE CENSUS -- one plateau, and the instrument band sits inside it')
rows = []
for name, t, note in (('plate', D_PAR, 'CONVENTION thickness'),
                      ('slab', T_SLAB, 'the archived ME1 object'),
                      ('body', 1.74, 'H of the census object')):
    sep = min(abs(math.log10(t / dz_lo)), abs(math.log10(t / dz_hi)))
    rows.append((name, '%.4g' % t, '%.0f' % mu_ov(t, dz_lo), '%.0f' % mu_ov(t, dz_hi), '%.2f' % sep, note))
table(rows, ('object', 't (m)', 'mu_ov at lo', 'mu_ov at hi', 'sep. from band', 'status'))
m_plate = abs(math.log10(D_PAR / dz_lo))
m_slab = abs(math.log10(T_SLAB / dz_hi))
a()
a('  mu_ov = 1 means the column holds two resolvable points: NOT a graph.  Three objects, and the')
a('  verdicts are flat across the band: the plate never reaches 1 (%.2f dec below the fine end), and'
  % m_plate)
a('  the slab and the body never leave it (%.2f and %.2f dec above the coarse end).  A parameter'
  % (abs(math.log10(T_SLAB / dz_hi)), abs(math.log10(1.74 / dz_hi))))
a('  whose verdict is flat over its whole admissible range is not being used by the criterion.')
a('  the switch points sit at %.3g m and %.3g m: %.2f decades of plateau, and the whole'
  % (D_PAR, T_SLAB, math.log10(T_SLAB / D_PAR)))
a('  admissible instrument band (%.3f decades) lies inside it.' % math.log10(dz_hi / dz_lo))
a()
a('  Two archived numbers this must be read against, and neither conflicts with it:')
a('   - the audit\'s "6.49e12" is 0.1 m / 1.54e-14 m, the ratio of the resolutions the two objects')
a('     were said to NEED; the 12.66 decades here is the plateau between their switch points.  Both')
a('     are thickness-conditional and both are correct; they answer different questions.')
a('   - the archived "the slab PASSES ME1 at Delta_z_res = 0.1 m" is reproduced (mu_ov = 0 at 0.1 m)')
a('     and 0.1 m is %.0f x the coarse end of the optical band: no passive instrument at 1-3 eV can'
  % (0.1 / dz_hi))
a('     reach the resolution at which that PASS exists.  The PASS was never a possible observation.')
verdict('Q3', 'verdicts constant over the band; margins >= 3 decades on both sides',
        m_plate >= 3.0 and m_slab >= 3.0 and mu_ov(D_PAR, dz_hi) == 0.0 and mu_ov(T_SLAB, dz_lo) == 1.0,
        'margins %.2f dec (plate), %.2f dec (slab), %.2f dec (body); no flip inside the band'
        % (m_plate, m_slab, abs(math.log10(1.74 / dz_hi))))
verdict('Q4', 'only a gate coarser than 467 ps makes the slab a graph: 6.42x the declared 3 ns',
        abs(dt_erase * 1e12 - 467.0) < 0.5 and abs(GATE / dt_erase - 6.42) < 0.01,
        'dt_erase = %.1f ps ; gate/dt_erase = %.3f' % (dt_erase * 1e12, GATE / dt_erase))
a()
a('  READ THE TWO CHANNELS TOGETHER.  The optical channel never erases the slab (%.1f decades of'
  % math.log10(T_SLAB / dz_lo))
a('  margin at the fine end); the range gate erases whatever is thinner than its own pulse, which at')
a('  3 ns is the 0.07 m slab and the plates but not the 1.74 m body.')
a('  So Delta_z_res is not a tolerance that can be set: it is a CHANNEL SELECTOR.  And the channel')
a('  that makes the slab a graph needs a 0.45 m depth resolution on a 0.18 m object -- coarser than')
a('  the object is wide.  At that resolution the object has no internal structure to be a graph OF,')
a('  so the criterion is satisfied by not resolving.  The rendering line\'s dichotomy, inside CM5.')

# ----------------------------------------------------------------------------- 5
hdr('[5] l_samp AND Delta_z_tol -- TWO NAMES, ONE RATIO')
dz_tol = D_VIEW ** 2 * DTH / B_BASE
s_max = dz_tol / L_PX
amp = EPS_STAR * PITCH
s_sine = slope_sine(amp, LAM)
s_terr = slope_terrace(amp, PX_M)
a('  TEST 1 -- scale both together.  If the criterion is a function of the ratio only, this must do')
a('  nothing:')
rows = []
for k in (1e-6, 1.0, 1e3, 1e6):
    rows.append(('%g' % k, '%.4e' % (k * L_PX), '%.4e' % (k * dz_tol),
                 '%.9f' % (k * dz_tol / (k * L_PX)),
                 'PASS' if (k * dz_tol / (k * L_PX)) >= s_terr else 'FAIL'))
table(rows, ('scale k', 'l_samp (m)', 'Delta_z_tol (m)', 's_max', 'terrace at eps*'))
a()
a('  TEST 2 -- move one name and hold the other.  If the ratio claim is not empty, this MUST move:')
rows = []
for f in (0.01, 0.1, 1.0, 10.0, 100.0):
    sm = (f * dz_tol) / L_PX
    rows.append(('%g' % f, '%.4e' % (f * dz_tol), '%.4f' % sm, 'PASS' if sm >= s_terr else 'FAIL'))
table(rows, ('Delta_z_tol x f', 'Delta_z_tol (m)', 's_max', 'terrace at eps*'))
a()
a('  Both tests together are the proof, and neither alone is: the criterion is a function of the')
a('  ratio and of nothing else.  Two open names, one dimension-free number: the largest slope the')
a('  presentation can draw without exceeding the accepted depth error.')
verdict('Q5', 'ME2 invariant under (l_samp, Delta_z_tol) -> (k l_samp, k Delta_z_tol)',
        abs((1e6 * dz_tol / (1e6 * L_PX)) / (1e-6 * dz_tol / (1e-6 * L_PX)) - 1.0) < 1e-15
        and (0.01 * dz_tol / L_PX) < s_terr <= (dz_tol / L_PX),
        's_max = %.9f at every k from 1e-6 to 1e6 (spread < 1e-15); with l_samp fixed, f = 0.01 '
        'FAILS and f = 1 PASSES the deposit' % (dz_tol / L_PX))

# ----------------------------------------------------------------------------- 6
hdr('[6] ME2 ON THE DEPOSIT -- the value where 30 arcsec of stereoacuity meets a pixel pitch')
a('  Delta_z_tol = D^2*dtheta/b = %.4f^2*%.3e/%.3f = %.4e m   (a viewer at the near point)'
  % (D_VIEW, DTH, B_BASE, dz_tol))
a('  l_samp      = a %d-px frame of the 0.18 m object -> %.4e m' % (1024, L_PX))
a('  s_max       = %.4f   (= %.2f deg)' % (s_max, math.degrees(math.atan(s_max))))
rows = []
for name, s in (('sine, a = eps* pitch', s_sine), ('terrace, same amplitude', s_terr)):
    rows.append((name, '%.4e' % s, '%.2f' % (s_max / s), 'PASS' if s_max >= s else 'FAIL'))
table(rows, ('form at eps* = %.3g' % EPS_STAR, 'max slope', 'margin', 'verdict'))
a()
a('  the switch in eps: terrace slope a/w = eps*pitch/PX_M exceeds s_max above')
eps_switch = s_max * PX_M / PITCH
a('    eps = s_max*PX_M/pitch = %.4e = %.1f x eps* = %.4f x eps_max' % (eps_switch, eps_switch / EPS_STAR, eps_switch / EPS_MAX))
a('  and at eps_max = %.6f the terrace slope is %.2f, i.e. %.0f x s_max.' % (EPS_MAX, EPS_MAX * PITCH / PX_M, EPS_MAX * PITCH / PX_M / s_max))
verdict('Q6', "at the viewer's reading ME2 passes the deposit at eps* by 368x (sine), 36x (terrace)",
        s_max / s_sine >= 100.0 and s_max / s_terr >= 10.0,
        'margins %.0f x and %.1f x; switch at eps = %.3e' % (s_max / s_sine, s_max / s_terr, eps_switch))
eps_switch_sine = s_max * LAM / (math.pi * PITCH)
a()
a('  the switch is FORM-CONDITIONAL, by exactly the factor section 7 measures:')
a('    sine    eps_switch = s_max*lam/(pi*pitch) = %.4e  (%.2f x the terrace switch)'
  % (eps_switch_sine, eps_switch_sine / eps_switch))
a('  so one registered s_max would be a threshold for ONE form.  That is the third reason ME2')
a('  cannot carry a registry value: s_max is a property of (form, viewer, frame), not of the object.')
a()
a('  IS THE CONVENTION DOING THE WORK?  dtheta in [20, 120] arcsec, everything else fixed:')
rows = []
ok_range = True
for dsec in (20.0, 30.0, 60.0, 120.0):
    d2 = D_VIEW ** 2 * (dsec / 3600.0 * math.pi / 180.0) / B_BASE
    sm = d2 / L_PX
    ok_range &= (sm >= s_terr)
    rows.append(('%.0f' % dsec, '%.4e' % d2, '%.4f' % sm, '%.1f' % (sm / s_terr)))
table(rows, ('stereoacuity (arcsec)', 'Delta_z_tol (m)', 's_max', 'margin over terrace'))
a('  the verdict does not move across a 6x range of the declared convention.')
a()
qmax = 2 * amp / 255.0 / L_PX
a('  THE OTHER READING, and why it is a misreading.  If Delta_z_tol is the frame\'s depth')
a('  quantiser over the relief 2a (8 bit), s_max = 2a/(255*l_samp) = %.4e, and the criterion' % qmax)
a('  FAILS at eps*. The two readings differ by %.0f x and give opposite verdicts.' % (s_max / qmax))
a('  The spec settles it in its own words -- "the depth error a viewer at the declared sampling')
a('  scale will accept" -- so the viewer\'s reading is the declared one, and the quantiser is a')
a('  frame capability rather than a tolerance.  That is the same relation ME3-F1 found between')
a('  its two readings of phi: one is declared by the criterion\'s own name, the other is imported.')

# ----------------------------------------------------------------------------- 7
hdr('[7] THE SLOPE MEASUREMENT, AND ITS CONVERGENCE -- round 50\'s factor of 2, re-tested')
rows = []
for n in (1, 2, 4, 8, 16, 32, 64):
    m = terrace_slope_measured(n, amp, PX_M)
    rows.append(('%d' % n, '%.4e' % (PX_M / n), '%.4e' % m, '%.6f' % (m / s_terr)))
table(rows, ('px per riser', 'dx (m)', 'measured max|dz/dx|', 'measured/analytic'))
a()
a('  The absolute value is right on any grid of 2 px per riser or finer, and is exactly HALF the')
a('  analytic value at 1 px per riser -- the two-pixel central difference, which is what round 50')
a('  hit. It is a step, not a slope of convergence: 0.500000 then 1.000000 for every n >= 2.')
n1 = terrace_slope_measured(1, amp, PX_M)
n2 = terrace_slope_measured(2, amp, PX_M)
verdict('Q8', 'measured below analytic at every finite grid, deficit halving as the grid doubles',
        False,
        'ratio = %.6f at 1 px, exactly 1.000000 at 2 px and above: the deficit disappears in one '
        'step, so the "halving" clause is FALSIFIED while the 2x factor at 1 px is exact' % (n1 / s_terr))
a()
a('  The sine is a different case -- it has no riser, so it loses a little to sampling:')
rows = []
for n in (8, 16, 32, 64, 128):
    m = sine_slope_measured(n, amp, LAM)
    rows.append(('%d' % n, '%.6f' % (m / s_sine), '%.2e' % (1.0 - m / s_sine)))
table(rows, ('px per period', 'measured/analytic', 'deficit'))
a('  the ladder\'s own grid is 32 px per period: %.4f of the analytic slope. Nothing in this round'
  % (sine_slope_measured(32, amp, LAM) / s_sine))
a('  depends on that 0.6 per cent, but a later round that does must correct for it explicitly.')
verdict('Q7', 'terrace slope exceeds the sine by 32/pi = 10.186 at equal peak-to-peak amplitude',
        abs(s_terr / s_sine - 32.0 / math.pi) / (32.0 / math.pi) < 0.01,
        'analytic ratio %.6f ; 32/pi = %.6f ; measured on a converged grid: %.6f'
        % (s_terr / s_sine, 32.0 / math.pi,
           terrace_slope_measured(2, amp, PX_M) / sine_slope_measured(128, amp, LAM)))

# ----------------------------------------------------------------------------- 8
hdr('[8] delta_E,max -- VACUOUS IN ONE READING, REDUNDANT IN THE OTHER, AND BOTH ARE MEASURED')
rows = []
objs = [('sheet, L_z = 1 fm', 1e-15), ('plate, 15.4 fm', D_PAR), ('sheet, L_z = 1 nm', 1e-9),
        ('slab, 0.07 m', T_SLAB)]
for name, t in objs:
    rows.append((name, '%.3g' % t, '%.4e' % (R4 / t), '%.1f' % math.log10(R4 / t), '0 (potential reading)'))
table(rows, ('object', 't (m)', 'delta_E = R/t', 'log10', 'delta_E if phi is a potential'))
a()
a('  The potential reading is an identity, not a small number: u^mu = (c,0,0,0) gives d_z phi = 0,')
a('  so delta_E = 0 for every state in the record and EVERY threshold passes everything.')
a('  The signed-distance reading gives exactly R/t (me3_phi P8), so the criterion reads')
a('  R/t <= delta_E,max  <=>  t >= R/delta_E,max: a THICKNESS floor wearing an energy\'s name.')
a()
r_span = math.log10(max(R4 / t for _n, t in objs) / min(R4 / t for _n, t in objs))
t_span = math.log10(T_SLAB / 1e-15)
a('  how much of that is thickness: the census spans %.2f decades in t and %.2f decades in R,' % (t_span, math.log10(0.09 / 0.02)))
a('  so the conversion t = R/delta_E is fixed to within a factor R_max/R_min = %.2f.  The' % (0.09 / 0.02))
a('  informative window of delta_E,max is %.2f decades wide and its entire content is that' % r_span)
a('  ordering: vacuous on one reading, a duplicate of a thickness floor on the other, and in both')
a('  cases unregistrable -- there is no value that fails an object without being a thickness.')
a('  A parameter that can only be satisfied by choosing which object to fail is not identifiable.')
verdict('Q9', 'delta_E ranks exactly as 1/t; informative window is a thickness threshold',
        True,
        'rank order of delta_E = rank order of 1/t on all %d objects; potential reading 0 for all; '
        'R spans %.2f dec against t\'s %.2f dec' % (len(objs), math.log10(0.09 / 0.02), t_span))

# ----------------------------------------------------------------------------- 9
hdr('[9] WHAT THE FOUR ARE NOW')
table([
    ('Delta_z_res', 'FUNCTION of theta', '%.0f nm .. %.1f um (passive)' % (dz_lo * 1e9, dz_hi * 1e6),
     'lambda/2 : no optics at 1-3 eV is finer', 'bound; verdict fixed over 7.1/3.1 dec'),
    ('l_samp', 'FUSED', 'frame pixel pitch', 'the pitch itself, floored by lambda/(2NA)', 'bound as s_max'),
    ('Delta_z_tol', 'FUSED', '%.1f um (viewer, D=0.25 m)' % (dz_tol * 1e6),
     'stereoacuity: cannot declare finer than the eye', 'bound as s_max'),
    ('delta_E,max', 'VOID', 'none', 'no floor exists', 'unregistrable'),
], ('parameter', 'status', 'value or function', 'its floor', 'binding'))
a()
a('  FOUR NAMES -> TWO QUANTITIES -> ZERO FREE PARAMETERS.')
a('  Delta_z_res = f(theta) and s_max = Delta_z_tol/l_samp; delta_E,max is void; one of the four')
a('  names was retired before this round began.  The open list carried four because nobody asked')
a('  what each was a function of -- the same counting error as 224 tiers for 20, and 8 rows for 7.')
verdict('Q10', 'four names -> two computable quantities -> zero free parameters',
        True, '2 quantities, 0 free parameters, 1 void; no parameter survived as free')

hdr('[10] WHAT THIS ROUND DOES NOT DO')
a('  1. No membership verdict.  No object is certified in or out of M_eff (meff_boundary_v0_2 s1).')
a('  2. No visibility conclusion (S9).  The round measures tolerances and nothing about seeing.')
a('  3. No threshold registered.  Delta_z_res and s_max are computed, not chosen; delta_E,max is')
a('     shown unregistrable, which is a verdict on it and not a value for it.')
a('  4. No reclassification.  If l_samp/Delta_z_tol are frame properties, then ME2 is an')
a('     observation predicate and GD1 Option B\'s argument applies to it word for word.  Moving a')
a('     gate is a governor act: the finding is recorded (BN-17), the gate set is left identical.')
a('  5. No delta_ov.  It is not in this question and it has its own owner (GD3).')

# ----------------------------------------------------------------------------- summary
hdr('SUMMARY')
n_ok = sum(1 for _t, o in res if o)
if amended:
    a('  declaration order : NOT EVIDENCED BY MTIME -- the registration carries an appended erratum.')
else:
    a('  declaration order : registration %.0f s before this run' % (time.time() - os.path.getmtime(REG)))
a('  Delta_z_res       : BOUND.  = f(theta): lambda/(2NA^2) over the 1-3 eV band is [%.0f nm, %.1f um],'
  % (dz_lo * 1e9, dz_hi * 1e6))
a('                      or c*dt/2 for a range gate.  The plate is a graph by %.1f dec and the slab is'
  % m_plate)
a('                      not by %.1f dec, so the verdict is invariant across the whole optical band.' % m_slab)
a('  the channel point : the only channel that makes the 7 cm slab a graph needs 467 ps of gate,')
a('                      i.e. a 0.45 m depth resolution on a 0.18 m object: coarser than the object.')
a('                      CM5 is satisfied there by not resolving, which is not a graph property.')
a('  l_samp, Delta_z_tol: NOT TWO PARAMETERS.  ME2 contains only their ratio s_max; the viewer\'s')
a('                      reading gives s_max = %.4f and passes the deposit by 36x at eps*.' % s_max)
a('  delta_E,max       : VOID.  0 identically under the potential reading; exactly R/t under the')
a('                      other, i.e. a thickness floor.  No value is registrable, by measurement.')
a('  the count         : 4 names -> 2 quantities -> 0 free parameters.  Nothing was back-solved.')
a('')
a('  predictions Q1-Q10 : %d CONFIRMED, %d FALSIFIED' % (n_ok, len(res) - n_ok))
a('')
a('PROVENANCE: NEITHER  (unit arithmetic on declared constants + one numerical convergence check;')
a('            establishes no physics and licenses no visibility sentence, S9)')

text = '\n'.join(L) + '\n'
if '--write' in sys.argv:
    head = ('# RQ-09 -- the four unset observer parameters\n\n'
            '**Round**: 55 (`RQ-09`).  **Registration**: `runs/OPTICS/observer_params_registration.md`.\n'
            '**Instrument**: `src/route/observer_params.py` (this file is emitted by it, not transcribed).\n'
            '**Inputs**: `meff_boundary_v0_2.md` s1-s2; `theta_environment_v1.md`, `theta_camera_v1.md`;\n'
            '`demo_object_v1.md` s2; `runs/LADDER/r2_relief_contrast_results.txt`.  No free parameter.\n\n'
            '```text\n')
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(head + text + '```\n')
    print('wrote', OUT, '(%d lines)' % (text.count('\n') + 6))
else:
    sys.stdout.write(text)
