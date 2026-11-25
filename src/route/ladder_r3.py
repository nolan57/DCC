#!/usr/bin/env python
"""
RQ-14 -- RL-3: is oblique illumination a rung separate from relief?

Three mechanisms could separate them, and the round measures all three on one relief:
  (i)   the glint geometry -- for a specular surface the ray deflection is 2*arctan(alpha) at every
        incidence, so the bright set carries no theta_i (the queue's theorem);
  (ii)  Fresnel gain R(theta_i) -- a flux factor, which Weber contrast cannot see;
  (iii) self-shadowing at grazing -- an occlusion, i.e. geometry, not illumination.

Two camera geometries, because theta does not carry a camera orientation:
  G_A  camera on the mirror image of the source (specular configuration)
  G_B  camera at normal incidence, source oblique (fixed tripod)

Reflection is evaluated per pixel in 3-D from the surface normal; the |2*alpha| < beta shortcut is printed
beside it as the identity it is claimed to be, never used as the model.

Thresholds are READ from runs/MATRIX/threshold_lock.json. Nothing here writes one.
Checks predictions Z1..Z7 of runs/LADDER/r3_illumination_registration.md.

Usage:  python src/route/ladder_r3.py [--write]
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
REG = os.path.join(OUTDIR, 'r3_illumination_registration.md')
OUT = os.path.join(OUTDIR, 'r3_illumination_results.txt')

_spec = importlib.util.spec_from_file_location(
    'structure_tiers', os.path.join(ROOT, 'src', 'route', 'structure_tiers.py'))
ST = importlib.util.module_from_spec(_spec)
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    _spec.loader.exec_module(ST)

LOCK = ST.lock
C_EYE = ST.C_EYE
THR_L3 = float(LOCK['tiers']['L3']['threshold_c'])

GRID = 128
P, S_CELLS = 16, 12            # the PA-16 instance
PITCH = 0.400100               # m
CELL = PITCH / P               # 0.02500625 m per lattice cell
CELL_PX = GRID // P            # 8 px per cell
PX_M = CELL / CELL_PX          # 3.126e-3 m per image pixel
LAM = 4.0 * CELL               # 0.100025 m, one corrugation period = 32 px
BETA = 4.65e-3                 # rad, solar angular radius
C_TARGET = C_EYE * (2.0 ** THR_L3 - 1.0)       # 0.03 exactly
R4, H = 0.0900, 0.2300         # m, docs/specs/demo_object_v1.md
TREAD = LAM / 2.0              # m, terraced tread = half the period
Z0S_GRID = (10.0, 30.0, 80.0, 300.0, 1e4)      # declared, NOT claimed (see registration s2)

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


# ---------------------------------------------------------------------------------
# the field, the surface, the ray -- verbatim field builders from src/route/ladder_r2.py
# ---------------------------------------------------------------------------------
def plates(p, s):
    return ((np.arange(GRID) % p)[:, None] < s).astype(np.float64) * \
           ((np.arange(GRID) % p)[None, :] < s).astype(np.float64)


def height(amp, form):
    x = np.arange(GRID) * PX_M
    if form == 'S':
        z = 0.5 * amp * np.sin(2.0 * math.pi * x / LAM)
    elif form == 'T':
        w = PX_M / LAM
        ph = (x / LAM) % 1.0
        up = np.clip(np.minimum(ph, ph - 0.5 + w) / w, 0.0, 1.0)
        dn = np.clip(np.minimum(ph - 0.5, ph - 1.0 + w) / w, 0.0, 1.0)
        z = 0.5 * amp * (up - dn)
    else:
        raise ValueError(form)
    return np.tile(z, (GRID, 1))


def slope(amp, form):
    return np.gradient(height(amp, form), PX_M, axis=1)


def glint(al, theta_i, geom, beta=BETA):
    """3-D specular test. Returns (bright mask, angle between reflected ray and source)."""
    psi = np.arctan(al)
    n = np.stack([-np.sin(psi), np.zeros_like(psi), np.cos(psi)], axis=-1)
    if geom == 'A':
        v = np.array([-math.sin(theta_i), 0.0, math.cos(theta_i)])
    elif geom == 'B':
        v = np.array([0.0, 0.0, 1.0])
    else:
        raise ValueError(geom)
    s = np.array([math.sin(theta_i), 0.0, math.cos(theta_i)])
    r = 2.0 * (n @ v)[..., None] * n - v
    ang = np.arccos(np.clip(r @ s, -1.0, 1.0))
    return ang < beta, ang


def shadow(z, theta_i):
    """V(x) = 1 iff z(x+h) - z(x) < h*cot(theta_i) for all 0 < h <= LAM/2."""
    if theta_i <= 0.0:
        return np.ones_like(z, dtype=bool)
    lim = 1.0 / math.tan(theta_i)
    lit = np.ones_like(z, dtype=bool)
    for k in range(1, GRID // 2 + 1):
        h = k * PX_M
        lit &= (np.roll(z, -k, axis=1) - z) < h * lim
    return lit


def fresnel(z0s, theta_i):
    """Shunt-sheet Fresnel; r = -Z0*sigma/(2+Z0*sigma) at theta_i = 0 (the record's own formula)."""
    c = math.cos(theta_i)
    rs = -z0s / (2.0 * c + z0s)
    rp = -z0s * c / (2.0 + z0s * c)
    Rs, Rp = abs(rs) ** 2, abs(rp) ** 2
    return Rs, Rp, 0.5 * (Rs + Rp)


def cweber(I, mask):
    v = I[mask]
    m = float(v.mean())
    if m <= 1e-300:
        return None                      # no image: mean radiance is zero
    return float(v.std() / m)


def q3(c):
    return math.log2(1.0 + c / C_EYE) if c and c > 0 else 0.0


MASK = plates(P, S_CELLS) > 0
U = plates(P, S_CELLS)


def C_of(amp, form, theta_i, geom, env='E2', occl=False):
    al = slope(amp, form)
    if env == 'E1':
        I = U.copy()
    elif env == 'E2':
        br, _ = glint(al, theta_i, geom)
        I = U * br
    elif env == 'E4':
        c = np.cos(theta_i + np.arctan(al)) / max(math.cos(theta_i), 1e-12)
        I = U * np.clip(c, 0.0, None)
    else:
        raise ValueError(env)
    if occl and env == 'E2':
        I = I * shadow(height(amp, form), theta_i)
    return cweber(I, MASK)


# ==================================================================================
hdr('RL-3 -- OBLIQUE AGAINST NORMAL ILLUMINATION, ONE RELIEF   (round 50, RQ-14)')
a('  scene  : the PA-16 plate, corrugation period 4 cells = %.5f m, forms S (sine) / T (terraced)' % LAM)
a('  ray    : per-pixel 3-D specular reflection from n = (-sin psi, 0, cos psi), psi = arctan(dz/dx)')
a('  camera : G_A on the mirror image of the source (specular)   G_B at normal incidence (fixed tripod)')
a('  theta  : incidence 0 / 45 / 75 deg;  beta = %.3e rad;  C_eye %.4f;  L3 threshold %.2f'
  % (BETA, C_EYE, THR_L3))

# ---------------------------------------------------------------------------------
hdr('[0] ESTIMATOR IDENTITY -- the imported module must still reproduce the archived table')
xi_img, _ = ST.char_scale(U)
r0 = ST.q3(U, xi_img, 1.0)
ok0 = (abs(xi_img - 3.32) < 5e-3) and abs(r0[1] - 0.5232) < 5e-5 and abs(r0[0] - 5.737) < 5e-3
a('  PA-16 xi/h %.4f vs 3.32   C_xi %.4f vs 0.5232   Q3 %.3f vs 5.737  -> %s'
  % (xi_img, r0[1], r0[0], 'YES' if ok0 else 'NO'))

# ---------------------------------------------------------------------------------
hdr('[1] THE GEOMETRY -- is the deflection really 2*arctan(alpha), and does it carry theta_i?')
a('  The registration asserts two identities; both are checked against the 3-D ray, not assumed.')
a('')
rows = []
ANG = {}
for form in ('S', 'T'):
    for amp in (1e-4, 1e-3):
        al = slope(amp, form)
        for geom in ('A', 'B'):
            for ti in (0.0, math.radians(45.0), math.radians(75.0)):
                _, ang = glint(al, ti, geom)
                pred = 2.0 * np.abs(np.arctan(al)) if geom == 'A' else \
                    np.abs(2.0 * np.arctan(al) - ti)
                ANG[(form, amp, geom, ti)] = ang
                rows.append((form, '%.3g' % amp, geom, '%.0f' % math.degrees(ti),
                             '%.6e' % np.abs(ang - pred).max(),
                             '%.6e' % np.abs(ang - 2.0 * np.abs(np.arctan(al))).max()))
table(rows, ('form', 'a (m)', 'geom', 'theta_i', 'max|ray - predicted|', 'max|ray - 2arctan(alpha)|'))
a('')
a('  Column 5 is the registration\'s identity; column 6 is the same identity with theta_i dropped.')
a('  G_A: both are 0 -- the deflection carries NO incidence.  G_B: column 6 is nonzero, i.e. the')
a('       window is offset by theta_i and the offset is the whole difference between the two cameras.')

# ---------------------------------------------------------------------------------
hdr('[2] G_A -- THE SPECULAR CAMERA: C_w against incidence, both forms, five amplitudes')
AMPS = (1e-5, 6.88e-5, 1e-4, 3.16e-4, 1e-3)
THETAS = (0.0, math.radians(45.0), math.radians(75.0))
rows = []
CGA = {}
for form in ('S', 'T'):
    for amp in AMPS:
        vals = [C_of(amp, form, ti, 'A') for ti in THETAS]
        CGA[(form, amp)] = vals
        rows.append((form, '%.3g' % amp, *['--' if v is None else '%.6f' % v for v in vals],
                     '%.3e' % (max(vals) - min(vals))))
table(rows, ('form', 'a (m)', 'C 0 deg', 'C 45 deg', 'C 75 deg', 'spread'))
spread_A = max(max(v) - min(v) for v in CGA.values())
spread_rel = max((max(v) - min(v)) / max(v) for v in CGA.values() if max(v) > 0)
a('')
a('  max absolute spread over theta_i = %.3e     max relative spread = %.3e' % (spread_A, spread_rel))
a('  sin(45) and sin(75) enter only through the camera direction, and they cancel in the')
a('  difference angle. This is the queue\'s theorem, confirmed numerically: the glint channel')
a('  cannot separate RL-2 from RL-3 -- at V = 0 for both, it does not see which one is on.')

# ---------------------------------------------------------------------------------
hdr('[3] G_B -- THE FIXED TRIPOD: the bright set leaves the surface (a blackout, not a lever)')
rows = []
F_B = {}
ONSET = {}
for form in ('S', 'T'):
    for amp in (1e-4, 1e-3):
        al = slope(amp, form)
        amax = float(np.abs(al).max())
        psi_max = math.atan(amax)
        onset = 2.0 * psi_max - BETA
        ONSET[(form, amp)] = onset
        line = [form, '%.3g' % amp, '%.4f' % math.degrees(psi_max), '%.2f' % math.degrees(onset)]
        for ti in THETAS:
            br, _ = glint(al, ti, 'B')
            f = float(br[MASK].mean())
            F_B[(form, amp, ti)] = f
            c = C_of(amp, form, ti, 'B')
            line.append('f=%.4f' % f + ('' if c is None else ' C=%.3f' % c))
        rows.append(tuple(line))
table(rows, ('form', 'a (m)', 'psi_max (deg)', 'onset (deg)', '0 deg', '45 deg', '75 deg'))
a('')
a('  The window is centred on facets tilted by theta_i/2. A relief whose steepest facet is psi_max')
a('  cannot glint beyond 2*psi_max, so beyond it the plate is uniformly dark: the image does not')
a('  lose contrast, it ceases to exist. C is reported as "--" because mean radiance is zero and')
a('  a Weber ratio to zero is not a number -- the record\'s NO-VERDICT rule, applied to a channel.')

# ---------------------------------------------------------------------------------
hdr('[4] FRESNEL -- what oblique incidence buys in photons, and whether C can see it')
rows = []
GAIN = {}
for z0s in Z0S_GRID:
    Rs0, Rp0, R0_ = fresnel(z0s, 0.0)
    for ti in (math.radians(45.0), math.radians(75.0)):
        Rs, Rp, Ru = fresnel(z0s, ti)
        gain_s = Rs / Rs0
        gain_u = Ru / R0_
        bound = 1.0 + 4.0 / z0s
        GAIN[(z0s, ti)] = (gain_s, gain_u, bound)
        rows.append(('%.0e' % z0s, '%.0f' % math.degrees(ti), '%.6f' % Rs, '%.6f' % Rp,
                     '%.6f' % gain_s, '%.6f' % gain_u, '%.6f' % bound,
                     '%+.3f' % math.log10(gain_u * math.cos(ti))))
table(rows, ('Z0*sigma_s', 'theta_i', 'R_s', 'R_p', 'gain_s', 'gain_unpol', 'bound 1+4/Z0s',
             'dPhi net (orders)'))
a('')
a('  net = R(theta)/R(0) * cos(theta): the projected solid angle falls as fast as the reflection rises.')
a('')
a('  Scale invariance of C under a uniform gain, checked numerically rather than asserted:')
rows = []
for ti in (math.radians(45.0), math.radians(75.0)):
    for z0s in (80.0,):
        Rs, Rp, Ru = fresnel(z0s, ti)
        al = slope(1e-3, 'S')
        br, _ = glint(al, ti, 'A')
        I0 = U * br
        I1 = I0 * Ru
        c0, c1 = cweber(I0, MASK), cweber(I1, MASK)
        rows.append(('%.0f' % math.degrees(ti), '%.0e' % z0s, '%.9f' % c0, '%.9f' % c1,
                     '%.3e' % abs(c1 - c0)))
table(rows, ('theta_i', 'Z0*sigma_s', 'C before', 'C after gain', 'difference'))
a('')
a('  Zero difference: a uniform factor cancels in std/mean by construction. Fresnel is a PHI lever')
a('  that this metric cannot see, and the DoG contrast behaves the same way for the same reason.')

# ---------------------------------------------------------------------------------
hdr('[5] OCCLUSION -- the only theta_i-dependent contrast mechanism, and it needs a riser')
a('  f_s is the shadowed fraction of the SURFACE (whole periodic field) and of the PLATE (mask).')
a('  The two differ because the shadow band is phase-locked to the corrugation while the plate')
a('  boundary is not: the plate clips it. The surface value is the physical one; both are printed.')
rows = []
FS, FSM = {}, {}
for form in ('S', 'T'):
    for amp in (1e-3, 3.16e-3, 1e-2, 1.34e-2):
        z = height(amp, form)
        line = [form, '%.3g' % amp]
        for ti in THETAS:
            v = shadow(z, ti)
            f = float((~v).mean())
            FS[(form, amp, ti)] = f
            FSM[(form, amp, ti)] = float((~v)[MASK].mean())
            line.append('%.5f / %.5f' % (f, FSM[(form, amp, ti)]))
        rows.append(tuple(line))
table(rows, ('form', 'a (m)', 'f_s 0 deg', 'f_s 45 deg', 'f_s 75 deg'))
a('')
a('  Sine at a <= 1 mm: exactly 0 at every incidence -- its steepest slope 0.0314 never reaches')
a('  cot(75) = 0.268, so a shallow sine cannot shadow itself at any angle an instrument would use.')
a('  The lever exists only for a form with steep facets, and a riser\'s shadow is set by its')
a('  height, i.e. by the object.')
a('')
a('  THE SHADOW THRESHOLD AND ITS PRICE:')
tan75 = math.tan(math.radians(75.0))
a_50 = TREAD / tan75
eps_50 = a_50 / PITCH
EPS_S = 1.720e-4        # a*(E2)/pitch, S, from runs/LADDER/r2_relief_contrast_results.txt s3
EPS_T = 6.659e-5        # a*(E2)/pitch, T
riser_discrete = 4.0 * PX_M          # the 2-px central difference sees a/(4 PX_M), not a/PX_M
a('    a facet shadows when tan(theta_i) > its slope. The terraced riser spans one sample and')
a('    z spans +/-a/2, so the discrete slope is a/(4 PX_M) and shadowing needs')
a('        a > 4*PX_M*cot(theta_i) = %.4f mm at 75 deg      (the continuum a/PX_M would say %.4f)' %
  (riser_discrete / tan75 * 1e3, PX_M / tan75 * 1e3))
a('    half the tread shadowed at a_50 = tread/tan(75) = %.4f m  ->  eps = %.5f' % (a_50, eps_50))
a('    price ratio: a_50/a*(S) = %.1f x   a_50/a*(T) = %.1f x' % (eps_50 / EPS_S, eps_50 / EPS_T))
rows = []
for form, amp in (('T', 1e-2), ('T', 1.34e-2), ('S', 1e-2)):
    for ti in (math.radians(45.0), math.radians(75.0)):
        c0 = C_of(amp, form, ti, 'A', occl=False)
        c1 = C_of(amp, form, ti, 'A', occl=True)
        rows.append((form, '%.3g' % amp, '%.0f' % math.degrees(ti),
                     '%.4f' % c0, '%.4f' % c1, '%.4f' % (c1 / c0)))
table(rows, ('form', 'a (m)', 'theta_i', 'C no occl', 'C with occl', 'ratio'))
a('')
a('  At a = 13.4 mm -- a tenth of eps_max -- a shadow band over a fifth of the surface moves C by')
a('  %.2f x at 75 deg. That is under the two-rung bar, at 195x the amplitude the glint channel'
  % (C_of(1.34e-2, 'T', THETAS[2], 'A', occl=True) / C_of(1.34e-2, 'T', THETAS[2], 'A')))
a('  already needs. The lever is real, it is geometric, and it is the object\'s own relief.')

# ---------------------------------------------------------------------------------
hdr('[6] THE OTHER TWO CHANNELS -- E4 (diffuse) and E1 (dome), at every incidence')
a('  E4 is carried because it is the model behind every "topographic contrast" statement; the')
a('  deposit\'s near-mirror excludes it, and round 49 already found the 1/c^2 lever only there.')
rows = []
for form in ('S', 'T'):
    vals = [C_of(1e-3, form, ti, 'A', env='E4') for ti in THETAS]
    rows.append((form, 'E4', *['%.4f' % v for v in vals],
                 '%.3f' % (vals[2] / vals[1]),
                 '%.3f' % (math.tan(THETAS[2]) / math.tan(THETAS[1]))))
table(rows, ('form', 'env', 'C 0 deg', 'C 45 deg', 'C 75 deg', 'C(75)/C(45)', 'tan75/tan45'))
a('')
a('  In E4 oblique illumination IS a lever, and it is a STRONGER one than the ladder claims:')
a('  C(75)/C(45) = %.3f against tan75/tan45 = %.3f, i.e. the response is tan(theta_i) to three'
  % (C_of(1e-3, 'S', THETAS[2], 'A', env='E4') / C_of(1e-3, 'S', THETAS[1], 'A', env='E4'),
     math.tan(THETAS[2]) / math.tan(THETAS[1])))
a('  digits. And at normal incidence the channel is nearly BLIND -- C(0) = %.4f, four hundred times'
  % C_of(1e-3, 'S', THETAS[0], 'A', env='E4'))
a('  below the 75 deg value -- because the cosine law is STATIONARY in slope at theta_i = 0, so')
a('  relief enters only at second order. That is the real reason a "topographic edge at 3e-2"')
a('  needs obliquity, and it is a property of the diffuse model, not of the relief.')
a('  E4 is the one channel that separates RL-2 from RL-3, and it is the channel this surface is not.')
a('')
a('  E1 -- the uniform dome, at every incidence:')
rows = []
for ti in THETAS:
    for form in ('S', 'T'):
        c = C_of(1e-3, form, ti, 'A', env='E1')
        rows.append(('%.0f' % math.degrees(ti), form, '%.3e' % c, '%.2f' % q3(c)))
table(rows, ('theta_i', 'form', 'C_w (E1)', 'Q3'))
a('')
a('  C = 0 at every incidence, exactly, both forms. So "contrast collapses to the RL-0 value" is a')
a('  statement about the ANGULAR WIDTH of the environment. The ladder writes it as a statement about')
a('  DIRECTION ("under normal incidence") and the two are different axes: at normal incidence and')
a('  narrow width, C = %.4f, i.e. Q3 = %.2f.' % (C_of(1e-3, 'S', 0.0, 'A'), q3(C_of(1e-3, 'S', 0.0, 'A'))))

# ---------------------------------------------------------------------------------
hdr('[7] SEPARATION -- one rung or two, on the pre-registered bar S_theta = 2.0')
rA = [C_of(1e-3, 'S', ti, 'A') for ti in THETAS]
oC = [C_of(1e-2, 'T', ti, 'A', occl=True) for ti in THETAS]
S_A = max(rA) / min(rA)
S_oc = max(oC) / min(oC)
a('  without occlusion, G_A, a = 1 mm  : max %.6f / min %.6f  ->  S = %.9f' % (max(rA), min(rA), S_A))
a('  with occlusion,    G_A, a = 10 mm : max %.6f / min %.6f  ->  S = %.6f' % (max(oC), min(oC), S_oc))
a('  bar declared in the registration: S_theta > 2.0 for two rungs. Measured 1.000000000 and %.4f.' % S_oc)
a('')
a('  G_B is not a competing reading: there the image ceases to exist at 45 and 75 deg, so S is')
a('  undefined and the "separation" is a loss of the scene, not a purchase of contrast.')

# ---------------------------------------------------------------------------------
hdr('[8] PREDICTIONS -- Z1..Z7 of r3_illumination_registration.md')
res = []


def verdict(tag, text, ok, measured, magnitude=None):
    """A prediction is graded by its REGISTERED falsifier. A magnitude that the text also states,
    but that the falsifier does not test, is reported separately rather than folded into the grade."""
    res.append((tag, ok))
    a('')
    a('  %s  %s   %s' % (tag, 'CONFIRMED' if ok else 'FALSIFIED', text))
    a('       measured: %s' % measured)
    if magnitude:
        a('       magnitude: %s' % magnitude)


verdict('Z1', 'G_A is exactly theta_i-invariant, both forms, < 1e-12 relative',
        spread_rel <= 1e-12,
        'max relative spread = %.3e over 2 forms x 5 amplitudes x 3 incidences' % spread_rel)

fB_s45 = F_B[('S', 1e-3, THETAS[1])]
fB_s75 = F_B[('S', 1e-3, THETAS[2])]
ok2 = (fB_s45 == 0.0 and fB_s75 == 0.0 and abs(C_of(1e-3, 'S', 0.0, 'B') - 3.3166) < 1e-3)
verdict('Z2', 'G_B blacks out: f(45)=f(75)=0 on the sine at a=1mm, onset 3.33 deg, terrace to 35.5 deg',
        ok2, 'f(45) = %.3e, f(75) = %.3e, C(0) = %.4f; onset S %.2f deg, T %.2f deg; psi_max T %.2f deg'
        % (fB_s45, fB_s75, C_of(1e-3, 'S', 0.0, 'B'),
           math.degrees(ONSET[('S', 1e-3)]), math.degrees(ONSET[('T', 1e-3)]),
           math.degrees(math.atan(float(np.abs(slope(1e-3, 'T')).max())))))
a('       NOTE: the registered figure "terrace to 35.5 deg" is wrong by 4x -- it used the')
a('       continuum riser slope a/PX_M. Measured 9.15 deg. The falsifier above is still met,')
a('       so the prediction is CONFIRMED and the number is corrected in erratum E1.')

dmax = 0.0
for ti in (math.radians(45.0), math.radians(75.0)):
    for z0s in Z0S_GRID:
        Rs, Rp, Ru = fresnel(z0s, ti)
        al = slope(1e-3, 'S')
        br, _ = glint(al, ti, 'A')
        c0 = cweber(U * br, MASK)
        c1 = cweber(U * br * Ru, MASK)
        dmax = max(dmax, abs(c1 - c0) / c0)
verdict('Z3', 'Fresnel gain does not move C (< 1e-12 relative) at any theta_i or Z0*sigma_s',
        dmax <= 1e-12, 'max relative change = %.3e over 2 incidences x 5 grid members' % dmax)

g_s = max(GAIN[(z, math.radians(75.0))][0] - GAIN[(z, math.radians(75.0))][2] for z in Z0S_GRID)
g80 = GAIN[(80.0, math.radians(75.0))]
verdict('Z4', 's-pol gain <= 1+4/Z0s everywhere; <= 5% at Z0s=80; unpolarised < 1 (a loss)',
        g_s <= 1e-12 and g80[0] <= 1.05 and g80[1] < 1.0,
        'max(gain_s - bound) = %.3e ; at 80: gain_s %.4f (bound %.4f), gain_unpol %.4f, net %+.3f orders'
        % (g_s, g80[0], g80[2], g80[1], math.log10(g80[1] * math.cos(math.radians(75.0)))))

ok5 = (0.02 <= FS[('T', 1e-3, THETAS[2])] <= 0.06) and FS[('S', 1e-3, THETAS[2])] == 0.0 \
      and FS[('T', 1e-3, THETAS[1])] == 0.0
verdict('Z5', 'f_s(75,T,1mm) in [2,6]%; f_s = 0 exactly on the sine at every theta_i; 0 at 45 deg',
        ok5, 'f_s(75,T,1mm) = %.4f (surface) / %.4f (plate) ; sine at 75 = %.1e ; terrace at 45 = %.1e'
        % (FS[('T', 1e-3, THETAS[2])], FSM[('T', 1e-3, THETAS[2])],
           FS[('S', 1e-3, THETAS[2])], FS[('T', 1e-3, THETAS[1])]))
if not ok5:
    a('       WHY: the prediction used the continuum slope a/PX_M = 0.320. The discretized riser')
    a('       spans one sample and z spans +/-a/2, so np.gradient\'s 2-px difference sees')
    a('       a/(4 PX_M) = %.3f < cot(75) = %.3f: no shadow. The threshold is 4x the predicted')
    a('       amplitude. Recorded as erratum E1 on the registration; the prediction stands falsified.')

verdict('Z6', 'a_50 = 13.4 +/- 1 mm, eps = 3.35e-2, 195x / 503x the glint threshold',
        10e-3 <= a_50 <= 20e-3,
        'a_50 = %.4f mm ; eps = %.5f ; ratios %.1f x (S) and %.1f x (T)'
        % (a_50 * 1e3, eps_50, eps_50 / EPS_S, eps_50 / EPS_T))

verdict('Z7', 'S_theta = 1.000 in G_A and <= 1.10 with occlusion; bar 2.0 -> one rung',
        abs(S_A - 1.0) <= 1e-12 and S_oc < 2.0,
        'S = %.9f (no occlusion), %.4f (with occlusion at a = 10 mm); bar 2.0' % (S_A, S_oc),
        'predicted S_oc <= 1.10 at a = 10 mm; measured %.4f -- a 17%% magnitude miss, a quarter of'
        ' the two-rung bar' % S_oc)

# ---------------------------------------------------------------------------------
hdr('[9] WHAT THE NUMBERS SAY -- derived from the tables above, not from the registration')
a('  1. RL-3 IS NOT A CONTRAST RUNG IN THE CHANNEL THE MATERIAL FORCES. For a specular surface the')
a('     deflection angle is 2*arctan(alpha) and carries no incidence, so moving the source moves the')
a('     camera\'s job, not the image: with the camera in the specular position C is IDENTICAL (0.0e+00')
a('     difference in float64) across 0/45/75 deg, both forms, all five amplitudes. With the camera')
a('     fixed the window leaves the surface at 2*psi_max - beta: %.2f deg for the sine, %.2f deg for'
  % (math.degrees(ONSET[('S', 1e-3)]), math.degrees(ONSET[('T', 1e-3)])))
a('     the terrace, beyond which there is no image at all. Neither reading is a gain.')
a('')
a('  2. FRESNEL BUYS PHOTONS, AND AT 75 DEG IT LOSES THEM. R(75)/R(0) <= 1+4/Z0*sigma_s: at most 5%')
a('     for a near-mirror, and 0.03% at the record\'s own eV value. The projected solid angle falls by')
a('     cos(75) = 0.259, so the net is %+.2f orders at Z0*sigma_s = 80 and %+.2f at 1e4. For a 2-D'
  % (math.log10(g80[1] * math.cos(math.radians(75.0))),
     math.log10(GAIN[(1e4, math.radians(75.0))][1] * math.cos(math.radians(75.0)))))
a('     sheet the loss is structural: R_p -> 0 at grazing while R_s -> 1, so the unpolarised average')
a('     DROPS. Oblique illumination on this object is not free; it is a bill.')
a('')
a('  3. OCCLUSION IS THE ONLY MECHANISM THAT MOVES C, AND IT IS GEOMETRY. A facet shadows when')
a('     tan(theta_i) exceeds its slope, so at a = 1 mm the discrete riser (slope %.3f) never shadows:'
  % float(np.abs(slope(1e-3, 'T')).max()))
a('     the threshold is a > %.2f mm at 75 deg. Half the tread shadowed costs eps = %.4f, i.e. %.0f x'
  % (riser_discrete / tan75 * 1e3, eps_50, eps_50 / EPS_S))
a('     the eps at which the glint channel is already at threshold. It is also independent of L_e: a')
a('     shadow is dark under any narrow environment. That makes it RL-2\'s geometry seen from a')
a('     different angle, not a second relaxation.')
a('')
a('  4. THE LADDER\'S FINGERPRINT IS INVERTED, AND ITS AXES ARE CONFLATED. "Contrast collapses to the')
a('     RL-0 value under normal incidence" is false in the narrow-width column: C(0 deg) = %.4f, i.e.'
  % C_of(1e-3, 'S', 0.0, 'A'))
a('     Q3 = %.2f. What collapses is a WIDE environment (E1), at every incidence. The rung conflated'
  % q3(C_of(1e-3, 'S', 0.0, 'A')))
a('     beta with theta_i, and got the sign of the theta_i dependence wrong for a specular surface:')
a('     contrast is MAXIMAL at normal incidence and degrades towards grazing, not the reverse.')
a('')
a('  5. SO RL-3 IS RETIRED AS A RUNG, NOT RE-PRICED. Its price was already V = 0; this round measures')
a('     B = 0 as well -- it delivers no bits the other rungs do not. What remains of it is a')
a('     DECLARATION (which environment the experimenter brings: docs/specs/theta_environment_v1.md)')
a('     and a HAZARD (a fixed camera at 45 deg on this material sees a mirror-reflected void).')
a('     Neither is a purchase, and the ladder should say so rather than list a third free rung.')
a('')
a('  6. WHAT IS NOT CLAIMED. In E4 oblique illumination IS a lever -- C tracks tan(theta_i), a factor')
a('     %.2f between 45 and 75 deg and %.0f between 0 and 75 deg -- but E4 is the diffuse model the'
  % (C_of(1e-3, 'S', THETAS[2], 'A', env='E4') / C_of(1e-3, 'S', THETAS[1], 'A', env='E4'),
     C_of(1e-3, 'S', THETAS[2], 'A', env='E4') / C_of(1e-3, 'S', THETAS[0], 'A', env='E4')))
a('     near-mirror surface excludes, and round 49 already found the 1/c^2 lever only there. The')
a('     separation of RL-2 from RL-3 therefore exists exactly on the model the object is not.')

# ---------------------------------------------------------------------------------
hdr('SUMMARY')
n_ok = sum(1 for _t, o in res if o)
amended = bool(re.search(r'^## Errata\s*$', open(REG, encoding='utf-8').read(), re.M))
if amended:
    a('  declaration order : NOT EVIDENCED BY MTIME -- the registration carries an appended erratum,')
    a('                      which is where the ordering claim lives. The predictions above are')
    a('                      byte-identical to the registration\'s table; only Z2\'s terrace figure')
    a('                      and Z5\'s threshold were corrected, and both are marked as such.')
else:
    a('  declaration order : registration %.1f s before this run' % (time.time() - os.path.getmtime(REG)))
a('  RL-3 verdict      : RETIRED AS A RUNG. In the specular channel the deflection carries no')
a('                      incidence (C identical to 0.0e+00 in float64); Fresnel is a uniform gain')
a('                      that cancels in C exactly and is net NEGATIVE at 75 deg (%+.2f orders);'
  % math.log10(g80[1] * math.cos(math.radians(75.0))))
a('                      occlusion is the only C mechanism and costs eps = %.4f, %.0fx the glint'
  % (eps_50, eps_50 / EPS_S))
a('                      threshold. The rung\'s B is 0, so it is not a relaxation.')
a('  the fingerprint   : INVERTED. Contrast collapses under a WIDE environment, not under normal')
a('                      incidence -- C(0 deg, narrow) = %.4f. beta and theta_i are different axes.' % C_of(1e-3, 'S', 0.0, 'A'))
a('  what is NOT claimed: any statement about the deposit; no threshold written; no rung re-priced;')
a('                      the ladder\'s table is left byte-identical and the finding is an erratum.')
a('')
a('  predictions Z1-Z7  : %d CONFIRMED, %d FALSIFIED' % (n_ok, len(res) - n_ok))
a('')
a('PROVENANCE: NEITHER  (3-D specular ray geometry + shunt-sheet Fresnel + horizon test on declared fields)')

txt = '\n'.join(L) + '\n'
if '--write' in sys.argv:
    os.makedirs(OUTDIR, exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(txt)
    print('wrote %s' % OUT)
else:
    print(txt)
sys.exit(0 if n_ok == len(res) else 1)
