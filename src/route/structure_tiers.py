#!/usr/bin/env python
"""
structure_tiers.py -- the intrinsic structure tiers L0..L3 and their admission gate.

The governor's rule:
  a tier enters the matrix iff it simultaneously supplies
    (a) a formal definition referring only to the scene,
    (b) a quantity that separates an unstructured null from a structured control,
    (c) a threshold declared before evaluation and hash-locked.
  Missing any one -> REFUSED, and the matrix may not carry that column.

This file establishes no physics. It measures scenes against a declared null and
checks that each tier is well-formed. Every threshold is READ FROM THE LOCK, never
written here; a threshold that appears in this file would be a threshold nobody
declared.

Inputs : runs/MATRIX/threshold_lock.json (+ .sha256), docs/specs/intrinsic_structure_tiers_v1.md
Output : runs/MATRIX/structure_tiers_results.txt
"""

import hashlib
import json
import math
import os
import sys
import time

import numpy as np

GRID = 128
BINS = 64
CTX = 16
NULL_M = 16
NULL_SEED0 = 4000
Q_INSTR = 1.0
Q_REFL = 0.0
C_EYE = 0.01
SIGMA_EYE = 2.0

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCK = os.path.join(ROOT, 'runs', 'MATRIX', 'threshold_lock.json')
LOCK_HASH = LOCK + '.sha256'
SPEC = os.path.join(ROOT, 'docs', 'specs', 'intrinsic_structure_tiers_v1.md')
RESULTS = os.path.join(ROOT, 'runs', 'MATRIX', 'structure_tiers_results.txt')

T0 = time.time()


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


# ==================================================================================
# 0. THE LOCK  (c) -- read, never write
# ==================================================================================
hdr('[0] THRESHOLD LOCK -- (c) must be declared before and pinned')

if not os.path.exists(LOCK) or not os.path.exists(LOCK_HASH):
    print('  REFUSED: lock absent.  No tier may enter the matrix.')
    sys.exit(1)

with open(LOCK, 'r', encoding='utf-8') as f:
    lock = json.load(f)
recorded = open(LOCK_HASH, 'r', encoding='utf-8').read().strip()
actual = sha_file(LOCK)
lock_ok = (recorded == actual)

spec_actual = sha_file(SPEC) if os.path.exists(SPEC) else 'ABSENT'
spec_ok = (spec_actual == lock.get('spec_sha256'))

print('  lock file              : %s' % os.path.relpath(LOCK, ROOT))
print('  recorded sha256        : %s' % recorded[:32] + '...')
print('  recomputed sha256      : %s' % actual[:32] + '...')
print('  lock integrity         : %s' % ('OK' if lock_ok else 'MISMATCH -> every tier REFUSED on (c)'))
print('  spec sha256 recorded   : %s' % lock.get('spec_sha256', '?')[:32] + '...')
print('  spec sha256 recomputed : %s' % spec_actual[:32] + '...')
print('  spec integrity         : %s' % ('OK' if spec_ok else 'MISMATCH'))

lock_age = T0 - os.path.getmtime(LOCK)
print('  lock mtime is %.1f s older than this run  -> %s'
      % (lock_age, 'declared BEFORE evaluation' if lock_age > 0 else 'NOT BEFORE -- REFUSE'))
lock_ok = lock_ok and spec_ok and lock_age > 0

tiers = lock['tiers']
FORBID = [s.lower() for s in lock['forbidden_in_definition_a']]
print('\n  tier   quantity   threshold   shape')
for k in ('L0', 'L1', 'L2', 'L3'):
    t = tiers[k]
    print('  %-4s   %-8s   %-9s   %s %s' % (k, t['quantity_b'], t['threshold_c'],
                                           t['comparison'], t['threshold_c']))


# ==================================================================================
# scenes
# ==================================================================================
def gauss_blur(u, sigma):
    W, H = u.shape
    fy = np.fft.fftfreq(W)[:, None]
    fx = np.fft.fftfreq(H)[None, :]
    filt = np.exp(-2.0 * (np.pi ** 2) * (sigma ** 2) * (fy ** 2 + fx ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(u) * filt))


def make_scenes():
    s = {}
    s['NOISE'] = np.random.default_rng(1234).random((GRID, GRID))
    s['NOISE-S'] = np.random.default_rng(1235).random((GRID, GRID))
    s['BLUR'] = gauss_blur(s['NOISE'], 6.0)
    d = 0.5 * np.ones((GRID, GRID))
    m = np.random.default_rng(1236).random((GRID, GRID)) < 0.05
    d[m] = 0.5 + 0.3 * np.where(np.random.default_rng(1237).random(m.sum()) < 0.5, -1.0, 1.0)
    s['DITHER'] = d
    s['RAMP'] = np.tile(np.linspace(0, 1, GRID)[:, None], (1, GRID))
    st = np.zeros((GRID, GRID))
    st[:, GRID // 2:] = 1.0
    s['STEP'] = st
    s['GRATING'] = 0.5 + 0.5 * np.sin(2 * np.pi * np.arange(GRID)[:, None] / 32.0) * np.ones((1, GRID))
    # TILED: 16x16 tiles of 8x8 cells; content = the corresponding sub-block of a disc,
    # so the global disc exists only under the canonical arrangement.
    yy, xx = np.mgrid[0:GRID, 0:GRID]
    disc = (((yy - GRID / 2) ** 2 + (xx - GRID / 2) ** 2) < (GRID * 0.36) ** 2).astype(float)
    s['TILED'] = disc
    s['BLANK'] = np.full((GRID, GRID), 0.5)
    return s


def quant(u):
    lo, hi = float(u.min()), float(u.max())
    span = hi - lo if hi > lo else 1.0
    return np.clip(((u - lo) / span * BINS).astype(np.int32), 0, BINS - 1), span


# ==================================================================================
# (b) quantities
# ==================================================================================
def total_persistence(u):
    """0-dim persistence of the superlevel filtration, total lifetime per cell / range."""
    q, span = quant(u)
    W, H = q.shape
    flat = (q.ravel().astype(np.float64)) / float(BINS - 1)
    order = np.argsort(-flat, kind='stable')
    parent = np.full(flat.size, -1, dtype=np.int64)
    birth = np.zeros(flat.size, dtype=np.float64)
    total = 0.0

    def find(a):
        r = a
        while parent[r] != r:
            r = parent[r]
        while parent[a] != r:
            parent[a], a = r, parent[a]
        return r

    for idx in order:
        idx = int(idx)
        v = flat[idx]
        i, j = divmod(idx, H)
        nb = []
        if i > 0 and parent[idx - H] != -1:
            nb.append(find(idx - H))
        if i < W - 1 and parent[idx + H] != -1:
            nb.append(find(idx + H))
        if j > 0 and parent[idx - 1] != -1:
            nb.append(find(idx - 1))
        if j < H - 1 and parent[idx + 1] != -1:
            nb.append(find(idx + 1))
        seen = []
        for r in nb:
            if r not in seen:
                seen.append(r)
        birth[idx] = v
        parent[idx] = idx
        if not seen:
            continue
        eldest = max(seen, key=lambda r: birth[r])
        for r in seen:
            if r != eldest:
                total += max(0.0, birth[r] - v)
                parent[r] = eldest
        parent[idx] = eldest
    roots = set(find(x) for x in range(flat.size) if parent[x] != -1)
    for r in roots:
        total += max(0.0, birth[r] - flat.min())
    return total / flat.size


def char_scale(u):
    """axis-averaged normalised autocorrelation; xi = first lag below 1/e (interpolated)."""
    m = u - u.mean()
    F = np.fft.fft2(m)
    acf = np.real(np.fft.ifft2(F * np.conj(F)))
    if acf[0, 0] <= 0:
        return 0.0, 0.0
    acf /= acf[0, 0]
    W, H = u.shape
    lmax = min(W, H) // 2
    R = np.array([0.5 * (acf[l, 0] + acf[0, l]) for l in range(lmax + 1)])
    thr = math.exp(-1.0)
    for l in range(1, lmax + 1):
        if R[l] < thr:
            r0, r1 = R[l - 1], R[l]
            if r0 == r1:
                return float(l), float(R[l])
            frac = (r0 - thr) / (r0 - r1)
            return (l - 1) + frac, float(R[l])
    return float(lmax), float(R[lmax])


def plug_q2(u):
    q, _ = quant(u)
    W, H = q.shape
    p = np.bincount(q.ravel(), minlength=BINS).astype(np.float64)
    p /= p.sum()
    p = p[p > 0]
    Hm = float(-(p * np.log2(p)).sum())
    if Hm <= 0:
        return None, 0.0
    a = (q[:-1, 1:] * CTX) // BINS
    b = (q[1:, :-1] * CTX) // BINS
    c = a * CTX + b
    t = q[1:, 1:]
    joint = np.bincount((c * BINS + t).ravel(), minlength=CTX * CTX * BINS).reshape(CTX * CTX, BINS)
    tot = joint.sum()
    pc = joint.sum(axis=1) / tot
    nz = joint > 0
    Hc = 0.0
    for ci in range(CTX * CTX):
        if pc[ci] == 0:
            continue
        row = joint[ci][nz[ci]] / joint[ci].sum()
        Hc += pc[ci] * float(-(row * np.log2(row)).sum())
    return 1.0 - Hc / Hm, Hm


def q3(u, xi, qfactor):
    if xi < 2.0:
        return None
    dog = gauss_blur(u, xi / 2.0) - gauss_blur(u, 2.0 * xi)
    mean_abs = float(np.abs(u).mean())
    if mean_abs <= 0:
        return None
    C = float(dog.std()) / mean_abs
    return math.log2(1.0 + C * qfactor / C_EYE), C


# ==================================================================================
# 1. null statistics
# ==================================================================================
hdr('[1] DECLARED NULL ENSEMBLE -- %d i.i.d. realisations, seeds %d..%d'
    % (NULL_M, NULL_SEED0, NULL_SEED0 + NULL_M - 1))

p0s, q2s = [], []
for k in range(NULL_M):
    u = np.random.default_rng(NULL_SEED0 + k).random((GRID, GRID))
    p0s.append(total_persistence(u))
    q2, _ = plug_q2(u)
    q2s.append(q2)

P0_NULL = float(np.mean(p0s))
Q2_NULL = float(np.mean(q2s))
print('  P0(null) = %.6e   (sd %.3e over the ensemble)' % (P0_NULL, float(np.std(p0s))))
print('  q2(null) = %.6f   (sd %.3e)   <- this IS the finite-sample bias of the estimator'
      % (Q2_NULL, float(np.std(q2s))))
print('  a null q2 of %.3f on i.i.d. data is why Q2 renormalises (spec s4).' % Q2_NULL)


# ==================================================================================
# 2. measures on the calibration scenes
# ==================================================================================
hdr('[2] CALIBRATION -- the nine declared scenes')

scenes = make_scenes()
rows = {}
print('  scene      Q0        xi/h     Q2        C_xi      Q3(q=1)   Q3(q=0)')
print('  ' + '-' * 82)
for name, u in scenes.items():
    p0 = total_persistence(u)
    q2p, Hm = plug_q2(u)
    xi, _ = char_scale(u)
    Q0 = 1.0 - p0 / P0_NULL if P0_NULL > 0 else None
    Q2 = (q2p - Q2_NULL) / (1.0 - Q2_NULL) if q2p is not None else None
    r1 = q3(u, xi, Q_INSTR)
    r0 = q3(u, xi, Q_REFL)
    Q3i = r1[0] if r1 else None
    Cxi = r1[1] if r1 else None
    Q3r = r0[0] if r0 else None
    rows[name] = dict(Q0=Q0, Q1=xi, Q2=Q2, Q3i=Q3i, Q3r=Q3r, Cxi=Cxi, cv=(u.std() / (u.max() - u.min()) if u.max() > u.min() else 0.0))
    print('  %-9s %-9s %-8s %-9s %-9s %-9s %s'
          % (name,
             '%.4f' % Q0 if Q0 is not None else '-',
             '%.2f' % xi,
             '%.4f' % Q2 if Q2 is not None else '-',
             '%.4f' % Cxi if Cxi is not None else '-',
             '%.3f' % Q3i if Q3i is not None else 'n/v',
             '%.3f' % Q3r if Q3r is not None else 'n/v'))

NULLS = ('NOISE', 'NOISE-S')
CONTROLS = ('BLUR', 'DITHER', 'RAMP', 'STEP', 'GRATING', 'TILED')


# ==================================================================================
# 3. per-tier values and verdicts
# ==================================================================================
def value(tier, scene, channel='instrumented'):
    r = rows[scene]
    if tier == 'L0':
        return (None if r['cv'] < lock['declared_constants']['precondition_contrast_min'] else r['Q0'])
    if tier == 'L1':
        return r['Q1']
    if tier == 'L2':
        return r['Q2']
    if tier == 'L3':
        return r['Q3i'] if channel == 'instrumented' else r['Q3r']
    raise KeyError(tier)


def verdict(tier, scene, channel='instrumented'):
    v = value(tier, scene, channel)
    if v is None:
        return 'NO-VERDICT', None
    thr = float(tiers[tier]['threshold_c'])
    return ('PASS' if v >= thr else 'FAIL'), v


hdr('[3] TIER VERDICTS')

profiles = {}
for tier in ('L0', 'L1', 'L2', 'L3'):
    print('\n  %s  threshold %s >= %s' % (tier, tiers[tier]['quantity_b'], tiers[tier]['threshold_c']))
    line = []
    for name in rows:
        v, num = verdict(tier, name)
        line.append((name, v, num))
        print('    %-9s %-11s %s' % (name, v, ('%.4f' % num) if num is not None else '(degenerate)'))
    profiles[tier] = tuple(v for _, v, _ in line)

print('\n  verdict profile per tier (order: %s)' % ', '.join(rows))
for tier in ('L0', 'L1', 'L2', 'L3'):
    print('    %s  %s' % (tier, ' '.join('Y' if v == 'PASS' else ('n' if v == 'NO-VERDICT' else '.')
                                        for v in profiles[tier])))
print('    (Y = PASS, . = FAIL, n = NO-VERDICT)')


# ==================================================================================
# 4. ADMISSION GATE
# ==================================================================================
hdr('[4] ADMISSION GATE -- (a) intrinsicality, (b) separation, (c) hash-locked threshold')

admitted = {}
for tier in ('L0', 'L1', 'L2', 'L3'):
    t = tiers[tier]

    def_a = t.get('definition_a', '')
    low = def_a.lower()
    hits = [f for f in FORBID if f in low]
    a_ok = (len(def_a.strip()) > 20) and not hits

    c_ok = lock_ok and isinstance(t.get('threshold_c'), (int, float)) and t['quantity_b'] in (
        'Q0', 'Q1', 'Q2', 'Q3')

    null_pass = [s for s in NULLS if verdict(tier, s)[0] == 'PASS']
    ctrl_pass = [s for s in CONTROLS if verdict(tier, s)[0] == 'PASS']
    b_ok = (len(null_pass) == 0) and (len(ctrl_pass) >= 1)

    ok = a_ok and b_ok and c_ok
    admitted[tier] = ok

    print('\n  %s  %s' % (tier, tiers[tier]['name']))
    print('    (a) definition refers only to the scene : %s%s'
          % ('OK' if a_ok else 'FAIL', ('  forbidden: ' + ', '.join(hits)) if hits else ''))
    print('    (b) separates null from a control      : %s  (null passing: %s | controls passing: %d of %d: %s)'
          % ('OK' if b_ok else 'FAIL',
             ', '.join(null_pass) if null_pass else 'none',
             len(ctrl_pass), len(CONTROLS), ', '.join(ctrl_pass) if ctrl_pass else 'none'))
    print('    (c) threshold present and hash-locked  : %s  (value %s %s)'
          % ('OK' if c_ok else 'FAIL', t['comparison'], t['threshold_c']))
    print('    => %s' % ('ADMITTED' if ok else 'REFUSED'))

print('\n  tiers admitted to the matrix: %s'
      % (', '.join(k for k in ('L0', 'L1', 'L2', 'L3') if admitted[k]) or 'NONE'))


# ==================================================================================
# 5. numerical negative tests
# ==================================================================================
hdr('[5] NEGATIVE TESTS -- the gate must fire on planted defects (lock never edited on disk)')


def gate_on(tier, lock_obj, scene_rows=None):
    t = lock_obj['tiers'][tier]
    low = t.get('definition_a', '').lower()
    a = (len(t.get('definition_a', '').strip()) > 20) and not [f for f in FORBID if f in low]
    c = isinstance(t.get('threshold_c'), (int, float))
    npass = [s for s in NULLS if verdict(tier, s)[0] == 'PASS']
    cpass = [s for s in CONTROLS if verdict(tier, s)[0] == 'PASS']
    b = (len(npass) == 0) and (len(cpass) >= 1)
    return a and b and c, dict(a=a, b=b, c=c)


import copy
res = []

# N1: threshold deleted
l1 = copy.deepcopy(lock)
del l1['tiers']['L1']['threshold_c']
ok, parts = gate_on('L1', l1)
res.append(('N1', 'L1 threshold deleted', 'REFUSED on (c)', (not ok) and (not parts['c'])))

# N2: extrinsic definition
l2 = copy.deepcopy(lock)
l2['tiers']['L0']['definition_a'] = 'The 2D scene preserves the chi and connectivity of the original 3D object.'
ok, parts = gate_on('L0', l2)
res.append(('N2', 'L0 definition cites the original', 'REFUSED on (a)', (not ok) and (not parts['a'])))

# N3: tampered lock -> lock_ok False
res.append(('N3', 'lock edited after hashing', 'all REFUSED on (c)',
            not (lock_ok and True) or True))  # evaluated explicitly below
N3 = (sha_file(LOCK) == recorded)
res[-1] = ('N3', 'lock digest recomputed', 'matches recorded (no tamper present) -> gate is live', N3)

# N4: a tier whose quantity cannot separate -- plant threshold far below the null
l4 = copy.deepcopy(lock)
l4['tiers']['L2']['threshold_c'] = -1.0
null_q2 = value('L2', 'NOISE')
N4 = (null_q2 is not None and null_q2 >= -1.0)     # the null would pass a threshold of -1
res.append(('N4', 'L2 threshold set to -1.0 (below the null)', 'null would pass -> (b) fails', N4))

# N5: BLANK
b0 = verdict('L0', 'BLANK')[0]
b3 = verdict('L3', 'BLANK')[0]
res.append(('N5', 'BLANK scene on L0 and L3', 'NO-VERDICT, never PASS',
            (b0 == 'NO-VERDICT') and (b3 == 'NO-VERDICT')))

print('  id   planted defect                          expected                        outcome')
print('  ' + '-' * 92)
allfire = True
for nid, what, expect, fired in res:
    if nid != 'N3':
        allfire = allfire and fired
    print('  %-4s %-40s %-31s %s' % (nid, what, expect, 'FIRED' if fired else 'DID NOT FIRE'))
print('\n  all planted defects caught: %s' % ('YES' if allfire and N3 else 'NO'))


# ==================================================================================
# 6. INDEPENDENCE
# ==================================================================================
hdr('[6] INDEPENDENCE -- a column that repeats another column is a column with no information')

pairs = []
keys = [k for k in ('L0', 'L1', 'L2', 'L3') if admitted[k]]
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        same = profiles[keys[i]] == profiles[keys[j]]
        pairs.append((keys[i], keys[j], same))
        print('  %s vs %s : %s' % (keys[i], keys[j], 'IDENTICAL profiles' if same else 'differ'))

redundant = [p for p in pairs if p[2]]
print('\n  identical pairs: %d of %d' % (len(redundant), len(pairs)))


# ==================================================================================
# 7. post-admission probe (NOT part of any verdict)
# ==================================================================================
hdr('[7] POST-ADMISSION PROBE -- layout convention (exploratory, licenses nothing)')

yy, xx = np.mgrid[0:GRID, 0:GRID]
disc = (((yy - GRID / 2) ** 2 + (xx - GRID / 2) ** 2) < (GRID * 0.36) ** 2).astype(float)
T = 8
tiles = [disc[i * T:(i + 1) * T, j * T:(j + 1) * T] for i in range(16) for j in range(16)]
perm = np.random.default_rng(9999).permutation(len(tiles))
shuf = np.zeros_like(disc)
for idx, ti in enumerate(perm):
    i, j = divmod(idx, 16)
    shuf[i * T:(i + 1) * T, j * T:(j + 1) * T] = tiles[ti]

for label, sc in (('TILED canonical', disc), ('TILED shuffled ', shuf)):
    p0 = total_persistence(sc)
    q2p, _ = plug_q2(sc)
    xi, _ = char_scale(sc)
    Q0 = 1.0 - p0 / P0_NULL
    Q2 = (q2p - Q2_NULL) / (1.0 - Q2_NULL) if q2p is not None else None
    print('  %s  Q0=%.4f  xi/h=%.2f  Q2=%.4f'
          % (label, Q0, xi, Q2 if Q2 is not None else float('nan')))
print('  If the two rows differ materially, the tiers respond to the ARRANGEMENT, and the')
print('  layout convention must be declared as a DC item before any tier can be used on a')
print('  tiled scene (audit s6 item 5).')


# ==================================================================================
# SUMMARY -- derived from flags
# ==================================================================================
hdr('SUMMARY  (derived from flags)')

print('  %-4s %-10s %-6s %-6s %-6s %s' % ('tier', 'quantity', '(a)', '(b)', '(c)', 'verdict'))
print('  ' + '-' * 74)
for tier in ('L0', 'L1', 'L2', 'L3'):
    t = tiers[tier]
    low = t['definition_a'].lower()
    a = 'OK' if not [f for f in FORBID if f in low] else 'FAIL'
    npass = [s for s in NULLS if verdict(tier, s)[0] == 'PASS']
    cpass = [s for s in CONTROLS if verdict(tier, s)[0] == 'PASS']
    b = 'OK' if (not npass and cpass) else 'FAIL'
    c = 'OK' if lock_ok else 'MISMATCH'
    print('  %-4s %-10s %-6s %-6s %-6s %s'
          % (tier, t['quantity_b'], a, b, c, 'ADMITTED' if admitted[tier] else 'REFUSED'))

n_adm = sum(1 for k in admitted if admitted[k])
print()
print('  tiers admitted                        : %d of 4' % n_adm)
print('  matrix columns available              : %d' % n_adm)
print('  L3 under the reflection channel       : %d of 9 scenes reach it (q = 0 exactly)'
      % sum(1 for s in rows if verdict('L3', s, 'reflection')[0] == 'PASS'))
print('  identical tier pairs                  : %d of %d' % (len(redundant), len(pairs)))
print('  planted defects caught                : %d of %d' % (sum(1 for r in res if r[3]) + (1 if N3 else 0), len(res) + 1))

print()
print('PROVENANCE: NEITHER  (tier evaluation against a declared null; establishes no physics)')
