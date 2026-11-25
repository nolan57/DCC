#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ladder_r1 -- RL-1: Q3 at theta_fast on a scene carrying content.

Spec:      docs/specs/relaxation_ladder_v1.md  s2 (RL-1), s5 measurement 1
Tiers:     docs/specs/intrinsic_structure_tiers_v1.md  s5 (L3, q, C_eye)
Budget:    runs/ROUTE/p2_clock_results.txt  P2-3, P2-4, P2-5
Predicts:  runs/LADDER/r1_observer_registration.md  X1-X6 (written before this file ran)

Estimators are imported from src/route/structure_tiers.py, never re-implemented; the
identity check in section 0 is what licenses that. Nothing here is edited after the run.
"""
import contextlib
import importlib.util
import io
import math
import os
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTDIR = os.path.join(ROOT, 'runs', 'LADDER')
REG = os.path.join(OUTDIR, 'r1_observer_registration.md')
OUT = os.path.join(OUTDIR, 'r1_observer_results.txt')
ARCH = os.path.join(ROOT, 'runs', 'MATRIX', 'structure_tiers_results.txt')
BUDGET = os.path.join(ROOT, 'runs', 'ROUTE', 'p2_clock_results.txt')

_spec = importlib.util.spec_from_file_location(
    'structure_tiers', os.path.join(ROOT, 'src', 'route', 'structure_tiers.py'))
ST = importlib.util.module_from_spec(_spec)
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    _spec.loader.exec_module(ST)

GRID = ST.GRID
C_EYE = ST.C_EYE
Q_INSTR = ST.Q_INSTR
Q_REFL = ST.Q_REFL
THR = {k: float(ST.lock['tiers'][k]['threshold_c']) for k in ('L0', 'L1', 'L2', 'L3')}

# ---- registered budget constants, read from the products, not chosen here -------------------
T_RIP = 8.255290e-9          # M-5 / P2-1: sqrt(2)*H/c at H = 1.75 m
TWO_H_C = 1.167474e-8        # M-5 / P2-1: the reflected round trip
DELTA_SHEET = 1.75e-15       # m, the 1.7-2.0 fm sheet (relaxation_ladder s2, RL-4)
N_REQ_1E7 = 9.000e14         # P2-3 visible row, dtau = 1e-7, SNR 3
FLUX_REQ = 9.539e31          # P2-3
SUN_225 = 2.7740e21          # P2-3
N_FRAME_REQ = 7.8747e23      # M-5: FLUX_REQ * t_rip
N_FRAME_SUN = 2.2900e13      # M-5: SUN_225 * t_rip
SHORTFALL = 3.4387e10        # M-5
C_DEPOSIT = 1.0e-3           # visualization_null_result_v1 s2: the near-mirror contrast
C_EDGE = 3.0e-2              # relaxation_ladder s3: topographic edge, oblique
C_GRAZE = 0.3                # relaxation_ladder s3: grazing incidence on relief
C_BASE = 1.0e-7              # the contrast the registered requirement was computed at (P2-3)

L = []


def a(s=''):
    L.append(s)


def hdr(t):
    a('')
    a('=' * 98)
    a(t)
    a('=' * 98)


def row(cells, w):
    a('  ' + '  '.join(str(c).ljust(w[i]) for i, c in enumerate(cells)))


def table(body, head):
    w = [max(len(str(head[i])), max((len(str(r[i])) for r in body), default=0)) for i in range(len(head))]
    row(head, w)
    a('  ' + '  '.join('-' * w[i] for i in range(len(head))))
    for r in body:
        row(r, w)


FLAGS = {}


def verdict(pid, claim, ok, detail):
    FLAGS[pid] = bool(ok)
    a('')
    a('  %s  %-11s %s' % (pid, 'CONFIRMED' if ok else 'FALSIFIED  ', claim))
    a('       measured: %s' % detail)


def archived(key):
    for line in open(ARCH, 'r', encoding='utf-8', errors='replace').read().splitlines():
        if key in line and '=' in line:
            return float(line.split('=')[1].split()[0])
    return None


# ============================================================================================
hdr('RL-1 -- Q3 AT theta_fast ON A SCENE THAT CARRIES CONTENT   (round 48, RQ-12)')
a('  theta_eye   q = 0        the naked-eye reflected channel (frozen corollary)')
a('  theta_ideal q = 1        the spec normalisation: instrumented channel, adequate budget')
a('  theta_fast  q = q(C_xi)  the 284 eV transmission channel, limited by the registered chain')

# ============================================================================================
hdr('[0] ESTIMATOR IDENTITY -- the imported module must reproduce the archived table')

p0_arch = archived('P0(null)')
q2_arch = archived('q2(null)')
TOL_P0, TOL_Q2 = 5e-9, 5e-7
id_p0 = abs(ST.P0_NULL - p0_arch) <= TOL_P0
id_q2 = abs(ST.Q2_NULL - q2_arch) <= TOL_Q2

scenes = ST.make_scenes()
u_tiled = scenes['TILED']
xi_tiled, _ = ST.char_scale(u_tiled)
q3_tiled, c_tiled = ST.q3(u_tiled, xi_tiled, Q_INSTR)
TOL_XI, TOL_C = 5e-3, 5e-5    # the archive prints xi to 2 dp and C_xi to 4 dp;
                             # equal within half a unit of the last printed place IS equality
id_xi = abs(xi_tiled - 27.55) <= TOL_XI
id_c = abs(c_tiled - 0.7867) <= TOL_C

a('  P0(null)  imported %.9e   archived %.9e   %s' % (ST.P0_NULL, p0_arch, 'MATCH' if id_p0 else 'MISMATCH'))
a('  q2(null)  imported %.7f      archived %.6f       %s' % (ST.Q2_NULL, q2_arch, 'MATCH' if id_q2 else 'MISMATCH'))
a('  TILED xi  recomputed %.4f        archived %.2f          %s' % (xi_tiled, 27.55, 'MATCH' if id_xi else 'MISMATCH'))
a('  TILED Cxi recomputed %.4f        archived %.4f        %s' % (c_tiled, 0.7867, 'MATCH' if id_c else 'MISMATCH'))
ident = id_p0 and id_q2 and id_xi and id_c
a('  => same estimator that produced runs/MATRIX/: %s' % ('YES' if ident else 'NO -- every number below is void'))
if not ident:
    print('\n'.join(L))
    sys.exit(2)

a('')
a('  locked values used, read from runs/MATRIX/threshold_lock.json:')
a('    C_eye (Weber)  %.4f      Q3 threshold  %.2f      q instrumented  %.1f      q reflected  %.1f'
  % (C_EYE, THR['L3'], Q_INSTR, Q_REFL))

# ============================================================================================
hdr('[1] WHAT MAKES theta_fast ADMISSIBLE -- the three channels, priced in time and flux')

path_refl = TWO_H_C
path_trans = 2.0 * DELTA_SHEET / 2.99792458e8
a('  t_rip = sqrt(2)*H/c = %.6e s   (H = 1.75 m, the deposit\'s own height)' % T_RIP)
a('')
table([
    ('reflection 2.25 eV', '%.4e' % path_refl, '%.4f' % (path_refl / T_RIP), 'q = 0 EXACT',
     'frozen corollary: ratio is sqrt(2) for every H and every size'),
    ('transmission 284 eV', '%.4e' % path_trans, '%.3e' % (path_trans / T_RIP), 'q = 1',
     'admissible: P2-5, sub-field frames only'),
    ('transmission 2.25 eV', '%.4e' % path_trans, '%.3e' % (path_trans / T_RIP), 'CLOSED',
     'RL-4: |Z0 sigma_s| ~ 1e4 at 2.25 eV -- a Drude mirror, no colour'),
], ('channel', 'path / c (s)', 'path / t_rip', 'channel factor', 'why'))

a('')
a('  The timing ground is scale-free: (2H/c)/t_rip = %.6f = sqrt(2), independent of H.' % (TWO_H_C / T_RIP))
a('  No choice of distance or of object size opens the reflected channel. RL-1 therefore does not')
a('  buy "an observer"; it buys ONE channel: 284 eV transmission, which the extrinsic L3 excluded')
a('  as band migration and the intrinsic L3 admits, because the intrinsic L3 asks only for a')
a('  declared theta (intrinsic_structure_tiers_v1 s5).')

# ============================================================================================
hdr('[2] SCENES -- the deposit-like class (isolated plates), pitch p, side 0.75p')


def plates(p, s):
    """Square plates of side s on a lattice of pitch p, exactly periodic on the 128 grid."""
    assert GRID % p == 0
    return ((np.arange(GRID) % p)[:, None] < s).astype(np.float64) * \
           ((np.arange(GRID) % p)[None, :] < s).astype(np.float64)


INSTANCES = (('PA-8', 8, 6), ('PA-16', 16, 12), ('PA-32', 32, 24))
SC = {n: plates(p, s) for n, p, s in INSTANCES}
table([(n, p, s, '%.4f' % ((s / p) ** 2)) for n, p, s in INSTANCES], ('id', 'p', 's', 'fill'))
a('')
a('  These are SEVERED objects (isolated plates, no bond). The bonded scene V4 needs does not exist,')
a('  because KIN-DYN supplies no constitutive law -- unchanged by this round.')

# ============================================================================================
hdr('[3] Q3 AT THREE DECLARATIONS OF q')

A_PIX = N_REQ_1E7 / N_FRAME_REQ          # implied by the registered pair, not assumed
N_AVAIL = N_FRAME_SUN * A_PIX
A_SIDE = math.sqrt(A_PIX)

rows = []
Q = {}
for n, p, s in INSTANCES:
    u = SC[n]
    xi, _ = ST.char_scale(u)
    q3i, cxi = ST.q3(u, xi, Q_INSTR) if xi >= 2.0 else (None, None)
    q3r = ST.q3(u, xi, Q_REFL)[0] if xi >= 2.0 else None
    short = SHORTFALL * (C_BASE / cxi) ** 2 if cxi else None
    qf = min(1.0, 1.0 / short) if short else None
    q3f = ST.q3(u, xi, qf)[0] if xi >= 2.0 else None
    Q[n] = dict(xi=xi, cxi=cxi, q3i=q3i, q3r=q3r, short=short, qf=qf, q3f=q3f)
    rows.append((n,
                 '%.2f' % xi,
                 '%.4f' % cxi if cxi else 'n/v',
                 '%.3f %s' % (q3i, 'PASS' if q3i >= THR['L3'] else 'FAIL') if q3i is not None else 'NO-VERDICT',
                 '%.3f' % q3r if q3r is not None else 'n/v',
                 '%.3e' % short if short else 'n/v',
                 '%.4f' % qf if qf is not None else 'n/v',
                 '%.3f' % q3f if q3f is not None else 'n/v'))

table(rows, ('scene', 'xi/h', 'C_xi', 'Q3 (q=1)', 'Q3 (q=0)', 'flux shortfall', 'q(theta_fast)', 'Q3 (theta_fast)'))
a('')
a('  L3 precondition: xi/h >= 2. Below it the tier returns NO VERDICT -- not a failure, an')
a('  inapplicable question (a scene with no scale cannot be certified legible for its structure).')
a('')
a('  READ THIS BEFORE THE 5.7: C_xi = 0.52 is the contrast of a DECLARED BINARY FIELD (u in {0,1},')
a('  mean|u| = 0.5625), not of the deposit. The deposit is a near-mirror and its own contrast is')
a('  1e-3 (visualization_null_result_v1 s2); relief is what would lift it to 3e-2. So the table')
a('  above establishes that L3 is EVALUABLE and NON-EMPTY once q > 0 -- the q = 0 emptiness was')
a('  the channel, not the content -- and it does not establish that the deposit is legible.')

# ---- the same formula on the ladder's declared contrasts ------------------------------------
hdr('[3b] THE SAME FORMULA ON THE LADDER\'S DECLARED CONTRASTS -- Q3(C) at q = 1')

a('  Q3(C) = log2(1 + C/C_eye) with C_eye = %.2f, threshold Q3 >= %.1f  <=>  C >= %.3f'
  % (C_EYE, THR['L3'], C_EYE * (2.0 ** THR['L3'] - 1.0)))
a('')
rows = []
for c, why in ((C_DEPOSIT, 'the deposit as it is (near-mirror)'),
               (C_EDGE, 'RL-2: topographic edge / oblique'),
               (C_GRAZE, 'RL-2 + RL-3: grazing on relief'),
               (0.5232, 'the plate class as declared (binary field)')):
    q3v = math.log2(1.0 + c / C_EYE)
    rows.append(('%.4f' % c, '%.4f' % q3v, 'PASS' if q3v >= THR['L3'] else 'FAIL',
                 '%+.3f' % (q3v - THR['L3']), why))
table(rows, ('C', 'Q3 (q=1)', 'L3', 'margin', 'declared as'))
a('')
a('  The third row is the finding: C = %.2f gives Q3 = %.6f EXACTLY, because Q3 = 2 needs'
  % (C_EDGE, math.log2(1.0 + C_EDGE / C_EYE)))
a('  C_eye*(2^2 - 1) = 3*C_eye = %.2f. The ladder declared RL-2\'s topographic contrast as 3e-2'
  % (3 * C_EYE))
a('  by independent reasoning, and the locked threshold was declared on 2026-11-22 -- so the')
a('  coincidence is real but its margin is ZERO: any contrast loss at all puts RL-2 under L3.')
a('  RL-2 alone reaches legibility at exactly threshold and the flux gate with 0.42 orders of')
a('  margin. That is the tightest a rung can be and still be a rung; it is not a comfortable one.')

# ============================================================================================
hdr('[4] THE DETECTION GATE -- where 3.4387e10 comes from, and what it is a function of')

a('  The registered chain, rebuilt from its own numbers so the arithmetic is checkable:')
a('    N_required(1e-7)      = (3 / 1e-7)^2          = %.4e  photons per element' % N_REQ_1E7)
a('    flux_required         = %.4e m^-2 s^-1        (P2-3, visible row)' % FLUX_REQ)
a('    x t_rip               = %.4e m^-2 per frame   (M-5)' % N_FRAME_REQ)
a('    full sun x t_rip      = %.4e m^-2 per frame   (M-5)' % N_FRAME_SUN)
a('    regression check      = %.4e  vs registered %.4e  %s'
  % (N_REQ_1E7 / N_AVAIL, SHORTFALL,
     'reproduced to %.1e relative' % (abs(N_REQ_1E7 / N_AVAIL - SHORTFALL) / SHORTFALL)))
a('    implied element area  = N_required / (flux_required * t_rip) = %.4e m^2  (side %.1f um)'
  % (A_PIX, A_SIDE * 1e6))
a('    available per element = %.4e * %.4e = %.4e photons'
  % (N_FRAME_SUN, A_PIX, N_AVAIL))
a('    shortfall at 1e-7     = %.4e / %.4e = %.4e      <- the registered 3.4387e10'
  % (N_REQ_1E7, N_AVAIL, N_REQ_1E7 / N_AVAIL))
a('')
a('  So the shortfall is a FUNCTION OF THE SCENE CONTRAST, and the registered value is its')
a('  evaluation at C = 1e-7 -- the SNR-3 detector floor, not the scene:')
a('')
a('      shortfall(C) = %.4e * (1e-7 / C)^2' % SHORTFALL)
a('      C*  = 1e-7 * sqrt(%.4e) = %.6e   (the contrast at which the gate is exactly met)' % (SHORTFALL, C_BASE * math.sqrt(SHORTFALL)))
C_STAR = C_BASE * math.sqrt(SHORTFALL)

cs = [(1e-7, 'P2-3 detector floor'), (1e-6, '--'), (1e-4, '--'),
      (C_DEPOSIT, 'the record\'s near-mirror contrast'),
      (C_EDGE, 'RL-2: topographic edge'),
      (C_GRAZE, 'RL-2+RL-3: grazing')]
rows = []
for c, why in cs:
    s_ = SHORTFALL * (C_BASE / c) ** 2
    rows.append(('%.0e' % c, '%.4e' % s_, '%+.2f' % math.log10(s_), 'OPEN' if s_ <= 1 else 'short', why))
table(rows, ('C', 'shortfall', 'orders', 'gate', 'declared as'))
a('')
a('  C* = %.5f sits BELOW the contrast L3 needs for Q3 = 2 at q = 1:' % C_STAR)
c_need = C_EYE * (2.0 ** THR['L3'] - 1.0)
a('    Q3 >= %.1f  <=>  C >= C_eye*(2^Q3 - 1) = %.4f, which is %.3f x C*  (%.3f x in photons)'
  % (THR['L3'], c_need, c_need / C_STAR, (c_need / C_STAR) ** 2))
a('  => the flux gate is NOT an independent ground. It is the L3 threshold expressed in photons.')

# ============================================================================================
hdr('[5] WHAT THIS DOES TO THE LADDER\'S PRICE LIST (s3 and s4 of relaxation_ladder_v1)')

a('  The ladder says: "that requirement was computed on a compositional contrast |dR| = 0.001"')
a('  and then applies a 1e-3 -> 3e-2 lever worth +2.9 orders, leaving 5.5-7.6 orders residual.')
a('  Measured here: the requirement is at 1e-7. At 1e-3 the same chain gives %.1f, i.e. %.2f orders.'
  % (SHORTFALL * (C_BASE / C_DEPOSIT) ** 2, math.log10(SHORTFALL * (C_BASE / C_DEPOSIT) ** 2)))
a('')
rows = []
for c, why in ((C_DEPOSIT, 'the deposit as it is'), (C_EDGE, '+ RL-2 (relief)'), (C_GRAZE, '+ RL-2 + RL-3')):
    s_ = SHORTFALL * (C_BASE / c) ** 2
    rows.append(('%.0e' % c, '%.4e' % s_, '%+.2f' % math.log10(s_),
                 '%.1f m^2 (%.1f m aperture)' % (s_, math.sqrt(s_)) if s_ > 1 else 'none needed',
                 '%.3g x t_rip' % s_ if s_ > 1 else '< 1'))
table(rows, ('contrast', 'shortfall', 'orders', 'collector to close it', 'integration instead'))
a('')
a('  theta_fast made explicit, as RQ-12\'s DoD asks:')
a('    q(A) = min(1, A / shortfall(C))   -- aperture enters q LINEARLY, so the "collector" column')
a('                                        above is exactly the A at which q = 1.')
a('    distance does not enter at all   -- (2H/c)/t_rip = sqrt(2) for every H (section 1).')
a('    band enters only through q = 0 vs q > 0: reflection is excluded outright, and the')
a('                                        surviving channel is 284 eV transmission.')
a('')
a('  The corrected price of RL-1+RL-2+RL-3 is therefore:')
a('    - RL-2 ALONE closes the flux gap: %.2f orders of margin -- and reaches L3 at EXACTLY its'
  % -math.log10(SHORTFALL * (C_BASE / C_EDGE) ** 2))
a('      threshold (section 3b). One rung, zero margin on legibility, 0.42 orders on flux.')
ladder_res = SHORTFALL * (C_DEPOSIT / C_GRAZE) ** 2      # the ladder's own arithmetic: base 1e-3
mine_res = SHORTFALL * (C_BASE / C_GRAZE) ** 2          # the same chain at its real base 1e-7
a('    - the ladder\'s "5.5-7.6 orders" is %.3e; the same chain at 1e-7 gives %.3e -- a factor %.0e,'
  % (ladder_res, mine_res, ladder_res / mine_res))
a('      i.e. 8.0 orders in photons, because the prose moved a 1e-7 requirement onto a 1e-3 baseline')
a('      without recomputing it. The rungs are unchanged; only their price label was wrong.')
a('    - and the whole Phi column is not independent of Q3 at all (section 4), so a ladder that')
a('      prices flux and legibility separately double-counts one wall and misses the other.')

# ============================================================================================
hdr('[6] PREDICTIONS -- X1..X6 of r1_observer_registration.md')

Q8, Q16, Q32 = Q['PA-8'], Q['PA-16'], Q['PA-32']

verdict('X1', 'L3 NO VERDICT at p=8 (xi/h < 2) while L0 and L2 PASS there',
        (Q8['xi'] < 2.0 and Q8['q3i'] is None),
        'xi/h = %.4f, Q3 = %s ; archived L0 = 0.7230 PASS, L2 = 0.5155 PASS'
        % (Q8['xi'], 'NO-VERDICT' if Q8['q3i'] is None else '%.3f' % Q8['q3i']))

ok2 = (Q16['q3i'] is not None and Q16['q3i'] >= THR['L3'] and Q32['q3i'] is not None and Q32['q3i'] >= THR['L3'])
verdict('X2', 'at q=1, Q3 >= 2.0 at both p=16 and p=32',
        ok2,
        'Q3 = %.3f (p=16, C_xi %.4f) and %.3f (p=32, C_xi %.4f); threshold needs C_xi >= %.3f'
        % (Q16['q3i'] or float('nan'), Q16['cxi'] or 0, Q32['q3i'] or float('nan'), Q32['cxi'] or 0, c_need))

vals = [q['q3r'] for q in (Q8, Q16, Q32) if q['q3r'] is not None]
verdict('X3', 'at q=0, Q3 = 0.000 exactly wherever a verdict exists',
        all(abs(v) < 1e-12 for v in vals),
        'values %s' % ', '.join('%.3e' % v for v in vals))

s_dep = SHORTFALL * (C_BASE / C_DEPOSIT) ** 2
verdict('X4', '3.4387e10 belongs to C=1e-7; at the record\'s own 1e-3 the chain gives 343.9',
        abs(s_dep - 343.87) < 0.05 and abs(N_REQ_1E7 / N_AVAIL - SHORTFALL) / SHORTFALL < 0.001,
        'shortfall(1e-7) = %.4e (regression error %.2e); shortfall(1e-3) = %.2f'
        % (N_REQ_1E7 / N_AVAIL, abs(N_REQ_1E7 / N_AVAIL - SHORTFALL) / SHORTFALL, s_dep))

verdict('X5', 'C* = 1.854e-2 < 0.03, ratio 1.618 in contrast / 2.618 in photons',
        abs(C_STAR - 1.854e-2) < 5e-5 and abs(c_need / C_STAR - 1.618) < 1e-3,
        'C* = %.5f, C(Q3=2) = %.4f, ratio %.4f / %.4f' % (C_STAR, c_need, c_need / C_STAR, (c_need / C_STAR) ** 2))

qf_all = [q['qf'] for q in (Q8, Q16, Q32) if q['qf'] is not None]
verdict('X6', 'at the measured C_xi, q(theta_fast) saturates at 1, so Q3(theta_fast) = Q3(q=1)',
        all(abs(v - 1.0) < 1e-12 for v in qf_all),
        'q values %s ; C_xi range %.4f .. %.4f vs C* %.5f'
        % (', '.join('%.6f' % v for v in qf_all), min(q['cxi'] for q in (Q16, Q32)),
           max(q['cxi'] for q in (Q16, Q32)), C_STAR))

# ============================================================================================
hdr('SUMMARY')
dt = time.time() - os.path.getmtime(REG) if os.path.exists(REG) else None
amended = '## Errata' in open(REG, encoding='utf-8').read() if os.path.exists(REG) else False
if amended:
    a('  declaration order : registration carries an appended erratum; mtime is the append time')
else:
    a('  declaration order : registration written %.1f s before this run %s'
      % (dt or 0, '(earlier -> declared BEFORE evaluation)' if (dt or 0) > 0 else 'NOT EARLIER'))

a('  RL-1 verdict      : ADMISSIBLE, and it is NOT free in the way s4 of the ladder states:')
a('                      it buys ONE channel (284 eV transmission); the flux wall it was said to')
a('                      leave standing is 8 orders smaller than stated, and is not independent')
a('                      of Q3 at all. What survives of the old verdict is the timing ground,')
a('                      which is exact, scale-free, and excludes reflection forever.')
a('  V4 (bonded Q3)    : still unanswered. No constitutive law, no scene. Unchanged.')
a('  what is NOT claimed: any statement about the deposit. The plate class is a declared stand-in;')
a('                      DEPOSIT-BLIND and MR1.6 are untouched. Every number is a locked estimator')
a('                      on a declared field, or arithmetic on p2_clock_results.')
a('')
a('  predictions X1-X6 : %d CONFIRMED, %d FALSIFIED'
  % (sum(FLAGS.values()), len(FLAGS) - sum(FLAGS.values())))
a('')
a('PROVENANCE: NEITHER  (locked estimators on declared fields + budget arithmetic; no new physics)')

txt = '\n'.join(L) + '\n'
if '--write' in sys.argv:
    os.makedirs(OUTDIR, exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(txt)
    print(txt)
    print('  wrote %s' % OUT)
else:
    print(txt)
sys.exit(0 if ident else 1)
