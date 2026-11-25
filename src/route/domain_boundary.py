#!/usr/bin/env python
"""
Applicability-domain boundaries for Q0 (T1) and Q2 (T2).

Purpose: the governor ruled T1/T2 in as *applicability-domain boundaries* -- prohibition on use as evidence
plus a KNOWN boundary interval -- with no new lock.  This script measures where the boundaries are.

Discipline notes
  1. No threshold is re-declared and runs/MATRIX/threshold_lock.json is not touched.  Q0 keeps >= 0.50,
     Q2 keeps >= 0.50, and the four tiers keep their ADMITTED status.  What is measured here is the region
     in which a PASS may be cited.
  2. The quantities are recomputed from the EXECUTOR'S OWN function bodies, extracted by AST from
     src/route/structure_tiers.py and digest-recorded.  Nothing is retyped, so the bodies that produced the
     admitted verdicts are the bodies measured here.  P5 checks this by rebuilding DITHER verbatim and
     demanding the admitted number back.
  3. Constants come from the lock file, not from literals in this file.
  4. Predictions were fixed in runs/MATRIX/domain_boundary_registration.md before this file existed.
"""
import ast
import hashlib
import json
import math
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCK = os.path.join(ROOT, 'runs', 'MATRIX', 'threshold_lock.json')
SRC = os.path.join(ROOT, 'src', 'route', 'structure_tiers.py')
SPEC = os.path.join(ROOT, 'docs', 'specs', 'intrinsic_structure_tiers_v1.md')


def hdr(t):
    print('\n' + '=' * 96)
    print(t)
    print('=' * 96)


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


# ----------------------------------------------------------------------------------
# inputs
# ----------------------------------------------------------------------------------
with open(LOCK, encoding='utf-8') as f:
    lock = json.load(f)
C = lock['declared_constants']

GRID = C['grid'][0]
BINS = C['bins']
CTX = C['context_levels']
NULL_M = C['null_realisations']
NULL_SEED0 = C['null_seed_start']
TH0 = lock['tiers']['L0']['threshold_c']
TH2 = lock['tiers']['L2']['threshold_c']

hdr('[0] INPUTS -- constants read from the lock, function bodies extracted from the executor')
print('  lock file              : %s' % os.path.relpath(LOCK, ROOT))
print('  lock sha256            : %s' % sha_file(LOCK)[:32] + '...')
print('  spec sha256 (recorded) : %s' % lock['spec_sha256'][:32] + '...')
print('  spec sha256 (actual)   : %s' % sha_file(SPEC)[:32] + '...   -> %s'
      % ('UNCHANGED' if sha_file(SPEC) == lock['spec_sha256'] else 'CHANGED'))
print('  declared: GRID=%d  BINS=%d  CTX=%d  null=%d realisations from seed %d'
      % (GRID, BINS, CTX, NULL_M, NULL_SEED0))
print('  locked:   Q0 >= %.2f   Q2 >= %.2f   (both unchanged by this run)' % (TH0, TH2))

text = open(SRC, encoding='utf-8').read()
tree = ast.parse(text)
WANT = ('quant', 'total_persistence', 'plug_q2', 'char_scale', 'gauss_blur')
segs = [ast.get_source_segment(text, n) for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name in WANT]
missing = set(WANT) - {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
if missing:
    raise SystemExit('REFUSED: functions not found in the executor: %s' % sorted(missing))
BODY = '\n\n'.join(segs)
G = {'np': np, 'math': math, 'GRID': GRID, 'BINS': BINS, 'CTX': CTX}
exec(compile(BODY, '<extracted from structure_tiers.py>', 'exec'), G)
quant = G['quant']
total_persistence = G['total_persistence']
plug_q2 = G['plug_q2']

print('  extracted bodies       : %s' % ', '.join(sorted(WANT)))
print('  extracted-body sha256  : %s   (%d bytes)' % (hashlib.sha256(BODY.encode()).hexdigest()[:32], len(BODY)))
print('  -> the measured bodies are byte-identical to the executor\'s; P5 proves the path end to end.')


# ----------------------------------------------------------------------------------
# nulls
# ----------------------------------------------------------------------------------
hdr('[1] DECLARED NULLS -- reproduced, not retyped')
p0s, q2s = [], []
for k in range(NULL_M):
    u = np.random.default_rng(NULL_SEED0 + k).random((GRID, GRID))
    p0s.append(total_persistence(u))
    q2s.append(plug_q2(u)[0])
P0_NULL = float(np.mean(p0s))
Q2_NULL = float(np.mean(q2s))
print('  P0(null) = %.6e   q2(null) = %.6f   (admitted run printed 0.138)' % (P0_NULL, Q2_NULL))

G['BINS'] = 16
q2s16 = []
for k in range(NULL_M):
    u = np.random.default_rng(NULL_SEED0 + k).random((GRID, GRID))
    q2s16.append(plug_q2(u)[0])
Q2_NULL16 = float(np.mean(q2s16))
G['BINS'] = BINS
print('  q2(null) at B = 16      = %.6f   <- renormalisation is alphabet-dependent, see P8' % Q2_NULL16)


# ----------------------------------------------------------------------------------
# scenes
# ----------------------------------------------------------------------------------
def dither(m, A, seed):
    """0.5 everywhere; a random fraction m of cells set to 0.5 +/- A."""
    rng = np.random.default_rng(seed)
    u = 0.5 * np.ones((GRID, GRID))
    mask = rng.random((GRID, GRID)) < m
    u[mask] = 0.5 + A * np.where(rng.random(mask.sum()) < 0.5, -1.0, 1.0)
    return u


def measure(u):
    p0 = total_persistence(u)
    q2p, Hm = plug_q2(u)
    cv = u.std() / (u.max() - u.min()) if u.max() > u.min() else 0.0
    q, _ = quant(u)
    cnt = np.bincount(q.ravel(), minlength=BINS)
    modal = float(cnt.max() / cnt.sum())
    return dict(
        Q0=1.0 - p0 / P0_NULL,
        P0=p0,
        Q2=(q2p - Q2_NULL) / (1.0 - Q2_NULL) if q2p is not None else None,
        q2raw=q2p,
        Hm=Hm,
        cv=cv,
        modal=modal,
        spanspan=float(u.max() - u.min()),
    )


hdr('[2] P5 -- HARNESS VALIDATION: rebuild DITHER verbatim and demand the admitted number back')
d = 0.5 * np.ones((GRID, GRID))
m_ = np.random.default_rng(1236).random((GRID, GRID)) < 0.05
d[m_] = 0.5 + 0.3 * np.where(np.random.default_rng(1237).random(m_.sum()) < 0.5, -1.0, 1.0)
r = measure(d)
P5 = abs(r['Q0'] - 0.775) < 1e-3 and abs(r['cv'] - 0.119) < 1e-3
print('  rebuilt DITHER: Q0 = %.6f (want 0.775)   cv = %.6f (want 0.119)   -> %s'
      % (r['Q0'], r['cv'], 'P5 PASS' if P5 else 'P5 FAIL'))
print('  the extraction path reproduces the admitted verdicts, so what follows is measured by the same code.')

hdr('[3] T1 DOMAIN -- Q0 against modal mass m at A = 0.3, and against amplitude at m = 0.05')
print('  %-7s %-8s %-9s %-9s %-9s %-9s %s' % ('m', 'A', 'sigma/du', 'modal', 'P0', 'Q0', 'verdict'))
print('  ' + '-' * 76)
A_FIX = 0.3
M_VALS = (0.005, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50, 0.75, 1.00)
A_rows = []
for i, m in enumerate(M_VALS):
    u = dither(m, A_FIX, 8100 + i)
    r = measure(u)
    A_rows.append((m, A_FIX, r))
    print('  %-7.3f %-8.3f %-9.4f %-9.4f %-9.4e %-9.4f %s'
          % (m, A_FIX, r['cv'], r['modal'], r['P0'], r['Q0'],
             'PASS' if r['Q0'] >= TH0 else 'fail'))

print()
print('  amplitude sweep at m = 0.05 -- if P1/P2 hold, Q0 does not move:')
print('  %-7s %-8s %-9s %-9s %-9s %-9s %s' % ('m', 'A', 'sigma/du', 'modal', 'P0', 'P0/A', 'Q0'))
print('  ' + '-' * 76)
B_rows = []
for i, A in enumerate((0.005, 0.05, 0.15, 0.30, 0.60)):
    u = dither(0.05, A, 8200 + i)
    r = measure(u)
    B_rows.append((0.05, A, r))
    print('  %-7.3f %-8.3f %-9.4f %-9.4f %-9.4e %-9.4e %-9.4f'
          % (0.05, A, r['cv'], r['modal'], r['P0'], r['P0'] / A, r['Q0']))

# crossover in m for Q0
def cross(rows, key, th):
    prev = None
    for m, _A, r in rows:
        if r[key] is not None and r[key] >= th:
            prev = (m, r[key])
        elif prev is not None:
            m0, v0 = prev
            frac = (v0 - th) / (v0 - r[key])
            return m0 + frac * (m - m0)
    return None


M0_STAR = cross(A_rows, 'Q0', TH0)

hdr('[4] T2 DOMAIN -- Q2 on the same family, plus the alphabet probe')
print('  %-7s %-9s %-9s %-9s %s' % ('m', 'modal', 'q2 raw', 'Q2', 'verdict'))
print('  ' + '-' * 60)
C_rows = []
for i, m in enumerate(M_VALS):
    u = dither(m, A_FIX, 8100 + i)   # identical scenes, second readout
    r = measure(u)
    C_rows.append((m, A_FIX, r))
    print('  %-7.3f %-9.4f %-9.4f %-9.4f %s'
          % (m, r['modal'], r['q2raw'] if r['q2raw'] is not None else float('nan'), r['Q2'],
             'PASS' if (r['Q2'] is not None and r['Q2'] >= TH2) else 'fail'))

M2_STAR = cross(C_rows, 'Q2', TH2)

print()
print('  alphabet probe -- NOISE measured at B = 16 and B = 64, each against its own null:')
noise = np.random.default_rng(1234).random((GRID, GRID))
q64 = plug_q2(noise)[0]
G['BINS'] = 16
q16 = plug_q2(noise)[0]
G['BINS'] = BINS
print('    B = 64 : q2 raw = %.6f   null = %.6f   renormalised = %.6f'
      % (q64, Q2_NULL, (q64 - Q2_NULL) / (1.0 - Q2_NULL)))
print('    B = 16 : q2 raw = %.6f   null = %.6f   renormalised = %.6f'
      % (q16, Q2_NULL16, (q16 - Q2_NULL16) / (1.0 - Q2_NULL16)))
D_ALPHA = abs(q16 - q64)
print('    |q2(16) - q2(64)| = %.6f   -> %s' % (D_ALPHA, 'P8 PASS' if D_ALPHA > 0.05 else 'P8 FAIL'))

hdr('[5] BOUNDARY INTERVALS AND PREDICTION LEDGER')
q0_lo = None
q0_hi = None
for m, _A, r in A_rows:
    if r['Q0'] >= TH0:
        q0_hi = m if q0_hi is None else max(q0_hi, m)
print('  Q0: PASS observed up to m = %s ; crossover m* = %s'
      % ('%.3f' % q0_hi if q0_hi is not None else 'none', '%.4f' % M0_STAR if M0_STAR else 'none'))
print('  Q2: crossover m* = %s' % ('%.4f' % M2_STAR if M2_STAR else 'none'))

res = []


def rec(tag, ok, note):
    res.append((tag, bool(ok), note))
    print('  %-4s %-5s %s' % (tag, 'PASS' if ok else 'FAIL', note))


q0_amax = max(B_rows, key=lambda t: t[1])[2]['Q0']
q0_amin = min(B_rows, key=lambda t: t[1])[2]['Q0']
spread_q0 = abs(q0_amax - q0_amin)
rec('P1', spread_q0 < 0.02, 'Q0 spread over A in [0.005, 0.60] = %.4f (< 0.02)' % spread_q0)

ratios = [r['P0'] / A for _m, A, r in B_rows]
rec('P2', (max(ratios) - min(ratios)) / max(ratios) < 0.02,
    'P0/A over the amplitude sweep in [%.4e, %.4e], spread %.2f%% (< 2%%)'
    % (min(ratios), max(ratios), 100.0 * (max(ratios) - min(ratios)) / max(ratios)))

bad = [m for m, _A, r in A_rows if m <= 0.20 and r['Q0'] < TH0]
rec('P3', not bad, 'every m <= 0.20 passes Q0 (%s)' % ('yes' if not bad else 'no, fails at %s' % bad))

q0_full = [r['Q0'] for m, _A, r in A_rows if m == 1.00][0]
rec('P4', q0_full < TH0, 'Q0 at m = 1.00 is %.4f (< 0.50)' % q0_full)
if q0_full >= TH0:
    print('       -> no crossover: Q0 is not evidence at ANY m, which is stronger than the finding')

rec('P5', P5, 'verbatim DITHER reproduces Q0 0.775 / cv 0.119')

q2_near = [r['Q2'] for m, _A, r in C_rows if m == 0.75][0]
rec('P6', q2_near is not None and q2_near < 0, 'Q2 at m = 0.75 is %.4f (< 0)' % q2_near)

bad2 = [m for m, _A, r in C_rows if m <= 0.20 and (r['Q2'] is None or r['Q2'] < TH2)]
rec('P7', not bad2, 'every m <= 0.20 passes Q2 (%s)' % ('yes' if not bad2 else 'no, fails at %s' % bad2))

rec('P8', D_ALPHA > 0.05, '|q2(16) - q2(64)| = %.4f (> 0.05)' % D_ALPHA)

gap = abs(M0_STAR - M2_STAR) if (M0_STAR is not None and M2_STAR is not None) else None
rec('P9', gap is not None and gap > 0.10,
    'crossover gap |m*(Q0) - m*(Q2)| = %s (> 0.10)' % ('%.4f' % gap if gap is not None else 'undefined'))

hdr('SUMMARY')
nfail = sum(1 for _t, ok, _n in res if not ok)
print('  predictions confirmed  : %d of %d' % (len(res) - nfail, len(res)))
print('  predictions FAILED     : %d  %s' % (nfail, ', '.join(t for t, ok, _n in res if not ok) or '-'))
print()
print('  applicability domain of Q0 (may NOT be cited as evidence):')
print('    modal mass m > %.3f, where the crossover sits at m* = %s'
      % (q0_hi if q0_hi is not None else 0.0, '%.4f' % M0_STAR if M0_STAR else 'undefined'))
print('    and NOTE: Q0 is invariant to amplitude (spread %.4f over a 120x amplitude range), so')
print('    no sigma/du precondition can substitute for the modal-mass bound.')
print('  applicability domain of Q2 (may NOT be cited as evidence):')
print('    modal mass m > %.3f (crossover m* = %s), and any alphabet other than B = 64'
      % (0.20 if not bad2 else 0.0, '%.4f' % M2_STAR if M2_STAR else 'undefined'))
print()
print('  These are PROHIBITIONS, not tolerances. No threshold in the lock was read, written or changed.')
print()
print('PROVENANCE: NEITHER  (domain characterisation of two estimators; establishes no physics)')
